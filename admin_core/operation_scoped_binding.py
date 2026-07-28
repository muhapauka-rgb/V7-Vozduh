"""Deterministic operation-scoped source binding for governed execution."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from admin_core import operator_execution, registry_readers


SCHEMA_VERSION = "v7.operation-scoped-source-binding.v2"
SOURCE_KEYS = ("users_registry", "egress_registry", "runtime_state", "candidate_suitability")
_CATEGORICAL_EGRESS_FIELDS = ("code", "diagnose_reason", "diagnose_severity", "load_status")
_CATEGORICAL_MOVE_FIELDS = (
    "action_class",
    "readiness",
    "readiness_state",
    "safety_verdict",
    "rollback_readiness",
    "verification_readiness",
    "service_fit_verdict",
    "recovery_applicability",
    "state_change_cost_verdict",
    "net_benefit_verdict",
)


def selected_identity(selected: dict[str, Any]) -> dict[str, str]:
    return {
        "user": str(selected.get("user") or selected.get("user_ip") or ""),
        "source": str(selected.get("from") or selected.get("current_egress") or selected.get("current_channel") or ""),
        "target": str(selected.get("to") or selected.get("recommended_egress") or selected.get("recommended_channel") or ""),
    }


def runtime_decision_projection(
    runtime_state: dict[str, Any], *, user: str, source: str, target: str
) -> dict[str, Any]:
    if not user or not source or not target or not isinstance(runtime_state, dict):
        return {}
    users = sorted(
        (row for row in (runtime_state.get("users") or []) if isinstance(row, dict) and str(row.get("ip") or "") == user),
        key=operator_execution.sha256_json,
    )
    desired = sorted(
        (row for row in (runtime_state.get("user_desired_state") or []) if isinstance(row, dict) and str(row.get("ip") or "") == user),
        key=operator_execution.sha256_json,
    )
    egress = runtime_state.get("egress") if isinstance(runtime_state.get("egress"), dict) else {}

    def project(channel: str) -> dict[str, Any]:
        row = egress.get(channel) if isinstance(egress.get(channel), dict) else {}
        return {key: row.get(key) for key in _CATEGORICAL_EGRESS_FIELDS if key in row}

    return {
        "schema_version": "v7.runtime-decision-projection.v2",
        "selected_identity": {"user": user, "source": source, "target": target},
        "runtime_user": users,
        "user_desired_state": desired,
        "source_egress": project(source),
        "target_egress": project(target),
    }


def candidate_suitability_decision_projection(
    suitability: dict[str, Any],
    *,
    user: str,
    source: str,
    target: str,
    selected: dict[str, Any],
) -> dict[str, Any]:
    if not user or not source or not target or not isinstance(suitability, dict):
        return {}
    user_row = next(
        (row for row in (suitability.get("items") or []) if isinstance(row, dict) and str(row.get("user") or "") == user),
        {},
    )
    candidates = []
    for row in user_row.get("candidates") if isinstance(user_row.get("candidates"), list) else []:
        if not isinstance(row, dict) or str(row.get("channel") or "") not in {source, target}:
            continue
        candidates.append({
            key: row.get(key)
            for key in ("user", "channel", "recommendation", "authority")
            if key in row
        })
    candidates.sort(key=lambda row: (str(row.get("channel") or ""), operator_execution.sha256_json(row)))
    move = {
        "user": user,
        "source": source,
        "target": target,
        **{key: selected.get(key) for key in _CATEGORICAL_MOVE_FIELDS if key in selected},
    }
    return {
        "schema_version": "v7.candidate-suitability-decision-projection.v2",
        "freshness_state": suitability.get("freshness_state"),
        "runtime_decision_authority": user_row.get("runtime_decision_authority"),
        "selected_identity": {"user": user, "source": source, "target": target},
        "selected_move": move,
        "source_and_target_candidates": candidates,
    }


def build_from_payloads(
    *,
    selected: dict[str, Any],
    users_registry: list[dict[str, str]],
    egress_registry: list[dict[str, str]],
    runtime_state: dict[str, Any],
    candidate_suitability: dict[str, Any],
    raw_source_hashes: dict[str, str] | None = None,
    read_consistency: dict[str, Any] | None = None,
) -> dict[str, Any]:
    identity = selected_identity(selected)
    user, source, target = identity["user"], identity["source"], identity["target"]
    runtime_projection = runtime_decision_projection(runtime_state, user=user, source=source, target=target)
    suitability_projection = candidate_suitability_decision_projection(
        candidate_suitability, user=user, source=source, target=target, selected=selected
    )
    projections = {
        "users_registry": sorted(
            (row for row in users_registry if str(row.get("ip") or "") == user),
            key=operator_execution.sha256_json,
        ),
        "egress_registry": sorted(
            (row for row in egress_registry if str(row.get("id") or row.get("name") or "") in {source, target}),
            key=lambda row: (str(row.get("id") or row.get("name") or ""), operator_execution.sha256_json(row)),
        ),
        "runtime_state": runtime_projection,
        "candidate_suitability": suitability_projection,
    }
    consistent = bool((read_consistency or {}).get("stable", True))
    identity_complete = bool(user and source and target)
    source_hashes = {
        key: operator_execution.sha256_json(value)
        for key, value in projections.items()
        if value and consistent and identity_complete
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "BOUND" if len(source_hashes) == len(SOURCE_KEYS) else "STOP_SAFE",
        "selected_identity": identity,
        "source_hashes": source_hashes,
        "source_bundle_hash": operator_execution.sha256_json(source_hashes) if len(source_hashes) == len(SOURCE_KEYS) else "",
        "snapshot_bundle_hash": operator_execution.sha256_json(source_hashes) if len(source_hashes) == len(SOURCE_KEYS) else "",
        "raw_source_hashes": dict(raw_source_hashes or {}),
        "runtime_projection": runtime_projection,
        "candidate_suitability_projection": suitability_projection,
        "projections": projections,
        "read_consistency": dict(read_consistency or {"stable": True, "attempts": 1}),
        "fail_closed_without_selected_identity": not identity_complete,
        "fail_closed_on_mixed_generation": not consistent,
    }


def build_cohort_from_payloads(
    *,
    selected_moves: list[dict[str, Any]],
    users_registry: list[dict[str, str]],
    egress_registry: list[dict[str, str]],
    runtime_state: dict[str, Any],
    candidate_suitability: dict[str, Any],
    raw_source_hashes: dict[str, str] | None = None,
    read_consistency: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Bind every selected move to one coherent source generation.

    This extends the existing operation-scoped owner; it is not a second
    snapshot registry.  Member projections are derived from the same four
    atomically observed source payloads and then folded into deterministic
    cohort hashes.
    """
    ordered = sorted(
        (dict(move) for move in selected_moves if isinstance(move, dict)),
        key=lambda move: (
            selected_identity(move)["user"],
            selected_identity(move)["source"],
            selected_identity(move)["target"],
            operator_execution.sha256_json(move),
        ),
    )
    members = [
        build_from_payloads(
            selected=move,
            users_registry=users_registry,
            egress_registry=egress_registry,
            runtime_state=runtime_state,
            candidate_suitability=candidate_suitability,
            raw_source_hashes=raw_source_hashes,
            read_consistency=read_consistency,
        )
        for move in ordered
    ]
    identities = [member.get("selected_identity") or {} for member in members]
    unique_identities = {
        (
            str(identity.get("user") or ""),
            str(identity.get("source") or ""),
            str(identity.get("target") or ""),
        )
        for identity in identities
    }
    consistent = bool((read_consistency or {}).get("stable", True))
    complete = bool(members) and len(unique_identities) == len(members)
    bound = consistent and complete and all(member.get("status") == "BOUND" for member in members)
    source_hashes = {}
    if bound:
        for key in SOURCE_KEYS:
            source_hashes[key] = operator_execution.sha256_json([
                {
                    "selected_identity": member.get("selected_identity") or {},
                    "source_hash": (member.get("source_hashes") or {}).get(key),
                }
                for member in members
            ])
    bundle_hash = operator_execution.sha256_json(source_hashes) if len(source_hashes) == len(SOURCE_KEYS) else ""
    return {
        "schema_version": SCHEMA_VERSION,
        "binding_scope": "COHORT",
        "status": "BOUND" if bound else "STOP_SAFE",
        "selected_move_count": len(members),
        "selected_identities": identities,
        "member_bindings": members,
        "source_hashes": source_hashes,
        "source_bundle_hash": bundle_hash,
        "snapshot_bundle_hash": bundle_hash,
        "raw_source_hashes": dict(raw_source_hashes or {}),
        "read_consistency": dict(read_consistency or {"stable": True, "attempts": 1}),
        "fail_closed_without_selected_identity": not complete,
        "fail_closed_on_mixed_generation": not consistent,
    }


