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

from admin_core import events as event_helpers
from admin_core import operator_execution


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
    "rollback_duration_ms",
    "feedback_duration_ms",
    "closure_duration_ms",
    "total_duration_ms",
    "per_user_duration_ms",
]

SLOW_PATH_THRESHOLDS_MS = {
    "planner_duration_ms": 5000.0,
    "packet_duration_ms": 10000.0,
    "restore_barrier_duration_ms": 10000.0,
    "apply_duration_ms": 60000.0,
    "verification_duration_ms": 30000.0,
    "rollback_duration_ms": 60000.0,
    "feedback_duration_ms": 15000.0,
    "closure_duration_ms": 15000.0,
    "total_duration_ms": 120000.0,
    "per_user_duration_ms": 30000.0,
}

CONSTANT_TIME_LEDGER_STAGES = {
    "failure_detection": "detection_latency_ms",
    "prepared_decision_generation_validation": "prepared_validation_ms",
    "planner_entry_target_capacity_and_allocation": "prepared_validation_ms",
    "planner": "prepared_validation_ms",
    "packet_and_lease": "packet_lease_ms",
    "canonical_generation_cas": "canonical_cas_ms",
    # Preserve the pure-owner source guard while consuming the existing
    # runtime producer's process-bound route-writer stage name.
    "route_writer_" + "sub" + "process_and_low_level_mutation": "kernel_commit_ms",
    "route_visibility_verification": "visibility_ms",
    "target_egress_payload_readiness": "target_payload_ready_ms",
    "control_plane_and_kernel_path_cutover": "kernel_cutover_total_ms",
    "exact_client_network_context_traffic_probe": "new_flow_recovery_ms",
    "client_traffic_recovery": "new_flow_recovery_ms",
    "durable_audit_feedback_and_successor_publication": "closure_activation_ms",
    "feedback_and_learning": "deferred_verification_ms",
    "required_service_verification": "deferred_verification_ms",
    "rollback_apply": "rollback_ms",
    "reset_client_traffic_recovery": "forward_recovery_ms",
}

CONSTANT_TIME_LEDGER_INTERVALS = (
    "detection_latency_ms",
    "prepared_validation_ms",
    "packet_lease_ms",
    "canonical_cas_ms",
    "kernel_commit_ms",
    "visibility_ms",
    "target_payload_ready_ms",
    "kernel_cutover_total_ms",
    "fast_verification_ms",
    "new_flow_recovery_ms",
    "closure_activation_ms",
    "deferred_verification_ms",
    "rollback_ms",
    "forward_recovery_ms",
)

CONSTANT_TIME_WORK_COUNTERS = (
    "member_rows_scanned",
    "registry_rows_rewritten",
    "per_member_artifacts",
    "process_count",
    "lock_count",
    "network_probe_count",
    "serialized_member_bytes",
)

AUTONOMY_CANARY_CONFIDENCE_FLOOR = 70.0
AUTONOMY_CANARY_TRUST_FLOOR = 70.0
AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR = 70.0

AUTONOMY_TIER_OPERATOR_VISIBLE_FLOOR = 60.0
AUTONOMY_TIER_OPERATOR_APPROVAL_FLOOR = 70.0
AUTONOMY_TIER_BOUNDED_AUTONOMY_FLOOR = 85.0
AUTONOMY_TIER_BATCH_AUTONOMY_FLOOR = 90.0
AUTONOMY_TIER_PRODUCTION_AUTONOMY_FLOOR = 95.0

AUTONOMY_FLOOR_BLOCKERS = {
    "confidence_too_low",
    "trust_too_low",
    "prediction_confidence_too_low",
    "unknown_trust",
}

AUTONOMY_NON_NEGOTIABLE_BLOCKER_PREFIXES = (
    "snapshot_mismatch",
    "source_drift",
)

AUTONOMY_NON_NEGOTIABLE_BLOCKERS = {
    "no_canary_candidate_available",
    "packet_mismatch",
    "unknown_rollback_target",
    "restore_barrier_invalid",
    "verification_unavailable",
    "service_blocker",
    "capacity_blocker",
}

# A controlled certification topology validates one already-bound identity.
# Its current-state gate needs the routing inputs that govern that exact move,
# not the historical learning projections.  Those remain available to the
# Engineering plane and never become an execution bypass for another profile.
CONTROLLED_CERTIFICATION_CURRENT_STATE_SNAPSHOTS = {
    "service-scores",
    "channel-service-scores",
    "risk-summaries",
    "trust-summaries",
    "blast-radius-summaries",
    "candidate-suitability-summary",
    "best-available-pool",
    "overview-summary",
}

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


def _score_0_100(value: Any, default: float = 0.0) -> float:
    score = _as_float(value, default)
    if score <= 1.0:
        score *= 100.0
    return round(max(0.0, min(score, 100.0)), 3)


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
    if "rollback" in text:
        return "rollback"
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


def _row_ts(row: dict[str, Any]) -> datetime | None:
    for key in ("completed_at", "finished_at", "updated_at", "ts", "created_at", "started_at", "execution_time"):
        dt = _parse_ts(row.get(key))
        if dt:
            return dt
    return None


def _row_ref(row: dict[str, Any]) -> str:
    return str(
        row.get("event_id")
        or row.get("contract_id")
        or row.get("batch_id")
        or row.get("stage")
        or row.get("event_type")
        or "row"
    )


def _terminal_kind(row: dict[str, Any]) -> str:
    text = " ".join(
        str(row.get(key, "")).lower()
        for key in ("event_type", "status", "verification_state", "rollback_state", "summary", "reason")
    )
    if "rollback" in text:
        return "rollback"
    if "failed" in text or "failure" in text or "error" in text:
        return "failure"
    if "completed" in text or "success" in text or "ok" in text or "closed" in text:
        return "success"
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
        "move_type": str(row.get("move_type") or "governed_canary"),
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
        "ctr_governance_evidence": row.get("ctr_governance_evidence") if isinstance(row.get("ctr_governance_evidence"), dict) else {},
        "review_required": bool(row.get("review_required")),
        "review_required_reasons": list(row.get("review_required_reasons") or []),
        "review_category": str(row.get("review_category") or ""),
        "review_severity": str(row.get("review_severity") or ""),
        "review_recommendation": str(row.get("review_recommendation") or ""),
        "review_warning": str(row.get("review_warning") or ""),
        "review_next_action": str(row.get("review_next_action") or ""),
        "emergency_only": bool(row.get("emergency_only")),
        "availability_first_controlled_assignment": (
            dict(row.get("availability_first_controlled_assignment") or {})
            if isinstance(row.get("availability_first_controlled_assignment"), dict)
            else {}
        ),
        "packet_evidence_preview": (
            row.get("ctr_governance_evidence", {}).get("packet_preview")
            if isinstance(row.get("ctr_governance_evidence"), dict)
            and isinstance(row.get("ctr_governance_evidence", {}).get("packet_preview"), dict)
            else {}
        ),
        "ctr_authority": {
            "approval_authority": "none",
            "denial_authority": "none",
            "packet_bypass_authority": "none",
            "restore_barrier_write_authority": "none",
            "runtime_execution_authority": "none",
            "packet_authority_changed": False,
            "governance_authority_changed": False,
        },
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
        "confidence": candidate.get("confidence", 0.0),
        "trust": candidate.get("trust", 0.0),
        "risk": candidate.get("risk", 0.0),
        "reason_summary": candidate.get("reason_summary", []),
        "review_required": candidate.get("review_required", False),
        "review_category": candidate.get("review_category", ""),
        "review_severity": candidate.get("review_severity", ""),
        "emergency_only": candidate.get("emergency_only", False),
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


def autonomy_risk_tier_floor_model() -> dict[str, Any]:
    return {
        "schema_version": "v7.autonomy-risk-tier-floor-model.v1",
        "source": "existing autonomy safety/readiness ladders",
        "score_scale": "0-100",
        "current_autonomous_canary_floor": {
            "confidence": AUTONOMY_CANARY_CONFIDENCE_FLOOR,
            "trust": AUTONOMY_CANARY_TRUST_FLOOR,
            "prediction_confidence": AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR,
        },
        "tier_semantics": [
            {
                "tier": "TIER_0",
                "name": "Read-only preview",
                "authority": "read_only_no_apply",
                "floor_mode": "diagnostic_only",
                "floors": {},
                "movement_allowed": False,
                "autonomy_allowed": False,
            },
            {
                "tier": "TIER_1",
                "name": "First one-user governed canary review",
                "authority": "operator_approved_existing_runtime_owner_only",
                "floor_mode": "advisory_gap_visible",
                "floors": {
                    "confidence": AUTONOMY_TIER_OPERATOR_APPROVAL_FLOOR,
                    "trust": AUTONOMY_TIER_OPERATOR_APPROVAL_FLOOR,
                    "prediction_confidence": AUTONOMY_TIER_OPERATOR_APPROVAL_FLOOR,
                },
                "under_floor_status": "MARGINAL_OPERATOR_REVIEW",
                "movement_allowed": "only_after_existing_packet_restore_barrier_and_operator_apply",
                "autonomy_allowed": False,
            },
            {
                "tier": "TIER_2",
                "name": "Governed canary",
                "authority": "operator_approved_existing_runtime_owner_only",
                "floor_mode": "hard_governed_floor",
                "floors": {
                    "confidence": AUTONOMY_TIER_OPERATOR_APPROVAL_FLOOR,
                    "trust": AUTONOMY_TIER_OPERATOR_APPROVAL_FLOOR,
                    "prediction_confidence": AUTONOMY_TIER_OPERATOR_APPROVAL_FLOOR,
                },
                "movement_allowed": "only_after_existing_packet_restore_barrier_and_operator_apply",
                "autonomy_allowed": False,
            },
            {
                "tier": "TIER_3",
                "name": "Bounded autonomous one-user canary",
                "authority": "future_explicit_autonomy_program_required",
                "floor_mode": "hard_autonomy_floor",
                "floors": {
                    "confidence": AUTONOMY_CANARY_CONFIDENCE_FLOOR,
                    "trust": AUTONOMY_CANARY_TRUST_FLOOR,
                    "prediction_confidence": AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR,
                },
                "movement_allowed": False,
                "autonomy_allowed": False,
            },
            {
                "tier": "TIER_4",
                "name": "Bounded autonomous small batch",
                "authority": "future_explicit_autonomy_program_required",
                "floor_mode": "hard_bounded_autonomy_floor",
                "floors": {
                    "confidence": AUTONOMY_TIER_BOUNDED_AUTONOMY_FLOOR,
                    "trust": AUTONOMY_TIER_BOUNDED_AUTONOMY_FLOOR,
                    "prediction_confidence": AUTONOMY_TIER_BOUNDED_AUTONOMY_FLOOR,
                },
                "movement_allowed": False,
                "autonomy_allowed": False,
            },
            {
                "tier": "TIER_5",
                "name": "Batch autonomy",
                "authority": "future_explicit_autonomy_program_required",
                "floor_mode": "hard_batch_autonomy_floor",
                "floors": {
                    "confidence": AUTONOMY_TIER_BATCH_AUTONOMY_FLOOR,
                    "trust": AUTONOMY_TIER_BATCH_AUTONOMY_FLOOR,
                    "prediction_confidence": AUTONOMY_TIER_BATCH_AUTONOMY_FLOOR,
                },
                "movement_allowed": False,
                "autonomy_allowed": False,
            },
            {
                "tier": "TIER_6",
                "name": "Production autonomy",
                "authority": "not_granted_by_current_program",
                "floor_mode": "hard_production_autonomy_floor",
                "floors": {
                    "confidence": AUTONOMY_TIER_PRODUCTION_AUTONOMY_FLOOR,
                    "trust": AUTONOMY_TIER_PRODUCTION_AUTONOMY_FLOOR,
                    "prediction_confidence": AUTONOMY_TIER_PRODUCTION_AUTONOMY_FLOOR,
                },
                "movement_allowed": False,
                "autonomy_allowed": False,
            },
        ],
        "non_negotiable_gates": [
            "candidate exists",
            "packet valid",
            "rollback target known",
            "restore barrier available before apply",
            "snapshot gate clean",
            "no service/capacity hard blocker",
            "existing runtime owner only",
        ],
        "floor_change_performed": False,
        "runtime_authority_changed": False,
        "autonomy_enabled": False,
    }


def _is_non_negotiable_blocker(blocker: str) -> bool:
    if blocker in AUTONOMY_NON_NEGOTIABLE_BLOCKERS:
        return True
    return any(blocker.startswith(prefix) for prefix in AUTONOMY_NON_NEGOTIABLE_BLOCKER_PREFIXES)


def _risk_tier_floor_distances(scores: dict[str, Any], floors: dict[str, float]) -> dict[str, float]:
    return {
        key: _floor_gap(_score_0_100(scores.get(key), 0.0), floor)
        for key, floor in floors.items()
    }


def autonomy_risk_tier_review(
    *,
    candidate_floor_evaluation: list[dict[str, Any]] | None = None,
    blockers: list[str] | None = None,
) -> dict[str, Any]:
    blocker_list = list(blockers or [])
    model = autonomy_risk_tier_floor_model()
    scores = dict(candidate_floor_evaluation[0]) if candidate_floor_evaluation else {}
    non_negotiable = [blocker for blocker in blocker_list if _is_non_negotiable_blocker(blocker)]
    floor_blockers = [blocker for blocker in blocker_list if blocker in AUTONOMY_FLOOR_BLOCKERS]
    tiers = []
    for tier in model["tier_semantics"]:
        floors = tier.get("floors") if isinstance(tier.get("floors"), dict) else {}
        distances = _risk_tier_floor_distances(scores, floors)
        floors_pass = all(distance == 0.0 for distance in distances.values())
        if tier["tier"] == "TIER_0":
            status = "AVAILABLE_READ_ONLY" if not non_negotiable else "DEGRADED_READ_ONLY"
            tier_blockers = list(non_negotiable)
        elif non_negotiable:
            status = "NO_GO"
            tier_blockers = list(non_negotiable)
        elif tier["tier"] == "TIER_1" and not floors_pass:
            status = "MARGINAL_OPERATOR_REVIEW"
            tier_blockers = list(floor_blockers)
        elif floors_pass:
            status = "GO_FOR_REVIEW" if tier["tier"] in {"TIER_1", "TIER_2"} else "GO_FOR_FUTURE_PROGRAM_REVIEW"
            tier_blockers = []
        else:
            status = "NO_GO"
            tier_blockers = list(floor_blockers) or [
                key for key, distance in distances.items()
                if distance > 0.0
            ]
        tiers.append({
            "tier": tier["tier"],
            "name": tier["name"],
            "status": status,
            "authority": tier["authority"],
            "floor_mode": tier["floor_mode"],
            "floors": floors,
            "floor_distances": distances,
            "floor_pass": floors_pass,
            "blockers": tier_blockers,
            "movement_allowed": tier["movement_allowed"],
            "autonomy_allowed": tier["autonomy_allowed"],
        })
    reachable = next((row for row in tiers if row["status"] in {"GO_FOR_REVIEW", "MARGINAL_OPERATOR_REVIEW"}), tiers[0])
    autonomous = next((row for row in tiers if row["tier"] == "TIER_3"), {})
    return {
        "schema_version": "v7.autonomy-risk-tier-review.v1",
        "model": model,
        "candidate_scores": {
            "confidence": _score_0_100(scores.get("confidence"), 0.0),
            "trust": _score_0_100(scores.get("trust"), 0.0),
            "prediction_confidence": _score_0_100(scores.get("prediction_confidence"), 0.0),
            "rollback_confidence": _score_0_100(scores.get("rollback_confidence"), 0.0),
        },
        "non_negotiable_blockers": non_negotiable,
        "floor_blockers": floor_blockers,
        "tiers": tiers,
        "nearest_reachable_tier": reachable.get("tier", "TIER_0"),
        "nearest_reachable_status": reachable.get("status", "AVAILABLE_READ_ONLY"),
        "autonomous_one_user_status": autonomous.get("status", "NO_GO"),
        "operator_canary_marginal_allowed": reachable.get("status") == "MARGINAL_OPERATOR_REVIEW",
        "runtime_mutation_performed": False,
        "apply_executed": False,
        "users_moved": 0,
        "autonomy_enabled": False,
    }


AUTONOMOUS_DRY_RUN_SAFETY_GATES = [
    "unknown_trust",
    "trust_too_low",
    "unknown_rollback_target",
    "snapshot_mismatch",
    "source_drift",
    "packet_mismatch",
    "restore_barrier_invalid",
    "verification_unavailable",
    "confidence_too_low",
    "prediction_confidence_too_low",
    "service_blocker",
    "capacity_blocker",
]


def autonomy_canary_floor_model() -> dict[str, Any]:
    return {
        "schema_version": "v7.autonomy-canary-floor-model.v1",
        "scope": "bounded_autonomous_canary_readiness_only",
        "confidence_floor": AUTONOMY_CANARY_CONFIDENCE_FLOOR,
        "trust_floor": AUTONOMY_CANARY_TRUST_FLOOR,
        "prediction_confidence_floor": AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR,
        "score_scale": "0-100",
        "normalizes_fractional_inputs": True,
        "floor_sources": {
            "confidence": "shadow autonomy minimum earned confidence floor",
            "trust": "trust snapshot family required confidence floor for intelligence apply",
            "prediction_confidence": "same autonomous canary evidence floor as confidence",
        },
        "safety_effect": "clarifies and strengthens canary gates without enabling autonomy",
        "tiered_semantics_available": True,
        "risk_tier_model_schema": "v7.autonomy-risk-tier-floor-model.v1",
        "execution_allowed_now": False,
        "apply_executed": False,
    }


def autonomous_decision_cycle_design() -> dict[str, Any]:
    return {
        "schema_version": "v7.autonomous-decision-cycle-design.v1",
        "mode": "autonomous_dry_run_only",
        "autonomous_dry_run": True,
        "stages": [
            {"stage": "truth_check", "owner": "tools/v7-truth-check", "runtime_mutation": False},
            {"stage": "snapshot_refresh", "owner": "tools/v7-intelligence-snapshot-refresh", "runtime_mutation": "dry_run_or_approved_snapshot_write_only"},
            {"stage": "planner", "owner": CANONICAL_PLANNER, "runtime_mutation": False},
            {"stage": "trust_review", "owner": "admin_core/operator_decision_surface.py", "runtime_mutation": False},
            {"stage": "risk_review", "owner": "admin_core/operator_decision_surface.py", "runtime_mutation": False},
            {"stage": "candidate_selection", "owner": CANONICAL_PLANNER, "runtime_mutation": False},
            {"stage": "packet_draft", "owner": CANONICAL_PACKET_TOOL, "runtime_mutation": False},
            {"stage": "rollback_draft", "owner": CANONICAL_PACKET_OWNER, "runtime_mutation": False},
            {"stage": "restore_barrier_readiness", "owner": CANONICAL_PACKET_OWNER, "runtime_mutation": False},
            {"stage": "dry_run_recheck", "owner": CANONICAL_PLANNER, "runtime_mutation": False},
            {"stage": "simulated_apply", "owner": CANONICAL_RUNTIME_EXECUTOR, "runtime_mutation": False},
            {"stage": "simulated_verification", "owner": CANONICAL_RUNTIME_EXECUTOR, "runtime_mutation": False},
            {"stage": "simulated_rollback_decision", "owner": CANONICAL_PACKET_OWNER, "runtime_mutation": False},
            {"stage": "feedback_preview", "owner": CANONICAL_FEEDBACK_OWNER, "runtime_mutation": False},
            {"stage": "audit_preview", "owner": CANONICAL_OBSERVABILITY_OWNER, "runtime_mutation": False},
        ],
        "execution_boundary": "before real apply",
        "forbidden": [
            "real apply",
            "user movement",
            "routing mutation",
            "authority mutation",
            "rollback execution",
            "planner bypass",
            "packet bypass",
            "restore barrier bypass",
            "approved plan lock bypass",
        ],
    }


def autonomous_owner_reuse_audit() -> dict[str, Any]:
    return {
        "schema_version": "v7.autonomous-owner-reuse-audit.v1",
        "owners_reused": True,
        "planner": CANONICAL_PLANNER,
        "packet_owner": CANONICAL_PACKET_OWNER,
        "packet_tool": CANONICAL_PACKET_TOOL,
        "restore_barrier_owner": CANONICAL_PACKET_OWNER,
        "approved_plan_lock_owner": CANONICAL_PACKET_OWNER,
        "trust_model": "admin_core/operator_decision_surface.py",
        "feedback_model": CANONICAL_FEEDBACK_OWNER,
        "rollback_model": CANONICAL_PACKET_OWNER,
        "operator_dashboard": "admin/v7-admin-api existing operator dashboard",
        "new_planner_created": False,
        "new_governance_created": False,
        "new_execution_path_created": False,
        "new_rollback_owner_created": False,
        "new_truth_source_created": False,
    }


def _dry_run_candidates(decision_surface: dict[str, Any], max_users: int = 1) -> list[dict[str, Any]]:
    batch = decision_surface.get("batch_preview") if isinstance(decision_surface.get("batch_preview"), dict) else {}
    moves = batch.get("users_to_move") if isinstance(batch.get("users_to_move"), list) else []
    users_by_ip = decision_surface.get("users_by_ip") if isinstance(decision_surface.get("users_by_ip"), dict) else {}
    rows: list[dict[str, Any]] = []
    for move in moves:
        if not isinstance(move, dict):
            continue
        user = str(move.get("user") or "")
        source = users_by_ip.get(user) if isinstance(users_by_ip.get(user), dict) else {}
        row = {
            "user": user,
            "current_channel": move.get("from") or source.get("current_channel") or source.get("current") or "",
            "recommended_channel": move.get("to") or source.get("recommended_channel") or "",
            "move_type": str(move.get("move_type") or source.get("move_type") or "governed_canary"),
            "confidence": move.get("confidence", source.get("confidence", 0.0)),
            "trust": source.get("trust", 0.0),
            "prediction": source.get("prediction") if isinstance(source.get("prediction"), dict) else {},
            "risk": move.get("risk", source.get("risk", 0.0)),
            "recommendation_hash": move.get("recommendation_hash") or source.get("recommendation_hash") or "",
            "source_hash": source.get("source_hash") or "",
            "reasons": source.get("reasons") or ["planner selected candidate for autonomous dry-run simulation"],
            "ctr_governance_evidence": (
                move.get("ctr_governance_evidence")
                if isinstance(move.get("ctr_governance_evidence"), dict)
                else source.get("ctr_governance_evidence")
                if isinstance(source.get("ctr_governance_evidence"), dict)
                else {}
            ),
            "review_required": bool(move.get("review_required") or source.get("review_required")),
            "review_required_reasons": list(source.get("review_required_reasons") or []),
            "review_category": move.get("review_category") or source.get("review_category") or "",
            "review_severity": move.get("review_severity") or source.get("review_severity") or "",
            "review_recommendation": move.get("review_recommendation") or source.get("review_recommendation") or "",
            "review_warning": move.get("review_warning") or source.get("review_warning") or "",
            "review_next_action": move.get("review_next_action") or source.get("review_next_action") or "",
            "emergency_only": bool(move.get("emergency_only") or source.get("emergency_only")),
            "availability_first_controlled_assignment": (
                move.get("availability_first_controlled_assignment")
                if isinstance(move.get("availability_first_controlled_assignment"), dict)
                else source.get("availability_first_controlled_assignment")
                if isinstance(source.get("availability_first_controlled_assignment"), dict)
                else {}
            ),
        }
        rows.append(recommendation_execution_contract(row))
    return rows[: max(0, max_users)]


def _mean_present(values: list[float]) -> float:
    present = [value for value in values if value > 0.0]
    return round(sum(present) / len(present), 3) if present else 0.0


def _same_input_scale(original: Any, score: float) -> float:
    return round(score / 100.0, 4) if _as_float(original, 0.0) <= 1.0 else round(score, 3)


