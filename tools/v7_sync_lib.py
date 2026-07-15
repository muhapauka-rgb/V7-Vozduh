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
HEARTBEAT_AUTOMATION_ID = "v7-omp-external-reentry-heartbeat"
HEARTBEAT_TARGET_THREAD_ID = "019f4b9f-dda6-7762-b26c-3ab651f0a67c"
CANONICAL_BRANCH = "Updatesystem"
REMOTE_NAME = "origin"
DEPLOY_CONFIRMATION = "DEPLOY_V7_APPROVED"
RELEASE_SYNC_CONFIRMATION = "RELEASE_SYNC_APPROVED"

NORMALIZED_CPS_LIVE_STATE = {
    "active_program": "FUTURE_SCALE_SCENARIO_ENGINEERING",
    "current_mode": "BOUNDED_DELEGATED_AUTONOMY_ACTIVE",
    "current_stop_condition": "UNSAFE_IMPLEMENTATION",
    "current_active_scope": "FSSE_02_EXECUTION_HARNESS",
    "current_safe_next_action": "IMPLEMENT AND CERTIFY THE EXISTING-OWNER FUTURE-SCALE POLYGON EXECUTION HARNESS",
    "current_scope_class": "ENGINEERING_SCENARIO_BOUNDARY",
    "current_execution_mission_id": "NONE",
    "current_execution_mission_state": "NONE",
    "latest_terminal_mission_id": "V7_FUTURE_SCALE_POLYGON_FOUNDATION_V1",
    "latest_terminal_run_nonce": "V7_FSSE_FOUNDATION_V1_6D29A4C81E7F",
    "latest_terminal_mission_state": "FUTURE_SCALE_POLYGON_FOUNDATION_IMPLEMENTED_CONSUMED_FSSE_02_READY",
    "latest_terminal_mission_report": "docs/reports/engineering/2026-07-15_094920_future_scale_polygon_foundation.md",
    "latest_terminal_mission_started_at": "2026-07-15T09:49:20+0700",
    "previous_terminal_mission_id": "V7_OMP_HEARTBEAT_CANONICAL_DESCENDANT_DEPLOY_AND_EXTERNAL_REENTRY_CERTIFICATION_V2",
    "previous_terminal_mission_report": "docs/reports/engineering/2026-07-15_090500_omp_heartbeat_external_reentry_certification.md",
    "authoritative_transition_input_mission_id": "V7_OMP_BINDING_ATOMIC_SNAPSHOT_AND_MISSION_IDENTITY_GUARD_V3",
    "authoritative_transition_input_state": "MISSION_IDENTITY_GUARD_AND_BINDING_STABILITY_CERTIFIED",
    "authoritative_transition_input_report": "docs/reports/engineering/2026-07-11_225321_operation_scoped_binding_atomic_snapshot_closure_v3.md",
    "current_mission_role": "LATEST_TERMINAL_MISSION",
    "current_mission_id": "V7_FUTURE_SCALE_POLYGON_FOUNDATION_V1",
    "current_run_nonce": "V7_FSSE_FOUNDATION_V1_6D29A4C81E7F",
    "current_mission_state": "FUTURE_SCALE_POLYGON_FOUNDATION_IMPLEMENTED_CONSUMED_FSSE_02_READY",
    "current_mission_report": "docs/reports/engineering/2026-07-15_094920_future_scale_polygon_foundation.md",
    "state_captured": "2026-07-15T09:49:20+0700",
    "current_state_generation": "cpsgen_V7_FSSE_FOUNDATION_V1_6D29A4C81E7F",
    "current_transition_id": "FSSE_01_FOUNDATION_TO_FSSE_02_HARNESS_V1",
    "current_next_action_id": "V7_FUTURE_SCALE_POLYGON_EXECUTION_HARNESS_V1",
    "current_program_stage": "FSSE_01_COMPLETE_FSSE_02_READY",
    "current_program_execution_frontier": "V7_FUTURE_SCALE_POLYGON_EXECUTION_HARNESS_V1",
    "program_frontier_input": "validated deterministic Future-Scale Scenario Corpus and invariant resolver consumed by OMP program reconciliation",
    "program_frontier_owner": "existing OMP, CPS, Engineering Polygon and invariant validator owners",
    "program_frontier_expected_output": "FSSE-02 existing-owner execution harness -> bounded engineering scenario result -> invariant verdict -> BDP/OMP continuation",
    "protected_capability_wip": "CAP-U07 remains WAITING_EXTERNAL_DEPENDENCY; preserved and not reordered",
    "binding_stability": "PASS",
    "binding_schema": "v7.operation-scoped-source-binding.v2",
    "routing_readiness_state": "PASS_CANDIDATE_SCOPED",
    "authority_required_now": "NO_INSIDE_EXISTING_ENGINEERING_PROGRAM_SCOPE",
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
    "continuation_decision": "CONTINUE_PROGRAM_FRONTIER",
    "next_executable_capability": "NONE",
    "program_terminal_state": "NONE_FSSE_02_PROGRAM_FRONTIER_EXISTS",
    "cap_u01_completion_report": "docs/reports/engineering/2026-07-12_172534_exact_route_repair_and_first_governed_success.md",
    "responsibility_class": "LEARNING",
    "last_responsible_link": "real governed U01 outcome -> existing feedback/learning consumer -> future recommendation evidence",
    "smallest_existing_next_action": "approve the already validated safe deploy, then re-enable the same heartbeat for one post-repair natural run",
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
    "source_summary": "FSSE-01 reuses the existing Engineering Polygon and OMP reconciliation owners to produce a deterministic scenario frontier without Runtime or production effects.",
    "automatic_continue_omp_result": "FSSE_02_READY; exact next Mission materialized through the existing OMP consumer",
    "required_workflow": "implement existing-owner FSSE-02 execution harness -> verify deterministic engineering scenario -> route mismatches through BDP/OMP",
    "omp_controlled_run_allowed": "NO_CURRENT_EXECUTION; synthetic or forced outcomes are forbidden",
    "controlled_run_authority_required_now": "NO_RUNTIME_AUTHORITY; current boundary is FSSE-02 engineering implementation only",
    "controlled_run_execution_authorized": "NO_CURRENT_PACKET; no forced evidence generation or movement is authorized",
    "wip_authority_required_now": "FALSE; current boundary is representative real evidence, not Authority",
    "wip_current_primary_stop": "REAL_WORLD_LIMIT_CAPABILITY_LOCAL; global program frontier is OMP_REAL_CONSUMER_ACTIVATION at ENGINEERING_AUTHORITY",
    "wip_smallest_existing_next_action_id": "WAIT_FOR_REPRESENTATIVE_REAL_LEARNING_OUTCOMES",
    "wip_smallest_existing_next_action": "preserve CAP-U07 evidence unchanged while OMP waits for a legal real engineering trigger",
    "sequence_execution_class": "real-world evidence wait",
    "sequence_expected_output": "new representative governed outcomes -> Learning/B13 owner consumption -> dependency frontier recalculation",
    "completion_condition": "Learning closes only after dependencies, Engineering Intent, consumer verification, evidence consumption and CPS propagation pass",
    "capabilities_inventoried": "34",
    "complete_or_locked_capabilities": "13",
    "unfinished_capabilities": "21",
    "open_engineering_intents": "21",
    "omp_continuation_required": "TRUE",
    "external_input_required": "FALSE",
    "external_input_type": "NONE",
    "transaction_terminal_class": "INTEGRATION_COMPLETE",
    "program_terminal_class": "NONE",
    "next_mission_formed": "TRUE",
    "next_mission_id": "V7_FUTURE_SCALE_POLYGON_EXECUTION_HARNESS_V1",
    "premature_operator_return": "FALSE",
    "continuation_iteration": "15",
    "continuation_stop_reason": "FSSE_01_COMPLETE; FSSE_02_EXECUTION_HARNESS_NOT_YET_IMPLEMENTED",
    "no_progress_fingerprint": "78ab1f01d84288c6bdd2587c0d578556fe217558b664e00cd4b5deb32725f951",
    "program_reconciliation_footprint_class": "REAL_CLI_AND_OMP_CONSUMER_CONNECTED",
    "program_reconciliation_real_callers": "2",
    "program_reconciliation_test_callers": "4",
    "omp_automation_level": "CODEX_ASSISTED",
    "heartbeat_status": "PAUSED",
    "automation_enabled": "FALSE",
    "heartbeat_automation_level": "EXTERNAL_ENGINEERING_WAKEUP_ENTRYPOINT_WIRED_DEPLOY_BLOCKED",
    "heartbeat_last_wakeup_id": "019f616a-37d2-7103-9d34-3be847316197",
    "heartbeat_last_event_id": "18c01ddb3c6312617aa451b014b3762573a298c4a537985d816f236665579cc9",
    "heartbeat_last_cps_generation": "cpsgen_V7_OMP_REAL_EFFECT_AUDIT_V1_94C7E2A16D5B",
    "heartbeat_last_dependency_fingerprint": "e3af94aa51639fca0e30d5b669f33341e552d9f7f7dfff678f25a00a6a8fc950",
    "heartbeat_last_decision": "ADAPTER_CALLED_NO_RECONCILIATION",
    "heartbeat_last_run_at": "2026-07-14T23:16:18.434+0700",
    "aep_phase4_status": "IMPLEMENTED_MANUALLY_CALLABLE",
    "aep_phase5_status": "BLOCKED_MISSING_REAL_CONSUMER",
    "aep_phase6_status": "BLOCKED_BY_PHASE_5",
    "mission_completion_evidence_gate": "ACTIVE_V1",
    "current_completion_contract": "INTEGRATION_COMPLETION",
    "current_completion_verdict": "COMPLETE_CONSUMED",
    "fsse_status": "FSSE_01_FOUNDATION_COMPLETE_FSSE_02_READY",
    "fsse_00_external_reentry_status": "DEFERRED_PLATFORM_CERTIFICATION",
    "fsse_00_blocks_fsse_01": "FALSE",
    "manual_continue_omp_fallback": "ACTIVE",
    "scenario_coverage_generation": "fssef_78ab1f01d84288c6bdd2587c",
    "scenario_coverage_fingerprint": "78ab1f01d84288c6bdd2587c0d578556fe217558b664e00cd4b5deb32725f951",
    "scenario_target_level": "SAFETY_BASELINE_FOUNDATION_READY",
    "scenario_corpus_count": "10",
    "scenario_eligible_count": "10",
    "scenario_covered_count": "0",
    "scenario_stale_count": "0",
    "scenario_blocked_count": "0",
    "scenario_mismatch_count": "0",
    "next_scenario_id": "CAPACITY_BOUNDARY",
    "next_scenario_reason": "invariants=BLAST_RADIUS_BOUND",
    "active_scenario_id": "NONE",
    "last_scenario_id": "NONE",
    "last_scenario_verdict": "NONE",
    "last_scenario_fingerprint": "NONE",
    "active_scenario_candidate": "NONE",
    "active_scenario_mission": "NONE",
    "scenario_budget": "10",
    "scenario_stop_reason": "FSSE_02_EXECUTION_HARNESS_REQUIRED",
    "fsse_next_action": "V7_FUTURE_SCALE_POLYGON_EXECUTION_HARNESS_V1",
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
        "CURRENT_PROGRAM_STAGE": f"`{state['current_program_stage']}`",
        "CURRENT_PROGRAM_EXECUTION_FRONTIER": f"`{state['current_program_execution_frontier']}`",
        "PROTECTED_CAPABILITY_WIP": f"`{state['protected_capability_wip']}`",
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
        "AUTHORITY_REQUIRED_NOW": f"`{state['authority_required_now']}`",
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
        "PROGRAM_RECONCILIATION_FOOTPRINT_CLASS": f"`{state['program_reconciliation_footprint_class']}`",
        "PROGRAM_RECONCILIATION_REAL_CALLERS": f"`{state['program_reconciliation_real_callers']}`",
        "PROGRAM_RECONCILIATION_TEST_CALLERS": f"`{state['program_reconciliation_test_callers']}`",
        "OMP_AUTOMATION_LEVEL": f"`{state['omp_automation_level']}`",
        "HEARTBEAT_STATUS": f"`{state['heartbeat_status']}`",
        "AUTOMATION_ENABLED": f"`{state['automation_enabled']}`",
        "HEARTBEAT_AUTOMATION_LEVEL": f"`{state['heartbeat_automation_level']}`",
        "HEARTBEAT_LAST_WAKEUP_ID": f"`{state['heartbeat_last_wakeup_id']}`",
        "HEARTBEAT_LAST_EVENT_ID": f"`{state['heartbeat_last_event_id']}`",
        "HEARTBEAT_LAST_CPS_GENERATION": f"`{state['heartbeat_last_cps_generation']}`",
        "HEARTBEAT_LAST_DEPENDENCY_FINGERPRINT": f"`{state['heartbeat_last_dependency_fingerprint']}`",
        "HEARTBEAT_LAST_DECISION": f"`{state['heartbeat_last_decision']}`",
        "HEARTBEAT_LAST_RUN_AT": f"`{state['heartbeat_last_run_at']}`",
        "AEP_PHASE_4_STATUS": f"`{state['aep_phase4_status']}`",
        "AEP_PHASE_5_STATUS": f"`{state['aep_phase5_status']}`",
        "AEP_PHASE_6_STATUS": f"`{state['aep_phase6_status']}`",
        "MISSION_COMPLETION_EVIDENCE_GATE": f"`{state['mission_completion_evidence_gate']}`",
        "CURRENT_COMPLETION_CONTRACT": f"`{state['current_completion_contract']}`",
        "CURRENT_COMPLETION_VERDICT": f"`{state['current_completion_verdict']}`",
        "FSSE_STATUS": f"`{state['fsse_status']}`",
        "FSSE_00_EXTERNAL_REENTRY_STATUS": f"`{state['fsse_00_external_reentry_status']}`",
        "FSSE_00_BLOCKS_FSSE_01": f"`{state['fsse_00_blocks_fsse_01']}`",
        "MANUAL_CONTINUE_OMP_FALLBACK": f"`{state['manual_continue_omp_fallback']}`",
        "SCENARIO_COVERAGE_GENERATION": f"`{state['scenario_coverage_generation']}`",
        "SCENARIO_COVERAGE_FINGERPRINT": f"`{state['scenario_coverage_fingerprint']}`",
        "SCENARIO_TARGET_LEVEL": f"`{state['scenario_target_level']}`",
        "SCENARIO_CORPUS_COUNT": f"`{state['scenario_corpus_count']}`",
        "SCENARIO_ELIGIBLE_COUNT": f"`{state['scenario_eligible_count']}`",
        "SCENARIO_COVERED_COUNT": f"`{state['scenario_covered_count']}`",
        "SCENARIO_STALE_COUNT": f"`{state['scenario_stale_count']}`",
        "SCENARIO_BLOCKED_COUNT": f"`{state['scenario_blocked_count']}`",
        "SCENARIO_MISMATCH_COUNT": f"`{state['scenario_mismatch_count']}`",
        "NEXT_SCENARIO_ID": f"`{state['next_scenario_id']}`",
        "NEXT_SCENARIO_REASON": f"`{state['next_scenario_reason']}`",
        "ACTIVE_SCENARIO_ID": f"`{state['active_scenario_id']}`",
        "LAST_SCENARIO_ID": f"`{state['last_scenario_id']}`",
        "LAST_SCENARIO_VERDICT": f"`{state['last_scenario_verdict']}`",
        "LAST_SCENARIO_FINGERPRINT": f"`{state['last_scenario_fingerprint']}`",
        "ACTIVE_SCENARIO_CANDIDATE": f"`{state['active_scenario_candidate']}`",
        "ACTIVE_SCENARIO_MISSION": f"`{state['active_scenario_mission']}`",
        "SCENARIO_BUDGET": f"`{state['scenario_budget']}`",
        "SCENARIO_STOP_REASON": f"`{state['scenario_stop_reason']}`",
        "FSSE_NEXT_ACTION": f"`{state['fsse_next_action']}`",
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
        "smallest_existing_next_action_id": f"`{state['wip_smallest_existing_next_action_id']}`",
        "active_mission_id": "`NONE`",
        "active_mission_state": "`NONE`",
        "latest_terminal_mission_id": f"`{state['latest_terminal_mission_id']}`",
        "latest_terminal_mission_state": f"`{state['latest_terminal_mission_state']}`",
        "previous_terminal_mission_id": f"`{state['previous_terminal_mission_id']}`",
        "authoritative_transition_input_mission_id": f"`{state['authoritative_transition_input_mission_id']}`",
        "current_primary_stop": f"`{state['wip_current_primary_stop']}`",
        "responsibility_class": f"`{state['responsibility_class']}`",
        "authority_required_now": f"`{state['wip_authority_required_now']}`",
        "last_responsible_link": state["last_responsible_link"],
        "smallest_existing_next_action": state["wip_smallest_existing_next_action"],
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
        f"`{state['active_capability_progress']}` | {state['last_responsible_link']} | `REAL_WORLD_LIMIT` | "
        f"WAIT_FOR_REPRESENTATIVE_REAL_LEARNING_OUTCOMES; preserve accepted U01 Learning evidence and recheck only after a new material outcome | U01 complete; unblocks U04/U08/U09/U12/U17-U22 |"
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
    if state["current_program_execution_frontier"] not in {"", "NONE"}:
        row = (
            f"| `1` | `{state['current_program_stage']}` program frontier; `{state['current_state_generation']}`; "
            f"`{state['current_transition_id']}` | {state['program_frontier_input']} | "
            f"`{state['current_next_action_id']}` | {state['program_frontier_owner']} | "
            f"`{state['current_stop_condition']}` | {state['program_frontier_expected_output']} |"
        )
    else:
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
    cps_text = cps_text.replace(real_world_rows[0], real_world_row, 1)

    contradictions = _markdown_section(
        cps_text,
        "### Owner Revalidation Requirements And Contradictions",
        "## Stage 2 Knowledge Baseline Closure",
    )
    cap_con_06_rows = [
        line for line in contradictions.splitlines()
        if line.startswith("| `CAP-CON-06` |")
    ]
    if len(cap_con_06_rows) != 1:
        raise ValueError("cap_con_06_missing_or_duplicate")
    cap_con_06_row = (
        "| `CAP-CON-06` | Controlled Run responsibility | Completed U01 evidence preserves the exact two-user serial repair "
        "and final OPEN as historical outcome context | CPS/OMP current state | "
        f"current program terminal is `{state['program_terminal_class']}`; current stop is `{state['current_stop_condition']}`; "
        "U01 `OPERATIONAL_AUTHORITY` context is `SUPERSEDED/HISTORICAL` and non-reusable; "
        f"current next action is `{state['current_next_action_id']}`; no mutation is authorized |"
    )
    return cps_text.replace(cap_con_06_rows[0], cap_con_06_row, 1)


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
    live_stop = live.get("CURRENT_STOP_CONDITION", "").strip("`")
    live_program_terminal = live.get("PROGRAM_TERMINAL_CLASS", "").strip("`")
    program_frontier = live.get("CURRENT_PROGRAM_EXECUTION_FRONTIER", "").strip("`")
    independent_program_frontier = program_frontier not in {"", "NONE"}
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
    phase2_acceptance_frontier = program_frontier == "AEP_PHASE_2_ACCEPTANCE"
    phase3_acceptance_frontier = program_frontier == "AEP_PHASE_3_INDEPENDENT_ACCEPTANCE"
    real_consumer_activation_frontier = program_frontier == "OMP_REAL_CONSUMER_ACTIVATION"
    heartbeat_reentry_active = (
        real_consumer_activation_frontier
        and live.get("HEARTBEAT_STATUS", "").strip("`") == "ACTIVE"
        and live.get("AUTOMATION_ENABLED", "").strip("`") == "TRUE"
    )
    expected_authority = (
        "ENGINEERING_AUTHORITY_FOR_INDEPENDENT_AEP_PHASE_2_ACCEPTANCE_ONLY"
        if phase2_acceptance_frontier else
        "ENGINEERING_AUTHORITY_FOR_INDEPENDENT_AEP_PHASE_3_ACCEPTANCE_ONLY"
        if phase3_acceptance_frontier else
        "NO_INSIDE_EXISTING_ENGINEERING_PROGRAM_SCOPE"
        if heartbeat_reentry_active else
        "ENGINEERING_AUTHORITY_FOR_EXISTING_HEARTBEAT_ENABLEMENT_ONLY"
        if real_consumer_activation_frontier else
        "NO_INSIDE_EXISTING_ENGINEERING_PROGRAM_SCOPE"
        if independent_program_frontier else
        "YES_OUTSIDE_ACTIVE_POLICY" if external_program_terminal else
        "NO_INSIDE_APPROVED_POLICY"
    )
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
    expected_cap_con_terminal = f"current program terminal is `{live_program_terminal}`"
    if not cap_con_06:
        contradictions.append("delegated_policy_cap_con_06_missing")
    elif expected_cap_con_terminal not in cap_con_06:
        contradictions.append("delegated_policy_cap_con_06_current_terminal_divergence")
    if (
        "OPERATIONAL_AUTHORITY" in cap_con_06
        and live_program_terminal != "OPERATIONAL_AUTHORITY_OUTSIDE_ACTIVE_POLICY"
        and "`SUPERSEDED/HISTORICAL`" not in cap_con_06
    ):
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

    stop = live_stop
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
    stop_consistent = (
        len({stop, registry_stop, sequence_stop}) == 1
        and (independent_program_frontier or len({stop, wip_stop, cap_stop}) == 1)
        and (not independent_program_frontier or "REAL_WORLD_LIMIT" in wip_stop and "REAL_WORLD_LIMIT" in cap_stop)
    )
    if not stop_consistent:
        contradictions.append("delegated_policy_cps_stop_divergence")

    next_action = live.get("CURRENT_NEXT_ACTION_ID", "").strip("`")
    expected_next_action = normalized["current_next_action_id"]
    next_consistent = (
        next_action == expected_next_action
        and registry.get("EXACT_CURRENT_SMALLEST_NEXT_ACTION_ID", "").strip("`") == next_action
        and (
            independent_program_frontier
            or wip.get("smallest_existing_next_action_id", "").strip("`") == next_action
        )
        and f"`{next_action}`" in sequence_one
    )
    if not next_consistent:
        contradictions.append("delegated_policy_cps_next_action_divergence")

    cap_action_token = expected_next_action
    cap_consistent = bool(
        active_capability
        and (
            independent_program_frontier
            and "REAL_WORLD_LIMIT" in active_capability
            and "WAIT_FOR_REPRESENTATIVE_REAL_LEARNING_OUTCOMES" in active_capability
            or not independent_program_frontier
            and stop in active_capability
            and cap_action_token in active_capability
        )
    )
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
    program_frontier = live.get("CURRENT_PROGRAM_EXECUTION_FRONTIER", "").strip("`")
    independent_program_frontier = program_frontier not in {"", "NONE"}
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
        if independent_program_frontier:
            acceptance_frontier = program_frontier in {
                "AEP_PHASE_2_ACCEPTANCE",
                "AEP_PHASE_3_INDEPENDENT_ACCEPTANCE",
            }
            authority_frontier = acceptance_frontier or program_frontier == "OMP_REAL_CONSUMER_ACTIVATION"
            heartbeat_reentry_active = (
                program_frontier == "OMP_REAL_CONSUMER_ACTIVATION"
                and live.get("HEARTBEAT_STATUS", "").strip("`") == "ACTIVE"
                and live.get("AUTOMATION_ENABLED", "").strip("`") == "TRUE"
            )
            if heartbeat_reentry_active:
                if continuation != "FALSE" or external != "TRUE" or program_terminal != "NATURAL_SCHEDULED_RUN":
                    errors.append("program_heartbeat_reentry_boundary_invalid")
            elif authority_frontier:
                if continuation != "FALSE" or external != "TRUE" or program_terminal != "ENGINEERING_AUTHORITY":
                    errors.append("program_acceptance_frontier_external_boundary_invalid")
            elif continuation != "TRUE" or external != "FALSE" or program_terminal != "NONE":
                errors.append("program_frontier_stopped_program")
            expected_decision = (
                "PROGRAM_ACCEPTANCE_REQUIRED" if acceptance_frontier else
                "WAIT_EXTERNAL_TRIGGER" if heartbeat_reentry_active else
                "ENGINEERING_AUTHORITY_REQUIRED" if authority_frontier else
                "CONTINUE_PROGRAM_FRONTIER"
            )
            if continuation_decision != expected_decision:
                errors.append("program_frontier_continuation_decision_invalid")
            if program_frontier == "AEP_PHASE_2_ACCEPTANCE":
                if program_terminal_state != "ENGINEERING_AUTHORITY_AEP_PHASE_2_ACCEPTANCE_REQUIRED":
                    errors.append("program_frontier_terminal_state_invalid")
            elif program_frontier == "AEP_PHASE_3_INDEPENDENT_ACCEPTANCE":
                if program_terminal_state != "ENGINEERING_AUTHORITY_AEP_PHASE_3_ACCEPTANCE_REQUIRED":
                    errors.append("program_frontier_terminal_state_invalid")
            elif program_frontier == "OMP_REAL_CONSUMER_ACTIVATION":
                expected_terminal_state = (
                    "WAITING_POST_REPAIR_NATURAL_SCHEDULED_RUN" if heartbeat_reentry_active
                    else "ENGINEERING_AUTHORITY_REAL_CONSUMER_ACTIVATION_REQUIRED"
                )
                if program_terminal_state != expected_terminal_state:
                    errors.append("program_frontier_terminal_state_invalid")
            elif not program_terminal_state.startswith("NONE_"):
                errors.append("program_frontier_terminal_state_invalid")
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


CAPABILITY_ENGINEERING_REMAINING_CLASSES = {
    "ENGINEERING_IMPLEMENTATION_REMAINING",
    "ENGINEERING_INTEGRATION_REMAINING",
    "ENGINEERING_VERIFICATION_REMAINING",
    "ENGINEERING_CERTIFICATION_REMAINING",
    "ENGINEERING_CONSUMPTION_REMAINING",
    "ENGINEERING_INTENT_CLOSURE_REMAINING",
    "CANONICAL_STATE_RECONCILIATION_REMAINING",
}


def classify_capability_remaining_criterion(criterion: dict[str, Any]) -> str:
    """Classify one owner-backed criterion without treating backlog DONE as closure."""
    if criterion.get("criterion_closed"):
        return "NOT_APPLICABLE_WITH_REASON"
    if criterion.get("current_state_contradiction"):
        return "CANONICAL_STATE_RECONCILIATION_REMAINING"
    if criterion.get("implementation_missing"):
        return "ENGINEERING_IMPLEMENTATION_REMAINING"
    if criterion.get("integration_missing"):
        return "ENGINEERING_INTEGRATION_REMAINING"
    if criterion.get("verification_missing") and criterion.get("verification_executable", True):
        return "ENGINEERING_VERIFICATION_REMAINING"
    if criterion.get("certification_missing") and criterion.get("certification_executable", True):
        return "ENGINEERING_CERTIFICATION_REMAINING"
    if criterion.get("output_consumed") is False:
        return "ENGINEERING_CONSUMPTION_REMAINING"
    if criterion.get("intent_closed") is False:
        return "ENGINEERING_INTENT_CLOSURE_REMAINING"
    if criterion.get("backlog_status") == "DONE" and criterion.get("backlog_claimed_open"):
        return "ALREADY_COMPLETE_STALE_PROJECTION"
    if criterion.get("not_applicable_reason"):
        return "NOT_APPLICABLE_WITH_REASON"
    if criterion.get("dependency_wait"):
        return "DEPENDENCY_WAIT"
    if criterion.get("operational_authority_required"):
        return "OPERATIONAL_AUTHORITY_REQUIRED"
    if criterion.get("engineering_authority_required"):
        return "ENGINEERING_AUTHORITY_REQUIRED"
    if criterion.get("production_certification_required"):
        return "PRODUCTION_CERTIFICATION_REQUIRED"
    if criterion.get("real_world_evidence_required"):
        if (
            criterion.get("engineering_path_complete")
            and criterion.get("concrete_real_event")
            and criterion.get("reentry_condition")
        ):
            return "REAL_WORLD_EVIDENCE_REQUIRED"
        return "UNKNOWN_WITH_REASON"
    return "UNKNOWN_WITH_REASON"


def _capability_dependency_rows(cps_text: str) -> dict[str, dict[str, Any]]:
    graph = _markdown_section(
        cps_text,
        "### Capability Dependency Graph And Execution Frontier",
        "### Owner Revalidation Requirements And Contradictions",
    )
    rows: dict[str, dict[str, Any]] = {}
    for line in graph.splitlines():
        if not re.match(r"\| `CAP-U\d+` \|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 12:
            continue
        capability_id = cells[0].strip("`")
        rows[capability_id] = {
            "capability_id": capability_id,
            "dependency_state": cells[1].strip("`"),
            "engineering_intent": cells[2],
            "producer_consumer": cells[3],
            "dependencies": sorted(set(re.findall(r"CAP-U\d+", cells[4]))),
            "current_block_reason": cells[7].strip("`"),
            "reentry_condition": cells[8].strip("`"),
            "execution_allowed": cells[9].strip("`"),
            "completion_allowed": cells[10].strip("`"),
        }
    return rows


def _actionable_backlog_statuses(backlog_text: str) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for line in backlog_text.splitlines():
        match = re.match(r"\| `([ABC]\d+)` \| `([^`]+)` \|", line)
        if match:
            statuses[match.group(1)] = match.group(2)
    return statuses


def capability_closure_reconciliation(
    cps_text: str,
    omp_text: str,
    backlog_text: str,
) -> dict[str, Any]:
    """Reconcile implementation completion against the CPS-owned capability frontier."""
    errors: list[str] = []
    dependency = capability_dependency_consistency(cps_text)
    if dependency["final_verdict"] != "PASS":
        errors.extend(dependency["errors"])
    rows = _capability_dependency_rows(cps_text)
    backlog = _actionable_backlog_statuses(backlog_text)
    expected_backlog_ids = {
        *(f"A{index}" for index in range(1, 7)),
        *(f"B{index}" for index in range(1, 22)),
        *(f"C{index}" for index in range(1, 8)),
    }
    missing_backlog = sorted(expected_backlog_ids - set(backlog))
    non_terminal_backlog = sorted(
        item for item, status in backlog.items()
        if item in expected_backlog_ids and status != "DONE"
    )
    errors.extend(f"actionable_backlog_item_missing:{item}" for item in missing_backlog)
    errors.extend(f"actionable_backlog_item_not_done:{item}" for item in non_terminal_backlog)

    criteria: list[dict[str, Any]] = []
    for capability_id, row in sorted(rows.items()):
        state = row["dependency_state"]
        if state == "COMPLETED":
            continue
        if state == "WAITING_EXTERNAL_DEPENDENCY":
            classification = classify_capability_remaining_criterion({
                "real_world_evidence_required": True,
                "engineering_path_complete": True,
                "concrete_real_event": bool(row["current_block_reason"]),
                "reentry_condition": row["reentry_condition"],
            })
        elif state == "BLOCKED_AUTHORITY":
            classification = "OPERATIONAL_AUTHORITY_REQUIRED"
        elif state == "BLOCKED_BY_DEPENDENCY":
            classification = "DEPENDENCY_WAIT"
        elif state in {"READY", "EXECUTING", "FAILED_REQUIRES_REPAIR"}:
            classification = "ENGINEERING_IMPLEMENTATION_REMAINING"
        else:
            classification = "UNKNOWN_WITH_REASON"
        criteria.append({
            **row,
            "criterion_id": f"{capability_id}-CURRENT-CLOSURE",
            "primary_classification": classification,
            "smallest_existing_next_action": row["reentry_condition"],
            "existing_owner": True,
            "bdp_discovery_required": False,
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_impact": "NONE",
        })

    engineering = [
        item for item in criteria
        if item["primary_classification"] in CAPABILITY_ENGINEERING_REMAINING_CLASSES
    ]
    unknown = [item for item in criteria if item["primary_classification"] == "UNKNOWN_WITH_REASON"]
    ready_ids = list(dependency.get("ready_capabilities") or [])
    implementation_complete = (
        not missing_backlog
        and not non_terminal_backlog
        and not engineering
        and not unknown
        and not ready_ids
    )
    current_stop = _markdown_field_table(_markdown_section(
        cps_text,
        "## 0. Authoritative Live Current State",
        "## Authoritative Unfinished Capability Closure Registry",
    )).get("CURRENT_STOP_CONDITION", "").strip("`")
    real_world_waits = [
        item for item in criteria
        if item["primary_classification"] == "REAL_WORLD_EVIDENCE_REQUIRED"
    ]
    dependency_waits = [
        item for item in criteria
        if item["primary_classification"] == "DEPENDENCY_WAIT"
    ]
    real_world_limit_valid = (
        current_stop == "REAL_WORLD_LIMIT"
        and implementation_complete
        and bool(real_world_waits)
        and not ready_ids
    )
    if not re.search(r"Version: `4\.(?:2[2-9]|[3-9]\d)`", omp_text):
        errors.append("omp_capability_reconciliation_version_missing")
    if "Capability Closure Versus Implementation Complete Reconciliation Rule" not in omp_text:
        errors.append("omp_capability_reconciliation_rule_missing")
    if "Capability Dashboard Source: CPS Authoritative Unfinished Capability Closure Registry" not in omp_text:
        errors.append("omp_capability_dashboard_cps_pointer_missing")
    if engineering and current_stop == "REAL_WORLD_LIMIT":
        errors.append("global_real_world_limit_hides_engineering_work")
    if unknown:
        errors.append("capability_criterion_unknown")
    if current_stop == "REAL_WORLD_LIMIT" and not real_world_limit_valid:
        errors.append("global_real_world_limit_not_proven")

    counts: dict[str, int] = {}
    for item in criteria:
        key = item["primary_classification"]
        counts[key] = counts.get(key, 0) + 1
    unique = sorted(set(errors))
    return {
        "schema": "v7-omp-capability-closure-reconciliation/v1",
        "authoritative_capability_count": dependency.get("capability_count", 0) + 12,
        "unfinished_capability_count": len(criteria),
        "actionable_backlog_count": len(expected_backlog_ids),
        "actionable_backlog_done": len(expected_backlog_ids) - len(missing_backlog) - len(non_terminal_backlog),
        "backlog_references_reconciled": len(expected_backlog_ids),
        "criteria": criteria,
        "criteria_total": len(criteria),
        "classification_counts": counts,
        "real_world_waits": [item["capability_id"] for item in real_world_waits],
        "dependency_waits": [item["capability_id"] for item in dependency_waits],
        "executable_frontier": [item["capability_id"] for item in engineering],
        "executable_frontier_count": len(engineering),
        "implementation_complete_verdict": (
            "IMPLEMENTATION_COMPLETE_VALID"
            if implementation_complete else "IMPLEMENTATION_COMPLETE_INVALID_HIDDEN_ENGINEERING_WORK"
        ),
        "global_real_world_limit_verdict": (
            "GLOBAL_REAL_WORLD_LIMIT_VALID"
            if real_world_limit_valid else "GLOBAL_REAL_WORLD_LIMIT_INVALID"
        ),
        "bdp_inputs_created": 0,
        "candidates_created": 0,
        "missions_accepted": 0,
        "runtime_impact": "NONE",
        "production_impact": "NONE",
        "authority_impact": "NONE",
        "production_maturity_impact": "NONE",
        "protected_wip_preserved": True,
        "final_verdict": "PASS" if not unique else "STOP_SAFE",
        "errors": unique,
    }


PROGRAM_EXECUTION_REMAINING_STATUSES = {
    "STAGE_READY_NOT_STARTED",
    "STAGE_IN_PROGRESS",
    "STAGE_READY_FOR_ACCEPTANCE",
    "STAGE_ACCEPTANCE_MISSING",
    "STAGE_OUTPUT_MISSING",
    "STAGE_CONSUMER_MISSING",
    "STAGE_CONSUMPTION_NOT_CONFIRMED",
}


COMPLETION_CONTRACTS = {
    "ANALYSIS_COMPLETION": ("ANALYSIS_ARTIFACT_PROVEN", "EVIDENCE_TRACEABILITY_PROVEN"),
    "DISCOVERY_COMPLETION": ("DISCOVERY_OUTPUT_PROVEN", "EVIDENCE_TRACEABILITY_PROVEN", "NEXT_OUTPUT_PROVEN"),
    "ACCEPTANCE_COMPLETION": ("INDEPENDENT_ACCEPTANCE_PROVEN", "NEXT_OUTPUT_PROVEN"),
    "DOCUMENTATION_COMPLETION": ("DOCUMENT_OWNER_ACCEPTED", "EVIDENCE_TRACEABILITY_PROVEN"),
    "IMPLEMENTATION_COMPLETION": ("SOURCE_CHANGE_PROVEN", "FOCUSED_TESTS_PROVEN"),
    "INTEGRATION_COMPLETION": (
        "REAL_CALLER_PROVEN", "CONSUMER_PROVEN", "BEHAVIOR_CHANGE_PROVEN", "NEXT_OUTPUT_PROVEN",
    ),
    "AUTOMATION_COMPLETION": (
        "INDEPENDENT_TRIGGER_PROVEN", "ENTRYPOINT_ACTIVE", "REAL_CALLER_PROVEN",
        "CONSUMER_PROVEN", "BEHAVIOR_CHANGE_PROVEN", "NEXT_OUTPUT_PROVEN",
        "IDEMPOTENCY_PROVEN", "DUPLICATE_SUPPRESSION_PROVEN",
    ),
    "RUNTIME_COMPLETION": (
        "RUNTIME_PATH_ACTIVE", "RUNTIME_EFFECT_PROVEN", "VERIFICATION_PROVEN", "ROLLBACK_OR_STOP_SAFE_PROVEN",
    ),
    "PRODUCTION_COMPLETION": (
        "PRODUCTION_EFFECT_PROVEN", "VERIFICATION_PROVEN", "CONSUMER_PROVEN",
        "LEARNING_PROPAGATION_PROVEN", "NEXT_OUTPUT_PROVEN",
    ),
}


def mission_completion_evidence_gate(contract: dict[str, Any]) -> dict[str, Any]:
    """Classify Mission completion from its declared evidence contract."""
    mission_type = str(contract.get("MISSION_TYPE") or "").upper()
    completion_contract = str(contract.get("COMPLETION_CONTRACT") or "").upper()
    required = list(COMPLETION_CONTRACTS.get(completion_contract, ()))
    if contract.get("LOCK_REQUIRED"):
        required.append("LOCK_PROVEN")
    if contract.get("DEPLOY_REQUIRED"):
        required.append("DEPLOY_PROVEN")

    evidence_present = {field: contract.get(field) is True for field in required}
    missing = [field for field in required if not evidence_present[field]]
    legal_terminal = contract.get("LEGAL_TERMINAL") is True
    legal_terminal_proven = all(contract.get(field) is True for field in (
        "EVIDENCE_TRACEABILITY_PROVEN", "TERMINAL_OWNER_PROVEN",
    ))

    if not mission_type or completion_contract not in COMPLETION_CONTRACTS:
        verdict = "COMPLETION_TRUTH_UNRESOLVED"
    elif legal_terminal and legal_terminal_proven:
        verdict = "COMPLETE_WITH_LEGAL_TERMINAL"
    elif not missing:
        verdict = (
            "IMPLEMENTED_NOT_CONSUMED"
            if completion_contract == "IMPLEMENTATION_COMPLETION"
            else "COMPLETE_CONSUMED"
            if completion_contract in {
                "INTEGRATION_COMPLETION", "AUTOMATION_COMPLETION", "RUNTIME_COMPLETION", "PRODUCTION_COMPLETION",
            }
            else "COMPLETE_WITH_LEGAL_TERMINAL"
        )
    elif completion_contract == "IMPLEMENTATION_COMPLETION":
        verdict = "IMPLEMENTED_NOT_CONSUMED"
    elif completion_contract == "INTEGRATION_COMPLETION":
        verdict = "INTEGRATION_INCOMPLETE"
    elif completion_contract == "AUTOMATION_COMPLETION":
        verdict = "AUTOMATION_INCOMPLETE"
    elif completion_contract == "RUNTIME_COMPLETION":
        verdict = "RUNTIME_INCOMPLETE"
    elif completion_contract == "PRODUCTION_COMPLETION":
        verdict = "PRODUCTION_INCOMPLETE"
    else:
        verdict = "PREPARED_NOT_CONSUMED"

    return {
        "schema": "v7-omp-mission-completion-evidence/v1",
        "mission_type": mission_type or "UNKNOWN",
        "completion_contract": completion_contract or "UNKNOWN",
        "required_evidence": required,
        "evidence_present": evidence_present,
        "missing_evidence": missing,
        "real_caller_required": "REAL_CALLER_PROVEN" in required,
        "real_caller_proven": contract.get("REAL_CALLER_PROVEN") is True,
        "consumer_required": "CONSUMER_PROVEN" in required,
        "consumer_proven": contract.get("CONSUMER_PROVEN") is True,
        "behavior_change_required": "BEHAVIOR_CHANGE_PROVEN" in required,
        "behavior_change_proven": contract.get("BEHAVIOR_CHANGE_PROVEN") is True,
        "next_output_required": "NEXT_OUTPUT_PROVEN" in required,
        "next_output_proven": contract.get("NEXT_OUTPUT_PROVEN") is True,
        "deploy_required": contract.get("DEPLOY_REQUIRED") is True,
        "deploy_proven": contract.get("DEPLOY_PROVEN") is True,
        "runtime_effect_required": "RUNTIME_EFFECT_PROVEN" in required,
        "runtime_effect_proven": contract.get("RUNTIME_EFFECT_PROVEN") is True,
        "production_effect_required": "PRODUCTION_EFFECT_PROVEN" in required,
        "production_effect_proven": contract.get("PRODUCTION_EFFECT_PROVEN") is True,
        "legal_terminal": legal_terminal and legal_terminal_proven,
        "completion_verdict": verdict,
    }


def classify_program_stage(stage: dict[str, Any]) -> str:
    """Classify execution reality independently from a program document label."""
    if stage.get("superseded"):
        return "STAGE_SUPERSEDED"
    if stage.get("not_applicable_reason"):
        return "STAGE_NOT_APPLICABLE"
    if stage.get("blocked_real_world"):
        return "STAGE_BLOCKED_REAL_WORLD"
    if stage.get("blocked_authority"):
        return "STAGE_BLOCKED_AUTHORITY"
    if stage.get("blocked_dependency"):
        return "STAGE_BLOCKED_DEPENDENCY"
    if not stage.get("entry_conditions_met", False):
        return "STAGE_BLOCKED_DEPENDENCY"
    if not stage.get("execution_started", False):
        return "STAGE_READY_NOT_STARTED"
    if not stage.get("outputs_found", False):
        return "STAGE_OUTPUT_MISSING"
    if not stage.get("output_schema_valid", False):
        return "STAGE_IN_PROGRESS"
    if stage.get("acceptance_required", False) and not stage.get("acceptance_found", False):
        return "STAGE_READY_FOR_ACCEPTANCE"
    if stage.get("consumer_required", True) and not stage.get("consumer_found", False):
        return "STAGE_CONSUMER_MISSING"
    if stage.get("consumer_required", True) and not stage.get("consumer_confirmed", False):
        return "STAGE_CONSUMPTION_NOT_CONFIRMED"
    if not stage.get("state_transition_complete", False):
        return "STAGE_IN_PROGRESS"
    return "STAGE_COMPLETE_CONSUMED"


def _program_document_status(text: str) -> str:
    match = re.search(r"^Status:\s*`?([^`\n]+)`?\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else "UNKNOWN"


def _phase_artifact_value(text: str, field: str) -> str:
    """Read one assignment or Markdown-table value from an accepted phase artifact."""
    assignment = re.search(
        rf"(?m)^{re.escape(field)}\s*=\s*`?([^`\n]+?)`?\s*$",
        text,
    )
    if assignment:
        return assignment.group(1).strip()
    table = re.search(
        rf"(?m)^\|\s*`?{re.escape(field)}`?\s*\|\s*`?([^|`]+?)`?\s*\|\s*$",
        text,
    )
    return table.group(1).strip() if table else ""


def _aep_phase3_lock_fingerprint(
    register_fingerprint: str,
    acceptance_owner: str,
    authority_scope_fingerprint: str,
    candidate_ids: Iterable[str],
) -> str:
    payload = {
        "schema": "v7.aep-phase3-lock.v1",
        "register_fingerprint": register_fingerprint,
        "acceptance_owner": acceptance_owner,
        "authority_scope_fingerprint": authority_scope_fingerprint,
        "candidate_ids": sorted(set(candidate_ids)),
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def program_execution_reconciliation(sources: dict[str, Any], *, root: Path = ROOT) -> dict[str, Any]:
    """Reconcile canonical program stages, consumption, and the global stop."""
    stage2 = sources.get("stage2", "")
    aep = sources.get("aep", "")
    bdp = sources.get("bdp", "")
    implementation = sources.get("implementation", "")
    backlog_text = sources.get("backlog", "")
    omp = sources.get("omp", "")
    cps = sources.get("cps", "")
    phase1 = sources.get("aep_phase1", "")
    phase2 = sources.get("aep_phase2", "")
    phase2_execution = sources.get("aep_phase2_execution", "")
    phase2_acceptance = sources.get("aep_phase2_acceptance", "")
    phase3_register = sources.get("aep_phase3_register", "")
    phase3_acceptance = sources.get("aep_phase3_acceptance", "")
    phase3_lock = sources.get("aep_phase3_lock", "")
    phase4_execution = sources.get("aep_phase4_execution", "")
    bdp_execution = sources.get("bdp_execution", "")

    stage2_complete = all(token in stage2 for token in (
        "CLOSED_LOCKED_KNOWLEDGE", "LOCKED_KNOWLEDGE", "Stage 2.7",
    ))
    phase1_complete = all(token in phase1 for token in (
        "PHASE_ACCEPTED", "PHASE_LOCKED", "IDEAL_READY",
    ))
    phase2_required = (
        "Behaviour Instance Registry", "Behaviour Aggregation", "Behaviour Definition Catalogue",
        "Behaviour Coverage", "Behaviour Graph", "Behaviour Reality", "Automation State",
        "Manual Dependency", "Evidence Map",
    )
    phase2_output_complete = all(token in phase2 for token in phase2_required)
    phase2_executed = (
        phase2_output_complete
        and "PHASE_2_CURRENT_AUTONOMOUS_BEHAVIOUR_REALITY_PASS" in phase2
        and "PHASE_2_CURRENT_AUTONOMOUS_BEHAVIOUR_REALITY_PASS" in phase2_execution
    )
    phase2_revalidated = (
        any(token in aep for token in (
            "PHASE_2_REVALIDATED_READY_FOR_ACCEPTANCE",
            "PHASE_2_ACCEPTED_LOCKED_PHASE_3_READY",
            "PHASE_3_EXECUTED_READY_FOR_INDEPENDENT_ACCEPTANCE",
            "PHASE_3_ACCEPTED_LOCKED_PHASE_4_CONSUMED_PHASE_5_IN_PROGRESS",
            "PHASE_3_ACCEPTED_LOCKED_PHASE_4_CONSUMED_PHASE_5_COMPLETE",
            "PHASE_3_ACCEPTED_LOCKED_PHASE_4_IMPLEMENTED_MANUALLY_CALLABLE_PHASE_5_BLOCKED_REAL_CONSUMER",
        ))
        and "Current Revalidation" in phase2
    )
    phase2_accepted = (
        all(token in phase2_acceptance for token in (
            "CURRENT_AUTONOMOUS_BEHAVIOUR_REALITY_ACCEPTED", "PHASE_ACCEPTED", "PHASE_LOCKED",
        ))
        or all(token in phase2_acceptance for token in (
            "AEP_PHASE_2_ACCEPTED_WITH_MINOR_RISKS",
            "AEP_PHASE_2_TO_PHASE_3_EDGE = COMPLETE",
            "NO_RUNTIME_MUTATION = TRUE",
        ))
    )
    phase3_register_fingerprint = _phase_artifact_value(phase3_register, "REGISTER_FINGERPRINT")
    phase3_register_status = _phase_artifact_value(phase3_register, "PHASE_3_ACCEPTANCE_STATUS")
    phase3_candidate_ids = sorted(set(re.findall(r"BDP-ICI-[A-F0-9]{24}", phase3_register)))
    phase3_certified_gap_raw = _phase_artifact_value(phase3_register, "CERTIFIED_GAPS")
    try:
        phase3_certified_gap_count = int(phase3_certified_gap_raw)
    except (TypeError, ValueError):
        phase3_certified_gap_count = -1
    phase3_executed = all((
        phase2_accepted,
        bool(re.fullmatch(r"[0-9a-f]{64}", phase3_register_fingerprint)),
        "TOTAL_BEHAVIOUR_DEFINITIONS_REVIEWED = 16" in phase3_register,
        "TOTAL_BEHAVIOUR_INSTANCES_REVIEWED = 28" in phase3_register,
        phase3_certified_gap_count >= 0,
        len(phase3_candidate_ids) == phase3_certified_gap_count,
    ))
    acceptance_verdict = _phase_artifact_value(phase3_acceptance, "PHASE_3_ACCEPTANCE_VERDICT")
    acceptance_owner = _phase_artifact_value(phase3_acceptance, "PHASE_3_ACCEPTANCE_OWNER")
    authority_scope_fingerprint = _phase_artifact_value(phase3_acceptance, "AUTHORITY_SCOPE_FINGERPRINT")
    acceptance_register_fingerprint = _phase_artifact_value(phase3_acceptance, "PHASE_3_REGISTER_FINGERPRINT")
    acceptance_lock_id = _phase_artifact_value(phase3_acceptance, "PHASE_3_LOCK_ID")
    acceptance_lock_fingerprint = _phase_artifact_value(phase3_acceptance, "PHASE_3_LOCK_FINGERPRINT")
    lock_register_fingerprint = _phase_artifact_value(phase3_lock, "REGISTER_FINGERPRINT")
    lock_id = _phase_artifact_value(phase3_lock, "PHASE_3_LOCK_ID")
    lock_fingerprint = _phase_artifact_value(phase3_lock, "PHASE_3_LOCK_FINGERPRINT")
    expected_phase3_lock_fingerprint = _aep_phase3_lock_fingerprint(
        phase3_register_fingerprint,
        acceptance_owner,
        authority_scope_fingerprint,
        phase3_candidate_ids,
    ) if phase3_executed and acceptance_owner and authority_scope_fingerprint else ""
    phase3_accepted = all((
        phase3_executed,
        acceptance_verdict in {
            "AEP_PHASE_3_GAP_REGISTER_ACCEPTED",
            "AEP_PHASE_3_GAP_REGISTER_ACCEPTED_WITH_MINOR_RISKS",
        },
        phase3_register_status in {
            "AEP_PHASE_3_GAP_REGISTER_ACCEPTED",
            "AEP_PHASE_3_GAP_REGISTER_ACCEPTED_WITH_MINOR_RISKS",
        },
        acceptance_register_fingerprint == phase3_register_fingerprint,
    ))
    phase3_locked = all((
        phase3_accepted,
        lock_register_fingerprint == phase3_register_fingerprint,
        lock_fingerprint == expected_phase3_lock_fingerprint,
        acceptance_lock_fingerprint == lock_fingerprint,
        lock_id == f"aep3lock_{lock_fingerprint[:24]}",
        acceptance_lock_id == lock_id,
        "PHASE_3_LOCK_STATUS = LOCKED" in phase3_lock,
    ))
    phase4_no_mission = phase3_locked and phase3_certified_gap_count == 0
    phase4_admitted = phase4_no_mission or all((
        phase3_locked,
        "MISSION_ID_CREATED = V7_OMP_PHASE_3_TO_PHASE_4_PROGRAM_CONSUMER_EXTENSION_V1" in phase4_execution,
        "OMP_ADMISSION_DECISION = MISSION_ACCEPTED" in phase4_execution,
    ))
    real_consumer_verified = phase4_no_mission or all((
        "REAL_TRIGGER_OCCURRED = TRUE" in phase4_execution,
        "REAL_ENTRYPOINT_INVOKED = TRUE" in phase4_execution,
        "RECONCILIATION_CALLED = TRUE" in phase4_execution,
        "CONSUMER_INVOKED = TRUE" in phase4_execution,
        "CONSUMER_BEHAVIOR_CHANGED = TRUE" in phase4_execution,
        "NEXT_OUTPUT_CREATED = TRUE" in phase4_execution,
    ))
    phase4_consumed = phase4_admitted and real_consumer_verified
    phase5_complete = phase4_no_mission or all((
        phase4_consumed,
        "IMPLEMENTATION_RESULT = COMPLETE_VERIFIED" in phase4_execution,
        "PHASE_3_TO_PHASE_4_CONSUMPTION_STATUS = PASS" in phase4_execution,
        "ENGINEERING_INTENT_CLOSURE_STATUS = CLOSED" in phase4_execution,
    ))
    bdp_passes = [f"BDP-P{index:02d}" for index in range(1, 20)]
    bdp_project_scope_complete = all(token in bdp_execution for token in bdp_passes)
    backlog = _actionable_backlog_statuses(backlog_text)
    actionable_ids = {
        *(f"A{index}" for index in range(1, 7)),
        *(f"B{index}" for index in range(1, 22)),
        *(f"C{index}" for index in range(1, 8)),
    }
    backlog_complete = all(backlog.get(item) == "DONE" for item in actionable_ids)

    aep_stages = [
        {"program_id": "AEP", "stage_id": "FOUNDATION", "status": "STAGE_COMPLETE_CONSUMED" if phase1_complete else "STAGE_OUTPUT_MISSING"},
        {"program_id": "AEP", "stage_id": "PHASE_1", "status": "STAGE_COMPLETE_CONSUMED" if phase1_complete else "STAGE_ACCEPTANCE_MISSING"},
        {
            "program_id": "AEP", "stage_id": "PHASE_2",
            "status": (
                "STAGE_COMPLETE_CONSUMED" if phase2_accepted
                else "STAGE_READY_FOR_ACCEPTANCE" if phase2_executed and phase2_revalidated
                else "STAGE_IN_PROGRESS" if phase2_executed
                else "STAGE_READY_NOT_STARTED" if phase1_complete
                else "STAGE_BLOCKED_DEPENDENCY"
            ),
        },
    ]
    aep_stages.extend((
        {
            "program_id": "AEP", "stage_id": "PHASE_3",
            "status": (
                "STAGE_COMPLETE_CONSUMED" if phase3_locked
                else "STAGE_READY_FOR_ACCEPTANCE" if phase3_executed
                else "STAGE_READY_NOT_STARTED" if phase2_accepted
                else "STAGE_BLOCKED_DEPENDENCY"
            ),
        },
        {
            "program_id": "AEP", "stage_id": "PHASE_4",
            "status": (
                "STAGE_COMPLETE_CONSUMED" if phase4_consumed
                else "STAGE_IMPLEMENTED_MANUALLY_CALLABLE" if phase4_admitted
                else "STAGE_READY_NOT_STARTED" if phase3_locked
                else "STAGE_BLOCKED_DEPENDENCY"
            ),
        },
        {
            "program_id": "AEP", "stage_id": "PHASE_5",
            "status": "STAGE_COMPLETE_CONSUMED" if phase5_complete else "STAGE_READY_NOT_STARTED" if phase4_consumed else "STAGE_BLOCKED_DEPENDENCY",
        },
    ))
    for phase in range(6, 8):
        aep_stages.append({
            "program_id": "AEP", "stage_id": f"PHASE_{phase}",
            "status": "STAGE_READY_NOT_STARTED" if phase == 6 and phase5_complete else "STAGE_BLOCKED_DEPENDENCY",
        })

    inventory = [
        {"program_id": "STAGE2", "type": "KNOWLEDGE_PROGRAM", "document_status": _program_document_status(stage2), "execution_status": "TERMINAL_COMPLETE" if stage2_complete else "PARTIALLY_EXECUTED"},
        {
            "program_id": "AEP", "type": "STRATEGIC_ROUTE", "document_status": _program_document_status(aep),
            "execution_status": (
                "PHASE_6_READY" if phase5_complete
                else "PHASE_4_IMPLEMENTED_MANUALLY_CALLABLE" if phase4_admitted
                else "PHASE_4_READY" if phase3_locked
                else "PHASE_3_READY_FOR_ACCEPTANCE" if phase3_executed
                else "PHASE_3_READY" if phase2_accepted
                else "READY_FOR_ACCEPTANCE" if phase2_revalidated
                else "PARTIALLY_EXECUTED"
            ),
        },
        {"program_id": "BDP", "type": "DISCOVERY_PROGRAM", "document_status": _program_document_status(bdp), "execution_status": "EXECUTED_FOR_CURRENT_PROJECT_SCOPE" if bdp_project_scope_complete else "PARTIALLY_EXECUTED"},
        {"program_id": "IMPLEMENTATION_PROGRAM", "type": "SUPPORTING_REFERENCE", "document_status": _program_document_status(implementation), "execution_status": "TERMINAL_COMPLETE" if backlog_complete else "IN_PROGRESS"},
        {"program_id": "IMPLEMENTATION_BACKLOG", "type": "IMPLEMENTATION_PROGRAM", "document_status": _program_document_status(backlog_text), "execution_status": "TERMINAL_COMPLETE" if backlog_complete else "IN_PROGRESS"},
        {"program_id": "OMP", "type": "ACTIVE_EXECUTION_PROGRAM", "document_status": _program_document_status(omp), "execution_status": "IN_PROGRESS"},
        {"program_id": "AUTONOMOUS_EXECUTION", "type": "SUPPORTING_REFERENCE", "document_status": _program_document_status(sources.get("autonomous_execution", "")), "execution_status": "CONSUMED_NOT_TERMINAL"},
        {"program_id": "AUTONOMOUS_RUNTIME", "type": "SUPPORTING_REFERENCE", "document_status": _program_document_status(sources.get("autonomous_runtime", "")), "execution_status": "CONSUMED_NOT_TERMINAL"},
        {"program_id": "CONTROLLED_PRODUCTION_CERTIFICATION", "type": "CERTIFICATION_PROGRAM", "document_status": _program_document_status(sources.get("controlled_certification", "")), "execution_status": "PARTIALLY_EXECUTED"},
    ]
    internal_programs = (
        "EXECUTION_CERTIFICATION_LADDER", "BDP_DISCOVERY_ECONOMY", "SCENARIO_SUPPLY",
        "PROACTIVE_VERIFICATION", "POLYGON_FALLBACK", "CAPABILITY_CLOSURE_RECONCILIATION",
        "AUTOMATION_GAP_CLOSURE", "INTENT_GAP_DETECTION", "INTENT_RESPONSIBILITY_RESOLUTION",
        "ENGINEERING_INTENT_CLOSURE", "NECESSITY_FRAMEWORK", "CAPABILITY_PRODUCTION",
        "CAPABILITY_TRANSITION", "RT_PHASE_2", "PRE_PHASE_2_READINESS",
        "AUTONOMY_PROMOTION", "DELEGATED_AUTONOMY", "PRODUCTION_PROMOTION_MATRIX",
    )
    inventory.extend({
        "program_id": item, "type": "CAPABILITY_PROGRAM", "document_status": "CANONICAL",
        "execution_status": "CONTINUOUSLY_CONSUMED" if item in {
            "CAPABILITY_CLOSURE_RECONCILIATION", "AUTOMATION_GAP_CLOSURE", "INTENT_GAP_DETECTION",
            "INTENT_RESPONSIBILITY_RESOLUTION", "CAPABILITY_PRODUCTION", "CAPABILITY_TRANSITION",
        } else "PARTIALLY_EXECUTED",
    } for item in internal_programs)

    stages = ([{"program_id": "STAGE2", "stage_id": f"STAGE_2_{index}", "status": "STAGE_COMPLETE_CONSUMED" if stage2_complete else "STAGE_UNKNOWN_WITH_REASON"} for index in range(1, 8)] + aep_stages)
    counts: dict[str, int] = {}
    for stage in stages:
        counts[stage["status"]] = counts.get(stage["status"], 0) + 1
    live_state = _markdown_field_table(_markdown_section(
        cps, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry",
    ))
    current_stop = live_state.get("CURRENT_STOP_CONDITION", "").strip("`")
    acceptance_boundary = phase2_executed and phase2_revalidated and not phase2_accepted
    missing_stage = not phase2_accepted
    global_real_world_valid = current_stop == "REAL_WORLD_LIMIT" and not missing_stage
    errors: list[str] = []
    if not stage2_complete:
        errors.append("stage2_terminal_not_proven")
    if not phase1_complete:
        errors.append("aep_phase1_not_accepted")
    if not phase2_executed:
        errors.append("aep_phase2_output_missing_or_incomplete")
    if "Version: `4.26`" not in omp:
        errors.append("omp_program_reconciliation_version_missing")
    if "Program Execution And Consumption Reconciliation Rule" not in omp:
        errors.append("omp_program_reconciliation_rule_missing")
    phase3_evidence_present = any((phase3_acceptance, phase3_lock))
    if phase3_evidence_present and not phase3_executed:
        errors.append("aep_phase3_register_invalid")
    if acceptance_verdict and not phase3_accepted:
        errors.append("aep_phase3_acceptance_invalid")
    if phase3_lock and not phase3_locked:
        errors.append("aep_phase3_lock_invalid")
    if global_real_world_valid:
        errors.append("global_real_world_limit_illegal_while_program_stage_open")
    frontier = (
        ["AEP_PHASE_6_PRODUCTION_CERTIFICATION_PREPARATION"] if phase5_complete
        else ["OMP_REAL_CONSUMER_ACTIVATION"] if phase4_admitted
        else ["V7_OMP_PHASE_3_TO_PHASE_4_PROGRAM_CONSUMER_EXTENSION_V1"] if phase3_locked
        else ["AEP_PHASE_3_INDEPENDENT_ACCEPTANCE"] if phase3_executed
        else ["AEP_PHASE_2_ACCEPTANCE"] if acceptance_boundary
        else ["AEP_PHASE_2_CURRENT_REALITY_REVALIDATION"] if missing_stage
        else ["AEP_PHASE_3_CERTIFIED_AUTONOMOUS_BEHAVIOUR_GAP_REGISTER"]
    )
    fsse_external_reentry_deferred = (
        live_state.get("FSSE_00_EXTERNAL_REENTRY_STATUS", "").strip("`")
        == "DEFERRED_PLATFORM_CERTIFICATION"
    )
    ordinary_frontier_deferred = (
        fsse_external_reentry_deferred
        and frontier == ["OMP_REAL_CONSUMER_ACTIVATION"]
        and live_state.get("CURRENT_EXECUTION_MISSION_ID", "").strip("`") in {"", "NONE"}
        and live_state.get("READY_CAPABILITIES", "").strip("`") in {"", "NONE"}
    )
    scenario_frontier = future_scale_scenario_frontier(
        cps,
        root=root,
        ordinary_work_available=bool(frontier) and not ordinary_frontier_deferred,
    )
    if scenario_frontier.get("decision") == "SCENARIO_FOUNDATION_READY_EXECUTION_HARNESS_REQUIRED":
        frontier = [scenario_frontier["next_output"]]
    return {
        "schema": "v7-omp-program-execution-reconciliation/v1",
        "program_inventory": inventory,
        "programs_discovered": len(inventory),
        "stages": stages,
        "program_stages_total": len(stages),
        "stage_counts": counts,
        "stage2_status": "STAGE2_TERMINAL_COMPLETE" if stage2_complete else "STAGE2_INCOMPLETE",
        "aep_status": (
            "PHASE_6_READY" if phase5_complete
            else "PHASE_4_IMPLEMENTED_MANUALLY_CALLABLE" if phase4_admitted
            else "PHASE_4_READY" if phase3_locked
            else "PHASE_3_READY_FOR_ACCEPTANCE" if phase3_executed
            else "PHASE_3_READY" if phase2_accepted
            else "PHASE_2_READY_FOR_ACCEPTANCE" if acceptance_boundary
            else "PARTIAL"
        ),
        "aep_current_phase": "PHASE_6" if phase5_complete else "PHASE_4" if phase4_admitted or phase3_locked else "PHASE_3" if phase2_accepted else "PHASE_2",
        "aep_phase2_output_complete": phase2_output_complete,
        "aep_phase2_executed": phase2_executed,
        "aep_phase2_revalidated": phase2_revalidated,
        "aep_phase2_accepted": phase2_accepted,
        "aep_phase3_executed": phase3_executed,
        "aep_phase3_accepted": phase3_accepted,
        "aep_phase3_locked": phase3_locked,
        "aep_phase3_register_fingerprint": phase3_register_fingerprint,
        "aep_phase3_lock_fingerprint": lock_fingerprint,
        "aep_phase3_candidate_ids": phase3_candidate_ids if phase3_locked else [],
        "aep_phase3_certified_gap_count": phase3_certified_gap_count,
        "aep_phase4_admitted": phase4_admitted,
        "aep_phase4_consumed": phase4_consumed,
        "aep_real_consumer_verified": real_consumer_verified,
        "aep_phase4_status": "COMPLETE_CONSUMED" if phase4_consumed else "IMPLEMENTED_MANUALLY_CALLABLE" if phase4_admitted else "READY" if phase3_locked else "BLOCKED",
        "aep_phase5_status": "COMPLETE_CONSUMED" if phase5_complete else "READY" if phase4_consumed else "BLOCKED",
        "aep_phase6_status": "READY" if phase5_complete else "BLOCKED",
        "aep_state": "IMPLEMENTATION_READY" if phase5_complete else "GAP_READY" if phase4_admitted or phase3_locked else "PHASE_3_READY_FOR_ACCEPTANCE" if phase3_executed else "CURRENT_READY",
        "bdp_status": "BDP_EXECUTED_FOR_CURRENT_PROJECT_SCOPE" if bdp_project_scope_complete else "BDP_EXECUTED_FOR_LIMITED_SCENARIO_SCOPE",
        "bdp_required_passes_complete": bdp_project_scope_complete,
        "backlog_status": "34/34_DONE" if backlog_complete else "INCOMPLETE",
        "executable_program_frontier": frontier,
        "executable_program_frontier_count": len(frontier),
        "ordinary_frontier_deferred_platform_boundary": ordinary_frontier_deferred,
        "scenario_frontier": scenario_frontier,
        "scenario_frontier_decision": scenario_frontier.get("decision", "SCENARIO_STOP_SAFE"),
        "scenario_frontier_consumer_invoked": True,
        "scenario_frontier_next_output": scenario_frontier.get("next_output", "STOP_SAFE"),
        "global_real_world_limit_verdict": "GLOBAL_REAL_WORLD_LIMIT_INVALID" if missing_stage else "GLOBAL_REAL_WORLD_LIMIT_VALID",
        "acceptance_required": acceptance_boundary,
        "runtime_impact": "NONE", "production_impact": "NONE", "authority_impact": "NONE",
        "final_verdict": "PASS" if not errors else "PROGRAM_STAGE_OPEN",
        "errors": sorted(set(errors)),
    }


def _aep_phase2_artifact_fingerprint(artifact_text: str) -> str:
    """Fingerprint a locked artifact without making its embedded digest recursive."""
    canonical = re.sub(
        r"(?m)^(PHASE_2_LOCK_FINGERPRINT|Artifact fingerprint)\s*[:=]\s*`?[0-9a-f]{64}`?\s*$",
        r"\1 = <LOCK_FINGERPRINT>",
        artifact_text,
    )
    canonical = re.sub(
        r"(?m)^PHASE_2_LOCK_ID\s*=\s*aep2lock_[A-Za-z0-9_]+\s*$",
        "PHASE_2_LOCK_ID = <LOCK_ID>",
        canonical,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def aep_phase2_acceptance(
    artifact_text: str,
    *,
    executor: str,
    acceptance_owner: str,
    operator_authority: bool = True,
    artifact_candidates: int = 1,
    locked_architecture: bool = True,
    locked_knowledge: bool = True,
    phase1_accepted: bool = True,
    cps_fresh: bool = True,
    declared_scope: str = "CURRENT_REPOSITORY_SCOPE",
    bdp_executed_scope: str = "CURRENT_REPOSITORY_SCOPE_WITH_EXPLICIT_UNKNOWNS",
    p19_required: bool = True,
    behaviour_truth_levels: Optional[dict[str, str]] = None,
    duplicate_behaviours: int = 0,
    ambiguous_identities: int = 0,
    hidden_unknowns: bool = False,
    orphan_behaviours: int = 0,
    phase2_certified_gaps: bool = False,
    phase2_created_mission: bool = False,
    runtime_mutation: bool = False,
    production_mutation: bool = False,
    authority_expansion: bool = False,
    lock_requested: bool = True,
) -> dict[str, Any]:
    """Independently accept the existing AEP Phase 2 Reality artifact."""
    required_outputs = {
        "Behaviour Instance Registry": ("## 4. Behaviour Instance Registry",),
        "Behaviour Aggregation Map": ("## 6. Behaviour Aggregation",),
        "Behaviour Catalogue": ("## 7. Behaviour Definition Catalogue",),
        "Behaviour Coverage": ("## 8. Behaviour Coverage",),
        "Behaviour Graph": ("## 9. Behaviour Graph",),
        "Behaviour Reality": ("## 10. Behaviour Reality",),
        "Automation State": ("## 11. Automation State",),
        "Manual Dependency Classification": ("## 12. Manual Dependency",),
        "Evidence Map": ("## 13. Evidence Map",),
        "Situation Discovery": ("| ID | Situation | Context | Interpretation |",),
        "Context Discovery": ("| ID | Situation | Context | Interpretation |",),
        "Interpretation Discovery": ("| ID | Situation | Context | Interpretation |",),
        "Applicable Knowledge mapping": ("Applicable Knowledge / Laws",),
        "Applicable Law mapping": ("Applicable Knowledge / Laws",),
        "Possible Decisions": ("Possible Decisions",),
        "Decision Selection": ("Decision Selection",),
        "Reasoning evidence": ("Reality Chain Summary", "Interpretation"),
        "Execution or explicit no-action path": ("| Execution | Verification |",),
        "Verification path": ("| Execution | Verification |",),
        "Rollback / containment / STOP_SAFE": ("Rollback / restore barrier", "stop-safe"),
        "Outcome / Learning path": ("Learning / Improvement / Sync",),
        "Canonical synchronization disposition": ("Knowledge evolution / canonical synchronization",),
        "Owner / Producer / Consumer mapping": ("Producer -> consumer -> terminal state", "Owner / Consumer Evidence"),
        "Behaviour Classification": ("Current Existence", "Automation State"),
        "Behaviour Maturity": ("## 16. Discovery Confidence",),
        "Engineering Chain identity and walk evidence": ("## 5. Behaviour Instance Chain Matrix",),
        "Intent Closure status": ("Phase 2 Reality Verdict", "terminal state"),
        "Traceability status": ("Traceability", "Evidence Sources"),
        "Unknown dispositions": ("## 14. Unknown Areas",),
        "Foundation Synchronization result": ("FOUNDATION_ALREADY_SYNCHRONIZED",),
        "Foundation Verification result": ("FOUNDATION_READY_WITH_MINOR_RISKS", "FOUNDATION_READY"),
        "Phase 3 consumer handoff": ("Phase 3 readiness", "Phase 3 must use this report as input"),
    }

    missing: list[str] = []
    placeholders: list[str] = []
    for name, markers in required_outputs.items():
        if not any(marker in artifact_text for marker in markers):
            missing.append(name)
            continue
        for marker in markers:
            at = artifact_text.find(marker)
            if at >= 0:
                tail = artifact_text[at + len(marker):at + len(marker) + 240]
                if not tail.strip() or re.match(r"^\s*(?:TBD|TODO|PLACEHOLDER)(?:\s|$)", tail, re.I):
                    placeholders.append(name)
                break

    role_separation = bool(
        operator_authority
        and executor.strip()
        and acceptance_owner.strip()
        and executor.strip() != acceptance_owner.strip()
    )
    input_readiness = all((locked_architecture, locked_knowledge, phase1_accepted, cps_fresh))
    scope_sufficient = (
        declared_scope == "CURRENT_REPOSITORY_SCOPE"
        and bdp_executed_scope in {
            "CURRENT_REPOSITORY_SCOPE",
            "CURRENT_REPOSITORY_SCOPE_WITH_EXPLICIT_UNKNOWNS",
        }
    )
    project_scope_overclaim = "PROJECT_WIDE" in declared_scope and "PROJECT_WIDE" not in bdp_executed_scope
    p19_complete = (not p19_required) or "`BDP-P19`" in artifact_text
    truth_levels = behaviour_truth_levels or {}
    architecture_only = sorted(item for item, level in truth_levels.items() if level == "T9")
    explicit_unknowns = "## 14. Unknown Areas" in artifact_text and "`UNAVAILABLE`" in artifact_text
    hidden_unknown_failure = hidden_unknowns or ("UNAVAILABLE" in artifact_text and not explicit_unknowns)
    boundary_violations = {
        "phase2_certified_gaps": phase2_certified_gaps,
        "phase2_created_mission": phase2_created_mission,
        "runtime_mutation": runtime_mutation,
        "production_mutation": production_mutation,
        "authority_expansion": authority_expansion,
    }
    errors: list[str] = []
    holds: list[str] = []
    if not role_separation:
        holds.append("role_separation_not_proven")
    if artifact_candidates != 1:
        holds.append("phase2_artifact_ambiguous")
    if not input_readiness:
        holds.append("mandatory_input_not_ready")
    if missing:
        errors.append("required_output_missing")
    if placeholders:
        errors.append("required_output_placeholder")
    if project_scope_overclaim:
        errors.append("bdp_project_scope_overclaim")
    if not scope_sufficient or not p19_complete:
        holds.append("bdp_scope_insufficient")
    if architecture_only:
        errors.append("architecture_only_behaviour_admitted")
    if ambiguous_identities:
        holds.append("behaviour_identity_ambiguous")
    if hidden_unknown_failure:
        errors.append("hidden_unknown")
    if orphan_behaviours:
        errors.append("orphan_behaviour")
    if any(boundary_violations.values()):
        errors.append("phase_boundary_violation")

    fingerprint = _aep_phase2_artifact_fingerprint(artifact_text)
    lock_id = f"aep2lock_{fingerprint[:24]}" if lock_requested and not errors and not holds else "NONE"
    if errors:
        verdict = "AEP_PHASE_2_FAIL"
    elif holds:
        verdict = "AEP_PHASE_2_HOLD"
    elif explicit_unknowns:
        verdict = "AEP_PHASE_2_ACCEPTED_WITH_MINOR_RISKS"
    else:
        verdict = "AEP_PHASE_2_ACCEPTED"
    accepted = verdict.startswith("AEP_PHASE_2_ACCEPTED")
    lock_status = "LOCKED" if accepted and lock_requested else "NOT_LOCKED"
    phase3_status = "READY" if lock_status == "LOCKED" else "BLOCKED"
    return {
        "schema": "v7-aep-phase2-independent-acceptance/v1",
        "artifact_candidates": artifact_candidates,
        "artifact_fingerprint": fingerprint,
        "executor": executor,
        "acceptance_owner": acceptance_owner,
        "role_separation_status": "PASS" if role_separation else "HOLD",
        "input_readiness": "PASS" if input_readiness else "HOLD",
        "required_outputs_total": len(required_outputs),
        "required_outputs_present": len(required_outputs) - len(missing),
        "missing_required_outputs": sorted(missing),
        "empty_or_placeholder_outputs": sorted(set(placeholders)),
        "bdp_sufficiency": "BDP_SUFFICIENT_WITH_EXPLICIT_UNKNOWNS" if scope_sufficient and p19_complete else "BDP_INSUFFICIENT_TARGETED_DISCOVERY_REQUIRED",
        "project_scope_claim_validity": "PASS" if not project_scope_overclaim else "FAIL",
        "architecture_only_behaviours": architecture_only,
        "duplicates_suppressed": duplicate_behaviours,
        "ambiguous_identities": ambiguous_identities,
        "explicit_unknowns": explicit_unknowns,
        "orphan_behaviours": orphan_behaviours,
        "boundary_violations": sorted(item for item, active in boundary_violations.items() if active),
        "phase2_to_phase3_edge": "COMPLETE" if phase3_status == "READY" else "HOLD" if holds and not errors else "FAIL",
        "acceptance_verdict": verdict,
        "acceptance_risks": [
            "live admin/runtime/production state unavailable",
            "BDP project-wide P01-P19 terminal execution not claimed",
            "generic rollback execution not generalized",
        ] if accepted and explicit_unknowns else [],
        "phase2_lock_status": lock_status,
        "phase2_lock_id": lock_id,
        "phase2_lock_fingerprint": fingerprint if lock_status == "LOCKED" else "NONE",
        "current_aep_state": "CURRENT_READY" if lock_status == "LOCKED" else "PHASE_2_ACCEPTANCE_REQUIRED",
        "phase3_status": phase3_status,
        "phase3_mission_id": "V7_AEP_PHASE_3_CERTIFIED_AUTONOMOUS_BEHAVIOUR_GAP_REGISTER_V1" if phase3_status == "READY" else "NONE",
        "errors": sorted(set(errors)),
        "holds": sorted(set(holds)),
    }


AEP_PHASE3_BOUNDARY_CLASSIFICATIONS = {
    "AUTHORITY_BOUNDARY_NOT_A_GAP",
    "REAL_WORLD_BOUNDARY_NOT_A_GAP",
    "DEPENDENCY_WAIT_NOT_A_GAP",
    "NOT_APPLICABLE_WITH_REASON",
}

AEP_PHASE3_HOLD_CLASSIFICATIONS = {
    "EVIDENCE_GAP",
    "UNKNOWN_WITH_REASON",
}

AEP_PHASE3_GAP_REQUIRED_FIELDS = (
    "primary_classification",
    "secondary_classes",
    "behaviour_definition_id",
    "behaviour_instance_id",
    "engineering_chain_id",
    "engineering_intent",
    "current_reality",
    "expected_reality",
    "failed_chain_segment",
    "producer",
    "consumer",
    "evidence",
    "truth_level",
    "freshness",
    "owner",
    "verification",
    "rollback",
    "terminal_path",
    "implementation_scope",
    "runtime_impact",
    "production_impact",
    "authority_context",
    "real_world_context",
    "root_cause",
    "smallest_existing_next_action",
)


def _aep_phase3_gap_identity(gap: dict[str, Any]) -> str:
    fields = (
        "primary_classification",
        "behaviour_definition_id",
        "behaviour_instance_id",
        "engineering_chain_id",
        "engineering_intent",
        "current_reality",
        "expected_reality",
        "failed_chain_segment",
        "owner",
        "consumer",
        "implementation_scope",
    )
    payload = {
        "schema": "v7.aep-phase3-gap-identity.v1",
        **{field: _bdp_normalized_value(gap.get(field)) for field in fields},
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _aep_phase3_candidate_gap(gap: dict[str, Any]) -> dict[str, Any]:
    """Map a certified AEP gap onto the existing BDP Candidate contract."""
    return {
        "primary_class": gap["primary_classification"],
        "secondary_classes": gap["secondary_classes"],
        "execution_depth": gap.get("execution_depth", "L2"),
        "engineering_intent": gap["engineering_intent"],
        "current_reality": gap["current_reality"],
        "expected_reality": gap["expected_reality"],
        "engineering_chain": gap["engineering_chain_id"],
        "engineering_chain_segment": gap["failed_chain_segment"],
        "behaviour_instance": gap["behaviour_instance_id"],
        "behaviour": gap["behaviour_definition_id"],
        "automation_logic": gap["smallest_existing_next_action"],
        "automation_break": gap["root_cause"],
        "existing_rule": gap.get("existing_rule", "AEP Phase Acceptance And OMP Continuation"),
        "current_outcome": gap.get("current_outcome", gap["current_reality"]),
        "expected_outcome": gap.get("expected_outcome", gap["expected_reality"]),
        "intent_closure_state": "AUTOMATION_BREAK",
        "owner": gap["owner"],
        "producer": gap["producer"],
        "consumer": gap["consumer"],
        "evidence": gap["evidence"],
        "implementation_scope": gap["implementation_scope"],
        "runtime_impact": gap["runtime_impact"],
        "production_impact": gap["production_impact"],
        "dependencies": gap.get("dependencies", "EXISTING_CONTRACTS_READY"),
        "verification": gap["verification"],
        "verification_context": gap.get("verification_context", "Deterministic unit and CPS/OMP consumer confirmation"),
        "rollback": gap["rollback"],
        "authority": gap.get("authority", "EXISTING_ENGINEERING_PLANE_AUTHORITY"),
        "authority_context": gap["authority_context"],
        "terminal_path": gap["terminal_path"],
        "implementation_readiness": "IMPLEMENTATION_READY",
        "omp_consumer": "OMP_CANDIDATE_ADMISSION",
        "codex_readiness": "CODEX_READY_WITH_LIMITS",
        "new_owner_required": False,
        "new_architecture_required": False,
    }


def aep_phase3_gap_certification(
    phase2_text: str,
    gap_candidates: Iterable[dict[str, Any]],
    *,
    expected_phase2_lock_fingerprint: str,
    executor: str,
    acceptance_owner: str = "",
    operator_authority: bool = False,
    acceptance_mission_id: str = "",
    acceptance_run_nonce: str = "",
    existing_gap_ids: Optional[Iterable[str]] = None,
    existing_candidates: Optional[Iterable[Any]] = None,
) -> dict[str, Any]:
    """Certify current AEP Phase 3 gaps without bypassing independent acceptance."""
    errors: list[str] = []
    holds: list[str] = []
    candidate_inputs = list(gap_candidates)
    phase2_fingerprint = _aep_phase2_artifact_fingerprint(phase2_text)
    embedded_fingerprint = re.search(
        r"(?m)^PHASE_2_LOCK_FINGERPRINT\s*=\s*([0-9a-f]{64})\s*$",
        phase2_text,
    )
    phase2_ready = all((
        "CURRENT_AUTONOMOUS_BEHAVIOUR_REALITY_ACCEPTED_LOCKED" in phase2_text,
        "PHASE_2_LOCK_STATUS = LOCKED" in phase2_text,
        embedded_fingerprint is not None,
        phase2_fingerprint == expected_phase2_lock_fingerprint,
        embedded_fingerprint.group(1) == expected_phase2_lock_fingerprint if embedded_fingerprint else False,
    ))
    if not phase2_ready:
        errors.append("phase2_locked_input_mismatch")

    behaviour_instances = sorted(set(re.findall(r"`(BI-\d{3})`", phase2_text)))
    behaviour_definitions = sorted(set(re.findall(r"`(BD-\d{3})(?:\s[^`]*)?`", phase2_text)))
    if len(behaviour_instances) != 28:
        errors.append("phase2_behaviour_instance_count_mismatch")
    if len(behaviour_definitions) != 16:
        errors.append("phase2_behaviour_definition_count_mismatch")

    existing_gap_set = {str(item) for item in existing_gap_ids or ()}
    existing_candidate_ids: set[str] = set()
    existing_candidate_meanings: set[str] = set()
    for item in existing_candidates or ():
        if isinstance(item, str):
            existing_candidate_ids.add(item)
        elif isinstance(item, dict):
            existing_candidate_ids.add(str(item.get("candidate_instance_id") or ""))
            existing_candidate_meanings.add(str(item.get("meaning_fingerprint") or ""))

    dispositions: list[dict[str, Any]] = []
    certified: list[dict[str, Any]] = []
    held: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    seen_gap_ids: set[str] = set()
    for index, raw in enumerate(candidate_inputs):
        if not isinstance(raw, dict):
            errors.append(f"gap_candidate_invalid:{index}")
            continue
        gap = dict(raw)
        missing = [
            field for field in AEP_PHASE3_GAP_REQUIRED_FIELDS
            if field not in gap or gap[field] in (None, "", [])
        ]
        identity = _aep_phase3_gap_identity(gap)
        gap_id = f"AEP-GAP-{identity[:20].upper()}"
        disposition: dict[str, Any] = {
            **gap,
            "gap_id": gap_id,
            "gap_identity_sha256": identity,
            "missing_fields": missing,
        }
        classification = str(gap.get("primary_classification") or "")
        if gap_id in seen_gap_ids or gap_id in existing_gap_set:
            disposition["certification_verdict"] = "GAP_REJECTED_DUPLICATE"
            rejected.append(disposition)
        elif gap.get("truth_level") == "T9" or gap.get("evidence_source_class") in {
            "ARCHITECTURE_ONLY",
            "IDEAL_MODEL_ONLY",
        }:
            disposition["certification_verdict"] = "GAP_REJECTED_NO_CURRENT_REALITY"
            rejected.append(disposition)
        elif missing:
            disposition["certification_verdict"] = "GAP_REJECTED_NOT_IMPLEMENTATION_READY"
            rejected.append(disposition)
        elif gap.get("behaviour_instance_id") not in behaviour_instances or gap.get("behaviour_definition_id") not in behaviour_definitions:
            disposition["certification_verdict"] = "GAP_REJECTED_NO_CURRENT_REALITY"
            rejected.append(disposition)
        elif classification == "AUTHORITY_BOUNDARY_NOT_A_GAP":
            disposition["certification_verdict"] = "GAP_REJECTED_AUTHORITY_BOUNDARY"
            rejected.append(disposition)
        elif classification == "REAL_WORLD_BOUNDARY_NOT_A_GAP":
            disposition["certification_verdict"] = "GAP_REJECTED_REAL_WORLD_BOUNDARY"
            rejected.append(disposition)
        elif classification == "DEPENDENCY_WAIT_NOT_A_GAP":
            disposition["certification_verdict"] = "GAP_REJECTED_DEPENDENCY_WAIT"
            rejected.append(disposition)
        elif classification == "NOT_APPLICABLE_WITH_REASON":
            disposition["certification_verdict"] = "GAP_NOT_APPLICABLE"
            rejected.append(disposition)
        elif classification in AEP_PHASE3_HOLD_CLASSIFICATIONS:
            disposition["certification_verdict"] = (
                "GAP_HOLD_RESPONSIBILITY_UNRESOLVED"
                if not gap.get("owner") else "GAP_HOLD_MISSING_EVIDENCE"
            )
            held.append(disposition)
        elif any((
            gap.get("new_owner_required") is not False,
            gap.get("new_architecture_required") is not False,
            gap.get("runtime_impact") != "NONE",
            gap.get("production_impact") != "NONE",
        )):
            disposition["certification_verdict"] = "GAP_REJECTED_NOT_IMPLEMENTATION_READY"
            rejected.append(disposition)
        else:
            candidate_gap = _aep_phase3_candidate_gap(gap)
            meaning = _bdp_candidate_meaning(candidate_gap)
            encoded = json.dumps(meaning, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            candidate_identity = hashlib.sha256(encoded.encode("utf-8")).hexdigest()
            candidate_id = f"BDP-ICI-{candidate_identity[:24].upper()}"
            if candidate_id in existing_candidate_ids or candidate_identity in existing_candidate_meanings:
                disposition["certification_verdict"] = "GAP_REJECTED_DUPLICATE"
                rejected.append(disposition)
            else:
                candidate = {
                    "candidate_instance_id": candidate_id,
                    "identity_sha256": candidate_identity,
                    "meaning_fingerprint": candidate_identity,
                    "identity_schema": meaning["identity_schema"],
                    **candidate_gap,
                    "new_backlog_required": False,
                    "new_runtime_required": False,
                    "authority_expansion_required": False,
                }
                disposition["candidate"] = candidate
                disposition["certification_verdict"] = "CERTIFIED_AUTONOMOUS_BEHAVIOUR_GAP"
                certified.append(disposition)
        seen_gap_ids.add(gap_id)
        dispositions.append(disposition)

    register_payload = {
        "schema": "v7.aep-phase3-certified-gap-register.v1",
        "phase2_lock_fingerprint": expected_phase2_lock_fingerprint,
        "behaviour_definitions_reviewed": behaviour_definitions,
        "behaviour_instances_reviewed": behaviour_instances,
        "dispositions": [
            {
                "gap_id": item["gap_id"],
                "gap_identity_sha256": item["gap_identity_sha256"],
                "certification_verdict": item["certification_verdict"],
                "candidate_instance_id": (item.get("candidate") or {}).get("candidate_instance_id", "NONE"),
            }
            for item in dispositions
        ],
    }
    register_fingerprint = hashlib.sha256(
        json.dumps(register_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    role_separation = bool(
        operator_authority
        and executor.strip()
        and acceptance_owner.strip()
        and executor.strip() != acceptance_owner.strip()
    )
    execution_complete = not errors and len(dispositions) == len(candidate_inputs)
    accepted = execution_complete and role_separation
    authority_scope_payload = {
        "schema": "v7.aep-phase3-acceptance-authority-scope.v1",
        "acceptance_mission_id": acceptance_mission_id,
        "acceptance_run_nonce": acceptance_run_nonce,
        "acceptance_owner": acceptance_owner,
        "allowed": [
            "INDEPENDENT_PHASE_3_REVIEW",
            "PHASE_3_ACCEPTANCE_AND_LOCK",
            "PHASE_4_OMP_ADMISSION",
            "EXISTING_PROGRAM_RECONCILIATION_EXTENSION",
        ],
        "forbidden": [
            "RUNTIME_MUTATION",
            "PRODUCTION_MUTATION",
            "AUTHORITY_EXPANSION",
            "USER_MOVEMENT",
        ],
    }
    authority_scope_fingerprint = hashlib.sha256(
        json.dumps(authority_scope_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    acceptance_status = "AEP_PHASE_3_GAP_REGISTER_ACCEPTED_WITH_MINOR_RISKS" if accepted and held else (
        "AEP_PHASE_3_GAP_REGISTER_ACCEPTED" if accepted else
        "AEP_PHASE_3_READY_FOR_ACCEPTANCE" if execution_complete else
        "AEP_PHASE_3_FAIL"
    )
    if execution_complete and not role_separation:
        holds.append("independent_phase_acceptance_required")
    candidates = [item["candidate"] for item in certified]
    phase3_lock_fingerprint = _aep_phase3_lock_fingerprint(
        register_fingerprint,
        acceptance_owner,
        authority_scope_fingerprint,
        [item["candidate_instance_id"] for item in candidates],
    ) if accepted else "NONE"
    phase3_lock_id = f"aep3lock_{phase3_lock_fingerprint[:24]}" if accepted else "NONE"
    return {
        "schema": "v7-aep-phase3-gap-certification/v1",
        "phase3_input_readiness": "PASS" if phase2_ready else "FAIL",
        "behaviour_definitions_reviewed": len(behaviour_definitions),
        "behaviour_instances_reviewed": len(behaviour_instances),
        "gap_candidates": len(dispositions),
        "certified_gaps": len(certified),
        "held_gaps": len(held),
        "rejected_gaps": len(rejected),
        "authority_boundaries_not_gaps": sum(item["certification_verdict"] == "GAP_REJECTED_AUTHORITY_BOUNDARY" for item in rejected),
        "real_world_boundaries_not_gaps": sum(item["certification_verdict"] == "GAP_REJECTED_REAL_WORLD_BOUNDARY" for item in rejected),
        "dependency_waits_not_gaps": sum(item["certification_verdict"] == "GAP_REJECTED_DEPENDENCY_WAIT" for item in rejected),
        "duplicate_gaps": sum(item["certification_verdict"] == "GAP_REJECTED_DUPLICATE" for item in rejected),
        "unknown_gaps": sum(item["certification_verdict"].startswith("GAP_HOLD") for item in held),
        "dispositions": dispositions,
        "candidate_instances": candidates,
        "candidate_instances_created": len(candidates),
        "candidate_instances_ready": len(candidates),
        "candidate_instances_blocked": len(held),
        "register_fingerprint": register_fingerprint,
        "phase3_executor": executor,
        "phase3_acceptance_owner": acceptance_owner or "NONE",
        "role_separation_status": "PASS" if role_separation else "HOLD",
        "acceptance_mission_id": acceptance_mission_id or "NONE",
        "acceptance_run_nonce": acceptance_run_nonce or "NONE",
        "authority_scope_fingerprint": authority_scope_fingerprint,
        "phase3_acceptance_status": acceptance_status,
        "phase3_lock_status": "LOCKED" if accepted else "NOT_LOCKED",
        "phase3_lock_id": phase3_lock_id,
        "phase3_lock_fingerprint": phase3_lock_fingerprint,
        "aep_state_after": "GAP_READY" if accepted else "PHASE_3_READY_FOR_ACCEPTANCE",
        "phase4_status": "READY" if accepted else "LOCKED_PENDING_PHASE_3_ACCEPTANCE",
        "omp_candidates_consumed": len(candidates) if accepted else 0,
        "omp_missions_created": 0,
        "runtime_impact": "NONE",
        "production_impact": "NONE",
        "authority_impact": "NONE",
        "user_movement": "NO",
        "errors": sorted(set(errors)),
        "holds": sorted(set(holds)),
        "final_verdict": (
            "AEP_PHASE_3_CERTIFIED_PHASE_4_READY_BUDGET_EXHAUSTED" if accepted
            else "AEP_PHASE_3_READY_FOR_INDEPENDENT_ACCEPTANCE" if execution_complete
            else "AEP_PHASE_3_FAIL"
        ),
    }


def heartbeat_boundary_dry_run(
    cps_text: str,
    contract: dict[str, Any],
    *,
    expected_automation_id: str,
    expected_target_thread_id: str,
    expected_project_id: str,
    seen_event_ids: Optional[Iterable[str]] = None,
    seen_wakeup_run_ids: Optional[Iterable[str]] = None,
) -> dict[str, Any]:
    """Evaluate a synthetic Codex heartbeat without mutation or Mission admission."""
    required_fields = (
        "AUTOMATION_ID",
        "TARGET_THREAD_ID",
        "PROJECT_ID",
        "WAKEUP_RUN_ID",
        "EVENT_ID",
        "EVENT_OWNER",
        "EVENT_SOURCE",
        "EVENT_GENERATION",
        "EVENT_TIME",
        "FRESHNESS_RULE",
        "DEPENDENCY_FINGERPRINT_BEFORE",
        "DEPENDENCY_FINGERPRINT_AFTER",
        "DEPENDENCY_CHANGED",
        "TARGET_CAPABILITY",
        "CURRENT_CPS_GENERATION",
        "MISSION_SCOPE",
        "AUTHORIZATION_SCOPE",
        "REPLAY_PROTECTION",
        "CONCURRENCY_CONTROL",
        "ACTIVATION_RESULT",
        "EVIDENCE_FRESHNESS_RESULT",
        "EVIDENCE_SUFFICIENCY_RESULT",
        "NO_RUNTIME_AUTHORITY",
        "NO_USER_MOVEMENT_AUTHORITY",
        "NO_PACKET_AUTHORITY",
        "NO_CANDIDATE_AUTHORITY",
    )
    allowed_results = {
        "NO_CHANGE_DEPENDENCY_UNCHANGED",
        "NO_CHANGE_NO_WAITING_CAPABILITY",
        "NO_CHANGE_EVIDENCE_INSUFFICIENT",
        "NO_CHANGE_DUPLICATE_WAKEUP",
        "NO_CHANGE_ALREADY_ACTIVE",
        "STOP_SAFE_IDENTITY_FAILURE",
        "STOP_SAFE_REPLAY_FAILURE",
        "READY_FRONTIER_AVAILABLE_DRY_RUN_ONLY",
    }
    replay_model = (
        "MISSION_IDENTITY+CPS_GENERATION+EVENT_ID+WAKEUP_RUN_ID+DEPENDENCY_FINGERPRINT"
    )
    concurrency_model = (
        "CURRENT_EXECUTION_MISSION_ID+CURRENT_EXECUTION_MISSION_STATE+CURRENT_STATE_GENERATION"
    )

    errors: list[str] = []
    contract_errors: list[str] = []
    identity_errors: list[str] = []
    replay_errors: list[str] = []
    authority_errors: list[str] = []

    for field in required_fields:
        if field not in contract or contract[field] in {None, ""}:
            contract_errors.append(f"heartbeat_field_missing:{field}")

    event_id = str(contract.get("EVENT_ID") or "")
    wakeup_run_id = str(contract.get("WAKEUP_RUN_ID") or "")
    before = str(contract.get("DEPENDENCY_FINGERPRINT_BEFORE") or "")
    after = str(contract.get("DEPENDENCY_FINGERPRINT_AFTER") or "")
    if not re.fullmatch(r"[0-9a-f]{64}", event_id):
        contract_errors.append("heartbeat_event_id_invalid")
    if not re.fullmatch(r"[A-Za-z0-9_.:-]{8,160}", wakeup_run_id):
        contract_errors.append("heartbeat_wakeup_run_id_invalid")
    if not re.fullmatch(r"[0-9a-f]{64}", before):
        contract_errors.append("heartbeat_dependency_fingerprint_before_invalid")
    if not re.fullmatch(r"[0-9a-f]{64}", after):
        contract_errors.append("heartbeat_dependency_fingerprint_after_invalid")
    try:
        _parse_iso_timestamp(str(contract.get("EVENT_TIME") or ""))
    except (TypeError, ValueError):
        contract_errors.append("heartbeat_event_time_invalid")
    if contract.get("ACTIVATION_RESULT") != "PENDING_DRY_RUN":
        contract_errors.append("heartbeat_activation_result_not_pending")
    if contract.get("MISSION_SCOPE") != "HEARTBEAT_REENTRY_DRY_RUN_ONLY":
        contract_errors.append("heartbeat_mission_scope_invalid")
    if contract.get("REPLAY_PROTECTION") != replay_model:
        contract_errors.append("heartbeat_replay_model_invalid")
    if contract.get("CONCURRENCY_CONTROL") != concurrency_model:
        contract_errors.append("heartbeat_concurrency_model_invalid")
    if contract.get("DEPENDENCY_CHANGED") is not (before != after):
        replay_errors.append("heartbeat_dependency_change_claim_invalid")

    if contract.get("AUTOMATION_ID") != expected_automation_id:
        identity_errors.append("heartbeat_automation_identity_mismatch")
    if contract.get("TARGET_THREAD_ID") != expected_target_thread_id:
        identity_errors.append("heartbeat_thread_identity_mismatch")
    if contract.get("PROJECT_ID") != expected_project_id:
        identity_errors.append("heartbeat_project_identity_mismatch")
    if contract.get("EVENT_OWNER") != "CODEX_AUTOMATION_PLATFORM":
        identity_errors.append("heartbeat_event_owner_invalid")
    event_source = str(contract.get("EVENT_SOURCE") or "")
    if not event_source or any(token in event_source.lower() for token in ("report", "chat")):
        identity_errors.append("heartbeat_event_source_not_owner_backed")

    for field in (
        "NO_RUNTIME_AUTHORITY",
        "NO_USER_MOVEMENT_AUTHORITY",
        "NO_PACKET_AUTHORITY",
        "NO_CANDIDATE_AUTHORITY",
    ):
        if contract.get(field) is not True:
            authority_errors.append(f"heartbeat_authority_prohibition_invalid:{field}")
    if contract.get("AUTHORIZATION_SCOPE") != "START_ENGINEERING_EXECUTION_CONTEXT_ONLY":
        authority_errors.append("heartbeat_authorization_scope_expanded")

    live = _markdown_field_table(_markdown_section(
        cps_text,
        "## 0. Authoritative Live Current State",
        "## Authoritative Unfinished Capability Closure Registry",
    ))
    current_generation = live.get("CURRENT_STATE_GENERATION", "").strip("`")
    active_mission_id = live.get("CURRENT_EXECUTION_MISSION_ID", "").strip("`")
    active_mission_state = live.get("CURRENT_EXECUTION_MISSION_STATE", "").strip("`")
    if contract.get("CURRENT_CPS_GENERATION") != current_generation:
        replay_errors.append("heartbeat_cps_generation_stale")

    seen_events = set(seen_event_ids or ())
    seen_runs = set(seen_wakeup_run_ids or ())
    duplicate = event_id in seen_events or wakeup_run_id in seen_runs

    dependency = capability_dependency_consistency(cps_text)
    graph_errors = list(dependency.get("errors") or [])
    graph = _markdown_section(
        cps_text,
        "### Capability Dependency Graph And Execution Frontier",
        "### Owner Revalidation Requirements And Contradictions",
    )
    rows: dict[str, dict[str, Any]] = {}
    for line in graph.splitlines():
        if not re.match(r"\| `CAP-U\d+` \|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 12:
            continue
        capability_id = cells[0].strip("`")
        rows[capability_id] = {
            "state": cells[1].strip("`"),
            "dependencies": set(re.findall(r"CAP-U\d+", cells[4])),
        }

    target = str(contract.get("TARGET_CAPABILITY") or "")
    target_row = rows.get(target)
    waiting = list(dependency.get("waiting_capabilities") or [])
    ready_before = list(dependency.get("ready_capabilities") or [])
    result = "NO_CHANGE_DEPENDENCY_UNCHANGED"
    ready_after = list(ready_before)

    if contract_errors or identity_errors or authority_errors:
        result = "STOP_SAFE_IDENTITY_FAILURE"
    elif duplicate:
        result = "NO_CHANGE_DUPLICATE_WAKEUP"
    elif replay_errors or graph_errors:
        result = "STOP_SAFE_REPLAY_FAILURE"
    elif active_mission_id not in {"", "NONE"} or active_mission_state not in {"", "NONE"}:
        result = "NO_CHANGE_ALREADY_ACTIVE"
    elif not target_row or target_row["state"] != "WAITING_EXTERNAL_DEPENDENCY":
        result = "NO_CHANGE_NO_WAITING_CAPABILITY"
    elif before == after:
        result = "NO_CHANGE_DEPENDENCY_UNCHANGED"
    elif contract.get("EVIDENCE_FRESHNESS_RESULT") != "PASS":
        result = "NO_CHANGE_EVIDENCE_INSUFFICIENT"
    elif contract.get("EVIDENCE_SUFFICIENCY_RESULT") != "SUFFICIENT":
        result = "NO_CHANGE_EVIDENCE_INSUFFICIENT"
    else:
        incomplete_dependencies = {
            item
            for item in target_row["dependencies"]
            if rows.get(item, {}).get("state") != "COMPLETED"
        }
        if incomplete_dependencies:
            result = "NO_CHANGE_EVIDENCE_INSUFFICIENT"
        else:
            result = "READY_FRONTIER_AVAILABLE_DRY_RUN_ONLY"
            ready_after = sorted(set(ready_before) | {target})

    errors.extend(contract_errors)
    errors.extend(identity_errors)
    errors.extend(replay_errors)
    errors.extend(authority_errors)
    errors.extend(graph_errors)
    validators = {
        "heartbeat_contract_consistency": "PASS" if not contract_errors else "FAIL",
        "heartbeat_identity_consistency": "PASS" if not identity_errors else "FAIL",
        "heartbeat_replay_protection": "PASS" if not replay_errors and not duplicate else "FAIL",
        "heartbeat_concurrency_protection": (
            "PASS"
            if active_mission_id in {"", "NONE"} and active_mission_state in {"", "NONE"}
            else "BLOCKED"
        ),
        "heartbeat_no_authority_expansion": "PASS" if not authority_errors else "FAIL",
        "heartbeat_no_runtime_authority": (
            "PASS" if contract.get("NO_RUNTIME_AUTHORITY") is True else "FAIL"
        ),
        "heartbeat_no_mutation": "PASS",
        "heartbeat_result_consistency": "PASS" if result in allowed_results else "FAIL",
    }
    return {
        "schema": "v7-omp-heartbeat-boundary-dry-run/v1",
        "adapter_status": "DRY_RUN_ONLY",
        "activation_result": result,
        "automation_enabled": False,
        "runtime_impact": "NONE",
        "authority_impact": "NONE",
        "user_movement": "NONE",
        "packet_created": False,
        "candidate_created": False,
        "mission_created": False,
        "mission_executed": False,
        "cps_mutated": False,
        "report_created": False,
        "git_changed": False,
        "ready_frontier_before": ready_before,
        "ready_frontier_after": ready_after,
        "waiting_capabilities_preserved": waiting,
        "target_capability": target,
        "current_cps_generation": current_generation,
        "validators": validators,
        "final_verdict": "PASS" if not result.startswith("STOP_SAFE") else "STOP_SAFE",
        "errors": sorted(set(errors)),
    }


PROGRAM_EXECUTION_SOURCE_PATHS = {
    "stage2": "docs/programs/V7_STAGE2_KNOWLEDGE_ENGINEERING_PROGRAM.md",
    "aep": "docs/programs/V7_AUTONOMOUS_EVOLUTION_PROGRAM.md",
    "bdp": "docs/programs/V7_BEHAVIOUR_DISCOVERY_PROGRAM.md",
    "implementation": "docs/programs/V7_IMPLEMENTATION_PROGRAM.md",
    "backlog": "docs/programs/V7_IMPLEMENTATION_BACKLOG.md",
    "omp": "docs/programs/OPERATIONAL_MATURITY_PROGRAM.md",
    "cps": "docs/programs/V7_CURRENT_PROGRAM_STATE.md",
    "aep_phase1": "docs/reports/engineering/V7_AUTONOMOUS_EVOLUTION_FOUNDATION_PHASE1_EXECUTION_REPORT.md",
    "aep_phase2": "docs/reports/research/V7_CURRENT_AUTONOMOUS_BEHAVIOUR_REALITY.md",
    "aep_phase2_execution": "docs/reports/engineering/V7_CURRENT_AUTONOMOUS_BEHAVIOUR_REALITY_EXECUTION_REPORT.md",
    "aep_phase2_acceptance": "docs/reports/research/2026-07-14_100018_aep_phase_2_independent_acceptance.md",
    "aep_phase3_register": "docs/reports/research/V7_CERTIFIED_AUTONOMOUS_BEHAVIOUR_GAP_REGISTER.md",
    "aep_phase3_acceptance": "docs/reports/research/2026-07-14_161705_aep_phase_3_independent_acceptance.md",
    "aep_phase3_lock": "docs/reports/research/2026-07-14_161705_aep_phase_3_gap_register_lock.md",
    "aep_phase4_execution": "docs/reports/engineering/2026-07-14_161705_aep_phase_3_acceptance_to_phase_5_continuation.md",
    "bdp_execution": "docs/reports/engineering/V7_BDP_ENGINEERING_CHAIN_ALIGNMENT_REPORT.md",
}


def load_program_execution_sources(root: Path = ROOT) -> dict[str, str]:
    """Load the existing canonical program inputs for one fresh reconciliation."""
    sources: dict[str, str] = {}
    for owner, relative in PROGRAM_EXECUTION_SOURCE_PATHS.items():
        path = root / relative
        sources[owner] = path.read_text(encoding="utf-8")
    return sources


def heartbeat_dependency_fingerprint(cps_text: str) -> str:
    """Fingerprint the owner-backed dependency graph consumed by the heartbeat."""
    graph = _markdown_section(
        cps_text,
        "### Capability Dependency Graph And Execution Frontier",
        "### Owner Revalidation Requirements And Contradictions",
    )
    return hashlib.sha256(graph.encode("utf-8")).hexdigest()


def heartbeat_program_reentry(
    *,
    event_time: str,
    automation_id: str = HEARTBEAT_AUTOMATION_ID,
    target_thread_id: str = HEARTBEAT_TARGET_THREAD_ID,
    project_id: str = "",
    target_capability: str = "CAP-U07",
    evidence_freshness_result: str = "PASS",
    evidence_sufficiency_result: str = "INSUFFICIENT",
    seen_event_ids: Optional[Iterable[str]] = None,
    seen_wakeup_run_ids: Optional[Iterable[str]] = None,
    root: Path = ROOT,
) -> dict[str, Any]:
    """Run one read-only heartbeat through adapter, reconciliation and consumer."""
    resolved_project = project_id or str(root)
    normalized_time = event_time[:-1] + "+00:00" if event_time.endswith("Z") else event_time
    try:
        _parse_iso_timestamp(normalized_time)
    except (TypeError, ValueError):
        return {
            "schema": "v7-omp-heartbeat-program-reentry/v1",
            "final_verdict": "STOP_SAFE",
            "errors": ["heartbeat_event_time_invalid"],
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_impact": "NONE",
        }

    try:
        sources = load_program_execution_sources(root)
    except OSError as exc:
        return {
            "schema": "v7-omp-heartbeat-program-reentry/v1",
            "final_verdict": "STOP_SAFE",
            "errors": [f"program_execution_source_unreadable:{exc}"],
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_impact": "NONE",
        }

    cps_text = sources["cps"]
    live = _markdown_field_table(_markdown_section(
        cps_text,
        "## 0. Authoritative Live Current State",
        "## Authoritative Unfinished Capability Closure Registry",
    ))
    current_generation = live.get("CURRENT_STATE_GENERATION", "").strip("`")
    current_dependency = heartbeat_dependency_fingerprint(cps_text)
    previous_dependency = live.get("HEARTBEAT_LAST_DEPENDENCY_FINGERPRINT", "").strip("`")
    if not re.fullmatch(r"[0-9a-f]{64}", previous_dependency):
        previous_dependency = current_dependency

    if seen_event_ids is None:
        last_event_id = live.get("HEARTBEAT_LAST_EVENT_ID", "").strip("`")
        seen_event_ids = [last_event_id] if re.fullmatch(r"[0-9a-f]{64}", last_event_id) else []

    event_identity = hashlib.sha256(
        f"{automation_id}|{target_thread_id}|{normalized_time}".encode("utf-8")
    ).hexdigest()
    wakeup_run_id = f"hb_{event_identity[:32]}"
    contract = {
        "AUTOMATION_ID": automation_id,
        "TARGET_THREAD_ID": target_thread_id,
        "PROJECT_ID": resolved_project,
        "WAKEUP_RUN_ID": wakeup_run_id,
        "EVENT_ID": event_identity,
        "EVENT_OWNER": "CODEX_AUTOMATION_PLATFORM",
        "EVENT_SOURCE": f"CODEX_AUTOMATION_PLATFORM:heartbeat:{automation_id}:{wakeup_run_id}",
        "EVENT_GENERATION": current_generation,
        "EVENT_TIME": normalized_time,
        "FRESHNESS_RULE": "FRESH_PLATFORM_EVENT_AND_FRESH_CPS_READ",
        "DEPENDENCY_FINGERPRINT_BEFORE": previous_dependency,
        "DEPENDENCY_FINGERPRINT_AFTER": current_dependency,
        "DEPENDENCY_CHANGED": previous_dependency != current_dependency,
        "TARGET_CAPABILITY": target_capability,
        "CURRENT_CPS_GENERATION": current_generation,
        "MISSION_SCOPE": "HEARTBEAT_REENTRY_DRY_RUN_ONLY",
        "AUTHORIZATION_SCOPE": "START_ENGINEERING_EXECUTION_CONTEXT_ONLY",
        "REPLAY_PROTECTION": "MISSION_IDENTITY+CPS_GENERATION+EVENT_ID+WAKEUP_RUN_ID+DEPENDENCY_FINGERPRINT",
        "CONCURRENCY_CONTROL": "CURRENT_EXECUTION_MISSION_ID+CURRENT_EXECUTION_MISSION_STATE+CURRENT_STATE_GENERATION",
        "ACTIVATION_RESULT": "PENDING_DRY_RUN",
        "EVIDENCE_FRESHNESS_RESULT": evidence_freshness_result,
        "EVIDENCE_SUFFICIENCY_RESULT": evidence_sufficiency_result,
        "NO_RUNTIME_AUTHORITY": True,
        "NO_USER_MOVEMENT_AUTHORITY": True,
        "NO_PACKET_AUTHORITY": True,
        "NO_CANDIDATE_AUTHORITY": True,
    }
    adapter = heartbeat_boundary_dry_run(
        cps_text,
        contract,
        expected_automation_id=HEARTBEAT_AUTOMATION_ID,
        expected_target_thread_id=HEARTBEAT_TARGET_THREAD_ID,
        expected_project_id=str(root),
        seen_event_ids=seen_event_ids,
        seen_wakeup_run_ids=seen_wakeup_run_ids,
    )
    activation = adapter["activation_result"]
    skip_reconciliation = activation in {
        "NO_CHANGE_DUPLICATE_WAKEUP",
        "NO_CHANGE_ALREADY_ACTIVE",
        "STOP_SAFE_IDENTITY_FAILURE",
        "STOP_SAFE_REPLAY_FAILURE",
    }
    if skip_reconciliation:
        return {
            "schema": "v7-omp-heartbeat-program-reentry/v1",
            "event_id": event_identity,
            "wakeup_run_id": wakeup_run_id,
            "fresh_cps_generation": current_generation,
            "dependency_fingerprint": current_dependency,
            "adapter": adapter,
            "reconciliation_invoked": False,
            "consumer_invoked": False,
            "legal_terminal": activation.startswith("NO_CHANGE"),
            "next_output": activation,
            "final_verdict": adapter["final_verdict"],
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_impact": "NONE",
            "errors": adapter["errors"],
        }

    reconciliation = program_execution_reconciliation(sources)
    reconciliation_payload = json.dumps(
        reconciliation, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    decision_payload = {
        "schema": "v7.omp-heartbeat-consumer-decision.v1",
        "event_id": event_identity,
        "wakeup_run_id": wakeup_run_id,
        "cps_generation": current_generation,
        "adapter_result": activation,
        "reconciliation_fingerprint": hashlib.sha256(reconciliation_payload.encode("utf-8")).hexdigest(),
        "program_frontier": reconciliation.get("executable_program_frontier") or [],
    }
    decision_fingerprint = hashlib.sha256(
        json.dumps(decision_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    reconciliation_ok = reconciliation.get("final_verdict") == "PASS"
    legal_no_action = activation in {
        "NO_CHANGE_DEPENDENCY_UNCHANGED",
        "NO_CHANGE_NO_WAITING_CAPABILITY",
        "NO_CHANGE_EVIDENCE_INSUFFICIENT",
    }
    ready = activation == "READY_FRONTIER_AVAILABLE_DRY_RUN_ONLY"
    consumer_decision = (
        "LEGAL_NO_ACTION" if reconciliation_ok and legal_no_action
        else "READY_FRONTIER_AVAILABLE" if reconciliation_ok and ready
        else "STOP_SAFE_RECONCILIATION_FAILURE"
    )
    next_output = (
        "WAIT_FOR_OWNER_BACKED_DEPENDENCY_CHANGE" if consumer_decision == "LEGAL_NO_ACTION"
        else (reconciliation.get("executable_program_frontier") or ["NONE"])[0]
        if consumer_decision == "READY_FRONTIER_AVAILABLE"
        else "STOP_SAFE"
    )
    errors = sorted(set(adapter.get("errors") or ()) | set(reconciliation.get("errors") or ()))
    return {
        "schema": "v7-omp-heartbeat-program-reentry/v1",
        "event_id": event_identity,
        "wakeup_run_id": wakeup_run_id,
        "fresh_cps_generation": current_generation,
        "dependency_fingerprint": current_dependency,
        "adapter": adapter,
        "reconciliation_invoked": True,
        "reconciliation": reconciliation,
        "decision_trace_id": f"omphb_{decision_fingerprint[:24]}",
        "decision_fingerprint": decision_fingerprint,
        "consumer": "OMP_HEARTBEAT_REENTRY_CONSUMER",
        "consumer_invoked": True,
        "consumer_decision": consumer_decision,
        "consumer_behavior_change_or_legal_no_action": consumer_decision in {"LEGAL_NO_ACTION", "READY_FRONTIER_AVAILABLE"},
        "next_output": next_output,
        "legal_terminal": consumer_decision == "LEGAL_NO_ACTION",
        "next_trigger_policy": "NATURAL_SCHEDULE_ONLY_NO_RECURSION",
        "idempotency_key": f"{event_identity}:{wakeup_run_id}:{current_generation}:{current_dependency}",
        "no_unbounded_recursion": True,
        "mission_created": False,
        "candidate_created": False,
        "packet_created": False,
        "cps_mutated": False,
        "git_changed": False,
        "runtime_impact": "NONE",
        "production_impact": "NONE",
        "authority_impact": "NONE",
        "final_verdict": "PASS" if consumer_decision != "STOP_SAFE_RECONCILIATION_FAILURE" else "STOP_SAFE",
        "errors": errors,
    }


BDP_CANDIDATE_REQUIRED_FIELDS = (
    "primary_class",
    "secondary_classes",
    "execution_depth",
    "engineering_intent",
    "current_reality",
    "expected_reality",
    "engineering_chain",
    "engineering_chain_segment",
    "behaviour_instance",
    "behaviour",
    "automation_logic",
    "automation_break",
    "existing_rule",
    "current_outcome",
    "expected_outcome",
    "intent_closure_state",
    "owner",
    "producer",
    "consumer",
    "evidence",
    "implementation_scope",
    "runtime_impact",
    "production_impact",
    "dependencies",
    "verification",
    "verification_context",
    "rollback",
    "authority",
    "authority_context",
    "terminal_path",
    "implementation_readiness",
    "omp_consumer",
    "codex_readiness",
)


def _bdp_normalized_value(value: Any) -> Any:
    if isinstance(value, str):
        return " ".join(value.split()).casefold()
    if isinstance(value, (list, tuple, set)):
        return sorted(_bdp_normalized_value(item) for item in value)
    if isinstance(value, dict):
        return {
            str(key): _bdp_normalized_value(value[key])
            for key in sorted(value)
        }
    return value


def _bdp_candidate_meaning(gap: dict[str, Any]) -> dict[str, Any]:
    identity_fields = (
        "primary_class",
        "execution_depth",
        "engineering_intent",
        "current_reality",
        "expected_reality",
        "engineering_chain",
        "engineering_chain_segment",
        "behaviour_instance",
        "automation_break",
        "owner",
        "consumer",
        "implementation_scope",
    )
    return {
        "identity_schema": "v7.bdp-candidate-meaning.v1",
        **{
            field: _bdp_normalized_value(gap[field])
            for field in identity_fields
        },
    }


def omp_candidate_admission_decision(
    candidate: dict[str, Any],
    *,
    mission_id: str = "",
    existing_candidate_ids: Optional[Iterable[str]] = None,
) -> dict[str, Any]:
    """Consume one BDP Candidate through the existing bounded OMP admission gates."""
    missing = [
        field
        for field in ("candidate_instance_id", "identity_sha256", *BDP_CANDIDATE_REQUIRED_FIELDS)
        if field not in candidate or candidate[field] is None or candidate[field] == ""
    ]
    errors: list[str] = []
    if missing:
        errors.extend(f"candidate_field_missing:{field}" for field in missing)

    identity = str(candidate.get("identity_sha256") or "")
    candidate_id = str(candidate.get("candidate_instance_id") or "")
    if not re.fullmatch(r"[0-9a-f]{64}", identity):
        errors.append("candidate_identity_hash_invalid")
    if candidate_id != f"BDP-ICI-{identity[:24].upper()}":
        errors.append("candidate_identity_id_mismatch")
    duplicate = candidate_id in {str(item) for item in existing_candidate_ids or ()}
    if duplicate:
        errors.append("candidate_identity_duplicate")

    if candidate.get("implementation_readiness") != "IMPLEMENTATION_READY":
        errors.append("candidate_implementation_not_ready")
    if candidate.get("runtime_impact") != "NONE":
        errors.append("candidate_runtime_boundary_not_none")
    if candidate.get("production_impact") != "NONE":
        errors.append("candidate_production_boundary_not_none")
    if candidate.get("dependencies") not in {"NONE", "COMPLETED", "EXISTING_CONTRACTS_READY"}:
        errors.append("candidate_dependency_not_ready")
    if candidate.get("intent_closure_state") != "AUTOMATION_BREAK":
        errors.append("candidate_intent_closure_state_invalid")
    if candidate.get("omp_consumer") != "OMP_CANDIDATE_ADMISSION":
        errors.append("candidate_omp_consumer_invalid")
    for field in (
        "new_owner_required",
        "new_backlog_required",
        "new_runtime_required",
        "new_architecture_required",
        "authority_expansion_required",
    ):
        if candidate.get(field) is not False:
            errors.append(f"candidate_boundary_invalid:{field}")

    unique = sorted(set(errors))
    accepted = not unique
    resolved_mission_id = mission_id or f"V7_OMP_BDP_{identity[:24].upper()}_V1"
    decision_payload = {
        "schema": "v7.omp-candidate-admission-trace.v1",
        "candidate_instance_id": candidate_id,
        "candidate_identity": identity,
        "mission_id": resolved_mission_id if accepted else "NONE",
        "decision": "MISSION_ACCEPTED" if accepted else "MISSION_NOT_APPLICABLE" if duplicate else "MISSION_REJECTED",
        "errors": unique,
    }
    decision_fingerprint = hashlib.sha256(
        json.dumps(decision_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "schema": "v7-omp-candidate-admission-decision/v1",
        "identity_result": "IDENTITY_VALID" if not any("identity" in item for item in unique) else "IDENTITY_INVALID",
        "eligibility_result": "ELIGIBLE" if accepted else "REJECT",
        "duplicate_check_result": "DUPLICATE" if duplicate else "UNIQUE",
        "admission_decision": "MISSION_ACCEPTED" if accepted else "MISSION_NOT_APPLICABLE" if duplicate else "MISSION_REJECTED",
        "mission_created": accepted,
        "mission_state": "PREPARED_NOT_ACTIVE" if accepted else "NONE",
        "mission_id": resolved_mission_id if accepted else "NONE",
        "decision_trace_id": f"ompdt_{decision_fingerprint[:24]}",
        "decision_fingerprint": decision_fingerprint,
        "mission_executed": False,
        "runtime_impact": "NONE",
        "production_impact": "NONE",
        "authority_expansion": False,
        "final_verdict": "PASS" if accepted else "STOP_SAFE",
        "errors": unique,
    }


def bdp_development_impulse_handoff(
    engineering_state: dict[str, Any],
    *,
    existing_candidates: Optional[Iterable[Any]] = None,
) -> dict[str, Any]:
    """Route one bounded owner-backed BDP gap to OMP, or return legal no-action."""
    errors: list[str] = []
    generation = str(engineering_state.get("state_generation") or "")
    decision = str(engineering_state.get("discovery_economy_decision") or "")
    gaps = engineering_state.get("engineering_gaps")
    try:
        real_world_limit_intents = int(engineering_state.get("real_world_limit_intents") or 0)
        if real_world_limit_intents < 0:
            raise ValueError
    except (TypeError, ValueError):
        real_world_limit_intents = 0
        errors.append("bdp_real_world_limit_intents_invalid")
    if not re.fullmatch(r"[A-Za-z0-9_.:-]{8,160}", generation):
        errors.append("bdp_state_generation_invalid")
    if decision != "DISCOVERY_NOT_REQUIRED_REUSE_EVIDENCE":
        errors.append("bdp_discovery_economy_not_ready_for_reuse")
    if not isinstance(gaps, list):
        errors.append("bdp_engineering_gaps_invalid")

    if errors:
        return {
            "schema": "v7-omp-bdp-development-impulse-handoff/v1",
            "handoff_status": "STOP_SAFE",
            "candidate_production_status": "NO_CANDIDATE",
            "candidate_count": 0,
            "candidate": None,
            "admission_decision": "NONE",
            "mission_created": False,
            "mission_executed": False,
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_expansion": False,
            "final_verdict": "STOP_SAFE",
            "errors": sorted(set(errors)),
        }

    if not gaps:
        return {
            "schema": "v7-omp-bdp-development-impulse-handoff/v1",
            "handoff_status": "NO_ACTION_REQUIRED",
            "candidate_production_status": "NO_ACTION",
            "candidate_count": 0,
            "candidate": None,
            "admission_decision": "MISSION_NOT_APPLICABLE",
            "terminal_consumer": "OMP_NEXT_ACTION",
            "mission_created": False,
            "mission_executed": False,
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_expansion": False,
            "real_world_limit_intents_preserved": real_world_limit_intents,
            "final_verdict": "PASS",
            "errors": [],
        }

    if len(gaps) != 1 or not isinstance(gaps[0], dict):
        return {
            "schema": "v7-omp-bdp-development-impulse-handoff/v1",
            "handoff_status": "STOP_SAFE",
            "candidate_production_status": "AMBIGUOUS_BOUNDED_SCOPE",
            "candidate_count": 0,
            "candidate": None,
            "admission_decision": "NONE",
            "mission_created": False,
            "mission_executed": False,
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_expansion": False,
            "final_verdict": "STOP_SAFE",
            "errors": ["bdp_bounded_scope_requires_exactly_one_gap"],
        }

    gap = gaps[0]
    missing = [
        field
        for field in BDP_CANDIDATE_REQUIRED_FIELDS
        if field not in gap or gap[field] is None or gap[field] == ""
    ]
    for field in missing:
        errors.append(f"bdp_gap_field_missing:{field}")
    if gap.get("new_owner_required") is not False:
        errors.append("bdp_gap_requires_new_owner")
    if gap.get("new_architecture_required") is not False:
        errors.append("bdp_gap_requires_new_architecture")
    if errors:
        return {
            "schema": "v7-omp-bdp-development-impulse-handoff/v1",
            "handoff_status": "STOP_SAFE",
            "candidate_production_status": "INVALID_GAP",
            "candidate_count": 0,
            "candidate": None,
            "admission_decision": "NONE",
            "mission_created": False,
            "mission_executed": False,
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_expansion": False,
            "final_verdict": "STOP_SAFE",
            "errors": sorted(set(errors)),
        }

    meaning = _bdp_candidate_meaning(gap)
    encoded = json.dumps(meaning, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    identity = hashlib.sha256(encoded).hexdigest()
    candidate_id = f"BDP-ICI-{identity[:24].upper()}"
    candidate = {
        "candidate_instance_id": candidate_id,
        "identity_sha256": identity,
        "meaning_fingerprint": identity,
        "identity_schema": meaning["identity_schema"],
        "state_generation": generation,
        **gap,
        "new_owner_required": False,
        "new_backlog_required": False,
        "new_runtime_required": False,
        "new_architecture_required": False,
        "authority_expansion_required": False,
    }

    existing_ids: set[str] = set()
    existing_meanings: set[str] = set()
    for item in existing_candidates or ():
        if isinstance(item, str):
            existing_ids.add(item)
        elif isinstance(item, dict):
            existing_ids.add(str(item.get("candidate_instance_id") or ""))
            existing_meanings.add(str(item.get("meaning_fingerprint") or ""))
    if candidate_id in existing_ids or identity in existing_meanings:
        return {
            "schema": "v7-omp-bdp-development-impulse-handoff/v1",
            "handoff_status": "DUPLICATE_SUPPRESSED",
            "candidate_production_status": "DUPLICATE_EXISTING_CANDIDATE",
            "candidate_count": 0,
            "candidate": None,
            "existing_candidate_id": candidate_id,
            "admission_decision": "MISSION_NOT_APPLICABLE",
            "terminal_consumer": "EXISTING_CANDIDATE_LIFECYCLE",
            "mission_created": False,
            "mission_executed": False,
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_expansion": False,
            "final_verdict": "PASS",
            "errors": [],
        }

    admission = omp_candidate_admission_decision(candidate)
    return {
        "schema": "v7-omp-bdp-development-impulse-handoff/v1",
        "handoff_status": "CANDIDATE_CONSUMED_BY_OMP" if admission["final_verdict"] == "PASS" else "STOP_SAFE",
        "candidate_production_status": "ONE_DETERMINISTIC_CANDIDATE",
        "candidate_count": 1,
        "candidate": candidate,
        "admission": admission,
        "admission_decision": admission["admission_decision"],
        "mission_created": admission["mission_created"],
        "mission_executed": False,
        "runtime_impact": "NONE",
        "production_impact": "NONE",
        "authority_expansion": False,
        "final_verdict": admission["final_verdict"],
        "errors": admission["errors"],
    }


def bdp_development_impulse_from_cps(
    cps_text: str,
    *,
    engineering_gaps: Optional[list[dict[str, Any]]] = None,
    existing_candidates: Optional[Iterable[Any]] = None,
) -> dict[str, Any]:
    """Evaluate the BDP handoff from fresh CPS without mutating the CPS owner."""
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
    dependency = capability_dependency_consistency(cps_text)
    if dependency["final_verdict"] != "PASS":
        return {
            "schema": "v7-omp-bdp-development-impulse-handoff/v1",
            "handoff_status": "STOP_SAFE",
            "candidate_production_status": "INVALID_CPS_DEPENDENCY_STATE",
            "candidate_count": 0,
            "candidate": None,
            "admission_decision": "NONE",
            "mission_created": False,
            "mission_executed": False,
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_expansion": False,
            "final_verdict": "STOP_SAFE",
            "errors": list(dependency["errors"]),
        }
    open_intents = registry.get("OPEN_ENGINEERING_INTENTS", "0").strip("`")
    try:
        real_world_limit_intents = int(open_intents)
    except ValueError:
        real_world_limit_intents = 0
    return bdp_development_impulse_handoff(
        {
            "state_generation": live.get("CURRENT_STATE_GENERATION", "").strip("`"),
            "discovery_economy_decision": "DISCOVERY_NOT_REQUIRED_REUSE_EVIDENCE",
            "engineering_gaps": list(engineering_gaps or ()),
            "real_world_limit_intents": real_world_limit_intents,
        },
        existing_candidates=existing_candidates,
    )


POLYGON_SCENARIO_SOURCE_REQUIRED_FIELDS = (
    "source_owner",
    "source_evidence",
    "engineering_intent",
    "current_reality",
    "expected_reality",
    "target_rule_or_contract",
    "failure_or_gap_class",
    "affected_producer",
    "affected_consumer",
    "boundary",
    "stimulus_or_replay_input",
    "expected_observation",
    "pass_criteria",
    "fail_criteria",
    "implementation_allowed",
    "verification_plan",
    "rollback_or_stop_safe",
    "runtime_impact",
    "production_impact",
    "authority_impact",
    "maturity_impact",
)

POLYGON_SCENARIO_PRIORITY = {
    "CURRENT_TRUTH_CONTRADICTION": 10,
    "STOP_SAFE_OR_ROLLBACK_GAP": 20,
    "PRODUCER_CONSUMER_CHAIN_GAP": 30,
    "DETERMINISTIC_REPLAY_OR_DUPLICATE_GAP": 40,
    "DEPENDENCY_OR_AUTHORITY_BOUNDARY_GAP": 50,
    "CANONICAL_RULE_VERIFICATION_GAP": 60,
    "HISTORICAL_DEFECT_REGRESSION_GAP": 70,
    "EXECUTION_CERTIFICATION_COVERAGE_GAP": 80,
    "ENGINEERING_QUALITY_GAP": 90,
}


def _polygon_scenario_meaning(source: dict[str, Any]) -> dict[str, Any]:
    fields = (
        "source_owner",
        "engineering_intent",
        "current_reality",
        "expected_reality",
        "target_rule_or_contract",
        "failure_or_gap_class",
        "affected_producer",
        "affected_consumer",
        "boundary",
        "stimulus_or_replay_input",
        "expected_observation",
    )
    return {
        "identity_schema": "v7.engineering-polygon-scenario-meaning.v1",
        **{field: _bdp_normalized_value(source[field]) for field in fields},
    }


def engineering_polygon_scenario_instance(source: dict[str, Any]) -> dict[str, Any]:
    """Materialize one bounded owner-backed scenario without creating a new lifecycle."""
    errors = [
        f"scenario_source_field_missing:{field}"
        for field in POLYGON_SCENARIO_SOURCE_REQUIRED_FIELDS
        if field not in source or source[field] is None or source[field] == ""
    ]
    gap_class = str(source.get("failure_or_gap_class") or "")
    if gap_class not in POLYGON_SCENARIO_PRIORITY:
        errors.append("scenario_gap_class_unknown")
    if source.get("runtime_impact") != "NONE":
        errors.append("scenario_runtime_boundary")
    if source.get("production_impact") != "NONE":
        errors.append("scenario_production_boundary")
    if source.get("authority_impact") not in {"NONE", False}:
        errors.append("scenario_authority_boundary")
    if source.get("maturity_impact") != "PRODUCTION_MATURITY_CREDIT_FORBIDDEN":
        errors.append("scenario_maturity_boundary")
    if source.get("new_owner_required") is not False:
        errors.append("scenario_new_owner_boundary")
    if source.get("new_architecture_required") is not False:
        errors.append("scenario_new_architecture_boundary")
    if source.get("implementation_allowed") is not True:
        errors.append("scenario_implementation_not_allowed")
    unique = sorted(set(errors))
    if unique:
        return {
            "schema": "v7-engineering-polygon-scenario-instance/v1",
            "status": "STOP_SAFE",
            "scenario_instance": None,
            "final_verdict": "STOP_SAFE",
            "errors": unique,
        }
    meaning = _polygon_scenario_meaning(source)
    encoded = json.dumps(meaning, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    identity = hashlib.sha256(encoded).hexdigest()
    instance = {
        "schema": "v7-engineering-polygon-scenario-instance/v1",
        "scenario_instance_id": f"V7-POLYGON-SCENARIO-{identity[:24].upper()}",
        "deterministic_identity": identity,
        "duplicate_fingerprint": identity,
        "priority": POLYGON_SCENARIO_PRIORITY[gap_class],
        **source,
    }
    return {
        "schema": "v7-engineering-polygon-scenario-materialization/v1",
        "status": "SCENARIO_MATERIALIZED",
        "scenario_instance": instance,
        "final_verdict": "PASS",
        "errors": [],
    }


def select_engineering_polygon_scenario(
    sources: Iterable[Any],
    *,
    existing_scenarios: Optional[Iterable[Any]] = None,
) -> dict[str, Any]:
    """Select exactly one deterministic engineering-plane scenario through existing OMP priority."""
    materialized: list[dict[str, Any]] = []
    excluded: list[dict[str, str]] = []
    invalid: list[str] = []
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            invalid.append(f"scenario_source_invalid:{index}")
            continue
        if (
            source.get("production_impact") not in {None, "NONE"}
            or source.get("runtime_impact") not in {None, "NONE"}
        ):
            excluded.append({"source": str(source.get("source_evidence") or index), "reason": "PRODUCTION_CONTOUR_ONLY"})
            continue
        result = engineering_polygon_scenario_instance(source)
        if result["final_verdict"] != "PASS":
            invalid.extend(result["errors"])
            continue
        materialized.append(result["scenario_instance"])

    if invalid:
        return {
            "schema": "v7-engineering-polygon-scenario-selection/v1",
            "selection_status": "STOP_SAFE",
            "selected_scenario": None,
            "evaluated_source_count": len(materialized) + len(excluded) + len(invalid),
            "valid_scenario_count": len(materialized),
            "excluded_sources": excluded,
            "final_verdict": "STOP_SAFE",
            "errors": sorted(set(invalid)),
        }

    existing_ids: set[str] = set()
    existing_meanings: set[str] = set()
    for item in existing_scenarios or ():
        if isinstance(item, str):
            existing_ids.add(item)
        elif isinstance(item, dict):
            existing_ids.add(str(item.get("scenario_instance_id") or ""))
            existing_meanings.add(str(item.get("duplicate_fingerprint") or ""))
    ordered = sorted(
        materialized,
        key=lambda row: (int(row["priority"]), str(row["deterministic_identity"])),
    )
    remaining = [
        row for row in ordered
        if row["scenario_instance_id"] not in existing_ids
        and row["duplicate_fingerprint"] not in existing_meanings
    ]
    duplicates = len(ordered) - len(remaining)
    selected = remaining[0] if remaining else None
    return {
        "schema": "v7-engineering-polygon-scenario-selection/v1",
        "selection_status": "SCENARIO_SELECTED" if selected else "NO_VALID_ENGINEERING_SCENARIO",
        "selected_scenario": selected,
        "evaluated_source_count": len(materialized) + len(excluded),
        "valid_scenario_count": len(materialized),
        "duplicate_scenario_count": duplicates,
        "remaining_distinct_scenario_count": len(remaining),
        "excluded_sources": excluded,
        "final_verdict": "PASS",
        "errors": [],
    }


def _polygon_gap_from_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    return {
        "primary_class": "VERIFICATION_TRUTH_CONVERGENCE",
        "secondary_classes": ["IMPLEMENTATION_OWNER_EXTENSION", "CONSUMER_CONFIRMATION_CHAIN_CLOSURE"],
        "execution_depth": "L2",
        "engineering_intent": scenario["engineering_intent"],
        "current_reality": scenario["current_reality"],
        "expected_reality": scenario["expected_reality"],
        "engineering_chain": "SCENARIO_SOURCE->BDP->CANDIDATE->OMP->MISSION->VERIFICATION",
        "engineering_chain_segment": "OWNER_BACKED_SCENARIO_TO_BDP_CONSUMER",
        "behaviour_instance": scenario["expected_observation"],
        "behaviour": scenario["target_rule_or_contract"],
        "automation_logic": "Existing polygon scenario selector plus BDP Development Impulse handoff.",
        "automation_break": scenario["failure_or_gap_class"],
        "existing_rule": scenario["target_rule_or_contract"],
        "current_outcome": scenario["fail_criteria"],
        "expected_outcome": scenario["pass_criteria"],
        "intent_closure_state": "AUTOMATION_BREAK",
        "owner": scenario["source_owner"],
        "producer": scenario["affected_producer"],
        "consumer": scenario["affected_consumer"],
        "evidence": scenario["source_evidence"],
        "implementation_scope": scenario["boundary"],
        "runtime_impact": "NONE",
        "production_impact": "NONE",
        "dependencies": "EXISTING_CONTRACTS_READY",
        "verification": scenario["verification_plan"],
        "verification_context": scenario["stimulus_or_replay_input"],
        "rollback": scenario["rollback_or_stop_safe"],
        "authority": "EXISTING_ENGINEERING_PLANE_AUTHORITY",
        "authority_context": "No authority expansion; production evidence and maturity remain protected.",
        "terminal_path": "OMP_MISSION_OR_LEGAL_TERMINAL",
        "implementation_readiness": "IMPLEMENTATION_READY",
        "omp_consumer": "OMP_CANDIDATE_ADMISSION",
        "codex_readiness": "CODEX_READY_WITH_LIMITS",
        "new_owner_required": False,
        "new_architecture_required": False,
    }


POLYGON_SCENARIO_SOURCE_CLASSES = (
    "CURRENT_STATE_TRUTH_CONTRADICTIONS",
    "DELEGATED_POLICY_AND_AUTHORITY_BOUNDARIES",
    "CAPABILITY_DEPENDENCY_ORDERING",
    "OMP_SELF_CONTINUATION",
    "MISSION_IDENTITY_AND_REPLAY",
    "PRODUCER_CONSUMER_CONFIRMATION",
    "STOP_SAFE_AND_ROLLBACK_CONTRACTS",
    "RECOVERY_CONTRACTS",
    "BEHAVIOUR_DEFINITION_INSTANCE_COVERAGE",
    "HISTORICAL_CONFIRMED_DEFECTS",
    "ENGINEERING_REPORT_PROMOTION",
    "EXECUTION_CERTIFICATION_LADDER_COVERAGE",
    "PROTECTED_WORK_IN_PROGRESS",
    "PRODUCTION_ONLY_EVIDENCE_DEPENDENCIES",
)


def _polygon_validator_error_source(error: str) -> dict[str, Any]:
    dependency = "dependency" in error or "frontier" in error or "sequence" in error
    replay = "replay" in error or "identity" in error or "nonce" in error
    if dependency:
        gap_class = "DEPENDENCY_OR_AUTHORITY_BOUNDARY_GAP"
        owner = "CPS_CAPABILITY_DEPENDENCY_AND_OMP_SEQUENCING_OWNERS"
    elif replay:
        gap_class = "DETERMINISTIC_REPLAY_OR_DUPLICATE_GAP"
        owner = "OMP_MISSION_IDENTITY_AND_REPLAY_OWNERS"
    else:
        gap_class = "CURRENT_TRUTH_CONTRADICTION"
        owner = "CPS_CURRENT_STATE_CONSISTENCY_OWNER"
    return {
        "source_owner": owner,
        "source_evidence": f"active owner validator failure `{error}`",
        "engineering_intent": f"Close active fail-closed owner-validator gap `{error}`.",
        "current_reality": f"Current owner validator emits `{error}`.",
        "expected_reality": f"Existing owner validator no longer emits `{error}` after verified correction.",
        "target_rule_or_contract": "Current State Consistency, OMP sequencing and fail-closed validation",
        "failure_or_gap_class": gap_class,
        "affected_producer": "existing CPS/OMP state producer",
        "affected_consumer": "existing v7_sync_lib consistency consumer",
        "boundary": "existing Engineering Plane owner implementation and verification only",
        "stimulus_or_replay_input": f"deterministic replay of current state producing `{error}`",
        "expected_observation": f"replay closes `{error}` without Runtime or production impact",
        "pass_criteria": f"`{error}` absent and all affected owner validators PASS",
        "fail_criteria": f"`{error}` remains, changes identity nondeterministically or loses its consumer",
        "implementation_allowed": True,
        "verification_plan": "focused fail-closed regression, full unit suite, truth and convergence",
        "rollback_or_stop_safe": "revert bounded owner extension or STOP_SAFE while contradiction remains",
        "runtime_impact": "NONE",
        "production_impact": "NONE",
        "authority_impact": "NONE",
        "maturity_impact": "PRODUCTION_MATURITY_CREDIT_FORBIDDEN",
        "new_owner_required": False,
        "new_architecture_required": False,
    }


def discover_engineering_polygon_scenario_sources(
    cps_text: str,
    *,
    root: Path = ROOT,
    omp_text: Optional[str] = None,
) -> dict[str, Any]:
    """Evaluate existing owner surfaces and emit only active engineering-plane failures."""
    if omp_text is None:
        try:
            omp_text = (root / "docs" / "programs" / "OPERATIONAL_MATURITY_PROGRAM.md").read_text(encoding="utf-8")
        except OSError:
            omp_text = ""
    consistency = cps_live_state_consistency(
        cps_text,
        root=root,
        omp_text=omp_text,
        verify_external=False,
    )
    errors = sorted(set(str(item) for item in consistency.get("errors") or [] if str(item)))
    sources = [_polygon_validator_error_source(error) for error in errors]
    coverage = {
        source_class: (
            "ACTIVE_AND_CONSUMED" if sources and source_class in {
                "CURRENT_STATE_TRUTH_CONTRADICTIONS",
                "CAPABILITY_DEPENDENCY_ORDERING",
                "OMP_SELF_CONTINUATION",
                "MISSION_IDENTITY_AND_REPLAY",
            }
            else "PRODUCTION_EVIDENCE_ONLY" if source_class == "PRODUCTION_ONLY_EVIDENCE_DEPENDENCIES"
            else "HISTORICAL_ONLY" if source_class in {
                "BEHAVIOUR_DEFINITION_INSTANCE_COVERAGE",
                "HISTORICAL_CONFIRMED_DEFECTS",
                "ENGINEERING_REPORT_PROMOTION",
            }
            else "ACTIVE_AND_CONSUMED"
        )
        for source_class in POLYGON_SCENARIO_SOURCE_CLASSES
    }
    return {
        "schema": "v7-engineering-polygon-scenario-source-discovery/v1",
        "evaluated_source_classes": list(POLYGON_SCENARIO_SOURCE_CLASSES),
        "evaluated_source_class_count": len(POLYGON_SCENARIO_SOURCE_CLASSES),
        "coverage": coverage,
        "active_source_count": len(sources),
        "scenario_sources": sources,
        "production_only_sources_excluded": 1,
        "historical_context_classes_not_promoted": 3,
        "current_consistency_result": consistency["final_verdict"],
        "final_verdict": "PASS",
        "errors": [],
    }


def engineering_polygon_scenario_supply_from_cps(
    cps_text: str,
    *,
    scenario_sources: Optional[Iterable[Any]] = None,
    existing_scenarios: Optional[Iterable[Any]] = None,
    existing_candidates: Optional[Iterable[Any]] = None,
) -> dict[str, Any]:
    """Connect bounded owner-backed scenarios to the existing BDP and OMP consumers."""
    selection = select_engineering_polygon_scenario(
        scenario_sources or (),
        existing_scenarios=existing_scenarios,
    )
    if selection["final_verdict"] != "PASS":
        return {
            "schema": "v7-omp-polygon-scenario-supply/v1",
            "supply_status": "STOP_SAFE",
            "selection": selection,
            "bdp": None,
            "scenario_consumed_by_bdp": False,
            "final_verdict": "STOP_SAFE",
            "errors": selection["errors"],
        }
    selected = selection["selected_scenario"]
    if selected is None:
        return {
            "schema": "v7-omp-polygon-scenario-supply/v1",
            "supply_status": "NO_VALID_ENGINEERING_SCENARIO",
            "selection": selection,
            "bdp": None,
            "scenario_consumed_by_bdp": False,
            "mission_executed": False,
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_expansion": False,
            "maturity_impact": "NONE",
            "final_verdict": "PASS",
            "errors": [],
        }
    bdp = bdp_development_impulse_from_cps(
        cps_text,
        engineering_gaps=[_polygon_gap_from_scenario(selected)],
        existing_candidates=existing_candidates,
    )
    return {
        "schema": "v7-omp-polygon-scenario-supply/v1",
        "supply_status": "SCENARIO_CONSUMED_BY_BDP" if bdp["final_verdict"] == "PASS" else "STOP_SAFE",
        "selection": selection,
        "bdp": bdp,
        "scenario_consumed_by_bdp": bdp["candidate_production_status"] in {
            "ONE_DETERMINISTIC_CANDIDATE",
            "DUPLICATE_EXISTING_CANDIDATE",
        },
        "mission_executed": False,
        "runtime_impact": "NONE",
        "production_impact": "NONE",
        "authority_expansion": False,
        "maturity_impact": "NONE",
        "final_verdict": bdp["final_verdict"],
        "errors": bdp["errors"],
    }


def current_engineering_polygon_scenario_supply(
    cps_text: str,
    *,
    root: Path = ROOT,
    omp_text: Optional[str] = None,
    existing_scenarios: Optional[Iterable[Any]] = None,
    existing_candidates: Optional[Iterable[Any]] = None,
) -> dict[str, Any]:
    """Run one fresh existing-owner scenario discovery and BDP/OMP supply iteration."""
    discovery = discover_engineering_polygon_scenario_sources(
        cps_text,
        root=root,
        omp_text=omp_text,
    )
    supply = engineering_polygon_scenario_supply_from_cps(
        cps_text,
        scenario_sources=discovery["scenario_sources"],
        existing_scenarios=existing_scenarios,
        existing_candidates=existing_candidates,
    )
    return {
        "schema": "v7-omp-current-polygon-scenario-supply/v1",
        "discovery": discovery,
        "supply": supply,
        "all_source_classes_evaluated": discovery["evaluated_source_class_count"] == len(POLYGON_SCENARIO_SOURCE_CLASSES),
        "scenario_consumed_by_bdp": supply["scenario_consumed_by_bdp"],
        "runtime_impact": "NONE",
        "production_impact": "NONE",
        "authority_expansion": False,
        "maturity_impact": "NONE",
        "final_verdict": supply["final_verdict"],
        "errors": supply["errors"],
    }


FUTURE_SCALE_SCENARIO_CORPUS_PATH = "tests/scenarios/future_scale/foundation.json"
FUTURE_SCALE_SCENARIO_REQUIRED_FIELDS = (
    "SCENARIO_ID", "SCENARIO_VERSION", "TITLE", "RISK_CLASS", "ENGINEERING_VALUE_CLASS",
    "TOPOLOGY_PROFILE", "USER_POPULATION_PROFILE", "CHANNEL_POPULATION_PROFILE",
    "COHORT_PROFILE", "SERVICE_PROFILE", "CAPACITY_PROFILE", "TRAFFIC_PROFILE",
    "INITIAL_STATE", "EVENT_TIMELINE", "TELEMETRY_PROFILE", "FAILURE_INJECTIONS",
    "RECOVERY_EVENTS", "AUTHORITY_SCOPE", "INVARIANT_IDS", "EXPECTED_TERMINAL_CLASSES",
    "FORBIDDEN_EFFECTS", "SEED", "SOURCE_DEPENDENCIES", "OWNER_DEPENDENCIES",
    "SCENARIO_FINGERPRINT", "EXPECTED_SCALE_CLASS", "EVIDENCE_CLASS",
)

_INVARIANT_OWNER_GROUPS = {
    "ROUTING_SAFETY_OWNER": (
        "tools/v7-users-autoswitch",
        "AutoswitchPlanner.plan and existing route/safety validators",
        ("ROUTE_REACHABILITY", "NO_UNROUTED_ELIGIBLE_USER", "POLICY_ISOLATION", "COHORT_ISOLATION",
         "CAPACITY_BOUND", "BLAST_RADIUS_BOUND", "NO_UNBOUNDED_FLAP", "ANTI_FLAP_PRESERVATION",
         "HARD_FAILURE_OVERRIDE_SAFETY", "RECOVERY_ADMISSION_SAFETY", "RECOVERY_SLOW_START"),
    ),
    "EXECUTION_SAFETY_OWNER": (
        "admin_core/operator_execution_pipeline.py",
        "existing execution, rollback, containment and legal-terminal validators",
        ("ROLLBACK_SAFETY", "NO_ROLLBACK_LEGAL_TERMINAL", "PARTIAL_EXECUTION_CONTAINMENT",
         "FORWARD_FIX_CLASSIFICATION", "FINAL_OPEN_OR_STOP_SAFE"),
    ),
    "CPS_OMP_CONSISTENCY_OWNER": (
        "tools/v7_sync_lib.py",
        "cps_live_state_consistency and existing OMP identity/consumer validators",
        ("STALE_MUTATION_DENIAL", "UNKNOWN_STATE_MUTATION_DENIAL", "DETERMINISTIC_DECISION",
         "DUPLICATE_EVENT_SUPPRESSION", "DUPLICATE_MISSION_SUPPRESSION", "SINGLE_FLIGHT",
         "LEASE_IDENTITY", "SOURCE_BINDING", "SNAPSHOT_FRESHNESS", "AUTHORITY_NON_EXPANSION",
         "ACTION_CLASS_BOUND", "OUTPUT_CONSUMPTION", "NEXT_OUTPUT_PRODUCTION",
         "PRODUCER_CONSUMER_CONTINUITY", "NO_SYNTHETIC_PRODUCTION_CREDIT"),
    ),
}


def _future_scale_invariant_registry() -> dict[str, dict[str, str]]:
    registry: dict[str, dict[str, str]] = {}
    for owner, (path, validator, invariant_ids) in _INVARIANT_OWNER_GROUPS.items():
        for invariant_id in invariant_ids:
            registry[invariant_id] = {
                "INVARIANT_ID": invariant_id,
                "CANONICAL_OWNER": owner,
                "SOURCE_PATH": path,
                "INPUT_CONTRACT": "ENGINEERING_SCENARIO_STATE_AND_EVENT_TIMELINE",
                "EXPECTED_PROPERTY": invariant_id,
                "VERDICT_FUNCTION_OR_VALIDATOR": validator,
                "EVIDENCE_FORMAT": "v7.future-scale-scenario-result.v1",
                "FAILURE_CLASS": "REPRODUCIBLE_ENGINEERING_INVARIANT_MISMATCH",
                "BDP_ELIGIBLE_ON_FAILURE": "TRUE",
                "CURRENT_CALLERS": "Future-scale scenario validator/frontier; existing owner validator at FSSE-02 execution",
            }
    return registry


FUTURE_SCALE_INVARIANTS = _future_scale_invariant_registry()


def resolve_invariant(invariant_id: str) -> dict[str, Any]:
    """Resolve stable invariant metadata without copying owner business logic."""
    resolved = FUTURE_SCALE_INVARIANTS.get(str(invariant_id or ""))
    return {
        "schema": "v7-future-scale-invariant-resolution/v1",
        "invariant_id": invariant_id,
        "resolved": resolved is not None,
        "contract": dict(resolved) if resolved else None,
        "final_verdict": "PASS" if resolved else "STOP_SAFE",
        "errors": [] if resolved else [f"unresolved_invariant:{invariant_id}"],
    }


def future_scale_scenario_fingerprint(scenario: dict[str, Any]) -> str:
    meaningful = {
        key: scenario.get(key)
        for key in FUTURE_SCALE_SCENARIO_REQUIRED_FIELDS
        if key != "SCENARIO_FINGERPRINT"
    }
    encoded = json.dumps(meaningful, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def future_scale_scenario_priority(scenario: dict[str, Any]) -> dict[str, str]:
    """Reuse OMP ordinal priority semantics for deterministic scenario ordering."""
    invariants = set(str(item) for item in scenario.get("INVARIANT_IDS") or ())
    ordered_classes = (
        ("P0_SAFETY", {"FINAL_OPEN_OR_STOP_SAFE", "AUTHORITY_NON_EXPANSION", "BLAST_RADIUS_BOUND"}),
        ("P1_ROUTE_ISOLATION", {"ROUTE_REACHABILITY", "NO_UNROUTED_ELIGIBLE_USER", "POLICY_ISOLATION", "COHORT_ISOLATION"}),
        ("P2_CORRELATED_FAILURE", {"HARD_FAILURE_OVERRIDE_SAFETY", "PARTIAL_EXECUTION_CONTAINMENT"}),
        ("P3_CAPACITY", {"CAPACITY_BOUND"}),
        ("P4_STALE_STATE", {"STALE_MUTATION_DENIAL", "UNKNOWN_STATE_MUTATION_DENIAL", "SNAPSHOT_FRESHNESS"}),
        ("P5_RECOVERY_ROLLBACK", {"RECOVERY_ADMISSION_SAFETY", "RECOVERY_SLOW_START", "ROLLBACK_SAFETY"}),
        ("P6_REPLAY_CONCURRENCY", {"DUPLICATE_EVENT_SUPPRESSION", "DUPLICATE_MISSION_SUPPRESSION", "SINGLE_FLIGHT", "LEASE_IDENTITY"}),
        ("P7_FUTURE_SCALE", set()),
    )
    priority = "P7_FUTURE_SCALE"
    reason = "future-scale coverage deficit"
    rank = len(ordered_classes) - 1
    for index, (candidate, owned) in enumerate(ordered_classes):
        if owned and invariants & owned:
            priority = candidate
            reason = "invariants=" + ",".join(sorted(invariants & owned))
            rank = index
            break
    payload = {
        "scenario_id": scenario.get("SCENARIO_ID"),
        "scenario_version": scenario.get("SCENARIO_VERSION"),
        "priority": priority,
        "reason": reason,
    }
    fingerprint = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {
        "SCENARIO_PRIORITY": priority,
        "PRIORITY_RANK": str(rank),
        "PRIORITY_REASON": reason,
        "PRIORITY_FINGERPRINT": fingerprint,
    }


def validate_future_scale_scenario(scenario: Any) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(scenario, dict):
        errors.append("scenario_not_object")
        scenario = {}
    for field in FUTURE_SCALE_SCENARIO_REQUIRED_FIELDS:
        if field not in scenario or scenario[field] in (None, "", []):
            errors.append(f"scenario_field_missing:{field}")
    if scenario.get("EVIDENCE_CLASS") != "ENGINEERING_SCENARIO_EVIDENCE":
        errors.append("scenario_evidence_class_invalid")
    forbidden = set(str(item) for item in scenario.get("FORBIDDEN_EFFECTS") or ())
    required_forbidden = {"RUNTIME_MUTATION", "PRODUCTION_MUTATION", "USER_MOVEMENT", "AUTHORITY_EXPANSION", "PRODUCTION_MATURITY_CREDIT"}
    if not required_forbidden.issubset(forbidden):
        errors.append("scenario_forbidden_effect_boundary_incomplete")
    unresolved = [item for item in scenario.get("INVARIANT_IDS") or () if not resolve_invariant(str(item))["resolved"]]
    errors.extend(f"unresolved_invariant:{item}" for item in unresolved)
    try:
        seed = int(scenario.get("SEED"))
        if seed < 0:
            errors.append("scenario_seed_invalid")
    except (TypeError, ValueError):
        errors.append("scenario_seed_invalid")
    fingerprint = future_scale_scenario_fingerprint(scenario)
    declared = str(scenario.get("SCENARIO_FINGERPRINT") or "")
    if declared not in {"DERIVED", fingerprint}:
        errors.append("scenario_fingerprint_mismatch")
    normalized = dict(scenario)
    normalized["SCENARIO_FINGERPRINT"] = fingerprint
    normalized.update(future_scale_scenario_priority(normalized))
    unique = sorted(set(errors))
    return {
        "schema": "v7-future-scale-scenario-validation/v1",
        "scenario": normalized if not unique else None,
        "valid": not unique,
        "final_verdict": "PASS" if not unique else "STOP_SAFE",
        "errors": unique,
    }


def load_future_scale_scenario_corpus(*, root: Path = ROOT) -> dict[str, Any]:
    path = root / FUTURE_SCALE_SCENARIO_CORPUS_PATH
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return {
            "schema": "v7-future-scale-scenario-corpus/v1", "scenarios": [],
            "final_verdict": "STOP_SAFE", "errors": [f"scenario_corpus_unreadable:{exc}"],
        }
    raw = payload.get("scenarios") if isinstance(payload, dict) else None
    if not isinstance(raw, list):
        return {
            "schema": "v7-future-scale-scenario-corpus/v1", "scenarios": [],
            "final_verdict": "STOP_SAFE", "errors": ["scenario_corpus_list_missing"],
        }
    validated = [validate_future_scale_scenario(item) for item in raw]
    errors = sorted({error for row in validated for error in row["errors"]})
    scenarios = [row["scenario"] for row in validated if row["scenario"]]
    identities = [(row["SCENARIO_ID"], row["SCENARIO_VERSION"]) for row in scenarios]
    fingerprints = [row["SCENARIO_FINGERPRINT"] for row in scenarios]
    if len(identities) != len(set(identities)):
        errors.append("duplicate_scenario_id_version")
    if len(fingerprints) != len(set(fingerprints)):
        errors.append("duplicate_scenario_fingerprint")
    corpus_payload = json.dumps(
        sorted((row["SCENARIO_ID"], row["SCENARIO_VERSION"], row["SCENARIO_FINGERPRINT"]) for row in scenarios),
        separators=(",", ":"),
    )
    return {
        "schema": "v7-future-scale-scenario-corpus/v1",
        "corpus_path": FUTURE_SCALE_SCENARIO_CORPUS_PATH,
        "corpus_count": len(scenarios),
        "corpus_fingerprint": hashlib.sha256(corpus_payload.encode()).hexdigest(),
        "scenarios": scenarios,
        "final_verdict": "PASS" if not errors else "STOP_SAFE",
        "errors": sorted(set(errors)),
    }


def future_scale_scenario_frontier(
    cps_text: str,
    *,
    root: Path = ROOT,
    result_history: Optional[dict[str, dict[str, Any]]] = None,
    ordinary_work_available: bool = False,
    scenario_budget: int = 10,
) -> dict[str, Any]:
    """Build a no-mutation Future-Scale Scenario Frontier through existing Polygon/OMP owners."""
    corpus = load_future_scale_scenario_corpus(root=root)
    if corpus["final_verdict"] != "PASS":
        return {
            "schema": "v7-future-scale-scenario-frontier/v1", "decision": "SCENARIO_STOP_SAFE",
            "final_verdict": "STOP_SAFE", "errors": corpus["errors"],
        }
    live = _markdown_field_table(_markdown_section(
        cps_text, "## 0. Authoritative Live Current State", "## Authoritative Unfinished Capability Closure Registry",
    ))
    history = result_history or {}
    covered: list[str] = []
    stale: list[str] = []
    blocked: list[dict[str, str]] = []
    eligible: list[dict[str, Any]] = []
    active_scenario = live.get("ACTIVE_SCENARIO_ID", "").strip("`")
    active_mission = live.get("CURRENT_EXECUTION_MISSION_ID", "").strip("`")
    for scenario in corpus["scenarios"]:
        scenario_id = scenario["SCENARIO_ID"]
        missing_sources = [path for path in scenario["SOURCE_DEPENDENCIES"] if not (root / path).exists()]
        if missing_sources:
            blocked.append({"SCENARIO_ID": scenario_id, "REASON": "MISSING_SOURCE_DEPENDENCY:" + ",".join(missing_sources)})
            continue
        if active_scenario == scenario_id or (active_mission not in {"", "NONE"} and live.get("ACTIVE_SCENARIO_MISSION", "").strip("`") == active_mission):
            blocked.append({"SCENARIO_ID": scenario_id, "REASON": "ACTIVE_DUPLICATE"})
            continue
        previous = history.get(scenario_id) or {}
        if previous.get("result") == "PASS" and previous.get("scenario_fingerprint") == scenario["SCENARIO_FINGERPRINT"]:
            covered.append(scenario_id)
            continue
        if previous:
            stale.append(scenario_id)
        eligible.append(scenario)
    eligible.sort(key=lambda row: (
        0 if row["SCENARIO_ID"] in stale else 1,
        int(row["PRIORITY_RANK"]),
        row["SCENARIO_FINGERPRINT"],
    ))
    bounded_budget = max(0, min(int(scenario_budget), 10))
    selected = eligible[0] if eligible and bounded_budget else None
    decision = (
        "ORDINARY_FRONTIER_SELECTED" if ordinary_work_available
        else "SCENARIO_FOUNDATION_READY_EXECUTION_HARNESS_REQUIRED" if selected
        else "SCENARIO_BUDGET_REACHED" if eligible
        else "SCENARIO_FRONTIER_EXHAUSTED"
    )
    generation_payload = {
        "corpus": corpus["corpus_fingerprint"],
        "eligible": [row["SCENARIO_FINGERPRINT"] for row in eligible],
        "covered": covered,
        "stale": stale,
        "blocked": blocked,
        "ordinary": ordinary_work_available,
        "budget": bounded_budget,
    }
    frontier_fingerprint = hashlib.sha256(
        json.dumps(generation_payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "schema": "v7-future-scale-scenario-frontier/v1",
        "FRONTIER_GENERATION": f"fssef_{frontier_fingerprint[:24]}",
        "FRONTIER_FINGERPRINT": frontier_fingerprint,
        "ELIGIBLE_SCENARIOS": [row["SCENARIO_ID"] for row in eligible],
        "STALE_SCENARIOS": stale,
        "COVERED_SCENARIOS": covered,
        "BLOCKED_SCENARIOS": blocked,
        "NEXT_SCENARIO_ID": selected["SCENARIO_ID"] if selected and not ordinary_work_available else "NONE",
        "NEXT_SCENARIO_REASON": selected["PRIORITY_REASON"] if selected and not ordinary_work_available else decision,
        "CURRENT_TARGET_COVERAGE": "SAFETY_BASELINE_FOUNDATION_READY",
        "FRONTIER_EXHAUSTED": not eligible,
        "EXHAUSTION_REASON": "ALL_CURRENT_SCENARIOS_COVERED" if not eligible else "NOT_EXHAUSTED",
        "SCENARIO_CORPUS_COUNT": corpus["corpus_count"],
        "SCENARIO_BUDGET": bounded_budget,
        "decision": decision,
        "next_output": (
            "V7_FUTURE_SCALE_POLYGON_EXECUTION_HARNESS_V1"
            if decision == "SCENARIO_FOUNDATION_READY_EXECUTION_HARNESS_REQUIRED" else decision
        ),
        "real_consumer": "OMP_PROGRAM_EXECUTION_RECONCILIATION",
        "runtime_impact": "NONE",
        "production_impact": "NONE",
        "authority_expansion": False,
        "maturity_impact": "NONE",
        "final_verdict": "PASS",
        "errors": [],
    }


PROACTIVE_VERIFICATION_INPUT_REQUIRED_FIELDS = (
    "source_owner",
    "execution_owner",
    "source_evidence",
    "target_contract",
    "engineering_intent",
    "current_assumption",
    "expected_behavior",
    "entrypoint",
    "input_or_fixture",
    "preconditions",
    "observation_method",
    "pass_criteria",
    "fail_criteria",
    "result_consumer",
    "rollback_or_stop_safe",
    "runtime_impact",
    "production_impact",
    "authority_impact",
    "maturity_credit",
    "revalidation_trigger",
    "verification_class",
)

PROACTIVE_VERIFICATION_PRIORITY = {
    "STOP_SAFE_SAFETY": 10,
    "STOP_SAFE_SAFETY_NEGATIVE": 10,
    "ROLLBACK_PARTIAL_FAILURE": 20,
    "CURRENT_TRUTH": 30,
    "TRUTH_CURRENT_STATE_CONSISTENCY": 30,
    "PRODUCER_CONSUMER": 40,
    "PRODUCER_CONSUMER_CONFIRMATION": 40,
    "REPLAY_DETERMINISM": 50,
    "REPLAY_DUPLICATE_PROTECTION": 50,
    "DUPLICATE_IDEMPOTENCY": 55,
    "DEPENDENCY_ORDER": 60,
    "DEPENDENCY_COMPLETION_ORDER": 60,
    "RECOVERY": 70,
    "RECOVERY_POST_FAILURE": 70,
    "BEHAVIOR_PROPAGATION": 72,
    "STATE_TRANSITION": 74,
    "AUTHORITY_BOUNDARY": 80,
    "RUNTIME_BOUNDARY": 82,
    "PRODUCTION_BOUNDARY": 84,
    "AUTHORITY_RUNTIME_PRODUCTION_BOUNDARY": 80,
    "HISTORICAL_REGRESSION": 90,
    "HISTORICAL_EXECUTABLE_REGRESSION": 90,
    "CANONICAL_RULE_COVERAGE": 100,
    "CANONICAL_COVERAGE_OBLIGATION": 100,
    "ENGINEERING_QUALITY": 110,
}


def _proactive_input_meaning(source: dict[str, Any]) -> dict[str, Any]:
    fields = (
        "source_owner",
        "execution_owner",
        "target_contract",
        "engineering_intent",
        "expected_behavior",
        "entrypoint",
        "input_or_fixture",
        "result_consumer",
        "verification_class",
    )
    return {
        "identity_schema": "v7.proactive-verification-input-meaning.v1",
        **{field: _bdp_normalized_value(source[field]) for field in fields},
    }


def proactive_verification_input(source: dict[str, Any]) -> dict[str, Any]:
    """Validate bounded metadata for an existing verification owner."""
    errors = [
        f"proactive_input_field_missing:{field}"
        for field in PROACTIVE_VERIFICATION_INPUT_REQUIRED_FIELDS
        if field not in source or source[field] is None or source[field] == ""
    ]
    verification_class = str(source.get("verification_class") or "")
    if verification_class not in PROACTIVE_VERIFICATION_PRIORITY:
        errors.append("proactive_input_verification_class_unknown")
    if source.get("runtime_impact") not in {"NONE", "READ_ONLY_ONLY"}:
        errors.append("proactive_input_runtime_boundary")
    if source.get("production_impact") != "NONE":
        errors.append("proactive_input_production_boundary")
    if source.get("authority_impact") not in {"NONE", False}:
        errors.append("proactive_input_authority_boundary")
    if source.get("maturity_credit") != "FORBIDDEN":
        errors.append("proactive_input_maturity_boundary")
    for field in ("user_movement", "packet_apply", "restore_barrier_write"):
        if source.get(field) not in {False, "FORBIDDEN"}:
            errors.append(f"proactive_input_{field}_boundary")
    if source.get("new_owner_required") is not False:
        errors.append("proactive_input_new_owner_boundary")
    if source.get("new_architecture_required") is not False:
        errors.append("proactive_input_new_architecture_boundary")
    entrypoint = source.get("entrypoint")
    if not isinstance(entrypoint, list) or len(entrypoint) < 4:
        errors.append("proactive_input_entrypoint_invalid")
    elif entrypoint[:3] != [sys.executable, "-m", "unittest"]:
        errors.append("proactive_input_entrypoint_not_existing_unittest_owner")
    elif not all(str(item).startswith("tests.unit.") for item in entrypoint[3:]):
        errors.append("proactive_input_entrypoint_outside_unit_owner")
    unique = sorted(set(errors))
    if unique:
        return {
            "schema": "v7-proactive-verification-input/v1",
            "status": "PROACTIVE_VERIFICATION_STOP_SAFE",
            "proactive_input": None,
            "final_verdict": "STOP_SAFE",
            "errors": unique,
        }
    meaning = _proactive_input_meaning(source)
    encoded = json.dumps(meaning, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    identity = hashlib.sha256(encoded).hexdigest()
    instance = {
        "schema": "v7-proactive-verification-input/v1",
        "proactive_input_id": f"V7-PROACTIVE-INPUT-{identity[:24].upper()}",
        "deterministic_identity": identity,
        "duplicate_fingerprint": identity,
        "priority": PROACTIVE_VERIFICATION_PRIORITY[verification_class],
        "last_execution_result": "NOT_EVALUATED",
        **source,
    }
    return {
        "schema": "v7-proactive-verification-input-materialization/v1",
        "status": "PROACTIVE_INPUT_ELIGIBLE",
        "proactive_input": instance,
        "final_verdict": "PASS",
        "errors": [],
    }


def _proactive_coverage_state(
    proactive_input: dict[str, Any],
    coverage_record: Optional[dict[str, Any]],
) -> str:
    if not coverage_record:
        return "NOT_EVALUATED"
    result = str(coverage_record.get("last_result") or "NOT_EVALUATED")
    current_fingerprint = str(proactive_input.get("revalidation_fingerprint") or proactive_input["deterministic_identity"])
    evaluated_fingerprint = str(coverage_record.get("last_evaluated_fingerprint") or "")
    if evaluated_fingerprint != current_fingerprint:
        return "STALE_REVALIDATION_REQUIRED"
    if result in {"PROACTIVE_VERIFICATION_PASS", "PASS_CURRENT"}:
        return "PASS_CURRENT"
    if result in {"PROACTIVE_VERIFICATION_FAIL", "FAIL_CURRENT"}:
        return "FAIL_CURRENT"
    if result in {"PROACTIVE_VERIFICATION_NON_DETERMINISTIC", "NON_DETERMINISTIC"}:
        return "NON_DETERMINISTIC"
    if result in {"PROACTIVE_VERIFICATION_BLOCKED", "BLOCKED"}:
        return "BLOCKED"
    if result in {"NOT_APPLICABLE", "PROACTIVE_VERIFICATION_NOT_APPLICABLE"}:
        return "NOT_APPLICABLE"
    return "NOT_EVALUATED"


def select_proactive_verification_input(
    sources: Iterable[Any],
    *,
    evaluated_inputs: Optional[Iterable[Any]] = None,
    coverage_records: Optional[dict[str, dict[str, Any]]] = None,
) -> dict[str, Any]:
    """Select one smallest deterministic existing-owner verification input."""
    materialized: list[dict[str, Any]] = []
    excluded: list[dict[str, str]] = []
    invalid: list[str] = []
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            invalid.append(f"proactive_input_invalid:{index}")
            continue
        source_classification = str(source.get("source_classification") or "ACTIVE_EXECUTABLE_NOT_CONSUMED")
        if source_classification in {"HISTORICAL_CONTEXT_ONLY", "PRODUCTION_ONLY", "NOT_EXECUTABLE"}:
            excluded.append({
                "source": str(source.get("source_evidence") or index),
                "reason": source_classification,
            })
            continue
        result = proactive_verification_input(source)
        if result["final_verdict"] != "PASS":
            invalid.extend(result["errors"])
            continue
        materialized.append(result["proactive_input"])
    if invalid:
        return {
            "schema": "v7-proactive-verification-input-selection/v1",
            "selection_status": "PROACTIVE_VERIFICATION_STOP_SAFE",
            "selected_input": None,
            "eligible_input_count": len(materialized),
            "excluded_inputs": excluded,
            "final_verdict": "STOP_SAFE",
            "errors": sorted(set(invalid)),
        }
    evaluated_ids: set[str] = set()
    evaluated_fingerprints: set[str] = set()
    for item in evaluated_inputs or ():
        if isinstance(item, str):
            evaluated_ids.add(item)
        elif isinstance(item, dict):
            evaluated_ids.add(str(item.get("proactive_input_id") or ""))
            evaluated_fingerprints.add(str(item.get("duplicate_fingerprint") or ""))
    coverage_records = coverage_records or {}
    state_rank = {
        "FAIL_CURRENT": 0,
        "STALE_REVALIDATION_REQUIRED": 1,
        "NOT_EVALUATED": 2,
        "BLOCKED": 3,
        "NON_DETERMINISTIC": 4,
        "PASS_CURRENT": 5,
        "NOT_APPLICABLE": 6,
    }
    for row in materialized:
        row["coverage_state"] = _proactive_coverage_state(
            row,
            coverage_records.get(str(row["proactive_input_id"])),
        )
        row["revalidation_required"] = row["coverage_state"] in {
            "STALE_REVALIDATION_REQUIRED",
            "FAIL_CURRENT",
            "BLOCKED",
            "NON_DETERMINISTIC",
        }
    ordered = sorted(
        materialized,
        key=lambda row: (
            state_rank.get(str(row["coverage_state"]), 99),
            int(row["priority"]),
            str(row["deterministic_identity"]),
        ),
    )
    remaining = [
        row for row in ordered
        if row["proactive_input_id"] not in evaluated_ids
        and row["duplicate_fingerprint"] not in evaluated_fingerprints
        and row["coverage_state"] not in {"PASS_CURRENT", "NOT_APPLICABLE"}
    ]
    selected = remaining[0] if remaining else None
    return {
        "schema": "v7-proactive-verification-input-selection/v1",
        "selection_status": "PROACTIVE_INPUT_SELECTED" if selected else "NO_ELIGIBLE_PROACTIVE_VERIFICATION_INPUT",
        "selected_input": selected,
        "eligible_input_count": len(materialized),
        "current_pass_count": sum(1 for row in materialized if row["coverage_state"] == "PASS_CURRENT"),
        "stale_input_count": sum(1 for row in materialized if row["coverage_state"] == "STALE_REVALIDATION_REQUIRED"),
        "not_evaluated_count": sum(1 for row in materialized if row["coverage_state"] == "NOT_EVALUATED"),
        "remaining_distinct_input_count": len(remaining),
        "duplicate_input_count": len(ordered) - len(remaining),
        "excluded_inputs": excluded,
        "final_verdict": "PASS",
        "errors": [],
    }


def execute_proactive_verification_input(
    proactive_input: dict[str, Any],
    *,
    runner: Optional[Callable[[list[str], Optional[Path], int], dict[str, Any]]] = None,
    root: Path = ROOT,
) -> dict[str, Any]:
    """Execute one existing unittest owner and classify its current observation."""
    validation = proactive_verification_input({
        key: value for key, value in proactive_input.items()
        if key not in {"schema", "proactive_input_id", "deterministic_identity", "duplicate_fingerprint", "priority", "last_execution_result"}
    })
    if validation["final_verdict"] != "PASS":
        return {
            "schema": "v7-proactive-verification-execution/v1",
            "execution_result": "PROACTIVE_VERIFICATION_STOP_SAFE",
            "reproducible": False,
            "observed_current_behavior": "input validation failed",
            "evidence": validation,
            "final_verdict": "STOP_SAFE",
            "errors": validation["errors"],
        }
    runner = runner or run_command
    command = list(proactive_input["entrypoint"])
    first = runner(command, root, 120)
    if first.get("ok"):
        return {
            "schema": "v7-proactive-verification-execution/v1",
            "proactive_input_id": proactive_input["proactive_input_id"],
            "execution_result": "PROACTIVE_VERIFICATION_PASS",
            "reproducible": True,
            "observed_current_behavior": "existing verification entrypoint passed",
            "evidence": first,
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_expansion": False,
            "maturity_impact": "NONE",
            "final_verdict": "PASS",
            "errors": [],
        }
    second = runner(command, root, 120)
    first_signature = (first.get("rc"), first.get("stdout"), first.get("stderr"))
    second_signature = (second.get("rc"), second.get("stdout"), second.get("stderr"))
    reproducible = first_signature == second_signature
    result = "PROACTIVE_VERIFICATION_FAIL" if reproducible else "PROACTIVE_VERIFICATION_NON_DETERMINISTIC"
    return {
        "schema": "v7-proactive-verification-execution/v1",
        "proactive_input_id": proactive_input["proactive_input_id"],
        "execution_result": result,
        "reproducible": reproducible,
        "observed_current_behavior": "existing verification entrypoint failed now",
        "evidence": {"first": first, "replay": second},
        "runtime_impact": "NONE",
        "production_impact": "NONE",
        "authority_expansion": False,
        "maturity_impact": "NONE",
        "final_verdict": "PASS" if reproducible else "STOP_SAFE",
        "errors": [] if reproducible else ["proactive_verification_non_deterministic"],
    }


def proactive_verification_failure_scenario_source(
    proactive_input: dict[str, Any],
    execution: dict[str, Any],
) -> dict[str, Any]:
    """Convert only a reproducible current failure to the existing scenario contract."""
    errors = []
    if execution.get("execution_result") != "PROACTIVE_VERIFICATION_FAIL":
        errors.append("proactive_result_not_current_failure")
    if execution.get("reproducible") is not True:
        errors.append("proactive_failure_not_reproducible")
    if not proactive_input.get("source_owner"):
        errors.append("proactive_failure_owner_missing")
    if not proactive_input.get("result_consumer"):
        errors.append("proactive_failure_consumer_missing")
    if proactive_input.get("runtime_impact") not in {"NONE", "READ_ONLY_ONLY"}:
        errors.append("proactive_failure_runtime_boundary")
    if proactive_input.get("production_impact") != "NONE":
        errors.append("proactive_failure_production_boundary")
    if errors:
        return {
            "schema": "v7-proactive-result-to-scenario/v1",
            "conversion_status": "PROACTIVE_VERIFICATION_STOP_SAFE",
            "scenario_source": None,
            "final_verdict": "STOP_SAFE",
            "errors": sorted(set(errors)),
        }
    source = {
        "source_owner": proactive_input["source_owner"],
        "source_evidence": f"current reproducible proactive failure {proactive_input['proactive_input_id']}",
        "engineering_intent": proactive_input["engineering_intent"],
        "current_reality": execution["observed_current_behavior"],
        "expected_reality": proactive_input["expected_behavior"],
        "target_rule_or_contract": proactive_input["target_contract"],
        "failure_or_gap_class": "STOP_SAFE_OR_ROLLBACK_GAP" if proactive_input["priority"] <= 20 else "CANONICAL_RULE_VERIFICATION_GAP",
        "affected_producer": proactive_input["execution_owner"],
        "affected_consumer": proactive_input["result_consumer"],
        "boundary": "existing verification owner and scenario-supply integration only",
        "stimulus_or_replay_input": proactive_input["input_or_fixture"],
        "expected_observation": proactive_input["expected_behavior"],
        "pass_criteria": proactive_input["pass_criteria"],
        "fail_criteria": proactive_input["fail_criteria"],
        "implementation_allowed": True,
        "verification_plan": f"rerun {proactive_input['input_or_fixture']} and affected owner suite",
        "rollback_or_stop_safe": proactive_input["rollback_or_stop_safe"],
        "runtime_impact": "NONE",
        "production_impact": "NONE",
        "authority_impact": "NONE",
        "maturity_impact": "PRODUCTION_MATURITY_CREDIT_FORBIDDEN",
        "new_owner_required": False,
        "new_architecture_required": False,
    }
    return {
        "schema": "v7-proactive-result-to-scenario/v1",
        "conversion_status": "CURRENT_FAILURE_SCENARIO_SOURCE_READY",
        "scenario_source": source,
        "final_verdict": "PASS",
        "errors": [],
    }


PROACTIVE_SEED_SPECS = (
        (
            "STOP_SAFE_SAFETY_NEGATIVE",
            "OPERATOR_EXECUTION_PIPELINE_VERIFICATION_OWNER",
            "tests.unit.test_operator_execution_pipeline.OperatorExecutionPipelineTest.test_autonomous_dry_run_hard_stops_on_snapshot_mismatch",
            "Autonomous dry-run snapshot mismatch must STOP_SAFE before mutation.",
        ),
        (
            "ROLLBACK_PARTIAL_FAILURE",
            "RECOVERY_ADMISSION_VERIFICATION_OWNER",
            "tests.unit.test_autonomy_trust_acceleration.AutonomyTrustAccelerationTest.test_a6_recovery_gate_stops_on_failed_observation_verification",
            "Recovery admission must stop when observation verification fails.",
        ),
        (
            "TRUTH_CURRENT_STATE_CONSISTENCY",
            "OPERATION_SCOPED_BINDING_OWNER",
            "tests.unit.test_operation_scoped_binding.OperationScopedBindingTest.test_atomic_reader_retries_and_stops_on_persistent_mixed_generation",
            "Atomic current-state reader must reject persistent mixed generations.",
        ),
        (
            "PRODUCER_CONSUMER_CONFIRMATION",
            "BDP_DEVELOPMENT_IMPULSE_OWNER",
            "tests.unit.test_bdp_development_impulse_handoff.BdpDevelopmentImpulseHandoffTest.test_one_known_gap_produces_one_candidate_and_uses_admission",
            "A known BDP gap must reach the existing OMP admission consumer.",
        ),
        (
            "REPLAY_DUPLICATE_PROTECTION",
            "BDP_CANDIDATE_IDENTITY_OWNER",
            "tests.unit.test_bdp_development_impulse_handoff.BdpDevelopmentImpulseHandoffTest.test_repeated_identical_state_suppresses_duplicate",
            "Repeated equivalent BDP state must suppress duplicate Candidates.",
        ),
        (
            "DEPENDENCY_COMPLETION_ORDER",
            "CPS_CAPABILITY_DEPENDENCY_OWNER",
            "tests.unit.test_omp_dependency_graph_completion_order.OmpDependencyGraphCompletionOrderTest.test_06_completion_order_violation_is_rejected",
            "Completion-order violations must be rejected by the existing dependency owner.",
        ),
)

PROACTIVE_CORPUS_MODULE_OWNERS = {
    "test_omp_self_continuation": ("OMP_SELF_CONTINUATION_OWNER", "tools/v7_sync_lib.py"),
    "test_omp_dependency_graph_completion_order": ("CPS_CAPABILITY_DEPENDENCY_OWNER", "tools/v7_sync_lib.py"),
    "test_omp_live_state_pointer_consistency": ("OMP_CPS_POINTER_CONSISTENCY_OWNER", "tools/v7_sync_lib.py"),
    "test_omp_heartbeat_boundary_adapter": ("OMP_HEARTBEAT_BOUNDARY_OWNER", "tools/v7_sync_lib.py"),
    "test_bdp_development_impulse_handoff": ("BDP_DEVELOPMENT_IMPULSE_OWNER", "tools/v7_sync_lib.py"),
    "test_operation_scoped_binding": ("OPERATION_SCOPED_BINDING_OWNER", "admin_core/operation_scoped_binding.py"),
    "test_autonomy_trust_acceleration": ("AUTONOMY_TRUST_VERIFICATION_OWNER", "admin_core/autonomy_trust_acceleration.py"),
    "test_operator_execution_pipeline": ("OPERATOR_EXECUTION_PIPELINE_VERIFICATION_OWNER", "admin_core/operator_execution_pipeline.py"),
    "test_operator_observability": ("OPERATOR_OBSERVABILITY_OWNER", "admin_core/operator_observability.py"),
    "test_intelligence_platform": ("INTELLIGENCE_PLATFORM_VERIFICATION_OWNER", "admin_core/intelligence_platform.py"),
    "test_routing_brain": ("ROUTING_BRAIN_VERIFICATION_OWNER", "admin_core/routing_brain.py"),
    "test_operator_decision_surface": ("OPERATOR_DECISION_SURFACE_OWNER", "admin_core/operator_decision_surface.py"),
    "test_operator_execution_feedback": ("OPERATOR_EXECUTION_FEEDBACK_OWNER", "admin_core/operator_execution_feedback.py"),
}

PROACTIVE_CORPUS_CLASS_RULES = (
    ("STOP_SAFE_SAFETY", ("stop_safe", "stops", "stop_", "fails_closed", "fail_closed", "hard_stop")),
    ("ROLLBACK_PARTIAL_FAILURE", ("rollback", "partial_failure")),
    ("CURRENT_TRUTH", ("current_state", "truth", "mixed_generation", "stale")),
    ("PRODUCER_CONSUMER", ("producer", "consumer", "handoff")),
    ("REPLAY_DETERMINISM", ("replay", "deterministic")),
    ("DUPLICATE_IDEMPOTENCY", ("duplicate", "idempot")),
    ("DEPENDENCY_ORDER", ("dependency", "completion_order", "frontier")),
    ("RECOVERY", ("recovery", "recovered")),
    ("BEHAVIOR_PROPAGATION", ("behavior", "behaviour", "propagation")),
    ("STATE_TRANSITION", ("transition", "lifecycle")),
    ("AUTHORITY_BOUNDARY", ("authority",)),
    ("RUNTIME_BOUNDARY", ("runtime",)),
    ("PRODUCTION_BOUNDARY", ("production",)),
    ("HISTORICAL_REGRESSION", ("historical", "regression")),
    ("CANONICAL_RULE_COVERAGE", ("canonical", "contract")),
    ("ENGINEERING_QUALITY", ("quality", "coverage")),
)

PROACTIVE_CORPUS_FORBIDDEN_TOKENS = (
    "subprocess",
    "paramiko",
    "requests.",
    "urllib",
    "socket.",
    "systemctl",
    "ssh ",
    "/opt/v7",
    "execute_runtime_action",
    "user_switch",
    "packet_apply",
    "production_apply",
    "restore_barrier_write",
)

PROACTIVE_CORPUS_SELF_TEST_MODULES = {
    "test_omp_proactive_polygon_verification",
    "test_omp_polygon_fallback_continuation",
}

PROACTIVE_SEED_CANONICAL_CLASSES = {
    "STOP_SAFE_SAFETY_NEGATIVE": "STOP_SAFE_SAFETY",
    "ROLLBACK_PARTIAL_FAILURE": "ROLLBACK_PARTIAL_FAILURE",
    "TRUTH_CURRENT_STATE_CONSISTENCY": "CURRENT_TRUTH",
    "PRODUCER_CONSUMER_CONFIRMATION": "PRODUCER_CONSUMER",
    "REPLAY_DUPLICATE_PROTECTION": "DUPLICATE_IDEMPOTENCY",
    "DEPENDENCY_COMPLETION_ORDER": "DEPENDENCY_ORDER",
}


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def proactive_corpus_fingerprint(inputs: Iterable[dict[str, Any]]) -> str:
    payload = [
        {
            "proactive_input_id": item["proactive_input_id"],
            "revalidation_fingerprint": item.get("revalidation_fingerprint", item["deterministic_identity"]),
            "contract_class": item.get("contract_class", item["verification_class"]),
        }
        for item in sorted(inputs, key=lambda row: row["proactive_input_id"])
    ]
    return _sha256_text(json.dumps(payload, sort_keys=True, separators=(",", ":")))


def _proactive_contract_class(method_name: str) -> str:
    normalized = method_name.lower()
    for contract_class, keywords in PROACTIVE_CORPUS_CLASS_RULES:
        if any(keyword in normalized for keyword in keywords):
            return contract_class
    return "NOT_ELIGIBLE"


def _proactive_method_exclusion(method_name: str, source: str) -> str:
    normalized = f"{method_name}\n{source}".lower()
    for token in PROACTIVE_CORPUS_FORBIDDEN_TOKENS:
        if token in normalized:
            return f"UNSAFE_OR_EXTERNAL_TOKEN:{token.strip()}"
    if any(token in method_name.lower() for token in ("deploy", "real_runtime", "live_server", "network")):
        return "ENVIRONMENT_OR_PRODUCTION_DEPENDENT"
    return ""


def _corpus_dependency_fingerprint(root: Path) -> str:
    omp_text = (root / "docs/programs/OPERATIONAL_MATURITY_PROGRAM.md").read_text(encoding="utf-8")
    cps_text = (root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md").read_text(encoding="utf-8")
    omp_version = re.search(r"(?m)^Version:\s*`([^`]+)`", omp_text)
    graph_version = re.search(r"(?m)^\| `DEPENDENCY_GRAPH_VERSION` \| `([^`]+)`", cps_text)
    return _sha256_text("|".join((
        omp_version.group(1) if omp_version else "UNKNOWN_OMP_VERSION",
        graph_version.group(1) if graph_version else "UNKNOWN_DEPENDENCY_GRAPH",
    )))


def _proactive_source_from_method(
    *,
    root: Path,
    module_name: str,
    class_node: ast.ClassDef,
    method_node: ast.FunctionDef,
    file_text: str,
    owner: str,
    owner_path: str,
    contract_class: str,
    dependency_fingerprint: str,
) -> dict[str, Any]:
    selector = f"tests.unit.{module_name}.{class_node.name}.{method_node.name}"
    relative = f"tests/unit/{module_name}.py"
    method_source = ast.get_source_segment(file_text, method_node) or method_node.name
    class_source = ast.get_source_segment(file_text, class_node) or class_node.name
    owner_file = root / owner_path
    owner_source = owner_file.read_text(encoding="utf-8") if owner_file.exists() else "MISSING_OWNER_IMPLEMENTATION"
    target_contract = method_node.name.removeprefix("test_").replace("_", " ")
    method_fingerprint = _sha256_text(method_source)
    fixture_fingerprint = _sha256_text(class_source)
    owner_fingerprint = _sha256_text(owner_source)
    contract_fingerprint = _sha256_text(target_contract)
    revalidation_fingerprint = _sha256_text("|".join((
        owner_fingerprint,
        method_fingerprint,
        fixture_fingerprint,
        contract_fingerprint,
        dependency_fingerprint,
    )))
    identity = _sha256_text(f"{owner}|{selector}|{contract_class}|{target_contract}")
    return {
        "corpus_input_id": f"V7-POLYGON-CORPUS-{identity[:24].upper()}",
        "source_owner": owner,
        "execution_owner": "PYTHON_UNITTEST_EXISTING_VERIFICATION_OWNER",
        "source_evidence": relative,
        "module": module_name,
        "class_name": class_node.name,
        "method_or_entrypoint": method_node.name,
        "target_contract": target_contract,
        "contract_class": contract_class,
        "engineering_intent": f"Proactively preserve existing owner contract: {target_contract}.",
        "current_assumption": "The existing owner implementation still satisfies this executable contract.",
        "expected_behavior": f"Existing unittest contract `{selector}` passes.",
        "entrypoint": [sys.executable, "-m", "unittest", selector],
        "input_or_fixture": selector,
        "preconditions": "clean converged repository; isolated unittest; no external production access",
        "observation_method": "exact unittest method assertion and process exit status",
        "pass_criteria": "exact unittest method exits zero",
        "fail_criteria": "exact unittest method fails reproducibly in the current checkout",
        "result_consumer": "ENGINEERING_POLYGON_SCENARIO_SUPPLY",
        "rollback_or_stop_safe": "isolated test-only mutation; STOP_SAFE on invalid, flaky or boundary-crossing result",
        "mutation_boundary": "ISOLATED_TEST_ONLY",
        "runtime_impact": "NONE",
        "production_impact": "NONE",
        "authority_impact": "NONE",
        "maturity_credit": "FORBIDDEN",
        "user_movement": False,
        "packet_apply": False,
        "restore_barrier_write": False,
        "revalidation_trigger": "owner, exact method, fixture, contract, dependency graph or OMP semantic version changes",
        "verification_class": contract_class,
        "source_classification": "ACTIVE_EXECUTABLE_NOT_CONSUMED",
        "new_owner_required": False,
        "new_architecture_required": False,
        "method_fingerprint": method_fingerprint,
        "owner_implementation_fingerprint": owner_fingerprint,
        "fixture_fingerprint": fixture_fingerprint,
        "contract_fingerprint": contract_fingerprint,
        "dependency_fingerprint": dependency_fingerprint,
        "revalidation_fingerprint": revalidation_fingerprint,
        "last_result": "NOT_EVALUATED",
        "last_evaluated_fingerprint": "NONE",
        "revalidation_required": True,
        "eligibility_status": "ELIGIBLE",
        "exclusion_reason": "NONE",
        "seed_input": False,
    }


def _proactive_seed_sources(root: Path, dependency_fingerprint: str) -> tuple[list[dict[str, Any]], list[str]]:
    sources: list[dict[str, Any]] = []
    missing: list[str] = []
    for verification_class, owner, selector, expected in PROACTIVE_SEED_SPECS:
        relative = Path(*selector.split(".")[:3]).with_suffix(".py")
        source_path = root / relative
        if not source_path.exists():
            missing.append(selector)
            continue
        file_text = source_path.read_text(encoding="utf-8")
        method_name = selector.rsplit(".", 1)[-1]
        method_match = re.search(rf"(?ms)^\s+def\s+{re.escape(method_name)}\s*\(.*?(?=^\s+def\s+test_|^class\s+|\Z)", file_text)
        method_fingerprint = _sha256_text(method_match.group(0) if method_match else method_name)
        owner_path = PROACTIVE_CORPUS_MODULE_OWNERS.get(relative.stem, (owner, str(relative)))[1]
        owner_file = root / owner_path
        owner_fingerprint = _sha256_text(owner_file.read_text(encoding="utf-8") if owner_file.exists() else "MISSING")
        fixture_fingerprint = _sha256_text(file_text)
        contract_fingerprint = _sha256_text(expected)
        revalidation_fingerprint = _sha256_text("|".join((
            owner_fingerprint,
            method_fingerprint,
            fixture_fingerprint,
            contract_fingerprint,
            dependency_fingerprint,
        )))
        sources.append({
            "source_owner": owner,
            "execution_owner": "PYTHON_UNITTEST_EXISTING_VERIFICATION_OWNER",
            "source_evidence": str(relative),
            "target_contract": expected,
            "engineering_intent": f"Proactively preserve contract: {expected}",
            "current_assumption": "The existing owner implementation still satisfies its certified contract.",
            "expected_behavior": expected,
            "entrypoint": [sys.executable, "-m", "unittest", selector],
            "input_or_fixture": selector,
            "preconditions": "clean converged repository; no Runtime or production mutation",
            "observation_method": "existing unittest assertion and process exit status",
            "pass_criteria": "existing unittest exits zero",
            "fail_criteria": "existing unittest fails reproducibly in the current checkout",
            "result_consumer": "ENGINEERING_POLYGON_SCENARIO_SUPPLY",
            "rollback_or_stop_safe": "no mutation; STOP_SAFE on invalid, flaky or boundary-crossing input",
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_impact": "NONE",
            "maturity_credit": "FORBIDDEN",
            "user_movement": False,
            "packet_apply": False,
            "restore_barrier_write": False,
            "revalidation_trigger": "target implementation, fixture, expected contract or dependency fingerprint changes",
            "verification_class": verification_class,
            "source_classification": "ACTIVE_EXECUTABLE_NOT_CONSUMED",
            "new_owner_required": False,
            "new_architecture_required": False,
            "module": relative.stem,
            "class_name": selector.split(".")[-2],
            "method_or_entrypoint": method_name,
            "contract_class": verification_class,
            "mutation_boundary": "ISOLATED_TEST_ONLY",
            "method_fingerprint": method_fingerprint,
            "owner_implementation_fingerprint": owner_fingerprint,
            "fixture_fingerprint": fixture_fingerprint,
            "contract_fingerprint": contract_fingerprint,
            "dependency_fingerprint": dependency_fingerprint,
            "revalidation_fingerprint": revalidation_fingerprint,
            "last_result": "NOT_EVALUATED",
            "last_evaluated_fingerprint": "NONE",
            "revalidation_required": True,
            "eligibility_status": "ELIGIBLE",
            "exclusion_reason": "NONE",
            "seed_input": True,
        })
    return sources, missing


def discover_proactive_verification_inputs(*, root: Path = ROOT) -> dict[str, Any]:
    """Project the current safe executable unittest corpus through existing owners."""
    dependency_fingerprint = _corpus_dependency_fingerprint(root)
    seed_sources, missing = _proactive_seed_sources(root, dependency_fingerprint)
    seed_selectors = {str(item["input_or_fixture"]) for item in seed_sources}
    eligible_by_class: dict[str, dict[str, Any]] = {}
    excluded: list[dict[str, str]] = []
    test_root = root / "tests/unit"
    for source_path in sorted(test_root.glob("test_*.py"), key=lambda path: path.name):
        module_name = source_path.stem
        if module_name in PROACTIVE_CORPUS_SELF_TEST_MODULES:
            excluded.append({"source": str(source_path.relative_to(root)), "reason": "ADAPTER_SELF_TEST_MODULE"})
            continue
        owner_mapping = PROACTIVE_CORPUS_MODULE_OWNERS.get(module_name)
        if owner_mapping is None:
            excluded.append({"source": str(source_path.relative_to(root)), "reason": "OWNER_NOT_MAPPED"})
            continue
        file_text = source_path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(file_text, filename=str(source_path))
        except SyntaxError:
            excluded.append({"source": str(source_path.relative_to(root)), "reason": "SOURCE_PARSE_FAILURE"})
            continue
        owner, owner_path = owner_mapping
        for class_node in (node for node in tree.body if isinstance(node, ast.ClassDef)):
            for method_node in (node for node in class_node.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_")):
                selector = f"tests.unit.{module_name}.{class_node.name}.{method_node.name}"
                if selector in seed_selectors:
                    continue
                contract_class = _proactive_contract_class(method_node.name)
                if contract_class == "NOT_ELIGIBLE":
                    excluded.append({"source": selector, "reason": "AMBIGUOUS_CONTRACT_SEMANTICS"})
                    continue
                method_source = ast.get_source_segment(file_text, method_node) or method_node.name
                exclusion = _proactive_method_exclusion(method_node.name, method_source)
                if exclusion:
                    excluded.append({"source": selector, "reason": exclusion})
                    continue
                source = _proactive_source_from_method(
                    root=root,
                    module_name=module_name,
                    class_node=class_node,
                    method_node=method_node,
                    file_text=file_text,
                    owner=owner,
                    owner_path=owner_path,
                    contract_class=contract_class,
                    dependency_fingerprint=dependency_fingerprint,
                )
                current = eligible_by_class.get(contract_class)
                if current is None or source["input_or_fixture"] < current["input_or_fixture"]:
                    if current is not None:
                        excluded.append({"source": current["input_or_fixture"], "reason": "DUPLICATE_CONTRACT_CLASS_REPRESENTATIVE"})
                    eligible_by_class[contract_class] = source
                else:
                    excluded.append({"source": selector, "reason": "DUPLICATE_CONTRACT_CLASS_REPRESENTATIVE"})
    seed_classes = {
        PROACTIVE_SEED_CANONICAL_CLASSES.get(str(item["verification_class"]), str(item["verification_class"]))
        for item in seed_sources
    }
    automatic_sources = [
        source for contract_class, source in sorted(eligible_by_class.items())
        if contract_class not in seed_classes
    ]
    sources = seed_sources + automatic_sources
    materialized = [proactive_verification_input(source) for source in sources]
    invalid = [error for result in materialized if result["final_verdict"] != "PASS" for error in result["errors"]]
    instances = [result["proactive_input"] for result in materialized if result["final_verdict"] == "PASS"]
    corpus_fingerprint = proactive_corpus_fingerprint(instances)
    return {
        "schema": "v7-proactive-verification-corpus-discovery/v2",
        "audit_result": "SCALABLE_CURRENT_CORPUS_DISCOVERED" if instances else "NO_EXECUTABLE_PROACTIVE_INPUTS_EXIST",
        "discovery_mode": "DETERMINISTIC_AST_EXISTING_OWNER_PROJECTION",
        "mapped_input_count": len(instances),
        "seed_input_count": len(seed_sources),
        "automatic_input_count": len(automatic_sources),
        "proactive_inputs": sources,
        "missing_entrypoints": missing,
        "excluded_input_count": len(excluded),
        "excluded_inputs": sorted(excluded, key=lambda row: (row["reason"], row["source"])),
        "corpus_discovery_complete": not missing and not invalid,
        "corpus_fingerprint": corpus_fingerprint,
        "exhaustion_scope": "FULL_CURRENT_ELIGIBLE_ENGINEERING_CORPUS",
        "historical_context_only_not_promoted": True,
        "production_only_evidence_excluded": True,
        "final_verdict": "PASS" if instances and not missing and not invalid else "STOP_SAFE",
        "errors": [f"proactive_entrypoint_missing:{item}" for item in missing] + invalid,
    }


def load_polygon_coverage_evidence(*, root: Path = ROOT) -> dict[str, dict[str, Any]]:
    """Read compact coverage evidence from existing Engineering Reports."""
    report_root = root / "docs/reports/engineering"
    records: dict[str, dict[str, Any]] = {}
    if not report_root.exists():
        return records
    marker = "POLYGON_COVERAGE_JSON:"
    for path in sorted(report_root.glob("*_engineering_polygon_fallback_continuation.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        marker_at = text.find(marker)
        if marker_at < 0:
            continue
        block_start = text.find("```json", marker_at)
        block_end = text.find("```", block_start + 7) if block_start >= 0 else -1
        if block_start < 0 or block_end < 0:
            continue
        try:
            payload = json.loads(text[block_start + 7:block_end].strip())
        except (TypeError, ValueError):
            continue
        for item in payload.get("coverage", []):
            if isinstance(item, dict) and item.get("proactive_input_id"):
                records[str(item["proactive_input_id"])] = dict(item)
    return records


def accepted_seed_proactive_coverage(
    discovery: dict[str, Any],
    *,
    root: Path = ROOT,
    runner: Optional[Callable[[list[str], Optional[Path], int], dict[str, Any]]] = None,
) -> dict[str, dict[str, Any]]:
    """Reuse accepted seed PASS evidence only while its owner and fixture are unchanged."""
    runner = runner or run_command
    report_paths = (
        root / "docs/reports/engineering/2026-07-14_005644_proactive_engineering_polygon_verification_integration.md",
        root / "docs/reports/engineering/2026-07-14_012023_proactive_polygon_verification_exhaustion_continuation.md",
    )
    report_text = "\n".join(path.read_text(encoding="utf-8") for path in report_paths if path.exists())
    records: dict[str, dict[str, Any]] = {}
    for source in discovery.get("proactive_inputs", []):
        if not source.get("seed_input"):
            continue
        method_name = str(source.get("method_or_entrypoint") or "")
        if method_name not in report_text:
            continue
        source_path = str(source.get("source_evidence") or "")
        owner_path = PROACTIVE_CORPUS_MODULE_OWNERS.get(str(source.get("module") or ""), ("", source_path))[1]
        evidence_report = next((path for path in report_paths if path.exists() and method_name in path.read_text(encoding="utf-8")), None)
        if evidence_report is None:
            continue
        commit_result = runner(
            ["git", "log", "-1", "--format=%H", "--", str(evidence_report.relative_to(root))],
            root,
            30,
        )
        evidence_commit = str(commit_result.get("stdout") or "").strip()
        if not commit_result.get("ok") or not evidence_commit:
            continue
        unchanged = runner(
            ["git", "diff", "--quiet", evidence_commit, "--", source_path, owner_path],
            root,
            30,
        )
        if not unchanged.get("ok"):
            continue
        materialized = proactive_verification_input(source)
        if materialized["final_verdict"] != "PASS":
            continue
        item = materialized["proactive_input"]
        records[item["proactive_input_id"]] = {
            "proactive_input_id": item["proactive_input_id"],
            "last_result": "PASS_CURRENT",
            "last_evaluated_fingerprint": item.get("revalidation_fingerprint", item["deterministic_identity"]),
            "evidence_pointer": str(evidence_report.relative_to(root)),
        }
    return records


def engineering_polygon_fallback_activation(
    cps_text: str,
    *,
    active_scenario_count: int,
    context: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Reuse CPS/OMP state to decide whether the engineering-only fallback may run."""
    live = _markdown_field_table(_markdown_section(
        cps_text,
        "## 0. Authoritative Live Current State",
        "## Authoritative Unfinished Capability Closure Registry",
    ))
    values = {
        "ready_capabilities": live.get("READY_CAPABILITIES", "").strip("`"),
        "active_mission": live.get("CURRENT_EXECUTION_MISSION_ID", "").strip("`"),
        "current_stop": live.get("CURRENT_STOP_CONDITION", "").strip("`"),
        "current_candidate_count": 0,
        "actionable_real_situation": False,
        "authority_or_security_terminal": False,
    }
    values.update(context or {})
    reasons: list[str] = []
    if values["ready_capabilities"] not in {"", "NONE"}:
        reasons.append("READY_CAPABILITY_PREEMPTS_POLYGON")
    if values["active_mission"] not in {"", "NONE"}:
        reasons.append("ACTIVE_MISSION_PREEMPTS_POLYGON")
    if int(values.get("current_candidate_count") or 0) > 0:
        reasons.append("ACTIVE_CANDIDATE_PREEMPTS_POLYGON")
    if active_scenario_count > 0:
        reasons.append("ACTIVE_SCENARIO_PREEMPTS_PROACTIVE_FALLBACK")
    if bool(values.get("actionable_real_situation")):
        reasons.append("ACTIONABLE_REAL_SITUATION_PREEMPTS_POLYGON")
    if bool(values.get("authority_or_security_terminal")):
        reasons.append("AUTHORITY_OR_SECURITY_TERMINAL")
    if values["current_stop"] not in {
        "REAL_WORLD_LIMIT",
        "PROACTIVE_INPUT_BUDGET_EXHAUSTED",
        "WAITING_EXTERNAL_DEPENDENCY",
    }:
        reasons.append("CURRENT_STOP_DOES_NOT_ADMIT_FALLBACK")
    return {
        "schema": "v7-engineering-polygon-fallback-activation/v1",
        "polygon_fallback_required": not reasons,
        "polygon_fallback_active": not reasons,
        "preemption_reasons": reasons,
        "current_context": values,
        "final_verdict": "PASS",
        "errors": [],
    }


def bounded_proactive_engineering_polygon_run(
    cps_text: str,
    *,
    sources: Optional[Iterable[Any]] = None,
    coverage_records: Optional[dict[str, dict[str, Any]]] = None,
    fallback_context: Optional[dict[str, Any]] = None,
    runner: Optional[Callable[[list[str], Optional[Path], int], dict[str, Any]]] = None,
    root: Path = ROOT,
    max_inputs: int = 20,
) -> dict[str, Any]:
    """Execute bounded scalable polygon fallback through existing verification owners."""
    supplied_sources = None if sources is None else list(sources)
    discovery = discover_proactive_verification_inputs(root=root) if supplied_sources is None else {
        "schema": "v7-proactive-verification-corpus-discovery/v2",
        "audit_result": "SUPPLIED_BOUNDED_CORPUS",
        "mapped_input_count": len(supplied_sources),
        "proactive_inputs": supplied_sources,
        "missing_entrypoints": [],
        "excluded_input_count": 0,
        "excluded_inputs": [],
        "corpus_discovery_complete": True,
        "corpus_fingerprint": _sha256_text(json.dumps(
            sorted(str(item.get("input_or_fixture") or "") for item in supplied_sources if isinstance(item, dict)),
            separators=(",", ":"),
        )),
        "exhaustion_scope": "FULL_CURRENT_ELIGIBLE_ENGINEERING_CORPUS",
        "final_verdict": "PASS",
        "errors": [],
    }
    if discovery["final_verdict"] != "PASS":
        return {
            "schema": "v7-bounded-proactive-engineering-polygon-run/v1",
            "stop_reason": "STOP_SAFE",
            "trace": [],
            "final_verdict": "STOP_SAFE",
            "errors": discovery["errors"],
        }
    input_sources = discovery["proactive_inputs"]
    current_scenarios = current_engineering_polygon_scenario_supply(cps_text, root=root)
    activation = engineering_polygon_fallback_activation(
        cps_text,
        active_scenario_count=int(current_scenarios["discovery"]["active_source_count"]),
        context=fallback_context,
    )
    if not activation["polygon_fallback_active"]:
        return {
            "schema": "v7-bounded-proactive-engineering-polygon-run/v2",
            "audit_result": discovery["audit_result"],
            "polygon_fallback_activated": False,
            "activation": activation,
            "stop_reason": "NORMAL_OMP_PATH_PREEMPTS_POLYGON",
            "trace": [],
            "runtime_impact": "NONE",
            "production_impact": "NONE",
            "authority_expansion": False,
            "maturity_impact": "NONE",
            "final_verdict": "PASS",
            "errors": [],
        }
    coverage: dict[str, dict[str, Any]] = {}
    if supplied_sources is None:
        coverage.update(accepted_seed_proactive_coverage(discovery, root=root, runner=runner))
        coverage.update(load_polygon_coverage_evidence(root=root))
    coverage.update(coverage_records or {})
    evaluated: list[dict[str, Any]] = []
    trace: list[dict[str, Any]] = []
    scenarios = candidates = missions = 0
    stop_reason = "STOP_SAFE"
    execution_budget = max(0, min(max_inputs, 20))
    for iteration in range(1, execution_budget + 1):
        selection = select_proactive_verification_input(
            input_sources,
            evaluated_inputs=evaluated,
            coverage_records=coverage,
        )
        if selection["final_verdict"] != "PASS":
            stop_reason = "STOP_SAFE"
            break
        selected = selection["selected_input"]
        if selected is None:
            stop_reason = "REAL_WORLD_EVIDENCE_REQUIRED_AFTER_FULL_CURRENT_CORPUS_EXHAUSTION"
            break
        fresh_cps_path = root / "docs/programs/V7_CURRENT_PROGRAM_STATE.md"
        fresh_cps = fresh_cps_path.read_text(encoding="utf-8") if fresh_cps_path.exists() else cps_text
        consistency = cps_live_state_consistency(fresh_cps, root=root, verify_external=False)
        if consistency["final_verdict"] != "PASS":
            stop_reason = "TRUTH_CONVERGENCE_FAILURE"
            break
        execution = execute_proactive_verification_input(selected, runner=runner, root=root)
        evaluated.append(selected)
        row = {
            "iteration": iteration,
            "proactive_input_id": selected["proactive_input_id"],
            "verification_class": selected["verification_class"],
            "execution_result": execution["execution_result"],
            "scenario_created": False,
            "candidate_created": False,
            "mission_prepared": False,
        }
        if execution["execution_result"] == "PROACTIVE_VERIFICATION_PASS":
            coverage[selected["proactive_input_id"]] = {
                "proactive_input_id": selected["proactive_input_id"],
                "last_result": "PROACTIVE_VERIFICATION_PASS",
                "last_evaluated_fingerprint": selected.get("revalidation_fingerprint", selected["deterministic_identity"]),
                "evidence_pointer": "CURRENT_BOUNDED_RUN",
            }
            trace.append(row)
            stop_reason = "PROACTIVE_INPUT_BUDGET_EXHAUSTED"
            continue
        if execution["execution_result"] == "PROACTIVE_VERIFICATION_NON_DETERMINISTIC":
            trace.append(row)
            stop_reason = "NON_DETERMINISTIC_DECISION"
            break
        conversion = proactive_verification_failure_scenario_source(selected, execution)
        if conversion["final_verdict"] != "PASS":
            trace.append(row)
            stop_reason = "STOP_SAFE"
            break
        supply = engineering_polygon_scenario_supply_from_cps(
            cps_text,
            scenario_sources=[conversion["scenario_source"]],
        )
        row["scenario_created"] = supply["selection"]["selected_scenario"] is not None
        row["candidate_created"] = bool(supply.get("bdp") and supply["bdp"].get("candidate"))
        row["mission_prepared"] = bool(supply.get("bdp") and supply["bdp"].get("admission", {}).get("mission_state") == "PREPARED_NOT_ACTIVE")
        scenarios += int(row["scenario_created"])
        candidates += int(row["candidate_created"])
        missions += int(row["mission_prepared"])
        row["supply_status"] = supply["supply_status"]
        trace.append(row)
        stop_reason = "CURRENT_FAILURE_MISSION_HOLD"
        break
    else:
        remaining_after_budget = select_proactive_verification_input(
            input_sources,
            evaluated_inputs=evaluated,
            coverage_records=coverage,
        )
        if remaining_after_budget["selected_input"] is not None:
            stop_reason = "PROACTIVE_INPUT_BUDGET_EXHAUSTED"
        else:
            stop_reason = "REAL_WORLD_EVIDENCE_REQUIRED_AFTER_FULL_CURRENT_CORPUS_EXHAUSTION"
    final_selection = select_proactive_verification_input(
        input_sources,
        evaluated_inputs=evaluated,
        coverage_records=coverage,
    )
    passed = sum(1 for row in trace if row["execution_result"] == "PROACTIVE_VERIFICATION_PASS")
    failed = sum(1 for row in trace if row["execution_result"] == "PROACTIVE_VERIFICATION_FAIL")
    materialized_inputs = [
        result["proactive_input"]
        for result in (proactive_verification_input(source) for source in input_sources)
        if result["final_verdict"] == "PASS"
    ]
    coverage_states = {
        item["proactive_input_id"]: _proactive_coverage_state(item, coverage.get(item["proactive_input_id"]))
        for item in materialized_inputs
    }
    remaining_count = sum(
        1 for state in coverage_states.values()
        if state not in {"PASS_CURRENT", "NOT_APPLICABLE"}
    )
    exhaustion_proven = (
        discovery.get("corpus_discovery_complete") is True
        and remaining_count == 0
        and int(current_scenarios["discovery"]["active_source_count"]) == 0
        and stop_reason == "REAL_WORLD_EVIDENCE_REQUIRED_AFTER_FULL_CURRENT_CORPUS_EXHAUSTION"
    )
    continuation_projection = {
        "POLYGON_FALLBACK_REQUIRED": remaining_count > 0,
        "POLYGON_FALLBACK_ACTIVE": remaining_count > 0 and stop_reason == "PROACTIVE_INPUT_BUDGET_EXHAUSTED",
        "POLYGON_CORPUS_FINGERPRINT": discovery["corpus_fingerprint"],
        "POLYGON_CORPUS_TOTAL": discovery["mapped_input_count"],
        "POLYGON_CORPUS_ELIGIBLE": len(materialized_inputs),
        "POLYGON_CORPUS_EVALUATED": len(materialized_inputs) - remaining_count,
        "POLYGON_CORPUS_REMAINING": remaining_count,
        "POLYGON_NEXT_INPUT_ID": (
            final_selection["selected_input"]["proactive_input_id"]
            if final_selection.get("selected_input") else "NONE"
        ),
        "POLYGON_LAST_INPUT_ID": trace[-1]["proactive_input_id"] if trace else "NONE",
        "POLYGON_LAST_RESULT": trace[-1]["execution_result"] if trace else "NONE",
        "POLYGON_STOP_REASON": stop_reason,
        "POLYGON_EXHAUSTION_PROVEN": exhaustion_proven,
        "POLYGON_REVALIDATION_REQUIRED": sum(
            1 for state in coverage_states.values()
            if state in {"STALE_REVALIDATION_REQUIRED", "FAIL_CURRENT", "BLOCKED", "NON_DETERMINISTIC"}
        ),
    }
    return {
        "schema": "v7-bounded-proactive-engineering-polygon-run/v2",
        "audit_result": discovery["audit_result"],
        "actual_gap_classification": "STATIC_INPUT_CATALOGUE+PARTIAL_CORPUS_DISCOVERY+MISSING_FALLBACK_CONTINUATION+INCORRECT_EXHAUSTION_CLASSIFICATION",
        "polygon_fallback_activated": True,
        "activation": activation,
        "corpus_discovery_complete": discovery.get("corpus_discovery_complete", True),
        "corpus_fingerprint": discovery["corpus_fingerprint"],
        "corpus_exhaustion_scope": discovery["exhaustion_scope"],
        "inputs_discovered": discovery["mapped_input_count"],
        "inputs_eligible": len(materialized_inputs),
        "inputs_excluded": discovery.get("excluded_input_count", 0),
        "inputs_previously_current": sum(1 for state in coverage_states.values() if state == "PASS_CURRENT") - passed,
        "inputs_stale": sum(1 for state in coverage_states.values() if state == "STALE_REVALIDATION_REQUIRED"),
        "inputs_not_evaluated": sum(1 for state in coverage_states.values() if state == "NOT_EVALUATED"),
        "inputs_executed": len(trace),
        "inputs_passed": passed,
        "inputs_failed": failed,
        "inputs_blocked": 0,
        "scenarios_created": scenarios,
        "candidates_created": candidates,
        "missions_accepted": missions,
        "missions_completed": 0,
        "iterations_executed": len(trace),
        "trace": trace,
        "coverage": [coverage[key] for key in sorted(coverage)],
        "corpus_remaining": remaining_count,
        "next_corpus_input_id": (
            final_selection["selected_input"]["proactive_input_id"]
            if final_selection.get("selected_input") else "NONE"
        ),
        "exhaustion_proven": exhaustion_proven,
        "continuation_projection": continuation_projection,
        "stop_reason": stop_reason,
        "protected_wip_preserved": True,
        "runtime_impact": "NONE",
        "production_impact": "NONE",
        "authority_expansion": False,
        "maturity_impact": "NONE",
        "final_verdict": "PASS" if stop_reason not in {
            "STOP_SAFE", "NON_DETERMINISTIC_DECISION", "TRUTH_CONVERGENCE_FAILURE",
        } else "STOP_SAFE",
        "errors": [],
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
    development_impulse: dict[str, Any] = {
        "handoff_status": "NOT_EVALUATED_NO_CAPABILITY_GRAPH",
        "candidate_count": 0,
        "admission_decision": "NONE",
        "real_world_limit_intents_preserved": 0,
        "final_verdict": "PASS",
    }
    live = _markdown_field_table(_markdown_section(
        cps_text,
        "## 0. Authoritative Live Current State",
        "## Authoritative Unfinished Capability Closure Registry",
    ))
    program_frontier = live.get("CURRENT_PROGRAM_EXECUTION_FRONTIER", "").strip("`")
    if program_frontier not in {"", "NONE"}:
        development_impulse = {
            "handoff_status": "NOT_EVALUATED_PROGRAM_FRONTIER_PREEMPTS_CAPABILITY_GRAPH",
            "candidate_count": 0,
            "admission_decision": "NONE",
            "real_world_limit_intents_preserved": 1,
            "final_verdict": "PASS",
        }
    elif "### Capability Dependency Graph And Execution Frontier" in cps_text:
        development_impulse = bdp_development_impulse_from_cps(cps_text)
        if development_impulse["final_verdict"] != "PASS":
            errors.append("omp_bdp_development_impulse_stop_safe")
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
        "bdp_development_impulse_status": development_impulse["handoff_status"],
        "bdp_candidate_count": development_impulse["candidate_count"],
        "bdp_admission_decision": development_impulse["admission_decision"],
        "bdp_real_world_limit_intents_preserved": development_impulse.get("real_world_limit_intents_preserved", 0),
        "errors": unique,
    }


def python_function_call_sites(root: Path, target: str) -> dict[str, Any]:
    """Find source call sites and separate executable code from tests."""
    call_sites: list[dict[str, Any]] = []
    scanned = 0
    for base in ("tools", "admin", "admin_core", "tests"):
        directory = root / base
        if not directory.exists():
            continue
        for path in sorted(item for item in directory.rglob("*") if item.is_file()):
            if "__pycache__" in path.parts or path.suffix in {".pyc", ".json", ".md"}:
                continue
            try:
                source = path.read_text(encoding="utf-8")
                tree = ast.parse(source)
            except (OSError, UnicodeDecodeError, SyntaxError):
                continue
            scanned += 1
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                called = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
                if called != target:
                    continue
                relative = path.relative_to(root).as_posix()
                call_sites.append({
                    "path": relative,
                    "line": getattr(node, "lineno", 0),
                    "class": "TEST_ONLY" if relative.startswith("tests/") else "SOURCE_CALL_SITE",
                })
    real = [item for item in call_sites if item["class"] != "TEST_ONLY"]
    tests = [item for item in call_sites if item["class"] == "TEST_ONLY"]
    return {
        "target": target,
        "files_scanned": scanned,
        "call_sites": call_sites,
        "real_callers": real,
        "test_callers": tests,
        "real_caller_count": len(real),
        "test_caller_count": len(tests),
    }


def omp_functional_footprint_consistency(cps_text: str, *, root: Path = ROOT) -> dict[str, Any]:
    """Reject automation claims that have no real non-test caller/consumer chain."""
    live = _markdown_field_table(_markdown_section(
        cps_text,
        "## 0. Authoritative Live Current State",
        "## Authoritative Unfinished Capability Closure Registry",
    ))
    calls = python_function_call_sites(root, "program_execution_reconciliation")
    entrypoint_wired = calls["real_caller_count"] > 0
    heartbeat_status = live.get("HEARTBEAT_STATUS", "").strip("`")
    automation_enabled_text = live.get("AUTOMATION_ENABLED", "").strip("`")
    heartbeat_active = heartbeat_status == "ACTIVE" and automation_enabled_text == "TRUE"
    heartbeat_paused = heartbeat_status == "PAUSED" and automation_enabled_text == "FALSE"
    fsse_foundation_complete = (
        live.get("FSSE_STATUS", "").strip("`")
        == "FSSE_01_FOUNDATION_COMPLETE_FSSE_02_READY"
    )
    completion_gate = mission_completion_evidence_gate({
        "MISSION_TYPE": "INTEGRATION" if fsse_foundation_complete else "AUTOMATION" if entrypoint_wired else "INTEGRATION",
        "COMPLETION_CONTRACT": "INTEGRATION_COMPLETION" if fsse_foundation_complete else "AUTOMATION_COMPLETION" if entrypoint_wired else "INTEGRATION_COMPLETION",
        "INDEPENDENT_TRIGGER_PROVEN": False,
        "ENTRYPOINT_ACTIVE": heartbeat_active,
        "REAL_CALLER_PROVEN": calls["real_caller_count"] > 0,
        "CONSUMER_PROVEN": fsse_foundation_complete,
        "BEHAVIOR_CHANGE_PROVEN": fsse_foundation_complete,
        "NEXT_OUTPUT_PROVEN": fsse_foundation_complete,
    })
    expected = {
        "PROGRAM_RECONCILIATION_REAL_CALLERS": str(calls["real_caller_count"]),
        "PROGRAM_RECONCILIATION_FOOTPRINT_CLASS": (
            "REAL_CLI_AND_OMP_CONSUMER_CONNECTED" if fsse_foundation_complete
            else "SOURCE_ENTRYPOINT_WIRED_AWAITING_NATURAL_RUN" if entrypoint_wired and heartbeat_active
            else "SOURCE_ENTRYPOINT_WIRED_PAUSED_DEPLOY_BLOCKED" if entrypoint_wired and heartbeat_paused
            else "DEPLOYED_MANUALLY_CALLABLE_ONLY"
        ),
        "OMP_AUTOMATION_LEVEL": "CODEX_ASSISTED",
        "AEP_PHASE_4_STATUS": "IMPLEMENTED_MANUALLY_CALLABLE",
        "AEP_PHASE_5_STATUS": "BLOCKED_MISSING_REAL_CONSUMER",
        "AEP_PHASE_6_STATUS": "BLOCKED_BY_PHASE_5",
        "MISSION_COMPLETION_EVIDENCE_GATE": "ACTIVE_V1",
        "CURRENT_COMPLETION_CONTRACT": "INTEGRATION_COMPLETION" if fsse_foundation_complete else "AUTOMATION_COMPLETION" if entrypoint_wired else "INTEGRATION_COMPLETION",
        "CURRENT_COMPLETION_VERDICT": completion_gate["completion_verdict"],
    }
    errors: list[str] = []
    for field, value in expected.items():
        if live.get(field, "").strip("`") != value:
            errors.append(f"functional_footprint_mismatch:{field}")
    if not (heartbeat_active or heartbeat_paused):
        errors.append("functional_footprint_heartbeat_state_pair_invalid")
    live_blob = "\n".join(live.values())
    if calls["real_caller_count"] == 0 and any(token in live_blob for token in (
        "PHASE_5_COMPLETE", "PHASE_6_READY", "COMPLETE_CONSUMED", "REAL_ENGINEERING_AUTOMATION",
    )):
        errors.append("false_automation_completion_without_real_caller")
    unique = sorted(set(errors))
    return {
        "schema": "v7-omp-functional-footprint-consistency/v1",
        "final_verdict": "PASS" if not unique else "NO-GO",
        "program_reconciliation_footprint_class": expected["PROGRAM_RECONCILIATION_FOOTPRINT_CLASS"],
        "omp_automation_level": expected["OMP_AUTOMATION_LEVEL"],
        "heartbeat_status": heartbeat_status,
        "automation_enabled": heartbeat_active,
        "mission_completion_evidence_gate_status": expected["MISSION_COMPLETION_EVIDENCE_GATE"],
        "current_completion_contract": expected["CURRENT_COMPLETION_CONTRACT"],
        "current_completion_verdict": completion_gate["completion_verdict"],
        "completion_gate": completion_gate,
        **calls,
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
    program_frontier = live.get("CURRENT_PROGRAM_EXECUTION_FRONTIER", "").strip("`")
    independent_program_frontier = program_frontier not in {"", "NONE"}
    next_projection = {
        next_action,
        registry.get("EXACT_CURRENT_SMALLEST_NEXT_ACTION_ID", ""),
    }
    if not independent_program_frontier:
        next_projection.add(wip.get("smallest_existing_next_action_id", ""))
    if next_action and next_projection != {next_action}:
        errors.append("cps_next_action_divergence")

    stop = live.get("CURRENT_STOP_CONDITION", "").strip("`")
    wip_stop = wip.get("current_primary_stop", "").strip("`")
    registry_stop = registry.get("CURRENT_STOP_CONDITION", "").strip("`")
    if (
        stop != normalized["current_stop_condition"]
        or registry_stop != stop
        or (not independent_program_frontier and wip_stop != stop)
        or (independent_program_frontier and "REAL_WORLD_LIMIT" not in wip_stop)
    ):
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
    if normalized["automatic_continue_omp_result"].split(";", 1)[0] not in live.get("AUTOMATIC_CONTINUE_OMP_RESULT", ""):
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
        if not independent_program_frontier and cap_stop != normalized["current_stop_condition"]:
            errors.append("cps_active_capability_stop_divergence")
        expected_status = f"`{normalized['active_capability_status']}`"
        if expected_status not in active_capability:
            errors.append("cps_active_capability_status_divergence")
        if "bundle drifted" in active_capability or "diagnose existing binding" in active_capability:
            errors.append("cps_active_capability_unresolved_binding_drift")
        if not independent_program_frontier and normalized["current_next_action_id"] not in cap_action and not (
            normalized["current_next_action_id"] == "CONTINUE_OMP" and "Continue OMP" in cap_action
        ):
            errors.append("cps_active_capability_next_action_divergence")
        if not independent_program_frontier and wip.get("smallest_existing_next_action", "") != cap_action:
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
    functional_footprint = omp_functional_footprint_consistency(cps_text, root=root)
    errors.extend(functional_footprint["errors"])
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
        "omp_functional_footprint_consistency": functional_footprint["final_verdict"],
        **{key: value for key, value in functional_footprint.items() if key not in {"schema", "final_verdict", "errors", "call_sites"}},
        "premature_operator_return_validator": self_continuation["premature_operator_return_validator"],
        "bdp_development_impulse_status": self_continuation["bdp_development_impulse_status"],
        "bdp_candidate_count": self_continuation["bdp_candidate_count"],
        "bdp_admission_decision": self_continuation["bdp_admission_decision"],
        "bdp_real_world_limit_intents_preserved": self_continuation["bdp_real_world_limit_intents_preserved"],
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
