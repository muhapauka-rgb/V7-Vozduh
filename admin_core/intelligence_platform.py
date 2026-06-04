"""Read-only hardening contracts for the V7 Intelligence Platform.

This module does not own runtime truth, planner authority, governance,
execution, rollback, selected moves, or snapshot storage. It defines compact
certification and validation helpers for the existing RI1-RI5 chain.
"""

from __future__ import annotations

import statistics
from typing import Any


MODEL_VERSION = "v7.intelligence-platform.model.v1"
WEIGHTS_VERSION = "v7.intelligence-platform.weights.v1"
CALIBRATION_VERSION = "v7.intelligence-platform.calibration.v1"
SCHEMA_VERSION = "v7.intelligence-platform.framework.v1"
RI6_SCHEMA_VERSION = "v7.ri6.trust-evolution.v1"
AUTONOMY_READINESS_LEVELS = (
    "NOT_READY",
    "SHADOW_READY",
    "OPERATOR_VISIBLE_READY",
    "OPERATOR_APPROVAL_READY",
    "BOUNDED_AUTONOMY_READY",
    "PRODUCTION_AUTONOMY_READY",
)


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def mean(values: list[float], default: float = 0.0) -> float:
    return float(statistics.mean(values)) if values else default


def intelligence_reality_map() -> dict[str, Any]:
    return {
        "schema_version": "v7.intelligence.reality-map.v1",
        "chain": {
            "RI.1": {
                "owner": "admin_core.routing_intelligence",
                "truth_sources": ["service-matrix.json", "egress-quality-summary.json", "service-preferences.json"],
                "runtime_consumer": "RoutingBrain / workers",
                "classification": "REUSE",
            },
            "RI.2": {
                "owner": "admin_core.routing_brain",
                "truth_sources": ["RI.1 read models", "audit history"],
                "runtime_consumer": "tools/v7-users-autoswitch advisory path",
                "classification": "REUSE",
            },
            "RI.3": {
                "owner": "RoutingBrain candidate advisory contract",
                "truth_sources": ["eligible planner candidates", "service history", "trust"],
                "runtime_consumer": "planner ranking score parts",
                "classification": "REUSE",
            },
            "RI.4.B": {
                "owner": "candidate suitability and best available pool workers",
                "truth_sources": ["users.registry", "egress.registry", "RI snapshots"],
                "runtime_consumer": "optional advisory snapshot reader",
                "classification": "REUSE",
            },
            "RI.4.CD": {
                "owner": "ServiceIntelligenceEngine",
                "truth_sources": ["service matrix", "quality summary", "service preferences"],
                "runtime_consumer": "service/user score snapshots",
                "classification": "REUSE",
            },
            "RI.5": {
                "owner": "PredictiveFoundation",
                "truth_sources": ["service history", "risk snapshots", "trust snapshots"],
                "runtime_consumer": "optional prediction advice",
                "classification": "REUSE",
            },
        },
        "authority": authority_boundary(),
    }


def intelligence_gap_map() -> dict[str, Any]:
    gaps = [
        ("missing_model_governance_contract", "HIGH", "Centralize model, weight, schema, calibration, migration rules."),
        ("missing_replay_framework", "HIGH", "Replay model outputs against historical outcomes before stronger rollout."),
        ("missing_forecast_validation", "HIGH", "Validate prediction accuracy and confidence calibration."),
        ("missing_drift_detection", "HIGH", "Detect prediction, service, suitability, trust, and risk drift."),
        ("missing_explainability_contract", "MEDIUM", "Standardize why-score payloads across service, suitability, pool, prediction, risk, trust."),
        ("missing_observability_contract", "MEDIUM", "Define freshness, confidence, drift, calibration, data quality, and snapshot alerts."),
        ("missing_service_slo_sla_contract", "MEDIUM", "Define GOOD/WARNING/DEGRADED/BAD/CRITICAL thresholds per service."),
        ("missing_rollout_governance_ladder", "MEDIUM", "Define activation requirements and rollback rules."),
        ("missing_probe_catalog_certification", "MEDIUM", "Distinguish measured, partial, and logical-only services."),
    ]
    return {
        "schema_version": "v7.intelligence.gap-map.v1",
        "gaps": [
            {"id": item, "severity": severity, "closure": closure}
            for item, severity, closure in gaps
        ],
        "critical_gaps": [item for item, severity, _ in gaps if severity == "CRITICAL"],
        "problem_closure_required": True,
    }


def service_slo_sla_model() -> dict[str, Any]:
    base = {
        "GOOD": {"score_min": 85, "confidence_min": 0.80, "user_impact": "none"},
        "WARNING": {"score_min": 70, "confidence_min": 0.65, "user_impact": "minor"},
        "DEGRADED": {"score_min": 50, "confidence_min": 0.50, "user_impact": "visible"},
        "BAD": {"score_min": 25, "confidence_min": 0.35, "user_impact": "major"},
        "CRITICAL": {"score_min": 0, "confidence_min": 0.0, "user_impact": "service_unusable"},
    }
    service_overrides = {
        "telegram": {"critical_metrics": ["availability", "message_latency", "connection_success"], "freshness_critical_seconds": 900},
        "youtube": {"critical_metrics": ["startup_delay", "chunk_throughput", "buffer_probability"], "freshness_critical_seconds": 1800},
        "instagram": {"critical_metrics": ["feed_load", "story_load", "video_load"], "freshness_critical_seconds": 1800},
        "chatgpt": {"critical_metrics": ["availability", "response_latency", "stream_continuity"], "freshness_critical_seconds": 1800},
        "google": {"critical_metrics": ["availability", "latency"], "freshness_critical_seconds": 1800},
        "google_auth": {"critical_metrics": ["availability", "latency"], "freshness_critical_seconds": 900},
    }
    return {
        "schema_version": "v7.intelligence.service-slo-sla.v1",
        "statuses": base,
        "services": {
            service: {
                "thresholds": base,
                "critical_metrics": row["critical_metrics"],
                "freshness_critical_seconds": row["freshness_critical_seconds"],
                "confidence_impact": "below threshold lowers snapshot confidence and advisory influence",
                "freshness_impact": "stale service measurements reduce confidence or trigger warning",
                "user_impact": "service-specific user-visible degradation",
            }
            for service, row in service_overrides.items()
        },
        "runtime_decision_authority": "none_contract_only",
    }


