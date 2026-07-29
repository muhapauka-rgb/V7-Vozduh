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
OUTCOME_QUALITY_SCHEMA_VERSION = "v7.decision-outcome-quality.v1"
LEARNING_RECORD_SCHEMA_VERSION = "v7.decision-outcome-learning-record.v1"
TERMINAL_OUTCOME_SUCCESS = "SUCCESS"
TERMINAL_OUTCOME_ROLLBACK_SUCCESS = "ROLLBACK_SUCCESS"
TERMINAL_OUTCOME_ROLLBACK_FAILURE = "ROLLBACK_FAILURE"
TERMINAL_OUTCOME_APPLY_FAILURE = "APPLY_FAILURE"
TERMINAL_OUTCOME_NO_EXECUTION = "NO_EXECUTION"
TERMINAL_OUTCOME_CORRECT_STAY = "CORRECT_STAY"
TERMINAL_OUTCOME_STOP_SAFE = "STOP_SAFE"
TERMINAL_OUTCOME_NO_CANDIDATE = "NO_CANDIDATE"
TERMINAL_OUTCOME_MISSED = "MISSED"

TERMINAL_OUTCOME_ALIASES = {
    "OK": TERMINAL_OUTCOME_SUCCESS,
    "APPLIED": TERMINAL_OUTCOME_SUCCESS,
    "VERIFIED": TERMINAL_OUTCOME_SUCCESS,
    "STAY": TERMINAL_OUTCOME_CORRECT_STAY,
    "NO_CHANGE": TERMINAL_OUTCOME_CORRECT_STAY,
    "STOP_SAFE_NO_ACTION": TERMINAL_OUTCOME_STOP_SAFE,
    "RECOVERY_OBSERVED_NO_ACTION": TERMINAL_OUTCOME_STOP_SAFE,
    "DENIED": TERMINAL_OUTCOME_STOP_SAFE,
    "NO_LEGAL_CANDIDATE": TERMINAL_OUTCOME_NO_CANDIDATE,
    "OPPORTUNITY_MISSED": TERMINAL_OUTCOME_MISSED,
}


def normalize_terminal_outcome_classification(value: Any) -> str:
    """Normalize producer aliases without inventing a second outcome taxonomy."""
    explicit = str(value or "").strip().upper()
    return TERMINAL_OUTCOME_ALIASES.get(explicit, explicit)


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


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "ok", "pass", "passed", "verified", "success", "applied"}
    return bool(value)


def rollback_was_used(
    execution_result: dict[str, Any] | None = None,
    verification_result: dict[str, Any] | None = None,
    rollback_result: dict[str, Any] | None = None,
) -> bool:
    """Return true only when rollback was required or actually attempted."""
    row = execution_result if isinstance(execution_result, dict) else {}
    verify = verification_result if isinstance(verification_result, dict) else {}
    rollback = rollback_result if isinstance(rollback_result, dict) else {}
    verdict = str(
        rollback.get("rollback_verdict")
        or rollback.get("verdict")
        or row.get("rollback_verdict")
        or ""
    ).upper()
    attempted = (
        bool_value(rollback.get("rollback_attempted"))
        or bool_value(row.get("rollback_attempted"))
    )
    required = (
        bool_value(rollback.get("rollback_required"))
        or bool_value(row.get("rollback_required"))
        or bool_value(verify.get("rollback_required"))
    )
    terminal_rollback = verdict in {
        "ROLLBACK_COMPLETED",
        "ROLLED_BACK",
        "ROLLBACK_FAILED",
        "FAILED",
        "OK",
        "SUCCESS",
    }
    return attempted or required or terminal_rollback


