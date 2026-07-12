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
    "current_stop_condition": "SOURCE_SNAPSHOT_BINDING_MISMATCH",
    "current_active_scope": "SINGLE_USER_FAILOVER_POLICY",
    "current_safe_next_action": "CONTINUE OMP; EXISTING PLANNER MAY SELECT ONE FRESH ELIGIBLE CANDIDATE; GENERATE A FRESH PACKET; EXECUTE OR STOP_SAFE THROUGH EXISTING OWNERS",
    "current_scope_class": "BOUNDED_DELEGATED_POLICY",
    "current_execution_mission_id": "NONE",
    "current_execution_mission_state": "NONE",
    "latest_terminal_mission_id": "V7_OMP_CPS_DELEGATED_POLICY_LIVE_STATE_RECONCILIATION_V1",
    "latest_terminal_run_nonce": "V7_CPS_DAP_SYNC_V1_6F2A9C84E173",
    "latest_terminal_mission_state": "CPS_DELEGATED_POLICY_LIVE_STATE_RECONCILED_CONTINUE_OMP_READY",
    "latest_terminal_mission_report": "docs/reports/engineering/2026-07-12_104030_cps_delegated_policy_live_state_reconciliation.md",
    "latest_terminal_mission_started_at": "2026-07-12T10:40:30+0700",
    "previous_terminal_mission_id": "CAP-U01_FIRST_REAL_GOVERNED_OUTCOME_CLOSURE_V1",
    "previous_terminal_mission_report": "docs/reports/engineering/2026-07-12_101353_first_real_governed_outcome_closure.md",
    "authoritative_transition_input_mission_id": "V7_OMP_BINDING_ATOMIC_SNAPSHOT_AND_MISSION_IDENTITY_GUARD_V3",
    "authoritative_transition_input_state": "MISSION_IDENTITY_GUARD_AND_BINDING_STABILITY_CERTIFIED",
    "authoritative_transition_input_report": "docs/reports/engineering/2026-07-11_225321_operation_scoped_binding_atomic_snapshot_closure_v3.md",
    "current_mission_role": "LATEST_TERMINAL_MISSION",
    "current_mission_id": "V7_OMP_CPS_DELEGATED_POLICY_LIVE_STATE_RECONCILIATION_V1",
    "current_run_nonce": "V7_CPS_DAP_SYNC_V1_6F2A9C84E173",
    "current_mission_state": "CPS_DELEGATED_POLICY_LIVE_STATE_RECONCILED_CONTINUE_OMP_READY",
    "current_mission_report": "docs/reports/engineering/2026-07-12_104030_cps_delegated_policy_live_state_reconciliation.md",
    "state_captured": "2026-07-12T10:40:30+0700",
    "current_state_generation": "cpsgen_V7_CPS_DAP_SYNC_V1_6F2A9C84E173",
    "current_transition_id": "CPS_DELEGATED_POLICY_LIVE_STATE_RECONCILIATION_V1",
    "current_next_action_id": "CONTINUE_OMP",
    "binding_stability": "PASS",
    "binding_schema": "v7.operation-scoped-source-binding.v2",
    "routing_readiness_state": "PASS_CANDIDATE_SCOPED",
    "authority_required_now": "NO_INSIDE_APPROVED_POLICY",
    "current_action_class": "single-user governed candidate failover",
    "current_action_class_state": "GOVERNED_ONLY",
    "old_packets_reusable": "NO",
    "active_wip": "CAP-U01-FIRST-GOVERNED-CONTROLLED-RUN",
    "responsibility_class": "BOUNDED_DELEGATED_POLICY_EXECUTION",
    "last_responsible_link": "approved bounded policy -> fresh semantic Candidate -> stable operation-scoped binding v2 -> fresh packet admission -> one governed transaction or STOP_SAFE -> verification/outcome/learning",
    "smallest_existing_next_action": "`Continue OMP`; generate all identities fresh; no Candidate/packet/hash approval inside policy",
    "parent_engineering_intent": "INTENT_NOT_CLOSED",
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
        "Source": "bounded policy activation, safe delivery, production read-only certification and one terminal STOP_SAFE certification attempt.",
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
        "AUTHORITY_REQUIRED_NOW": "`NO_INSIDE_APPROVED_POLICY; Engineering Authority remains required for expansion`",
        "CURRENT_ACTION_CLASS": f"`{state['current_action_class']}`",
        "CURRENT_ACTION_CLASS_STATE": f"`{state['current_action_class_state']}`",
        "OLD_PACKETS_REUSABLE": f"`{state['old_packets_reusable']}`",
        "CURRENT_CLASS_CANDIDATE_SELECTED": "`NONE_OPEN`",
        "CURRENT_CLASS_OUTCOME": "`NO_ACTION`",
        "CURRENT_CLASS_DELTA_CLOSED": "`NO`",
        "PARENT_ENGINEERING_INTENT": f"`{state['parent_engineering_intent']}`",
        "AUTOMATIC_CONTINUE_OMP_RESULT": "`BOUNDED_POLICY_ACTIVATED; CAP-U01 preserved first; normal operator command is Continue OMP; no packet is durable between transactions`",
        "REQUIRED_WORKFLOW": "`Continue OMP -> fresh existing-Planner Candidate -> fresh packet -> policy admission -> live gates -> one bounded transaction or STOP_SAFE -> verification/rollback -> final OPEN -> outcome/learning/maturity`",
        "OMP_CONTROLLED_RUN_ALLOWED": "`CONTINUE_OMP_BOUNDED_POLICY; fresh Candidate and packet only; one serial transaction or STOP_SAFE`",
        "CONTROLLED_RUN_PRIMARY_STOP": f"`{state['current_stop_condition']}`",
        "CONTROLLED_RUN_RESPONSIBILITY_CLASS": f"`{state['responsibility_class']}`",
        "CONTROLLED_RUN_AUTHORITY_REQUIRED_NOW": "`NO_INSIDE_APPROVED_POLICY`",
        "CONTROLLED_RUN_EXECUTION_AUTHORIZED": "`BOUNDED_POLICY_ONLY; exact one-user class; all live gates mandatory`",
        "CONTROLLED_RUN_AUTHORITY_CLASS": "`BOUNDED_DELEGATED_POLICY; expansion requires Engineering Authority`",
        "CONTROLLED_RUN_AUTHORITY_GENERATION": "`POLICY_SCOPED; NO_PACKET_SPECIFIC_AUTHORITY_REQUIRED`",
        "CONTROLLED_RUN_AUTHORITY_DECISION": "`APPROVED_BOUNDED_SCOPE; packet-specific Authority is not reusable or required`",
        "CONTROLLED_RUN_INVALIDATION_REASON": "`SUPERSEDED/HISTORICAL: SOURCE_SNAPSHOT_BUNDLE_DRIFT; gap closed by binding v2 certification`",
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
        "authority_required_now": "`FALSE inside approved policy; TRUE only for expansion`",
        "last_responsible_link": state["last_responsible_link"],
        "smallest_existing_next_action": state["smallest_existing_next_action"],
        "binding_stability": "`CERTIFIED`",
        "completion_condition": "one governed action reaches verification/rollback, mandatory final `OPEN`, outcome/learning/maturity/CPS/OMP consumption",
    }
    for key, value in wip_values.items():
        cps_text = _replace_section_field(
            cps_text,
            "### Active Protected Work In Progress",
            "### Complete Or Locked Capability Records",
            key,
            value,
        )

    cap_section = _markdown_section(
        cps_text,
        "### Unfinished Capability Closure Records",
        "### Open Engineering Intents And Last Responsible Links",
    )
    cap_rows = [line for line in cap_section.splitlines() if line.startswith("| `CAP-U01` |")]
    if len(cap_rows) != 1:
        raise ValueError("cap_u01_missing_or_duplicate")
    cap_row = (
        "| `CAP-U01` | First Governed Controlled Run | Admin Safe Mode, execution packet/lease/pipeline, OMP | `ACTIVE` | "
        "`NOT_APPLICABLE_WITH_REASON: instance chain`; binding stability `CERTIFIED`; protected WIP `TRUE`; bounded policy `APPROVED` | "
        f"{state['last_responsible_link']} | `{state['current_stop_condition']}` | {state['smallest_existing_next_action']} | "
        "first; completion requires verification/rollback, final OPEN, outcome/learning/maturity/CPS/OMP; unblocks U03/U04/U05/U07/U08/U09 |"
    )
    cps_text = cps_text.replace(cap_rows[0], cap_row, 1)

    sequence = _markdown_section(cps_text, "### Deterministic Execution Sequence", "### Authority, Reality And Safety Stops")
    rows = [line for line in sequence.splitlines() if line.startswith("| `1` |")]
    if len(rows) != 1:
        raise ValueError("sequence_position_1_missing_or_duplicate")
    row = (
        f"| `1` | `U01` Controlled Run WIP; `{state['current_state_generation']}`; `{state['current_transition_id']}` | "
        "protected active root; binding v2 and bounded policy certified; no packet open | "
        f"`{state['current_next_action_id']}` | bounded delegated one-user transaction | `{state['current_stop_condition']}` | "
        "fresh Candidate -> fresh packet -> policy admission -> final live revalidation -> one transaction or legal no-action -> "
        "verification/rollback/final OPEN -> outcome/learning/maturity/promotion |"
    )
    return cps_text.replace(rows[0], row, 1)


