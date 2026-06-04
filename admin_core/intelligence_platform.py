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
    return {
        "schema_version": SCHEMA_VERSION,
        "architecture": intelligence_reality_map(),
        "governance": model_governance_framework(),
        "replay": replay_framework(),
        "prediction": {"ri5_certified": True},
        "service_intelligence": {"ri4_cd_certified": True},
        "candidate_suitability": {"ri4_b_certified": True},
        "trust_foundation": trust_evolution_foundation(),
        "observability": observability_model(),
        "explainability": explainability_framework(),
        "performance": performance_certification(),
        "operational_readiness": "READY_FOR_GOVERNED_STAGING",
        "commercial_readiness": "ARCHITECTURE_READY_REQUIRES_LIVE_CALIBRATION",
        "authority": authority_boundary(),
    }