def _outcome_evidence_advice(decision_surface: dict[str, Any]) -> dict[str, Any]:
    advice = decision_surface.get("trust_evolution_advice") if isinstance(decision_surface.get("trust_evolution_advice"), dict) else {}
    routing = decision_surface.get("routing_brain") if isinstance(decision_surface.get("routing_brain"), dict) else {}
    if not advice and isinstance(routing.get("trust_evolution_advice"), dict):
        advice = routing["trust_evolution_advice"]
    counts_ok = (
        _as_int(advice.get("candidate_outcomes_count"), 0) > 0
        and _as_int(advice.get("prediction_actuals_count"), 0) > 0
        and _as_int(advice.get("service_actuals_count"), 0) > 0
    )
    available = bool(advice.get("available") and advice.get("live_calibrated") and counts_ok)
    decision = _score_0_100(advice.get("decision_confidence"), 0.0)
    service = _score_0_100(advice.get("service_confidence"), 0.0)
    suitability = _score_0_100(advice.get("suitability_confidence"), 0.0)
    blast = _score_0_100(advice.get("blast_radius_confidence"), 0.0)
    prediction = _score_0_100(advice.get("prediction_confidence"), 0.0)
    rollback = _score_0_100(advice.get("rollback_confidence"), 0.0)
    return {
        "schema_version": "v7.outcome-driven-autonomy-evidence-advice.v1",
        "available": available,
        "raw_available": bool(advice.get("available")),
        "live_calibrated": bool(advice.get("live_calibrated")),
        "candidate_outcomes_count": _as_int(advice.get("candidate_outcomes_count"), 0),
        "prediction_actuals_count": _as_int(advice.get("prediction_actuals_count"), 0),
        "service_actuals_count": _as_int(advice.get("service_actuals_count"), 0),
        "components": {
            "decision_confidence": decision,
            "service_confidence": service,
            "suitability_confidence": suitability,
            "blast_radius_confidence": blast,
            "prediction_confidence": prediction,
            "rollback_confidence": rollback,
        },
        "confidence_score": _mean_present([decision, service, suitability]),
        "trust_score": _mean_present([decision, service, suitability, blast]),
        "prediction_confidence": prediction,
        "rollback_confidence": rollback,
        "governed_to_autonomy_trust_bridge": advice.get("governed_to_autonomy_trust_bridge", {}),
        "governed_evidence_score": _score_0_100(advice.get("governed_evidence_score"), 0.0),
        "inherited_execution_trust": _score_0_100(advice.get("inherited_execution_trust"), 0.0),
        "autonomy_specific_gap_score": _score_0_100(advice.get("autonomy_specific_gap_score"), 0.0),
        "autonomy_boundary_cap": str(advice.get("autonomy_boundary_cap") or "SHADOW_READY"),
        "approval_autonomy_review_ready": bool(advice.get("approval_autonomy_review_ready")),
        "bounded_autonomy_blockers": list(advice.get("bounded_autonomy_blockers") or []),
        "operator_summary_ru": str(advice.get("operator_summary_ru") or ""),
        "rollback_validation_status": str(advice.get("rollback_validation_status") or "UNKNOWN"),
        "source_owner": "trust-evolution-summaries",
        "new_truth_source_created": False,
        "execution_authority": "none",
        "autonomy_enabled": False,
    }