def delegated_policy_live_state_consistency(cps_text: str, omp_text: str = "") -> dict[str, Any]:
    """Reject stale packet-approval authority projections inside the approved policy."""
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
    if not authority_required.startswith("NO_INSIDE_APPROVED_POLICY"):
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

    cap_rows = [line for line in capabilities.splitlines() if line.startswith("| `CAP-U01` |")]
    cap_u01 = cap_rows[0] if len(cap_rows) == 1 else ""
    sequence_rows = [line for line in sequence.splitlines() if line.startswith("| `1` |")]
    sequence_one = sequence_rows[0] if len(sequence_rows) == 1 else ""
    sequence_four_rows = [line for line in sequence.splitlines() if line.startswith("| `4` | `U01` |")]
    sequence_four = sequence_four_rows[0] if len(sequence_four_rows) == 1 else ""

    if "explicit approval" in sequence_four.lower() or "operational_authority" in sequence_four.lower():
        stale_operational.append("DETERMINISTIC_SEQUENCE_POSITION_4")
        contradictions.append("delegated_policy_sequence_requires_explicit_approval")
    if "fresh Candidate" not in sequence_one or "fresh packet" not in sequence_one or "policy admission" not in sequence_one:
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
    if stop == "OPERATIONAL_AUTHORITY":
        stale_operational.append("CURRENT_STOP_CONDITION")
        contradictions.append("delegated_policy_current_stop_is_operational_authority")
    registry_stop = registry.get("CURRENT_STOP_CONDITION", "").strip("`")
    wip_stop = wip.get("current_primary_stop", "").strip("`")
    cap_stop = ""
    if cap_u01:
        cells = [cell.strip() for cell in cap_u01.strip().strip("|").split("|")]
        cap_stop = cells[6].strip("`") if len(cells) > 6 else ""
    sequence_stop = ""
    if sequence_one:
        cells = [cell.strip() for cell in sequence_one.strip().strip("|").split("|")]
        sequence_stop = cells[5].strip("`") if len(cells) > 5 else ""
    stop_consistent = len({stop, registry_stop, wip_stop, cap_stop, sequence_stop}) == 1
    if not stop_consistent:
        contradictions.append("delegated_policy_cps_stop_divergence")

    next_action = live.get("CURRENT_NEXT_ACTION_ID", "").strip("`")
    next_consistent = (
        next_action == "CONTINUE_OMP"
        and registry.get("EXACT_CURRENT_SMALLEST_NEXT_ACTION_ID", "").strip("`") == next_action
        and wip.get("smallest_existing_next_action_id", "").strip("`") == next_action
        and "`CONTINUE_OMP`" in sequence_one
    )
    if not next_consistent:
        contradictions.append("delegated_policy_cps_next_action_divergence")

    cap_consistent = bool(cap_u01 and stop in cap_u01 and "Continue OMP" in cap_u01 and "explicit approval" not in cap_u01.lower())
    if not cap_consistent:
        contradictions.append("delegated_policy_cap_u01_divergence")
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
        "cap_u01_consistency": "PASS" if cap_consistent else "FAIL",
        "deterministic_sequence_consistency": "PASS" if sequence_consistent else "FAIL",
        "contradiction_count": len(contradiction_ids),
        "contradiction_ids": contradiction_ids,
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
        "PARENT_ENGINEERING_INTENT": normalized["parent_engineering_intent"],
    }
    for key, expected in exact_live.items():
        if live.get(key, "").strip("`") != expected:
            errors.append(f"cps_normalized_field_divergence:{key}")
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
    if not live.get("AUTHORITY_REQUIRED_NOW", "").strip("`").startswith("NO_INSIDE_APPROVED_POLICY"):
        errors.append("cps_authority_required_not_policy_bounded")
    if not wip.get("authority_required_now", "").strip("`").startswith("FALSE inside approved policy"):
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
    if live.get("CURRENT_CLASS_OUTCOME", "").strip("`") != "NO_ACTION":
        errors.append("cps_current_class_outcome_not_no_action")
    if live.get("CURRENT_ACTION_CLASS_STATE", "").strip("`") != "GOVERNED_ONLY":
        errors.append("cps_action_class_state_divergence")
    if "BOUNDED_POLICY_ACTIVATED" not in live.get("AUTOMATIC_CONTINUE_OMP_RESULT", ""):
        errors.append("cps_continue_omp_stop_divergence")
    if not live.get("OMP_CONTROLLED_RUN_ALLOWED", "").strip("`").startswith("CONTINUE_OMP_BOUNDED_POLICY"):
        errors.append("cps_omp_consumption_divergence")
    if not live.get("CONTROLLED_RUN_EXECUTION_AUTHORIZED", "").strip("`").startswith("BOUNDED_POLICY_ONLY"):
        errors.append("cps_execution_authority_not_policy_bounded")
    if live.get("CONTROLLED_RUN_RESPONSIBILITY_CLASS", "").strip("`") != "BOUNDED_DELEGATED_POLICY_EXECUTION":
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

    cap_rows = [line for line in capabilities.splitlines() if line.startswith("| `CAP-U01` |")]
    cap_u01 = cap_rows[0] if len(cap_rows) == 1 else ""
    if len(cap_rows) != 1:
        errors.append("cps_cap_u01_missing_or_duplicate")
    else:
        cap_cells = [cell.strip() for cell in cap_u01.strip().strip("|").split("|")]
        cap_stop = cap_cells[6].strip("`") if len(cap_cells) > 6 else ""
        cap_action = cap_cells[7] if len(cap_cells) > 7 else ""
        if cap_stop != normalized["current_stop_condition"]:
            errors.append("cps_cap_u01_stop_divergence")
        if "binding stability `CERTIFIED`" not in cap_u01 or "protected WIP `TRUE`" not in cap_u01:
            errors.append("cps_cap_u01_binding_not_certified")
        if "bundle drifted" in cap_u01 or "diagnose existing binding" in cap_u01:
            errors.append("cps_cap_u01_unresolved_binding_drift")
        if "Continue OMP" not in cap_action:
            errors.append("cps_cap_u01_next_action_divergence")
        if wip.get("smallest_existing_next_action", "") != cap_action:
            errors.append("cps_wip_cap_u01_next_action_divergence")
        if "final OPEN" not in cap_u01 or "outcome/learning/maturity/CPS/OMP" not in cap_u01:
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
        "cap_u01_consistency": delegated_live_state["cap_u01_consistency"],
        "deterministic_sequence_consistency": delegated_live_state["deterministic_sequence_consistency"],
        "registry_sequence_consistency": "PASS" if not any("sequence" in item or "cap_u01" in item or "next_action" in item for item in unique_errors) else "FAIL",
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
