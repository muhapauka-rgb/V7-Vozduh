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
import hashlib
import json
import os
import secrets
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
CURRENT_ACTION_CLASS_CONTRACT_REQUEST_TTL_SECONDS = 300
CURRENT_ACTION_CLASS_AUDIT_SCHEMA = "v7.current-action-class-contract-authority-audit.v1"
DEFAULT_PRODUCTION_OPERATOR_EXECUTION_AUDIT_STORE = Path("/opt/v7/audit/operator-execution-audit.jsonl")
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
        "max_ttl_seconds": min(CURRENT_ACTION_CLASS_CONTRACT_MAX_TTL_SECONDS, max(1, as_int(template.get("max_ttl_seconds"), 300))),
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
        if authority.get("action_class") != "single-user governed candidate failover":
            errors.append("delegated_policy_action_class_invalid")
        if as_int(authority.get("max_users_per_transaction"), 0) != 1:
            errors.append("delegated_policy_blast_radius_invalid")
        if as_int(authority.get("max_concurrent_transactions"), 0) != 1:
            errors.append("delegated_policy_concurrency_invalid")
        if authority.get("candidate_identity") != "FRESH_ONLY":
            errors.append("delegated_policy_candidate_freshness_invalid")
        if authority.get("packet_reuse") != "FORBIDDEN":
            errors.append("delegated_policy_packet_reuse_invalid")
        if authority.get("self_expansion_allowed") is not False:
            errors.append("delegated_policy_self_expansion_invalid")
        if normalized_scope:
            if normalized_scope.get("allowed_action_classes") != ["single-user governed candidate failover"]:
                errors.append("delegated_policy_normalized_action_classes_invalid")
            if as_int(normalized_scope.get("max_users_per_action"), 0) != 1:
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


def replay_seen(records, approval_id):
    for record in records:
        if record.get("approval_id") == approval_id:
            return True
    return False


def engineering_authority_replay_seen(records, request_id):
    if not request_id:
        return False
    return any(str(record.get("engineering_authority_request_id") or "") == str(request_id) for record in records)


def append_record(audit_store, record):
    path = Path(audit_store)
    path.parent.mkdir(parents=True, exist_ok=True)
    previous_records = read_audit_records(path)
    previous_hash = previous_records[-1].get("record_hash", "GENESIS") if previous_records else "GENESIS"
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
    now = now or utc_now()
    approval_id = packet.get("approval_id") or stable_id("appr", packet)
    records = read_audit_records(audit_store)
    engineering_authority = packet.get("engineering_authority") if isinstance(packet.get("engineering_authority"), dict) else {}
    engineering_request_id = str(engineering_authority.get("request_id") or "")
    if engineering_authority_replay_seen(records, engineering_request_id):
        recheck = {"allow": False, "verdict": "DENY_REPLAY", "errors": ["engineering_authority_request_already_consumed"]}
    elif replay_seen(records, approval_id):
        recheck = {"allow": False, "verdict": "DENY_REPLAY", "errors": ["approval_id_already_recorded"]}
    else:
        recheck = runtime_recheck(packet, state_dir, now=now, planner_snapshot=planner_snapshot)
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
    written = append_record(audit_store, redact(record))
    if clearance_result and clearance_result.get("ok") and lifecycle_store:
        lifecycle_records = append_lifecycle_records(lifecycle_store, packet, recheck, clearance_result, written, now=now)
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
            moves.append({
                "user_ip": user_ip,
                "current_egress": current,
                "recommended_egress": target,
                "move_type": str(item.get("move_type") or "governed_canary"),
            })
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


def packet_from_plan(plan, *, approval_author, approval_reviewer, ttl_seconds=DEFAULT_CLEARANCE_TTL_SECONDS, breaker_generation=""):
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
        "approvals": [
            {"operator_id": approval_author, "role": "approval_author", "confirmed_at": now.isoformat()},
            {"operator_id": approval_reviewer, "role": "approval_reviewer", "confirmed_at": now.isoformat()},
        ],
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
    packet_hash = sha256_bytes(canonical_json(packet).encode("utf-8"))
    packet["approved_plan_lock"] = approved_plan_lock_from_selected(selected, packet, packet_hash)
    validation = validate_packet(packet, now=now)
    if not validation.get("ok"):
        raise PacketError(",".join(validation.get("errors") or ["packet_invalid"]))
    return packet


def load_packet(path, repo_root):
    packet_path = resolve_under_repo(path, repo_root)
    return read_json(packet_path), packet_path


def issue_current_action_class_contract_to_policy(
    policy_path, request_path, *, decision, expected_request_id="", expected_request_hash="", now=None,
    audit_store=None, actor_id="",
):
    """Persist a contract only through this existing Authority owner surface."""
    policy_path = Path(policy_path)
    request_path = Path(request_path)
    request = read_json(request_path)
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
        "--decline-current-action-class-contract-from-request", default="",
        help="Existing Authority owner only: append one exact DECLINE decision without writing policy.",
    )
    parser.add_argument("--action-class-policy-file", default="/etc/v7/policy.json")
    parser.add_argument("--authority-decision", default="")
    parser.add_argument("--authority-actor-id", default="", help="Required provenance identity for an APPROVE or DECLINE decision.")
    parser.add_argument("--expected-authority-request-id", default="")
    parser.add_argument("--expected-authority-request-hash", default="")
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    try:
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
