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


def recheck_nonzero_packet(packet, state_dir, planner_snapshot):
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
    lifecycle_records = None
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
    parser.add_argument("--packet-output", default="")
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
    parser.add_argument("--execute-runtime-action", action="store_true")
    parser.add_argument("--runtime-governance-store", default="docs/track7/productization/e23-evidence/operator-runtime-governance-actions.jsonl")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    try:
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