def terminal_transaction_classification(
    execution_result: dict[str, Any] | None = None,
    verification_result: dict[str, Any] | None = None,
    rollback_result: dict[str, Any] | None = None,
) -> str:
    """Classify from final terminal transaction state, never only from apply."""
    row = execution_result if isinstance(execution_result, dict) else {}
    verify = verification_result if isinstance(verification_result, dict) else {}
    rollback = rollback_result if isinstance(rollback_result, dict) else {}
    explicit = normalize_terminal_outcome_classification(
        row.get("terminal_outcome_classification") or row.get("terminal_classification")
    )
    if explicit in {
        TERMINAL_OUTCOME_SUCCESS,
        TERMINAL_OUTCOME_ROLLBACK_SUCCESS,
        TERMINAL_OUTCOME_ROLLBACK_FAILURE,
        TERMINAL_OUTCOME_APPLY_FAILURE,
        TERMINAL_OUTCOME_NO_EXECUTION,
        TERMINAL_OUTCOME_CORRECT_STAY,
        TERMINAL_OUTCOME_STOP_SAFE,
        TERMINAL_OUTCOME_NO_CANDIDATE,
        TERMINAL_OUTCOME_MISSED,
    }:
        return explicit

    apply_result = row.get("apply_result") if isinstance(row.get("apply_result"), dict) else {}
    legacy_result = str(row.get("result") or row.get("status") or "").lower()
    if legacy_result in {"rollback_success", "rolled_back"} and not verify:
        return TERMINAL_OUTCOME_ROLLBACK_SUCCESS
    if legacy_result in {"rollback_failure", "rollback_failed"} and not verify:
        return TERMINAL_OUTCOME_ROLLBACK_FAILURE
    applied = (
        bool_value(row.get("applied"))
        or bool_value(apply_result.get("applied"))
        or str(row.get("result") or "").lower() == "applied"
        or str(row.get("status") or "").lower() == "applied"
        or legacy_result in {"ok", "success", "pass", "passed", "verified"}
    )
    apply_attempted = (
        bool_value(row.get("apply_attempted"))
        or bool_value(row.get("apply_executed"))
        or applied
        or row.get("success") is False
        or str(row.get("terminal_state") or "").upper() in {"FAILED", "DENIED"}
    )
    if not applied:
        return TERMINAL_OUTCOME_APPLY_FAILURE if apply_attempted else TERMINAL_OUTCOME_NO_EXECUTION

    verification_passed = (
        verify.get("success") is True
        or verify.get("verification_passed") is True
        or str(verify.get("status") or verify.get("result") or "").lower() in {"success", "verified", "pass", "passed"}
    )
    if verification_passed or (legacy_result in {"ok", "success", "pass", "passed", "verified"} and not verify):
        return TERMINAL_OUTCOME_SUCCESS

    rollback_verdict = str(
        rollback.get("rollback_verdict")
        or rollback.get("verdict")
        or row.get("rollback_verdict")
        or ""
    ).upper()
    rollback_required = rollback_was_used(row, verify, rollback)
    if rollback_required and rollback_verdict in {"ROLLBACK_COMPLETED", "ROLLED_BACK", "OK", "SUCCESS"}:
        return TERMINAL_OUTCOME_ROLLBACK_SUCCESS
    if rollback_required:
        return TERMINAL_OUTCOME_ROLLBACK_FAILURE
    return TERMINAL_OUTCOME_APPLY_FAILURE


def outcome_status_from_terminal(terminal_classification: str) -> str:
    return {
        TERMINAL_OUTCOME_SUCCESS: "success",
        TERMINAL_OUTCOME_ROLLBACK_SUCCESS: "rollback_success",
        TERMINAL_OUTCOME_ROLLBACK_FAILURE: "rollback_failure",
        TERMINAL_OUTCOME_APPLY_FAILURE: "failure",
        TERMINAL_OUTCOME_NO_EXECUTION: "no_execution",
        TERMINAL_OUTCOME_CORRECT_STAY: "correct_stay",
        TERMINAL_OUTCOME_STOP_SAFE: "stop_safe",
        TERMINAL_OUTCOME_NO_CANDIDATE: "no_candidate",
        TERMINAL_OUTCOME_MISSED: "missed",
    }.get(terminal_classification, "unknown")


def classify_outcome(result: dict[str, Any] | None = None, verification: dict[str, Any] | None = None) -> str:
    row = result if isinstance(result, dict) else {}
    verify = verification if isinstance(verification, dict) else {}
    terminal = normalize_terminal_outcome_classification(
        row.get("terminal_outcome_classification") or row.get("terminal_classification")
    )
    if terminal:
        return outcome_status_from_terminal(terminal)
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
    elif outcome_status in {"rollback_required", "rollback_success"}:
        trust_delta = 0.0
        recommendation_delta = -0.75
    elif outcome_status in {"failure", "rollback_failure", "missed"}:
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


def _verification_complete(verification: dict[str, Any]) -> bool:
    if not verification:
        return False
    return bool(
        verification.get("success") is True
        or verification.get("verification_passed") is True
        or str(verification.get("status") or verification.get("result") or "").lower() in {"success", "verified", "pass", "passed"}
    )