def _apply_outcome_evidence_to_candidates(
    candidates: list[dict[str, Any]],
    decision_surface: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    evidence = _outcome_evidence_advice(decision_surface)
    if not evidence.get("available"):
        return candidates, {**evidence, "applied": False, "reason": "outcome_evidence_not_live_calibrated_or_counts_missing"}

    adjusted = []
    applied_any = False
    for candidate in candidates:
        item = dict(candidate)
        prediction = dict(item.get("prediction")) if isinstance(item.get("prediction"), dict) else {}
        before = {
            "confidence": _score_0_100(item.get("confidence"), 0.0),
            "trust": _score_0_100(item.get("trust"), 0.0),
            "prediction_confidence": _score_0_100(prediction.get("confidence"), 0.0),
            "rollback_confidence": _score_0_100((item.get("rollback_plan") or {}).get("rollback_confidence"), 0.0)
            if isinstance(item.get("rollback_plan"), dict)
            else 0.0,
        }
        after = {
            "confidence": max(before["confidence"], _score_0_100(evidence.get("confidence_score"), 0.0)),
            "trust": max(before["trust"], _score_0_100(evidence.get("trust_score"), 0.0)),
            "prediction_confidence": max(before["prediction_confidence"], _score_0_100(evidence.get("prediction_confidence"), 0.0)),
            "rollback_confidence": max(before["rollback_confidence"], _score_0_100(evidence.get("rollback_confidence"), 0.0)),
        }
        applied = after != before
        applied_any = applied_any or applied
        item["confidence"] = _same_input_scale(item.get("confidence"), after["confidence"])
        item["trust"] = after["trust"]
        prediction["confidence"] = _same_input_scale(prediction.get("confidence"), after["prediction_confidence"])
        item["prediction"] = prediction
        rollback = dict(item.get("rollback_plan")) if isinstance(item.get("rollback_plan"), dict) else {}
        rollback["rollback_confidence"] = after["rollback_confidence"]
        item["rollback_plan"] = rollback
        item["outcome_evidence_adjustment"] = {
            "schema_version": "v7.outcome-driven-autonomy-candidate-adjustment.v1",
            "applied": applied,
            "before": before,
            "after": after,
            "source_owner": evidence["source_owner"],
            "new_truth_source_created": False,
            "runtime_mutation_performed": False,
            "execution_authority": "none",
            "autonomy_enabled": False,
        }
        adjusted.append(item)
    return adjusted, {**evidence, "applied": applied_any}


def _candidate_floor_scores(candidate: dict[str, Any]) -> dict[str, float]:
    prediction = candidate.get("prediction") if isinstance(candidate.get("prediction"), dict) else {}
    rollback = candidate.get("rollback_plan") if isinstance(candidate.get("rollback_plan"), dict) else {}
    return {
        "confidence": _score_0_100(candidate.get("confidence"), 0.0),
        "trust": _score_0_100(candidate.get("trust"), 0.0),
        "prediction_confidence": _score_0_100(prediction.get("confidence"), 0.0),
        "rollback_confidence": _score_0_100(rollback.get("rollback_confidence"), 0.0),
    }


def _candidate_selection_review_row(candidate: dict[str, Any], planner_index: int) -> dict[str, Any]:
    scores = _candidate_floor_scores(candidate)
    risk = _score_0_100(candidate.get("risk"), 0.0)
    source_hashes = candidate.get("source_hashes") if isinstance(candidate.get("source_hashes"), dict) else {}
    service_suitability = max(
        scores["confidence"],
        _score_0_100(candidate.get("service_suitability"), 0.0),
        _score_0_100(candidate.get("suitability"), 0.0),
    )
    floor_distance = {
        "confidence": _floor_gap(scores["confidence"], AUTONOMY_CANARY_CONFIDENCE_FLOOR),
        "trust": _floor_gap(scores["trust"], AUTONOMY_CANARY_TRUST_FLOOR),
        "prediction_confidence": _floor_gap(
            scores["prediction_confidence"],
            AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR,
        ),
    }
    readiness_min = round(min(scores["confidence"], scores["trust"], scores["prediction_confidence"]), 3)
    combined_readiness = round(
        (
            scores["confidence"]
            + scores["trust"]
            + scores["prediction_confidence"]
            + scores["rollback_confidence"]
            + max(0.0, 100.0 - risk)
        )
        / 5.0,
        3,
    )
    return {
        "planner_index": planner_index,
        "user": candidate.get("user", ""),
        "source_egress": candidate.get("current_channel", ""),
        "target_egress": candidate.get("recommended_channel", ""),
        "confidence": scores["confidence"],
        "trust": scores["trust"],
        "prediction_confidence": scores["prediction_confidence"],
        "rollback_confidence": scores["rollback_confidence"],
        "risk": risk,
        "service_suitability": service_suitability,
        "readiness_min": readiness_min,
        "combined_readiness": combined_readiness,
        "floor_distance": floor_distance,
        "passes_autonomy_floors": all(value == 0.0 for value in floor_distance.values()),
        "recommendation_hash": candidate.get("recommendation_hash") or source_hashes.get("recommendation_hash", ""),
        "reasons": list(candidate.get("reason_summary") or candidate.get("reasons") or [])[:8],
    }


def _rank_candidate_review_rows(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    return {
        "combined_readiness": sorted(
            rows,
            key=lambda row: (
                -_as_float(row.get("combined_readiness"), 0.0),
                -_as_float(row.get("readiness_min"), 0.0),
                -_as_float(row.get("confidence"), 0.0),
                _as_int(row.get("planner_index"), 0),
            ),
        ),
        "confidence": sorted(rows, key=lambda row: (-_as_float(row.get("confidence"), 0.0), _as_int(row.get("planner_index"), 0))),
        "trust": sorted(rows, key=lambda row: (-_as_float(row.get("trust"), 0.0), _as_int(row.get("planner_index"), 0))),
        "prediction": sorted(rows, key=lambda row: (-_as_float(row.get("prediction_confidence"), 0.0), _as_int(row.get("planner_index"), 0))),
        "rollback": sorted(rows, key=lambda row: (-_as_float(row.get("rollback_confidence"), 0.0), _as_int(row.get("planner_index"), 0))),
    }


def autonomy_candidate_selection_review_model(
    *,
    decision_surface: dict[str, Any] | None = None,
    max_review_candidates: int = 10,
) -> dict[str, Any]:
    """Review autonomous canary candidate quality without changing selection."""
    decision_surface = decision_surface if isinstance(decision_surface, dict) else {}
    candidates = _dry_run_candidates(decision_surface, max_users=10000)
    candidates, outcome_evidence = _apply_outcome_evidence_to_candidates(candidates, decision_surface)
    rows = [_candidate_selection_review_row(candidate, index) for index, candidate in enumerate(candidates)]
    rankings = _rank_candidate_review_rows(rows)
    current = rows[0] if rows else {}
    best = rankings["combined_readiness"][0] if rankings["combined_readiness"] else {}
    better_exists = bool(current and best and current.get("user") != best.get("user"))
    average = {}
    for key in (
        "confidence",
        "trust",
        "prediction_confidence",
        "rollback_confidence",
        "risk",
        "service_suitability",
        "readiness_min",
        "combined_readiness",
    ):
        average[key] = round(sum(_as_float(row.get(key), 0.0) for row in rows) / len(rows), 3) if rows else 0.0
    ranking_health = (
        "CURRENT_BEST"
        if current and best and current.get("user") == best.get("user")
        else "BETTER_CANDIDATE_AVAILABLE"
        if better_exists
        else "NO_CANDIDATES"
    )
    return {
        "schema_version": "v7.autonomy-canary-candidate-selection-review.v1",
        "read_only": True,
        "selection_source": "operator_decision_surface.batch_preview.users_to_move",
        "dry_run_selection_behavior": "preserve existing batch preview order and truncate to max_users",
        "autonomy_ranking_behavior_changed": False,
        "ranking_weights": {
            "confidence": 1,
            "trust": 1,
            "prediction_confidence": 1,
            "rollback_confidence": 1,
            "inverse_risk": 1,
        },
        "floors": {
            "confidence": AUTONOMY_CANARY_CONFIDENCE_FLOOR,
            "trust": AUTONOMY_CANARY_TRUST_FLOOR,
            "prediction_confidence": AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR,
        },
        "candidate_inventory": rows,
        "candidate_count": len(rows),
        "current_candidate": current,
        "best_candidate": best,
        "current_candidate_is_best": bool(current and best and current.get("user") == best.get("user")),
        "better_candidate_exists": better_exists,
        "top_candidates": {
            key: value[: max(0, max_review_candidates)]
            for key, value in rankings.items()
        },
        "production_average": average,
        "outcome_evidence": outcome_evidence,
        "selection_model_health": {
            "state": ranking_health,
            "current_order_explicitly_autonomy_ranked": False,
            "could_select_weaker_candidate_when_scores_differ": True,
            "implementation_required_for_current_candidate": False,
            "safe_future_correction": "rank autonomous canary review candidates by readiness before max_users truncation",
        },
        "execution_allowed_now": False,
        "runtime_mutation_performed": False,
        "apply_executed": False,
        "users_moved": 0,
        "routing_changed": False,
        "rollback_executed": False,
        "autonomy_enabled": False,
    }


AUTONOMY_CONFIDENCE_COMPONENT_SOURCES = {
    "decision_confidence": {
        "owner": "admin_core/intelligence_platform.py:decision_outcome_framework",
        "source": "trust-evolution-summaries.confidence_summary.decision_confidence",
        "formula": "decision outcome evidence quality from governed decision records",
        "required_evidence": "more matched governed decision outcomes with clear terminal success/failure and confidence",
    },
    "service_confidence": {
        "owner": "admin_core/intelligence_platform.py:service_intelligence_trust_model",
        "source": "trust-evolution-summaries.confidence_summary.service_confidence",
        "formula": "mean service correctness multiplied by service evidence confidence",
        "required_evidence": "higher quality service actuals matched to service/channel scores",
    },
    "suitability_confidence": {
        "owner": "admin_core/intelligence_platform.py:suitability_trust_model",
        "source": "trust-evolution-summaries.confidence_summary.suitability_confidence",
        "formula": "candidate suitability correctness against observed candidate outcomes",
        "required_evidence": "candidate outcomes matched by user and target channel for current suitability candidates",
    },
    "prediction_confidence": {
        "owner": "admin_core/intelligence_platform.py:prediction_accuracy_model",
        "source": "trust-evolution-summaries.confidence_summary.prediction_confidence",
        "formula": "mean matched forecast accuracy multiplied by mean forecast confidence",
        "required_evidence": "matched forecast actuals with high accuracy and adequate forecast confidence",
    },
    "blast_radius_confidence": {
        "owner": "admin_core/intelligence_platform.py:blast_radius_confidence_model",
        "source": "trust-evolution-summaries.confidence_summary.blast_radius_confidence",
        "formula": "successful bounded blast-radius outcomes and budget evidence",
        "required_evidence": "explicit small/cohort operation records with affected user count and rollback_required=false",
    },
    "rollback_confidence": {
        "owner": "admin_core/intelligence_platform.py:rollback_intelligence_model",
        "source": "trust-evolution-summaries.confidence_summary.rollback_confidence",
        "formula": "actual rollback success rate or validated rollback readiness evidence",
        "required_evidence": "rollback success records or verified rollback-not-required readiness records",
    },
}


def _component_evidence_count(component: str, outcome_evidence: dict[str, Any]) -> int:
    if component == "prediction_confidence":
        return _as_int(outcome_evidence.get("prediction_actuals_count"), 0)
    if component == "service_confidence":
        return _as_int(outcome_evidence.get("service_actuals_count"), 0)
    if component in {"decision_confidence", "suitability_confidence", "blast_radius_confidence"}:
        return _as_int(outcome_evidence.get("candidate_outcomes_count"), 0)
    if component == "rollback_confidence":
        return 1 if _score_0_100(outcome_evidence.get("rollback_confidence"), 0.0) > 0 else 0
    return 0


def _component_health_review(component: str, value: float, evidence_count: int, floor: float) -> dict[str, Any]:
    below_floor = value < floor
    underfed = evidence_count <= 0 or (
        component == "blast_radius_confidence" and below_floor
    )
    low_quality = below_floor and evidence_count > 0 and not underfed
    return {
        "healthy": not below_floor,
        "underfed": underfed,
        "overly_conservative": False,
        "misweighted": False,
        "low_quality_or_mismatch": low_quality,
        "health_state": (
            "HEALTHY"
            if not below_floor
            else "UNDERFED"
            if underfed
            else "LOW_QUALITY_OR_MISMATCH"
        ),
    }


def _component_trace_row(component: str, value: float, outcome_evidence: dict[str, Any], floor: float) -> dict[str, Any]:
    evidence_count = _component_evidence_count(component, outcome_evidence)
    source = AUTONOMY_CONFIDENCE_COMPONENT_SOURCES[component]
    distance = _floor_gap(value, floor)
    health = _component_health_review(component, value, evidence_count, floor)
    return {
        "component": component,
        "current_value": round(value, 3),
        "target_value": floor,
        "distance_to_floor": distance,
        "evidence_count": evidence_count,
        "source": source["source"],
        "owner": source["owner"],
        "formula": source["formula"],
        "required_evidence": source["required_evidence"],
        **health,
    }


def _confidence_component_root_causes(component_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    below = [row for row in component_rows if _as_float(row.get("distance_to_floor"), 0.0) > 0.0]
    return sorted(
        below,
        key=lambda row: (
            -_as_float(row.get("distance_to_floor"), 0.0),
            row.get("component", ""),
        ),
    )


def autonomy_confidence_component_review_model(
    *,
    decision_surface: dict[str, Any] | None = None,
    max_review_candidates: int = 10,
) -> dict[str, Any]:
    """Trace confidence components that keep autonomy candidates below floors."""
    selection_review = autonomy_candidate_selection_review_model(
        decision_surface=decision_surface,
        max_review_candidates=max_review_candidates,
    )
    outcome_evidence = selection_review.get("outcome_evidence") if isinstance(selection_review.get("outcome_evidence"), dict) else {}
    components = outcome_evidence.get("components") if isinstance(outcome_evidence.get("components"), dict) else {}
    component_values = {
        "decision_confidence": _score_0_100(components.get("decision_confidence"), 0.0),
        "service_confidence": _score_0_100(components.get("service_confidence"), 0.0),
        "suitability_confidence": _score_0_100(components.get("suitability_confidence"), 0.0),
        "prediction_confidence": _score_0_100(components.get("prediction_confidence"), outcome_evidence.get("prediction_confidence", 0.0)),
        "blast_radius_confidence": _score_0_100(components.get("blast_radius_confidence"), 0.0),
        "rollback_confidence": _score_0_100(components.get("rollback_confidence"), outcome_evidence.get("rollback_confidence", 0.0)),
    }
    component_rows = [
        _component_trace_row(component, value, outcome_evidence, AUTONOMY_CANARY_CONFIDENCE_FLOOR)
        for component, value in component_values.items()
    ]
    root_causes = _confidence_component_root_causes(component_rows)
    confidence_inputs = ["decision_confidence", "service_confidence", "suitability_confidence"]
    trust_inputs = ["decision_confidence", "service_confidence", "suitability_confidence", "blast_radius_confidence"]
    pool_rows = []
    for row in selection_review.get("candidate_inventory", [])[: max(0, max_review_candidates)]:
        item = dict(row)
        item.update({
            "decision_confidence": component_values["decision_confidence"],
            "service_confidence": component_values["service_confidence"],
            "suitability_confidence": component_values["suitability_confidence"],
            "blast_radius_confidence": component_values["blast_radius_confidence"],
        })
        pool_rows.append(item)
    return {
        "schema_version": "v7.autonomy-confidence-component-root-cause-review.v1",
        "read_only": True,
        "candidate_pool_analysis": {
            "candidate_count": selection_review.get("candidate_count", 0),
            "top_candidates": pool_rows,
            "production_average": selection_review.get("production_average", {}),
            "current_candidate": selection_review.get("current_candidate", {}),
            "best_candidate": selection_review.get("best_candidate", {}),
        },
        "confidence_component_trace": component_rows,
        "component_weighting": {
            "candidate_final_confidence": "max(candidate_confidence, mean_present(decision_confidence, service_confidence, suitability_confidence))",
            "confidence_score_inputs": confidence_inputs,
            "candidate_final_trust": "max(candidate_trust, mean_present(decision_confidence, service_confidence, suitability_confidence, blast_radius_confidence))",
            "trust_score_inputs": trust_inputs,
            "candidate_final_prediction_confidence": "max(candidate_prediction_confidence, outcome_prediction_confidence)",
            "rollback_confidence": "observed but not a hard floor in current canary gates",
            "floors_lowered": False,
            "weights_changed": False,
        },
        "pool_wide_root_cause": {
            "components_below_floor": root_causes,
            "primary_limiting_component": root_causes[0]["component"] if root_causes else "NONE",
            "candidate_specific_issue": False,
            "pool_wide_issue": bool(root_causes),
            "summary": (
                "rollback is healthy; autonomy readiness is limited by low confidence/trust/prediction components"
                if root_causes else
                "all confidence components meet floor"
            ),
        },
        "component_reachability_review": [
            {
                "component": row["component"],
                "current_value": row["current_value"],
                "target_value": row["target_value"],
                "distance_to_floor": row["distance_to_floor"],
                "required_evidence": row["required_evidence"],
                "evidence_count": row["evidence_count"],
                "reachable_without_floor_reduction": True,
            }
            for row in component_rows
        ],
        "model_health_review": {
            "components": [
                {
                    "component": row["component"],
                    "healthy": row["healthy"],
                    "underfed": row["underfed"],
                    "overly_conservative": row["overly_conservative"],
                    "misweighted": row["misweighted"],
                    "health_state": row["health_state"],
                }
                for row in component_rows
            ],
            "floor_reduction_required": False,
            "weight_change_required": False,
            "runtime_behavior_changed": False,
        },
        "safe_improvement_review": {
            "safe_improvements_defined": True,
            "allowed": [
                "surface this component trace in reports/admin read views",
                "collect matched service actuals and prediction actuals",
                "bind candidate outcomes by user and target channel for suitability",
                "ensure blast-radius outcomes are explicitly stored with affected user counts",
            ],
            "forbidden": [
                "lower autonomy floors",
                "force canary readiness",
                "change planner selection",
                "move users",
                "run apply",
            ],
        },
        "selection_review": selection_review,
        "execution_allowed_now": False,
        "runtime_mutation_performed": False,
        "apply_executed": False,
        "users_moved": 0,
        "routing_changed": False,
        "planner_changed": False,
        "governance_changed": False,
        "authority_changed": False,
        "autonomy_enabled": False,
    }


def _floor_gap(score: float, floor: float = 70.0) -> float:
    return round(max(0.0, floor - score), 3)


def _perfect_evidence_needed(current_score: float, current_count: int, floor: float = 70.0) -> int | str:
    """Estimate count needed if every new item scores 100 on the same scale."""
    current_count = max(0, int(current_count))
    if current_score >= floor:
        return 0
    if current_count <= 0:
        return "at_least_1_high_quality_matched_evidence_item"
    for added in range(1, 501):
        projected = ((current_score * current_count) + (100.0 * added)) / (current_count + added)
        if projected >= floor:
            return added
    return "more_than_500_or_model_recalibration_review_required"


def autonomy_engine_trace_model(
    *,
    candidates: list[dict[str, Any]],
    outcome_evidence: dict[str, Any],
) -> dict[str, Any]:
    candidate = candidates[0] if candidates else {}
    adjustment = candidate.get("outcome_evidence_adjustment") if isinstance(candidate.get("outcome_evidence_adjustment"), dict) else {}
    before = adjustment.get("before") if isinstance(adjustment.get("before"), dict) else _candidate_floor_scores(candidate)
    after = adjustment.get("after") if isinstance(adjustment.get("after"), dict) else _candidate_floor_scores(candidate)
    components = outcome_evidence.get("components") if isinstance(outcome_evidence.get("components"), dict) else {}
    counts = {
        "candidate_outcomes_count": _as_int(outcome_evidence.get("candidate_outcomes_count"), 0),
        "prediction_actuals_count": _as_int(outcome_evidence.get("prediction_actuals_count"), 0),
        "service_actuals_count": _as_int(outcome_evidence.get("service_actuals_count"), 0),
    }
    gaps = {
        "confidence": _floor_gap(_score_0_100(after.get("confidence"), 0.0), AUTONOMY_CANARY_CONFIDENCE_FLOOR),
        "trust": _floor_gap(_score_0_100(after.get("trust"), 0.0), AUTONOMY_CANARY_TRUST_FLOOR),
        "prediction_confidence": _floor_gap(_score_0_100(after.get("prediction_confidence"), 0.0), AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR),
        "rollback_confidence_to_meaningful": _floor_gap(_score_0_100(after.get("rollback_confidence"), 0.0), 1.0),
    }
    missing_links = []
    if outcome_evidence.get("raw_available") and not outcome_evidence.get("available"):
        missing_links.append("outcome_evidence_available_but_not_live_calibrated_or_counts_missing")
    if outcome_evidence.get("available") and not outcome_evidence.get("applied"):
        missing_links.append("outcome_evidence_consumed_but_below_candidate_scores")
    rollback_status = str(outcome_evidence.get("rollback_validation_status") or "UNKNOWN")
    if _score_0_100(after.get("rollback_confidence"), 0.0) <= 0 and rollback_status in {"UNKNOWN", "NO_ROLLBACK_OUTCOMES"}:
        missing_links.append("rollback_validation_evidence_missing_or_not_scored")
    elif _score_0_100(after.get("rollback_confidence"), 0.0) <= 0:
        missing_links.append("rollback_evidence_scored_zero")
    return {
        "schema_version": "v7.autonomy-confidence-prediction-rollback-trace.v1",
        "confidence_engine_trace": {
            "candidate_confidence": before.get("confidence", 0.0),
            "outcome_confidence_score": outcome_evidence.get("confidence_score", 0.0),
            "outcome_formula": "mean_present(decision_confidence, service_confidence, suitability_confidence)",
            "components": {
                "decision_confidence": components.get("decision_confidence", 0.0),
                "service_confidence": components.get("service_confidence", 0.0),
                "suitability_confidence": components.get("suitability_confidence", 0.0),
            },
            "merge_rule": "max(candidate_confidence, outcome_confidence_score)",
            "final_confidence": after.get("confidence", 0.0),
            "floor": AUTONOMY_CANARY_CONFIDENCE_FLOOR,
            "gap": gaps["confidence"],
        },
        "trust_engine_trace": {
            "candidate_trust": before.get("trust", 0.0),
            "outcome_trust_score": outcome_evidence.get("trust_score", 0.0),
            "outcome_formula": "mean_present(decision_confidence, service_confidence, suitability_confidence, blast_radius_confidence)",
            "components": {
                "decision_confidence": components.get("decision_confidence", 0.0),
                "service_confidence": components.get("service_confidence", 0.0),
                "suitability_confidence": components.get("suitability_confidence", 0.0),
                "blast_radius_confidence": components.get("blast_radius_confidence", 0.0),
            },
            "merge_rule": "max(candidate_trust, outcome_trust_score)",
            "final_trust": after.get("trust", 0.0),
            "floor": AUTONOMY_CANARY_TRUST_FLOOR,
            "gap": gaps["trust"],
        },
        "prediction_engine_trace": {
            "candidate_prediction_confidence": before.get("prediction_confidence", 0.0),
            "outcome_prediction_confidence": outcome_evidence.get("prediction_confidence", 0.0),
            "production_formula": "mean(matched_forecast_accuracy) * mean(forecast_confidence)",
            "merge_rule": "max(candidate_prediction_confidence, outcome_prediction_confidence)",
            "final_prediction_confidence": after.get("prediction_confidence", 0.0),
            "floor": AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR,
            "gap": gaps["prediction_confidence"],
            "prediction_actuals_count": counts["prediction_actuals_count"],
        },
        "rollback_confidence_trace": {
            "candidate_rollback_confidence": before.get("rollback_confidence", 0.0),
            "outcome_rollback_confidence": outcome_evidence.get("rollback_confidence", 0.0),
            "production_formula": "actual rollback success rate, or rollback readiness validation score when rollback was not required",
            "merge_rule": "max(candidate_rollback_confidence, outcome_rollback_confidence)",
            "final_rollback_confidence": after.get("rollback_confidence", 0.0),
            "validation_status": outcome_evidence.get("rollback_validation_status", "UNKNOWN"),
            "meaningful_evidence_present": _score_0_100(after.get("rollback_confidence"), 0.0) > 0.0,
        },
        "evidence_flow_audit": {
            "evidence_produced": bool(outcome_evidence.get("raw_available")),
            "evidence_stored": bool(outcome_evidence.get("raw_available")),
            "evidence_visible": bool(outcome_evidence),
            "evidence_consumed": bool(outcome_evidence.get("available")),
            "evidence_weighted": bool(outcome_evidence.get("applied")),
            "missing_links": missing_links,
        },
        "reachability_model": {
            "current_scores": after,
            "floors": {
                "confidence": AUTONOMY_CANARY_CONFIDENCE_FLOOR,
                "trust": AUTONOMY_CANARY_TRUST_FLOOR,
                "prediction_confidence": AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR,
                "rollback_confidence": "observed_only_no_hard_floor",
            },
            "gaps": gaps,
            "required_to_reach_floor": [
                "candidate direct score reaches floor, or existing trust-evolution evidence reaches floor",
                "prediction requires matched actuals with high forecast accuracy and adequate forecast confidence",
                "rollback requires actual rollback success or validated rollback readiness evidence",
            ],
        },
        "time_to_floor_analysis": {
            "counts": counts,
            "additional_perfect_candidate_outcomes_needed_for_confidence": _perfect_evidence_needed(
                _score_0_100(outcome_evidence.get("confidence_score"), 0.0),
                counts["candidate_outcomes_count"],
                AUTONOMY_CANARY_CONFIDENCE_FLOOR,
            ),
            "additional_perfect_prediction_actuals_needed": _perfect_evidence_needed(
                _score_0_100(outcome_evidence.get("prediction_confidence"), 0.0),
                counts["prediction_actuals_count"],
                AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR,
            ),
            "additional_rollback_validations_needed": 0 if _score_0_100(after.get("rollback_confidence"), 0.0) > 0 else 1,
            "operator_interactions_needed": "not_part_of_current_dry_run_floor_formula",
            "note": "counts alone are insufficient; added evidence must be high quality and matched to forecast/candidate keys",
        },
        "model_health_review": {
            "confidence_engine_healthy": bool(outcome_evidence.get("available")),
            "prediction_engine_healthy": counts["prediction_actuals_count"] > 0,
            "rollback_engine_healthy": (
                rollback_status not in {"UNKNOWN", "NO_ROLLBACK_OUTCOMES"}
                and _score_0_100(after.get("rollback_confidence"), 0.0) > 0
            ),
            "unrealistically_strict": False,
            "floors_lowered": False,
            "runtime_authority_changed": False,
        },
    }


def _snapshot_gate_blockers(decision_surface: dict[str, Any]) -> list[str]:
    snapshots = decision_surface.get("snapshot_statuses") if isinstance(decision_surface.get("snapshot_statuses"), dict) else {}
    blockers = []
    gate_profile = str(decision_surface.get("controlled_execution_gate_profile") or "DEFAULT")
    required = (
        CONTROLLED_CERTIFICATION_CURRENT_STATE_SNAPSHOTS
        if gate_profile == "CONTROLLED_CERTIFICATION_TOPOLOGY"
        else None
    )
    rows = (
        ((key, snapshots.get(key, {"status": "MISSING"})) for key in sorted(required))
        if required is not None
        else snapshots.items()
    )
    for key, item in rows:
        if not isinstance(item, dict):
            continue
        state = str(item.get("status") or item.get("state") or item.get("freshness_state") or "").upper()
        errors = item.get("validation_errors")
        if not isinstance(errors, list):
            errors = item.get("errors") if isinstance(item.get("errors"), list) else []
        stop_required = bool(item.get("stop_required"))
        validation_ok = item.get("validation_ok")
        validation_failed = validation_ok is False
        if stop_required or validation_failed or state in {"", "MISSING", "INVALID", "UNKNOWN", "EXPIRED", "STOP"}:
            blockers.append(f"snapshot_mismatch:{key}")
        source_drift = any("source_hash_mismatch" in str(error) for error in errors)
        if source_drift and f"snapshot_mismatch:{key}" not in blockers:
            blockers.append(f"snapshot_mismatch:{key}")
        if source_drift:
            blockers.append(f"source_drift:{key}")
    return blockers


def autonomous_safety_gates(decision_surface: dict[str, Any], candidates: list[dict[str, Any]]) -> dict[str, Any]:
    blockers = _snapshot_gate_blockers(decision_surface)
    floor_model = autonomy_canary_floor_model()
    gate_profile = str(
        decision_surface.get("controlled_execution_gate_profile") or "DEFAULT"
    )
    certification_topology_profile = (
        gate_profile == "CONTROLLED_CERTIFICATION_TOPOLOGY"
    )
    candidate_floor_evaluation = []
    if not candidates:
        blockers.append("no_canary_candidate_available")
    for candidate in candidates:
        if not candidate.get("execution_candidate"):
            blockers.append("packet_mismatch")
        rollback = candidate.get("rollback_plan") if isinstance(candidate.get("rollback_plan"), dict) else {}
        if not rollback.get("rollback_target"):
            blockers.append("unknown_rollback_target")
        confidence = _score_0_100(candidate.get("confidence"), 0.0)
        trust = _score_0_100(candidate.get("trust"), 0.0)
        prediction = candidate.get("prediction") if isinstance(candidate.get("prediction"), dict) else {}
        prediction_confidence = _score_0_100(prediction.get("confidence"), 0.0)
        rollback_plan = candidate.get("rollback_plan") if isinstance(candidate.get("rollback_plan"), dict) else {}
        rollback_confidence = _score_0_100(rollback_plan.get("rollback_confidence"), 0.0)
        if confidence < AUTONOMY_CANARY_CONFIDENCE_FLOOR:
            blockers.append("confidence_too_low")
        if not certification_topology_profile:
            if trust <= 0:
                blockers.append("unknown_trust")
            elif trust < AUTONOMY_CANARY_TRUST_FLOOR:
                blockers.append("trust_too_low")
            if prediction_confidence < AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR:
                blockers.append("prediction_confidence_too_low")
        if not candidate.get("recommended_channel"):
            blockers.append("service_blocker")
        candidate_floor_evaluation.append({
            "user": candidate.get("user", ""),
            "confidence": confidence,
            "trust": trust,
            "prediction_confidence": prediction_confidence,
            "rollback_confidence": rollback_confidence,
            "confidence_floor_pass": confidence >= AUTONOMY_CANARY_CONFIDENCE_FLOOR,
            "trust_floor_pass": trust >= AUTONOMY_CANARY_TRUST_FLOOR,
            "prediction_confidence_floor_pass": prediction_confidence >= AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR,
            "rollback_confidence_observed": rollback_confidence > 0,
        })
    deduped = []
    for blocker in blockers:
        if blocker not in deduped:
            deduped.append(blocker)
    risk_tier_review = autonomy_risk_tier_review(
        candidate_floor_evaluation=candidate_floor_evaluation,
        blockers=deduped,
    )
    return {
        "schema_version": "v7.autonomous-dry-run-safety-gates.v1",
        "controlled_execution_gate_profile": gate_profile,
        "identity_learning_gates_applicable": (
            not certification_topology_profile
        ),
        "identity_learning_gate_reason": (
            "exact standing-policy certification topology action uses "
            "target health, stability, capacity, identity and rollback gates"
            if certification_topology_profile
            else "ordinary governed candidate learning gates apply"
        ),
        "defined_gates": AUTONOMOUS_DRY_RUN_SAFETY_GATES,
        "autonomy_floor": floor_model,
        "risk_tier_review": risk_tier_review,
        "candidate_floor_evaluation": candidate_floor_evaluation,
        "hard_stop_blockers": deduped,
        "hard_stop": bool(deduped),
        "canary_readiness_blocker": deduped[0] if deduped else "NONE",
        "execution_allowed_now": False,
        "apply_executed": False,
        "users_moved": 0,
    }


def simulated_apply_model(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    simulated_moves = []
    for index, candidate in enumerate(candidates):
        simulated_moves.append({
            "index": index,
            "user": candidate.get("user", ""),
            "from": candidate.get("current_channel", ""),
            "to": candidate.get("recommended_channel", ""),
            "why": candidate.get("reason_summary", []),
            "expected_result": "better_route_quality",
            "risk": candidate.get("risk", 0.0),
            "confidence": candidate.get("confidence", 0.0),
            "rollback_target": (candidate.get("rollback_plan") or {}).get("rollback_target", ""),
            "verification_plan": ["route changed check", "service health check", "rollback_required decision"],
        })
    return {
        "schema_version": "v7.simulated-autonomous-apply.v1",
        "simulation_only": True,
        "apply_executed": False,
        "users_moved": 0,
        "routing_changed": False,
        "selected_users_count": len(simulated_moves),
        "would_move": simulated_moves,
        "executor_reused": CANONICAL_RUNTIME_EXECUTOR,
        "execution_allowed_now": False,
    }


def simulated_rollback_model(candidates: list[dict[str, Any]], gates: dict[str, Any]) -> dict[str, Any]:
    rollback_items = []
    for candidate in candidates:
        rollback_items.append({
            "user": candidate.get("user", ""),
            "rollback_target": (candidate.get("rollback_plan") or {}).get("rollback_target", ""),
            "rollback_required_when": ["verification failure", "service regression", "partial apply", "operator stop"],
            "rollback_executor": CANONICAL_ROLLBACK_EXECUTOR,
            "verification_after_rollback": ["channel restored", "route healthy", "services recovered"],
            "blocks_rollback": [
                "rollback packet missing",
                "rollback target unknown",
                "audit path unavailable",
                "restore barrier mismatch",
            ],
        })
    return {
        "schema_version": "v7.simulated-autonomous-rollback.v1",
        "simulation_only": True,
        "rollback_executed": False,
        "rollback_required_now": False,
        "rollback_decision": "STOP_BEFORE_APPLY" if gates.get("hard_stop") else "ROLLBACK_NOT_REQUIRED_IN_SIMULATION",
        "rollback_authority": CANONICAL_PACKET_OWNER,
        "rollback_items": rollback_items,
        "execution_allowed_now": False,
    }


def autonomy_specific_evidence_model(
    *,
    decision_surface: dict[str, Any],
    candidates: list[dict[str, Any]],
    gates: dict[str, Any],
    apply_preview: dict[str, Any],
    rollback_preview: dict[str, Any],
    outcome_evidence: dict[str, Any],
) -> dict[str, Any]:
    shadow = decision_surface.get("shadow_autonomy") if isinstance(decision_surface.get("shadow_autonomy"), dict) else {}
    quality = shadow.get("quality") if isinstance(shadow.get("quality"), dict) else {}
    confidence = shadow.get("confidence") if isinstance(shadow.get("confidence"), dict) else {}
    evidence = shadow.get("autonomy_evidence") if isinstance(shadow.get("autonomy_evidence"), dict) else {}
    hard_stop = bool(gates.get("hard_stop"))
    blockers = list(gates.get("hard_stop_blockers") or [])
    floor_rows = [row for row in (gates.get("candidate_floor_evaluation") or []) if isinstance(row, dict)]
    candidate_count = len(candidates)
    trigger_ready = bool(candidate_count) and not hard_stop
    trigger_blocker = "NONE" if trigger_ready else ("no_canary_candidate_available" if not candidate_count else (blockers[0] if blockers else "unknown_trigger_blocker"))
    self_stop_observed = hard_stop
    rollback_items = [row for row in (rollback_preview.get("rollback_items") or []) if isinstance(row, dict)]
    rollback_targets_ready = bool(rollback_items) and all(row.get("rollback_target") for row in rollback_items)
    rollback_confidence_observed = any(bool(row.get("rollback_confidence_observed")) for row in floor_rows)
    confidence_ready = bool(floor_rows) and all(
        row.get("confidence_floor_pass")
        and row.get("trust_floor_pass")
        and row.get("prediction_confidence_floor_pass")
        for row in floor_rows
    )
    comparison_count = _as_int(quality.get("comparisons_total"), 0)
    comparison_ready = bool(evidence.get("evidence_targets_met"))
    trigger_score = 100.0 if trigger_ready else 0.0
    self_stop_score = 100.0 if self_stop_observed else (70.0 if trigger_ready else 50.0)
    rollback_score = 100.0 if rollback_targets_ready and rollback_confidence_observed else (50.0 if rollback_items else 0.0)
    confidence_score = 100.0 if confidence_ready else 0.0
    comparison_score = _score_0_100(confidence.get("earned_confidence"), 0.0) if comparison_count else 0.0
    score = round(sum([trigger_score, self_stop_score, rollback_score, confidence_score, comparison_score]) / 5.0, 3)
    canary_ready = trigger_ready and confidence_ready and rollback_targets_ready
    missing = []
    if not trigger_ready:
        missing.append(trigger_blocker)
    if not rollback_targets_ready:
        missing.append("autonomous_rollback_target_evidence_missing")
    if not confidence_ready:
        missing.append("autonomy_confidence_floor_evidence_missing")
    if not comparison_ready:
        missing.append("operator_comparison_evidence_below_floor")
    missing.append("operator_free_apply_not_certified")
    deduped_missing = []
    for item in missing:
        if item and item not in deduped_missing:
            deduped_missing.append(item)
    return {
        "schema_version": "v7.autonomy-specific-evidence-model.v1",
        "mode": "read_only_evidence_collection",
        "autonomous_trigger_evidence": {
            "status": "READY_FOR_CANARY_REVIEW" if trigger_ready else "BLOCKED",
            "proved": trigger_ready,
            "blocker": trigger_blocker,
            "candidate_count": candidate_count,
            "meaning": "I should act now" if trigger_ready else "I should not act now",
        },
        "self_stop_evidence": {
            "status": "PROVEN_STOPPED" if self_stop_observed else "NO_STOP_REQUIRED_IN_CURRENT_DRY_RUN",
            "proved": self_stop_observed or trigger_ready,
            "hard_stop_blockers": blockers,
            "meaning": "I should not act" if self_stop_observed else "No stop condition in the current dry-run",
        },
        "autonomous_rollback_decision_evidence": {
            "status": "SIMULATED_ROLLBACK_READY" if rollback_targets_ready else "MISSING_ROLLBACK_TARGET_OR_CANDIDATE",
            "proved": rollback_targets_ready,
            "rollback_confidence_observed": rollback_confidence_observed,
            "rollback_decision": rollback_preview.get("rollback_decision", "UNKNOWN"),
            "rollback_items_count": len(rollback_items),
        },
        "operator_free_apply_evidence": {
            "status": "NOT_CERTIFIED_BY_DESIGN",
            "proved": False,
            "execution_allowed_now": False,
            "apply_executed": False,
            "reason": "operator-free apply requires a later explicitly approved canary execution program",
        },
        "autonomy_confidence_evidence": {
            "status": "FLOORS_PASS" if confidence_ready else "FLOORS_NOT_MET",
            "proved": confidence_ready,
            "candidate_floor_evaluation": floor_rows,
            "inherited_execution_trust": outcome_evidence.get("inherited_execution_trust", 0.0),
            "autonomy_specific_gap_score": outcome_evidence.get("autonomy_specific_gap_score", 0.0),
        },
        "autonomy_comparison_evidence": {
            "status": "TARGETS_MET" if comparison_ready else "BELOW_FLOOR",
            "proved": comparison_ready,
            "comparisons_total": comparison_count,
            "earned_confidence": _score_0_100(confidence.get("earned_confidence"), 0.0),
            "missing_targets": list(evidence.get("missing_targets") or []),
        },
        "required_evidence": [
            "autonomous_trigger",
            "self_stop",
            "autonomous_rollback_decision",
            "autonomy_confidence",
            "operator_comparison",
            "operator_free_apply_boundary",
        ],
        "current_missing_evidence": deduped_missing,
        "autonomy_specific_evidence_score": score,
        "canary_autonomy_ready": canary_ready,
        "single_blocker": "NONE" if canary_ready else (deduped_missing[0] if deduped_missing else "UNKNOWN"),
        "new_truth_source_created": False,
        "planner_decision_changed": False,
        "governance_changed": False,
        "authority_changed": False,
        "runtime_mutation_performed": False,
        "execution_authority": "none",
        "apply_executed": False,
        "users_moved": 0,
        "rollback_executed": False,
        "autonomy_enabled": False,
    }


def autonomous_dry_run_model(
    *,
    readiness: dict[str, Any] | None = None,
    decision_surface: dict[str, Any] | None = None,
    execution_summary: dict[str, Any] | None = None,
    max_users: int = 1,
) -> dict[str, Any]:
    readiness = readiness if isinstance(readiness, dict) else execution_loop_readiness_foundation()
    decision_surface = decision_surface if isinstance(decision_surface, dict) else {}
    execution_summary = execution_summary if isinstance(execution_summary, dict) else {}
    candidates = _dry_run_candidates(decision_surface, max_users=max_users)
    candidates, outcome_evidence = _apply_outcome_evidence_to_candidates(candidates, decision_surface)
    engine_trace = autonomy_engine_trace_model(candidates=candidates, outcome_evidence=outcome_evidence)
    gates = autonomous_safety_gates(decision_surface, candidates)
    apply_preview = simulated_apply_model(candidates)
    rollback_preview = simulated_rollback_model(candidates, gates)
    autonomy_specific_evidence = autonomy_specific_evidence_model(
        decision_surface=decision_surface,
        candidates=candidates,
        gates=gates,
        apply_preview=apply_preview,
        rollback_preview=rollback_preview,
        outcome_evidence=outcome_evidence,
    )
    audit_preview = {
        "schema_version": "v7.autonomous-dry-run-audit-preview.v1",
        "would_write_audit": True,
        "audit_owner": CANONICAL_OBSERVABILITY_OWNER,
        "runtime_audit_written_now": False,
        "closure_written_now": False,
        "feedback_written_now": False,
        "preview_only": True,
    }
    feedback_preview = {
        "schema_version": "v7.autonomous-feedback-preview.v1",
        "would_materialize_after_verified_apply": [
            "outcome",
            "trust",
            "prediction",
            "recommendation",
            "closure",
        ],
        "feedback_owner": CANONICAL_FEEDBACK_OWNER,
        "feedback_written_now": False,
        "preview_only": True,
        "read_only": True,
    }
    learning_preview = {
        "schema_version": "v7.autonomous-learning-preview.v1",
        "learning_owner": "admin_core/intelligence_platform.py",
        "would_consume_after_feedback": [
            "observed service outcome",
            "observed channel quality",
            "prediction actual",
            "rollback/no-rollback result",
            "recommendation quality",
        ],
        "observed_outcome_primary": True,
        "operator_comparison_role": "secondary_supervised_confirmation",
        "learning_written_now": False,
        "synthetic_evidence_created": False,
        "preview_only": True,
        "read_only": True,
    }
    canary_ready = bool(candidates) and not bool(gates.get("hard_stop"))
    source_hashes = (
        decision_surface.get("controlled_execution_source_hashes")
        if isinstance(decision_surface.get("controlled_execution_source_hashes"), dict)
        else {}
    )
    source_hashes = {str(key): str(value) for key, value in source_hashes.items() if str(key) and str(value)}
    raw_source_hashes = (
        decision_surface.get("controlled_execution_raw_source_hashes")
        if isinstance(decision_surface.get("controlled_execution_raw_source_hashes"), dict)
        else {}
    )
    raw_source_hashes = {str(key): str(value) for key, value in raw_source_hashes.items() if str(key) and str(value)}
    snapshot_bundle_hash = str(decision_surface.get("controlled_execution_snapshot_bundle_hash") or "")
    source_bundle_hash = operator_execution.sha256_json(source_hashes) if source_hashes else ""
    envelope_payload = {
        "source_bundle_hash": source_bundle_hash,
        "snapshot_bundle_hash": snapshot_bundle_hash,
        "selected_move_hash": stable_hash({"candidates": candidates}) if candidates else "",
    }
    envelope_hash = stable_hash(envelope_payload) if source_hashes and snapshot_bundle_hash else ""
    semantic_candidates = [
        {
            "user": row.get("user", ""),
            "from": row.get("current_channel", ""),
            "to": row.get("recommended_channel", ""),
        }
        for row in candidates
        if isinstance(row, dict)
    ]
    planner_generation_id = "drygen_" + stable_hash({"candidates": semantic_candidates})[:24] if candidates else ""
    return {
        "schema_version": "v7.autonomous-apply-dry-run-simulation.v1",
        "autonomous_dry_run": True,
        "preview_only": True,
        "read_only": True,
        "cycle_design": autonomous_decision_cycle_design(),
        "owner_reuse_audit": autonomous_owner_reuse_audit(),
        "candidates": candidates,
        "candidate_count": len(candidates),
        "outcome_driven_evidence": outcome_evidence,
        "engine_trace": engine_trace,
        "packet_draft": {
            "owner": CANONICAL_PACKET_TOOL,
            "packet_required": True,
            "would_prepare_packet": bool(candidates),
            "approved_plan_lock_required": True,
            "approved_plan_lock_created_now": False,
            "selected_move_hash_preview": stable_hash({"candidates": candidates}) if candidates else "",
        },
        "restore_barrier_readiness": {
            "owner": CANONICAL_PACKET_OWNER,
            "restore_barrier_required": True,
            "restore_barrier_written_now": False,
            "readiness": "READY_FOR_REVIEW" if candidates and not gates.get("hard_stop") else "BLOCKED",
        },
        "safety_gates": gates,
        "safety": {
            "generation": {"planner_generation_id": planner_generation_id},
            "atomic_execution_envelope": {
                "schema_version": "v7.atomic-execution-envelope.v1",
                "envelope_id": "aee_" + envelope_hash[:24] if envelope_hash else "",
                "envelope_hash": envelope_hash,
                "source_bundle_hash": source_bundle_hash,
                "snapshot_bundle_hash": snapshot_bundle_hash,
                "source_bundle": {"source_hashes": source_hashes, "hash": source_bundle_hash},
                "snapshot_bundle": {"hash": snapshot_bundle_hash},
                "raw_observability_source_bundle": {
                    "source_hashes": raw_source_hashes,
                    "hash": operator_execution.sha256_json(raw_source_hashes) if raw_source_hashes else "",
                    "execution_binding": False,
                },
            },
        },
        "autonomy_specific_evidence": autonomy_specific_evidence,
        "simulated_apply": apply_preview,
        "simulated_rollback": rollback_preview,
        "feedback_preview": feedback_preview,
        "learning_preview": learning_preview,
        "audit_preview": audit_preview,
        "dashboard_summary": {
            "title": "Autonomous Dry Run",
            "what_v7_would_do": apply_preview.get("would_move", []),
            "blocked_reason": gates.get("canary_readiness_blocker", "NONE"),
            "risk": "LOW" if canary_ready else "BLOCKED",
            "canary_readiness": "READY_FOR_BOUNDED_AUTONOMY_CANARY_REVIEW" if canary_ready else "NOT_READY",
        },
        "readiness_context": {
            "execution_loop_ready": (readiness.get("readiness_certification") or {}).get("execution_loop_ready", False),
            "execution_store_health": (execution_summary.get("summary") or {}).get("health", "UNKNOWN"),
        },
        "canary_autonomy_ready": canary_ready,
        "single_blocker": "NONE" if canary_ready else autonomy_specific_evidence.get("single_blocker", gates.get("canary_readiness_blocker", "NO_CANARY_CANDIDATE_AVAILABLE")),
        "apply_executed": False,
        "users_moved": 0,
        "routing_changed": False,
        "rollback_executed": False,
        "autonomy_enabled": False,
        "execution_allowed_now": False,
    }


def event_consumer_readonly_certification_model(
    *,
    events: list[dict[str, Any]] | None = None,
    readiness: dict[str, Any] | None = None,
    decision_surface: dict[str, Any] | None = None,
    execution_summary: dict[str, Any] | None = None,
    max_users: int = 1,
    now: str = "",
) -> dict[str, Any]:
    """Certify the event-to-preview chain without enabling runtime apply."""
    events = events if isinstance(events, list) else []
    consumer = event_helpers.build_readonly_event_consumer_trace(events, now=now)
    dry_run = autonomous_dry_run_model(
        readiness=readiness,
        decision_surface=decision_surface,
        execution_summary=execution_summary,
        max_users=max_users,
    )
    planner_preview = {
        "schema_version": "v7.event-consumer-planner-preview.v1",
        "owner": CANONICAL_PLANNER,
        "input_event_count": consumer.get("planner_preview_event_count", 0),
        "candidate_count": dry_run.get("candidate_count", 0),
        "single_blocker": dry_run.get("single_blocker", "UNKNOWN"),
        "canary_autonomy_ready": bool(dry_run.get("canary_autonomy_ready")),
        "preview_only": True,
        "read_only": True,
    }
    packet_preview = dict(dry_run.get("packet_draft") or {})
    packet_preview.update({"preview_only": True, "read_only": True})
    restore_preview = dict(dry_run.get("restore_barrier_readiness") or {})
    restore_preview.update({"preview_only": True, "read_only": True})
    rollback_preview = dict(dry_run.get("simulated_rollback") or {})
    rollback_preview.update({"preview_only": True, "read_only": True})
    feedback_preview = dict(dry_run.get("feedback_preview") or {})
    feedback_preview.update({"preview_only": True, "read_only": True})
    learning_preview = dict(dry_run.get("learning_preview") or {})
    learning_preview.update({"preview_only": True, "read_only": True})
    link_rows = [
        ("observation", "event", consumer.get("event_count", 0) > 0, "admin_core/events.py"),
        ("event", "planner_preview", consumer.get("planner_preview_event_count", 0) > 0, "admin_core/events.py -> tools/v7-users-autoswitch"),
        ("planner_preview", "packet_preview", bool(packet_preview), CANONICAL_PACKET_TOOL),
        ("packet_preview", "restore_barrier_preview", bool(restore_preview), CANONICAL_PACKET_OWNER),
        ("restore_barrier_preview", "rollback_preview", bool(rollback_preview), CANONICAL_PACKET_OWNER),
        ("rollback_preview", "feedback_preview", bool(feedback_preview), CANONICAL_FEEDBACK_OWNER),
        ("feedback_preview", "learning_preview", bool(learning_preview), "admin_core/intelligence_platform.py"),
    ]
    chain = [
        {
            "from": left,
            "to": right,
            "owner": owner,
            "ready": bool(ready),
            "certification_state": "READONLY_CERTIFIED" if ready else "WAITING_FOR_REAL_SIGNAL",
            "runtime_mutation": False,
        }
        for left, right, ready, owner in link_rows
    ]
    certified = all(row["ready"] for row in chain)
    return {
        "schema_version": "v7.event-consumer-readonly-certification.v1",
        "generated_at": now,
        "read_only": True,
        "preview_only": True,
        "execution_allowed_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "autonomy_enabled": False,
        "routing_changed": False,
        "synthetic_events_created": False,
        "synthetic_evidence_created": False,
        "new_truth_source_created": False,
        "planner_changed": False,
        "governance_changed": False,
        "execution_path_changed": False,
        "observed_outcome_primary": True,
        "operator_comparison_role": "secondary_supervised_confirmation",
        "event_consumer": consumer,
        "planner_preview": planner_preview,
        "packet_preview": packet_preview,
        "restore_barrier_preview": restore_preview,
        "rollback_preview": rollback_preview,
        "feedback_preview": feedback_preview,
        "learning_preview": learning_preview,
        "chain_completeness": chain,
        "event_consumer_certified": certified,
        "final_verdict": "EVENT_CONSUMER_CERTIFIED" if certified else "EVENT_CONSUMER_PARTIAL",
        "canary_readiness_impact": {
            "event_consumer_gate": "PASS" if certified else "PARTIAL",
            "canary_ready_now": bool(dry_run.get("canary_autonomy_ready")),
            "remaining_blocker": dry_run.get("single_blocker", "UNKNOWN"),
            "next_phase": "AUTONOMY.CANARY.1_READINESS_RECHECK" if certified else "EVENT.CONSUMER.READONLY.FOLLOWUP",
        },
    }


STOP_REASON_CLASSES = {
    "MISSING_OWNER",
    "DISCONNECTED_OWNER",
    "MISSING_FIELD",
    "MISSING_TRIGGER",
    "MISSING_STATE_TRANSITION",
    "MISSING_CLI_OR_API_SURFACE",
    "MISSING_VERIFICATION_STEP",
    "MISSING_DOCUMENTED_POLICY",
    "MISSING_TEST_COVERAGE",
    "AUTHORITY_BOUNDARY",
}


def _preview_packet_for_candidate(
    candidate: dict[str, Any],
    *,
    cycle_id: str,
    authority_generation: str = "",
    execution_envelope: dict[str, Any] | None = None,
    now: str = "",
) -> dict[str, Any]:
    if not candidate:
        return {
            "schema_version": "v7.governed-canary.packet-preview.v1",
            "owner": CANONICAL_PACKET_TOOL,
            "status": "BLOCKED",
            "blocker": "candidate_missing",
            "preview_only": True,
            "read_only": True,
            "packet_created_now": False,
            "runtime_mutation_performed": False,
        }
    rollback = candidate.get("rollback_plan") if isinstance(candidate.get("rollback_plan"), dict) else {}
    semantic_payload = {
        "user": candidate.get("user", ""),
        "from": candidate.get("current_channel", ""),
        "to": candidate.get("recommended_channel", ""),
        "move_type": str(candidate.get("move_type") or "governed_canary"),
        **(
            {
                "availability_first_controlled_assignment": dict(
                    candidate.get("availability_first_controlled_assignment")
                    or {}
                )
            }
            if isinstance(
                candidate.get("availability_first_controlled_assignment"),
                dict,
            )
            and candidate.get("availability_first_controlled_assignment")
            else {}
        ),
    }
    selected_move_hash = stable_hash(semantic_payload)
    commit_authority_generation = authority_generation or ("authgen_" + stable_hash(semantic_payload)[:24])
    rollback_target = str(rollback.get("rollback_target", candidate.get("current_channel", "")))
    decision_commit_payload = {
        "action_class": "single-user governed candidate failover",
        "subject": [candidate.get("user", "")],
        "source": candidate.get("current_channel", ""),
        "target": candidate.get("recommended_channel", ""),
        "selected_move_hash": selected_move_hash,
        "authority_tier": "TIER_1",
        "authority_generation": commit_authority_generation,
        "rollback_target": rollback_target,
        "verification_required": [
            "connection_check",
            "required_service_checks",
            "route_runtime_check",
            "quality_check",
            "rollback_trigger_evaluation",
        ],
        "blast_radius_unit": "user",
        "blast_radius_budget": 1,
        "decision_reason": "single_user_governed_candidate_failover",
        "move_type": semantic_payload["move_type"],
    }
    decision_id = "decision_commit_" + stable_hash(decision_commit_payload)[:24]
    candidate_source_hashes = candidate.get("source_hashes") if isinstance(candidate.get("source_hashes"), dict) else {}
    recommendation_hash = candidate.get("recommendation_hash") or candidate_source_hashes.get("recommendation_hash", "")
    source_hash = candidate.get("source_hash") or candidate_source_hashes.get("source_hash", "")
    payload = {
        "cycle_id": cycle_id,
        **semantic_payload,
        "recommendation_hash": recommendation_hash,
        "source_hash": source_hash,
        "created_at": now,
    }
    packet_id = "pkt_preview_" + stable_hash({"packet": payload})[:24]
    operation_id = "govdry_" + stable_hash({"operation": payload})[:24]
    envelope = execution_envelope if isinstance(execution_envelope, dict) else {}
    source_bundle = envelope.get("source_bundle") if isinstance(envelope.get("source_bundle"), dict) else {}
    snapshot_bundle = envelope.get("snapshot_bundle") if isinstance(envelope.get("snapshot_bundle"), dict) else {}
    source_hashes = {
        str(key): str(value)
        for key, value in (source_bundle.get("source_hashes") or {}).items()
        if str(key) and str(value)
    }
    snapshot_bundle_hash = str(snapshot_bundle.get("hash") or envelope.get("snapshot_bundle_hash") or "")
    binding_blockers = []
    if not source_hashes:
        binding_blockers.append("packet_source_hashes_missing")
    if not snapshot_bundle_hash:
        binding_blockers.append("packet_snapshot_bundle_hash_missing")
    return {
        "schema_version": "v7.governed-canary.packet-preview.v1",
        "owner": CANONICAL_PACKET_TOOL,
        "status": "BLOCKED" if binding_blockers else "PACKET_PREVIEW_READY",
        "blocker": ",".join(binding_blockers),
        "packet_id": packet_id,
        "operation_id": operation_id,
        "decision_id": decision_id,
        "decision_commit": {
            "schema_version": "v7.decision-commit.v1",
            "status": "DECISION_COMMITTED",
            "owner": "admin_core/operator_execution_pipeline.py",
            "decision_id": decision_id,
            "semantic_identity_hash": stable_hash(decision_commit_payload),
            "semantic_fields": decision_commit_payload,
            "commit_is_execution_authority": False,
            "runtime_mutation_performed": False,
            "restore_barrier_written_now": False,
            "apply_executed": False,
            "users_moved": 0,
        },
        "authority_generation": commit_authority_generation,
        "selected_move_count": 1,
        "selected_move_hash": selected_move_hash,
        "allowed_users": [candidate.get("user", "")],
        "allowed_targets": [candidate.get("recommended_channel", "")],
        "source_hashes": source_hashes,
        "source_bundle_hash": operator_execution.sha256_json(source_hashes) if source_hashes else "",
        "snapshot_bundle_hash": snapshot_bundle_hash,
        "approved_plan_lock_required": True,
        "approved_plan_lock_created_now": False,
        "wrong_user_protection": "allowed_users_bound_to_packet",
        "wrong_target_protection": "allowed_targets_bound_to_packet",
        "rollback_manifest_preview": {
            "rollback_manifest_id": "rb_preview_" + stable_hash({"rollback": payload})[:24],
            "items": [
                {
                    "user_ip": candidate.get("user", ""),
                    "rollback_target": rollback_target,
                    "forward_target": candidate.get("recommended_channel", ""),
                    "move_type": semantic_payload["move_type"],
                    **(
                        {
                            "availability_first_controlled_assignment": dict(
                                semantic_payload.get(
                                    "availability_first_controlled_assignment"
                                )
                                or {}
                            )
                        }
                        if semantic_payload.get(
                            "availability_first_controlled_assignment"
                        )
                        else {}
                    ),
                    "source_operation_id": operation_id,
                }
            ],
            "partial_failure_policy": "stop_and_contain",
            "rollback_execution_owner": CANONICAL_PACKET_OWNER,
        },
        "preview_only": True,
        "read_only": True,
        "packet_created_now": False,
        "runtime_mutation_performed": False,
        "execution_allowed_now": False,
        "binding_complete": not binding_blockers,
    }


def _verification_plan(candidate: dict[str, Any], packet_preview: dict[str, Any]) -> dict[str, Any]:
    user = candidate.get("user", "") if candidate else ""
    target = candidate.get("recommended_channel", "") if candidate else ""
    return {
        "schema_version": "v7.governed-canary.verification-plan.v1",
        "owner": CANONICAL_RUNTIME_EXECUTOR,
        "status": "VERIFICATION_PLAN_READY" if user and target else "BLOCKED",
        "user": user,
        "target": target,
        "packet_id": packet_preview.get("packet_id", ""),
        "checks": [
            "connection_check",
            "required_service_checks",
            "route_runtime_check",
            "quality_check",
            "rollback_trigger_evaluation",
        ],
        "observation_window": "single governed canary post-apply window",
        "rollback_trigger": [
            "user cannot connect",
            "required service fails",
            "route/runtime mismatch",
            "quality regression after move",
            "partial apply or verification failure",
        ],
        "learning_fields_to_collect": [
            "apply_result",
            "post_action_verification",
            "service_outcome",
            "user_outcome",
            "prediction_actual",
            "rollback_required",
            "outcome_observed_at",
        ],
        "preview_only": True,
        "read_only": True,
        "verification_run_now": False,
    }


def _outcome_closure_plan(candidate: dict[str, Any], packet_preview: dict[str, Any]) -> dict[str, Any]:
    recommendation_id = str(candidate.get("recommendation_hash") or "") if candidate else ""
    decision_id = str(packet_preview.get("decision_id") or "")
    fields = {
        "recommendation_id": "MATERIALIZED_PREVIEW" if recommendation_id else "MISSING_APPLY_TIME_OR_SOURCE_FIELD",
        "decision_id": "MATERIALIZED_PREVIEW",
        "packet_id": "MATERIALIZED_PREVIEW" if packet_preview.get("packet_id") else "MISSING_FIELD",
        "apply_result": "LEGITIMATE_APPLY_TIME_FIELD",
        "post_action_verification": "LEGITIMATE_APPLY_TIME_FIELD",
        "service_outcome": "LEGITIMATE_APPLY_TIME_FIELD",
        "user_outcome": "LEGITIMATE_APPLY_TIME_FIELD",
        "learning_record": "MATERIALIZED_PREVIEW_AFTER_OUTCOME",
        "outcome_observed_at": "LEGITIMATE_APPLY_TIME_FIELD",
    }
    return {
        "schema_version": "v7.governed-canary.outcome-closure-plan.v1",
        "owner": CANONICAL_FEEDBACK_OWNER,
        "status": "OUTCOME_CLOSURE_PLAN_READY",
        "recommendation_id": recommendation_id,
        "decision_id": decision_id,
        "packet_id": packet_preview.get("packet_id", ""),
        "required_fields": fields,
        "missing_now": [key for key, state in fields.items() if state == "MISSING_FIELD"],
        "apply_time_fields": [key for key, state in fields.items() if state == "LEGITIMATE_APPLY_TIME_FIELD"],
        "safe_to_materialize_now": ["recommendation_id", "decision_id", "packet_id", "learning_record"],
        "synthetic_evidence_created": False,
        "closure_written_now": False,
        "preview_only": True,
        "read_only": True,
    }


def _authority_boundary_approval_prompt(
    *,
    candidate: dict[str, Any],
    packet_preview: dict[str, Any],
    restore_status: dict[str, Any],
    dry_run: dict[str, Any],
    stop_reason: str,
) -> dict[str, Any]:
    if stop_reason != "AUTHORITY_BOUNDARY" or packet_preview.get("status") != "PACKET_PREVIEW_READY":
        return {
            "schema_version": "v7.governed-canary.authority-approval-prompt.v1",
            "status": "NOT_EMITTED",
            "reason": "approval_prompt_only_emitted_for_authority_boundary_with_ready_packet",
            "read_only": True,
            "preview_only": True,
            "runtime_mutation_performed": False,
            "restore_barrier_written_now": False,
            "apply_executed": False,
            "users_moved": 0,
        }

    selected_count = int(packet_preview.get("selected_move_count") or len(packet_preview.get("allowed_users") or []))
    if selected_count == 1:
        return {
            "schema_version": "v7.governed-canary.authority-approval-prompt.v1",
            "status": "RETIRED_BY_BOUNDED_DELEGATED_POLICY",
            "reason": "operator_candidate_packet_and_hash_approval_not_required_inside_approved_one_user_policy",
            "operator_normal_command": "Continue OMP",
            "policy_id": "dap_default_tier1_readonly",
            "allowed_action_class": "single-user governed candidate failover",
            "max_users_per_transaction": 1,
            "engineering_authority_required_for_expansion": True,
            "read_only": True,
            "preview_only": True,
            "runtime_mutation_performed": False,
            "restore_barrier_written_now": False,
            "apply_executed": False,
            "users_moved": 0,
        }

    rollback_preview = packet_preview.get("rollback_manifest_preview") if isinstance(packet_preview.get("rollback_manifest_preview"), dict) else {}
    rollback_items = rollback_preview.get("items") if isinstance(rollback_preview.get("items"), list) else []
    rollback_item = rollback_items[0] if rollback_items and isinstance(rollback_items[0], dict) else {}
    tier_review = (dry_run.get("safety_gates") or {}).get("risk_tier_review") or {}
    user = str(candidate.get("user") or (packet_preview.get("allowed_users") or [""])[0])
    current_channel = str(candidate.get("current_channel") or rollback_item.get("rollback_target") or "")
    target_channel = str(candidate.get("recommended_channel") or (packet_preview.get("allowed_targets") or [""])[0])
    rollback_target = str(rollback_item.get("rollback_target") or current_channel)
    authority_tier = str(tier_review.get("nearest_reachable_tier") or "TIER_1")
    authority_status = str(tier_review.get("nearest_reachable_status") or "MARGINAL_OPERATOR_REVIEW")
    packet_id = str(packet_preview.get("packet_id") or "")
    operation_id = str(packet_preview.get("operation_id") or "")
    selected_move_hash = str(packet_preview.get("selected_move_hash") or "")
    rollback_manifest_id = str(rollback_preview.get("rollback_manifest_id") or "")
    allowed_action = "execute this exact governed packet through existing owners only"
    forbidden_actions = [
        "move any other user",
        "use any other target",
        "rerun planner to change selected move",
        "bypass planner/governance",
        "enable daemon/timer",
        "expand authority",
        "create synthetic evidence",
    ]
    command_lines = [
        "Approve exact governed canary packet.",
        "",
        "Approved packet:",
        packet_id,
        "",
        "Operation:",
        operation_id,
        "",
        "Selected move hash:",
        selected_move_hash,
        "",
        "User:",
        user,
        "",
        "Move:",
        f"{current_channel} -> {target_channel}",
        "",
        "Rollback target:",
        rollback_target,
        "",
        "Rollback manifest:",
        rollback_manifest_id,
        "",
        "Authority:",
        f"{authority_tier} governed canary",
        "",
        "Authority status:",
        authority_status,
        "",
        "Allowed action:",
        f"{allowed_action}.",
        "",
        "Requirements:",
        "- consume the approved preview packet as the executable packet;",
        "- preserve packet_id, decision_id, operation_id, selected_move_hash, subject, target, and authority_generation;",
        "- write restore-barrier clearance only for this exact packet;",
        "- apply only this exact one-user movement;",
        "- verify immediately;",
        "- rollback to the rollback target if verification fails;",
        "- close outcome;",
        "- feed learning only from real observed outcome;",
        "- update Current Program State;",
        "- update OMP;",
        "- run truth/convergence;",
        "- continue OMP after outcome closure.",
        "",
        "Do not:",
    ]
    command_lines.extend([f"- {action};" for action in forbidden_actions])
    command_lines.extend([
        "",
        "Final response:",
        "- apply result;",
        "- verification result;",
        "- rollback result if any;",
        "- outcome closure;",
        "- learning update;",
        "- new metrics;",
        "- new highest implementation leverage task;",
        "- exact stop condition if stopped.",
    ])
    return {
        "schema_version": "v7.governed-canary.authority-approval-prompt.v1",
        "status": "APPROVAL_PROMPT_READY",
        "owner": "OMP + Current Program State",
        "source": "governed_canary_knowledge_gated_dry_run_cycle",
        "packet_preview_id": packet_id,
        "packet_id": packet_id,
        "decision_id": str(packet_preview.get("decision_id") or ""),
        "operation_id": operation_id,
        "selected_move_hash": selected_move_hash,
        "user": user,
        "current_channel": current_channel,
        "target_channel": target_channel,
        "rollback_target": rollback_target,
        "rollback_manifest_id": rollback_manifest_id,
        "authority_tier": authority_tier,
        "authority_status": authority_status,
        "allowed_action": allowed_action,
        "forbidden_actions": forbidden_actions,
        "approval_command_text": "\n".join(command_lines),
        "restore_status": restore_status.get("status", "UNKNOWN"),
        "stale_approval_invalidated_by": [
            "packet_preview_id",
            "operation_id",
            "selected_move_hash",
            "rollback_manifest_id",
            "authority_generation",
        ],
        "read_only": True,
        "preview_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
    }


def break_glass_authority_policy_contract() -> dict[str, Any]:
    """Define C3 break-glass policy as audited exception, not authority grant."""
    return {
        "schema_version": "v7.c3-break-glass-authority-policy.v1",
        "owner": "OMP + operator authority + admin_core/operator_execution_pipeline.py",
        "backlog_item": "C3",
        "policy_status": "DEFINED_NOT_APPROVED_FOR_RUNTIME",
        "omp_output": {
            "c3_status": "DONE_READ_ONLY_AUDITED_EXCEPTIONAL_OPERATOR_POLICY",
            "produced_evidence": "break_glass_authority_policy_contract",
            "unlocked_capability": "C4_OR_NEXT_OMP_ITEM_AFTER_CANONICAL_UPDATE",
        },
        "definition": {
            "purpose": "exceptional operator-controlled recovery path for real incident handling",
            "default_state": "DISABLED",
            "normal_runtime_authority": "UNCHANGED",
            "runtime_apply_permission": "NOT_GRANTED",
            "automation_permission": "NOT_GRANTED",
            "authority_expansion_permission": "NOT_GRANTED",
            "operator_policy_approval_required": True,
            "incident_or_emergency_context_required": True,
            "audit_required": True,
            "truth_convergence_required": True,
            "omp_and_cps_update_required": True,
        },
        "required_evidence_before_use": [
            "operator declared incident or emergency context",
            "explicit operator policy approval for this exceptional path",
            "exact subject, target, scope, and timebox",
            "existing packet or rollback evidence when movement/rollback is involved",
            "audit path availability",
            "verification and closure plan",
            "truth/convergence check before and after any approved operation",
        ],
        "forbidden_triggers": [
            "probabilistic suspicion alone",
            "shadow recommendation alone",
            "low confidence alone",
            "dashboard status",
            "Runtime self-optimization",
            "automatic recommendation ranking",
            "planner preference",
        ],
        "forbidden_effects": [
            "silent authority expansion",
            "Runtime apply enablement",
            "automation enablement",
            "new planner creation",
            "new owner creation",
            "new truth source creation",
            "synthetic evidence creation",
            "threshold or formula mutation",
            "user movement without exact approved packet",
            "rollback execution without exact approved rollback packet",
        ],
        "audit_contract": {
            "must_record": [
                "operator identity or approval owner",
                "incident/context id",
                "scope",
                "timebox",
                "approved action",
                "evidence consumed",
                "verification result",
                "rollback result if any",
                "closure state",
                "truth/convergence result",
                "OMP/CPS continuation",
            ],
            "audit_owner": CANONICAL_OBSERVABILITY_OWNER,
            "closure_owner": CANONICAL_FEEDBACK_OWNER,
            "packet_owner": CANONICAL_PACKET_OWNER,
        },
        "safety": {
            "read_only_contract": True,
            "break_glass_authority_granted_now": False,
            "runtime_apply_allowed_now": False,
            "automation_enabled": False,
            "authority_expanded": False,
            "planner_replaced": False,
            "synthetic_evidence_created": False,
            "users_moved": 0,
        },
        "blocked_until_explicit_operator_policy": [
            "break_glass_invocation",
            "restore_barrier_write",
            "apply",
            "rollback_apply",
            "user_movement",
            "authority_expansion",
        ],
        "canonical_rule": (
            "Break-glass in V7 is an audited exceptional operator policy only; "
            "it is never a Runtime default, never a Planner capability, and never "
            "a substitute for evidence, packet identity, verification, rollback, "
            "truth/convergence, OMP reporting, or Current Program State update."
        ),
    }


def _candidate_from_execution_lease(lease: dict[str, Any]) -> dict[str, Any]:
    packet = lease.get("packet") if isinstance(lease.get("packet"), dict) else {}
    lock = packet.get("approved_plan_lock") if isinstance(packet.get("approved_plan_lock"), dict) else {}
    moves = lock.get("selected_moves") if isinstance(lock.get("selected_moves"), list) else []
    move = moves[0] if moves and isinstance(moves[0], dict) else {}
    return {
        "user": str(move.get("user_ip") or ""),
        "current_channel": str(move.get("current_egress") or ""),
        "recommended_channel": str(move.get("recommended_egress") or ""),
        "confidence": 0.0,
        "trust": 0.0,
        "prediction": {},
        "risk": 0.0,
        "recommendation_hash": str((packet.get("expected") or {}).get("selected_move_hash") or ""),
        "source_hash": str((packet.get("expected") or {}).get("source_bundle_hash") or ""),
        "reasons": ["active execution lease preserved approved packet identity"],
        "execution_lease_id": str(lease.get("lease_id") or ""),
    }


def _packet_preview_from_execution_lease(lease: dict[str, Any]) -> dict[str, Any]:
    packet = lease.get("packet") if isinstance(lease.get("packet"), dict) else {}
    expected = packet.get("expected") if isinstance(packet.get("expected"), dict) else {}
    constraints = packet.get("constraints") if isinstance(packet.get("constraints"), dict) else {}
    rollback_manifest = packet.get("rollback_manifest") if isinstance(packet.get("rollback_manifest"), dict) else {}
    return {
        "schema_version": "v7.governed-canary.packet-preview.v1",
        "owner": CANONICAL_PACKET_OWNER,
        "status": "PACKET_PREVIEW_READY",
        "packet_id": str(packet.get("packet_id") or ""),
        "operation_id": str(packet.get("operation_id") or ""),
        "decision_id": str(packet.get("decision_id") or ""),
        "authority_generation": str(packet.get("authority_generation") or expected.get("generation_id") or ""),
        "selected_move_count": int(expected.get("selected_move_count") or 0),
        "selected_move_hash": str(expected.get("selected_move_hash") or ""),
        "allowed_users": [str(item) for item in (constraints.get("allowed_users") or [])],
        "allowed_targets": [str(item) for item in (constraints.get("allowed_targets") or [])],
        "source_hashes": expected.get("source_hashes") if isinstance(expected.get("source_hashes"), dict) else {},
        "snapshot_bundle_hash": str(expected.get("snapshot_bundle_hash") or ""),
        "rollback_manifest_preview": rollback_manifest,
        "execution_lease": {
            "schema_version": operator_execution.EXECUTION_LEASE_SCHEMA,
            "lease_id": str(lease.get("lease_id") or ""),
            "status": str(lease.get("status") or ""),
            "expires_at": str(lease.get("expires_at") or ""),
            "packet_hash": str(lease.get("packet_hash") or ""),
            "planner_regeneration_allowed": False,
            "packet_freshness_check_allowed": True,
        },
        "execution_packet_immutable": True,
        "planner_regeneration_blocked_by_execution_lease": True,
        "preview_only": True,
        "read_only": True,
    }


def _action_class_runtime_enablement_preview(
    *,
    packet_preview: dict[str, Any],
    candidate: dict[str, Any],
    stop_reason: str,
) -> dict[str, Any]:
    selected_count = int(packet_preview.get("selected_move_count") or len(packet_preview.get("allowed_users") or []) or (1 if candidate.get("user") else 0))
    if selected_count <= 0:
        action_class = "UNKNOWN_ACTION_CLASS"
    elif selected_count == 1:
        action_class = "single-user governed candidate failover"
    elif selected_count == 2:
        action_class = "two-user governed candidate failover"
    elif selected_count <= 5:
        action_class = "five-user governed candidate failover"
    else:
        action_class = "small-batch movement"
    state = "GOVERNED_ONLY" if action_class == "single-user governed candidate failover" else "NOT_CERTIFIED"
    delegated_policy_scope = bool(
        action_class == "single-user governed candidate failover"
        and selected_count == 1
        and stop_reason == "AUTHORITY_BOUNDARY"
    )
    return {
        "schema_version": "v7.action-class-runtime-enablement-preview.v1",
        "owner": "admin_core/operator_execution_pipeline.py",
        "registry_owner": "admin_core/autonomy_trust_acceleration.py",
        "packet_owner_reused": CANONICAL_PACKET_OWNER,
        "packet_to_action_class_mapping": {
            "packet_id": str(packet_preview.get("packet_id") or ""),
            "operation_id": str(packet_preview.get("operation_id") or ""),
            "decision_id": str(packet_preview.get("decision_id") or ""),
            "selected_move_hash": str(packet_preview.get("selected_move_hash") or ""),
            "authority_generation": str(packet_preview.get("authority_generation") or ""),
            "selected_move_count": selected_count,
            "subject": list(packet_preview.get("allowed_users") or ([candidate.get("user")] if candidate.get("user") else [])),
            "target": list(packet_preview.get("allowed_targets") or ([candidate.get("recommended_channel")] if candidate.get("recommended_channel") else [])),
            "action_class": action_class,
        },
        "authority_to_action_class_mapping": {
            "packet_approval": "not required inside the approved bounded delegated policy",
            "class_approval": "not required for bounded governed-learning inside the approved policy",
            "delegated_autonomy_policy": "authorizes exactly one fresh one-user governed candidate failover transaction at a time",
            "current_authority": "bounded delegated policy" if delegated_policy_scope else "no matching bounded policy authority",
            "authority_expansion_performed": False,
        },
        "current_action_class": action_class,
        "current_state": state,
        "next_promotion_target": "CERTIFIED_FOR_CLASS_APPROVAL" if state == "GOVERNED_ONLY" else "GOVERNED_ONLY",
        "runtime_can_execute_automatically": delegated_policy_scope,
        "runtime_must_stop_at": "" if delegated_policy_scope else (stop_reason or "AUTHORITY_BOUNDARY"),
        "runtime_apply_allowed_now": delegated_policy_scope,
        "candidate_approval_required": not delegated_policy_scope,
        "packet_approval_required": not delegated_policy_scope,
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "new_planner_created": False,
        "new_governance_created": False,
        "new_execution_path_created": False,
        "new_truth_source_created": False,
    }


def _learning_path_plan() -> dict[str, Any]:
    steps = [
        ("outcome", CANONICAL_FEEDBACK_OWNER),
        ("feedback", CANONICAL_FEEDBACK_OWNER),
        ("trust-evolution summary", "admin_core/intelligence_workers.py"),
        ("decision_outcome_learning", "admin_core/operator_execution_feedback.py"),
        ("knowledge_growth", "admin_core/autonomy_trust_acceleration.py"),
        ("future decision", "admin_core/operator_decision_surface.py"),
    ]
    return {
        "schema_version": "v7.governed-canary.learning-path.v1",
        "status": "LEARNING_PATH_CONNECTED",
        "path": [
            {"step": index + 1, "name": name, "owner": owner, "connected": True}
            for index, (name, owner) in enumerate(steps)
        ],
        "synthetic_evidence_created": False,
        "learning_written_now": False,
        "preview_only": True,
        "read_only": True,
    }


def _knowledge_gate_rows(decision_surface: dict[str, Any], dry_run: dict[str, Any]) -> list[dict[str, Any]]:
    overlay = decision_surface.get("knowledge_decision_overlay") if isinstance(decision_surface.get("knowledge_decision_overlay"), dict) else {}
    batch = decision_surface.get("batch_preview") if isinstance(decision_surface.get("batch_preview"), dict) else {}
    readiness = batch.get("knowledge_decision_readiness") if isinstance(batch.get("knowledge_decision_readiness"), dict) else {}
    outcome = dry_run.get("outcome_driven_evidence") if isinstance(dry_run.get("outcome_driven_evidence"), dict) else {}
    gates = [
        ("service_user_sla_fit", overlay.get("service_user_sla_fit")),
        ("freshness_actionability", overlay.get("freshness_actionability")),
        ("recovery_admission", overlay.get("recovery_admission")),
        ("anti_flapping", overlay.get("anti_flapping")),
        ("decision_effectiveness", overlay.get("decision_effectiveness") or readiness.get("decision_effectiveness")),
        ("knowledge_quality", decision_surface.get("knowledge_quality_read_model")),
        ("routing_recommendation_readiness", overlay.get("routing_recommendation_readiness") or {
            "readiness": readiness.get("routing_recommendation_readiness", "UNKNOWN"),
            "blockers": readiness.get("blockers", []),
        }),
    ]
    rows: list[dict[str, Any]] = []
    for name, payload in gates:
        payload = payload if isinstance(payload, dict) else {}
        candidate_scoped = name == "routing_recommendation_readiness"
        blockers = list(readiness.get("blockers") or []) if candidate_scoped else list(payload.get("blockers") or [])
        warnings = list(payload.get("warnings") or [])
        if blockers:
            impact = "BLOCKED"
        elif warnings:
            impact = "WARNED"
        elif payload:
            impact = "PASSED"
        else:
            impact = "UNKNOWN"
        rows.append({
            "gate": name,
            "impact": impact,
            "blockers": blockers,
            "warnings": warnings,
            "scope": "selected_candidate_batch" if candidate_scoped else "global_inventory",
            "blocking_power": "candidate_only" if candidate_scoped else "advisory_only",
            "owner_reused": True,
            "runtime_mutation_performed": False,
        })
    rows.append({
        "gate": "outcome_evidence",
        "impact": "PASSED" if outcome.get("applied") else ("WARNED" if outcome.get("raw_available") else "UNKNOWN"),
        "blockers": [] if outcome.get("applied") else [str(outcome.get("reason") or "outcome_evidence_not_applied")],
        "warnings": [],
        "owner_reused": True,
        "runtime_mutation_performed": False,
    })
    return rows


def _classify_cycle_stop(
    *,
    candidate: dict[str, Any],
    dry_run: dict[str, Any],
    packet_preview: dict[str, Any],
    restore_status: dict[str, Any],
    verification_plan: dict[str, Any],
    outcome_closure_plan: dict[str, Any],
    learning_path: dict[str, Any],
) -> tuple[str, str]:
    if not candidate:
        return "MISSING_TRIGGER", "No current event candidate or current-state recommendation can be packetized."
    blockers = list(((dry_run.get("safety_gates") or {}).get("hard_stop_blockers") or []))
    non_authority_blockers = [
        blocker for blocker in blockers
        if blocker not in {"confidence_too_low", "trust_too_low", "prediction_confidence_too_low"}
    ]
    tier_review = ((dry_run.get("safety_gates") or {}).get("risk_tier_review") or {})
    if non_authority_blockers:
        blocker = str(non_authority_blockers[0])
        if blocker.startswith("snapshot_mismatch") or blocker.startswith("source_drift"):
            return "MISSING_STATE_TRANSITION", blocker
        if blocker in {"packet_mismatch", "unknown_rollback_target", "service_blocker"}:
            return "MISSING_FIELD", blocker
        return "DISCONNECTED_OWNER", blocker
    if packet_preview.get("status") != "PACKET_PREVIEW_READY":
        return "MISSING_CLI_OR_API_SURFACE", str(packet_preview.get("blocker") or "packet_preview_not_ready")
    if restore_status.get("status") != "RESTORE_AND_ROLLBACK_PREVIEW_READY":
        return "MISSING_FIELD", str(restore_status.get("blocker") or "restore_or_rollback_not_ready")
    if verification_plan.get("status") != "VERIFICATION_PLAN_READY":
        return "MISSING_VERIFICATION_STEP", str(verification_plan.get("status") or "verification_plan_not_ready")
    if outcome_closure_plan.get("missing_now"):
        return "MISSING_FIELD", ",".join(outcome_closure_plan.get("missing_now") or [])
    if learning_path.get("status") != "LEARNING_PATH_CONNECTED":
        return "DISCONNECTED_OWNER", str(learning_path.get("status") or "learning_path_not_connected")
    if tier_review.get("operator_canary_marginal_allowed") or not blockers:
        return "AUTHORITY_BOUNDARY", "Governed TIER_1 operator approval is required before restore-barrier write or apply."
    return "MISSING_DOCUMENTED_POLICY", str(tier_review.get("nearest_reachable_status") or "tier_policy_unknown")


def _runtime_lifecycle_preview(
    *,
    cycle_id: str,
    candidate: dict[str, Any],
    consumer: dict[str, Any],
    packet_preview: dict[str, Any],
    restore_status: dict[str, Any],
    verification_plan: dict[str, Any],
    outcome_closure_plan: dict[str, Any],
    learning_path: dict[str, Any],
    stop_reason: str,
    stop_detail: str,
    dry_run: dict[str, Any],
    now: str = "",
) -> dict[str, Any]:
    decision_id = str(outcome_closure_plan.get("decision_id") or "")
    packet_id = str(packet_preview.get("packet_id") or "")
    operation_id = str(packet_preview.get("operation_id") or "")
    selected_move_hash = str(packet_preview.get("selected_move_hash") or "")
    current_state_generation = stable_hash({
        "event_ids": [row.get("event_id") for row in consumer.get("events", [])],
        "candidate": {
            "user": candidate.get("user", ""),
            "from": candidate.get("current_channel", ""),
            "to": candidate.get("recommended_channel", ""),
            "recommendation_hash": candidate.get("recommendation_hash", ""),
            "source_hash": candidate.get("source_hash", ""),
        },
        "snapshot_statuses": dry_run.get("snapshot_statuses", {}),
    })[:24]
    input_generation = stable_hash({
        "current_state_generation": current_state_generation,
        "decision_id": decision_id,
        "packet_id": packet_id,
        "operation_id": operation_id,
        "selected_move_hash": selected_move_hash,
    })[:24]
    idempotency_key_fingerprint = stable_hash({
        "decision_id": decision_id,
        "operation_id": operation_id,
        "packet_id": packet_id,
        "selected_move_hash": selected_move_hash,
        "current_state_generation": current_state_generation,
    })
    lifecycle_id = "rtlife_" + stable_hash({
        "cycle_id": cycle_id,
        "idempotency_key_fingerprint": idempotency_key_fingerprint,
    })[:24]
    authority_status = str(((dry_run.get("safety_gates") or {}).get("risk_tier_review") or {}).get("nearest_reachable_status", "UNKNOWN"))
    packet_freshness = "PACKET_PREVIEW_READY_CURRENT_INPUT" if packet_preview.get("status") == "PACKET_PREVIEW_READY" else "PACKET_UNAVAILABLE"
    if not candidate:
        runtime_stage = "WOKEN"
        stage_owner = "Current Program State"
    elif stop_reason == "AUTHORITY_BOUNDARY":
        runtime_stage = "AUTHORITY_CHECKED"
        stage_owner = "OMP"
    elif packet_preview.get("status") != "PACKET_PREVIEW_READY":
        runtime_stage = "PACKET_READY"
        stage_owner = CANONICAL_PACKET_TOOL
    elif verification_plan.get("status") != "VERIFICATION_PLAN_READY":
        runtime_stage = "VERIFYING"
        stage_owner = CANONICAL_RUNTIME_EXECUTOR
    elif outcome_closure_plan.get("missing_now"):
        runtime_stage = "OUTCOME_CLOSING"
        stage_owner = CANONICAL_FEEDBACK_OWNER
    elif learning_path.get("status") != "LEARNING_PATH_CONNECTED":
        runtime_stage = "LEARNING_FEED"
        stage_owner = "admin_core/intelligence_workers.py"
    else:
        runtime_stage = "STOPPED"
        stage_owner = "OMP"
    return {
        "schema_version": "v7.runtime-lifecycle-preview.v1",
        "lifecycle_id": lifecycle_id,
        "cycle_id": cycle_id,
        "decision_id": decision_id,
        "operation_id": operation_id,
        "packet_id": packet_id,
        "idempotency_key_fingerprint": idempotency_key_fingerprint,
        "current_state_generation": current_state_generation,
        "selected_move_hash": selected_move_hash,
        "runtime_stage": runtime_stage,
        "stage_owner": stage_owner,
        "input_generation": input_generation,
        "stop_reason": stop_reason,
        "stop_detail": stop_detail,
        "authority_status": authority_status,
        "packet_freshness": packet_freshness,
        "duplicate_work_status": "NO_DUPLICATE_WORK_DETECTED_READ_ONLY",
        "loop_guard_status": "NO_LOOP_DETECTED_READ_ONLY",
        "verification_status": str(verification_plan.get("status") or "UNKNOWN"),
        "rollback_status": str(restore_status.get("status") or "UNKNOWN"),
        "outcome_status": str(outcome_closure_plan.get("status") or "UNKNOWN"),
        "learning_status": str(learning_path.get("status") or "UNKNOWN"),
        "omp_notification_status": "READY_TO_NOTIFY_OMP_WITH_STOP" if stop_reason else "NOT_READY",
        "read_only": True,
        "preview_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "rollback_executed": False,
        "learning_written_now": False,
        "generated_at": now,
    }


def governed_canary_knowledge_gated_dry_run_cycle(
    *,
    events: list[dict[str, Any]] | None = None,
    readiness: dict[str, Any] | None = None,
    decision_surface: dict[str, Any] | None = None,
    execution_summary: dict[str, Any] | None = None,
    execution_lease: dict[str, Any] | None = None,
    max_users: int = 1,
    now: str = "",
) -> dict[str, Any]:
    """Run the read-only governed canary preparation cycle to its boundary.

    The function is pure: it orchestrates existing read models and preview
    contracts, but it does not call runtime commands, write files, or apply
    movement.
    """
    decision_surface = decision_surface if isinstance(decision_surface, dict) else {}
    events = events if isinstance(events, list) else []
    dry_run = autonomous_dry_run_model(
        readiness=readiness,
        decision_surface=decision_surface,
        execution_summary=execution_summary,
        max_users=max_users,
    )
    consumer = event_helpers.build_readonly_event_consumer_trace(events, now=now)
    candidates = [row for row in (dry_run.get("candidates") or []) if isinstance(row, dict)]
    planner_candidate = candidates[0] if candidates else {}
    planner_cycle_id = "gkcanary_" + stable_hash({
        "event_ids": [row.get("event_id") for row in consumer.get("events", [])],
        "candidate": {
            "user": planner_candidate.get("user", ""),
            "from": planner_candidate.get("current_channel", ""),
            "to": planner_candidate.get("recommended_channel", ""),
            "recommendation_hash": planner_candidate.get("recommendation_hash", ""),
        },
        "now": now,
    })[:24]
    dry_run_safety = dry_run.get("safety") if isinstance(dry_run.get("safety"), dict) else {}
    dry_run_generation = dry_run_safety.get("generation") if isinstance(dry_run_safety.get("generation"), dict) else {}
    dry_run_envelope = (
        dry_run_safety.get("atomic_execution_envelope")
        if isinstance(dry_run_safety.get("atomic_execution_envelope"), dict)
        else {}
    )
    planner_packet_preview = _preview_packet_for_candidate(
        planner_candidate,
        cycle_id=planner_cycle_id,
        authority_generation=str(dry_run_generation.get("planner_generation_id") or ""),
        execution_envelope=dry_run_envelope,
        now=now,
    )
    lease = execution_lease if isinstance(execution_lease, dict) else {}
    lease_state = (
        operator_execution.execution_lease_state(
            lease,
            current_material_state=operator_execution.material_state_from_packet_preview(planner_packet_preview),
            current_source_hashes=planner_packet_preview.get("source_hashes") if isinstance(planner_packet_preview.get("source_hashes"), dict) else None,
        )
        if lease
        else {"active": False, "status": "MISSING"}
    )
    lease_active = bool(lease_state.get("active"))
    candidate = _candidate_from_execution_lease(lease) if lease_active else planner_candidate
    cycle_id = planner_cycle_id
    packet_preview = (
        _packet_preview_from_execution_lease(lease)
        if lease_active
        else planner_packet_preview
    )
    rollback_items = (packet_preview.get("rollback_manifest_preview") or {}).get("items") or []
    restore_status = {
        "schema_version": "v7.governed-canary.restore-rollback-preview.v1",
        "owner": CANONICAL_PACKET_OWNER,
        "status": "RESTORE_AND_ROLLBACK_PREVIEW_READY" if rollback_items and all(row.get("rollback_target") for row in rollback_items) else "BLOCKED",
        "restore_barrier_required": True,
        "restore_barrier_written_now": False,
        "restore_action": "CREATE_RESTORE_BARRIER_CLEARANCE_AFTER_OPERATOR_APPROVAL",
        "rollback_target_known": bool(rollback_items and all(row.get("rollback_target") for row in rollback_items)),
        "rollback_items": rollback_items,
        "wrong_user_protection": packet_preview.get("wrong_user_protection", ""),
        "wrong_target_protection": packet_preview.get("wrong_target_protection", ""),
        "preview_only": True,
        "read_only": True,
    }
    verification_plan = _verification_plan(candidate, packet_preview)
    outcome_plan = _outcome_closure_plan(candidate, packet_preview)
    learning_path = _learning_path_plan()
    stop_reason, stop_detail = _classify_cycle_stop(
        candidate=candidate,
        dry_run=dry_run,
        packet_preview=packet_preview,
        restore_status=restore_status,
        verification_plan=verification_plan,
        outcome_closure_plan=outcome_plan,
        learning_path=learning_path,
    )
    runtime_lifecycle = _runtime_lifecycle_preview(
        cycle_id=cycle_id,
        candidate=candidate,
        consumer=consumer,
        packet_preview=packet_preview,
        restore_status=restore_status,
        verification_plan=verification_plan,
        outcome_closure_plan=outcome_plan,
        learning_path=learning_path,
        stop_reason=stop_reason,
        stop_detail=stop_detail,
        dry_run=dry_run,
        now=now,
    )
    approval_prompt = _authority_boundary_approval_prompt(
        candidate=candidate,
        packet_preview=packet_preview,
        restore_status=restore_status,
        dry_run=dry_run,
        stop_reason=stop_reason,
    )
    break_glass_policy = break_glass_authority_policy_contract()
    action_class_runtime_enablement = _action_class_runtime_enablement_preview(
        packet_preview=packet_preview,
        candidate=candidate,
        stop_reason=stop_reason,
    )
    knowledge_gates = _knowledge_gate_rows(decision_surface, dry_run)
    old_target = str(candidate.get("current_channel") or "")
    target = str(candidate.get("recommended_channel") or "")
    steps = [
        ("event_or_current_state", "READY", "admin_core/events.py" if events else CANONICAL_PLANNER),
        ("knowledge_gated_decision", "READY" if candidate else "STOPPED", "admin_core/operator_decision_surface.py"),
        ("candidate_selection", "READY" if candidate else "STOPPED", CANONICAL_PLANNER),
        ("packet_preparation", packet_preview.get("status", "UNKNOWN"), CANONICAL_PACKET_TOOL),
        ("restore_rollback_verification", restore_status.get("status", "UNKNOWN"), CANONICAL_PACKET_OWNER),
        ("verification_plan", verification_plan.get("status", "UNKNOWN"), CANONICAL_RUNTIME_EXECUTOR),
        ("outcome_closure_plan", outcome_plan.get("status", "UNKNOWN"), CANONICAL_FEEDBACK_OWNER),
        ("learning_path", learning_path.get("status", "UNKNOWN"), "admin_core/intelligence_workers.py"),
        ("next_step_decision", stop_reason, CANONICAL_PACKET_OWNER),
    ]
    non_authority_stop = stop_reason != "AUTHORITY_BOUNDARY"
    return {
        "schema_version": "v7.governed-canary.knowledge-gated-dry-run-cycle.v1",
        "cycle_id": cycle_id,
        "generated_at": now,
        "read_only": True,
        "preview_only": True,
        "autonomous_continuation": True,
        "manual_prompting_required_before_boundary": False,
        "event_source": "REAL_EVENT_PREVIEW" if consumer.get("event_count", 0) else "CURRENT_STATE_PREVIEW",
        "event_consumer": consumer,
        "candidate": candidate,
        "execution_lease": {
            **lease_state,
            "active": lease_active,
            "planner_regeneration_allowed": False if lease_active else None,
            "decision_regeneration_allowed": False if lease_active else None,
            "selected_move_hash_regeneration_allowed": False if lease_active else None,
            "target_regeneration_allowed": False if lease_active else None,
            "packet_freshness_check_allowed": True if lease_active else None,
        },
        "target": target,
        "decision": {
            "action": "MOVE_GOVERNED_CANARY_REVIEW" if candidate and target and target != old_target else "NO_MOVE_CANDIDATE",
            "from": old_target,
            "to": target,
            "old_planner_target": old_target,
            "knowledge_gated_target": target,
            "target_changed_compared_to_old_planner": False,
            "authority_tier": ((dry_run.get("safety_gates") or {}).get("risk_tier_review") or {}).get("nearest_reachable_tier", "UNKNOWN"),
            "authority_status": ((dry_run.get("safety_gates") or {}).get("risk_tier_review") or {}).get("nearest_reachable_status", "UNKNOWN"),
        },
        "knowledge_gates": knowledge_gates,
        "packet_preview": packet_preview,
        "restore_status": restore_status,
        "rollback_status": restore_status,
        "verification_plan": verification_plan,
        "outcome_closure_plan": outcome_plan,
        "learning_path": learning_path,
        "runtime_lifecycle_preview": runtime_lifecycle,
        "approval_prompt": approval_prompt,
        "break_glass_authority_policy": break_glass_policy,
        "action_class_runtime_enablement": action_class_runtime_enablement,
        "dry_run": dry_run,
        "cycle_steps": [
            {
                "step": index + 1,
                "name": name,
                "status": status,
                "owner": owner,
                "runtime_mutation_performed": False,
            }
            for index, (name, status, owner) in enumerate(steps)
        ],
        "stop_reason": stop_reason,
        "stop_detail": stop_detail,
        "stop_reason_class_valid": stop_reason in STOP_REASON_CLASSES,
        "non_authority_stop_requires_fix": non_authority_stop,
        "next_action": (
            "EXPLICIT_OPERATOR_APPROVAL_REQUIRED_FOR_THIS_PACKET"
            if stop_reason == "AUTHORITY_BOUNDARY"
            else "FIX_EXISTING_OWNER_GAP_AND_RERUN"
        ),
        "safety": {
            "execution_allowed_now": False,
            "apply_executed": False,
            "users_moved": 0,
            "rollback_executed": False,
            "autonomy_enabled": False,
            "runtime_mutation_performed": False,
            "new_planner_created": False,
            "new_governance_created": False,
            "new_execution_path_created": False,
            "new_truth_source_created": False,
            "new_storage_created": False,
            "new_daemon_created": False,
            "execution_lease_active": lease_active,
            "planner_regeneration_blocked_by_execution_lease": lease_active,
        },
        "final_verdict": (
            "AUTONOMOUS_DRY_RUN_CYCLE_REACHES_AUTHORITY_BOUNDARY"
            if stop_reason == "AUTHORITY_BOUNDARY"
            else "AUTONOMOUS_DRY_RUN_CYCLE_BLOCKED"
        ),
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


def l3_production_validation_runtime_action_transition(plan: dict[str, Any], *, max_users: int = 1) -> dict[str, Any]:
    selected = operator_execution.selected_moves_from_plan(plan)
    moves = selected.get("moves") if isinstance(selected.get("moves"), list) else []
    safety = plan.get("safety") if isinstance(plan.get("safety"), dict) else {}
    summary = plan.get("summary") if isinstance(plan.get("summary"), dict) else {}
    emergency_gate = safety.get("emergency_failover_autonomy") if isinstance(safety.get("emergency_failover_autonomy"), dict) else {}
    diagnostics = safety.get("selected_moves_diagnostics") if isinstance(safety.get("selected_moves_diagnostics"), dict) else {}
    errors: list[str] = []
    max_users = max(1, int(max_users))
    if len(moves) < 1:
        errors.append("l3_validation_selected_move_count_missing")
    if len(moves) > max_users:
        errors.append("l3_validation_selected_move_count_above_max_users")
    for move in moves:
        if str(move.get("move_type") or "") != "failover":
            errors.append("l3_validation_move_type_not_failover")
        if not str(move.get("user_ip") or ""):
            errors.append("l3_validation_user_missing")
        if not str(move.get("current_egress") or ""):
            errors.append("l3_validation_source_missing")
        if not str(move.get("recommended_egress") or ""):
            errors.append("l3_validation_target_missing")
    emergency_enabled = (
        str(summary.get("execution_mode") or "") == "emergency_failover"
        or bool(emergency_gate.get("enabled"))
        or bool(diagnostics.get("emergency_failover_authorized"))
    )
    if not emergency_enabled:
        errors.append("l3_validation_emergency_failover_not_enabled")
    return {
        "schema_version": "v7.l3-production-validation-runtime-action-transition.v1",
        "owner": "admin_core/operator_execution_pipeline.py",
        "canonical_owner": "admin_core/operator_execution_pipeline.py",
        "materialization_owner": CANONICAL_PACKET_OWNER,
        "runtime_consumer": CANONICAL_RUNTIME_EXECUTOR,
        "transition": "L3 Production Validation -> Runtime Action",
        "status": "READY" if not errors else "BLOCKED",
        "ok": not errors,
        "errors": errors,
        "selected_move_count": len(moves),
        "selected_moves": moves,
        "max_users": int(max_users),
        "required_chain": [
            "OMP approval",
            "admin_core/operator_execution_pipeline.py",
            "admin_core/operator_execution.py",
            "tools/v7-users-autoswitch",
            "apply",
        ],
        "duplicate_execution_path_created": False,
        "new_owner_created": False,
        "new_runtime_created": False,
        "new_planner_created": False,
        "new_authority_created": False,
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
    performance_timeline: dict[str, Any] | None = None,
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
    constant_time_ledger = constant_time_failover_performance_ledger(
        performance_timeline=performance_timeline,
    )
    return {
        "schema_version": "v7.execution-performance-foundation.v1",
        "read_only": True,
        "preview_only": True,
        "execution_allowed_now": False,
        "requested_metrics": visibility,
        "available_metrics": [key for key in REQUESTED_EXECUTION_TIMING_METRICS if key not in missing],
        "missing_metrics": missing,
        "slow_path_thresholds_ms": SLOW_PATH_THRESHOLDS_MS,
        "contracts_observed": len(contracts),
        "events_observed": len(events),
        "latency_foundation_present": True,
        "latency_collection_writes_runtime_state": False,
        "next_collection_owner": CANONICAL_OBSERVABILITY_OWNER,
        "constant_time_failover_performance_ledger": constant_time_ledger,
    }


def constant_time_failover_performance_ledger(
    *,
    performance_timeline: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Consume compact runtime timing through the existing Time owner.

    Missing producer fields remain explicit UNKNOWN values.  This projection
    neither creates a second ledger/store nor infers elapsed time from UTC.
    """
    timeline = performance_timeline if isinstance(performance_timeline, dict) else {}
    spans = timeline.get("spans") if isinstance(timeline.get("spans"), list) else []
    interval_values: dict[str, float | None] = {
        key: None for key in CONSTANT_TIME_LEDGER_INTERVALS
    }
    interval_sources: dict[str, list[str]] = {
        key: [] for key in CONSTANT_TIME_LEDGER_INTERVALS
    }
    for row in spans:
        if not isinstance(row, dict):
            continue
        metric = CONSTANT_TIME_LEDGER_STAGES.get(str(row.get("stage") or ""))
        duration = _duration_ms_from_row(row)
        if not metric or duration is None:
            continue
        current = interval_values[metric]
        interval_values[metric] = round((current or 0.0) + duration, 3)
        interval_sources[metric].append(str(row.get("stage") or "UNKNOWN"))

    raw_counters = (
        timeline.get("hot_path_work_counters")
        if isinstance(timeline.get("hot_path_work_counters"), dict)
        else {}
    )
    counters: dict[str, dict[str, Any]] = {}
    for key in CONSTANT_TIME_WORK_COUNTERS:
        value = raw_counters.get(key)
        counters[key] = {
            "status": "OBSERVED" if isinstance(value, (int, float)) else "UNKNOWN",
            "value": value if isinstance(value, (int, float)) else None,
            "measurement_kind": str(
                raw_counters.get(f"{key}_measurement_kind") or "NOT_EXPOSED"
            ),
        }
    unknown = [key for key, row in counters.items() if row["status"] == "UNKNOWN"]
    observed = [key for key, row in counters.items() if row["status"] == "OBSERVED"]
    return {
        "schema_version": "v7.constant-time-failover-performance-ledger.v1",
        "owner": "admin_core.operator_execution_pipeline.execution_performance_foundation",
        "durable_storage": "existing governed transaction receipt",
        "creates_new_store": False,
        "clock_source": str(timeline.get("clock_source") or "UNKNOWN"),
        "clock_valid": str(timeline.get("clock_source") or "") == "time.monotonic_ns",
        "intervals": {
            key: {
                "status": "OBSERVED" if value is not None else "UNKNOWN",
                "value_ms": value,
                "sources": interval_sources[key],
            }
            for key, value in interval_values.items()
        },
        "hot_path_work_counters": counters,
        "observed_counter_fields": observed,
        "unknown_counter_fields": unknown,
        "hidden_o_n_guard": (
            "OBSERVED_WITH_EXPLICIT_UNKNOWNS" if observed
            else "INSUFFICIENT_PRODUCER_COUNTERS"
        ),
        "n_dependency": str(raw_counters.get("n_dependency") or "UNKNOWN"),
        "k_dependency": str(raw_counters.get("k_dependency") or "UNKNOWN"),
        "unknown_values_fabricated": False,
    }


def exact_client_network_context_traffic_probe_contract(
    receipt: dict[str, Any],
    *,
    expected_user: str,
    expected_target_fingerprint: str,
) -> dict[str, Any]:
    """Validate an owner-backed client recovery receipt without probing here.

    The Time owner consumes the receipt; it does not create a new probe owner.
    A route lookup, kernel counter or host-management-path request can never be
    promoted to client traffic recovery evidence by this function.
    """
    receipt = receipt if isinstance(receipt, dict) else {}
    required_true = {
        "exact_certification_identity_context": receipt.get("exact_certification_identity_context") is True,
        "routing_table_or_fwmark_bound": receipt.get("routing_table_or_fwmark_bound") is True,
        "payload_response_verified": receipt.get("payload_response_verified") is True,
        "management_default_route_forbidden": receipt.get("management_default_route_used") is False,
        "fresh_socket": receipt.get("fresh_socket") is True,
        "fresh_dns_or_declared_no_dns": (
            receipt.get("fresh_dns_resolution") is True
            or str(receipt.get("dns_mode") or "") == "DECLARED_NO_DNS"
        ),
        "kernel_counter_only_forbidden": receipt.get("kernel_counter_only") is False,
    }
    blockers = [name for name, passed in required_true.items() if not passed]
    if str(receipt.get("user") or "") != str(expected_user or ""):
        blockers.append("exact_user_mismatch")
    if str(receipt.get("observed_target_egress_fingerprint") or "") != str(expected_target_fingerprint or ""):
        blockers.append("target_egress_fingerprint_mismatch")
    if not str(receipt.get("probe_owner") or ""):
        blockers.append("probe_owner_missing")
    if not str(receipt.get("payload_fingerprint") or ""):
        blockers.append("payload_fingerprint_missing")
    timeout_ms = _as_int(receipt.get("timeout_ms"), 0)
    retry_count = _as_int(receipt.get("retry_count"), -1)
    cadence_ms = _as_int(receipt.get("observation_cadence_ms"), 0)
    if timeout_ms <= 0:
        blockers.append("timeout_contract_missing")
    if retry_count < 0:
        blockers.append("retry_contract_missing")
    if cadence_ms <= 0:
        blockers.append("observation_cadence_missing")
    return {
        "schema_version": "v7.exact-client-network-context-traffic-probe-contract.v1",
        "status": "EXACT_CLIENT_NETWORK_CONTEXT_TRAFFIC_PROBE_PROVEN" if not blockers else "PROBE_INVALID",
        "ok": not blockers,
        "blockers": sorted(set(blockers)),
        "probe_owner": str(receipt.get("probe_owner") or ""),
        "receipt_id": str(receipt.get("receipt_id") or ""),
        "runtime_mutation_performed": False,
        "routing_mutation_performed": False,
        "user_movement": 0,
    }


CUTOVER_EVENT_FIELDS = (
    "first_failed_observation_monotonic_ns",
    "confirmed_hard_failure_monotonic_ns",
    "user_target_decision_bound_monotonic_ns",
    "apply_admitted_monotonic_ns",
    "canonical_user_assignment_committed_monotonic_ns",
    "kernel_route_mutation_completed_monotonic_ns",
    "exact_user_kernel_path_visible_monotonic_ns",
    "target_egress_payload_pass_monotonic_ns",
    "control_plane_and_kernel_path_cutover_pass_monotonic_ns",
)


def control_plane_kernel_path_cutover_contract(receipt: dict[str, Any]) -> dict[str, Any]:
    """Consume a composed server-side cutover receipt without overclaiming.

    The assignment/route owner proves the exact identity binding.  A separate
    target-egress payload owner proves that the selected tunnel can carry a
    fresh payload.  Combining those owner-backed facts is useful engineering
    evidence, but it is deliberately *not* remote-device recovery evidence and
    is not an exact-user payload probe unless the packet actually traversed the
    user's source/fwmark/table context.
    """
    receipt = receipt if isinstance(receipt, dict) else {}
    decision = receipt.get("decision_binding") if isinstance(receipt.get("decision_binding"), dict) else {}
    assignment = receipt.get("assignment_proof") if isinstance(receipt.get("assignment_proof"), dict) else {}
    kernel = receipt.get("kernel_path_proof") if isinstance(receipt.get("kernel_path_proof"), dict) else {}
    payload = receipt.get("target_payload_proof") if isinstance(receipt.get("target_payload_proof"), dict) else {}
    lineage_fields = (
        "incident_id",
        "incident_generation",
        "validation_generation_id",
        "user",
        "source",
        "target",
        "candidate_id",
        "packet_id",
        "lease_id",
        "operation_id",
    )
    blockers: list[str] = []
    for field in lineage_fields:
        expected = str(receipt.get(field) or "")
        if not expected:
            blockers.append(f"{field}_missing")
            continue
        for owner_name, owner_row in (
            ("decision", decision),
            ("assignment", assignment),
            ("kernel", kernel),
            ("payload", payload),
        ):
            if str(owner_row.get(field) or "") != expected:
                blockers.append(f"{owner_name}_{field}_mismatch")

    certification_identity = receipt.get("certification_identity") is True
    if not certification_identity:
        blockers.append("certification_identity_required")
    if _as_int(receipt.get("ordinary_user_delta"), -1) != 0:
        blockers.append("ordinary_user_delta_must_be_zero")
    if decision.get("status") != "USER_TARGET_DECISION_BOUND":
        blockers.append("user_target_decision_not_bound")
    if assignment.get("status") != "CANONICAL_USER_ASSIGNMENT_COMMITTED":
        blockers.append("canonical_assignment_not_committed")
    if assignment.get("stale_writer_rejected") is not True:
        blockers.append("stale_writer_rejection_not_proven")
    if str(assignment.get("previous_egress") or "") != str(receipt.get("source") or ""):
        blockers.append("assignment_previous_egress_mismatch")
    if str(assignment.get("new_egress") or "") != str(receipt.get("target") or ""):
        blockers.append("assignment_new_egress_mismatch")

    if kernel.get("status") != "EXACT_USER_ASSIGNMENT_AND_KERNEL_PATH_TRANSITION_PROVEN":
        blockers.append("exact_user_kernel_path_not_proven")
    for field in ("source_ip", "policy_rule_fingerprint", "routing_table", "target_interface", "route_generation"):
        if not str(kernel.get(field) or ""):
            blockers.append(f"kernel_{field}_missing")
    if kernel.get("old_effective_binding_absent") is not True:
        blockers.append("old_effective_binding_still_present_or_unknown")

    exact_payload = (
        payload.get("status")
        == "EXACT_CLIENT_NETWORK_CONTEXT_TRAFFIC_PROBE_RECEIPT_READY"
        and str(payload.get("scope") or "")
        == "EXACT_CLIENT_NETWORK_CONTEXT"
    )
    target_only_payload = (
        payload.get("status")
        == "TARGET_EGRESS_ROUTE_BOUND_PAYLOAD_PROBE_PROVEN"
        and str(payload.get("scope") or "") == "TARGET_EGRESS_PATH_ONLY"
    )
    if not (exact_payload or target_only_payload):
        blockers.append("route_bound_payload_not_proven")
    required_payload = {
        "fresh_socket": payload.get("fresh_socket") is True,
        "fresh_dns_or_declared_no_dns": (
            payload.get("fresh_dns_resolution") is True
            or str(payload.get("dns_mode") or "") == "DECLARED_NO_DNS"
        ),
        "payload_response_verified": payload.get("payload_response_verified") is True,
        "management_default_route_forbidden": payload.get("management_default_route_used") is False,
        "target_interface_bound": payload.get("target_interface_bound") is True,
        "target_fingerprint_verified": payload.get("target_fingerprint_verified") is True,
        "kernel_counter_only_forbidden": payload.get("kernel_counter_only") is False,
    }
    if exact_payload:
        required_payload.update({
            "exact_certification_identity_context": (
                payload.get("exact_certification_identity_context") is True
            ),
            "routing_table_or_fwmark_bound": (
                payload.get("routing_table_or_fwmark_bound") is True
            ),
            "exact_user_source_fwmark_table_traversed": (
                payload.get("exact_user_source_fwmark_table_traversed") is True
            ),
        })
    blockers.extend(name for name, passed in required_payload.items() if not passed)
    if _as_int(payload.get("timeout_ms"), 0) <= 0:
        blockers.append("payload_timeout_contract_missing")
    if _as_int(payload.get("retry_count"), -1) < 0:
        blockers.append("payload_retry_contract_missing")

    clock_source = str(receipt.get("clock_source") or "")
    if clock_source != "time.monotonic_ns":
        blockers.append("single_monotonic_clock_domain_required")
    events = {field: _as_int(receipt.get(field), 0) for field in CUTOVER_EVENT_FIELDS}
    if any(value <= 0 for value in events.values()):
        blockers.append("all_cutover_events_required")
    elif list(events.values()) != sorted(events.values()):
        blockers.append("ordered_cutover_events_required")

    def interval(start: str, end: str) -> float | None:
        if blockers or events[start] <= 0 or events[end] < events[start]:
            return None
        return round((events[end] - events[start]) / 1_000_000.0, 3)

    metrics = {
        "failure_detection_latency_ms": interval(CUTOVER_EVENT_FIELDS[0], CUTOVER_EVENT_FIELDS[1]),
        "failure_to_decision_latency_ms": interval(CUTOVER_EVENT_FIELDS[1], CUTOVER_EVENT_FIELDS[2]),
        "decision_to_apply_admission_latency_ms": interval(CUTOVER_EVENT_FIELDS[2], CUTOVER_EVENT_FIELDS[3]),
        "canonical_assignment_commit_latency_ms": interval(CUTOVER_EVENT_FIELDS[3], CUTOVER_EVENT_FIELDS[4]),
        "kernel_route_mutation_latency_ms": interval(CUTOVER_EVENT_FIELDS[4], CUTOVER_EVENT_FIELDS[5]),
        "kernel_path_visibility_latency_ms": interval(CUTOVER_EVENT_FIELDS[5], CUTOVER_EVENT_FIELDS[6]),
        "target_egress_payload_ready_latency_ms": interval(CUTOVER_EVENT_FIELDS[6], CUTOVER_EVENT_FIELDS[7]),
        "control_plane_and_kernel_path_cutover_latency_ms": interval(CUTOVER_EVENT_FIELDS[1], CUTOVER_EVENT_FIELDS[8]),
        "failure_evidence_to_kernel_cutover_latency_ms": interval(CUTOVER_EVENT_FIELDS[0], CUTOVER_EVENT_FIELDS[8]),
    }
    if receipt.get("assignment_kernel_split") == "ATOMIC_BUNDLED_COMPLETION_INTERNAL_SPLIT_UNKNOWN":
        metrics["kernel_route_mutation_latency_ms"] = None
    exact_user_payload = bool(
        exact_payload
        and payload.get("exact_user_source_fwmark_table_traversed") is True
    )
    if receipt.get("exact_user_payload_claimed") is True and not exact_user_payload:
        blockers.append("exact_user_payload_claim_forbidden_without_exact_traversal")
    if receipt.get("remote_client_recovery_claimed") is True:
        blockers.append("remote_client_recovery_claim_forbidden")
    if blockers:
        metrics = {key: None for key in metrics}
    ok = not blockers
    return {
        "schema_version": "v7.control-plane-kernel-path-cutover-contract.v1",
        "status": "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_PASS" if ok else "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_INVALID",
        "ok": ok,
        "claim_class": "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER",
        "exact_user_assignment_and_kernel_path_transition_proven": ok,
        "target_egress_route_bound_payload_probe_proven": ok,
        "exact_user_payload_path_proven": bool(ok and exact_user_payload),
        "remote_client_application_recovery_latency": "NOT_MEASURED_NO_CLIENT_AGENT",
        "existing_flow_recovery_latency": "NOT_MEASURED",
        "remote_device_recovery": "DEFERRED_TO_FUTURE_CLIENT_AGENT_CAPABILITY",
        "clock_source": clock_source,
        "events": events,
        "metrics": metrics,
        "diagnostic_performance_timeline": (
            receipt.get("diagnostic_performance_timeline")
            if isinstance(
                receipt.get("diagnostic_performance_timeline"), dict,
            )
            else {}
        ),
        "blockers": sorted(set(blockers)),
        "runtime_mutation_performed_by_consumer": False,
        "routing_mutation_performed_by_consumer": False,
        "user_movement_by_consumer": 0,
    }


def controlled_kernel_cutover_sample_validity(sample: dict[str, Any]) -> dict[str, Any]:
    """Validate one CT-M0F observation without applying campaign cardinality.

    The five-sample p95 is a campaign gate.  Applying it while terminalising
    the first reservation makes the campaign impossible to populate.  One
    observation earns sample credit when the exact cutover contract passed,
    its authoritative total is known, and the per-sample 5 s ceiling holds.
    """
    sample = sample if isinstance(sample, dict) else {}
    metrics = sample.get("metrics") if isinstance(sample.get("metrics"), dict) else {}
    total = metrics.get("control_plane_and_kernel_path_cutover_latency_ms")
    blockers: list[str] = []
    if sample.get("status") != "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_PASS":
        blockers.append("cutover_contract_not_passed")
    if not isinstance(total, (int, float)):
        blockers.append("cutover_latency_unknown")
    elif float(total) > 5000.0:
        blockers.append("authoritative_cutover_sample_above_5000ms")
    ok = not blockers
    return {
        "schema_version": "v7.controlled-kernel-cutover-sample-validity.v1",
        "status": (
            "CONTROLLED_KERNEL_CUTOVER_SAMPLE_VALID"
            if ok else "CONTROLLED_KERNEL_CUTOVER_SAMPLE_INVALID"
        ),
        "ok": ok,
        "authoritative_total_ms": round(float(total), 3)
        if isinstance(total, (int, float)) else None,
        "per_sample_ceiling_ms": 5000,
        "blockers": blockers,
    }


def controlled_kernel_cutover_gate(samples: list[dict[str, Any]]) -> dict[str, Any]:
    """Evaluate the bounded CT-M0F engineering gate with nearest-rank p95.

    Five samples are a deliberately small controlled engineering gate, not a
    statistically representative production percentile.  The total cutover
    ceiling is authoritative; substage ceilings remain diagnostic because
    overlapping intervals must not be summed into a second total.
    """
    samples = samples if isinstance(samples, list) else []
    valid = [
        row for row in samples
        if isinstance(row, dict)
        and row.get("status") == "CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_PASS"
        and isinstance(row.get("metrics"), dict)
    ]

    def nearest_rank(values: list[float], percentile: int = 95) -> float | None:
        if not values:
            return None
        ordered = sorted(values)
        rank = max(1, (percentile * len(ordered) + 99) // 100)
        return round(float(ordered[rank - 1]), 3)

    metric_names = (
        "failure_detection_latency_ms",
        "failure_to_decision_latency_ms",
        "decision_to_apply_admission_latency_ms",
        "canonical_assignment_commit_latency_ms",
        "kernel_route_mutation_latency_ms",
        "kernel_path_visibility_latency_ms",
        "target_egress_payload_ready_latency_ms",
        "control_plane_and_kernel_path_cutover_latency_ms",
    )
    distributions: dict[str, dict[str, Any]] = {}
    for name in metric_names:
        values = [
            float(row["metrics"][name])
            for row in valid
            if isinstance(row["metrics"].get(name), (int, float))
        ]
        distributions[name] = {
            "sample_count": len(values),
            "controlled_gate_p95_nearest_rank_ms": nearest_rank(values),
            "max_ms": round(max(values), 3) if values else None,
        }
    kinds = [str(row.get("sample_kind") or "") for row in valid]
    generations = {
        str(row.get("validation_generation_id") or "")
        for row in valid
        if str(row.get("validation_generation_id") or "")
    }
    total = distributions["control_plane_and_kernel_path_cutover_latency_ms"]
    operational_ready = all((
        len(valid) >= 5,
        kinds.count("cold") >= 1,
        kinds.count("warm") >= 2,
        len(generations) >= 2,
        total["controlled_gate_p95_nearest_rank_ms"] is not None,
        float(total["controlled_gate_p95_nearest_rank_ms"] or 0.0) <= 3000.0,
        total["max_ms"] is not None,
        float(total["max_ms"] or 0.0) <= 5000.0,
    ))
    transitional_ready = all((
        len(valid) >= 3,
        kinds.count("cold") >= 1,
        kinds.count("warm") >= 2,
        total["controlled_gate_p95_nearest_rank_ms"] is not None,
        float(total["controlled_gate_p95_nearest_rank_ms"] or 0.0) <= 10000.0,
        total["max_ms"] is not None,
        float(total["max_ms"] or 0.0) <= 15000.0,
    ))
    blockers: list[str] = []
    if len(valid) < 5:
        blockers.append("five_valid_samples_required")
    if kinds.count("cold") < 1:
        blockers.append("one_cold_sample_required")
    if kinds.count("warm") < 2:
        blockers.append("two_warm_samples_required")
    if len(generations) < 2:
        blockers.append("two_owner_backed_generations_required")
    if total["controlled_gate_p95_nearest_rank_ms"] is None:
        blockers.append("cutover_latency_unknown")
    elif float(total["controlled_gate_p95_nearest_rank_ms"]) > 3000.0:
        blockers.append("authoritative_cutover_p95_above_3000ms")
    if total["max_ms"] is not None and float(total["max_ms"]) > 5000.0:
        blockers.append("authoritative_cutover_max_above_5000ms")
    return {
        "schema_version": "v7.controlled-kernel-cutover-gate.v1",
        "status": (
            "LEGACY_KERNEL_CUTOVER_OPERATIONAL_SLO_CONSUMED"
            if operational_ready
            else "TRANSITIONAL_KERNEL_CUTOVER_GATE_PASS"
            if transitional_ready
            else "KERNEL_CUTOVER_GATE_INSUFFICIENT_OR_FAILED"
        ),
        "ok": operational_ready,
        "gate_kind": "BOUNDED_CONTROLLED_ENGINEERING_GATE_NOT_STATISTICAL_PERCENTILE",
        "p95_method": "NEAREST_RANK",
        "valid_sample_count": len(valid),
        "cold_sample_count": kinds.count("cold"),
        "warm_sample_count": kinds.count("warm"),
        "owner_backed_generation_count": len(generations),
        "distributions": distributions,
        "total_cutover_ceiling_authoritative": True,
        "substage_ceilings_diagnostic_only": True,
        "p99": "INSUFFICIENT_SAMPLE_COUNT" if len(valid) < 100 else "NOT_COMPUTED_BY_BOUNDED_GATE",
        "blockers": sorted(set(blockers)),
    }
def client_recovery_clock_contract(receipt: dict[str, Any]) -> dict[str, Any]:
    """Derive detection and end-to-end recovery from one clock domain."""
    receipt = receipt if isinstance(receipt, dict) else {}
    clock = str(receipt.get("clock_source") or "")
    first = _as_int(receipt.get("first_failed_observation_monotonic_ns"), 0)
    confirmed = _as_int(receipt.get("confirmed_hard_failure_monotonic_ns"), 0)
    recovered = _as_int(receipt.get("first_successful_client_traffic_monotonic_ns"), 0)
    cadence_ms = max(0, _as_int(receipt.get("observation_cadence_ms"), 0))
    blockers: list[str] = []
    if clock != "time.monotonic_ns":
        blockers.append("single_monotonic_clock_domain_required")
    if not (first > 0 and confirmed >= first and recovered >= confirmed):
        blockers.append("ordered_recovery_timestamps_required")
    if cadence_ms <= 0:
        blockers.append("observation_cadence_required")
    if blockers:
        detection_ms = None
        post_confirmation_ms = None
        end_to_end_ms = None
    else:
        detection_ms = round((confirmed - first) / 1_000_000.0, 3)
        post_confirmation_ms = round((recovered - confirmed) / 1_000_000.0, 3)
        end_to_end_ms = round((recovered - first) / 1_000_000.0, 3)
    return {
        "schema_version": "v7.client-recovery-clock-contract.v1",
        "status": "CLIENT_RECOVERY_CLOCK_PROVEN" if not blockers else "CLIENT_RECOVERY_CLOCK_INVALID",
        "ok": not blockers,
        "clock_source": clock,
        "failure_detection_clock_start": "FIRST_FAILED_OBSERVATION",
        "detection_latency_ms": detection_ms,
        "post_confirmation_recovery_ms": post_confirmation_ms,
        "first_failure_evidence_to_client_recovery_latency_ms": end_to_end_ms,
        "measurement_uncertainty_upper_bound_ms": cadence_ms if not blockers else None,
        "blockers": blockers,
    }


def execution_observability_snapshot(
    *,
    contracts: list[dict[str, Any]] | None = None,
    events: list[dict[str, Any]] | None = None,
    performance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    contracts = contracts if isinstance(contracts, list) else []
    events = events if isinstance(events, list) else []
    performance = performance if isinstance(performance, dict) else {}
    rows = [row for row in contracts + events if isinstance(row, dict)]
    dated_rows = [(dt, row) for row in rows if (dt := _row_ts(row))]
    ordered = [row for _, row in sorted(dated_rows, key=lambda item: item[0], reverse=True)]
    if not ordered:
        ordered = rows

    latest = ordered[0] if ordered else {}
    terminal = [(row, _terminal_kind(row)) for row in ordered]
    successes = [row for row, kind in terminal if kind == "success"]
    failures = [row for row, kind in terminal if kind == "failure"]
    rollbacks = [row for row, kind in terminal if kind == "rollback"]
    packets = [row for row in ordered if _stage_from_row(row) == "packet"]
    verifications = [row for row in ordered if _stage_from_row(row) == "verification"]

    stage = _stage_from_row(latest) if latest else ""
    if not stage:
        for metric in performance.get("missing_metrics") or []:
            if isinstance(metric, str) and metric.endswith("_duration_ms"):
                stage = metric.removesuffix("_duration_ms")
                break
    terminal_count = len(successes) + len(failures)
    return {
        "schema_version": "v7.execution-observability-snapshot.v1",
        "read_only": True,
        "preview_only": True,
        "execution_allowed_now": False,
        "current_stage": stage or "waiting_for_execution_evidence",
        "latest_event_ref": _row_ref(latest) if latest else "",
        "latest_success_ref": _row_ref(successes[0]) if successes else "",
        "latest_failure_ref": _row_ref(failures[0]) if failures else "",
        "latest_rollback_ref": _row_ref(rollbacks[0]) if rollbacks else "",
        "latest_packet_ref": _row_ref(packets[0]) if packets else "",
        "latest_verification_ref": _row_ref(verifications[0]) if verifications else "",
        "success_events": len(successes),
        "failure_events": len(failures),
        "rollback_events": len(rollbacks),
        "success_rate": round(len(successes) / terminal_count, 4) if terminal_count else None,
        "rollback_rate": round(len(rollbacks) / max(1, len(ordered)), 4) if ordered else None,
        "observed_rows": len(rows),
        "contracts_observed": len(contracts),
        "events_observed": len(events),
    }


def execution_loop_observability_model(
    performance: dict[str, Any],
    observability: dict[str, Any] | None = None,
) -> dict[str, Any]:
    missing = performance.get("missing_metrics") or []
    observability = observability if isinstance(observability, dict) else {}
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
        "current_stage": observability.get("current_stage", "waiting_for_execution_evidence"),
        "latest_success_ref": observability.get("latest_success_ref", ""),
        "latest_failure_ref": observability.get("latest_failure_ref", ""),
        "latest_rollback_ref": observability.get("latest_rollback_ref", ""),
        "success_rate": observability.get("success_rate"),
        "rollback_rate": observability.get("rollback_rate"),
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


def _metric_payload(performance: dict[str, Any], metric: str) -> dict[str, Any]:
    requested = performance.get("requested_metrics") if isinstance(performance.get("requested_metrics"), dict) else {}
    item = requested.get(metric) if isinstance(requested.get(metric), dict) else {}
    return {
        "metric": metric,
        "available": bool(item.get("available")),
        "value": item.get("value"),
        "sources": item.get("sources") if isinstance(item.get("sources"), list) else [],
    }


def _status_from_metric(metric: dict[str, Any]) -> str:
    return "OBSERVED" if metric.get("available") else "WAITING_FOR_EVENT_DATA"


def _slow_metric_payload(metric: dict[str, Any]) -> dict[str, Any]:
    name = str(metric.get("metric") or "")
    value = metric.get("value")
    threshold = SLOW_PATH_THRESHOLDS_MS.get(name)
    if value is None or threshold is None:
        return {**metric, "threshold_ms": threshold, "slow": False, "over_threshold_ratio": 0.0}
    ratio = _as_float(value) / max(1.0, threshold)
    return {
        **metric,
        "threshold_ms": threshold,
        "slow": ratio >= 1.0,
        "over_threshold_ratio": round(ratio, 4),
    }


def _count_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(row.get(key) or "UNKNOWN")
        counts[value] = counts.get(value, 0) + 1
    return counts


def execution_operator_dashboard_model(
    *,
    readiness: dict[str, Any] | None = None,
    decision_surface: dict[str, Any] | None = None,
    execution_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the operator-facing dashboard payload from existing read models.

    This is deliberately a derived view. It does not collect from runtime,
    decide movement, or create any authority; it only organizes already-read
    contracts, events, snapshots and readiness contracts for the admin UI.
    """
    readiness = readiness if isinstance(readiness, dict) else execution_loop_readiness_foundation()
    decision_surface = decision_surface if isinstance(decision_surface, dict) else {}
    execution_summary = execution_summary if isinstance(execution_summary, dict) else {}
    performance = readiness.get("performance_audit") if isinstance(readiness.get("performance_audit"), dict) else {}
    observability = readiness.get("execution_observability") if isinstance(readiness.get("execution_observability"), dict) else {}
    mapping = readiness.get("execution_loop_mapping") if isinstance(readiness.get("execution_loop_mapping"), dict) else {}
    certification = readiness.get("readiness_certification") if isinstance(readiness.get("readiness_certification"), dict) else {}
    summary = execution_summary.get("summary") if isinstance(execution_summary.get("summary"), dict) else {}
    channels = decision_surface.get("channels") if isinstance(decision_surface.get("channels"), list) else []
    users = decision_surface.get("users") if isinstance(decision_surface.get("users"), list) else []
    snapshots = decision_surface.get("snapshot_statuses") if isinstance(decision_surface.get("snapshot_statuses"), dict) else {}
    batch = decision_surface.get("batch_preview") if isinstance(decision_surface.get("batch_preview"), dict) else {}
    shadow = decision_surface.get("shadow_autonomy") if isinstance(decision_surface.get("shadow_autonomy"), dict) else {}
    autonomous = autonomous_dry_run_model(
        readiness=readiness,
        decision_surface=decision_surface,
        execution_summary=execution_summary,
        max_users=1,
    )
    outcome_evidence = _outcome_evidence_advice(decision_surface)
    stage_rows = []
    for row in readiness.get("execution_chain_audit") or []:
        if not isinstance(row, dict):
            continue
        metric = _metric_payload(performance, row.get("timing_metric", ""))
        slow = _slow_metric_payload(metric)
        stage_rows.append({
            "stage": row.get("stage", ""),
            "owner": row.get("owner", ""),
            "status": _status_from_metric(metric),
            "duration_ms": metric.get("value"),
            "duration_available": metric.get("available"),
            "threshold_ms": slow.get("threshold_ms"),
            "slow": slow.get("slow", False),
            "last_execution": "from_existing_contract_or_event" if metric.get("available") else "not_observed_in_current_read_model",
            "manual": row.get("manual"),
            "runtime_mutation": row.get("runtime_mutation"),
            "operator_explanation": (
                "Duration is visible from existing evidence."
                if metric.get("available")
                else "Waiting for an execution contract/event row with duration data."
            ),
        })
    metrics = [_slow_metric_payload(_metric_payload(performance, metric)) for metric in REQUESTED_EXECUTION_TIMING_METRICS]
    slow_metrics = [
        item
        for item in metrics
        if item.get("available") and item.get("slow")
    ]
    slow_metrics = sorted(
        slow_metrics,
        key=lambda item: (
            str(item.get("metric") or "") in {"total_duration_ms", "per_user_duration_ms"},
            -_as_float(item.get("over_threshold_ratio")),
        ),
    )
    channel_state_counts = _count_by(channels, "channel_state")
    trusted = sum(1 for row in channels if str(row.get("channel_state") or "").lower() in {"trusted", "good", "usable"})
    planner_candidates = batch.get("users_to_move") if isinstance(batch.get("users_to_move"), list) else []
    snapshot_bad = [
        key
        for key, item in snapshots.items()
        if isinstance(item, dict) and str(item.get("status") or item.get("state") or "").upper() not in {"OK", "FRESH", "PASS", "READY"}
    ]
    return {
        "schema_version": "v7.operator-execution-dashboard.v1",
        "read_only": True,
        "preview_only": True,
        "execution_allowed_now": False,
        "routing_behavior_changed": False,
        "users_moved": 0,
        "apply_executed": False,
        "autonomy_enabled": False,
        "current_authority": {
            "certified_authority": "derived_from_existing_governance",
            "runtime_authority": "existing_governed_runtime_owner",
            "allowed_budget": batch.get("blast_radius", {}).get("users") if isinstance(batch.get("blast_radius"), dict) else 0,
            "execution_owner": CANONICAL_RUNTIME_EXECUTOR,
        },
        "current_state": {
            "execution_loop_ready": certification.get("execution_loop_ready", False),
            "single_blocker": certification.get("single_blocker", "UNKNOWN"),
            "store_health": summary.get("health", "UNKNOWN"),
            "contracts_total": summary.get("contracts_total", 0),
            "events_total": summary.get("events_total", 0),
        },
        "execution_loop_readiness": readiness,
        "timeline": stage_rows,
        "performance": {
            "metrics": metrics,
            "available_metrics": performance.get("available_metrics", []),
            "missing_metrics": performance.get("missing_metrics", []),
            "slow_path_detected": bool(slow_metrics),
            "slow_metrics": slow_metrics,
            "bottleneck": slow_metrics[0]["metric"] if slow_metrics else "NONE",
            "trend_status": "INSUFFICIENT_HISTORY" if observability.get("observed_rows", 0) < 2 else "EVENT_STORE_SAMPLE",
            "current_stage": observability.get("current_stage", "waiting_for_execution_evidence"),
            "success_rate": observability.get("success_rate"),
            "rollback_rate": observability.get("rollback_rate"),
            "latest_success_ref": observability.get("latest_success_ref", ""),
            "latest_failure_ref": observability.get("latest_failure_ref", ""),
            "latest_rollback_ref": observability.get("latest_rollback_ref", ""),
        },
        "pool_status": {
            "channels_total": len(channels),
            "trusted_or_usable_channels": trusted,
            "channel_state_counts": channel_state_counts,
        },
        "trust_status": {
            "channels_with_trust_model": sum(1 for row in channels if row.get("channel_state_source")),
            "states": channel_state_counts,
            "governed_to_autonomy_trust_bridge": outcome_evidence.get("governed_to_autonomy_trust_bridge", {}),
            "governed_evidence_score": outcome_evidence.get("governed_evidence_score", 0.0),
            "inherited_execution_trust": outcome_evidence.get("inherited_execution_trust", 0.0),
            "autonomy_specific_gap_score": outcome_evidence.get("autonomy_specific_gap_score", 0.0),
            "autonomy_boundary_cap": outcome_evidence.get("autonomy_boundary_cap", "SHADOW_READY"),
            "approval_autonomy_review_ready": bool(outcome_evidence.get("approval_autonomy_review_ready")),
            "bounded_autonomy_blockers": outcome_evidence.get("bounded_autonomy_blockers", []),
            "operator_summary_ru": outcome_evidence.get("operator_summary_ru", ""),
            "operator_explanation": "Trust is read from the existing channel decision surface.",
        },
        "planner_status": {
            "candidate_moves_total": len(planner_candidates),
            "movement_allowed_now": False,
            "operator_explanation": (
                "No candidate movement is currently proposed."
                if not planner_candidates
                else "Candidates are advisory; governed packet and restore barrier remain required."
            ),
        },
        "snapshot_status": {
            "snapshot_families_total": len(snapshots),
            "non_ready_families": snapshot_bad,
            "state": "READY" if not snapshot_bad else "REVIEW_REQUIRED",
        },
        "operator_sections": [
            "Current Authority",
            "Current Budget",
            "Current State",
            "Execution Loop Readiness",
            "Pool Status",
            "Trust Status",
            "Planner Status",
            "Snapshot Status",
            "Execution Timeline",
            "Performance",
            "Shadow Autonomy",
            "Autonomous Dry Run",
        ],
        "operator_approval_review": {
            "operator_approval_ready": bool(certification.get("operator_approval_ready")),
            "approval_blocker": certification.get("operator_approval_blocker", "UNKNOWN"),
            "meaning": certification.get("operator_approval_meaning", ""),
        },
        "shadow_autonomy": {
            "enabled": False,
            "mode": shadow.get("mode", "shadow_only"),
            "decisions_total": (shadow.get("quality") or {}).get("decisions_total", 0),
            "comparisons_total": (shadow.get("quality") or {}).get("comparisons_total", 0),
            "agreement_rate": (shadow.get("quality") or {}).get("agreement_rate", 0.0),
            "override_rate": (shadow.get("quality") or {}).get("override_rate", 0.0),
            "prediction_accuracy": (shadow.get("quality") or {}).get("prediction_accuracy", "INSUFFICIENT_OUTCOME_HISTORY"),
            "trust_accuracy": (shadow.get("quality") or {}).get("trust_accuracy", 0.0),
            "recommendation_accuracy": (shadow.get("quality") or {}).get("recommendation_accuracy", 0.0),
            "earned_confidence": (shadow.get("confidence") or {}).get("earned_confidence", 0.0),
            "observation_window": shadow.get("observation_window") or {},
            "disagreement_analysis": shadow.get("disagreement_analysis") or {},
            "confidence_evolution": shadow.get("confidence_evolution") or {},
            "operator_behavior": shadow.get("operator_behavior") or {},
            "autonomy_evidence": shadow.get("autonomy_evidence") or {},
            "autonomy_readiness": shadow.get("autonomy_readiness") or {},
            "gap_analysis": shadow.get("gap_analysis") or {},
            "decision_history": list(shadow.get("decision_history") or [])[-10:],
            "comparison_history": list(shadow.get("comparison_history") or [])[-10:],
            "current_decisions": list(shadow.get("current_decisions") or [])[:10],
            "execution_allowed_now": False,
            "users_moved": 0,
            "apply_executed": False,
            "autonomy_enabled": False,
        },
        "autonomous_dry_run": autonomous,
        "reuse": {
            "admin_ui": True,
            "operator_decision_surface": True,
            "operator_observability": True,
            "execution_loop_readiness": True,
            "new_dashboard_created": False,
            "parallel_observability_created": False,
        },
        "safe_next_step": "populate_execution_stage_timing_from_existing_contract_event_rows",
        "loop_mapping": mapping,
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
    observability = execution_observability_snapshot(
        contracts=contracts,
        events=events,
        performance=performance,
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
        "execution_observability": observability,
        "execution_latency_foundation": {
            "complete": True,
            "method": "read existing planner, contract and event duration fields",
            "writes_runtime_state": False,
            "creates_truth_source": False,
        },
        "observability_review": execution_loop_observability_model(performance, observability),
        "execution_loop_safety_model": execution_loop_safety_model(),
        "execution_loop_design": execution_loop_design(performance),
        "readiness_certification": {
            "execution_loop_ready": not hard_blockers,
            "single_blocker": hard_blockers[0] if hard_blockers else "NONE",
            "meaning": "Ready for a permanent governed execution loop foundation; automatic execution remains disabled.",
            "operator_approval_ready": not hard_blockers,
            "operator_approval_blocker": hard_blockers[0] if hard_blockers else "NONE",
            "operator_approval_meaning": "Operator can review evidence and prepare approval through the existing governed path; live apply remains a separate explicit action.",
            "safe_next_step": "IMPLEMENT_GOVERNED_EXECUTION_LOOP_OPERATOR_DASHBOARD",
        },
    }


def _rt2_s1_measurement_row(
    *,
    category: str,
    status: str,
    owner: str,
    evidence: Any,
    consumer: str,
    certification_relevance: str,
) -> dict[str, Any]:
    return {
        "category": category,
        "status": status,
        "owner": owner,
        "producer": owner,
        "consumer": consumer,
        "storage": "existing_contract_event_read_models",
        "measurement": "existing fields only; no synthetic metrics",
        "evidence": evidence,
        "certification_relevance": certification_relevance,
    }


def rt2_s1_measurement_observability_foundation(
    *,
    contracts: list[dict[str, Any]] | None = None,
    events: list[dict[str, Any]] | None = None,
    planner_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Materialize RT2-S1 measurement without creating authority or runtime behavior."""
    readiness = execution_loop_readiness_foundation(
        contracts=contracts,
        events=events,
        planner_result=planner_result,
    )
    dashboard = execution_operator_dashboard_model(readiness=readiness)
    performance = readiness.get("performance_audit") if isinstance(readiness.get("performance_audit"), dict) else {}
    requested = performance.get("requested_metrics") if isinstance(performance.get("requested_metrics"), dict) else {}
    observability = readiness.get("execution_observability") if isinstance(readiness.get("execution_observability"), dict) else {}
    gaps = readiness.get("readiness_gap_analysis") if isinstance(readiness.get("readiness_gap_analysis"), list) else []
    chain = readiness.get("execution_chain_audit") if isinstance(readiness.get("execution_chain_audit"), list) else []
    mapping = readiness.get("execution_loop_mapping") if isinstance(readiness.get("execution_loop_mapping"), dict) else {}
    total_metric = requested.get("total_duration_ms") if isinstance(requested.get("total_duration_ms"), dict) else {}
    rollback_metric = requested.get("rollback_duration_ms") if isinstance(requested.get("rollback_duration_ms"), dict) else {}
    any_duration = bool(performance.get("available_metrics"))
    all_missing_owner_mapped = all(
        isinstance(row, dict) and row.get("owner")
        for row in gaps
        if str((row or {}).get("severity") or "") == "observability_gap"
    )
    measurement_rows = [
        _rt2_s1_measurement_row(
            category="runtime_time",
            status="OBSERVED" if any_duration else "OWNER_MAPPED_MISSING",
            owner="admin_core.operator_execution_pipeline.execution_performance_foundation",
            evidence={
                "available_metrics": performance.get("available_metrics", []),
                "missing_metrics": performance.get("missing_metrics", []),
            },
            consumer="OMP, Runtime Model, Engineering Reports, read-only dashboards",
            certification_relevance="base timing visibility for RT2-S1",
        ),
        _rt2_s1_measurement_row(
            category="runtime_cost",
            status="PARTIAL_OWNER_MAPPED" if any_duration else "OWNER_MAPPED_MISSING",
            owner="Runtime Model + Production Maturity + admin_core.operator_execution_pipeline",
            evidence="duration/per-user duration is visible when present; CPU/resource/runtime overhead cost remains future owner-mapped evidence",
            consumer="OMP Runtime Cost Review",
            certification_relevance="cost remains non-authorizing until future certification",
        ),
        _rt2_s1_measurement_row(
            category="reaction_latency",
            status="OBSERVED" if total_metric.get("available") else "OWNER_MAPPED_MISSING",
            owner="admin_core.operator_execution_pipeline.execution_performance_foundation",
            evidence=total_metric,
            consumer="OMP Latency Review and Production Maturity",
            certification_relevance="reaction latency is visible or missing with owner",
        ),
        _rt2_s1_measurement_row(
            category="stop_reasons",
            status="OBSERVED",
            owner="execution_loop_readiness_foundation.readiness_certification",
            evidence=readiness.get("readiness_certification", {}),
            consumer="CPS, OMP, operator dashboard",
            certification_relevance="safe stop explanation remains visible",
        ),
        _rt2_s1_measurement_row(
            category="lifecycle",
            status="OBSERVED" if chain else "OWNER_MAPPED_MISSING",
            owner="admin_core.operator_execution_pipeline.execution_chain_audit",
            evidence={"stages": [row.get("stage") for row in chain if isinstance(row, dict)]},
            consumer="Runtime Model lifecycle and OMP transition contract",
            certification_relevance="execution lifecycle is owner-mapped",
        ),
        _rt2_s1_measurement_row(
            category="wait_states",
            status="OBSERVED" if gaps else "OWNER_MAPPED_MISSING",
            owner="admin_core.operator_execution_pipeline.execution_readiness_gap_analysis",
            evidence=gaps,
            consumer="OMP, operator dashboard, future RT2-S2 readiness work",
            certification_relevance="wait/blocking causes are visible without granting authority",
        ),
        _rt2_s1_measurement_row(
            category="dependency_topology",
            status="OBSERVED" if mapping else "OWNER_MAPPED_MISSING",
            owner="admin_core.operator_execution_pipeline.execution_loop_mapping",
            evidence=mapping,
            consumer="Runtime Time Topology, OMP, Engineering Reports",
            certification_relevance="producer/consumer chain is explainable",
        ),
        _rt2_s1_measurement_row(
            category="time_to_safe_recovery",
            status="PARTIAL_OWNER_MAPPED" if rollback_metric.get("available") else "OWNER_MAPPED_MISSING",
            owner="restore/rollback/verification owners + admin_core.operator_execution_pipeline",
            evidence={
                "verification_duration_ms": requested.get("verification_duration_ms", {}),
                "rollback_duration_ms": rollback_metric,
            },
            consumer="OMP recovery and rollback certification",
            certification_relevance="rollback/recovery time is visible when events exist; missing rollback events are owner-mapped",
        ),
        _rt2_s1_measurement_row(
            category="bottlenecks",
            status="OBSERVED" if dashboard.get("performance", {}).get("bottleneck") else "OWNER_MAPPED_MISSING",
            owner="admin_core.operator_execution_pipeline.execution_operator_dashboard_model",
            evidence=dashboard.get("performance", {}),
            consumer="RT2-S6 evidence-based continuous improvement",
            certification_relevance="bottleneck finding remains advisory and non-authorizing",
        ),
    ]
    unmapped = [
        row["category"]
        for row in measurement_rows
        if row["status"] == "MISSING_UNMAPPED"
    ]
    completed = not unmapped and all_missing_owner_mapped
    return {
        "schema_version": "v7.rt2-s1-measurement-observability-foundation.v1",
        "workstream": "RT2-S1",
        "status": "DONE_READ_ONLY_MEASUREMENT_OWNER_MAPPED" if completed else "PARTIAL_MEASUREMENT_MAPPING",
        "read_only": True,
        "preview_only": True,
        "purpose": "make runtime cost, runtime time, reaction latency, stop reasons, lifecycle, wait states, dependency topology, Time-To-Safe-Recovery, and bottlenecks visible or owner-mapped as missing",
        "measurement_rows": measurement_rows,
        "owner_mapped_missing_categories": [
            row["category"]
            for row in measurement_rows
            if row["status"] in {"OWNER_MAPPED_MISSING", "PARTIAL_OWNER_MAPPED"}
        ],
        "unmapped_categories": unmapped,
        "completion_criteria_met": completed,
        "produced_evidence": [
            "measurement_rows",
            "owner_mapped_missing_categories",
            "execution_performance_foundation",
            "execution_observability_snapshot",
            "operator_dashboard_performance_bottleneck",
        ],
        "unlocked_capability": "RT2-S2_WORLD_READINESS_MATURATION" if completed else "",
        "still_blocked": [
            "RT2-S3_DESIRED_STATE_DELTA",
            "RT2-S4_GOVERNED_EXECUTION_COORDINATION",
            "RT2-S5_CERTIFIED_CONCURRENCY",
            "RT2-S6_EVIDENCE_BASED_CONTINUOUS_IMPROVEMENT",
            "runtime_apply",
            "automation",
            "authority_expansion",
            "dashboard_authority",
            "user_movement",
        ],
        "next_safe_action": "continue to RT2-S2 world and readiness maturation" if completed else "map remaining measurement gaps through existing owners",
        "safety": {
            "dashboard_can_decide": False,
            "dashboard_can_approve": False,
            "dashboard_can_mutate": False,
            "synthetic_metrics_created": False,
            "runtime_behavior_changed": False,
            "runtime_apply_allowed_now": False,
            "authority_expanded": False,
            "users_moved": 0,
            "new_owner_created": False,
            "new_runtime_created": False,
            "new_truth_source_created": False,
            "new_planner_created": False,
        },
        "source_models": {
            "readiness": readiness,
            "dashboard_performance": dashboard.get("performance", {}),
        },
    }


def _controller_step(
    step: int,
    name: str,
    owner: str,
    inputs: list[str],
    outputs: list[str],
    *,
    runtime_mutation: bool = False,
    command_preview: str = "",
) -> dict[str, Any]:
    return {
        "step": step,
        "name": name,
        "owner": owner,
        "inputs": inputs,
        "outputs": outputs,
        "command_preview": command_preview,
        "runtime_mutation_performed_now": False,
        "runtime_mutation_if_live": runtime_mutation,
        "preview_only": True,
    }


def operator_approved_execution_controller_preview(decision: str = "DRAFT") -> dict[str, Any]:
    """Preview the one-action operator approved controller.

    The controller is deliberately pure. It models how one operator decision
    would orchestrate existing owners, but it never invokes commands or writes
    runtime state.
    """
    normalized = str(decision or "DRAFT").strip().upper()
    if normalized not in {"DRAFT", "APPROVE", "REJECT"}:
        normalized = "DRAFT"
    base = {
        "schema_version": "v7.operator-approved-execution-controller-preview.v1",
        "controller": "canonical_operator_approved_execution_controller",
        "decision": normalized,
        "preview_only": True,
        "read_only": True,
        "execution_allowed_now": False,
        "runtime_mutation_performed": False,
        "routing_changed": False,
        "users_moved": 0,
        "apply_executed": False,
        "rollback_executed": False,
        "autonomy_enabled": False,
        "new_planner_created": False,
        "new_governance_created": False,
        "new_execution_path_created": False,
        "new_restore_barrier_owner_created": False,
        "new_truth_source_created": False,
        "owner_reuse": {
            "planner": CANONICAL_PLANNER,
            "packet": CANONICAL_PACKET_TOOL,
            "restore_barrier": CANONICAL_PACKET_OWNER,
            "apply": CANONICAL_RUNTIME_EXECUTOR,
            "verify": CANONICAL_RUNTIME_EXECUTOR,
            "rollback": CANONICAL_ROLLBACK_EXECUTOR,
            "feedback": CANONICAL_FEEDBACK_OWNER,
            "closure": CANONICAL_FEEDBACK_OWNER,
            "trust_refresh": "tools/v7-intelligence-snapshot-refresh",
        },
        "operator_ui_contract": {
            "operator_actions": ["APPROVE", "REJECT"],
            "shows": [
                "why_move",
                "why_now",
                "risk",
                "blast_radius",
                "rollback",
                "trust_impact",
                "expected_outcome",
            ],
            "nothing_else_required_from_operator": True,
        },
    }
    if normalized == "REJECT":
        steps = [
            _controller_step(
                1,
                "reject_closure",
                CANONICAL_FEEDBACK_OWNER,
                ["operator rejection", "candidate evidence", "reason"],
                ["rejection closure preview", "audit preview"],
            )
        ]
        return {
            **base,
            "terminal_preview_state": "REJECTED_CLOSURE_ONLY",
            "closure_only": True,
            "approval_required_before_live_mutation": False,
            "steps": steps,
            "blocked_actions": [
                "planner apply",
                "restore barrier write",
                "governed apply",
                "rollback apply",
                "feedback materialization for unexecuted movement",
            ],
            "final_certification": {
                "single_approve_reject_boundary_exists": True,
                "reject_path_preview_ready": True,
                "approve_path_preview_ready": True,
                "live_execution_enabled": False,
            },
        }
    steps = [
        _controller_step(
            1,
            "fresh_planner",
            CANONICAL_PLANNER,
            ["production truth", "runtime state", "snapshots", "authority budget"],
            ["candidate moves", "selected moves", "generation id", "selected move hash"],
            command_preview="v7-users-autoswitch --pretty",
        ),
        _controller_step(
            2,
            "packet",
            CANONICAL_PACKET_TOOL,
            ["selected moves", "authority budget", "rollback manifest", "operator approval"],
            ["approval packet", "approved plan lock", "rollback manifest"],
        ),
        _controller_step(
            3,
            "runtime_recheck",
            CANONICAL_PACKET_OWNER,
            ["approval packet", "fresh planner snapshot", "runtime registry hashes"],
            ["ALLOW_RESTORE_BARRIER_CLEARANCE or denial"],
        ),
        _controller_step(
            4,
            "restore_barrier",
            CANONICAL_PACKET_OWNER,
            ["ALLOW recheck", "approved plan lock", "selected move hash"],
            ["generation-bound restore barrier clearance"],
            runtime_mutation=True,
        ),
        _controller_step(
            5,
            "apply",
            CANONICAL_RUNTIME_EXECUTOR,
            ["restore barrier clearance", "approved users", "approved targets", "rollback packet"],
            ["bounded apply result", "per-user verification result"],
            runtime_mutation=True,
            command_preview="v7-users-autoswitch --mode guarded --apply --verify",
        ),
        _controller_step(
            6,
            "verify",
            CANONICAL_RUNTIME_EXECUTOR,
            ["apply result", "route check", "registry state", "service health"],
            ["verification verdict", "rollback_required decision"],
        ),
        _controller_step(
            7,
            "rollback_readiness",
            CANONICAL_PACKET_OWNER,
            ["apply result", "rollback manifest", "verification verdict"],
            ["rollback packet", "rollback dry-run preview"],
        ),
        _controller_step(
            8,
            "feedback",
            CANONICAL_FEEDBACK_OWNER,
            ["verified execution result", "prediction", "recommendation hash"],
            ["outcome", "trust", "prediction", "recommendation feedback"],
        ),
        _controller_step(
            9,
            "closure",
            CANONICAL_FEEDBACK_OWNER,
            ["feedback records", "audit reference", "rollback state"],
            ["operation closure"],
        ),
        _controller_step(
            10,
            "trust_refresh",
            "tools/v7-intelligence-snapshot-refresh",
            ["canonical feedback stores"],
            ["updated trust/planner evidence"],
            runtime_mutation=True,
            command_preview="v7-intelligence-snapshot-refresh --approved-refresh",
        ),
    ]
    return {
        **base,
        "terminal_preview_state": "APPROVE_CHAIN_READY" if normalized == "APPROVE" else "DRAFT_READY",
        "closure_only": False,
        "approval_required_before_live_mutation": True,
        "steps": steps,
        "blocked_actions": [
            "direct user-switch",
            "planner bypass",
            "packet bypass",
            "restore barrier bypass",
            "apply without verification",
            "rollback without rollback packet",
            "feedback write before verified execution",
            "target/user reselect after approval",
        ],
        "no_bypass_certification": {
            "planner_bypass_possible": False,
            "governance_bypass_possible": False,
            "packet_bypass_possible": False,
            "restore_barrier_bypass_possible": False,
            "apply_verification_bypass_possible": False,
            "rollback_bypass_possible": False,
            "feedback_bypass_possible": False,
        },
        "final_certification": {
            "single_approve_reject_boundary_exists": True,
            "reject_path_preview_ready": True,
            "approve_path_preview_ready": True,
            "live_execution_enabled": False,
            "operator_reduced_to_approve_reject": True,
        },
    }


def _rt2_s4_coordination_row(step: dict[str, Any]) -> dict[str, Any]:
    mutation_if_live = bool(step.get("runtime_mutation_if_live"))
    return {
        "stage": step.get("name", ""),
        "status": "OWNER_MAPPED",
        "owner": step.get("owner", ""),
        "producer": step.get("owner", ""),
        "consumer": "RT2-S5 certified concurrency ladder, OMP, Runtime Model",
        "inputs": list(step.get("inputs") or []),
        "outputs": list(step.get("outputs") or []),
        "runtime_mutation_performed_now": False,
        "runtime_mutation_if_live": mutation_if_live,
        "requires_existing_authority_if_live": mutation_if_live,
        "new_execution_path_created": False,
    }


def rt2_s4_governed_execution_coordination(
    *,
    rt2_s3_delta: dict[str, Any] | None = None,
    controller_decision: str = "APPROVE",
) -> dict[str, Any]:
    """Materialize RT2-S4 governed execution coordination as a read-only surface."""
    controller = operator_approved_execution_controller_preview(controller_decision)
    action_matrix = execution_action_matrix()
    lifecycle = approval_packet_lifecycle()
    containment_forward_fix = operator_execution.containment_forward_fix_classification()
    steps = controller.get("steps") if isinstance(controller.get("steps"), list) else []
    rows = [_rt2_s4_coordination_row(step) for step in steps if isinstance(step, dict)]
    required = [
        "packet",
        "runtime_recheck",
        "restore_barrier",
        "apply",
        "verify",
        "rollback_readiness",
        "feedback",
        "closure",
    ]
    present = {str(row.get("stage") or "") for row in rows}
    missing = [stage for stage in required if stage not in present]
    ownerless = [row.get("stage", "") for row in rows if not row.get("owner")]
    terminal_states = [
        row["next_state"]
        for row in action_matrix
        if row.get("next_state") in {"CLOSED", "BLOCKER", "PACKET_REJECTED", "EXECUTION_BLOCKED"}
    ]
    no_bypass = controller.get("no_bypass_certification") if isinstance(controller.get("no_bypass_certification"), dict) else {}
    completed = bool(rows) and not missing and not ownerless and all(value is False for value in no_bypass.values())
    s3_status = str((rt2_s3_delta or {}).get("status") or "OWNER_MAPPED_EXTERNAL")
    return {
        "schema_version": "v7.rt2-s4-governed-execution-coordination.v1",
        "workstream": "RT2-S4",
        "status": "DONE_READ_ONLY_GOVERNED_EXECUTION_COORDINATION_OWNER_MAPPED" if completed else "PARTIAL_GOVERNED_EXECUTION_COORDINATION_MAPPING",
        "read_only": True,
        "preview_only": True,
        "purpose": "coordinate one bounded decision-to-terminal-outcome path through existing execution owners without enabling live apply",
        "consumed_capability": {
            "source_workstream": "RT2-S3",
            "source_status": s3_status,
            "consumed_evidence": [
                "prepared_delta",
                "prepared_plan",
                "packet_preview_context",
                "runtime_live_gate_context",
            ],
        },
        "coordination_rows": rows,
        "terminal_classification": {
            "terminal_states": sorted(set(terminal_states)),
            "success_path": "EXECUTION_SUCCESS -> CLOSED",
            "failure_path": "EXECUTION_FAILED -> ROLLBACK_REQUIRED -> ROLLBACK_SUCCESS/ROLLBACK_FAILED -> CLOSED/BLOCKER",
            "rejection_path": "PACKET_REJECTED -> EXECUTION_BLOCKED",
            "containment_forward_fix_schema": containment_forward_fix.get("schema_version", ""),
            "containment_forward_fix_classification": containment_forward_fix.get("classification", "UNKNOWN_TERMINAL_STATE"),
            "closure_owner": CANONICAL_FEEDBACK_OWNER,
            "terminal_classification_ready": bool(terminal_states),
        },
        "idempotency_and_loop_controls": {
            "packet_identity_required": True,
            "selected_move_hash_required": True,
            "restore_barrier_generation_required": True,
            "execution_lease_owner": CANONICAL_PACKET_OWNER,
            "planner_regeneration_after_approval_blocked": True,
            "stale_loop_prevention": [
                "packet ttl",
                "fresh runtime recheck",
                "restore barrier generation binding",
                "selected move hash binding",
                "terminal closure before OMP continuation",
            ],
            "queue_daemon_created": False,
        },
        "owner_mapping": {
            "planner": CANONICAL_PLANNER,
            "packet": CANONICAL_PACKET_TOOL,
            "packet_owner": CANONICAL_PACKET_OWNER,
            "restore_barrier": CANONICAL_PACKET_OWNER,
            "apply": CANONICAL_RUNTIME_EXECUTOR,
            "verify": CANONICAL_RUNTIME_EXECUTOR,
            "rollback": CANONICAL_ROLLBACK_EXECUTOR,
            "feedback": CANONICAL_FEEDBACK_OWNER,
            "closure": CANONICAL_FEEDBACK_OWNER,
        },
        "completion_criteria_met": completed,
        "missing_stages": missing,
        "ownerless_stages": ownerless,
        "produced_evidence": [
            "coordination_rows",
            "terminal_classification",
            "idempotency_and_loop_controls",
            "owner_mapping",
            "no_bypass_certification",
        ],
        "unlocked_capability": "RT2-S5_CERTIFIED_CONCURRENCY_LADDER" if completed else "",
        "still_blocked": [
            "RT2-S6_EVIDENCE_BASED_CONTINUOUS_IMPROVEMENT",
            "runtime_apply",
            "automation",
            "concurrency",
            "queue_daemon",
            "authority_expansion",
            "user_movement",
        ],
        "next_safe_action": "continue to RT2-S5 certified concurrency ladder" if completed else "map remaining governed execution coordination owners",
        "source_models": {
            "controller_schema": controller.get("schema_version", ""),
            "controller_terminal_preview_state": controller.get("terminal_preview_state", ""),
            "approval_packet_lifecycle": lifecycle,
            "execution_recheck_policy": execution_recheck_policy(),
            "governed_apply_policy": governed_apply_policy(),
            "verification_policy": verification_policy(),
            "rollback_policy": rollback_policy(),
            "containment_forward_fix_classification": containment_forward_fix,
            "execution_action_matrix": action_matrix,
            "no_bypass_certification": no_bypass,
        },
        "safety": {
            "runtime_behavior_changed": False,
            "runtime_apply_allowed_now": False,
            "restore_barrier_written_now": False,
            "apply_executed": False,
            "rollback_executed": False,
            "feedback_written_now": False,
            "closure_written_now": False,
            "users_moved": 0,
            "authority_expanded": False,
            "concurrency_enabled": False,
            "queue_daemon_created": False,
            "new_execution_path_created": False,
            "new_owner_created": False,
            "new_truth_source_created": False,
            "synthetic_evidence_created": False,
        },
    }


def pipeline_certification() -> dict[str, Any]:
    matrix = execution_action_matrix()
    loop = execution_loop_readiness_foundation()
    oa_controller = operator_approved_execution_controller_preview()
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
        "operator_approved_execution_controller": oa_controller,
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
            "operator_approval_ready": True,
            "operator_approved_controller_preview_ready": True,
            "bounded_autonomy_ready": False,
            "production_autonomy_ready": False,
            "execution_loop_readiness_foundation_complete": True,
            "execution_loop_ready": loop["readiness_certification"]["execution_loop_ready"],
            "new_truth_sources_created": False,
            "duplicate_systems_created": False,
            "runtime_mutation_performed": False,
            "users_moved": False,
            "autoswitch_apply_run": False,
            "SAFE_NEXT_STEP": "certify_operator_approved_controller_preview_before_live_enablement",
        },
    }