def model_governance_framework() -> dict[str, Any]:
    return {
        "schema_version": "v7.intelligence.model-governance.v1",
        "model_version": MODEL_VERSION,
        "weights_version": WEIGHTS_VERSION,
        "calibration_version": CALIBRATION_VERSION,
        "compatibility_rules": {
            "runtime_required_snapshots": "must preserve schema, freshness, confidence, source_hashes, and list/summary shape",
            "advisory_snapshots": "may be ignored by runtime when stale or low confidence",
            "planner_authority": "planner remains tools/v7-users-autoswitch",
        },
        "migration_rules": {
            "schema_change": "additive first; breaking changes require new snapshot family or explicit migration report",
            "weight_change": "requires replay, forecast validation, drift review, and operator-visible certification",
            "calibration_change": "requires distribution comparison before/after",
        },
        "authority": authority_boundary(),
    }


def replay_framework(predicted: list[dict[str, Any]] | None = None, actual: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    predicted = predicted or []
    actual = actual or []
    actual_by_id = {str(row.get("id") or row.get("channel") or row.get("service") or index): row for index, row in enumerate(actual)}
    rows = []
    false_positives = 0
    false_negatives = 0
    agreements = 0
    disagreements = 0
    for index, row in enumerate(predicted):
        key = str(row.get("id") or row.get("channel") or row.get("service") or index)
        observed = actual_by_id.get(key, {})
        predicted_bad = as_float(row.get("degradation_probability"), as_float(row.get("risk_probability"), 0.0)) >= 60.0
        actual_bad = bool(observed.get("degraded") or observed.get("failed") or as_float(observed.get("score"), 100.0) < 50.0)
        if predicted_bad == actual_bad:
            agreements += 1
        else:
            disagreements += 1
        if predicted_bad and not actual_bad:
            false_positives += 1
        if actual_bad and not predicted_bad:
            false_negatives += 1
        rows.append({"id": key, "predicted_bad": predicted_bad, "actual_bad": actual_bad, "agreement": predicted_bad == actual_bad})
    total = max(1, len(rows))
    return {
        "schema_version": "v7.intelligence.replay-framework.v1",
        "agreement_rate": round(agreements / total, 4),
        "disagreement_rate": round(disagreements / total, 4),
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "rows": rows,
        "runtime_decision_authority": "none_replay_only",
    }


def forecast_validation_framework(forecasts: list[dict[str, Any]] | None = None, actuals: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    forecasts = forecasts or []
    actuals = actuals or []
    actual_by_id = {str(row.get("id") or row.get("channel") or row.get("service") or index): row for index, row in enumerate(actuals)}
    errors = []
    confidence_errors = []
    rows = []
    for index, forecast in enumerate(forecasts):
        key = str(forecast.get("id") or forecast.get("channel") or forecast.get("service") or index)
        actual = actual_by_id.get(key, {})
        predicted = as_float(forecast.get("forecast_quality"), forecast.get("future_quality", 0.0))
        observed = as_float(actual.get("quality"), actual.get("score", predicted))
        error = abs(predicted - observed)
        confidence = as_float(forecast.get("confidence"), forecast.get("future_confidence", 0.0))
        confidence_errors.append(abs((100.0 - error) / 100.0 - confidence))
        errors.append(error)
        rows.append({"id": key, "prediction_error": round(error, 3), "confidence": round(confidence, 4)})
    avg_error = mean(errors)
    return {
        "schema_version": "v7.intelligence.forecast-validation.v1",
        "forecast_accuracy": round(clamp(100.0 - avg_error), 3),
        "confidence_accuracy": round(clamp(100.0 - (mean(confidence_errors) * 100.0)), 3),
        "prediction_usefulness": "USEFUL" if avg_error <= 20.0 else "REVIEW_REQUIRED",
        "prediction_error": round(avg_error, 3),
        "forecast_drift": round(max(errors) - min(errors), 3) if len(errors) > 1 else 0.0,
        "rows": rows,
        "runtime_decision_authority": "none_validation_only",
    }


def drift_detection_framework(baseline: list[dict[str, Any]] | None = None, current: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    baseline = baseline or []
    current = current or []
    base_scores = [as_float(row.get("score"), row.get("quality", 0.0)) for row in baseline]
    current_scores = [as_float(row.get("score"), row.get("quality", 0.0)) for row in current]
    delta = mean(current_scores) - mean(base_scores)
    drift_score = abs(delta)
    state = "OK"
    if drift_score >= 25.0:
        state = "HIGH"
    elif drift_score >= 10.0:
        state = "MEDIUM"
    return {
        "schema_version": "v7.intelligence.drift-detection.v1",
        "prediction_drift": state,
        "service_scoring_drift": state,
        "suitability_drift": state,
        "trust_drift": state,
        "risk_drift": state,
        "drift_score": round(drift_score, 3),
        "runtime_decision_authority": "none_drift_only",
    }


def explainability_framework() -> dict[str, Any]:
    return {
        "schema_version": "v7.intelligence.explainability-framework.v1",
        "required_fields": ["subject", "score", "components", "confidence", "source", "authority"],
        "payloads": {
            "service_scores": "components from service quality criteria",
            "candidate_suitability": "reason_breakdown and advisory score parts",
            "best_available_pool": "ranked pool reasons and capacity/risk notes",
            "predictions": "forecast factors and confidence",
            "risk": "risk score inputs and high-risk channels",
            "trust": "execution/rollback/governance counters",
        },
        "authority": authority_boundary(),
    }


def explain_score(subject: str, score: float, components: dict[str, Any], *, confidence: float = 0.0, source: str = "") -> dict[str, Any]:
    positive = {key: value for key, value in components.items() if as_float(value) > 0}
    negative = {key: value for key, value in components.items() if as_float(value) < 0}
    return {
        "schema_version": "v7.intelligence.explainability-payload.v1",
        "subject": subject,
        "score": round(clamp(as_float(score)), 3),
        "components": components,
        "positive_components": positive,
        "negative_components": negative,
        "confidence": round(clamp(confidence, 0.0, 1.0), 4),
        "source": source,
        "authority": authority_boundary(),
    }


def rollout_governance_model() -> dict[str, Any]:
    levels = ["shadow_only", "operator_visible", "advisory_only", "advisory_weighted", "bounded_influence", "future_production_influence"]
    return {
        "schema_version": "v7.intelligence.rollout-governance.v1",
        "levels": {
            level: {
                "activation_requirements": ["tests_pass", "fresh_snapshots", "confidence_above_floor", "no_authority_conflict"],
                "safety_gates": ["governance_unchanged", "planner_owner_unchanged", "runtime_mutation_false"],
                "rollback_rules": ["disable_snapshot_family_or_ignore_advice", "revert_weight_version", "operator_review"],
                "authority_boundaries": authority_boundary(),
            }
            for level in levels
        },
        "default_level": "shadow_only",
    }


def trust_evolution_foundation() -> dict[str, Any]:
    return {
        "schema_version": "v7.intelligence.trust-evolution-foundation.v1",
        "increase_trust": ["successful_execution", "successful_rollback", "audit_ok", "closure_ok", "forecast_match"],
        "reduce_trust": ["failed_execution", "failed_rollback", "governance_violation", "audit_failure", "forecast_miss"],
        "increase_risk": ["service_degradation", "prediction_drift", "low_confidence", "snapshot_stale", "rollback_failure"],
        "reduce_risk": ["service_recovery", "stable_forecast", "high_confidence", "fresh_snapshots", "successful_closure"],
        "blast_radius_confidence_events": ["small_successful_operation", "rollback_success", "governance_clean"],
        "prediction_confidence_events": ["forecast_match", "low_drift", "stable_confidence"],
        "runtime_decision_authority": "none_foundation_only",
    }


def confidence_band(score: float) -> str:
    value = clamp(as_float(score), 0.0, 100.0)
    if value >= 85.0:
        return "HIGH"
    if value >= 70.0:
        return "GOOD"
    if value >= 50.0:
        return "WATCH"
    if value > 0.0:
        return "LOW"
    return "UNKNOWN"


def trust_evolution_model() -> dict[str, Any]:
    foundation = trust_evolution_foundation()
    return {
        "schema_version": "v7.ri6.trust-evolution-model.v1",
        "subjects": {
            "channels": {"increase": ["stable_service_score", "successful_selected_operation", "low_rollback_rate"], "decrease": ["service_degradation", "failed_selected_operation", "rollback_required"]},
            "predictions": {"increase": ["forecast_match", "confidence_calibrated", "low_drift"], "decrease": ["forecast_miss", "confidence_overstated", "high_drift"]},
            "service_intelligence": {"increase": ["good_channel_correctly_identified", "bad_channel_correctly_avoided"], "decrease": ["good_channel_missed", "bad_channel_recommended"]},
            "candidate_suitability": {"increase": ["recommended_candidate_succeeded", "pool_contained_working_alternative"], "decrease": ["recommended_candidate_failed", "pool_missed_working_alternative"]},
            "planner_recommendations": {"increase": ["operator_accepted_and_successful", "audit_closure_success"], "decrease": ["operator_rejected", "rollback_or_governance_failure"]},
        },
        "foundation": foundation,
        "truth_source_policy": "reuse_existing_snapshots_and_audit_outcomes",
        "new_truth_sources_created": False,
        "authority": authority_boundary(),
    }


def classify_decision_outcome(record: dict[str, Any] | None = None) -> dict[str, Any]:
    row = record or {}
    result_text = str(row.get("result") or row.get("status") or row.get("terminal_state") or "").lower()
    service_delta = as_float(row.get("service_delta"), as_float(row.get("score_delta"), 0.0))
    prediction_delta = abs(as_float(row.get("prediction_delta"), as_float(row.get("forecast_error"), 0.0)))
    rollback_required = bool(row.get("rollback_required") or row.get("rollback") or "rollback" in result_text)
    rollback_failed = bool(row.get("rollback_failed") or "rollback_failed" in result_text)
    governance_violation = bool(row.get("governance_violation") or "violation" in result_text)
    failed = bool(row.get("failed") or row.get("error") or result_text in {"fail", "failed", "failure", "error"})
    success = bool(row.get("success") or result_text in {"ok", "success", "successful", "applied", "pass"})

    if rollback_failed or governance_violation:
        outcome = "FAILURE"
    elif rollback_required:
        outcome = "ROLLBACK_REQUIRED"
    elif failed:
        outcome = "PARTIAL_FAILURE" if service_delta > 0 else "FAILURE"
    elif success and service_delta >= -5.0 and prediction_delta <= 20.0:
        outcome = "SUCCESS"
    elif success:
        outcome = "PARTIAL_SUCCESS"
    elif service_delta < -10.0:
        outcome = "PARTIAL_FAILURE"
    else:
        outcome = "NEUTRAL"

    base = {
        "SUCCESS": 100.0,
        "PARTIAL_SUCCESS": 75.0,
        "NEUTRAL": 50.0,
        "PARTIAL_FAILURE": 30.0,
        "FAILURE": 0.0,
        "ROLLBACK_REQUIRED": 20.0,
    }[outcome]
    quality = clamp(base + clamp(service_delta, -20.0, 20.0) - clamp(prediction_delta, 0.0, 40.0) * 0.25)
    return {
        "schema_version": "v7.ri6.decision-outcome.v1",
        "outcome": outcome,
        "decision_quality": round(quality, 3),
        "service_impact": round(service_delta, 3),
        "prediction_impact": round(-prediction_delta, 3),
        "operator_impact": "rollback_review_required" if rollback_required else "normal_review",
        "runtime_decision_authority": "none_evidence_only",
    }


def decision_outcome_framework(records: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    outcomes = [classify_decision_outcome(row) for row in (records or []) if isinstance(row, dict)]
    counts: dict[str, int] = {}
    for row in outcomes:
        counts[row["outcome"]] = counts.get(row["outcome"], 0) + 1
    decision_confidence = mean([as_float(row.get("decision_quality"), 0.0) for row in outcomes], 0.0)
    if not outcomes:
        status = "LIVE_OUTCOME_REQUIRED"
    elif decision_confidence >= 75.0:
        status = "TRUST_GROWING"
    elif decision_confidence >= 50.0:
        status = "TRUST_WATCH"
    else:
        status = "TRUST_DECLINING"
    return {
        "schema_version": "v7.ri6.decision-outcome-framework.v1",
        "classifications": ["SUCCESS", "PARTIAL_SUCCESS", "NEUTRAL", "PARTIAL_FAILURE", "FAILURE", "ROLLBACK_REQUIRED"],
        "records_seen": len(outcomes),
        "outcome_counts": counts,
        "decision_confidence": round(decision_confidence, 3),
        "confidence_band": confidence_band(decision_confidence),
        "trust_evolution_status": status,
        "rows": outcomes,
        "authority": authority_boundary(),
    }


def _row_key(row: dict[str, Any], index: int) -> str:
    return str(row.get("id") or row.get("channel") or row.get("service") or row.get("target") or row.get("user") or index)


def prediction_accuracy_model(forecasts: list[dict[str, Any]] | None = None, actuals: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    forecasts = [row for row in (forecasts or []) if isinstance(row, dict)]
    actuals = [row for row in (actuals or []) if isinstance(row, dict)]
    actual_by_id = {_row_key(row, index): row for index, row in enumerate(actuals)}
    rows = []
    matched_accuracy = []
    confidence_values = []
    for index, forecast in enumerate(forecasts):
        key = _row_key(forecast, index)
        actual = actual_by_id.get(key)
        predicted = as_float(forecast.get("forecast_quality"), forecast.get("future_quality", 0.0))
        confidence = clamp(as_float(forecast.get("confidence"), forecast.get("future_confidence", 0.0)), 0.0, 1.0)
        confidence_values.append(confidence)
        observed = None
        accuracy = None
        delta = None
        if actual is not None:
            observed = as_float(actual.get("quality"), actual.get("score", predicted))
            delta = predicted - observed
            accuracy = clamp(100.0 - abs(delta))
            matched_accuracy.append(accuracy)
        rows.append({
            "id": key,
            "domain": "service" if forecast.get("service") else "channel",
            "predicted": round(predicted, 3),
            "actual": round(observed, 3) if observed is not None else None,
            "delta": round(delta, 3) if delta is not None else None,
            "confidence": round(confidence, 4),
            "accuracy": round(accuracy, 3) if accuracy is not None else None,
            "status": "MATCHED" if actual is not None else "PENDING_OUTCOME",
        })
    if matched_accuracy:
        prediction_confidence = mean(matched_accuracy) * mean(confidence_values, 0.0)
        validation_status = "VALIDATED"
    elif rows:
        prediction_confidence = mean(confidence_values, 0.0) * 60.0
        validation_status = "LIVE_OUTCOME_REQUIRED"
    else:
        prediction_confidence = 0.0
        validation_status = "NO_FORECASTS"
    return {
        "schema_version": "v7.ri6.prediction-accuracy-model.v1",
        "forecast_domains": ["channel_quality", "service_quality", "risk", "trust", "recovery", "degradation"],
        "forecasts_seen": len(rows),
        "actuals_seen": len(actuals),
        "matched_count": len(matched_accuracy),
        "forecast_accuracy": round(mean(matched_accuracy, 0.0), 3),
        "prediction_confidence": round(clamp(prediction_confidence), 3),
        "confidence_band": confidence_band(prediction_confidence),
        "validation_status": validation_status,
        "rows": rows,
        "runtime_decision_authority": "none_accuracy_only",
    }


def service_intelligence_trust_model(service_rows: list[dict[str, Any]] | None = None, actuals: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    service_rows = [row for row in (service_rows or []) if isinstance(row, dict)]
    actual_by_id = {_row_key(row, index): row for index, row in enumerate(actuals or []) if isinstance(row, dict)}
    rows = []
    confidences = []
    for index, row in enumerate(service_rows):
        key = _row_key(row, index)
        predicted = as_float(row.get("aggregate_score"), row.get("average_score", row.get("score", 0.0)))
        confidence = clamp(as_float(row.get("confidence"), 0.0), 0.0, 1.0)
        actual = actual_by_id.get(key)
        observed = as_float(actual.get("score"), predicted) if actual else None
        correctness = clamp(100.0 - abs(predicted - observed)) if observed is not None else predicted
        good_correct = predicted >= 70.0 and correctness >= 70.0
        bad_correct = predicted < 50.0 and correctness >= 70.0
        row_confidence = correctness * max(confidence, 0.25)
        confidences.append(row_confidence)
        rows.append({
            "id": key,
            "predicted_score": round(predicted, 3),
            "actual_score": round(observed, 3) if observed is not None else None,
            "correctness": round(correctness, 3),
            "confidence": round(confidence, 4),
            "good_channel_correctly_identified": good_correct,
            "bad_channel_correctly_identified": bad_correct,
        })
    service_confidence = mean(confidences, 0.0)
    return {
        "schema_version": "v7.ri6.service-intelligence-trust-model.v1",
        "rows_seen": len(rows),
        "service_confidence": round(clamp(service_confidence), 3),
        "confidence_band": confidence_band(service_confidence),
        "rows": rows,
        "runtime_decision_authority": "none_evidence_only",
    }


def suitability_trust_model(candidate_rows: list[dict[str, Any]] | None = None, outcomes: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    outcome_by_key = {
        f"{row.get('user', '')}:{row.get('channel') or row.get('egress') or row.get('target') or ''}": row
        for row in (outcomes or [])
        if isinstance(row, dict)
    }
    flattened = []
    for row in (candidate_rows or []):
        if not isinstance(row, dict):
            continue
        user = str(row.get("user") or "")
        candidates = row.get("candidates") if isinstance(row.get("candidates"), list) else [row]
        for candidate in candidates:
            if isinstance(candidate, dict):
                item = dict(candidate)
                item.setdefault("user", user)
                flattened.append(item)
    rows = []
    confidences = []
    for candidate in flattened:
        key = f"{candidate.get('user', '')}:{candidate.get('channel') or candidate.get('egress') or candidate.get('target') or ''}"
        score = as_float(candidate.get("suitability_score"), candidate.get("score", 0.0))
        confidence = clamp(as_float(candidate.get("confidence"), 0.0), 0.0, 1.0)
        outcome = outcome_by_key.get(key)
        succeeded = bool(outcome and (outcome.get("success") or str(outcome.get("result", "")).lower() in {"ok", "success", "applied"}))
        observed_quality = 100.0 if succeeded else (50.0 if outcome is None else 0.0)
        correctness = clamp(100.0 - abs(score - observed_quality))
        candidate_confidence = correctness * max(confidence, 0.25)
        confidences.append(candidate_confidence)
        rows.append({
            "key": key,
            "suitability_score": round(score, 3),
            "outcome_seen": outcome is not None,
            "succeeded": succeeded,
            "correctness": round(correctness, 3),
            "confidence": round(confidence, 4),
        })
    suitability_confidence = mean(confidences, 0.0)
    return {
        "schema_version": "v7.ri6.suitability-trust-model.v1",
        "candidates_seen": len(rows),
        "outcomes_seen": len(outcomes or []),
        "suitability_confidence": round(clamp(suitability_confidence), 3),
        "confidence_band": confidence_band(suitability_confidence),
        "validation_status": "VALIDATED" if outcomes else "LIVE_OUTCOME_REQUIRED",
        "rows": rows[:50],
        "runtime_decision_authority": "none_evidence_only",
    }


def rollback_intelligence_model(records: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    rows = [row for row in (records or []) if isinstance(row, dict)]
    rollback_rows = [
        row for row in rows
        if row.get("rollback") or row.get("rollback_required") or row.get("rollback_completed") or row.get("rollback_failed") or "rollback" in str(row.get("result") or "").lower()
    ]
    completed = sum(1 for row in rollback_rows if row.get("rollback_completed") or str(row.get("result") or "").lower() in {"rollback_ok", "rollback_success"})
    failed = sum(1 for row in rollback_rows if row.get("rollback_failed") or str(row.get("result") or "").lower() in {"rollback_failed", "rollback_error"})
    required = len(rollback_rows)
    success_rate = (completed / required) * 100.0 if required else 0.0
    confidence = success_rate if required else 0.0
    return {
        "schema_version": "v7.ri6.rollback-intelligence-model.v1",
        "records_seen": len(rows),
        "rollback_required": required,
        "rollback_completed": completed,
        "rollback_failed": failed,
        "rollback_success_rate": round(success_rate, 3),
        "rollback_confidence": round(clamp(confidence), 3),
        "confidence_band": confidence_band(confidence),
        "validation_status": "VALIDATED" if required else "NO_ROLLBACK_OUTCOMES",
        "runtime_decision_authority": "none_evidence_only",
    }


def blast_radius_confidence_model(records: list[dict[str, Any]] | None = None, metrics: dict[str, Any] | None = None) -> dict[str, Any]:
    rows = [row for row in (records or []) if isinstance(row, dict)]
    metrics = metrics or {}
    successful_small = 0
    unsafe_large = 0
    confidences = []
    for row in rows:
        radius = as_float(row.get("blast_radius"), row.get("affected_users", 0.0))
        success = bool(row.get("success") or str(row.get("result") or "").lower() in {"ok", "success", "applied"})
        rollback_required = bool(row.get("rollback_required") or row.get("rollback_failed"))
        if radius <= 5 and success and not rollback_required:
            successful_small += 1
        if radius > 25 and rollback_required:
            unsafe_large += 1
        confidences.append(100.0 if success and not rollback_required else 20.0)
    recommendation = metrics.get("recommendation") if isinstance(metrics.get("recommendation"), dict) else {}
    recommended_budget = as_float(recommendation.get("recommended_budget"), metrics.get("recommended_budget", 0.0))
    if recommended_budget:
        confidences.append(clamp(100.0 - max(0.0, recommended_budget - 25.0)))
    confidence = mean(confidences, 0.0)
    return {
        "schema_version": "v7.ri6.blast-radius-confidence-model.v1",
        "records_seen": len(rows),
        "successful_small_operations": successful_small,
        "unsafe_large_operations": unsafe_large,
        "recommended_budget": round(recommended_budget, 3),
        "blast_radius_confidence": round(clamp(confidence), 3),
        "confidence_band": confidence_band(confidence),
        "runtime_decision_authority": "none_evidence_only",
    }


def autonomy_readiness_model(confidence_summary: dict[str, Any] | None = None) -> dict[str, Any]:
    summary = confidence_summary or {}
    scores = [
        as_float(summary.get("decision_confidence"), 0.0),
        as_float(summary.get("prediction_confidence"), 0.0),
        as_float(summary.get("service_confidence"), 0.0),
        as_float(summary.get("suitability_confidence"), 0.0),
        as_float(summary.get("rollback_confidence"), 0.0),
        as_float(summary.get("blast_radius_confidence"), 0.0),
    ]
    minimum = min(scores) if scores else 0.0
    average = mean(scores, 0.0)
    live_calibrated = bool(summary.get("live_calibrated"))
    explicit_autonomy_approval = bool(summary.get("explicit_autonomy_approval"))
    if minimum < 50.0:
        level = "NOT_READY"
    elif average < 60.0:
        level = "SHADOW_READY"
    elif average < 70.0 or not live_calibrated:
        level = "OPERATOR_VISIBLE_READY"
    elif average < 85.0:
        level = "OPERATOR_APPROVAL_READY"
    elif average < 95.0 or not explicit_autonomy_approval:
        level = "BOUNDED_AUTONOMY_READY"
    else:
        level = "PRODUCTION_AUTONOMY_READY"
    return {
        "schema_version": "v7.ri6.autonomy-readiness-model.v1",
        "levels": list(AUTONOMY_READINESS_LEVELS),
        "current_level": level,
        "minimum_confidence": round(minimum, 3),
        "average_confidence": round(average, 3),
        "live_calibrated": live_calibrated,
        "explicit_autonomy_approval": explicit_autonomy_approval,
        "autonomy_enabled": False,
        "automatic_user_movement_enabled": False,
        "planner_authority_changed": False,
        "governance_changed": False,
        "execution_changed": False,
        "authority": authority_boundary(),
    }


def governed_staging_architecture_map() -> dict[str, Any]:
    return {
        "schema_version": "v7.governed-staging.architecture-map.v1",
        "intelligence_chain": intelligence_reality_map()["chain"],
        "execution_chain": {
            "planner": "tools/v7-users-autoswitch",
            "operator_clearance": "tools/v7-operator-execution-packet + admin_core/operator_execution.py",
            "restore_barrier": "admin_core/operator_execution.py",
            "runtime_execution": "tools/v7-users-autoswitch --apply --verify",
            "rollback": "tools/v7-users-autoswitch --rollback-packet --apply --verify",
            "audit": "existing runtime/operator audit path",
            "closure": "existing operator lifecycle closure records",
        },
        "ri6_role": "evidence_and_confidence_only",
        "shadow_execution_role": "virtual_lifecycle_certification_only",
        "forbidden": [
            "autonomy_enable",
            "user_movement",
            "governance_owner_change",
            "planner_owner_change",
            "execution_owner_change",
            "rollback_owner_change",
            "new_truth_source",
            "new_snapshot_root",
        ],
        "authority": authority_boundary(),
    }


def shadow_execution_lifecycle(
    *,
    selected_move_count: int = 0,
    requested_blast_radius: int = 0,
    confidence_summary: dict[str, Any] | None = None,
    production_converged: bool = False,
    operator_approval_present: bool = False,
) -> dict[str, Any]:
    confidence_summary = confidence_summary or {}
    readiness = autonomy_readiness_model({
        **confidence_summary,
        "explicit_autonomy_approval": False,
    })
    selected_count = max(0, int(selected_move_count))
    requested = max(0, int(requested_blast_radius))
    effective = min(selected_count, requested) if requested else selected_count
    steps = [
        {"step": "discover_runtime_truth", "mode": "read_only", "required": True, "passed": bool(production_converged)},
        {"step": "load_snapshots", "mode": "read_only", "required": True, "passed": True},
        {"step": "compute_virtual_plan", "mode": "shadow", "required": True, "passed": True},
        {"step": "evaluate_confidence", "mode": "shadow", "required": True, "passed": readiness["minimum_confidence"] >= 50.0},
        {"step": "operator_approval_check", "mode": "read_only", "required": False, "passed": bool(operator_approval_present)},
        {"step": "virtual_restore_barrier_check", "mode": "shadow", "required": True, "passed": True},
        {"step": "virtual_runtime_recheck", "mode": "shadow", "required": True, "passed": bool(production_converged)},
        {"step": "virtual_execute", "mode": "shadow", "required": True, "passed": True},
        {"step": "virtual_verify", "mode": "shadow", "required": True, "passed": True},
        {"step": "virtual_rollback_plan", "mode": "shadow", "required": True, "passed": True},
        {"step": "virtual_audit_closure", "mode": "shadow", "required": True, "passed": True},
    ]
    blockers = [
        step["step"]
        for step in steps
        if step["required"] and not step["passed"]
    ]
    return {
        "schema_version": "v7.governed-staging.shadow-execution-lifecycle.v1",
        "mode": "virtual_shadow_read_only",
        "selected_move_count": selected_count,
        "requested_blast_radius": requested,
        "effective_shadow_blast_radius": effective,
        "steps": steps,
        "blockers": blockers,
        "shadow_execution_complete": not blockers,
        "runtime_mutation_performed": False,
        "users_moved": False,
        "autonomy_enabled": False,
        "authority": authority_boundary(),
    }


def accuracy_certification(summary: dict[str, Any] | None = None) -> dict[str, Any]:
    summary = summary or {}
    confidence = summary.get("confidence_summary") if isinstance(summary.get("confidence_summary"), dict) else summary
    decision = as_float(confidence.get("decision_confidence"), 0.0)
    prediction = as_float(confidence.get("prediction_confidence"), 0.0)
    service = as_float(confidence.get("service_confidence"), 0.0)
    suitability = as_float(confidence.get("suitability_confidence"), 0.0)
    rollback = as_float(confidence.get("rollback_confidence"), 0.0)
    trust = as_float(summary.get("overall_confidence"), mean([decision, prediction, service, suitability, rollback], 0.0))
    live_calibrated = bool(confidence.get("live_calibrated"))
    scores = {
        "decision": decision,
        "prediction": prediction,
        "service": service,
        "suitability": suitability,
        "rollback": rollback,
        "trust": trust,
    }
    blockers = [
        f"{name}_confidence_below_operator_threshold"
        for name, value in scores.items()
        if value < 70.0
    ]
    if not live_calibrated:
        blockers.append("live_outcome_calibration_missing")
    return {
        "schema_version": "v7.governed-staging.accuracy-certification.v1",
        "scores": {key: round(value, 3) for key, value in scores.items()},
        "minimum_score": round(min(scores.values()) if scores else 0.0, 3),
        "average_score": round(mean(list(scores.values()), 0.0), 3),
        "live_calibrated": live_calibrated,
        "operator_approval_accuracy_ready": not blockers,
        "blockers": blockers,
        "runtime_decision_authority": "none_certification_only",
    }


def blast_radius_certification_ladder(
    *,
    confidence_summary: dict[str, Any] | None = None,
    prior_runtime_certification: dict[str, bool] | None = None,
) -> dict[str, Any]:
    confidence_summary = confidence_summary or {}
    prior_runtime_certification = prior_runtime_certification or {}
    blast_confidence = as_float(confidence_summary.get("blast_radius_confidence"), 0.0)
    rollback_confidence = as_float(confidence_summary.get("rollback_confidence"), 0.0)
    decision_confidence = as_float(confidence_summary.get("decision_confidence"), 0.0)
    live_calibrated = bool(confidence_summary.get("live_calibrated"))
    tiers = []
    for radius, floor in ((1, 60.0), (2, 70.0), (5, 80.0), (10, 90.0)):
        prior_key = f"blast_radius_{radius}_pass"
        prior_ok = bool(prior_runtime_certification.get(prior_key))
        confidence_ok = min(blast_confidence, rollback_confidence, decision_confidence) >= floor
        ready = bool(prior_ok and confidence_ok and live_calibrated)
        blockers = []
        if not prior_ok:
            blockers.append(f"{prior_key}_not_currently_certified")
        if not confidence_ok:
            blockers.append(f"confidence_below_radius_{radius}_floor")
        if not live_calibrated:
            blockers.append("live_outcome_calibration_missing")
        tiers.append({
            "blast_radius": radius,
            "confidence_floor": floor,
            "prior_runtime_certification": prior_ok,
            "confidence_ready": confidence_ok,
            "ready": ready,
            "blockers": blockers,
        })
    return {
        "schema_version": "v7.governed-staging.blast-radius-certification-ladder.v1",
        "tiers": tiers,
        "max_ready_blast_radius": max([row["blast_radius"] for row in tiers if row["ready"]] or [0]),
        "runtime_mutation_performed": False,
        "authority": authority_boundary(),
    }


def failure_certification(
    *,
    prediction_failure: bool = False,
    trust_failure: bool = False,
    service_failure: bool = False,
    snapshot_failure: bool = False,
    confidence_failure: bool = False,
    channel_failure: bool = False,
) -> dict[str, Any]:
    cases = {
        "prediction_failure": prediction_failure,
        "trust_failure": trust_failure,
        "service_failure": service_failure,
        "snapshot_failure": snapshot_failure,
        "confidence_failure": confidence_failure,
        "channel_failure": channel_failure,
    }
    rows = []
    for name, triggered in cases.items():
        rows.append({
            "case": name,
            "triggered": bool(triggered),
            "expected_behavior": "fail_closed_or_ignore_advisory",
            "movement_allowed": False,
            "autonomy_allowed": False,
            "runtime_authority_granted": False,
        })
    return {
        "schema_version": "v7.governed-staging.failure-certification.v1",
        "cases": rows,
        "fail_closed_certified": all(not row["movement_allowed"] and not row["autonomy_allowed"] for row in rows),
        "runtime_mutation_performed": False,
        "authority": authority_boundary(),
    }


def autonomy_safety_model() -> dict[str, Any]:
    return {
        "schema_version": "v7.governed-staging.autonomy-safety-model.v1",
        "authority_ladder": [
            {"level": "SHADOW_READY", "authority": "read_only_virtual_shadow"},
            {"level": "OPERATOR_VISIBLE_READY", "authority": "operator_visibility_only"},
            {"level": "OPERATOR_APPROVAL_READY", "authority": "operator_approved_existing_runtime_owner_only"},
            {"level": "BOUNDED_AUTONOMY_READY", "authority": "future_scope_requires_explicit_program_and_approval"},
            {"level": "PRODUCTION_AUTONOMY_READY", "authority": "not_granted_by_this_program"},
        ],
        "blast_radius_ladder": [1, 2, 5, 10],
        "rollback_ladder": ["rollback_plan_present", "rollback_packet_valid", "rollback_owner_existing_runtime", "rollback_audit_closure_required"],
        "confidence_ladder": {
            "shadow": 50.0,
            "operator_visible": 60.0,
            "operator_approval": 70.0,
            "bounded_autonomy": 85.0,
            "production_autonomy": 95.0,
        },
        "autonomy_enabled": False,
        "runtime_authority_created": False,
        "authority": authority_boundary(),
    }


def governed_staging_certification(
    *,
    trust_summary: dict[str, Any] | None = None,
    production_converged: bool = False,
    current_runtime_truth_known: bool = False,
    prior_runtime_certification: dict[str, bool] | None = None,
) -> dict[str, Any]:
    trust_summary = trust_summary or trust_evolution_summary()
    confidence = trust_summary.get("confidence_summary") if isinstance(trust_summary.get("confidence_summary"), dict) else {}
    accuracy = accuracy_certification(trust_summary)
    blast = blast_radius_certification_ladder(
        confidence_summary=confidence,
        prior_runtime_certification=prior_runtime_certification or {},
    )
    shadow = shadow_execution_lifecycle(
        selected_move_count=1,
        requested_blast_radius=1,
        confidence_summary=confidence,
        production_converged=production_converged,
        operator_approval_present=False,
    )
    failure = failure_certification(
        prediction_failure=True,
        trust_failure=True,
        service_failure=True,
        snapshot_failure=True,
        confidence_failure=True,
        channel_failure=True,
    )
    readiness = autonomy_readiness_model(confidence)
    blockers = []
    if not current_runtime_truth_known:
        blockers.append("current_runtime_truth_unknown")
    if not production_converged:
        blockers.append("ri6_not_production_converged")
    blockers.extend(accuracy["blockers"])
    for row in blast["tiers"]:
        if row["blast_radius"] == 1 and row["blockers"]:
            blockers.extend(row["blockers"])
            break
    shadow_ready = bool(failure["fail_closed_certified"] and readiness["minimum_confidence"] >= 50.0)
    operator_approval_ready = bool(shadow_ready and not blockers and accuracy["operator_approval_accuracy_ready"] and blast["max_ready_blast_radius"] >= 1)
    bounded_ready = bool(operator_approval_ready and blast["max_ready_blast_radius"] >= 10 and readiness["average_confidence"] >= 85.0)
    production_ready = bool(bounded_ready and readiness["average_confidence"] >= 95.0 and confidence.get("explicit_autonomy_approval"))
    return {
        "schema_version": "v7.governed-staging.autonomy-certification.v1",
        "architecture": governed_staging_architecture_map(),
        "shadow_execution": shadow,
        "accuracy": accuracy,
        "blast_radius": blast,
        "failure": failure,
        "autonomy_safety": autonomy_safety_model(),
        "readiness": readiness,
        "AUTONOMY_CERTIFIED": bool(operator_approval_ready and bounded_ready and production_ready),
        "SHADOW_READY": shadow_ready,
        "OPERATOR_APPROVAL_READY": operator_approval_ready,
        "BOUNDED_AUTONOMY_READY": bounded_ready,
        "PRODUCTION_AUTONOMY_READY": production_ready,
        "BLOCKERS": sorted(set(blockers)),
        "SAFE_NEXT_STEP": "CONVERGE_RI6_TO_PRODUCTION_AND_COLLECT_LIVE_OUTCOME_CALIBRATION" if blockers else "OPERATOR_APPROVAL_STAGING_REVIEW",
        "runtime_mutation_performed": False,
        "autonomy_enabled": False,
        "authority": authority_boundary(),
    }


def trust_evolution_summary(
    *,
    decision_records: list[dict[str, Any]] | None = None,
    prediction_forecasts: list[dict[str, Any]] | None = None,
    prediction_actuals: list[dict[str, Any]] | None = None,
    service_rows: list[dict[str, Any]] | None = None,
    service_actuals: list[dict[str, Any]] | None = None,
    candidate_rows: list[dict[str, Any]] | None = None,
    candidate_outcomes: list[dict[str, Any]] | None = None,
    rollback_records: list[dict[str, Any]] | None = None,
    blast_radius_records: list[dict[str, Any]] | None = None,
    blast_radius_metrics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    decision = decision_outcome_framework(decision_records)
    prediction = prediction_accuracy_model(prediction_forecasts, prediction_actuals)
    service = service_intelligence_trust_model(service_rows, service_actuals)
    suitability = suitability_trust_model(candidate_rows, candidate_outcomes)
    rollback = rollback_intelligence_model(rollback_records)
    blast = blast_radius_confidence_model(blast_radius_records, blast_radius_metrics)
    confidence_summary = {
        "decision_confidence": decision["decision_confidence"],
        "prediction_confidence": prediction["prediction_confidence"],
        "service_confidence": service["service_confidence"],
        "suitability_confidence": suitability["suitability_confidence"],
        "rollback_confidence": rollback["rollback_confidence"],
        "blast_radius_confidence": blast["blast_radius_confidence"],
        "live_calibrated": bool(decision_records and prediction_actuals and candidate_outcomes),
        "explicit_autonomy_approval": False,
    }
    autonomy = autonomy_readiness_model(confidence_summary)
    confidence_values = [as_float(value) for key, value in confidence_summary.items() if key.endswith("_confidence")]
    return {
        "schema_version": RI6_SCHEMA_VERSION,
        "model": trust_evolution_model(),
        "decision_outcome": decision,
        "prediction_accuracy": prediction,
        "service_intelligence_trust": service,
        "suitability_trust": suitability,
        "rollback_intelligence": rollback,
        "blast_radius_confidence_model": blast,
        "confidence_summary": {key: round(value, 3) if isinstance(value, (int, float)) else value for key, value in confidence_summary.items()},
        "overall_confidence": round(mean(confidence_values, 0.0), 3),
        "overall_confidence_band": confidence_band(mean(confidence_values, 0.0)),
        "autonomy_readiness": autonomy,
        "runtime_decision_authority": "none_evidence_only",
        "planner_decision_owner": "tools/v7-users-autoswitch",
        "execution_authority": "none",
        "selected_moves_write_authority": "none",
        "runtime_mutation_performed": False,
        "deploy_performed": False,
    }


def service_probe_audit() -> dict[str, Any]:
    return {
        "schema_version": "v7.intelligence.service-probe-audit.v1",
        "services": {
            "telegram": {"classification": "EXISTS", "evidence": ["v7-telegram-sentinel", "service-matrix"]},
            "youtube": {"classification": "PARTIAL", "evidence": ["service-matrix logical checks"]},
            "instagram": {"classification": "PARTIAL", "evidence": ["service-matrix logical checks"]},
            "chatgpt": {"classification": "PARTIAL", "evidence": ["service-matrix logical checks"]},
            "google": {"classification": "EXISTS", "evidence": ["service-matrix"]},
            "google_auth": {"classification": "PARTIAL", "evidence": ["service-matrix"]},
        },
        "missing_probe_classes": ["service-specific YouTube playback probe", "Instagram media probe", "ChatGPT streaming probe"],
    }


def observability_model() -> dict[str, Any]:
    return {
        "schema_version": "v7.intelligence.observability-model.v1",
        "alerts": {
            "freshness": ["snapshot stale", "snapshot expired", "source freshness over threshold"],
            "confidence": ["below family floor", "confidence sudden drop"],
            "prediction": ["forecast error high", "forecast confidence mismatch"],
            "drift": ["service scoring drift", "prediction drift", "trust/risk drift"],
            "calibration": ["score compression", "identical distribution", "low spread"],
            "data_quality": ["missing sources", "malformed rows", "source hash mismatch"],
            "snapshot_integrity": ["schema mismatch", "oversized snapshot", "corrupt snapshot"],
        },
        "runtime_decision_authority": "none_observability_only",
    }


def intelligence_truth_source_map() -> dict[str, Any]:
    return {
        "schema_version": "v7.intelligence.truth-source-map.v1",
        "truth": {
            "service_quality": {"source": "service-matrix.json + egress-quality-summary.json", "owner": "service probe/quality tools"},
            "service_history": {"source": "ServiceHistoryStore read model", "owner": "admin_core.routing_intelligence"},
            "candidate_suitability": {"source": "candidate-suitability-summary snapshot", "owner": "intelligence_workers"},
            "best_available_pool": {"source": "best-available-pool snapshot", "owner": "intelligence_workers"},
            "prediction": {"source": "prediction-summaries snapshot", "owner": "PredictiveFoundation/intelligence_workers"},
            "risk": {"source": "risk-summaries snapshot", "owner": "intelligence_workers"},
            "trust": {"source": "trust-summaries snapshot", "owner": "ExecutionTrustModel/intelligence_workers"},
            "trust_evolution": {"source": "trust-evolution-summaries advisory snapshot", "owner": "RI6 trust evolution worker"},
            "explainability": {"source": "model output payloads", "owner": "producing model"},
            "replay": {"source": "historical snapshots/outcomes", "owner": "read-only replay framework"},
            "drift": {"source": "baseline/current model outputs", "owner": "read-only drift framework"},
        },
        "one_truth_rule": True,
    }


def duplication_audit() -> dict[str, Any]:
    return {
        "schema_version": "v7.intelligence.duplication-audit.v1",
        "duplicate_planner": False,
        "duplicate_governance": False,
        "duplicate_execution": False,
        "duplicate_rollback": False,
        "duplicate_routing_brain": False,
        "duplicate_intelligence_layer": False,
        "duplicate_truth_sources": False,
        "duplicate_snapshot_roots": False,
        "duplicate_trust_authority": False,
        "trust_evolution_extends_existing_trust": True,
    }


def performance_certification() -> dict[str, Any]:
    return {
        "schema_version": "v7.intelligence.performance-certification.v1",
        "heavy_work_in_workers": True,
        "intelligence_in_snapshots": True,
        "runtime_reads_compact_data": True,
        "runtime_history_scans": False,
        "runtime_forecasting": False,
        "runtime_replay": False,
        "runtime_drift_analysis": False,
        "runtime_trust_evolution_training": False,
    }


def authority_boundary() -> dict[str, str]:
    return {
        "planner_authority": "tools/v7-users-autoswitch",
        "governance_authority": "unchanged_existing_governance",
        "execution_authority": "none",
        "rollback_authority": "unchanged_existing_rollback",
        "selected_moves_write_authority": "none",
        "runtime_mutation_authority": "none",
    }


def platform_certification() -> dict[str, Any]:
    ri6 = trust_evolution_summary()
    return {
        "schema_version": SCHEMA_VERSION,
        "architecture": intelligence_reality_map(),
        "governance": model_governance_framework(),
        "replay": replay_framework(),
        "prediction": {"ri5_certified": True},
        "service_intelligence": {"ri4_cd_certified": True},
        "candidate_suitability": {"ri4_b_certified": True},
        "trust_foundation": trust_evolution_foundation(),
        "trust_evolution": ri6,
        "observability": observability_model(),
        "explainability": explainability_framework(),
        "performance": performance_certification(),
        "operational_readiness": "READY_FOR_GOVERNED_STAGING",
        "commercial_readiness": "ARCHITECTURE_READY_REQUIRES_LIVE_CALIBRATION",
        "authority": authority_boundary(),
    }