def _service_impact(result: dict[str, Any], verification: dict[str, Any], outcome_status: str) -> str:
    service_payload = verification.get("service_outcome") or verification.get("service_actual") or result.get("service_outcome")
    if isinstance(service_payload, dict):
        text = json.dumps(service_payload, sort_keys=True, ensure_ascii=True).lower()
        if any(token in text for token in ("fail", "degraded", "down", "error")):
            return "DEGRADED"
        if any(token in text for token in ("ok", "pass", "success", "improved", "verified")):
            return "IMPROVED"
    if outcome_status == "success":
        return "IMPROVED"
    if outcome_status in {"failure", "rollback_required", "rollback_success", "rollback_failure"}:
        return "DEGRADED"
    if outcome_status == "partial_success":
        return "UNCHANGED"
    return "UNKNOWN"


def _user_impact(result: dict[str, Any], verification: dict[str, Any], outcome_status: str) -> str:
    user_payload = verification.get("user_outcome") or result.get("user_outcome")
    if isinstance(user_payload, dict):
        text = json.dumps(user_payload, sort_keys=True, ensure_ascii=True).lower()
        if any(token in text for token in ("connected", "ok", "pass", "success", "improved")):
            return "IMPROVED"
        if any(token in text for token in ("failed", "offline", "degraded", "error")):
            return "DEGRADED"
    if outcome_status == "success":
        return "IMPROVED"
    if outcome_status in {"failure", "rollback_required", "rollback_success", "rollback_failure"}:
        return "DEGRADED"
    if outcome_status == "partial_success":
        return "UNCHANGED"
    return "UNKNOWN"


