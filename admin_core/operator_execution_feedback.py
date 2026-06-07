"""Execution feedback contracts for governed operator movement.

The module is pure: it builds append-only records that callers may write into
existing audit/event/closure stores. It does not execute movement, approve
governance, create snapshot roots, or call runtime tools.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any


SCHEMA_VERSION = "v7.operator-execution-feedback.v1"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return default if number != number else number


def classify_outcome(result: dict[str, Any] | None = None, verification: dict[str, Any] | None = None) -> str:
    row = result if isinstance(result, dict) else {}
    verify = verification if isinstance(verification, dict) else {}
    text = " ".join(
        str(value).lower()
        for value in [
            row.get("outcome_status"),
            row.get("status"),
            row.get("result"),
            row.get("error"),
            row.get("message"),
            verify.get("status"),
            verify.get("result"),
            verify.get("error"),
        ]
        if value is not None
    )
    if row.get("rollback_required") or verify.get("rollback_required") or "rollback" in text:
        return "rollback_required"
    if row.get("partial_success") or verify.get("partial_success") or "partial" in text:
        return "partial_success"
    if row.get("success") is True or verify.get("success") is True or any(token in text for token in ("success", "applied", "verified", "pass")):
        return "success"
    if row.get("success") is False or verify.get("success") is False or any(token in text for token in ("failed", "failure", "error", "denied")):
        return "failure"
    return "unknown"


def feedback_deltas(outcome_status: str, prediction_expected: float = 0.0, prediction_actual: float = 0.0) -> dict[str, float]:
    miss = abs(as_float(prediction_expected) - as_float(prediction_actual))
    if outcome_status == "success":
        trust_delta = 1.0
        recommendation_delta = 1.0
    elif outcome_status == "partial_success":
        trust_delta = 0.25
        recommendation_delta = 0.25
    elif outcome_status == "rollback_required":
        trust_delta = -1.0
        recommendation_delta = -0.75
    elif outcome_status == "failure":
        trust_delta = -1.5
        recommendation_delta = -1.0
    else:
        trust_delta = 0.0
        recommendation_delta = 0.0
    prediction_delta = max(-1.0, min(1.0, 1.0 - miss)) if outcome_status != "unknown" else 0.0
    return {
        "trust_delta": round(trust_delta, 3),
        "prediction_delta": round(prediction_delta, 3),
        "recommendation_delta": round(recommendation_delta, 3),
    }


def execution_feedback_contract(
    *,
    user: str,
    source_channel: str,
    target_channel: str,
    execution_result: dict[str, Any] | None = None,
    verification_result: dict[str, Any] | None = None,
    rollback_result: dict[str, Any] | None = None,
    recommendation_hash: str = "",
    prediction_expected: float = 0.0,
    prediction_actual: float = 0.0,
    audit_reference: str = "",
    closure_reference: str = "",
    execution_time: str = "",
    verification_time: str = "",
    stability_window_seconds: int = 0,
) -> dict[str, Any]:
    execution_result = execution_result if isinstance(execution_result, dict) else {}
    verification_result = verification_result if isinstance(verification_result, dict) else {}
    rollback_result = rollback_result if isinstance(rollback_result, dict) else {}
    outcome_status = classify_outcome(execution_result, verification_result)
    deltas = feedback_deltas(outcome_status, prediction_expected, prediction_actual)
    now = utc_now()
    contract = {
        "schema_version": SCHEMA_VERSION,
        "user": str(user or ""),
        "source_channel": str(source_channel or ""),
        "target_channel": str(target_channel or ""),
        "execution_time": execution_time or str(execution_result.get("execution_time") or execution_result.get("created_at") or now),
        "verification_time": verification_time or str(verification_result.get("verification_time") or verification_result.get("created_at") or now),
        "outcome_status": outcome_status,
        "execution_outcome": execution_result,
        "verification_result": verification_result,
        "rollback_result": rollback_result,
        "trust_delta": deltas["trust_delta"],
        "prediction_delta": deltas["prediction_delta"],
        "recommendation_delta": deltas["recommendation_delta"],
        "trust_feedback": {
            "subject": target_channel,
            "delta": deltas["trust_delta"],
            "reason": outcome_status,
        },
        "prediction_feedback": {
            "prediction_expected": prediction_expected,
            "prediction_actual": prediction_actual,
            "delta": deltas["prediction_delta"],
            "outcome": outcome_status,
        },
        "recommendation_feedback": {
            "recommendation_hash": recommendation_hash,
            "delta": deltas["recommendation_delta"],
            "outcome": outcome_status,
        },
        "audit_reference": audit_reference,
        "closure_reference": closure_reference,
        "stability_window_seconds": int(stability_window_seconds or 0),
        "runtime_mutation_performed": False,
        "new_truth_sources_created": False,
    }
    contract["feedback_id"] = "execfb_" + stable_hash({
        "user": contract["user"],
        "source_channel": contract["source_channel"],
        "target_channel": contract["target_channel"],
        "recommendation_hash": recommendation_hash,
        "outcome_status": outcome_status,
        "execution_time": contract["execution_time"],
    })[:24]
    return contract


def materialized_feedback_records(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    base = {
        "feedback_id": contract.get("feedback_id", ""),
        "user": contract.get("user", ""),
        "source_channel": contract.get("source_channel", ""),
        "target_channel": contract.get("target_channel", ""),
        "outcome_status": contract.get("outcome_status", "unknown"),
        "audit_reference": contract.get("audit_reference", ""),
        "closure_reference": contract.get("closure_reference", ""),
        "stability_window_seconds": int(contract.get("stability_window_seconds") or 0),
        "created_at": utc_now(),
    }
    return {
        "outcome": {
            "schema_version": "v7.execution-outcome-record.v1",
            **base,
            "execution_outcome": contract.get("execution_outcome", {}),
            "verification_result": contract.get("verification_result", {}),
            "rollback_result": contract.get("rollback_result", {}),
        },
        "trust": {
            "schema_version": "v7.execution-trust-feedback.v1",
            **base,
            **(contract.get("trust_feedback") or {}),
        },
        "prediction": {
            "schema_version": "v7.execution-prediction-feedback.v1",
            **base,
            **(contract.get("prediction_feedback") or {}),
        },
        "recommendation": {
            "schema_version": "v7.execution-recommendation-feedback.v1",
            **base,
            **(contract.get("recommendation_feedback") or {}),
        },
        "closure": {
            "schema_version": "v7.execution-feedback-closure.v1",
            "object_type": "execution_feedback",
            "object_id": contract.get("feedback_id", ""),
            "closure_state": "CLOSED" if contract.get("outcome_status") != "unknown" else "OPEN",
            "closure_reason": f"execution feedback materialized: {contract.get('outcome_status', 'unknown')}",
            "closure_actor": "operator_execution_feedback",
            "closure_timestamp": utc_now(),
            **base,
        },
    }


def recommendation_approval_packet(row: dict[str, Any], *, actor: str = "", now: str = "") -> dict[str, Any]:
    now = now or utc_now()
    user = str(row.get("user") or row.get("ip") or "")
    current = str(row.get("current_channel") or row.get("current") or "")
    target = str(row.get("recommended_channel") or row.get("target") or "")
    recommendation_hash = str(row.get("recommendation_hash") or row.get("hash") or "")
    packet = {
        "schema_version": "v7.operator-recommendation-approval-intent.v1",
        "created_at": now,
        "created_by": actor or "operator",
        "user": user,
        "current_channel": current,
        "recommended_channel": target,
        "recommendation_hash": recommendation_hash,
        "confidence": row.get("confidence", 0.0),
        "trust": row.get("trust", 0.0),
        "risk": row.get("risk", 0.0),
        "prediction": row.get("prediction") if isinstance(row.get("prediction"), dict) else {},
        "source_hashes": {
            "source_hash": str(row.get("source_hash") or ""),
            "recommendation_hash": recommendation_hash,
        },
        "approval_packet_required": True,
        "execution_allowed_now": False,
        "next_state": "EXECUTION_RECHECK_REQUIRED",
        "required_executor": "tools/v7-operator-execution-packet + tools/v7-users-autoswitch --apply --verify",
        "blocked_actions": ["direct_user_switch", "autoswitch_apply_without_restore_barrier", "execution_without_rollback_packet"],
    }
    packet["approval_intent_id"] = "apprint_" + stable_hash(packet)[:24]
    return packet
