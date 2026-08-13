"""Minimal effect-free V7 Routing Core contract implementation.

RESET-M4 shadow code only: it performs no I/O, subprocess, lock, network,
policy, assignment, kernel, Runtime or production mutation. Existing owners
remain authoritative for every input fact and for any later effectful adapter.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from time import perf_counter
from typing import Any


CORE_INPUT_SCHEMA = "v7.routing-core-input.v1"
CORE_SHADOW_SCHEMA = "v7.routing-core-shadow-result.v1"
FORBIDDEN_ENGINEERING_INPUTS = {
    "cps",
    "omp",
    "reports",
    "production_maturity",
    "learning",
    "replay",
    "polygon",
    "campaign",
    "history",
}


class RoutingCoreContractError(ValueError):
    """Fail-closed contract error with a stable machine status."""

    def __init__(self, status: str) -> None:
        super().__init__(status)
        self.status = status


def _required_text(row: dict[str, Any], key: str) -> str:
    value = str(row.get(key, "") or "").strip()
    if not value:
        raise RoutingCoreContractError(f"MISSING_{key.upper()}")
    return value


def _parse_time(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise RoutingCoreContractError("INVALID_OBSERVED_AT") from exc
    if parsed.tzinfo is None:
        raise RoutingCoreContractError("OBSERVED_AT_MUST_BE_TIMEZONE_AWARE")
    return parsed.astimezone(timezone.utc)


def _canonical_hash(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def observe(envelope: dict[str, Any], *, now: datetime | None = None) -> dict[str, Any]:
    """Validate and normalize one immutable generation-bound input receipt."""
    if envelope.get("schema") != CORE_INPUT_SCHEMA:
        raise RoutingCoreContractError("INVALID_INPUT_SCHEMA")
    forbidden = sorted(FORBIDDEN_ENGINEERING_INPUTS.intersection(envelope))
    if forbidden:
        raise RoutingCoreContractError(f"FORBIDDEN_ENGINEERING_INPUT:{forbidden[0]}")
    generation = _required_text(envelope, "generation")
    observed_at = _parse_time(_required_text(envelope, "observed_at"))
    max_age_ms = int(envelope.get("max_age_ms", 0) or 0)
    if max_age_ms <= 0:
        raise RoutingCoreContractError("INVALID_MAX_AGE_MS")
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    age_ms = max(0, int((current - observed_at).total_seconds() * 1000))
    if age_ms > max_age_ms:
        raise RoutingCoreContractError("STALE_INPUT_STOP_SAFE")
    normalized = deepcopy(envelope)
    normalized["generation"] = generation
    normalized["observed_at"] = observed_at.isoformat()
    normalized["age_ms"] = age_ms
    normalized["freshness_decision"] = "USE_FRESH_PREPARED_RECEIPT"
    return normalized


def state(observation: dict[str, Any]) -> dict[str, Any]:
    """Validate the one-owner Runtime facts required by deterministic PLAN."""
    assignments = observation.get("assignments")
    targets = observation.get("targets")
    scope = observation.get("scope")
    policy = observation.get("policy")
    authority = observation.get("authority")
    operation = observation.get("operation")
    if not isinstance(assignments, dict) or not isinstance(targets, dict):
        raise RoutingCoreContractError("MISSING_ASSIGNMENT_OR_TARGET_TRUTH")
    if not isinstance(scope, dict) or not isinstance(policy, dict):
        raise RoutingCoreContractError("MISSING_SCOPE_OR_POLICY")
    if not isinstance(authority, dict) or not isinstance(operation, dict):
        raise RoutingCoreContractError("MISSING_AUTHORITY_OR_OPERATION")
    for row, keys in (
        (policy, ("generation",)),
        (authority, ("generation",)),
        (operation, ("id", "lease_id", "fencing_token", "idempotency_key")),
    ):
        for key in keys:
            _required_text(row, key)
    users = sorted({str(item) for item in scope.get("users", []) if str(item)})
    if not users:
        raise RoutingCoreContractError("EMPTY_SCOPE")
    permitted = {str(item) for item in authority.get("permitted_users", [])}
    if not set(users).issubset(permitted):
        raise RoutingCoreContractError("AUTHORITY_SCOPE_MISMATCH_STOP_SAFE")
    max_users = int(authority.get("max_users", 0) or 0)
    if max_users <= 0 or len(users) > max_users:
        raise RoutingCoreContractError("AUTHORITY_BLAST_LIMIT_STOP_SAFE")
    return {
        "generation": observation["generation"],
        "assignments": deepcopy(assignments),
        "targets": deepcopy(targets),
        "scope": {"source": str(scope.get("source", "") or ""), "users": users},
        "policy": deepcopy(policy),
        "authority": deepcopy(authority),
        "operation": deepcopy(operation),
    }


def plan(runtime_state: dict[str, Any]) -> dict[str, Any]:
    """Produce a pure deterministic minimal desired-assignment delta."""
    source = _required_text(runtime_state["scope"], "source")
    allowed = {str(item) for item in runtime_state["policy"].get("allowed_targets", [])}
    reserve = int(runtime_state["policy"].get("capacity_reserve", 0) or 0)
    candidates: list[tuple[int, str]] = []
    for target, receipt in runtime_state["targets"].items():
        if target == source or target not in allowed or not isinstance(receipt, dict):
            continue
        if receipt.get("healthy") is not True:
            continue
        capacity = int(receipt.get("capacity", 0) or 0)
        assigned = int(receipt.get("assigned", 0) or 0)
        available = capacity - assigned - reserve
        if available > 0:
            candidates.append((available, str(target)))
    candidates.sort(key=lambda item: (-item[0], item[1]))
    if not candidates:
        return {"decision": "STOP_SAFE_NO_LAWFUL_TARGET", "moves": []}
    remaining = {target: available for available, target in candidates}
    moves: list[dict[str, str]] = []
    for user in runtime_state["scope"]["users"]:
        if runtime_state["assignments"].get(user) != source:
            continue
        target = next((name for _, name in candidates if remaining[name] > 0), "")
        if not target:
            return {"decision": "STOP_SAFE_INSUFFICIENT_CAPACITY", "moves": []}
        moves.append({"user": user, "source": source, "target": target})
        remaining[target] -= 1
    return {"decision": "PLAN_READY" if moves else "NO_CHANGE", "moves": moves}


def apply_shadow(runtime_state: dict[str, Any], desired: dict[str, Any]) -> dict[str, Any]:
    """Bind the future APPLY contract while guaranteeing zero effects."""
    operation = runtime_state["operation"]
    return {
        "mode": "SHADOW_EFFECTS_ZERO",
        "operation_id": operation["id"],
        "lease_id": operation["lease_id"],
        "fencing_token": operation["fencing_token"],
        "idempotency_key": operation["idempotency_key"],
        "desired_delta_hash": _canonical_hash(desired.get("moves", [])),
        "apply_executed": False,
        "users_moved": 0,
        "runtime_mutation": False,
    }


def verify_contract(runtime_state: dict[str, Any], desired: dict[str, Any]) -> dict[str, Any]:
    """Describe exact post-apply proofs without running probes in shadow mode."""
    return {
        "mode": "CONTRACT_ONLY_NO_PROBE",
        "generation": runtime_state["generation"],
        "operation_id": runtime_state["operation"]["id"],
        "required": [
            "assignment_generation_match",
            "kernel_route_visibility",
            "exact_client_routing_context",
            "expected_target_egress_identity",
            "target_payload_response",
        ],
        "move_count": len(desired.get("moves", [])),
        "verification_executed": False,
    }


def run_shadow(envelope: dict[str, Any], *, now: datetime | None = None) -> dict[str, Any]:
    """Execute OBSERVE -> STATE -> PLAN -> shadow APPLY -> VERIFY contract."""
    started = perf_counter()
    observed = observe(envelope, now=now)
    runtime_state = state(observed)
    desired = plan(runtime_state)
    shadow_apply = apply_shadow(runtime_state, desired)
    verification = verify_contract(runtime_state, desired)
    elapsed_ms = round((perf_counter() - started) * 1000.0, 3)
    decision_material = {
        "generation": runtime_state["generation"],
        "policy_generation": runtime_state["policy"]["generation"],
        "authority_generation": runtime_state["authority"]["generation"],
        "operation_id": runtime_state["operation"]["id"],
        "decision": desired,
    }
    return {
        "schema": CORE_SHADOW_SCHEMA,
        "status": "SHADOW_PASS",
        "effects": "ZERO",
        "freshness_decision": observed["freshness_decision"],
        "decision": desired,
        "decision_fingerprint": _canonical_hash(decision_material),
        "apply": shadow_apply,
        "verify": verification,
        "elapsed_ms": elapsed_ms,
    }


def prepare_semantic_classes(assignments: dict[str, dict[str, Any]], *, generation: str) -> dict[str, Any]:
    """Compact an Engineering Plane scan into generation-bound class receipts."""
    if not generation:
        raise RoutingCoreContractError("MISSING_CLASS_PREPARATION_GENERATION")
    grouped: dict[str, list[str]] = {}
    semantics: dict[str, dict[str, Any]] = {}
    required = ("source_channel", "service_compatibility", "policy_set", "eligible_target_bucket", "path_fingerprint", "correlation_domain", "exception_boundary")
    for user, row in assignments.items():
        if not isinstance(row, dict) or any(not str(row.get(key, "") or "") for key in required):
            raise RoutingCoreContractError("INCOMPLETE_SEMANTIC_CLASS_INPUT")
        semantic = {key: str(row[key]) for key in required}
        class_id = "rclass_" + _canonical_hash(semantic)[:24]
        semantics[class_id] = semantic
        grouped.setdefault(class_id, []).append(str(user))
    classes = []
    for class_id, members in sorted(grouped.items()):
        ordered = sorted(set(members))
        classes.append({"class_id": class_id, "semantic": semantics[class_id], "member_count": len(ordered), "membership_fingerprint": _canonical_hash(ordered), "raw_members_retained": False})
    return {"schema": "v7.routing-core-prepared-classes.v1", "generation": generation, "classes": classes, "class_count": len(classes), "input_member_count": len(assignments), "projection_fingerprint": _canonical_hash({"generation": generation, "classes": classes}), "runtime_effects": "ZERO"}


def bounded_class_bucket_commit(
    prepared: dict[str, Any], *, class_id: str, expected_generation: str,
    expected_projection_fingerprint: str, target_bucket: str,
    target_generation: str, capacity_available: int,
) -> dict[str, Any]:
    """Validate one O(1)-bounded class indirection commit without effects."""
    if prepared.get("schema") != "v7.routing-core-prepared-classes.v1":
        raise RoutingCoreContractError("INVALID_PREPARED_CLASS_SCHEMA")
    if str(prepared.get("generation") or "") != expected_generation:
        raise RoutingCoreContractError("CLASS_GENERATION_CHANGED_STOP_SAFE")
    if str(prepared.get("projection_fingerprint") or "") != expected_projection_fingerprint:
        raise RoutingCoreContractError("CLASS_PROJECTION_CHANGED_STOP_SAFE")
    if not class_id or not target_bucket or not target_generation:
        raise RoutingCoreContractError("CLASS_COMMIT_BINDING_MISSING")
    match = next((row for row in prepared.get("classes", []) if row.get("class_id") == class_id), None)
    if not isinstance(match, dict):
        raise RoutingCoreContractError("PREPARED_CLASS_MISSING_STOP_SAFE")
    member_count = int(match.get("member_count", 0) or 0)
    if member_count <= 0 or capacity_available < member_count:
        raise RoutingCoreContractError("TARGET_BUCKET_CAPACITY_STOP_SAFE")
    commit = {"class_id": class_id, "membership_fingerprint": str(match.get("membership_fingerprint") or ""), "member_count": member_count, "source_generation": expected_generation, "target_bucket": target_bucket, "target_generation": target_generation}
    return {"schema": "v7.routing-core-class-bucket-commit.v1", "status": "CLASS_BUCKET_COMMIT_READY", "commit": commit, "commit_fingerprint": _canonical_hash(commit), "member_rows_scanned_in_hot_path": 0, "raw_members_loaded_in_hot_path": False, "per_user_writes_requested": 0, "runtime_effects": "ZERO_CONTRACT_ONLY"}
