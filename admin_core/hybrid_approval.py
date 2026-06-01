"""Hybrid approval contract for bounded V7 autonomy.

This module is intentionally side-effect light. It can classify runtime state,
build stable fingerprints, validate one-user hybrid approval packets, and append
governance audit records. It does not call v7-user-switch, v7-users-autoswitch,
ip, nft, systemctl, or any deployment helper.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from admin_core.registry_readers import parse_registry_lines
from admin_core.sanitize import redact


SCHEMA_VERSION = "z2.hybrid-approval.v1"
AUDIT_SCHEMA_VERSION = "z2.hybrid-autonomy-audit.v1"
ALLOWED_POLICY_BUDGET = 1
REQUIRED_EXCLUSIONS = {"DIRECT_RU", "TRUSTED_RU_SENSITIVE"}


class HybridApprovalError(ValueError):
    pass


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_ts(value: str) -> datetime:
    if not value:
        raise HybridApprovalError("missing_timestamp")
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise HybridApprovalError("invalid_timestamp") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def canonical_json(value: Any) -> str:
    return json.dumps(redact(value), sort_keys=True, ensure_ascii=True, separators=(",", ":"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_bytes(canonical_json(value).encode("utf-8"))


def sha256_file(path: Path) -> str:
    try:
        return sha256_bytes(path.read_bytes())
    except OSError:
        return ""


def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def read_registry(path: Path) -> list[dict[str, str]]:
    try:
        return parse_registry_lines(path.read_text(encoding="utf-8").splitlines())
    except OSError:
        return []


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def falsy(value: Any) -> bool:
    return str(value).strip().lower() in {"0", "false", "no", "off"}


def egress_id(row: dict[str, Any]) -> str:
    return str(row.get("id") or row.get("egress_id") or "")


def registry_by_id(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {egress_id(row): row for row in rows if egress_id(row)}


def user_counts(users: list[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in users:
        if not truthy(row.get("enabled", "1")):
            continue
        current = str(row.get("current") or "")
        if current:
            counts[current] = counts.get(current, 0) + 1
    return counts


def route_class(row: dict[str, Any]) -> str:
    return str(row.get("role") or row.get("route_class") or "UNKNOWN")


def trust_class(row: dict[str, Any]) -> str:
    exclusions = {item.strip() for item in str(row.get("exclude_route_classes") or "").split(",") if item.strip()}
    return "RU_SENSITIVE_EXCLUDED" if REQUIRED_EXCLUSIONS.issubset(exclusions) else "RU_SENSITIVE_UNKNOWN"


def policy_class(row: dict[str, Any]) -> str:
    role = route_class(row)
    if role == "EXECUTION_ONLY":
        return "EXECUTION_ONLY"
    if truthy(row.get("manual_only")) or truthy(row.get("reserve_only")):
        return "MANUAL_OR_RESERVED"
    if row.get("autoswitch_allowed") is not None and falsy(row.get("autoswitch_allowed")):
        return "AUTOSWITCH_FORBIDDEN"
    return "AUTOSWITCH_ALLOWED"


def capacity_class(row: dict[str, Any], counts: dict[str, int]) -> str:
    current = counts.get(egress_id(row), int(row.get("users_count_from_registry") or 0))
    hard = int(row.get("hard_limit") or 0)
    soft = int(row.get("soft_limit") or 0)
    if hard and current >= hard:
        return "HARD_FULL"
    if soft and current >= soft:
        return "SOFT_FULL"
    if current == 0:
        return "EMPTY"
    return "HAS_ROOM"


def target_descriptor(row: dict[str, Any], counts: dict[str, int] | None = None) -> dict[str, Any]:
    counts = counts or {}
    return {
        "egress_id": egress_id(row),
        "route_class": route_class(row),
        "trust_class": trust_class(row),
        "policy_class": policy_class(row),
        "capacity_class": capacity_class(row, counts),
        "protocol": row.get("protocol", ""),
        "enabled": truthy(row.get("enabled", "1")),
    }


def selected_moves_state(state_dir: Path) -> dict[str, Any]:
    for name in ("selected-moves.json", "selected_moves.json", "current-selected-moves.json"):
        path = state_dir / name
        if not path.exists():
            continue
        data = read_json(path, [])
        moves = data.get("selected_moves", data if isinstance(data, list) else [])
        return {"count": len(moves), "hash": sha256_json(moves), "source": str(path)}
    return {"count": 0, "hash": sha256_json([]), "source": "missing_treated_as_empty"}


def runtime_state(state_dir: Path, safety_path: Path | None = None) -> dict[str, Any]:
    users_path = state_dir / "users.registry"
    egress_path = state_dir / "egress.registry"
    users = read_registry(users_path)
    egress = read_registry(egress_path)
    selected = selected_moves_state(state_dir)
    safety = read_json(safety_path, {}) if safety_path else read_json(state_dir / "autoswitch-safety.json", {})
    counts = user_counts(users)
    return {
        "users_registry_exists": users_path.exists(),
        "egress_registry_exists": egress_path.exists(),
        "users_registry_hash": sha256_file(users_path),
        "egress_registry_hash": sha256_file(egress_path),
        "selected_move_hash": selected["hash"],
        "selected_move_count": selected["count"],
        "selected_move_source": selected["source"],
        "safety_status": str((safety or {}).get("status") or "unknown").lower(),
        "users": users,
        "egress": egress,
        "user_counts": counts,
        "targets": {row["egress_id"]: row for row in (target_descriptor(row, counts) for row in egress) if row["egress_id"]},
    }


def proposal_moves(proposal: dict[str, Any]) -> list[dict[str, Any]]:
    moves = proposal.get("proposal_moves", [])
    return moves if isinstance(moves, list) else []


def proposal_fingerprint(proposal: dict[str, Any]) -> str:
    moves = [
        {
            "user_ip": row.get("user_ip"),
            "action": row.get("action"),
            "move_type": row.get("move_type"),
            "current_egress": row.get("current_egress"),
            "recommended_egress": row.get("recommended_egress"),
            "route_class": row.get("route_class"),
        }
        for row in proposal_moves(proposal)
    ]
    return sha256_json({"budget": proposal.get("budget"), "proposal_moves": moves})


def policy_fingerprint(policy: dict[str, Any]) -> str:
    fields = {
        "approval_mode": policy.get("approval_mode", "HYBRID"),
        "budget": policy.get("budget"),
        "allowed_users": sorted(policy.get("allowed_users") or []),
        "route_class": policy.get("route_class"),
        "target_class": policy.get("target_class"),
        "trust_class": policy.get("trust_class"),
        "policy_class": policy.get("policy_class"),
        "capacity_rule": policy.get("capacity_rule"),
        "rollback": policy.get("rollback"),
    }
    return sha256_json(fields)


def runtime_fingerprint(runtime: dict[str, Any]) -> str:
    return sha256_json({
        "users_registry_hash": runtime.get("users_registry_hash"),
        "egress_registry_hash": runtime.get("egress_registry_hash"),
        "selected_move_hash": runtime.get("selected_move_hash"),
        "selected_move_count": runtime.get("selected_move_count"),
        "safety_status": runtime.get("safety_status"),
    })


def approval_fingerprint(packet: dict[str, Any]) -> str:
    return sha256_json({
        "schema_version": packet.get("schema_version"),
        "approval_id": packet.get("approval_id"),
        "approval_mode": packet.get("approval_mode"),
        "policy": packet.get("policy"),
        "target_approval": packet.get("target_approval"),
        "expected": packet.get("expected"),
        "expires_at": packet.get("expires_at"),
    })


def target_approval_required(move: dict[str, Any], target: dict[str, Any], policy: dict[str, Any]) -> bool:
    if int(policy.get("budget") or 0) != ALLOWED_POLICY_BUDGET:
        return True
    if policy_class(target) != "AUTOSWITCH_ALLOWED":
        return True
    if route_class(target) != policy.get("route_class"):
        return True
    if trust_class(target) != policy.get("trust_class"):
        return True
    if str(move.get("move_type") or "") not in {"failover", "reconnect", "policy_move", "bounded_autonomy"}:
        return True
    return False


def validate_target_substitution(packet: dict[str, Any], proposal: dict[str, Any], runtime: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    moves = proposal_moves(proposal)
    policy = packet.get("policy") or {}
    target_rows = registry_by_id(runtime.get("egress", []))
    counts = runtime.get("user_counts", {})

    if int(policy.get("budget") or 0) != ALLOWED_POLICY_BUDGET or len(moves) != 1:
        errors.append("policy_requires_exactly_one_move_and_budget_1")
        return {"ok": False, "errors": errors, "target_approval_required": True}

    move = moves[0]
    target_id = str(move.get("recommended_egress") or "")
    target_row = target_rows.get(target_id)
    if not target_row:
        errors.append("target_missing_from_runtime_registry")
        return {"ok": False, "errors": errors, "target_approval_required": True}

    descriptor = target_descriptor(target_row, counts)
    requires_target = target_approval_required(move, target_row, policy)
    target_approval = packet.get("target_approval") or {}
    if requires_target:
        if target_approval.get("exact_target") != target_id:
            errors.append("target_approval_required_for_high_risk_or_class_change")
    else:
        if move.get("user_ip") not in (policy.get("allowed_users") or []):
            errors.append("user_not_allowed_by_policy")
        if descriptor["route_class"] != policy.get("route_class"):
            errors.append("route_class_mismatch")
        if descriptor["trust_class"] != policy.get("trust_class"):
            errors.append("trust_class_mismatch")
        if descriptor["policy_class"] != policy.get("policy_class"):
            errors.append("policy_class_mismatch")
        if descriptor["capacity_class"] == "HARD_FULL":
            errors.append("target_capacity_hard_full")
        rollback = policy.get("rollback") or {}
        if rollback.get("user_ip") != move.get("user_ip") or rollback.get("target") != move.get("current_egress"):
            errors.append("rollback_incompatible")

    return {
        "ok": not errors,
        "errors": errors,
        "target_approval_required": requires_target,
        "target_descriptor": descriptor,
    }


def read_audit_records(audit_store: Path) -> list[dict[str, Any]]:
    if not audit_store.exists():
        return []
    records = []
    for line in audit_store.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            records.append({"record_type": "CORRUPT_RECORD", "raw_hash": sha256_bytes(line.encode("utf-8"))})
    return records


def append_record(audit_store: Path, record: dict[str, Any]) -> dict[str, Any]:
    audit_store.parent.mkdir(parents=True, exist_ok=True)
    previous = read_audit_records(audit_store)
    previous_hash = previous[-1].get("record_hash", "GENESIS") if previous else "GENESIS"
    payload = {k: v for k, v in record.items() if k != "record_hash"}
    payload["previous_record_hash"] = previous_hash
    payload["record_hash"] = sha256_json(payload)
    fd = os.open(audit_store, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        with os.fdopen(fd, "a", encoding="utf-8") as handle:
            handle.write(canonical_json(payload) + "\n")
    finally:
        try:
            os.chmod(audit_store, 0o600)
        except OSError:
            pass
    return payload


def validate_packet(packet: dict[str, Any], proposal: dict[str, Any], runtime: dict[str, Any], audit_store: Path, now: datetime | None = None) -> dict[str, Any]:
    now = now or utc_now()
    errors: list[str] = []
    if packet.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version_invalid")
    if packet.get("approval_mode") != "HYBRID":
        errors.append("approval_mode_not_hybrid")
    try:
        if now >= parse_ts(packet.get("expires_at")):
            errors.append("approval_expired")
    except HybridApprovalError as exc:
        errors.append(str(exc))
    if runtime.get("selected_move_count") != 0:
        errors.append("selected_moves_not_empty")
    if not runtime.get("users_registry_exists") or not runtime.get("egress_registry_exists"):
        errors.append("runtime_registry_missing")
    if runtime.get("safety_status") not in {"ok", "warn"}:
        errors.append("safety_status_not_ok_or_warn")

    expected = packet.get("expected") or {}
    checks = {
        "proposal_fingerprint": proposal_fingerprint(proposal),
        "policy_fingerprint": policy_fingerprint(packet.get("policy") or {}),
        "runtime_fingerprint": runtime_fingerprint(runtime),
        "users_registry_hash": runtime.get("users_registry_hash"),
        "egress_registry_hash": runtime.get("egress_registry_hash"),
        "selected_move_hash": runtime.get("selected_move_hash"),
    }
    for key, actual in checks.items():
        expected_value = expected.get(key)
        if expected_value and expected_value != actual:
            errors.append(f"{key}_mismatch")

    if int(proposal.get("budget") or 0) != ALLOWED_POLICY_BUDGET:
        errors.append("proposal_budget_not_1")
    if int((packet.get("policy") or {}).get("budget") or 0) != ALLOWED_POLICY_BUDGET:
        errors.append("policy_budget_not_1")
    if len(proposal_moves(proposal)) != 1:
        errors.append("proposal_move_count_not_1")

    substitution = validate_target_substitution(packet, proposal, runtime)
    errors.extend(substitution["errors"])

    approval_id = str(packet.get("approval_id") or "")
    if not approval_id:
        errors.append("approval_id_missing")
    elif any(row.get("approval_id") == approval_id for row in read_audit_records(audit_store)):
        errors.append("approval_replay")

    verdict = "ALLOW_HYBRID_BOUNDED_AUTONOMY" if not errors else "DENY_HYBRID_APPROVAL"
    return {
        "allow": not errors,
        "verdict": verdict,
        "errors": errors,
        "checks": checks,
        "substitution": substitution,
        "runtime_mutation_performed": False,
        "users_moved": False,
        "routing_changed": False,
        "autoswitch_apply_run": False,
    }


def execute_record(packet: dict[str, Any], proposal: dict[str, Any], runtime: dict[str, Any], audit_store: Path, now: datetime | None = None) -> dict[str, Any]:
    now = now or utc_now()
    validation = validate_packet(packet, proposal, runtime, audit_store, now=now)
    record = {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "record_type": "hybrid_autonomy_record" if validation["allow"] else "hybrid_autonomy_denial",
        "approval_id": packet.get("approval_id", ""),
        "packet_id": packet.get("packet_id", ""),
        "created_at": now.isoformat(),
        "verdict": validation["verdict"],
        "errors": validation["errors"],
        "checks": validation["checks"],
        "substitution": validation["substitution"],
        "budget": ALLOWED_POLICY_BUDGET,
        "proposal_moves": proposal_moves(proposal),
        "bounded_autonomy_authorized": validation["allow"],
        "movement_executor_invoked": False,
        "runtime_mutation_performed": False,
        "users_moved": False,
        "routing_changed": False,
        "autoswitch_apply_run": False,
    }
    written = append_record(audit_store, redact(record))
    return {"record_written": True, "record": written, "validation": validation}


def build_expected(packet: dict[str, Any], proposal: dict[str, Any], runtime: dict[str, Any]) -> dict[str, str]:
    return {
        "proposal_fingerprint": proposal_fingerprint(proposal),
        "policy_fingerprint": policy_fingerprint(packet.get("policy") or {}),
        "runtime_fingerprint": runtime_fingerprint(runtime),
        "users_registry_hash": runtime.get("users_registry_hash", ""),
        "egress_registry_hash": runtime.get("egress_registry_hash", ""),
        "selected_move_hash": runtime.get("selected_move_hash", ""),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate or record a V7 Z2 hybrid approval packet.")
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--proposal", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--safety-json", type=Path)
    parser.add_argument("--audit-store", type=Path, default=Path("docs/track7/productization/z2-evidence/hybrid-autonomy-audit.jsonl"))
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--execute-record", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args(argv)

    packet = read_json(args.packet, {})
    proposal = read_json(args.proposal, {})
    runtime = runtime_state(args.state_dir, args.safety_json)
    if args.execute_record:
        result = execute_record(packet, proposal, runtime, args.audit_store)
    else:
        result = validate_packet(packet, proposal, runtime, args.audit_store)
    print(json.dumps(redact(result), ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=True))
    return 0 if result.get("allow") or result.get("validation", {}).get("allow") else 1


if __name__ == "__main__":
    raise SystemExit(main())
