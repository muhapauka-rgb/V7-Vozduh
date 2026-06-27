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
import hashlib
import json
import os
import secrets
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
LEASE_TERMINAL_STATUSES = {"EXECUTION_FINISHED", "ROLLBACK_FINISHED", "OPERATOR_CANCELLED"}
MATERIAL_STATE_FIELDS = [
    "selected_move_hash",
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
]


class PacketError(ValueError):
    pass


def utc_now():
    return datetime.now(timezone.utc)


def parse_ts(value):
    if not value:
        raise PacketError("missing_timestamp")
    text = str(value).replace("Z", "+00:00")
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


def validate_approvals(packet, errors):
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
    validate_approvals(packet, errors)
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
    validate_approvals(packet, errors)
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
    if not expected.get("source_bundle_hash"):
        errors.append("source_bundle_hash_missing")
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
    decisions = plan.get("decisions") or []
    constraints = None

    if selected_moves:
        source_rows = selected_moves
        source_kind = "selected_moves"
    elif approved_candidates:
        source_rows = approved_candidates
        source_kind = "approved_candidate_moves_before_guard"
    else:
        source_rows = decisions
        source_kind = "decisions"
    for row in source_rows:
        if source_kind != "decisions" or (
            row.get("action") == "switch"
            and row.get("recommended_egress") != row.get("current_egress")
        ):
            moves.append({
                "user_ip": str(row.get("user_ip") or ""),
                "current_egress": str(row.get("current_egress") or ""),
                "recommended_egress": str(row.get("recommended_egress") or ""),
                "move_type": str(row.get("move_type") or ""),
            })
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
                "user_ip": move["user_ip"],
                "current_egress": move["current_egress"],
                "recommended_egress": move["recommended_egress"],
                "move_type": move.get("move_type", ""),
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
    return {
        "packet_id": str(packet.get("packet_id") or ""),
        "operation_id": str(packet.get("operation_id") or ""),
        "decision_id": str(packet.get("decision_id") or ""),
        "authority_generation": str(packet.get("authority_generation") or expected.get("generation_id") or ""),
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
    return {
        "packet_id": str(preview.get("packet_id") or ""),
        "operation_id": str(preview.get("operation_id") or ""),
        "decision_id": str(preview.get("decision_id") or ""),
        "authority_generation": str(selected.get("authority_generation") or ""),
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
    }


def material_state_from_packet_preview(preview):
    preview = extract_packet_preview(preview)
    rollback_preview = preview.get("rollback_manifest_preview") if isinstance(preview.get("rollback_manifest_preview"), dict) else {}
    targets = _string_list(preview.get("allowed_targets"))
    users = _string_list(preview.get("allowed_users"))
    rollback_targets = _rollback_targets_from_manifest(rollback_preview)
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
    )


def material_state_from_packet(packet):
    packet = packet if isinstance(packet, dict) else {}
    expected = packet.get("expected") if isinstance(packet.get("expected"), dict) else {}
    constraints = packet.get("constraints") if isinstance(packet.get("constraints"), dict) else {}
    rollback_manifest = packet.get("rollback_manifest") if isinstance(packet.get("rollback_manifest"), dict) else {}
    targets = _string_list(constraints.get("allowed_targets"))
    users = _string_list(constraints.get("allowed_users"))
    rollback_targets = _rollback_targets_from_manifest(rollback_manifest)
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
    base = {
        "approval_id": packet.get("approval_id", ""),
        "packet_id": packet.get("packet_id", ""),
        "operation_id": packet.get("operation_id", ""),
        "selected_move_hash": (packet.get("expected") or {}).get("selected_move_hash", ""),
        "selected_move_count": (packet.get("expected") or {}).get("selected_move_count", 0),
        "atomic_execution_envelope_id": (packet.get("expected") or {}).get("atomic_execution_envelope_id", ""),
        "atomic_execution_envelope_hash": (packet.get("expected") or {}).get("atomic_execution_envelope_hash", ""),
        "created_at": now.isoformat(),
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
):
    now = now or utc_now()
    approval_id = packet.get("approval_id") or stable_id("appr", packet)
    records = read_audit_records(audit_store)
    if replay_seen(records, approval_id):
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
    if preview_source_hashes:
        source_hashes = {str(key): str(value) for key, value in preview_source_hashes.items() if str(value)}
    else:
        source_hashes = {
            "preview_packet": sha256_json({
                "packet_id": packet_id,
                "operation_id": operation_id,
                "decision_id": decision_id,
                "authority_generation": authority_generation,
                "selected_move_hash": selected_hash,
            }),
            "source_hash": str(preview.get("source_hash") or ""),
            "recommendation_hash": str(preview.get("recommendation_hash") or ""),
        }
        source_hashes = {key: value for key, value in source_hashes.items() if value}
    source_bundle_hash = sha256_json(source_hashes)
    snapshot_bundle_hash = str(preview.get("snapshot_bundle_hash") or "") or sha256_json({
        "preview_packet_id": packet_id,
        "preview_operation_id": operation_id,
        "selected_move_hash": selected_hash,
        "selected_move_count": selected_count,
    })
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


def packet_from_preview(preview, *, approval_author, approval_reviewer, ttl_seconds=DEFAULT_CLEARANCE_TTL_SECONDS):
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
        },
        "governance_owner": CANONICAL_CLEARANCE_OWNER,
    }
    packet_hash = sha256_bytes(canonical_json(packet).encode("utf-8"))
    packet["approved_plan_lock"] = approved_plan_lock_from_selected(selected, packet, packet_hash)
    validation = validate_packet(packet, now=now)
    if not validation.get("ok"):
        raise PacketError(",".join(validation.get("errors") or ["packet_invalid"]))
    return packet


def packet_from_plan(plan, *, approval_author, approval_reviewer, ttl_seconds=DEFAULT_CLEARANCE_TTL_SECONDS):
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
    }
    operation_id = stable_id("govexec", operation_payload)
    packet = {
        "schema_version": GOVERNANCE_PACKET_SCHEMA,
        "packet_id": stable_id("pkt", {**operation_payload, "created_at": now.isoformat()}),
        "approval_id": stable_id("appr", {**operation_payload, "expires_at": expires_at.isoformat()}),
        "operation_id": operation_id,
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
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    try:
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
