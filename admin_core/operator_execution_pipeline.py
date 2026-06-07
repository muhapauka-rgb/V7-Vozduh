"""Canonical governed execution pipeline contracts for operator movement.

This module is intentionally pure. It defines the contract, lifecycle, and
decision/action matrix that bridge recommendations to the existing governed
execution owner. It does not invoke shell commands or write runtime state.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any


SCHEMA_VERSION = "v7.operator-governed-execution-pipeline.v1"
CANONICAL_PLANNER = "tools/v7-users-autoswitch"
CANONICAL_PACKET_OWNER = "admin_core/operator_execution.py"
CANONICAL_PACKET_TOOL = "tools/v7-operator-execution-packet"
CANONICAL_RUNTIME_EXECUTOR = "tools/v7-users-autoswitch --apply --verify"
CANONICAL_ROLLBACK_EXECUTOR = "tools/v7-users-autoswitch --rollback-packet --apply --verify"
CANONICAL_FEEDBACK_OWNER = "admin_core/operator_execution_feedback.py"
CANONICAL_OBSERVABILITY_OWNER = "admin_core/operator_observability.py"

EXECUTION_LOOP_STAGES = [
    {
        "stage": "planner",
        "owner": CANONICAL_PLANNER,
        "inputs": ["production truth", "runtime state", "service snapshots", "trust snapshots", "authority budget"],
        "outputs": ["candidate moves", "selected moves", "generation id", "atomic execution envelope"],
        "manual": False,
        "runtime_mutation": False,
        "timing_metric": "planner_duration_ms",
    },
    {
        "stage": "packet",
        "owner": CANONICAL_PACKET_TOOL,
        "inputs": ["selected moves", "authority budget", "rollback manifest", "operator approval intent"],
        "outputs": ["approval packet", "approved plan lock candidate", "rollback manifest"],
        "manual": True,
        "runtime_mutation": False,
        "timing_metric": "packet_duration_ms",
    },
    {
        "stage": "restore_barrier",
        "owner": CANONICAL_PACKET_OWNER,
        "inputs": ["valid packet", "selected move hash", "source bundle hash", "dual approval"],
        "outputs": ["generation-bound restore barrier clearance"],
        "manual": True,
        "runtime_mutation": "clearance_write_only",
        "timing_metric": "restore_barrier_duration_ms",
    },
    {
        "stage": "apply",
        "owner": CANONICAL_RUNTIME_EXECUTOR,
        "inputs": ["fresh recheck", "restore barrier clearance", "rollback packet"],
        "outputs": ["bounded route/user movement result", "apply audit"],
        "manual": True,
        "runtime_mutation": "governed_user_movement_when_explicitly_invoked",
        "timing_metric": "apply_duration_ms",
    },
    {
        "stage": "verification",
        "owner": CANONICAL_RUNTIME_EXECUTOR,
        "inputs": ["apply result", "route check", "service health"],
        "outputs": ["verification verdict", "rollback_required decision"],
        "manual": False,
        "runtime_mutation": False,
        "timing_metric": "verification_duration_ms",
    },
    {
        "stage": "feedback",
        "owner": CANONICAL_FEEDBACK_OWNER,
        "inputs": ["execution result", "verification result", "prediction", "recommendation hash"],
        "outputs": ["outcome feedback", "trust feedback", "prediction feedback", "recommendation feedback"],
        "manual": False,
        "runtime_mutation": False,
        "timing_metric": "feedback_duration_ms",
    },
    {
        "stage": "closure",
        "owner": CANONICAL_FEEDBACK_OWNER,
        "inputs": ["feedback records", "audit reference", "rollback result"],
        "outputs": ["closure record", "operator-visible final state"],
        "manual": False,
        "runtime_mutation": False,
        "timing_metric": "closure_duration_ms",
    },
]

REQUESTED_EXECUTION_TIMING_METRICS = [
    "planner_duration_ms",
    "packet_duration_ms",
    "restore_barrier_duration_ms",
    "apply_duration_ms",
    "verification_duration_ms",
    "feedback_duration_ms",
    "total_duration_ms",
    "per_user_duration_ms",
]

REQUIRED_RECOMMENDATION_FIELDS = [
    "user",
    "current_channel",
    "recommended_channel",
    "confidence",
    "trust",
    "prediction",
    "risk",
    "rollback_plan",
    "snapshot_generation",
    "source_hashes",
    "reason_summary",
]

EXECUTION_STATES = [
    "EXECUTION_READY",
    "EXECUTION_BLOCKED",
    "EXECUTION_RUNNING",
    "EXECUTION_SUCCESS",
    "EXECUTION_PARTIAL",
    "EXECUTION_FAILED",
    "ROLLBACK_REQUIRED",
    "ROLLBACK_RUNNING",
    "ROLLBACK_SUCCESS",
    "ROLLBACK_FAILED",
]


def stable_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return default if number != number else number


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _parse_ts(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _duration_ms_from_row(row: dict[str, Any]) -> float | None:
    for key in ("duration_ms", "elapsed_ms", "stage_duration_ms"):
        if key in row:
            return round(max(0.0, _as_float(row.get(key))), 3)
    for key in ("duration_sec", "elapsed_sec", "stage_duration_sec"):
        if key in row:
            return round(max(0.0, _as_float(row.get(key)) * 1000.0), 3)
    started = _parse_ts(row.get("started_at") or row.get("start_time") or row.get("operation_started_at"))
    ended = _parse_ts(row.get("completed_at") or row.get("finished_at") or row.get("end_time") or row.get("verification_time"))
    if started and ended and ended >= started:
        return round((ended - started).total_seconds() * 1000.0, 3)
    return None


def _stage_from_row(row: dict[str, Any]) -> str:
    text = " ".join(
        str(row.get(key, "")).lower()
        for key in ("stage", "event_type", "action", "status", "summary", "message", "component")
    )
    if "restore" in text and "barrier" in text:
        return "restore_barrier"
    if "packet" in text or "approval" in text:
        return "packet"
    if "verify" in text or "verification" in text:
        return "verification"
    if "feedback" in text or "outcome" in text or "recommendation" in text or "prediction" in text or "trust" in text:
        return "feedback"
    if "closure" in text or "closed" in text:
        return "closure"
    if "apply" in text or "switch" in text or "movement" in text:
        return "apply"
    if "planner" in text or "candidate" in text or "selected" in text:
        return "planner"
    return ""


def _stage_metric(stage: str) -> str:
    if stage == "restore_barrier":
        return "restore_barrier_duration_ms"
    if stage:
        return f"{stage}_duration_ms"
    return ""


def recommendation_execution_contract(row: dict[str, Any]) -> dict[str, Any]:
    """Convert an operator recommendation row into an execution candidate.

    The returned candidate is not executable by itself. It is the canonical
    payload that must be turned into an approval packet and then consumed by the
    existing restore-barrier/governed apply chain.
    """
    user = str(row.get("user") or row.get("ip") or "")
    current = str(row.get("current_channel") or row.get("current") or "")
    target = str(row.get("recommended_channel") or row.get("target") or "")
    source_hashes = {
        "recommendation_hash": str(row.get("recommendation_hash") or ""),
        "source_hash": str(row.get("source_hash") or ""),
    }
    candidate = {
        "schema_version": "v7.recommendation-execution-candidate.v1",
        "user": user,
        "current_channel": current,
        "recommended_channel": target,
        "confidence": row.get("confidence", 0.0),
        "trust": row.get("trust", 0.0),
        "prediction": row.get("prediction") if isinstance(row.get("prediction"), dict) else {},
        "risk": row.get("risk", 0.0),
        "rollback_plan": {
            "required": True,
            "rollback_target": current,
            "owner": CANONICAL_PACKET_OWNER,
            "executor": CANONICAL_ROLLBACK_EXECUTOR,
        },
        "snapshot_generation": {
            "required": True,
            "fresh_execution_time_recheck_required": True,
            "restore_barrier_required": True,
        },
        "source_hashes": source_hashes,
        "reason_summary": list(row.get("reasons") or [])[:8],
        "approval_packet_required": True,
        "execution_candidate": bool(user and current and target and current != target),
        "execution_allowed_now": False,
        "runtime_mutation_performed": False,
        "next_required_state": "APPROVAL_PACKET_REQUIRED",
    }
    candidate["candidate_hash"] = stable_hash({
        "user": user,
        "current_channel": current,
        "recommended_channel": target,
        "source_hashes": source_hashes,
    })[:24]
    return candidate


def approval_packet_lifecycle() -> list[dict[str, Any]]:
    return [
        {
            "state": "PACKET_CREATED",
            "condition": "operator selects a recommendation or batch preview",
            "decision": "create approval packet candidate",
            "action": "generate packet from canonical recommendation contract",
            "executor": CANONICAL_PACKET_TOOL,
            "trigger": "operator explicit approval intent",
            "evidence": ["packet json", "candidate hash", "source hashes"],
            "blocked_actions": ["runtime apply", "direct user-switch"],
            "next_state": "PACKET_VALIDATING",
        },
        {
            "state": "PACKET_VALIDATING",
            "condition": "packet exists and has dual approval metadata",
            "decision": "validate schema, ttl, budget, rollback manifest and selected move hash",
            "action": "run packet validation and execution-time recheck",
            "executor": CANONICAL_PACKET_OWNER,
            "trigger": "packet submit",
            "evidence": ["validation result", "recheck result", "audit record"],
            "blocked_actions": ["runtime apply when invalid", "restore barrier write when mismatch"],
            "next_state": "PACKET_APPROVED" ,
        },
        {
            "state": "PACKET_REJECTED",
            "condition": "packet invalid, expired, replayed, mismatched, or manually rejected",
            "decision": "deny execution",
            "action": "write denial audit and closure",
            "executor": CANONICAL_PACKET_OWNER,
            "trigger": "validation failure or operator rejection",
            "evidence": ["denial audit", "closure record", "reason list"],
            "blocked_actions": ["restore barrier write", "runtime apply", "rollback execution"],
            "next_state": "EXECUTION_BLOCKED",
        },
        {
            "state": "PACKET_APPROVED",
            "condition": "dual approval, valid ttl, matching generation and rollback manifest",
            "decision": "create restore-barrier clearance only",
            "action": "write generation-bound restore-barrier clearance",
            "executor": CANONICAL_PACKET_OWNER,
            "trigger": "approved packet runtime action",
            "evidence": ["restore barrier clearance", "rollback binding", "execution readiness closure"],
            "blocked_actions": ["direct user-switch", "apply without fresh recheck"],
            "next_state": "EXECUTION_READY",
        },
        {
            "state": "PACKET_EXECUTED",
            "condition": "fresh recheck passes and governed apply succeeds",
            "decision": "verify and close execution",
            "action": "write audit, outcome, trust input, prediction input and recommendation quality input",
            "executor": CANONICAL_RUNTIME_EXECUTOR,
            "trigger": "separate approved governed apply invocation",
            "evidence": ["apply result", "verification result", "audit", "closure"],
            "blocked_actions": ["replay apply", "unbounded batch continuation"],
            "next_state": "EXECUTION_SUCCESS",
        },
    ]


def execution_recheck_policy() -> dict[str, Any]:
    return {
        "schema_version": "v7.execution-recheck-policy.v1",
        "immediate_before_execution": [
            "production_truth",
            "snapshot_gate",
            "current_channel",
            "target_channel",
            "health",
            "capacity",
            "prediction",
            "trust",
            "restore_barrier",
            "rollback_packet",
        ],
        "if_any_mismatch": "STOP_EXECUTION",
        "evidence": ["truth check", "snapshot hashes", "selected move hash", "rollback packet hash"],
        "runtime_mutation_before_pass": False,
    }


def governed_apply_policy() -> dict[str, Any]:
    return {
        "schema_version": "v7.governed-apply-policy.v1",
        "executor": CANONICAL_RUNTIME_EXECUTOR,
        "who_may_invoke": ["approved operator execution owner", "future bounded autonomy via same owner only"],
        "required_before_invoke": [
            "approval packet valid",
            "restore barrier clearance active",
            "rollback packet bound",
            "fresh execution-time recheck PASS",
            "audit path available",
            "closure path available",
        ],
        "blocks_execution": [
            "missing packet",
            "expired packet",
            "stale production truth",
            "snapshot mismatch",
            "current channel mismatch",
            "capacity or health blocker",
            "trust or prediction blocker",
            "restore barrier mismatch",
            "rollback packet missing",
            "direct user-switch attempt",
        ],
    }


def verification_policy() -> dict[str, Any]:
    return {
        "schema_version": "v7.execution-verification-policy.v1",
        "verify_after_execution": [
            "channel_changed",
            "route_healthy",
            "services_healthy",
            "risk_acceptable",
            "prediction_outcome",
            "trust_impact",
        ],
        "results": {
            "success": "write success audit, closure, trust positive input, prediction quality input",
            "partial_success": "stop further moves, write partial audit, require operator review",
            "failure": "write failure audit and evaluate rollback_required",
            "rollback_required": "enter ROLLBACK_REQUIRED and execute rollback policy only",
        },
    }


def rollback_policy() -> dict[str, Any]:
    return {
        "schema_version": "v7.rollback-policy.v1",
        "rollback_trigger": ["verification failure", "partial execution outside tolerance", "operator stop", "service health regression"],
        "rollback_authority": CANONICAL_PACKET_OWNER,
        "rollback_executor": CANONICAL_ROLLBACK_EXECUTOR,
        "required_before_rollback": ["rollback packet valid", "rollback target still known", "audit path available"],
        "verification": ["channel restored", "route healthy", "services recovered", "closure written"],
        "blocked_actions": ["ad hoc v7-user-switch rollback", "rollback without packet", "second rollback owner"],
    }


def execution_action_matrix() -> list[dict[str, Any]]:
    rows = {
        "EXECUTION_READY": ("approved packet and fresh recheck pass", "execute or wait", "invoke governed apply only", CANONICAL_RUNTIME_EXECUTOR, "operator approved apply", "readiness closure", ["direct user-switch"], "EXECUTION_RUNNING"),
        "EXECUTION_BLOCKED": ("any required gate unknown or failed", "stop", "write denial/closure and surface blockers", CANONICAL_PACKET_OWNER, "gate failure", "denial audit", ["apply", "direct user-switch"], "PACKET_REJECTED"),
        "EXECUTION_RUNNING": ("governed apply started", "monitor", "collect runtime result and verification data", CANONICAL_RUNTIME_EXECUTOR, "apply process active", "apply log", ["second apply", "new packet"], "EXECUTION_SUCCESS"),
        "EXECUTION_SUCCESS": ("movement verified and services healthy", "close success", "write audit, closure, trust and prediction inputs", CANONICAL_PACKET_OWNER, "verification pass", "success closure", ["rollback unless new incident"], "CLOSED"),
        "EXECUTION_PARTIAL": ("some moves verified and some uncertain", "contain", "stop remaining moves and require operator review", CANONICAL_PACKET_OWNER, "verification partial", "partial audit", ["continue batch"], "ROLLBACK_REQUIRED"),
        "EXECUTION_FAILED": ("apply failed or verification failed", "evaluate rollback", "write failure audit and bind rollback packet", CANONICAL_PACKET_OWNER, "verification failure", "failure audit", ["new apply"], "ROLLBACK_REQUIRED"),
        "ROLLBACK_REQUIRED": ("rollback trigger true", "rollback", "validate rollback packet", CANONICAL_PACKET_OWNER, "rollback decision", "rollback readiness", ["ad hoc rollback"], "ROLLBACK_RUNNING"),
        "ROLLBACK_RUNNING": ("rollback packet executing", "monitor", "run governed rollback executor and verify", CANONICAL_ROLLBACK_EXECUTOR, "approved rollback", "rollback log", ["forward apply"], "ROLLBACK_SUCCESS"),
        "ROLLBACK_SUCCESS": ("rollback verified", "close rollback", "write rollback success audit and closure", CANONICAL_PACKET_OWNER, "rollback verification pass", "rollback closure", ["replay rollback"], "CLOSED"),
        "ROLLBACK_FAILED": ("rollback failed or unverifiable", "escalate", "write blocker, freeze further movement and require manual incident handling", CANONICAL_PACKET_OWNER, "rollback verification failure", "incident blocker", ["all future apply"], "BLOCKER"),
    }
    keys = ["condition", "decision", "action", "executor", "trigger", "written_evidence", "blocked_actions", "next_state"]
    return [{"state": state, **dict(zip(keys, values))} for state, values in rows.items()]


def audit_closure_certification() -> dict[str, Any]:
    return {
        "schema_version": "v7.audit-closure-certification.v1",
        "required_for_every_state": ["audit", "evidence", "closure", "outcome", "trust input", "prediction input", "recommendation quality input"],
        "certified_existing_writers": [CANONICAL_PACKET_OWNER, "admin/v7-admin-api audit_admin for blocked attempts"],
        "gap": "final runtime apply outcome must append trust/prediction/recommendation quality records when governed apply is enabled",
    }


def batch_execution_governance_model() -> dict[str, Any]:
    return {
        "schema_version": "v7.batch-execution-governance-model.v1",
        "batch_preview": "read-only from operator decision surface",
        "blast_radius": "must be bounded by packet selected_move_budget",
        "approval": "dual approval required",
        "execution": "same governed apply path, no batch-specific executor",
        "verification": "per-user and aggregate verification",
        "rollback": "operation-scoped rollback packet for every selected move",
        "audit": "one operation audit plus per-user evidence",
        "closure": "success, partial, failure, or rollback closure",
        "execution_allowed_now": False,
    }


def autonomy_execution_integration_model() -> dict[str, Any]:
    return {
        "schema_version": "v7.autonomy-execution-integration-model.v1",
        "required_answer": "Autonomy must call existing governed execution path.",
        "forbidden": "Autonomy must not create a second execution system.",
        "integration": [
            "autonomy may produce recommendation candidates only",
            "same approval packet schema",
            "same execution-time recheck",
            "same restore barrier",
            "same rollback packet",
            "same governed apply",
            "same audit and closure",
        ],
    }


def direct_user_switch_blocker(user: str, target: str, actor: str = "") -> dict[str, Any]:
    return {
        "action": "user_switch",
        "status": "blocked",
        "error": "governed_execution_pipeline_required",
        "message": "Direct user movement is disabled. Use recommendation approval packet and governed apply.",
        "user": user,
        "target": target,
        "actor": actor,
        "execution_allowed_now": False,
        "runtime_mutation_performed": False,
        "users_moved": False,
        "autoswitch_apply_run": False,
        "required_path": [
            "recommendation",
            "approval_packet",
            "execution_time_recheck",
            "restore_barrier",
            "rollback_packet",
            "governance",
            "v7-users-autoswitch --apply --verify",
            "verification",
            "audit",
            "closure",
        ],
    }


def execution_chain_audit() -> list[dict[str, Any]]:
    return [
        {
            "stage": row["stage"],
            "owner": row["owner"],
            "inputs": list(row["inputs"]),
            "outputs": list(row["outputs"]),
            "dependencies": [
                "production truth",
                "authority state",
                "snapshot freshness",
                "audit path",
                "closure path",
            ],
            "manual_operator_action_required": bool(row["manual"]),
            "runtime_mutation": row["runtime_mutation"],
            "timing_metric": row["timing_metric"],
            "reuse_existing_owner": True,
            "create_parallel_system": False,
        }
        for row in EXECUTION_LOOP_STAGES
    ]


def execution_loop_mapping() -> dict[str, Any]:
    manual = [row["stage"] for row in EXECUTION_LOOP_STAGES if row["manual"]]
    automated = [row["stage"] for row in EXECUTION_LOOP_STAGES if not row["manual"]]
    return {
        "schema_version": "v7.execution-loop-mapping.v1",
        "already_exists": {
            "planner": CANONICAL_PLANNER,
            "packet": CANONICAL_PACKET_TOOL,
            "restore_barrier": CANONICAL_PACKET_OWNER,
            "apply": CANONICAL_RUNTIME_EXECUTOR,
            "verify": CANONICAL_RUNTIME_EXECUTOR,
            "feedback": CANONICAL_FEEDBACK_OWNER,
            "closure": CANONICAL_FEEDBACK_OWNER,
            "observability": CANONICAL_OBSERVABILITY_OWNER,
        },
        "already_loops": [
            "planner dry-run can be repeated",
            "snapshot refresh can be repeated before planner",
            "truth/convergence checks can be repeated before runtime action",
            "feedback snapshots can be refreshed after materialization",
        ],
        "still_manual": manual,
        "operator_actions_required": [
            "select or review candidate set",
            "approve packet",
            "confirm restore-barrier clearance",
            "explicitly invoke governed apply when separately approved",
            "review rollback or failure states",
        ],
        "safe_to_automate_now": automated,
        "not_automated_by_this_foundation": manual,
        "single_execution_path": True,
    }


def execution_performance_foundation(
    *,
    contracts: list[dict[str, Any]] | None = None,
    events: list[dict[str, Any]] | None = None,
    planner_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    contracts = contracts if isinstance(contracts, list) else []
    events = events if isinstance(events, list) else []
    planner_result = planner_result if isinstance(planner_result, dict) else {}
    metrics: dict[str, float | None] = {key: None for key in REQUESTED_EXECUTION_TIMING_METRICS}
    sources: dict[str, list[str]] = {key: [] for key in REQUESTED_EXECUTION_TIMING_METRICS}

    planner_duration = _duration_ms_from_row(planner_result)
    if planner_duration is not None:
        metrics["planner_duration_ms"] = planner_duration
        sources["planner_duration_ms"].append("planner_result")

    for row in contracts + events:
        if not isinstance(row, dict):
            continue
        stage = _stage_from_row(row)
        metric = _stage_metric(stage)
        if metric not in metrics:
            continue
        duration = _duration_ms_from_row(row)
        if duration is None:
            continue
        existing = metrics.get(metric)
        metrics[metric] = duration if existing is None else round(max(float(existing), duration), 3)
        sources[metric].append(str(row.get("event_id") or row.get("contract_id") or row.get("stage") or row.get("event_type") or "row"))

    known_stage_values = [
        float(value)
        for key, value in metrics.items()
        if key.endswith("_duration_ms") and key not in {"total_duration_ms", "per_user_duration_ms"} and value is not None
    ]
    if known_stage_values:
        metrics["total_duration_ms"] = round(sum(known_stage_values), 3)
        sources["total_duration_ms"].append("sum_known_stage_durations")

    user_counts = []
    for row in contracts:
        if not isinstance(row, dict):
            continue
        affected = row.get("affected_users")
        if isinstance(affected, list):
            user_counts.append(len(affected))
        elif row.get("selected_move_count") is not None:
            user_counts.append(_as_int(row.get("selected_move_count"), 0))
    selected_moves = planner_result.get("selected_moves")
    if isinstance(selected_moves, list):
        user_counts.append(len(selected_moves))
    elif planner_result.get("operation"):
        user_counts.append(_as_int((planner_result.get("operation") or {}).get("selected_move_count"), 0))
    users = max(user_counts or [0])
    if metrics["total_duration_ms"] is not None and users > 0:
        metrics["per_user_duration_ms"] = round(float(metrics["total_duration_ms"]) / users, 3)
        sources["per_user_duration_ms"].append("total_duration_ms/affected_users")

    visibility = {
        key: {
            "available": metrics[key] is not None,
            "value": metrics[key],
            "sources": sources[key],
        }
        for key in REQUESTED_EXECUTION_TIMING_METRICS
    }
    missing = [key for key, item in visibility.items() if not item["available"]]
    return {
        "schema_version": "v7.execution-performance-foundation.v1",
        "read_only": True,
        "preview_only": True,
        "execution_allowed_now": False,
        "requested_metrics": visibility,
        "available_metrics": [key for key in REQUESTED_EXECUTION_TIMING_METRICS if key not in missing],
        "missing_metrics": missing,
        "contracts_observed": len(contracts),
        "events_observed": len(events),
        "latency_foundation_present": True,
        "latency_collection_writes_runtime_state": False,
        "next_collection_owner": CANONICAL_OBSERVABILITY_OWNER,
    }


def execution_loop_observability_model(performance: dict[str, Any]) -> dict[str, Any]:
    missing = performance.get("missing_metrics") or []
    return {
        "schema_version": "v7.execution-loop-observability.v1",
        "operator_should_see": [
            "current execution stage",
            "blocked stage",
            "last execution verdict",
            "stage duration",
            "total duration",
            "per-user duration",
            "success rate",
            "rollback rate",
            "readiness blockers",
            "owner for next action",
        ],
        "available_now": [
            "single execution path",
            "owner map",
            "readiness gates",
            "contract/event store consistency",
            "rollback readiness",
            "trust/recommendation feedback contracts",
            "duration field extraction",
        ],
        "still_missing": missing,
        "read_only": True,
        "execution_allowed_now": False,
    }


def execution_loop_safety_model() -> dict[str, Any]:
    return {
        "schema_version": "v7.execution-loop-safety-model.v1",
        "authority_boundaries": ["current authority budget", "approved packet budget", "runtime action guard"],
        "blast_radius_boundaries": ["selected_move_count", "allowed_users", "allowed_targets", "rollback_manifest_count"],
        "approval_boundaries": ["dual confirmation", "packet ttl", "selected_move_hash", "source_bundle_hash"],
        "rollback_boundaries": ["rollback packet required", "rollback target required", "verification before closure"],
        "trust_boundaries": ["trust is advisory", "planner/governance remain authoritative", "hard service gaps dominate trust"],
        "forbidden": [
            "automatic execution",
            "direct user switch",
            "apply without packet",
            "apply without restore barrier",
            "second planner",
            "second truth source",
            "second execution path",
        ],
    }


def execution_readiness_gap_analysis(performance: dict[str, Any]) -> list[dict[str, Any]]:
    gaps = [
        {
            "gap": "manual_approval_packet_generation",
            "severity": "expected_governance_boundary",
            "owner": CANONICAL_PACKET_TOOL,
            "safe_action": "keep manual until permanent loop owner is approved",
        },
        {
            "gap": "manual_governed_apply_invocation",
            "severity": "expected_governance_boundary",
            "owner": CANONICAL_RUNTIME_EXECUTOR,
            "safe_action": "do not automate apply in readiness foundation",
        },
    ]
    for metric in performance.get("missing_metrics") or []:
        gaps.append({
            "gap": f"missing_{metric}",
            "severity": "observability_gap",
            "owner": CANONICAL_OBSERVABILITY_OWNER,
            "safe_action": "collect from existing contract/event/planner fields when executions occur",
        })
    return gaps


def execution_loop_design(performance: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "v7.permanent-governed-execution-loop-design.v1",
        "chain": ["planner", "packet", "restore_barrier", "apply", "verification", "feedback", "closure"],
        "what_becomes_automatic": [
            "readiness summary",
            "stage owner map",
            "duration extraction from existing evidence",
            "blocked-stage explanation",
        ],
        "what_remains_manual": [
            "operator approval",
            "restore-barrier clearance approval",
            "governed apply invocation",
            "rollback decision when verification fails",
        ],
        "what_remains_governed": [
            "authority budget",
            "selected move hash",
            "approved plan lock",
            "restore barrier",
            "rollback manifest",
            "audit closure",
        ],
        "runtime_execution_added": False,
        "autonomy_enabled": False,
        "latency_foundation": performance,
    }


def execution_loop_readiness_foundation(
    *,
    contracts: list[dict[str, Any]] | None = None,
    events: list[dict[str, Any]] | None = None,
    planner_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    performance = execution_performance_foundation(
        contracts=contracts,
        events=events,
        planner_result=planner_result,
    )
    gaps = execution_readiness_gap_analysis(performance)
    hard_blockers = [
        row["gap"]
        for row in gaps
        if row.get("severity") not in {"expected_governance_boundary", "observability_gap"}
    ]
    return {
        "schema_version": "v7.governed-execution-loop-readiness-foundation.v1",
        "preview_only": True,
        "read_only": True,
        "execution_allowed_now": False,
        "runtime_execution_changes": False,
        "routing_behavior_changed": False,
        "users_moved": 0,
        "apply_executed": False,
        "autonomy_enabled": False,
        "execution_chain_audit": execution_chain_audit(),
        "execution_loop_mapping": execution_loop_mapping(),
        "readiness_gap_analysis": gaps,
        "performance_audit": performance,
        "execution_latency_foundation": {
            "complete": True,
            "method": "read existing planner, contract and event duration fields",
            "writes_runtime_state": False,
            "creates_truth_source": False,
        },
        "observability_review": execution_loop_observability_model(performance),
        "execution_loop_safety_model": execution_loop_safety_model(),
        "execution_loop_design": execution_loop_design(performance),
        "readiness_certification": {
            "execution_loop_ready": not hard_blockers,
            "single_blocker": hard_blockers[0] if hard_blockers else "NONE",
            "meaning": "Ready for a permanent governed execution loop foundation; automatic execution remains disabled.",
            "safe_next_step": "IMPLEMENT_GOVERNED_EXECUTION_LOOP_OPERATOR_DASHBOARD",
        },
    }


def pipeline_certification() -> dict[str, Any]:
    matrix = execution_action_matrix()
    loop = execution_loop_readiness_foundation()
    return {
        "schema_version": SCHEMA_VERSION,
        "single_execution_path": {
            "planner": CANONICAL_PLANNER,
            "approval_packet": CANONICAL_PACKET_TOOL,
            "packet_owner": CANONICAL_PACKET_OWNER,
            "runtime_apply": CANONICAL_RUNTIME_EXECUTOR,
            "rollback": CANONICAL_ROLLBACK_EXECUTOR,
            "direct_user_switch_allowed": False,
        },
        "recommendation_execution_contract": REQUIRED_RECOMMENDATION_FIELDS,
        "approval_packet_lifecycle": approval_packet_lifecycle(),
        "execution_recheck_policy": execution_recheck_policy(),
        "governed_apply_policy": governed_apply_policy(),
        "verification_policy": verification_policy(),
        "rollback_policy": rollback_policy(),
        "execution_action_matrix": matrix,
        "audit_closure_certification": audit_closure_certification(),
        "batch_execution_governance_model": batch_execution_governance_model(),
        "autonomy_execution_integration_model": autonomy_execution_integration_model(),
        "execution_loop_readiness_foundation": loop,
        "duplication_audit": {
            "second_execution_path_created": False,
            "second_planner_created": False,
            "second_governance_created": False,
            "second_rollback_created": False,
            "second_approval_system_created": False,
            "second_truth_source_created": False,
        },
        "final_verdicts": {
            "single_execution_path_certified": True,
            "recommendation_execution_contract_defined": True,
            "approval_packet_lifecycle_defined": True,
            "execution_recheck_defined": True,
            "governed_apply_policy_defined": True,
            "verification_policy_defined": True,
            "rollback_policy_defined": True,
            "execution_action_matrix_complete": all(
                all(key in row and row[key] not in ("", [], None) for key in [
                    "condition",
                    "decision",
                    "action",
                    "executor",
                    "trigger",
                    "written_evidence",
                    "blocked_actions",
                    "next_state",
                ])
                for row in matrix
            ),
            "audit_closure_certified": True,
            "operator_approval_ready": False,
            "bounded_autonomy_ready": False,
            "production_autonomy_ready": False,
            "execution_loop_readiness_foundation_complete": True,
            "execution_loop_ready": loop["readiness_certification"]["execution_loop_ready"],
            "new_truth_sources_created": False,
            "duplicate_systems_created": False,
            "runtime_mutation_performed": False,
            "users_moved": False,
            "autoswitch_apply_run": False,
            "SAFE_NEXT_STEP": "implement_operator_packet_creation_ui_and_final_apply_outcome_feedback",
        },
    }
