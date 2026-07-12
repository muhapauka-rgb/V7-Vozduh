#!/usr/bin/env python3
"""Safe source-to-production sync helpers for V7.

The helpers in this module are fail-closed by design. They reuse
``tools/v7-truth-check`` for source-of-truth decisions and only model deployment
of explicitly approved binaries.
"""

from __future__ import annotations

import argparse
import ast
import base64
import hashlib
import importlib.machinery
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Optional


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs" / "track7" / "runtime-convergence" / "V7_TRUTH_MANIFEST.json"
TRUTH_CHECK_PATH = ROOT / "tools" / "v7-truth-check"
CPS_PATH = ROOT / "docs" / "programs" / "V7_CURRENT_PROGRAM_STATE.md"
OMP_PATH = ROOT / "docs" / "programs" / "OPERATIONAL_MATURITY_PROGRAM.md"
CANONICAL_BRANCH = "Updatesystem"
REMOTE_NAME = "origin"
DEPLOY_CONFIRMATION = "DEPLOY_V7_APPROVED"
RELEASE_SYNC_CONFIRMATION = "RELEASE_SYNC_APPROVED"

NORMALIZED_CPS_LIVE_STATE = {
    "active_program": "OMP",
    "current_mode": "BOUNDED_DELEGATED_AUTONOMY_ACTIVE",
    "current_stop_condition": "REAL_WORLD_LIMIT",
    "current_active_scope": "LEARNING_REPRESENTATIVE_OUTCOME_EVIDENCE",
    "current_safe_next_action": "WAIT FOR REPRESENTATIVE REAL GOVERNED OUTCOMES; RECHECK CAP-U07 ONLY AFTER OWNER-BACKED EVIDENCE CHANGE",
    "current_scope_class": "REAL_WORLD_EVIDENCE_BOUNDARY",
    "current_execution_mission_id": "NONE",
    "current_execution_mission_state": "NONE",
    "latest_terminal_mission_id": "V7_OMP_CAP_U07_LEARNING_OUTCOME_CONSUMPTION_V1",
    "latest_terminal_run_nonce": "V7_CAP_U07_LEARNING_V1_5070685E53FE",
    "latest_terminal_mission_state": "CAP_U07_LEARNING_OUTCOME_CONSUMED_REAL_WORLD_LIMIT",
    "latest_terminal_mission_report": "docs/reports/engineering/2026-07-12_200149_cap_u07_learning_outcome_consumption.md",
    "latest_terminal_mission_started_at": "2026-07-12T20:01:49+0700",
    "previous_terminal_mission_id": "V7_OMP_DEPENDENCY_GRAPH_AND_COMPLETION_ORDER_PROTECTION_V1",
    "previous_terminal_mission_report": "docs/reports/engineering/2026-07-12_193308_dependency_graph_completion_order_protection.md",
    "authoritative_transition_input_mission_id": "V7_OMP_BINDING_ATOMIC_SNAPSHOT_AND_MISSION_IDENTITY_GUARD_V3",
    "authoritative_transition_input_state": "MISSION_IDENTITY_GUARD_AND_BINDING_STABILITY_CERTIFIED",
    "authoritative_transition_input_report": "docs/reports/engineering/2026-07-11_225321_operation_scoped_binding_atomic_snapshot_closure_v3.md",
    "current_mission_role": "LATEST_TERMINAL_MISSION",
    "current_mission_id": "V7_OMP_CAP_U07_LEARNING_OUTCOME_CONSUMPTION_V1",
    "current_run_nonce": "V7_CAP_U07_LEARNING_V1_5070685E53FE",
    "current_mission_state": "CAP_U07_LEARNING_OUTCOME_CONSUMED_REAL_WORLD_LIMIT",
    "current_mission_report": "docs/reports/engineering/2026-07-12_200149_cap_u07_learning_outcome_consumption.md",
    "state_captured": "2026-07-12T20:01:49+0700",
    "current_state_generation": "cpsgen_V7_CAP_U07_LEARNING_V1_5070685E53FE",
    "current_transition_id": "CAP_U07_LEARNING_OUTCOME_CONSUMPTION_V1",
    "current_next_action_id": "WAIT_FOR_REPRESENTATIVE_REAL_LEARNING_OUTCOMES",
    "binding_stability": "PASS",
    "binding_schema": "v7.operation-scoped-source-binding.v2",
    "routing_readiness_state": "PASS_CANDIDATE_SCOPED",
    "authority_required_now": "NO_INSIDE_APPROVED_POLICY",
    "current_action_class": "single-user governed candidate failover",
    "current_action_class_state": "GOVERNED_ONLY",
    "old_packets_reusable": "NO",
    "active_wip": "CAP-U07-LEARNING",
    "active_capability_id": "CAP-U07",
    "active_capability_status": "WAITING_EXTERNAL_DEPENDENCY",
    "active_capability_progress": "PARTIAL_REAL_OUTCOME_CONSUMED; exact U01 SUCCESS produced HIGH learning but representative real outcome evidence remains insufficient",
    "dependency_graph_version": "v7.omp-capability-dependency-graph.v1",
    "current_execution_frontier": "NONE",
    "waiting_capabilities": "CAP-U02,CAP-U05,CAP-U06,CAP-U07",
    "ready_capabilities": "NONE",
    "blocked_capabilities": "CAP-U03,CAP-U04,CAP-U08,CAP-U09,CAP-U10,CAP-U11,CAP-U12,CAP-U13,CAP-U14,CAP-U15,CAP-U16,CAP-U17,CAP-U18,CAP-U19,CAP-U20,CAP-U21,CAP-U22",
    "continuation_decision": "PROGRAM_TERMINAL_REAL_WORLD_LIMIT",
    "next_executable_capability": "NONE",
    "program_terminal_state": "REAL_WORLD_LIMIT_READY_FRONTIER_EMPTY",
    "cap_u01_completion_report": "docs/reports/engineering/2026-07-12_172534_exact_route_repair_and_first_governed_success.md",
    "responsibility_class": "LEARNING",
    "last_responsible_link": "real governed U01 outcome -> existing feedback/learning consumer -> future recommendation evidence",
    "smallest_existing_next_action": "WAIT_FOR_REPRESENTATIVE_REAL_LEARNING_OUTCOMES; preserve exact U01 Learning evidence and recheck only after a new material outcome",
    "current_class_outcome": "SUCCESS",
    "current_class_delta_closed": "YES",
    "current_class_outcome_evidence": "SUCCESS; 10.7.0.5 awg0 -> vless; global route verification PASS; feedback execfb_b287532347352c661799e985",
    "verification_result": "PASS; exact U01 outcome, prediction, trust, recommendation, learning and closure records agree",
    "rollback_result": "NOT_REQUIRED; governance-only change with no Runtime apply or user movement",
    "learning_result": "LEARNING_UPDATED_PARTIAL; feedback execfb_b287532347352c661799e985 -> learn_5070685e53fe93acdda4ce8a, HIGH, real and non-synthetic",
    "action_class_non_consumption_root_cause": "CLOSED; exact route integrity repaired and successful verified current-class outcome accepted",
    "action_class_promotion_evaluation": "NOT_REQUESTED; current action class remains GOVERNED_ONLY and no authority expansion is proposed",
    "action_class_exact_missing_delta": "NONE_FOR_CAP_U01; exact repair, global route verification and fresh governed SUCCESS are certified",
    "class_approval_ready": "NO_EXPANSION_REQUESTED; current class remains GOVERNED_ONLY at the CAP-U02 real-world evidence boundary",
    "conditional_engineering_authority_used": "NO; successful outcome was completed inside existing bounded delegated policy",
    "certification_transaction_executed": "YES; exactly one fresh delegated transaction after exact route repair; mutation 1, verification PASS, rollback NOT_REQUIRED",
    "controlled_run_engineering_intent_closure": "INTENT_CLOSED; CAP-U01 certified from exact repair through governed SUCCESS, verification, learning and final OPEN",
    "production_maturity_decision": "PARTIAL_ACCEPT; CAP-U01 COMPLETE, CAP-U02 PARTIAL_REVALIDATED_FROM_REAL_SUCCESS, current action class remains GOVERNED_ONLY",
    "production_runtime_impact": "NONE; OMP/CPS continuation and validation semantics only",
    "routing_impact": "10.7.0.5, 10.7.0.32 and 10.7.0.38 use vless/tun0 with verified policy routes",
    "user_movement": "NO; current Mission performed evidence refresh and read-only revalidation only",
    "admin_safe_mode_live_state": "schema=v7.autonomous-execution-control.v2; state=OPEN; generation=aec_dda6c420c87e99e97236883c; reason=GOVERNED_TRANSACTION_COMPLETED",
    "parent_engineering_intent": "INTENT_NOT_CLOSED; CAP-U07 consumed one real success but representative Learning evidence remains a real-world dependency",
    "source_summary": "CAP-U07 reused the exact U01 Learning chain; no duplicate evidence was written and the recalculated READY frontier is empty.",
    "automatic_continue_omp_result": "PROGRAM_TERMINAL_REAL_WORLD_LIMIT; CAP-U02/U05/U06/U07 are WAITING and no independent READY capability remains",
    "required_workflow": "wait for new material governed outcomes -> revalidate representative Learning and B13 consumption -> recalculate dependency graph",
    "omp_controlled_run_allowed": "NO_CURRENT_EXECUTION; synthetic or forced outcomes are forbidden",
    "controlled_run_authority_required_now": "NO_INSIDE_APPROVED_POLICY",
    "controlled_run_execution_authorized": "NO_CURRENT_PACKET; no forced evidence generation or movement is authorized",
    "wip_authority_required_now": "FALSE; current boundary is representative real evidence, not Authority",
    "sequence_execution_class": "real-world evidence wait",
    "sequence_expected_output": "new representative governed outcomes -> Learning/B13 owner consumption -> dependency frontier recalculation",
    "completion_condition": "Learning closes only after dependencies, Engineering Intent, consumer verification, evidence consumption and CPS propagation pass",
    "capabilities_inventoried": "34",
    "complete_or_locked_capabilities": "13",
    "unfinished_capabilities": "21",
    "open_engineering_intents": "21",
    "omp_continuation_required": "FALSE",
    "external_input_required": "TRUE",
    "external_input_type": "REAL_WORLD_LIMIT",
    "transaction_terminal_class": "LEARNING_OUTCOME_CONSUMED_PARTIAL",
    "program_terminal_class": "REAL_WORLD_LIMIT",
    "next_mission_formed": "TRUE",
    "next_mission_id": "V7_OMP_CAP_U07_LEARNING_OUTCOME_RECHECK_V2",
    "premature_operator_return": "FALSE",
    "continuation_iteration": "7",
    "continuation_stop_reason": "REPRESENTATIVE_REAL_LEARNING_OUTCOMES_ABSENT_AND_READY_FRONTIER_EMPTY",
    "no_progress_fingerprint": "1b4bb8ba0f73324015ab844bec96d32aa38e545ba85b5d3db6e0857201cc7921",
}


def normalized_cps_live_state(overrides: Optional[dict[str, str]] = None) -> dict[str, str]:
    state = dict(NORMALIZED_CPS_LIVE_STATE)
    state.update(overrides or {})
    return state


def _markdown_section(text: str, start: str, end: str = "") -> str:
    start_at = text.find(start)
    if start_at < 0:
        return ""
    end_at = text.find(end, start_at + len(start)) if end else -1
    return text[start_at:end_at if end_at >= 0 else len(text)]


