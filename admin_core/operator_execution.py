"""Operator execution packet validation and audit persistence.

This module is intentionally narrow: it can validate a zero-movement operator
packet or a bounded nonzero clearance packet, run file rechecks, and append
approval/denial audit records. Its only runtime mutation is a canonical
restore-barrier clearance write for an already-approved selected-move set. It
never performs user movement, routing changes, service control, or autoswitch
apply actions.
"""

from __future__ import annotations

import argparse
import copy
import fcntl
import gzip
import hashlib
import json
import mmap
import os
import re
import secrets
import time
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from admin_core.sanitize import redact


ZERO_ACTION = "ZERO_MOVEMENT_GENERATION_CLEARANCE_RECHECK"
NONZERO_ACTION = "NONZERO_MOVEMENT_GENERATION_CLEARANCE_RECHECK"
RUNTIME_ACTION_RECORD_ONLY = "RECHECK_AND_RECORD_ONLY"
RUNTIME_ACTION_ZERO_MOVE_GOVERNANCE = "ZERO_MOVE_GOVERNANCE_STATE_TRANSITION"
RUNTIME_ACTION_CREATE_CLEARANCE = "CREATE_RESTORE_BARRIER_CLEARANCE"
RUNTIME_ACTION = RUNTIME_ACTION_RECORD_ONLY
ALLOWED_RUNTIME_ACTIONS = {
    RUNTIME_ACTION_RECORD_ONLY,
    RUNTIME_ACTION_ZERO_MOVE_GOVERNANCE,
    RUNTIME_ACTION_CREATE_CLEARANCE,
}
EMPTY_SELECTED_MOVES_HASH = hashlib.sha256(b"[]").hexdigest()
GOVERNANCE_PACKET_SCHEMA = "c1.governance-lifecycle-packet.v1"
ZERO_PACKET_SCHEMA = "e22.operator-execution-packet.v1"
CANONICAL_CLEARANCE_OWNER = "admin_core/operator_execution.py"
DEFAULT_CLEARANCE_TTL_SECONDS = 900
EXECUTION_LEASE_SCHEMA = "v7.execution-lease.v1"
DEFAULT_EXECUTION_LEASE_TTL_SECONDS = DEFAULT_CLEARANCE_TTL_SECONDS
AUTONOMOUS_EXECUTION_CONTROL_SCHEMA = "v7.autonomous-execution-control.v2"
DEFAULT_AUTONOMOUS_EXECUTION_CONTROL_FILE = Path("/etc/v7/admin/safe-mode.json")
AUTONOMOUS_EXECUTION_ROLLBACK_POLICY = "CERTIFIED_ROLLBACK_ONLY"
AUTONOMOUS_EXECUTION_ACTION_CLASSES = {
    "AUTHORITY_PROMOTION",
    "BOUNDED_REBALANCE",
    "DEGRADATION_MOVEMENT",
    "EMERGENCY_FAILOVER",
    "RECOVERY_ADMISSION",
    "USER_SWITCH",
}
LEASE_TERMINAL_STATUSES = {"EXECUTION_FINISHED", "ROLLBACK_FINISHED", "OPERATOR_CANCELLED"}
SELECTED_MOVE_SEMANTIC_FIELDS = (
    "reason",
    "important_services",
    "candidates",
    "scores",
    "service_failover",
    "availability_first_controlled_assignment",
)
MATERIAL_STATE_FIELDS = [
    "breaker_generation",
    "selected_move_hash",
    "source_bundle_hash",
    "source_hashes_hash",
    "snapshot_bundle_hash",
    "target_channel",
    "rollback_target",
    "policy_generation",
    "authority_generation",
    "blast_radius_eligibility",
    "rollback_readiness",
    "verification_prerequisites",
    "destination_eligibility",
    "source_eligibility",
]
APPROVED_PACKET_BINDING_FIELDS = [
    "packet_id",
    "decision_id",
    "operation_id",
    "selected_move_hash",
    "user",
    "source",
    "target",
    "authority_generation",
    "breaker_generation",
    "source_bundle_hash",
    "source_hashes_hash",
    "snapshot_bundle_hash",
    "max_users",
]
B15_CONTAINMENT_FORWARD_FIX_SCHEMA = "v7.b15-containment-forward-fix-classification.v1"
C5_ROLLBACK_OPERATIONAL_COMPENSATION_SCHEMA = "v7.c5-rollback-operational-compensation.v1"
ENGINEERING_AUTHORITY_REQUEST_SCHEMA = "v7.controlled-rollback-condition-engineering-authority-request.v1"
ENGINEERING_AUTHORITY_BINDING_SCHEMA = "v7.engineering-authority-binding.v1"
ENGINEERING_AUTHORITY_APPROVAL = "APPROVE_ONCE_AS_SCOPED"
ENGINEERING_AUTHORITY_REPAIR_CONTINUATION_POLICY_SCHEMA = "v7.controlled-rollback-repair-continuation-policy.v1"
CURRENT_ACTION_CLASS_CONTRACT_REQUEST_SCHEMA = "v7.current-action-class-contract-authority-request.v1"
CURRENT_ACTION_CLASS_CONTRACT_SCHEMA = "v7.current-action-class-contract.v2"
CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER = CANONICAL_CLEARANCE_OWNER
CURRENT_ACTION_CLASS_CONTRACT_MAX_TTL_SECONDS = 900
CURRENT_ACTION_CLASS_CONTRACT_REQUEST_TTL_SECONDS = 900
CURRENT_ACTION_CLASS_AUDIT_SCHEMA = "v7.current-action-class-contract-authority-audit.v1"
CURRENT_ACTION_CLASS_REQUEST_RECORD_TYPE = "current_action_class_contract_request_emitted"
DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE = Path("/opt/v7/audit/operator-execution-audit.jsonl")
STANDING_DELEGATED_POLICY_REQUEST_SCHEMA = "v7.standing-delegated-operational-policy-authority-request.v1"
STANDING_DELEGATED_POLICY_SCHEMA = "v7.standing-delegated-operational-policy.v1"
STANDING_DELEGATED_POLICY_REQUEST_RECORD_TYPE = "standing_delegated_operational_policy_request_emitted"
STANDING_DELEGATED_POLICY_DECISION_RECORD_TYPE = "standing_delegated_operational_policy_authority_decision"
STANDING_DELEGATED_POLICY_REQUEST_TTL_SECONDS = 24 * 60 * 60
STANDING_DELEGATED_POLICY_MAX_TTL_SECONDS = 30 * 24 * 60 * 60
STANDING_DELEGATED_POLICY_ID = "dap_default_tier1_readonly"
CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_SCHEMA = (
    "v7.controlled-certification-substrate-engineering-authority-request.v1"
)
CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_RECORD_TYPE = (
    "controlled_certification_substrate_authority_request_emitted"
)
CONTROLLED_CERTIFICATION_SUBSTRATE_DECISION_RECORD_TYPE = (
    "controlled_certification_substrate_authority_decision"
)
CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_TTL_SECONDS = 24 * 60 * 60
CONTROLLED_CERTIFICATION_SUBSTRATE_APPROVAL = (
    "APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN"
)
CONTROLLED_CERTIFICATION_SUBSTRATE_TIER48_PROFILE = "TIER48_CONTROLLED_CAMPAIGN"
CONTROLLED_CERTIFICATION_SUBSTRATE_CT_M0F_ONE_USER_PROFILE = (
    "CT_M0F_ONE_USER_SUBSTRATE"
)
CT_M0F_CONTROLLED_VALIDATION_REQUEST_SCHEMA = (
    "v7.ct-m0f-controlled-validation-engineering-authority-request.v1"
)
CT_M0F_CONTROLLED_VALIDATION_REQUEST_RECORD_TYPE = (
    "ct_m0f_controlled_validation_authority_request_emitted"
)
CT_M0F_CONTROLLED_VALIDATION_DECISION_RECORD_TYPE = (
    "ct_m0f_controlled_validation_authority_decision"
)
CT_M0F_CONTROLLED_VALIDATION_CONSUMPTION_RECORD_TYPE = (
    "ct_m0f_controlled_validation_admission_consumed"
)
CT_M0F_CONTROLLED_VALIDATION_APPROVAL = (
    "APPROVE_CT_M0F_CONTROLLED_VALIDATION_ONCE"
)
CT_M0F_CONTROLLED_VALIDATION_REQUEST_TTL_SECONDS = 24 * 60 * 60
CT_M0F_STANDING_VALIDATION_REQUEST_SCHEMA = (
    "v7.ct-m0f-standing-validation-authority-request.v1"
)
CT_M0F_STANDING_VALIDATION_CONTRACT_SCHEMA = (
    "v7.ct-m0f-standing-validation-policy.v1"
)
CT_M0F_STANDING_VALIDATION_REQUEST_RECORD_TYPE = (
    "ct_m0f_standing_validation_policy_request_emitted"
)
CT_M0F_STANDING_VALIDATION_DECISION_RECORD_TYPE = (
    "ct_m0f_standing_validation_policy_authority_decision"
)
CT_M0F_STANDING_VALIDATION_SAMPLE_RESERVATION_RECORD_TYPE = (
    "ct_m0f_standing_validation_sample_reserved"
)
CT_M0F_STANDING_VALIDATION_TRANSACTION_RESERVATION_RECORD_TYPE = (
    "ct_m0f_standing_validation_transaction_reserved"
)
CT_M0F_STANDING_VALIDATION_TRANSACTION_BINDING_RECORD_TYPE = (
    "ct_m0f_standing_validation_transaction_bound"
)
CT_M0F_STANDING_VALIDATION_TRANSACTION_TERMINAL_RECORD_TYPE = (
    "ct_m0f_standing_validation_transaction_terminal"
)
CT_M0F_STANDING_VALIDATION_SAMPLE_TERMINAL_RECORD_TYPE = (
    "ct_m0f_standing_validation_sample_terminal"
)
CT_M0F_STANDING_VALIDATION_FORWARD_RECORD_TYPE = (
    "ct_m0f_standing_validation_forward_evidence"
)
CT_M0F_STANDING_VALIDATION_LINEAGE_CHECKPOINT_RECORD_TYPE = (
    "ct_m0f_standing_validation_lineage_checkpoint"
)
CT_M0F_STANDING_VALIDATION_FINGERPRINT_SCOPED_RECORD_TYPES = {
    CT_M0F_STANDING_VALIDATION_SAMPLE_RESERVATION_RECORD_TYPE,
    CT_M0F_STANDING_VALIDATION_TRANSACTION_RESERVATION_RECORD_TYPE,
    CT_M0F_STANDING_VALIDATION_TRANSACTION_BINDING_RECORD_TYPE,
    CT_M0F_STANDING_VALIDATION_TRANSACTION_TERMINAL_RECORD_TYPE,
    CT_M0F_STANDING_VALIDATION_SAMPLE_TERMINAL_RECORD_TYPE,
    CT_M0F_STANDING_VALIDATION_FORWARD_RECORD_TYPE,
    CT_M0F_STANDING_VALIDATION_LINEAGE_CHECKPOINT_RECORD_TYPE,
}
CT_M0F_STANDING_VALIDATION_APPROVAL = (
    "APPROVE_STANDING_DELEGATED_CT_M0F_VALIDATION_POLICY"
)
CT_M0F_STANDING_VALIDATION_REQUEST_TTL_SECONDS = 24 * 60 * 60
CT_M0F_STANDING_VALIDATION_CONTRACT_TTL_SECONDS = 30 * 24 * 60 * 60
# This is deliberately short: it covers Matrix observation plus one governed
# handoff, rather than turning a certification source reservation into an
# indefinite identity pin.  Expiry is itself a release condition.
CT_M0F_STANDING_VALIDATION_TRANSACTION_TTL_SECONDS = 5 * 60
CT_M0F_STANDING_VALIDATION_POLICY_KEY = "ct_m0f_standing_validation_policy"
CONTROLLED_CERTIFICATION_CAMPAIGN_EFFECT_RECORD_TYPE = (
    "controlled_certification_substrate_effect"
)
CONTROLLED_CERTIFICATION_CAMPAIGN_STAGE_EFFECT_CLASS = (
    "CONTROLLED_SERVICE_FAILURE_CAMPAIGN_STAGE_CONSUMED"
)
CONTROLLED_CERTIFICATION_CAMPAIGN_STAGES = (5, 10, 25, 48)
AVAILABILITY_FIRST_CAMPAIGN_STAGE_EFFECT_CLASS = (
    "AVAILABILITY_FIRST_CAMPAIGN_STAGE_CONSUMED"
)
AVAILABILITY_FIRST_TARGET_BOUND_EFFECT_CLASS = (
    "AVAILABILITY_FIRST_TARGET_BOUND_CONSUMED"
)
CONTROLLED_CERTIFICATION_SUBSTRATE_SUBSCOPES = (
    "IDENTITY_PROVISIONING",
    "CERTIFICATION_CLASSIFICATION_AND_ASSIGNMENT",
    "CONTROLLED_SOURCE_CONDITION",
    "PROGRESSIVE_CAMPAIGN_EXECUTION",
)
CONTROLLED_SOURCE_TOPOLOGY_REQUEST_SCHEMA = (
    "v7.controlled-source-topology-authority-request.v1"
)
CONTROLLED_SOURCE_TOPOLOGY_REQUEST_RECORD_TYPE = (
    "controlled_source_topology_authority_request_emitted"
)
CONTROLLED_SOURCE_TOPOLOGY_DECISION_RECORD_TYPE = (
    "controlled_source_topology_authority_decision"
)
CONTROLLED_SOURCE_TOPOLOGY_INVALIDATION_RECORD_TYPE = (
    "controlled_source_topology_authority_request_invalidated"
)
CONTROLLED_SOURCE_TOPOLOGY_PROVISION_RECORD_TYPE = (
    "controlled_source_topology_provision_consumed"
)
CONTROLLED_SOURCE_TOPOLOGY_REQUEST_TTL_SECONDS = 24 * 60 * 60
CONTROLLED_SOURCE_TOPOLOGY_ACTIONS = {
    "REBIND_CONTROLLED_CERTIFICATION_SOURCE",
    "PROVISION_DEDICATED_CONTROLLED_CERTIFICATION_SOURCE",
}
CURRENT_ACTION_CLASS_REQUIRED_STOP_CONDITIONS = {
    "no_safe_target",
    "stale_or_changed_situation",
    "selected_move_identity_changed",
    "target_capacity_or_service_gate_failed",
    "verification_failure",
    "rollback_required",
    "authority_decision_expired",
    "one_use_consumed_or_contended",
}
CURRENT_ACTION_CLASS_AUTHORITY_RANK = {
    "CANARY": 0,
    "SMALL_BATCH": 1,
    "MEDIUM_BATCH": 2,
    "LARGE_BATCH": 3,
    "XLARGE_BATCH": 4,
    "FULL_INCIDENT": 5,
    "POOL": 5,
}


class PacketError(ValueError):
    pass


def utc_now():
    return datetime.now(timezone.utc)


def parse_ts(value):
    if not value:
        raise PacketError("missing_timestamp")
    text = str(value).replace("Z", "+00:00")
    if len(text) >= 5 and text[-5] in {"+", "-"} and text[-4:].isdigit():
        text = text[:-2] + ":" + text[-2:]
    try:
        dt = datetime.fromisoformat(text)
    except ValueError as exc:
        raise PacketError("invalid_timestamp") from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PacketError(f"cannot_read_json:{path}") from exc


def write_json_atomic(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    tmp.write_text(json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def mission_report_identity_guard(
    *,
    requested_mission_id: str,
    requested_run_nonce: str,
    mission_start_timestamp: str,
    report_path: Path,
    cps_text: str,
) -> dict[str, Any]:
    """Reject a report that is not bound to the requested Mission execution."""
    errors: list[str] = []
    try:
        report_text = report_path.read_text(encoding="utf-8")
        stat = report_path.stat()
    except OSError:
        report_text = ""
        stat = None
        errors.append("report_missing")
    expected_id = f"Mission ID: `{requested_mission_id}`"
    expected_nonce = f"Run Nonce: `{requested_run_nonce}`"
    lines = report_text.splitlines()
    if len(lines) < 2 or lines[0] != expected_id:
        errors.append("report_mission_id_mismatch")
    if len(lines) < 2 or lines[1] != expected_nonce:
        errors.append("report_run_nonce_mismatch")
    try:
        start = parse_ts(mission_start_timestamp).timestamp()
    except PacketError:
        start = 0.0
    report_created_at = float(getattr(stat, "st_birthtime", 0.0) or getattr(stat, "st_ctime", 0.0)) if stat else 0.0
    report_modified_at = float(getattr(stat, "st_mtime", 0.0)) if stat else 0.0
    if start <= 0:
        errors.append("mission_start_timestamp_invalid")
    elif min(report_created_at or report_modified_at, report_modified_at) + 0.001 < start:
        errors.append("report_predates_mission_start")
    if requested_mission_id not in cps_text:
        errors.append("cps_mission_id_mismatch")
    if requested_run_nonce not in cps_text:
        errors.append("cps_run_nonce_mismatch")
    return {
        "schema_version": "v7.mission-report-identity-guard.v1",
        "ok": not errors,
        "status": "MISSION_IDENTITY_MATCH" if not errors else "MISSION_CONTEXT_MISMATCH_STOP_SAFE",
        "errors": errors,
        "requested_mission_id": requested_mission_id,
        "requested_run_nonce": requested_run_nonce,
        "report_path": str(report_path),
        "report_created_after_mission_start": "report_predates_mission_start" not in errors and stat is not None,
        "report_identity_match": not any(item.startswith("report_") and item.endswith("mismatch") for item in errors),
        "cps_identity_match": not any(item.startswith("cps_") for item in errors),
    }


def sha256_json(payload):
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(encoded)


def sha256_file(path):
    try:
        return sha256_bytes(Path(path).read_bytes())
    except OSError:
        return ""


def canonical_json(data):
    return json.dumps(redact(data), sort_keys=True, ensure_ascii=True, separators=(",", ":"))


def stable_id(prefix, payload):
    return f"{prefix}_{sha256_bytes(canonical_json(payload).encode('utf-8'))[:24]}"


def build_autonomous_execution_control_state(
    enabled,
    *,
    actor,
    reason,
    now=None,
    operation_id="",
    selected_move_hash="",
    action_class="",
    source_bundle_hash="",
    snapshot_bundle_hash="",
    max_users=0,
):
    now = now or utc_now()
    enabled = bool(enabled)
    actor = str(actor or "admin").strip() or "admin"
    reason = str(reason or "operator_control").strip()[:240] or "operator_control"
    generation = stable_id("aec", {
        "enabled": enabled,
        "actor": actor,
        "reason": reason,
        "updated_at": now.isoformat(),
        "nonce": secrets.token_hex(16),
    })
    state = {
        "schema_version": AUTONOMOUS_EXECUTION_CONTROL_SCHEMA,
        "enabled": enabled,
        "state": "OPEN" if enabled else "CLOSED",
        "scope": "global" if enabled or not all([
            str(operation_id or ""),
            str(selected_move_hash or ""),
            str(action_class or ""),
            str(source_bundle_hash or ""),
            str(snapshot_bundle_hash or ""),
            as_int(max_users, 0) == 1,
        ]) else "operation",
        "generation": generation,
        "updated_at": now.isoformat(),
        "valid_until": "" if enabled else (now + timedelta(seconds=DEFAULT_EXECUTION_LEASE_TTL_SECONDS)).isoformat(),
        "updated_by": actor,
        "reason": reason,
        "rollback_policy": AUTONOMOUS_EXECUTION_ROLLBACK_POLICY,
    }
    if not enabled and state["scope"] == "operation":
        state.update({
            "operation_id": str(operation_id or ""),
            "selected_move_hash": str(selected_move_hash or ""),
            "action_class": str(action_class or "").upper(),
            "source_bundle_hash": str(source_bundle_hash or ""),
            "snapshot_bundle_hash": str(snapshot_bundle_hash or ""),
            "max_users": as_int(max_users, 0),
        })
    return state


def autonomous_execution_control_state(path=DEFAULT_AUTONOMOUS_EXECUTION_CONTROL_FILE, *, now=None):
    now = now or utc_now()
    blockers = []
    try:
        data = read_json(path)
    except PacketError:
        data = {}
        blockers.append("execution_control_missing_or_unreadable")
    if not isinstance(data, dict):
        data = {}
        blockers.append("execution_control_not_object")
    if data.get("schema_version") != AUTONOMOUS_EXECUTION_CONTROL_SCHEMA:
        blockers.append("execution_control_schema_unknown")
    enabled = data.get("enabled")
    state = str(data.get("state") or "")
    if not isinstance(enabled, bool):
        blockers.append("execution_control_enabled_invalid")
    expected_state = "OPEN" if enabled is True else ("CLOSED" if enabled is False else "")
    if state not in {"OPEN", "CLOSED", "HALF_OPEN"} or state != expected_state:
        blockers.append("execution_control_state_invalid")
    scope = str(data.get("scope") or "")
    if state == "OPEN" and scope != "global":
        blockers.append("execution_control_scope_unknown")
    if state == "CLOSED" and scope not in {"global", "operation"}:
        blockers.append("execution_control_scope_unknown")
    if state == "CLOSED" and scope == "operation":
        if not str(data.get("operation_id") or "").strip():
            blockers.append("execution_control_operation_id_missing")
        if not str(data.get("selected_move_hash") or "").strip():
            blockers.append("execution_control_selected_move_hash_missing")
        if str(data.get("action_class") or "").upper() not in AUTONOMOUS_EXECUTION_ACTION_CLASSES:
            blockers.append("execution_control_action_class_invalid")
        if not str(data.get("source_bundle_hash") or "").strip():
            blockers.append("execution_control_source_bundle_hash_missing")
        if not str(data.get("snapshot_bundle_hash") or "").strip():
            blockers.append("execution_control_snapshot_bundle_hash_missing")
        if as_int(data.get("max_users"), 0) != 1:
            blockers.append("execution_control_max_users_not_one")
    generation = str(data.get("generation") or "")
    if not generation.startswith("aec_"):
        blockers.append("execution_control_generation_invalid")
    if not str(data.get("updated_by") or "").strip():
        blockers.append("execution_control_actor_missing")
    if not str(data.get("reason") or "").strip():
        blockers.append("execution_control_reason_missing")
    if data.get("rollback_policy") != AUTONOMOUS_EXECUTION_ROLLBACK_POLICY:
        blockers.append("execution_control_rollback_policy_invalid")
    try:
        updated_at = parse_ts(data.get("updated_at"))
        if updated_at > now + timedelta(minutes=5):
            blockers.append("execution_control_updated_at_future")
    except PacketError:
        blockers.append("execution_control_updated_at_invalid")
    valid_until = None
    if state == "CLOSED":
        try:
            valid_until = parse_ts(data.get("valid_until"))
            if now >= valid_until:
                blockers.append("execution_control_closed_expired")
        except PacketError:
            blockers.append("execution_control_valid_until_invalid")
    return {
        **data,
        "enabled": enabled is True,
        "state": state or "UNKNOWN",
        "generation": generation,
        "valid": not blockers,
        "blockers": sorted(set(blockers)),
        "forward_mutation_allowed": not blockers and state == "CLOSED",
        "read_only_allowed": True,
        "valid_until": data.get("valid_until", ""),
    }


def autonomous_execution_control_decision(
    path=DEFAULT_AUTONOMOUS_EXECUTION_CONTROL_FILE,
    *,
    mutation_kind="forward",
    action_class="USER_SWITCH",
    expected_generation="",
    rollback_certified=False,
    operation_id="",
    selected_move_hash="",
    source_bundle_hash="",
    snapshot_bundle_hash="",
    max_users=0,
    now=None,
):
    state = autonomous_execution_control_state(path, now=now)
    blockers = list(state.get("blockers") or [])
    action_class = str(action_class or "").upper()
    mutation_kind = str(mutation_kind or "").lower()
    if action_class not in AUTONOMOUS_EXECUTION_ACTION_CLASSES:
        blockers.append("execution_control_action_class_unknown")
    if mutation_kind not in {"forward", "rollback"}:
        blockers.append("execution_control_mutation_kind_unknown")
    if expected_generation and expected_generation != state.get("generation"):
        blockers.append("execution_control_generation_mismatch")
    if mutation_kind == "forward" and state.get("scope") == "operation":
        bindings = {
            "operation_id": str(operation_id or ""),
            "selected_move_hash": str(selected_move_hash or ""),
            "action_class": action_class,
            "source_bundle_hash": str(source_bundle_hash or ""),
            "snapshot_bundle_hash": str(snapshot_bundle_hash or ""),
            "max_users": as_int(max_users, 0),
        }
        for field, value in bindings.items():
            if value in {"", 0}:
                blockers.append(f"execution_control_{field}_missing")
            elif value != state.get(field):
                blockers.append(f"execution_control_{field}_mismatch")
    if mutation_kind == "rollback" and (not rollback_certified or not str(operation_id or "")):
        blockers.append("execution_control_rollback_uncertified")
    if mutation_kind == "forward" and state.get("state") != "CLOSED":
        blockers.append("execution_control_forward_suspended")
    allowed_forward = not blockers and mutation_kind == "forward" and state.get("state") == "CLOSED"
    allowed_rollback = not blockers and mutation_kind == "rollback" and bool(rollback_certified)
    return {
        "schema_version": "v7.autonomous-execution-control-decision.v1",
        "allowed": bool(allowed_forward or allowed_rollback),
        "allowed_forward_mutation": bool(allowed_forward),
        "rollback_only_allowed": bool(allowed_rollback),
        "mutation_kind": mutation_kind,
        "action_class": action_class,
        "operation_id": str(operation_id or ""),
        "selected_move_hash": str(selected_move_hash or ""),
        "source_bundle_hash": str(source_bundle_hash or ""),
        "snapshot_bundle_hash": str(snapshot_bundle_hash or ""),
        "max_users": as_int(max_users, 0),
        "state": state.get("state", "UNKNOWN"),
        "scope": state.get("scope", ""),
        "generation": state.get("generation", ""),
        "updated_at": state.get("updated_at", ""),
        "valid_until": state.get("valid_until", ""),
        "updated_by": state.get("updated_by", ""),
        "reason": state.get("reason", ""),
        "blockers": sorted(set(blockers)),
        "authority_granted": False,
        "authority_expanded": False,
        "planner_changed": False,
    }


def finalize_autonomous_execution_control_window(
    path=DEFAULT_AUTONOMOUS_EXECUTION_CONTROL_FILE,
    *,
    expected_generation="",
    operation_id="",
    actor="governed-execution-finalizer",
    reason="controlled_window_terminal_open",
    now=None,
    force_fail_closed_open=False,
):
    """Idempotently return an owned controlled window to fail-closed OPEN."""
    now = now or utc_now()
    before = autonomous_execution_control_state(path, now=now)
    if before.get("valid") and before.get("state") == "OPEN":
        return {"ok": True, "idempotent": True, "before": before, "after": before, "final_open": True}
    blockers = []
    if not force_fail_closed_open:
        if str(expected_generation or "") != str(before.get("generation") or ""):
            blockers.append("execution_control_finalization_generation_mismatch")
        if str(operation_id or "") != str(before.get("operation_id") or ""):
            blockers.append("execution_control_finalization_operation_mismatch")
        if before.get("state") != "CLOSED":
            blockers.append("execution_control_finalization_state_not_closed")
    if blockers:
        return {"ok": False, "idempotent": False, "before": before, "after": before, "final_open": False, "blockers": blockers}
    opened = build_autonomous_execution_control_state(True, actor=actor, reason=reason, now=now)
    write_json_atomic(path, opened)
    after = autonomous_execution_control_state(path, now=now)
    return {
        "ok": bool(after.get("valid") and after.get("state") == "OPEN"),
        "idempotent": False,
        "forced_fail_closed_recovery": bool(force_fail_closed_open),
        "before": before,
        "after": after,
        "final_open": bool(after.get("valid") and after.get("state") == "OPEN"),
        "blockers": list(after.get("blockers") or []),
    }


def resolve_under_repo(path, repo_root):
    repo_root = Path(repo_root).resolve()
    resolved = Path(path).expanduser()
    if not resolved.is_absolute():
        resolved = repo_root / resolved
    resolved = resolved.resolve()
    try:
        resolved.relative_to(repo_root)
    except ValueError as exc:
        raise PacketError("path_outside_repo") from exc
    return resolved


def as_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def is_zero_packet(packet):
    return packet.get("selected_first_action") == ZERO_ACTION


def is_nonzero_clearance_packet(packet):
    return packet.get("selected_first_action") == NONZERO_ACTION


def engineering_authority_request_hash(request):
    canonical = copy.deepcopy(request if isinstance(request, dict) else {})
    canonical.pop("request_id", None)
    canonical.pop("contract_hash", None)
    return sha256_json(canonical)


def engineering_authority_repair_continuation_policy_hash(policy):
    canonical = copy.deepcopy(policy if isinstance(policy, dict) else {})
    canonical.pop("policy_id", None)
    canonical.pop("policy_hash", None)
    return sha256_json(canonical)


def current_action_class_contract_request_hash(request):
    canonical = copy.deepcopy(request if isinstance(request, dict) else {})
    canonical.pop("request_id", None)
    canonical.pop("request_hash", None)
    return sha256_json(canonical)


def current_action_class_contract_hash(contract):
    canonical = copy.deepcopy(contract if isinstance(contract, dict) else {})
    canonical.pop("contract_id", None)
    canonical.pop("contract_hash", None)
    canonical.pop("one_use_consumption", None)
    return sha256_json(canonical)


def routing_core_primary_promotion_hash(contract):
    canonical = copy.deepcopy(contract if isinstance(contract, dict) else {})
    canonical.pop("contract_id", None)
    canonical.pop("contract_hash", None)
    return sha256_json(canonical)


def build_routing_core_primary_promotion_request(
    *, runtime_fingerprint_path="/opt/v7/runtime-fingerprint.json",
    routing_sync_path="/usr/local/bin/v7-routing-sync",
    routing_core_path="/usr/local/bin/admin_core/routing_core.py", now=None,
):
    """Build a fresh M8 decision request; never writes policy or Runtime."""
    now = now or utc_now()
    runtime = read_json(Path(runtime_fingerprint_path))
    request = {
        "schema_version": "v7.routing-core-primary-promotion-request.v1",
        "status": "AWAITING_INDEPENDENT_AUTHORITY_DECISION",
        "created_at": now.isoformat(),
        "expires_at": (now + timedelta(minutes=15)).isoformat(),
        "active_program": "V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1",
        "scope": "ALL_COMPATIBLE_PRODUCTION_USERS",
        "decision_set": ["APPROVE_CORE_PRIMARY_WITH_FALLBACK", "DECLINE"],
        "runtime_generation": {
            "commit": str(runtime.get("commit") or ""),
            "deploy_id": str(runtime.get("deploy_id") or ""),
            "routing_sync_sha256": sha256_file(Path(routing_sync_path)),
            "routing_core_sha256": sha256_file(Path(routing_core_path)),
        },
        "required_gates": {
            "reset_m6_production_correctness_latency_bounded_complexity": True,
            "reset_m7_10k_50_egress_constant_time_warm_path": True,
            "single_writer_fencing": True,
            "crash_restart_rebuild": True,
            "duplicate_effect_suppression": True,
            "blast_radius_and_capacity": True,
            "kernel_and_payload_verification": True,
            "observability": True,
            "legacy_fallback_required": True,
            "per_user_legacy_rules_retained_until_m9": True,
        },
        "authority_effect": "CORE_PRIMARY_PROMOTION_ONLY",
        "self_expansion_allowed": False,
    }
    request["request_hash"] = sha256_json(request)
    request["request_id"] = "rcppreq_" + request["request_hash"][:24]
    return request


def issue_routing_core_primary_promotion_to_policy(
    policy_path, request_path, *, decision, actor_id, audit_store=None, now=None,
):
    """Issue exact Core-primary policy through the existing Authority owner."""
    now = now or utc_now()
    if decision != "APPROVE_CORE_PRIMARY_WITH_FALLBACK":
        raise PacketError("routing_core_primary_promotion_decision_not_exact")
    if not str(actor_id or ""):
        raise PacketError("routing_core_primary_promotion_actor_missing")
    request = read_json(Path(request_path))
    request_copy = copy.deepcopy(request)
    request_id = str(request_copy.pop("request_id", "") or "")
    request_hash = str(request_copy.pop("request_hash", "") or "")
    if request.get("schema_version") != "v7.routing-core-primary-promotion-request.v1" or not request_id or sha256_json(request_copy) != request_hash:
        raise PacketError("routing_core_primary_promotion_request_invalid")
    if parse_ts(request.get("expires_at")) <= now:
        raise PacketError("routing_core_primary_promotion_request_expired")
    generation = request.get("runtime_generation") if isinstance(request.get("runtime_generation"), dict) else {}
    gates = request.get("required_gates") if isinstance(request.get("required_gates"), dict) else {}
    if not all(str(generation.get(key) or "") for key in ("commit", "deploy_id", "routing_sync_sha256", "routing_core_sha256")):
        raise PacketError("routing_core_primary_promotion_runtime_generation_missing")
    if not gates or not all(value is True for value in gates.values()):
        raise PacketError("routing_core_primary_promotion_gate_incomplete")
    contract = {
        "schema_version": "v7.routing-core-primary-promotion.v1",
        "state": "APPROVED",
        "issued_at": now.isoformat(),
        "active_program": request["active_program"],
        "scope": request["scope"],
        "legacy_fallback_required": True,
        "runtime_generation": copy.deepcopy(generation),
        "required_gates": copy.deepcopy(gates),
        "authority_decision": {"decision": decision, "actor_id": str(actor_id), "request_id": request_id, "request_hash": request_hash, "decided_at": now.isoformat()},
        "self_expansion_allowed": False,
    }
    contract["contract_hash"] = routing_core_primary_promotion_hash(contract)
    contract["contract_id"] = "rcpp_" + contract["contract_hash"][:24]
    policy_path = Path(policy_path)
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    with current_action_class_contract_policy_lock(policy_path):
        policy = read_json(policy_path)
        if isinstance(policy.get("routing_core_primary_promotion"), dict) and policy["routing_core_primary_promotion"].get("state") == "APPROVED":
            raise PacketError("routing_core_primary_promotion_already_approved")
        policy["routing_core_primary_promotion"] = contract
        write_json_atomic(policy_path, policy)
        append_record(audit_store, {"schema_version": CURRENT_ACTION_CLASS_AUDIT_SCHEMA, "record_type": "routing_core_primary_promotion_issued", "contract_id": contract["contract_id"], "contract_hash": contract["contract_hash"], "request_id": request_id, "request_hash": request_hash, "actor_provenance": {"actor_id": str(actor_id), "issuing_owner": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER}, "created_at": now.isoformat()})
    return {"status": "ROUTING_CORE_PRIMARY_PROMOTION_ISSUED", "contract": contract, "policy_write": True, "runtime_apply": False, "routing_mutation": False, "users_moved": 0}


def standing_delegated_policy_request_hash(request):
    canonical = copy.deepcopy(request if isinstance(request, dict) else {})
    canonical.pop("request_id", None)
    canonical.pop("request_hash", None)
    return sha256_json(canonical)


def standing_delegated_policy_contract_hash(contract):
    canonical = copy.deepcopy(contract if isinstance(contract, dict) else {})
    canonical.pop("contract_id", None)
    canonical.pop("contract_hash", None)
    return sha256_json(canonical)


SERVICE_FAILURE_DELEGATED_ACTION_CLASSES = {
    1: "single-user governed candidate failover",
    2: "channel hard-fail failover",
    4: "channel hard-fail failover",
    5: "channel hard-fail failover",
    10: "channel hard-fail failover",
    25: "channel hard-fail failover",
    48: "channel hard-fail failover",
}
CONTROLLED_TOPOLOGY_DELEGATED_ACTION_CLASS = (
    "bounded autonomous controlled certification topology"
)
CONTROLLED_TOPOLOGY_STANDING_POLICY_PROFILE = (
    "SERVICE_FAILURE_WITH_CONTROLLED_CERTIFICATION_TOPOLOGY_V1"
)
AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS = (
    "bounded availability-first controlled failover"
)
AVAILABILITY_FIRST_STANDING_POLICY_PROFILE = (
    "SERVICE_FAILURE_WITH_CONTROLLED_CERTIFICATION_AVAILABILITY_FIRST_V2"
)
AVAILABILITY_FIRST_ALLOWED_ACTIONS = (
    "ASSIGN_CERTIFICATION_COHORT_TO_SHARED_TARGET",
    "ASSIGN_CERTIFICATION_COHORT_TO_SHARED_TARGET_SET",
    "RESERVE_SHARED_TARGET_SPARE_CAPACITY",
    "RELEASE_SHARED_TARGET_SPARE_CAPACITY",
    "REDISTRIBUTE_CERTIFICATION_SUBSET",
    "ROLLBACK_CERTIFICATION_SUBSET",
    "RESTORE_CONTROLLED_CERTIFICATION_BASELINE",
    "CONTINUE_PROGRESSIVE_CERTIFICATION_STAGE",
)
AVAILABILITY_FIRST_LADDER = (1, 2, 5, 10, 25, 48)
GENERIC_MOVEMENT_ENGINEERING_CERTIFIED_MAX_USERS = 48
SERVICE_FAILURE_ADAPTER_ENGINEERING_MAX_USERS = 48
SERVICE_FAILURE_ORDINARY_PRODUCTION_PROVEN_MAX_USERS = 4
SERVICE_FAILURE_CONTROLLED_PRODUCTION_PROVEN_MAX_USERS = 0


def standing_delegated_policy_runtime_axes(
    contract,
    *,
    ordinary_production_proven_max=SERVICE_FAILURE_ORDINARY_PRODUCTION_PROVEN_MAX_USERS,
    controlled_production_proven_max=SERVICE_FAILURE_CONTROLLED_PRODUCTION_PROVEN_MAX_USERS,
):
    """Project the independently different Authority/evidence/Runtime axes.

    A standing Authority ceiling is not itself production proof.  The current
    Tier-48 contract predates an explicit execution-context field, so its
    approved maximum remains intact while Runtime fails safely to the
    owner-backed ordinary-production proof floor.  The larger ceiling is
    available only when the executor independently proves the exact controlled
    certification context for every member.

    This is a read model over the existing Authority and certification owners;
    it neither rewrites the contract nor creates a second policy owner.
    """
    contract = contract if isinstance(contract, dict) else {}
    policy = contract.get("policy") if isinstance(contract.get("policy"), dict) else {}
    authority_approved = max(0, as_int(policy.get("max_users_per_action"), 0))
    ordinary_proven = max(0, as_int(ordinary_production_proven_max, 0))
    controlled_proven = max(0, as_int(controlled_production_proven_max, 0))
    controlled_runtime = authority_approved
    ordinary_runtime = min(authority_approved, ordinary_proven)
    return {
        "schema_version": "v7.service-failure-runtime-scope-axes.v1",
        "authority_approved_max": authority_approved,
        "controlled_certification_runtime_max": controlled_runtime,
        "ordinary_production_runtime_max": ordinary_runtime,
        "controlled_production_proven_max": controlled_proven,
        "ordinary_production_proven_max": ordinary_proven,
        "context_selection": "EXACT_EXECUTOR_PROOF_REQUIRED",
        "legacy_contract_context": (
            "UNSCOPED_CONTEXT_RECONCILED_BY_EXISTING_RUNTIME_GATE"
            if authority_approved
            else "NO_ACTIVE_AUTHORITY"
        ),
        "ordinary_runtime_narrowing_reason": (
            "controlled_service_failure_outcomes_5_10_25_48_not_yet_consumed"
            if authority_approved > ordinary_runtime
            else "NONE"
        ),
        "contract_rewritten": False,
        "authority_expanded": False,
        "owner": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
        "evidence_owner": "existing Controlled Production Certification Program",
    }


def controlled_certification_campaign_stage_status(
    audit_records,
    *,
    request_id="",
    request_hash="",
    now=None,
):
    """Project consumed campaign stages from the existing Authority audit owner.

    This is a compact read model, not a second campaign registry.  Only an
    exact approved request and complete Outcome/Replay/Learning receipts count.
    Duplicate, out-of-order or malformed receipts fail closed.
    """
    records = list(audit_records or [])
    authority = controlled_certification_substrate_authority_status(
        records,
        now=now,
    )
    active_request_id = str(authority.get("request_id") or "")
    active_request_hash = str(authority.get("request_hash") or "")
    expected_request_id = str(request_id or active_request_id)
    expected_request_hash = str(request_hash or active_request_hash)
    blockers = []
    if authority.get("status") != "APPROVED":
        blockers.append("controlled_campaign_authority_not_approved")
    if (
        str(authority.get("decision") or "")
        != CONTROLLED_CERTIFICATION_SUBSTRATE_APPROVAL
    ):
        blockers.append("controlled_campaign_authority_decision_not_exact")
    if expected_request_id != active_request_id:
        blockers.append("controlled_campaign_request_id_not_current")
    if expected_request_hash != active_request_hash:
        blockers.append("controlled_campaign_request_hash_not_current")

    request = (
        authority.get("request")
        if isinstance(authority.get("request"), dict)
        else {}
    )
    scope = request.get("scope") if isinstance(request.get("scope"), dict) else {}
    stages = tuple(as_int(item, 0) for item in (scope.get("campaign_stages") or []))
    if stages != CONTROLLED_CERTIFICATION_CAMPAIGN_STAGES:
        blockers.append("controlled_campaign_stage_contract_changed")
        stages = CONTROLLED_CERTIFICATION_CAMPAIGN_STAGES

    stage_rows = [
        row
        for row in records
        if row.get("record_type")
        == CONTROLLED_CERTIFICATION_CAMPAIGN_EFFECT_RECORD_TYPE
        and row.get("effect_class")
        == CONTROLLED_CERTIFICATION_CAMPAIGN_STAGE_EFFECT_CLASS
        and str(row.get("authority_request_id") or "") == expected_request_id
    ]
    receipts_by_stage = {}
    for row in stage_rows:
        stage = as_int(row.get("campaign_stage"), 0)
        receipts_by_stage.setdefault(stage, []).append(row)
        if stage not in stages:
            blockers.append(f"controlled_campaign_stage_not_admitted:{stage}")
        if str(row.get("authority_request_hash") or "") != expected_request_hash:
            blockers.append(f"controlled_campaign_stage_hash_mismatch:{stage}")
        if not all(
            row.get(key) is True
            for key in (
                "outcome_consumed",
                "replay_consumed",
                "learning_consumed",
                "baseline_reset_verified",
            )
        ):
            blockers.append(f"controlled_campaign_stage_incomplete:{stage}")
        if as_int(row.get("ordinary_customer_count"), -1) != 0:
            blockers.append(f"controlled_campaign_ordinary_customer_effect:{stage}")
    for stage, rows in receipts_by_stage.items():
        if len(rows) != 1:
            blockers.append(f"controlled_campaign_stage_duplicate:{stage}")

    completed_stages = [
        stage
        for stage in stages
        if len(receipts_by_stage.get(stage, [])) == 1
        and not any(
            item.endswith(f":{stage}")
            for item in blockers
        )
    ]
    prefix = []
    for stage in stages:
        if stage not in completed_stages:
            break
        prefix.append(stage)
    if completed_stages != prefix:
        blockers.append("controlled_campaign_stage_order_gap")
    valid_completed = prefix if not blockers else []
    next_stage = next(
        (stage for stage in stages if stage not in valid_completed),
        0,
    )
    return {
        "schema_version": "v7.controlled-certification-campaign-stage-status.v1",
        "status": "PASS" if not blockers else "STOP_SAFE",
        "ok": not blockers,
        "request_id": expected_request_id,
        "request_hash": expected_request_hash,
        "stages": list(stages),
        "completed_stages": valid_completed,
        "controlled_production_proven_max": (
            valid_completed[-1] if valid_completed else 0
        ),
        "next_stage": next_stage,
        "completed": not blockers and next_stage == 0,
        "receipt_ids": [
            str(receipts_by_stage[stage][0].get("receipt_id") or "")
            for stage in valid_completed
        ],
        "blockers": sorted(set(blockers)),
        "owner": (
            "existing admin_core/operator_execution.py append-only "
            "Authority audit owner"
        ),
    }


def availability_first_campaign_stage_status(
    audit_records,
    *,
    contract=None,
    now=None,
):
    """Project the 1/2/5/10/25/48 ladder from the existing audit owner.

    This is a read model over the active standing contract and its append-only
    effect receipts.  It is deliberately not a campaign registry.  A receipt
    counts only when the exact allocation, production Outcome, deterministic
    Replay, Learning, ordinary-user protection, and baseline reset were all
    consumed for one stage.
    """
    records = list(audit_records or [])
    contract = contract if isinstance(contract, dict) else {}
    validation = validate_standing_delegated_operational_policy(
        contract,
        audit_records=records,
        now=now,
    )
    policy = (
        validation.get("policy")
        if isinstance(validation.get("policy"), dict)
        else {}
    )
    blockers = list(validation.get("errors") or [])
    if (
        policy.get("policy_profile")
        != AVAILABILITY_FIRST_STANDING_POLICY_PROFILE
    ):
        blockers.append("availability_first_policy_profile_not_active")
    if (
        AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS
        not in set(policy.get("allowed_action_classes") or [])
    ):
        blockers.append("availability_first_action_class_not_active")
    contract_id = str(contract.get("contract_id") or "")
    contract_hash = str(contract.get("contract_hash") or "")
    stage_rows = [
        row
        for row in records
        if row.get("record_type")
        == CONTROLLED_CERTIFICATION_CAMPAIGN_EFFECT_RECORD_TYPE
        and row.get("effect_class")
        == AVAILABILITY_FIRST_CAMPAIGN_STAGE_EFFECT_CLASS
        and str(row.get("standing_policy_contract_id") or "")
        == contract_id
    ]
    target_bound_rows = [
        row
        for row in records
        if row.get("record_type")
        == CONTROLLED_CERTIFICATION_CAMPAIGN_EFFECT_RECORD_TYPE
        and row.get("effect_class")
        == AVAILABILITY_FIRST_TARGET_BOUND_EFFECT_CLASS
        and str(row.get("standing_policy_contract_id") or "")
        == contract_id
    ]
    receipts_by_stage = {}
    target_proven_bounds = {}
    for row in stage_rows:
        stage = as_int(row.get("campaign_stage"), 0)
        receipts_by_stage.setdefault(stage, []).append(row)
        if stage not in AVAILABILITY_FIRST_LADDER:
            blockers.append(f"availability_first_stage_not_admitted:{stage}")
        if (
            str(row.get("standing_policy_contract_hash") or "")
            != contract_hash
        ):
            blockers.append(
                f"availability_first_stage_contract_hash_mismatch:{stage}"
            )
        if not all(
            row.get(key) is True
            for key in (
                "allocation_immutable",
                "capacity_reservation_verified",
                "outcome_consumed",
                "replay_consumed",
                "learning_consumed",
                "per_user_verification_passed",
                "per_target_verification_passed",
                "aggregate_verification_passed",
                "ordinary_user_protection_passed",
                "baseline_reset_verified",
            )
        ):
            blockers.append(f"availability_first_stage_incomplete:{stage}")
        if as_int(row.get("ordinary_customer_count"), -1) != 0:
            blockers.append(
                f"availability_first_stage_ordinary_customer_effect:{stage}"
            )
        target_receipts = [
            item
            for item in (row.get("target_receipts") or [])
            if isinstance(item, dict)
        ]
        if (
            not target_receipts
            or sum(
                as_int(item.get("verified_scope"), 0)
                for item in target_receipts
            )
            != stage
        ):
            blockers.append(
                f"availability_first_stage_target_receipts_invalid:{stage}"
            )
        for item in target_receipts:
            target_id = str(item.get("target_id") or "")
            verified_scope = as_int(item.get("verified_scope"), 0)
            if (
                not target_id
                or verified_scope <= 0
                or not str(item.get("target_fingerprint") or "")
                or not str(
                    item.get("capacity_bounds_fingerprint") or ""
                )
            ):
                blockers.append(
                    f"availability_first_stage_target_receipt_incomplete:{stage}"
                )
                continue
            target_proven_bounds[target_id] = max(
                as_int(target_proven_bounds.get(target_id), 0),
                verified_scope,
            )
    target_bound_receipts = {}
    for row in target_bound_rows:
        target_id = str(row.get("target_id") or "")
        verified_scope = as_int(row.get("verified_scope"), 0)
        identity = (target_id, verified_scope)
        target_bound_receipts.setdefault(identity, []).append(row)
        if (
            str(row.get("standing_policy_contract_hash") or "")
            != contract_hash
        ):
            blockers.append(
                "availability_first_target_bound_contract_hash_mismatch:"
                f"{target_id}:{verified_scope}"
            )
        if (
            not target_id
            or verified_scope not in AVAILABILITY_FIRST_LADDER
            or not str(row.get("target_fingerprint") or "")
            or not str(row.get("capacity_bounds_fingerprint") or "")
        ):
            blockers.append(
                "availability_first_target_bound_identity_invalid:"
                f"{target_id}:{verified_scope}"
            )
        if not all(
            row.get(key) is True
            for key in (
                "allocation_immutable",
                "capacity_reservation_verified",
                "outcome_consumed",
                "replay_consumed",
                "learning_consumed",
                "per_user_verification_passed",
                "per_target_verification_passed",
                "aggregate_verification_passed",
                "ordinary_user_protection_passed",
                "baseline_reset_verified",
            )
        ):
            blockers.append(
                "availability_first_target_bound_incomplete:"
                f"{target_id}:{verified_scope}"
            )
        if as_int(row.get("ordinary_customer_count"), -1) != 0:
            blockers.append(
                "availability_first_target_bound_ordinary_customer_effect:"
                f"{target_id}:{verified_scope}"
            )
        target_proven_bounds[target_id] = max(
            as_int(target_proven_bounds.get(target_id), 0),
            verified_scope,
        )
    for (target_id, verified_scope), rows in target_bound_receipts.items():
        if len(rows) != 1:
            blockers.append(
                "availability_first_target_bound_duplicate:"
                f"{target_id}:{verified_scope}"
            )
    for stage, rows in receipts_by_stage.items():
        if len(rows) != 1:
            blockers.append(f"availability_first_stage_duplicate:{stage}")
    completed = [
        stage
        for stage in AVAILABILITY_FIRST_LADDER
        if len(receipts_by_stage.get(stage, [])) == 1
        and not any(item.endswith(f":{stage}") for item in blockers)
    ]
    prefix = []
    for stage in AVAILABILITY_FIRST_LADDER:
        if stage not in completed:
            break
        prefix.append(stage)
    if completed != prefix:
        blockers.append("availability_first_stage_order_gap")
    valid_completed = prefix if not blockers else []
    next_stage = next(
        (
            stage
            for stage in AVAILABILITY_FIRST_LADDER
            if stage not in valid_completed
        ),
        0,
    )
    return {
        "schema_version": "v7.availability-first-campaign-stage-status.v1",
        "status": "PASS" if not blockers else "STOP_SAFE",
        "ok": not blockers,
        "standing_policy_contract_id": contract_id,
        "standing_policy_contract_hash": contract_hash,
        "stages": list(AVAILABILITY_FIRST_LADDER),
        "completed_stages": valid_completed,
        "production_proven_max": (
            valid_completed[-1] if valid_completed else 0
        ),
        "next_stage": next_stage,
        "completed": not blockers and next_stage == 0,
        "receipt_ids": [
            str(receipts_by_stage[stage][0].get("receipt_id") or "")
            for stage in valid_completed
        ],
        "target_proven_bounds": target_proven_bounds,
        "target_bound_receipt_ids": [
            str(rows[0].get("receipt_id") or "")
            for _, rows in sorted(target_bound_receipts.items())
            if len(rows) == 1
        ],
        "blockers": sorted(set(blockers)),
        "owner": (
            "existing admin_core/operator_execution.py append-only "
            "Authority audit owner"
        ),
    }


def controlled_certification_substrate_request_hash(request):
    canonical = copy.deepcopy(request if isinstance(request, dict) else {})
    canonical.pop("request_id", None)
    canonical.pop("request_hash", None)
    return sha256_json(canonical)


def controlled_certification_substrate_semantic_fingerprint(request):
    """Return one stable semantic identity across expiry-only replacements."""
    canonical = copy.deepcopy(request if isinstance(request, dict) else {})
    for key in (
        "request_id",
        "request_hash",
        "created_at",
        "expires_at",
        "semantic_request_fingerprint",
        "supersession",
    ):
        canonical.pop(key, None)
    return sha256_json(canonical)


def ct_m0f_controlled_validation_request_hash(request):
    canonical = copy.deepcopy(request if isinstance(request, dict) else {})
    canonical.pop("request_id", None)
    canonical.pop("request_hash", None)
    return sha256_json(canonical)


def ct_m0f_controlled_validation_semantic_fingerprint(request):
    """Stable one-generation scope identity excluding request lifetime."""
    canonical = copy.deepcopy(request if isinstance(request, dict) else {})
    for key in ("request_id", "request_hash", "created_at", "expires_at"):
        canonical.pop(key, None)
    return sha256_json(canonical)


def build_ct_m0f_controlled_validation_authority_request(
    *,
    active_program,
    source_id,
    current_pool_status,
    current_policy_contract_id,
    current_policy_contract_hash,
    sample_kind="cold",
    now=None,
):
    """Build one independently decidable CT-M0F validation generation.

    This is an extension of the existing operator-execution Authority owner,
    not a campaign or standing-policy request.  It grants no action by itself
    and intentionally binds the target to the existing planner's fresh safe
    selection because Candidate/Packet materialization occurs only after the
    independent decision.
    """
    now = now or utc_now()
    pool = current_pool_status if isinstance(current_pool_status, dict) else {}
    registry_hashes = (
        pool.get("registry_hashes")
        if isinstance(pool.get("registry_hashes"), dict)
        else {}
    )
    sample_kind = str(sample_kind or "cold").lower()
    generation_seed = {
        "active_program": str(active_program or ""),
        "source_id": str(source_id or ""),
        "sample_kind": sample_kind,
        "pool_fingerprint": str(pool.get("fingerprint") or ""),
        "policy_contract_id": str(current_policy_contract_id or ""),
        "policy_contract_hash": str(current_policy_contract_hash or ""),
        "created_at": now.isoformat(),
    }
    request = {
        "schema_version": CT_M0F_CONTROLLED_VALIDATION_REQUEST_SCHEMA,
        "status": "AWAITING_INDEPENDENT_ENGINEERING_AUTHORITY_DECISION",
        "created_at": now.isoformat(),
        "expires_at": (
            now + timedelta(seconds=CT_M0F_CONTROLLED_VALIDATION_REQUEST_TTL_SECONDS)
        ).isoformat(),
        "decision_set": [CT_M0F_CONTROLLED_VALIDATION_APPROVAL, "DECLINE"],
        "issuing_owner_required": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
        "active_program": str(active_program or ""),
        "mission": "V7_CONSTANT_TIME_COHORT_FAILOVER_REUSABLE_FAST_PRIMITIVES_CLOSURE_V1",
        "validation_generation_id": "ctm0fgen_" + sha256_json(generation_seed)[:24],
        "scope": {
            "profile": "CT_M0F_ONE_GENERATION_KERNEL_CUTOVER_VALIDATION",
            "sample_kind": sample_kind,
            "certification_only": True,
            "ordinary_customer_involvement": False,
            "source_id": str(source_id or ""),
            "target_selection": "FRESH_EXISTING_PLANNER_SAFE_TARGET",
            "max_users": 1,
            "max_concurrent_transactions": 1,
            "generation_use_limit": 1,
            "candidate_packet_lease_before_decision": False,
            "fresh_candidate_packet_lease_required_after_decision": True,
            "automatic_campaign_progression": False,
            "self_expansion_allowed": False,
        },
        "current_owner_backed_state": {
            "total_enabled_certification_users": int(
                pool.get("total_enabled_certification_users") or 0
            ),
            "max_enabled_certification_users_on_source": int(
                pool.get("max_enabled_certification_users_on_one_active_source") or 0
            ),
            "pool_fingerprint": str(pool.get("fingerprint") or ""),
            "users_registry_hash": str(registry_hashes.get("users_registry") or ""),
            "egress_registry_hash": str(registry_hashes.get("egress_registry") or ""),
            "active_policy_contract_id": str(current_policy_contract_id or ""),
            "active_policy_contract_hash": str(current_policy_contract_hash or ""),
        },
        "verification_and_containment": {
            "exact_policy_rule_table_route_required": True,
            "target_egress_fresh_payload_required": True,
            "rollback_or_certified_no_rollback_required": True,
            "reset_and_deferred_closure_required": True,
            "final_safe_mode": "OPEN",
            "remote_client_recovery_claimed": False,
        },
        "one_use_law": {
            "approval_use_limit": 1,
            "implicit_renewal": False,
            "retry_under_same_approval": False,
            "candidate_packet_lease_reuse": False,
        },
        "forbidden_effects": [
            "ordinary_customer_use",
            "authority_self_expansion",
            "production_maturity_change",
            "natural_l8_claim",
            "remote_client_recovery_claim",
            "campaign_stage_credit",
            "more_than_one_user",
            "more_than_one_concurrent_transaction",
        ],
        "next_required_consumer": "existing independent Authority owner",
        "reentry_condition": (
            "exact decision for this request id/hash; on approval the existing "
            "Matrix/governed consumer must revalidate pool, policy, source, target, "
            "capacity and create fresh Candidate/Packet/lease"
        ),
    }
    request_hash = ct_m0f_controlled_validation_request_hash(request)
    request["request_hash"] = request_hash
    request["request_id"] = f"ctm0fauth_r1_{request_hash[:24]}"
    return request


def validate_ct_m0f_controlled_validation_authority_request(
    request,
    *,
    decision="DECLINE",
    expected_request_id="",
    expected_request_hash="",
    now=None,
):
    now = now or utc_now()
    request = request if isinstance(request, dict) else {}
    errors = []
    request_id = str(request.get("request_id") or "")
    request_hash = str(request.get("request_hash") or "")
    if request.get("schema_version") != CT_M0F_CONTROLLED_VALIDATION_REQUEST_SCHEMA:
        errors.append("ct_m0f_validation_request_schema_invalid")
    if ct_m0f_controlled_validation_request_hash(request) != request_hash:
        errors.append("ct_m0f_validation_request_hash_mismatch")
    if request_id != f"ctm0fauth_r1_{request_hash[:24]}":
        errors.append("ct_m0f_validation_request_identity_mismatch")
    if expected_request_id and request_id != str(expected_request_id):
        errors.append("ct_m0f_validation_expected_request_mismatch")
    if expected_request_hash and request_hash != str(expected_request_hash):
        errors.append("ct_m0f_validation_expected_hash_mismatch")
    if request.get("status") != "AWAITING_INDEPENDENT_ENGINEERING_AUTHORITY_DECISION":
        errors.append("ct_m0f_validation_request_not_pending")
    if decision not in set(request.get("decision_set") or []):
        errors.append("ct_m0f_validation_decision_not_allowed")
    try:
        if parse_ts(request.get("expires_at")) <= now:
            errors.append("ct_m0f_validation_request_expired")
        if parse_ts(request.get("created_at")) > now:
            errors.append("ct_m0f_validation_created_at_invalid")
    except PacketError:
        errors.append("ct_m0f_validation_timestamps_invalid")
    if request.get("issuing_owner_required") != CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER:
        errors.append("ct_m0f_validation_owner_invalid")
    if request.get("active_program") != "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1":
        errors.append("ct_m0f_validation_program_invalid")
    scope = request.get("scope") if isinstance(request.get("scope"), dict) else {}
    if scope.get("profile") != "CT_M0F_ONE_GENERATION_KERNEL_CUTOVER_VALIDATION":
        errors.append("ct_m0f_validation_profile_invalid")
    if str(scope.get("sample_kind") or "") not in {"cold", "warm"}:
        errors.append("ct_m0f_validation_sample_kind_invalid")
    if not str(scope.get("source_id") or ""):
        errors.append("ct_m0f_validation_source_missing")
    if int(scope.get("max_users") or 0) != 1 or int(scope.get("max_concurrent_transactions") or 0) != 1:
        errors.append("ct_m0f_validation_blast_radius_invalid")
    if int(scope.get("generation_use_limit") or 0) != 1:
        errors.append("ct_m0f_validation_use_limit_invalid")
    if scope.get("certification_only") is not True or scope.get("ordinary_customer_involvement") is not False:
        errors.append("ct_m0f_validation_identity_boundary_invalid")
    if scope.get("automatic_campaign_progression") is not False or scope.get("self_expansion_allowed") is not False:
        errors.append("ct_m0f_validation_expansion_boundary_invalid")
    state = request.get("current_owner_backed_state") if isinstance(request.get("current_owner_backed_state"), dict) else {}
    if int(state.get("max_enabled_certification_users_on_source") or 0) < 1:
        errors.append("ct_m0f_validation_certification_identity_missing")
    if not str(state.get("active_policy_contract_id") or "") or not str(state.get("active_policy_contract_hash") or ""):
        errors.append("ct_m0f_validation_policy_binding_missing")
    one_use = request.get("one_use_law") if isinstance(request.get("one_use_law"), dict) else {}
    if int(one_use.get("approval_use_limit") or 0) != 1 or one_use.get("implicit_renewal") is not False or one_use.get("retry_under_same_approval") is not False:
        errors.append("ct_m0f_validation_one_use_law_invalid")
    if not str(request.get("validation_generation_id") or ""):
        errors.append("ct_m0f_validation_generation_missing")
    return {
        "ok": not errors,
        "errors": sorted(set(errors)),
        "request_id": request_id,
        "request_hash": request_hash,
        "validation_generation_id": str(request.get("validation_generation_id") or ""),
        "decision": decision,
        "expires_at": str(request.get("expires_at") or ""),
    }


def register_ct_m0f_controlled_validation_authority_request(
    request,
    *,
    audit_store=None,
    producer_id="tools/v7-users-autoswitch",
    now=None,
):
    """Append one exact request through the existing Authority audit."""
    now = now or utc_now()
    validation = validate_ct_m0f_controlled_validation_authority_request(
        request, decision="DECLINE", now=now,
    )
    if not validation.get("ok"):
        raise PacketError(",".join(validation.get("errors") or ["ct_m0f_validation_request_invalid"]))
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    with current_action_class_contract_policy_lock(audit_store):
        records = read_live_execution_lineage_records(audit_store)
        existing = [
            row for row in records
            if row.get("record_type") == CT_M0F_CONTROLLED_VALIDATION_REQUEST_RECORD_TYPE
            and str(row.get("authority_request_id") or "") == request["request_id"]
        ]
        if existing:
            if len(existing) == 1 and existing[0].get("request") == request:
                return {
                    "status": "ALREADY_REGISTERED_EXACT",
                    "request_id": request["request_id"],
                    "request_hash": request["request_hash"],
                    "audit_write": False,
                }
            raise PacketError("ct_m0f_validation_request_audit_identity_conflict")
        decided = {
            str(row.get("authority_request_id") or "")
            for row in records
            if row.get("record_type") == CT_M0F_CONTROLLED_VALIDATION_DECISION_RECORD_TYPE
        }
        semantic = ct_m0f_controlled_validation_semantic_fingerprint(request)
        for row in records:
            if row.get("record_type") != CT_M0F_CONTROLLED_VALIDATION_REQUEST_RECORD_TYPE:
                continue
            prior = row.get("request") if isinstance(row.get("request"), dict) else {}
            prior_id = str(prior.get("request_id") or "")
            if not prior_id or prior_id in decided:
                continue
            try:
                active = parse_ts(prior.get("expires_at")) > now
            except PacketError:
                active = False
            if active and ct_m0f_controlled_validation_semantic_fingerprint(prior) == semantic:
                raise PacketError("ct_m0f_validation_active_semantic_request_exists")
        append_record(audit_store, {
            "schema_version": "v7.ct-m0f-controlled-validation-authority-audit.v1",
            "record_type": CT_M0F_CONTROLLED_VALIDATION_REQUEST_RECORD_TYPE,
            "authority_request_id": request["request_id"],
            "authority_request_hash": request["request_hash"],
            "request": copy.deepcopy(request),
            "producer": str(producer_id or "tools/v7-users-autoswitch"),
            "created_at": now.isoformat(),
        })
    return {
        "status": "REGISTERED",
        "request_id": request["request_id"],
        "request_hash": request["request_hash"],
        "audit_write": True,
    }


def ct_m0f_controlled_validation_request_from_audit(
    request_id,
    request_hash,
    *,
    audit_store=None,
    now=None,
):
    now = now or utc_now()
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    matches = [
        row for row in read_audit_records(audit_store)
        if row.get("record_type") == CT_M0F_CONTROLLED_VALIDATION_REQUEST_RECORD_TYPE
        and str(row.get("authority_request_id") or "") == str(request_id or "")
    ]
    if len(matches) != 1:
        raise PacketError("ct_m0f_validation_request_audit_missing_or_duplicate")
    if str(matches[0].get("authority_request_hash") or "") != str(request_hash or ""):
        raise PacketError("ct_m0f_validation_request_audit_hash_mismatch")
    request = matches[0].get("request") if isinstance(matches[0].get("request"), dict) else {}
    validation = validate_ct_m0f_controlled_validation_authority_request(
        request,
        decision="DECLINE",
        expected_request_id=request_id,
        expected_request_hash=request_hash,
        now=now,
    )
    if not validation.get("ok"):
        raise PacketError(",".join(validation.get("errors") or ["ct_m0f_validation_request_invalid"]))
    return request


def record_ct_m0f_controlled_validation_authority_decision(
    *,
    request_id,
    request_hash,
    decision,
    actor_id,
    audit_store=None,
    now=None,
):
    """Append one exact independent decision; never executes the generation."""
    now = now or utc_now()
    if decision not in {CT_M0F_CONTROLLED_VALIDATION_APPROVAL, "DECLINE"}:
        raise PacketError("ct_m0f_validation_decision_not_exact")
    if not str(actor_id or "").strip():
        raise PacketError("ct_m0f_validation_authority_actor_missing")
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    with current_action_class_contract_policy_lock(audit_store):
        records = read_audit_records(audit_store)
        existing = [
            row for row in records
            if row.get("record_type") == CT_M0F_CONTROLLED_VALIDATION_DECISION_RECORD_TYPE
            and str(row.get("authority_request_id") or "") == str(request_id or "")
        ]
        decision_id = stable_id("ctm0fdec", {
            "request_id": request_id,
            "request_hash": request_hash,
            "decision": decision,
            "actor_id": str(actor_id),
        })
        if existing:
            exact = [row for row in existing if row.get("decision_id") == decision_id]
            if len(existing) == 1 and len(exact) == 1:
                return {
                    "status": "ALREADY_RECORDED_EXACT",
                    "request_id": request_id,
                    "request_hash": request_hash,
                    "decision": decision,
                    "decision_id": decision_id,
                    "audit_write": False,
                    "runtime_apply": False,
                    "users_moved": 0,
                }
            raise PacketError("ct_m0f_validation_authority_decision_conflict")
        request = ct_m0f_controlled_validation_request_from_audit(
            request_id, request_hash, audit_store=audit_store, now=now,
        )
        validation = validate_ct_m0f_controlled_validation_authority_request(
            request,
            decision=decision,
            expected_request_id=request_id,
            expected_request_hash=request_hash,
            now=now,
        )
        if not validation.get("ok"):
            raise PacketError(",".join(validation.get("errors") or ["ct_m0f_validation_decision_invalid"]))
        append_record(audit_store, {
            "schema_version": "v7.ct-m0f-controlled-validation-authority-decision.v1",
            "record_type": CT_M0F_CONTROLLED_VALIDATION_DECISION_RECORD_TYPE,
            "decision_id": decision_id,
            "authority_request_id": request_id,
            "authority_request_hash": request_hash,
            "validation_generation_id": request["validation_generation_id"],
            "decision": decision,
            "actor_provenance": {
                "actor_id": str(actor_id),
                "issuing_owner": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
                "recorded_at": now.isoformat(),
            },
            "created_at": now.isoformat(),
        })
    return {
        "status": "APPROVED" if decision == CT_M0F_CONTROLLED_VALIDATION_APPROVAL else "DECLINED",
        "request_id": request_id,
        "request_hash": request_hash,
        "decision": decision,
        "decision_id": decision_id,
        "validation_generation_id": request["validation_generation_id"],
        "next_required_consumer": (
            "existing Matrix/governed CT-M0F validation consumer"
            if decision == CT_M0F_CONTROLLED_VALIDATION_APPROVAL
            else "existing CPS/OMP residual reconciliation owner"
        ),
        "audit_write": True,
        "policy_write": False,
        "candidate_created": False,
        "packet_created": False,
        "lease_created": False,
        "runtime_apply": False,
        "routing_mutation": False,
        "users_moved": 0,
        "authority_self_expansion": False,
        "production_maturity_change": False,
    }


def ct_m0f_controlled_validation_authority_binding_from_audit(
    request_id,
    request_hash,
    validation_generation_id,
    *,
    audit_store=None,
    now=None,
):
    """Read-only proof that one exact independent decision currently admits the generation."""
    now = now or utc_now()
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    request = ct_m0f_controlled_validation_request_from_audit(
        request_id, request_hash, audit_store=audit_store, now=now,
    )
    records = read_audit_records(audit_store)
    decisions = [
        row for row in records
        if row.get("record_type") == CT_M0F_CONTROLLED_VALIDATION_DECISION_RECORD_TYPE
        and str(row.get("authority_request_id") or "") == str(request_id or "")
        and str(row.get("authority_request_hash") or "") == str(request_hash or "")
    ]
    errors = []
    if len(decisions) != 1:
        errors.append("ct_m0f_validation_decision_missing_or_duplicate")
    else:
        decision = decisions[0]
        if decision.get("decision") != CT_M0F_CONTROLLED_VALIDATION_APPROVAL:
            errors.append("ct_m0f_validation_not_approved")
        if str(decision.get("validation_generation_id") or "") != str(validation_generation_id or ""):
            errors.append("ct_m0f_validation_decision_generation_mismatch")
    if str(request.get("validation_generation_id") or "") != str(validation_generation_id or ""):
        errors.append("ct_m0f_validation_request_generation_mismatch")
    consumed = [
        row for row in records
        if row.get("record_type") == CT_M0F_CONTROLLED_VALIDATION_CONSUMPTION_RECORD_TYPE
        and str(row.get("authority_request_id") or "") == str(request_id or "")
    ]
    if consumed:
        errors.append("ct_m0f_validation_admission_already_consumed")
    return {
        "ok": not errors,
        "status": "ADMITTED_READY_FOR_FRESH_ARTIFACTS" if not errors else "STOP_SAFE",
        "errors": sorted(set(errors)),
        "request": copy.deepcopy(request),
        "decision": copy.deepcopy(decisions[0]) if len(decisions) == 1 else {},
        "request_id": str(request_id or ""),
        "request_hash": str(request_hash or ""),
        "validation_generation_id": str(validation_generation_id or ""),
        "admission_consumed": bool(consumed),
    }


def consume_ct_m0f_controlled_validation_admission(
    *,
    request_id,
    request_hash,
    validation_generation_id,
    packet_id,
    operation_id,
    lease_id,
    user,
    source,
    target,
    audit_store=None,
    consumer_id="tools/v7-governed-canary-dry-run-cycle",
    now=None,
):
    """Atomically consume the exact one-use admission after fresh artifacts exist."""
    now = now or utc_now()
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    required = {
        "request_id": str(request_id or ""),
        "request_hash": str(request_hash or ""),
        "validation_generation_id": str(validation_generation_id or ""),
        "packet_id": str(packet_id or ""),
        "operation_id": str(operation_id or ""),
        "lease_id": str(lease_id or ""),
        "user": str(user or ""),
        "source": str(source or ""),
        "target": str(target or ""),
    }
    missing = [f"ct_m0f_validation_{key}_missing" for key, value in required.items() if not value]
    if missing:
        return {"ok": False, "status": "STOP_SAFE", "errors": missing, "audit_write": False}
    with current_action_class_contract_policy_lock(audit_store):
        binding = ct_m0f_controlled_validation_authority_binding_from_audit(
            request_id,
            request_hash,
            validation_generation_id,
            audit_store=audit_store,
            now=now,
        )
        errors = list(binding.get("errors") or [])
        request = binding.get("request") if isinstance(binding.get("request"), dict) else {}
        scope = request.get("scope") if isinstance(request.get("scope"), dict) else {}
        if str(scope.get("source_id") or "") != required["source"]:
            errors.append("ct_m0f_validation_source_mismatch")
        if int(scope.get("max_users") or 0) != 1 or int(scope.get("max_concurrent_transactions") or 0) != 1:
            errors.append("ct_m0f_validation_scope_changed")
        if errors:
            return {
                "ok": False,
                "status": "STOP_SAFE",
                "errors": sorted(set(errors)),
                "audit_write": False,
                "runtime_apply": False,
                "users_moved": 0,
            }
        record = append_record(audit_store, {
            "schema_version": "v7.ct-m0f-controlled-validation-admission-consumption.v1",
            "record_type": CT_M0F_CONTROLLED_VALIDATION_CONSUMPTION_RECORD_TYPE,
            "consumption_id": stable_id("ctm0fconsume", required),
            "authority_request_id": required["request_id"],
            "authority_request_hash": required["request_hash"],
            "validation_generation_id": required["validation_generation_id"],
            "packet_id": required["packet_id"],
            "operation_id": required["operation_id"],
            "lease_id": required["lease_id"],
            "user": required["user"],
            "source": required["source"],
            "target": required["target"],
            "consumer": str(consumer_id or "tools/v7-governed-canary-dry-run-cycle"),
            "consumed_at": now.isoformat(),
            "one_use_consumed": True,
        })
    return {
        "ok": True,
        "status": "CONSUMED_EXACT_ONCE",
        "consumption_id": record["consumption_id"],
        "request_id": required["request_id"],
        "request_hash": required["request_hash"],
        "validation_generation_id": required["validation_generation_id"],
        "packet_id": required["packet_id"],
        "operation_id": required["operation_id"],
        "lease_id": required["lease_id"],
        "audit_write": True,
        "policy_write": False,
        "runtime_apply": False,
        "routing_mutation": False,
        "users_moved": 0,
        "authority_expansion": False,
        "production_maturity_change": False,
    }


def validate_ct_m0f_controlled_validation_consumption(
    *,
    request_id,
    request_hash,
    validation_generation_id,
    packet_id,
    operation_id,
    lease_id,
    user,
    source,
    target,
    audit_store=None,
):
    """Read-only proof that the exact one-use admission was consumed for this apply."""
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    expected = {
        "authority_request_id": str(request_id or ""),
        "authority_request_hash": str(request_hash or ""),
        "validation_generation_id": str(validation_generation_id or ""),
        "packet_id": str(packet_id or ""),
        "operation_id": str(operation_id or ""),
        "lease_id": str(lease_id or ""),
        "user": str(user or ""),
        "source": str(source or ""),
        "target": str(target or ""),
    }
    missing = [f"ct_m0f_validation_{key}_missing" for key, value in expected.items() if not value]
    records = read_audit_records(audit_store)
    matches = [
        row for row in records
        if row.get("record_type") == CT_M0F_CONTROLLED_VALIDATION_CONSUMPTION_RECORD_TYPE
        and all(str(row.get(key) or "") == value for key, value in expected.items())
    ]
    errors = list(missing)
    if len(matches) != 1:
        errors.append("ct_m0f_validation_consumption_missing_or_duplicate")
    return {
        "ok": not errors,
        "status": "EXACT_CONSUMPTION_PROVEN" if not errors else "STOP_SAFE",
        "errors": sorted(set(errors)),
        "consumption": copy.deepcopy(matches[0]) if len(matches) == 1 else {},
        "runtime_apply": False,
        "routing_mutation": False,
        "users_moved": 0,
    }


def ct_m0f_standing_validation_envelope():
    """Immutable semantic Authority envelope for the bounded CT-M0F campaign."""
    return {
        "profile": "CT_M0F_BOUNDED_MULTI_GENERATION_USER_PATH_CUTOVER_VALIDATION",
        "classification": "STANDING_DELEGATED_CT_M0F_VALIDATION_POLICY",
        "program": "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
        "mission": "V7_CONSTANT_TIME_COHORT_FAILOVER_REUSABLE_FAST_PRIMITIVES_CLOSURE_V1",
        "purpose": "USER_PATH_CUTOVER_LATENCY_VALIDATION",
        "evidence_class": "CONTROLLED_CERTIFICATION_ONLY",
        "action_class": "BOUNDED_CT_M0F_USER_PATH_CUTOVER_VALIDATION",
        "subject_selection": {
            "certification_identities_only": True,
            "ordinary_identities_forbidden": True,
            "hard_coded_identity_forbidden": True,
            "owner": "existing controlled-production owner",
        },
        "execution_bounds": {
            "max_users_per_transaction": 1,
            "max_concurrent_transactions": 1,
            "max_active_operations": 1,
            "source_target_distinct": True,
            "source_target_selection": (
                "FRESH_EXISTING_OWNER_ELIGIBLE_ISOLATED_SOURCE_AND_SAFE_DISTINCT_TARGET"
            ),
        },
        "campaign_budget": {
            "max_valid_samples_per_implementation_fingerprint": 5,
            "max_invalid_or_safety_stopped_attempts_per_implementation_fingerprint": 3,
            "min_cold_valid_samples": 1,
            "min_warm_valid_samples": 2,
            "min_owner_backed_generations": 2,
            "stop_when_slo_proven": True,
            "identical_sample_after_residual_proven_forbidden": True,
        },
        "fresh_artifact_law": {
            "validation_generation": "FRESH_ONE_USE",
            "candidate": "FRESH_ONE_USE",
            "packet": "FRESH_ONE_USE",
            "lease": "FRESH_ONE_USE",
            "restore_barrier": "FRESH_OPERATION_BOUND",
            "source_target_snapshots": "FRESH_OR_GENERATION_VALID",
        },
        "verification_recovery": {
            "assignment_and_kernel_path": "REQUIRED",
            "target_egress_payload": "REQUIRED",
            "rollback_or_certified_no_rollback": "REQUIRED",
            "reset_or_forward_recovery": "REQUIRED",
            "deferred_closure": "REQUIRED",
            "outcome_replay_learning_time_consumption": "REQUIRED",
            "final_safe_mode": "OPEN",
        },
        "implementation_fingerprint_law": {
            "semantic_envelope_change_requires_new_decision": True,
            "implementation_only_change_requires_new_decision": False,
            "implementation_change_invalidates_prepared_artifacts": True,
            "per_fingerprint_sample_ledger_resets": True,
        },
        "lifecycle": {
            "revoke_supported": True,
            "freeze_supported": True,
            "kill_supported": True,
            "silent_renewal": False,
            "self_expansion": False,
        },
        "forbidden_effects_and_credit": [
            "ordinary_user_movement",
            "ordinary_user_reclassification",
            "stage_25_credit",
            "stage_48_credit",
            "ct_m8_credit",
            "natural_l8_credit",
            "authority_expansion",
            "runtime_scope_expansion",
            "production_maturity_change",
            "concurrency_increase",
            "new_failure_or_action_class",
            "external_resource_or_credential_mutation",
            "shared_target_fault_injection",
        ],
    }


def ct_m0f_standing_validation_request_hash(request):
    canonical = copy.deepcopy(request if isinstance(request, dict) else {})
    canonical.pop("request_id", None)
    canonical.pop("request_hash", None)
    return sha256_json(canonical)


def ct_m0f_standing_validation_contract_hash(contract):
    canonical = copy.deepcopy(contract if isinstance(contract, dict) else {})
    canonical.pop("contract_id", None)
    canonical.pop("contract_hash", None)
    return sha256_json(canonical)


def ct_m0f_runtime_implementation_fingerprint(
    *, governed_cycle, matrix_failure_consumer, autoswitch, health_runtime,
    routing_runtime,
):
    """Bind one certification campaign to the exact executable hot path."""
    governed_cycle = Path(governed_cycle)
    matrix_failure_consumer = Path(matrix_failure_consumer)
    routing_runtime = Path(routing_runtime)
    return sha256_json({
        "operator_execution": sha256_file(Path(__file__)),
        "operator_execution_pipeline": sha256_file(
            Path(__file__).with_name("operator_execution_pipeline.py")
        ),
        "intelligence_workers": sha256_file(
            Path(__file__).with_name("intelligence_workers.py")
        ),
        "governed_cycle": sha256_file(governed_cycle),
        "matrix_failure_consumer": sha256_file(matrix_failure_consumer),
        "matrix_signal_producer": sha256_file(
            matrix_failure_consumer.with_name("v7-service-matrix-test")
        ),
        "autoswitch": sha256_file(Path(autoswitch)),
        "health_runtime": sha256_file(Path(health_runtime)),
        "routing_runtime": sha256_file(routing_runtime),
        "route_writer_runtime": sha256_file(
            routing_runtime.with_name("v7-user-switch")
        ),
        "payload_consumer_runtime": sha256_file(
            governed_cycle.with_name("v7-client-speed-api")
        ),
    })


def build_ct_m0f_standing_validation_authority_request(
    *, policy_generation_hash, now=None,
):
    now = now or utc_now()
    request = {
        "schema_version": CT_M0F_STANDING_VALIDATION_REQUEST_SCHEMA,
        "status": "AWAITING_INDEPENDENT_AUTHORITY_DECISION",
        "created_at": now.isoformat(),
        "expires_at": (
            now + timedelta(seconds=CT_M0F_STANDING_VALIDATION_REQUEST_TTL_SECONDS)
        ).isoformat(),
        "decision_set": [CT_M0F_STANDING_VALIDATION_APPROVAL, "DECLINE_STANDING_DELEGATED_CT_M0F_VALIDATION_POLICY"],
        "issuing_owner_required": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
        "policy_generation_hash": str(policy_generation_hash or ""),
        "contract_ttl_seconds": CT_M0F_STANDING_VALIDATION_CONTRACT_TTL_SECONDS,
        "envelope": ct_m0f_standing_validation_envelope(),
        "future_identity_binding": "SELECTION_LAW_ONLY_NO_USER_TARGET_PACKET_OR_LEASE",
    }
    request_hash = ct_m0f_standing_validation_request_hash(request)
    request["request_hash"] = request_hash
    request["request_id"] = f"ctm0fsdpauth_r1_{request_hash[:24]}"
    return request


def validate_ct_m0f_standing_validation_authority_request(
    request, *, decision="DECLINE_STANDING_DELEGATED_CT_M0F_VALIDATION_POLICY",
    expected_request_id="", expected_request_hash="", now=None,
):
    now = now or utc_now()
    request = request if isinstance(request, dict) else {}
    errors = []
    request_id = str(request.get("request_id") or "")
    request_hash = str(request.get("request_hash") or "")
    if request.get("schema_version") != CT_M0F_STANDING_VALIDATION_REQUEST_SCHEMA:
        errors.append("ct_m0f_standing_request_schema_invalid")
    if ct_m0f_standing_validation_request_hash(request) != request_hash:
        errors.append("ct_m0f_standing_request_hash_mismatch")
    if request_id != f"ctm0fsdpauth_r1_{request_hash[:24]}":
        errors.append("ct_m0f_standing_request_identity_mismatch")
    if expected_request_id and request_id != str(expected_request_id):
        errors.append("ct_m0f_standing_expected_request_mismatch")
    if expected_request_hash and request_hash != str(expected_request_hash):
        errors.append("ct_m0f_standing_expected_hash_mismatch")
    if request.get("status") != "AWAITING_INDEPENDENT_AUTHORITY_DECISION":
        errors.append("ct_m0f_standing_request_not_pending")
    if decision not in set(request.get("decision_set") or []):
        errors.append("ct_m0f_standing_decision_not_exact")
    try:
        if parse_ts(request.get("expires_at")) <= now:
            errors.append("ct_m0f_standing_request_expired")
        if parse_ts(request.get("created_at")) > now:
            errors.append("ct_m0f_standing_created_at_invalid")
    except PacketError:
        errors.append("ct_m0f_standing_timestamps_invalid")
    if request.get("issuing_owner_required") != CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER:
        errors.append("ct_m0f_standing_owner_invalid")
    if len(str(request.get("policy_generation_hash") or "")) != 64:
        errors.append("ct_m0f_standing_policy_generation_missing")
    if int(request.get("contract_ttl_seconds") or 0) != CT_M0F_STANDING_VALIDATION_CONTRACT_TTL_SECONDS:
        errors.append("ct_m0f_standing_contract_ttl_invalid")
    if request.get("envelope") != ct_m0f_standing_validation_envelope():
        errors.append("ct_m0f_standing_envelope_invalid")
    if request.get("future_identity_binding") != "SELECTION_LAW_ONLY_NO_USER_TARGET_PACKET_OR_LEASE":
        errors.append("ct_m0f_standing_future_identity_binding_invalid")
    return {
        "ok": not errors,
        "errors": sorted(set(errors)),
        "request_id": request_id,
        "request_hash": request_hash,
        "decision": decision,
    }


def register_ct_m0f_standing_validation_authority_request(
    request, *, audit_store=None, producer_id="tools/v7-operator-execution-packet", now=None,
):
    now = now or utc_now()
    validation = validate_ct_m0f_standing_validation_authority_request(request, now=now)
    if not validation.get("ok"):
        raise PacketError(",".join(validation.get("errors") or ["ct_m0f_standing_request_invalid"]))
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    with current_action_class_contract_policy_lock(audit_store):
        records = read_audit_records(audit_store)
        active_pending = []
        decided = {
            str(row.get("authority_request_id") or "") for row in records
            if row.get("record_type") == CT_M0F_STANDING_VALIDATION_DECISION_RECORD_TYPE
        }
        for row in records:
            if row.get("record_type") != CT_M0F_STANDING_VALIDATION_REQUEST_RECORD_TYPE:
                continue
            prior = row.get("request") if isinstance(row.get("request"), dict) else {}
            prior_id = str(prior.get("request_id") or "")
            if prior_id == request["request_id"]:
                if prior == request and str(row.get("authority_request_hash") or "") == request["request_hash"]:
                    return {"status": "ALREADY_REGISTERED_EXACT", "request_id": request["request_id"], "request_hash": request["request_hash"], "audit_write": False}
                raise PacketError("ct_m0f_standing_request_identity_conflict")
            if prior_id in decided:
                continue
            try:
                if parse_ts(prior.get("expires_at")) > now:
                    active_pending.append(prior_id)
            except PacketError:
                pass
        if active_pending:
            raise PacketError("ct_m0f_standing_active_pending_request_exists")
        append_record(audit_store, {
            "schema_version": "v7.ct-m0f-standing-validation-authority-audit.v1",
            "record_type": CT_M0F_STANDING_VALIDATION_REQUEST_RECORD_TYPE,
            "authority_request_id": request["request_id"],
            "authority_request_hash": request["request_hash"],
            "request": copy.deepcopy(request),
            "producer": str(producer_id or "tools/v7-operator-execution-packet"),
            "created_at": now.isoformat(),
        })
    return {"status": "REGISTERED", "request_id": request["request_id"], "request_hash": request["request_hash"], "audit_write": True}


def pending_ct_m0f_standing_validation_authority_request(
    *, policy_generation_hash, audit_store=None, now=None,
):
    """Reuse one equivalent undecided request instead of creating churn."""
    now = now or utc_now()
    records = read_live_execution_lineage_records(
        Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    )
    decided = {
        str(row.get("authority_request_id") or "")
        for row in records
        if row.get("record_type")
        == CT_M0F_STANDING_VALIDATION_DECISION_RECORD_TYPE
    }
    matches = []
    for row in records:
        if row.get("record_type") != CT_M0F_STANDING_VALIDATION_REQUEST_RECORD_TYPE:
            continue
        request = row.get("request") if isinstance(row.get("request"), dict) else {}
        if str(request.get("request_id") or "") in decided:
            continue
        validation = validate_ct_m0f_standing_validation_authority_request(
            request, now=now,
        )
        if not validation.get("ok"):
            continue
        if str(request.get("policy_generation_hash") or "") != str(
            policy_generation_hash or ""
        ):
            continue
        matches.append(request)
    if len(matches) > 1:
        raise PacketError("ct_m0f_standing_pending_request_duplicate")
    return copy.deepcopy(matches[0]) if len(matches) == 1 else {}


def ct_m0f_standing_validation_request_from_audit(
    request_id, request_hash, *, audit_store=None, now=None,
):
    now = now or utc_now()
    # CT-M0F is a standing multi-generation contract.  Its exact request and
    # decision remain authoritative after the append-only audit rotates; using
    # only the active segment makes a still-valid policy disappear at rotation.
    records = read_live_execution_lineage_records(
        Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    )
    matches = [row for row in records if row.get("record_type") == CT_M0F_STANDING_VALIDATION_REQUEST_RECORD_TYPE and str(row.get("authority_request_id") or "") == str(request_id or "")]
    if len(matches) != 1:
        raise PacketError("ct_m0f_standing_request_missing_or_duplicate")
    request = matches[0].get("request") if isinstance(matches[0].get("request"), dict) else {}
    validation = validate_ct_m0f_standing_validation_authority_request(
        request, expected_request_id=request_id, expected_request_hash=request_hash, now=now,
    )
    if not validation.get("ok"):
        raise PacketError(",".join(validation.get("errors") or ["ct_m0f_standing_request_invalid"]))
    return request


def issue_ct_m0f_standing_validation_policy_from_audit(
    policy_path, *, request_id, request_hash, decision, actor_id,
    audit_store=None, now=None,
):
    allowed_decisions = {
        CT_M0F_STANDING_VALIDATION_APPROVAL,
        "DECLINE_STANDING_DELEGATED_CT_M0F_VALIDATION_POLICY",
    }
    if decision not in allowed_decisions:
        raise PacketError("ct_m0f_standing_decision_not_exact")
    if not str(actor_id or "").strip():
        raise PacketError("ct_m0f_standing_actor_missing")
    now = now or utc_now()
    policy_path = Path(policy_path)
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    with current_action_class_contract_policy_lock(policy_path):
        records = read_live_execution_lineage_records(audit_store)
        matching_decisions = [
            row for row in records
            if row.get("record_type")
            == CT_M0F_STANDING_VALIDATION_DECISION_RECORD_TYPE
            and str(row.get("authority_request_id") or "")
            == str(request_id or "")
        ]
        if len(matching_decisions) > 1:
            raise PacketError("ct_m0f_standing_decision_duplicate")
        policy_root = read_json(policy_path)
        policy_root = policy_root if isinstance(policy_root, dict) else {}
        current_contract = policy_root.get(CT_M0F_STANDING_VALIDATION_POLICY_KEY)
        if isinstance(current_contract, dict) and current_contract.get("status") == "ACTIVE":
            current_decision = (
                current_contract.get("authority_decision")
                if isinstance(current_contract.get("authority_decision"), dict)
                else {}
            )
            current_validation = validate_ct_m0f_standing_validation_policy(
                current_contract, audit_records=records, now=now,
            )
            if (
                current_validation.get("ok")
                and str(current_decision.get("request_id") or "")
                == str(request_id or "")
                and str(current_decision.get("request_hash") or "")
                == str(request_hash or "")
                and current_decision.get("decision") == decision
            ):
                return {
                    "status": "ALREADY_ACTIVATED_EXACT",
                    "contract": copy.deepcopy(current_contract),
                    "decision_id": current_decision.get("decision_id"),
                    "policy_write": False,
                    "candidate_created": False,
                    "packet_created": False,
                    "lease_created": False,
                    "runtime_apply": False,
                    "routing_mutation": False,
                    "users_moved": 0,
                    "production_maturity_change": False,
                }
            try:
                current_expires_at = parse_ts(current_contract.get("expires_at"))
            except PacketError as exc:
                raise PacketError("ct_m0f_standing_existing_contract_invalid") from exc
            if current_expires_at > now:
                raise PacketError("ct_m0f_standing_active_contract_exists")
        request = ct_m0f_standing_validation_request_from_audit(
            request_id, request_hash, audit_store=audit_store, now=now,
        )
        if request.get("policy_generation_hash") != sha256_file(policy_path):
            raise PacketError("ct_m0f_standing_policy_generation_changed")
        decision_id = stable_id("ctm0fsdpdec", {"request_id": request_id, "request_hash": request_hash, "decision": decision, "actor_id": str(actor_id)})
        if matching_decisions:
            existing = matching_decisions[0]
            if not (
                existing.get("decision_id") == decision_id
                and existing.get("authority_request_hash") == request_hash
                and existing.get("decision") == decision
                and str((existing.get("actor_provenance") or {}).get("actor_id") or "")
                == str(actor_id)
            ):
                raise PacketError("ct_m0f_standing_decision_conflict")
            decision_record = existing
        else:
            decision_record = append_record(audit_store, {
                "schema_version": "v7.ct-m0f-standing-validation-authority-decision.v1",
                "record_type": CT_M0F_STANDING_VALIDATION_DECISION_RECORD_TYPE,
                "decision_id": decision_id,
                "authority_request_id": request_id,
                "authority_request_hash": request_hash,
                "decision": decision,
                "actor_provenance": {"actor_id": str(actor_id), "issuing_owner": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER, "recorded_at": now.isoformat()},
                "created_at": now.isoformat(),
            })
        if decision != CT_M0F_STANDING_VALIDATION_APPROVAL:
            return {
                "status": "STANDING_DELEGATED_CT_M0F_VALIDATION_POLICY_DECLINED",
                "decision_id": decision_id,
                "policy_write": False,
                "candidate_created": False,
                "packet_created": False,
                "lease_created": False,
                "runtime_apply": False,
                "routing_mutation": False,
                "users_moved": 0,
                "production_maturity_change": False,
            }
        decided_at = parse_ts(
            (decision_record.get("actor_provenance") or {}).get("recorded_at")
            or decision_record.get("created_at")
        )
        contract = {
            "schema_version": CT_M0F_STANDING_VALIDATION_CONTRACT_SCHEMA,
            "status": "ACTIVE",
            "issued_at": decided_at.isoformat(),
            "expires_at": (decided_at + timedelta(seconds=CT_M0F_STANDING_VALIDATION_CONTRACT_TTL_SECONDS)).isoformat(),
            "issuing_owner": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
            "envelope": copy.deepcopy(request["envelope"]),
            "authority_decision": {"decision": decision, "decision_id": decision_id, "request_id": request_id, "request_hash": request_hash, "actor_id": str(actor_id), "decided_at": decided_at.isoformat()},
            "lifecycle": {"enabled": True, "frozen": False, "revoked": False, "killed": False, "renewal": "EXPLICIT_NEW_DECISION_ONLY"},
        }
        contract_hash = ct_m0f_standing_validation_contract_hash(contract)
        contract["contract_hash"] = contract_hash
        contract["contract_id"] = f"ctm0fsdpc_{contract_hash[:24]}"
        policy_root[CT_M0F_STANDING_VALIDATION_POLICY_KEY] = contract
        write_json_atomic(policy_path, policy_root)
    return {
        "status": "STANDING_DELEGATED_CT_M0F_VALIDATION_POLICY_ACTIVATED",
        "contract": contract,
        "decision_id": decision_id,
        "policy_write": True,
        "candidate_created": False,
        "packet_created": False,
        "lease_created": False,
        "runtime_apply": False,
        "routing_mutation": False,
        "users_moved": 0,
        "production_maturity_change": False,
    }


def validate_ct_m0f_standing_validation_policy(
    contract, *, audit_records=None, now=None,
):
    now = now or utc_now()
    contract = contract if isinstance(contract, dict) else {}
    errors = []
    contract_hash = str(contract.get("contract_hash") or "")
    if contract.get("schema_version") != CT_M0F_STANDING_VALIDATION_CONTRACT_SCHEMA:
        errors.append("ct_m0f_standing_contract_schema_invalid")
    if ct_m0f_standing_validation_contract_hash(contract) != contract_hash:
        errors.append("ct_m0f_standing_contract_hash_invalid")
    if str(contract.get("contract_id") or "") != f"ctm0fsdpc_{contract_hash[:24]}":
        errors.append("ct_m0f_standing_contract_identity_invalid")
    if contract.get("status") != "ACTIVE":
        errors.append("ct_m0f_standing_contract_not_active")
    try:
        if parse_ts(contract.get("expires_at")) <= now:
            errors.append("ct_m0f_standing_contract_expired")
    except PacketError:
        errors.append("ct_m0f_standing_contract_expiry_invalid")
    if contract.get("issuing_owner") != CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER:
        errors.append("ct_m0f_standing_contract_owner_invalid")
    if contract.get("envelope") != ct_m0f_standing_validation_envelope():
        errors.append("ct_m0f_standing_contract_envelope_invalid")
    lifecycle = contract.get("lifecycle") if isinstance(contract.get("lifecycle"), dict) else {}
    if lifecycle.get("enabled") is not True or any(lifecycle.get(key) is True for key in ("frozen", "revoked", "killed")):
        errors.append("ct_m0f_standing_contract_lifecycle_blocks_execution")
    decision = contract.get("authority_decision") if isinstance(contract.get("authority_decision"), dict) else {}
    if decision.get("decision") != CT_M0F_STANDING_VALIDATION_APPROVAL or not decision.get("request_id") or not decision.get("request_hash") or not decision.get("actor_id"):
        errors.append("ct_m0f_standing_contract_authority_provenance_invalid")
    if audit_records is not None:
        matches = [row for row in audit_records if row.get("record_type") == CT_M0F_STANDING_VALIDATION_DECISION_RECORD_TYPE and row.get("decision_id") == decision.get("decision_id") and row.get("authority_request_id") == decision.get("request_id") and row.get("authority_request_hash") == decision.get("request_hash") and row.get("decision") == decision.get("decision")]
        checkpoints = [
            row for row in audit_records
            if (
                row.get("record_type")
                == CT_M0F_STANDING_VALIDATION_LINEAGE_CHECKPOINT_RECORD_TYPE
                and row.get("contract_id") == contract.get("contract_id")
                and row.get("contract_hash") == contract_hash
                and row.get("decision_id") == decision.get("decision_id")
                and row.get("authority_request_id") == decision.get("request_id")
                and row.get("authority_request_hash") == decision.get("request_hash")
                and row.get("decision") == decision.get("decision")
                and row.get("no_prior_campaign_records_for_fingerprint") is True
                and len(str(row.get("source_authority_record_hash") or "")) == 64
                and str(row.get("record_hash") or "")
                == sha256_bytes(canonical_json({
                    key: value for key, value in row.items()
                    if key != "record_hash"
                }).encode("utf-8"))
            )
        ]
        if len(matches) != 1 and not (len(matches) == 0 and len(checkpoints) == 1):
            errors.append("ct_m0f_standing_authority_audit_missing_or_duplicate")
    return {"ok": not errors, "status": "ACTIVE" if not errors else "STOP_SAFE", "errors": sorted(set(errors)), "contract": copy.deepcopy(contract)}


def ensure_ct_m0f_standing_validation_lineage_checkpoint(
    contract,
    implementation_fingerprint,
    *,
    audit_store,
    audit_records,
    supporting_authority_decision_ids=(),
    now=None,
):
    """Roll immutable Authority proof into the live audit for one new build.

    The checkpoint is a bounded pointer inside the existing append-only audit,
    not another state owner.  It is created only when a complete lineage scan
    proves that the exact implementation fingerprint has no prior campaign
    records.  Later readers may therefore stop at the checkpoint while still
    counting every reservation/forward/terminal record for that fingerprint.
    """
    now = now or utc_now()
    contract = contract if isinstance(contract, dict) else {}
    fingerprint = str(implementation_fingerprint or "")
    audit_store = Path(audit_store)
    if len(fingerprint) != 64:
        return {
            "status": "STOP_SAFE_INVALID_IMPLEMENTATION_FINGERPRINT",
            "ok": False,
            "audit_write": False,
        }
    decision = (
        contract.get("authority_decision")
        if isinstance(contract.get("authority_decision"), dict)
        else {}
    )

    def exact_checkpoints(records):
        return [
            row for row in records
            if (
                row.get("record_type")
                == CT_M0F_STANDING_VALIDATION_LINEAGE_CHECKPOINT_RECORD_TYPE
                and row.get("contract_id") == contract.get("contract_id")
                and row.get("contract_hash") == contract.get("contract_hash")
                and row.get("implementation_fingerprint") == fingerprint
                and row.get("decision_id") == decision.get("decision_id")
                and row.get("no_prior_campaign_records_for_fingerprint") is True
            )
        ]

    def prior_campaign_records(records):
        return [
            row for row in records
            if (
                row.get("record_type") in {
                    CT_M0F_STANDING_VALIDATION_SAMPLE_RESERVATION_RECORD_TYPE,
                    CT_M0F_STANDING_VALIDATION_FORWARD_RECORD_TYPE,
                    CT_M0F_STANDING_VALIDATION_SAMPLE_TERMINAL_RECORD_TYPE,
                }
                and row.get("contract_id") == contract.get("contract_id")
                and row.get("implementation_fingerprint") == fingerprint
            )
        ]

    records = audit_records if isinstance(audit_records, list) else []
    supporting_ids = tuple(sorted({
        str(value)
        for value in (supporting_authority_decision_ids or ())
        if str(value)
    }))
    supporting_record_types = {
        CT_M0F_STANDING_VALIDATION_DECISION_RECORD_TYPE,
        STANDING_DELEGATED_POLICY_DECISION_RECORD_TYPE,
    }

    def verified_supporting_authority_records():
        selected = []
        for decision_id in supporting_ids:
            matches = [
                row for row in records
                if (
                    row.get("record_type") in supporting_record_types
                    and str(row.get("decision_id") or "") == decision_id
                )
            ]
            if len(matches) != 1:
                return []
            row = copy.deepcopy(matches[0])
            record_hash = str(row.get("record_hash") or "")
            if (
                len(record_hash) != 64
                or record_hash
                != sha256_bytes(canonical_json({
                    key: value for key, value in row.items()
                    if key != "record_hash"
                }).encode("utf-8"))
            ):
                return []
            selected.append(row)
        return selected

    existing = exact_checkpoints(records)
    if len(existing) == 1:
        return {"status": "REUSED", "ok": True, "audit_write": False}
    if len(existing) > 1 or prior_campaign_records(records):
        return {
            "status": "NOT_ADMITTED_EXISTING_FINGERPRINT_LINEAGE",
            "ok": True,
            "audit_write": False,
        }
    decisions = [
        row for row in records
        if (
            row.get("record_type") == CT_M0F_STANDING_VALIDATION_DECISION_RECORD_TYPE
            and row.get("decision_id") == decision.get("decision_id")
            and row.get("authority_request_id") == decision.get("request_id")
            and row.get("authority_request_hash") == decision.get("request_hash")
            and row.get("decision") == decision.get("decision")
        )
    ]
    if len(decisions) != 1:
        return {
            # The caller has already completed the authoritative policy/audit
            # validation.  A compact checkpoint is an optional acceleration,
            # never a new execution prerequisite; absence of an exact source
            # row therefore keeps the established full-scan behavior.
            "status": "NOT_ADMITTED_AUTHORITY_DECISION_NOT_EXACT",
            "ok": True,
            "audit_write": False,
        }
    source_hash = str(decisions[0].get("record_hash") or "")
    source_hash_valid = bool(
        len(source_hash) == 64
        and source_hash
        == sha256_bytes(canonical_json({
            key: value for key, value in decisions[0].items()
            if key != "record_hash"
        }).encode("utf-8"))
    )
    if not source_hash_valid:
        return {
            "status": "STOP_SAFE_AUTHORITY_RECORD_HASH_INVALID",
            "ok": False,
            "audit_write": False,
        }
    supporting_records = verified_supporting_authority_records()
    if supporting_ids and len(supporting_records) != len(supporting_ids):
        return {
            "status": "STOP_SAFE_SUPPORTING_AUTHORITY_LINEAGE_INVALID",
            "ok": False,
            "audit_write": False,
        }
    with current_action_class_contract_policy_lock(audit_store):
        current = read_live_execution_lineage_records(audit_store)
        existing = exact_checkpoints(current)
        if len(existing) == 1:
            return {"status": "REUSED", "ok": True, "audit_write": False}
        if len(existing) > 1 or prior_campaign_records(current):
            return {
                "status": "NOT_ADMITTED_EXISTING_FINGERPRINT_LINEAGE",
                "ok": True,
                "audit_write": False,
            }
        record = append_record(audit_store, {
            "schema_version": "v7.ct-m0f-standing-validation-lineage-checkpoint.v2",
            "record_type": CT_M0F_STANDING_VALIDATION_LINEAGE_CHECKPOINT_RECORD_TYPE,
            "contract_id": str(contract.get("contract_id") or ""),
            "contract_hash": str(contract.get("contract_hash") or ""),
            "implementation_fingerprint": fingerprint,
            "decision_id": str(decision.get("decision_id") or ""),
            "authority_request_id": str(decision.get("request_id") or ""),
            "authority_request_hash": str(decision.get("request_hash") or ""),
            "decision": str(decision.get("decision") or ""),
            "source_authority_record_hash": source_hash,
            # Hash-verified copies of the exact immutable Authority rows from
            # this same append-only owner let failure-time validation avoid a
            # repeated read of historical compressed segments.  This is only
            # an acceleration projection and grants no additional Authority.
            "supporting_authority_records": supporting_records,
            "no_prior_campaign_records_for_fingerprint": True,
            "producer": "admin_core.operator_execution",
            "created_at": now.isoformat(),
        })
    return {
        "status": "CREATED",
        "ok": True,
        "audit_write": True,
        "record_hash": str(record.get("record_hash") or ""),
    }


def ct_m0f_standing_validation_budget_status(
    contract, implementation_fingerprint, *, audit_records,
):
    contract_id = str((contract or {}).get("contract_id") or "")
    fingerprint = str(implementation_fingerprint or "")
    reservations = [row for row in audit_records if row.get("record_type") == CT_M0F_STANDING_VALIDATION_SAMPLE_RESERVATION_RECORD_TYPE and row.get("contract_id") == contract_id and row.get("implementation_fingerprint") == fingerprint]
    terminals = [row for row in audit_records if row.get("record_type") == CT_M0F_STANDING_VALIDATION_SAMPLE_TERMINAL_RECORD_TYPE and row.get("contract_id") == contract_id and row.get("implementation_fingerprint") == fingerprint]
    terminal_by_reservation = {str(row.get("reservation_id") or ""): row for row in terminals}
    valid = [row for row in terminals if row.get("sample_valid") is True]
    invalid = [row for row in terminals if row.get("sample_valid") is not True]
    cold = [row for row in valid if row.get("sample_kind") == "cold"]
    warm = [row for row in valid if row.get("sample_kind") == "warm"]
    generations = {str(row.get("validation_generation_id") or "") for row in valid if str(row.get("validation_generation_id") or "")}
    active = [row for row in reservations if str(row.get("reservation_id") or "") not in terminal_by_reservation]
    from admin_core import operator_execution_pipeline
    gate = operator_execution_pipeline.controlled_kernel_cutover_gate([
        row.get("sample_evidence")
        for row in valid
        if isinstance(row.get("sample_evidence"), dict)
    ])
    slo_proven = bool(gate.get("ok"))
    complete = bool(len(valid) >= 5 and len(cold) >= 1 and len(warm) >= 2 and len(generations) >= 2 and slo_proven)
    next_kind = "NONE" if complete else "cold" if not cold else "warm"
    return {
        "contract_id": contract_id,
        "implementation_fingerprint": fingerprint,
        "valid_samples": len(valid),
        "invalid_or_safety_stopped_attempts": len(invalid),
        "cold_valid_samples": len(cold),
        "warm_valid_samples": len(warm),
        "owner_backed_generation_count": len(generations),
        "active_reservations": len(active),
        "active_reservation": copy.deepcopy(active[0]) if len(active) == 1 else {},
        "slo_proven": slo_proven,
        "slo_gate": gate,
        "campaign_complete": complete,
        "next_sample_kind": next_kind,
        "attempt_budget_exhausted": len(invalid) >= 3,
        "valid_sample_budget_exhausted": len(valid) >= 5 and not complete,
    }


def reserve_ct_m0f_standing_validation_sample(
    policy_path, *, implementation_fingerprint, validation_generation_id,
    packet_id, operation_id, lease_id, user, source, target,
    audit_store=None, now=None,
):
    now = now or utc_now()
    policy_path = Path(policy_path)
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    required = {"implementation_fingerprint": str(implementation_fingerprint or ""), "validation_generation_id": str(validation_generation_id or ""), "packet_id": str(packet_id or ""), "operation_id": str(operation_id or ""), "lease_id": str(lease_id or ""), "user": str(user or ""), "source": str(source or ""), "target": str(target or "")}
    missing = [f"ct_m0f_standing_{key}_missing" for key, value in required.items() if not value]
    if missing or required["source"] == required["target"]:
        return {"ok": False, "status": "STOP_SAFE", "errors": sorted(set(missing + (["ct_m0f_standing_source_target_collision"] if required["source"] == required["target"] else []))), "audit_write": False}
    with current_action_class_contract_policy_lock(policy_path):
        policy_root = read_json(policy_path)
        contract = (policy_root or {}).get(CT_M0F_STANDING_VALIDATION_POLICY_KEY, {}) if isinstance(policy_root, dict) else {}
        # Name the exact immutable standing decision so the lineage reader
        # can reuse its already validated, source-signature-bound projection
        # while retaining every newer reservation/terminal row.  Any append
        # or rotation changes that signature and forces a fresh scan.
        standing_decision = (
            contract.get("authority_decision")
            if isinstance(contract.get("authority_decision"), dict)
            else {}
        )
        records = read_live_execution_lineage_records(
            audit_store,
            required_decision_ids=tuple(filter(None, [
                str(standing_decision.get("decision_id") or "")
            ])),
        )
        validation = validate_ct_m0f_standing_validation_policy(contract, audit_records=records, now=now)
        if not validation.get("ok"):
            return {"ok": False, "status": "STOP_SAFE", "errors": validation.get("errors") or [], "audit_write": False}
        budget = ct_m0f_standing_validation_budget_status(contract, required["implementation_fingerprint"], audit_records=records)
        exact = [row for row in records if row.get("record_type") == CT_M0F_STANDING_VALIDATION_SAMPLE_RESERVATION_RECORD_TYPE and row.get("contract_id") == contract.get("contract_id") and row.get("validation_generation_id") == required["validation_generation_id"]]
        if exact:
            if len(exact) == 1 and all(str(exact[0].get(key) or "") == value for key, value in required.items()):
                return {"ok": True, "status": "ALREADY_RESERVED_EXACT", "reservation": copy.deepcopy(exact[0]), "budget": budget, "audit_write": False}
            return {"ok": False, "status": "STOP_SAFE", "errors": ["ct_m0f_standing_generation_reservation_conflict"], "audit_write": False}
        errors = []
        if budget["campaign_complete"]:
            errors.append("ct_m0f_standing_campaign_complete")
        if budget["active_reservations"]:
            errors.append("ct_m0f_standing_active_operation_exists")
        if budget["attempt_budget_exhausted"]:
            errors.append("ct_m0f_standing_attempt_budget_exhausted")
        if budget["valid_sample_budget_exhausted"]:
            errors.append("ct_m0f_standing_valid_sample_budget_exhausted")
        if errors:
            return {"ok": False, "status": "STOP_SAFE", "errors": errors, "budget": budget, "audit_write": False}
        reservation_id = stable_id("ctm0fsample", {**required, "contract_id": contract["contract_id"]})
        record = append_record(audit_store, {
            "schema_version": "v7.ct-m0f-standing-validation-sample-reservation.v1",
            "record_type": CT_M0F_STANDING_VALIDATION_SAMPLE_RESERVATION_RECORD_TYPE,
            "reservation_id": reservation_id,
            "contract_id": contract["contract_id"],
            "contract_hash": contract["contract_hash"],
            "sample_kind": budget["next_sample_kind"],
            **required,
            "status": "RESERVED",
            "created_at": now.isoformat(),
        })
    return {"ok": True, "status": "AUTO_ADMITTED_BY_STANDING_DELEGATED_CT_M0F_VALIDATION_POLICY", "reservation": record, "budget": budget, "audit_write": True}


def validate_ct_m0f_standing_validation_sample_reservation(
    *, contract_id, contract_hash, implementation_fingerprint,
    validation_generation_id, packet_id, operation_id, lease_id, user, source, target,
    audit_store=None, audit_records=None,
):
    expected = {"contract_id": str(contract_id or ""), "contract_hash": str(contract_hash or ""), "implementation_fingerprint": str(implementation_fingerprint or ""), "validation_generation_id": str(validation_generation_id or ""), "packet_id": str(packet_id or ""), "operation_id": str(operation_id or ""), "lease_id": str(lease_id or ""), "user": str(user or ""), "source": str(source or ""), "target": str(target or "")}
    records = (
        list(audit_records)
        if isinstance(audit_records, (list, tuple))
        else read_live_execution_lineage_records(
            Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
        )
    )
    matches = [row for row in records if row.get("record_type") == CT_M0F_STANDING_VALIDATION_SAMPLE_RESERVATION_RECORD_TYPE and all(str(row.get(key) or "") == value for key, value in expected.items())]
    errors = [f"ct_m0f_standing_{key}_missing" for key, value in expected.items() if not value]
    if len(matches) != 1:
        errors.append("ct_m0f_standing_sample_reservation_missing_or_duplicate")
    return {"ok": not errors, "status": "EXACT_RESERVATION_PROVEN" if not errors else "STOP_SAFE", "errors": sorted(set(errors)), "reservation": copy.deepcopy(matches[0]) if len(matches) == 1 else {}}


def ct_m0f_standing_validation_sample_from_audit(
    reservation_id, *, audit_store=None,
):
    """Return one exact standing sample lineage and its durable progress."""
    records = read_live_execution_lineage_records(
        Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    )
    reservations = [
        row for row in records
        if row.get("record_type")
        == CT_M0F_STANDING_VALIDATION_SAMPLE_RESERVATION_RECORD_TYPE
        and row.get("reservation_id") == str(reservation_id or "")
    ]
    forwards = [
        row for row in records
        if row.get("record_type")
        == CT_M0F_STANDING_VALIDATION_FORWARD_RECORD_TYPE
        and row.get("reservation_id") == str(reservation_id or "")
    ]
    terminals = [
        row for row in records
        if row.get("record_type")
        == CT_M0F_STANDING_VALIDATION_SAMPLE_TERMINAL_RECORD_TYPE
        and row.get("reservation_id") == str(reservation_id or "")
    ]
    errors = []
    if len(reservations) != 1:
        errors.append("ct_m0f_standing_sample_reservation_missing_or_duplicate")
    if len(forwards) > 1:
        errors.append("ct_m0f_standing_forward_evidence_duplicate")
    if len(terminals) > 1:
        errors.append("ct_m0f_standing_sample_terminal_duplicate")
    return {
        "ok": not errors,
        "status": "EXACT_SAMPLE_LINEAGE_PROVEN" if not errors else "STOP_SAFE",
        "errors": errors,
        "reservation": copy.deepcopy(reservations[0]) if len(reservations) == 1 else {},
        "forward_evidence": copy.deepcopy(forwards[0]) if len(forwards) == 1 else {},
        "terminal": copy.deepcopy(terminals[0]) if len(terminals) == 1 else {},
    }


def reserve_ct_m0f_standing_validation_transaction(
    *, contract, implementation_fingerprint, user, source, target,
    sample_binding_fingerprint, source_reservation_id, source_fingerprint,
    audit_store=None, now=None,
):
    """Reserve the bounded pre-T0 interval through the existing audit owner.

    This is not an assignment lock.  It protects one certification identity
    from an *independent* recovery/rebalance only while its exact controlled
    failure transaction is live.  A later Packet/Lease binds the same record
    to the governed operation; terminal cleanup or expiry releases it.
    """
    now = now or utc_now()
    audit_store = Path(
        audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE
    )
    contract = contract if isinstance(contract, dict) else {}
    required = {
        "contract_id": str(contract.get("contract_id") or ""),
        "contract_hash": str(contract.get("contract_hash") or ""),
        "implementation_fingerprint": str(implementation_fingerprint or ""),
        "user": str(user or ""),
        "source": str(source or ""),
        "target": str(target or ""),
        "sample_binding_fingerprint": str(sample_binding_fingerprint or ""),
        "source_reservation_id": str(source_reservation_id or ""),
        "source_fingerprint": str(source_fingerprint or ""),
    }
    missing = [
        f"ct_m0f_transaction_{key}_missing"
        for key, value in required.items() if not value
    ]
    if missing or required["source"] == required["target"]:
        return {
            "ok": False,
            "status": "STOP_SAFE",
            "errors": sorted(set(
                missing + (
                    ["ct_m0f_transaction_source_target_collision"]
                    if required["source"] == required["target"] else []
                )
            )),
            "audit_write": False,
        }
    with current_action_class_contract_policy_lock(audit_store):
        records = read_live_execution_lineage_records(audit_store)
        validation = validate_ct_m0f_standing_validation_policy(
            contract, audit_records=records, now=now,
        )
        if not validation.get("ok"):
            return {
                "ok": False,
                "status": "STOP_SAFE",
                "errors": validation.get("errors") or [],
                "audit_write": False,
            }
        active = active_ct_m0f_standing_validation_transactions(
            records, now=now,
        )
        exact = [
            item for item in active
            if all(str(item.get(key) or "") == value for key, value in required.items())
        ]
        if exact:
            if len(exact) == 1:
                return {
                    "ok": True,
                    "status": "ALREADY_RESERVED_EXACT",
                    "reservation": copy.deepcopy(exact[0]),
                    "audit_write": False,
                }
            return {
                "ok": False,
                "status": "STOP_SAFE",
                "errors": ["ct_m0f_transaction_duplicate_exact_reservation"],
                "audit_write": False,
            }
        conflicts = [
            item for item in active
            if str(item.get("user") or "") == required["user"]
            or str(item.get("source") or "") == required["source"]
        ]
        if conflicts:
            return {
                "ok": False,
                "status": "STOP_SAFE",
                "errors": ["ct_m0f_transaction_active_reservation_conflict"],
                "active_reservations": copy.deepcopy(conflicts),
                "audit_write": False,
            }
        reservation_id = stable_id("ctm0ftx", required)
        record = append_record(audit_store, {
            "schema_version": "v7.ct-m0f-standing-validation-transaction-reservation.v1",
            "record_type": CT_M0F_STANDING_VALIDATION_TRANSACTION_RESERVATION_RECORD_TYPE,
            "transaction_reservation_id": reservation_id,
            **required,
            "status": "RESERVED_PRE_T0",
            "created_at": now.isoformat(),
            "expires_at": (
                now + timedelta(
                    seconds=CT_M0F_STANDING_VALIDATION_TRANSACTION_TTL_SECONDS
                )
            ).isoformat(),
            "owner": "admin_core.operator_execution existing CT-M0F reservation owner",
        })
    return {
        "ok": True,
        "status": "RESERVED_PRE_T0",
        "reservation": record,
        "audit_write": True,
    }


def active_ct_m0f_standing_validation_transactions(records, *, now=None):
    """Return durable, unexpired CT-M0F transaction reservations only."""
    now = now or utc_now()
    rows = list(records or [])
    reservations = [
        row for row in rows
        if row.get("record_type")
        == CT_M0F_STANDING_VALIDATION_TRANSACTION_RESERVATION_RECORD_TYPE
    ]
    bindings = {
        str(row.get("transaction_reservation_id") or ""): row
        for row in rows
        if row.get("record_type")
        == CT_M0F_STANDING_VALIDATION_TRANSACTION_BINDING_RECORD_TYPE
    }
    terminal_ids = {
        str(row.get("transaction_reservation_id") or "")
        for row in rows
        if row.get("record_type")
        == CT_M0F_STANDING_VALIDATION_TRANSACTION_TERMINAL_RECORD_TYPE
    }
    active = []
    for reservation in reservations:
        reservation_id = str(reservation.get("transaction_reservation_id") or "")
        if not reservation_id or reservation_id in terminal_ids:
            continue
        try:
            if now >= parse_ts(reservation.get("expires_at")):
                continue
        except PacketError:
            continue
        item = copy.deepcopy(reservation)
        binding = bindings.get(reservation_id)
        if isinstance(binding, dict):
            item["operation_binding"] = copy.deepcopy(binding)
        active.append(item)
    return active


def ct_m0f_standing_validation_transaction_guard(
    *, user, source, target, operation_id="", audit_store=None, now=None,
):
    """Tell existing Planner consumers whether a move is independently safe.

    An active unbound reservation stops all normal moves of its identity.  A
    bound reservation permits only the exact governed operation/source/target.
    This leaves normal health processing alive for every other identity.
    """
    now = now or utc_now()
    audit_store = Path(
        audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE
    )
    records = read_live_execution_lineage_records(audit_store)
    matching = [
        row for row in active_ct_m0f_standing_validation_transactions(
            records, now=now,
        )
        if str(row.get("user") or "") == str(user or "")
        and str(row.get("source") or "") == str(source or "")
    ]
    if not matching:
        return {
            "ok": True,
            "status": "NO_ACTIVE_CT_M0F_TRANSACTION_RESERVATION",
            "independent_reassignment_allowed": True,
            "reservation": {},
        }
    if len(matching) != 1:
        return {
            "ok": False,
            "status": "STOP_SAFE",
            "independent_reassignment_allowed": False,
            "blockers": ["ct_m0f_transaction_reservation_ambiguous"],
            "reservation": {},
        }
    reservation = matching[0]
    binding = (
        reservation.get("operation_binding")
        if isinstance(reservation.get("operation_binding"), dict)
        else {}
    )
    exact_governed = bool(
        binding
        and str(binding.get("operation_id") or "") == str(operation_id or "")
        and str(reservation.get("target") or "") == str(target or "")
    )
    return {
        "ok": exact_governed,
        "status": (
            "EXACT_GOVERNED_CT_M0F_TRANSACTION_OPERATION_PERMITTED"
            if exact_governed
            else "CT_M0F_TRANSACTION_RESERVATION_PROTECTS_IDENTITY"
        ),
        "independent_reassignment_allowed": False,
        "reservation": reservation,
        "blockers": ([] if exact_governed else [
            "ct_m0f_active_transaction_reservation_requires_exact_governed_operation"
        ]),
    }


def bind_ct_m0f_standing_validation_transaction(
    *, transaction_reservation_id, packet_id, operation_id, lease_id,
    matrix_sample_binding_fingerprint,
    audit_store=None, now=None,
):
    """Bind the pre-T0 reservation to the exact existing Packet/Lease."""
    now = now or utc_now()
    audit_store = Path(
        audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE
    )
    required = {
        "transaction_reservation_id": str(transaction_reservation_id or ""),
        "packet_id": str(packet_id or ""),
        "operation_id": str(operation_id or ""),
        "lease_id": str(lease_id or ""),
        # This is the fresh Matrix -> Planner selection binding observed on
        # the governed side of T0.  It is intentionally recorded alongside,
        # rather than compared with, the pre-T0 reservation fingerprint:
        # an ordinary Matrix generation is allowed to refresh its derived
        # selection receipt while the immutable user/source/target and
        # source-reservation envelope remains exact.
        "matrix_sample_binding_fingerprint": str(
            matrix_sample_binding_fingerprint or ""
        ),
    }
    missing = [
        f"ct_m0f_transaction_{key}_missing"
        for key, value in required.items() if not value
    ]
    if missing:
        return {"ok": False, "status": "STOP_SAFE", "errors": missing, "audit_write": False}
    with current_action_class_contract_policy_lock(audit_store):
        records = read_live_execution_lineage_records(audit_store)
        active = {
            str(row.get("transaction_reservation_id") or ""): row
            for row in active_ct_m0f_standing_validation_transactions(records, now=now)
        }
        reservation = active.get(required["transaction_reservation_id"])
        if not reservation:
            return {
                "ok": False,
                "status": "STOP_SAFE",
                "errors": ["ct_m0f_transaction_reservation_not_active"],
                "audit_write": False,
            }
        existing = [
            row for row in records
            if row.get("record_type")
            == CT_M0F_STANDING_VALIDATION_TRANSACTION_BINDING_RECORD_TYPE
            and str(row.get("transaction_reservation_id") or "")
            == required["transaction_reservation_id"]
        ]
        if existing:
            if len(existing) == 1 and all(
                str(existing[0].get(key) or "") == value
                for key, value in required.items()
            ):
                return {
                    "ok": True,
                    "status": "ALREADY_BOUND_EXACT",
                    "binding": copy.deepcopy(existing[0]),
                    "audit_write": False,
                }
            return {
                "ok": False,
                "status": "STOP_SAFE",
                "errors": ["ct_m0f_transaction_binding_conflict"],
                "audit_write": False,
            }
        record = append_record(audit_store, {
            "schema_version": "v7.ct-m0f-standing-validation-transaction-binding.v1",
            "record_type": CT_M0F_STANDING_VALIDATION_TRANSACTION_BINDING_RECORD_TYPE,
            **required,
            "user": str(reservation.get("user") or ""),
            "source": str(reservation.get("source") or ""),
            "target": str(reservation.get("target") or ""),
            "implementation_fingerprint": str(
                reservation.get("implementation_fingerprint") or ""
            ),
            "bound_at": now.isoformat(),
            "owner": "admin_core.operator_execution existing CT-M0F reservation owner",
        })
    return {"ok": True, "status": "BOUND_TO_EXACT_PACKET_LEASE", "binding": record, "audit_write": True}


def release_ct_m0f_standing_validation_transaction(
    *, transaction_reservation_id, reason, audit_store=None, now=None,
):
    """Close one transaction reservation on terminal/rollback recovery."""
    now = now or utc_now()
    audit_store = Path(
        audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE
    )
    reservation_id = str(transaction_reservation_id or "")
    if not reservation_id or not str(reason or ""):
        return {"ok": False, "status": "STOP_SAFE", "errors": ["ct_m0f_transaction_release_identity_missing"], "audit_write": False}
    with current_action_class_contract_policy_lock(audit_store):
        records = read_live_execution_lineage_records(audit_store)
        reservations = [
            row for row in records
            if row.get("record_type")
            == CT_M0F_STANDING_VALIDATION_TRANSACTION_RESERVATION_RECORD_TYPE
            and str(row.get("transaction_reservation_id") or "") == reservation_id
        ]
        terminals = [
            row for row in records
            if row.get("record_type")
            == CT_M0F_STANDING_VALIDATION_TRANSACTION_TERMINAL_RECORD_TYPE
            and str(row.get("transaction_reservation_id") or "") == reservation_id
        ]
        if len(reservations) != 1:
            return {"ok": False, "status": "STOP_SAFE", "errors": ["ct_m0f_transaction_reservation_missing_or_duplicate"], "audit_write": False}
        if terminals:
            if len(terminals) == 1:
                return {"ok": True, "status": "ALREADY_TERMINAL", "terminal": copy.deepcopy(terminals[0]), "audit_write": False}
            return {"ok": False, "status": "STOP_SAFE", "errors": ["ct_m0f_transaction_terminal_duplicate"], "audit_write": False}
        record = append_record(audit_store, {
            "schema_version": "v7.ct-m0f-standing-validation-transaction-terminal.v1",
            "record_type": CT_M0F_STANDING_VALIDATION_TRANSACTION_TERMINAL_RECORD_TYPE,
            "transaction_reservation_id": reservation_id,
            "implementation_fingerprint": str(
                reservations[0].get("implementation_fingerprint") or ""
            ),
            "terminal_reason": str(reason),
            "terminal_at": now.isoformat(),
            "owner": "admin_core.operator_execution existing CT-M0F reservation owner",
        })
    return {"ok": True, "status": "RELEASED", "terminal": record, "audit_write": True}


def record_ct_m0f_standing_validation_forward_evidence(
    *, reservation_id, sample_evidence, audit_store=None, now=None,
):
    """Bind one exact CT-M0F observation before reset/closure begins.

    A valid observation is the only one that may earn a CT-M0F sample.  An
    invalid observation is still durable diagnostic evidence: dropping it
    turns an exhausted bounded campaign into an opaque retry loop.  Both use
    the existing reservation/audit owner and remain one-record-per-reservation.
    """
    now = now or utc_now()
    audit_store = Path(
        audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE
    )
    evidence = sample_evidence if isinstance(sample_evidence, dict) else {}
    status = str(evidence.get("status") or "")
    if status not in {
        "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_PASS",
        "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_INVALID",
    }:
        raise PacketError("ct_m0f_standing_forward_evidence_status_invalid")
    if (
        status == "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_INVALID"
        and not [value for value in evidence.get("blockers", []) if str(value)]
    ):
        raise PacketError(
            "ct_m0f_standing_invalid_evidence_blockers_required"
        )
    with current_action_class_contract_policy_lock(audit_store):
        records = read_live_execution_lineage_records(audit_store)
        reservations = [
            row for row in records
            if row.get("record_type")
            == CT_M0F_STANDING_VALIDATION_SAMPLE_RESERVATION_RECORD_TYPE
            and row.get("reservation_id") == str(reservation_id or "")
        ]
        if len(reservations) != 1:
            raise PacketError(
                "ct_m0f_standing_sample_reservation_missing_or_duplicate"
            )
        existing = [
            row for row in records
            if row.get("record_type")
            == CT_M0F_STANDING_VALIDATION_FORWARD_RECORD_TYPE
            and row.get("reservation_id") == str(reservation_id or "")
        ]
        if existing:
            if len(existing) == 1 and existing[0].get("sample_evidence") == evidence:
                return {
                    "status": "ALREADY_RECORDED_EXACT",
                    "record": copy.deepcopy(existing[0]),
                    "audit_write": False,
                }
            raise PacketError("ct_m0f_standing_forward_evidence_conflict")
        reservation = reservations[0]
        record = append_record(audit_store, {
            "schema_version": "v7.ct-m0f-standing-validation-forward-evidence.v1",
            "record_type": CT_M0F_STANDING_VALIDATION_FORWARD_RECORD_TYPE,
            "forward_evidence_id": stable_id("ctm0ffwd", {
                "reservation_id": reservation_id,
                "sample_evidence": evidence,
            }),
            "reservation_id": reservation["reservation_id"],
            "contract_id": reservation["contract_id"],
            "implementation_fingerprint": reservation[
                "implementation_fingerprint"
            ],
            "validation_generation_id": reservation[
                "validation_generation_id"
            ],
            "sample_kind": reservation["sample_kind"],
            "evidence_classification": (
                "VALID_FORWARD_EVIDENCE"
                if status == "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_PASS"
                else "INVALID_DIAGNOSTIC_EVIDENCE"
            ),
            "sample_classification": str(
                evidence.get("sample_classification")
                or (
                    "FUNCTIONALLY_VALID_PERFORMANCE_PASS"
                    if status == "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_PASS"
                    else "MEASUREMENT_INVALID"
                )
            ),
            "sample_evidence": copy.deepcopy(evidence),
            "created_at": now.isoformat(),
        })
    return {
        "status": (
            "RECORDED"
            if status == "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_PASS"
            else "RECORDED_INVALID_DIAGNOSTIC"
        ),
        "record": record,
        "audit_write": True,
    }


def record_ct_m0f_standing_validation_sample_terminal(
    *, reservation_id, sample_valid, sample_evidence=None, terminal_reason="",
    audit_store=None, now=None,
):
    now = now or utc_now()
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    with current_action_class_contract_policy_lock(audit_store):
        records = read_live_execution_lineage_records(audit_store)
        reservations = [row for row in records if row.get("record_type") == CT_M0F_STANDING_VALIDATION_SAMPLE_RESERVATION_RECORD_TYPE and row.get("reservation_id") == str(reservation_id or "")]
        if len(reservations) != 1:
            raise PacketError("ct_m0f_standing_sample_reservation_missing_or_duplicate")
        existing = [row for row in records if row.get("record_type") == CT_M0F_STANDING_VALIDATION_SAMPLE_TERMINAL_RECORD_TYPE and row.get("reservation_id") == str(reservation_id or "")]
        if existing:
            if len(existing) == 1 and existing[0].get("sample_valid") == bool(sample_valid) and existing[0].get("sample_evidence") == (sample_evidence if isinstance(sample_evidence, dict) else {}) and str(existing[0].get("terminal_reason") or "") == str(terminal_reason or ""):
                return {"status": "ALREADY_RECORDED_EXACT", "record": copy.deepcopy(existing[0]), "audit_write": False}
            raise PacketError("ct_m0f_standing_sample_terminal_conflict")
        reservation = reservations[0]
        record = append_record(audit_store, {
            "schema_version": "v7.ct-m0f-standing-validation-sample-terminal.v1",
            "record_type": CT_M0F_STANDING_VALIDATION_SAMPLE_TERMINAL_RECORD_TYPE,
            "terminal_id": stable_id("ctm0fsampleterm", {"reservation_id": reservation_id, "sample_valid": bool(sample_valid), "sample_evidence": sample_evidence if isinstance(sample_evidence, dict) else {}, "terminal_reason": str(terminal_reason or "")}),
            "reservation_id": reservation["reservation_id"],
            "contract_id": reservation["contract_id"],
            "implementation_fingerprint": reservation["implementation_fingerprint"],
            "validation_generation_id": reservation["validation_generation_id"],
            "sample_kind": reservation["sample_kind"],
            "sample_valid": bool(sample_valid),
            "sample_evidence": copy.deepcopy(sample_evidence) if isinstance(sample_evidence, dict) else {},
            "terminal_reason": str(terminal_reason or ""),
            "created_at": now.isoformat(),
        })
    return {"status": "RECORDED", "record": record, "audit_write": True}


def build_controlled_certification_substrate_authority_request(
    *,
    active_program,
    source_id,
    current_pool_status,
    current_policy_contract_id,
    current_policy_contract_hash,
    target_total=48,
    profile=CONTROLLED_CERTIFICATION_SUBSTRATE_TIER48_PROFILE,
    controlled_target_id="",
    controlled_target_admission=None,
    now=None,
):
    """Build one coordinated, independently decidable Tier-48 substrate request.

    The request is produced by the existing operator-execution Authority owner.
    Its four subscopes are explicit and non-transitive: approving identity
    provisioning does not implicitly approve assignment, controlled
    degradation, or execution.  A later decision must name the exact combined
    request and every admitted subscope.
    """
    now = now or utc_now()
    pool = current_pool_status if isinstance(current_pool_status, dict) else {}
    profile = str(profile or CONTROLLED_CERTIFICATION_SUBSTRATE_TIER48_PROFILE)
    if profile == CONTROLLED_CERTIFICATION_SUBSTRATE_CT_M0F_ONE_USER_PROFILE:
        # This is a setup-only, one-identity substrate.  Packet/lease/apply
        # remain separately admitted by the existing CT-M0F validation owner.
        target_total = 1
    else:
        target_total = max(0, as_int(target_total, 0))
    current_total = max(0, as_int(pool.get("total_enabled_certification_users"), 0))
    current_on_source = max(
        0,
        as_int(pool.get("max_enabled_certification_users_on_one_active_source"), 0),
    )
    controlled_target_admission = (
        controlled_target_admission
        if isinstance(controlled_target_admission, dict)
        else {}
    )
    reuse_existing_pool = current_on_source >= target_total
    required_incremental_identities = max(0, target_total - current_on_source)
    registry_hashes = (
        pool.get("registry_hashes")
        if isinstance(pool.get("registry_hashes"), dict)
        else {}
    )
    request = {
        "schema_version": CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_SCHEMA,
        "status": "AWAITING_INDEPENDENT_ENGINEERING_AUTHORITY_DECISION",
        "created_at": now.isoformat(),
        "expires_at": (
            now + timedelta(seconds=CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_TTL_SECONDS)
        ).isoformat(),
        "decision_set": [CONTROLLED_CERTIFICATION_SUBSTRATE_APPROVAL, "DECLINE"],
        "issuing_owner_required": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
        "active_program": str(active_program or ""),
        "mission": (
            "V7_HOT_PATH_CT_M0F_ONE_USER_CONTROLLED_SUBSTRATE"
            if profile == CONTROLLED_CERTIFICATION_SUBSTRATE_CT_M0F_ONE_USER_PROFILE
            else "V7_SERVICE_FAILURE_T48_M8_CONTROLLED_POOL_RECONCILIATION"
        ),
        "scope": {
            "profile": profile,
            "target_total_certification_identities": target_total,
            "max_new_certification_identities": (
                0 if reuse_existing_pool else required_incremental_identities
            ),
            "identity_strategy": (
                "REUSE_EXISTING_VALID_POOL"
                if reuse_existing_pool
                else "PROVISION_INCREMENTAL_DELTA"
            ),
            "certification_only": True,
            "ordinary_customer_involvement": False,
            "billing_or_customer_entitlement": False,
            "real_customer_workload_dependency": False,
            "source_id": str(source_id or ""),
            "controlled_target_id": str(controlled_target_id or ""),
            "controlled_target_admission_class": (
                "EXECUTION_ONLY_CONTROLLED_CERTIFICATION_TARGET"
                if controlled_target_id
                else "EXISTING_PLANNER_SAFE_TARGET"
            ),
            "single_controlled_source_required": True,
            "campaign_stages": (
                [1]
                if profile == CONTROLLED_CERTIFICATION_SUBSTRATE_CT_M0F_ONE_USER_PROFILE
                else [5, 10, 25, 48]
            ),
            "max_concurrent_transactions": 1,
            "automatic_stage_progression": (
                False
                if profile == CONTROLLED_CERTIFICATION_SUBSTRATE_CT_M0F_ONE_USER_PROFILE
                else True
            ),
            "self_expansion_allowed": False,
        },
        "current_owner_backed_state": {
            "total_enabled_certification_users": current_total,
            "max_enabled_certification_users_on_source": current_on_source,
            "pool_fingerprint": str(pool.get("fingerprint") or ""),
            "users_registry_hash": str(registry_hashes.get("users_registry") or ""),
            "egress_registry_hash": str(registry_hashes.get("egress_registry") or ""),
            "active_policy_contract_id": str(current_policy_contract_id or ""),
            "active_policy_contract_hash": str(current_policy_contract_hash or ""),
            "controlled_target_fingerprint": str(
                controlled_target_admission.get("fingerprint") or ""
            ),
        },
        "controlled_target_contract": {
            "target_id": str(controlled_target_id or ""),
            "role": str(controlled_target_admission.get("role") or ""),
            "reservation_owner": str(
                controlled_target_admission.get("reservation_owner") or ""
            ),
            "execution_reserved": bool(
                controlled_target_admission.get("execution_reserved")
            ),
            "canary_reserved": bool(
                controlled_target_admission.get("canary_reserved")
            ),
            "autoswitch_allowed": False,
            "rebalance_allowed": False,
            "ordinary_production_assignment_allowed": False,
            "certification_only_assignment_allowed": bool(controlled_target_id),
            "zero_user_at_request": (
                int(controlled_target_admission.get("enabled_assigned_users") or 0)
                == 0
            ),
            "fresh_health_required_per_stage": True,
            "capacity_and_reserve_required_per_stage": True,
            "scope_lifetime": "THIS_EXACT_CONTROLLED_CAMPAIGN_ONLY",
        },
        "coordinated_subscopes": [
            {
                "id": "IDENTITY_PROVISIONING",
                "owner": "existing v7-user-create-from-ipam + users.registry owner",
                "exact_action": "create up to the requested total dedicated identities",
                "independent_admission_required": True,
            },
            {
                "id": "CERTIFICATION_CLASSIFICATION_AND_ASSIGNMENT",
                "owner": "existing users.registry + assignment owner",
                "exact_action": "mark certification-only and assign to the exact controlled source",
                "independent_admission_required": True,
            },
            *([] if profile == CONTROLLED_CERTIFICATION_SUBSTRATE_CT_M0F_ONE_USER_PROFILE else [{
                "id": "CONTROLLED_SOURCE_CONDITION",
                "owner": "existing v7-egress-set-state + Controlled Production owner",
                "exact_action": "materialize and restore one bounded controlled failure per stage",
                "independent_admission_required": True,
            }, {
                "id": "PROGRESSIVE_CAMPAIGN_EXECUTION",
                "owner": "existing Matrix/Packet/lease/cohort transaction owners",
                "exact_action": "execute 5 -> 10 -> 25 -> 48 with fresh gates and reset between stages",
                "independent_admission_required": True,
            }]),
        ],
        "subscope_law": {
            "approval_is_non_transitive": True,
            "every_subscope_must_be_named_by_decision": True,
            "no_implicit_cross_grant": True,
            "setup_and_cleanup_are_not_evidence": True,
        },
        "per_stage_reset_law": {
            "sequence": (
                [
                    "identity_provisioning",
                    "certification_classification_and_assignment",
                    "identity_baseline_verification",
                    "separate_ct_m0f_validation_admission",
                ]
                if profile == CONTROLLED_CERTIFICATION_SUBSTRATE_CT_M0F_ONE_USER_PROFILE
                else [
                    "stage_outcome",
                    "source_restoration",
                    "certification_identity_baseline_restoration",
                    "assignment_verification",
                    "new_incident_generation",
                    "fresh_controlled_condition",
                    "next_stage",
                ]
            ),
            "fresh_candidate_packet_lease_required": True,
            "packet_reuse_forbidden": True,
        },
        "verification_and_containment": {
            "per_user_verification_required": True,
            "aggregate_verification_required": True,
            "rollback_or_certified_no_rollback_required": True,
            "cohort_circuit_breaker_required": True,
            "final_safe_mode": "OPEN",
            "cleanup_and_retirement_required": True,
        },
        "kill_switch": {
            "owner": "existing autonomous execution control owner",
            "required": True,
            "stop_before_next_member_or_stage": True,
        },
        "forbidden_effects": [
            "ordinary_customer_reclassification",
            "ordinary_customer_movement_for_certification",
            "execution_only_target_use_outside_exact_controlled_campaign",
            "ordinary_production_eligibility_for_execution_only_target",
            "authority_self_expansion",
            "parallel_transactions_above_one",
            "packet_or_lease_reuse",
            "production_maturity_change",
            "natural_l8_claim",
        ],
        "reentry_condition": (
            "exact Authority decision admits or declines every coordinated subscope; "
            "on approval, the existing provisioning owner revalidates current "
            "registries before any write; CT-M0F Packet/lease/apply requires its "
            "separate existing one-use admission"
        ),
    }
    request_hash = controlled_certification_substrate_request_hash(request)
    request["request_hash"] = request_hash
    request["request_id"] = f"cpsauth_r1_{request_hash[:24]}"
    return request


def validate_controlled_certification_substrate_authority_request(
    request,
    *,
    decision="DECLINE",
    expected_request_id="",
    expected_request_hash="",
    now=None,
):
    now = now or utc_now()
    request = request if isinstance(request, dict) else {}
    errors = []
    request_id = str(request.get("request_id") or "")
    request_hash = str(request.get("request_hash") or "")
    if request.get("schema_version") != CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_SCHEMA:
        errors.append("controlled_certification_substrate_request_schema_invalid")
    if controlled_certification_substrate_request_hash(request) != request_hash:
        errors.append("controlled_certification_substrate_request_hash_mismatch")
    if request_id != f"cpsauth_r1_{request_hash[:24]}":
        errors.append("controlled_certification_substrate_request_identity_mismatch")
    if expected_request_id and request_id != expected_request_id:
        errors.append("controlled_certification_substrate_expected_request_mismatch")
    if expected_request_hash and request_hash != expected_request_hash:
        errors.append("controlled_certification_substrate_expected_hash_mismatch")
    if request.get("status") != "AWAITING_INDEPENDENT_ENGINEERING_AUTHORITY_DECISION":
        errors.append("controlled_certification_substrate_request_not_pending")
    try:
        if parse_ts(request.get("expires_at")) <= now:
            errors.append("controlled_certification_substrate_request_expired")
        if parse_ts(request.get("created_at")) > now:
            errors.append("controlled_certification_substrate_request_created_at_invalid")
    except PacketError:
        errors.append("controlled_certification_substrate_request_timestamps_invalid")
    if decision not in set(request.get("decision_set") or []):
        errors.append("controlled_certification_substrate_decision_not_allowed")
    if request.get("issuing_owner_required") != CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER:
        errors.append("controlled_certification_substrate_owner_invalid")
    scope = request.get("scope") if isinstance(request.get("scope"), dict) else {}
    profile = str(scope.get("profile") or CONTROLLED_CERTIFICATION_SUBSTRATE_TIER48_PROFILE)
    one_user = profile == CONTROLLED_CERTIFICATION_SUBSTRATE_CT_M0F_ONE_USER_PROFILE
    if profile not in {
        CONTROLLED_CERTIFICATION_SUBSTRATE_TIER48_PROFILE,
        CONTROLLED_CERTIFICATION_SUBSTRATE_CT_M0F_ONE_USER_PROFILE,
    }:
        errors.append("controlled_certification_substrate_profile_invalid")
    if as_int(scope.get("target_total_certification_identities"), 0) != (1 if one_user else 48):
        errors.append("controlled_certification_substrate_target_invalid")
    max_new = as_int(scope.get("max_new_certification_identities"), -1)
    identity_strategy = str(scope.get("identity_strategy") or "")
    if identity_strategy == "REUSE_EXISTING_VALID_POOL":
        if max_new != 0:
            errors.append(
                "controlled_certification_substrate_reuse_creation_ceiling_invalid"
            )
    elif identity_strategy == "PROVISION_INCREMENTAL_DELTA":
        if max_new < 0 or max_new > (1 if one_user else 48):
            errors.append(
                "controlled_certification_substrate_creation_ceiling_invalid"
            )
    elif max_new != (1 if one_user else 48):
        # Backward-compatible validation for requests emitted before the
        # explicit incremental/reuse strategy was introduced.
        errors.append("controlled_certification_substrate_creation_ceiling_invalid")
    if scope.get("certification_only") is not True or scope.get("ordinary_customer_involvement") is not False:
        errors.append("controlled_certification_substrate_identity_scope_invalid")
    if scope.get("campaign_stages") != ([1] if one_user else [5, 10, 25, 48]):
        errors.append("controlled_certification_substrate_campaign_invalid")
    if scope.get("automatic_stage_progression") is not (False if one_user else True):
        errors.append("controlled_certification_substrate_progression_invalid")
    if as_int(scope.get("max_concurrent_transactions"), 0) != 1:
        errors.append("controlled_certification_substrate_concurrency_invalid")
    controlled_target_id = str(scope.get("controlled_target_id") or "")
    target_contract = (
        request.get("controlled_target_contract")
        if isinstance(request.get("controlled_target_contract"), dict)
        else {}
    )
    if controlled_target_id:
        if (
            scope.get("controlled_target_admission_class")
            != "EXECUTION_ONLY_CONTROLLED_CERTIFICATION_TARGET"
            or str(target_contract.get("target_id") or "") != controlled_target_id
            or str(target_contract.get("role") or "").upper() != "EXECUTION_ONLY"
            or target_contract.get("reservation_owner")
            != "operator_execution_governance"
            or target_contract.get("execution_reserved") is not True
            or target_contract.get("canary_reserved") is not True
            or target_contract.get("autoswitch_allowed") is not False
            or target_contract.get("rebalance_allowed") is not False
            or target_contract.get("ordinary_production_assignment_allowed")
            is not False
            or target_contract.get("certification_only_assignment_allowed")
            is not True
            or target_contract.get("zero_user_at_request") is not True
            or target_contract.get("fresh_health_required_per_stage") is not True
            or target_contract.get("capacity_and_reserve_required_per_stage")
            is not True
            or target_contract.get("scope_lifetime")
            != "THIS_EXACT_CONTROLLED_CAMPAIGN_ONLY"
        ):
            errors.append(
                "controlled_certification_execution_only_target_contract_invalid"
            )
    subscopes = request.get("coordinated_subscopes")
    required_subscopes = (
        {"IDENTITY_PROVISIONING", "CERTIFICATION_CLASSIFICATION_AND_ASSIGNMENT"}
        if one_user else set(CONTROLLED_CERTIFICATION_SUBSTRATE_SUBSCOPES)
    )
    if not isinstance(subscopes, list) or {
        str(row.get("id") or "") for row in subscopes if isinstance(row, dict)
    } != required_subscopes:
        errors.append("controlled_certification_substrate_subscopes_invalid")
    law = request.get("subscope_law") if isinstance(request.get("subscope_law"), dict) else {}
    if (
        law.get("approval_is_non_transitive") is not True
        or law.get("every_subscope_must_be_named_by_decision") is not True
        or law.get("no_implicit_cross_grant") is not True
    ):
        errors.append("controlled_certification_substrate_subscope_law_invalid")
    semantic_fingerprint = str(request.get("semantic_request_fingerprint") or "")
    if (
        semantic_fingerprint
        and semantic_fingerprint
        != controlled_certification_substrate_semantic_fingerprint(request)
    ):
        errors.append("controlled_certification_substrate_semantic_fingerprint_invalid")
    supersession = (
        request.get("supersession")
        if isinstance(request.get("supersession"), dict)
        else {}
    )
    if supersession and (
        supersession.get("reason") != "EXPIRY_ONLY"
        or not supersession.get("supersedes_request_id")
        or len(str(supersession.get("supersedes_request_hash") or "")) != 64
        or supersession.get("semantic_request_fingerprint")
        != controlled_certification_substrate_semantic_fingerprint(request)
    ):
        errors.append("controlled_certification_substrate_supersession_invalid")
    return {
        "ok": not errors,
        "errors": sorted(set(errors)),
        "request_id": request_id,
        "request_hash": request_hash,
        "expires_at": str(request.get("expires_at") or ""),
    }


def _controlled_certification_substrate_request_records(records, request_id):
    return [
        record for record in (records if isinstance(records, list) else [])
        if record.get("record_type")
        == CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_RECORD_TYPE
        and str(record.get("authority_request_id") or "")
        == str(request_id or "")
    ]


def _controlled_certification_substrate_decision_records(records, request_id):
    return [
        record for record in (records if isinstance(records, list) else [])
        if record.get("record_type")
        == CONTROLLED_CERTIFICATION_SUBSTRATE_DECISION_RECORD_TYPE
        and str(record.get("authority_request_id") or "")
        == str(request_id or "")
    ]


def controlled_certification_substrate_request_from_audit(
    request_id,
    request_hash,
    *,
    audit_store=None,
    now=None,
):
    """Return one exact unexpired coordinated request from the Authority audit."""
    audit_store = Path(
        audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE
    )
    matches = _controlled_certification_substrate_request_records(
        read_audit_records(audit_store), request_id,
    )
    if len(matches) != 1:
        raise PacketError(
            "controlled_certification_substrate_request_audit_missing_or_duplicate"
        )
    record = matches[0]
    request = (
        record.get("request") if isinstance(record.get("request"), dict) else {}
    )
    if str(record.get("authority_request_hash") or "") != str(request_hash or ""):
        raise PacketError(
            "controlled_certification_substrate_request_audit_hash_mismatch"
        )
    validation = validate_controlled_certification_substrate_authority_request(
        request,
        decision="DECLINE",
        expected_request_id=request_id,
        expected_request_hash=request_hash,
        now=now or utc_now(),
    )
    if not validation.get("ok"):
        raise PacketError(",".join(
            validation.get("errors")
            or ["controlled_certification_substrate_request_audit_invalid"]
        ))
    return request


def controlled_certification_substrate_authority_status(records, *, now=None):
    """Project the exact request/decision lifecycle without creating new truth."""
    now = now or utc_now()
    records = records if isinstance(records, list) else []
    requests = [
        record for record in records
        if record.get("record_type")
        == CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_RECORD_TYPE
    ]
    requests.sort(key=lambda row: (
        str(((row.get("request") or {}).get("created_at")) or ""),
        str(row.get("authority_request_id") or ""),
    ))
    if not requests:
        return {
            "status": "NONE",
            "request_id": "",
            "request_hash": "",
            "decision": "",
            "decision_id": "",
            "expires_at": "",
            "semantic_request_fingerprint": "",
        }
    record = requests[-1]
    request = (
        record.get("request") if isinstance(record.get("request"), dict) else {}
    )
    request_id = str(request.get("request_id") or "")
    decisions = _controlled_certification_substrate_decision_records(
        records, request_id,
    )
    validation = validate_controlled_certification_substrate_authority_request(
        request,
        decision="DECLINE",
        expected_request_id=request_id,
        expected_request_hash=str(record.get("authority_request_hash") or ""),
        now=now,
    )
    non_expiry_errors = [
        error for error in (validation.get("errors") or [])
        if error != "controlled_certification_substrate_request_expired"
    ]
    if non_expiry_errors:
        status = "STOP_SAFE_INVALID_REQUEST"
        decision = {}
    elif len(decisions) > 1:
        status = "STOP_SAFE_DUPLICATE_OR_CONFLICTING_DECISIONS"
        decision = {}
    elif decisions:
        decision = decisions[0]
        status = (
            "APPROVED"
            if decision.get("decision")
            == CONTROLLED_CERTIFICATION_SUBSTRATE_APPROVAL
            else "DECLINED"
        )
    else:
        decision = {}
        try:
            status = (
                "EXPIRED"
                if parse_ts(request.get("expires_at")) <= now
                else "PENDING"
            )
        except PacketError:
            status = "STOP_SAFE_INVALID_REQUEST_EXPIRY"
    return {
        "status": status,
        "request_id": request_id,
        "request_hash": str(request.get("request_hash") or ""),
        "created_at": str(request.get("created_at") or ""),
        "expires_at": str(request.get("expires_at") or ""),
        "semantic_request_fingerprint": (
            controlled_certification_substrate_semantic_fingerprint(request)
        ),
        "decision": str(decision.get("decision") or ""),
        "decision_id": str(decision.get("decision_id") or ""),
        "actor_id": str(
            ((decision.get("actor_provenance") or {}).get("actor_id")) or ""
        ),
        "admitted_subscopes": list(decision.get("admitted_subscopes") or []),
        "request": copy.deepcopy(request),
    }


def record_controlled_certification_substrate_authority_decision(
    *,
    request_id,
    request_hash,
    decision,
    actor_id,
    admitted_subscopes=None,
    audit_store=None,
    now=None,
):
    """Append one exact independent decision; never provision or execute."""
    now = now or utc_now()
    if decision not in {CONTROLLED_CERTIFICATION_SUBSTRATE_APPROVAL, "DECLINE"}:
        raise PacketError(
            "controlled_certification_substrate_decision_not_exact"
        )
    if not str(actor_id or "").strip():
        raise PacketError(
            "controlled_certification_substrate_authority_actor_missing"
        )
    admitted = sorted(set(str(item) for item in (admitted_subscopes or [])))
    if decision != CONTROLLED_CERTIFICATION_SUBSTRATE_APPROVAL and admitted:
        raise PacketError(
            "controlled_certification_substrate_decline_admits_subscopes"
        )
    audit_store = Path(
        audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE
    )
    with current_action_class_contract_policy_lock(audit_store):
        records = read_audit_records(audit_store)
        existing = _controlled_certification_substrate_decision_records(
            records, request_id,
        )
        decision_id = stable_id("cpsdec", {
            "request_id": request_id,
            "request_hash": request_hash,
            "decision": decision,
            "actor_id": str(actor_id),
            "admitted_subscopes": admitted,
        })
        if existing:
            exact = [
                row for row in existing
                if row.get("decision_id") == decision_id
                and row.get("authority_request_hash") == request_hash
                and row.get("decision") == decision
                and sorted(row.get("admitted_subscopes") or []) == admitted
                and str(
                    ((row.get("actor_provenance") or {}).get("actor_id")) or ""
                ) == str(actor_id)
            ]
            if len(existing) == 1 and len(exact) == 1:
                return {
                    "status": "ALREADY_RECORDED_EXACT",
                    "request_id": request_id,
                    "request_hash": request_hash,
                    "decision": decision,
                    "decision_id": decision_id,
                    "audit_write": False,
                    "policy_write": False,
                    "runtime_apply": False,
                    "routing_mutation": False,
                    "users_moved": 0,
                }
            raise PacketError(
                "controlled_certification_substrate_authority_decision_conflict"
            )
        request = controlled_certification_substrate_request_from_audit(
            request_id,
            request_hash,
            audit_store=audit_store,
            now=now,
        )
        expected = sorted(
            str(row.get("id") or "")
            for row in (request.get("coordinated_subscopes") or [])
            if isinstance(row, dict)
        )
        if decision == CONTROLLED_CERTIFICATION_SUBSTRATE_APPROVAL and admitted != expected:
            raise PacketError(
                "controlled_certification_substrate_approval_subscopes_incomplete"
            )
        validation = validate_controlled_certification_substrate_authority_request(
            request,
            decision=decision,
            expected_request_id=request_id,
            expected_request_hash=request_hash,
            now=now,
        )
        if not validation.get("ok"):
            raise PacketError(",".join(
                validation.get("errors")
                or ["controlled_certification_substrate_decision_invalid"]
            ))
        record = append_record(audit_store, {
            "schema_version": (
                "v7.controlled-certification-substrate-authority-decision.v1"
            ),
            "record_type": (
                CONTROLLED_CERTIFICATION_SUBSTRATE_DECISION_RECORD_TYPE
            ),
            "decision_id": decision_id,
            "authority_request_id": request_id,
            "authority_request_hash": request_hash,
            "semantic_request_fingerprint": (
                controlled_certification_substrate_semantic_fingerprint(request)
            ),
            "decision": decision,
            "admitted_subscopes": admitted,
            "actor_provenance": {
                "actor_id": str(actor_id),
                "decision_surface": "tools/v7-operator-execution-packet",
                "issuing_owner": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
                "recorded_at": now.isoformat(),
            },
            "created_at": now.isoformat(),
        })
    return {
        "status": "APPROVED" if decision == CONTROLLED_CERTIFICATION_SUBSTRATE_APPROVAL else "DECLINED",
        "request_id": request_id,
        "request_hash": request_hash,
        "decision": decision,
        "decision_id": record["decision_id"],
        "admitted_subscopes": admitted,
        "next_required_consumer": (
            "existing T48-M8 controlled substrate owner"
            if decision == CONTROLLED_CERTIFICATION_SUBSTRATE_APPROVAL
            else "existing CPS/OMP residual reconciliation owner"
        ),
        "audit_write": True,
        "policy_write": False,
        "registry_write": False,
        "identity_creation": False,
        "assignment_change": False,
        "controlled_condition": False,
        "candidate_created": False,
        "packet_created": False,
        "lease_created": False,
        "runtime_apply": False,
        "routing_mutation": False,
        "users_moved": 0,
        "rollback_apply": False,
        "authority_self_expansion": False,
        "production_maturity_change": False,
    }


def build_expiry_replacement_controlled_certification_substrate_request(
    request,
    *,
    now=None,
):
    """Create one semantic replacement only after the prior request expires."""
    now = now or utc_now()
    request = copy.deepcopy(request if isinstance(request, dict) else {})
    try:
        if parse_ts(request.get("expires_at")) > now:
            raise PacketError(
                "controlled_certification_substrate_request_not_expired"
            )
    except PacketError as exc:
        if str(exc) == "controlled_certification_substrate_request_not_expired":
            raise
        raise PacketError(
            "controlled_certification_substrate_request_expiry_invalid"
        )
    old_id = str(request.get("request_id") or "")
    old_hash = str(request.get("request_hash") or "")
    semantic = controlled_certification_substrate_semantic_fingerprint(request)
    request.pop("request_id", None)
    request.pop("request_hash", None)
    request["created_at"] = now.isoformat()
    request["expires_at"] = (
        now + timedelta(
            seconds=CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_TTL_SECONDS
        )
    ).isoformat()
    request["semantic_request_fingerprint"] = semantic
    request["supersession"] = {
        "reason": "EXPIRY_ONLY",
        "supersedes_request_id": old_id,
        "supersedes_request_hash": old_hash,
        "semantic_request_fingerprint": semantic,
    }
    request_hash = controlled_certification_substrate_request_hash(request)
    request["request_hash"] = request_hash
    request["request_id"] = f"cpsauth_r1_{request_hash[:24]}"
    return request


def replace_expired_controlled_certification_substrate_request(
    *,
    request_id,
    request_hash,
    audit_store=None,
    producer_id="tools/v7-operator-execution-packet",
    now=None,
):
    """Supersede one expired undecided request without creating two active ones."""
    now = now or utc_now()
    audit_store = Path(
        audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE
    )
    with current_action_class_contract_policy_lock(audit_store):
        records = read_audit_records(audit_store)
        if _controlled_certification_substrate_decision_records(
            records, request_id,
        ):
            raise PacketError(
                "controlled_certification_substrate_expired_request_decided"
            )
        matches = _controlled_certification_substrate_request_records(
            records, request_id,
        )
        if len(matches) != 1:
            raise PacketError(
                "controlled_certification_substrate_request_audit_missing_or_duplicate"
            )
        old_request = (
            matches[0].get("request")
            if isinstance(matches[0].get("request"), dict)
            else {}
        )
        if (
            str(matches[0].get("authority_request_hash") or "")
            != str(request_hash or "")
            or str(old_request.get("request_hash") or "")
            != str(request_hash or "")
        ):
            raise PacketError(
                "controlled_certification_substrate_request_audit_hash_mismatch"
            )
        replacement = (
            build_expiry_replacement_controlled_certification_substrate_request(
                old_request,
                now=now,
            )
        )
        registration = (
            register_controlled_certification_substrate_authority_request(
                replacement,
                audit_store=audit_store,
                producer_id=producer_id,
                now=now,
            )
        )
    return {
        "status": "EXPIRY_REPLACEMENT_REGISTERED",
        "request": replacement,
        "registration": registration,
        "supersedes_request_id": request_id,
        "supersedes_request_hash": request_hash,
        "semantic_request_fingerprint": (
            controlled_certification_substrate_semantic_fingerprint(replacement)
        ),
        "authority_granted": False,
        "policy_write": False,
        "registry_write": False,
        "runtime_apply": False,
        "routing_mutation": False,
        "users_moved": 0,
    }


def register_controlled_certification_substrate_authority_request(
    request,
    *,
    audit_store=None,
    producer_id="tools/v7-users-autoswitch",
    now=None,
):
    """Append the exact request preimage through the existing Authority audit."""
    now = now or utc_now()
    validation = validate_controlled_certification_substrate_authority_request(
        request,
        decision="DECLINE",
        now=now,
    )
    if not validation.get("ok"):
        raise PacketError(",".join(
            validation.get("errors")
            or ["controlled_certification_substrate_request_invalid"]
        ))
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    records = read_audit_records(audit_store)
    existing = [
        record for record in records
        if record.get("record_type") == CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_RECORD_TYPE
        and str(record.get("authority_request_id") or "") == request["request_id"]
    ]
    if existing:
        if (
            len(existing) != 1
            or existing[0].get("authority_request_hash") != request["request_hash"]
            or existing[0].get("request") != request
        ):
            raise PacketError("controlled_certification_substrate_request_audit_identity_conflict")
        return {
            "status": "ALREADY_REGISTERED_EXACT",
            "request_id": request["request_id"],
            "request_hash": request["request_hash"],
            "audit_store": str(audit_store),
            "audit_write": False,
        }
    semantic = controlled_certification_substrate_semantic_fingerprint(request)
    decided_ids = {
        str(record.get("authority_request_id") or "")
        for record in records
        if record.get("record_type")
        == CONTROLLED_CERTIFICATION_SUBSTRATE_DECISION_RECORD_TYPE
    }
    for record in records:
        if (
            record.get("record_type")
            != CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_RECORD_TYPE
        ):
            continue
        prior = (
            record.get("request")
            if isinstance(record.get("request"), dict)
            else {}
        )
        prior_id = str(prior.get("request_id") or "")
        if not prior_id or prior_id in decided_ids:
            continue
        try:
            prior_active = parse_ts(prior.get("expires_at")) > now
        except PacketError:
            prior_active = False
        if (
            prior_active
            and controlled_certification_substrate_semantic_fingerprint(prior)
            == semantic
        ):
            raise PacketError(
                "controlled_certification_substrate_active_semantic_request_exists"
            )
    append_record(audit_store, {
        "schema_version": "v7.controlled-certification-substrate-authority-audit.v1",
        "record_type": CONTROLLED_CERTIFICATION_SUBSTRATE_REQUEST_RECORD_TYPE,
        "authority_request_id": request["request_id"],
        "authority_request_hash": request["request_hash"],
        "request": copy.deepcopy(request),
        "producer": str(producer_id or "tools/v7-users-autoswitch"),
        "created_at": now.isoformat(),
    })
    return {
        "status": "REGISTERED",
        "request_id": request["request_id"],
        "request_hash": request["request_hash"],
        "audit_store": str(audit_store),
        "audit_write": True,
    }


def controlled_source_topology_request_hash(request):
    canonical = copy.deepcopy(request if isinstance(request, dict) else {})
    canonical.pop("request_id", None)
    canonical.pop("request_hash", None)
    return sha256_json(canonical)


def controlled_source_topology_semantic_fingerprint(request):
    """Stable identity for duplicate suppression across expiry-only requests."""
    canonical = copy.deepcopy(request if isinstance(request, dict) else {})
    for key in (
        "request_id",
        "request_hash",
        "created_at",
        "expires_at",
        "semantic_request_fingerprint",
        "supersession",
    ):
        canonical.pop(key, None)
    return sha256_json(canonical)


def build_controlled_source_topology_authority_request(
    request_payload,
    *,
    now=None,
):
    """Bind one exact source-topology preflight to the existing Authority owner.

    This only constructs an independently decidable request.  It cannot reserve
    an egress, change assignments, create execution artifacts or grant campaign
    Authority.
    """
    now = now or utc_now()
    payload = copy.deepcopy(
        request_payload if isinstance(request_payload, dict) else {}
    )
    for key in (
        "request_id",
        "request_hash",
        "created_at",
        "expires_at",
        "semantic_request_fingerprint",
        "registered",
        "registration_reason",
        "actionable",
        "authority_lifecycle",
    ):
        payload.pop(key, None)
    payload.update({
        "schema_version": CONTROLLED_SOURCE_TOPOLOGY_REQUEST_SCHEMA,
        "status": "AWAITING_INDEPENDENT_ENGINEERING_AUTHORITY_DECISION",
        "created_at": now.isoformat(),
        "expires_at": (
            now
            + timedelta(seconds=CONTROLLED_SOURCE_TOPOLOGY_REQUEST_TTL_SECONDS)
        ).isoformat(),
        "issuing_owner_required": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
    })
    exact_action = str(payload.get("exact_action") or "")
    payload["decision_set"] = [
        f"APPROVE_{exact_action}" if exact_action else "",
        "DECLINE",
    ]
    request_hash = controlled_source_topology_request_hash(payload)
    payload["request_hash"] = request_hash
    payload["request_id"] = f"cstopauth_r1_{request_hash[:24]}"
    return payload


def validate_controlled_source_topology_authority_request(
    request,
    *,
    decision="DECLINE",
    expected_request_id="",
    expected_request_hash="",
    now=None,
):
    """Fail closed unless the request is one exact one-identity topology setup."""
    now = now or utc_now()
    request = request if isinstance(request, dict) else {}
    errors = []
    request_id = str(request.get("request_id") or "")
    request_hash = str(request.get("request_hash") or "")
    exact_action = str(request.get("exact_action") or "")
    approval = f"APPROVE_{exact_action}" if exact_action else ""
    if request.get("schema_version") != CONTROLLED_SOURCE_TOPOLOGY_REQUEST_SCHEMA:
        errors.append("controlled_source_topology_request_schema_invalid")
    if controlled_source_topology_request_hash(request) != request_hash:
        errors.append("controlled_source_topology_request_hash_mismatch")
    if request_id != f"cstopauth_r1_{request_hash[:24]}":
        errors.append("controlled_source_topology_request_identity_mismatch")
    if expected_request_id and request_id != str(expected_request_id):
        errors.append("controlled_source_topology_expected_request_mismatch")
    if expected_request_hash and request_hash != str(expected_request_hash):
        errors.append("controlled_source_topology_expected_hash_mismatch")
    if (
        request.get("status")
        != "AWAITING_INDEPENDENT_ENGINEERING_AUTHORITY_DECISION"
    ):
        errors.append("controlled_source_topology_request_not_pending")
    try:
        if parse_ts(request.get("expires_at")) <= now:
            errors.append("controlled_source_topology_request_expired")
        if parse_ts(request.get("created_at")) > now:
            errors.append("controlled_source_topology_created_at_invalid")
    except PacketError:
        errors.append("controlled_source_topology_timestamps_invalid")
    if exact_action not in CONTROLLED_SOURCE_TOPOLOGY_ACTIONS:
        errors.append("controlled_source_topology_action_invalid")
    if request.get("decision_set") != [approval, "DECLINE"]:
        errors.append("controlled_source_topology_decision_set_invalid")
    if decision not in set(request.get("decision_set") or []):
        errors.append("controlled_source_topology_decision_not_allowed")
    if (
        request.get("issuing_owner_required")
        != CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER
    ):
        errors.append("controlled_source_topology_owner_invalid")
    if (
        request.get("active_program")
        != "V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1"
        or request.get("mission")
        != (
            "CONTROLLED_SOURCE_RESELECTION_PROVISIONING_AND_"
            "SLICE_FEASIBILITY_V1"
        )
    ):
        errors.append("controlled_source_topology_program_binding_invalid")
    if request.get("tier48_capability_or_campaign_reapproval") is not False:
        errors.append("controlled_source_topology_campaign_reapproval_forbidden")
    if (
        request.get("ordinary_customer_involvement") is not False
        or request.get("self_expansion_allowed") is not False
    ):
        errors.append("controlled_source_topology_scope_invalid")
    manifest = (
        request.get("manifest")
        if isinstance(request.get("manifest"), dict)
        else {}
    )
    authority_basis = (
        request.get("authority_basis")
        if isinstance(request.get("authority_basis"), dict)
        else {}
    )
    if authority_basis.get("kind") == "CT_M0F_STANDING_VALIDATION_POLICY":
        if (
            not str(authority_basis.get("contract_id") or "")
            or len(str(authority_basis.get("contract_hash") or "")) != 64
            or not str(authority_basis.get("authority_request_id") or "")
            or len(str(authority_basis.get("authority_request_hash") or "")) != 64
            or not str(authority_basis.get("expires_at") or "")
        ):
            errors.append("controlled_source_topology_ct_m0f_basis_invalid")
        if manifest.get("validation_profile") != "CT_M0F_ONE_USER_CONTROLLED_CONDITION":
            errors.append("controlled_source_topology_ct_m0f_profile_invalid")
    else:
        if not str(request.get("current_campaign_request_id") or ""):
            errors.append("controlled_source_topology_campaign_request_missing")
        if len(str(request.get("current_campaign_request_hash") or "")) != 64:
            errors.append("controlled_source_topology_campaign_hash_invalid")
    manifest_hash = str(manifest.get("manifest_hash") or "")
    manifest_preimage = copy.deepcopy(manifest)
    manifest_preimage.pop("manifest_hash", None)
    if not manifest or sha256_json(manifest_preimage) != manifest_hash:
        errors.append("controlled_source_topology_manifest_hash_invalid")
    if (
        int(manifest.get("trial_identity_count") or 0) != 1
        or not str(manifest.get("trial_identity") or "")
        or int(manifest.get("capacity_reservation") or 0) != 1
        or int(manifest.get("max_concurrent_transactions") or 0) != 1
    ):
        errors.append("controlled_source_topology_trial_scope_invalid")
    if (
        manifest.get("expected_ordinary_assignment_delta") != "NONE"
        or manifest.get("expected_ordinary_route_delta") != "NONE"
    ):
        errors.append("controlled_source_topology_ordinary_delta_invalid")
    if (
        manifest.get("lease_and_expiry_required") is not True
        or manifest.get("packet_required_before_effect") is not True
        or manifest.get("restore_barrier_required_before_effect") is not True
        or not str(manifest.get("verification") or "")
        or not str(manifest.get("rollback") or "")
    ):
        errors.append("controlled_source_topology_safety_contract_invalid")
    existing_source = str(manifest.get("existing_source") or "")
    selected_resource = str(manifest.get("selected_source_or_draft") or "")
    if not existing_source or not selected_resource:
        errors.append("controlled_source_topology_resource_binding_missing")
    if (
        exact_action == "REBIND_CONTROLLED_CERTIFICATION_SOURCE"
        and existing_source == selected_resource
    ):
        errors.append("controlled_source_topology_rebind_same_source")
    semantic_fingerprint = str(
        request.get("semantic_request_fingerprint") or ""
    )
    if (
        semantic_fingerprint
        and semantic_fingerprint
        != controlled_source_topology_semantic_fingerprint(request)
    ):
        errors.append("controlled_source_topology_semantic_fingerprint_invalid")
    return {
        "ok": not errors,
        "errors": sorted(set(errors)),
        "request_id": request_id,
        "request_hash": request_hash,
        "expires_at": str(request.get("expires_at") or ""),
        "approval_decision": approval,
    }


def _controlled_source_topology_request_records(records, request_id):
    return [
        record for record in (records if isinstance(records, list) else [])
        if record.get("record_type")
        == CONTROLLED_SOURCE_TOPOLOGY_REQUEST_RECORD_TYPE
        and str(record.get("authority_request_id") or "")
        == str(request_id or "")
    ]


def _controlled_source_topology_decision_records(records, request_id):
    return [
        record for record in (records if isinstance(records, list) else [])
        if record.get("record_type")
        == CONTROLLED_SOURCE_TOPOLOGY_DECISION_RECORD_TYPE
        and str(record.get("authority_request_id") or "")
        == str(request_id or "")
    ]


def _controlled_source_topology_invalidation_records(records, request_id):
    return [
        record for record in (records if isinstance(records, list) else [])
        if record.get("record_type")
        == CONTROLLED_SOURCE_TOPOLOGY_INVALIDATION_RECORD_TYPE
        and str(record.get("authority_request_id") or "")
        == str(request_id or "")
    ]


def controlled_source_topology_authority_status(records, *, now=None):
    """Project the newest exact topology request/decision from the same audit."""
    now = now or utc_now()
    records = records if isinstance(records, list) else []
    requests = [
        record for record in records
        if record.get("record_type")
        == CONTROLLED_SOURCE_TOPOLOGY_REQUEST_RECORD_TYPE
    ]
    requests.sort(key=lambda row: (
        str(((row.get("request") or {}).get("created_at")) or ""),
        str(row.get("authority_request_id") or ""),
    ))
    if not requests:
        return {
            "status": "NONE",
            "request_id": "",
            "request_hash": "",
            "decision": "",
            "decision_id": "",
            "request": {},
        }
    record = requests[-1]
    request = (
        record.get("request")
        if isinstance(record.get("request"), dict)
        else {}
    )
    request_id = str(request.get("request_id") or "")
    decisions = _controlled_source_topology_decision_records(
        records, request_id,
    )
    invalidations = _controlled_source_topology_invalidation_records(
        records, request_id,
    )
    validation = validate_controlled_source_topology_authority_request(
        request,
        decision="DECLINE",
        expected_request_id=request_id,
        expected_request_hash=str(record.get("authority_request_hash") or ""),
        now=now,
    )
    non_expiry_errors = [
        error for error in (validation.get("errors") or [])
        if error != "controlled_source_topology_request_expired"
    ]
    decision_record = decisions[0] if len(decisions) == 1 else {}
    try:
        request_expired = parse_ts(request.get("expires_at")) <= now
    except PacketError:
        request_expired = False
    if len(invalidations) > 1:
        status = "STOP_SAFE_DUPLICATE_REQUEST_INVALIDATIONS"
    elif invalidations:
        status = "SUPERSEDED_STALE_PREFLIGHT"
    elif non_expiry_errors:
        status = "STOP_SAFE_INVALID_REQUEST"
    elif request_expired:
        # An approval is bound to the same one-use request TTL.  Retaining an
        # old decision as APPROVED after that TTL would let a topology consumer
        # reserve a source with an already-expired authority boundary.
        status = "EXPIRED"
    elif len(decisions) > 1:
        status = "STOP_SAFE_DUPLICATE_OR_CONFLICTING_DECISIONS"
    elif decisions:
        status = (
            "APPROVED"
            if str(decision_record.get("decision") or "").startswith(
                "APPROVE_"
            )
            else "DECLINED"
        )
    else:
        try:
            status = (
                "EXPIRED"
                if parse_ts(request.get("expires_at")) <= now
                else "PENDING"
            )
        except PacketError:
            status = "STOP_SAFE_INVALID_REQUEST_EXPIRY"
    return {
        "status": status,
        "request_id": request_id,
        "request_hash": str(request.get("request_hash") or ""),
        "created_at": str(request.get("created_at") or ""),
        "expires_at": str(request.get("expires_at") or ""),
        "semantic_request_fingerprint": (
            controlled_source_topology_semantic_fingerprint(request)
        ),
        "decision": str(decision_record.get("decision") or ""),
        "decision_id": str(decision_record.get("decision_id") or ""),
        "actor_id": str(
            ((decision_record.get("actor_provenance") or {}).get("actor_id"))
            or ""
        ),
        "invalidation_id": str(
            (invalidations[0].get("invalidation_id") if invalidations else "")
            or ""
        ),
        "invalidation_reason": str(
            (
                invalidations[0].get("reason")
                if invalidations else ""
            )
            or ""
        ),
        "request": copy.deepcopy(request),
    }


def register_controlled_source_topology_authority_request(
    request,
    *,
    audit_store=None,
    producer_id="tools/v7-users-autoswitch",
    now=None,
):
    """Persist one request in the existing append-only owner, exact-once."""
    now = now or utc_now()
    validation = validate_controlled_source_topology_authority_request(
        request,
        decision="DECLINE",
        now=now,
    )
    if not validation.get("ok"):
        raise PacketError(",".join(
            validation.get("errors")
            or ["controlled_source_topology_request_invalid"]
        ))
    audit_store = Path(
        audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE
    )
    with current_action_class_contract_policy_lock(audit_store):
        records = read_audit_records(audit_store)
        existing = _controlled_source_topology_request_records(
            records, request["request_id"],
        )
        if existing:
            if (
                len(existing) != 1
                or existing[0].get("authority_request_hash")
                != request["request_hash"]
                or existing[0].get("request") != request
            ):
                raise PacketError(
                    "controlled_source_topology_request_audit_identity_conflict"
                )
            return {
                "status": "ALREADY_REGISTERED_EXACT",
                "request_id": request["request_id"],
                "request_hash": request["request_hash"],
                "audit_store": str(audit_store),
                "audit_write": False,
            }
        semantic = controlled_source_topology_semantic_fingerprint(request)
        decided_ids = {
            str(record.get("authority_request_id") or "")
            for record in records
            if record.get("record_type")
            == CONTROLLED_SOURCE_TOPOLOGY_DECISION_RECORD_TYPE
        }
        invalidated_ids = {
            str(record.get("authority_request_id") or "")
            for record in records
            if record.get("record_type")
            == CONTROLLED_SOURCE_TOPOLOGY_INVALIDATION_RECORD_TYPE
        }
        invalidated_requests = []
        for record in records:
            if (
                record.get("record_type")
                != CONTROLLED_SOURCE_TOPOLOGY_REQUEST_RECORD_TYPE
            ):
                continue
            prior = (
                record.get("request")
                if isinstance(record.get("request"), dict)
                else {}
            )
            prior_id = str(prior.get("request_id") or "")
            if (
                not prior_id
                or prior_id in decided_ids
                or prior_id in invalidated_ids
            ):
                continue
            try:
                prior_active = parse_ts(prior.get("expires_at")) > now
            except PacketError:
                prior_active = False
            if (
                prior_active
                and controlled_source_topology_semantic_fingerprint(prior)
                == semantic
            ):
                return {
                    "status": "ALREADY_REGISTERED_SEMANTIC_ACTIVE",
                    "request_id": prior_id,
                    "request_hash": str(prior.get("request_hash") or ""),
                    "audit_store": str(audit_store),
                    "audit_write": False,
                    "request": copy.deepcopy(prior),
                }
            if prior_active:
                invalidation_id = stable_id("cstopinv", {
                    "authority_request_id": prior_id,
                    "authority_request_hash": str(
                        prior.get("request_hash") or ""
                    ),
                    "replacement_request_id": request["request_id"],
                    "replacement_request_hash": request["request_hash"],
                    "reason": "MATERIAL_PREFLIGHT_CHANGED",
                })
                append_record(audit_store, {
                    "schema_version": (
                        "v7.controlled-source-topology-authority-"
                        "invalidation.v1"
                    ),
                    "record_type": (
                        CONTROLLED_SOURCE_TOPOLOGY_INVALIDATION_RECORD_TYPE
                    ),
                    "invalidation_id": invalidation_id,
                    "authority_request_id": prior_id,
                    "authority_request_hash": str(
                        prior.get("request_hash") or ""
                    ),
                    "replacement_request_id": request["request_id"],
                    "replacement_request_hash": request["request_hash"],
                    "reason": "MATERIAL_PREFLIGHT_CHANGED",
                    "producer": str(
                        producer_id or "tools/v7-users-autoswitch"
                    ),
                    "created_at": now.isoformat(),
                    "authority_decision": False,
                    "topology_materialized": False,
                    "runtime_apply": False,
                    "routing_mutation": False,
                    "users_moved": 0,
                })
                invalidated_ids.add(prior_id)
                invalidated_requests.append({
                    "request_id": prior_id,
                    "request_hash": str(prior.get("request_hash") or ""),
                    "invalidation_id": invalidation_id,
                    "reason": "MATERIAL_PREFLIGHT_CHANGED",
                })
        append_record(audit_store, {
            "schema_version": (
                "v7.controlled-source-topology-authority-audit.v1"
            ),
            "record_type": CONTROLLED_SOURCE_TOPOLOGY_REQUEST_RECORD_TYPE,
            "authority_request_id": request["request_id"],
            "authority_request_hash": request["request_hash"],
            "request": copy.deepcopy(request),
            "producer": str(producer_id or "tools/v7-users-autoswitch"),
            "created_at": now.isoformat(),
        })
    return {
        "status": (
            "REGISTERED_AFTER_STALE_PREFLIGHT_INVALIDATION"
            if invalidated_requests else "REGISTERED"
        ),
        "request_id": request["request_id"],
        "request_hash": request["request_hash"],
        "audit_store": str(audit_store),
        "audit_write": True,
        "invalidated_requests": invalidated_requests,
        "request": copy.deepcopy(request),
    }


def invalidate_released_controlled_source_topology_request(
    *,
    request_id,
    request_hash,
    source_id,
    release_snapshot,
    audit_store=None,
    now=None,
):
    """Close one consumed topology request after its source was owner-released.

    This does not reserve, create, assign, or execute.  It only records that
    the source has returned to an exact empty/unreserved state, making the old
    one-use request permanently unavailable and permitting a later *fresh*
    request through the same Authority owner.
    """
    now = now or utc_now()
    source_id = str(source_id or "")
    snapshot = release_snapshot if isinstance(release_snapshot, dict) else {}
    required = {
        "source_id": source_id,
        "source_exists": True,
        "reservation_absent": True,
        "controlled_source_markers_absent": True,
        "assigned_user_count": 0,
        "snapshot_fingerprint": str(snapshot.get("snapshot_fingerprint") or ""),
    }
    if not source_id or not required["snapshot_fingerprint"]:
        raise PacketError("controlled_source_topology_release_snapshot_invalid")
    for key, expected in required.items():
        if snapshot.get(key) != expected:
            raise PacketError("controlled_source_topology_release_snapshot_invalid")
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    with current_action_class_contract_policy_lock(audit_store):
        records = read_audit_records(audit_store)
        invalidation_id = stable_id("cstopinv", {
            "authority_request_id": str(request_id),
            "authority_request_hash": str(request_hash),
            "source_id": source_id,
            "release_snapshot_fingerprint": required["snapshot_fingerprint"],
            "reason": "OWNER_OBSERVED_RELEASED_RESERVATION_REENTRY",
        })
        existing = _controlled_source_topology_invalidation_records(records, request_id)
        if existing:
            exact = [row for row in existing if row.get("invalidation_id") == invalidation_id]
            if len(existing) == 1 and len(exact) == 1:
                return {"status": "ALREADY_INVALIDATED_EXACT", "invalidation_id": invalidation_id, "audit_write": False}
            raise PacketError("controlled_source_topology_release_invalidation_conflict")
        request = controlled_source_topology_request_from_audit(
            request_id, request_hash, audit_store=audit_store, now=now,
        )
        decisions = _controlled_source_topology_decision_records(records, request_id)
        provisions = [
            row for row in records
            if row.get("record_type") == CONTROLLED_SOURCE_TOPOLOGY_PROVISION_RECORD_TYPE
            and str(row.get("authority_request_id") or "") == str(request_id)
            and str(row.get("authority_request_hash") or "") == str(request_hash)
            and str(row.get("source_id") or "") == source_id
        ]
        approved = [
            row for row in decisions
            if str(row.get("authority_request_hash") or "") == str(request_hash)
            and str(row.get("decision") or "") == f"APPROVE_{request.get('exact_action') or ''}"
        ]
        if len(approved) != 1 or len(provisions) != 1:
            raise PacketError("controlled_source_topology_release_predecessor_missing")
        append_record(audit_store, {
            "schema_version": "v7.controlled-source-topology-authority-invalidation.v1",
            "record_type": CONTROLLED_SOURCE_TOPOLOGY_INVALIDATION_RECORD_TYPE,
            "invalidation_id": invalidation_id,
            "authority_request_id": str(request_id),
            "authority_request_hash": str(request_hash),
            "reason": "OWNER_OBSERVED_RELEASED_RESERVATION_REENTRY",
            "source_id": source_id,
            "release_snapshot_fingerprint": required["snapshot_fingerprint"],
            "producer": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
            "created_at": now.isoformat(),
            "authority_decision": False,
            "topology_materialized": False,
            "runtime_apply": False,
            "routing_mutation": False,
            "users_moved": 0,
        })
    return {"status": "INVALIDATED_RELEASED_PREDECESSOR", "invalidation_id": invalidation_id, "audit_write": True}


def controlled_source_topology_request_from_audit(
    request_id,
    request_hash,
    *,
    audit_store=None,
    now=None,
):
    audit_store = Path(
        audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE
    )
    matches = _controlled_source_topology_request_records(
        read_audit_records(audit_store), request_id,
    )
    if len(matches) != 1:
        raise PacketError(
            "controlled_source_topology_request_audit_missing_or_duplicate"
        )
    record = matches[0]
    invalidations = _controlled_source_topology_invalidation_records(
        read_audit_records(audit_store), request_id,
    )
    if invalidations:
        raise PacketError(
            "controlled_source_topology_request_superseded_stale_preflight"
        )
    request = (
        record.get("request")
        if isinstance(record.get("request"), dict)
        else {}
    )
    if str(record.get("authority_request_hash") or "") != str(request_hash or ""):
        raise PacketError(
            "controlled_source_topology_request_audit_hash_mismatch"
        )
    validation = validate_controlled_source_topology_authority_request(
        request,
        decision="DECLINE",
        expected_request_id=request_id,
        expected_request_hash=request_hash,
        now=now or utc_now(),
    )
    if not validation.get("ok"):
        raise PacketError(",".join(
            validation.get("errors")
            or ["controlled_source_topology_request_audit_invalid"]
        ))
    return request


def record_controlled_source_topology_authority_decision(
    *,
    request_id,
    request_hash,
    decision,
    actor_id,
    audit_store=None,
    now=None,
):
    """Append one exact decision; never materialize the approved topology."""
    now = now or utc_now()
    if not str(actor_id or "").strip():
        raise PacketError("controlled_source_topology_authority_actor_missing")
    audit_store = Path(
        audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE
    )
    with current_action_class_contract_policy_lock(audit_store):
        records = read_audit_records(audit_store)
        existing = _controlled_source_topology_decision_records(
            records, request_id,
        )
        request = controlled_source_topology_request_from_audit(
            request_id,
            request_hash,
            audit_store=audit_store,
            now=now,
        )
        validation = validate_controlled_source_topology_authority_request(
            request,
            decision=decision,
            expected_request_id=request_id,
            expected_request_hash=request_hash,
            now=now,
        )
        if not validation.get("ok"):
            raise PacketError(",".join(
                validation.get("errors")
                or ["controlled_source_topology_decision_invalid"]
            ))
        decision_id = stable_id("cstopdec", {
            "request_id": request_id,
            "request_hash": request_hash,
            "decision": decision,
            "actor_id": str(actor_id),
        })
        if existing:
            exact = [
                row for row in existing
                if row.get("decision_id") == decision_id
                and row.get("authority_request_hash") == request_hash
                and row.get("decision") == decision
                and str(
                    ((row.get("actor_provenance") or {}).get("actor_id")) or ""
                ) == str(actor_id)
            ]
            if len(existing) == 1 and len(exact) == 1:
                return {
                    "status": "ALREADY_RECORDED_EXACT",
                    "request_id": request_id,
                    "request_hash": request_hash,
                    "decision": decision,
                    "decision_id": decision_id,
                    "audit_write": False,
                    "topology_materialized": False,
                    "runtime_apply": False,
                    "routing_mutation": False,
                    "users_moved": 0,
                }
            raise PacketError(
                "controlled_source_topology_authority_decision_conflict"
            )
        record = append_record(audit_store, {
            "schema_version": (
                "v7.controlled-source-topology-authority-decision.v1"
            ),
            "record_type": CONTROLLED_SOURCE_TOPOLOGY_DECISION_RECORD_TYPE,
            "decision_id": decision_id,
            "authority_request_id": request_id,
            "authority_request_hash": request_hash,
            "semantic_request_fingerprint": (
                controlled_source_topology_semantic_fingerprint(request)
            ),
            "manifest_hash": str(
                ((request.get("manifest") or {}).get("manifest_hash")) or ""
            ),
            "decision": decision,
            "actor_provenance": {
                "actor_id": str(actor_id),
                "decision_surface": "tools/v7-operator-execution-packet",
                "issuing_owner": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
                "recorded_at": now.isoformat(),
            },
            "created_at": now.isoformat(),
        })
    return {
        "status": (
            "APPROVED" if decision.startswith("APPROVE_") else "DECLINED"
        ),
        "request_id": request_id,
        "request_hash": request_hash,
        "decision": decision,
        "decision_id": record["decision_id"],
        "next_required_consumer": (
            "existing controlled-source reservation/provisioning preflight owner"
            if decision.startswith("APPROVE_")
            else "existing CPS/OMP residual reconciliation owner"
        ),
        "audit_write": True,
        "policy_write": False,
        "registry_write": False,
        "identity_creation": False,
        "assignment_change": False,
        "topology_materialized": False,
        "candidate_created": False,
        "packet_created": False,
        "lease_created": False,
        "restore_barrier_write": False,
        "runtime_apply": False,
        "routing_mutation": False,
        "users_moved": 0,
        "rollback_apply": False,
        "authority_self_expansion": False,
        "production_maturity_change": False,
    }


def standing_delegated_operational_policy_template(
    max_users=1,
    *,
    include_controlled_topology=False,
    include_availability_first=False,
):
    """Return the exact narrow scope consumed by the existing executor.

    The template is not Authority and cannot enable execution.  It keeps the
    scope definition with the established policy/packet owners and is turned
    into live Authority only by ``issue_standing_delegated_policy_from_audit``.
    """
    from admin_core import autonomy_trust_acceleration

    max_users = as_int(max_users, 0)
    if max_users not in SERVICE_FAILURE_DELEGATED_ACTION_CLASSES:
        raise PacketError("standing_delegated_policy_tier_not_engineering_qualified")
    action_class = SERVICE_FAILURE_DELEGATED_ACTION_CLASSES[max_users]
    policy = copy.deepcopy(autonomy_trust_acceleration.DEFAULT_DELEGATED_AUTONOMY_POLICY)
    policy.update({
        "policy_state": "APPROVED",
        "current_mode": "DELEGATED_AUTONOMY",
        "target_mode": "DELEGATED_AUTONOMY",
        "allowed_action_classes": [action_class],
        "max_users_per_action": max_users,
        "max_concurrent_transactions": 1,
        "max_blast_radius": {"users": max_users},
        "runtime_apply_enabled": True,
        "current_action_class_contract_state": "STANDING_POLICY_ACTIVE",
        "operator_candidate_approval_required": False,
        "operator_packet_approval_required": False,
        "operator_hash_approval_required": False,
        "self_expansion_allowed": False,
        "final_safe_mode": "OPEN",
    })
    if max_users > 1:
        policy.update({
            "policy_id": f"dap_service_failure_tier{max_users}",
            "policy_name": f"Bounded Service Failure Tier {max_users} Delegated Autonomy Policy",
        })
    if include_availability_first:
        include_controlled_topology = True
    if include_controlled_topology:
        policy.update({
            "policy_profile": (
                AVAILABILITY_FIRST_STANDING_POLICY_PROFILE
                if include_availability_first
                else CONTROLLED_TOPOLOGY_STANDING_POLICY_PROFILE
            ),
            "allowed_action_classes": [
                action_class,
                CONTROLLED_TOPOLOGY_DELEGATED_ACTION_CLASS,
                *(
                    [AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS]
                    if include_availability_first else []
                ),
            ],
            "action_class_scopes": {
                action_class: {
                    "max_users_per_transaction": max_users,
                    "max_concurrent_transactions": 1,
                    "source_target_selection": "EXISTING_PLANNER_SAFE_TARGET_ONLY",
                },
                CONTROLLED_TOPOLOGY_DELEGATED_ACTION_CLASS: {
                    "allowed_actions": [
                        "REBIND_CONTROLLED_CERTIFICATION_SOURCE",
                    ],
                    "certification_identities_only": True,
                    "max_users_per_transaction": 1,
                    "max_concurrent_transactions": 1,
                    "ordinary_identity_delta": 0,
                    "ordinary_route_delta": 0,
                    "ordinary_assignment_mutation_allowed": False,
                    "target_ordinary_users": 0,
                    "target_health": "FRESH_PASS_REQUIRED",
                    "target_stability": "OWNER_BACKED_FLOOR_REQUIRED",
                    "capacity_after_reserve": "SUFFICIENT_REQUIRED",
                    "immutable_manifest_required": True,
                    "fresh_candidate_required": True,
                    "fresh_packet_required": True,
                    "fresh_lease_required": True,
                    "restore_barrier_before_apply_required": True,
                    "verification_required": True,
                    "bounded_idempotent_rollback_required": True,
                    "private_credential_mutation_allowed": False,
                    "external_resource_creation_allowed": False,
                    "hard_limit_modification_allowed": False,
                    "authority_self_expansion_allowed": False,
                    "material_inventory_change_result": (
                        "INVALIDATE_ALLOCATION_NOT_STANDING_POLICY"
                    ),
                },
                **({
                    AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS: {
                        "allowed_actions": list(
                            AVAILABILITY_FIRST_ALLOWED_ACTIONS
                        ),
                        "certification_identities_only": True,
                        "max_users_per_transaction": max_users,
                        "max_concurrent_transactions": 1,
                        "ladder": list(AVAILABILITY_FIRST_LADDER),
                        "ladder_stage_semantics": (
                            "EXACT_TOTAL_COHORT_WITH_BASELINE_RESET"
                        ),
                        "allowed_target_classifications": [
                            "HEALTHY",
                            "DEGRADED_USABLE",
                            "LAST_RESORT_USABLE",
                        ],
                        "degraded_usable_initial_trial_scope": 1,
                        "last_resort_initial_trial_scope": 1,
                        "target_specific_real_outcome_required_for_growth": True,
                        "adaptive_capacity_owner_backed": True,
                        "aggregate_capacity_must_cover_exact_allocation": True,
                        "capacity_double_counting_forbidden": True,
                        "source_target_collision_forbidden": True,
                        "ordinary_identity_delta": 0,
                        "ordinary_route_delta": 0,
                        "ordinary_assignment_mutation_allowed": False,
                        "ordinary_reclassification_allowed": False,
                        "shared_target_fault_injection_allowed": False,
                        "shared_target_restart_allowed": False,
                        "hard_limit_modification_allowed": False,
                        "private_credential_mutation_allowed": False,
                        "external_resource_creation_allowed": False,
                        "immutable_allocation_required": True,
                        "fresh_inventory_required": True,
                        "fresh_candidate_required": True,
                        "fresh_packet_or_packet_set_required": True,
                        "fresh_lease_required": True,
                        "restore_barrier_before_apply_required": True,
                        "per_user_verification_required": True,
                        "per_target_verification_required": True,
                        "aggregate_verification_required": True,
                        "ordinary_user_quality_verification_required": True,
                        "cohort_circuit_breaker_required": True,
                        "partial_target_containment_required": True,
                        "rollback_or_redistribution_required": True,
                        "baseline_reset_between_stages_required": True,
                        "material_inventory_change_result": (
                            "INVALIDATE_ALLOCATION_CANDIDATE_PACKET_LEASE"
                        ),
                        "authority_self_expansion_allowed": False,
                    },
                } if include_availability_first else {}),
            },
            "allowed_production_effects": {
                CONTROLLED_TOPOLOGY_DELEGATED_ACTION_CLASS: [
                    "certification_only_assignment_change",
                    "controlled_source_reservation",
                    "restore_barrier_write",
                    "bounded_runtime_apply",
                    "bounded_idempotent_rollback",
                ],
                **({
                    AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS: [
                        "certification_only_assignment_change",
                        "shared_target_capacity_reservation",
                        "restore_barrier_write",
                        "bounded_runtime_apply",
                        "bounded_subset_redistribution",
                        "bounded_idempotent_rollback",
                    ],
                } if include_availability_first else {}),
            },
        })
    return policy


def build_standing_delegated_policy_authority_request(
    *,
    policy_generation_hash,
    active_program,
    max_users=1,
    include_controlled_topology=False,
    include_availability_first=False,
    now=None,
):
    """Build a short-lived request to activate the bounded standing policy."""
    from admin_core import autonomy_trust_acceleration

    now = now or utc_now()
    if include_availability_first:
        include_controlled_topology = True
    policy = standing_delegated_operational_policy_template(
        max_users=max_users,
        include_controlled_topology=include_controlled_topology,
        include_availability_first=include_availability_first,
    )
    normalized_scope = autonomy_trust_acceleration.normalized_delegated_autonomy_scope(policy)
    request = {
        "schema_version": STANDING_DELEGATED_POLICY_REQUEST_SCHEMA,
        "status": "AWAITING_INDEPENDENT_AUTHORITY_DECISION",
        "created_at": now.isoformat(),
        "expires_at": (now + timedelta(seconds=STANDING_DELEGATED_POLICY_REQUEST_TTL_SECONDS)).isoformat(),
        "decision_set": ["APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY", "DECLINE"],
        "issuing_owner_required": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
        "active_program": str(active_program or ""),
        "policy_generation_hash": str(policy_generation_hash or ""),
        "policy_id": STANDING_DELEGATED_POLICY_ID,
        "policy": policy,
        "policy_template_hash": sha256_json(policy),
        "normalized_scope": normalized_scope,
        "policy_scope_hash": autonomy_trust_acceleration.delegated_autonomy_scope_hash(policy),
        "contract_ttl_seconds": STANDING_DELEGATED_POLICY_MAX_TTL_SECONDS,
        "per_action_law": {
            "candidate_owner": "tools/v7-users-autoswitch",
            "candidate_identity": "FRESH_ONLY",
            "packet_owner": CANONICAL_CLEARANCE_OWNER,
            "packet_generation": "FRESH_IMMEDIATELY_BEFORE_EXECUTION",
            "packet_reuse": "FORBIDDEN",
            "lease_required": True,
            "max_users": int(policy["max_users_per_action"]),
            "max_concurrent_transactions": 1,
            "verification_required": True,
            "rollback_or_certified_no_rollback_required": True,
            "final_safe_mode": "OPEN",
            **({
                "controlled_topology": {
                    "action_class": CONTROLLED_TOPOLOGY_DELEGATED_ACTION_CLASS,
                    "allowed_actions": [
                        "REBIND_CONTROLLED_CERTIFICATION_SOURCE",
                    ],
                    "max_users": 1,
                    "max_concurrent_transactions": 1,
                    "candidate_owner": "tools/v7-users-autoswitch",
                    "packet_owner": CANONICAL_CLEARANCE_OWNER,
                    "execution_owner": "tools/v7-governed-canary-dry-run-cycle",
                    "reservation_owner": "tools/v7-egress-set-state",
                    "candidate_identity": "FRESH_ONLY",
                    "packet_reuse": "FORBIDDEN",
                    "lease_required": True,
                    "restore_barrier_required": True,
                    "verification_required": True,
                    "rollback_or_certified_no_rollback_required": True,
                    "ordinary_user_effect": "FORBIDDEN",
                    "external_resource_or_credential_mutation": "FORBIDDEN",
                    "self_expansion_allowed": False,
                },
            } if include_controlled_topology else {}),
            **({
                "availability_first": {
                    "action_class": (
                        AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS
                    ),
                    "allowed_actions": list(
                        AVAILABILITY_FIRST_ALLOWED_ACTIONS
                    ),
                    "ladder": list(AVAILABILITY_FIRST_LADDER),
                    "stage_semantics": (
                        "EXACT_TOTAL_COHORT_WITH_BASELINE_RESET"
                    ),
                    "max_users": max_users,
                    "max_concurrent_transactions": 1,
                    "target_selection": (
                        "FRESH_EXISTING_PLANNER_SAFE_TARGET_OR_TARGET_SET"
                    ),
                    "candidate_identity": "FRESH_ONLY",
                    "packet_reuse": "FORBIDDEN",
                    "lease_required": True,
                    "restore_barrier_required": True,
                    "per_user_per_target_aggregate_verification": True,
                    "ordinary_user_protection_required": True,
                    "partial_target_containment_required": True,
                    "rollback_or_redistribution_required": True,
                    "baseline_reset_between_stages_required": True,
                    "self_expansion_allowed": False,
                },
            } if include_availability_first else {}),
        },
        "forbidden_effects": [
            "authority_self_expansion",
            (
                "action_class_outside_exact_combined_profile"
                if include_controlled_topology
                else "new_action_class"
            ),
            "blast_radius_increase",
            "candidate_or_packet_reuse",
            "production_maturity_change",
        ],
    }
    request_hash = standing_delegated_policy_request_hash(request)
    request["request_hash"] = request_hash
    request["request_id"] = f"sdpauth_r1_{request_hash[:24]}"
    return request


def validate_standing_delegated_policy_authority_request(
    request, *, decision, expected_request_id="", expected_request_hash="", now=None,
    allow_decline=False,
):
    from admin_core import autonomy_trust_acceleration

    now = now or utc_now()
    request = request if isinstance(request, dict) else {}
    errors = []
    request_id = str(request.get("request_id") or "")
    request_hash = str(request.get("request_hash") or "")
    if request.get("schema_version") != STANDING_DELEGATED_POLICY_REQUEST_SCHEMA:
        errors.append("standing_delegated_policy_request_schema_invalid")
    if standing_delegated_policy_request_hash(request) != request_hash:
        errors.append("standing_delegated_policy_request_hash_mismatch")
    if request_id != f"sdpauth_r1_{request_hash[:24]}":
        errors.append("standing_delegated_policy_request_identity_mismatch")
    if expected_request_id and request_id != expected_request_id:
        errors.append("standing_delegated_policy_expected_request_mismatch")
    if expected_request_hash and request_hash != expected_request_hash:
        errors.append("standing_delegated_policy_expected_hash_mismatch")
    if request.get("status") != "AWAITING_INDEPENDENT_AUTHORITY_DECISION":
        errors.append("standing_delegated_policy_request_not_pending")
    try:
        if parse_ts(request.get("expires_at")) <= now:
            errors.append("standing_delegated_policy_request_expired")
        if parse_ts(request.get("created_at")) > now:
            errors.append("standing_delegated_policy_request_created_at_invalid")
    except PacketError:
        errors.append("standing_delegated_policy_request_timestamps_invalid")
    allowed_decisions = {"APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY"}
    if allow_decline:
        allowed_decisions.add("DECLINE")
    if decision not in allowed_decisions or decision not in set(request.get("decision_set") or []):
        errors.append("standing_delegated_policy_decision_not_exact")
    if request.get("issuing_owner_required") != CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER:
        errors.append("standing_delegated_policy_issuing_owner_invalid")
    if not str(request.get("active_program") or ""):
        errors.append("standing_delegated_policy_active_program_missing")
    if len(str(request.get("policy_generation_hash") or "")) != 64:
        errors.append("standing_delegated_policy_generation_missing")
    if request.get("policy_id") != STANDING_DELEGATED_POLICY_ID:
        errors.append("standing_delegated_policy_id_invalid")
    requested_policy = request.get("policy") if isinstance(request.get("policy"), dict) else {}
    requested_max_users = as_int(requested_policy.get("max_users_per_action"), 0)
    include_availability_first = (
        requested_policy.get("policy_profile")
        == AVAILABILITY_FIRST_STANDING_POLICY_PROFILE
    )
    include_controlled_topology = (
        requested_policy.get("policy_profile")
        in {
            CONTROLLED_TOPOLOGY_STANDING_POLICY_PROFILE,
            AVAILABILITY_FIRST_STANDING_POLICY_PROFILE,
        }
    )
    try:
        expected = standing_delegated_operational_policy_template(
            max_users=requested_max_users,
            include_controlled_topology=include_controlled_topology,
            include_availability_first=include_availability_first,
        )
    except PacketError:
        expected = {}
        errors.append("standing_delegated_policy_tier_not_engineering_qualified")
    expected_scope = autonomy_trust_acceleration.normalized_delegated_autonomy_scope(expected)
    if request.get("policy") != expected or request.get("policy_template_hash") != sha256_json(expected):
        errors.append("standing_delegated_policy_template_invalid")
    if request.get("normalized_scope") != expected_scope:
        errors.append("standing_delegated_policy_scope_invalid")
    if request.get("policy_scope_hash") != autonomy_trust_acceleration.delegated_autonomy_scope_hash(expected):
        errors.append("standing_delegated_policy_scope_hash_invalid")
    if as_int(request.get("contract_ttl_seconds"), 0) != STANDING_DELEGATED_POLICY_MAX_TTL_SECONDS:
        errors.append("standing_delegated_policy_ttl_invalid")
    law = request.get("per_action_law") if isinstance(request.get("per_action_law"), dict) else {}
    exact_law = {
        "candidate_owner": "tools/v7-users-autoswitch",
        "candidate_identity": "FRESH_ONLY",
        "packet_owner": CANONICAL_CLEARANCE_OWNER,
        "packet_generation": "FRESH_IMMEDIATELY_BEFORE_EXECUTION",
        "packet_reuse": "FORBIDDEN",
        "lease_required": True,
        "max_users": requested_max_users,
        "max_concurrent_transactions": 1,
        "verification_required": True,
        "rollback_or_certified_no_rollback_required": True,
        "final_safe_mode": "OPEN",
        **({
            "controlled_topology": {
                "action_class": CONTROLLED_TOPOLOGY_DELEGATED_ACTION_CLASS,
                "allowed_actions": [
                    "REBIND_CONTROLLED_CERTIFICATION_SOURCE",
                ],
                "max_users": 1,
                "max_concurrent_transactions": 1,
                "candidate_owner": "tools/v7-users-autoswitch",
                "packet_owner": CANONICAL_CLEARANCE_OWNER,
                "execution_owner": "tools/v7-governed-canary-dry-run-cycle",
                "reservation_owner": "tools/v7-egress-set-state",
                "candidate_identity": "FRESH_ONLY",
                "packet_reuse": "FORBIDDEN",
                "lease_required": True,
                "restore_barrier_required": True,
                "verification_required": True,
                "rollback_or_certified_no_rollback_required": True,
                "ordinary_user_effect": "FORBIDDEN",
                "external_resource_or_credential_mutation": "FORBIDDEN",
                "self_expansion_allowed": False,
            },
        } if include_controlled_topology else {}),
        **({
            "availability_first": {
                "action_class": AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS,
                "allowed_actions": list(AVAILABILITY_FIRST_ALLOWED_ACTIONS),
                "ladder": list(AVAILABILITY_FIRST_LADDER),
                "stage_semantics": (
                    "EXACT_TOTAL_COHORT_WITH_BASELINE_RESET"
                ),
                "max_users": requested_max_users,
                "max_concurrent_transactions": 1,
                "target_selection": (
                    "FRESH_EXISTING_PLANNER_SAFE_TARGET_OR_TARGET_SET"
                ),
                "candidate_identity": "FRESH_ONLY",
                "packet_reuse": "FORBIDDEN",
                "lease_required": True,
                "restore_barrier_required": True,
                "per_user_per_target_aggregate_verification": True,
                "ordinary_user_protection_required": True,
                "partial_target_containment_required": True,
                "rollback_or_redistribution_required": True,
                "baseline_reset_between_stages_required": True,
                "self_expansion_allowed": False,
            },
        } if include_availability_first else {}),
    }
    if law != exact_law:
        errors.append("standing_delegated_policy_per_action_law_invalid")
    return {"ok": not errors, "errors": sorted(set(errors)), "request_id": request_id, "request_hash": request_hash}


def validate_standing_delegated_operational_policy(contract, *, now=None, audit_records=None):
    """Fail closed unless the live policy contains an exact owner-issued grant."""
    from admin_core import autonomy_trust_acceleration

    now = now or utc_now()
    contract = contract if isinstance(contract, dict) else {}
    errors = []
    if contract.get("schema_version") != STANDING_DELEGATED_POLICY_SCHEMA:
        errors.append("standing_delegated_policy_contract_schema_invalid")
    contract_hash = str(contract.get("contract_hash") or "")
    if standing_delegated_policy_contract_hash(contract) != contract_hash:
        errors.append("standing_delegated_policy_contract_hash_invalid")
    if str(contract.get("contract_id") or "") != f"sdpc_{contract_hash[:24]}":
        errors.append("standing_delegated_policy_contract_identity_invalid")
    if contract.get("status") != "ACTIVE":
        errors.append("standing_delegated_policy_contract_not_active")
    try:
        if parse_ts(contract.get("expires_at")) <= now:
            errors.append("standing_delegated_policy_contract_expired")
    except PacketError:
        errors.append("standing_delegated_policy_contract_expiry_invalid")
    if contract.get("issuing_owner") != CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER:
        errors.append("standing_delegated_policy_contract_owner_invalid")
    policy = contract.get("policy") if isinstance(contract.get("policy"), dict) else {}
    requested_max_users = as_int(policy.get("max_users_per_action"), 0)
    include_availability_first = (
        policy.get("policy_profile")
        == AVAILABILITY_FIRST_STANDING_POLICY_PROFILE
    )
    include_controlled_topology = (
        policy.get("policy_profile")
        in {
            CONTROLLED_TOPOLOGY_STANDING_POLICY_PROFILE,
            AVAILABILITY_FIRST_STANDING_POLICY_PROFILE,
        }
    )
    try:
        expected = standing_delegated_operational_policy_template(
            max_users=requested_max_users,
            include_controlled_topology=include_controlled_topology,
            include_availability_first=include_availability_first,
        )
    except PacketError:
        expected = {}
        errors.append("standing_delegated_policy_tier_not_engineering_qualified")
    if autonomy_trust_acceleration.normalized_delegated_autonomy_scope(policy) != autonomy_trust_acceleration.normalized_delegated_autonomy_scope(expected):
        errors.append("standing_delegated_policy_contract_scope_invalid")
    if contract.get("policy_scope_hash") != autonomy_trust_acceleration.delegated_autonomy_scope_hash(expected):
        errors.append("standing_delegated_policy_contract_scope_hash_invalid")
    law = contract.get("per_action_law") if isinstance(contract.get("per_action_law"), dict) else {}
    if (
        as_int(law.get("max_users"), 0) != requested_max_users
        or as_int(law.get("max_concurrent_transactions"), 0) != 1
        or law.get("candidate_identity") != "FRESH_ONLY"
        or law.get("packet_reuse") != "FORBIDDEN"
        or law.get("lease_required") is not True
        or law.get("verification_required") is not True
        or law.get("rollback_or_certified_no_rollback_required") is not True
        or law.get("final_safe_mode") != "OPEN"
    ):
        errors.append("standing_delegated_policy_contract_per_action_law_invalid")
    request_binding = contract.get("authority_decision") if isinstance(contract.get("authority_decision"), dict) else {}
    if (
        request_binding.get("decision") != "APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY"
        or not request_binding.get("request_id")
        or not request_binding.get("request_hash")
        or not request_binding.get("actor_id")
    ):
        errors.append("standing_delegated_policy_authority_provenance_invalid")
    if audit_records is not None:
        matching_records = [
            record for record in (audit_records if isinstance(audit_records, list) else [])
            if record.get("record_type") == STANDING_DELEGATED_POLICY_DECISION_RECORD_TYPE
            and record.get("decision_id") == request_binding.get("decision_id")
            and record.get("authority_request_id") == request_binding.get("request_id")
            and record.get("authority_request_hash") == request_binding.get("request_hash")
            and record.get("decision") == request_binding.get("decision")
            and ((record.get("actor_provenance") or {}).get("actor_id") == request_binding.get("actor_id"))
        ]
        if len(matching_records) != 1:
            errors.append("standing_delegated_policy_authority_audit_missing_or_duplicate")
    return {"ok": not errors, "errors": sorted(set(errors)), "policy": policy, "contract": contract}


@contextmanager
def current_action_class_contract_policy_lock(policy_path):
    """Serialize the existing policy owner's read -> validate -> write lifecycle.

    The sidecar lock is only an interprocess coordination primitive.  It is not
    a state owner, queue, registry or source of truth; durable truth remains
    the existing policy and operator-execution audit owners.
    """
    policy_path = Path(policy_path)
    lock_path = policy_path.with_name(f".{policy_path.name}.action-class-contract.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _current_action_class_decision_records(records, request_id):
    return [
        record for record in records
        if record.get("record_type") == "current_action_class_contract_authority_decision"
        and str(record.get("authority_request_id") or "") == str(request_id or "")
    ]


def _current_action_class_request_records(records, request_id):
    return [
        record for record in records
        if record.get("record_type") == CURRENT_ACTION_CLASS_REQUEST_RECORD_TYPE
        and str(record.get("authority_request_id") or "") == str(request_id or "")
    ]


def register_current_action_class_contract_request(request, *, audit_store=None, producer_id="tools/v7-users-autoswitch", now=None):
    """Persist an exact short-lived request in the established audit owner.

    This is request provenance only: it does not write policy, issue a contract,
    grant Authority, or create an execution artifact.  Keeping the immutable
    preimage in the existing append-only audit closes the producer -> exact
    Authority-consumer handoff without introducing another registry.
    """
    envelope = request if isinstance(request, dict) else {}
    if isinstance(envelope.get("authority_decision_request"), dict):
        package = envelope.get("approval_package") if isinstance(envelope.get("approval_package"), dict) else {}
        forbidden_effects = {
            "authority_granted", "contract_written", "runtime_apply", "routing_mutation",
            "candidate_created", "packet_created", "lease_created",
        }
        if not (
            envelope.get("schema_version") == "v7.action-class-contract-reconciliation-request.v1"
            and envelope.get("status") == "ACTION_CLASS_CONTRACT_ISSUE_REVIEW_READY"
            and envelope.get("authority_classification") == "ENGINEERING_AUTHORITY_ACTION_CLASS_CONTRACT_REQUEST_READY"
            and envelope.get("exact_legal_next_action") == "INDEPENDENT_DECISION_ON_FRESH_ONE_USE_ACTION_CLASS_CONTRACT_REQUEST"
            and package.get("status") == "AWAITING_INDEPENDENT_AUTHORITY_DECISION"
            and package.get("actionable") is True
            and all(envelope.get(key) is False for key in forbidden_effects)
            and int(envelope.get("users_moved") or 0) == 0
        ):
            raise PacketError("current_action_class_contract_reconciliation_envelope_invalid")
        request = envelope["authority_decision_request"]
        if package.get("request_id") != request.get("request_id") or package.get("request_hash") != request.get("request_hash"):
            raise PacketError("current_action_class_contract_reconciliation_envelope_identity_mismatch")
    else:
        request = envelope
    now = now or utc_now()
    validation = validate_current_action_class_contract_authority_request(
        request, decision="DECLINE", allow_decline=True, now=now,
    )
    if not validation.get("ok"):
        raise PacketError(",".join(validation.get("errors") or ["current_action_class_contract_request_invalid"]))
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    records = read_audit_records(audit_store)
    existing = _current_action_class_request_records(records, request["request_id"])
    if existing:
        if len(existing) != 1 or str(existing[0].get("authority_request_hash") or "") != request["request_hash"]:
            raise PacketError("current_action_class_contract_request_audit_identity_conflict")
        if existing[0].get("request") != request:
            raise PacketError("current_action_class_contract_request_audit_preimage_conflict")
        return {"status": "ALREADY_REGISTERED", "request_id": request["request_id"], "request_hash": request["request_hash"], "audit_store": str(audit_store), "policy_write": False}
    record = append_record(audit_store, {
        "schema_version": CURRENT_ACTION_CLASS_AUDIT_SCHEMA,
        "record_type": CURRENT_ACTION_CLASS_REQUEST_RECORD_TYPE,
        "authority_request_id": request["request_id"],
        "authority_request_hash": request["request_hash"],
        "expires_at": request["expires_at"],
        "producer_provenance": {"producer_id": str(producer_id), "recorded_at": now.isoformat()},
        "request": copy.deepcopy(request),
        "created_at": now.isoformat(),
    })
    return {"status": "REGISTERED", "request_id": request["request_id"], "request_hash": request["request_hash"], "audit_store": str(audit_store), "record_hash": record["record_hash"], "policy_write": False}


def current_action_class_contract_request_from_audit(request_id, request_hash, *, audit_store=None, now=None):
    """Return only one unexpired immutable request preimage from the audit owner."""
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    matches = _current_action_class_request_records(read_audit_records(audit_store), request_id)
    if len(matches) != 1:
        raise PacketError("current_action_class_contract_request_audit_missing_or_duplicate")
    record = matches[0]
    request = record.get("request") if isinstance(record.get("request"), dict) else {}
    if str(record.get("authority_request_hash") or "") != str(request_hash or ""):
        raise PacketError("current_action_class_contract_request_audit_hash_mismatch")
    validation = validate_current_action_class_contract_authority_request(
        request, decision="DECLINE", expected_request_id=request_id,
        expected_request_hash=request_hash, now=now or utc_now(), allow_decline=True,
    )
    if not validation.get("ok"):
        raise PacketError(",".join(validation.get("errors") or ["current_action_class_contract_request_audit_invalid"]))
    return request


def _current_action_class_contract_audit_record(
    request, *, decision, actor_id, policy_generation_hash, now,
):
    if not str(actor_id or "").strip():
        raise PacketError("current_action_class_contract_authority_actor_missing")
    request = request if isinstance(request, dict) else {}
    decision_id = stable_id("accdec", {
        "request_id": request.get("request_id", ""),
        "request_hash": request.get("request_hash", ""),
        "decision": decision,
        "actor_id": str(actor_id),
    })
    return {
        "schema_version": CURRENT_ACTION_CLASS_AUDIT_SCHEMA,
        "record_type": "current_action_class_contract_authority_decision",
        "decision_id": decision_id,
        "authority_request_id": str(request.get("request_id") or ""),
        "authority_request_hash": str(request.get("request_hash") or ""),
        "decision": str(decision),
        "active_program": str(request.get("active_program") or ""),
        "subject": copy.deepcopy(request.get("subject") or {}),
        "scope": copy.deepcopy(request.get("scope") or {}),
        "incident_generation": copy.deepcopy(request.get("incident_generation") or {}),
        "source_generation": copy.deepcopy(request.get("source_generation") or {}),
        "policy_generation_hash": str(policy_generation_hash or ""),
        "actor_provenance": {
            "actor_id": str(actor_id),
            "decision_surface": "tools/v7-operator-execution-packet",
            "issuing_owner": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
            "recorded_at": now.isoformat(),
        },
        "created_at": now.isoformat(),
    }


def build_current_action_class_contract_authority_request(template, *, issue_preflight=None, now=None):
    """Build the existing Authority owner's exact one-use decision input.

    This deliberately returns a non-durable request.  It has no policy-write
    capability: only ``issue_current_action_class_contract`` below, owned by
    this established Authority surface, can turn an exact approval into the
    policy field consumed by autoswitch.
    """
    now = now or utc_now()
    template = copy.deepcopy(template if isinstance(template, dict) else {})
    scope = template.get("scope") if isinstance(template.get("scope"), dict) else {}
    subject = template.get("subject") if isinstance(template.get("subject"), dict) else {}
    source_generation = template.get("source_generation") if isinstance(template.get("source_generation"), dict) else {}
    incident_generation = template.get("incident_generation") if isinstance(template.get("incident_generation"), dict) else {}
    request = {
        "schema_version": CURRENT_ACTION_CLASS_CONTRACT_REQUEST_SCHEMA,
        "status": "AWAITING_INDEPENDENT_AUTHORITY_DECISION",
        "created_at": now.isoformat(),
        "expires_at": (now + timedelta(seconds=CURRENT_ACTION_CLASS_CONTRACT_REQUEST_TTL_SECONDS)).isoformat(),
        "decision_set": [ENGINEERING_AUTHORITY_APPROVAL, "DECLINE"],
        "issuing_owner_required": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
        "active_program": str(template.get("active_program") or ""),
        "action_class": str(template.get("action_class") or ""),
        "max_authority_class": str(template.get("max_authority_class") or ""),
        "authority_ceiling": str(template.get("authority_ceiling") or template.get("max_authority_class") or ""),
        "policy_generation_hash": str(template.get("policy_generation_hash") or ""),
        "subject": {"user_ip": str(subject.get("user_ip") or "")},
        "scope": {
            "source_egress": str(scope.get("source_egress") or ""),
            "target_egress": str(scope.get("target_egress") or ""),
            "max_users": as_int(template.get("max_users"), 0),
            "max_concurrent_transactions": as_int(template.get("max_concurrent_transactions"), 0),
        },
        "incident_generation": incident_generation,
        "source_generation": source_generation,
        "verification_contract": copy.deepcopy(template.get("verification_contract") or {}),
        "rollback_containment_contract": copy.deepcopy(template.get("rollback_containment_contract") or {}),
        "cooldown": copy.deepcopy(template.get("cooldown") or {}),
        "anti_flap": copy.deepcopy(template.get("anti_flap") or {}),
        "stop_conditions": [str(item) for item in (template.get("stop_conditions") or []) if str(item).strip()],
        "max_ttl_seconds": min(CURRENT_ACTION_CLASS_CONTRACT_MAX_TTL_SECONDS, max(1, as_int(template.get("max_ttl_seconds"), 900))),
        "one_use_law": {
            "approval_use_limit": 1,
            "implicit_renewal": False,
            "retry_under_same_approval": False,
            "consumption_owner": "tools/v7-users-autoswitch",
        },
        "issue_preflight": copy.deepcopy(issue_preflight if isinstance(issue_preflight, dict) else {}),
    }
    request_hash = current_action_class_contract_request_hash(request)
    request["request_hash"] = request_hash
    request["request_id"] = f"accauth_r1_{request_hash[:24]}"
    return request


def validate_current_action_class_contract_authority_request(
    request, *, decision, expected_request_id="", expected_request_hash="", now=None, allow_decline=False,
):
    now = now or utc_now()
    request = request if isinstance(request, dict) else {}
    errors: list[str] = []
    request_id = str(request.get("request_id") or "")
    request_hash = str(request.get("request_hash") or "")
    if request.get("schema_version") != CURRENT_ACTION_CLASS_CONTRACT_REQUEST_SCHEMA:
        errors.append("current_action_class_contract_request_schema_invalid")
    if current_action_class_contract_request_hash(request) != request_hash:
        errors.append("current_action_class_contract_request_hash_mismatch")
    if request_id != f"accauth_r1_{request_hash[:24]}":
        errors.append("current_action_class_contract_request_identity_mismatch")
    if expected_request_id and request_id != expected_request_id:
        errors.append("current_action_class_contract_expected_request_mismatch")
    if expected_request_hash and request_hash != expected_request_hash:
        errors.append("current_action_class_contract_expected_hash_mismatch")
    if str(request.get("status") or "") != "AWAITING_INDEPENDENT_AUTHORITY_DECISION":
        errors.append("current_action_class_contract_request_not_pending")
    try:
        if parse_ts(request.get("expires_at")) <= now:
            errors.append("current_action_class_contract_request_expired")
        if parse_ts(request.get("created_at")) > now:
            errors.append("current_action_class_contract_request_created_at_invalid")
    except PacketError:
        errors.append("current_action_class_contract_request_timestamps_invalid")
    permitted_decisions = {ENGINEERING_AUTHORITY_APPROVAL}
    if allow_decline:
        permitted_decisions.add("DECLINE")
    if decision not in permitted_decisions or decision not in set(request.get("decision_set") or []):
        errors.append("current_action_class_contract_decision_not_exact")
    if str(request.get("issuing_owner_required") or "") != CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER:
        errors.append("current_action_class_contract_issuing_owner_invalid")
    scope = request.get("scope") if isinstance(request.get("scope"), dict) else {}
    subject = request.get("subject") if isinstance(request.get("subject"), dict) else {}
    if not str(request.get("active_program") or ""):
        errors.append("current_action_class_contract_program_missing")
    if str(request.get("action_class") or "").upper() not in {"GOVERNED_ONLY", "EMERGENCY_FAILOVER"}:
        errors.append("current_action_class_contract_action_class_invalid")
    max_authority_class = str(request.get("max_authority_class") or "").upper()
    authority_ceiling = str(request.get("authority_ceiling") or "").upper()
    if max_authority_class not in CURRENT_ACTION_CLASS_AUTHORITY_RANK or authority_ceiling not in CURRENT_ACTION_CLASS_AUTHORITY_RANK:
        errors.append("current_action_class_contract_authority_ceiling_invalid")
    elif CURRENT_ACTION_CLASS_AUTHORITY_RANK[max_authority_class] > CURRENT_ACTION_CLASS_AUTHORITY_RANK[authority_ceiling]:
        errors.append("current_action_class_contract_authority_exceeds_ceiling")
    if len(str(request.get("policy_generation_hash") or "")) != 64:
        errors.append("current_action_class_contract_policy_generation_missing")
    if not str(subject.get("user_ip") or ""):
        errors.append("current_action_class_contract_subject_missing")
    if not str(scope.get("source_egress") or "") or not str(scope.get("target_egress") or ""):
        errors.append("current_action_class_contract_scope_missing")
    if as_int(scope.get("max_users"), 0) != 1 or as_int(scope.get("max_concurrent_transactions"), 0) != 1:
        errors.append("current_action_class_contract_blast_radius_invalid")
    source_generation = request.get("source_generation") if isinstance(request.get("source_generation"), dict) else {}
    if not all(str(source_generation.get(key) or "") for key in ("planner_generation_id", "source_bundle_hash", "snapshot_bundle_hash", "selected_move_hash")):
        errors.append("current_action_class_contract_source_generation_missing")
    incident_generation = request.get("incident_generation") if isinstance(request.get("incident_generation"), dict) else {}
    if not all(str(incident_generation.get(key) or "") for key in ("incident_id", "incident_generation")):
        errors.append("current_action_class_contract_incident_generation_invalid")
    verification = request.get("verification_contract") if isinstance(request.get("verification_contract"), dict) else {}
    if not all(verification.get(key) for key in ("owner", "required", "immediate_and_temporal_observation", "success_criteria")):
        errors.append("current_action_class_contract_verification_contract_missing")
    rollback = request.get("rollback_containment_contract") if isinstance(request.get("rollback_containment_contract"), dict) else {}
    if not (
        rollback.get("owner") and rollback.get("required") is True
        and rollback.get("triggered_by_verifier") is True
        and rollback.get("direct_terminal_manufacture_forbidden") is True
    ):
        errors.append("current_action_class_contract_rollback_contract_missing")
    cooldown = request.get("cooldown") if isinstance(request.get("cooldown"), dict) else {}
    anti_flap = request.get("anti_flap") if isinstance(request.get("anti_flap"), dict) else {}
    if as_int(cooldown.get("seconds"), -1) < 0 or cooldown.get("required") is not True:
        errors.append("current_action_class_contract_cooldown_invalid")
    if anti_flap.get("required") is not True or anti_flap.get("same_source_target_repeat_forbidden") is not True:
        errors.append("current_action_class_contract_anti_flap_invalid")
    stop_conditions = {str(item).strip() for item in (request.get("stop_conditions") or []) if str(item).strip()}
    if not CURRENT_ACTION_CLASS_REQUIRED_STOP_CONDITIONS.issubset(stop_conditions):
        errors.append("current_action_class_contract_stop_conditions_incomplete")
    one_use = request.get("one_use_law") if isinstance(request.get("one_use_law"), dict) else {}
    if as_int(one_use.get("approval_use_limit"), 0) != 1 or one_use.get("implicit_renewal") is not False or one_use.get("retry_under_same_approval") is not False:
        errors.append("current_action_class_contract_one_use_law_invalid")
    if str(one_use.get("consumption_owner") or "") != "tools/v7-users-autoswitch":
        errors.append("current_action_class_contract_consumption_owner_invalid")
    preflight = request.get("issue_preflight") if isinstance(request.get("issue_preflight"), dict) else {}
    if preflight.get("ready") is not True or preflight.get("blockers") not in ([], None):
        errors.append("current_action_class_contract_issue_preflight_not_ready")
    return {"ok": not errors, "errors": sorted(set(errors)), "request_id": request_id, "request_hash": request_hash, "evaluated_at": now.isoformat()}


def issue_current_action_class_contract(
    policy, request, *, decision, expected_request_id="", expected_request_hash="", now=None,
    authority_actor_id="", authority_decision_id="",
):
    """Issue the policy contract through the existing Authority owner only.

    The returned policy is deliberately not a runtime action.  Its contract
    carries the exact Authority decision, fresh source generation and a
    one-use state; autoswitch must independently revalidate it before any
    Candidate/Packet/apply lifecycle can proceed.
    """
    now = now or utc_now()
    validation = validate_current_action_class_contract_authority_request(
        request, decision=decision, expected_request_id=expected_request_id,
        expected_request_hash=expected_request_hash, now=now,
    )
    if not validation.get("ok"):
        raise PacketError(",".join(validation.get("errors") or ["current_action_class_contract_request_invalid"]))
    if not str(authority_actor_id or "").strip() or not str(authority_decision_id or "").strip():
        raise PacketError("current_action_class_contract_authority_audit_provenance_missing")
    policy = copy.deepcopy(policy if isinstance(policy, dict) else {})
    authority_budget = policy.get("authority_budget") if isinstance(policy.get("authority_budget"), dict) else {}
    previous = authority_budget.get("current_action_class_contract") if isinstance(authority_budget.get("current_action_class_contract"), dict) else {}
    previous_one_use = previous.get("one_use_consumption") if isinstance(previous.get("one_use_consumption"), dict) else {}
    if str(previous_one_use.get("state") or "") == "ISSUED":
        try:
            previous_unexpired = parse_ts(previous.get("expires_at")) > now
        except PacketError:
            previous_unexpired = False
        if previous_unexpired:
            raise PacketError("current_action_class_contract_unconsumed_contract_already_issued")
    ttl_seconds = as_int(request.get("max_ttl_seconds"), 0)
    if ttl_seconds <= 0 or ttl_seconds > CURRENT_ACTION_CLASS_CONTRACT_MAX_TTL_SECONDS:
        raise PacketError("current_action_class_contract_ttl_invalid")
    issued_at = now.isoformat()
    expires_at = (now + timedelta(seconds=ttl_seconds)).isoformat()
    scope = request.get("scope") or {}
    contract = {
        "schema_version": CURRENT_ACTION_CLASS_CONTRACT_SCHEMA,
        "issuing_owner": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
        "active_program": str(request.get("active_program") or ""),
        "action_class": str(request.get("action_class") or ""),
        "max_authority_class": str(request.get("max_authority_class") or ""),
        "authority_ceiling": str(request.get("authority_ceiling") or ""),
        "policy_generation_hash": str(request.get("policy_generation_hash") or ""),
        "subject": copy.deepcopy(request.get("subject") or {}),
        "scope": {"source_egress": str(scope.get("source_egress") or ""), "target_egress": str(scope.get("target_egress") or "")},
        "max_users": 1,
        "max_concurrent_transactions": 1,
        "incident_generation": copy.deepcopy(request.get("incident_generation") or {}),
        "source_generation": copy.deepcopy(request.get("source_generation") or {}),
        "issued_at": issued_at,
        "expires_at": expires_at,
        "verification_contract": copy.deepcopy(request.get("verification_contract") or {}),
        "rollback_containment_contract": copy.deepcopy(request.get("rollback_containment_contract") or {}),
        "cooldown": copy.deepcopy(request.get("cooldown") or {}),
        "anti_flap": copy.deepcopy(request.get("anti_flap") or {}),
        "required_gates": {
            "fresh_evidence_required": True, "verification_required": True,
            "rollback_required": True, "anti_flap_required": True,
            "cooldown_seconds": as_int((request.get("cooldown") or {}).get("seconds"), 0),
        },
        "stop_conditions": copy.deepcopy(request.get("stop_conditions") or []),
        "authority_decision": {
            "decision": ENGINEERING_AUTHORITY_APPROVAL,
            "request_id": validation["request_id"],
            "request_hash": validation["request_hash"],
            "decided_at": issued_at,
            "actor_id": str(authority_actor_id or ""),
            "decision_id": str(authority_decision_id or ""),
            "approval_use_limit": 1,
            "implicit_renewal": False,
            "retry_under_same_approval": False,
        },
        "one_use_consumption": {
            "state": "ISSUED", "allowed_uses": 1, "consumed_uses": 0,
            "consumption_owner": "tools/v7-users-autoswitch", "consumption_id": "",
            "consumed_at": "", "retry_allowed": False,
        },
    }
    contract_hash = current_action_class_contract_hash(contract)
    contract["contract_hash"] = contract_hash
    contract["contract_id"] = f"acc_{contract_hash[:24]}"
    authority_budget = dict(authority_budget)
    authority_budget["current_action_class_contract"] = contract
    policy["authority_budget"] = authority_budget
    return {"policy": policy, "contract": contract, "validation": validation}


def consume_current_action_class_contract(policy, *, contract_id, contract_hash, subject, scope, source_generation, operation_id, now=None):
    """Atomically consume a v2 contract before its sole forward mutation.

    A failed or interrupted downstream apply still consumes the decision.  That
    is intentional: retrying requires a fresh Situation and a fresh Authority
    decision, never reuse of an old policy field.
    """
    now = now or utc_now()
    policy = copy.deepcopy(policy if isinstance(policy, dict) else {})
    budget = policy.get("authority_budget") if isinstance(policy.get("authority_budget"), dict) else {}
    contract = budget.get("current_action_class_contract") if isinstance(budget.get("current_action_class_contract"), dict) else {}
    consumption = contract.get("one_use_consumption") if isinstance(contract.get("one_use_consumption"), dict) else {}
    if str(contract.get("schema_version") or "") != CURRENT_ACTION_CLASS_CONTRACT_SCHEMA:
        raise PacketError("current_action_class_contract_consumption_schema_invalid")
    if str(contract.get("contract_id") or "") != str(contract_id or "") or str(contract.get("contract_hash") or "") != str(contract_hash or ""):
        raise PacketError("current_action_class_contract_consumption_identity_mismatch")
    if current_action_class_contract_hash(contract) != str(contract_hash or ""):
        raise PacketError("current_action_class_contract_consumption_hash_invalid")
    try:
        if parse_ts(contract.get("expires_at")) <= now:
            raise PacketError("current_action_class_contract_consumption_expired")
    except PacketError as exc:
        if str(exc) == "current_action_class_contract_consumption_expired":
            raise
        raise PacketError("current_action_class_contract_consumption_expiry_invalid") from exc
    if str(consumption.get("state") or "") != "ISSUED" or as_int(consumption.get("allowed_uses"), 0) != 1 or as_int(consumption.get("consumed_uses"), -1) != 0:
        raise PacketError("current_action_class_contract_not_available_for_one_use_consumption")
    expected_subject = contract.get("subject") if isinstance(contract.get("subject"), dict) else {}
    expected_scope = contract.get("scope") if isinstance(contract.get("scope"), dict) else {}
    if str((subject or {}).get("user_ip") or "") != str(expected_subject.get("user_ip") or ""):
        raise PacketError("current_action_class_contract_consumption_subject_mismatch")
    if {
        "source_egress": str((scope or {}).get("source_egress") or ""),
        "target_egress": str((scope or {}).get("target_egress") or ""),
    } != {
        "source_egress": str(expected_scope.get("source_egress") or ""),
        "target_egress": str(expected_scope.get("target_egress") or ""),
    }:
        raise PacketError("current_action_class_contract_consumption_scope_mismatch")
    if dict(source_generation or {}) != dict(contract.get("source_generation") or {}):
        raise PacketError("current_action_class_contract_consumption_generation_mismatch")
    if not str(operation_id or ""):
        raise PacketError("current_action_class_contract_consumption_operation_missing")
    consumption = dict(consumption)
    consumption.update({
        "state": "CONSUMED", "consumed_uses": 1,
        "consumption_id": stable_id("accuse", {"contract_id": contract_id, "operation_id": operation_id}),
        "consumed_at": now.isoformat(), "operation_id": str(operation_id),
        "retry_allowed": False,
    })
    contract["one_use_consumption"] = consumption
    # The contract hash identifies the immutable issuance; consumption is a
    # governed lifecycle transition and intentionally does not rewrite it.
    budget = dict(budget)
    budget["current_action_class_contract"] = contract
    policy["authority_budget"] = budget
    return {"policy": policy, "consumption": consumption, "contract": contract}


def consume_current_action_class_contract_to_policy(policy_path, *, audit_store=None, actor_id="tools/v7-users-autoswitch", **kwargs):
    """Consume once under the existing policy owner's interprocess lock.

    Locking covers the read, exact identity checks and atomic policy replace, so
    two autoswitch processes cannot both observe ISSUED.  The audit append is
    linked to the resulting consumption id and uses the established
    operator-execution audit store.
    """
    policy_path = Path(policy_path)
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    with current_action_class_contract_policy_lock(policy_path):
        result = consume_current_action_class_contract(read_json(policy_path), **kwargs)
        write_json_atomic(policy_path, result["policy"])
        append_record(audit_store, {
            "schema_version": CURRENT_ACTION_CLASS_AUDIT_SCHEMA,
            "record_type": "current_action_class_contract_consumed",
            "contract_id": result["contract"].get("contract_id", ""),
            "contract_hash": result["contract"].get("contract_hash", ""),
            "authority_request_id": ((result["contract"].get("authority_decision") or {}).get("request_id", "")),
            "consumption_id": result["consumption"].get("consumption_id", ""),
            "operation_id": str(kwargs.get("operation_id") or ""),
            "actor_provenance": {
                "actor_id": str(actor_id or "tools/v7-users-autoswitch"),
                "consumption_owner": "tools/v7-users-autoswitch",
                "recorded_at": (kwargs.get("now") or utc_now()).isoformat(),
            },
            "created_at": (kwargs.get("now") or utc_now()).isoformat(),
        })
    return result


def cancel_unconsumed_current_action_class_contract_to_policy(
    policy_path, *, expected_contract_id, expected_contract_hash,
    actor_id, reason, audit_store=None, now=None,
):
    """Fail-closed cancellation for a misbound, still-unconsumed one-use grant."""
    if not str(actor_id or "").strip() or not str(reason or "").strip():
        raise PacketError("current_action_class_contract_cancellation_provenance_missing")
    now = now or utc_now()
    policy_path = Path(policy_path)
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    with current_action_class_contract_policy_lock(policy_path):
        policy = read_json(policy_path)
        budget = policy.get("authority_budget") if isinstance(policy.get("authority_budget"), dict) else {}
        contract = budget.get("current_action_class_contract") if isinstance(budget.get("current_action_class_contract"), dict) else {}
        if (
            str(contract.get("contract_id") or "") != str(expected_contract_id or "")
            or str(contract.get("contract_hash") or "") != str(expected_contract_hash or "")
        ):
            raise PacketError("current_action_class_contract_cancellation_identity_mismatch")
        consumption = contract.get("one_use_consumption") if isinstance(contract.get("one_use_consumption"), dict) else {}
        if str(consumption.get("state") or "") != "ISSUED" or as_int(consumption.get("consumed_uses"), 0) != 0:
            raise PacketError("current_action_class_contract_cancellation_requires_unconsumed_issued_state")
        predecessor = {"contract_id": contract.get("contract_id"), "contract_hash": contract.get("contract_hash")}
        contract = copy.deepcopy(contract)
        contract["one_use_consumption"] = {
            **consumption,
            "state": "CANCELLED",
            "retry_allowed": False,
        }
        contract["cancellation"] = {
            "cancelled_at": now.isoformat(),
            "actor_id": str(actor_id),
            "reason": str(reason),
            "predecessor": predecessor,
        }
        contract_hash = current_action_class_contract_hash(contract)
        contract["contract_hash"] = contract_hash
        contract["contract_id"] = f"acc_{contract_hash[:24]}"
        policy["authority_budget"] = {**budget, "current_action_class_contract": contract}
        write_json_atomic(policy_path, policy)
        append_record(audit_store, {
            "schema_version": CURRENT_ACTION_CLASS_AUDIT_SCHEMA,
            "record_type": "current_action_class_contract_cancelled",
            "contract_id": predecessor["contract_id"],
            "contract_hash": predecessor["contract_hash"],
            "replacement_contract_id": contract["contract_id"],
            "replacement_contract_hash": contract["contract_hash"],
            "actor_provenance": {"actor_id": str(actor_id), "recorded_at": now.isoformat()},
            "reason": str(reason),
            "created_at": now.isoformat(),
        })
    return {
        "status": "CANCELLED_UNCONSUMED",
        "contract": contract,
        "policy_write": True,
        "runtime_apply": False,
        "routing_mutation": False,
        "users_moved": 0,
    }


def _standing_delegated_policy_request_records(records, request_id):
    return [
        record for record in records
        if record.get("record_type") == STANDING_DELEGATED_POLICY_REQUEST_RECORD_TYPE
        and str(record.get("authority_request_id") or "") == str(request_id or "")
    ]


def _standing_delegated_policy_decision_records(records, request_id):
    return [
        record for record in records
        if record.get("record_type") == STANDING_DELEGATED_POLICY_DECISION_RECORD_TYPE
        and str(record.get("authority_request_id") or "") == str(request_id or "")
    ]


def latest_pending_standing_delegated_policy_request(records, *, now=None):
    """Return the newest valid undecided request held by the existing audit owner."""
    now = now or utc_now()
    records = records if isinstance(records, list) else []
    decided = {
        str(record.get("authority_request_id") or "")
        for record in records
        if record.get("record_type") == STANDING_DELEGATED_POLICY_DECISION_RECORD_TYPE
    }
    pending = []
    for record in records:
        if record.get("record_type") != STANDING_DELEGATED_POLICY_REQUEST_RECORD_TYPE:
            continue
        request = record.get("request") if isinstance(record.get("request"), dict) else {}
        request_id = str(request.get("request_id") or record.get("authority_request_id") or "")
        if not request_id or request_id in decided:
            continue
        validation = validate_standing_delegated_policy_authority_request(
            request,
            decision="DECLINE",
            expected_request_id=request_id,
            expected_request_hash=str(record.get("authority_request_hash") or ""),
            now=now,
            allow_decline=True,
        )
        if not validation.get("ok"):
            continue
        pending.append(request)
    pending.sort(key=lambda request: (str(request.get("created_at") or ""), str(request.get("request_id") or "")))
    return {
        "status": "PENDING" if pending else "NONE",
        "pending_count": len(pending),
        "request": copy.deepcopy(pending[-1]) if pending else {},
    }


def register_standing_delegated_policy_request(
    request, *, audit_store=None, producer_id="tools/v7-operator-execution-packet", now=None,
):
    """Append the exact decision preimage without changing live policy."""
    now = now or utc_now()
    validation = validate_standing_delegated_policy_authority_request(
        request, decision="DECLINE", allow_decline=True, now=now,
    )
    if not validation.get("ok"):
        raise PacketError(",".join(validation.get("errors") or ["standing_delegated_policy_request_invalid"]))
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    records = read_audit_records(audit_store)
    existing = _standing_delegated_policy_request_records(records, request["request_id"])
    if existing:
        if (
            len(existing) != 1
            or existing[0].get("authority_request_hash") != request["request_hash"]
            or existing[0].get("request") != request
        ):
            raise PacketError("standing_delegated_policy_request_audit_identity_conflict")
        return {
            "status": "ALREADY_REGISTERED",
            "request_id": request["request_id"],
            "request_hash": request["request_hash"],
            "audit_store": str(audit_store),
            "policy_write": False,
        }
    record = append_record(audit_store, {
        "schema_version": CURRENT_ACTION_CLASS_AUDIT_SCHEMA,
        "record_type": STANDING_DELEGATED_POLICY_REQUEST_RECORD_TYPE,
        "authority_request_id": request["request_id"],
        "authority_request_hash": request["request_hash"],
        "expires_at": request["expires_at"],
        "producer_provenance": {
            "producer_id": str(producer_id),
            "recorded_at": now.isoformat(),
        },
        "request": copy.deepcopy(request),
        "created_at": now.isoformat(),
    })
    return {
        "status": "REGISTERED",
        "request_id": request["request_id"],
        "request_hash": request["request_hash"],
        "audit_store": str(audit_store),
        "record_hash": record["record_hash"],
        "policy_write": False,
    }


def standing_delegated_policy_request_from_audit(
    request_id, request_hash, *, audit_store=None, now=None,
):
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    matches = _standing_delegated_policy_request_records(read_audit_records(audit_store), request_id)
    if len(matches) != 1:
        raise PacketError("standing_delegated_policy_request_audit_missing_or_duplicate")
    record = matches[0]
    request = record.get("request") if isinstance(record.get("request"), dict) else {}
    if record.get("authority_request_hash") != request_hash:
        raise PacketError("standing_delegated_policy_request_audit_hash_mismatch")
    validation = validate_standing_delegated_policy_authority_request(
        request, decision="DECLINE", expected_request_id=request_id,
        expected_request_hash=request_hash, now=now or utc_now(), allow_decline=True,
    )
    if not validation.get("ok"):
        raise PacketError(",".join(validation.get("errors") or ["standing_delegated_policy_request_audit_invalid"]))
    return request


def issue_standing_delegated_policy_from_audit(
    policy_path, *, request_id, request_hash, decision, audit_store=None,
    actor_id="", now=None,
):
    """Activate one bounded standing policy through the existing Authority owner."""
    if decision != "APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY":
        raise PacketError("standing_delegated_policy_decision_not_exact")
    if not str(actor_id or "").strip():
        raise PacketError("standing_delegated_policy_authority_actor_missing")
    now = now or utc_now()
    policy_path = Path(policy_path)
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    with current_action_class_contract_policy_lock(policy_path):
        records = read_audit_records(audit_store)
        if _standing_delegated_policy_decision_records(records, request_id):
            raise PacketError("standing_delegated_policy_authority_decision_already_recorded")
        request = standing_delegated_policy_request_from_audit(
            request_id, request_hash, audit_store=audit_store, now=now,
        )
        validation = validate_standing_delegated_policy_authority_request(
            request, decision=decision, expected_request_id=request_id,
            expected_request_hash=request_hash, now=now,
        )
        if not validation.get("ok"):
            raise PacketError(",".join(validation.get("errors") or ["standing_delegated_policy_request_invalid"]))
        policy_generation_hash = sha256_file(policy_path)
        if request.get("policy_generation_hash") != policy_generation_hash:
            raise PacketError("standing_delegated_policy_generation_changed")
        decision_id = stable_id("sdpdec", {
            "request_id": request_id,
            "request_hash": request_hash,
            "decision": decision,
            "actor_id": str(actor_id),
        })
        decision_record = append_record(audit_store, {
            "schema_version": CURRENT_ACTION_CLASS_AUDIT_SCHEMA,
            "record_type": STANDING_DELEGATED_POLICY_DECISION_RECORD_TYPE,
            "decision_id": decision_id,
            "authority_request_id": request_id,
            "authority_request_hash": request_hash,
            "decision": decision,
            "actor_provenance": {
                "actor_id": str(actor_id),
                "decision_surface": "tools/v7-operator-execution-packet",
                "issuing_owner": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
                "recorded_at": now.isoformat(),
            },
            "created_at": now.isoformat(),
        })
        contract = {
            "schema_version": STANDING_DELEGATED_POLICY_SCHEMA,
            "status": "ACTIVE",
            "issued_at": now.isoformat(),
            "expires_at": (now + timedelta(seconds=STANDING_DELEGATED_POLICY_MAX_TTL_SECONDS)).isoformat(),
            "issuing_owner": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
            "active_program": request["active_program"],
            "policy_scope_hash": request["policy_scope_hash"],
            "policy": copy.deepcopy(request["policy"]),
            "authority_decision": {
                "decision": decision,
                "decision_id": decision_record["decision_id"],
                "request_id": request_id,
                "request_hash": request_hash,
                "actor_id": str(actor_id),
                "decided_at": now.isoformat(),
            },
            "per_action_law": copy.deepcopy(request["per_action_law"]),
        }
        contract_hash = standing_delegated_policy_contract_hash(contract)
        contract["contract_hash"] = contract_hash
        contract["contract_id"] = f"sdpc_{contract_hash[:24]}"
        policy = read_json(policy_path)
        policy["delegated_autonomy_policy"] = contract
        write_json_atomic(policy_path, policy)
        superseded_topology_requests = []
        if (
            request["policy"].get("policy_profile")
            in {
                CONTROLLED_TOPOLOGY_STANDING_POLICY_PROFILE,
                AVAILABILITY_FIRST_STANDING_POLICY_PROFILE,
            }
        ):
            decided_topology_ids = {
                str(record.get("authority_request_id") or "")
                for record in records
                if record.get("record_type")
                == CONTROLLED_SOURCE_TOPOLOGY_DECISION_RECORD_TYPE
            }
            invalidated_topology_ids = {
                str(record.get("authority_request_id") or "")
                for record in records
                if record.get("record_type")
                == CONTROLLED_SOURCE_TOPOLOGY_INVALIDATION_RECORD_TYPE
            }
            for record in records:
                if (
                    record.get("record_type")
                    != CONTROLLED_SOURCE_TOPOLOGY_REQUEST_RECORD_TYPE
                ):
                    continue
                topology_request = (
                    record.get("request")
                    if isinstance(record.get("request"), dict)
                    else {}
                )
                topology_request_id = str(
                    topology_request.get("request_id") or ""
                )
                if (
                    not topology_request_id
                    or topology_request_id in decided_topology_ids
                    or topology_request_id in invalidated_topology_ids
                ):
                    continue
                invalidation_id = stable_id("cstopinv", {
                    "authority_request_id": topology_request_id,
                    "authority_request_hash": str(
                        topology_request.get("request_hash") or ""
                    ),
                    "replacement_request_id": request_id,
                    "replacement_request_hash": request_hash,
                    "reason": (
                        "SUPERSEDED_BY_STANDING_DELEGATED_"
                        "CONTROLLED_TOPOLOGY_POLICY"
                    ),
                })
                append_record(audit_store, {
                    "schema_version": (
                        "v7.controlled-source-topology-authority-"
                        "invalidation.v1"
                    ),
                    "record_type": (
                        CONTROLLED_SOURCE_TOPOLOGY_INVALIDATION_RECORD_TYPE
                    ),
                    "invalidation_id": invalidation_id,
                    "authority_request_id": topology_request_id,
                    "authority_request_hash": str(
                        topology_request.get("request_hash") or ""
                    ),
                    "replacement_request_id": request_id,
                    "replacement_request_hash": request_hash,
                    "replacement_contract_id": contract["contract_id"],
                    "replacement_contract_hash": contract["contract_hash"],
                    "reason": (
                        "SUPERSEDED_BY_STANDING_DELEGATED_"
                        "CONTROLLED_TOPOLOGY_POLICY"
                    ),
                    "producer": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
                    "created_at": now.isoformat(),
                    "authority_decision": False,
                    "topology_materialized": False,
                    "runtime_apply": False,
                    "routing_mutation": False,
                    "users_moved": 0,
                })
                invalidated_topology_ids.add(topology_request_id)
                superseded_topology_requests.append({
                    "request_id": topology_request_id,
                    "request_hash": str(
                        topology_request.get("request_hash") or ""
                    ),
                    "invalidation_id": invalidation_id,
                })
    return {
        "status": "ACTIVATED",
        "policy_path": str(policy_path),
        "contract": contract,
        "authority_owner": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
        "policy_write": True,
        "authority_expanded": True,
        "runtime_apply": False,
        "routing_mutation": False,
        "users_moved": 0,
        "candidate_created": False,
        "packet_created": False,
        "lease_created": False,
        "production_maturity_changed": False,
        "superseded_one_off_topology_requests": (
            superseded_topology_requests
        ),
    }


def _engineering_authority_exact_scope(payload):
    payload = payload if isinstance(payload, dict) else {}
    subject = payload.get("subject") if isinstance(payload.get("subject"), dict) else {}
    scope = payload.get("scope") if isinstance(payload.get("scope"), dict) else {}
    condition = payload.get("controlled_condition") if isinstance(payload.get("controlled_condition"), dict) else {}
    return {
        "program_id": str(payload.get("program_id") or ""),
        "action_class": str(payload.get("action_class") or ""),
        "evidence_cell": str(payload.get("evidence_cell") or ""),
        "user_ip": str(subject.get("user_ip") or ""),
        "certification_user": subject.get("certification_user") is True,
        "ordinary_customer": subject.get("ordinary_customer") is True,
        "max_users": as_int(scope.get("max_users"), 0),
        "max_concurrent_transactions": as_int(scope.get("max_concurrent_transactions"), 0),
        "max_material_outcomes": as_int(scope.get("max_material_outcomes"), 0),
        "source_egress": str(scope.get("source_egress") or ""),
        "source_interface": str(scope.get("source_interface") or ""),
        "source_protocol": str(scope.get("source_protocol") or ""),
        "target_egress": str(scope.get("target_egress") or ""),
        "target_interface": str(scope.get("target_interface") or ""),
        "target_protocol": str(scope.get("target_protocol") or ""),
        "policy_id": str(scope.get("policy_id") or ""),
        "policy_scope_hash": str(scope.get("policy_scope_hash") or ""),
        "controlled_condition": str(condition.get("name") or payload.get("controlled_condition") or ""),
        "rollback_failure_injection": bool(condition.get("rollback_failure_injection")),
        "direct_rollback_invocation_for_evidence": bool(condition.get("direct_rollback_invocation_for_evidence")),
    }


def validate_engineering_authority_repair_continuation(policy, request, *, now=None):
    """Resolve a fresh one-use decision after a repaired pre-apply STOP_SAFE."""
    now = now or utc_now()
    errors: list[str] = []
    policy = policy if isinstance(policy, dict) else {}
    request = request if isinstance(request, dict) else {}
    policy_hash = str(policy.get("policy_hash") or "")
    policy_id = str(policy.get("policy_id") or "")
    if policy.get("schema") != ENGINEERING_AUTHORITY_REPAIR_CONTINUATION_POLICY_SCHEMA:
        errors.append("engineering_authority_repair_policy_schema_invalid")
    if engineering_authority_repair_continuation_policy_hash(policy) != policy_hash:
        errors.append("engineering_authority_repair_policy_hash_mismatch")
    if policy_id != f"engrepair_{policy_hash[:24]}":
        errors.append("engineering_authority_repair_policy_identity_mismatch")
    if policy.get("status") != "APPROVED_EXACT_SCOPE_REPAIR_CONTINUATION":
        errors.append("engineering_authority_repair_policy_not_approved")
    if policy.get("allowed_decision") != ENGINEERING_AUTHORITY_APPROVAL:
        errors.append("engineering_authority_repair_policy_decision_invalid")
    if policy.get("fresh_request_required") is not True or policy.get("approval_reuse_allowed") is not False:
        errors.append("engineering_authority_repair_policy_freshness_invalid")
    if policy.get("background_runtime_allowed") is not False or policy.get("self_expansion_allowed") is not False:
        errors.append("engineering_authority_repair_policy_runtime_scope_invalid")
    if as_int(policy.get("max_users"), 0) != 1 or as_int(policy.get("max_concurrent_transactions"), 0) != 1:
        errors.append("engineering_authority_repair_policy_blast_radius_invalid")

    automatic = request.get("automatic_reissue") if isinstance(request.get("automatic_reissue"), dict) else {}
    if str(automatic.get("policy_id") or "") != policy_id or str(automatic.get("policy_hash") or "") != policy_hash:
        errors.append("engineering_authority_repair_policy_request_binding_mismatch")
    if automatic.get("fresh_request") is not True or automatic.get("reuses_previous_approval") is not False:
        errors.append("engineering_authority_repair_request_not_fresh")
    expected_scope = policy.get("exact_scope") if isinstance(policy.get("exact_scope"), dict) else {}
    actual_scope = _engineering_authority_exact_scope(request)
    if actual_scope != expected_scope:
        errors.append("engineering_authority_repair_exact_scope_mismatch")
    if actual_scope.get("ordinary_customer") or not actual_scope.get("certification_user"):
        errors.append("engineering_authority_repair_subject_invalid")
    if actual_scope.get("rollback_failure_injection") or actual_scope.get("direct_rollback_invocation_for_evidence"):
        errors.append("engineering_authority_repair_condition_expanded")

    previous = request.get("previous_consumed_request") if isinstance(request.get("previous_consumed_request"), dict) else {}
    if str(previous.get("request_id") or "") != str(automatic.get("previous_request_id") or ""):
        errors.append("engineering_authority_repair_previous_request_binding_mismatch")
    if str(previous.get("request_id") or "") == str(request.get("request_id") or ""):
        errors.append("engineering_authority_repair_request_identity_reused")
    if previous.get("reuse_forbidden") is not True:
        errors.append("engineering_authority_repair_previous_reuse_not_forbidden")
    if str(previous.get("terminal") or "") != "CONSUMED_STOP_SAFE_BEFORE_APPLY":
        errors.append("engineering_authority_repair_previous_terminal_invalid")
    if previous.get("apply_executed") is not False or as_int(previous.get("users_moved"), -1) != 0:
        errors.append("engineering_authority_repair_previous_apply_present")
    if previous.get("rollback_attempted") is not False:
        errors.append("engineering_authority_repair_previous_rollback_present")
    if str(previous.get("cleanup_result") or "") != "PASS_EXACT_PRESTATE_RESTORED":
        errors.append("engineering_authority_repair_cleanup_not_proven")
    if not str(previous.get("blocker_fingerprint") or ""):
        errors.append("engineering_authority_repair_blocker_fingerprint_missing")
    if not str(previous.get("repair_commit") or "") or not str(previous.get("repair_deploy_id") or ""):
        errors.append("engineering_authority_repair_deploy_proof_missing")
    if previous.get("repair_tests_passed") is not True or previous.get("truth_convergence_aligned") is not True:
        errors.append("engineering_authority_repair_verification_missing")
    if str(previous.get("repair_commit") or "") != str(request.get("current_commit") or ""):
        errors.append("engineering_authority_repair_commit_binding_mismatch")
    blocker_fingerprint = str(previous.get("blocker_fingerprint") or "")
    prior_fingerprints = {str(value) for value in (automatic.get("prior_repaired_blocker_fingerprints") or []) if str(value)}
    repeated_fingerprint = blocker_fingerprint in prior_fingerprints
    repair_generation = {
        "repair_commit": str(previous.get("repair_commit") or ""),
        "repair_deploy_id": str(previous.get("repair_deploy_id") or ""),
        "repair_binary_sha256": str(previous.get("repair_binary_sha256") or ""),
    }
    if repeated_fingerprint:
        # A blocker fingerprint describes the failed gate, not the deployed
        # implementation which evaluated it.  The same fingerprint may be
        # evaluated exactly once after a newer, independently proven repair
        # generation.  This preserves the anti-loop boundary while avoiding a
        # permanent deadlock where the final repair is deployed only after the
        # one-use request has already been consumed.
        if policy.get("repair_generation_aware") is not True:
            errors.append("engineering_authority_repair_same_blocker_recurred")
        if as_int(policy.get("max_attempts_per_repair_generation"), 0) != 1:
            errors.append("engineering_authority_repair_generation_attempt_budget_invalid")
        if as_int(automatic.get("max_attempts_per_repair_generation"), 0) != 1:
            errors.append("engineering_authority_repair_generation_request_budget_invalid")
        prior_generations = automatic.get("prior_repaired_blocker_generations")
        if not isinstance(prior_generations, list):
            prior_generations = []
        matching_generations = [
            row for row in prior_generations
            if isinstance(row, dict) and str(row.get("blocker_fingerprint") or "") == blocker_fingerprint
        ]
        if not matching_generations:
            errors.append("engineering_authority_repair_generation_history_missing")
        if not all(repair_generation.values()):
            errors.append("engineering_authority_repair_generation_proof_missing")
        for row in matching_generations:
            prior_generation = (
                str(row.get("repair_commit") or ""),
                str(row.get("repair_deploy_id") or ""),
                str(row.get("repair_binary_sha256") or ""),
            )
            if not all(prior_generation):
                errors.append("engineering_authority_repair_generation_history_invalid")
            if prior_generation == tuple(repair_generation.values()):
                errors.append("engineering_authority_repair_generation_already_attempted")
        terminal_at = str(previous.get("terminal_at") or "")
        deployed_at = str(previous.get("repair_deployed_at") or "")
        if previous.get("repair_deployed_after_terminal") is not True or not terminal_at or not deployed_at:
            errors.append("engineering_authority_repair_generation_order_unproven")
        else:
            try:
                if parse_ts(deployed_at) <= parse_ts(terminal_at):
                    errors.append("engineering_authority_repair_generation_not_newer_than_terminal")
            except PacketError:
                errors.append("engineering_authority_repair_generation_timestamp_invalid")
    return {
        "ok": not errors,
        "errors": sorted(set(errors)),
        "decision": ENGINEERING_AUTHORITY_APPROVAL if not errors else "",
        "decision_provenance": "USER_APPROVED_EXACT_SCOPE_REPAIR_CONTINUATION_POLICY" if not errors else "DENIED",
        "policy_id": policy_id,
        "policy_hash": policy_hash,
        "request_id": str(request.get("request_id") or ""),
        "evaluated_at": now.isoformat(),
        "approval_reused": False,
        "fresh_one_use_request_required": True,
        "repeated_blocker_fingerprint": repeated_fingerprint,
        "repair_generation": repair_generation,
    }


def validate_engineering_authority_request(
    request,
    *,
    decision,
    expected_request_id="",
    expected_contract_hash="",
    now=None,
):
    now = now or utc_now()
    errors = []
    request = request if isinstance(request, dict) else {}
    request_id = str(request.get("request_id") or "")
    contract_hash = str(request.get("contract_hash") or "")
    if request.get("schema") != ENGINEERING_AUTHORITY_REQUEST_SCHEMA:
        errors.append("engineering_authority_request_schema_invalid")
    if engineering_authority_request_hash(request) != contract_hash:
        errors.append("engineering_authority_contract_hash_mismatch")
    if request_id != f"engauth_r1_{contract_hash[:24]}":
        errors.append("engineering_authority_request_identity_mismatch")
    if expected_request_id and request_id != expected_request_id:
        errors.append("engineering_authority_expected_request_mismatch")
    if expected_contract_hash and contract_hash != expected_contract_hash:
        errors.append("engineering_authority_expected_contract_mismatch")
    if decision != ENGINEERING_AUTHORITY_APPROVAL:
        errors.append("engineering_authority_decision_not_exact_approval")
    if decision not in set(request.get("decision_set") or []):
        errors.append("engineering_authority_decision_not_allowed")
    if request.get("status") != "AWAITING_INDEPENDENT_AUTHORITY_DECISION":
        errors.append("engineering_authority_request_not_pending")
    try:
        if now >= parse_ts(request.get("expires_at")):
            errors.append("engineering_authority_request_expired")
    except PacketError:
        errors.append("engineering_authority_expiry_invalid")
    one_use = request.get("one_use_law") if isinstance(request.get("one_use_law"), dict) else {}
    if as_int(one_use.get("approval_use_limit"), 0) != 1:
        errors.append("engineering_authority_use_limit_invalid")
    if one_use.get("implicit_renewal") is not False or one_use.get("retry_under_same_approval") is not False:
        errors.append("engineering_authority_one_use_law_invalid")
    scope = request.get("scope") if isinstance(request.get("scope"), dict) else {}
    subject = request.get("subject") if isinstance(request.get("subject"), dict) else {}
    if as_int(scope.get("max_users"), 0) != 1 or as_int(scope.get("max_concurrent_transactions"), 0) != 1:
        errors.append("engineering_authority_blast_radius_invalid")
    if not subject.get("certification_user") or subject.get("ordinary_customer") is not False:
        errors.append("engineering_authority_subject_invalid")
    return {
        "ok": not errors,
        "errors": sorted(set(errors)),
        "request_id": request_id,
        "contract_hash": contract_hash,
        "decision": decision,
        "expires_at": request.get("expires_at", ""),
    }


def engineering_authority_binding_from_preview(
    request,
    preview,
    *,
    decision,
    expected_request_id="",
    expected_contract_hash="",
    now=None,
):
    now = now or utc_now()
    validation = validate_engineering_authority_request(
        request,
        decision=decision,
        expected_request_id=expected_request_id,
        expected_contract_hash=expected_contract_hash,
        now=now,
    )
    if not validation.get("ok"):
        raise PacketError(",".join(validation.get("errors") or ["engineering_authority_request_invalid"]))
    selected = selected_moves_from_preview(extract_packet_preview(preview))
    moves = selected.get("moves") if isinstance(selected.get("moves"), list) else []
    if len(moves) != 1:
        raise PacketError("engineering_authority_selected_move_count_not_one")
    move = moves[0]
    request_scope = request.get("scope") if isinstance(request.get("scope"), dict) else {}
    subject = request.get("subject") if isinstance(request.get("subject"), dict) else {}
    expected = {
        "user": str(subject.get("user_ip") or ""),
        "source": str(request_scope.get("source_egress") or ""),
        "target": str(request_scope.get("target_egress") or ""),
    }
    actual = {
        "user": str(move.get("user_ip") or ""),
        "source": str(move.get("current_egress") or ""),
        "target": str(move.get("recommended_egress") or ""),
    }
    if actual != expected:
        raise PacketError("engineering_authority_candidate_scope_mismatch:" + sha256_json({"expected": expected, "actual": actual}))
    return {
        "schema_version": ENGINEERING_AUTHORITY_BINDING_SCHEMA,
        "decision": decision,
        "decision_recorded_at": now.isoformat(),
        "request_id": validation["request_id"],
        "contract_hash": validation["contract_hash"],
        "expires_at": validation["expires_at"],
        "transaction_nonce": secrets.token_hex(24),
        "approval_use_limit": 1,
        "implicit_renewal": False,
        "retry_under_same_approval": False,
        "evidence_cell": str(request.get("evidence_cell") or ""),
        "controlled_condition": str((request.get("controlled_condition") or {}).get("name") or ""),
        "subject": expected,
        "policy_id": str(request_scope.get("policy_id") or ""),
        "policy_scope_hash": str(request_scope.get("policy_scope_hash") or ""),
        "request": copy.deepcopy(request),
    }


def validate_engineering_authority_binding(packet, errors, *, now=None):
    binding = packet.get("engineering_authority")
    if not isinstance(binding, dict) or not binding:
        return
    now = now or utc_now()
    if binding.get("schema_version") != ENGINEERING_AUTHORITY_BINDING_SCHEMA:
        errors.append("engineering_authority_binding_schema_invalid")
        return
    validation = validate_engineering_authority_request(
        binding.get("request"),
        decision=str(binding.get("decision") or ""),
        expected_request_id=str(binding.get("request_id") or ""),
        expected_contract_hash=str(binding.get("contract_hash") or ""),
        now=now,
    )
    errors.extend(validation.get("errors") or [])
    if not str(binding.get("transaction_nonce") or ""):
        errors.append("engineering_authority_transaction_nonce_missing")
    if as_int(binding.get("approval_use_limit"), 0) != 1:
        errors.append("engineering_authority_binding_use_limit_invalid")
    constraints = packet.get("constraints") if isinstance(packet.get("constraints"), dict) else {}
    rollback_items = ((packet.get("rollback_manifest") or {}).get("items") or [])
    subject = binding.get("subject") if isinstance(binding.get("subject"), dict) else {}
    if constraints.get("allowed_users") != [subject.get("user")]:
        errors.append("engineering_authority_packet_user_mismatch")
    if constraints.get("allowed_targets") != [subject.get("target")]:
        errors.append("engineering_authority_packet_target_mismatch")
    if len(rollback_items) != 1 or str((rollback_items[0] or {}).get("rollback_target") or "") != str(subject.get("source") or ""):
        errors.append("engineering_authority_packet_source_mismatch")
    delegated = packet.get("delegated_policy_authority") if isinstance(packet.get("delegated_policy_authority"), dict) else {}
    if str(delegated.get("policy_id") or "") != str(binding.get("policy_id") or ""):
        errors.append("engineering_authority_policy_id_mismatch")
    if str(delegated.get("policy_scope_hash") or "") != str(binding.get("policy_scope_hash") or ""):
        errors.append("engineering_authority_policy_scope_hash_mismatch")


def validate_approvals(packet, errors, *, now=None):
    authority = packet.get("delegated_policy_authority")
    if isinstance(authority, dict) and authority:
        if authority.get("authority_basis") != "DELEGATED_AUTONOMY_POLICY":
            errors.append("delegated_policy_authority_basis_invalid")
        if not authority.get("policy_id"):
            errors.append("delegated_policy_id_missing")
        if not authority.get("policy_scope_hash"):
            errors.append("delegated_policy_scope_hash_missing")
        normalized_scope = authority.get("normalized_scope") if isinstance(authority.get("normalized_scope"), dict) else {}
        if not normalized_scope:
            errors.append("delegated_policy_normalized_scope_missing")
        elif sha256_json(normalized_scope) != authority.get("policy_scope_hash"):
            errors.append("delegated_policy_scope_hash_mismatch")
        if authority.get("policy_state") != "APPROVED":
            errors.append("delegated_policy_not_approved")
        if authority.get("current_mode") != "DELEGATED_AUTONOMY":
            errors.append("delegated_policy_mode_invalid")
        allowed_action_classes = set(normalized_scope.get("allowed_action_classes") or [])
        action_class = str(authority.get("action_class") or "")
        topology_action = (
            action_class == CONTROLLED_TOPOLOGY_DELEGATED_ACTION_CLASS
        )
        availability_first_action = (
            action_class == AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS
        )
        if action_class not in allowed_action_classes:
            errors.append("delegated_policy_action_class_invalid")
        authorized_max_users = as_int(normalized_scope.get("max_users_per_action"), 0)
        action_class_scopes = (
            normalized_scope.get("action_class_scopes")
            if isinstance(normalized_scope.get("action_class_scopes"), dict)
            else {}
        )
        topology_scope = (
            action_class_scopes.get(CONTROLLED_TOPOLOGY_DELEGATED_ACTION_CLASS)
            if isinstance(
                action_class_scopes.get(
                    CONTROLLED_TOPOLOGY_DELEGATED_ACTION_CLASS
                ),
                dict,
            )
            else {}
        )
        availability_first_scope = (
            action_class_scopes.get(AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS)
            if isinstance(
                action_class_scopes.get(
                    AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS
                ),
                dict,
            )
            else {}
        )
        if topology_action:
            if (
                normalized_scope.get("policy_profile")
                not in {
                    CONTROLLED_TOPOLOGY_STANDING_POLICY_PROFILE,
                    AVAILABILITY_FIRST_STANDING_POLICY_PROFILE,
                }
            ):
                errors.append("delegated_topology_policy_profile_invalid")
            if as_int(authority.get("max_users_per_transaction"), 0) != 1:
                errors.append("delegated_topology_blast_radius_invalid")
            if as_int(topology_scope.get("max_users_per_transaction"), 0) != 1:
                errors.append("delegated_topology_scope_blast_radius_invalid")
            if as_int(topology_scope.get("max_concurrent_transactions"), 0) != 1:
                errors.append("delegated_topology_scope_concurrency_invalid")
            if list(topology_scope.get("allowed_actions") or []) != [
                "REBIND_CONTROLLED_CERTIFICATION_SOURCE"
            ]:
                errors.append("delegated_topology_allowed_actions_invalid")
            if topology_scope.get("certification_identities_only") is not True:
                errors.append("delegated_topology_certification_identity_fence_missing")
            if topology_scope.get("ordinary_assignment_mutation_allowed") is not False:
                errors.append("delegated_topology_ordinary_assignment_fence_invalid")
            if as_int(topology_scope.get("ordinary_identity_delta"), -1) != 0:
                errors.append("delegated_topology_ordinary_identity_delta_invalid")
            if as_int(topology_scope.get("ordinary_route_delta"), -1) != 0:
                errors.append("delegated_topology_ordinary_route_delta_invalid")
        elif availability_first_action:
            if (
                normalized_scope.get("policy_profile")
                != AVAILABILITY_FIRST_STANDING_POLICY_PROFILE
            ):
                errors.append(
                    "delegated_availability_first_policy_profile_invalid"
                )
            transaction_users = as_int(
                authority.get("max_users_per_transaction"), 0
            )
            scope_users = as_int(
                availability_first_scope.get("max_users_per_transaction"), 0
            )
            if (
                transaction_users < 1
                or transaction_users > scope_users
                or scope_users != authorized_max_users
            ):
                errors.append(
                    "delegated_availability_first_blast_radius_invalid"
                )
            if (
                list(
                    availability_first_scope.get("allowed_actions") or []
                )
                != list(AVAILABILITY_FIRST_ALLOWED_ACTIONS)
            ):
                errors.append(
                    "delegated_availability_first_actions_invalid"
                )
            if (
                list(availability_first_scope.get("ladder") or [])
                != list(AVAILABILITY_FIRST_LADDER)
            ):
                errors.append(
                    "delegated_availability_first_ladder_invalid"
                )
            if not str(
                authority.get(
                    "availability_first_allocation_fingerprint"
                )
                or ""
            ):
                errors.append(
                    "delegated_availability_first_allocation_missing"
                )
            if not str(
                authority.get("availability_first_subset_fingerprint")
                or ""
            ):
                errors.append(
                    "delegated_availability_first_subset_missing"
                )
            if not str(
                authority.get("controlled_certification_target_id")
                or ""
            ):
                errors.append(
                    "delegated_availability_first_target_missing"
                )
            for field, expected in {
                "certification_identities_only": True,
                "max_concurrent_transactions": 1,
                "ordinary_identity_delta": 0,
                "ordinary_route_delta": 0,
                "ordinary_assignment_mutation_allowed": False,
                "ordinary_reclassification_allowed": False,
                "shared_target_fault_injection_allowed": False,
                "shared_target_restart_allowed": False,
                "capacity_double_counting_forbidden": True,
                "source_target_collision_forbidden": True,
                "immutable_allocation_required": True,
                "fresh_inventory_required": True,
                "fresh_candidate_required": True,
                "fresh_packet_or_packet_set_required": True,
                "fresh_lease_required": True,
                "restore_barrier_before_apply_required": True,
                "per_user_verification_required": True,
                "per_target_verification_required": True,
                "aggregate_verification_required": True,
                "ordinary_user_quality_verification_required": True,
                "cohort_circuit_breaker_required": True,
                "partial_target_containment_required": True,
                "rollback_or_redistribution_required": True,
                "baseline_reset_between_stages_required": True,
                "authority_self_expansion_allowed": False,
            }.items():
                if availability_first_scope.get(field) != expected:
                    errors.append(
                        "delegated_availability_first_scope_"
                        + field
                        + "_invalid"
                    )
        else:
            transaction_users = as_int(
                authority.get("max_users_per_transaction"), 0
            )
            # The standing policy's ``max_users_per_action`` is an upper
            # bound, not a requirement to consume its entire blast radius.
            # A fresh ordinary service-failure cohort may therefore use a
            # smaller already-qualified tier (for example 4 under the active
            # tier-48 contract).  It must still name the exact existing
            # service-failure action class and may never exceed that ceiling.
            transaction_action_class = SERVICE_FAILURE_DELEGATED_ACTION_CLASSES.get(
                transaction_users, ""
            )
            if (
                authorized_max_users not in SERVICE_FAILURE_DELEGATED_ACTION_CLASSES
                or transaction_users < 1
                or transaction_users > authorized_max_users
                or action_class != transaction_action_class
            ):
                errors.append("delegated_policy_blast_radius_invalid")
        if as_int(authority.get("max_concurrent_transactions"), 0) != 1:
            errors.append("delegated_policy_concurrency_invalid")
        if authority.get("candidate_identity") != "FRESH_ONLY":
            errors.append("delegated_policy_candidate_freshness_invalid")
        if authority.get("packet_reuse") != "FORBIDDEN":
            errors.append("delegated_policy_packet_reuse_invalid")
        if authority.get("self_expansion_allowed") is not False:
            errors.append("delegated_policy_self_expansion_invalid")
        if authority.get("authority_audit_verified") is not True:
            errors.append("delegated_policy_authority_audit_not_verified")
        standing_contract = authority.get("standing_policy_contract") if isinstance(authority.get("standing_policy_contract"), dict) else {}
        standing_validation = validate_standing_delegated_operational_policy(standing_contract, now=now)
        if not standing_validation.get("ok"):
            errors.extend(standing_validation.get("errors") or ["standing_delegated_policy_contract_invalid"])
        elif normalized_delegated_scope := (
            standing_validation.get("policy") if isinstance(standing_validation.get("policy"), dict) else {}
        ):
            from admin_core import autonomy_trust_acceleration
            if autonomy_trust_acceleration.normalized_delegated_autonomy_scope(normalized_delegated_scope) != normalized_scope:
                errors.append("standing_delegated_policy_packet_scope_mismatch")
        if normalized_scope:
            expected_action_class = SERVICE_FAILURE_DELEGATED_ACTION_CLASSES.get(authorized_max_users, "")
            combined_profile = (
                normalized_scope.get("policy_profile")
                in {
                    CONTROLLED_TOPOLOGY_STANDING_POLICY_PROFILE,
                    AVAILABILITY_FIRST_STANDING_POLICY_PROFILE,
                }
            )
            availability_profile = (
                normalized_scope.get("policy_profile")
                == AVAILABILITY_FIRST_STANDING_POLICY_PROFILE
            )
            expected_action_classes = (
                [
                    expected_action_class,
                    CONTROLLED_TOPOLOGY_DELEGATED_ACTION_CLASS,
                    *(
                        [AVAILABILITY_FIRST_DELEGATED_ACTION_CLASS]
                        if availability_profile else []
                    ),
                ]
                if combined_profile
                else [expected_action_class]
            )
            if normalized_scope.get("allowed_action_classes") != expected_action_classes:
                errors.append("delegated_policy_normalized_action_classes_invalid")
            if authorized_max_users not in SERVICE_FAILURE_DELEGATED_ACTION_CLASSES:
                errors.append("delegated_policy_normalized_blast_radius_invalid")
            if as_int(normalized_scope.get("max_concurrent_transactions"), 0) != 1:
                errors.append("delegated_policy_normalized_concurrency_invalid")
            if normalized_scope.get("required_anti_flap") != "PASS":
                errors.append("delegated_policy_anti_flap_invalid")
            if not normalized_scope.get("required_freshness"):
                errors.append("delegated_policy_freshness_requirements_missing")
            if not normalized_scope.get("required_verification"):
                errors.append("delegated_policy_verification_requirements_missing")
            if not normalized_scope.get("required_rollback"):
                errors.append("delegated_policy_rollback_requirement_missing")
            if normalized_scope.get("final_safe_mode") != "OPEN":
                errors.append("delegated_policy_final_safe_mode_invalid")
            if normalized_scope.get("operator_packet_approval_required") is not False:
                errors.append("delegated_policy_packet_approval_not_retired")
        if packet.get("approvals") not in ([], None):
            errors.append("operator_approvals_present_for_delegated_packet")
        validate_engineering_authority_binding(packet, errors, now=now)
        return
    approvals = packet.get("approvals") or []
    if len(approvals) != 2:
        errors.append("dual_confirmation_missing")
        return
    first = approvals[0].get("operator_id")
    second = approvals[1].get("operator_id")
    if not first or not second:
        errors.append("operator_id_missing")
    if first == second:
        errors.append("dual_confirmation_same_actor")
    roles = {row.get("role") for row in approvals}
    if not {"approval_author", "approval_reviewer"}.issubset(roles):
        errors.append("approval_roles_invalid")


def validate_expiry(packet, now, errors):
    try:
        expires_at = parse_ts(packet.get("expires_at"))
        if now >= expires_at:
            errors.append("approval_expired")
    except PacketError:
        errors.append("expires_at_invalid")


def validate_zero_packet(packet, now):
    errors = []
    if packet.get("schema_version") != ZERO_PACKET_SCHEMA:
        errors.append("schema_version_invalid")
    if packet.get("selected_first_action") != ZERO_ACTION:
        errors.append("unsupported_action")
    if packet.get("runtime_action") not in {RUNTIME_ACTION_RECORD_ONLY, RUNTIME_ACTION_ZERO_MOVE_GOVERNANCE}:
        errors.append("runtime_action_not_allowed")
    constraints = packet.get("constraints") or {}
    if as_int(constraints.get("selected_move_budget"), -1) != 0:
        errors.append("selected_move_budget_not_zero")
    if constraints.get("allowed_users") not in ([], None):
        errors.append("allowed_users_not_empty")
    if constraints.get("allowed_targets") not in ([], None):
        errors.append("allowed_targets_not_empty")
    if constraints.get("user_movement_allowed") is not False:
        errors.append("user_movement_not_forbidden")
    if constraints.get("routing_mutation_allowed") is not False:
        errors.append("routing_mutation_not_forbidden")
    validate_approvals(packet, errors, now=now)
    validate_expiry(packet, now, errors)
    expected = packet.get("expected") or {}
    if expected.get("selected_move_hash") != EMPTY_SELECTED_MOVES_HASH:
        errors.append("selected_move_hash_invalid_for_zero_budget")
    if not expected.get("generation_id"):
        errors.append("generation_id_missing")
    if errors:
        return {"ok": False, "verdict": "DENY_PACKET_INVALID", "errors": errors}
    return {"ok": True, "verdict": "PACKET_VALID", "errors": []}


def validate_nonzero_packet(packet, now):
    errors = []
    if packet.get("schema_version") != GOVERNANCE_PACKET_SCHEMA:
        errors.append("schema_version_invalid")
    if packet.get("selected_first_action") != NONZERO_ACTION:
        errors.append("unsupported_action")
    if packet.get("runtime_action") != RUNTIME_ACTION_CREATE_CLEARANCE:
        errors.append("runtime_action_not_allowed")
    constraints = packet.get("constraints") or {}
    budget = as_int(constraints.get("selected_move_budget"), -1)
    allowed_users = constraints.get("allowed_users") or []
    allowed_targets = constraints.get("allowed_targets") or []
    if budget <= 0:
        errors.append("selected_move_budget_not_positive")
    if not allowed_users:
        errors.append("allowed_users_missing")
    if not allowed_targets:
        errors.append("allowed_targets_missing")
    if constraints.get("user_movement_allowed") is not False:
        errors.append("user_movement_not_forbidden_for_clearance_action")
    if constraints.get("routing_mutation_allowed") is not False:
        errors.append("routing_mutation_not_forbidden")
    if constraints.get("autoswitch_apply_allowed") is not False:
        errors.append("autoswitch_apply_not_forbidden_for_clearance_action")
    validate_approvals(packet, errors, now=now)
    validate_expiry(packet, now, errors)
    expected = packet.get("expected") or {}
    if not expected.get("generation_id"):
        errors.append("generation_id_missing")
    if not expected.get("selected_move_hash") or expected.get("selected_move_hash") == EMPTY_SELECTED_MOVES_HASH:
        errors.append("selected_move_hash_missing_for_nonzero_budget")
    if as_int(expected.get("selected_move_count"), 0) <= 0:
        errors.append("selected_move_count_not_positive")
    if expected.get("selected_move_count") and budget < as_int(expected.get("selected_move_count"), 0):
        errors.append("selected_move_budget_below_expected_count")
    if not expected.get("atomic_execution_envelope_id"):
        errors.append("atomic_execution_envelope_id_missing")
    if not expected.get("atomic_execution_envelope_hash"):
        errors.append("atomic_execution_envelope_hash_missing")
    strict_binding = bool((packet.get("execution_metadata") or {}).get("operation_scoped_binding_required"))
    if strict_binding:
        if not expected.get("source_bundle_hash"):
            errors.append("source_bundle_hash_missing")
        source_hashes = expected.get("source_hashes") if isinstance(expected.get("source_hashes"), dict) else {}
        normalized_source_hashes = {str(key): str(value) for key, value in source_hashes.items() if str(key) and str(value)}
        if not normalized_source_hashes:
            errors.append("source_hashes_missing")
        elif sha256_json(normalized_source_hashes) != str(expected.get("source_bundle_hash") or ""):
            errors.append("source_bundle_hash_mismatch")
        if not expected.get("snapshot_bundle_hash"):
            errors.append("snapshot_bundle_hash_missing")
        if not str(packet.get("breaker_generation") or "") or packet.get("breaker_generation") == "UNBOUND_READ_ONLY":
            errors.append("breaker_generation_unbound")
    rollback_manifest = packet.get("rollback_manifest") or {}
    rollback_items = rollback_manifest.get("items") or []
    if not rollback_manifest.get("rollback_manifest_id"):
        errors.append("rollback_manifest_id_missing")
    if len(rollback_items) != as_int(expected.get("selected_move_count"), 0):
        errors.append("rollback_manifest_count_mismatch")
    for item in rollback_items:
        if not item.get("user_ip") or not item.get("rollback_target") or not item.get("source_operation_id"):
            errors.append("rollback_manifest_item_incomplete")
            break
    # Generic packets have no incident lineage.  A packet which claims the
    # existing Matrix lineage must be complete and source-bound, so later
    # outcome consumption never reconstructs causality from timing alone.
    causal_binding = packet.get("service_failure_causal_binding")
    if causal_binding is not None:
        if not isinstance(causal_binding, dict):
            errors.append("service_failure_causal_binding_invalid")
        else:
            source_incident_id = str(causal_binding.get("source_incident_id") or "")
            source_event_id = str(causal_binding.get("source_event_id") or "")
            source_event_ids = causal_binding.get("source_event_ids")
            source_event_ids = source_event_ids if isinstance(source_event_ids, list) else []
            bound_source = str(causal_binding.get("source_channel") or "")
            event_type = str(causal_binding.get("event_type") or "")
            if not source_incident_id or not (source_event_id or source_event_ids):
                errors.append("service_failure_causal_binding_identity_missing")
            if event_type not in {"SERVICE_FAILURE_OBSERVED", "SERVICE_FAILURE_REVALIDATED"}:
                errors.append("service_failure_causal_binding_event_type_invalid")
            source_scope = causal_binding.get("source_scope")
            source_scope = source_scope if isinstance(source_scope, dict) else {}
            if (
                int(source_scope.get("affected_scope_count") or 0) <= 0
                or not str(source_scope.get("affected_scope_fingerprint") or "")
                or str(source_scope.get("source_channel") or "") != bound_source
                or bool(source_scope.get("raw_user_list_stored"))
            ):
                errors.append("service_failure_causal_binding_source_scope_invalid")
            rollback_sources = {
                str(item.get("rollback_target") or "")
                for item in rollback_items
                if isinstance(item, dict) and str(item.get("rollback_target") or "")
            }
            if not bound_source or rollback_sources != {bound_source}:
                errors.append("service_failure_causal_binding_source_mismatch")
    if errors:
        return {"ok": False, "verdict": "DENY_PACKET_INVALID", "errors": sorted(set(errors))}
    return {"ok": True, "verdict": "PACKET_VALID", "errors": []}


def validate_packet(packet, now=None):
    now = now or utc_now()
    if is_zero_packet(packet):
        return validate_zero_packet(packet, now)
    if is_nonzero_clearance_packet(packet):
        return validate_nonzero_packet(packet, now)
    return {"ok": False, "verdict": "DENY_PACKET_INVALID", "errors": ["unsupported_action"]}


def selected_moves_state(state_dir):
    candidates = [
        Path(state_dir) / "selected-moves.json",
        Path(state_dir) / "selected_moves.json",
        Path(state_dir) / "current-selected-moves.json",
    ]
    for path in candidates:
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"count": -1, "hash": "", "source": str(path), "error": "selected_moves_unreadable"}
        moves = data.get("selected_moves", data if isinstance(data, list) else [])
        return {"count": len(moves), "hash": sha256_bytes(canonical_json(moves).encode("utf-8")), "source": str(path)}
    return {"count": 0, "hash": EMPTY_SELECTED_MOVES_HASH, "source": "missing_treated_as_empty"}


def selected_moves_from_plan(plan):
    barrier = ((plan.get("safety") or {}).get("restore_barrier") or {})
    selected_count = as_int(barrier.get("clearance_selected_moves_before_guard"), 0)
    selected_hash = str(barrier.get("clearance_selected_moves_hash") or "")
    moves = []
    selected_moves = plan.get("selected_moves") or []
    approved_candidates = barrier.get("approved_candidate_moves_before_guard") or []
    if not isinstance(approved_candidates, list):
        approved_candidates = []
    diagnostics = ((plan.get("safety") or {}).get("selected_moves_diagnostics") or {})
    pre_restore_rows = diagnostics.get("selected_moves_before_restore_barrier_rows") if isinstance(diagnostics, dict) else []
    if not isinstance(pre_restore_rows, list):
        pre_restore_rows = []
    decisions = plan.get("decisions") or []
    constraints = None
    semantic_rows_by_identity = {}
    if isinstance(decisions, list):
        for row in decisions:
            if not isinstance(row, dict):
                continue
            identity = (
                str(row.get("user_ip") or row.get("user") or ""),
                str(row.get("current_egress") or row.get("from") or ""),
                str(row.get("recommended_egress") or row.get("to") or ""),
            )
            if all(identity):
                semantic_rows_by_identity.setdefault(identity, row)

    if selected_moves:
        source_rows = selected_moves
        source_kind = "selected_moves"
    elif approved_candidates:
        source_rows = approved_candidates
        source_kind = "approved_candidate_moves_before_guard"
    elif pre_restore_rows:
        source_rows = pre_restore_rows
        source_kind = "selected_moves_before_restore_barrier_rows"
    else:
        source_rows = decisions
        source_kind = "decisions"
    for row in source_rows:
        if source_kind != "decisions" or (
            row.get("action") == "switch"
            and row.get("recommended_egress") != row.get("current_egress")
        ):
            user_ip = str(row.get("user_ip") or row.get("user") or "")
            current_egress = str(row.get("current_egress") or row.get("from") or "")
            recommended_egress = str(row.get("recommended_egress") or row.get("to") or "")
            move = {
                "user_ip": user_ip,
                "current_egress": current_egress,
                "recommended_egress": recommended_egress,
                "move_type": str(row.get("move_type") or ""),
            }
            for key in SELECTED_MOVE_SEMANTIC_FIELDS:
                if key in row:
                    move[key] = copy.deepcopy(row.get(key))
            semantic_row = semantic_rows_by_identity.get((user_ip, current_egress, recommended_egress))
            if isinstance(semantic_row, dict):
                for key in SELECTED_MOVE_SEMANTIC_FIELDS:
                    if key not in move and key in semantic_row:
                        move[key] = copy.deepcopy(semantic_row.get(key))
            moves.append(move)
    if selected_count > 0 and len(moves) > selected_count:
        moves = moves[:selected_count]
    if not selected_hash and moves:
        selected_hash = sha256_bytes(canonical_json([
            {
                "user_ip": move["user_ip"],
                "from": move["current_egress"],
                "to": move["recommended_egress"],
                "move_type": move["move_type"],
            }
            for move in moves
        ]).encode("utf-8"))
    if selected_count <= 0:
        selected_count = len(moves)
    if moves:
        constraints = {
            "allowed_users": [move["user_ip"] for move in moves],
            "allowed_targets": sorted({move["recommended_egress"] for move in moves}),
        }
    generation = ((plan.get("safety") or {}).get("generation") or {})
    atomic_envelope = ((plan.get("safety") or {}).get("atomic_execution_envelope") or {})
    source_hashes = ((atomic_envelope.get("source_bundle") or {}).get("source_hashes") or {})
    snapshot_bundle_hash = atomic_envelope.get("snapshot_bundle_hash", "")
    source_bundle_hash = atomic_envelope.get("source_bundle_hash", "")
    runtime_snapshot_hash = (plan.get("operation") or {}).get("runtime_snapshot_hash", "")
    atomic_envelope_id = atomic_envelope.get("envelope_id", "")
    atomic_envelope_hash = atomic_envelope.get("envelope_hash", "")
    if moves and selected_hash and source_hashes and snapshot_bundle_hash:
        source_bundle_hash = sha256_json(source_hashes)
        runtime_snapshot_hash = sha256_json({
            "users_registry_hash": source_hashes.get("users_registry", ""),
            "egress_registry_hash": source_hashes.get("egress_registry", ""),
            "selected_move_hash": selected_hash,
        })
        envelope_payload = {
            "planner_generation_id": generation.get("planner_generation_id") or (plan.get("operation") or {}).get("planner_generation_id", ""),
            "selected_move_hash": selected_hash,
            "selected_move_count": selected_count,
            "runtime_snapshot_hash": runtime_snapshot_hash,
            "source_bundle_hash": source_bundle_hash,
            "snapshot_bundle_hash": snapshot_bundle_hash,
        }
        atomic_envelope_hash = sha256_json(envelope_payload)
        atomic_envelope_id = "aee_" + atomic_envelope_hash[:24]
    return {
        "planner_generation_id": generation.get("planner_generation_id") or (plan.get("operation") or {}).get("planner_generation_id", ""),
        "selected_move_hash": selected_hash,
        "selected_move_count": selected_count,
        "moves": moves,
        "constraints": constraints or {},
        "runtime_snapshot_hash": runtime_snapshot_hash,
        "atomic_execution_envelope_id": atomic_envelope_id,
        "atomic_execution_envelope_hash": atomic_envelope_hash,
        "source_bundle_hash": source_bundle_hash,
        "source_hashes": source_hashes,
        "snapshot_bundle_hash": snapshot_bundle_hash,
    }


def approved_plan_lock_from_selected(selected, packet, packet_hash):
    moves = selected.get("moves") or []
    constraints = selected.get("constraints") or {}
    payload = {
        "schema_version": "v7.approved-plan-lock.v1",
        "identity_source": selected.get("identity_source", ""),
        "decision_id": selected.get("decision_id", ""),
        "authority_generation": selected.get("authority_generation", ""),
        "planner_generation_id": selected.get("planner_generation_id", ""),
        "selected_move_hash": selected.get("selected_move_hash", ""),
        "selected_move_count": as_int(selected.get("selected_move_count"), 0),
        "selected_moves": [
            {
                **{
                    "user_ip": move["user_ip"],
                    "current_egress": move["current_egress"],
                    "recommended_egress": move["recommended_egress"],
                    "move_type": move.get("move_type", ""),
                },
                **{
                    key: copy.deepcopy(move.get(key))
                    for key in SELECTED_MOVE_SEMANTIC_FIELDS
                    if key in move
                },
            }
            for move in moves
        ],
        "allowed_users": constraints.get("allowed_users") or [],
        "allowed_targets": constraints.get("allowed_targets") or [],
        "atomic_execution_envelope_id": selected.get("atomic_execution_envelope_id", ""),
        "atomic_execution_envelope_hash": selected.get("atomic_execution_envelope_hash", ""),
        "source_bundle_hash": selected.get("source_bundle_hash", ""),
        "source_hashes": selected.get("source_hashes", {}),
        "snapshot_bundle_hash": selected.get("snapshot_bundle_hash", ""),
        "users_registry_hash": ((packet.get("expected") or {}).get("users_registry_hash") or ""),
        "egress_registry_hash": ((packet.get("expected") or {}).get("egress_registry_hash") or ""),
        "packet_id": packet.get("packet_id", ""),
        "operation_id": packet.get("operation_id", ""),
        "packet_hash": packet_hash,
        "restore_barrier_id": "",
        "restore_barrier_hash": "",
        "expires_at": packet.get("expires_at", ""),
        "owner": CANONICAL_CLEARANCE_OWNER,
        "executor_may_reselect": False,
        "executor_may_replace_users": False,
        "executor_may_replace_targets": False,
    }
    payload["lock_id"] = stable_id("apl", payload)
    payload["lock_hash"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    return payload


def _packet_identity(packet):
    expected = packet.get("expected") or {}
    constraints = packet.get("constraints") or {}
    rollback_manifest = packet.get("rollback_manifest") or {}
    lock = packet.get("approved_plan_lock") if isinstance(packet.get("approved_plan_lock"), dict) else {}
    lock_moves = lock.get("selected_moves") if isinstance(lock.get("selected_moves"), list) else []
    lock_move = lock_moves[0] if lock_moves and isinstance(lock_moves[0], dict) else {}
    source_hashes = expected.get("source_hashes") if isinstance(expected.get("source_hashes"), dict) else {}
    return {
        "packet_id": str(packet.get("packet_id") or ""),
        "operation_id": str(packet.get("operation_id") or ""),
        "decision_id": str(packet.get("decision_id") or ""),
        "authority_generation": str(packet.get("authority_generation") or expected.get("generation_id") or ""),
        "breaker_generation": str(packet.get("breaker_generation") or ""),
        "source_bundle_hash": str(expected.get("source_bundle_hash") or ""),
        "source_hashes_hash": sha256_json(source_hashes) if source_hashes else "",
        "snapshot_bundle_hash": str(expected.get("snapshot_bundle_hash") or ""),
        "max_users": as_int(constraints.get("selected_move_budget"), 0),
        "selected_move_hash": str(expected.get("selected_move_hash") or ""),
        "selected_move_count": as_int(expected.get("selected_move_count"), 0),
        "user": str(lock_move.get("user_ip") or ((constraints.get("allowed_users") or [""])[0]) or ""),
        "source": str(lock_move.get("current_egress") or ""),
        "target": str(lock_move.get("recommended_egress") or ((constraints.get("allowed_targets") or [""])[0]) or ""),
        "allowed_users": [str(item) for item in (constraints.get("allowed_users") or [])],
        "allowed_targets": [str(item) for item in (constraints.get("allowed_targets") or [])],
        "rollback_manifest_id": str(rollback_manifest.get("rollback_manifest_id") or ""),
    }


def packet_identity(packet):
    return _packet_identity(packet if isinstance(packet, dict) else {})


def preview_packet_identity(preview):
    preview = extract_packet_preview(preview)
    selected = selected_moves_from_preview(preview)
    moves = selected.get("moves") or []
    move = moves[0] if moves and isinstance(moves[0], dict) else {}
    rollback_preview = preview.get("rollback_manifest_preview") if isinstance(preview.get("rollback_manifest_preview"), dict) else {}
    source_hashes = preview.get("source_hashes") if isinstance(preview.get("source_hashes"), dict) else {}
    return {
        "packet_id": str(preview.get("packet_id") or ""),
        "operation_id": str(preview.get("operation_id") or ""),
        "decision_id": str(preview.get("decision_id") or ""),
        "authority_generation": str(selected.get("authority_generation") or ""),
        "breaker_generation": str(preview.get("breaker_generation") or ""),
        "source_bundle_hash": sha256_json(source_hashes) if source_hashes else "",
        "source_hashes_hash": sha256_json(source_hashes) if source_hashes else "",
        "snapshot_bundle_hash": str(preview.get("snapshot_bundle_hash") or ""),
        "max_users": as_int(preview.get("selected_move_count"), 0),
        "selected_move_hash": str(selected.get("selected_move_hash") or ""),
        "selected_move_count": as_int(selected.get("selected_move_count"), 0),
        "user": str(move.get("user_ip") or ""),
        "source": str(move.get("current_egress") or ""),
        "target": str(move.get("recommended_egress") or ""),
        "allowed_users": [str(item) for item in (preview.get("allowed_users") or [])],
        "allowed_targets": [str(item) for item in (preview.get("allowed_targets") or [])],
        "rollback_manifest_id": str(rollback_preview.get("rollback_manifest_id") or ""),
    }


def approved_packet_binding_status(actual_identity, approved_identity):
    actual = actual_identity if isinstance(actual_identity, dict) else {}
    approved = approved_identity if isinstance(approved_identity, dict) else {}
    normalized_approved = {
        str(key): str(value)
        for key, value in approved.items()
        if str(key) and value not in (None, "")
    }
    missing_fields = [
        field for field in APPROVED_PACKET_BINDING_FIELDS
        if not normalized_approved.get(field)
        and not (field == "breaker_generation" and str(actual.get(field) or "") in {"", "UNBOUND_READ_ONLY"})
    ]
    mismatches = [
        {
            "field": field,
            "approved": normalized_approved.get(field, ""),
            "actual": str(actual.get(field) or ""),
        }
        for field in APPROVED_PACKET_BINDING_FIELDS
        if normalized_approved.get(field) and str(actual.get(field) or "") != normalized_approved.get(field)
    ]
    return {
        "ok": not missing_fields and not mismatches,
        "binding_required_fields": list(APPROVED_PACKET_BINDING_FIELDS),
        "missing_fields": missing_fields,
        "mismatches": mismatches,
        "approved_identity": normalized_approved,
        "actual_identity": {field: str(actual.get(field) or "") for field in APPROVED_PACKET_BINDING_FIELDS},
    }


def _string_list(value):
    if isinstance(value, list):
        return sorted(str(item) for item in value if str(item))
    if value in (None, ""):
        return []
    return [str(value)]


def _rollback_targets_from_manifest(manifest):
    manifest = manifest if isinstance(manifest, dict) else {}
    items = manifest.get("items") if isinstance(manifest.get("items"), list) else []
    return sorted(str(item.get("rollback_target") or "") for item in items if isinstance(item, dict) and str(item.get("rollback_target") or ""))


def _truthy(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "ok", "pass", "passed", "verified", "success", "applied"}
    return bool(value)


def _terminal_text(*values):
    return " ".join(str(value or "").upper() for value in values if value is not None)


def containment_forward_fix_classification(
    *,
    packet=None,
    execution_result=None,
    verification_result=None,
    rollback_result=None,
    generated_at=None,
):
    """Classify containment vs forward-fix from existing terminal evidence only."""
    generated = generated_at or utc_now().isoformat()
    packet = packet if isinstance(packet, dict) else {}
    execution = execution_result if isinstance(execution_result, dict) else {}
    verification = verification_result if isinstance(verification_result, dict) else {}
    rollback = rollback_result if isinstance(rollback_result, dict) else {}
    manifest = packet.get("rollback_manifest") if isinstance(packet.get("rollback_manifest"), dict) else {}
    manifest_items = [item for item in (manifest.get("items") or []) if isinstance(item, dict)]
    apply_result = execution.get("apply_result") if isinstance(execution.get("apply_result"), dict) else {}
    results = apply_result.get("results") if isinstance(apply_result.get("results"), list) else []
    applied = (
        _truthy(execution.get("applied"))
        or _truthy(execution.get("apply_executed"))
        or _truthy(apply_result.get("applied"))
        or str(execution.get("result") or "").lower() == "applied"
    )
    verification_passed = (
        verification.get("success") is True
        or verification.get("verification_passed") is True
        or str(verification.get("status") or verification.get("result") or "").lower() in {"success", "verified", "pass", "passed"}
    )
    rollback_verdict = str(
        rollback.get("rollback_verdict")
        or rollback.get("verdict")
        or execution.get("rollback_verdict")
        or ""
    ).upper()
    rollback_required = (
        _truthy(rollback.get("rollback_required"))
        or _truthy(verification.get("rollback_required"))
        or _truthy(execution.get("rollback_required"))
        or bool(rollback_verdict)
    )
    rollback_completed = rollback_verdict in {"ROLLBACK_COMPLETED", "ROLLED_BACK", "OK", "SUCCESS"}
    rollback_failed = rollback_required and not rollback_completed
    partial = (
        _truthy(execution.get("partial_success"))
        or _truthy(verification.get("partial_success"))
        or (results and len(results) < len(manifest_items))
    )
    text = _terminal_text(
        execution.get("terminal_state"),
        execution.get("terminal_reason"),
        execution.get("result"),
        verification.get("status"),
        verification.get("result"),
        rollback_verdict,
    )
    if not applied:
        classification = "NO_EXECUTION_CONTAINED"
        operator_summary = "No runtime mutation executed; containment is already satisfied."
        safe_next = "review_or_refresh_evidence"
    elif verification_passed and not partial:
        classification = "FORWARD_FIX_VERIFIED"
        operator_summary = "Forward action verified; rollback is not required by observed terminal evidence."
        safe_next = "close_outcome_and_learn"
    elif rollback_completed:
        classification = "CONTAINED_BY_ROLLBACK"
        operator_summary = "Forward action did not verify, but rollback completed and contained the failed path."
        safe_next = "close_rollback_outcome_and_learn"
    elif rollback_failed:
        classification = "CONTAINMENT_FAILED_OPERATOR_REVIEW_REQUIRED"
        operator_summary = "Rollback was required but did not complete; operator review remains required."
        safe_next = "operator_review_required"
    elif partial or "PARTIAL" in text:
        classification = "PARTIAL_FORWARD_FIX_REQUIRES_CONTAINMENT_REVIEW"
        operator_summary = "Forward action appears partial; containment review is required before treating it as success."
        safe_next = "containment_review_required"
    elif applied:
        classification = "FORWARD_FIX_UNVERIFIED_CONTAINMENT_PENDING"
        operator_summary = "Forward action exists without complete verification; containment remains pending."
        safe_next = "complete_verification_or_containment_review"
    else:
        classification = "UNKNOWN_TERMINAL_STATE"
        operator_summary = "Terminal evidence is insufficient for containment or forward-fix classification."
        safe_next = "collect_terminal_evidence"
    rows = []
    for index, item in enumerate(manifest_items):
        rows.append({
            "user": str(item.get("user_ip") or ""),
            "forward_target": str(item.get("forward_target") or ""),
            "rollback_target": str(item.get("rollback_target") or ""),
            "move_type": str(item.get("move_type") or ""),
            "containment_owner": CANONICAL_CLEARANCE_OWNER,
            "source_operation_id": str(item.get("source_operation_id") or packet.get("operation_id") or ""),
            "classification": classification,
            "row_index": index,
        })
    return {
        "schema_version": B15_CONTAINMENT_FORWARD_FIX_SCHEMA,
        "generated_at": generated,
        "owner": CANONICAL_CLEARANCE_OWNER,
        "backlog_item": "B15",
        "purpose": "expose_containment_forward_fix_classification_without_runtime_behavior_change",
        "policy_source": "POLICY_007_ROLLBACK",
        "source_owners_reused": [
            "admin_core.operator_execution packet and execution lease owner",
            "admin_core.operator_execution_feedback terminal outcome classification",
            "admin_core.operator_execution_pipeline governed execution coordination",
            "tools/v7-users-autoswitch rollback/apply/verify owner when separately approved",
        ],
        "packet_identity": _packet_identity(packet) if packet else {},
        "partial_failure_policy": str(manifest.get("partial_failure_policy") or "UNKNOWN"),
        "rollback_execution_owner": str(manifest.get("rollback_execution_owner") or ""),
        "classification": classification,
        "operator_summary": operator_summary,
        "safe_next_step": safe_next,
        "evidence": {
            "applied": applied,
            "verification_passed": verification_passed,
            "partial_success": bool(partial),
            "rollback_required": rollback_required,
            "rollback_completed": rollback_completed,
            "rollback_failed": rollback_failed,
            "manifest_items": len(manifest_items),
            "result_rows": len(results),
        },
        "rows": rows,
        "classification_matrix": [
            {"terminal_condition": "no apply", "classification": "NO_EXECUTION_CONTAINED", "meaning": "nothing to roll back"},
            {"terminal_condition": "apply + verification pass", "classification": "FORWARD_FIX_VERIFIED", "meaning": "forward path succeeded"},
            {"terminal_condition": "apply + verification fail + rollback complete", "classification": "CONTAINED_BY_ROLLBACK", "meaning": "failure contained"},
            {"terminal_condition": "apply + verification fail + rollback fail", "classification": "CONTAINMENT_FAILED_OPERATOR_REVIEW_REQUIRED", "meaning": "operator review required"},
            {"terminal_condition": "partial apply or partial verification", "classification": "PARTIAL_FORWARD_FIX_REQUIRES_CONTAINMENT_REVIEW", "meaning": "cannot treat as success"},
            {"terminal_condition": "apply without verification", "classification": "FORWARD_FIX_UNVERIFIED_CONTAINMENT_PENDING", "meaning": "verification or containment still required"},
        ],
        "canonical_rules": [
            "b15_classifies_terminal_evidence_only",
            "containment_is_observability_not_automatic_rollback_authority",
            "forward_fix_requires_verification_before_success",
            "partial_failure_policy_stop_and_contain_remains_existing_packet_policy",
            "b15_does_not_execute_runtime_apply_or_rollback",
        ],
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "rollback_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "synthetic_evidence_created": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_runtime_created": False,
        "new_planner_created": False,
    }


def rollback_operational_compensation_contract(*, generated_at=None):
    """Preserve rollback semantics as operational compensation, not transaction rewind."""
    generated = generated_at or utc_now().isoformat()
    terminal_outcomes = [
        {
            "outcome": "NO_EXECUTION_CONTAINED",
            "meaning": "No runtime mutation occurred; nothing needs transaction-style rollback.",
            "compensation_required": False,
        },
        {
            "outcome": "FORWARD_FIX_VERIFIED",
            "meaning": "Forward path verified; rollback is unnecessary and learning can close the outcome.",
            "compensation_required": False,
        },
        {
            "outcome": "CONTAINED_BY_ROLLBACK",
            "meaning": "Failed forward path was compensated by a certified restore/rollback action.",
            "compensation_required": True,
        },
        {
            "outcome": "PARTIAL_FORWARD_FIX_REQUIRES_CONTAINMENT_REVIEW",
            "meaning": "Partial outcome requires containment review before success can be claimed.",
            "compensation_required": "operator_review",
        },
        {
            "outcome": "CONTAINMENT_FAILED_OPERATOR_REVIEW_REQUIRED",
            "meaning": "Compensation did not complete; operator review remains required.",
            "compensation_required": "operator_review",
        },
        {
            "outcome": "FORWARD_FIX_UNVERIFIED_CONTAINMENT_PENDING",
            "meaning": "Verification or containment evidence is still missing.",
            "compensation_required": "pending_evidence",
        },
    ]
    return {
        "schema_version": C5_ROLLBACK_OPERATIONAL_COMPENSATION_SCHEMA,
        "generated_at": generated,
        "owner": CANONICAL_CLEARANCE_OWNER,
        "backlog_item": "C5",
        "purpose": "preserve_rollback_as_operational_compensation_not_transaction_rollback",
        "policy_source": "POLICY_007_ROLLBACK",
        "source_owners_reused": [
            "docs/reference/V7_RUNTIME_MODEL.md rollback/no-rollback contract",
            "docs/policies/POLICY_007_ROLLBACK.md rollback policy",
            "admin_core.operator_execution containment_forward_fix_classification",
            "admin_core.operator_execution_pipeline governed execution coordination",
            "tools/v7-users-autoswitch rollback/apply/verify owner when separately approved",
            "docs/programs/OPERATIONAL_MATURITY_PROGRAM.md C5 transition owner",
        ],
        "semantic_contract": {
            "rollback_semantics": "OPERATIONAL_COMPENSATION",
            "transaction_rollback_supported": False,
            "database_transaction_semantics_claimed": False,
            "rollback_is_global_state_rewind": False,
            "rollback_is_authority": False,
            "rollback_is_planner": False,
            "allowed_compensation_forms": [
                "abort_before_mutation",
                "certified_no_rollback",
                "restore_to_fresh_rollback_target",
                "containment_review",
                "forward_fix_with_verification",
                "operator_review_when_compensation_fails",
            ],
            "required_evidence": [
                "restore_barrier_or_explicit_no_rollback_classification",
                "fresh_rollback_target_when_restore_is_claimed",
                "verification_or_terminal_outcome_evidence",
                "authority_for_any_future_runtime_action",
                "post_action_verification",
                "feedback_and_learning_closure",
            ],
        },
        "terminal_outcome_model": terminal_outcomes,
        "canonical_rules": [
            "c5_rollback_is_operational_compensation_not_transaction_rewind",
            "c5_compensation_can_abort_restore_contain_forward_fix_or_certify_no_rollback",
            "c5_restore_barrier_is_safety_preparation_not_transaction_log",
            "c5_compensation_requires_fresh_evidence_authority_verification_and_closure",
            "c5_does_not_execute_runtime_apply_or_rollback",
            "c5_does_not_expand_authority_runtime_planner_owner_or_truth_source",
        ],
        "forbidden": [
            "database_transaction_rollback_claim",
            "global_state_rewind_claim",
            "rollback_without_fresh_restore_target",
            "rollback_without_authority",
            "rollback_without_post_action_verification",
            "automatic_rollback_execution",
            "runtime_apply",
            "authority_expansion",
            "planner_replacement",
            "synthetic_evidence",
            "user_movement",
        ],
        "omp_output": {
            "c5_status": "DONE_READ_ONLY_ROLLBACK_OPERATIONAL_COMPENSATION_PRESERVED",
            "produced_evidence": "rollback_operational_compensation_contract",
            "unlocked_capability": "C6_BOUNDED_STALE_ALLOWANCE_BY_ACTION_CLASS",
            "blocked_later_steps": [
                "runtime_apply",
                "automatic_rollback_execution",
                "authority_expansion",
                "automation",
                "planner_replacement",
                "synthetic_evidence",
                "user_movement",
                "transaction_rollback_abstraction",
            ],
            "next_safe_action": "continue_omp_to_c6_bounded_stale_allowance_by_action_class",
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "rollback_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "synthetic_evidence_created": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_runtime_created": False,
        "new_planner_created": False,
    }


def _material_state_from_components(
    *,
    selected_move_hash="",
    target_channel=None,
    rollback_target=None,
    policy_generation="",
    authority_generation="",
    blast_radius_eligibility="",
    rollback_readiness="",
    verification_prerequisites=None,
    destination_eligibility="",
    source_eligibility="",
    breaker_generation="",
    source_bundle_hash="",
    source_hashes_hash="",
    snapshot_bundle_hash="",
):
    return {
        "selected_move_hash": str(selected_move_hash or ""),
        "target_channel": _string_list(target_channel),
        "rollback_target": _string_list(rollback_target),
        "policy_generation": str(policy_generation or ""),
        "authority_generation": str(authority_generation or ""),
        "blast_radius_eligibility": str(blast_radius_eligibility or ""),
        "rollback_readiness": str(rollback_readiness or ""),
        "verification_prerequisites": _string_list(verification_prerequisites),
        "destination_eligibility": str(destination_eligibility or ""),
        "source_eligibility": str(source_eligibility or ""),
        "breaker_generation": str(breaker_generation or ""),
        "source_bundle_hash": str(source_bundle_hash or ""),
        "source_hashes_hash": str(source_hashes_hash or ""),
        "snapshot_bundle_hash": str(snapshot_bundle_hash or ""),
    }


def material_state_from_packet_preview(preview):
    preview = extract_packet_preview(preview)
    rollback_preview = preview.get("rollback_manifest_preview") if isinstance(preview.get("rollback_manifest_preview"), dict) else {}
    targets = _string_list(preview.get("allowed_targets"))
    users = _string_list(preview.get("allowed_users"))
    rollback_targets = _rollback_targets_from_manifest(rollback_preview)
    source_hashes = preview.get("source_hashes") if isinstance(preview.get("source_hashes"), dict) else {}
    return _material_state_from_components(
        selected_move_hash=preview.get("selected_move_hash", ""),
        target_channel=targets,
        rollback_target=rollback_targets,
        policy_generation=preview.get("policy_generation", ""),
        authority_generation=preview.get("authority_generation", ""),
        blast_radius_eligibility=preview.get("blast_radius_eligibility", ""),
        rollback_readiness=preview.get("rollback_readiness", "") or ("READY" if rollback_targets else "BLOCKED"),
        verification_prerequisites=preview.get("verification_prerequisites") or preview.get("verification_required"),
        destination_eligibility=preview.get("destination_eligibility", "") or ("ELIGIBLE" if targets else "UNKNOWN"),
        source_eligibility=preview.get("source_eligibility", "") or ("ELIGIBLE" if users else "UNKNOWN"),
        breaker_generation=preview.get("breaker_generation", ""),
        source_bundle_hash=sha256_json(source_hashes) if source_hashes else "",
        source_hashes_hash=sha256_json(source_hashes) if source_hashes else "",
        snapshot_bundle_hash=preview.get("snapshot_bundle_hash", ""),
    )


def material_state_from_packet(packet):
    packet = packet if isinstance(packet, dict) else {}
    expected = packet.get("expected") if isinstance(packet.get("expected"), dict) else {}
    constraints = packet.get("constraints") if isinstance(packet.get("constraints"), dict) else {}
    rollback_manifest = packet.get("rollback_manifest") if isinstance(packet.get("rollback_manifest"), dict) else {}
    targets = _string_list(constraints.get("allowed_targets"))
    users = _string_list(constraints.get("allowed_users"))
    rollback_targets = _rollback_targets_from_manifest(rollback_manifest)
    source_hashes = expected.get("source_hashes") if isinstance(expected.get("source_hashes"), dict) else {}
    return _material_state_from_components(
        selected_move_hash=expected.get("selected_move_hash", ""),
        target_channel=targets,
        rollback_target=rollback_targets,
        policy_generation=packet.get("policy_generation", ""),
        authority_generation=packet.get("authority_generation") or expected.get("generation_id", ""),
        blast_radius_eligibility=packet.get("blast_radius_eligibility", ""),
        rollback_readiness=packet.get("rollback_readiness", "") or ("READY" if rollback_targets else "BLOCKED"),
        verification_prerequisites=packet.get("verification_prerequisites"),
        destination_eligibility=packet.get("destination_eligibility", "") or ("ELIGIBLE" if targets else "UNKNOWN"),
        source_eligibility=packet.get("source_eligibility", "") or ("ELIGIBLE" if users else "UNKNOWN"),
        breaker_generation=packet.get("breaker_generation", ""),
        source_bundle_hash=expected.get("source_bundle_hash", ""),
        source_hashes_hash=sha256_json(source_hashes) if source_hashes else "",
        snapshot_bundle_hash=expected.get("snapshot_bundle_hash", ""),
    )


def _normalize_material_state(state):
    state = state if isinstance(state, dict) else {}
    normalized = {}
    for field in MATERIAL_STATE_FIELDS:
        value = state.get(field)
        if field in {"target_channel", "rollback_target", "verification_prerequisites"}:
            normalized[field] = _string_list(value)
        else:
            normalized[field] = str(value or "")
    return normalized


def material_state_change_gate(lease, *, current_material_state=None, current_source_hashes=None):
    lease = lease if isinstance(lease, dict) else {}
    approved_state = _normalize_material_state(
        lease.get("material_state") if isinstance(lease.get("material_state"), dict) else material_state_from_packet(lease.get("packet") or {})
    )
    current_state = _normalize_material_state(current_material_state) if isinstance(current_material_state, dict) else None
    if (
        current_state is not None
        and approved_state.get("breaker_generation") == "UNBOUND_READ_ONLY"
        and not current_state.get("breaker_generation")
    ):
        current_state["breaker_generation"] = "UNBOUND_READ_ONLY"
    changed_fields = []
    if current_state is not None:
        changed_fields = [
            field for field in MATERIAL_STATE_FIELDS
            if approved_state.get(field) != current_state.get(field)
        ]
    material_keys = {str(key) for key in (lease.get("material_source_keys") or [])}
    approved_hashes = lease.get("source_hashes") if isinstance(lease.get("source_hashes"), dict) else {}
    current_hashes = current_source_hashes if isinstance(current_source_hashes, dict) else None
    changed_source_keys: list[str] = []
    material_changed_source_keys: list[str] = []
    if current_hashes is not None:
        changed_source_keys = sorted(
            key for key, approved in approved_hashes.items()
            if str(current_hashes.get(key) or "") != str(approved or "")
        )
        material_changed_source_keys = sorted(set(changed_source_keys) & material_keys)
    material_change = bool(changed_fields or material_changed_source_keys)
    return {
        "material_state_change": material_change,
        "changed_fields": changed_fields,
        "changed_source_keys": changed_source_keys,
        "material_changed_source_keys": material_changed_source_keys,
        "approved_material_state": approved_state,
        "current_material_state": current_state or {},
        "lease_keep_reason": "" if material_change else "no_material_state_change",
        "lease_invalidation_reason": (
            "material_state_fields_changed"
            if changed_fields
            else ("material_source_keys_changed" if material_changed_source_keys else "")
        ),
    }


def build_execution_lease(packet, *, source_preview=None, now=None):
    now = now or utc_now()
    packet_hash = sha256_bytes(canonical_json(packet).encode("utf-8"))
    expected = packet.get("expected") or {}
    source_hashes = expected.get("source_hashes") if isinstance(expected.get("source_hashes"), dict) else {}
    identity = _packet_identity(packet)
    lease = {
        "schema_version": EXECUTION_LEASE_SCHEMA,
        "status": "ACTIVE",
        "lease_id": stable_id("execlease", {
            **identity,
            "packet_hash": packet_hash,
        }),
        "owner": CANONICAL_CLEARANCE_OWNER,
        "created_at": now.isoformat(),
        "expires_at": packet.get("expires_at", ""),
        "terminal_statuses": sorted(LEASE_TERMINAL_STATUSES),
        "invalidate_only_on": [
            "timeout",
            "execution_finished",
            "rollback_finished",
            "operator_cancel",
            "source_state_materially_changed",
        ],
        "planner_regeneration_allowed": False,
        "decision_regeneration_allowed": False,
        "selected_move_hash_regeneration_allowed": False,
        "target_regeneration_allowed": False,
        "packet_freshness_check_allowed": True,
        "immutable_packet_identity": identity,
        "packet_hash": packet_hash,
        "source_hashes": {str(key): str(value) for key, value in source_hashes.items()},
        "material_state": material_state_from_packet(packet),
        "material_state_fields": list(MATERIAL_STATE_FIELDS),
        "material_source_keys": ["egress_registry", "service_preferences", "users_registry"],
        "allowed_non_material_source_drift": ["quality_summary", "service_matrix"],
        "packet": packet,
        "source_preview": redact(source_preview or {}),
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
    }
    lease["lease_hash"] = sha256_bytes(canonical_json({
        key: value for key, value in lease.items() if key != "lease_hash"
    }).encode("utf-8"))
    return lease


def create_execution_lease_from_packet(packet, *, source_preview=None):
    packet = packet if isinstance(packet, dict) else {}
    validation = validate_packet(packet)
    if not validation.get("ok"):
        raise PacketError(",".join(validation.get("errors") or ["approved_packet_invalid"]))
    return build_execution_lease(packet, source_preview=source_preview)


def create_execution_lease_from_preview(
    preview,
    *,
    approval_author,
    approval_reviewer,
    ttl_seconds=DEFAULT_EXECUTION_LEASE_TTL_SECONDS,
    approved_identity=None,
):
    preview = extract_packet_preview(preview)
    if approved_identity is not None:
        binding = approved_packet_binding_status(preview_packet_identity(preview), approved_identity)
        if not binding.get("ok"):
            raise PacketError("approved_packet_binding_failed:" + sha256_json(binding))
    packet = packet_from_preview(
        preview,
        approval_author=approval_author,
        approval_reviewer=approval_reviewer,
        ttl_seconds=ttl_seconds,
    )
    if approved_identity is not None:
        binding = approved_packet_binding_status(packet_identity(packet), approved_identity)
        if not binding.get("ok"):
            raise PacketError("approved_packet_materialization_changed_identity:" + sha256_json(binding))
    return create_execution_lease_from_packet(packet, source_preview=preview)


def execution_lease_state(lease, *, now=None, current_source_hashes=None, current_material_state=None):
    now = now or utc_now()
    if not isinstance(lease, dict) or not lease:
        return {"active": False, "status": "MISSING", "reason": "execution_lease_missing"}
    if lease.get("schema_version") != EXECUTION_LEASE_SCHEMA:
        return {"active": False, "status": "INVALID", "reason": "execution_lease_schema_invalid"}
    status = str(lease.get("status") or "")
    if status in LEASE_TERMINAL_STATUSES:
        return {"active": False, "status": status, "reason": "execution_lease_terminal"}
    try:
        expires_at = parse_ts(lease.get("expires_at"))
    except PacketError:
        return {"active": False, "status": "INVALID", "reason": "execution_lease_expires_at_invalid"}
    if now >= expires_at:
        return {"active": False, "status": "EXPIRED", "reason": "execution_lease_expired", "expires_at": lease.get("expires_at")}
    packet = lease.get("packet") if isinstance(lease.get("packet"), dict) else {}
    identity = _packet_identity(packet)
    if identity != (lease.get("immutable_packet_identity") or {}):
        return {
            "active": False,
            "status": "INVALID",
            "reason": "execution_lease_packet_identity_changed",
            "packet_identity": identity,
            "lease_identity": lease.get("immutable_packet_identity") or {},
        }
    if sha256_bytes(canonical_json(packet).encode("utf-8")) != str(lease.get("packet_hash") or ""):
        return {"active": False, "status": "INVALID", "reason": "execution_lease_packet_hash_changed"}
    gate = material_state_change_gate(
        lease,
        current_material_state=current_material_state,
        current_source_hashes=current_source_hashes,
    )
    if gate.get("material_state_change"):
        return {
            "active": False,
            "status": "INVALIDATED",
            "reason": "execution_lease_source_state_materially_changed",
            **gate,
        }
    return {
        "active": True,
        "status": "ACTIVE",
        "reason": "execution_lease_active",
        "lease_id": str(lease.get("lease_id") or ""),
        "packet_id": identity.get("packet_id", ""),
        "operation_id": identity.get("operation_id", ""),
        "selected_move_hash": identity.get("selected_move_hash", ""),
        "expires_at": lease.get("expires_at"),
        **gate,
    }


def load_execution_lease(path):
    path = Path(path)
    if not path.exists():
        return {}
    return read_json(path)


def write_execution_lease(path, lease, *, now=None):
    path = Path(path)
    current = load_execution_lease(path)
    state = execution_lease_state(current, now=now)
    if state.get("active"):
        return {
            "ok": False,
            "verdict": "DENY_DUPLICATE_EXECUTION_LEASE",
            "errors": ["active_execution_lease_exists"],
            "active_lease": state,
            "execution_allowed_now": False,
        }
    write_json_atomic(path, lease)
    return {
        "ok": True,
        "verdict": "EXECUTION_LEASE_WRITTEN",
        "lease_file": str(path),
        "lease": redact(lease),
        "execution_allowed_now": False,
    }


def cancel_execution_lease(path, *, reason="operator_cancel", now=None):
    now = now or utc_now()
    path = Path(path)
    lease = load_execution_lease(path)
    if not lease:
        return {"ok": False, "verdict": "EXECUTION_LEASE_MISSING", "execution_allowed_now": False}
    lease["status"] = "OPERATOR_CANCELLED"
    lease["cancel_reason"] = reason
    lease["cancelled_at"] = now.isoformat()
    lease["runtime_mutation_performed"] = False
    lease["apply_executed"] = False
    lease["users_moved"] = 0
    write_json_atomic(path, lease)
    return {
        "ok": True,
        "verdict": "EXECUTION_LEASE_CANCELLED",
        "lease_file": str(path),
        "lease": redact(lease),
        "execution_allowed_now": False,
    }


def finish_execution_lease(path, *, status="EXECUTION_FINISHED", reason="", operation=None, now=None):
    now = now or utc_now()
    path = Path(path)
    lease = load_execution_lease(path)
    if not lease:
        return {"ok": False, "verdict": "EXECUTION_LEASE_MISSING", "execution_allowed_now": False}
    if status not in LEASE_TERMINAL_STATUSES:
        return {
            "ok": False,
            "verdict": "EXECUTION_LEASE_TERMINAL_STATUS_INVALID",
            "errors": ["invalid_execution_lease_terminal_status"],
            "execution_allowed_now": False,
        }
    state = execution_lease_state(lease, now=now)
    if not state.get("active") and state.get("status") in LEASE_TERMINAL_STATUSES:
        return {
            "ok": True,
            "verdict": "EXECUTION_LEASE_ALREADY_TERMINAL",
            "lease_file": str(path),
            "lease": redact(lease),
            "execution_allowed_now": False,
        }
    operation = operation if isinstance(operation, dict) else {}
    apply_result = operation.get("apply_result") if isinstance(operation.get("apply_result"), dict) else {}
    results = apply_result.get("results") if isinstance(apply_result.get("results"), list) else []
    lease["status"] = status
    lease["terminal_reason"] = str(reason or operation.get("terminal_reason") or status.lower())
    lease["finished_at"] = now.isoformat()
    lease["runtime_mutation_performed"] = bool(apply_result.get("applied"))
    lease["apply_executed"] = bool(apply_result.get("applied"))
    lease["users_moved"] = len(results)
    lease["operation_terminal_state"] = str(operation.get("terminal_state") or "")
    lease["operation_terminal_reason"] = str(operation.get("terminal_reason") or "")
    lease["rollback_verdict"] = str(operation.get("rollback_verdict") or "")
    lease["operation_id"] = str(operation.get("operation_id") or state.get("operation_id") or "")
    lease["packet_id"] = str(state.get("packet_id") or ((lease.get("packet") or {}).get("packet_id") if isinstance(lease.get("packet"), dict) else ""))
    lease["selected_move_hash"] = str(state.get("selected_move_hash") or "")
    write_json_atomic(path, lease)
    return {
        "ok": True,
        "verdict": "EXECUTION_LEASE_TERMINALIZED",
        "lease_file": str(path),
        "lease": redact(lease),
        "execution_allowed_now": False,
    }


def is_preview_derived_packet(packet):
    return (
        str(packet.get("identity_source") or "") == "approved_preview_packet"
        or str(((packet.get("execution_metadata") or {}).get("identity_source")) or "") == "approved_preview_packet"
    )


def recheck_preview_derived_nonzero_packet(packet, state_dir):
    state_dir = Path(state_dir)
    users_path = state_dir / "users.registry"
    egress_path = state_dir / "egress.registry"
    if not users_path.exists() or not egress_path.exists():
        return {
            "allow": False,
            "verdict": "DENY_STALE_RUNTIME",
            "errors": ["runtime_registry_missing"],
            "checks": {"users_registry_exists": users_path.exists(), "egress_registry_exists": egress_path.exists()},
        }
    expected = packet.get("expected") or {}
    constraints = packet.get("constraints") or {}
    lock = packet.get("approved_plan_lock") or {}
    moves = lock.get("selected_moves") or []
    allowed_users = constraints.get("allowed_users") or []
    allowed_targets = constraints.get("allowed_targets") or []
    move_users = [str(move.get("user_ip") or "") for move in moves]
    move_targets = sorted({str(move.get("recommended_egress") or "") for move in moves})
    mismatches = []
    if not moves:
        mismatches.append("approved_plan_lock_selected_moves")
    if str(lock.get("identity_source") or "") != "approved_preview_packet":
        mismatches.append("approved_plan_lock_identity_source")
    if str(lock.get("packet_id") or "") != str(packet.get("packet_id") or ""):
        mismatches.append("packet_id")
    if str(lock.get("operation_id") or "") != str(packet.get("operation_id") or ""):
        mismatches.append("operation_id")
    if str(lock.get("decision_id") or "") != str(packet.get("decision_id") or ""):
        mismatches.append("decision_id")
    if str(lock.get("authority_generation") or "") != str(packet.get("authority_generation") or ""):
        mismatches.append("authority_generation")
    if str(lock.get("selected_move_hash") or "") != str(expected.get("selected_move_hash") or ""):
        mismatches.append("selected_move_hash")
    if as_int(lock.get("selected_move_count"), 0) != as_int(expected.get("selected_move_count"), 0):
        mismatches.append("selected_move_count")
    if sorted(allowed_users) != sorted(move_users):
        mismatches.append("allowed_users")
    if sorted(allowed_targets) != move_targets:
        mismatches.append("allowed_targets")
    if mismatches:
        return {
            "allow": False,
            "verdict": "DENY_HASH_MISMATCH",
            "errors": sorted(set(mismatches)),
            "checks": {
                "packet_id": packet.get("packet_id", ""),
                "operation_id": packet.get("operation_id", ""),
                "decision_id": packet.get("decision_id", ""),
                "authority_generation": packet.get("authority_generation", ""),
                "selected_move_hash": expected.get("selected_move_hash", ""),
                "selected_move_count": expected.get("selected_move_count", 0),
            },
        }
    return {
        "allow": True,
        "verdict": "ALLOW_RESTORE_BARRIER_CLEARANCE",
        "errors": [],
        "checks": {
            "identity_source": "approved_preview_packet",
            "packet_id": packet.get("packet_id", ""),
            "operation_id": packet.get("operation_id", ""),
            "decision_id": packet.get("decision_id", ""),
            "authority_generation": packet.get("authority_generation", ""),
            "selected_move_hash": expected.get("selected_move_hash", ""),
            "selected_move_count": expected.get("selected_move_count", 0),
            "planner_generation_id": expected.get("generation_id", ""),
            "moves": moves,
            "constraints": constraints,
            "users_registry_hash": sha256_file(users_path),
            "egress_registry_hash": sha256_file(egress_path),
            "real_runtime_action_after_recheck": True,
            "runtime_action_scope": "restore_barrier_clearance_only",
        },
    }


def recheck_nonzero_packet(packet, state_dir, planner_snapshot):
    if is_preview_derived_packet(packet):
        return recheck_preview_derived_nonzero_packet(packet, state_dir)
    if not isinstance(planner_snapshot, dict):
        return {"allow": False, "verdict": "DENY_RUNTIME_PLAN_MISSING", "errors": ["planner_snapshot_required"]}
    state_dir = Path(state_dir)
    users_path = state_dir / "users.registry"
    egress_path = state_dir / "egress.registry"
    if not users_path.exists() or not egress_path.exists():
        return {
            "allow": False,
            "verdict": "DENY_STALE_RUNTIME",
            "errors": ["runtime_registry_missing"],
            "checks": {"users_registry_exists": users_path.exists(), "egress_registry_exists": egress_path.exists()},
        }
    expected = packet.get("expected") or {}
    constraints = packet.get("constraints") or {}
    plan_selected = selected_moves_from_plan(planner_snapshot)
    mismatches = []
    if expected.get("generation_id") != plan_selected.get("planner_generation_id"):
        mismatches.append("generation_id")
    if expected.get("selected_move_hash") != plan_selected.get("selected_move_hash"):
        mismatches.append("selected_move_hash")
    if as_int(expected.get("selected_move_count"), 0) != as_int(plan_selected.get("selected_move_count"), 0):
        mismatches.append("selected_move_count")
    if sorted(constraints.get("allowed_users") or []) != sorted(plan_selected.get("constraints", {}).get("allowed_users") or []):
        mismatches.append("allowed_users")
    if sorted(constraints.get("allowed_targets") or []) != sorted(plan_selected.get("constraints", {}).get("allowed_targets") or []):
        mismatches.append("allowed_targets")
    if as_int(constraints.get("selected_move_budget"), 0) < as_int(plan_selected.get("selected_move_count"), 0):
        mismatches.append("selected_move_budget")
    if expected.get("atomic_execution_envelope_id") != plan_selected.get("atomic_execution_envelope_id"):
        mismatches.append("atomic_execution_envelope_id")
    if expected.get("atomic_execution_envelope_hash") != plan_selected.get("atomic_execution_envelope_hash"):
        mismatches.append("atomic_execution_envelope_hash")
    if expected.get("source_bundle_hash") != plan_selected.get("source_bundle_hash"):
        mismatches.append("source_bundle_hash")
    expected_snapshot_bundle = expected.get("snapshot_bundle_hash")
    if expected_snapshot_bundle and expected_snapshot_bundle != plan_selected.get("snapshot_bundle_hash"):
        mismatches.append("snapshot_bundle_hash")
    if mismatches:
        return {
            "allow": False,
            "verdict": "DENY_HASH_MISMATCH",
            "errors": mismatches,
            "checks": plan_selected,
        }
    return {
        "allow": True,
        "verdict": "ALLOW_RESTORE_BARRIER_CLEARANCE",
        "errors": [],
        "checks": {
            **plan_selected,
            "users_registry_hash": sha256_file(users_path),
            "egress_registry_hash": sha256_file(egress_path),
            "real_runtime_action_after_recheck": True,
            "runtime_action_scope": "restore_barrier_clearance_only",
        },
    }


def runtime_recheck(packet, state_dir, now=None, planner_snapshot=None):
    now = now or utc_now()
    validation = validate_packet(packet, now=now)
    if not validation["ok"]:
        return {"allow": False, "verdict": validation["verdict"], "errors": validation["errors"]}
    if is_nonzero_clearance_packet(packet):
        return recheck_nonzero_packet(packet, state_dir, planner_snapshot)
    state_dir = Path(state_dir)
    users_path = state_dir / "users.registry"
    egress_path = state_dir / "egress.registry"
    if not users_path.exists() or not egress_path.exists():
        return {
            "allow": False,
            "verdict": "DENY_STALE_RUNTIME",
            "errors": ["runtime_registry_missing"],
            "checks": {"users_registry_exists": users_path.exists(), "egress_registry_exists": egress_path.exists()},
        }
    users_hash = sha256_file(users_path)
    egress_hash = sha256_file(egress_path)
    selected = selected_moves_state(state_dir)
    snapshot_hash = sha256_bytes(canonical_json({
        "users_registry_hash": users_hash,
        "egress_registry_hash": egress_hash,
        "selected_move_hash": selected["hash"],
    }).encode("utf-8"))
    expected = packet.get("expected") or {}
    mismatches = []
    if expected.get("users_registry_hash") and expected.get("users_registry_hash") != users_hash:
        mismatches.append("users_registry_hash")
    if expected.get("egress_registry_hash") and expected.get("egress_registry_hash") != egress_hash:
        mismatches.append("egress_registry_hash")
    if expected.get("runtime_snapshot_hash") and expected.get("runtime_snapshot_hash") != snapshot_hash:
        mismatches.append("runtime_snapshot_hash")
    if expected.get("selected_move_hash") != selected["hash"] or selected["count"] != 0:
        mismatches.append("selected_moves")
    if mismatches:
        return {
            "allow": False,
            "verdict": "DENY_HASH_MISMATCH",
            "errors": mismatches,
            "checks": {
                "users_registry_hash": users_hash,
                "egress_registry_hash": egress_hash,
                "selected_move_hash": selected["hash"],
                "selected_move_count": selected["count"],
                "runtime_snapshot_hash": snapshot_hash,
            },
        }
    return {
        "allow": True,
        "verdict": "ALLOW_RECORD_ONLY",
        "errors": [],
        "checks": {
            "users_registry_hash": users_hash,
            "egress_registry_hash": egress_hash,
            "selected_move_hash": selected["hash"],
            "selected_move_count": selected["count"],
            "runtime_snapshot_hash": snapshot_hash,
            "real_runtime_action_after_recheck": False,
        },
    }


def read_audit_records(audit_store):
    path = Path(audit_store)
    if not path.exists():
        return []
    records = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            records.append({"record_type": "CORRUPT_RECORD", "raw_hash": sha256_bytes(line.encode("utf-8"))})
    return records


def read_last_audit_record(audit_store):
    """Read only the final non-empty append-only audit row.

    ``append_record`` needs the predecessor hash, not a materialized copy of
    every earlier payload.  Reading the complete (and intentionally rich)
    active journal on every append made one governed transaction repeatedly
    decode megabytes before its next write.  This bounded reverse read keeps
    the same append-only owner and the same corrupt-tail behavior.
    """
    path = Path(audit_store)
    if not path.exists():
        return {}
    try:
        with path.open("rb") as handle:
            handle.seek(0, os.SEEK_END)
            position = handle.tell()
            pending = b""
            while position > 0:
                size = min(65536, position)
                position -= size
                handle.seek(position)
                pending = handle.read(size) + pending
                lines = pending.splitlines()
                if position > 0 and lines:
                    pending = lines.pop(0)
                else:
                    pending = b""
                for raw in reversed(lines):
                    if not raw.strip():
                        continue
                    text = raw.decode("utf-8", errors="replace")
                    try:
                        row = json.loads(text)
                    except json.JSONDecodeError:
                        return {
                            "record_type": "CORRUPT_RECORD",
                            "raw_hash": sha256_bytes(raw),
                        }
                    return row if isinstance(row, dict) else {}
            if pending.strip():
                text = pending.decode("utf-8", errors="replace")
                try:
                    row = json.loads(text)
                except json.JSONDecodeError:
                    return {
                        "record_type": "CORRUPT_RECORD",
                        "raw_hash": sha256_bytes(pending),
                    }
                return row if isinstance(row, dict) else {}
    except OSError:
        return {}
    return {}


_LIVE_EXECUTION_LINEAGE_PROCESS_CACHE: dict[
    tuple[str, int, bool, tuple[str, ...], str, tuple[tuple[str, int, int], ...]],
    tuple[dict[str, Any], ...],
] = {}


def _cached_live_execution_lineage_superset(
    *,
    path: Path,
    max_rotated_segments: int,
    include_runtime_actions: bool,
    required_ids: tuple[str, ...],
    checkpoint_fingerprint: str,
    source_signature: tuple[tuple[str, int, int], ...],
) -> list[dict[str, Any]] | None:
    """Reuse an already parsed exact-source projection for another validator.

    One Matrix invocation validates several current standing contracts against
    the same append-only audit generation.  A decision-bounded scan retains
    every durable row in each segment it had to traverse, so that result may
    safely satisfy another exact decision only when the requested decision is
    actually present.  The source signature equality preserves the same
    append/rotation invalidation contract as the primary cache key.
    """
    requested = set(required_ids)
    for cache_key, cached in reversed(
        list(_LIVE_EXECUTION_LINEAGE_PROCESS_CACHE.items())
    ):
        (
            cached_path,
            cached_segments,
            cached_runtime_actions,
            _cached_required_ids,
            cached_checkpoint_fingerprint,
            cached_signature,
        ) = cache_key
        if (
            cached_path != str(path)
            or cached_segments != max_rotated_segments
            or cached_runtime_actions != include_runtime_actions
            or cached_checkpoint_fingerprint != checkpoint_fingerprint
            or cached_signature != source_signature
        ):
            continue
        if requested and not requested.issubset({
            str(row.get("decision_id") or "")
            for row in cached
            if isinstance(row, dict)
        }):
            continue
        return copy.deepcopy(list(cached))
    return None


def _cached_live_execution_lineage_append_extension(
    *,
    path: Path,
    max_rotated_segments: int,
    include_runtime_actions: bool,
    required_ids: tuple[str, ...],
    checkpoint_fingerprint: str,
    source_signature: tuple[tuple[str, int, int], ...],
    durable_record_types: set[str],
    durable_effect_classes: set[str],
) -> list[dict[str, Any]] | None:
    """Extend a cached append-only lineage from verified new records only.

    Packet/lease materialisation appends to the same audit between planning
    and the final mutable-owner revalidation. Re-reading every rotated segment
    cannot add evidence from the immutable prefix. Reuse that prefix only when
    every rotated source is byte-generation-identical, the active file only
    grew, the previous prefix ended on a record boundary, and every appended
    record continues the audit hash chain. Any replacement, truncation,
    partial write or chain mismatch returns ``None`` and the established full
    scan below remains the fail-closed path.
    """
    requested = set(required_ids)
    current_by_path = {row[0]: row for row in source_signature}
    active_path = str(path)
    for cache_key, cached in reversed(
        list(_LIVE_EXECUTION_LINEAGE_PROCESS_CACHE.items())
    ):
        (
            cached_path,
            cached_segments,
            cached_runtime_actions,
            _cached_required_ids,
            cached_checkpoint_fingerprint,
            cached_signature,
        ) = cache_key
        if (
            cached_path != active_path
            or cached_segments != max_rotated_segments
            or cached_runtime_actions != include_runtime_actions
            or cached_checkpoint_fingerprint != checkpoint_fingerprint
        ):
            continue
        if requested and not requested.issubset({
            str(row.get("decision_id") or "")
            for row in cached
            if isinstance(row, dict)
        }):
            continue
        previous_by_path = {row[0]: row for row in cached_signature}
        if set(previous_by_path) != set(current_by_path):
            continue
        previous_active = previous_by_path.get(active_path)
        current_active = current_by_path.get(active_path)
        if previous_active is None or current_active is None:
            continue
        if any(
            previous_by_path[name] != current_by_path[name]
            for name in previous_by_path
            if name != active_path
        ):
            continue
        previous_size = int(previous_active[1])
        current_size = int(current_active[1])
        if current_size <= previous_size or previous_size <= 0:
            continue
        try:
            with path.open("rb") as handle:
                handle.seek(previous_size - 1)
                if handle.read(1) != b"\n":
                    continue
                position = previous_size
                pending = b""
                previous_row: dict[str, Any] = {}
                while position > 0 and not previous_row:
                    size = min(65536, position)
                    position -= size
                    handle.seek(position)
                    pending = handle.read(size) + pending
                    parts = pending.split(b"\n")
                    candidates = parts[1:] if position > 0 else parts
                    for raw in reversed(candidates):
                        if not raw.strip():
                            continue
                        value = json.loads(raw.decode("utf-8"))
                        if isinstance(value, dict):
                            previous_row = value
                        break
                previous_hash = str(previous_row.get("record_hash") or "")
                if not previous_hash:
                    continue
                handle.seek(previous_size)
                appended = handle.read(current_size - previous_size)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        if not appended or not appended.endswith(b"\n"):
            continue
        appended_rows: list[dict[str, Any]] = []
        chain_hash = previous_hash
        chain_valid = True
        for raw in appended.splitlines():
            if not raw.strip():
                continue
            try:
                row = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                chain_valid = False
                break
            if not isinstance(row, dict):
                chain_valid = False
                break
            if str(row.get("previous_record_hash") or "") != chain_hash:
                chain_valid = False
                break
            chain_hash = str(row.get("record_hash") or "")
            if not chain_hash:
                chain_valid = False
                break
            runtime_action = bool(
                include_runtime_actions
                and row.get("runtime_action_performed") is True
                and str(row.get("clearance_verdict") or "")
                == "RESTORE_BARRIER_CLEARANCE_WRITTEN"
            )
            if (
                row.get("record_type") in durable_record_types
                or row.get("effect_class") in durable_effect_classes
                or runtime_action
            ):
                if (
                    checkpoint_fingerprint
                    and row.get("record_type")
                    in CT_M0F_STANDING_VALIDATION_FINGERPRINT_SCOPED_RECORD_TYPES
                    and str(row.get("implementation_fingerprint") or "")
                    != checkpoint_fingerprint
                ):
                    continue
                appended_rows.append(row)
        if not chain_valid:
            continue
        extended = copy.deepcopy(list(cached)) + appended_rows
        new_key = (
            active_path,
            max_rotated_segments,
            include_runtime_actions,
            required_ids,
            checkpoint_fingerprint,
            source_signature,
        )
        if len(_LIVE_EXECUTION_LINEAGE_PROCESS_CACHE) >= 16:
            _LIVE_EXECUTION_LINEAGE_PROCESS_CACHE.clear()
        _LIVE_EXECUTION_LINEAGE_PROCESS_CACHE[new_key] = tuple(
            copy.deepcopy(extended)
        )
        return extended
    return None


def read_live_execution_lineage_records(
    audit_store,
    *,
    max_rotated_segments=8,
    include_runtime_actions=False,
    required_decision_ids=(),
    required_checkpoint_fingerprint="",
):
    """Read compact durable execution lineage across bounded audit rotation.

    The active audit file is intentionally rotated.  Authority decisions and
    exact-once campaign receipts remain authoritative after that rotation, but
    loading every historical audit row on each Matrix/member invocation would
    turn the append-only log into a scale bottleneck.  Reuse the same audit
    owner and stream only the durable decision/receipt record classes from a
    bounded number of recent segments.

    This is a read projection, not a registry or cache: the source of truth
    remains the append-only operator-execution audit.
    """
    path = Path(audit_store)
    names = [path]
    for index in range(1, max(0, int(max_rotated_segments)) + 1):
        plain = path.with_name(f"{path.name}.{index}")
        compressed = path.with_name(f"{path.name}.{index}.gz")
        if plain.exists():
            names.append(plain)
        elif compressed.exists():
            names.append(compressed)
    durable_record_types = {
        STANDING_DELEGATED_POLICY_DECISION_RECORD_TYPE,
        CONTROLLED_CERTIFICATION_SUBSTRATE_DECISION_RECORD_TYPE,
        # The topology decision is meaningful only with its immutable request
        # (and any invalidation) from the same append-only owner.  Keeping
        # only the decision made an approved provision invisible after the
        # bounded live-lineage projection was read.
        CONTROLLED_SOURCE_TOPOLOGY_REQUEST_RECORD_TYPE,
        CONTROLLED_SOURCE_TOPOLOGY_DECISION_RECORD_TYPE,
        CONTROLLED_SOURCE_TOPOLOGY_INVALIDATION_RECORD_TYPE,
        CONTROLLED_SOURCE_TOPOLOGY_PROVISION_RECORD_TYPE,
        CONTROLLED_CERTIFICATION_CAMPAIGN_EFFECT_RECORD_TYPE,
        CT_M0F_STANDING_VALIDATION_REQUEST_RECORD_TYPE,
        CT_M0F_STANDING_VALIDATION_DECISION_RECORD_TYPE,
        CT_M0F_STANDING_VALIDATION_SAMPLE_RESERVATION_RECORD_TYPE,
        CT_M0F_STANDING_VALIDATION_TRANSACTION_RESERVATION_RECORD_TYPE,
        CT_M0F_STANDING_VALIDATION_TRANSACTION_BINDING_RECORD_TYPE,
        CT_M0F_STANDING_VALIDATION_TRANSACTION_TERMINAL_RECORD_TYPE,
        CT_M0F_STANDING_VALIDATION_FORWARD_RECORD_TYPE,
        CT_M0F_STANDING_VALIDATION_SAMPLE_TERMINAL_RECORD_TYPE,
        CT_M0F_STANDING_VALIDATION_LINEAGE_CHECKPOINT_RECORD_TYPE,
    }
    durable_effect_classes = {
        AVAILABILITY_FIRST_CAMPAIGN_STAGE_EFFECT_CLASS,
        AVAILABILITY_FIRST_TARGET_BOUND_EFFECT_CLASS,
        CONTROLLED_CERTIFICATION_CAMPAIGN_STAGE_EFFECT_CLASS,
    }
    source_signature: list[tuple[str, int, int]] = []
    for candidate in names:
        try:
            stat = candidate.stat()
        except OSError:
            continue
        source_signature.append(
            (str(candidate), int(stat.st_size), int(stat.st_mtime_ns))
        )
    required_ids = tuple(sorted({
        str(value) for value in (required_decision_ids or ()) if str(value)
    }))
    checkpoint_fingerprint = str(required_checkpoint_fingerprint or "")
    cache_key = (
        str(path),
        max(0, int(max_rotated_segments)),
        bool(include_runtime_actions),
        required_ids,
        checkpoint_fingerprint,
        tuple(source_signature),
    )
    cached = _LIVE_EXECUTION_LINEAGE_PROCESS_CACHE.get(cache_key)
    if cached is not None:
        # Callers historically received independent parsed rows.  Preserve
        # that contract so one validator cannot mutate another validator's
        # view while still avoiding repeated gzip/JSON work in the same
        # bounded execution process.
        return copy.deepcopy(list(cached))
    cached_superset = _cached_live_execution_lineage_superset(
        path=path,
        max_rotated_segments=max(0, int(max_rotated_segments)),
        include_runtime_actions=bool(include_runtime_actions),
        required_ids=required_ids,
        checkpoint_fingerprint=checkpoint_fingerprint,
        source_signature=tuple(source_signature),
    )
    if cached_superset is not None:
        _LIVE_EXECUTION_LINEAGE_PROCESS_CACHE[cache_key] = tuple(
            copy.deepcopy(cached_superset)
        )
        return cached_superset

    # A current implementation checkpoint is an immutable, hash-verified
    # Authority pointer created only after a complete historical scan proved
    # that this fingerprint had no earlier campaign rows.  When that exact
    # checkpoint is still in the active append-only segment, one search for
    # the fingerprint yields the complete current cohort and makes another
    # multi-enum scan of the same hundreds-of-MiB file unnecessary.  Rotation
    # or any missing/invalid checkpoint falls through to the full fail-closed
    # reader below.
    if checkpoint_fingerprint and path.exists() and path.suffix != ".gz":
        fingerprint_marker = json.dumps(
            checkpoint_fingerprint, ensure_ascii=True,
        ).encode("ascii")
        fingerprint_rows: list[dict[str, Any]] = []
        fast_rows: list[dict[str, Any]] = []
        checkpoint_rows: list[tuple[int, dict[str, Any]]] = []
        try:
            with path.open("rb") as raw_handle:
                if os.fstat(raw_handle.fileno()).st_size:
                    with mmap.mmap(
                        raw_handle.fileno(), 0, access=mmap.ACCESS_READ,
                    ) as mapped:
                        line_offsets: set[tuple[int, int]] = set()
                        position = 0
                        while True:
                            found = mapped.find(fingerprint_marker, position)
                            if found < 0:
                                break
                            start = mapped.rfind(b"\n", 0, found) + 1
                            end = mapped.find(b"\n", found)
                            if end < 0:
                                end = len(mapped)
                            line_offsets.add((start, end))
                            position = found + len(fingerprint_marker)
                        fingerprint_rows_with_offsets: list[
                            tuple[int, dict[str, Any]]
                        ] = []
                        for start, end in sorted(line_offsets):
                            try:
                                row = json.loads(mapped[start:end])
                            except (UnicodeDecodeError, json.JSONDecodeError):
                                continue
                            if (
                                isinstance(row, dict)
                                and str(row.get("implementation_fingerprint") or "")
                                == checkpoint_fingerprint
                                and row.get("record_type")
                                in CT_M0F_STANDING_VALIDATION_FINGERPRINT_SCOPED_RECORD_TYPES
                            ):
                                fingerprint_rows.append(row)
                                fingerprint_rows_with_offsets.append(
                                    (start, row)
                                )
                        checkpoint_rows = [
                            (start, row)
                            for start, row in fingerprint_rows_with_offsets
                            if row.get("record_type")
                            == CT_M0F_STANDING_VALIDATION_LINEAGE_CHECKPOINT_RECORD_TYPE
                            and row.get(
                                "no_prior_campaign_records_for_fingerprint"
                            ) is True
                            and (
                                not required_ids
                                or str(row.get("decision_id") or "")
                                in required_ids
                            )
                        ]
                        supporting_rows: list[dict[str, Any]] = []
                        supporting_ids: set[str] = set()
                        if len(checkpoint_rows) == 1:
                            checkpoint = checkpoint_rows[0][1]
                            checkpoint_hash = str(
                                checkpoint.get("record_hash") or ""
                            )
                            checkpoint_hash_valid = bool(
                                len(checkpoint_hash) == 64
                                and checkpoint_hash
                                == sha256_bytes(canonical_json({
                                    key: value
                                    for key, value in checkpoint.items()
                                    if key != "record_hash"
                                }).encode("utf-8"))
                            )
                            if not checkpoint_hash_valid:
                                checkpoint_rows = []
                            for row in (
                                checkpoint.get(
                                    "supporting_authority_records"
                                ) or []
                            ):
                                if not isinstance(row, dict):
                                    continue
                                decision_id = str(
                                    row.get("decision_id") or ""
                                )
                                record_hash = str(row.get("record_hash") or "")
                                if (
                                    row.get("record_type")
                                    not in durable_record_types
                                    or not decision_id
                                    or len(record_hash) != 64
                                    or record_hash
                                    != sha256_bytes(canonical_json({
                                        key: value
                                        for key, value in row.items()
                                        if key != "record_hash"
                                    }).encode("utf-8"))
                                ):
                                    continue
                                supporting_rows.append(row)
                                supporting_ids.add(decision_id)
                        checkpoint_decision_ids = {
                            str(row.get("decision_id") or "")
                            for _, row in checkpoint_rows
                            if str(row.get("decision_id") or "")
                        }
                        required_authority_covered = set(required_ids).issubset(
                            checkpoint_decision_ids | supporting_ids
                        )
                        if (
                            len(checkpoint_rows) == 1
                            and required_authority_covered
                        ):
                            if not include_runtime_actions:
                                fast_rows = list(fingerprint_rows) + supporting_rows
                            else:
                                # Runtime clearance/lease records do not carry
                                # the CT fingerprint.  They are nevertheless
                                # part of this exact cohort when they occur
                                # after its immutable checkpoint.  The
                                # fingerprint search above already retained
                                # every CT durable cohort row, so scanning and
                                # JSON-decoding every unrelated audit row in
                                # the suffix only makes later warm samples
                                # slower as the journal grows.  Search for the
                                # exact clearance verdict and decode only its
                                # containing lines; the predicate below still
                                # rejects nested or look-alike payloads.
                                fast_rows = list(fingerprint_rows) + supporting_rows
                                checkpoint_start = checkpoint_rows[0][0]
                                runtime_marker = json.dumps(
                                    "RESTORE_BARRIER_CLEARANCE_WRITTEN",
                                    ensure_ascii=True,
                                ).encode("ascii")
                                runtime_line_offsets: set[
                                    tuple[int, int]
                                ] = set()
                                position = checkpoint_start
                                while True:
                                    found = mapped.find(
                                        runtime_marker, position
                                    )
                                    if found < 0:
                                        break
                                    start = (
                                        mapped.rfind(b"\n", 0, found) + 1
                                    )
                                    end = mapped.find(b"\n", found)
                                    if end < 0:
                                        end = len(mapped)
                                    runtime_line_offsets.add((start, end))
                                    position = found + len(runtime_marker)
                                for start, end in sorted(
                                    runtime_line_offsets
                                ):
                                    try:
                                        row = json.loads(mapped[start:end])
                                    except (
                                        UnicodeDecodeError,
                                        json.JSONDecodeError,
                                    ):
                                        continue
                                    if not isinstance(row, dict):
                                        continue
                                    runtime_action = bool(
                                        row.get(
                                            "runtime_action_performed"
                                        ) is True
                                        and str(
                                            row.get("clearance_verdict") or ""
                                        )
                                        == "RESTORE_BARRIER_CLEARANCE_WRITTEN"
                                    )
                                    if runtime_action:
                                        fast_rows.append(row)
        except OSError:
            fingerprint_rows = []
            fast_rows = []
            checkpoint_rows = []
        if len(checkpoint_rows) == 1 and fast_rows:
            _LIVE_EXECUTION_LINEAGE_PROCESS_CACHE[cache_key] = tuple(
                copy.deepcopy(fast_rows)
            )
            return fast_rows

    durable_value_markers = tuple(
        json.dumps(value, ensure_ascii=True)
        for value in sorted(durable_record_types | durable_effect_classes)
    )
    runtime_value_markers = (
        json.dumps("RESTORE_BARRIER_CLEARANCE_WRITTEN"),
    ) if include_runtime_actions else ()
    appended_extension = _cached_live_execution_lineage_append_extension(
        path=path,
        max_rotated_segments=max(0, int(max_rotated_segments)),
        include_runtime_actions=bool(include_runtime_actions),
        required_ids=required_ids,
        checkpoint_fingerprint=checkpoint_fingerprint,
        source_signature=tuple(source_signature),
        durable_record_types=durable_record_types,
        durable_effect_classes=durable_effect_classes,
    )
    if appended_extension is not None:
        return copy.deepcopy(appended_extension)
    segment_records: list[list[dict[str, Any]]] = []
    found_required_ids: set[str] = set()
    # A caller that names the exact current Authority decision needs the
    # complete newer lineage plus that immutable decision, not unrelated
    # older contracts.  Scan newest -> oldest and stop only after every exact
    # requested decision is found.  The returned records are still restored
    # to oldest -> newest order below.  Callers without an exact decision keep
    # the historical full bounded horizon unchanged.
    scan_names = names if required_ids else list(reversed(names))
    for candidate in scan_names:
        current_segment: list[dict[str, Any]] = []
        try:
            opener = gzip.open if candidate.suffix == ".gz" else open
            candidate_lines: list[str] = []
            if candidate.suffix != ".gz":
                # The active production journal is append-only and can be
                # hundreds of MiB, while durable lineage occupies only a tiny
                # fraction of its rows. Search immutable enum values in the
                # kernel-backed mapping and decode only the containing lines.
                # This is still a direct read of the canonical audit owner:
                # no index, sidecar, cache, watcher or alternate truth is
                # created, and the exact predicates below remain unchanged.
                encoded_markers = tuple(
                    marker.encode("ascii")
                    for marker in durable_value_markers
                    + runtime_value_markers
                )
                line_offsets: set[tuple[int, int]] = set()
                with candidate.open("rb") as raw_handle:
                    if os.fstat(raw_handle.fileno()).st_size:
                        with mmap.mmap(
                            raw_handle.fileno(), 0, access=mmap.ACCESS_READ
                        ) as mapped:
                            # One C-level alternation pass replaces one full
                            # mmap scan per durable enum value.  On the active
                            # audit this removes repeated traversal of hundreds
                            # of MiB from the failure-to-decision path while
                            # preserving the exact same line and JSON checks.
                            marker_pattern = re.compile(
                                b"|".join(
                                    re.escape(marker)
                                    for marker in encoded_markers
                                )
                            )
                            for match in marker_pattern.finditer(mapped):
                                found = match.start()
                                start = mapped.rfind(b"\n", 0, found) + 1
                                end = mapped.find(b"\n", found)
                                if end < 0:
                                    end = len(mapped)
                                line_offsets.add((start, end))
                            candidate_lines = [
                                mapped[start:end].decode(
                                    "utf-8", errors="replace"
                                )
                                for start, end in sorted(line_offsets)
                            ]
            else:
                with opener(
                    candidate, "rt", encoding="utf-8", errors="replace"
                ) as handle:
                    candidate_lines = list(handle)
            for line in candidate_lines:
                if not line.strip():
                    continue
                # Most append-only audit rows are unrelated to current
                # Authority/receipt lineage. Test the immutable enum
                # values before JSON decoding: false positives are safe
                # (the exact predicates below still decide), while every
                # qualifying row necessarily contains one of these quoted
                # values regardless of JSON key ordering or whitespace.
                if not any(
                    marker in line
                    for marker in durable_value_markers
                    + runtime_value_markers
                ):
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                runtime_action = bool(
                    include_runtime_actions
                    and row.get("runtime_action_performed") is True
                    and str(row.get("clearance_verdict") or "")
                    == "RESTORE_BARRIER_CLEARANCE_WRITTEN"
                )
                if (
                    row.get("record_type") in durable_record_types
                    or row.get("effect_class") in durable_effect_classes
                    or runtime_action
                ):
                    if (
                        checkpoint_fingerprint
                        and row.get("record_type")
                        in CT_M0F_STANDING_VALIDATION_FINGERPRINT_SCOPED_RECORD_TYPES
                        and str(row.get("implementation_fingerprint") or "")
                        != checkpoint_fingerprint
                    ):
                        continue
                    current_segment.append(row)
                    decision_id = str(row.get("decision_id") or "")
                    if (
                        decision_id in required_ids
                        and (
                            row.get("record_type")
                            != CT_M0F_STANDING_VALIDATION_LINEAGE_CHECKPOINT_RECORD_TYPE
                            or (
                                checkpoint_fingerprint
                                and row.get("implementation_fingerprint")
                                == checkpoint_fingerprint
                            )
                        )
                    ):
                        found_required_ids.add(decision_id)
        except OSError:
            continue
        segment_records.append(current_segment)
        if required_ids and found_required_ids == set(required_ids):
            break
    if required_ids:
        segment_records.reverse()
    records = [
        row for segment in segment_records for row in segment
    ]
    # This cache is deliberately process-local and keyed by the stat identity
    # of the active file and every bounded rotated segment.  An append,
    # rotation or replacement therefore invalidates it without a watcher,
    # sidecar, registry or second source of truth.
    if len(_LIVE_EXECUTION_LINEAGE_PROCESS_CACHE) >= 16:
        _LIVE_EXECUTION_LINEAGE_PROCESS_CACHE.clear()
    _LIVE_EXECUTION_LINEAGE_PROCESS_CACHE[cache_key] = tuple(
        copy.deepcopy(records)
    )
    return records


def replay_seen(records, approval_id):
    for record in records:
        if record.get("approval_id") == approval_id:
            return True
    return False


def engineering_authority_replay_seen(records, request_id):
    if not request_id:
        return False
    return any(str(record.get("engineering_authority_request_id") or "") == str(request_id) for record in records)


def audit_replay_flags(audit_store, approval_id, engineering_request_id=""):
    """Stream only rows which can match the two one-use replay keys.

    The canonical journal remains the sole replay owner.  Materializing every
    unrelated historical payload before an emergency cutover added latency
    and memory without strengthening the equality check performed by
    ``replay_seen``.  The byte prefilter is only an optimization; matching
    rows are still JSON-decoded and compared by field.
    """
    path = Path(audit_store)
    if not path.exists():
        return {
            "approval_seen": False,
            "engineering_authority_seen": False,
        }
    approval_id = str(approval_id or "")
    engineering_request_id = str(engineering_request_id or "")
    approval_marker = (
        f'"approval_id":{json.dumps(approval_id, ensure_ascii=True)}'
        if approval_id else ""
    )
    authority_marker = (
        '"engineering_authority_request_id":'
        + json.dumps(engineering_request_id, ensure_ascii=True)
        if engineering_request_id else ""
    )
    approval_seen = False
    authority_seen = False
    try:
        # The audit journal can be several hundred MB, while replay safety
        # needs equality for at most two immutable one-use identifiers.  Let
        # the kernel search the mapped bytes and JSON-decode only matching
        # lines.  This remains a direct read of the canonical append-only
        # owner; it adds no cache, index, watcher or second truth source.
        with path.open("rb") as handle:
            if os.fstat(handle.fileno()).st_size <= 0:
                return {
                    "approval_seen": False,
                    "engineering_authority_seen": False,
                }
            with mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as mapped:
                marker_kinds = []
                if approval_marker:
                    marker_kinds.append((approval_marker.encode("ascii"), "approval"))
                if authority_marker:
                    marker_kinds.append((authority_marker.encode("ascii"), "authority"))
                decoded_lines = set()
                for marker, _kind in marker_kinds:
                    offset = 0
                    while True:
                        position = mapped.find(marker, offset)
                        if position < 0:
                            break
                        line_start = mapped.rfind(b"\n", 0, position) + 1
                        line_end = mapped.find(b"\n", position)
                        if line_end < 0:
                            line_end = len(mapped)
                        identity = (line_start, line_end)
                        offset = position + max(1, len(marker))
                        if identity in decoded_lines:
                            continue
                        decoded_lines.add(identity)
                        try:
                            row = json.loads(
                                mapped[line_start:line_end].decode(
                                    "utf-8", errors="replace"
                                )
                            )
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            continue
                        approval_seen = approval_seen or bool(
                            approval_id
                            and str(row.get("approval_id") or "") == approval_id
                        )
                        authority_seen = authority_seen or bool(
                            engineering_request_id
                            and str(
                                row.get("engineering_authority_request_id") or ""
                            ) == engineering_request_id
                        )
                        if approval_seen and (
                            authority_seen or not engineering_request_id
                        ):
                            break
                    if approval_seen and (
                        authority_seen or not engineering_request_id
                    ):
                        break
    except OSError:
        # Preserve the old reader's absent/unreadable-file behavior: no row
        # was observable, and the later append remains the durable operation.
        pass
    return {
        "approval_seen": bool(approval_seen),
        "engineering_authority_seen": bool(authority_seen),
    }


def append_record(audit_store, record):
    path = Path(audit_store)
    path.parent.mkdir(parents=True, exist_ok=True)
    previous_record = read_last_audit_record(path)
    previous_hash = previous_record.get("record_hash", "GENESIS") if previous_record else "GENESIS"
    payload = {k: v for k, v in record.items() if k != "record_hash"}
    payload["previous_record_hash"] = previous_hash
    payload["record_hash"] = sha256_bytes(canonical_json(payload).encode("utf-8"))
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND
    fd = os.open(path, flags, 0o600)
    try:
        with os.fdopen(fd, "a", encoding="utf-8") as handle:
            handle.write(canonical_json(payload) + "\n")
    finally:
        try:
            os.chmod(path, 0o600)
        except OSError:
            pass
    return payload


def append_runtime_governance_action(governance_store, packet, recheck, now=None):
    now = now or utc_now()
    record = {
        "schema_version": "e23.zero-move-runtime-governance-action.v1",
        "record_type": "zero_move_governance_state_transition",
        "approval_id": packet.get("approval_id", ""),
        "packet_id": packet.get("packet_id", ""),
        "operation_id": packet.get("operation_id", ""),
        "selected_first_action": packet.get("selected_first_action", ""),
        "runtime_action": packet.get("runtime_action", ""),
        "created_at": now.isoformat(),
        "selected_move_budget": 0,
        "allowed_users": [],
        "allowed_targets": [],
        "rollback_manifest": packet.get("rollback_manifest", "NONE_NOT_REQUIRED"),
        "recheck_verdict": recheck.get("verdict"),
        "checks": recheck.get("checks", {}),
        "runtime_mutation_scope": "append_only_runtime_governance_state",
        "user_movement": False,
        "routing_mutation": False,
        "kill_switch_mutation": False,
        "autoswitch_apply": False,
        "canary": False,
    }
    return append_record(governance_store, redact(record))


def current_clearance_conflict(barrier):
    if not isinstance(barrier, dict) or not barrier:
        return ""
    owner = str(barrier.get("owner") or "")
    expires_at = str(barrier.get("clearance_expires_at") or "")
    active = bool(barrier.get("generation_clearance")) and bool(barrier.get("allow_post_ttl_apply"))
    if not active:
        return ""
    if expires_at and parse_ts(expires_at) <= utc_now():
        return ""
    if owner and owner != CANONICAL_CLEARANCE_OWNER:
        return "duplicate_clearance_owner"
    return ""


def build_restore_barrier_clearance(packet, now=None):
    now = now or utc_now()
    expected = packet.get("expected") or {}
    constraints = packet.get("constraints") or {}
    rollback_manifest = packet.get("rollback_manifest") or {}
    approved_plan_lock = dict(packet.get("approved_plan_lock") or {})
    engineering_authority = packet.get("engineering_authority") if isinstance(packet.get("engineering_authority"), dict) else {}
    clearance = {
        "schema_version": 1,
        "enabled": True,
        "expires_at": "2000-01-01T00:00:00+00:00",
        "allow_post_ttl_apply": True,
        "generation_clearance": True,
        "clearance_max_selected_moves": as_int(constraints.get("selected_move_budget"), 0),
        "clearance_expected_selected_moves": as_int(expected.get("selected_move_count"), 0),
        "clearance_generation_id": expected.get("generation_id", ""),
        "approved_selected_moves_hash": expected.get("selected_move_hash", ""),
        "approved_atomic_execution_envelope_id": expected.get("atomic_execution_envelope_id", ""),
        "approved_atomic_execution_envelope_hash": expected.get("atomic_execution_envelope_hash", ""),
        "approved_source_bundle_hash": expected.get("source_bundle_hash", ""),
        "approved_source_hashes": expected.get("source_hashes", {}),
        "approved_snapshot_bundle_hash": expected.get("snapshot_bundle_hash", ""),
        "clearance_expires_at": packet.get("expires_at", ""),
        "generation_token": packet.get("generation_token") or secrets.token_hex(16),
        "allowed_users": constraints.get("allowed_users") or [],
        "allowed_targets": constraints.get("allowed_targets") or [],
        "allowed_user": (constraints.get("allowed_users") or [""])[0],
        "allowed_target": (constraints.get("allowed_targets") or [""])[0],
        "approval_id": packet.get("approval_id", ""),
        "packet_id": packet.get("packet_id", ""),
        "operation_id": packet.get("operation_id", ""),
        "engineering_authority_request_id": engineering_authority.get("request_id", ""),
        "engineering_authority_contract_hash": engineering_authority.get("contract_hash", ""),
        "engineering_authority_transaction_nonce": engineering_authority.get("transaction_nonce", ""),
        "rollback_manifest_id": rollback_manifest.get("rollback_manifest_id", ""),
        "owner": CANONICAL_CLEARANCE_OWNER,
        "created_at": now.isoformat(),
        "reason": "C.1 canonical nonzero governance lifecycle clearance",
        "ttl_reason": "generation-bound execution readiness clearance",
    }
    if approved_plan_lock:
        approved_plan_lock["restore_barrier_id"] = stable_id("rbclear", clearance)
        approved_plan_lock["restore_barrier_hash"] = sha256_bytes(canonical_json(clearance).encode("utf-8"))
        clearance["approved_plan_lock"] = approved_plan_lock
        clearance["approved_plan_lock_id"] = approved_plan_lock.get("lock_id", "")
        clearance["approved_plan_lock_hash"] = approved_plan_lock.get("lock_hash", "")
    return clearance


def preview_restore_barrier_clearance(restore_barrier_file, packet, recheck, now=None):
    now = now or utc_now()
    path = Path(restore_barrier_file)
    current = {}
    if path.exists():
        try:
            current = read_json(path)
        except PacketError:
            current = {}
    conflict = current_clearance_conflict(current)
    if conflict:
        return {"ok": False, "verdict": "DENY_DUPLICATE_CLEARANCE_OWNER", "errors": [conflict]}
    clearance = build_restore_barrier_clearance(packet, now=now)
    return {
        "ok": True,
        "verdict": "RESTORE_BARRIER_CLEARANCE_PREVIEW_VALID",
        "restore_barrier_file": str(path),
        "clearance": redact(clearance),
        "recheck_verdict": recheck.get("verdict"),
        "runtime_mutation": False,
        "user_movement": False,
        "routing_mutation": False,
        "autoswitch_apply": False,
    }


def restore_barrier_operational_authority_package(packet, recheck):
    """Build a read-only Operational Authority package for one exact packet.

    The package is deliberately not an approval and cannot write a restore
    barrier.  It is emitted only after the canonical packet recheck passes, so
    an absent, stale or mismatched packet can never be presented as an
    Operational Authority decision surface.
    """
    identity = packet_identity(packet)
    required_identity = (
        "packet_id", "operation_id", "decision_id", "authority_generation",
        "source_bundle_hash", "snapshot_bundle_hash", "selected_move_hash",
        "user", "source", "target",
    )
    missing = [key for key in required_identity if not str(identity.get(key) or "")]
    ready = (
        packet.get("runtime_action") == RUNTIME_ACTION_CREATE_CLEARANCE
        and bool(recheck.get("allow"))
        and not missing
        and as_int(identity.get("max_users"), 0) == 1
        and as_int(identity.get("selected_move_count"), 0) == 1
    )
    return {
        "schema_version": "v7.restore-barrier-operational-authority-package.v1",
        "status": "OPERATIONAL_AUTHORITY_RESTORE_BARRIER_READY" if ready else "STOP_SAFE_PACKET_BOUND_OPERATIONAL_AUTHORITY_NOT_READY",
        "actionable": False,
        "packet_identity": identity,
        "recheck_verdict": str(recheck.get("verdict") or ""),
        "missing_identity_fields": missing,
        "scope": {
            "max_users": 1,
            "max_concurrent_transactions": 1,
            "user": identity.get("user", ""),
            "source": identity.get("source", ""),
            "target": identity.get("target", ""),
        },
        "exact_action": "INDEPENDENT_DECISION_ON_PACKET_BOUND_RESTORE_BARRIER_CLEARANCE",
        "forbidden_effects": [
            "restore_barrier_write_without_independent_operational_decision",
            "runtime_apply",
            "routing_mutation",
            "user_movement",
            "rollback_apply",
            "authority_expansion",
            "production_maturity_change",
        ],
        "reentry_condition": (
            "independent owner approves or declines this exact fresh packet; "
            "a later apply still rechecks the one-use Action Class contract"
        ) if ready else "fresh exact packet and canonical recheck are required",
    }


def append_restore_barrier_clearance(restore_barrier_file, packet, recheck, now=None):
    now = now or utc_now()
    path = Path(restore_barrier_file)
    current = {}
    if path.exists():
        try:
            current = read_json(path)
        except PacketError:
            current = {}
    conflict = current_clearance_conflict(current)
    if conflict:
        return {"ok": False, "verdict": "DENY_DUPLICATE_CLEARANCE_OWNER", "errors": [conflict]}
    clearance = build_restore_barrier_clearance(packet, now=now)
    backup_path = ""
    if path.exists():
        backup = path.with_name(f"{path.name}.backup-c1-{now.strftime('%Y%m%dT%H%M%SZ')}")
        backup.write_text(path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        backup_path = str(backup)
        clearance["backup_path"] = backup_path
    write_json_atomic(path, clearance)
    return {
        "ok": True,
        "verdict": "RESTORE_BARRIER_CLEARANCE_WRITTEN",
        "restore_barrier_file": str(path),
        "backup_path": backup_path,
        "clearance": redact(clearance),
        "recheck_verdict": recheck.get("verdict"),
    }


def append_lifecycle_records(lifecycle_store, packet, recheck, clearance_result, audit_record, now=None):
    now = now or utc_now()
    rollback_manifest = packet.get("rollback_manifest") or {}
    engineering_authority = packet.get("engineering_authority") if isinstance(packet.get("engineering_authority"), dict) else {}
    base = {
        "approval_id": packet.get("approval_id", ""),
        "packet_id": packet.get("packet_id", ""),
        "operation_id": packet.get("operation_id", ""),
        "selected_move_hash": (packet.get("expected") or {}).get("selected_move_hash", ""),
        "selected_move_count": (packet.get("expected") or {}).get("selected_move_count", 0),
        "atomic_execution_envelope_id": (packet.get("expected") or {}).get("atomic_execution_envelope_id", ""),
        "atomic_execution_envelope_hash": (packet.get("expected") or {}).get("atomic_execution_envelope_hash", ""),
        "created_at": now.isoformat(),
        "engineering_authority_request_id": engineering_authority.get("request_id", ""),
        "engineering_authority_contract_hash": engineering_authority.get("contract_hash", ""),
        "engineering_authority_transaction_nonce": engineering_authority.get("transaction_nonce", ""),
    }
    clearance_record = append_record(lifecycle_store, {
        "schema_version": "c1.governance-lifecycle-record.v1",
        "record_type": "restore_barrier_clearance_created",
        **base,
        "owner": CANONICAL_CLEARANCE_OWNER,
        "clearance_verdict": clearance_result.get("verdict"),
        "restore_barrier_file": clearance_result.get("restore_barrier_file", ""),
        "audit_record_hash": audit_record.get("record_hash", ""),
        "runtime_mutation_scope": "restore_barrier_clearance_only",
        "user_movement": False,
        "routing_mutation": False,
        "autoswitch_apply": False,
    })
    rollback_record = append_record(lifecycle_store, {
        "schema_version": "c1.governance-lifecycle-record.v1",
        "record_type": "operation_scoped_rollback_bound",
        **base,
        "rollback_owner": CANONICAL_CLEARANCE_OWNER,
        "rollback_manifest": rollback_manifest,
        "linked_audit_record_hash": audit_record.get("record_hash", ""),
        "rollback_execution_performed": False,
    })
    closure_record = append_record(lifecycle_store, {
        "schema_version": "c1.governance-lifecycle-record.v1",
        "record_type": "execution_readiness_closure_created",
        **base,
        "closure_owner": CANONICAL_CLEARANCE_OWNER,
        "closure_state": "EXECUTION_READY",
        "linked_audit_record_hash": audit_record.get("record_hash", ""),
        "linked_rollback_manifest_id": rollback_manifest.get("rollback_manifest_id", ""),
        "execution_allowed_now": True,
        "user_movement": False,
        "routing_mutation": False,
        "autoswitch_apply": False,
    })
    return {
        "clearance_record": clearance_record,
        "rollback_record": rollback_record,
        "closure_record": closure_record,
    }


def execute_packet(
    packet,
    audit_store,
    state_dir,
    now=None,
    mode="execute",
    runtime_governance_store=None,
    planner_snapshot=None,
    restore_barrier_file=None,
    lifecycle_store=None,
    execution_lease_id="",
):
    timing_started_ns = time.monotonic_ns()
    timing_cursor_ns = timing_started_ns
    timing_spans = []

    def mark_timing(stage):
        nonlocal timing_cursor_ns
        completed_ns = time.monotonic_ns()
        timing_spans.append({
            "stage": stage,
            "duration_ms": round(
                (completed_ns - timing_cursor_ns) / 1_000_000.0, 3
            ),
        })
        timing_cursor_ns = completed_ns

    now = now or utc_now()
    approval_id = packet.get("approval_id") or stable_id("appr", packet)
    engineering_authority = packet.get("engineering_authority") if isinstance(packet.get("engineering_authority"), dict) else {}
    engineering_request_id = str(engineering_authority.get("request_id") or "")
    replay = audit_replay_flags(
        audit_store, approval_id, engineering_request_id,
    )
    mark_timing("canonical_replay_recheck")
    if replay.get("engineering_authority_seen"):
        recheck = {"allow": False, "verdict": "DENY_REPLAY", "errors": ["engineering_authority_request_already_consumed"]}
    elif replay.get("approval_seen"):
        recheck = {"allow": False, "verdict": "DENY_REPLAY", "errors": ["approval_id_already_recorded"]}
    else:
        recheck = runtime_recheck(packet, state_dir, now=now, planner_snapshot=planner_snapshot)
    mark_timing("packet_and_runtime_recheck")
    if mode == "validate":
        return {"mode": mode, "approval_id": approval_id, "recheck": validate_packet(packet, now=now), "record_written": False}
    if mode == "recheck":
        return {"mode": mode, "approval_id": approval_id, "recheck": recheck, "record_written": False}
    runtime_action_record = None
    runtime_action_performed = False
    runtime_mutation = False
    clearance_result = None
    clearance_preview = None
    lifecycle_records = None
    if mode == "runtime_action_preview":
        if packet.get("runtime_action") == RUNTIME_ACTION_CREATE_CLEARANCE:
            if recheck.get("allow"):
                if not restore_barrier_file:
                    raise PacketError("restore_barrier_file_required")
                clearance_preview = preview_restore_barrier_clearance(restore_barrier_file, packet, recheck, now=now)
                if not clearance_preview.get("ok"):
                    recheck = {
                        "allow": False,
                        "verdict": clearance_preview.get("verdict", "DENY_CLEARANCE_PREVIEW"),
                        "errors": clearance_preview.get("errors", []),
                    }
        else:
            recheck = {
                "allow": False,
                "verdict": "DENY_RUNTIME_ACTION_UNSUPPORTED",
                "errors": ["runtime_action_not_supported_by_canonical_owner"],
            }
        return {
            "mode": mode,
            "approval_id": approval_id,
            "recheck": recheck,
            "record_written": False,
            "runtime_action_record": None,
            "clearance_preview": clearance_preview,
            "operational_authority_package": (
                restore_barrier_operational_authority_package(packet, recheck)
                if packet.get("runtime_action") == RUNTIME_ACTION_CREATE_CLEARANCE else None
            ),
            "execution_allowed_now": False,
            "real_runtime_action_performed": False,
            "runtime_mutation": False,
            "user_movement": False,
            "routing_mutation": False,
            "autoswitch_apply": False,
        }
    if mode == "runtime_action":
        if engineering_authority and recheck.get("allow"):
            if not execution_lease_id:
                recheck = {
                    "allow": False,
                    "verdict": "DENY_ENGINEERING_AUTHORITY_PARTIAL_BINDING",
                    "errors": ["engineering_authority_execution_lease_id_missing"],
                }
            else:
                append_record(audit_store, {
                    "schema_version": "v7.engineering-authority-consumption.v1",
                    "record_type": "engineering_authority_consumed",
                    "engineering_authority_request_id": engineering_request_id,
                    "engineering_authority_contract_hash": engineering_authority.get("contract_hash", ""),
                    "engineering_authority_decision": engineering_authority.get("decision", ""),
                    "engineering_authority_decision_provenance": copy.deepcopy(
                        engineering_authority.get("decision_provenance")
                        if isinstance(engineering_authority.get("decision_provenance"), dict)
                        else {}
                    ),
                    "transaction_nonce": engineering_authority.get("transaction_nonce", ""),
                    "approval_id": approval_id,
                    "packet_id": packet.get("packet_id", ""),
                    "operation_id": packet.get("operation_id", ""),
                    "execution_lease_id": str(execution_lease_id),
                    "created_at": now.isoformat(),
                    "one_use": True,
                    "retry_allowed": False,
                    "runtime_mutation": False,
                    "user_movement": False,
                    "routing_mutation": False,
                })
                mark_timing("engineering_authority_consumption")
        if packet.get("runtime_action") == RUNTIME_ACTION_ZERO_MOVE_GOVERNANCE:
            if recheck.get("allow"):
                if runtime_governance_store is None:
                    raise PacketError("runtime_governance_store_required")
                runtime_action_record = append_runtime_governance_action(
                    runtime_governance_store,
                    packet,
                    recheck,
                    now=now,
                )
                runtime_action_performed = True
                runtime_mutation = True
        elif packet.get("runtime_action") == RUNTIME_ACTION_CREATE_CLEARANCE:
            if recheck.get("allow"):
                if not restore_barrier_file:
                    raise PacketError("restore_barrier_file_required")
                clearance_result = append_restore_barrier_clearance(restore_barrier_file, packet, recheck, now=now)
                mark_timing("restore_barrier_clearance_write")
                if clearance_result.get("ok"):
                    runtime_action_performed = True
                    runtime_mutation = True
                else:
                    recheck = {
                        "allow": False,
                        "verdict": clearance_result.get("verdict", "DENY_CLEARANCE_WRITE"),
                        "errors": clearance_result.get("errors", []),
                    }
        else:
            recheck = {
                "allow": False,
                "verdict": "DENY_RUNTIME_ACTION_UNSUPPORTED",
                "errors": ["runtime_action_not_supported_by_canonical_owner"],
            }
    record_type = "approval_record_persisted" if recheck.get("allow") else "denial_record"
    if mode == "runtime_action" and recheck.get("allow"):
        record_type = "runtime_action_record_persisted"
    record = {
        "schema_version": "e22.operator-execution-audit-record.v1",
        "record_type": record_type,
        "approval_id": approval_id,
        "packet_id": packet.get("packet_id", ""),
        "operation_id": packet.get("operation_id", ""),
        "selected_first_action": packet.get("selected_first_action", ""),
        "runtime_action": packet.get("runtime_action", ""),
        "verdict": recheck.get("verdict"),
        "errors": recheck.get("errors", []),
        "checks": recheck.get("checks", {}),
        "created_at": now.isoformat(),
        "runtime_mutation": runtime_mutation,
        "runtime_mutation_scope": (
            "restore_barrier_clearance_only"
            if clearance_result and clearance_result.get("ok")
            else ("append_only_runtime_governance_state" if runtime_mutation else "none")
        ),
        "user_movement": False,
        "routing_mutation": False,
        "kill_switch_mutation": False,
        "autoswitch_apply": False,
        "canary": False,
        "runtime_action_performed": runtime_action_performed,
        "runtime_action_record_hash": runtime_action_record.get("record_hash") if runtime_action_record else "",
        "clearance_verdict": clearance_result.get("verdict") if clearance_result else "",
        "engineering_authority_request_id": engineering_request_id,
    }
    redacted_record = redact(record)
    mark_timing("audit_record_redaction")
    written = append_record(audit_store, redacted_record)
    mark_timing("canonical_audit_append")
    if clearance_result and clearance_result.get("ok") and lifecycle_store:
        lifecycle_records = append_lifecycle_records(lifecycle_store, packet, recheck, clearance_result, written, now=now)
    mark_timing("lifecycle_projection_append")
    return {
        "mode": mode,
        "approval_id": approval_id,
        "recheck": recheck,
        "record_written": True,
        "record": written,
        "runtime_action_record": runtime_action_record,
        "clearance_result": clearance_result,
        "lifecycle_records": lifecycle_records,
        "execution_allowed_now": bool(clearance_result and clearance_result.get("ok")),
        "real_runtime_action_performed": runtime_action_performed,
        "execution_timing": {
            "schema_version": "v7.operator-execution-hot-path-timing.v1",
            "clock_source": "time.monotonic_ns",
            "total_duration_ms": round(
                (time.monotonic_ns() - timing_started_ns) / 1_000_000.0, 3
            ),
            "spans": timing_spans,
        },
    }


def load_optional_json(path):
    if not path:
        return None
    return read_json(path)


def extract_packet_preview(payload):
    if not isinstance(payload, dict):
        return {}
    if payload.get("packet_id") and payload.get("selected_move_hash"):
        return payload
    direct = payload.get("packet_preview")
    if isinstance(direct, dict) and direct.get("packet_id") and direct.get("selected_move_hash"):
        return direct
    pipeline = payload.get("operator_execution_pipeline")
    if isinstance(pipeline, dict):
        pipeline_preview = pipeline.get("packet_preview")
        if isinstance(pipeline_preview, dict) and pipeline_preview.get("packet_id") and pipeline_preview.get("selected_move_hash"):
            return pipeline_preview
    stack = list(payload.values())
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            if item.get("packet_id") and item.get("selected_move_hash"):
                return item
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
    return {}


def selected_moves_from_preview(preview):
    preview = extract_packet_preview(preview)
    packet_id = str(preview.get("packet_id") or "")
    operation_id = str(preview.get("operation_id") or "")
    decision_id = str(preview.get("decision_id") or "")
    authority_generation = str(
        preview.get("authority_generation")
        or preview.get("current_state_generation")
        or preview.get("cycle_id")
        or ""
    )
    selected_hash = str(preview.get("selected_move_hash") or "")
    selected_count = as_int(preview.get("selected_move_count"), 0)
    allowed_users = [str(item) for item in (preview.get("allowed_users") or []) if str(item)]
    allowed_targets = [str(item) for item in (preview.get("allowed_targets") or []) if str(item)]
    rollback_preview = preview.get("rollback_manifest_preview") or {}
    rollback_items = rollback_preview.get("items") or []
    moves = []
    for index, item in enumerate(rollback_items):
        if not isinstance(item, dict):
            continue
        user_ip = str(item.get("user_ip") or (allowed_users[index] if index < len(allowed_users) else ""))
        current = str(item.get("rollback_target") or item.get("current_egress") or "")
        target = str(item.get("forward_target") or item.get("recommended_egress") or (allowed_targets[0] if allowed_targets else ""))
        if user_ip and current and target:
            move = {
                "user_ip": user_ip,
                "current_egress": current,
                "recommended_egress": target,
                "move_type": str(item.get("move_type") or "governed_canary"),
            }
            for key in SELECTED_MOVE_SEMANTIC_FIELDS:
                if key in item:
                    move[key] = copy.deepcopy(item.get(key))
            moves.append(move)
    if not moves and allowed_users and allowed_targets:
        moves.append({
            "user_ip": allowed_users[0],
            "current_egress": str(preview.get("from") or preview.get("current_channel") or ""),
            "recommended_egress": allowed_targets[0],
            "move_type": "governed_canary",
        })
    preview_source_hashes = preview.get("source_hashes") if isinstance(preview.get("source_hashes"), dict) else {}
    source_hashes = {str(key): str(value) for key, value in preview_source_hashes.items() if str(key) and str(value)}
    source_bundle_hash = sha256_json(source_hashes) if source_hashes else ""
    snapshot_bundle_hash = str(preview.get("snapshot_bundle_hash") or "")
    if source_hashes.get("users_registry") and source_hashes.get("egress_registry"):
        runtime_snapshot_hash = sha256_json({
            "users_registry_hash": source_hashes.get("users_registry", ""),
            "egress_registry_hash": source_hashes.get("egress_registry", ""),
            "selected_move_hash": selected_hash,
        })
    else:
        runtime_snapshot_hash = sha256_json({
            "authority_generation": authority_generation,
            "selected_move_hash": selected_hash,
            "selected_move_count": selected_count,
        })
    envelope_payload = {
        "planner_generation_id": authority_generation,
        "selected_move_hash": selected_hash,
        "selected_move_count": selected_count,
        "runtime_snapshot_hash": runtime_snapshot_hash,
        "source_bundle_hash": source_bundle_hash,
        "snapshot_bundle_hash": snapshot_bundle_hash,
    }
    envelope_hash = sha256_json(envelope_payload)
    return {
        "identity_source": "approved_preview_packet",
        "decision_id": decision_id,
        "authority_generation": authority_generation,
        "planner_generation_id": authority_generation,
        "selected_move_hash": selected_hash,
        "selected_move_count": selected_count,
        "moves": moves,
        "constraints": {
            "allowed_users": allowed_users,
            "allowed_targets": allowed_targets,
        },
        "runtime_snapshot_hash": runtime_snapshot_hash,
        "atomic_execution_envelope_id": "aee_" + envelope_hash[:24],
        "atomic_execution_envelope_hash": envelope_hash,
        "source_bundle_hash": source_bundle_hash,
        "source_hashes": source_hashes,
        "snapshot_bundle_hash": snapshot_bundle_hash,
    }


def packet_from_preview(
    preview,
    *,
    approval_author,
    approval_reviewer,
    ttl_seconds=DEFAULT_CLEARANCE_TTL_SECONDS,
    breaker_generation="",
    require_execution_binding=False,
    delegated_policy_authority=None,
    engineering_authority=None,
    service_failure_causal_binding=None,
):
    preview = extract_packet_preview(preview)
    now = utc_now()
    expires_at = now + timedelta(seconds=max(1, as_int(ttl_seconds, DEFAULT_CLEARANCE_TTL_SECONDS)))
    selected = selected_moves_from_preview(preview)
    moves = selected.get("moves") or []
    packet_id = str(preview.get("packet_id") or "")
    operation_id = str(preview.get("operation_id") or "")
    decision_id = str(preview.get("decision_id") or "")
    authority_generation = str(selected.get("authority_generation") or "")
    if not packet_id:
        raise PacketError("preview_packet_id_missing")
    if not operation_id:
        raise PacketError("preview_operation_id_missing")
    if not decision_id:
        raise PacketError("preview_decision_id_missing")
    if not authority_generation:
        raise PacketError("preview_authority_generation_missing")
    if not selected.get("selected_move_hash"):
        raise PacketError("preview_selected_move_hash_missing")
    if not moves:
        raise PacketError("preview_selected_moves_missing")
    allowed_users = [move["user_ip"] for move in moves]
    allowed_targets = sorted({move["recommended_egress"] for move in moves})
    rollback_preview = preview.get("rollback_manifest_preview") or {}
    packet = {
        "schema_version": GOVERNANCE_PACKET_SCHEMA,
        "identity_source": "approved_preview_packet",
        "packet_id": packet_id,
        "approval_id": stable_id("appr", {
            "packet_id": packet_id,
            "operation_id": operation_id,
            "decision_id": decision_id,
            "expires_at": expires_at.isoformat(),
        }),
        "operation_id": operation_id,
        "decision_id": decision_id,
        "authority_generation": authority_generation,
        "breaker_generation": str(breaker_generation or preview.get("breaker_generation") or "UNBOUND_READ_ONLY"),
        "selected_first_action": NONZERO_ACTION,
        "runtime_action": RUNTIME_ACTION_CREATE_CLEARANCE,
        "created_at": now.isoformat(),
        "expires_at": expires_at.isoformat(),
        "approvals": [] if delegated_policy_authority else [
            {"operator_id": approval_author, "role": "approval_author", "confirmed_at": now.isoformat()},
            {"operator_id": approval_reviewer, "role": "approval_reviewer", "confirmed_at": now.isoformat()},
        ],
        "delegated_policy_authority": copy.deepcopy(delegated_policy_authority or {}),
        "engineering_authority": copy.deepcopy(engineering_authority or {}),
        "constraints": {
            "selected_move_budget": as_int(selected.get("selected_move_count"), 0),
            "allowed_users": allowed_users,
            "allowed_targets": allowed_targets,
            "user_movement_allowed": False,
            "routing_mutation_allowed": False,
            "autoswitch_apply_allowed": False,
        },
        "expected": {
            "generation_id": authority_generation,
            "decision_id": decision_id,
            "selected_move_hash": selected.get("selected_move_hash", ""),
            "selected_move_count": as_int(selected.get("selected_move_count"), 0),
            "runtime_snapshot_hash": selected.get("runtime_snapshot_hash", ""),
            "atomic_execution_envelope_id": selected.get("atomic_execution_envelope_id", ""),
            "atomic_execution_envelope_hash": selected.get("atomic_execution_envelope_hash", ""),
            "source_bundle_hash": selected.get("source_bundle_hash", ""),
            "source_hashes": selected.get("source_hashes", {}),
            "snapshot_bundle_hash": selected.get("snapshot_bundle_hash", ""),
        },
        "rollback_manifest": {
            "rollback_manifest_id": str(rollback_preview.get("rollback_manifest_id") or stable_id("rb", {
                "packet_id": packet_id,
                "operation_id": operation_id,
                "selected_move_hash": selected.get("selected_move_hash", ""),
            })),
            "source_operation_id": operation_id,
            "items": [
                {
                    "user_ip": move["user_ip"],
                    "rollback_target": move["current_egress"],
                    "forward_target": move["recommended_egress"],
                    "move_type": move.get("move_type", ""),
                    "source_operation_id": operation_id,
                    "selected_move_hash": selected.get("selected_move_hash", ""),
                }
                for move in moves
            ],
            "partial_failure_policy": "stop_and_contain",
            "rollback_execution_owner": CANONICAL_CLEARANCE_OWNER,
        },
        "execution_metadata": {
            "identity_source": "approved_preview_packet",
            "preview_schema_version": preview.get("schema_version", ""),
            "materialized_at": now.isoformat(),
            "semantic_identity_preserved": True,
            "execution_metadata_only_added": True,
            "operation_scoped_binding_required": bool(require_execution_binding),
        },
        "governance_owner": CANONICAL_CLEARANCE_OWNER,
    }
    if service_failure_causal_binding is not None:
        packet["service_failure_causal_binding"] = copy.deepcopy(service_failure_causal_binding)
    if engineering_authority:
        packet["approval_id"] = stable_id("appr", {
            "packet_id": packet_id,
            "operation_id": operation_id,
            "decision_id": decision_id,
            "engineering_authority_request_id": engineering_authority.get("request_id", ""),
            "transaction_nonce": engineering_authority.get("transaction_nonce", ""),
            "expires_at": expires_at.isoformat(),
        })
    packet_hash = sha256_bytes(canonical_json(packet).encode("utf-8"))
    packet["approved_plan_lock"] = approved_plan_lock_from_selected(selected, packet, packet_hash)
    validation = validate_packet(packet, now=now)
    if not validation.get("ok"):
        raise PacketError(",".join(validation.get("errors") or ["packet_invalid"]))
    return packet


def packet_from_plan(
    plan,
    *,
    approval_author,
    approval_reviewer,
    ttl_seconds=DEFAULT_CLEARANCE_TTL_SECONDS,
    breaker_generation="",
    delegated_policy_authority=None,
    service_failure_causal_binding=None,
):
    now = utc_now()
    expires_at = now + timedelta(seconds=max(1, as_int(ttl_seconds, DEFAULT_CLEARANCE_TTL_SECONDS)))
    selected = selected_moves_from_plan(plan)
    moves = selected.get("moves") or []
    if not moves:
        raise PacketError("planner_snapshot_has_no_candidate_moves")
    allowed_users = [move["user_ip"] for move in moves]
    allowed_targets = sorted({move["recommended_egress"] for move in moves})
    operation_payload = {
        "planner_generation_id": selected.get("planner_generation_id"),
        "selected_move_hash": selected.get("selected_move_hash"),
        "selected_move_count": selected.get("selected_move_count"),
        "allowed_users": allowed_users,
        "allowed_targets": allowed_targets,
        "breaker_generation": str(breaker_generation or plan.get("breaker_generation") or "UNBOUND_READ_ONLY"),
    }
    operation_id = stable_id("govexec", operation_payload)
    packet = {
        "schema_version": GOVERNANCE_PACKET_SCHEMA,
        "packet_id": stable_id("pkt", {**operation_payload, "created_at": now.isoformat()}),
        "approval_id": stable_id("appr", {**operation_payload, "expires_at": expires_at.isoformat()}),
        "operation_id": operation_id,
        "breaker_generation": operation_payload["breaker_generation"],
        "selected_first_action": NONZERO_ACTION,
        "runtime_action": RUNTIME_ACTION_CREATE_CLEARANCE,
        "created_at": now.isoformat(),
        "expires_at": expires_at.isoformat(),
        "approvals": [] if delegated_policy_authority else [
            {"operator_id": approval_author, "role": "approval_author", "confirmed_at": now.isoformat()},
            {"operator_id": approval_reviewer, "role": "approval_reviewer", "confirmed_at": now.isoformat()},
        ],
        "delegated_policy_authority": copy.deepcopy(delegated_policy_authority or {}),
        "constraints": {
            "selected_move_budget": as_int(selected.get("selected_move_count"), 0),
            "allowed_users": allowed_users,
            "allowed_targets": allowed_targets,
            "user_movement_allowed": False,
            "routing_mutation_allowed": False,
            "autoswitch_apply_allowed": False,
        },
        "expected": {
            "generation_id": selected.get("planner_generation_id", ""),
            "selected_move_hash": selected.get("selected_move_hash", ""),
            "selected_move_count": as_int(selected.get("selected_move_count"), 0),
            "runtime_snapshot_hash": selected.get("runtime_snapshot_hash", ""),
            "atomic_execution_envelope_id": selected.get("atomic_execution_envelope_id", ""),
            "atomic_execution_envelope_hash": selected.get("atomic_execution_envelope_hash", ""),
            "source_bundle_hash": selected.get("source_bundle_hash", ""),
            "source_hashes": selected.get("source_hashes", {}),
            "snapshot_bundle_hash": selected.get("snapshot_bundle_hash", ""),
        },
        "rollback_manifest": {
            "rollback_manifest_id": stable_id("rb", operation_payload),
            "source_operation_id": operation_id,
            "items": [
                {
                    "user_ip": move["user_ip"],
                    "rollback_target": move["current_egress"],
                    "forward_target": move["recommended_egress"],
                    "move_type": move.get("move_type", ""),
                    "source_operation_id": operation_id,
                    "selected_move_hash": selected.get("selected_move_hash", ""),
                }
                for move in moves
            ],
            "partial_failure_policy": "stop_and_contain",
            "rollback_execution_owner": CANONICAL_CLEARANCE_OWNER,
        },
        "governance_owner": CANONICAL_CLEARANCE_OWNER,
    }
    if service_failure_causal_binding:
        packet["service_failure_causal_binding"] = copy.deepcopy(
            service_failure_causal_binding
        )
    packet_hash = sha256_bytes(canonical_json(packet).encode("utf-8"))
    packet["approved_plan_lock"] = approved_plan_lock_from_selected(selected, packet, packet_hash)
    validation = validate_packet(packet, now=now)
    if not validation.get("ok"):
        raise PacketError(",".join(validation.get("errors") or ["packet_invalid"]))
    return packet


def load_packet(path, repo_root):
    packet_path = resolve_under_repo(path, repo_root)
    return read_json(packet_path), packet_path


def _issue_current_action_class_contract_request_to_policy(
    policy_path, request, *, decision, expected_request_id="", expected_request_hash="", now=None,
    audit_store=None, actor_id="",
):
    """Persist one already-materialized request through the existing Authority owner."""
    policy_path = Path(policy_path)
    request = request if isinstance(request, dict) else {}
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    now = now or utc_now()
    with current_action_class_contract_policy_lock(policy_path):
        policy_generation_hash = sha256_file(policy_path)
        if _current_action_class_decision_records(read_audit_records(audit_store), request.get("request_id")):
            raise PacketError("current_action_class_contract_authority_decision_already_recorded")
        validation = validate_current_action_class_contract_authority_request(
            request, decision=decision, expected_request_id=expected_request_id,
            expected_request_hash=expected_request_hash, now=now,
        )
        if not validation.get("ok"):
            raise PacketError(",".join(validation.get("errors") or ["current_action_class_contract_request_invalid"]))
        if str(request.get("policy_generation_hash") or "") != policy_generation_hash:
            raise PacketError("current_action_class_contract_policy_generation_changed")
        decision_record = append_record(audit_store, _current_action_class_contract_audit_record(
            request, decision=decision, actor_id=actor_id,
            policy_generation_hash=policy_generation_hash, now=now,
        ))
        result = issue_current_action_class_contract(
            read_json(policy_path), request, decision=decision,
            expected_request_id=expected_request_id, expected_request_hash=expected_request_hash,
            now=now, authority_actor_id=actor_id,
            authority_decision_id=decision_record["decision_id"],
        )
        write_json_atomic(policy_path, result["policy"])
    return {
        "status": "ISSUED",
        "policy_path": str(policy_path),
        "contract": result["contract"],
        "authority_owner": CURRENT_ACTION_CLASS_CONTRACT_ISSUING_OWNER,
        "policy_write": True,
        "authority_granted": False,
        "runtime_apply": False,
        "routing_mutation": False,
        "users_moved": 0,
        "candidate_created": False,
        "packet_created": False,
        "lease_created": False,
        "production_maturity_changed": False,
        "authority_decision_audit": {
            "decision_id": decision_record["decision_id"],
            "audit_store": str(audit_store),
            "actor_id": str(actor_id),
            "append_only": True,
        },
    }


def issue_current_action_class_contract_to_policy(
    policy_path, request_path, *, decision, expected_request_id="", expected_request_hash="", now=None,
    audit_store=None, actor_id="",
):
    """Persist a contract from one supplied exact request JSON preimage."""
    return _issue_current_action_class_contract_request_to_policy(
        policy_path, read_json(Path(request_path)), decision=decision,
        expected_request_id=expected_request_id, expected_request_hash=expected_request_hash,
        now=now, audit_store=audit_store, actor_id=actor_id,
    )


def issue_current_action_class_contract_from_audit(
    policy_path, *, request_id, request_hash, decision, now=None, audit_store=None, actor_id="",
):
    """Issue only the exact unexpired request preimage held by the audit owner."""
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    request = current_action_class_contract_request_from_audit(
        request_id, request_hash, audit_store=audit_store, now=now,
    )
    return _issue_current_action_class_contract_request_to_policy(
        policy_path, request, decision=decision, expected_request_id=request_id,
        expected_request_hash=request_hash, now=now, audit_store=audit_store,
        actor_id=actor_id,
    )


def decline_current_action_class_contract_request(
    policy_path, request_path, *, decision, expected_request_id="", expected_request_hash="", now=None,
    audit_store=None, actor_id="",
):
    """Record one owner-backed decline without writing an action-class contract."""
    if decision != "DECLINE":
        raise PacketError("current_action_class_contract_decline_not_exact")
    policy_path = Path(policy_path)
    request = read_json(Path(request_path))
    audit_store = Path(audit_store or DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
    now = now or utc_now()
    with current_action_class_contract_policy_lock(policy_path):
        policy_generation_hash = sha256_file(policy_path)
        if _current_action_class_decision_records(read_audit_records(audit_store), request.get("request_id")):
            raise PacketError("current_action_class_contract_authority_decision_already_recorded")
        validation = validate_current_action_class_contract_authority_request(
            request, decision=decision, expected_request_id=expected_request_id,
            expected_request_hash=expected_request_hash, now=now, allow_decline=True,
        )
        if not validation.get("ok"):
            raise PacketError(",".join(validation.get("errors") or ["current_action_class_contract_decline_invalid"]))
        if str(request.get("policy_generation_hash") or "") != policy_generation_hash:
            raise PacketError("current_action_class_contract_policy_generation_changed")
        decision_record = append_record(audit_store, _current_action_class_contract_audit_record(
            request, decision=decision, actor_id=actor_id,
            policy_generation_hash=policy_generation_hash, now=now,
        ))
    return {
        "status": "DECLINED",
        "policy_path": str(policy_path),
        "policy_write": False,
        "authority_granted": False,
        "authority_decision_audit": {
            "decision_id": decision_record["decision_id"], "audit_store": str(audit_store),
            "actor_id": str(actor_id), "append_only": True,
        },
        "runtime_apply": False,
        "routing_mutation": False,
        "users_moved": 0,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate and consume V7 operator execution packets without user movement.")
    parser.add_argument("--packet")
    parser.add_argument("--generate-from-plan", default="")
    parser.add_argument("--generate-from-preview", default="")
    parser.add_argument("--packet-output", default="")
    parser.add_argument("--create-execution-lease", action="store_true")
    parser.add_argument("--execution-lease-file", default="")
    parser.add_argument("--cancel-execution-lease", action="store_true")
    parser.add_argument("--cancel-reason", default="operator_cancel")
    parser.add_argument("--finish-execution-lease", action="store_true")
    parser.add_argument("--finish-status", default="EXECUTION_FINISHED")
    parser.add_argument("--finish-reason", default="")
    parser.add_argument("--operation-result", default="")
    parser.add_argument("--approval-author", default="operator-a")
    parser.add_argument("--approval-reviewer", default="operator-b")
    parser.add_argument("--ttl-seconds", type=int, default=DEFAULT_CLEARANCE_TTL_SECONDS)
    parser.add_argument("--audit-store", default="docs/track7/productization/e22-evidence/operator-execution-audit.jsonl")
    parser.add_argument("--state-dir", default="/opt/v7/egress/state")
    parser.add_argument("--planner-snapshot", default="")
    parser.add_argument("--restore-barrier-file", default="/opt/v7/egress/state/autoswitch-restore-barrier.json")
    parser.add_argument("--lifecycle-store", default="docs/track7/productization/c1-evidence/governance-lifecycle.jsonl")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--recheck-only", action="store_true")
    parser.add_argument("--execute-approval-record", action="store_true")
    parser.add_argument("--preview-runtime-action", action="store_true")
    parser.add_argument("--execute-runtime-action", action="store_true")
    parser.add_argument("--runtime-governance-store", default="docs/track7/productization/e23-evidence/operator-runtime-governance-actions.jsonl")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--check-autonomous-execution-control", action="store_true")
    parser.add_argument("--execution-control-file", default=str(DEFAULT_AUTONOMOUS_EXECUTION_CONTROL_FILE))
    parser.add_argument("--expected-breaker-generation", default="")
    parser.add_argument("--mutation-kind", choices=("forward", "rollback"), default="forward")
    parser.add_argument("--action-class", default="USER_SWITCH")
    parser.add_argument("--operation-id", default="")
    parser.add_argument("--selected-move-hash", default="")
    parser.add_argument("--source-bundle-hash", default="")
    parser.add_argument("--snapshot-bundle-hash", default="")
    parser.add_argument("--max-users", type=int, default=0)
    parser.add_argument("--rollback-certified", action="store_true")
    parser.add_argument(
        "--issue-current-action-class-contract-from-request", default="",
        help="Existing Authority owner only: issue one exact approved action-class contract from a fresh request JSON.",
    )
    parser.add_argument(
        "--register-current-action-class-contract-request", default="",
        help="Append one validated short-lived request preimage to the existing Authority audit; never writes policy or issues a contract.",
    )
    parser.add_argument(
        "--issue-current-action-class-contract-from-audit-request-id", default="",
        help="Existing Authority owner only: issue from one exact unexpired request preimage already held by its audit owner.",
    )
    parser.add_argument(
        "--decline-current-action-class-contract-from-request", default="",
        help="Existing Authority owner only: append one exact DECLINE decision without writing policy.",
    )
    parser.add_argument("--cancel-current-action-class-contract-id", default="")
    parser.add_argument("--cancel-current-action-class-contract-hash", default="")
    parser.add_argument("--cancel-current-action-class-contract-reason", default="")
    parser.add_argument("--prepare-routing-core-primary-promotion-request", default="")
    parser.add_argument("--issue-routing-core-primary-promotion-from-request", default="")
    parser.add_argument(
        "--prepare-standing-delegated-policy-request", action="store_true",
        help="Build and register one fresh exact standing-policy Authority request without activating it.",
    )
    parser.add_argument(
        "--issue-standing-delegated-policy-from-audit-request-id", default="",
        help="Activate only one exact registered standing-policy request after its independent decision.",
    )
    parser.add_argument(
        "--record-controlled-certification-substrate-decision-from-audit-request-id",
        default="",
        help=(
            "Existing Authority owner only: append one exact APPROVE or DECLINE "
            "decision for the coordinated controlled-certification substrate request. "
            "Never provisions identities or enters execution."
        ),
    )
    parser.add_argument(
        "--replace-expired-controlled-certification-substrate-request-id",
        default="",
        help=(
            "Supersede one exact expired undecided controlled-substrate request "
            "without changing its semantic scope or granting Authority."
        ),
    )
    parser.add_argument(
        "--controlled-certification-substrate-request-hash",
        default="",
    )
    parser.add_argument(
        "--record-ct-m0f-controlled-validation-decision-from-audit-request-id",
        default="",
        help=(
            "Existing Authority owner only: append one exact APPROVE or DECLINE "
            "decision for a single CT-M0F certification validation generation. "
            "Never creates execution artifacts or performs routing effects."
        ),
    )
    parser.add_argument("--ct-m0f-controlled-validation-request-hash", default="")
    parser.add_argument(
        "--prepare-ct-m0f-standing-validation-policy-request",
        action="store_true",
        help=(
            "Build and register one bounded multi-generation CT-M0F standing "
            "validation request without activating policy or producing effects."
        ),
    )
    parser.add_argument(
        "--issue-ct-m0f-standing-validation-policy-from-audit-request-id",
        default="",
        help=(
            "Existing Authority owner only: activate one exact independently "
            "approved CT-M0F standing validation request."
        ),
    )
    parser.add_argument("--ct-m0f-standing-validation-request-hash", default="")
    parser.add_argument(
        "--controlled-certification-substrate-admitted-subscope",
        action="append",
        default=[],
    )
    parser.add_argument(
        "--record-controlled-source-topology-decision-from-audit-request-id",
        default="",
        help=(
            "Existing Authority owner only: append one exact APPROVE or "
            "DECLINE decision for a registered controlled-source topology "
            "request. Never reserves an egress or changes assignments."
        ),
    )
    parser.add_argument(
        "--controlled-source-topology-request-hash",
        default="",
    )
    parser.add_argument(
        "--standing-policy-active-program",
        default="V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1",
    )
    parser.add_argument(
        "--standing-policy-max-users",
        type=int,
        default=1,
        choices=tuple(sorted(SERVICE_FAILURE_DELEGATED_ACTION_CLASSES)),
        help="Exact engineering-qualified tier for a fresh standing-policy Authority request; never activates it.",
    )
    parser.add_argument(
        "--standing-policy-include-controlled-topology",
        action="store_true",
        help=(
            "Add the exact bounded controlled-certification topology action "
            "class to a fresh standing-policy request. This only prepares and "
            "registers an Authority request; it never activates policy or "
            "performs production effects."
        ),
    )
    parser.add_argument(
        "--standing-policy-include-availability-first",
        action="store_true",
        help=(
            "Extend the same combined standing-policy request with the exact "
            "certification-only availability-first shared-target action class "
            "and 1/2/5/10/25/48 maximum ladder. This never activates policy "
            "or performs a production effect."
        ),
    )
    parser.add_argument("--action-class-policy-file", default="/etc/v7/policy.json")
    parser.add_argument("--authority-decision", default="")
    parser.add_argument("--authority-actor-id", default="", help="Required provenance identity for an APPROVE or DECLINE decision.")
    parser.add_argument("--expected-authority-request-id", default="")
    parser.add_argument("--expected-authority-request-hash", default="")
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    try:
        if args.prepare_routing_core_primary_promotion_request:
            request = build_routing_core_primary_promotion_request()
            output = Path(args.prepare_routing_core_primary_promotion_request)
            write_json_atomic(output, request)
            print(json.dumps({"status": "ROUTING_CORE_PRIMARY_PROMOTION_REQUEST_READY", "request": request, "output": str(output), "policy_write": False, "runtime_apply": False}, indent=2 if args.pretty else None, sort_keys=True))
            return 0
        if args.issue_routing_core_primary_promotion_from_request:
            result = issue_routing_core_primary_promotion_to_policy(
                args.action_class_policy_file,
                args.issue_routing_core_primary_promotion_from_request,
                decision=args.authority_decision,
                actor_id=args.authority_actor_id,
                audit_store=args.audit_store,
            )
            print(json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True))
            return 0
        if args.cancel_current_action_class_contract_id:
            result = cancel_unconsumed_current_action_class_contract_to_policy(
                args.action_class_policy_file,
                expected_contract_id=args.cancel_current_action_class_contract_id,
                expected_contract_hash=args.cancel_current_action_class_contract_hash,
                actor_id=args.authority_actor_id,
                reason=args.cancel_current_action_class_contract_reason,
                audit_store=args.audit_store,
            )
            print(json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True))
            return 0
        if args.prepare_ct_m0f_standing_validation_policy_request:
            if (
                args.packet or args.generate_from_plan or args.generate_from_preview
                or args.record_ct_m0f_controlled_validation_decision_from_audit_request_id
                or args.issue_ct_m0f_standing_validation_policy_from_audit_request_id
                or args.prepare_standing_delegated_policy_request
                or args.issue_standing_delegated_policy_from_audit_request_id
            ):
                raise PacketError("ct_m0f_standing_prepare_mode_must_not_mix_other_modes")
            policy_path = Path(args.action_class_policy_file)
            audit_store = (
                str(DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
                if args.audit_store == "docs/track7/productization/e22-evidence/operator-execution-audit.jsonl"
                else args.audit_store
            )
            policy_root = read_json(policy_path)
            existing_contract = (
                policy_root.get(CT_M0F_STANDING_VALIDATION_POLICY_KEY, {})
                if isinstance(policy_root, dict) else {}
            )
            existing_validation = validate_ct_m0f_standing_validation_policy(
                existing_contract,
                audit_records=read_live_execution_lineage_records(
                    Path(audit_store)
                ),
            )
            if existing_validation.get("ok"):
                result = {
                    "status": "VALID_ACTIVE_STANDING_CT_M0F_POLICY_REUSED",
                    "contract_id": existing_contract.get("contract_id"),
                    "contract_hash": existing_contract.get("contract_hash"),
                    "request_created": False,
                    "policy_write": False,
                    "runtime_apply": False,
                    "users_moved": 0,
                }
            else:
                policy_generation_hash = sha256_file(policy_path)
                request = pending_ct_m0f_standing_validation_authority_request(
                    policy_generation_hash=policy_generation_hash,
                    audit_store=audit_store,
                )
                if request:
                    registration = {
                        "status": "ALREADY_REGISTERED_EQUIVALENT",
                        "request_id": request.get("request_id"),
                        "request_hash": request.get("request_hash"),
                        "audit_write": False,
                    }
                else:
                    request = build_ct_m0f_standing_validation_authority_request(
                        policy_generation_hash=policy_generation_hash,
                    )
                    registration = register_ct_m0f_standing_validation_authority_request(
                        request, audit_store=audit_store,
                    )
                result = {
                    "status": "ENGINEERING_AUTHORITY_STANDING_DELEGATED_CT_M0F_VALIDATION_POLICY_REQUIRED",
                    "request": request,
                    "registration": registration,
                    "policy_write": False,
                    "candidate_created": False,
                    "packet_created": False,
                    "lease_created": False,
                    "runtime_apply": False,
                    "routing_mutation": False,
                    "users_moved": 0,
                    "production_maturity_change": False,
                }
            print(json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True))
            return 0
        if args.issue_ct_m0f_standing_validation_policy_from_audit_request_id:
            if (
                args.packet or args.generate_from_plan or args.generate_from_preview
                or args.prepare_ct_m0f_standing_validation_policy_request
                or args.record_ct_m0f_controlled_validation_decision_from_audit_request_id
                or args.prepare_standing_delegated_policy_request
                or args.issue_standing_delegated_policy_from_audit_request_id
            ):
                raise PacketError("ct_m0f_standing_issue_mode_must_not_mix_other_modes")
            result = issue_ct_m0f_standing_validation_policy_from_audit(
                args.action_class_policy_file,
                request_id=args.issue_ct_m0f_standing_validation_policy_from_audit_request_id,
                request_hash=args.ct_m0f_standing_validation_request_hash,
                decision=args.authority_decision,
                actor_id=args.authority_actor_id,
                audit_store=(
                    str(DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
                    if args.audit_store == "docs/track7/productization/e22-evidence/operator-execution-audit.jsonl"
                    else args.audit_store
                ),
            )
            print(json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True))
            return 0
        if args.record_ct_m0f_controlled_validation_decision_from_audit_request_id:
            if (
                args.packet or args.generate_from_plan or args.generate_from_preview
                or args.prepare_standing_delegated_policy_request
                or args.issue_standing_delegated_policy_from_audit_request_id
                or args.record_controlled_certification_substrate_decision_from_audit_request_id
                or args.replace_expired_controlled_certification_substrate_request_id
                or args.record_controlled_source_topology_decision_from_audit_request_id
            ):
                raise PacketError(
                    "ct_m0f_validation_decision_mode_must_not_mix_other_modes"
                )
            result = record_ct_m0f_controlled_validation_authority_decision(
                request_id=(
                    args.record_ct_m0f_controlled_validation_decision_from_audit_request_id
                ),
                request_hash=args.ct_m0f_controlled_validation_request_hash,
                decision=args.authority_decision,
                actor_id=args.authority_actor_id,
                audit_store=(
                    str(DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
                    if args.audit_store
                    == "docs/track7/productization/e22-evidence/operator-execution-audit.jsonl"
                    else args.audit_store
                ),
            )
            print(json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True))
            return 0
        if (
            args
            .record_controlled_source_topology_decision_from_audit_request_id
        ):
            if (
                args.packet or args.generate_from_plan
                or args.generate_from_preview
                or args.prepare_standing_delegated_policy_request
                or args.issue_standing_delegated_policy_from_audit_request_id
                or args.record_controlled_certification_substrate_decision_from_audit_request_id
                or args.replace_expired_controlled_certification_substrate_request_id
            ):
                raise PacketError(
                    "controlled_source_topology_decision_mode_must_not_mix_other_modes"
                )
            result = record_controlled_source_topology_authority_decision(
                request_id=(
                    args
                    .record_controlled_source_topology_decision_from_audit_request_id
                ),
                request_hash=args.controlled_source_topology_request_hash,
                decision=args.authority_decision,
                actor_id=args.authority_actor_id,
                audit_store=(
                    str(DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
                    if args.audit_store
                    == "docs/track7/productization/e22-evidence/operator-execution-audit.jsonl"
                    else args.audit_store
                ),
            )
            print(json.dumps(
                redact(result),
                indent=2 if args.pretty else None,
                sort_keys=True,
            ))
            return 0
        if args.record_controlled_certification_substrate_decision_from_audit_request_id:
            if (
                args.packet or args.generate_from_plan or args.generate_from_preview
                or args.prepare_standing_delegated_policy_request
                or args.issue_standing_delegated_policy_from_audit_request_id
                or args.replace_expired_controlled_certification_substrate_request_id
            ):
                raise PacketError(
                    "controlled_certification_substrate_decision_mode_must_not_mix_other_modes"
                )
            result = record_controlled_certification_substrate_authority_decision(
                request_id=(
                    args.record_controlled_certification_substrate_decision_from_audit_request_id
                ),
                request_hash=args.controlled_certification_substrate_request_hash,
                decision=args.authority_decision,
                actor_id=args.authority_actor_id,
                admitted_subscopes=(
                    args.controlled_certification_substrate_admitted_subscope
                ),
                audit_store=(
                    str(DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
                    if args.audit_store
                    == "docs/track7/productization/e22-evidence/operator-execution-audit.jsonl"
                    else args.audit_store
                ),
            )
            print(json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True))
            return 0
        if args.replace_expired_controlled_certification_substrate_request_id:
            if (
                args.packet or args.generate_from_plan or args.generate_from_preview
                or args.prepare_standing_delegated_policy_request
                or args.issue_standing_delegated_policy_from_audit_request_id
                or args.record_controlled_certification_substrate_decision_from_audit_request_id
            ):
                raise PacketError(
                    "controlled_certification_substrate_replacement_mode_must_not_mix_other_modes"
                )
            result = replace_expired_controlled_certification_substrate_request(
                request_id=(
                    args.replace_expired_controlled_certification_substrate_request_id
                ),
                request_hash=args.controlled_certification_substrate_request_hash,
                audit_store=(
                    str(DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
                    if args.audit_store
                    == "docs/track7/productization/e22-evidence/operator-execution-audit.jsonl"
                    else args.audit_store
                ),
            )
            print(json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True))
            return 0
        if args.prepare_standing_delegated_policy_request:
            if (
                args.packet or args.generate_from_plan or args.generate_from_preview
                or args.issue_current_action_class_contract_from_request
                or args.issue_current_action_class_contract_from_audit_request_id
                or args.decline_current_action_class_contract_from_request
                or args.issue_standing_delegated_policy_from_audit_request_id
            ):
                raise PacketError("standing_delegated_policy_prepare_mode_must_not_mix_execution_or_decision_modes")
            request = build_standing_delegated_policy_authority_request(
                policy_generation_hash=sha256_file(Path(args.action_class_policy_file)),
                active_program=args.standing_policy_active_program,
                max_users=args.standing_policy_max_users,
                include_controlled_topology=(
                    args.standing_policy_include_controlled_topology
                ),
                include_availability_first=(
                    args.standing_policy_include_availability_first
                ),
            )
            registration = register_standing_delegated_policy_request(
                request,
                audit_store=(str(DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
                if args.audit_store == "docs/track7/productization/e22-evidence/operator-execution-audit.jsonl" else args.audit_store),
            )
            result = {
                "status": "STANDING_DELEGATED_POLICY_AUTHORITY_REQUEST_READY",
                "request": request,
                "registration": registration,
                "authority_granted": False,
                "policy_write": False,
                "runtime_apply": False,
                "routing_mutation": False,
                "users_moved": 0,
            }
            print(json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True))
            return 0
        if args.issue_standing_delegated_policy_from_audit_request_id:
            if (
                args.packet or args.generate_from_plan or args.generate_from_preview
                or args.issue_current_action_class_contract_from_request
                or args.issue_current_action_class_contract_from_audit_request_id
                or args.decline_current_action_class_contract_from_request
            ):
                raise PacketError("standing_delegated_policy_issue_mode_must_not_mix_packet_modes")
            result = issue_standing_delegated_policy_from_audit(
                args.action_class_policy_file,
                request_id=args.issue_standing_delegated_policy_from_audit_request_id,
                request_hash=args.expected_authority_request_hash,
                decision=args.authority_decision,
                audit_store=(str(DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
                if args.audit_store == "docs/track7/productization/e22-evidence/operator-execution-audit.jsonl" else args.audit_store),
                actor_id=args.authority_actor_id,
            )
            print(json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True))
            return 0
        if args.register_current_action_class_contract_request:
            if args.packet or args.generate_from_plan or args.generate_from_preview or args.issue_current_action_class_contract_from_request or args.issue_current_action_class_contract_from_audit_request_id or args.decline_current_action_class_contract_from_request:
                raise PacketError("current_action_class_contract_request_register_mode_must_not_mix_execution_or_decision_modes")
            request = read_json(Path(args.register_current_action_class_contract_request))
            result = register_current_action_class_contract_request(
                request, audit_store=(str(DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
                if args.audit_store == "docs/track7/productization/e22-evidence/operator-execution-audit.jsonl" else args.audit_store),
            )
            print(json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True))
            return 0
        if args.issue_current_action_class_contract_from_audit_request_id:
            if args.packet or args.generate_from_plan or args.generate_from_preview or args.issue_current_action_class_contract_from_request or args.decline_current_action_class_contract_from_request:
                raise PacketError("current_action_class_contract_issue_audit_mode_must_not_mix_packet_modes")
            result = issue_current_action_class_contract_from_audit(
                args.action_class_policy_file,
                request_id=args.issue_current_action_class_contract_from_audit_request_id,
                request_hash=args.expected_authority_request_hash,
                decision=args.authority_decision,
                audit_store=(str(DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
                if args.audit_store == "docs/track7/productization/e22-evidence/operator-execution-audit.jsonl" else args.audit_store),
                actor_id=args.authority_actor_id,
            )
            print(json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True))
            return 0
        if args.issue_current_action_class_contract_from_request:
            if args.packet or args.generate_from_plan or args.generate_from_preview or args.decline_current_action_class_contract_from_request:
                raise PacketError("current_action_class_contract_issue_mode_must_not_mix_packet_modes")
            result = issue_current_action_class_contract_to_policy(
                args.action_class_policy_file,
                args.issue_current_action_class_contract_from_request,
                decision=args.authority_decision,
                expected_request_id=args.expected_authority_request_id,
                expected_request_hash=args.expected_authority_request_hash,
                audit_store=(
                    str(DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
                    if args.audit_store == "docs/track7/productization/e22-evidence/operator-execution-audit.jsonl"
                    else args.audit_store
                ),
                actor_id=args.authority_actor_id,
            )
            text = json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True)
            print(text)
            return 0
        if args.decline_current_action_class_contract_from_request:
            if args.packet or args.generate_from_plan or args.generate_from_preview:
                raise PacketError("current_action_class_contract_decline_mode_must_not_mix_packet_modes")
            result = decline_current_action_class_contract_request(
                args.action_class_policy_file,
                args.decline_current_action_class_contract_from_request,
                decision=args.authority_decision,
                expected_request_id=args.expected_authority_request_id,
                expected_request_hash=args.expected_authority_request_hash,
                audit_store=(
                    str(DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE)
                    if args.audit_store == "docs/track7/productization/e22-evidence/operator-execution-audit.jsonl"
                    else args.audit_store
                ),
                actor_id=args.authority_actor_id,
            )
            print(json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True))
            return 0
        if args.check_autonomous_execution_control:
            result = autonomous_execution_control_decision(
                Path(args.execution_control_file),
                mutation_kind=args.mutation_kind,
                action_class=args.action_class,
                expected_generation=args.expected_breaker_generation,
                rollback_certified=args.rollback_certified,
                operation_id=args.operation_id,
                selected_move_hash=args.selected_move_hash,
                source_bundle_hash=args.source_bundle_hash,
                snapshot_bundle_hash=args.snapshot_bundle_hash,
                max_users=args.max_users,
            )
            print(json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True))
            return 0 if result.get("allowed") else 2
        if args.cancel_execution_lease:
            if not args.execution_lease_file:
                raise PacketError("execution_lease_file_required")
            lease_path = resolve_under_repo(args.execution_lease_file, repo_root)
            result = cancel_execution_lease(lease_path, reason=args.cancel_reason)
            text = json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True)
            print(text)
            return 0 if result.get("ok") else 2
        if args.finish_execution_lease:
            if not args.execution_lease_file:
                raise PacketError("execution_lease_file_required")
            lease_path = resolve_under_repo(args.execution_lease_file, repo_root)
            operation = load_optional_json(args.operation_result) or {}
            result = finish_execution_lease(
                lease_path,
                status=args.finish_status,
                reason=args.finish_reason,
                operation=operation,
            )
            text = json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True)
            print(text)
            return 0 if result.get("ok") else 2
        if args.generate_from_plan:
            plan = read_json(args.generate_from_plan)
            packet = packet_from_plan(
                plan,
                approval_author=args.approval_author,
                approval_reviewer=args.approval_reviewer,
                ttl_seconds=args.ttl_seconds,
            )
            if args.packet_output:
                packet_path = resolve_under_repo(args.packet_output, repo_root)
                write_json_atomic(packet_path, packet)
            else:
                packet_path = Path(args.generate_from_plan)
            result = {
                "mode": "generate",
                "packet": redact(packet),
                "packet_path": str(packet_path),
                "execution_allowed_now": False,
                "real_runtime_action_performed": False,
            }
            text = json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True)
            print(text)
            return 0
        if args.generate_from_preview:
            preview = extract_packet_preview(read_json(args.generate_from_preview))
            packet = packet_from_preview(
                preview,
                approval_author=args.approval_author,
                approval_reviewer=args.approval_reviewer,
                ttl_seconds=args.ttl_seconds,
            )
            if args.packet_output:
                packet_path = resolve_under_repo(args.packet_output, repo_root)
                write_json_atomic(packet_path, packet)
            else:
                packet_path = Path(args.generate_from_preview)
            lease_result = {}
            if args.create_execution_lease:
                if not args.execution_lease_file:
                    raise PacketError("execution_lease_file_required")
                lease = build_execution_lease(packet, source_preview=preview)
                lease_path = resolve_under_repo(args.execution_lease_file, repo_root)
                lease_result = write_execution_lease(lease_path, lease)
                if not lease_result.get("ok"):
                    result = {
                        "mode": "generate_from_preview",
                        "packet": redact(packet),
                        "packet_path": str(packet_path),
                        "execution_lease": lease_result,
                        "execution_allowed_now": False,
                        "real_runtime_action_performed": False,
                    }
                    text = json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True)
                    print(text)
                    return 2
            result = {
                "mode": "generate_from_preview",
                "packet": redact(packet),
                "packet_path": str(packet_path),
                "execution_lease": lease_result,
                "identity_preserved": {
                    "packet_id": packet.get("packet_id") == preview.get("packet_id"),
                    "operation_id": packet.get("operation_id") == preview.get("operation_id"),
                    "decision_id": packet.get("decision_id") == preview.get("decision_id"),
                    "authority_generation": packet.get("authority_generation") == (
                        preview.get("authority_generation") or preview.get("current_state_generation") or preview.get("cycle_id")
                    ),
                    "selected_move_hash": (packet.get("expected") or {}).get("selected_move_hash") == preview.get("selected_move_hash"),
                },
                "execution_allowed_now": False,
                "real_runtime_action_performed": False,
            }
            text = json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True)
            print(text)
            return 0
        if not args.packet:
            raise PacketError("packet_required")
        packet, packet_path = load_packet(args.packet, repo_root)
        audit_store = resolve_under_repo(args.audit_store, repo_root)
        planner_snapshot = load_optional_json(args.planner_snapshot)
        lifecycle_store = resolve_under_repo(args.lifecycle_store, repo_root)
        if args.validate_only:
            result = execute_packet(packet, audit_store, args.state_dir, mode="validate")
        elif args.recheck_only:
            result = execute_packet(packet, audit_store, args.state_dir, mode="recheck", planner_snapshot=planner_snapshot)
        elif args.execute_approval_record:
            result = execute_packet(packet, audit_store, args.state_dir, mode="execute", planner_snapshot=planner_snapshot)
        elif args.preview_runtime_action:
            result = execute_packet(
                packet,
                audit_store,
                args.state_dir,
                mode="runtime_action_preview",
                planner_snapshot=planner_snapshot,
                restore_barrier_file=args.restore_barrier_file,
            )
        elif args.execute_runtime_action:
            runtime_governance_store = resolve_under_repo(args.runtime_governance_store, repo_root)
            result = execute_packet(
                packet,
                audit_store,
                args.state_dir,
                mode="runtime_action",
                runtime_governance_store=runtime_governance_store,
                planner_snapshot=planner_snapshot,
                restore_barrier_file=args.restore_barrier_file,
                lifecycle_store=lifecycle_store,
            )
            result["runtime_governance_store"] = str(runtime_governance_store)
            result["lifecycle_store"] = str(lifecycle_store)
        else:
            raise PacketError("mode_required")
        result["packet_path"] = str(packet_path)
        result["audit_store"] = str(audit_store)
        result["execution_allowed_now"] = bool(result.get("execution_allowed_now"))
        result["real_runtime_action_performed"] = bool(result.get("record", {}).get("runtime_action_performed"))
    except PacketError as exc:
        result = {"error": str(exc), "execution_allowed_now": False, "real_runtime_action_performed": False}
    text = json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True)
    print(text)
    return 0 if not result.get("error") else 2


if __name__ == "__main__":
    raise SystemExit(main())