def _signature(path: Path) -> tuple[int, int, int, int] | None:
    try:
        stat = path.stat()
    except OSError:
        return None
    return (int(stat.st_dev), int(stat.st_ino), int(stat.st_size), int(stat.st_mtime_ns))


def read_binding(
    *,
    state_dir: Path,
    snapshot_root: Path,
    selected: dict[str, Any],
    max_attempts: int = 2,
    after_read_hook: Callable[[int], None] | None = None,
) -> dict[str, Any]:
    paths = {
        "users_registry": state_dir / "users.registry",
        "egress_registry": state_dir / "egress.registry",
        "runtime_state": state_dir / "v7-state.json",
        "candidate_suitability": snapshot_root / "candidate-suitability-summary.json",
    }
    last_before: dict[str, Any] = {}
    last_after: dict[str, Any] = {}
    for attempt in range(1, max(1, int(max_attempts)) + 1):
        before = {key: _signature(path) for key, path in paths.items()}
        blobs: dict[str, bytes] = {}
        try:
            blobs = {key: path.read_bytes() for key, path in paths.items()}
        except OSError:
            blobs = {}
        if after_read_hook:
            after_read_hook(attempt)
        after = {key: _signature(path) for key, path in paths.items()}
        last_before, last_after = before, after
        if blobs and before == after and all(value is not None for value in before.values()):
            try:
                users = registry_readers.parse_registry_lines(blobs["users_registry"].decode("utf-8").splitlines())
                egress = registry_readers.parse_registry_lines(blobs["egress_registry"].decode("utf-8").splitlines())
                runtime = json.loads(blobs["runtime_state"].decode("utf-8"))
                suitability = json.loads(blobs["candidate_suitability"].decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                break
            raw = {key: operator_execution.sha256_bytes(value) for key, value in blobs.items()}
            return build_from_payloads(
                selected=selected,
                users_registry=users,
                egress_registry=egress,
                runtime_state=runtime,
                candidate_suitability=suitability,
                raw_source_hashes=raw,
                read_consistency={"stable": True, "attempts": attempt, "signatures": after},
            )
    return build_from_payloads(
        selected=selected,
        users_registry=[],
        egress_registry=[],
        runtime_state={},
        candidate_suitability={},
        read_consistency={
            "stable": False,
            "attempts": max(1, int(max_attempts)),
            "reason": "mixed_generation_or_unreadable_input",
            "before": last_before,
            "after": last_after,
        },
    )


def read_cohort_binding(
    *,
    state_dir: Path,
    snapshot_root: Path,
    selected_moves: list[dict[str, Any]],
    max_attempts: int = 2,
    after_read_hook: Callable[[int], None] | None = None,
) -> dict[str, Any]:
    """Read one stable source generation and bind an entire selected cohort."""
    paths = {
        "users_registry": state_dir / "users.registry",
        "egress_registry": state_dir / "egress.registry",
        "runtime_state": state_dir / "v7-state.json",
        "candidate_suitability": snapshot_root / "candidate-suitability-summary.json",
    }
    last_before: dict[str, Any] = {}
    last_after: dict[str, Any] = {}
    for attempt in range(1, max(1, int(max_attempts)) + 1):
        before = {key: _signature(path) for key, path in paths.items()}
        blobs: dict[str, bytes] = {}
        try:
            blobs = {key: path.read_bytes() for key, path in paths.items()}
        except OSError:
            blobs = {}
        if after_read_hook:
            after_read_hook(attempt)
        after = {key: _signature(path) for key, path in paths.items()}
        last_before, last_after = before, after
        if blobs and before == after and all(value is not None for value in before.values()):
            try:
                users = registry_readers.parse_registry_lines(blobs["users_registry"].decode("utf-8").splitlines())
                egress = registry_readers.parse_registry_lines(blobs["egress_registry"].decode("utf-8").splitlines())
                runtime = json.loads(blobs["runtime_state"].decode("utf-8"))
                suitability = json.loads(blobs["candidate_suitability"].decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                break
            raw = {key: operator_execution.sha256_bytes(value) for key, value in blobs.items()}
            return build_cohort_from_payloads(
                selected_moves=selected_moves,
                users_registry=users,
                egress_registry=egress,
                runtime_state=runtime,
                candidate_suitability=suitability,
                raw_source_hashes=raw,
                read_consistency={"stable": True, "attempts": attempt, "signatures": after},
            )
    return build_cohort_from_payloads(
        selected_moves=selected_moves,
        users_registry=[],
        egress_registry=[],
        runtime_state={},
        candidate_suitability={},
        read_consistency={
            "stable": False,
            "attempts": max(1, int(max_attempts)),
            "reason": "mixed_generation_or_unreadable_input",
            "before": last_before,
            "after": last_after,
        },
    )