def _markdown_field_table(section: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        key = cells[0].strip("`")
        if not key or key in {"Field", "---"} or set(key) == {"-"}:
            continue
        fields[key] = cells[1].strip()
    return fields


def _classified_markdown_blocks(text: str) -> list[dict[str, Any]]:
    """Return H2/H3 blocks with explicit state-surface classification metadata."""
    headings = list(re.finditer(r"(?m)^(#{2,3})\s+(.+?)\s*$", text))
    blocks: list[dict[str, Any]] = []
    for index, match in enumerate(headings):
        level = len(match.group(1))
        end = len(text)
        for later in headings[index + 1:]:
            if len(later.group(1)) <= level:
                end = later.start()
                break
        body = text[match.end():end]
        classification_match = re.search(
            r"(?mi)^Classification:\s*`(PERMANENT_RULE|CURRENT_PROGRAM_STATE_REFERENCE|HISTORICAL_SNAPSHOT|HISTORICAL_MILESTONE|HISTORICAL_EXAMPLE|DEPRECATED_CURRENT_STATE)`\.?",
            body[:1200],
        )
        blocks.append({
            "start": match.start(),
            "end": end,
            "heading": match.group(2),
            "level": level,
            "body": body,
            "classification": classification_match.group(1) if classification_match else "",
        })
    return blocks


def omp_live_state_consistency(cps_text: str, omp_text: str) -> dict[str, Any]:
    """Fail closed when OMP exposes volatile or historical state outside the CPS pointer."""
    live = _markdown_field_table(_markdown_section(
        cps_text,
        "## 0. Authoritative Live Current State",
        "## Authoritative Unfinished Capability Closure Registry",
    ))
    cps_stop = live.get("CURRENT_STOP_CONDITION", "").strip("`")
    cps_next_action = live.get("CURRENT_NEXT_ACTION_ID", "").strip("`")
    cps_report = live.get("CURRENT_MISSION_REPORT", "").strip("`")
    blocks = _classified_markdown_blocks(omp_text)
    contradictions: list[str] = []
    historical_leaks: list[str] = []
    unqualified: list[str] = []
    stale_identities: list[str] = []

    historical_classes = {"HISTORICAL_SNAPSHOT", "HISTORICAL_MILESTONE", "HISTORICAL_EXAMPLE"}
    for block in blocks:
        classification = block["classification"]
        body = block["body"]
        identity = re.sub(r"[^a-z0-9]+", "_", block["heading"].lower()).strip("_")
        if classification in historical_classes:
            required = (
                "Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`",
                "Scheduling Authority: `NONE`",
                "Execution Authority: `NONE`",
            )
            for marker in required:
                if marker not in body:
                    historical_leaks.append(f"historical_metadata_missing:{identity}:{marker.split(':', 1)[0]}")
            if re.search(r"(?mi)^Scheduling Authority:\s*`(?!NONE`)", body):
                historical_leaks.append(f"historical_scheduling_authority_present:{identity}")
            if re.search(r"(?mi)^Execution Authority:\s*`(?!NONE`)", body):
                historical_leaks.append(f"historical_execution_authority_present:{identity}")
            if re.search(r"(?mi)^MISSION_ADMITTED\s*=\s*YES\s*$", body):
                historical_leaks.append(f"historical_mission_admission_present:{identity}")
            if re.search(r"(?mi)^(?:OLD_PACKETS_REUSABLE|PACKET_REUSE)\s*=\s*YES\s*$", body):
                historical_leaks.append(f"historical_packet_reuse_present:{identity}")

    def block_for(position: int) -> Optional[dict[str, Any]]:
        candidates = [block for block in blocks if block["start"] <= position < block["end"]]
        return max(candidates, key=lambda item: item["level"]) if candidates else None

    live_patterns = (
        r"(?mi)^Current blocker:\s*$",
        r"(?mi)^Current stop:\s*`?[^\n|]+",
        r"(?mi)^Current next action:\s*[^\n]+",
        r"(?mi)^CURRENT_STEP\s*=\s*[^\n]+",
        r"(?mi)^STOP_CONDITION\s*=\s*[^\n]+",
        r"(?mi)^NEXT_LEGAL_STEP\s*=\s*[^\n]+",
        r"(?mi)^AUTHORITY_REQUIRED_NOW\s*=\s*[^\n]+",
        r"(?mi)^PACKET_PREPARED\s*=\s*[^\n]+",
    )
    for pattern in live_patterns:
        for match in re.finditer(pattern, omp_text):
            block = block_for(match.start())
            classification = block["classification"] if block else ""
            if classification not in historical_classes | {"CURRENT_PROGRAM_STATE_REFERENCE", "PERMANENT_RULE"}:
                value = match.group(0).strip().replace("\n", " ")
                unqualified.append(f"unqualified:{match.start()}:{value[:96]}")

    for match in re.finditer(r"\b(?:pkt_preview|execlease|rbclear)_[a-zA-Z0-9]+\b", omp_text):
        block = block_for(match.start())
        classification = block["classification"] if block else ""
        if classification not in historical_classes:
            stale_identities.append(f"stale_identity:{match.group(0)}")

    section20 = _markdown_section(omp_text, "## 20. Stop Conditions", "## 21. Phase History")
    if "### 20.1 Historical Stop Conditions Snapshot" not in section20:
        contradictions.append("omp_section20_historical_snapshot_missing")
    if "### 20.2 Current Stop Reference" not in section20:
        contradictions.append("omp_section20_current_reference_missing")
    if "Historical blocker:\n\n`UNSAFE_IMPLEMENTATION`" not in section20:
        contradictions.append("omp_section20_historical_blocker_not_preserved")
    if "Scheduling Authority: `NONE`" not in section20:
        contradictions.append("omp_section20_historical_scheduling_authority_not_none")
    section20_pointer = _markdown_section(section20, "### 20.2 Current Stop Reference")
    section20_stop_match = re.search(r"(?m)^Resolved current stop:\s*`([^`]+)`", section20_pointer)
    section20_next_match = re.search(r"(?m)^Resolved current next action:\s*`([^`]+)`", section20_pointer)
    section20_pointer_ok = (
        "Classification: `CURRENT_PROGRAM_STATE_REFERENCE`" in section20_pointer
        and "Authoritative owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`" in section20_pointer
        and "Scheduling Authority: `CPS_ONLY`" in section20_pointer
        and "Execution Authority: `NONE`" in section20_pointer
        and bool(section20_stop_match and section20_stop_match.group(1) == cps_stop)
        and bool(section20_next_match and section20_next_match.group(1) == cps_next_action)
    )
    if not section20_pointer_ok:
        contradictions.append("omp_section20_current_pointer_mismatch")
    if section20_stop_match and section20_stop_match.group(1) != cps_stop:
        contradictions.append("omp_current_stop_divergence")
    if section20_next_match and section20_next_match.group(1) != cps_next_action:
        contradictions.append("omp_current_next_action_divergence")

    pointer = _markdown_section(omp_text, "## 26. Current Volatile State Pointer", "## 27. Permanent Production Command Verdict")
    pointer_classification = "CURRENT_PROGRAM_STATE_REFERENCE" if "Classification: `CURRENT_PROGRAM_STATE_REFERENCE`" in pointer else ""
    stop_match = re.search(r"(?m)^Resolved current stop:\s*`([^`]+)`", pointer)
    next_match = re.search(r"(?m)^Resolved current next action:\s*`([^`]+)`", pointer)
    report_match = re.search(r"(?m)^Latest consumed report:\s*`([^`]+)`", pointer)
    omp_stop = stop_match.group(1) if stop_match else ""
    omp_next_action = next_match.group(1) if next_match else ""
    omp_report = report_match.group(1) if report_match else ""
    pointer_ok = (
        pointer_classification == "CURRENT_PROGRAM_STATE_REFERENCE"
        and "Authoritative owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`" in pointer
        and "Scheduling Authority: `CPS_ONLY`" in pointer
        and "Execution Authority: `NONE`" in pointer
        and omp_stop == cps_stop
        and omp_next_action == cps_next_action
        and section20_pointer_ok
    )
    report_pointer_ok = bool(cps_report and omp_report == cps_report and cps_report in omp_text[:3000])
    if not pointer_ok:
        contradictions.append("omp_current_pointer_mismatch")
    if not report_pointer_ok:
        contradictions.append("omp_report_pointer_mismatch")
    if omp_stop and omp_stop != cps_stop:
        contradictions.append("omp_current_stop_divergence")
    if omp_next_action and omp_next_action != cps_next_action:
        contradictions.append("omp_current_next_action_divergence")

    contradiction_ids = sorted(set(contradictions + historical_leaks + unqualified + stale_identities))
    errors: list[str] = []
    if contradictions:
        errors.append("OMP_CURRENT_POINTER_MISMATCH")
    if unqualified:
        errors.append("OMP_UNQUALIFIED_CURRENT_STATE")
    if historical_leaks or stale_identities:
        errors.append("OMP_HISTORICAL_STATE_LEAK")
    if contradiction_ids:
        errors.append("OMP_LIVE_STATE_CONTRADICTION_STOP_SAFE")
    return {
        "schema": "v7-omp-live-state-consistency/v1",
        "final_verdict": "PASS" if not contradiction_ids else "NO-GO",
        "omp_live_state_consistency": "PASS" if not contradiction_ids else "FAIL",
        "omp_current_pointer_consistency": "PASS" if pointer_ok else "FAIL",
        "omp_unqualified_live_heading_count": len(set(unqualified)),
        "omp_historical_isolation": "PASS" if not historical_leaks and not stale_identities else "FAIL",
        "omp_current_stop": omp_stop,
        "cps_current_stop": cps_stop,
        "omp_next_action": omp_next_action,
        "cps_next_action": cps_next_action,
        "omp_stale_identity_count": len(set(stale_identities)),
        "omp_contradiction_count": len(contradiction_ids),
        "omp_contradiction_ids": contradiction_ids,
        "omp_report_pointer_consistency": "PASS" if report_pointer_ok else "FAIL",
        "omp_section20_classification": "HISTORICAL_SNAPSHOT" if "### 20.1 Historical Stop Conditions Snapshot" in section20 else "MISSING",
        "omp_section20_scheduling_authority": "NONE" if "Scheduling Authority: `NONE`" in section20 else "UNKNOWN",
        "errors": errors,
    }


def _cps_header_metadata(cps_text: str) -> dict[str, str]:
    header = cps_text.partition("## 0. Authoritative Live Current State")[0]
    values: dict[str, str] = {}
    for line in header.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip("`")
    return values


def _parse_iso_timestamp(value: str) -> datetime:
    if re.search(r"[+-]\d{4}$", value):
        value = value[:-5] + value[-5:-2] + ":" + value[-2:]
    return datetime.fromisoformat(value)


def mission_role_consistency(
    cps_text: str,
    *,
    root: Path = ROOT,
    omp_text: Optional[str] = None,
    verify_external: bool = True,
) -> dict[str, Any]:
    """Validate explicit current/latest/previous/transition Mission roles."""
    state = normalized_cps_live_state()
    header = _cps_header_metadata(cps_text)
    live = _markdown_field_table(_markdown_section(
        cps_text,
        "## 0. Authoritative Live Current State",
        "## Authoritative Unfinished Capability Closure Registry",
    ))
    registry = _markdown_field_table(_markdown_section(
        cps_text,
        "### Registry Metadata And Truth Lifecycle",
        "### Active Protected Work In Progress",
    ))
    wip = _markdown_field_table(_markdown_section(
        cps_text,
        "### Active Protected Work In Progress",
        "### Complete Or Locked Capability Records",
    ))
    contradictions: list[str] = []
    role_ambiguities: list[str] = []
    terminal_marked_active: list[str] = []

    def plain(value: str) -> str:
        return value.strip().strip("`")

    latest = state["latest_terminal_mission_id"]
    previous = state["previous_terminal_mission_id"]
    transition_input = state["authoritative_transition_input_mission_id"]

    header_checks = {
        "State captured": state["state_captured"],
        "Latest terminal Mission": latest,
        "Latest terminal Mission state": state["latest_terminal_mission_state"],
        "Latest terminal Mission report": state["latest_terminal_mission_report"],
        "Authoritative transition input Mission": transition_input,
    }
    for key, expected in header_checks.items():
        if header.get(key, "") != expected:
            contradictions.append(f"cps_header_mismatch:{key}")

    live_checks = {
        "CURRENT_EXECUTION_MISSION_ID": state["current_execution_mission_id"],
        "CURRENT_EXECUTION_MISSION_STATE": state["current_execution_mission_state"],
        "LATEST_TERMINAL_MISSION_ID": latest,
        "LATEST_TERMINAL_RUN_NONCE": state["latest_terminal_run_nonce"],
        "LATEST_TERMINAL_MISSION_STATE": state["latest_terminal_mission_state"],
        "LATEST_TERMINAL_MISSION_REPORT": state["latest_terminal_mission_report"],
        "LATEST_TERMINAL_MISSION_STARTED_AT": state["latest_terminal_mission_started_at"],
        "PREVIOUS_TERMINAL_MISSION_ID": previous,
        "AUTHORITATIVE_TRANSITION_INPUT_MISSION_ID": transition_input,
        "AUTHORITATIVE_TRANSITION_INPUT_STATE": state["authoritative_transition_input_state"],
        "AUTHORITATIVE_TRANSITION_INPUT_REPORT": state["authoritative_transition_input_report"],
        "CURRENT_MISSION_ROLE": state["current_mission_role"],
    }
    for key, expected in live_checks.items():
        if plain(live.get(key, "")) != expected:
            contradictions.append(f"cps_section0_mismatch:{key}")

    aliases = {
        "CURRENT_MISSION_ID": "LATEST_TERMINAL_MISSION_ID",
        "CURRENT_RUN_NONCE": "LATEST_TERMINAL_RUN_NONCE",
        "CURRENT_MISSION_STATE": "LATEST_TERMINAL_MISSION_STATE",
        "CURRENT_MISSION_REPORT": "LATEST_TERMINAL_MISSION_REPORT",
    }
    for alias, owner in aliases.items():
        if plain(live.get(alias, "")) != plain(live.get(owner, "")):
            role_ambiguities.append(f"mission_alias_divergence:{alias}:{owner}")

    registry_checks = {
        "ACTIVE_MISSIONS": "NONE",
        "LATEST_TERMINAL_MISSION_ID": latest,
        "LATEST_TERMINAL_MISSION_STATE": state["latest_terminal_mission_state"],
        "LATEST_TERMINAL_MISSION_REPORT": state["latest_terminal_mission_report"],
        "PREVIOUS_TERMINAL_MISSION_ID": previous,
        "AUTHORITATIVE_TRANSITION_INPUT_MISSION_ID": transition_input,
    }
    for key, expected in registry_checks.items():
        if plain(registry.get(key, "")) != expected:
            contradictions.append(f"cps_registry_mismatch:{key}")

    wip_checks = {
        "active_mission_id": "NONE",
        "active_mission_state": "NONE",
        "latest_terminal_mission_id": latest,
        "latest_terminal_mission_state": state["latest_terminal_mission_state"],
        "previous_terminal_mission_id": previous,
        "authoritative_transition_input_mission_id": transition_input,
    }
    for key, expected in wip_checks.items():
        if plain(wip.get(key, "")) != expected:
            contradictions.append(f"cps_active_wip_mismatch:{key}")

    active_execution = plain(live.get("CURRENT_EXECUTION_MISSION_ID", ""))
    active_wip_mission = plain(wip.get("active_mission_id", ""))
    if active_execution not in {"", "NONE"}:
        terminal_marked_active.append(f"current_execution_mission_not_none:{active_execution}")
    if active_wip_mission not in {"", "NONE"}:
        terminal_marked_active.append(f"active_wip_mission_not_none:{active_wip_mission}")
    if plain(registry.get("ACTIVE_MISSIONS", "")) == "NONE" and active_execution != "NONE":
        role_ambiguities.append("active_missions_none_with_current_execution_mission")
    if len({latest, previous, transition_input}) != 3:
        role_ambiguities.append("mission_roles_not_distinct")

    mission_report_pointer_consistency = "NOT_CHECKED"
    mission_nonce_consistency = "NOT_CHECKED"
    mission_timestamp_consistency = "NOT_CHECKED"
    anti_replay_consistency = "NOT_CHECKED"
    report_selector_consistency = "NOT_CHECKED"
    omp_transition_input_consistency = "NOT_CHECKED"
    if verify_external:
        report_path = root / state["latest_terminal_mission_report"]
        try:
            report_text = report_path.read_text(encoding="utf-8")
        except OSError:
            report_text = ""
        report_lines = report_text.splitlines()
        expected_id = f"Mission ID: `{latest}`"
        expected_nonce = f"Run Nonce: `{state['latest_terminal_run_nonce']}`"
        id_ok = len(report_lines) >= 1 and report_lines[0] == expected_id
        nonce_ok = len(report_lines) >= 2 and report_lines[1] == expected_nonce
        if not id_ok:
            contradictions.append("latest_terminal_report_mission_id_mismatch")
        if not nonce_ok:
            contradictions.append("latest_terminal_report_nonce_mismatch")
        mission_nonce_consistency = "PASS" if nonce_ok else "FAIL"
        report_selector_consistency = "PASS" if id_ok and nonce_ok else "FAIL"
        projected_latest = plain(live.get("LATEST_TERMINAL_MISSION_ID", ""))
        projected_previous = plain(live.get("PREVIOUS_TERMINAL_MISSION_ID", ""))
        projected_transition = plain(live.get("AUTHORITATIVE_TRANSITION_INPUT_MISSION_ID", ""))
        anti_replay_consistency = "PASS" if (
            id_ok
            and nonce_ok
            and projected_latest == latest
            and projected_latest not in {projected_previous, projected_transition}
        ) else "FAIL"
        if anti_replay_consistency == "FAIL":
            contradictions.append("anti_replay_selected_wrong_mission_role")

        try:
            captured = _parse_iso_timestamp(header.get("State captured", ""))
            started = _parse_iso_timestamp(plain(live.get("LATEST_TERMINAL_MISSION_STARTED_AT", "")))
            timestamp_ok = captured >= started
        except ValueError:
            timestamp_ok = False
        mission_timestamp_consistency = "PASS" if timestamp_ok else "FAIL"
        if not timestamp_ok:
            contradictions.append("mission_timestamp_predates_start")

        if omp_text is None:
            try:
                omp_text = OMP_PATH.read_text(encoding="utf-8")
            except OSError:
                omp_text = ""
        latest_pointer_ok = (
            state["latest_terminal_mission_report"] in omp_text[:5000]
            and state["latest_terminal_mission_state"] in omp_text[:5000]
            and f"Latest consumed report: `{state['latest_terminal_mission_report']}`" in omp_text
        )
        previous_pointer_ok = (
            state["previous_terminal_mission_report"] in omp_text[:5000]
            and f"Previous consumed report: `{state['previous_terminal_mission_report']}`" in omp_text
        )
        transition_pointer_ok = (
            state["authoritative_transition_input_report"] in omp_text[:5000]
            and transition_input in omp_text[:5000]
            and f"Authoritative transition input report: `{state['authoritative_transition_input_report']}`" in omp_text
        )
        mission_report_pointer_consistency = "PASS" if latest_pointer_ok and previous_pointer_ok else "FAIL"
        omp_transition_input_consistency = "PASS" if transition_pointer_ok else "FAIL"
        if mission_report_pointer_consistency == "FAIL":
            contradictions.append("omp_latest_or_previous_report_pointer_mismatch")
        if omp_transition_input_consistency == "FAIL":
            contradictions.append("omp_transition_input_pointer_mismatch")

    contradiction_ids = sorted(set(contradictions + role_ambiguities + terminal_marked_active))
    errors: list[str] = []
    if role_ambiguities:
        errors.append("MISSION_ROLE_AMBIGUITY_STOP_SAFE")
    if terminal_marked_active:
        errors.append("TERMINAL_MISSION_MARKED_ACTIVE_STOP_SAFE")
    if any("latest_terminal" in item or "header_mismatch:Latest terminal" in item for item in contradictions):
        errors.append("LATEST_TERMINAL_MISSION_MISMATCH")
    if any("transition_input" in item for item in contradictions):
        errors.append("TRANSITION_INPUT_ROLE_MISMATCH")
    if mission_report_pointer_consistency == "FAIL":
        errors.append("MISSION_REPORT_POINTER_MISMATCH")
    if mission_nonce_consistency == "FAIL":
        errors.append("MISSION_NONCE_MISMATCH")
    if mission_timestamp_consistency == "FAIL":
        errors.append("MISSION_TIMESTAMP_MISMATCH")
    if contradiction_ids:
        errors.append("CURRENT_STATE_CONSISTENCY_FAIL")

    return {
        "schema": "v7-mission-role-consistency/v1",
        "final_verdict": "PASS" if not contradiction_ids else "NO-GO",
        "mission_identity_consistency": "PASS" if not contradiction_ids else "FAIL",
        "current_execution_mission_consistency": "PASS" if not terminal_marked_active else "FAIL",
        "latest_terminal_mission_consistency": "PASS" if not any("latest_terminal" in item or "Latest terminal" in item for item in contradiction_ids) else "FAIL",
        "transition_input_mission_consistency": "PASS" if not any("transition_input" in item for item in contradiction_ids) else "FAIL",
        "previous_terminal_mission_consistency": "PASS" if not any("previous_terminal" in item for item in contradiction_ids) else "FAIL",
        "mission_role_ambiguity_count": len(set(role_ambiguities)),
        "terminal_mission_marked_active_count": len(set(terminal_marked_active)),
        "mission_report_pointer_consistency": mission_report_pointer_consistency,
        "mission_nonce_consistency": mission_nonce_consistency,
        "mission_timestamp_consistency": mission_timestamp_consistency,
        "mission_identity_contradiction_count": len(contradiction_ids),
        "mission_identity_contradiction_ids": contradiction_ids,
        "anti_replay_consistency": anti_replay_consistency,
        "report_selector_consistency": report_selector_consistency,
        "omp_transition_input_consistency": omp_transition_input_consistency,
        "cps_header_identity_consistency": "PASS" if not any(item.startswith("cps_header_mismatch") for item in contradiction_ids) else "FAIL",
        "cps_section0_identity_consistency": "PASS" if not any(item.startswith("cps_section0_mismatch") or item.startswith("mission_alias") for item in contradiction_ids) else "FAIL",
        "registry_identity_consistency": "PASS" if not any(item.startswith("cps_registry_mismatch") for item in contradiction_ids) else "FAIL",
        "active_wip_identity_consistency": "PASS" if not any(item.startswith("cps_active_wip_mismatch") for item in contradiction_ids) and not terminal_marked_active else "FAIL",
        "errors": sorted(set(errors)),
    }


def _replace_section_field(text: str, start: str, end: str, key: str, value: str) -> str:
    section = _markdown_section(text, start, end)
    if not section:
        raise ValueError(f"section_missing:{start}")
    prefix = f"| `{key}` |"
    matches = [line for line in section.splitlines() if line.startswith(prefix)]
    if len(matches) != 1:
        raise ValueError(f"field_missing_or_duplicate:{key}")
    updated = section.replace(matches[0], f"| `{key}` | {value} |", 1)
    return text.replace(section, updated, 1)


def build_normalized_cps_document(cps_text: str, state: Optional[dict[str, str]] = None) -> str:
    """Build all CPS live projections from one normalized terminal result."""
    state = normalized_cps_live_state(state)
    header_values = {
        "State captured": state["state_captured"],
        "Latest terminal Mission": f"`{state['latest_terminal_mission_id']}`",
        "Latest terminal Mission state": f"`{state['latest_terminal_mission_state']}`",
        "Latest terminal Mission report": f"`{state['latest_terminal_mission_report']}`",
        "Authoritative transition input Mission": f"`{state['authoritative_transition_input_mission_id']}`",
        "Source": state["source_summary"],
    }
    header, separator, remainder = cps_text.partition("## 0. Authoritative Live Current State")
    for key, value in header_values.items():
        pattern = rf"(?m)^{re.escape(key)}:.*$"
        replacement = f"{key}: {value}"
        if re.search(pattern, header):
            header = re.sub(pattern, replacement, header, count=1)
        else:
            header = header.rstrip() + f"\n{replacement}\n\n"
    cps_text = header + separator + remainder
    cps_text = re.sub(
        r"(?m)^Captured:\s*`[^`]+`$",
        f"Captured: `{state['state_captured']}`",
        cps_text,
        count=1,
    )
    cps_text = re.sub(
        r"(?m)^Generated At:\s*`[^`]+`$",
        f"Generated At: `{state['state_captured']}`",
        cps_text,
        count=1,
    )
    live_values = {
        "ACTIVE_PROGRAM": f"`{state['active_program']}`",
        "CURRENT_MODE": f"`{state['current_mode']}`",
        "CURRENT_STOP_CONDITION": f"`{state['current_stop_condition']}`",
        "CURRENT_ACTIVE_SCOPE": f"`{state['current_active_scope']}`",
        "CURRENT_SAFE_NEXT_ACTION": f"`{state['current_safe_next_action']}`",
        "CURRENT_SCOPE_CLASS": f"`{state['current_scope_class']}`",
        "CURRENT_STATE_GENERATION": f"`{state['current_state_generation']}`",
        "CURRENT_TRANSITION_ID": f"`{state['current_transition_id']}`",
        "CURRENT_NEXT_ACTION_ID": f"`{state['current_next_action_id']}`",
        "DEPENDENCY_GRAPH_VERSION": f"`{state['dependency_graph_version']}`",
        "CURRENT_EXECUTION_FRONTIER": f"`{state['current_execution_frontier']}`",
        "WAITING_CAPABILITIES": f"`{state['waiting_capabilities']}`",
        "READY_CAPABILITIES": f"`{state['ready_capabilities']}`",
        "BLOCKED_CAPABILITIES": f"`{state['blocked_capabilities']}`",
        "CONTINUATION_DECISION": f"`{state['continuation_decision']}`",
        "NEXT_EXECUTABLE_CAPABILITY": f"`{state['next_executable_capability']}`",
        "PROGRAM_TERMINAL_STATE": f"`{state['program_terminal_state']}`",
        "CURRENT_EXECUTION_MISSION_ID": f"`{state['current_execution_mission_id']}`",
        "CURRENT_EXECUTION_MISSION_STATE": f"`{state['current_execution_mission_state']}`",
        "LATEST_TERMINAL_MISSION_ID": f"`{state['latest_terminal_mission_id']}`",
        "LATEST_TERMINAL_RUN_NONCE": f"`{state['latest_terminal_run_nonce']}`",
        "LATEST_TERMINAL_MISSION_STATE": f"`{state['latest_terminal_mission_state']}`",
        "LATEST_TERMINAL_MISSION_REPORT": f"`{state['latest_terminal_mission_report']}`",
        "LATEST_TERMINAL_MISSION_STARTED_AT": f"`{state['latest_terminal_mission_started_at']}`",
        "PREVIOUS_TERMINAL_MISSION_ID": f"`{state['previous_terminal_mission_id']}`",
        "CURRENT_MISSION_ROLE": f"`{state['current_mission_role']}`",
        "CURRENT_MISSION_ID": f"`{state['current_mission_id']}`",
        "CURRENT_RUN_NONCE": f"`{state['current_run_nonce']}`",
        "CURRENT_MISSION_STATE": f"`{state['current_mission_state']}`",
        "CURRENT_MISSION_REPORT": f"`{state['current_mission_report']}`",
        "AUTHORITATIVE_TRANSITION_INPUT_MISSION_ID": f"`{state['authoritative_transition_input_mission_id']}`",
        "AUTHORITATIVE_TRANSITION_INPUT_STATE": f"`{state['authoritative_transition_input_state']}`",
        "AUTHORITATIVE_TRANSITION_INPUT_REPORT": f"`{state['authoritative_transition_input_report']}`",
        "BINDING_STABILITY": f"`{state['binding_stability']}; 22 post-deploy read-only cycles, 10 consecutive stable Candidate cycles, zero unexplained mismatches, zero mixed-generation snapshots`",
        "BINDING_SCHEMA": f"`{state['binding_schema']}; shared by preview, admission and low-level pre-mutation recheck`",
        "ROUTING_READINESS_STATE": f"`{state['routing_readiness_state']}; global inventory diagnostics are advisory_only and no longer cross-scope blockers`",
        "AUTHORITY_REQUIRED_NOW": f"`{state['authority_required_now']}; current boundary is real-world evidence, not authority`",
        "CURRENT_ACTION_CLASS": f"`{state['current_action_class']}`",
        "CURRENT_ACTION_CLASS_STATE": f"`{state['current_action_class_state']}`",
        "OLD_PACKETS_REUSABLE": f"`{state['old_packets_reusable']}`",
        "CURRENT_CLASS_CANDIDATE_SELECTED": "`NONE_OPEN`",
        "CURRENT_CLASS_OUTCOME": f"`{state['current_class_outcome']}`",
        "CURRENT_CLASS_DELTA_CLOSED": f"`{state['current_class_delta_closed']}`",
        "CURRENT_CLASS_OUTCOME_EVIDENCE": f"`{state['current_class_outcome_evidence']}`",
        "ACTION_CLASS_NON_CONSUMPTION_ROOT_CAUSE": f"`{state['action_class_non_consumption_root_cause']}`",
        "ACTION_CLASS_PROMOTION_EVALUATION": f"`{state['action_class_promotion_evaluation']}`",
        "ACTION_CLASS_EXACT_MISSING_DELTA": f"`{state['action_class_exact_missing_delta']}`",
        "CLASS_APPROVAL_READY": f"`{state['class_approval_ready']}`",
        "CONDITIONAL_ENGINEERING_AUTHORITY_USED": f"`{state['conditional_engineering_authority_used']}`",
        "CERTIFICATION_TRANSACTION_EXECUTED": f"`{state['certification_transaction_executed']}`",
        "VERIFICATION_RESULT": f"`{state['verification_result']}`",
        "ROLLBACK_RESULT": f"`{state['rollback_result']}`",
        "LEARNING_RESULT": f"`{state['learning_result']}`",
        "PRODUCTION_MATURITY_DECISION": f"`{state['production_maturity_decision']}`",
        "PARENT_ENGINEERING_INTENT": f"`{state['parent_engineering_intent']}`",
        "AUTOMATIC_CONTINUE_OMP_RESULT": f"`{state['automatic_continue_omp_result']}`",
        "REQUIRED_WORKFLOW": f"`{state['required_workflow']}`",
        "OMP_CONTROLLED_RUN_ALLOWED": f"`{state['omp_controlled_run_allowed']}`",
        "CONTROLLED_RUN_PRIMARY_STOP": f"`{state['current_stop_condition']}`",
        "CONTROLLED_RUN_RESPONSIBILITY_CLASS": f"`{state['responsibility_class']}`",
        "CONTROLLED_RUN_AUTHORITY_REQUIRED_NOW": f"`{state['controlled_run_authority_required_now']}`",
        "CONTROLLED_RUN_EXECUTION_AUTHORIZED": f"`{state['controlled_run_execution_authorized']}`",
        "CONTROLLED_RUN_AUTHORITY_CLASS": "`BOUNDED_DELEGATED_POLICY; expansion requires Engineering Authority`",
        "CONTROLLED_RUN_AUTHORITY_GENERATION": "`POLICY_SCOPED; NO_PACKET_SPECIFIC_AUTHORITY_REQUIRED`",
        "CONTROLLED_RUN_AUTHORITY_DECISION": "`APPROVED_BOUNDED_SCOPE; packet-specific Authority is not reusable or required`",
        "CONTROLLED_RUN_INVALIDATION_REASON": "`SUPERSEDED/HISTORICAL: SOURCE_SNAPSHOT_BUNDLE_DRIFT; gap closed by binding v2 certification`",
        "CONTROLLED_RUN_ENGINEERING_INTENT_CLOSURE": f"`{state['controlled_run_engineering_intent_closure']}`",
        "PRODUCTION_RUNTIME_IMPACT": f"`{state['production_runtime_impact']}`",
        "ROUTING_IMPACT": f"`{state['routing_impact']}`",
        "USER_MOVEMENT": f"`{state['user_movement']}`",
        "ADMIN_SAFE_MODE_LIVE_STATE": f"`{state['admin_safe_mode_live_state']}`",
        "OMP_CONTINUATION_REQUIRED": f"`{state['omp_continuation_required']}`",
        "EXTERNAL_INPUT_REQUIRED": f"`{state['external_input_required']}`",
        "EXTERNAL_INPUT_TYPE": f"`{state['external_input_type']}`",
        "TRANSACTION_TERMINAL_CLASS": f"`{state['transaction_terminal_class']}`",
        "PROGRAM_TERMINAL_CLASS": f"`{state['program_terminal_class']}`",
        "NEXT_MISSION_FORMED": f"`{state['next_mission_formed']}`",
        "NEXT_MISSION_ID": f"`{state['next_mission_id']}`",
        "PREMATURE_OPERATOR_RETURN": f"`{state['premature_operator_return']}`",
        "CONTINUATION_ITERATION": f"`{state['continuation_iteration']}`",
        "CONTINUATION_STOP_REASON": f"`{state['continuation_stop_reason']}`",
        "NO_PROGRESS_FINGERPRINT": f"`{state['no_progress_fingerprint']}`",
    }
    for key, value in live_values.items():
        cps_text = _replace_section_field(
            cps_text,
            "## 0. Authoritative Live Current State",
            "## Authoritative Unfinished Capability Closure Registry",
            key,
            value,
        )

    registry_values = {
        "CURRENT_STATE_GENERATION": f"`{state['current_state_generation']}`",
        "CURRENT_TRANSITION_ID": f"`{state['current_transition_id']}`",
        "EXACT_CURRENT_SMALLEST_NEXT_ACTION_ID": f"`{state['current_next_action_id']}`",
        "CURRENT_STOP_CONDITION": f"`{state['current_stop_condition']}`",
        "CAPABILITIES_INVENTORIED": f"`{state['capabilities_inventoried']}`",
        "COMPLETE_OR_LOCKED_CAPABILITIES": f"`{state['complete_or_locked_capabilities']}`",
        "UNFINISHED_CAPABILITIES": f"`{state['unfinished_capabilities']}`",
        "OPEN_ENGINEERING_INTENTS": f"`{state['open_engineering_intents']}`",
        "ACTIVE_MISSIONS": "`NONE`",
        "LATEST_TERMINAL_MISSION_ID": f"`{state['latest_terminal_mission_id']}`",
        "LATEST_TERMINAL_MISSION_STATE": f"`{state['latest_terminal_mission_state']}`",
        "LATEST_TERMINAL_MISSION_REPORT": f"`{state['latest_terminal_mission_report']}`",
        "PREVIOUS_TERMINAL_MISSION_ID": f"`{state['previous_terminal_mission_id']}`",
        "AUTHORITATIVE_TRANSITION_INPUT_MISSION_ID": f"`{state['authoritative_transition_input_mission_id']}`",
        "EXACT_CURRENT_SMALLEST_NEXT_ACTION": f"`{state['smallest_existing_next_action']}`",
    }
    for key, value in registry_values.items():
        cps_text = _replace_section_field(
            cps_text,
            "### Registry Metadata And Truth Lifecycle",
            "### Active Protected Work In Progress",
            key,
            value,
        )

    wip_values = {
        "capability_id": f"`{state['active_wip']}`",
        "current_state_generation": f"`{state['current_state_generation']}`",
        "current_transition_id": f"`{state['current_transition_id']}`",
        "smallest_existing_next_action_id": f"`{state['current_next_action_id']}`",
        "active_mission_id": "`NONE`",
        "active_mission_state": "`NONE`",
        "latest_terminal_mission_id": f"`{state['latest_terminal_mission_id']}`",
        "latest_terminal_mission_state": f"`{state['latest_terminal_mission_state']}`",
        "previous_terminal_mission_id": f"`{state['previous_terminal_mission_id']}`",
        "authoritative_transition_input_mission_id": f"`{state['authoritative_transition_input_mission_id']}`",
        "current_primary_stop": f"`{state['current_stop_condition']}`",
        "responsibility_class": f"`{state['responsibility_class']}`",
        "authority_required_now": f"`{state['wip_authority_required_now']}`",
        "last_responsible_link": state["last_responsible_link"],
        "smallest_existing_next_action": state["smallest_existing_next_action"],
        "binding_stability": "`CERTIFIED`",
        "completion_condition": state["completion_condition"],
    }
    for key, value in wip_values.items():
        cps_text = _replace_section_field(
            cps_text,
            "### Active Protected Work In Progress",
            "### Complete Or Locked Capability Records",
            key,
            value,
        )

    complete_section = _markdown_section(
        cps_text,
        "### Complete Or Locked Capability Records",
        "### Unfinished Capability Closure Records",
    )
    completed_u01_row = (
        "| `CAP-U01` | First Governed Controlled Run | Admin Safe Mode, execution packet/lease/pipeline, OMP | "
        "`COMPLETE` | `100.0` | `Capability Certified` | Exact two-user route repair, first successful governed outcome, "
        f"global verification, learning and final OPEN; `{state['cap_u01_completion_report']}` |"
    )
    complete_u01_rows = [line for line in complete_section.splitlines() if line.startswith("| `CAP-U01` |")]
    if len(complete_u01_rows) > 1:
        raise ValueError("complete_cap_u01_duplicate")
    if complete_u01_rows:
        cps_text = cps_text.replace(complete_u01_rows[0], completed_u01_row, 1)
    else:
        complete_rows = [line for line in complete_section.splitlines() if line.startswith("| `CAP-")]
        if not complete_rows:
            raise ValueError("complete_capability_rows_missing")
        cps_text = cps_text.replace(complete_rows[-1], complete_rows[-1] + "\n" + completed_u01_row, 1)

    cap_section = _markdown_section(
        cps_text,
        "### Unfinished Capability Closure Records",
        "### Open Engineering Intents And Last Responsible Links",
    )
    unfinished_u01_rows = [line for line in cap_section.splitlines() if line.startswith("| `CAP-U01` |")]
    if len(unfinished_u01_rows) > 1:
        raise ValueError("unfinished_cap_u01_duplicate")
    if unfinished_u01_rows:
        cps_text = cps_text.replace(unfinished_u01_rows[0] + "\n", "", 1)
        cap_section = _markdown_section(
            cps_text,
            "### Unfinished Capability Closure Records",
            "### Open Engineering Intents And Last Responsible Links",
        )

    active_capability_id = state["active_capability_id"]
    active_rows = [line for line in cap_section.splitlines() if line.startswith(f"| `{active_capability_id}` |")]
    if len(active_rows) != 1:
        raise ValueError("active_capability_missing_or_duplicate")
    active_row = (
        f"| `CAP-U07` | Learning | feedback/learning, OMP, Canonical Reference | `{state['active_capability_status']}` | "
        f"`{state['active_capability_progress']}` | {state['last_responsible_link']} | `{state['current_stop_condition']}` | "
        f"{state['smallest_existing_next_action']} | U01 complete; unblocks U04/U08/U09/U12/U17-U22 |"
    )
    cps_text = cps_text.replace(active_rows[0], active_row, 1)

    waiting_u02_rows = [line for line in cap_section.splitlines() if line.startswith("| `CAP-U02` |")]
    if len(waiting_u02_rows) != 1:
        raise ValueError("waiting_cap_u02_missing_or_duplicate")
    waiting_u02_row = (
        "| `CAP-U02` | Movement Protection | OMP, Movement Protection Model, Runtime Model | "
        "`WAITING_EXTERNAL_DEPENDENCY` | `PARTIAL_REVALIDATED_FROM_REAL_SUCCESS`; owner-backed evidence and "
        "no-progress fingerprint preserved | single-user governed success -> U03/U04/U05/U06 production-class "
        "evidence -> full Movement Protection certification | `REAL_WORLD_LIMIT` | "
        "WAIT_FOR_QUALIFYING_REAL_WORLD_MOVEMENT_EVIDENCE; no Candidate, packet, Authority request or forced mutation | "
        "U03/U04/U05/U06 completion; unblocks U09 |"
    )
    cps_text = cps_text.replace(waiting_u02_rows[0], waiting_u02_row, 1)

    intents_section = _markdown_section(
        cps_text,
        "### Open Engineering Intents And Last Responsible Links",
        "### Deterministic Execution Sequence",
    )
    closed_u01_intents = [line for line in intents_section.splitlines() if line.startswith("| `U01` |")]
    if len(closed_u01_intents) > 1:
        raise ValueError("open_intent_u01_duplicate")
    if closed_u01_intents:
        cps_text = cps_text.replace(closed_u01_intents[0] + "\n", "", 1)

    sequence = _markdown_section(cps_text, "### Deterministic Execution Sequence", "### Authority, Reality And Safety Stops")
    rows = [line for line in sequence.splitlines() if line.startswith("| `1` |")]
    if len(rows) != 1:
        raise ValueError("sequence_position_1_missing_or_duplicate")
    row = (
        f"| `1` | `U07` Learning WAITING WIP; `{state['current_state_generation']}`; `{state['current_transition_id']}` | "
        "U01 Learning chain is consumed; representative real outcomes remain unavailable and no independent READY capability exists | "
        f"`{state['current_next_action_id']}` | {state['sequence_execution_class']} | `{state['current_stop_condition']}` | "
        f"{state['sequence_expected_output']} |"
    )
    cps_text = cps_text.replace(rows[0], row, 1)

    sequence = _markdown_section(cps_text, "### Deterministic Execution Sequence", "### Authority, Reality And Safety Stops")
    position_four = [line for line in sequence.splitlines() if line.startswith("| `4` |")]
    if len(position_four) != 1:
        raise ValueError("sequence_position_4_missing_or_duplicate")
    completed_u01_sequence = (
        "| `4` | `U01 COMPLETE` | satisfied prerequisite; terminal evidence retained by existing owners | "
        "none; do not repeat governed certification | terminal historical evidence | `NONE` | "
        "certified outcome -> U02/U07/U08/U22 consumers |"
    )
    cps_text = cps_text.replace(position_four[0], completed_u01_sequence, 1)

    sequence = _markdown_section(cps_text, "### Deterministic Execution Sequence", "### Authority, Reality And Safety Stops")
    position_five = [line for line in sequence.splitlines() if line.startswith("| `5` |")]
    if len(position_five) != 1:
        raise ValueError("sequence_position_5_missing_or_duplicate")
    rollback_sequence = (
        "| `5` | `U05` | U01 no-rollback SUCCESS is certified; broader rollback-class evidence remains owner-gated | "
        "wait for qualifying real rollback/no-rollback evidence; do not force mutation | governed verification | "
        "`REAL_WORLD_LIMIT` | qualifying terminal result -> rollback owner and Production Maturity |"
    )
    cps_text = cps_text.replace(position_five[0], rollback_sequence, 1)

    authority_stops = _markdown_section(
        cps_text,
        "### Authority, Reality And Safety Stops",
        "### Owner Revalidation Requirements And Contradictions",
    )
    operational_rows = [line for line in authority_stops.splitlines() if line.startswith("| `OPERATIONAL_AUTHORITY` |")]
    real_world_rows = [line for line in authority_stops.splitlines() if line.startswith("| `REAL_WORLD_LIMIT` |")]
    if len(operational_rows) != 1 or len(real_world_rows) != 1:
        raise ValueError("authority_stop_rows_missing_or_duplicate")
    operational_row = (
        "| `OPERATIONAL_AUTHORITY` | `SUPERSEDED/HISTORICAL`; U01 boundary for the completed exact two-user serial repair outside "
        "`dap_default_tier1_readonly`; not current and not reusable. |"
    )
    real_world_row = (
        "| `REAL_WORLD_LIMIT` | Capability-local WAITING boundary for CAP-U02/U05/U06; it becomes a program terminal "
        "only when the READY execution frontier is empty. |"
    )
    cps_text = cps_text.replace(operational_rows[0], operational_row, 1)
    return cps_text.replace(real_world_rows[0], real_world_row, 1)


def delegated_policy_live_state_consistency(cps_text: str, omp_text: str = "") -> dict[str, Any]:
    """Reject stale packet-approval authority projections inside the approved policy."""
    normalized = normalized_cps_live_state()
    live = _markdown_field_table(_markdown_section(
        cps_text,
        "## 0. Authoritative Live Current State",
        "## Authoritative Unfinished Capability Closure Registry",
    ))
    registry = _markdown_field_table(_markdown_section(
        cps_text,
        "### Registry Metadata And Truth Lifecycle",
        "### Active Protected Work In Progress",
    ))
    wip = _markdown_field_table(_markdown_section(
        cps_text,
        "### Active Protected Work In Progress",
        "### Complete Or Locked Capability Records",
    ))
    capabilities = _markdown_section(
        cps_text,
        "### Unfinished Capability Closure Records",
        "### Open Engineering Intents And Last Responsible Links",
    )
    completed_capabilities = _markdown_section(
        cps_text,
        "### Complete Or Locked Capability Records",
        "### Unfinished Capability Closure Records",
    )
    open_intents = _markdown_section(
        cps_text,
        "### Open Engineering Intents And Last Responsible Links",
        "### Deterministic Execution Sequence",
    )
    sequence = _markdown_section(
        cps_text,
        "### Deterministic Execution Sequence",
        "### Authority, Reality And Safety Stops",
    )
    authority_stops = _markdown_section(
        cps_text,
        "### Authority, Reality And Safety Stops",
        "### Owner Revalidation Requirements And Contradictions",
    )
    contradictions: list[str] = []
    stale_operational: list[str] = []
    stale_packet: list[str] = []
    stale_candidate: list[str] = []

    external_program_terminal = (
        live.get("EXTERNAL_INPUT_REQUIRED", "").strip("`") == "TRUE"
        and live.get("PROGRAM_TERMINAL_CLASS", "").strip("`")
        == "OPERATIONAL_AUTHORITY_OUTSIDE_ACTIVE_POLICY"
    )
    policy_active = (
        live.get("CURRENT_MODE", "").strip("`") == "BOUNDED_DELEGATED_AUTONOMY_ACTIVE"
        and live.get("DELEGATED_AUTONOMY_POLICY", "").strip("`") == "APPROVED"
    )
    if not policy_active:
        contradictions.append("delegated_policy_live_state_not_active")

    def require_no(field: str, bucket: list[str], contradiction: str) -> None:
        if live.get(field, "").strip("`") != "NO":
            bucket.append(field)
            contradictions.append(contradiction)

    require_no("CANDIDATE_APPROVAL_REQUIRED", stale_candidate, "delegated_policy_live_candidate_approval_required")
    require_no("PACKET_APPROVAL_REQUIRED", stale_packet, "delegated_policy_live_packet_approval_required")
    require_no("HASH_APPROVAL_REQUIRED", stale_packet, "delegated_policy_live_hash_approval_required")
    if not live.get("PACKET_APPROVAL_STILL_REQUIRED", "").strip("`").startswith("NO inside approved policy"):
        stale_packet.append("PACKET_APPROVAL_STILL_REQUIRED")
        contradictions.append("delegated_policy_manual_packet_fallback_inside_policy")

    authority_required = live.get("AUTHORITY_REQUIRED_NOW", "").strip("`")
    expected_authority = "YES_OUTSIDE_ACTIVE_POLICY" if external_program_terminal else "NO_INSIDE_APPROVED_POLICY"
    if not authority_required.startswith(expected_authority):
        stale_operational.append("AUTHORITY_REQUIRED_NOW")
        contradictions.append("delegated_policy_live_operational_authority_required")

    authority_generation = live.get("CONTROLLED_RUN_AUTHORITY_GENERATION", "").strip("`")
    expected_generation = "POLICY_SCOPED; NO_PACKET_SPECIFIC_AUTHORITY_REQUIRED"
    if authority_generation != expected_generation:
        stale_operational.append("CONTROLLED_RUN_AUTHORITY_GENERATION")
        contradictions.append("delegated_policy_stale_exact_authority_generation_request")

    authority_decision = live.get("CONTROLLED_RUN_AUTHORITY_DECISION", "").strip("`")
    if not authority_decision.startswith("APPROVED_BOUNDED_SCOPE"):
        stale_operational.append("CONTROLLED_RUN_AUTHORITY_DECISION")
        contradictions.append("delegated_policy_authority_decision_not_bounded_scope")

    active_capability_match = re.search(r"CAP-U\d+", wip.get("capability_id", ""))
    active_capability_id = active_capability_match.group(0) if active_capability_match else ""
    cap_rows = [line for line in capabilities.splitlines() if line.startswith(f"| `{active_capability_id}` |")]
    active_capability = cap_rows[0] if len(cap_rows) == 1 else ""
    sequence_rows = [line for line in sequence.splitlines() if line.startswith("| `1` |")]
    sequence_one = sequence_rows[0] if len(sequence_rows) == 1 else ""
    sequence_four_rows = [line for line in sequence.splitlines() if line.startswith("| `4` |")]
    sequence_four = sequence_four_rows[0] if len(sequence_four_rows) == 1 else ""

    if "explicit approval" in sequence_four.lower() or "operational_authority" in sequence_four.lower():
        stale_operational.append("DETERMINISTIC_SEQUENCE_POSITION_4")
        contradictions.append("delegated_policy_sequence_requires_explicit_approval")
    if external_program_terminal:
        if "authority decision" not in sequence_one or "serial two-user repair" not in sequence_one:
            contradictions.append("delegated_policy_external_boundary_workflow_missing")
    elif active_capability_id == "CAP-U01" and (
        "fresh Candidate" not in sequence_one or "fresh packet" not in sequence_one or "policy admission" not in sequence_one
    ):
        contradictions.append("delegated_policy_sequence_workflow_missing")

    authority_row = next(
        (line for line in authority_stops.splitlines() if line.startswith("| `OPERATIONAL_AUTHORITY` |")),
        "",
    )
    if "Current U01 stop" in authority_row:
        stale_operational.append("AUTHORITY_REALITY_SAFETY_STOPS")
        contradictions.append("delegated_policy_operational_authority_is_current_u01_stop")

    cap_con_06 = next(
        (line for line in cps_text.splitlines() if line.startswith("| `CAP-CON-06` |")),
        "",
    )
    if "current boundary is `OPERATIONAL_AUTHORITY`" in cap_con_06:
        stale_operational.append("CAP-CON-06")
        contradictions.append("delegated_policy_cap_con_06_stale_operational_authority")

    live_registry_blob = "\n".join((
        _markdown_section(cps_text, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry"),
        _markdown_section(cps_text, "## Authoritative Unfinished Capability Closure Registry", "## 1. Historical / Capability State Summary"),
    ))
    for line in live_registry_blob.splitlines():
        lowered = line.lower()
        if "operational_authority" in lowered and "historical" in lowered and "SUPERSEDED/HISTORICAL" not in line:
            stale_operational.append("UNCLASSIFIED_HISTORICAL_OPERATIONAL_AUTHORITY")
            contradictions.append("historical_operational_authority_without_classification")
            break

    stop = live.get("CURRENT_STOP_CONDITION", "").strip("`")
    if stop == "OPERATIONAL_AUTHORITY" and not external_program_terminal:
        stale_operational.append("CURRENT_STOP_CONDITION")
        contradictions.append("delegated_policy_current_stop_is_operational_authority")
    registry_stop = registry.get("CURRENT_STOP_CONDITION", "").strip("`")
    wip_stop = wip.get("current_primary_stop", "").strip("`")
    cap_stop = ""
    if active_capability:
        cells = [cell.strip() for cell in active_capability.strip().strip("|").split("|")]
        cap_stop = cells[6].strip("`") if len(cells) > 6 else ""
    sequence_stop = ""
    if sequence_one:
        cells = [cell.strip() for cell in sequence_one.strip().strip("|").split("|")]
        sequence_stop = cells[5].strip("`") if len(cells) > 5 else ""
    stop_consistent = len({stop, registry_stop, wip_stop, cap_stop, sequence_stop}) == 1
    if not stop_consistent:
        contradictions.append("delegated_policy_cps_stop_divergence")

    next_action = live.get("CURRENT_NEXT_ACTION_ID", "").strip("`")
    expected_next_action = normalized["current_next_action_id"]
    next_consistent = (
        next_action == expected_next_action
        and registry.get("EXACT_CURRENT_SMALLEST_NEXT_ACTION_ID", "").strip("`") == next_action
        and wip.get("smallest_existing_next_action_id", "").strip("`") == next_action
        and f"`{next_action}`" in sequence_one
    )
    if not next_consistent:
        contradictions.append("delegated_policy_cps_next_action_divergence")

    cap_action_token = expected_next_action
    cap_consistent = bool(active_capability and stop in active_capability and cap_action_token in active_capability)
    if not cap_consistent:
        contradictions.append("delegated_policy_active_capability_divergence")
    sequence_consistent = bool(sequence_one and sequence_four and not any(item.startswith("delegated_policy_sequence") for item in contradictions))
    if not sequence_consistent:
        contradictions.append("delegated_policy_deterministic_sequence_divergence")

    contradiction_ids = sorted(set(contradictions))
    return {
        "schema": "v7-delegated-policy-live-state-consistency/v1",
        "delegated_policy_live_state_consistency": "PASS" if not contradiction_ids else "FAIL",
        "stale_operational_authority_projection_count": len(set(stale_operational)),
        "stale_packet_approval_projection_count": len(set(stale_packet)),
        "stale_candidate_approval_projection_count": len(set(stale_candidate)),
        "cps_stop_consistency": "PASS" if stop_consistent else "FAIL",
        "cps_next_action_consistency": "PASS" if next_consistent else "FAIL",
        "active_capability_consistency": "PASS" if cap_consistent else "FAIL",
        "cap_u01_consistency": "PASS" if cap_consistent else "FAIL",
        "deterministic_sequence_consistency": "PASS" if sequence_consistent else "FAIL",
        "contradiction_count": len(contradiction_ids),
        "contradiction_ids": contradiction_ids,
    }


def capability_dependency_consistency(cps_text: str) -> dict[str, Any]:
    """Validate the CPS-owned dependency graph and derive the executable frontier."""
    live = _markdown_field_table(_markdown_section(
        cps_text,
        "## 0. Authoritative Live Current State",
        "## Authoritative Unfinished Capability Closure Registry",
    ))
    graph = _markdown_section(
        cps_text,
        "### Capability Dependency Graph And Execution Frontier",
        "### Owner Revalidation Requirements And Contradictions",
    )
    completed_section = _markdown_section(
        cps_text,
        "### Complete Or Locked Capability Records",
        "### Unfinished Capability Closure Records",
    )
    unfinished_section = _markdown_section(
        cps_text,
        "### Unfinished Capability Closure Records",
        "### Open Engineering Intents And Last Responsible Links",
    )
    errors: list[str] = []
    if not graph:
        errors.append("capability_dependency_graph_missing")

    completed_ids = {
        match.group(1)
        for line in completed_section.splitlines()
        if (match := re.match(r"\| `(CAP-[CU]\d+)` \|", line))
    }
    unfinished_ids = {
        match.group(1)
        for line in unfinished_section.splitlines()
        if (match := re.match(r"\| `(CAP-U\d+)` \|", line))
    }
    expected_ids = {item for item in completed_ids | unfinished_ids if item.startswith("CAP-U")}
    rows: dict[str, dict[str, Any]] = {}
    for line in graph.splitlines():
        if not re.match(r"\| `CAP-U\d+` \|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 12:
            errors.append("dependency_graph_row_shape_invalid")
            continue
        capability_id = cells[0].strip("`")
        if capability_id in rows:
            errors.append(f"dependency_graph_duplicate:{capability_id}")
            continue
        rows[capability_id] = {
            "state": cells[1].strip("`"),
            "engineering_intent": cells[2],
            "producer_consumer": cells[3],
            "dependencies": set(re.findall(r"CAP-U\d+", cells[4])),
            "blocks": set(re.findall(r"CAP-U\d+", cells[5])),
            "does_not_block": set(re.findall(r"CAP-U\d+", cells[6])),
            "block_reason": cells[7],
            "reentry": cells[8],
            "execution_allowed": cells[9].strip("`"),
            "completion_allowed": cells[10].strip("`"),
            "completion_rule": cells[11].strip("`"),
            "raw": line,
        }

    graph_ids = set(rows)
    for missing in sorted(expected_ids - graph_ids):
        errors.append(f"dependency_graph_capability_missing:{missing}")
    for extra in sorted(graph_ids - expected_ids):
        errors.append(f"dependency_graph_unknown_capability:{extra}")

    valid_states = {
        "READY",
        "WAITING_EXTERNAL_DEPENDENCY",
        "BLOCKED_BY_DEPENDENCY",
        "EXECUTING",
        "COMPLETED",
        "FAILED_REQUIRES_REPAIR",
        "BLOCKED_AUTHORITY",
    }
    completion_rule = "ALL_DEPENDENCIES_COMPLETED+INTENT_CLOSED+CONSUMER_VERIFIED+EVIDENCE_CONSUMED+CPS_UPDATED"
    ready: list[str] = []
    waiting: list[str] = []
    blocked: list[str] = []
    dependency_violations: list[str] = []
    completion_violations: list[str] = []
    for capability_id, row in sorted(rows.items()):
        state = row["state"]
        dependencies = row["dependencies"]
        unknown_dependencies = dependencies - graph_ids
        if state not in valid_states:
            errors.append(f"dependency_state_invalid:{capability_id}")
        if unknown_dependencies:
            dependency_violations.append(f"dependency_unknown:{capability_id}")
        incomplete_dependencies = {
            item for item in dependencies
            if rows.get(item, {}).get("state") != "COMPLETED"
        }
        if row["completion_rule"] != completion_rule:
            completion_violations.append(f"completion_rule_invalid:{capability_id}")
        if "ALL_DEPENDENCIES_COMPLETED" not in row["completion_rule"]:
            completion_violations.append(f"DEPENDENCY_NOT_COMPLETED:{capability_id}")
        if "INTENT_CLOSED" not in row["completion_rule"]:
            completion_violations.append(f"INTENT_CHAIN_INCOMPLETE:{capability_id}")
        if "CONSUMER_VERIFIED" not in row["completion_rule"]:
            completion_violations.append(f"CONSUMER_MISSING:{capability_id}")
        if "EVIDENCE_CONSUMED" not in row["completion_rule"]:
            completion_violations.append(f"EVIDENCE_NOT_CONSUMED:{capability_id}")
        if "CPS_UPDATED" not in row["completion_rule"]:
            completion_violations.append(f"CPS_UPDATE_MISSING:{capability_id}")
        if state == "COMPLETED":
            if incomplete_dependencies:
                completion_violations.append(f"DEPENDENCY_NOT_COMPLETED:{capability_id}")
            if row["completion_allowed"] != "YES":
                completion_violations.append(f"completion_not_allowed_for_completed:{capability_id}")
            continue
        if row["completion_allowed"] == "YES":
            completion_violations.append(f"COMPLETION_ORDER_VIOLATION:{capability_id}")
        if state == "READY":
            ready.append(capability_id)
            if incomplete_dependencies or row["execution_allowed"] != "YES":
                dependency_violations.append(f"ready_with_incomplete_dependency:{capability_id}")
        elif state == "WAITING_EXTERNAL_DEPENDENCY":
            waiting.append(capability_id)
            if row["execution_allowed"] != "NO":
                dependency_violations.append(f"waiting_execution_allowed:{capability_id}")
            if not row["reentry"] or row["reentry"].strip("`").upper() in {"NONE", "UNKNOWN"}:
                dependency_violations.append(f"waiting_reentry_missing:{capability_id}")
            lowered = row["raw"].lower()
            if "create packet" in lowered or "request authority" in lowered:
                dependency_violations.append(f"waiting_mutation_path_present:{capability_id}")
        elif state in {"BLOCKED_BY_DEPENDENCY", "BLOCKED_AUTHORITY", "FAILED_REQUIRES_REPAIR"}:
            blocked.append(capability_id)
            if state == "BLOCKED_BY_DEPENDENCY" and not incomplete_dependencies:
                dependency_violations.append(f"blocked_without_incomplete_dependency:{capability_id}")
            if row["execution_allowed"] != "NO":
                dependency_violations.append(f"blocked_execution_allowed:{capability_id}")
        elif state == "EXECUTING":
            if incomplete_dependencies or row["execution_allowed"] != "YES":
                dependency_violations.append(f"executing_with_incomplete_dependency:{capability_id}")

    if rows.get("CAP-U02", {}).get("state") != "WAITING_EXTERNAL_DEPENDENCY":
        dependency_violations.append("cap_u02_not_waiting_external_dependency")
    if rows.get("CAP-U01", {}).get("state") != "COMPLETED":
        completion_violations.append("cap_u01_not_completed")

    expected_projection = {
        "DEPENDENCY_GRAPH_VERSION": "v7.omp-capability-dependency-graph.v1",
        "CURRENT_EXECUTION_FRONTIER": ",".join(ready) or "NONE",
        "WAITING_CAPABILITIES": ",".join(waiting) or "NONE",
        "READY_CAPABILITIES": ",".join(ready) or "NONE",
        "BLOCKED_CAPABILITIES": ",".join(blocked) or "NONE",
        "NEXT_EXECUTABLE_CAPABILITY": ready[0] if ready else "NONE",
    }
    for key, expected in expected_projection.items():
        if live.get(key, "").strip("`") != expected:
            errors.append(f"dependency_frontier_projection_divergence:{key}")

    continuation = live.get("OMP_CONTINUATION_REQUIRED", "").strip("`")
    external = live.get("EXTERNAL_INPUT_REQUIRED", "").strip("`")
    program_terminal = live.get("PROGRAM_TERMINAL_CLASS", "").strip("`")
    continuation_decision = live.get("CONTINUATION_DECISION", "").strip("`")
    program_terminal_state = live.get("PROGRAM_TERMINAL_STATE", "").strip("`")
    premature_program_stop = False
    if ready:
        if continuation != "TRUE" or external != "FALSE" or program_terminal != "NONE":
            premature_program_stop = True
            errors.append("ready_frontier_stopped_program")
        if continuation_decision != "CONTINUE_READY_FRONTIER":
            errors.append("ready_frontier_continuation_decision_invalid")
        if program_terminal_state != "NONE_READY_FRONTIER_EXISTS":
            errors.append("program_terminal_state_invalid_with_ready_frontier")
    else:
        if continuation != "FALSE" or external != "TRUE" or program_terminal in {"", "NONE"}:
            errors.append("empty_frontier_without_program_terminal")
        if not continuation_decision.startswith("PROGRAM_TERMINAL_"):
            errors.append("empty_frontier_continuation_decision_invalid")
        if not program_terminal_state.startswith(program_terminal):
            errors.append("empty_frontier_program_terminal_state_invalid")

    errors.extend(dependency_violations)
    errors.extend(completion_violations)
    unique = sorted(set(errors))
    return {
        "schema": "v7-omp-capability-dependency-consistency/v1",
        "dependency_graph_version": live.get("DEPENDENCY_GRAPH_VERSION", "").strip("`"),
        "dependency_graph_consistency": "PASS" if not dependency_violations and not any("dependency_graph" in item for item in unique) else "FAIL",
        "execution_frontier_validity": "PASS" if not any("frontier" in item or "execution_allowed" in item for item in unique) else "FAIL",
        "completion_order_consistency": "PASS" if not completion_violations else "FAIL",
        "waiting_state_consistency": "PASS" if not any("waiting" in item for item in unique) else "FAIL",
        "program_terminal_validity": "PASS" if not premature_program_stop else "FAIL",
        "premature_program_stop": premature_program_stop,
        "capability_count": len(rows),
        "waiting_capabilities": waiting,
        "ready_capabilities": ready,
        "blocked_capabilities": blocked,
        "execution_frontier": ready,
        "blocked_dependency_count": len(blocked),
        "ready_capability_count": len(ready),
        "dependency_violation_count": len(set(dependency_violations)),
        "completion_order_violation_count": len(set(completion_violations)),
        "final_verdict": "PASS" if not unique else "NO-GO",
        "errors": unique,
    }


def omp_self_continuation_consistency(cps_text: str) -> dict[str, Any]:
    """Fail closed when a transaction terminal is returned as a program terminal."""
    live = _markdown_field_table(_markdown_section(
        cps_text,
        "## 0. Authoritative Live Current State",
        "## Authoritative Unfinished Capability Closure Registry",
    ))
    required = (
        "OMP_CONTINUATION_REQUIRED",
        "EXTERNAL_INPUT_REQUIRED",
        "EXTERNAL_INPUT_TYPE",
        "TRANSACTION_TERMINAL_CLASS",
        "PROGRAM_TERMINAL_CLASS",
        "NEXT_MISSION_FORMED",
        "NEXT_MISSION_ID",
        "PREMATURE_OPERATOR_RETURN",
        "CONTINUATION_ITERATION",
        "CONTINUATION_STOP_REASON",
        "NO_PROGRESS_FINGERPRINT",
    )
    values = {key: live.get(key, "").strip("`") for key in required}
    errors: list[str] = []
    errors.extend(
        f"omp_self_continuation_field_missing:{key}"
        for key, value in values.items()
        if not value
    )
    continuation = values["OMP_CONTINUATION_REQUIRED"]
    external = values["EXTERNAL_INPUT_REQUIRED"]
    premature = values["PREMATURE_OPERATOR_RETURN"]
    next_formed = values["NEXT_MISSION_FORMED"]
    program_terminal = values["PROGRAM_TERMINAL_CLASS"]
    external_type = values["EXTERNAL_INPUT_TYPE"]
    next_action = live.get("CURRENT_NEXT_ACTION_ID", "").strip("`")
    mission_state = live.get("CURRENT_MISSION_STATE", "").strip("`")
    if continuation not in {"TRUE", "FALSE"}:
        errors.append("omp_continuation_required_invalid")
    if external not in {"TRUE", "FALSE"}:
        errors.append("omp_external_input_required_invalid")
    if premature != "FALSE":
        errors.append("PREMATURE_OMP_RETURN_TO_OPERATOR")
    if next_action == "CONTINUE_OMP" and external == "FALSE" and continuation != "TRUE":
        errors.append("PREMATURE_OMP_RETURN_TO_OPERATOR")
    if "CONTINUE_OMP_READY" in mission_state and external == "FALSE" and continuation != "TRUE":
        errors.append("continue_omp_ready_misclassified_as_program_terminal")
    if continuation == "TRUE":
        if external != "FALSE" or program_terminal != "NONE":
            errors.append("omp_continuation_program_terminal_conflict")
        if next_formed != "TRUE" or values["NEXT_MISSION_ID"] in {"", "NONE"}:
            errors.append("omp_next_mission_not_formed")
    if external == "TRUE":
        if continuation != "FALSE":
            errors.append("omp_external_boundary_continuation_conflict")
        if external_type in {"", "NONE"} or program_terminal in {"", "NONE"}:
            errors.append("omp_external_boundary_unclassified")
    try:
        if int(values["CONTINUATION_ITERATION"]) < 1:
            errors.append("omp_continuation_iteration_invalid")
    except ValueError:
        errors.append("omp_continuation_iteration_invalid")
    if not re.fullmatch(r"[0-9a-f]{64}", values["NO_PROGRESS_FINGERPRINT"]):
        errors.append("omp_no_progress_fingerprint_invalid")
    unique = sorted(set(errors))
    return {
        "schema": "v7-omp-self-continuation-consistency/v1",
        "final_verdict": "PASS" if not unique else "NO-GO",
        "premature_operator_return_validator": "PASS" if "PREMATURE_OMP_RETURN_TO_OPERATOR" not in unique else "FAIL",
        "omp_continuation_required": continuation,
        "external_input_required": external,
        "external_input_type": external_type,
        "transaction_terminal_class": values["TRANSACTION_TERMINAL_CLASS"],
        "program_terminal_class": program_terminal,
        "next_mission_formed": next_formed,
        "next_mission_id": values["NEXT_MISSION_ID"],
        "continuation_iteration": values["CONTINUATION_ITERATION"],
        "continuation_stop_reason": values["CONTINUATION_STOP_REASON"],
        "no_progress_fingerprint": values["NO_PROGRESS_FINGERPRINT"],
        "errors": unique,
    }


def cps_live_state_consistency(
    cps_text: str,
    *,
    root: Path = ROOT,
    omp_text: Optional[str] = None,
    verify_external: bool = True,
) -> dict[str, Any]:
    """Validate one atomic owner-backed CPS live projection across its consumers."""
    live = _markdown_field_table(_markdown_section(
        cps_text,
        "## 0. Authoritative Live Current State",
        "## Authoritative Unfinished Capability Closure Registry",
    ))
    registry = _markdown_field_table(_markdown_section(
        cps_text,
        "### Registry Metadata And Truth Lifecycle",
        "### Active Protected Work In Progress",
    ))
    wip = _markdown_field_table(_markdown_section(
        cps_text,
        "### Active Protected Work In Progress",
        "### Complete Or Locked Capability Records",
    ))
    sequence = _markdown_section(
        cps_text,
        "### Deterministic Execution Sequence",
        "### Authority, Reality And Safety Stops",
    )
    capabilities = _markdown_section(
        cps_text,
        "### Unfinished Capability Closure Records",
        "### Open Engineering Intents And Last Responsible Links",
    )
    completed_capabilities = _markdown_section(
        cps_text,
        "### Complete Or Locked Capability Records",
        "### Unfinished Capability Closure Records",
    )
    open_intents = _markdown_section(
        cps_text,
        "### Open Engineering Intents And Last Responsible Links",
        "### Deterministic Execution Sequence",
    )
    errors: list[str] = []
    for name, fields in (("live", live), ("registry", registry), ("wip", wip)):
        if not fields:
            errors.append(f"cps_{name}_projection_missing")

    generation = live.get("CURRENT_STATE_GENERATION", "")
    transition = live.get("CURRENT_TRANSITION_ID", "")
    next_action = live.get("CURRENT_NEXT_ACTION_ID", "")
    for key, value in (
        ("CURRENT_STATE_GENERATION", generation),
        ("CURRENT_TRANSITION_ID", transition),
        ("CURRENT_NEXT_ACTION_ID", next_action),
    ):
        if not value:
            errors.append(f"cps_{key.lower()}_missing")
    normalized = normalized_cps_live_state()
    exact_live = {
        "ACTIVE_PROGRAM": normalized["active_program"],
        "CURRENT_MODE": normalized["current_mode"],
        "CURRENT_STOP_CONDITION": normalized["current_stop_condition"],
        "CURRENT_ACTIVE_SCOPE": normalized["current_active_scope"],
        "CURRENT_SCOPE_CLASS": normalized["current_scope_class"],
        "CURRENT_EXECUTION_MISSION_ID": normalized["current_execution_mission_id"],
        "CURRENT_EXECUTION_MISSION_STATE": normalized["current_execution_mission_state"],
        "LATEST_TERMINAL_MISSION_ID": normalized["latest_terminal_mission_id"],
        "LATEST_TERMINAL_RUN_NONCE": normalized["latest_terminal_run_nonce"],
        "LATEST_TERMINAL_MISSION_STATE": normalized["latest_terminal_mission_state"],
        "LATEST_TERMINAL_MISSION_REPORT": normalized["latest_terminal_mission_report"],
        "LATEST_TERMINAL_MISSION_STARTED_AT": normalized["latest_terminal_mission_started_at"],
        "PREVIOUS_TERMINAL_MISSION_ID": normalized["previous_terminal_mission_id"],
        "CURRENT_MISSION_ROLE": normalized["current_mission_role"],
        "CURRENT_MISSION_ID": normalized["current_mission_id"],
        "CURRENT_RUN_NONCE": normalized["current_run_nonce"],
        "CURRENT_MISSION_STATE": normalized["current_mission_state"],
        "CURRENT_MISSION_REPORT": normalized["current_mission_report"],
        "AUTHORITATIVE_TRANSITION_INPUT_MISSION_ID": normalized["authoritative_transition_input_mission_id"],
        "AUTHORITATIVE_TRANSITION_INPUT_STATE": normalized["authoritative_transition_input_state"],
        "AUTHORITATIVE_TRANSITION_INPUT_REPORT": normalized["authoritative_transition_input_report"],
        "CURRENT_ACTION_CLASS": normalized["current_action_class"],
        "CURRENT_ACTION_CLASS_STATE": normalized["current_action_class_state"],
        "OLD_PACKETS_REUSABLE": normalized["old_packets_reusable"],
        "CURRENT_CLASS_OUTCOME": normalized["current_class_outcome"],
        "CURRENT_CLASS_DELTA_CLOSED": normalized["current_class_delta_closed"],
        "ACTION_CLASS_NON_CONSUMPTION_ROOT_CAUSE": normalized["action_class_non_consumption_root_cause"],
        "ACTION_CLASS_PROMOTION_EVALUATION": normalized["action_class_promotion_evaluation"],
        "ACTION_CLASS_EXACT_MISSING_DELTA": normalized["action_class_exact_missing_delta"],
        "CLASS_APPROVAL_READY": normalized["class_approval_ready"],
        "CONDITIONAL_ENGINEERING_AUTHORITY_USED": normalized["conditional_engineering_authority_used"],
        "CERTIFICATION_TRANSACTION_EXECUTED": normalized["certification_transaction_executed"],
        "CONTROLLED_RUN_ENGINEERING_INTENT_CLOSURE": normalized["controlled_run_engineering_intent_closure"],
        "PARENT_ENGINEERING_INTENT": normalized["parent_engineering_intent"],
        "DEPENDENCY_GRAPH_VERSION": normalized["dependency_graph_version"],
        "CURRENT_EXECUTION_FRONTIER": normalized["current_execution_frontier"],
        "WAITING_CAPABILITIES": normalized["waiting_capabilities"],
        "READY_CAPABILITIES": normalized["ready_capabilities"],
        "BLOCKED_CAPABILITIES": normalized["blocked_capabilities"],
        "CONTINUATION_DECISION": normalized["continuation_decision"],
        "NEXT_EXECUTABLE_CAPABILITY": normalized["next_executable_capability"],
        "PROGRAM_TERMINAL_STATE": normalized["program_terminal_state"],
        "OMP_CONTINUATION_REQUIRED": normalized["omp_continuation_required"],
        "EXTERNAL_INPUT_REQUIRED": normalized["external_input_required"],
        "EXTERNAL_INPUT_TYPE": normalized["external_input_type"],
        "TRANSACTION_TERMINAL_CLASS": normalized["transaction_terminal_class"],
        "PROGRAM_TERMINAL_CLASS": normalized["program_terminal_class"],
        "NEXT_MISSION_FORMED": normalized["next_mission_formed"],
        "NEXT_MISSION_ID": normalized["next_mission_id"],
        "PREMATURE_OPERATOR_RETURN": normalized["premature_operator_return"],
        "CONTINUATION_ITERATION": normalized["continuation_iteration"],
        "CONTINUATION_STOP_REASON": normalized["continuation_stop_reason"],
        "NO_PROGRESS_FINGERPRINT": normalized["no_progress_fingerprint"],
    }
    for key, expected in exact_live.items():
        if live.get(key, "").strip("`") != expected:
            errors.append(f"cps_normalized_field_divergence:{key}")
    for key, expected in (
        ("CAPABILITIES_INVENTORIED", normalized["capabilities_inventoried"]),
        ("COMPLETE_OR_LOCKED_CAPABILITIES", normalized["complete_or_locked_capabilities"]),
        ("UNFINISHED_CAPABILITIES", normalized["unfinished_capabilities"]),
        ("OPEN_ENGINEERING_INTENTS", normalized["open_engineering_intents"]),
    ):
        if registry.get(key, "").strip("`") != expected:
            errors.append(f"cps_registry_count_divergence:{key}")
    complete_rows = [line for line in completed_capabilities.splitlines() if line.startswith("| `CAP-")]
    unfinished_rows = [line for line in capabilities.splitlines() if line.startswith("| `CAP-")]
    if len(complete_rows) != int(normalized["complete_or_locked_capabilities"]):
        errors.append("cps_complete_capability_count_divergence")
    if len(unfinished_rows) != int(normalized["unfinished_capabilities"]):
        errors.append("cps_unfinished_capability_count_divergence")
    if len(complete_rows) + len(unfinished_rows) != int(normalized["capabilities_inventoried"]):
        errors.append("cps_inventory_total_divergence")
    if any(line.startswith("| `U01` |") for line in open_intents.splitlines()):
        errors.append("cps_closed_u01_still_open_intent")
    for key, expected in (
        ("BINDING_STABILITY", normalized["binding_stability"]),
        ("BINDING_SCHEMA", normalized["binding_schema"]),
        ("ROUTING_READINESS_STATE", normalized["routing_readiness_state"]),
        ("AUTHORITY_REQUIRED_NOW", normalized["authority_required_now"]),
    ):
        if not live.get(key, "").strip("`").startswith(expected):
            errors.append(f"cps_normalized_field_divergence:{key}")
    if generation and {
        generation,
        registry.get("CURRENT_STATE_GENERATION", ""),
        wip.get("current_state_generation", ""),
    } != {generation}:
        errors.append("cps_generation_divergence")
    if transition and {
        transition,
        registry.get("CURRENT_TRANSITION_ID", ""),
        wip.get("current_transition_id", ""),
    } != {transition}:
        errors.append("cps_transition_divergence")
    if next_action and {
        next_action,
        registry.get("EXACT_CURRENT_SMALLEST_NEXT_ACTION_ID", ""),
        wip.get("smallest_existing_next_action_id", ""),
    } != {next_action}:
        errors.append("cps_next_action_divergence")

    stop = live.get("CURRENT_STOP_CONDITION", "").strip("`")
    wip_stop = wip.get("current_primary_stop", "").strip("`")
    registry_stop = registry.get("CURRENT_STOP_CONDITION", "").strip("`")
    if stop != normalized["current_stop_condition"] or wip_stop != stop or registry_stop != stop:
        errors.append("cps_current_stop_divergence")
    if not live.get("AUTHORITY_REQUIRED_NOW", "").strip("`").startswith(normalized["authority_required_now"]):
        errors.append("cps_authority_required_not_policy_bounded")
    if not wip.get("authority_required_now", "").strip("`").startswith(normalized["wip_authority_required_now"]):
        errors.append("cps_wip_authority_required_not_policy_bounded")
    if wip.get("capability_id", "").strip("`") != normalized["active_wip"]:
        errors.append("cps_active_wip_identity_divergence")
    if wip.get("responsibility_class", "").strip("`") != normalized["responsibility_class"]:
        errors.append("cps_wip_responsibility_class_divergence")
    if wip.get("last_responsible_link", "") != normalized["last_responsible_link"]:
        errors.append("cps_wip_last_responsible_link_divergence")
    if not live.get("BINDING_STABILITY", "").strip("`").startswith("PASS"):
        errors.append("cps_binding_stability_not_pass")
    if live.get("OLD_PACKETS_REUSABLE", "").strip("`") != "NO":
        errors.append("cps_old_packets_reusable")
    if live.get("CURRENT_CLASS_OUTCOME", "").strip("`") != normalized["current_class_outcome"]:
        errors.append("cps_current_class_outcome_divergence")
    if live.get("CURRENT_ACTION_CLASS_STATE", "").strip("`") != "GOVERNED_ONLY":
        errors.append("cps_action_class_state_divergence")
    if normalized["automatic_continue_omp_result"] not in live.get("AUTOMATIC_CONTINUE_OMP_RESULT", ""):
        errors.append("cps_continue_omp_stop_divergence")
    if not live.get("OMP_CONTROLLED_RUN_ALLOWED", "").strip("`").startswith(normalized["omp_controlled_run_allowed"].split(";", 1)[0]):
        errors.append("cps_omp_consumption_divergence")
    if not live.get("CONTROLLED_RUN_EXECUTION_AUTHORIZED", "").strip("`").startswith(normalized["controlled_run_execution_authorized"].split(";", 1)[0]):
        errors.append("cps_execution_authority_not_policy_bounded")
    if live.get("CONTROLLED_RUN_RESPONSIBILITY_CLASS", "").strip("`") != normalized["responsibility_class"]:
        errors.append("cps_responsibility_class_divergence")
    if live.get("CURRENT_ACTIVE_SCOPE", "").strip("`") == "ONE_FRESH_CURRENT_CLASS_TRANSACTION":
        for key in (
            "CONTROLLED_RUN_PACKET_PREVIEW",
            "CONTROLLED_RUN_DECISION_ID",
            "CONTROLLED_RUN_OPERATION_ID",
            "CONTROLLED_RUN_SELECTED_MOVE_HASH",
            "CONTROLLED_RUN_SOURCE_BUNDLE_HASH",
            "CONTROLLED_RUN_SNAPSHOT_BUNDLE_HASH",
        ):
            if not live.get(key, "").strip("`").startswith("NONE_OPEN"):
                errors.append(f"cps_historical_packet_identity_live:{key}")

    live_blob = "\n".join(live.values())
    stale_markers = (
        "READ_ONLY_BINDING_DIAGNOSIS_ONLY",
        "stops at STOP_SAFE source/snapshot binding stability closure",
        "close operation-scoped binding stability through existing owner",
        "PRE_WRITE_SOURCE_SNAPSHOT_BINDING_STABILITY_CLOSURE",
    )
    for marker in stale_markers:
        if marker in live_blob or marker in registry.get("EXACT_CURRENT_SMALLEST_NEXT_ACTION", "") or marker in wip.get("smallest_existing_next_action", ""):
            errors.append(f"cps_stale_live_marker:{marker}")
    invalidation = live.get("CONTROLLED_RUN_INVALIDATION_REASON", "")
    if "SOURCE_SNAPSHOT_BUNDLE_DRIFT_" in invalidation and "SUPERSEDED/HISTORICAL" not in invalidation:
        errors.append("cps_historical_invalidation_looks_live")

    sequence_rows = [line for line in sequence.splitlines() if line.startswith("| `1` |")]
    if len(sequence_rows) != 1:
        errors.append("cps_sequence_position_1_missing_or_duplicate")
    else:
        sequence_cells = [cell.strip() for cell in sequence_rows[0].strip().strip("|").split("|")]
        sequence_stop = sequence_cells[5].strip("`") if len(sequence_cells) > 5 else ""
        if sequence_stop != stop or not all(token in sequence_rows[0] for token in (generation, transition, next_action)):
            errors.append("cps_sequence_position_1_divergence")

    active_capability_id = normalized["active_capability_id"]
    cap_rows = [line for line in capabilities.splitlines() if line.startswith(f"| `{active_capability_id}` |")]
    active_capability = cap_rows[0] if len(cap_rows) == 1 else ""
    if len(cap_rows) != 1:
        errors.append("cps_active_capability_missing_or_duplicate")
    else:
        cap_cells = [cell.strip() for cell in active_capability.strip().strip("|").split("|")]
        cap_stop = cap_cells[6].strip("`") if len(cap_cells) > 6 else ""
        cap_action = cap_cells[7] if len(cap_cells) > 7 else ""
        if cap_stop != normalized["current_stop_condition"]:
            errors.append("cps_active_capability_stop_divergence")
        expected_status = f"`{normalized['active_capability_status']}`"
        if expected_status not in active_capability:
            errors.append("cps_active_capability_status_divergence")
        if "bundle drifted" in active_capability or "diagnose existing binding" in active_capability:
            errors.append("cps_active_capability_unresolved_binding_drift")
        if normalized["current_next_action_id"] not in cap_action and not (
            normalized["current_next_action_id"] == "CONTINUE_OMP" and "Continue OMP" in cap_action
        ):
            errors.append("cps_active_capability_next_action_divergence")
        if wip.get("smallest_existing_next_action", "") != cap_action:
            errors.append("cps_wip_active_capability_next_action_divergence")

    completed_u01_rows = [line for line in completed_capabilities.splitlines() if line.startswith("| `CAP-U01` |")]
    cap_u01 = completed_u01_rows[0] if len(completed_u01_rows) == 1 else ""
    if len(completed_u01_rows) != 1 or "`COMPLETE`" not in cap_u01 or "`100.0`" not in cap_u01:
        errors.append("cps_cap_u01_completion_divergence")

    historical = _markdown_section(cps_text, "## 1. Historical / Capability State Summary")
    prohibited_headings = []
    for line in historical.splitlines():
        if not line.startswith("##"):
            continue
        lowered = line.lower()
        if ("current" in lowered or "latest" in lowered) and "historical" not in lowered:
            prohibited_headings.append(line)
    if prohibited_headings:
        errors.append("cps_historical_current_looking_headings")

    mission_identity_consistency = "NOT_CHECKED"
    omp_pointer_consistency = "NOT_CHECKED"
    mission_roles = mission_role_consistency(
        cps_text,
        root=root,
        omp_text=omp_text,
        verify_external=False,
    )
    errors.extend(mission_roles["errors"])
    omp_consistency: dict[str, Any] = {
        "omp_live_state_consistency": "NOT_CHECKED",
        "omp_current_pointer_consistency": "NOT_CHECKED",
        "omp_unqualified_live_heading_count": 0,
        "omp_historical_isolation": "NOT_CHECKED",
        "omp_current_stop": "",
        "cps_current_stop": stop,
        "omp_next_action": "",
        "cps_next_action": next_action.strip("`"),
        "omp_stale_identity_count": 0,
        "omp_contradiction_count": 0,
        "omp_contradiction_ids": [],
        "omp_report_pointer_consistency": "NOT_CHECKED",
        "omp_section20_classification": "NOT_CHECKED",
        "omp_section20_scheduling_authority": "NOT_CHECKED",
    }
    if verify_external:
        report_ref = live.get("CURRENT_MISSION_REPORT", "").strip("`")
        report_path = root / report_ref
        try:
            report_lines = report_path.read_text(encoding="utf-8").splitlines()
        except OSError:
            report_lines = []
        expected_id = f"Mission ID: `{live.get('CURRENT_MISSION_ID', '').strip('`')}`"
        expected_nonce = f"Run Nonce: `{live.get('CURRENT_RUN_NONCE', '').strip('`')}`"
        if len(report_lines) < 2 or report_lines[0] != expected_id or report_lines[1] != expected_nonce:
            errors.append("cps_current_mission_report_identity_mismatch")
            mission_identity_consistency = "FAIL"
        else:
            mission_identity_consistency = "PASS"
        if omp_text is None:
            try:
                omp_text = (root / "docs" / "programs" / "OPERATIONAL_MATURITY_PROGRAM.md").read_text(encoding="utf-8")
            except OSError:
                omp_text = ""
        if (
            report_ref
            and report_ref in omp_text
            and live.get("CURRENT_MISSION_STATE", "").strip("`") in omp_text
            and "Live continuation and the current bounded delegated policy state are owned only by CPS" in omp_text
        ):
            omp_pointer_consistency = "PASS"
        else:
            errors.append("cps_omp_pointer_mismatch")
            omp_pointer_consistency = "FAIL"

        omp_consistency = omp_live_state_consistency(cps_text, omp_text)
        errors.extend(omp_consistency["errors"])
        mission_roles = mission_role_consistency(
            cps_text,
            root=root,
            omp_text=omp_text,
            verify_external=True,
        )
        errors.extend(mission_roles["errors"])
        mission_identity_consistency = mission_roles["mission_identity_consistency"]

    delegated_live_state = delegated_policy_live_state_consistency(cps_text, omp_text or "")
    errors.extend(delegated_live_state["contradiction_ids"])
    self_continuation = omp_self_continuation_consistency(cps_text)
    errors.extend(self_continuation["errors"])
    dependency_consistency = capability_dependency_consistency(cps_text)
    errors.extend(dependency_consistency["errors"])
    unique_errors = sorted(set(errors))
    stale_ids = [
        item for item in unique_errors
        if "stale" in item or "historical" in item or "unresolved_binding_drift" in item
    ]

    return {
        "schema": "v7-cps-live-state-consistency/v1",
        "final_verdict": "PASS" if not unique_errors else "NO-GO",
        "status": "ATOMIC_CPS_LIVE_STATE_CONSISTENT" if not unique_errors else "CURRENT_STATE_CONSISTENCY_FAIL",
        "current_state_consistency": "PASS" if not unique_errors else "FAIL",
        "contradiction_count": len(unique_errors),
        "contradiction_ids": unique_errors,
        "stale_live_projection_count": len(stale_ids),
        "delegated_policy_live_state_consistency": delegated_live_state["delegated_policy_live_state_consistency"],
        "stale_operational_authority_projection_count": delegated_live_state["stale_operational_authority_projection_count"],
        "stale_packet_approval_projection_count": delegated_live_state["stale_packet_approval_projection_count"],
        "stale_candidate_approval_projection_count": delegated_live_state["stale_candidate_approval_projection_count"],
        "cps_stop_consistency": delegated_live_state["cps_stop_consistency"],
        "cps_next_action_consistency": delegated_live_state["cps_next_action_consistency"],
        "active_capability_consistency": delegated_live_state["active_capability_consistency"],
        "cap_u01_consistency": "PASS" if "cps_cap_u01_completion_divergence" not in unique_errors else "FAIL",
        "deterministic_sequence_consistency": delegated_live_state["deterministic_sequence_consistency"],
        "omp_self_continuation_consistency": self_continuation["final_verdict"],
        "premature_operator_return_validator": self_continuation["premature_operator_return_validator"],
        **{key: value for key, value in dependency_consistency.items() if key not in {"schema", "final_verdict", "errors"}},
        "registry_sequence_consistency": "PASS" if not any("sequence" in item or "cap_u01" in item or "active_capability" in item or "next_action" in item for item in unique_errors) else "FAIL",
        "mission_identity_consistency": mission_identity_consistency,
        **{key: value for key, value in mission_roles.items() if key not in {"schema", "final_verdict", "errors", "mission_identity_consistency"}},
        "omp_pointer_consistency": omp_pointer_consistency,
        **{key: value for key, value in omp_consistency.items() if key not in {"schema", "final_verdict", "errors"}},
        "errors": unique_errors,
        "current_state_generation": generation,
        "current_transition_id": transition,
        "current_next_action_id": next_action,
        "current_stop": stop,
        "section_0_fields": len(live),
        "registry_fields": len(registry),
        "active_wip_fields": len(wip),
        "historical_current_looking_headings": prohibited_headings,
        "sequence_position_1": sequence_rows[0] if len(sequence_rows) == 1 else "",
        "active_capability": active_capability,
        "cap_u01": cap_u01,
    }


def current_cps_consistency(path: Path = CPS_PATH) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {
            "schema": "v7-cps-live-state-consistency/v1",
            "final_verdict": "NO-GO",
            "status": "CPS_LIVE_STATE_CONTRADICTION_STOP_SAFE",
            "errors": ["cps_unreadable"],
        }
    return cps_live_state_consistency(text)


def atomic_reconcile_cps(
    path: Path = CPS_PATH,
    *,
    state: Optional[dict[str, str]] = None,
    replace_func: Callable[[str, str], None] = os.replace,
    post_write_hook: Optional[Callable[[Path], None]] = None,
) -> dict[str, Any]:
    """Render, validate, atomically replace, reread, and rollback CPS on failure."""
    try:
        original = path.read_text(encoding="utf-8")
        candidate = build_normalized_cps_document(original, state)
    except (OSError, ValueError) as exc:
        return {
            "ok": False,
            "status": "CURRENT_STATE_CONSISTENCY_FAIL",
            "errors": [f"cps_render_failed:{exc}"],
            "previous_state_preserved": True,
        }
    precheck = cps_live_state_consistency(candidate, verify_external=False)
    if precheck.get("final_verdict") != "PASS":
        return {
            "ok": False,
            "status": "CURRENT_STATE_CONSISTENCY_FAIL",
            "errors": precheck.get("errors") or [],
            "previous_state_preserved": True,
        }

    temp_name = ""
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=str(path.parent),
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_name = handle.name
            handle.write(candidate)
            handle.flush()
            os.fsync(handle.fileno())
        replace_func(temp_name, str(path))
        temp_name = ""
        if post_write_hook:
            post_write_hook(path)
    except OSError as exc:
        if temp_name:
            try:
                Path(temp_name).unlink()
            except OSError:
                pass
        return {
            "ok": False,
            "status": "CPS_ATOMIC_WRITE_FAILED",
            "errors": [str(exc)],
            "previous_state_preserved": path.read_text(encoding="utf-8") == original,
        }

    try:
        reread = path.read_text(encoding="utf-8")
    except OSError:
        reread = ""
    postcheck = cps_live_state_consistency(reread, verify_external=False)
    if reread != candidate or postcheck.get("final_verdict") != "PASS":
        rollback_name = ""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=str(path.parent),
                prefix=f".{path.name}.rollback.",
                suffix=".tmp",
                delete=False,
            ) as handle:
                rollback_name = handle.name
                handle.write(original)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(rollback_name, str(path))
            rollback_name = ""
        finally:
            if rollback_name:
                try:
                    Path(rollback_name).unlink()
                except OSError:
                    pass
        return {
            "ok": False,
            "status": "CPS_POST_WRITE_REREAD_FAILED_ROLLED_BACK",
            "errors": postcheck.get("errors") or ["cps_post_write_content_mismatch"],
            "previous_state_preserved": path.read_text(encoding="utf-8") == original,
        }
    return {
        "ok": True,
        "status": "ATOMIC_CPS_UPDATE_APPLIED",
        "errors": [],
        "previous_state_preserved": False,
        "post_write_reread": "PASS",
        "consistency": postcheck,
    }

APPROVED_DEPLOY_FILES = [
    {
        "name": "v7_sync_lib.py",
        "local_path": "tools/v7_sync_lib.py",
        "remote_path": "/usr/local/bin/v7_sync_lib.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/__init__.py",
        "local_path": "admin_core/__init__.py",
        "remote_path": "/usr/local/bin/admin_core/__init__.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "v7-users-autoswitch",
        "local_path": "tools/v7-users-autoswitch",
        "remote_path": "/usr/local/bin/v7-users-autoswitch",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-user-switch",
        "local_path": "tools/runtime-support/v7-user-switch",
        "remote_path": "/usr/local/bin/v7-user-switch",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-audit-log",
        "local_path": "tools/runtime-support/v7-audit-log",
        "remote_path": "/usr/local/bin/v7-audit-log",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-egress-load",
        "local_path": "tools/runtime-support/v7-egress-load",
        "remote_path": "/usr/local/bin/v7-egress-load",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-truth-check",
        "local_path": "tools/v7-truth-check",
        "remote_path": "/usr/local/bin/v7-truth-check",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-admin-api",
        "local_path": "admin/v7-admin-api",
        "remote_path": "/usr/local/bin/v7-admin-api",
        "mode": "0755",
        "service": "v7-admin-api.service",
    },
    {
        "name": "v7-operator-execution-packet",
        "local_path": "tools/v7-operator-execution-packet",
        "remote_path": "/usr/local/bin/v7-operator-execution-packet",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-intelligence-snapshot-refresh",
        "local_path": "tools/v7-intelligence-snapshot-refresh",
        "remote_path": "/usr/local/bin/v7-intelligence-snapshot-refresh",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-autonomy-trust-evidence-inventory",
        "local_path": "tools/v7-autonomy-trust-evidence-inventory",
        "remote_path": "/usr/local/bin/v7-autonomy-trust-evidence-inventory",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-governed-canary-dry-run-cycle",
        "local_path": "tools/v7-governed-canary-dry-run-cycle",
        "remote_path": "/usr/local/bin/v7-governed-canary-dry-run-cycle",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-users-autoswitch.service",
        "local_path": "systemd/v7-users-autoswitch.service",
        "remote_path": "/etc/systemd/system/v7-users-autoswitch.service",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "v7-service-matrix-refresh-all",
        "local_path": "tools/v7-service-matrix-refresh-all",
        "remote_path": "/usr/local/bin/v7-service-matrix-refresh-all",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-service-matrix-test",
        "local_path": "tools/v7-service-matrix-test",
        "remote_path": "/usr/local/bin/v7-service-matrix-test",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-egress-quality-compact",
        "local_path": "tools/v7-egress-quality-compact",
        "remote_path": "/usr/local/bin/v7-egress-quality-compact",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-egress-guard",
        "local_path": "tools/runtime-support/v7-egress-guard",
        "remote_path": "/usr/local/bin/v7-egress-guard",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-egress-set-state",
        "local_path": "tools/v7-egress-set-state",
        "remote_path": "/usr/local/bin/v7-egress-set-state",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-telegram-sentinel",
        "local_path": "tools/v7-telegram-sentinel",
        "remote_path": "/usr/local/bin/v7-telegram-sentinel",
        "mode": "0755",
        "service": None,
    },
    {
        "name": "v7-autoswitch-planner.service",
        "local_path": "systemd/drafts/v7-autoswitch-planner.service",
        "remote_path": "/etc/systemd/system/v7-autoswitch-planner.service",
        "mode": "0644",
        "service": "v7-autoswitch-planner.service",
    },
    {
        "name": "admin_core/admin_registry_views.py",
        "local_path": "admin_core/admin_registry_views.py",
        "remote_path": "/usr/local/bin/admin_core/admin_registry_views.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/diagnostic_views.py",
        "local_path": "admin_core/diagnostic_views.py",
        "remote_path": "/usr/local/bin/admin_core/diagnostic_views.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/events.py",
        "local_path": "admin_core/events.py",
        "remote_path": "/usr/local/bin/admin_core/events.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/intelligence_snapshots.py",
        "local_path": "admin_core/intelligence_snapshots.py",
        "remote_path": "/usr/local/bin/admin_core/intelligence_snapshots.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/intelligence_workers.py",
        "local_path": "admin_core/intelligence_workers.py",
        "remote_path": "/usr/local/bin/admin_core/intelligence_workers.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/intelligence_platform.py",
        "local_path": "admin_core/intelligence_platform.py",
        "remote_path": "/usr/local/bin/admin_core/intelligence_platform.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/autonomy_trust_acceleration.py",
        "local_path": "admin_core/autonomy_trust_acceleration.py",
        "remote_path": "/usr/local/bin/admin_core/autonomy_trust_acceleration.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/explainability_adapter.py",
        "local_path": "admin_core/explainability_adapter.py",
        "remote_path": "/usr/local/bin/admin_core/explainability_adapter.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/operator_execution.py",
        "local_path": "admin_core/operator_execution.py",
        "remote_path": "/usr/local/bin/admin_core/operator_execution.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/operation_scoped_binding.py",
        "local_path": "admin_core/operation_scoped_binding.py",
        "remote_path": "/usr/local/bin/admin_core/operation_scoped_binding.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/operator_execution_feedback.py",
        "local_path": "admin_core/operator_execution_feedback.py",
        "remote_path": "/usr/local/bin/admin_core/operator_execution_feedback.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/operator_execution_pipeline.py",
        "local_path": "admin_core/operator_execution_pipeline.py",
        "remote_path": "/usr/local/bin/admin_core/operator_execution_pipeline.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/operator_observability.py",
        "local_path": "admin_core/operator_observability.py",
        "remote_path": "/usr/local/bin/admin_core/operator_observability.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/operator_decision_surface.py",
        "local_path": "admin_core/operator_decision_surface.py",
        "remote_path": "/usr/local/bin/admin_core/operator_decision_surface.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/shadow_autonomy.py",
        "local_path": "admin_core/shadow_autonomy.py",
        "remote_path": "/usr/local/bin/admin_core/shadow_autonomy.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/operator_views.py",
        "local_path": "admin_core/operator_views.py",
        "remote_path": "/usr/local/bin/admin_core/operator_views.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/overview_views.py",
        "local_path": "admin_core/overview_views.py",
        "remote_path": "/usr/local/bin/admin_core/overview_views.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/performance_summaries.py",
        "local_path": "admin_core/performance_summaries.py",
        "remote_path": "/usr/local/bin/admin_core/performance_summaries.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/registry_readers.py",
        "local_path": "admin_core/registry_readers.py",
        "remote_path": "/usr/local/bin/admin_core/registry_readers.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/route_reality_views.py",
        "local_path": "admin_core/route_reality_views.py",
        "remote_path": "/usr/local/bin/admin_core/route_reality_views.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/route_views.py",
        "local_path": "admin_core/route_views.py",
        "remote_path": "/usr/local/bin/admin_core/route_views.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/routing_brain.py",
        "local_path": "admin_core/routing_brain.py",
        "remote_path": "/usr/local/bin/admin_core/routing_brain.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/routing_intelligence.py",
        "local_path": "admin_core/routing_intelligence.py",
        "remote_path": "/usr/local/bin/admin_core/routing_intelligence.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/runtime_read_views.py",
        "local_path": "admin_core/runtime_read_views.py",
        "remote_path": "/usr/local/bin/admin_core/runtime_read_views.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/sanitize.py",
        "local_path": "admin_core/sanitize.py",
        "remote_path": "/usr/local/bin/admin_core/sanitize.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/service_views.py",
        "local_path": "admin_core/service_views.py",
        "remote_path": "/usr/local/bin/admin_core/service_views.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/summary_builders.py",
        "local_path": "admin_core/summary_builders.py",
        "remote_path": "/usr/local/bin/admin_core/summary_builders.py",
        "mode": "0644",
        "service": None,
    },
    {
        "name": "admin_core/time.py",
        "local_path": "admin_core/time.py",
        "remote_path": "/usr/local/bin/admin_core/time.py",
        "mode": "0644",
        "service": None,
    },
]

RUNTIME_ENTRYPOINTS = (
    "tools/v7-users-autoswitch",
    "tools/v7-intelligence-snapshot-refresh",
    "tools/v7-service-matrix-refresh-all",
    "tools/v7-service-matrix-test",
    "tools/v7-egress-quality-compact",
    "tools/v7-telegram-sentinel",
    "admin/v7-admin-api",
    "tools/v7-operator-execution-packet",
    "tools/v7-governed-canary-dry-run-cycle",
)

SNAPSHOT_REQUIRED_FILES = (
    "service-scores.json",
    "channel-service-scores.json",
    "risk-summaries.json",
    "trust-summaries.json",
    "blast-radius-summaries.json",
    "overview-summary.json",
)

SNAPSHOT_SYSTEMD_UNITS = (
    "v7-intelligence-snapshot-refresh.service",
    "v7-intelligence-snapshot-refresh.timer",
)

FORBIDDEN_USER_ARGS = {"--force", "-f", "--force-with-lease", "--delete", "--mirror"}
FORBIDDEN_RUNTIME_TOKENS = {
    "autoswitch_apply",
    "restore_barrier_mutation",
    "routing_mutation",
    "user_movement",
    "planner_mutation",
}

DEPLOYABLE_CHANGE_PREFIXES = (
    "admin/",
    "admin_core/",
    "tools/",
    "systemd/",
)

DOCS_ONLY_CHANGE_PREFIXES = (
    "docs/",
    "tests/",
    "canary_expansion_execution_evidence/",
    "service_matrix_lineage_evidence/",
    "version_convergence_guard_evidence/",
)

ALLOWLISTED_RUNTIME_HASH_COMMAND_PATHS = {
    "/usr/local/bin/v7-users-autoswitch",
    "/usr/local/bin/v7-audit-log",
    "/usr/local/bin/v7-admin-api",
    "/usr/local/bin/v7-intelligence-snapshot-refresh",
    "/usr/local/bin/v7-service-matrix-refresh-all",
    "/usr/local/bin/v7-service-matrix-test",
    "/usr/local/bin/v7-egress-quality-compact",
}

ALLOWLISTED_RUNTIME_EXECUTABLE_TEST_PATHS = {
    "/usr/local/bin/v7-users-autoswitch",
    "/usr/local/bin/v7-audit-log",
    "/usr/local/bin/v7-admin-api",
    "/usr/local/bin/v7-intelligence-snapshot-refresh",
    "/usr/local/bin/v7-service-matrix-refresh-all",
    "/usr/local/bin/v7-service-matrix-test",
    "/usr/local/bin/v7-egress-quality-compact",
}

CommandRunner = Callable[[list[str], Optional[Path], int], dict[str, Any]]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run_command(cmd: list[str], cwd: Optional[Path] = None, timeout: int = 30) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ok": False, "rc": 127, "stdout": "", "stderr": str(exc), "cmd": cmd}
    return {
        "ok": proc.returncode == 0,
        "rc": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "cmd": cmd,
    }


def run_command_stdin(cmd: list[str], stdin: str, cwd: Optional[Path] = None, timeout: int = 30) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            input=stdin,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ok": False, "rc": 127, "stdout": "", "stderr": str(exc), "cmd": cmd}
    return {
        "ok": proc.returncode == 0,
        "rc": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "cmd": cmd,
    }


def emit(result: dict[str, Any], *, as_json: bool) -> int:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(human_summary(result))
    return 0 if result.get("final_verdict") == "PASS" else 1


def human_summary(result: dict[str, Any]) -> str:
    lines = [
        f"{result.get('tool', 'v7-sync')}: {result.get('final_verdict', 'UNKNOWN')}",
        f"status: {result.get('status', result.get('convergence_status', 'UNKNOWN'))}",
    ]
    for key in ("branch", "commit", "remote_commit", "runtime_commit", "mode"):
        if result.get(key):
            lines.append(f"{key}: {result[key]}")
    blockers = result.get("blockers") or []
    warnings = result.get("warnings") or []
    if blockers:
        lines.append("blockers: " + ", ".join(blockers))
    if warnings:
        lines.append("warnings: " + ", ".join(warnings))
    return "\n".join(lines)


def load_truth_module() -> Any:
    loader = importlib.machinery.SourceFileLoader("v7_truth_check_for_sync", str(TRUTH_CHECK_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def configured_runtime_snapshot_path(manifest: dict[str, Any]) -> Path:
    return ROOT / str(manifest.get("runtime_snapshot_path", ""))


def runtime_snapshot_seed_path(manifest: dict[str, Any]) -> Path:
    return ROOT / str(manifest.get("runtime_snapshot_seed_path", manifest.get("runtime_snapshot_path", "")))


def production_ssh_target(manifest: dict[str, Any] | None = None) -> str:
    manifest = manifest or load_manifest()
    return os.environ.get("V7_PROD_SSH_TARGET") or str(manifest.get("production_ssh_target") or "root@195.2.79.116")


def command_stdout(cmd: list[str], *, cwd: Path = ROOT, timeout: int = 30) -> str:
    return str(run_command(cmd, cwd=cwd, timeout=timeout).get("stdout") or "").strip()


def truth_check(mode: str = "all", *, runner: CommandRunner = run_command) -> dict[str, Any]:
    truth = load_truth_module()
    manifest = truth.load_manifest(MANIFEST_PATH)
    return truth.combine_results(manifest, mode=mode, runner=runner, cwd=ROOT)


def git_status() -> str:
    return command_stdout(["git", "status", "--short"])


def current_branch() -> str:
    return command_stdout(["git", "branch", "--show-current"])


def current_commit() -> str:
    return command_stdout(["git", "rev-parse", "HEAD"])


def origin_url() -> str:
    return command_stdout(["git", "remote", "get-url", REMOTE_NAME])


def remote_commit(remote_url: str, branch: str, *, runner: CommandRunner = run_command) -> str:
    result = runner(["git", "ls-remote", remote_url, f"refs/heads/{branch}"], ROOT, 30)
    if not result.get("ok"):
        return ""
    truth = load_truth_module()
    return truth.parse_ls_remote(str(result.get("stdout") or ""), branch)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def deploy_file_records() -> list[dict[str, Any]]:
    records = []
    for item in APPROVED_DEPLOY_FILES:
        local_path = ROOT / item["local_path"]
        exists = local_path.exists()
        records.append(
            {
                **item,
                "local_abs_path": str(local_path),
                "exists": exists,
                "sha256": sha256_file(local_path) if exists else "MISSING",
            }
        )
    return records


def approved_local_paths() -> set[str]:
    return {str(item["local_path"]) for item in APPROVED_DEPLOY_FILES}


def admin_core_imports(path: Path) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return set()
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name
                if name.startswith("admin_core."):
                    imports.add(name.split(".", 2)[1])
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module == "admin_core":
                for alias in node.names:
                    imports.add(alias.name)
            elif module.startswith("admin_core."):
                imports.add(module.split(".", 2)[1])
    return imports


def required_admin_core_paths_for_runtime() -> set[str]:
    pending = [ROOT / path for path in RUNTIME_ENTRYPOINTS if (ROOT / path).exists()]
    seen_files: set[Path] = set()
    required: set[str] = set()
    while pending:
        path = pending.pop()
        if path in seen_files or not path.exists():
            continue
        seen_files.add(path)
        for module in admin_core_imports(path):
            module_path = ROOT / "admin_core" / f"{module}.py"
            if not module_path.exists():
                continue
            local = str(module_path.relative_to(ROOT))
            if local not in required:
                required.add(local)
                pending.append(module_path)
    if required:
        init_path = ROOT / "admin_core" / "__init__.py"
        if init_path.exists():
            required.add(str(init_path.relative_to(ROOT)))
    return required


def deploy_allowlist_validation() -> dict[str, Any]:
    approved = approved_local_paths()
    required_runtime = set(RUNTIME_ENTRYPOINTS)
    required_admin = required_admin_core_paths_for_runtime()
    required = required_runtime | required_admin
    missing = sorted(path for path in required if path not in approved)
    extra = sorted(path for path in approved if path.startswith("admin_core/") and path not in required)
    records = deploy_file_records()
    missing_local_files = sorted(item["local_path"] for item in records if not item["exists"])
    duplicate_remote_paths = sorted(
        path
        for path in {item["remote_path"] for item in APPROVED_DEPLOY_FILES}
        if sum(1 for item in APPROVED_DEPLOY_FILES if item["remote_path"] == path) > 1
    )
    return {
        "schema": "v7-deploy-allowlist-validation/v1",
        "owner": "tools/v7_sync_lib.APPROVED_DEPLOY_FILES",
        "runtime_entrypoints": list(RUNTIME_ENTRYPOINTS),
        "required_admin_core_paths": sorted(required_admin),
        "approved_local_paths": sorted(approved),
        "missing_required_paths": missing,
        "documentation_extra_paths": extra,
        "missing_local_files": missing_local_files,
        "duplicate_remote_paths": duplicate_remote_paths,
        "final_verdict": "PASS" if not missing and not missing_local_files and not duplicate_remote_paths else "NO-GO",
    }


def build_runtime_fingerprint(*, branch: str, commit: str, deploy_id: str) -> dict[str, Any]:
    records = deploy_file_records()
    return {
        "schema": "v7-runtime-fingerprint/v1",
        "created_at": utc_now(),
        "branch": branch,
        "commit": commit,
        "deploy_id": deploy_id,
        "runtime_root": "/opt/v7",
        "critical_files": [
            {
                "name": item["name"],
                "local_path": item["local_path"],
                "remote_path": item["remote_path"],
                "sha256": item["sha256"],
                "mode": item["mode"],
            }
            for item in records
        ],
        "systemd_units": [
            "v7-autoswitch-planner.service",
            "v7-autoswitch-planner.timer",
            "v7-users-autoswitch.service",
            "v7-users-autoswitch.timer",
            "v7-admin-api.service",
            *SNAPSHOT_SYSTEMD_UNITS,
        ],
        "snapshot_subsystem": {
            "root": "/opt/v7/egress/state/intelligence",
            "refresh_cli": "/usr/local/bin/v7-intelligence-snapshot-refresh",
            "required_files": list(SNAPSHOT_REQUIRED_FILES),
            "systemd_units": list(SNAPSHOT_SYSTEMD_UNITS),
        },
        "authority": {
            "canonical_truth_gate": "tools/v7-truth-check",
            "canonical_deploy_tool": "tools/v7-safe-deploy",
            "canonical_status_command": "tools/v7-convergence-status",
        },
    }


def validate_runtime_fingerprint(fingerprint: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if fingerprint.get("schema") != "v7-runtime-fingerprint/v1":
        errors.append("schema_mismatch")
    if not fingerprint.get("commit"):
        errors.append("commit_missing")
    files = fingerprint.get("critical_files")
    if not isinstance(files, list) or not files:
        errors.append("critical_files_missing")
    else:
        for row in files:
            if not isinstance(row, dict):
                errors.append("critical_file_row_invalid")
                continue
            for key in ("local_path", "remote_path", "sha256"):
                if not row.get(key):
                    errors.append(f"critical_file_{key}_missing")
    snapshot = fingerprint.get("snapshot_subsystem")
    if not isinstance(snapshot, dict):
        errors.append("snapshot_subsystem_missing")
    else:
        if not snapshot.get("refresh_cli"):
            errors.append("snapshot_refresh_cli_missing")
        if not snapshot.get("required_files"):
            errors.append("snapshot_required_files_missing")
    return {
        "schema": "v7-runtime-fingerprint-validation/v1",
        "errors": sorted(set(errors)),
        "final_verdict": "PASS" if not errors else "NO-GO",
    }


def classify_status(status: str) -> dict[str, Any]:
    truth = load_truth_module()
    return truth.classify_git_status(status)


def reject_forbidden_args(argv: Iterable[str]) -> list[str]:
    seen = [arg for arg in argv if arg in FORBIDDEN_USER_ARGS]
    return [f"forbidden_arg:{arg}" for arg in seen]


def dirty_requires_runtime_approval(dirty: dict[str, Any]) -> bool:
    return bool(dirty.get("counts", {}).get("runtime_critical") or dirty.get("counts", {}).get("unknown"))


def safe_commit_plan(
    *,
    message: str,
    apply: bool,
    allow_runtime_critical: bool,
    runner: CommandRunner = run_command,
) -> dict[str, Any]:
    manifest = load_manifest()
    branch = current_branch()
    status = git_status()
    dirty = classify_status(status)
    blockers: list[str] = []
    warnings: list[str] = []

    if str(manifest.get("canonical_branch")) != CANONICAL_BRANCH:
        blockers.append("manifest_authoritative_branch_unexpected")
    if branch != str(manifest.get("canonical_branch")):
        blockers.append("branch_mismatch")
    if not message.strip():
        blockers.append("commit_message_required")
    if dirty.get("clean"):
        blockers.append("nothing_to_commit")
    if dirty.get("blocking") and not allow_runtime_critical:
        blockers.append("runtime_or_unknown_dirty_requires_explicit_allowance")
    if dirty.get("warning"):
        warnings.append("runtime_relevant_dirty")
    if dirty.get("info_paths"):
        warnings.append("documentation_dirty_present")

    commands = [
        ["git", "status", "--short"],
        ["git", "add", "--", "."],
        ["git", "commit", "-m", message],
    ]
    result = {
        "tool": "v7-safe-commit",
        "schema": "v7-safe-commit/v1",
        "mode": "apply" if apply else "dry-run",
        "branch": branch or "UNKNOWN",
        "commit_before": current_commit() or "UNKNOWN",
        "dirty_classification": dirty,
        "planned_commands": commands,
        "warnings": warnings,
        "blockers": blockers,
        "final_verdict": "PASS" if not blockers else "NO-GO",
    }
    if blockers or not apply:
        return result

    add_result = runner(["git", "add", "--", "."], ROOT, 30)
    commit_result = runner(["git", "commit", "-m", message], ROOT, 60)
    result["command_results"] = {"git_add": add_result, "git_commit": commit_result}
    if not add_result.get("ok"):
        result["blockers"].append("git_add_failed")
    if not commit_result.get("ok"):
        result["blockers"].append("git_commit_failed")
    result["commit_after"] = current_commit() or "UNKNOWN"
    result["final_verdict"] = "PASS" if not result["blockers"] else "NO-GO"
    return result


def safe_push_plan(*, apply: bool, argv: Iterable[str] = (), runner: CommandRunner = run_command) -> dict[str, Any]:
    manifest = load_manifest()
    branch = current_branch()
    commit = current_commit()
    remote = origin_url()
    expected_remote = str(manifest.get("canonical_remote"))
    blockers = reject_forbidden_args(argv)
    if branch != str(manifest.get("canonical_branch")):
        blockers.append("branch_mismatch")
    if remote != expected_remote:
        blockers.append("remote_mismatch")
    status = git_status()
    dirty = classify_status(status)
    if dirty.get("blocking"):
        blockers.append("blocking_dirty_workspace")
    before = remote_commit(remote, branch, runner=runner) if remote and branch else ""
    if before and before != commit and apply:
        ancestor = runner(["git", "merge-base", "--is-ancestor", before, commit], ROOT, 30)
        if not ancestor.get("ok"):
            blockers.append("remote_commit_not_ancestor_of_local")

    commands = [["git", "push", REMOTE_NAME, f"HEAD:{branch}"]]
    result = {
        "tool": "v7-safe-push",
        "schema": "v7-safe-push/v1",
        "mode": "apply" if apply else "dry-run",
        "branch": branch or "UNKNOWN",
        "commit": commit or "UNKNOWN",
        "remote": remote or "UNKNOWN",
        "remote_commit_before": before or "UNKNOWN",
        "planned_commands": commands,
        "blockers": blockers,
        "warnings": ["documentation_dirty_present"] if dirty.get("info_paths") else [],
        "final_verdict": "PASS" if not blockers else "NO-GO",
    }
    if blockers or not apply:
        return result

    push_result = runner(["git", "push", REMOTE_NAME, f"HEAD:{branch}"], ROOT, 120)
    after = remote_commit(remote, branch, runner=runner) if push_result.get("ok") else ""
    result["command_results"] = {"git_push": push_result}
    result["remote_commit_after"] = after or "UNKNOWN"
    if not push_result.get("ok"):
        result["blockers"].append("git_push_failed")
    if after and after != commit:
        result["blockers"].append("remote_commit_after_mismatch")
    result["final_verdict"] = "PASS" if not result["blockers"] else "NO-GO"
    return result


def deployment_id(branch: str, commit: str) -> str:
    stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    return f"deploy-z8-14-{branch}-{commit[:7]}-{stamp}"


def build_deploy_manifest(*, branch: str, commit: str, deploy_id: str) -> dict[str, Any]:
    fingerprint = build_runtime_fingerprint(branch=branch, commit=commit, deploy_id=deploy_id)
    return {
        "schema": "v7-deploy-manifest/v1",
        "project": "V7 Vozduh",
        "created_at": utc_now(),
        "deploy_id": deploy_id,
        "deploy_branch": branch,
        "deploy_commit": commit,
        "deployment_model": "copied_binaries_with_safe_sync_manifest",
        "approved_deploy_files": deploy_file_records(),
        "allowlist_validation": deploy_allowlist_validation(),
        "runtime_fingerprint": fingerprint,
        "runtime_fingerprint_validation": validate_runtime_fingerprint(fingerprint),
        "safety": {
            "autoswitch_apply_executed": False,
            "user_movement_executed": False,
            "routing_mutation_executed": False,
            "restore_barrier_modified": False,
            "planner_modified": False,
            "policy_modified": False,
        },
    }


def build_runtime_linkage(*, branch: str, commit: str, deploy_id: str) -> dict[str, Any]:
    return {
        "schema": "v7-runtime-linkage/v1",
        "updated_at": utc_now(),
        "runtime_identity_model": "copied_binaries_from_deploy_manifest",
        "runtime_root_is_git_checkout": False,
        "deploy_id": deploy_id,
        "deploy_branch": branch,
        "deploy_commit": commit,
        "runtime_fingerprint_schema": "v7-runtime-fingerprint/v1",
        "authoritative_workspace": str(ROOT),
        "authoritative_branch": branch,
    }


def build_release_manifest(
    *,
    branch: str,
    commit: str,
    deploy_id: str,
    service_restart_required: bool = False,
) -> dict[str, Any]:
    return {
        "schema": "v7-release-manifest/v1",
        "created_at": utc_now(),
        "release_id": deploy_id,
        "branch": branch,
        "commit": commit,
        "deploy_manifest": "/opt/v7/deploy-manifest.json",
        "runtime_linkage": "/opt/v7/runtime-linkage.json",
        "runtime_fingerprint": "/opt/v7/runtime-fingerprint.json",
        "rollback_manifest_required": True,
        "service_restart_required": bool(service_restart_required),
    }


def production_hashes_from_snapshot() -> dict[str, str]:
    manifest = load_manifest()
    snapshot_path = configured_runtime_snapshot_path(manifest)
    if not snapshot_path.exists():
        snapshot_path = runtime_snapshot_seed_path(manifest)
    if not snapshot_path.exists():
        return {}
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    command_results = snapshot.get("command_results") if isinstance(snapshot.get("command_results"), dict) else {}
    hashes: dict[str, str] = {}
    for command, value in command_results.items():
        if not command.startswith("sha256sum "):
            continue
        stdout = str((value or {}).get("stdout") or "")
        parts = stdout.split()
        if len(parts) >= 2:
            hashes[parts[1]] = parts[0]
    additional = (
        snapshot.get("additional_readonly_findings")
        if isinstance(snapshot.get("additional_readonly_findings"), dict)
        else {}
    )
    safe_deploy_hashes = (
        additional.get("safe_deploy_runtime_hashes")
        if isinstance(additional.get("safe_deploy_runtime_hashes"), dict)
        else {}
    )
    for remote_path, sha256 in safe_deploy_hashes.items():
        if remote_path and sha256:
            hashes[str(remote_path)] = str(sha256)
    return hashes


def deploy_delta() -> list[dict[str, Any]]:
    production = production_hashes_from_snapshot()
    delta = []
    for item in deploy_file_records():
        remote_hash = production.get(item["remote_path"], "UNKNOWN")
        delta.append(
            {
                "name": item["name"],
                "local_path": item["local_path"],
                "remote_path": item["remote_path"],
                "local_sha256": item["sha256"],
                "production_sha256": remote_hash,
                "matches": remote_hash == item["sha256"],
                "exists": item["exists"],
            }
        )
    return delta


def is_docs_only_change(path: str) -> bool:
    normalized = path.strip()
    if not normalized:
        return False
    first = normalized.split("/", 1)[0]
    first_lower = first.lower()
    return (
        normalized.startswith(DOCS_ONLY_CHANGE_PREFIXES)
        or first_lower.endswith("_evidence")
        or first_lower.endswith("-evidence")
        or first_lower.endswith("evidence")
        or (normalized.startswith("PROGRAM_") and normalized.endswith(".md"))
        or normalized.endswith("_REPORT.md")
    )


def is_deployable_change(path: str) -> bool:
    normalized = path.strip()
    if not normalized:
        return False
    return normalized in approved_local_paths() or normalized.startswith(DEPLOYABLE_CHANGE_PREFIXES)


def classify_deployable_changes(paths: Iterable[str]) -> dict[str, Any]:
    deploy_required: list[str] = []
    docs_only: list[str] = []
    unknown: list[str] = []
    for raw in paths:
        path = str(raw).strip()
        if not path:
            continue
        if is_docs_only_change(path):
            docs_only.append(path)
        elif is_deployable_change(path):
            deploy_required.append(path)
        else:
            unknown.append(path)
    if deploy_required:
        classification = "DEPLOY_REQUIRED"
    elif unknown:
        classification = "UNKNOWN"
    elif docs_only:
        classification = "DOCS_ONLY_MISMATCH"
    else:
        classification = "NO_CHANGES"
    return {
        "schema": "v7-deployable-change-classification/v1",
        "classification": classification,
        "deploy_required_paths": sorted(deploy_required),
        "docs_only_paths": sorted(docs_only),
        "unknown_paths": sorted(unknown),
        "deployment_required": bool(deploy_required),
        "docs_only_mismatch": bool(docs_only and not deploy_required and not unknown),
        "final_verdict": "PASS" if not unknown else "NO-GO",
    }


def changed_files_between_commits(
    base_commit: str,
    head_commit: str,
    *,
    runner: CommandRunner = run_command,
) -> list[str]:
    if not base_commit or not head_commit or "UNKNOWN" in {base_commit, head_commit}:
        return []
    if base_commit == head_commit:
        return []
    result = runner(["git", "diff", "--name-only", f"{base_commit}..{head_commit}"], ROOT, 30)
    if not result.get("ok"):
        return []
    return [line.strip() for line in str(result.get("stdout") or "").splitlines() if line.strip()]


def runtime_action_guard_for_status(
    status: dict[str, Any],
    *,
    changed_files: Optional[Iterable[str]] = None,
) -> dict[str, Any]:
    local_commit = str(status.get("local", {}).get("commit") or status.get("commit") or "UNKNOWN")
    github_commit = str(status.get("github", {}).get("commit") or status.get("remote_commit") or "UNKNOWN")
    production_commit = str(status.get("production", {}).get("commit") or status.get("runtime_commit") or "UNKNOWN")
    diagnosis = [str(item) for item in (status.get("diagnosis") or status.get("blockers") or [])]
    deploy_delta_rows = status.get("deploy_delta_mismatches") or []
    if not deploy_delta_rows and isinstance(status.get("deploy_delta"), list):
        deploy_delta_rows = [row for row in status["deploy_delta"] if isinstance(row, dict) and not row.get("matches")]
    classification = classify_deployable_changes(changed_files or [])
    deploy_required_by_delta = bool(deploy_delta_rows)
    deploy_required_by_changes = classification.get("classification") == "DEPLOY_REQUIRED"
    deployment_required = deploy_required_by_delta or deploy_required_by_changes
    docs_only_mismatch = (
        classification.get("classification") == "DOCS_ONLY_MISMATCH"
        and not deploy_required_by_delta
        and not deploy_required_by_changes
    )
    safe_deploy_command = (
        "tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED "
        "--update-local-snapshot --restart-admin-if-changed --json"
    )

    if status.get("final_verdict") == "PASS" and not deployment_required:
        guard_status = "READY_FOR_RUNTIME_ACTION"
        reason = "local_github_production_aligned"
        runtime_action_safe = True
        safe_next_command = "tools/v7-truth-check --all --json"
        final_verdict = "PASS"
    elif docs_only_mismatch and local_commit == github_commit and production_commit != "UNKNOWN":
        guard_status = "DOCS_ONLY_MISMATCH"
        reason = "production_commit_behind_only_docs_or_evidence_changes"
        runtime_action_safe = True
        safe_next_command = "tools/v7-convergence-status --json"
        final_verdict = "PASS"
    elif deployment_required or any("runtime_local_commit_mismatch" in item for item in diagnosis):
        guard_status = "DEPLOY_REQUIRED"
        reason = "production_runtime_not_at_deployable_current_truth"
        runtime_action_safe = False
        safe_next_command = safe_deploy_command
        final_verdict = "NO-GO"
    else:
        guard_status = "NO_GO"
        reason = "unclassified_convergence_blocker"
        runtime_action_safe = False
        safe_next_command = "tools/v7-convergence-status --json"
        final_verdict = "NO-GO"

    if classification.get("classification") == "UNKNOWN":
        guard_status = "NO_GO"
        reason = "changed_files_include_unknown_paths"
        runtime_action_safe = False
        safe_next_command = "STOP_REVIEW_CHANGED_FILES"
        final_verdict = "NO-GO"

    return {
        "schema": "v7-runtime-action-deploy-guard/v1",
        "status": guard_status,
        "reason": reason,
        "local_commit": local_commit,
        "github_commit": github_commit,
        "production_commit": production_commit,
        "deployment_required": deployment_required,
        "docs_only_mismatch": docs_only_mismatch,
        "runtime_action_safe": runtime_action_safe,
        "safe_next_command": safe_next_command,
        "deploy_delta_mismatches": deploy_delta_rows,
        "changed_files_since_production": sorted(str(path) for path in (changed_files or [])),
        "deployable_change_classification": classification,
        "diagnosis": diagnosis,
        "final_verdict": final_verdict,
    }


def safe_deploy_plan(
    *,
    apply: bool,
    confirm: str,
    update_local_snapshot: bool,
    restart_admin_if_changed: bool = False,
    runner: CommandRunner = run_command,
) -> dict[str, Any]:
    manifest = load_manifest()
    branch = current_branch()
    commit = current_commit()
    deploy_id = deployment_id(branch, commit)
    truth = truth_check("github", runner=runner)
    delta = deploy_delta()
    allowlist = deploy_allowlist_validation()
    blockers: list[str] = []
    if branch != str(manifest.get("canonical_branch")):
        blockers.append("branch_mismatch")
    if truth.get("final_verdict") != "PASS":
        blockers.append("github_truth_check_failed")
    if allowlist.get("final_verdict") != "PASS":
        blockers.append("deploy_allowlist_validation_failed")
    if any(not item["exists"] for item in deploy_file_records()):
        blockers.append("approved_deploy_file_missing")
    changed_admin = any(item["name"] == "v7-admin-api" and not item["matches"] for item in delta)
    changed_systemd = any(
        item["remote_path"].startswith("/etc/systemd/system/")
        and not item["matches"]
        for item in delta
    )
    if apply and confirm != DEPLOY_CONFIRMATION:
        blockers.append("deploy_confirmation_required")
    if apply and changed_admin and not restart_admin_if_changed:
        blockers.append("admin_binary_changed_requires_explicit_restart_flag")

    deploy_manifest = build_deploy_manifest(branch=branch, commit=commit, deploy_id=deploy_id)
    runtime_linkage = build_runtime_linkage(branch=branch, commit=commit, deploy_id=deploy_id)
    release_manifest = build_release_manifest(
        branch=branch,
        commit=commit,
        deploy_id=deploy_id,
        service_restart_required=bool(restart_admin_if_changed and changed_admin),
    )
    planned_remote_paths = {
        "backup_root": f"/root/v7-deploy-backups/{deploy_id}",
        "release_dir": f"/opt/v7/ops/{deploy_id}",
        "deploy_manifest": "/opt/v7/deploy-manifest.json",
        "runtime_linkage": "/opt/v7/runtime-linkage.json",
        "runtime_fingerprint": "/opt/v7/runtime-fingerprint.json",
        "release_manifest": f"/opt/v7/ops/{deploy_id}/release-manifest.json",
    }
    result = {
        "tool": "v7-safe-deploy",
        "schema": "v7-safe-deploy/v1",
        "mode": "apply" if apply else "dry-run",
        "branch": branch or "UNKNOWN",
        "commit": commit or "UNKNOWN",
        "deploy_id": deploy_id,
        "truth_check": truth,
        "deploy_delta": delta,
        "allowlist_validation": allowlist,
        "deployment_required": any(not item["matches"] for item in delta),
        "restart_admin_if_changed": restart_admin_if_changed,
        "planned_remote_paths": planned_remote_paths,
        "deploy_manifest": deploy_manifest,
        "runtime_linkage": runtime_linkage,
        "runtime_fingerprint": deploy_manifest["runtime_fingerprint"],
        "release_manifest": release_manifest,
        "blockers": blockers,
        "warnings": [],
        "final_verdict": "PASS" if not blockers else "NO-GO",
    }
    if blockers or not apply:
        return result

    ssh_target = production_ssh_target(manifest)
    payload = {
        "deploy_manifest": deploy_manifest,
        "runtime_linkage": runtime_linkage,
        "runtime_fingerprint": deploy_manifest["runtime_fingerprint"],
        "release_manifest": release_manifest,
        "update_local_snapshot": update_local_snapshot,
        "restart_admin_if_changed": restart_admin_if_changed,
        "files": [],
    }
    delta_by_path = {item["remote_path"]: item for item in delta}
    for item in deploy_file_records():
        replacement_required = not delta_by_path[item["remote_path"]]["matches"]
        file_payload = {
            "name": item["name"],
            "remote_path": item["remote_path"],
            "mode": item["mode"],
            "service": item["service"],
            "replace": replacement_required,
        }
        if replacement_required:
            file_payload["content_b64"] = base64.b64encode(Path(item["local_abs_path"]).read_bytes()).decode("ascii")
        payload["files"].append(file_payload)
    payload_b64 = base64.b64encode(json.dumps(payload, ensure_ascii=False).encode("utf-8")).decode("ascii")
    daemon_reload_block = "systemctl daemon-reload\n" if changed_systemd else ""
    restart_block = "systemctl restart v7-admin-api.service\n" if restart_admin_if_changed and changed_admin else ""
    script = (
        "set -eu\n"
        f"backup_root={planned_remote_paths['backup_root']}\n"
        f"release_dir={planned_remote_paths['release_dir']}\n"
        "mkdir -p \"$backup_root\" \"$release_dir\"\n"
        "for f in /usr/local/bin/v7-users-autoswitch /usr/local/bin/v7-audit-log /usr/local/bin/v7-admin-api; do "
        "if test -e \"$f\"; then cp -p \"$f\" \"$backup_root/$(basename \"$f\").pre-sync\"; fi; done\n"
        "python3 - <<'PY'\n"
        "import base64, json, os, pathlib, shutil\n"
        f"payload=json.loads(base64.b64decode('{payload_b64}').decode('utf-8'))\n"
        f"backup_root=pathlib.Path('{planned_remote_paths['backup_root']}')\n"
        "for item in payload['files']:\n"
        "    if not item.get('replace'):\n"
        "        continue\n"
        "    remote=pathlib.Path(item['remote_path'])\n"
        "    remote.parent.mkdir(parents=True, exist_ok=True)\n"
        "    if remote.exists():\n"
        "        backup_name=str(remote).strip('/').replace('/', '__') + '.pre-sync'\n"
        "        shutil.copy2(remote, backup_root / backup_name)\n"
        "    tmp=remote.with_suffix(remote.suffix + '.v7-sync-new')\n"
        "    tmp.write_bytes(base64.b64decode(item['content_b64']))\n"
        "    os.chmod(tmp, int(item['mode'], 8))\n"
        "    tmp.replace(remote)\n"
        "pathlib.Path('/opt/v7/deploy-manifest.json').write_text(json.dumps(payload['deploy_manifest'], indent=2, ensure_ascii=False)+'\\n')\n"
        "pathlib.Path('/opt/v7/runtime-linkage.json').write_text(json.dumps(payload['runtime_linkage'], indent=2, ensure_ascii=False)+'\\n')\n"
        "pathlib.Path('/opt/v7/runtime-fingerprint.json').write_text(json.dumps(payload['runtime_fingerprint'], indent=2, ensure_ascii=False)+'\\n')\n"
        f"pathlib.Path('{planned_remote_paths['release_manifest']}').write_text(json.dumps(payload['release_manifest'], indent=2, ensure_ascii=False)+'\\n')\n"
        "PY\n"
        f"{daemon_reload_block}"
        f"{restart_block}"
        f"ln -sfn {planned_remote_paths['release_dir']} /opt/v7/releases/current\n"
    )
    if runner is run_command:
        ssh_result = run_command_stdin(["ssh", ssh_target, "bash", "-s"], script, ROOT, 120)
    else:
        ssh_result = runner(["ssh", ssh_target, "bash", "-s"], ROOT, 120)
    result["command_results"] = {"ssh_manifest_refresh": ssh_result}
    if not ssh_result.get("ok"):
        result["blockers"].append("production_manifest_refresh_failed")
    elif update_local_snapshot:
        update_snapshot_for_deploy(deploy_id=deploy_id, branch=branch, commit=commit)
    result["final_verdict"] = "PASS" if not result["blockers"] else "NO-GO"
    return result


def update_snapshot_for_deploy(*, deploy_id: str, branch: str, commit: str) -> None:
    manifest = load_manifest()
    snapshot_path = configured_runtime_snapshot_path(manifest)
    seed_path = runtime_snapshot_seed_path(manifest)
    source_path = snapshot_path if snapshot_path.exists() else seed_path
    if not source_path.exists():
        return
    snapshot = json.loads(source_path.read_text(encoding="utf-8"))
    snapshot["collected_at"] = utc_now()
    snapshot["collection_mode"] = "z8_14_safe_deploy_provenance_refresh"
    additional = snapshot.setdefault("additional_readonly_findings", {})
    additional["z8_14_safe_sync"] = {
        "commit": commit,
        "deploy_id": deploy_id,
        "binary_replacement_performed": False,
        "autoswitch_apply_executed": False,
        "user_movement_executed": False,
        "routing_mutation_executed": False,
        "restore_barrier_modified": False,
        "service_restart_performed": False,
    }
    derived = snapshot.setdefault("derived", {})
    derived["deployment_model"] = "copied_binaries_from_safe_sync_manifest"
    derived["runtime_identity_model"] = "copied_binaries_from_safe_sync_manifest"
    derived["deploy_branch"] = branch
    derived["deploy_commit"] = commit
    derived["deploy_id"] = deploy_id
    fingerprint = build_runtime_fingerprint(branch=branch, commit=commit, deploy_id=deploy_id)
    command_results = snapshot.get("command_results") if isinstance(snapshot.get("command_results"), dict) else {}
    for command, value in list(command_results.items()):
        if isinstance(value, dict) and value.get("source") == "v7-safe-deploy-runtime-fingerprint":
            command_results.pop(command, None)
    runtime_hashes: dict[str, str] = {}
    for item in fingerprint.get("critical_files", []):
        remote_path = str(item.get("remote_path") or "")
        sha256 = str(item.get("sha256") or "")
        if not remote_path or not sha256:
            continue
        runtime_hashes[remote_path] = sha256
        if remote_path in ALLOWLISTED_RUNTIME_HASH_COMMAND_PATHS:
            command_results[f"sha256sum {remote_path}"] = {
                "ok": True,
                "rc": 0,
                "stdout": f"{sha256}  {remote_path}",
                "stderr": "",
                "cmd": ["sha256sum", remote_path],
                "source": "v7-safe-deploy-runtime-fingerprint",
            }
        if remote_path in ALLOWLISTED_RUNTIME_EXECUTABLE_TEST_PATHS:
            command_results[f"test -x {remote_path}"] = {
                "ok": True,
                "rc": 0,
                "stdout": "",
                "stderr": "",
                "cmd": ["test", "-x", remote_path],
                "source": "v7-safe-deploy-runtime-fingerprint",
            }
    additional["safe_deploy_runtime_hashes"] = runtime_hashes
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sync_status(*, runner: CommandRunner = run_command) -> dict[str, Any]:
    manifest = load_manifest()
    branch = current_branch()
    commit = current_commit()
    remote = origin_url()
    remote_head = remote_commit(remote, branch, runner=runner) if remote and branch else ""
    local_truth = truth_check("local", runner=runner)
    all_truth = truth_check("all", runner=runner)
    delta = deploy_delta()
    runtime = all_truth.get("runtime", {}) if isinstance(all_truth.get("runtime"), dict) else {}
    blockers: list[str] = []
    if local_truth.get("final_verdict") != "PASS":
        blockers.append("local_truth_failed")
    if remote_head and remote_head != commit:
        blockers.append("github_not_at_local_commit")
    if all_truth.get("final_verdict") != "PASS":
        blockers.extend([f"truth:{item}" for item in all_truth.get("blockers", [])])
    return {
        "tool": "v7-sync-status",
        "schema": "v7-sync-status/v1",
        "status": "SYNCED" if not blockers else "NO-GO",
        "branch": branch or "UNKNOWN",
        "commit": commit or "UNKNOWN",
        "remote": remote or "UNKNOWN",
        "remote_commit": remote_head or "UNKNOWN",
        "runtime_commit": runtime.get("runtime_commit", "UNKNOWN"),
        "local_truth": local_truth,
        "truth_check_all": all_truth,
        "deploy_delta": delta,
        "blockers": blockers,
        "warnings": all_truth.get("warnings", []),
        "final_verdict": "PASS" if not blockers else "NO-GO",
    }


def convergence_status(*, runner: CommandRunner = run_command) -> dict[str, Any]:
    status = sync_status(runner=runner)
    truth_all = status.get("truth_check_all") if isinstance(status.get("truth_check_all"), dict) else {}
    local = truth_all.get("local") if isinstance(truth_all.get("local"), dict) else {}
    github = truth_all.get("github") if isinstance(truth_all.get("github"), dict) else {}
    runtime = truth_all.get("runtime") if isinstance(truth_all.get("runtime"), dict) else {}
    deploy_delta_rows = status.get("deploy_delta") if isinstance(status.get("deploy_delta"), list) else []
    mismatched = [row for row in deploy_delta_rows if isinstance(row, dict) and not row.get("matches")]
    result = {
        "tool": "v7-convergence-status",
        "schema": "v7-convergence-status/v1",
        "canonical_truth_model": {
            "canonical_branch": CANONICAL_BRANCH,
            "canonical_deploy_source": "origin/Updatesystem plus tools/v7-safe-deploy approved package",
            "canonical_truth_gate": "tools/v7-truth-check",
            "canonical_deploy_tool": "tools/v7-safe-deploy",
            "canonical_runtime_fingerprint": "/opt/v7/runtime-fingerprint.json",
        },
        "local": {
            "commit": local.get("current_commit", status.get("commit", "UNKNOWN")),
            "status": local.get("final_verdict", "UNKNOWN"),
        },
        "github": {
            "commit": github.get("remote_branch_commit", status.get("remote_commit", "UNKNOWN")),
            "status": github.get("final_verdict", "UNKNOWN"),
        },
        "production": {
            "commit": runtime.get("runtime_commit", "UNKNOWN"),
            "status": runtime.get("final_verdict", "UNKNOWN"),
            "runtime_access_status": runtime.get("runtime_access_status", "UNKNOWN"),
            "runtime_truth_status": runtime.get("runtime_truth_status", "UNKNOWN"),
        },
        "deploy_allowlist": deploy_allowlist_validation(),
        "deploy_delta_mismatches": mismatched,
        "status": "ALIGNED" if status.get("final_verdict") == "PASS" else "NOT_ALIGNED",
        "diagnosis": status.get("blockers", []),
        "source_status": status,
        "final_verdict": status.get("final_verdict", "NO-GO"),
    }
    changed_files = changed_files_between_commits(
        str(result["production"].get("commit") or ""),
        str(result["local"].get("commit") or ""),
        runner=runner,
    )
    guard = runtime_action_guard_for_status(result, changed_files=changed_files)
    result["runtime_action_guard"] = guard
    result["runtime_action_status"] = guard["status"]
    result["runtime_action_safe"] = guard["runtime_action_safe"]
    result["safe_next_command"] = guard["safe_next_command"]
    return result


def convergence_owner_status(*, runner: CommandRunner = run_command) -> dict[str, Any]:
    status = convergence_status(runner=runner)
    source = status.get("source_status") if isinstance(status.get("source_status"), dict) else {}
    truth_all = source.get("truth_check_all") if isinstance(source.get("truth_check_all"), dict) else {}
    local_truth = truth_all.get("local") if isinstance(truth_all.get("local"), dict) else {}
    dirty = local_truth.get("dirty_classification") if isinstance(local_truth.get("dirty_classification"), dict) else {}
    diagnosis = list(status.get("diagnosis") or [])
    ssh_target = production_ssh_target()

    if status.get("final_verdict") == "PASS":
        next_action = "NONE_MONITOR"
        safe_command = "tools/v7-truth-check --all"
        explanation = "local_github_production_aligned"
    elif any("github_not_at_local_commit" in item or "local_remote_commit_mismatch" in item for item in diagnosis):
        next_action = "PUSH_CANONICAL_BRANCH"
        safe_command = "tools/v7-safe-push --apply --json"
        explanation = "github_is_not_at_local_commit"
    elif any("runtime_local_commit_mismatch" in item for item in diagnosis):
        next_action = "RUN_APPROVED_SAFE_DEPLOY"
        safe_command = (
            f"V7_PROD_SSH_TARGET={ssh_target} "
            "tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --json"
        )
        explanation = "production_is_not_at_local_commit"
    elif any("github_remote_unreadable" in item for item in diagnosis):
        next_action = "RETRY_WITH_NETWORK_ACCESS"
        safe_command = "tools/v7-truth-check --all"
        explanation = "github_read_failed"
    else:
        next_action = "STOP_REVIEW_BLOCKERS"
        safe_command = "tools/v7-convergence-status --json"
        explanation = "unclassified_blocker"

    return {
        "tool": "v7-convergence-owner",
        "schema": "v7-convergence-owner/v1",
        "status": status.get("status", "UNKNOWN"),
        "final_verdict": status.get("final_verdict", "NO-GO"),
        "local_commit": status.get("local", {}).get("commit", "UNKNOWN"),
        "github_commit": status.get("github", {}).get("commit", "UNKNOWN"),
        "production_commit": status.get("production", {}).get("commit", "UNKNOWN"),
        "runtime_access_status": status.get("production", {}).get("runtime_access_status", "UNKNOWN"),
        "runtime_truth_status": status.get("production", {}).get("runtime_truth_status", "UNKNOWN"),
        "workspace_runtime_clean": not bool(dirty.get("blocking") or dirty.get("warning")),
        "documentation_dirty_ignored": bool(dirty.get("documentation_only")),
        "next_required_action": next_action,
        "safe_command": safe_command,
        "explanation": explanation,
        "diagnosis": diagnosis,
        "source_status": status,
    }


def run_unit_tests() -> dict[str, Any]:
    cmd = [sys.executable, "-m", "unittest", "tests/unit/test_v7_sync_tools.py", "tests/unit/test_v7_truth_check.py"]
    return run_command(cmd, ROOT, 120)


def release_sync_plan(
    *,
    apply: bool,
    message: str,
    confirm: str,
    allow_runtime_critical: bool,
    runner: CommandRunner = run_command,
) -> dict[str, Any]:
    blockers: list[str] = []
    if apply and confirm != RELEASE_SYNC_CONFIRMATION:
        blockers.append("release_sync_confirmation_required")
    initial = sync_status(runner=runner)
    tests = run_unit_tests()
    commit_result = safe_commit_plan(
        message=message,
        apply=apply,
        allow_runtime_critical=allow_runtime_critical,
        runner=runner,
    )
    push_result = safe_push_plan(apply=apply, runner=runner)
    deploy_result = safe_deploy_plan(
        apply=apply,
        confirm=DEPLOY_CONFIRMATION if apply else "",
        update_local_snapshot=apply,
        restart_admin_if_changed=False,
        runner=runner,
    )
    final_truth = truth_check("all", runner=runner) if not apply else truth_check("all", runner=runner)
    if not tests.get("ok"):
        blockers.append("unit_tests_failed")
    for name, section in (
        ("commit", commit_result),
        ("push", push_result),
        ("deploy", deploy_result),
        ("truth", final_truth),
    ):
        if section.get("final_verdict") != "PASS":
            blockers.append(f"{name}_stage_no_go")
    return {
        "tool": "v7-release-sync",
        "schema": "v7-release-sync/v1",
        "mode": "apply" if apply else "dry-run",
        "initial_status": initial,
        "test_result": tests,
        "commit_result": commit_result,
        "push_result": push_result,
        "deploy_result": deploy_result,
        "final_truth_check": final_truth,
        "blockers": blockers,
        "warnings": [],
        "final_verdict": "PASS" if not blockers else "NO-GO",
    }


def add_common_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")


def add_apply_flags(parser: argparse.ArgumentParser, *, confirmation: str) -> None:
    parser.add_argument("--apply", action="store_true", help="perform the planned safe action")
    parser.add_argument("--confirm", default="", help=f"required confirmation token: {confirmation}")


def ensure_no_unsafe_tool_body(paths: Iterable[Path]) -> dict[str, Any]:
    findings = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        if "git push --force" in text or "--force-with-lease" in text:
            findings.append({"path": str(path), "issue": "force_push_token"})
        if "/usr/local/bin/v7-users-autoswitch --apply" in text:
            findings.append({"path": str(path), "issue": "autoswitch_apply_token"})
    return {
        "schema": "v7-sync-source-safety-scan/v1",
        "findings": findings,
        "final_verdict": "PASS" if not findings else "NO-GO",
    }


def executable_installed(path: Path) -> bool:
    return path.exists() and os.access(path, os.X_OK)


def copy_available() -> bool:
    return shutil.which("ssh") is not None
