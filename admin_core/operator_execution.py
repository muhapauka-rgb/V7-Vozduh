"""Operator execution packet validation and audit persistence.

This module is intentionally narrow: it can validate a zero-movement operator
packet, run read-only file rechecks, and append approval/denial audit records.
It never performs user movement, routing changes, service control, or runtime
apply actions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from admin_core.sanitize import redact


ZERO_ACTION = "ZERO_MOVEMENT_GENERATION_CLEARANCE_RECHECK"
RUNTIME_ACTION_RECORD_ONLY = "RECHECK_AND_RECORD_ONLY"
RUNTIME_ACTION_ZERO_MOVE_GOVERNANCE = "ZERO_MOVE_GOVERNANCE_STATE_TRANSITION"
RUNTIME_ACTION = RUNTIME_ACTION_RECORD_ONLY
ALLOWED_RUNTIME_ACTIONS = {RUNTIME_ACTION_RECORD_ONLY, RUNTIME_ACTION_ZERO_MOVE_GOVERNANCE}
EMPTY_SELECTED_MOVES_HASH = hashlib.sha256(b"[]").hexdigest()


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


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


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


def validate_packet(packet, now=None):
    now = now or utc_now()
    errors = []
    if packet.get("schema_version") != "e22.operator-execution-packet.v1":
        errors.append("schema_version_invalid")
    if packet.get("selected_first_action") != ZERO_ACTION:
        errors.append("unsupported_action")
    if packet.get("runtime_action") not in ALLOWED_RUNTIME_ACTIONS:
        errors.append("runtime_action_not_allowed")
    constraints = packet.get("constraints") or {}
    if int(constraints.get("selected_move_budget", -1)) != 0:
        errors.append("selected_move_budget_not_zero")
    if constraints.get("allowed_users") not in ([], None):
        errors.append("allowed_users_not_empty")
    if constraints.get("allowed_targets") not in ([], None):
        errors.append("allowed_targets_not_empty")
    if constraints.get("user_movement_allowed") is not False:
        errors.append("user_movement_not_forbidden")
    if constraints.get("routing_mutation_allowed") is not False:
        errors.append("routing_mutation_not_forbidden")
    approvals = packet.get("approvals") or []
    if len(approvals) != 2:
        errors.append("dual_confirmation_missing")
    else:
        first = approvals[0].get("operator_id")
        second = approvals[1].get("operator_id")
        if not first or not second:
            errors.append("operator_id_missing")
        if first == second:
            errors.append("dual_confirmation_same_actor")
        roles = {row.get("role") for row in approvals}
        if not {"approval_author", "approval_reviewer"}.issubset(roles):
            errors.append("approval_roles_invalid")
    try:
        expires_at = parse_ts(packet.get("expires_at"))
        if now >= expires_at:
            errors.append("approval_expired")
    except PacketError:
        errors.append("expires_at_invalid")
    expected = packet.get("expected") or {}
    if expected.get("selected_move_hash") != EMPTY_SELECTED_MOVES_HASH:
        errors.append("selected_move_hash_invalid_for_zero_budget")
    if not expected.get("generation_id"):
        errors.append("generation_id_missing")
    if errors:
        return {"ok": False, "verdict": "DENY_PACKET_INVALID", "errors": errors}
    return {"ok": True, "verdict": "PACKET_VALID", "errors": []}


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


def runtime_recheck(packet, state_dir, now=None):
    now = now or utc_now()
    validation = validate_packet(packet, now=now)
    if not validation["ok"]:
        return {"allow": False, "verdict": validation["verdict"], "errors": validation["errors"]}
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


def execute_packet(packet, audit_store, state_dir, now=None, mode="execute", runtime_governance_store=None):
    now = now or utc_now()
    approval_id = packet.get("approval_id") or stable_id("appr", packet)
    records = read_audit_records(audit_store)
    if replay_seen(records, approval_id):
        recheck = {"allow": False, "verdict": "DENY_REPLAY", "errors": ["approval_id_already_recorded"]}
    else:
        recheck = runtime_recheck(packet, state_dir, now=now)
    if mode == "validate":
        return {"mode": mode, "approval_id": approval_id, "recheck": validate_packet(packet, now=now), "record_written": False}
    if mode == "recheck":
        return {"mode": mode, "approval_id": approval_id, "recheck": recheck, "record_written": False}
    runtime_action_record = None
    runtime_action_performed = False
    runtime_mutation = False
    if mode == "runtime_action":
        if packet.get("runtime_action") != RUNTIME_ACTION_ZERO_MOVE_GOVERNANCE:
            recheck = {
                "allow": False,
                "verdict": "DENY_RUNTIME_ACTION_UNSUPPORTED",
                "errors": ["runtime_action_not_zero_move_governance_transition"],
            }
        elif recheck.get("allow"):
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
        "runtime_mutation_scope": "append_only_runtime_governance_state" if runtime_mutation else "none",
        "user_movement": False,
        "routing_mutation": False,
        "kill_switch_mutation": False,
        "autoswitch_apply": False,
        "canary": False,
        "runtime_action_performed": runtime_action_performed,
        "runtime_action_record_hash": runtime_action_record.get("record_hash") if runtime_action_record else "",
    }
    written = append_record(audit_store, redact(record))
    return {
        "mode": mode,
        "approval_id": approval_id,
        "recheck": recheck,
        "record_written": True,
        "record": written,
        "runtime_action_record": runtime_action_record,
    }


def load_packet(path, repo_root):
    packet_path = resolve_under_repo(path, repo_root)
    return read_json(packet_path), packet_path


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate and consume V7 operator execution packets without runtime actions.")
    parser.add_argument("--packet", required=True)
    parser.add_argument("--audit-store", default="docs/track7/productization/e22-evidence/operator-execution-audit.jsonl")
    parser.add_argument("--state-dir", default="/opt/v7/egress/state")
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
        packet, packet_path = load_packet(args.packet, repo_root)
        audit_store = resolve_under_repo(args.audit_store, repo_root)
        if args.validate_only:
            result = execute_packet(packet, audit_store, args.state_dir, mode="validate")
        elif args.recheck_only:
            result = execute_packet(packet, audit_store, args.state_dir, mode="recheck")
        elif args.execute_approval_record:
            result = execute_packet(packet, audit_store, args.state_dir, mode="execute")
        elif args.execute_runtime_action:
            runtime_governance_store = resolve_under_repo(args.runtime_governance_store, repo_root)
            result = execute_packet(
                packet,
                audit_store,
                args.state_dir,
                mode="runtime_action",
                runtime_governance_store=runtime_governance_store,
            )
            result["runtime_governance_store"] = str(runtime_governance_store)
        else:
            raise PacketError("mode_required")
        result["packet_path"] = str(packet_path)
        result["audit_store"] = str(audit_store)
        result["execution_allowed_now"] = False
        result["real_runtime_action_performed"] = bool(result.get("record", {}).get("runtime_action_performed"))
    except PacketError as exc:
        result = {"error": str(exc), "execution_allowed_now": False, "real_runtime_action_performed": False}
    text = json.dumps(redact(result), indent=2 if args.pretty else None, sort_keys=True)
    print(text)
    return 0 if not result.get("error") else 2


if __name__ == "__main__":
    raise SystemExit(main())