def outcome_quality_evaluation(
    *,
    execution_result: dict[str, Any] | None = None,
    verification_result: dict[str, Any] | None = None,
    rollback_result: dict[str, Any] | None = None,
    prediction_expected: float = 0.0,
    prediction_actual: float = 0.0,
) -> dict[str, Any]:
    """Classify a real observed outcome without creating evidence."""
    execution_result = execution_result if isinstance(execution_result, dict) else {}
    verification_result = verification_result if isinstance(verification_result, dict) else {}
    rollback_result = rollback_result if isinstance(rollback_result, dict) else {}
    terminal_classification = terminal_transaction_classification(execution_result, verification_result, rollback_result)
    outcome_status = outcome_status_from_terminal(terminal_classification)
    if terminal_classification == TERMINAL_OUTCOME_SUCCESS:
        quality = "SUCCESS"
    elif outcome_status == "partial_success":
        quality = "PARTIAL_SUCCESS"
    elif terminal_classification == TERMINAL_OUTCOME_ROLLBACK_SUCCESS:
        quality = "ROLLBACK_SUCCESS"
    elif terminal_classification == TERMINAL_OUTCOME_ROLLBACK_FAILURE:
        quality = "ROLLBACK_FAILURE"
    elif terminal_classification == TERMINAL_OUTCOME_APPLY_FAILURE:
        quality = "FAILED"
    elif terminal_classification == TERMINAL_OUTCOME_NO_EXECUTION:
        quality = "NO_EXECUTION"
    else:
        quality = "UNKNOWN"
    verification_complete = _verification_complete(verification_result)
    rollback_used = bool(
        rollback_was_used(
            execution_result,
            verification_result,
            rollback_result,
        )
        or outcome_status
        in {"rollback_required", "rollback_success", "rollback_failure"}
    )
    prediction_error = abs(as_float(prediction_expected) - as_float(prediction_actual))
    if quality == "SUCCESS" and verification_complete and prediction_error <= 0.2:
        learning_value = "HIGH"
    elif quality in {"SUCCESS", "PARTIAL_SUCCESS", "FAILED", "ROLLBACK_SUCCESS", "ROLLBACK_FAILURE"}:
        learning_value = "MEDIUM"
    else:
        learning_value = "LOW"
    return {
        "schema_version": OUTCOME_QUALITY_SCHEMA_VERSION,
        "outcome_quality": quality,
        "outcome_status": outcome_status,
        "terminal_outcome_classification": terminal_classification,
        "service_impact": _service_impact(execution_result, verification_result, outcome_status),
        "user_impact": _user_impact(execution_result, verification_result, outcome_status),
        "verification_complete": verification_complete,
        "rollback_used": rollback_used,
        "prediction_error": round(prediction_error, 4),
        "learning_value": learning_value,
        "synthetic_evidence_created": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def knowledge_growth_from_outcome(outcome_quality: dict[str, Any]) -> dict[str, Any]:
    quality = str(outcome_quality.get("outcome_quality") or "UNKNOWN")
    learning_value = str(outcome_quality.get("learning_value") or "LOW")
    rollback_used = bool(outcome_quality.get("rollback_used"))
    if quality == "SUCCESS":
        decision = "improved"
        suitability = "improved"
        prediction = "improved" if as_float(outcome_quality.get("prediction_error"), 1.0) <= 0.2 else "unchanged"
        service = "improved" if outcome_quality.get("service_impact") == "IMPROVED" else "unchanged"
        recovery = "improved" if not rollback_used else "unchanged"
    elif quality == "PARTIAL_SUCCESS":
        decision = "gained"
        suitability = "unchanged"
        prediction = "unchanged"
        service = "unchanged"
        recovery = "unchanged"
    elif quality == "FAILED":
        decision = "gained"
        suitability = "degraded"
        prediction = "degraded"
        service = "degraded" if outcome_quality.get("service_impact") == "DEGRADED" else "unchanged"
        recovery = "improved" if rollback_used else "unchanged"
    elif quality == "ROLLBACK_SUCCESS":
        decision = "gained"
        suitability = "degraded"
        prediction = "degraded"
        service = "degraded" if outcome_quality.get("service_impact") == "DEGRADED" else "unchanged"
        recovery = "improved"
    elif quality == "ROLLBACK_FAILURE":
        decision = "gained"
        suitability = "degraded"
        prediction = "degraded"
        service = "degraded" if outcome_quality.get("service_impact") == "DEGRADED" else "unchanged"
        recovery = "degraded"
    else:
        decision = suitability = prediction = service = recovery = "unchanged"
    return {
        "schema_version": "v7.decision-knowledge-growth.v1",
        "knowledge_gained": quality in {"SUCCESS", "PARTIAL_SUCCESS", "FAILED", "ROLLBACK_SUCCESS", "ROLLBACK_FAILURE"},
        "knowledge_improved": [name for name, state in {
            "Decision Outcome": decision,
            "Suitability": suitability,
            "Prediction": prediction,
            "Service": service,
            "Recovery": recovery,
        }.items() if state == "improved"],
        "knowledge_unchanged": [name for name, state in {
            "Decision Outcome": decision,
            "Suitability": suitability,
            "Prediction": prediction,
            "Service": service,
            "Recovery": recovery,
        }.items() if state == "unchanged"],
        "knowledge_degraded": [name for name, state in {
            "Decision Outcome": decision,
            "Suitability": suitability,
            "Prediction": prediction,
            "Service": service,
            "Recovery": recovery,
        }.items() if state == "degraded"],
        "by_object": {
            "Decision Outcome": decision,
            "Suitability": suitability,
            "Prediction": prediction,
            "Service": service,
            "Recovery": recovery,
            "Knowledge Quality": "improved" if learning_value in {"HIGH", "MEDIUM"} and quality != "UNKNOWN" else "unchanged",
        },
        "source": "existing_execution_feedback_outcome",
        "synthetic_evidence_created": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def decision_learning_record(contract: dict[str, Any]) -> dict[str, Any]:
    outcome_quality = contract.get("outcome_quality") if isinstance(contract.get("outcome_quality"), dict) else {}
    knowledge_growth = contract.get("knowledge_growth") if isinstance(contract.get("knowledge_growth"), dict) else {}
    record = {
        "schema_version": LEARNING_RECORD_SCHEMA_VERSION,
        "feedback_id": contract.get("feedback_id", ""),
        "recommendation_id": contract.get("recommendation_id", ""),
        "decision_id": contract.get("decision_id", ""),
        "packet_id": contract.get("packet_id", ""),
        "user": contract.get("user", ""),
        "source_channel": contract.get("source_channel", ""),
        "target_channel": contract.get("target_channel", ""),
        "outcome_quality": outcome_quality.get("outcome_quality", "UNKNOWN"),
        "terminal_outcome_classification": outcome_quality.get("terminal_outcome_classification", ""),
        "learning_value": outcome_quality.get("learning_value", "LOW"),
        "knowledge_growth": knowledge_growth,
        "trust_delta": contract.get("trust_delta", 0.0),
        "prediction_delta": contract.get("prediction_delta", 0.0),
        "recommendation_delta": contract.get("recommendation_delta", 0.0),
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
        "synthetic_evidence_created": False,
    }
    record["learning_record_id"] = "learn_" + stable_hash(record)[:24]
    return record


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
    packet_id: str = "",
    execution_time: str = "",
    verification_time: str = "",
    stability_window_seconds: int = 0,
    evidence_class: str = "",
    decision_trace_id: str = "",
    input_snapshot_identity: str = "",
    expected_terminal: str = "",
    service_failure_causal_binding: dict[str, Any] | None = None,
) -> dict[str, Any]:
    execution_result = execution_result if isinstance(execution_result, dict) else {}
    verification_result = verification_result if isinstance(verification_result, dict) else {}
    rollback_result = rollback_result if isinstance(rollback_result, dict) else {}
    terminal_classification = terminal_transaction_classification(execution_result, verification_result, rollback_result)
    outcome_status = outcome_status_from_terminal(terminal_classification)
    deltas = feedback_deltas(outcome_status, prediction_expected, prediction_actual)
    quality = outcome_quality_evaluation(
        execution_result=execution_result,
        verification_result=verification_result,
        rollback_result=rollback_result,
        prediction_expected=prediction_expected,
        prediction_actual=prediction_actual,
    )
    growth = knowledge_growth_from_outcome(quality)
    now = utc_now()
    contract = {
        "schema_version": SCHEMA_VERSION,
        "user": str(user or ""),
        "source_channel": str(source_channel or ""),
        "target_channel": str(target_channel or ""),
        "selected_moves": execution_result.get("selected_moves") if isinstance(execution_result.get("selected_moves"), list) else [{
            "user": str(user or ""),
            "from": str(source_channel or ""),
            "target": str(target_channel or ""),
            "to": str(target_channel or ""),
        }],
        "execution_time": execution_time or str(execution_result.get("execution_time") or execution_result.get("created_at") or now),
        "verification_time": verification_time or str(verification_result.get("verification_time") or verification_result.get("created_at") or now),
        "outcome_status": outcome_status,
        "terminal_outcome_classification": terminal_classification,
        "outcome_quality": quality,
        "knowledge_growth": growth,
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
            "terminal_outcome_classification": terminal_classification,
        },
        "prediction_feedback": {
            "prediction_expected": prediction_expected,
            "prediction_actual": prediction_actual,
            "delta": deltas["prediction_delta"],
            "outcome": outcome_status,
            "terminal_outcome_classification": terminal_classification,
        },
        "recommendation_feedback": {
            "recommendation_hash": recommendation_hash,
            "delta": deltas["recommendation_delta"],
            "outcome": outcome_status,
            "terminal_outcome_classification": terminal_classification,
        },
        "audit_reference": audit_reference,
        "closure_reference": closure_reference,
        "packet_id": packet_id or str(execution_result.get("packet_id") or verification_result.get("packet_id") or ""),
        "recommendation_id": recommendation_hash,
        "stability_window_seconds": int(stability_window_seconds or 0),
        "evidence_class": str(evidence_class or ""),
        "decision_trace_id": str(decision_trace_id or ""),
        "input_snapshot_identity": str(input_snapshot_identity or ""),
        "expected_terminal": str(expected_terminal or terminal_classification),
        "service_failure_causal_binding": (
            dict(service_failure_causal_binding)
            if isinstance(service_failure_causal_binding, dict) else {}
        ),
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
    contract["decision_id"] = contract["feedback_id"]
    contract["learning_record"] = decision_learning_record(contract)
    return contract


def materialized_feedback_records(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    causal_binding = (
        contract.get("service_failure_causal_binding")
        if isinstance(contract.get("service_failure_causal_binding"), dict) else {}
    )
    base = {
        "feedback_id": contract.get("feedback_id", ""),
        "user": contract.get("user", ""),
        "source_channel": contract.get("source_channel", ""),
        "target_channel": contract.get("target_channel", ""),
        "outcome_status": contract.get("outcome_status", "unknown"),
        "terminal_outcome_classification": contract.get("terminal_outcome_classification", ""),
        "audit_reference": contract.get("audit_reference", ""),
        "closure_reference": contract.get("closure_reference", ""),
        "recommendation_id": contract.get("recommendation_id", contract.get("recommendation_hash", "")),
        "decision_id": contract.get("decision_id", contract.get("feedback_id", "")),
        "packet_id": contract.get("packet_id", ""),
        "outcome_quality": contract.get("outcome_quality", {}),
        "knowledge_growth": contract.get("knowledge_growth", {}),
        "learning_record": contract.get("learning_record", {}),
        "selected_moves": contract.get("selected_moves", []),
        "outcome_observed_at": contract.get("verification_time") or contract.get("execution_time") or utc_now(),
        "service_outcome": (contract.get("verification_result") or {}).get("service_outcome", {}),
        "user_outcome": (contract.get("verification_result") or {}).get("user_outcome", {
            "user": contract.get("user", ""),
            "source_channel": contract.get("source_channel", ""),
            "target_channel": contract.get("target_channel", ""),
            "outcome_status": contract.get("outcome_status", "unknown"),
        }),
        "stability_window_seconds": int(contract.get("stability_window_seconds") or 0),
        "evidence_class": contract.get("evidence_class", ""),
        "decision_trace_id": contract.get("decision_trace_id", ""),
        "input_snapshot_identity": contract.get("input_snapshot_identity", ""),
        "expected_terminal": contract.get("expected_terminal", ""),
        "service_failure_causal_binding": causal_binding,
        "source_incident_id": str(causal_binding.get("source_incident_id") or ""),
        "source_event_id": str(causal_binding.get("source_event_id") or ""),
        "source_event_ids": [str(item) for item in (causal_binding.get("source_event_ids") or []) if str(item)],
        "source_event_type": str(causal_binding.get("event_type") or ""),
        "source_event_observation_generation": str(causal_binding.get("observation_generation") or ""),
        "source_event_provenance": str(causal_binding.get("event_provenance") or ""),
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


def _record_outcome_quality(record: dict[str, Any]) -> dict[str, Any]:
    execution = record.get("execution_outcome") if isinstance(record.get("execution_outcome"), dict) else record
    verification = record.get("verification_result") if isinstance(record.get("verification_result"), dict) else {}
    rollback = record.get("rollback_result") if isinstance(record.get("rollback_result"), dict) else {}
    prediction_feedback = record.get("prediction_feedback") if isinstance(record.get("prediction_feedback"), dict) else record
    return outcome_quality_evaluation(
        execution_result=execution,
        verification_result=verification,
        rollback_result=rollback,
        prediction_expected=as_float(prediction_feedback.get("prediction_expected"), 0.0),
        prediction_actual=as_float(prediction_feedback.get("prediction_actual"), 0.0),
    )


def decision_outcome_learning_model(
    decision_records: list[dict[str, Any]] | None = None,
    *,
    generated_at: str = "",
) -> dict[str, Any]:
    """Aggregate existing closed outcomes into read-only learning/effectiveness."""
    rows: list[dict[str, Any]] = []
    for index, record in enumerate(decision_records or []):
        if not isinstance(record, dict):
            continue
        quality = record.get("outcome_quality") if isinstance(record.get("outcome_quality"), dict) else _record_outcome_quality(record)
        growth = record.get("knowledge_growth") if isinstance(record.get("knowledge_growth"), dict) else knowledge_growth_from_outcome(quality)
        learning = record.get("learning_record") if isinstance(record.get("learning_record"), dict) else {}
        outcome_quality = str(quality.get("outcome_quality") or "UNKNOWN")
        if outcome_quality == "UNKNOWN":
            continue
        rows.append({
            "record_index": index,
            "recommendation_id": str(record.get("recommendation_id") or record.get("recommendation_hash") or ""),
            "decision_id": str(record.get("decision_id") or record.get("operation_id") or record.get("object_id") or ""),
            "packet_id": str(record.get("packet_id") or record.get("approval_packet_id") or ""),
            "user": str(record.get("user") or record.get("ip") or ""),
            "channel": str(record.get("target_channel") or record.get("channel") or record.get("egress") or record.get("target") or ""),
            "outcome_quality": outcome_quality,
            "terminal_outcome_classification": str(quality.get("terminal_outcome_classification") or record.get("terminal_outcome_classification") or ""),
            "service_impact": quality.get("service_impact", "UNKNOWN"),
            "user_impact": quality.get("user_impact", "UNKNOWN"),
            "verification_complete": bool(quality.get("verification_complete")),
            "rollback_used": bool(quality.get("rollback_used")),
            "learning_value": quality.get("learning_value", "LOW"),
            "knowledge_growth": growth,
            "learning_record_id": learning.get("learning_record_id", ""),
        })
    total = len(rows)
    success = sum(1 for row in rows if row["outcome_quality"] == "SUCCESS")
    partial = sum(1 for row in rows if row["outcome_quality"] == "PARTIAL_SUCCESS")
    failed = sum(1 for row in rows if row["outcome_quality"] == "FAILED")
    rollback_success = sum(1 for row in rows if row["outcome_quality"] == "ROLLBACK_SUCCESS")
    rollback_failure = sum(1 for row in rows if row["outcome_quality"] == "ROLLBACK_FAILURE")
    no_execution = sum(1 for row in rows if row["outcome_quality"] == "NO_EXECUTION")
    service_improved = sum(1 for row in rows if row["service_impact"] == "IMPROVED")
    rollback_used = sum(1 for row in rows if row["rollback_used"])
    prediction_correct = sum(
        1 for row in rows
        if (row.get("knowledge_growth") or {}).get("by_object", {}).get("Prediction") == "improved"
    )
    fit_correct = sum(
        1 for row in rows
        if (row.get("knowledge_growth") or {}).get("by_object", {}).get("Suitability") == "improved"
    )
    recovery_correct = sum(
        1 for row in rows
        if (row.get("knowledge_growth") or {}).get("by_object", {}).get("Recovery") == "improved"
    )
    knowledge_improved = sorted({
        item
        for row in rows
        for item in ((row.get("knowledge_growth") or {}).get("knowledge_improved") or [])
    })
    knowledge_degraded = sorted({
        item
        for row in rows
        for item in ((row.get("knowledge_growth") or {}).get("knowledge_degraded") or [])
    })
    return {
        "schema_version": "v7.decision-outcome-learning.model.v1",
        "generated_at": generated_at or utc_now(),
        "owner": "admin_core.operator_execution_feedback",
        "source": "existing_decision_feedback_closure_records",
        "outcome_quality_counts": {
            "SUCCESS": success,
            "PARTIAL_SUCCESS": partial,
            "FAILED": failed,
            "ROLLBACK_SUCCESS": rollback_success,
            "ROLLBACK_FAILURE": rollback_failure,
            "NO_EXECUTION": no_execution,
            "UNKNOWN": 0,
        },
        "effectiveness": {
            "recommendation_correct_rate": round((success + (partial * 0.5)) / total, 4) if total else 0.0,
            "service_improved_rate": round(service_improved / total, 4) if total else 0.0,
            "rollback_rate": round(rollback_used / total, 4) if total else 0.0,
            "fit_prediction_correct_rate": round(fit_correct / total, 4) if total else 0.0,
            "recovery_prediction_correct_rate": round(recovery_correct / total, 4) if total else 0.0,
            "prediction_correct_rate": round(prediction_correct / total, 4) if total else 0.0,
        },
        "knowledge_growth": {
            "knowledge_gained": total,
            "knowledge_improved": knowledge_improved,
            "knowledge_degraded": knowledge_degraded,
            "knowledge_unchanged_count": sum(
                len((row.get("knowledge_growth") or {}).get("knowledge_unchanged") or [])
                for row in rows
            ),
        },
        "rows": rows[-50:],
        "read_only": True,
        "synthetic_evidence_created": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
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
        "ctr_packet_evidence_preview": (
            row.get("ctr_governance_evidence", {}).get("packet_preview")
            if isinstance(row.get("ctr_governance_evidence"), dict)
            and isinstance(row.get("ctr_governance_evidence", {}).get("packet_preview"), dict)
            else {}
        ),
        "ctr_governance_evidence": row.get("ctr_governance_evidence") if isinstance(row.get("ctr_governance_evidence"), dict) else {},
        "ctr_review": {
            "review_required": bool(row.get("review_required")),
            "review_required_reasons": list(row.get("review_required_reasons") or []),
            "review_category": str(row.get("review_category") or ""),
            "review_severity": str(row.get("review_severity") or ""),
            "review_recommendation": str(row.get("review_recommendation") or ""),
            "review_warning": str(row.get("review_warning") or ""),
            "review_next_action": str(row.get("review_next_action") or ""),
            "emergency_only": bool(row.get("emergency_only")),
            "approval_authority": "none",
            "denial_authority": "none",
            "packet_authority_changed": False,
            "execution_authority_changed": False,
        },
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
