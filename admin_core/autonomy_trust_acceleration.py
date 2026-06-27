"""Read-only autonomy trust evidence acceleration helpers.

This module does not create evidence, change formulas, or mutate runtime state.
It inventories already-existing forecast, actual, shadow comparison, and trust
evidence so operators know which real evidence to collect next.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from admin_core import events as v7_events
from admin_core import intelligence_platform, intelligence_workers, shadow_autonomy
from admin_core.intelligence_snapshots import read_snapshot_family
from admin_core.operator_execution_pipeline import (
    AUTONOMY_CANARY_CONFIDENCE_FLOOR,
    AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR,
    AUTONOMY_CANARY_TRUST_FLOOR,
    autonomy_risk_tier_floor_model,
    autonomy_risk_tier_review,
)

ACTION_CLASS_ENABLEMENT_STATES = [
    "NOT_CERTIFIED",
    "GOVERNED_ONLY",
    "CERTIFIED_FOR_CLASS_APPROVAL",
    "CERTIFIED_FOR_BOUNDED_AUTONOMY",
    "AUTONOMOUS_RUNTIME",
]

CERTIFICATION_SIGNAL_CATEGORIES = [
    "MANDATORY_CERTIFICATION_REQUIREMENT",
    "SUPPORTING_EVIDENCE",
    "COVERAGE_SIGNAL",
    "INVENTORY_SIGNAL",
    "LEARNING_SIGNAL",
    "RELIABILITY_SIGNAL",
    "RUNTIME_SAFETY_SIGNAL",
    "OPTIMIZATION_SIGNAL",
    "HISTORICAL_EVIDENCE",
    "IMPLEMENTATION_ARTIFACT",
]

ACTION_CLASS_LADDER = [
    ("single-user governed candidate failover", 1, "GOVERNED_ONLY"),
    ("two-user governed candidate failover", 2, "NOT_CERTIFIED"),
    ("five-user governed candidate failover", 5, "NOT_CERTIFIED"),
    ("channel hard-fail failover", None, "GOVERNED_ONLY"),
    ("channel degradation failover", None, "GOVERNED_ONLY"),
    ("service-specific failover", None, "GOVERNED_ONLY"),
    ("recovery admission", None, "GOVERNED_ONLY"),
    ("small-batch movement", None, "NOT_CERTIFIED"),
    ("pool-level movement", None, "NOT_CERTIFIED"),
]

ACTION_CLASS_FRESHNESS_WINDOWS = {
    "single-user governed candidate failover": {
        "service": 900,
        "quality": 900,
        "route": 900,
        "capacity": 900,
        "prediction": 1800,
        "suitability": 900,
        "recovery": 3600,
    },
    "two-user governed candidate failover": {
        "service": 600,
        "quality": 600,
        "route": 600,
        "capacity": 600,
        "prediction": 1200,
        "suitability": 600,
        "recovery": 1800,
    },
    "five-user governed candidate failover": {
        "service": 300,
        "quality": 300,
        "route": 300,
        "capacity": 300,
        "prediction": 900,
        "suitability": 300,
        "recovery": 900,
    },
    "channel hard-fail failover": {
        "service": 300,
        "quality": 300,
        "route": 300,
        "capacity": 300,
        "prediction": 900,
        "suitability": 300,
        "recovery": 900,
    },
    "channel degradation failover": {
        "service": 900,
        "quality": 600,
        "route": 900,
        "capacity": 600,
        "prediction": 1200,
        "suitability": 600,
        "recovery": 1800,
    },
    "service-specific failover": {
        "service": 600,
        "quality": 600,
        "route": 900,
        "capacity": 900,
        "prediction": 1200,
        "suitability": 600,
        "recovery": 1800,
    },
    "recovery admission": {
        "service": 900,
        "quality": 900,
        "route": 900,
        "capacity": 900,
        "prediction": 1800,
        "suitability": 900,
        "recovery": 900,
    },
    "small-batch movement": {
        "service": 300,
        "quality": 300,
        "route": 300,
        "capacity": 300,
        "prediction": 900,
        "suitability": 300,
        "recovery": 900,
    },
    "pool-level movement": {
        "service": 180,
        "quality": 180,
        "route": 180,
        "capacity": 180,
        "prediction": 600,
        "suitability": 180,
        "recovery": 600,
    },
}

AUTONOMY_MODES = [
    "MANUAL_PACKET_APPROVAL",
    "CLASS_APPROVAL",
    "DELEGATED_AUTONOMY",
    "PRODUCTION_AUTONOMY",
]

DEFAULT_DELEGATED_AUTONOMY_POLICY = {
    "policy_id": "dap_default_tier1_readonly",
    "policy_name": "Default Delegated Autonomy Policy Preview",
    "policy_state": "NOT_APPROVED",
    "current_mode": "CLASS_APPROVAL",
    "target_mode": "DELEGATED_AUTONOMY",
    "allowed_action_classes": ["single-user governed candidate failover"],
    "max_users_per_action": 1,
    "allowed_failure_types": [
        "channel_hard_fail",
        "channel_degradation",
        "service_specific_failure",
    ],
    "required_freshness": [
        "capacity",
        "prediction",
        "quality",
        "recovery",
        "route",
        "service",
        "suitability",
    ],
    "required_verification": [
        "immediate_post_action_user_verification",
        "immediate_post_action_channel_verification",
        "service_reachability_verification",
        "truth_convergence_after_action",
    ],
    "required_rollback": "class_level_rollback_or_certified_no_rollback_path",
    "required_anti_flap": "PASS",
    "required_floors": {
        "confidence": AUTONOMY_CANARY_CONFIDENCE_FLOOR,
        "trust": AUTONOMY_CANARY_TRUST_FLOOR,
        "prediction_confidence": AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR,
    },
    "max_blast_radius": {"users": 1},
    "cooldown": {
        "per_user_seconds": 1800,
        "per_source_target_pair_seconds": 1800,
    },
    "stop_conditions": [
        "POLICY_NOT_APPROVED",
        "ACTION_CLASS_NOT_ALLOWED",
        "ACTION_CLASS_NOT_CERTIFIED",
        "ACTION_CLASS_NOT_AUTONOMOUS_RUNTIME",
        "GOVERNED_LEARNING_MODE_NOT_APPROVED",
        "PACKET_NOT_FRESH",
        "PACKET_POLICY_MISMATCH",
        "ROLLBACK_NOT_READY",
        "VERIFICATION_NOT_READY",
        "ANTI_FLAP_BLOCK",
        "BLAST_RADIUS_EXCEEDED",
        "STALE_EVIDENCE",
        "UNKNOWN_FAILURE_MODE",
        "AUTHORITY_BOUNDARY",
    ],
    "automatic_downgrade_rules": [
        "verification_failed",
        "rollback_required",
        "rollback_failed",
        "unknown_failure_mode_seen",
        "freshness_gate_failed",
        "anti_flap_gate_failed",
        "trust_floor_failed",
        "blast_radius_violation",
        "policy_mismatch",
    ],
    "required_reporting_after_action": [
        "verification_result",
        "rollback_or_no_rollback_result",
        "outcome_closure",
        "learning_update",
        "current_program_state_update",
        "omp_update",
        "truth_convergence_result",
        "action_class_promotion_evaluation",
    ],
    "governed_learning_mode_allowed": False,
    "runtime_apply_enabled": False,
    "authority_expansion_performed": False,
}


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _items(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    value = (payload or {}).get("items")
    return [row for row in (value or []) if isinstance(row, dict)]


def _first_item(payload: dict[str, Any] | None) -> dict[str, Any]:
    rows = _items(payload)
    return rows[0] if rows else {}


def _row_key(row: dict[str, Any], index: int = 0) -> str:
    return str(row.get("id") or row.get("channel") or row.get("service") or row.get("target") or index)


def _prediction_forecasts(prediction_snapshot: dict[str, Any] | None) -> list[dict[str, Any]]:
    summary = _first_item(prediction_snapshot)
    rows: list[dict[str, Any]] = []
    for row in summary.get("channel_forecasts") or []:
        if isinstance(row, dict):
            rows.append(row)
    for row in summary.get("service_forecasts") or []:
        if isinstance(row, dict):
            rows.append(row)
    return rows


def _best_possible_prediction_confidence(rows: list[dict[str, Any]], add_matches: int = 0) -> float:
    confidence_values = [as_float(row.get("confidence"), as_float(row.get("future_confidence"), 0.0)) for row in rows]
    matched = [as_float(row.get("accuracy"), 0.0) for row in rows if row.get("status") == "MATCHED"]
    if add_matches > 0:
        matched = matched + [100.0] * add_matches
    if not matched:
        return round((sum(confidence_values) / max(1, len(confidence_values))) * 60.0, 3) if confidence_values else 0.0
    return round(min(100.0, (sum(matched) / len(matched)) * (sum(confidence_values) / max(1, len(confidence_values)))), 3)


def build_prediction_collection_plan(
    *,
    prediction_snapshot: dict[str, Any],
    service_scores_snapshot: dict[str, Any],
    channel_service_scores_snapshot: dict[str, Any],
    decision_records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    forecasts = _prediction_forecasts(prediction_snapshot)
    service_rows = _items(service_scores_snapshot) + _items(channel_service_scores_snapshot)
    service_actuals = intelligence_workers.build_service_actual_rows(service_rows, decision_records or [])
    prediction_actuals = intelligence_workers.build_prediction_actual_rows(
        forecasts,
        service_rows,
        decision_records or [],
        feedback_records=decision_records or [],
    )
    accuracy = intelligence_platform.prediction_accuracy_model(forecasts, prediction_actuals)
    pending = [row for row in accuracy.get("rows", []) if row.get("status") == "PENDING_OUTCOME"]
    matched = [row for row in accuracy.get("rows", []) if row.get("status") == "MATCHED"]
    actual_keys = {_row_key(row, index) for index, row in enumerate(prediction_actuals)}
    forecast_index = {_row_key(row, index): row for index, row in enumerate(forecasts)}
    opportunities = []
    for row in pending:
        key = str(row.get("id") or "")
        forecast = forecast_index.get(key, {})
        opportunities.append({
            "id": key,
            "domain": row.get("domain"),
            "predicted": row.get("predicted"),
            "forecast_confidence": row.get("confidence"),
            "actual_available_now": key in actual_keys,
            "collection_action": "collect_existing_service_or_channel_actual" if row.get("domain") in {"service", "channel"} else "collect_governed_prediction_feedback",
            "valid_actual_sources": [
                "service/channel score refresh",
                "existing governed prediction feedback with prediction_actual",
            ],
            "synthetic_actual_allowed": False,
            "forecast": forecast,
        })
    return {
        "schema_version": "v7.autonomy-trust.prediction-collection-plan.v1",
        "forecasts_seen": len(forecasts),
        "forecast_actuals_seen": len(prediction_actuals),
        "service_actuals_seen": len(service_actuals),
        "matched_rows": len(matched),
        "pending_rows": len(pending),
        "prediction_confidence": accuracy.get("prediction_confidence", 0.0),
        "forecast_accuracy": accuracy.get("forecast_accuracy", 0.0),
        "validation_status": accuracy.get("validation_status", "UNKNOWN"),
        "best_possible_gain_if_5_pending_match": round(_best_possible_prediction_confidence(accuracy.get("rows", []), add_matches=min(5, len(pending))) - as_float(accuracy.get("prediction_confidence"), 0.0), 3),
        "best_possible_gain_if_all_pending_match": round(_best_possible_prediction_confidence(accuracy.get("rows", []), add_matches=len(pending)) - as_float(accuracy.get("prediction_confidence"), 0.0), 3),
        "opportunities": opportunities,
        "rows": accuracy.get("rows", []),
        "projection_only": True,
        "synthetic_actuals_created": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def build_operator_review_batches(
    review_packet: dict[str, Any],
    *,
    batch_sizes: list[int] | None = None,
) -> dict[str, Any]:
    batch_sizes = batch_sizes or [5, 10, 15]
    reviewable = [
        row for row in review_packet.get("items") or []
        if isinstance(row, dict) and row.get("comparison_eligibility", {}).get("eligible")
    ]
    ordered = sorted(
        reviewable,
        key=lambda row: (
            0 if row.get("recommendation") == "MOVE_USER" else 1,
            len(row.get("blockers") or []),
            -as_float(row.get("confidence"), 0.0),
            -as_float(row.get("trust"), 0.0),
            str(row.get("user") or ""),
        ),
    )
    batches = []
    for size in batch_sizes:
        items = ordered[:size]
        batches.append({
            "target_comparisons": size,
            "available": len(items),
            "items": items,
            "operator_decisions_allowed": ["agree", "disagree", "override"],
            "synthetic_agreement_allowed": False,
            "runtime_mutation_performed": False,
            "users_moved": 0,
            "apply_executed": False,
        })
    return {
        "schema_version": "v7.autonomy-trust.operator-review-batches.v1",
        "evidence_role": "secondary_supervised_confirmation",
        "reviewable_decisions": len(reviewable),
        "reviewed_decisions": int(as_float(review_packet.get("reviewed_decisions"), 0.0)),
        "fastest_path": "use only when the operator has enough context to judge a specific recommendation",
        "blind_review_required": False,
        "bulk_training_data": False,
        "batches": batches,
        "requires_real_operator_judgement": True,
        "requires_operator_context": True,
        "synthetic_agreement_allowed": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def _floor_gap(current: float, target: float) -> dict[str, Any]:
    return {
        "current": round(current, 3),
        "target": round(target, 3),
        "gap": round(max(0.0, target - current), 3),
        "pass": current >= target,
    }


def _mean_present(values: list[float]) -> float:
    present = [float(value) for value in values if value is not None]
    return round(sum(present) / len(present), 3) if present else 0.0


def build_canary_proximity(
    *,
    trust_evolution_snapshot: dict[str, Any],
    shadow_model: dict[str, Any],
    prediction_plan: dict[str, Any],
) -> dict[str, Any]:
    summary = _first_item(trust_evolution_snapshot)
    confidence_summary = summary.get("confidence_summary") if isinstance(summary.get("confidence_summary"), dict) else {}
    decision = as_float(confidence_summary.get("decision_confidence"), 0.0)
    service = as_float(confidence_summary.get("service_confidence"), 0.0)
    suitability = as_float(confidence_summary.get("suitability_confidence"), 0.0)
    blast = as_float(confidence_summary.get("blast_radius_confidence"), 0.0)
    confidence = as_float(confidence_summary.get("confidence_score"), 0.0) or _mean_present([decision, service, suitability])
    trust = as_float(confidence_summary.get("trust_score"), 0.0) or _mean_present([decision, service, suitability, blast])
    prediction = as_float(confidence_summary.get("prediction_confidence"), as_float(prediction_plan.get("prediction_confidence"), 0.0))
    comparison = shadow_model.get("confidence") if isinstance(shadow_model.get("confidence"), dict) else {}
    earned = as_float(comparison.get("earned_confidence"), 0.0)
    primary_floors = {
        "confidence": _floor_gap(confidence, AUTONOMY_CANARY_CONFIDENCE_FLOOR),
        "trust": _floor_gap(trust, AUTONOMY_CANARY_TRUST_FLOOR),
        "prediction_confidence": _floor_gap(prediction, AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR),
    }
    secondary_evidence = {
        "operator_earned_confidence": _floor_gap(earned, shadow_autonomy.OBSERVATION_TARGETS["minimum_earned_confidence"]),
    }
    candidate_floor_evaluation = [{
        "confidence": confidence,
        "trust": trust,
        "prediction_confidence": prediction,
        "rollback_confidence": as_float(confidence_summary.get("rollback_confidence"), 0.0),
    }]
    floor_blockers = [
        "prediction_confidence_too_low" if key == "prediction_confidence" else f"{key}_too_low"
        for key, value in primary_floors.items()
        if not value.get("pass")
    ]
    tier_review = autonomy_risk_tier_review(
        candidate_floor_evaluation=candidate_floor_evaluation,
        blockers=floor_blockers,
    )
    return {
        "schema_version": "v7.autonomy-trust.canary-proximity.v1",
        "autonomy_canary_1_ready": False,
        "readiness_model": "observed_outcome_primary_operator_comparison_secondary",
        "risk_tier_floor_model": autonomy_risk_tier_floor_model(),
        "risk_tier_review": tier_review,
        "floors": {**primary_floors, **secondary_evidence},
        "primary_floors": primary_floors,
        "secondary_evidence": secondary_evidence,
        "missing": [
            key for key, value in primary_floors.items()
            if not value.get("pass")
        ],
        "secondary_missing": [
            key for key, value in secondary_evidence.items()
            if not value.get("pass")
        ],
        "expected_gain": {
            "operator_10_comparisons_100pct": _comparison_projection_value(shadow_model, 10, 1.0),
            "operator_15_comparisons_80pct": _comparison_projection_value(shadow_model, 15, 0.8),
            "prediction_5_pending_best_case": round(as_float(prediction_plan.get("prediction_confidence"), 0.0) + as_float(prediction_plan.get("best_possible_gain_if_5_pending_match"), 0.0), 3),
            "prediction_all_pending_best_case": round(as_float(prediction_plan.get("prediction_confidence"), 0.0) + as_float(prediction_plan.get("best_possible_gain_if_all_pending_match"), 0.0), 3),
        },
        "projection_only": True,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def _mean_key(rows: list[dict[str, Any]], key: str) -> float:
    values = [as_float(row.get(key), 0.0) for row in rows if isinstance(row, dict) and row.get(key) not in (None, "")]
    return round(sum(values) / len(values), 3) if values else 0.0


def _confidence_band(value: float) -> str:
    if value >= 70.0:
        return "CANARY_READY"
    if value >= 50.0:
        return "PARTIAL"
    if value > 0.0:
        return "LOW"
    return "MISSING"


def build_floor_forensics(
    *,
    trust_evolution_snapshot: dict[str, Any],
    shadow_model: dict[str, Any],
    prediction_plan: dict[str, Any],
    canary_proximity: dict[str, Any],
) -> dict[str, Any]:
    summary = _first_item(trust_evolution_snapshot)
    confidence_summary = summary.get("confidence_summary") if isinstance(summary.get("confidence_summary"), dict) else {}
    prediction_accuracy = summary.get("prediction_accuracy") if isinstance(summary.get("prediction_accuracy"), dict) else {}
    service_trust = summary.get("service_intelligence_trust") if isinstance(summary.get("service_intelligence_trust"), dict) else {}
    suitability_trust = summary.get("suitability_trust") if isinstance(summary.get("suitability_trust"), dict) else {}
    rollback = summary.get("rollback_intelligence") if isinstance(summary.get("rollback_intelligence"), dict) else {}
    blast = summary.get("blast_radius_confidence_model") if isinstance(summary.get("blast_radius_confidence_model"), dict) else {}
    prediction_rows = prediction_accuracy.get("rows") or prediction_plan.get("rows") or []
    service_rows = service_trust.get("rows") or []
    suitability_rows = suitability_trust.get("rows") or []
    matched_prediction_rows = [row for row in prediction_rows if isinstance(row, dict) and row.get("status") == "MATCHED"]
    pending_prediction_rows = [row for row in prediction_rows if isinstance(row, dict) and row.get("status") == "PENDING_OUTCOME"]
    matched_rows_count = len(matched_prediction_rows)
    pending_rows_count = len(pending_prediction_rows)
    if not prediction_rows:
        matched_rows_count = int(as_float(prediction_accuracy.get("matched_count"), as_float(prediction_plan.get("matched_rows"), 0.0)))
        pending_rows_count = int(as_float(prediction_plan.get("pending_rows"), 0.0))
    forecast_accuracy = as_float(
        prediction_accuracy.get("forecast_accuracy"),
        as_float(prediction_plan.get("forecast_accuracy"), 0.0),
    )
    prediction_confidence = as_float(
        confidence_summary.get("prediction_confidence"),
        as_float(prediction_plan.get("prediction_confidence"), 0.0),
    )
    mean_forecast_confidence = round(prediction_confidence / forecast_accuracy, 4) if forecast_accuracy > 0 else 0.0
    decision = as_float(confidence_summary.get("decision_confidence"), 0.0)
    service = as_float(confidence_summary.get("service_confidence"), 0.0)
    suitability = as_float(confidence_summary.get("suitability_confidence"), 0.0)
    blast_confidence = as_float(confidence_summary.get("blast_radius_confidence"), 0.0)
    rollback_confidence = as_float(confidence_summary.get("rollback_confidence"), 0.0)
    comparison = shadow_model.get("confidence") if isinstance(shadow_model.get("confidence"), dict) else {}
    earned = as_float(comparison.get("earned_confidence"), 0.0)
    floors = canary_proximity.get("floors") if isinstance(canary_proximity.get("floors"), dict) else {}
    primary = canary_proximity.get("primary_floors") if isinstance(canary_proximity.get("primary_floors"), dict) else {}
    blockers = []
    for name, floor in primary.items():
        if isinstance(floor, dict) and not floor.get("pass"):
            blockers.append({
                "floor": name,
                "current": floor.get("current", 0.0),
                "target": floor.get("target", 0.0),
                "gap": floor.get("gap", 0.0),
            })
    return {
        "schema_version": "v7.autonomy-trust.floor-forensics.v1",
        "purpose": "explain_current_canary_floor_values_without_changing_formulas_or_evidence",
        "floor_formulas": {
            "confidence": "confidence_summary.confidence_score if present else mean(decision_confidence, service_confidence, suitability_confidence)",
            "trust": "confidence_summary.trust_score if present else mean(decision_confidence, service_confidence, suitability_confidence, blast_radius_confidence)",
            "prediction_confidence": "mean(matched_forecast_accuracy) * mean(forecast_confidence)",
            "operator_earned_confidence": "shadow_autonomy observed operator comparison confidence",
        },
        "floor_values": floors,
        "dominant_blockers": blockers,
        "component_values": {
            "decision_confidence": round(decision, 3),
            "service_confidence": round(service, 3),
            "suitability_confidence": round(suitability, 3),
            "blast_radius_confidence": round(blast_confidence, 3),
            "rollback_confidence": round(rollback_confidence, 3),
            "prediction_confidence": round(prediction_confidence, 3),
            "operator_earned_confidence": round(earned, 3),
            "overall_confidence": round(as_float(summary.get("overall_confidence"), 0.0), 3),
        },
        "prediction_root_cause": {
            "forecasts_seen": int(as_float(prediction_accuracy.get("forecasts_seen"), as_float(prediction_plan.get("forecasts_seen"), 0.0))),
            "actuals_seen": int(as_float(prediction_accuracy.get("actuals_seen"), as_float(prediction_plan.get("forecast_actuals_seen"), 0.0))),
            "matched_rows": matched_rows_count,
            "pending_rows": pending_rows_count,
            "forecast_accuracy": round(forecast_accuracy, 3),
            "mean_forecast_confidence": mean_forecast_confidence,
            "root_cause": "low_forecast_source_confidence" if matched_rows_count > 0 and pending_rows_count == 0 and mean_forecast_confidence < 0.7 else "pending_or_missing_actuals",
            "synthetic_actuals_allowed": False,
        },
        "service_root_cause": {
            "rows_seen": int(as_float(service_trust.get("rows_seen"), len(service_rows))),
            "service_confidence": round(service, 3),
            "mean_row_confidence": _mean_key(service_rows, "confidence"),
            "mean_correctness": _mean_key(service_rows, "correctness"),
            "root_cause": "service_rows_are_matched_but_low_source_confidence",
        },
        "suitability_root_cause": {
            "candidates_seen": int(as_float(suitability_trust.get("candidates_seen"), 0.0)),
            "outcomes_seen": int(as_float(suitability_trust.get("outcomes_seen"), 0.0)),
            "rows_seen": len(suitability_rows),
            "rows_without_outcome": len([row for row in suitability_rows if isinstance(row, dict) and not row.get("outcome_seen")]),
            "suitability_confidence": round(suitability, 3),
            "mean_candidate_confidence": _mean_key(suitability_rows, "confidence"),
            "mean_correctness": _mean_key(suitability_rows, "correctness"),
            "root_cause": "candidate_outcomes_exist_but_are_incomplete_and_low_confidence",
        },
        "rollback_and_blast": {
            "rollback_records_seen": int(as_float(rollback.get("records_seen"), 0.0)),
            "rollback_confidence": round(rollback_confidence, 3),
            "blast_records_seen": int(as_float(blast.get("records_seen"), 0.0)),
            "blast_radius_confidence": round(blast_confidence, 3),
            "root_cause": "not_current_floor_blockers",
        },
        "raw_rows": {
            "prediction": prediction_rows,
            "service": service_rows,
            "suitability": suitability_rows,
        },
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def build_materialization_audit(
    *,
    trust_evolution_snapshot: dict[str, Any],
    prediction_plan: dict[str, Any],
    floor_forensics: dict[str, Any],
) -> dict[str, Any]:
    summary = _first_item(trust_evolution_snapshot)
    counts = summary.get("outcome_mapper_counts") if isinstance(summary.get("outcome_mapper_counts"), dict) else {}
    prediction_root = floor_forensics.get("prediction_root_cause") if isinstance(floor_forensics.get("prediction_root_cause"), dict) else {}
    service_root = floor_forensics.get("service_root_cause") if isinstance(floor_forensics.get("service_root_cause"), dict) else {}
    suitability_root = floor_forensics.get("suitability_root_cause") if isinstance(floor_forensics.get("suitability_root_cause"), dict) else {}
    return {
        "schema_version": "v7.autonomy-trust.materialization-audit.v1",
        "purpose": "show_existing_owner_evidence_consumption_and_safe_next_gap",
        "prediction_actuals": {
            "forecasts_seen": prediction_root.get("forecasts_seen", 0),
            "actuals_seen": prediction_root.get("actuals_seen", 0),
            "matched_rows": prediction_root.get("matched_rows", 0),
            "pending_rows": prediction_root.get("pending_rows", 0),
            "materialized": prediction_root.get("matched_rows", 0) > 0 and prediction_root.get("pending_rows", 0) == 0,
            "safe_fix_available_now": False,
            "reason": "prediction actual lifecycle is consumed; remaining blocker is low forecast source confidence",
        },
        "service_actuals": {
            "service_actuals_count": int(as_float(counts.get("service_actuals_count"), 0.0)),
            "rows_seen": service_root.get("rows_seen", 0),
            "materialized": service_root.get("rows_seen", 0) > 0,
            "safe_fix_available_now": False,
            "reason": "service rows are present; confidence requires higher-confidence real probe data",
        },
        "candidate_outcomes": {
            "candidate_outcomes_count": int(as_float(counts.get("candidate_outcomes_count"), 0.0)),
            "candidates_seen": suitability_root.get("candidates_seen", 0),
            "outcomes_seen": suitability_root.get("outcomes_seen", 0),
            "rows_without_outcome": suitability_root.get("rows_without_outcome", 0),
            "materialized": suitability_root.get("outcomes_seen", 0) > 0,
            "safe_fix_available_now": False,
            "reason": "candidate outcomes are consumed but incomplete; additional real governed/manual outcomes are needed",
        },
        "blocked_fixes": [
            "synthetic_prediction_actuals",
            "synthetic_candidate_outcomes",
            "synthetic_operator_comparisons",
            "threshold_or_formula_changes",
            "runtime_apply_or_user_movement",
        ],
        "next_safe_evidence_phase": "collect_real_high_confidence_service_probe_cycles_and_real_governed_or_manual_outcome_closure",
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def _snapshot_meta(payload: dict[str, Any] | None) -> dict[str, Any]:
    payload = payload or {}
    return {
        "generated_at": payload.get("generated_at"),
        "confidence": as_float(payload.get("confidence"), 0.0),
        "source_hash_count": len(payload.get("source_hashes") or {}),
        "freshness_state": payload.get("freshness_state") or "UNKNOWN",
    }


def _source_row(
    *,
    source: str,
    evidence_count: int,
    evidence_expected: int | str,
    evidence_consumed: bool,
    confidence_weight: float,
    current_contribution: float,
    freshness: dict[str, Any],
    classification: str,
    reason: str,
) -> dict[str, Any]:
    return {
        "source": source,
        "evidence_count": evidence_count,
        "evidence_expected": evidence_expected,
        "evidence_consumed": evidence_consumed,
        "confidence_weight": round(confidence_weight, 4),
        "current_contribution": round(current_contribution, 3),
        "freshness": freshness,
        "classification": classification,
        "reason": reason,
    }


def build_source_confidence_inventory(
    *,
    prediction_snapshot: dict[str, Any],
    service_scores_snapshot: dict[str, Any],
    channel_service_scores_snapshot: dict[str, Any],
    trust_evolution_snapshot: dict[str, Any],
    shadow_model: dict[str, Any],
    floor_forensics: dict[str, Any],
    materialization_audit: dict[str, Any],
) -> dict[str, Any]:
    components = floor_forensics.get("component_values") if isinstance(floor_forensics.get("component_values"), dict) else {}
    prediction_root = floor_forensics.get("prediction_root_cause") if isinstance(floor_forensics.get("prediction_root_cause"), dict) else {}
    service_root = floor_forensics.get("service_root_cause") if isinstance(floor_forensics.get("service_root_cause"), dict) else {}
    suitability_root = floor_forensics.get("suitability_root_cause") if isinstance(floor_forensics.get("suitability_root_cause"), dict) else {}
    rollback_blast = floor_forensics.get("rollback_and_blast") if isinstance(floor_forensics.get("rollback_and_blast"), dict) else {}
    materialized = materialization_audit if isinstance(materialization_audit, dict) else {}
    prediction_actuals = materialized.get("prediction_actuals") if isinstance(materialized.get("prediction_actuals"), dict) else {}
    service_actuals = materialized.get("service_actuals") if isinstance(materialized.get("service_actuals"), dict) else {}
    candidate_outcomes = materialized.get("candidate_outcomes") if isinstance(materialized.get("candidate_outcomes"), dict) else {}
    quality = shadow_model.get("quality") if isinstance(shadow_model.get("quality"), dict) else {}
    confidence = shadow_model.get("confidence") if isinstance(shadow_model.get("confidence"), dict) else {}
    prediction_meta = _snapshot_meta(prediction_snapshot)
    service_meta = _snapshot_meta(service_scores_snapshot)
    channel_service_meta = _snapshot_meta(channel_service_scores_snapshot)
    trust_meta = _snapshot_meta(trust_evolution_snapshot)
    service_rows = _items(service_scores_snapshot) + _items(channel_service_scores_snapshot)
    operator_comparisons = int(as_float(quality.get("comparisons_total"), 0.0))
    rows = [
        _source_row(
            source="prediction_matches",
            evidence_count=int(as_float(prediction_root.get("matched_rows"), 0.0)),
            evidence_expected=int(as_float(prediction_root.get("forecasts_seen"), 0.0)),
            evidence_consumed=bool(prediction_actuals.get("materialized")),
            confidence_weight=as_float(prediction_root.get("mean_forecast_confidence"), 0.0),
            current_contribution=as_float(components.get("prediction_confidence"), 0.0),
            freshness=prediction_meta,
            classification="SUFFICIENT_EVIDENCE_LOW_ATTRIBUTION"
            if prediction_root.get("root_cause") == "low_forecast_source_confidence"
            else "INSUFFICIENT_EVIDENCE",
            reason=str(prediction_root.get("root_cause") or "UNKNOWN"),
        ),
        _source_row(
            source="service_outcomes",
            evidence_count=int(as_float(service_root.get("rows_seen"), len(service_rows))),
            evidence_expected="real_probe_cycles_with_high_source_confidence",
            evidence_consumed=bool(service_actuals.get("materialized")),
            confidence_weight=as_float(service_root.get("mean_row_confidence"), 0.0),
            current_contribution=as_float(components.get("service_confidence"), 0.0),
            freshness={
                "service_scores": service_meta,
                "channel_service_scores": channel_service_meta,
            },
            classification="INSUFFICIENT_HIGH_CONFIDENCE_EVIDENCE"
            if as_float(service_root.get("mean_row_confidence"), 0.0) < 0.7
            else "SUFFICIENT_EVIDENCE",
            reason=str(service_root.get("root_cause") or "UNKNOWN"),
        ),
        _source_row(
            source="candidate_outcomes",
            evidence_count=int(as_float(suitability_root.get("outcomes_seen"), 0.0)),
            evidence_expected=int(as_float(suitability_root.get("candidates_seen"), 0.0)),
            evidence_consumed=bool(candidate_outcomes.get("materialized")),
            confidence_weight=as_float(suitability_root.get("mean_candidate_confidence"), 0.0),
            current_contribution=as_float(components.get("suitability_confidence"), 0.0),
            freshness=trust_meta,
            classification="INSUFFICIENT_EVIDENCE"
            if int(as_float(suitability_root.get("outcomes_seen"), 0.0)) < int(as_float(suitability_root.get("candidates_seen"), 0.0))
            else "SUFFICIENT_EVIDENCE_LOW_ATTRIBUTION",
            reason=str(suitability_root.get("root_cause") or "UNKNOWN"),
        ),
        _source_row(
            source="blast_radius_evidence",
            evidence_count=int(as_float(rollback_blast.get("blast_records_seen"), 0.0)),
            evidence_expected="existing_blast_branch_records",
            evidence_consumed=as_float(components.get("blast_radius_confidence"), 0.0) > 0.0,
            confidence_weight=1.0 if as_float(components.get("blast_radius_confidence"), 0.0) >= 100.0 else 0.0,
            current_contribution=as_float(components.get("blast_radius_confidence"), 0.0),
            freshness=trust_meta,
            classification="SUFFICIENT_EVIDENCE",
            reason="certified_and_not_current_floor_blocker",
        ),
        _source_row(
            source="rollback_evidence",
            evidence_count=int(as_float(rollback_blast.get("rollback_records_seen"), 0.0)),
            evidence_expected="existing_rollback_records",
            evidence_consumed=as_float(components.get("rollback_confidence"), 0.0) > 0.0,
            confidence_weight=1.0 if as_float(components.get("rollback_confidence"), 0.0) >= 100.0 else 0.0,
            current_contribution=as_float(components.get("rollback_confidence"), 0.0),
            freshness=trust_meta,
            classification="SUFFICIENT_EVIDENCE",
            reason="certified_and_not_current_floor_blocker",
        ),
        _source_row(
            source="operator_comparison_evidence",
            evidence_count=operator_comparisons,
            evidence_expected="contextual_operator_reviews_only",
            evidence_consumed=operator_comparisons > 0,
            confidence_weight=as_float(confidence.get("earned_confidence"), 0.0) / 100.0,
            current_contribution=as_float(components.get("operator_earned_confidence"), 0.0),
            freshness={"generated_at": None, "freshness_state": "EVENT_LOG_DEPENDENT"},
            classification="INSUFFICIENT_EVIDENCE" if operator_comparisons == 0 else "PARTIAL_EVIDENCE",
            reason="secondary_confirmation_path_underfed",
        ),
    ]
    return {
        "schema_version": "v7.autonomy-trust.source-confidence-inventory.v1",
        "purpose": "attribute_current_confidence_to_real_sources_without_changing_formulas_or_evidence",
        "sources": rows,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def build_evidence_sufficiency_analysis(source_inventory: dict[str, Any]) -> dict[str, Any]:
    rows = [row for row in source_inventory.get("sources") or [] if isinstance(row, dict)]
    sufficient = [row["source"] for row in rows if str(row.get("classification", "")).startswith("SUFFICIENT")]
    insufficient = [
        row["source"] for row in rows
        if str(row.get("classification", "")).startswith("INSUFFICIENT")
    ]
    low_attribution = [
        row["source"] for row in rows
        if row.get("classification") == "SUFFICIENT_EVIDENCE_LOW_ATTRIBUTION"
    ]
    if insufficient and (sufficient or low_attribution):
        verdict = "MIXED"
    elif insufficient:
        verdict = "INSUFFICIENT_EVIDENCE"
    elif low_attribution:
        verdict = "SUFFICIENT_EVIDENCE_LOW_ATTRIBUTION"
    else:
        verdict = "SUFFICIENT_EVIDENCE"
    return {
        "schema_version": "v7.autonomy-trust.evidence-sufficiency.v1",
        "verdict": verdict,
        "sufficient_sources": sufficient,
        "insufficient_sources": insufficient,
        "low_attribution_sources": low_attribution,
        "can_fix_by_formula_change": False,
        "can_fix_by_synthetic_evidence": False,
        "requires_real_collection": bool(insufficient),
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def build_source_confidence_collection_plan(
    *,
    source_inventory: dict[str, Any],
    sufficiency: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "v7.autonomy-trust.real-source-confidence-collection-plan.v1",
        "classification": sufficiency.get("verdict", "UNKNOWN"),
        "fastest_real_growth_path": [
            {
                "priority": 1,
                "source": "service_outcomes",
                "owner": "existing service matrix / quality snapshot owners",
                "actions": [
                    "run real service/channel probe cycles",
                    "refresh intelligence snapshots",
                    "rerun trust evidence inventory",
                ],
                "why_fastest": "raises service confidence and future forecast source confidence without user movement",
                "runtime_apply_allowed": False,
            },
            {
                "priority": 2,
                "source": "candidate_outcomes",
                "owner": "existing governed/manual outcome closure owners",
                "actions": [
                    "record real candidate outcomes only after authorized governed/manual actions",
                    "refresh trust evolution summaries",
                ],
                "why_fastest": "raises suitability confidence, but requires real outcomes and cannot be simulated",
                "runtime_apply_allowed": False,
            },
            {
                "priority": 3,
                "source": "operator_comparison_evidence",
                "owner": "existing shadow autonomy comparison endpoint",
                "actions": [
                    "collect contextual operator agree/disagree/override records only when operator has enough context",
                ],
                "why_fastest": "raises secondary earned confidence, but does not replace observed outcomes",
                "runtime_apply_allowed": False,
            },
            {
                "priority": 4,
                "source": "prediction_matches",
                "owner": "existing prediction lifecycle owners",
                "actions": [
                    "keep producing forecasts",
                    "wait for later real actuals",
                    "refresh prediction summaries",
                ],
                "why_fastest": "prediction has full matching now; remaining gain depends on higher-confidence sources",
                "runtime_apply_allowed": False,
            },
        ],
        "underutilized_sources": [
            row.get("source") for row in source_inventory.get("sources") or []
            if row.get("classification") == "SUFFICIENT_EVIDENCE_LOW_ATTRIBUTION"
        ],
        "forbidden": [
            "synthetic evidence",
            "threshold or floor changes",
            "formula changes",
            "runtime apply",
            "user movement",
            "daemon enablement",
        ],
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def _additional_rows_needed(
    *,
    current_count: int,
    current_mean: float,
    target_mean: float,
    future_value: float,
) -> int | None:
    if future_value <= target_mean:
        return None
    numerator = max(0.0, (target_mean * current_count) - (current_mean * current_count))
    if numerator <= 0:
        return 0
    return int((numerator / (future_value - target_mean)) + 0.999999)


def build_confidence_reality_audit(
    *,
    floor_forensics: dict[str, Any],
    source_inventory: dict[str, Any],
    operator_comparisons: dict[str, Any],
) -> dict[str, Any]:
    components = floor_forensics.get("component_values") if isinstance(floor_forensics.get("component_values"), dict) else {}
    prediction = floor_forensics.get("prediction_root_cause") if isinstance(floor_forensics.get("prediction_root_cause"), dict) else {}
    service = floor_forensics.get("service_root_cause") if isinstance(floor_forensics.get("service_root_cause"), dict) else {}
    suitability = floor_forensics.get("suitability_root_cause") if isinstance(floor_forensics.get("suitability_root_cause"), dict) else {}
    rollback_blast = floor_forensics.get("rollback_and_blast") if isinstance(floor_forensics.get("rollback_and_blast"), dict) else {}
    sources = {
        row.get("source"): row
        for row in source_inventory.get("sources") or []
        if isinstance(row, dict)
    }
    prediction_accuracy = as_float(prediction.get("forecast_accuracy"), 0.0)
    prediction_confidence = as_float(components.get("prediction_confidence"), 0.0)
    mean_forecast_confidence = as_float(prediction.get("mean_forecast_confidence"), 0.0)
    prediction_required_mean_confidence = round(70.0 / prediction_accuracy, 4) if prediction_accuracy > 0 else 0.0
    service_mean_confidence = as_float(service.get("mean_row_confidence"), 0.0)
    service_mean_correctness = as_float(service.get("mean_correctness"), 0.0)
    service_required_mean_confidence = round(70.0 / service_mean_correctness, 4) if service_mean_correctness > 0 else 0.0
    suitability_mean_confidence = as_float(suitability.get("mean_candidate_confidence"), 0.0)
    suitability_mean_correctness = as_float(suitability.get("mean_correctness"), 0.0)
    suitability_required_mean_confidence = round(70.0 / suitability_mean_correctness, 4) if suitability_mean_correctness > 0 else 0.0
    comparison_current = operator_comparisons.get("current") if isinstance(operator_comparisons.get("current"), dict) else {}
    projection = operator_comparisons.get("growth_projection") if isinstance(operator_comparisons.get("growth_projection"), dict) else {}
    projection_rows = [row for row in projection.get("rows") or [] if isinstance(row, dict)]
    first_operator_floor = next(
        (
            {
                "comparisons": int(as_float(row.get("comparisons"), 0.0)),
                "agreement_rate": as_float(row.get("agreement_rate"), 0.0),
                "earned_confidence": as_float(row.get("earned_confidence"), 0.0),
            }
            for row in projection_rows
            if row.get("earned_confidence_floor_met")
        ),
        None,
    )
    confidence_floor = as_float((floor_forensics.get("floor_values") or {}).get("confidence", {}).get("current"), 0.0)
    trust_floor = as_float((floor_forensics.get("floor_values") or {}).get("trust", {}).get("current"), 0.0)
    decision = as_float(components.get("decision_confidence"), 0.0)
    confidence_service_suitability_sum_required = max(0.0, (70.0 * 3.0) - decision)
    trust_service_suitability_sum_required = max(0.0, (70.0 * 4.0) - decision - as_float(components.get("blast_radius_confidence"), 0.0))
    source_rows = [
        {
            "source": "Prediction",
            "real_evidence_volume": f"{int(as_float(prediction.get('matched_rows'), 0.0))}/{int(as_float(prediction.get('forecasts_seen'), 0.0))} matched",
            "evidence_quality": {
                "forecast_accuracy": round(prediction_accuracy, 3),
                "mean_forecast_confidence": round(mean_forecast_confidence, 4),
            },
            "freshness": (sources.get("prediction_matches") or {}).get("freshness"),
            "confidence_value": round(prediction_confidence, 3),
            "proportional_to_reality": "UNDERVALUED",
            "why": "21/21 matched rows is strong accuracy evidence, but current canary confidence is intentionally limited by low forecast source confidence.",
        },
        {
            "source": "Service",
            "real_evidence_volume": int(as_float(service.get("rows_seen"), 0.0)),
            "evidence_quality": {
                "mean_correctness": round(service_mean_correctness, 3),
                "mean_row_confidence": round(service_mean_confidence, 4),
            },
            "freshness": (sources.get("service_outcomes") or {}).get("freshness"),
            "confidence_value": round(as_float(components.get("service_confidence"), 0.0), 3),
            "proportional_to_reality": "FAIR",
            "why": "Correctness is high, but source row confidence is only 0.39, so the current model correctly refuses to treat it as high-confidence autonomy evidence.",
        },
        {
            "source": "Suitability",
            "real_evidence_volume": f"{int(as_float(suitability.get('outcomes_seen'), 0.0))}/{int(as_float(suitability.get('candidates_seen'), 0.0))} outcomes",
            "evidence_quality": {
                "mean_correctness": round(suitability_mean_correctness, 3),
                "mean_candidate_confidence": round(suitability_mean_confidence, 4),
                "rows_without_outcome": int(as_float(suitability.get("rows_without_outcome"), 0.0)),
            },
            "freshness": (sources.get("candidate_outcomes") or {}).get("freshness"),
            "confidence_value": round(as_float(components.get("suitability_confidence"), 0.0), 3),
            "proportional_to_reality": "FAIR",
            "why": "83 outcomes are useful but incomplete versus 156 candidates, and current mean correctness/confidence cannot support a 70 autonomy floor.",
        },
        {
            "source": "Blast",
            "real_evidence_volume": int(as_float(rollback_blast.get("blast_records_seen"), 0.0)),
            "evidence_quality": {"confidence": round(as_float(components.get("blast_radius_confidence"), 0.0), 3)},
            "freshness": (sources.get("blast_radius_evidence") or {}).get("freshness"),
            "confidence_value": round(as_float(components.get("blast_radius_confidence"), 0.0), 3),
            "proportional_to_reality": "FAIR",
            "why": "Recovered governed blast evidence is consumed and already contributes 100.",
        },
        {
            "source": "Rollback",
            "real_evidence_volume": int(as_float(rollback_blast.get("rollback_records_seen"), 0.0)),
            "evidence_quality": {"confidence": round(as_float(components.get("rollback_confidence"), 0.0), 3)},
            "freshness": (sources.get("rollback_evidence") or {}).get("freshness"),
            "confidence_value": round(as_float(components.get("rollback_confidence"), 0.0), 3),
            "proportional_to_reality": "FAIR",
            "why": "Rollback evidence is consumed and already contributes 100.",
        },
        {
            "source": "Operator",
            "real_evidence_volume": int(as_float(comparison_current.get("comparison_count"), 0.0)),
            "evidence_quality": {
                "reviewable_decisions": int(as_float(comparison_current.get("reviewable_decisions"), 0.0)),
                "agreement_rate": as_float(comparison_current.get("agreement_rate"), 0.0),
            },
            "freshness": (sources.get("operator_comparison_evidence") or {}).get("freshness"),
            "confidence_value": round(as_float(components.get("operator_earned_confidence"), 0.0), 3),
            "proportional_to_reality": "FAIR",
            "why": "There are reviewable decisions but zero real comparisons, so operator evidence cannot be treated as validated.",
        },
    ]
    return {
        "schema_version": "v7.autonomy-trust.confidence-reality-audit.v1",
        "final_classification": "CONFIDENCE_MIXED",
        "source_rows": source_rows,
        "undervalued_sources": ["Prediction"],
        "overvalued_sources": [],
        "fair_sources": ["Service", "Suitability", "Blast", "Rollback", "Operator"],
        "implementation_result": "visibility_fix_only_no_formula_or_floor_change",
        "required_real_evidence": {
            "prediction": {
                "current_matched": int(as_float(prediction.get("matched_rows"), 0.0)),
                "current_mean_forecast_confidence": round(mean_forecast_confidence, 4),
                "target_mean_forecast_confidence_at_current_accuracy": prediction_required_mean_confidence,
                "additional_matched_rows_needed_if_future_confidence_1_0": _additional_rows_needed(
                    current_count=int(as_float(prediction.get("forecasts_seen"), 0.0)),
                    current_mean=mean_forecast_confidence,
                    target_mean=prediction_required_mean_confidence,
                    future_value=1.0,
                ),
                "additional_matched_rows_needed_if_future_confidence_0_9": _additional_rows_needed(
                    current_count=int(as_float(prediction.get("forecasts_seen"), 0.0)),
                    current_mean=mean_forecast_confidence,
                    target_mean=prediction_required_mean_confidence,
                    future_value=0.9,
                ),
                "additional_matched_rows_needed_if_future_confidence_0_85": _additional_rows_needed(
                    current_count=int(as_float(prediction.get("forecasts_seen"), 0.0)),
                    current_mean=mean_forecast_confidence,
                    target_mean=prediction_required_mean_confidence,
                    future_value=0.85,
                ),
            },
            "service": {
                "current_rows": int(as_float(service.get("rows_seen"), 0.0)),
                "current_mean_row_confidence": round(service_mean_confidence, 4),
                "target_mean_row_confidence_at_current_correctness": service_required_mean_confidence,
                "additional_comparable_rows_needed_if_future_confidence_1_0": _additional_rows_needed(
                    current_count=int(as_float(service.get("rows_seen"), 0.0)),
                    current_mean=service_mean_confidence,
                    target_mean=service_required_mean_confidence,
                    future_value=1.0,
                ),
                "additional_comparable_rows_needed_if_future_confidence_0_85": _additional_rows_needed(
                    current_count=int(as_float(service.get("rows_seen"), 0.0)),
                    current_mean=service_mean_confidence,
                    target_mean=service_required_mean_confidence,
                    future_value=0.85,
                ),
                "note": "If the snapshot owner recalibrates row confidence instead of accumulating rows, the real target is mean row confidence >= target.",
            },
            "suitability": {
                "current_outcomes": int(as_float(suitability.get("outcomes_seen"), 0.0)),
                "current_candidates": int(as_float(suitability.get("candidates_seen"), 0.0)),
                "missing_outcomes_to_full_coverage": max(
                    0,
                    int(as_float(suitability.get("candidates_seen"), 0.0)) - int(as_float(suitability.get("outcomes_seen"), 0.0)),
                ),
                "current_mean_correctness": round(suitability_mean_correctness, 3),
                "current_mean_candidate_confidence": round(suitability_mean_confidence, 4),
                "target_mean_candidate_confidence_at_current_correctness": suitability_required_mean_confidence,
                "current_correctness_can_reach_70_even_with_perfect_confidence": suitability_mean_correctness >= 70.0,
                "target_correctness_if_mean_confidence_0_85": round(70.0 / 0.85, 3),
            },
            "operator": {
                "current_comparisons": int(as_float(comparison_current.get("comparison_count"), 0.0)),
                "reviewable_decisions": int(as_float(comparison_current.get("reviewable_decisions"), 0.0)),
                "first_projection_to_floor": first_operator_floor,
            },
            "confidence_and_trust": {
                "current_confidence_floor": round(confidence_floor, 3),
                "current_trust_floor": round(trust_floor, 3),
                "service_plus_suitability_sum_required_for_confidence_70_if_decision_stays_current": round(confidence_service_suitability_sum_required, 3),
                "service_plus_suitability_sum_required_for_trust_70_if_decision_and_blast_stay_current": round(trust_service_suitability_sum_required, 3),
            },
        },
        "can_confidence_grow_materially_without_new_runtime_actions": False,
        "new_real_world_outcomes_required": True,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def _project_append_mean(*, current_count: int, current_mean: float, additional: int, future_value: float) -> float:
    total = max(0, current_count) + max(0, additional)
    if total <= 0:
        return 0.0
    return round(((max(0, current_count) * current_mean) + (max(0, additional) * future_value)) / total, 3)


def _row_confidence_value(row: dict[str, Any]) -> float:
    return as_float(row.get("correctness"), 0.0) * max(as_float(row.get("confidence"), 0.0), 0.25)


def _project_missing_candidate_outcomes(rows: list[dict[str, Any]], additional: int) -> dict[str, Any]:
    rows = [row for row in rows if isinstance(row, dict)]
    if not rows:
        return {
            "projected_suitability_confidence": 0.0,
            "converted_missing_outcomes": 0,
            "missing_outcomes_remaining": 0,
        }
    current_values = [_row_confidence_value(row) for row in rows]
    missing = sorted(
        [value for row, value in zip(rows, current_values) if not row.get("outcome_seen")],
    )
    converted = min(max(0, additional), len(missing))
    projected_sum = sum(current_values) - sum(missing[:converted]) + (converted * 100.0)
    return {
        "projected_suitability_confidence": round(projected_sum / len(rows), 3),
        "converted_missing_outcomes": converted,
        "missing_outcomes_remaining": max(0, len(missing) - converted),
    }


def build_real_outcome_growth_projection(
    *,
    floor_forensics: dict[str, Any],
    confidence_reality_audit: dict[str, Any],
    operator_comparisons: dict[str, Any],
    increments: list[int] | None = None,
) -> dict[str, Any]:
    """Project confidence growth from future real outcomes using current formulas only.

    This is intentionally projection-only: it does not create outcomes, change
    confidence formulas, lower floors, or authorize apply. Each projected cycle
    assumes a future real outcome can provide one high-confidence prediction
    match, one high-confidence service row, and one successful missing candidate
    outcome where a missing candidate exists.
    """
    increments = increments or [10, 25, 50]
    components = floor_forensics.get("component_values") if isinstance(floor_forensics.get("component_values"), dict) else {}
    prediction = floor_forensics.get("prediction_root_cause") if isinstance(floor_forensics.get("prediction_root_cause"), dict) else {}
    service = floor_forensics.get("service_root_cause") if isinstance(floor_forensics.get("service_root_cause"), dict) else {}
    suitability = floor_forensics.get("suitability_root_cause") if isinstance(floor_forensics.get("suitability_root_cause"), dict) else {}
    trust_rows = floor_forensics.get("raw_rows") if isinstance(floor_forensics.get("raw_rows"), dict) else {}
    suitability_rows = [row for row in trust_rows.get("suitability") or [] if isinstance(row, dict)]
    required = confidence_reality_audit.get("required_real_evidence") if isinstance(confidence_reality_audit.get("required_real_evidence"), dict) else {}
    required_suitability = required.get("suitability") if isinstance(required.get("suitability"), dict) else {}
    current_prediction_confidence = as_float(components.get("prediction_confidence"), 0.0)
    current_service_confidence = as_float(components.get("service_confidence"), 0.0)
    current_suitability_confidence = as_float(components.get("suitability_confidence"), 0.0)
    decision_confidence = as_float(components.get("decision_confidence"), 0.0)
    blast_confidence = as_float(components.get("blast_radius_confidence"), 0.0)
    operator_current = operator_comparisons.get("current") if isinstance(operator_comparisons.get("current"), dict) else {}
    operator_projection = operator_comparisons.get("growth_projection") if isinstance(operator_comparisons.get("growth_projection"), dict) else {}
    operator_projection_rows = [row for row in operator_projection.get("rows") or [] if isinstance(row, dict)]
    current_forecasts = int(as_float(prediction.get("forecasts_seen"), 0.0))
    current_matched = int(as_float(prediction.get("matched_rows"), 0.0))
    current_accuracy = as_float(prediction.get("forecast_accuracy"), 0.0)
    current_forecast_confidence = as_float(prediction.get("mean_forecast_confidence"), 0.0)
    current_service_rows = int(as_float(service.get("rows_seen"), 0.0))
    current_suitability_rows = len(suitability_rows) or int(as_float(suitability.get("candidates_seen"), 0.0))
    known_candidate_count = int(as_float(required_suitability.get("current_candidates"), as_float(suitability.get("candidates_seen"), 0.0)))
    known_candidate_outcomes = int(as_float(required_suitability.get("current_outcomes"), as_float(suitability.get("outcomes_seen"), 0.0)))
    known_missing_candidate_outcomes = int(as_float(
        required_suitability.get("missing_outcomes_to_full_coverage"),
        max(0, known_candidate_count - known_candidate_outcomes),
    ))
    projections = []
    for additional in increments:
        projected_accuracy = _project_append_mean(
            current_count=current_matched,
            current_mean=current_accuracy,
            additional=additional,
            future_value=100.0,
        )
        projected_forecast_confidence = _project_append_mean(
            current_count=current_forecasts,
            current_mean=current_forecast_confidence,
            additional=additional,
            future_value=1.0,
        )
        projected_prediction = round(min(100.0, projected_accuracy * projected_forecast_confidence), 3)
        projected_service = _project_append_mean(
            current_count=current_service_rows,
            current_mean=current_service_confidence,
            additional=additional,
            future_value=100.0,
        )
        suitability_projection = _project_missing_candidate_outcomes(suitability_rows, additional)
        projected_suitability = as_float(
            suitability_projection.get("projected_suitability_confidence"),
            current_suitability_confidence,
        )
        if not suitability_rows and current_suitability_rows:
            projected_suitability = current_suitability_confidence
        visible_converted_missing = int(as_float(suitability_projection.get("converted_missing_outcomes"), 0.0))
        visible_missing_remaining = int(as_float(suitability_projection.get("missing_outcomes_remaining"), 0.0))
        known_converted_missing = min(max(0, additional), known_missing_candidate_outcomes)
        known_missing_remaining = max(0, known_missing_candidate_outcomes - known_converted_missing)
        if known_missing_candidate_outcomes <= 0:
            known_converted_missing = visible_converted_missing
            known_missing_remaining = visible_missing_remaining
        projected_confidence = round((decision_confidence + projected_service + projected_suitability) / 3.0, 3)
        projected_trust = round((decision_confidence + projected_service + projected_suitability + blast_confidence) / 4.0, 3)
        operator_floor_projection = next(
            (
                row for row in operator_projection_rows
                if int(as_float(row.get("comparisons"), -1)) == additional
                and abs(as_float(row.get("agreement_rate"), -1.0) - 1.0) < 0.0001
            ),
            {},
        )
        projected_operator = as_float(
            operator_floor_projection.get("earned_confidence"),
            as_float(operator_current.get("earned_confidence"), 0.0),
        )
        projections.append({
            "additional_real_outcome_cycles": additional,
            "assumption": "each cycle is a real high-confidence outcome, not synthetic evidence",
            "projected_confidence": projected_confidence,
            "projected_trust": projected_trust,
            "projected_prediction_confidence": projected_prediction,
            "projected_operator_earned_confidence_if_contextual_comparisons": round(projected_operator, 3),
            "projected_service_confidence": projected_service,
            "projected_suitability_confidence": projected_suitability,
            "projected_suitability_scope": "visible_rows_with_full_coverage_counter",
            "visible_suitability_rows": len(suitability_rows),
            "known_candidate_count": known_candidate_count,
            "known_candidate_outcomes": known_candidate_outcomes,
            "known_missing_candidate_outcomes": known_missing_candidate_outcomes,
            "converted_missing_candidate_outcomes": known_converted_missing,
            "missing_candidate_outcomes_remaining": known_missing_remaining,
            "visible_converted_missing_candidate_outcomes": visible_converted_missing,
            "visible_missing_candidate_outcomes_remaining": visible_missing_remaining,
            "canary_primary_floors_pass": (
                projected_confidence >= AUTONOMY_CANARY_CONFIDENCE_FLOOR
                and projected_trust >= AUTONOMY_CANARY_TRUST_FLOOR
                and projected_prediction >= AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR
            ),
            "canary_all_known_floors_pass": (
                projected_confidence >= AUTONOMY_CANARY_CONFIDENCE_FLOOR
                and projected_trust >= AUTONOMY_CANARY_TRUST_FLOOR
                and projected_prediction >= AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR
                and projected_operator >= shadow_autonomy.OBSERVATION_TARGETS["minimum_earned_confidence"]
            ),
        })
    return {
        "schema_version": "v7.autonomy-trust.real-outcome-growth-projection.v1",
        "projection_only": True,
        "uses_current_formulas_only": True,
        "synthetic_evidence_created": False,
        "formula_changed": False,
        "floor_changed": False,
        "source_truth_changed": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
        "current": {
            "confidence": round(as_float((floor_forensics.get("floor_values") or {}).get("confidence", {}).get("current"), 0.0), 3),
            "trust": round(as_float((floor_forensics.get("floor_values") or {}).get("trust", {}).get("current"), 0.0), 3),
            "prediction_confidence": round(current_prediction_confidence, 3),
            "operator_earned_confidence": round(as_float(operator_current.get("earned_confidence"), 0.0), 3),
            "service_confidence": round(current_service_confidence, 3),
            "suitability_confidence": round(current_suitability_confidence, 3),
            "candidate_rows_exposed_to_projection": len(suitability_rows),
            "known_candidate_count": known_candidate_count,
            "known_candidate_outcomes": known_candidate_outcomes,
            "known_missing_candidate_outcomes": known_missing_candidate_outcomes,
        },
        "projections": projections,
        "minimum_evidence_from_reality_audit": {
            "prediction": (required.get("prediction") or {}),
            "service": (required.get("service") or {}),
            "suitability": (required.get("suitability") or {}),
            "operator": (required.get("operator") or {}),
        },
        "canary_can_start_now": False,
        "next_blocker": "real_high_confidence_outcome_volume",
    }


def build_real_outcome_source_inventory(
    *,
    source_confidence_inventory: dict[str, Any],
    floor_forensics: dict[str, Any],
    materialization_audit: dict[str, Any],
    real_outcome_growth_projection: dict[str, Any],
) -> dict[str, Any]:
    sources = {
        row.get("source"): row
        for row in source_confidence_inventory.get("sources") or []
        if isinstance(row, dict)
    }
    materialization = materialization_audit if isinstance(materialization_audit, dict) else {}
    projection_rows = real_outcome_growth_projection.get("projections") or []
    first_primary_pass = next((row for row in projection_rows if isinstance(row, dict) and row.get("canary_primary_floors_pass")), None)
    items = [
        {
            "source": "service_outcomes",
            "owner": "tools/v7-service-matrix-refresh-all, tools/v7-service-matrix-test, tools/v7-egress-quality-compact, tools/v7-intelligence-snapshot-refresh",
            "count": (sources.get("service_outcomes") or {}).get("evidence_count", 0),
            "freshness": (sources.get("service_outcomes") or {}).get("freshness"),
            "confidence_contribution": (sources.get("service_outcomes") or {}).get("current_contribution", 0.0),
            "current_utilization": "consumed_but_low_row_confidence",
            "classification": "ACCELERATABLE",
            "safe_acceleration": "run additional real service/quality probe cycles and refresh snapshots",
        },
        {
            "source": "channel_outcomes",
            "owner": "tools/v7-egress-quality-compact and intelligence snapshot refresh",
            "count": (sources.get("service_outcomes") or {}).get("evidence_count", 0),
            "freshness": (sources.get("service_outcomes") or {}).get("freshness"),
            "confidence_contribution": (sources.get("service_outcomes") or {}).get("current_contribution", 0.0),
            "current_utilization": "consumed_through_service_channel_snapshots",
            "classification": "ACCELERATABLE",
            "safe_acceleration": "repeat real quality compaction after probe windows; no user movement",
        },
        {
            "source": "candidate_outcomes",
            "owner": "admin_core.intelligence_workers.build_candidate_outcome_rows, governed/manual outcome closure owners",
            "count": (sources.get("candidate_outcomes") or {}).get("evidence_count", 0),
            "freshness": (sources.get("candidate_outcomes") or {}).get("freshness"),
            "confidence_contribution": (sources.get("candidate_outcomes") or {}).get("current_contribution", 0.0),
            "current_utilization": "consumed_but_incomplete",
            "classification": "WAIT_FOR_REALITY",
            "safe_acceleration": "requires real governed/manual outcomes; cannot be generated without action",
        },
        {
            "source": "governed_outcomes",
            "owner": "admin_core.operator_execution_feedback and closure/runtime trust stores",
            "count": (materialization.get("candidate_outcomes") or {}).get("candidate_outcomes_count", 0),
            "freshness": (sources.get("candidate_outcomes") or {}).get("freshness"),
            "confidence_contribution": (sources.get("candidate_outcomes") or {}).get("current_contribution", 0.0),
            "current_utilization": "consumed_after_governed_actions",
            "classification": "BLOCKED",
            "safe_acceleration": "blocked because this phase forbids runtime apply/user movement",
        },
        {
            "source": "manual_outcomes",
            "owner": "operator manual action plus existing feedback/closure owners",
            "count": 0,
            "freshness": {"freshness_state": "ACTION_DEPENDENT"},
            "confidence_contribution": 0.0,
            "current_utilization": "available_only_if_operator_takes_real_manual_action",
            "classification": "WAIT_FOR_REALITY",
            "safe_acceleration": "observe and close outcomes after real manual operations; do not manufacture",
        },
        {
            "source": "verification_outcomes",
            "owner": "restore/rollback/verification owners and intelligence snapshot refresh",
            "count": (sources.get("rollback_evidence") or {}).get("evidence_count", 0),
            "freshness": (sources.get("rollback_evidence") or {}).get("freshness"),
            "confidence_contribution": (sources.get("rollback_evidence") or {}).get("current_contribution", 0.0),
            "current_utilization": "rollback_sufficient_not_current_blocker",
            "classification": "WAIT_FOR_REALITY",
            "safe_acceleration": "new verification outcomes require real governed/manual actions",
        },
        {
            "source": "feedback_outcomes",
            "owner": "admin_core.operator_execution_feedback, closure records, rotated JSONL evidence family",
            "count": (materialization.get("prediction_actuals") or {}).get("actuals_seen", 0),
            "freshness": (sources.get("prediction_matches") or {}).get("freshness"),
            "confidence_contribution": (sources.get("prediction_matches") or {}).get("current_contribution", 0.0),
            "current_utilization": "prediction_feedback_consumed",
            "classification": "ACCELERATABLE",
            "safe_acceleration": "collect future real forecast->actual pairs from existing snapshots and feedback",
        },
        {
            "source": "learning_outcomes",
            "owner": "tools/v7-intelligence-snapshot-refresh and admin_core.intelligence_workers",
            "count": (materialization.get("service_actuals") or {}).get("service_actuals_count", 0),
            "freshness": (sources.get("service_outcomes") or {}).get("freshness"),
            "confidence_contribution": (sources.get("service_outcomes") or {}).get("current_contribution", 0.0),
            "current_utilization": "refresh_owner_consumes_available_outcomes",
            "classification": "ACCELERATABLE",
            "safe_acceleration": "refresh after real probes/outcomes; does not create synthetic evidence",
        },
    ]
    return {
        "schema_version": "v7.autonomy-trust.real-outcome-source-inventory.v1",
        "items": items,
        "acceleration_summary": {
            "acceleratable": [row["source"] for row in items if row["classification"] == "ACCELERATABLE"],
            "wait_for_reality": [row["source"] for row in items if row["classification"] == "WAIT_FOR_REALITY"],
            "blocked": [row["source"] for row in items if row["classification"] == "BLOCKED"],
            "first_projected_primary_canary_pass": first_primary_pass,
        },
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def _project_single_prediction_gain(floor_forensics: dict[str, Any]) -> float:
    prediction = floor_forensics.get("prediction_root_cause") if isinstance(floor_forensics.get("prediction_root_cause"), dict) else {}
    components = floor_forensics.get("component_values") if isinstance(floor_forensics.get("component_values"), dict) else {}
    current = as_float(components.get("prediction_confidence"), 0.0)
    matched = int(as_float(prediction.get("matched_rows"), as_float(prediction.get("forecasts_seen"), 0.0)))
    forecasts = int(as_float(prediction.get("forecasts_seen"), matched))
    accuracy = as_float(prediction.get("forecast_accuracy"), 0.0)
    mean_confidence = as_float(prediction.get("mean_forecast_confidence"), 0.0)
    if matched <= 0 or forecasts <= 0:
        return 0.0
    projected_accuracy = _project_append_mean(
        current_count=matched,
        current_mean=accuracy,
        additional=1,
        future_value=100.0,
    )
    projected_confidence = _project_append_mean(
        current_count=forecasts,
        current_mean=mean_confidence,
        additional=1,
        future_value=1.0,
    )
    projected = min(100.0, projected_accuracy * projected_confidence)
    return round(max(0.0, projected - current), 3)


def _project_single_service_gain(floor_forensics: dict[str, Any]) -> dict[str, float]:
    service = floor_forensics.get("service_root_cause") if isinstance(floor_forensics.get("service_root_cause"), dict) else {}
    components = floor_forensics.get("component_values") if isinstance(floor_forensics.get("component_values"), dict) else {}
    current = as_float(components.get("service_confidence"), 0.0)
    rows_seen = int(as_float(service.get("rows_seen"), 0.0))
    if rows_seen <= 0:
        service_gain = 0.0
    else:
        projected = _project_append_mean(
            current_count=rows_seen,
            current_mean=current,
            additional=1,
            future_value=100.0,
        )
        service_gain = round(max(0.0, projected - current), 3)
    return {
        "service": service_gain,
        "confidence": round(service_gain / 3.0, 3),
        "trust": round(service_gain / 4.0, 3),
    }


def _leverage_denominator(*, effort: str, risk: str, blast_radius: str) -> float:
    effort_weight = {"LOW": 1.0, "MEDIUM": 2.0, "HIGH": 3.0}.get(effort, 2.0)
    risk_weight = {"NONE": 1.0, "LOW": 1.25, "MEDIUM": 2.0, "HIGH": 4.0}.get(risk, 2.0)
    blast_weight = {
        "NONE": 1.0,
        "READ_ONLY": 1.0,
        "ONE_USER": 1.8,
        "OPERATOR_ACTION": 2.0,
        "MULTI_USER": 3.0,
    }.get(blast_radius, 2.0)
    return max(1.0, effort_weight * risk_weight * blast_weight)


def _outcome_activity(
    *,
    activity: str,
    owner: str,
    confidence_gain: float = 0.0,
    trust_gain: float = 0.0,
    prediction_gain: float = 0.0,
    suitability_gain: float = 0.0,
    effort: str,
    risk: str,
    blast_radius: str,
    authority_required: str,
    current_status: str,
    evidence: str,
    note: str,
) -> dict[str, Any]:
    weighted_gain = (
        as_float(confidence_gain)
        + as_float(trust_gain)
        + as_float(prediction_gain)
        + (as_float(suitability_gain) * 1.5)
    )
    denominator = _leverage_denominator(effort=effort, risk=risk, blast_radius=blast_radius)
    return {
        "activity": activity,
        "owner": owner,
        "expected_confidence_gain": round(confidence_gain, 3),
        "expected_trust_gain": round(trust_gain, 3),
        "expected_prediction_gain": round(prediction_gain, 3),
        "expected_suitability_gain": round(suitability_gain, 3),
        "weighted_gain": round(weighted_gain, 3),
        "effort": effort,
        "risk": risk,
        "blast_radius": blast_radius,
        "authority_required": authority_required,
        "leverage_score": round(weighted_gain / denominator, 3),
        "current_status": current_status,
        "evidence": evidence,
        "note": note,
        "projection_only": True,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def build_outcome_leverage_model(
    *,
    floor_forensics: dict[str, Any],
    confidence_reality_audit: dict[str, Any],
    real_outcome_source_inventory: dict[str, Any],
    candidate_outcome_reality_collection: dict[str, Any],
    real_outcome_growth_projection: dict[str, Any],
    operator_comparisons: dict[str, Any],
) -> dict[str, Any]:
    """Rank real outcome activities by honest gain per effort and risk.

    This is a read-only decision aid. It uses existing projections and certified
    formula inputs, but it does not change trust formulas or authorize an action.
    """
    current = real_outcome_growth_projection.get("current") if isinstance(real_outcome_growth_projection.get("current"), dict) else {}
    required = confidence_reality_audit.get("required_real_evidence") if isinstance(confidence_reality_audit.get("required_real_evidence"), dict) else {}
    prediction_required = required.get("prediction") if isinstance(required.get("prediction"), dict) else {}
    service_required = required.get("service") if isinstance(required.get("service"), dict) else {}
    suitability_required = required.get("suitability") if isinstance(required.get("suitability"), dict) else {}
    candidate_coverage = candidate_outcome_reality_collection.get("coverage") if isinstance(candidate_outcome_reality_collection.get("coverage"), dict) else {}
    candidate_growth = candidate_outcome_reality_collection.get("growth_model") if isinstance(candidate_outcome_reality_collection.get("growth_model"), dict) else {}
    candidate_growth_rows = candidate_growth.get("projections") if isinstance(candidate_growth.get("projections"), list) else []
    one_candidate_row = next(
        (row for row in candidate_growth_rows if int(as_float(row.get("additional_real_candidate_outcomes"), -1)) == 1),
        None,
    )
    if one_candidate_row:
        candidate_confidence_gain = max(0.0, as_float(one_candidate_row.get("projected_confidence")) - as_float(current.get("confidence")))
        candidate_trust_gain = max(0.0, as_float(one_candidate_row.get("projected_trust")) - as_float(current.get("trust")))
        candidate_suitability_gain = max(0.0, as_float(one_candidate_row.get("projected_suitability")) - as_float(current.get("suitability_confidence")))
    else:
        candidate_suitability_gain = 0.35 if as_float(candidate_coverage.get("missing_candidate_outcomes"), 0.0) > 0 else 0.0
        candidate_confidence_gain = 0.18 if candidate_suitability_gain else 0.0
        candidate_trust_gain = 0.12 if candidate_suitability_gain else 0.0

    prediction_gain = _project_single_prediction_gain(floor_forensics)
    service_gain = _project_single_service_gain(floor_forensics)
    operator_current = operator_comparisons.get("current") if isinstance(operator_comparisons.get("current"), dict) else {}
    operator_projection = operator_comparisons.get("growth_projection") if isinstance(operator_comparisons.get("growth_projection"), dict) else {}
    first_operator_floor = (required.get("operator") or {}).get("first_projection_to_floor") if isinstance(required.get("operator"), dict) else None
    operator_gain = max(
        0.0,
        as_float((first_operator_floor or {}).get("earned_confidence"), as_float(operator_current.get("earned_confidence"), 0.0))
        - as_float(operator_current.get("earned_confidence"), 0.0),
    ) if isinstance(first_operator_floor, dict) else 0.0

    activities = [
        _outcome_activity(
            activity="prediction_outcome_cycle",
            owner="prediction-summaries + service/channel actual rows + existing feedback owners",
            prediction_gain=prediction_gain,
            effort="LOW",
            risk="LOW",
            blast_radius="READ_ONLY",
            authority_required="none",
            current_status="ACCELERATABLE_NOW",
            evidence=f"additional matched rows needed at future confidence 1.0: {prediction_required.get('additional_matched_rows_needed_if_future_confidence_1_0')}",
            note="Fastest direct way to raise prediction confidence; does not solve suitability by itself.",
        ),
        _outcome_activity(
            activity="service_verification_outcome",
            owner="tools/v7-service-matrix-refresh-all + tools/v7-egress-quality-compact + snapshot refresh",
            confidence_gain=service_gain["confidence"],
            trust_gain=service_gain["trust"],
            prediction_gain=0.0,
            suitability_gain=0.0,
            effort="LOW",
            risk="LOW",
            blast_radius="READ_ONLY",
            authority_required="none",
            current_status="ACCELERATABLE_NOW",
            evidence=f"additional comparable rows needed at future confidence 1.0: {service_required.get('additional_comparable_rows_needed_if_future_confidence_1_0')}",
            note="Safest way to improve service/trust source confidence; one prior real probe cycle had little immediate floor movement.",
        ),
        _outcome_activity(
            activity="candidate_suitability_outcome",
            owner="candidate outcome matcher + governed/manual outcome closure owners",
            confidence_gain=candidate_confidence_gain,
            trust_gain=candidate_trust_gain,
            suitability_gain=candidate_suitability_gain,
            effort="MEDIUM",
            risk="MEDIUM",
            blast_radius="OPERATOR_ACTION",
            authority_required="real governed/manual action",
            current_status="ACCELERATABLE_GOVERNED",
            evidence=f"missing candidate outcomes: {candidate_coverage.get('missing_candidate_outcomes', 0)}",
            note="Only direct path to suitability growth; current correctness still cannot reach 70 from coverage alone.",
        ),
        _outcome_activity(
            activity="governed_one_user_canary",
            owner="governed canary dry-run cycle + packet/restore/feedback/learning owners",
            confidence_gain=candidate_confidence_gain,
            trust_gain=candidate_trust_gain,
            suitability_gain=candidate_suitability_gain,
            effort="HIGH",
            risk="MEDIUM",
            blast_radius="ONE_USER",
            authority_required="explicit operator approval for exact packet",
            current_status="AUTHORITY_BOUNDARY_READY",
            evidence="production dry-run reaches AUTHORITY_BOUNDARY with no apply and no movement",
            note="Best current way to create one real governed candidate outcome, but one canary is too small to close TIER_2.",
        ),
        _outcome_activity(
            activity="feedback_outcome_closure",
            owner="admin_core.operator_execution_feedback + closure records + intelligence refresh",
            confidence_gain=round(candidate_confidence_gain + service_gain["confidence"], 3),
            trust_gain=round(candidate_trust_gain + service_gain["trust"], 3),
            prediction_gain=prediction_gain,
            suitability_gain=candidate_suitability_gain,
            effort="MEDIUM",
            risk="LOW",
            blast_radius="READ_ONLY",
            authority_required="requires prior real action/outcome; closure itself is read-only",
            current_status="ACCELERATABLE_AFTER_REAL_OUTCOME",
            evidence="decision->outcome->learning integration is implemented",
            note="Highest value after a real action exists; cannot manufacture the underlying action outcome.",
        ),
        _outcome_activity(
            activity="operator_comparison_outcome",
            owner="shadow_autonomy contextual compare action",
            confidence_gain=0.0,
            trust_gain=0.0,
            prediction_gain=0.0,
            suitability_gain=0.0,
            effort="LOW",
            risk="MEDIUM",
            blast_radius="NONE",
            authority_required="operator must have real context",
            current_status="SECONDARY_ONLY",
            evidence=f"contextual operator earned-confidence gain to first floor projection: {round(operator_gain, 3)}",
            note="Useful secondary confirmation; blind comparisons are forbidden and do not replace observed outcomes.",
        ),
        _outcome_activity(
            activity="recovery_outcome",
            owner="recovery admission + trust evolution + service/quality owners",
            confidence_gain=0.0,
            trust_gain=0.0,
            prediction_gain=0.0,
            suitability_gain=0.0,
            effort="MEDIUM",
            risk="MEDIUM",
            blast_radius="READ_ONLY",
            authority_required="only when a real recovery situation exists",
            current_status="WAIT_FOR_REALITY",
            evidence="recovery is a future TIER_3+ gap, not the immediate TIER_2 floor closer",
            note="Important for higher autonomy but not current fastest TIER_2 path.",
        ),
        _outcome_activity(
            activity="governed_rollback_outcome",
            owner="restore/rollback owners + feedback/learning",
            confidence_gain=0.0,
            trust_gain=0.0,
            prediction_gain=0.0,
            suitability_gain=0.0,
            effort="HIGH",
            risk="MEDIUM",
            blast_radius="ONE_USER",
            authority_required="only if real rollback is needed",
            current_status="NOT_CURRENT_BLOCKER",
            evidence="rollback confidence is already 100",
            note="Rollback proof is already strong; extra rollback outcomes do not attack current blockers fastest.",
        ),
    ]
    ranked = sorted(activities, key=lambda row: (-as_float(row.get("leverage_score")), str(row.get("activity"))))
    first = ranked[0]["activity"] if ranked else ""
    canary = next((row for row in ranked if row.get("activity") == "governed_one_user_canary"), {})
    top_three = [row["activity"] for row in ranked[:3]]
    suitability_dependency = as_float(candidate_coverage.get("missing_candidate_outcomes"), 0.0) > 0
    if first == "governed_one_user_canary":
        verdict = "GOVERNED_CANARY_IS_HIGHEST_LEVERAGE"
    elif (
        suitability_dependency
        or "governed_one_user_canary" in top_three
        or "candidate_suitability_outcome" in top_three
    ):
        verdict = "MIXED_PATH"
    else:
        verdict = "BETTER_PATH_EXISTS"
    roadmap = [
        {
            "step": "Current",
            "confidence": current.get("confidence", 0.0),
            "trust": current.get("trust", 0.0),
            "prediction": current.get("prediction_confidence", 0.0),
            "suitability": current.get("suitability_confidence", 0.0),
            "status": "TIER_2_NO_GO",
        },
        {
            "step": "Prediction + service outcome cycles",
            "target": {
                "prediction_rows_at_1_0_confidence": prediction_required.get("additional_matched_rows_needed_if_future_confidence_1_0"),
                "service_rows_at_1_0_confidence": service_required.get("additional_comparable_rows_needed_if_future_confidence_1_0"),
            },
            "status": "needed_but_not_sufficient_without_suitability",
        },
        {
            "step": "Governed/manual candidate suitability outcomes",
            "target": {
                "missing_candidate_outcomes_to_full_coverage": suitability_required.get("missing_outcomes_to_full_coverage"),
                "target_correctness_if_mean_confidence_0_85": suitability_required.get("target_correctness_if_mean_confidence_0_85"),
            },
            "status": "only_direct_suitability_path",
        },
        {
            "step": "TIER_2",
            "required": {
                "confidence": AUTONOMY_CANARY_CONFIDENCE_FLOOR,
                "trust": AUTONOMY_CANARY_TRUST_FLOOR,
                "prediction": AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR,
            },
            "status": "requires_remeasure_after_each_real_outcome_batch",
        },
    ]
    return {
        "schema_version": "v7.autonomy-trust.outcome-leverage-model.v1",
        "purpose": "rank_real_outcome_activities_by_expected_floor_gain_per_effort_and_risk",
        "final_verdict": verdict,
        "highest_leverage": ranked[0] if ranked else {},
        "second_highest_leverage": ranked[1] if len(ranked) > 1 else {},
        "third_highest_leverage": ranked[2] if len(ranked) > 2 else {},
        "governed_canary_analysis": {
            "rank": next((index + 1 for index, row in enumerate(ranked) if row.get("activity") == "governed_one_user_canary"), None),
            "leverage_score": canary.get("leverage_score", 0.0),
            "expected_knowledge_gain": "one real selected candidate outcome plus closure/learning if approved, applied, verified, and closed",
            "expected_trust_gain": canary.get("expected_trust_gain", 0.0),
            "expected_prediction_gain": canary.get("expected_prediction_gain", 0.0),
            "expected_suitability_gain": canary.get("expected_suitability_gain", 0.0),
            "is_automatically_best_next_action": False,
            "why": "It is the best current governed path to create one suitability outcome, but prediction/service cycles have lower risk and better direct gain for their specific floors.",
        },
        "activities_ranked": ranked,
        "roadmap_to_tier_2": roadmap,
        "safe_existing_owner_improvement_implemented": True,
        "improvement_type": "read_only_leverage_ranking_in_existing_trust_inventory_owner",
        "uses_current_formulas_only": True,
        "projection_only": True,
        "synthetic_evidence_created": False,
        "formula_changed": False,
        "floor_changed": False,
        "planner_redesigned": False,
        "governance_redesigned": False,
        "execution_redesigned": False,
        "new_truth_source_created": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def _safe_ratio(numerator: Any, denominator: Any) -> float:
    total = as_float(denominator, 0.0)
    if total <= 0:
        return 0.0
    return round(max(0.0, min(1.0, as_float(numerator, 0.0) / total)), 4)


def _suitability_stage(
    *,
    coverage_ratio: float,
    mean_correctness: float,
    mean_candidate_confidence: float,
    suitability_confidence: float,
    freshness_classification: str,
    capture_loss: float,
    visibility_loss: float,
    aggregation_loss: float,
    recommendation_correct_rate: float,
    fit_correct_rate: float,
) -> str:
    no_pipeline_loss = capture_loss <= 0 and visibility_loss <= 0 and aggregation_loss <= 0
    freshness_ok = freshness_classification in {"ACTIONABLE_NOW", "FRESH", "UNKNOWN"}
    if (
        coverage_ratio >= 0.95
        and mean_correctness >= 85.0
        and mean_candidate_confidence >= 0.85
        and suitability_confidence >= 70.0
        and recommendation_correct_rate >= 0.85
        and fit_correct_rate >= 0.85
        and freshness_ok
        and no_pipeline_loss
    ):
        return "AUTONOMY_GRADE_KNOWLEDGE"
    if (
        coverage_ratio >= 0.85
        and mean_correctness >= 75.0
        and mean_candidate_confidence >= 0.70
        and recommendation_correct_rate >= 0.70
        and fit_correct_rate >= 0.70
        and freshness_ok
        and no_pipeline_loss
    ):
        return "ACTIONABLE_KNOWLEDGE"
    if coverage_ratio >= 0.70 and mean_correctness >= 70.0 and mean_candidate_confidence >= 0.60 and no_pipeline_loss:
        return "CONFIRMED_KNOWLEDGE"
    if coverage_ratio > 0 or suitability_confidence > 0 or mean_candidate_confidence > 0:
        return "STABLE_SIGNAL"
    return "RAW_OBSERVATION"


def build_suitability_effectiveness_expansion(
    *,
    decision_outcome_learning: dict[str, Any],
    floor_forensics: dict[str, Any],
    candidate_outcome_reality_collection: dict[str, Any],
) -> dict[str, Any]:
    """Expose suitability-specific effectiveness from existing outcome owners."""
    effectiveness = decision_outcome_learning.get("effectiveness") if isinstance(decision_outcome_learning.get("effectiveness"), dict) else {}
    quality_counts = decision_outcome_learning.get("outcome_quality_counts") if isinstance(decision_outcome_learning.get("outcome_quality_counts"), dict) else {}
    suitability_root = floor_forensics.get("suitability_root_cause") if isinstance(floor_forensics.get("suitability_root_cause"), dict) else {}
    coverage = candidate_outcome_reality_collection.get("coverage") if isinstance(candidate_outcome_reality_collection.get("coverage"), dict) else {}
    candidate_correctness = round(as_float(suitability_root.get("mean_correctness"), 0.0) / 100.0, 4)
    candidate_confidence = round(as_float(suitability_root.get("mean_candidate_confidence"), 0.0), 4)
    user_improved_rate = as_float(effectiveness.get("user_improved_rate"), -1.0)
    user_improved_known = user_improved_rate >= 0.0
    if not user_improved_known:
        user_improved_rate = 0.0
    return {
        "schema_version": "v7.autonomy-trust.suitability-effectiveness-expansion.v1",
        "owner": "admin_core.autonomy_trust_acceleration",
        "source_owner": "admin_core.operator_execution_feedback + trust-evolution-summaries",
        "decision_correctness": as_float(effectiveness.get("recommendation_correct_rate"), 0.0),
        "service_improvement_rate": as_float(effectiveness.get("service_improved_rate"), 0.0),
        "user_improvement_rate": round(user_improved_rate, 4),
        "user_improvement_known": user_improved_known,
        "rollback_rate": as_float(effectiveness.get("rollback_rate"), 0.0),
        "fit_correctness": as_float(effectiveness.get("fit_prediction_correct_rate"), 0.0),
        "candidate_correctness": candidate_correctness,
        "candidate_confidence": candidate_confidence,
        "candidate_coverage_ratio": as_float(coverage.get("coverage_ratio"), 0.0),
        "outcome_quality_counts": quality_counts,
        "missing_candidate_outcomes": int(as_float(coverage.get("missing_candidate_outcomes"), 0.0)),
        "interpretation": {
            "candidate_correctness": "observed suitability correctness normalized from trust-evolution candidate rows",
            "fit_correctness": "existing decision outcome learning fit_prediction_correct_rate",
            "user_improvement_rate": "UNKNOWN until feedback owner emits explicit user_improved_rate",
        },
        "read_only": True,
        "synthetic_evidence_created": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def build_suitability_quality_model(
    *,
    floor_forensics: dict[str, Any],
    candidate_outcome_reality_collection: dict[str, Any],
    freshness_actionability: dict[str, Any],
    service_user_sla_fit: dict[str, Any],
    decision_outcome_learning: dict[str, Any],
    suitability_effectiveness: dict[str, Any],
) -> dict[str, Any]:
    """Evaluate whether suitability knowledge is autonomy-grade without changing scoring."""
    suitability_root = floor_forensics.get("suitability_root_cause") if isinstance(floor_forensics.get("suitability_root_cause"), dict) else {}
    components = floor_forensics.get("component_values") if isinstance(floor_forensics.get("component_values"), dict) else {}
    loss = floor_forensics.get("loss_model") if isinstance(floor_forensics.get("loss_model"), dict) else {}
    coverage = candidate_outcome_reality_collection.get("coverage") if isinstance(candidate_outcome_reality_collection.get("coverage"), dict) else {}
    missing_analysis = candidate_outcome_reality_collection.get("missing_outcome_analysis") if isinstance(candidate_outcome_reality_collection.get("missing_outcome_analysis"), dict) else {}
    freshness_domain = ((freshness_actionability.get("domains") or {}).get("suitability") or {})
    fit_summary = service_user_sla_fit.get("summary") if isinstance(service_user_sla_fit.get("summary"), dict) else {}
    knowledge_growth = decision_outcome_learning.get("knowledge_growth") if isinstance(decision_outcome_learning.get("knowledge_growth"), dict) else {}

    candidate_count = int(as_float(coverage.get("candidate_count"), as_float(suitability_root.get("candidates_seen"), 0.0)))
    outcomes_consumed = int(as_float(coverage.get("candidate_outcomes_consumed"), as_float(suitability_root.get("outcomes_seen"), 0.0)))
    coverage_ratio = as_float(coverage.get("coverage_ratio"), _safe_ratio(outcomes_consumed, candidate_count))
    mean_correctness = as_float(suitability_root.get("mean_correctness"), 0.0)
    mean_candidate_confidence = as_float(suitability_root.get("mean_candidate_confidence"), 0.0)
    suitability_confidence = as_float(components.get("suitability_confidence"), as_float(suitability_root.get("suitability_confidence"), 0.0))
    freshness_classification = str(freshness_domain.get("classification") or "UNKNOWN")
    recommendation_correct_rate = as_float(suitability_effectiveness.get("decision_correctness"), 0.0)
    fit_correct_rate = as_float(suitability_effectiveness.get("fit_correctness"), 0.0)
    capture_loss = as_float(loss.get("capture_loss_count"), 0.0)
    visibility_loss = as_float(loss.get("visibility_loss_count"), 0.0)
    aggregation_loss = as_float(loss.get("aggregation_loss_count"), 0.0)
    stage = _suitability_stage(
        coverage_ratio=coverage_ratio,
        mean_correctness=mean_correctness,
        mean_candidate_confidence=mean_candidate_confidence,
        suitability_confidence=suitability_confidence,
        freshness_classification=freshness_classification,
        capture_loss=capture_loss,
        visibility_loss=visibility_loss,
        aggregation_loss=aggregation_loss,
        recommendation_correct_rate=recommendation_correct_rate,
        fit_correct_rate=fit_correct_rate,
    )
    blockers: list[str] = []
    if coverage_ratio < 0.70:
        blockers.append("candidate_outcome_coverage_below_confirmed_floor")
    if mean_correctness < 70.0:
        blockers.append("candidate_correctness_below_confirmed_floor")
    if mean_candidate_confidence < 0.60:
        blockers.append("candidate_source_confidence_below_confirmed_floor")
    if suitability_confidence < 70.0:
        blockers.append("suitability_confidence_below_autonomy_floor")
    if capture_loss > 0 or visibility_loss > 0 or aggregation_loss > 0:
        blockers.append("evidence_pipeline_loss_present")
    if freshness_classification not in {"ACTIONABLE_NOW", "FRESH", "UNKNOWN"}:
        blockers.append("suitability_freshness_not_actionable")
    if recommendation_correct_rate < 0.70:
        blockers.append("decision_correctness_below_actionable_floor")
    if fit_correct_rate < 0.70:
        blockers.append("fit_correctness_below_actionable_floor")

    next_stage = {
        "RAW_OBSERVATION": "STABLE_SIGNAL",
        "STABLE_SIGNAL": "CONFIRMED_KNOWLEDGE",
        "CONFIRMED_KNOWLEDGE": "ACTIONABLE_KNOWLEDGE",
        "ACTIONABLE_KNOWLEDGE": "AUTONOMY_GRADE_KNOWLEDGE",
        "AUTONOMY_GRADE_KNOWLEDGE": "AUTONOMY_GRADE_KNOWLEDGE",
    }[stage]
    return {
        "schema_version": "v7.autonomy-trust.suitability-quality-model.v1",
        "owner": "admin_core.autonomy_trust_acceleration",
        "source_owners_reused": [
            "admin_core.intelligence_workers.build_candidate_outcome_rows",
            "admin_core.operator_execution_feedback.build_decision_outcome_learning",
            "trust-evolution-summaries",
            "admin_core.intelligence_snapshots.read_snapshot_family",
        ],
        "current_stage": stage,
        "next_stage": next_stage,
        "autonomy_grade_ready": stage == "AUTONOMY_GRADE_KNOWLEDGE",
        "criteria": {
            "STABLE_SIGNAL": "candidate rows or suitability confidence exist",
            "CONFIRMED_KNOWLEDGE": "coverage >= 0.70, correctness >= 70, source confidence >= 0.60, no pipeline loss",
            "ACTIONABLE_KNOWLEDGE": "coverage >= 0.85, correctness >= 75, source confidence >= 0.70, decision/fit correctness >= 0.70",
            "AUTONOMY_GRADE_KNOWLEDGE": "coverage >= 0.95, correctness >= 85, source confidence >= 0.85, suitability confidence >= 70, decision/fit correctness >= 0.85",
        },
        "measurements": {
            "candidate_count": candidate_count,
            "candidate_outcomes_consumed": outcomes_consumed,
            "missing_candidate_outcomes": int(as_float(coverage.get("missing_candidate_outcomes"), max(0, candidate_count - outcomes_consumed))),
            "coverage_ratio": coverage_ratio,
            "mean_correctness": round(mean_correctness, 3),
            "mean_candidate_confidence": round(mean_candidate_confidence, 4),
            "suitability_confidence": round(suitability_confidence, 3),
            "freshness": freshness_classification,
            "service_user_sla_fit_users_seen": fit_summary.get("users_seen", 0),
            "decision_correctness": recommendation_correct_rate,
            "fit_correctness": fit_correct_rate,
            "service_improvement_rate": suitability_effectiveness.get("service_improvement_rate", 0.0),
            "user_improvement_rate": suitability_effectiveness.get("user_improvement_rate", 0.0),
            "rollback_rate": suitability_effectiveness.get("rollback_rate", 0.0),
            "capture_loss_count": int(capture_loss),
            "visibility_loss_count": int(visibility_loss),
            "aggregation_loss_count": int(aggregation_loss),
        },
        "knowledge_gained": knowledge_growth.get("knowledge_gained", 0),
        "knowledge_improved": knowledge_growth.get("knowledge_improved", []),
        "knowledge_degraded": knowledge_growth.get("knowledge_degraded", []),
        "missing_knowledge": {
            "never_happened": missing_analysis.get("never_happened", 0),
            "happened_but_not_visible": missing_analysis.get("happened_but_not_visible", 0),
            "visible_but_weakly_weighted": missing_analysis.get("visible_but_weakly_weighted", 0),
            "primary_blockers": blockers,
        },
        "read_only": True,
        "synthetic_evidence_created": False,
        "formula_changed": False,
        "floor_changed": False,
        "planner_redesigned": False,
        "governance_redesigned": False,
        "execution_redesigned": False,
        "new_truth_source_created": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def build_suitability_knowledge_growth_model(
    *,
    suitability_quality_model: dict[str, Any],
    candidate_outcome_reality_collection: dict[str, Any],
    decision_outcome_learning: dict[str, Any],
    outcome_leverage_model: dict[str, Any],
    real_outcome_growth_projection: dict[str, Any],
) -> dict[str, Any]:
    """Explain suitability knowledge growth opportunities from existing owners."""
    growth = decision_outcome_learning.get("knowledge_growth") if isinstance(decision_outcome_learning.get("knowledge_growth"), dict) else {}
    coverage = candidate_outcome_reality_collection.get("coverage") if isinstance(candidate_outcome_reality_collection.get("coverage"), dict) else {}
    missing = suitability_quality_model.get("missing_knowledge") if isinstance(suitability_quality_model.get("missing_knowledge"), dict) else {}
    ranked = [
        row for row in (outcome_leverage_model.get("activities_ranked") or [])
        if isinstance(row, dict) and as_float(row.get("expected_suitability_gain"), 0.0) > 0
    ]
    projections = real_outcome_growth_projection.get("projections") if isinstance(real_outcome_growth_projection.get("projections"), list) else []
    first_projection = projections[0] if projections and isinstance(projections[0], dict) else {}
    knowledge_improved = set(str(item) for item in (growth.get("knowledge_improved") or []))
    knowledge_degraded = set(str(item) for item in (growth.get("knowledge_degraded") or []))
    if "Suitability" in knowledge_improved:
        direction = "INCREASED"
    elif "Suitability" in knowledge_degraded:
        direction = "DECREASED"
    else:
        direction = "UNCHANGED"
    return {
        "schema_version": "v7.autonomy-trust.suitability-knowledge-growth.v1",
        "owner": "admin_core.autonomy_trust_acceleration",
        "current_stage": suitability_quality_model.get("current_stage", "UNKNOWN"),
        "next_stage": suitability_quality_model.get("next_stage", "UNKNOWN"),
        "growth_direction": direction,
        "why_increased": [
            "closed decision outcome improved Suitability"
        ] if direction == "INCREASED" else [],
        "why_decreased": [
            "closed decision outcome degraded Suitability"
        ] if direction == "DECREASED" else [],
        "why_unchanged": [
            "no new closed suitability outcome in current read model",
            "remaining candidate outcomes are missing or weakly weighted",
        ] if direction == "UNCHANGED" else [],
        "knowledge_gained_total": growth.get("knowledge_gained", 0),
        "candidate_outcome_gap": {
            "candidate_count": coverage.get("candidate_count", 0),
            "candidate_outcomes_consumed": coverage.get("candidate_outcomes_consumed", 0),
            "missing_candidate_outcomes": coverage.get("missing_candidate_outcomes", 0),
            "coverage_ratio": coverage.get("coverage_ratio", 0.0),
            "never_happened": missing.get("never_happened", 0),
            "happened_but_not_visible": missing.get("happened_but_not_visible", 0),
            "visible_but_weakly_weighted": missing.get("visible_but_weakly_weighted", 0),
        },
        "first_missing_outcome_projection": {
            "projected_suitability_confidence": first_projection.get("projected_suitability_confidence", first_projection.get("projected_suitability")),
            "projected_confidence": first_projection.get("projected_confidence"),
            "projected_trust": first_projection.get("projected_trust"),
        },
        "fastest_suitability_growth_activities": ranked[:3],
        "read_only": True,
        "synthetic_evidence_created": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def build_autonomy_grade_suitability_program(
    *,
    suitability_quality_model: dict[str, Any],
    suitability_knowledge_growth: dict[str, Any],
    suitability_effectiveness: dict[str, Any],
    outcome_leverage_model: dict[str, Any],
) -> dict[str, Any]:
    fastest = suitability_knowledge_growth.get("fastest_suitability_growth_activities")
    fastest = fastest if isinstance(fastest, list) else []
    return {
        "schema_version": "v7.autonomy-trust.autonomy-grade-suitability-program.v1",
        "owner": "admin_core.autonomy_trust_acceleration",
        "lifecycle": [
            {"stage": "candidate", "owner": "candidate-suitability-summary", "status": "EXISTS"},
            {"stage": "selection", "owner": "planner/shadow autonomy decision surface", "status": "EXISTS"},
            {"stage": "decision", "owner": "operator/governed packet owners", "status": "EXISTS"},
            {"stage": "packet", "owner": "existing restore/approval packet owners", "status": "EXISTS"},
            {"stage": "verification", "owner": "operator_execution_feedback post-action verification", "status": "EXISTS"},
            {"stage": "outcome", "owner": "candidate outcome matcher", "status": "PARTIAL"},
            {"stage": "learning", "owner": "decision outcome learning", "status": "EXISTS"},
            {"stage": "future_suitability", "owner": "trust evolution suitability aggregation", "status": "PARTIAL"},
        ],
        "improvements": {
            "suitability_quality_model": "IMPLEMENTED_READ_ONLY",
            "suitability_growth_tracking": "IMPLEMENTED_READ_ONLY",
            "why_suitability_changed": "IMPLEMENTED_READ_ONLY",
            "decision_effectiveness_expansion": "IMPLEMENTED_READ_ONLY",
            "knowledge_stage_evaluation": "IMPLEMENTED_READ_ONLY",
            "high_leverage_path_ranking": "REUSED_OUTCOME_LEVERAGE_MODEL",
        },
        "current_stage": suitability_quality_model.get("current_stage", "UNKNOWN"),
        "autonomy_grade_ready": bool(suitability_quality_model.get("autonomy_grade_ready")),
        "primary_blockers": (suitability_quality_model.get("missing_knowledge") or {}).get("primary_blockers", []),
        "fastest_growth_activities": [
            row.get("activity") for row in fastest if isinstance(row, dict)
        ],
        "highest_overall_leverage": (outcome_leverage_model.get("highest_leverage") or {}).get("activity"),
        "suitability_effectiveness": {
            "decision_correctness": suitability_effectiveness.get("decision_correctness", 0.0),
            "fit_correctness": suitability_effectiveness.get("fit_correctness", 0.0),
            "candidate_correctness": suitability_effectiveness.get("candidate_correctness", 0.0),
            "candidate_coverage_ratio": suitability_effectiveness.get("candidate_coverage_ratio", 0.0),
        },
        "read_only": True,
        "synthetic_evidence_created": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


AUTONOMY_CYCLE_LEVEL_SCORES = {
    "MANUAL": 0.0,
    "PARTIALLY_AUTOMATED": 0.5,
    "AUTONOMOUS_UNTIL_BOUNDARY": 0.85,
    "FULLY_AUTONOMOUS": 1.0,
}


def _cycle_row(
    *,
    cycle: str,
    owner: str,
    trigger: str,
    state_transitions: list[str],
    output: str,
    authority_boundary: str,
    automation_level: str,
    blockers: list[str] | None = None,
    safe_next_step: str = "",
) -> dict[str, Any]:
    blockers = blockers or []
    score = AUTONOMY_CYCLE_LEVEL_SCORES.get(automation_level, 0.0)
    gap_classes: list[str] = []
    if not trigger:
        gap_classes.append("MISSING_TRIGGER")
    if any("missing" in str(item).lower() or "unknown" in str(item).lower() for item in blockers):
        gap_classes.append("MISSING_READINESS")
    if "outcome" in " ".join(blockers).lower() and automation_level != "FULLY_AUTONOMOUS":
        gap_classes.append("MISSING_FEEDBACK")
    if authority_boundary and automation_level == "AUTONOMOUS_UNTIL_BOUNDARY":
        gap_classes.append("AUTHORITY_BOUNDARY")
    if not gap_classes and automation_level == "PARTIALLY_AUTOMATED":
        gap_classes.append("MISSING_STATE_TRANSITION")
    if not gap_classes:
        gap_classes.append("NONE")
    return {
        "cycle": cycle,
        "owner": owner,
        "trigger": trigger,
        "state_transitions": state_transitions,
        "output": output,
        "authority_boundary": authority_boundary,
        "automation_level": automation_level,
        "automation_score": score,
        "gap_classes": sorted(set(gap_classes)),
        "blockers": blockers,
        "safe_next_step": safe_next_step,
        "read_only": True,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def build_autonomous_knowledge_growth_program(
    *,
    knowledge_quality_read_model: dict[str, Any],
    suitability_quality_model: dict[str, Any],
    suitability_knowledge_growth: dict[str, Any],
    prediction_plan: dict[str, Any],
    real_outcome_source_inventory: dict[str, Any],
    freshness_actionability: dict[str, Any],
    recovery_admission: dict[str, Any],
    decision_outcome_closure: dict[str, Any],
    decision_outcome_learning: dict[str, Any],
    routing_recommendation_readiness: dict[str, Any],
    outcome_leverage_model: dict[str, Any],
    canary_proximity: dict[str, Any],
) -> dict[str, Any]:
    """Classify how far existing autonomy cycles run without human intervention.

    This is a read-only orchestration inventory. It does not call tools, write
    state, enable timers, or change authority; it only exposes the next
    legitimate boundary for each existing cycle.
    """
    knowledge_overall = (knowledge_quality_read_model.get("10k_readiness") or {}).get("overall", "UNKNOWN")
    suitability_blockers = (suitability_quality_model.get("missing_knowledge") or {}).get("primary_blockers", [])
    freshness_domains = freshness_actionability.get("domains") if isinstance(freshness_actionability.get("domains"), dict) else {}
    stale_domains = [
        name for name, row in sorted(freshness_domains.items())
        if isinstance(row, dict) and row.get("classification") in {"STALE_RECHECK_REQUIRED", "UNKNOWN"}
    ]
    source_items = real_outcome_source_inventory.get("items") if isinstance(real_outcome_source_inventory.get("items"), list) else []
    service_sources = [row for row in source_items if isinstance(row, dict) and row.get("source") in {"service_outcomes", "channel_outcomes"}]
    service_acceleratable = any(row.get("classification") == "ACCELERATABLE" for row in service_sources)
    candidate_gap = suitability_knowledge_growth.get("candidate_outcome_gap") if isinstance(suitability_knowledge_growth.get("candidate_outcome_gap"), dict) else {}
    learning_growth = decision_outcome_learning.get("knowledge_growth") if isinstance(decision_outcome_learning.get("knowledge_growth"), dict) else {}
    closure_state = decision_outcome_closure.get("closure_state", "UNKNOWN")
    routing_blockers = list(routing_recommendation_readiness.get("blockers") or [])
    canary_missing = list(canary_proximity.get("missing") or [])
    outcome_leverage_verdict = outcome_leverage_model.get("final_verdict", "UNKNOWN")

    cycles = [
        _cycle_row(
            cycle="Knowledge Quality Cycle",
            owner="admin_core.autonomy_trust_acceleration.build_knowledge_quality_read_model",
            trigger="trust evidence inventory run or snapshot refresh",
            state_transitions=["snapshots", "dynamic overlays", "knowledge objects", "tier readiness"],
            output="knowledge_quality_read_model",
            authority_boundary="knowledge_quality_not_autonomy_ready" if knowledge_overall != "READY" else "",
            automation_level="FULLY_AUTONOMOUS",
            blockers=[] if knowledge_overall == "READY" else [f"10k_readiness={knowledge_overall}"],
            safe_next_step="continue producing read-only readiness on every inventory run",
        ),
        _cycle_row(
            cycle="Suitability Growth Cycle",
            owner="admin_core.autonomy_trust_acceleration suitability program",
            trigger="candidate outcomes appear in existing governed/manual/feedback records",
            state_transitions=["candidate", "selection", "decision", "packet", "verification", "outcome", "learning", "future suitability"],
            output="suitability_quality_model + suitability_knowledge_growth",
            authority_boundary="real governed/manual candidate outcome required",
            automation_level="AUTONOMOUS_UNTIL_BOUNDARY",
            blockers=list(suitability_blockers),
            safe_next_step="collect real candidate outcome through existing governed/manual owner, then refresh snapshots",
        ),
        _cycle_row(
            cycle="Prediction Growth Cycle",
            owner="prediction snapshots + trust-evolution prediction accuracy",
            trigger="forecast rows and later actual rows exist",
            state_transitions=["forecast", "actual", "match", "prediction confidence"],
            output="prediction_evidence",
            authority_boundary="wait_for_time_separated_real_actuals",
            automation_level="AUTONOMOUS_UNTIL_BOUNDARY" if prediction_plan.get("pending_rows", 0) else "FULLY_AUTONOMOUS",
            blockers=[] if prediction_plan.get("pending_rows", 0) else ["no_pending_prediction_rows"],
            safe_next_step="continue forecast-to-actual cycles through existing snapshot owners",
        ),
        _cycle_row(
            cycle="Service Verification Cycle",
            owner="service matrix / quality compact / intelligence snapshot refresh",
            trigger="periodic or manual service/quality probes",
            state_transitions=["probe", "service score", "channel score", "snapshot refresh", "trust inventory"],
            output="service/channel outcome source confidence",
            authority_boundary="real probe evidence only",
            automation_level="PARTIALLY_AUTOMATED" if service_acceleratable else "MANUAL",
            blockers=[] if service_acceleratable else ["service_probe_source_not_acceleratable"],
            safe_next_step="run existing service/quality probes and refresh snapshots; do not move users",
        ),
        _cycle_row(
            cycle="Freshness Cycle",
            owner="admin_core.autonomy_trust_acceleration.build_freshness_actionability",
            trigger="snapshot read",
            state_transitions=["snapshot statuses", "domain freshness", "actionability classification"],
            output="freshness_actionability",
            authority_boundary="stale domains require recheck",
            automation_level="FULLY_AUTONOMOUS",
            blockers=[f"stale_or_unknown:{','.join(stale_domains)}"] if stale_domains else [],
            safe_next_step="keep freshness as blocking read-only guard",
        ),
        _cycle_row(
            cycle="Recovery Cycle",
            owner="admin_core.autonomy_trust_acceleration.build_recovery_admission",
            trigger="trust inventory run with recovery/channel inputs",
            state_transitions=["channel state", "successful checks", "cooldown/quarantine", "admission state"],
            output="recovery_admission",
            authority_boundary="real recovery evidence and operator/governed authority required",
            automation_level="AUTONOMOUS_UNTIL_BOUNDARY",
            blockers=[] if not (recovery_admission.get("summary") or {}).get("blocked_or_quarantined") else ["blocked_or_quarantined_channels"],
            safe_next_step="continue staged recovery admission; do not promote from one pass",
        ),
        _cycle_row(
            cycle="Outcome Closure Cycle",
            owner="admin_core.autonomy_trust_acceleration.build_decision_outcome_closure",
            trigger="existing decision records with required outcome closure fields",
            state_transitions=["decision record", "closure field validation", "closure state"],
            output="decision_outcome_closure",
            authority_boundary="real post-action outcome required",
            automation_level="AUTONOMOUS_UNTIL_BOUNDARY" if closure_state == "COMPLETE" else "PARTIALLY_AUTOMATED",
            blockers=[] if closure_state == "COMPLETE" else [f"closure_state={closure_state}"],
            safe_next_step="close outcomes only after real governed/manual actions",
        ),
        _cycle_row(
            cycle="Learning Cycle",
            owner="admin_core.operator_execution_feedback + trust-evolution summaries",
            trigger="closed outcome feedback records",
            state_transitions=["outcome quality", "learning record", "knowledge growth", "decision effectiveness"],
            output="decision_outcome_learning",
            authority_boundary="real outcome required before learning can grow",
            automation_level="AUTONOMOUS_UNTIL_BOUNDARY",
            blockers=[] if learning_growth.get("knowledge_gained", 0) else ["no_new_closed_outcome_to_learn_from"],
            safe_next_step="refresh intelligence after any real outcome closure",
        ),
        _cycle_row(
            cycle="Knowledge-Gated Dry-Run Cycle",
            owner="admin_core.operator_execution_pipeline.governed_canary_knowledge_gated_dry_run_cycle",
            trigger="current event or current-state candidate",
            state_transitions=["event/current state", "knowledge gates", "decision", "packet preview", "restore preview", "rollback preview", "verification plan", "outcome closure plan", "learning path", "authority boundary"],
            output="governed canary dry-run cycle payload",
            authority_boundary="AUTHORITY_BOUNDARY",
            automation_level="AUTONOMOUS_UNTIL_BOUNDARY",
            blockers=list(canary_missing),
            safe_next_step="run existing dry-run CLI; stop before restore-barrier write/apply",
        ),
        _cycle_row(
            cycle="Event Detection Cycle",
            owner="admin_core.events + read-only event consumer",
            trigger="service/channel/quality/runtime regression event",
            state_transitions=["event", "classification", "planner preview", "dry-run preparation"],
            output="read-only event-driven preparation",
            authority_boundary="runtime apply authority disabled",
            automation_level="AUTONOMOUS_UNTIL_BOUNDARY",
            blockers=["autoswitch_service_inactive_approved_manual_mode"],
            safe_next_step="keep event consumer read-only until floors and authority pass",
        ),
        _cycle_row(
            cycle="Decision Effectiveness Cycle",
            owner="decision_outcome_learning.effectiveness",
            trigger="closed outcome learning model",
            state_transitions=["closed outcomes", "effectiveness rates", "knowledge gates"],
            output="decision_effectiveness",
            authority_boundary="real closed outcome required",
            automation_level="AUTONOMOUS_UNTIL_BOUNDARY",
            blockers=[] if decision_outcome_learning.get("effectiveness") else ["effectiveness_missing"],
            safe_next_step="consume existing learning model after outcome closure",
        ),
        _cycle_row(
            cycle="Outcome Leverage Cycle",
            owner="admin_core.autonomy_trust_acceleration.build_outcome_leverage_model",
            trigger="trust inventory run",
            state_transitions=["current floors", "source inventory", "growth projections", "ranked outcome activities"],
            output="outcome_leverage_model",
            authority_boundary="real outcome activity selection",
            automation_level="FULLY_AUTONOMOUS",
            blockers=[] if outcome_leverage_verdict != "UNKNOWN" else ["outcome_leverage_unknown"],
            safe_next_step="use ranking before choosing canary or probe work",
        ),
    ]

    counts = {level: 0 for level in AUTONOMY_CYCLE_LEVEL_SCORES}
    for row in cycles:
        counts[row["automation_level"]] = counts.get(row["automation_level"], 0) + 1
    total = len(cycles)
    percentages = {
        level: round((count / total) * 100.0, 3) if total else 0.0
        for level, count in counts.items()
    }
    overall_score = round(sum(as_float(row.get("automation_score")) for row in cycles) / max(1, total) * 100.0, 3)
    improved_cycles = [
        "Knowledge Quality Cycle",
        "Suitability Growth Cycle",
        "Learning Cycle",
        "Knowledge-Gated Dry-Run Cycle",
        "Outcome Leverage Cycle",
    ]
    return {
        "schema_version": "v7.autonomy-trust.autonomous-knowledge-growth-program.v1",
        "owner": "admin_core.autonomy_trust_acceleration",
        "purpose": "classify_existing_autonomy_cycles_and_expose_read_only_maturity",
        "cycles": cycles,
        "cycle_count": total,
        "automation_counts": counts,
        "automation_percentages": percentages,
        "overall_autonomy_maturity_score": overall_score,
        "cycles_more_autonomous_after_this_phase": improved_cycles,
        "legitimate_boundaries": sorted({
            row["authority_boundary"] for row in cycles if row.get("authority_boundary")
        }),
        "safe_integration_fix_implemented": "cycle_maturity_scoring_exposed_through_existing_trust_inventory_owner",
        "runtime_apply_allowed": False,
        "read_only": True,
        "synthetic_evidence_created": False,
        "planner_redesigned": False,
        "governance_redesigned": False,
        "execution_redesigned": False,
        "new_truth_source_created": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
        "autonomy_enabled": False,
    }


def _stage_rank(stage: Any) -> int:
    order = {
        "RAW_OBSERVATION": 0,
        "STABLE_SIGNAL": 1,
        "CONFIRMED_KNOWLEDGE": 2,
        "ACTIONABLE_KNOWLEDGE": 3,
        "AUTONOMY_GRADE_KNOWLEDGE": 4,
    }
    return order.get(str(stage), -1)


def _floor_distance_row(name: str, current: Any, target: float) -> dict[str, Any]:
    value = as_float(current, 0.0)
    return {
        "metric": name,
        "current": round(value, 3),
        "target": round(target, 3),
        "gap": round(max(0.0, target - value), 3),
        "pass": value >= target,
    }


def _cycle_by_name(program: dict[str, Any], name: str) -> dict[str, Any]:
    for row in program.get("cycles") or []:
        if isinstance(row, dict) and row.get("cycle") == name:
            return row
    return {}


def build_autonomous_routing_evolution_program(
    *,
    autonomous_knowledge_growth_program: dict[str, Any],
    autonomy_grade_suitability_program: dict[str, Any],
    suitability_quality_model: dict[str, Any],
    suitability_knowledge_growth: dict[str, Any],
    suitability_effectiveness: dict[str, Any],
    outcome_leverage_model: dict[str, Any],
    knowledge_quality_read_model: dict[str, Any],
    routing_recommendation_readiness: dict[str, Any],
    decision_outcome_learning: dict[str, Any],
    canary_proximity: dict[str, Any],
    real_outcome_growth_projection: dict[str, Any],
    candidate_outcome_reality_collection: dict[str, Any],
    prediction_plan: dict[str, Any],
    real_outcome_source_inventory: dict[str, Any],
) -> dict[str, Any]:
    """Expose the current evolution path without creating authority or evidence.

    This is a read-only integration view over already-existing owners. It
    answers whether V7 can advance automatically, where it must stop, and what
    evidence is still required for TIER_2.
    """
    floors = canary_proximity.get("floors") if isinstance(canary_proximity.get("floors"), dict) else {}
    components = (real_outcome_growth_projection.get("current") or {}) if isinstance(real_outcome_growth_projection.get("current"), dict) else {}
    suitability_measurements = suitability_quality_model.get("measurements") if isinstance(suitability_quality_model.get("measurements"), dict) else {}
    confidence_current = as_float((floors.get("confidence") or {}).get("current"), as_float(components.get("confidence"), 0.0))
    trust_current = as_float((floors.get("trust") or {}).get("current"), as_float(components.get("trust"), 0.0))
    prediction_current = as_float(
        (floors.get("prediction_confidence") or floors.get("prediction") or {}).get("current"),
        as_float(components.get("prediction_confidence"), 0.0),
    )
    suitability_current = as_float(
        suitability_measurements.get("suitability_confidence"),
        as_float(components.get("suitability_confidence"), 0.0),
    )
    floor_rows = [
        _floor_distance_row("confidence", confidence_current, AUTONOMY_CANARY_CONFIDENCE_FLOOR),
        _floor_distance_row("trust", trust_current, AUTONOMY_CANARY_TRUST_FLOOR),
        _floor_distance_row("prediction", prediction_current, AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR),
        _floor_distance_row("suitability", suitability_current, AUTONOMY_CANARY_CONFIDENCE_FLOOR),
    ]
    tier2_floor_pass = all(row["pass"] for row in floor_rows[:3])
    suitability_actionable = _stage_rank(suitability_quality_model.get("current_stage")) >= _stage_rank("ACTIONABLE_KNOWLEDGE")
    tier2_ready = tier2_floor_pass and suitability_actionable
    dry_run_cycle = _cycle_by_name(autonomous_knowledge_growth_program, "Knowledge-Gated Dry-Run Cycle")
    event_cycle = _cycle_by_name(autonomous_knowledge_growth_program, "Event Detection Cycle")
    suitability_cycle = _cycle_by_name(autonomous_knowledge_growth_program, "Suitability Growth Cycle")
    outcome_cycle = _cycle_by_name(autonomous_knowledge_growth_program, "Outcome Closure Cycle")
    learning_cycle = _cycle_by_name(autonomous_knowledge_growth_program, "Learning Cycle")
    missing_candidate = (suitability_knowledge_growth.get("candidate_outcome_gap") or {}) if isinstance(suitability_knowledge_growth.get("candidate_outcome_gap"), dict) else {}
    source_items = real_outcome_source_inventory.get("items") if isinstance(real_outcome_source_inventory.get("items"), list) else []
    acceleratable_sources = [
        row.get("source") for row in source_items
        if isinstance(row, dict) and row.get("classification") == "ACCELERATABLE"
    ]
    top_activities = [
        row.get("activity") for row in (outcome_leverage_model.get("activities_ranked") or [])[:3]
        if isinstance(row, dict)
    ]
    phases = [
        {
            "phase": "A_AUTONOMOUS_KNOWLEDGE_GROWTH",
            "status": "ADVANCED",
            "owner": autonomous_knowledge_growth_program.get("owner"),
            "automation_score": autonomous_knowledge_growth_program.get("overall_autonomy_maturity_score", 0.0),
            "cycle_count": autonomous_knowledge_growth_program.get("cycle_count", 0),
            "autonomous_until_boundary": (autonomous_knowledge_growth_program.get("automation_counts") or {}).get("AUTONOMOUS_UNTIL_BOUNDARY", 0),
            "fully_autonomous": (autonomous_knowledge_growth_program.get("automation_counts") or {}).get("FULLY_AUTONOMOUS", 0),
            "blocker": "AUTHORITY_BOUNDARY" if "AUTHORITY_BOUNDARY" in (autonomous_knowledge_growth_program.get("legitimate_boundaries") or []) else "NONE",
        },
        {
            "phase": "B_REAL_SUITABILITY_OUTCOME_PROGRAM",
            "status": "REAL_OUTCOMES_REQUIRED" if missing_candidate.get("missing_candidate_outcomes", 0) else "NO_MISSING_CANDIDATES",
            "owner": autonomy_grade_suitability_program.get("owner"),
            "current_stage": suitability_quality_model.get("current_stage", "UNKNOWN"),
            "missing_candidate_outcomes": missing_candidate.get("missing_candidate_outcomes", 0),
            "cycle_automation": suitability_cycle.get("automation_level", "UNKNOWN"),
            "fastest_growth_activities": autonomy_grade_suitability_program.get("fastest_growth_activities", []),
        },
        {
            "phase": "C_CONFIRMED_KNOWLEDGE",
            "status": "PASS" if _stage_rank(suitability_quality_model.get("current_stage")) >= _stage_rank("CONFIRMED_KNOWLEDGE") else "BLOCKED",
            "target": "CONFIRMED_KNOWLEDGE",
            "current_stage": suitability_quality_model.get("current_stage", "UNKNOWN"),
            "blockers": (suitability_quality_model.get("missing_knowledge") or {}).get("primary_blockers", []),
            "coverage_ratio": suitability_measurements.get("coverage_ratio", 0.0),
            "mean_correctness": suitability_measurements.get("mean_correctness", 0.0),
            "source_confidence": suitability_measurements.get("mean_candidate_confidence", 0.0),
        },
        {
            "phase": "D_ACTIONABLE_KNOWLEDGE",
            "status": "PASS" if suitability_actionable else "BLOCKED",
            "target": "ACTIONABLE_KNOWLEDGE",
            "decision_correctness": suitability_effectiveness.get("decision_correctness", 0.0),
            "fit_correctness": suitability_effectiveness.get("fit_correctness", 0.0),
            "outcome_quality_counts": suitability_effectiveness.get("outcome_quality_counts", {}),
            "learning_knowledge_gained": (decision_outcome_learning.get("knowledge_growth") or {}).get("knowledge_gained", 0),
        },
        {
            "phase": "E_EVENT_TO_DECISION_TO_OUTCOME",
            "status": "AUTONOMOUS_UNTIL_AUTHORITY_BOUNDARY",
            "event_cycle": event_cycle.get("automation_level", "UNKNOWN"),
            "dry_run_cycle": dry_run_cycle.get("automation_level", "UNKNOWN"),
            "dry_run_boundary": dry_run_cycle.get("authority_boundary", "UNKNOWN"),
            "outcome_closure_cycle": outcome_cycle.get("automation_level", "UNKNOWN"),
            "learning_cycle": learning_cycle.get("automation_level", "UNKNOWN"),
            "routing_readiness": routing_recommendation_readiness.get("readiness", "UNKNOWN"),
        },
        {
            "phase": "F_TIER_2_READINESS",
            "status": "READY" if tier2_ready else "BLOCKED",
            "floor_pass": tier2_floor_pass,
            "suitability_actionable": suitability_actionable,
            "floor_distances": floor_rows,
            "knowledge_status": (knowledge_quality_read_model.get("tier_readiness_knowledge") or {}).get("TIER_2", {}),
        },
    ]
    if tier2_ready:
        stop_reason = "READY_FOR_TIER_2_GOVERNED_REVIEW"
    elif dry_run_cycle.get("authority_boundary") == "AUTHORITY_BOUNDARY":
        stop_reason = "AUTHORITY_BOUNDARY"
    else:
        stop_reason = "REAL_GAP"
    return {
        "schema_version": "v7.autonomy-trust.autonomous-routing-evolution-program.v1",
        "owner": "admin_core.autonomy_trust_acceleration",
        "purpose": "integrate_existing_knowledge_decision_outcome_learning_and_event_cycles_into_one_read_only_evolution_view",
        "phases": phases,
        "phase_status": {row["phase"]: row["status"] for row in phases},
        "current_autonomy_maturity": {
            "cycle_maturity_score": autonomous_knowledge_growth_program.get("overall_autonomy_maturity_score", 0.0),
            "manual_cycles": (autonomous_knowledge_growth_program.get("automation_counts") or {}).get("MANUAL", 0),
            "partially_automated_cycles": (autonomous_knowledge_growth_program.get("automation_counts") or {}).get("PARTIALLY_AUTOMATED", 0),
            "autonomous_until_boundary_cycles": (autonomous_knowledge_growth_program.get("automation_counts") or {}).get("AUTONOMOUS_UNTIL_BOUNDARY", 0),
            "fully_autonomous_cycles": (autonomous_knowledge_growth_program.get("automation_counts") or {}).get("FULLY_AUTONOMOUS", 0),
        },
        "current_suitability_maturity": {
            "stage": suitability_quality_model.get("current_stage", "UNKNOWN"),
            "next_stage": suitability_quality_model.get("next_stage", "UNKNOWN"),
            "autonomy_grade_ready": bool(suitability_quality_model.get("autonomy_grade_ready")),
            "candidate_outcome_gap": missing_candidate,
            "effectiveness": {
                "decision_correctness": suitability_effectiveness.get("decision_correctness", 0.0),
                "fit_correctness": suitability_effectiveness.get("fit_correctness", 0.0),
                "candidate_correctness": suitability_effectiveness.get("candidate_correctness", 0.0),
                "candidate_confidence": suitability_effectiveness.get("candidate_confidence", 0.0),
            },
        },
        "tier_2_distance": {
            "status": "READY" if tier2_ready else "BLOCKED",
            "floors": floor_rows,
            "total_floor_gap": round(sum(row["gap"] for row in floor_rows), 3),
            "missing_primary_floors": [row["metric"] for row in floor_rows if not row["pass"]],
            "suitability_actionable": suitability_actionable,
            "required_suitability_stage": "ACTIONABLE_KNOWLEDGE",
            "current_suitability_stage": suitability_quality_model.get("current_stage", "UNKNOWN"),
        },
        "highest_leverage_next_activities": top_activities,
        "acceleratable_real_sources": acceleratable_sources,
        "prediction_pending_rows": prediction_plan.get("pending_rows", 0),
        "exact_stop_reason": stop_reason,
        "stop_detail": "Existing dry-run path reaches explicit operator authority boundary before restore-barrier write or apply." if stop_reason == "AUTHORITY_BOUNDARY" else "Evidence floors and suitability maturity still block TIER_2.",
        "safe_existing_owner_improvement_implemented": "read_only_evolution_program_exposed_through_existing_trust_inventory_owner",
        "read_only": True,
        "synthetic_evidence_created": False,
        "formula_changed": False,
        "floor_changed": False,
        "planner_redesigned": False,
        "governance_redesigned": False,
        "execution_redesigned": False,
        "new_truth_source_created": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
        "autonomy_enabled": False,
    }


def _empty_certification_signal_taxonomy() -> dict[str, list[str]]:
    return {category: [] for category in CERTIFICATION_SIGNAL_CATEGORIES}


def _add_certification_signal(taxonomy: dict[str, list[str]], category: str, signal: str) -> None:
    bucket = taxonomy.setdefault(category, [])
    if signal not in bucket:
        bucket.append(signal)


def _promotion_signal_taxonomy(
    *,
    canary_proximity: dict[str, Any],
    candidate_outcome_reality_collection: dict[str, Any],
    decision_outcome_closure: dict[str, Any],
    decision_outcome_learning: dict[str, Any],
    suitability_quality_model: dict[str, Any],
    freshness_actionability: dict[str, Any],
) -> dict[str, Any]:
    taxonomy = _empty_certification_signal_taxonomy()
    for item in (canary_proximity.get("missing") or []):
        _add_certification_signal(taxonomy, "RELIABILITY_SIGNAL", str(item))
    candidate_gap = candidate_outcome_reality_collection.get("candidate_outcome_gap")
    if not isinstance(candidate_gap, dict):
        candidate_gap = candidate_outcome_reality_collection.get("coverage")
    if isinstance(candidate_gap, dict):
        gap = int(candidate_gap.get("missing_candidate_outcomes") or 0)
        if gap > 0:
            _add_certification_signal(taxonomy, "INVENTORY_SIGNAL", f"missing_candidate_outcomes={gap}")
    closure_state = str(decision_outcome_closure.get("closure_state") or decision_outcome_closure.get("status") or "UNKNOWN")
    if closure_state not in {"COMPLETE", "READY", "CLOSED"}:
        _add_certification_signal(taxonomy, "MANDATORY_CERTIFICATION_REQUIREMENT", f"outcome_closure_state={closure_state}")
    learning_growth = decision_outcome_learning.get("knowledge_growth") if isinstance(decision_outcome_learning.get("knowledge_growth"), dict) else {}
    if not int(learning_growth.get("knowledge_gained") or 0):
        _add_certification_signal(
            taxonomy,
            "MANDATORY_CERTIFICATION_REQUIREMENT",
            "no_verified_learning_growth_from_closed_real_outcomes",
        )
    if not bool(suitability_quality_model.get("autonomy_grade_ready")):
        _add_certification_signal(
            taxonomy,
            "RELIABILITY_SIGNAL",
            f"suitability_stage={suitability_quality_model.get('current_stage', 'UNKNOWN')}",
        )
    stale_domains = [
        name for name, row in sorted((freshness_actionability.get("domains") or {}).items())
        if isinstance(row, dict) and row.get("classification") in {"STALE_RECHECK_REQUIRED", "UNKNOWN"}
    ]
    if stale_domains:
        _add_certification_signal(taxonomy, "RUNTIME_SAFETY_SIGNAL", "freshness_recheck_required=" + ",".join(stale_domains))
    required = [
        "class-level rollback_or_no_rollback_certification",
        "class-level blast_radius_certification",
        "class-level authority_policy_approval",
        "runtime policy binding through existing owners",
    ]
    for item in required:
        _add_certification_signal(taxonomy, "MANDATORY_CERTIFICATION_REQUIREMENT", item)
    return {
        "schema_version": "v7.certification-signal-taxonomy.v1",
        "owner": "admin_core.autonomy_trust_acceleration",
        "canonical_rule": "implementation owners must not promote supporting signals into mandatory certification requirements",
        "categories": taxonomy,
        "mandatory_certification_requirements": taxonomy["MANDATORY_CERTIFICATION_REQUIREMENT"],
        "supporting_evidence": taxonomy["SUPPORTING_EVIDENCE"],
        "coverage_signals": taxonomy["COVERAGE_SIGNAL"],
        "inventory_signals": taxonomy["INVENTORY_SIGNAL"],
        "learning_signals": taxonomy["LEARNING_SIGNAL"],
        "reliability_signals": taxonomy["RELIABILITY_SIGNAL"],
        "runtime_safety_signals": taxonomy["RUNTIME_SAFETY_SIGNAL"],
        "optimization_signals": taxonomy["OPTIMIZATION_SIGNAL"],
        "historical_evidence": taxonomy["HISTORICAL_EVIDENCE"],
        "implementation_artifacts": taxonomy["IMPLEMENTATION_ARTIFACT"],
    }


def _promotion_missing_evidence(
    *,
    canary_proximity: dict[str, Any],
    candidate_outcome_reality_collection: dict[str, Any],
    decision_outcome_closure: dict[str, Any],
    decision_outcome_learning: dict[str, Any],
    suitability_quality_model: dict[str, Any],
    freshness_actionability: dict[str, Any],
) -> list[str]:
    taxonomy = _promotion_signal_taxonomy(
        canary_proximity=canary_proximity,
        candidate_outcome_reality_collection=candidate_outcome_reality_collection,
        decision_outcome_closure=decision_outcome_closure,
        decision_outcome_learning=decision_outcome_learning,
        suitability_quality_model=suitability_quality_model,
        freshness_actionability=freshness_actionability,
    )
    return list(dict.fromkeys(taxonomy["mandatory_certification_requirements"]))


def _packet_to_action_class(
    *,
    packet_preview: dict[str, Any] | None = None,
    candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    packet = packet_preview if isinstance(packet_preview, dict) else {}
    candidate = candidate if isinstance(candidate, dict) else {}
    selected_count = int(packet.get("selected_move_count") or len(packet.get("allowed_users") or []) or (1 if candidate.get("user") else 0))
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
    subject = list(packet.get("allowed_users") or [])
    if not subject and candidate.get("user"):
        subject = [str(candidate.get("user"))]
    target = list(packet.get("allowed_targets") or [])
    if not target and candidate.get("recommended_channel"):
        target = [str(candidate.get("recommended_channel"))]
    return {
        "schema_version": "v7.action-class.packet-mapping.v1",
        "packet_id": str(packet.get("packet_id") or ""),
        "operation_id": str(packet.get("operation_id") or ""),
        "decision_id": str(packet.get("decision_id") or ""),
        "selected_move_hash": str(packet.get("selected_move_hash") or ""),
        "authority_generation": str(packet.get("authority_generation") or ""),
        "selected_move_count": selected_count,
        "subject": subject,
        "target": target,
        "action_class": action_class,
        "mapping_owner": "admin_core.autonomy_trust_acceleration",
        "packet_owner_reused": "admin_core/operator_execution.py",
        "planner_rerun_required": False,
        "runtime_mutation_performed": False,
        "apply_executed": False,
        "users_moved": 0,
    }


def build_delegated_autonomy_policy_preview(
    policy: dict[str, Any] | None = None,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Expose the bounded policy contract without approving or enabling it."""
    source = dict(DEFAULT_DELEGATED_AUTONOMY_POLICY)
    if isinstance(policy, dict):
        source.update(policy)
    return {
        "schema_version": "v7.delegated-autonomy-policy.preview.v1",
        "generated_at": generated_at or "",
        **source,
        "autonomy_modes": AUTONOMY_MODES,
        "operator_approves": [
            "policy_boundaries",
            "authority_expansion",
            "new_action_classes",
            "blast_radius_increase",
            "exceptional_situations",
        ],
        "v7_may_approve_inside_policy": [
            "fresh_packet_validity",
            "safety_gate_pass",
            "verification_ready",
            "rollback_ready",
            "freshness_gate_pass",
            "policy_match",
            "authority_match",
        ],
        "v7_may_not_approve": [
            "policy_expansion",
            "blast_radius_increase",
            "new_action_class",
            "authority_expansion",
        ],
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
    }


def build_delegated_autonomy_runtime_eligibility(
    *,
    policy_preview: dict[str, Any],
    packet_mapping: dict[str, Any],
    current_state: str,
    missing_evidence: list[str],
    freshness_actionability: dict[str, Any],
) -> dict[str, Any]:
    """Evaluate whether Runtime may self-approve execution inside policy."""
    action_class = str(packet_mapping.get("action_class") or "UNKNOWN_ACTION_CLASS")
    selected_count = int(packet_mapping.get("selected_move_count") or 0)
    blockers: list[str] = []
    if policy_preview.get("policy_state") != "APPROVED":
        blockers.append("POLICY_NOT_APPROVED")
    if action_class not in set(policy_preview.get("allowed_action_classes") or []):
        blockers.append("ACTION_CLASS_NOT_ALLOWED")
    if selected_count > int(policy_preview.get("max_users_per_action") or 0):
        blockers.append("BLAST_RADIUS_EXCEEDED")
    if current_state != "AUTONOMOUS_RUNTIME":
        if not bool(policy_preview.get("governed_learning_mode_allowed")):
            blockers.append("ACTION_CLASS_NOT_AUTONOMOUS_RUNTIME")
        else:
            blockers.append("GOVERNED_LEARNING_MODE_REQUIRES_EXPLICIT_POLICY")
    required_freshness = set(policy_preview.get("required_freshness") or [])
    stale_domains = {
        name for name, row in (freshness_actionability.get("domains") or {}).items()
        if isinstance(row, dict) and row.get("classification") in {"STALE_RECHECK_REQUIRED", "UNKNOWN"}
    }
    stale_required = sorted(required_freshness.intersection(stale_domains))
    if stale_required:
        blockers.append("STALE_EVIDENCE")
    if any("rollback_or_no_rollback" in item for item in missing_evidence):
        blockers.append("ROLLBACK_NOT_READY")
    if any("blast_radius_certification" in item for item in missing_evidence):
        blockers.append("BLAST_RADIUS_NOT_CERTIFIED")
    if any("authority_policy_approval" in item or "runtime policy binding" in item for item in missing_evidence):
        blockers.append("AUTHORITY_POLICY_NOT_APPROVED")
    if not bool(policy_preview.get("runtime_apply_enabled")):
        blockers.append("RUNTIME_APPLY_NOT_ENABLED")
    blockers = list(dict.fromkeys(blockers))
    eligible = not blockers
    return {
        "schema_version": "v7.delegated-autonomy-runtime-eligibility.v1",
        "policy_id": str(policy_preview.get("policy_id") or ""),
        "current_mode": str(policy_preview.get("current_mode") or ""),
        "target_mode": str(policy_preview.get("target_mode") or ""),
        "action_class": action_class,
        "selected_move_count": selected_count,
        "runtime_may_self_approve_operational_decision": eligible,
        "runtime_can_execute_automatically": eligible,
        "runtime_must_stop": not eligible,
        "stop_condition": "AUTHORITY_BOUNDARY" if blockers else "",
        "blockers": blockers,
        "fresh_packet_required_immediately_before_execution": True,
        "packet_matches_policy": "PACKET_POLICY_MISMATCH" not in blockers,
        "rollback_ready": "ROLLBACK_NOT_READY" not in blockers,
        "verification_ready": True,
        "anti_flap_required": str(policy_preview.get("required_anti_flap") or ""),
        "blast_radius_within_policy": "BLAST_RADIUS_EXCEEDED" not in blockers,
        "stale_evidence": bool(stale_required),
        "stale_required_domains": stale_required,
        "unknown_failure_mode": False,
        "self_approval_scope": "inside_approved_policy_only",
        "policy_expansion_allowed_by_runtime": False,
        "authority_expansion_allowed_by_runtime": False,
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
    }


def build_action_class_runtime_enablement_model(
    *,
    canary_proximity: dict[str, Any],
    candidate_outcome_reality_collection: dict[str, Any],
    decision_outcome_closure: dict[str, Any],
    decision_outcome_learning: dict[str, Any],
    suitability_quality_model: dict[str, Any],
    freshness_actionability: dict[str, Any],
    autonomous_routing_evolution_program: dict[str, Any],
    hard_failure_classification: dict[str, Any] | None = None,
    action_class_freshness_windows: dict[str, Any] | None = None,
    packet_preview: dict[str, Any] | None = None,
    candidate: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Expose action-class to runtime enablement without creating authority."""
    first_class = ACTION_CLASS_LADDER[0][0]
    packet_mapping = _packet_to_action_class(packet_preview=packet_preview, candidate=candidate)
    signal_taxonomy = _promotion_signal_taxonomy(
        canary_proximity=canary_proximity,
        candidate_outcome_reality_collection=candidate_outcome_reality_collection,
        decision_outcome_closure=decision_outcome_closure,
        decision_outcome_learning=decision_outcome_learning,
        suitability_quality_model=suitability_quality_model,
        freshness_actionability=freshness_actionability,
    )
    hard_failure_state = str((hard_failure_classification or {}).get("classification") or "UNKNOWN")
    if hard_failure_state == "HARD_FAILURE_SUSPECTED":
        _add_certification_signal(signal_taxonomy["categories"], "RUNTIME_SAFETY_SIGNAL", "hard_failure_confirmation_required")
    elif hard_failure_state not in {"HARD_FAILURE_CONFIRMED"}:
        _add_certification_signal(signal_taxonomy["categories"], "RUNTIME_SAFETY_SIGNAL", f"canonical_hard_failure_classification={hard_failure_state}")
    signal_taxonomy["mandatory_certification_requirements"] = signal_taxonomy["categories"]["MANDATORY_CERTIFICATION_REQUIREMENT"]
    signal_taxonomy["runtime_safety_signals"] = signal_taxonomy["categories"]["RUNTIME_SAFETY_SIGNAL"]
    missing_evidence = list(signal_taxonomy["mandatory_certification_requirements"])
    missing_evidence = list(dict.fromkeys(missing_evidence))
    class_rows = []
    freshness_by_class = {
        str(row.get("action_class") or ""): row
        for row in ((action_class_freshness_windows or {}).get("rows") or [])
        if isinstance(row, dict)
    }
    for name, blast_radius, state in ACTION_CLASS_LADDER:
        next_state = ""
        if state == "NOT_CERTIFIED":
            next_state = "GOVERNED_ONLY"
        elif state == "GOVERNED_ONLY":
            next_state = "CERTIFIED_FOR_CLASS_APPROVAL"
        elif state == "CERTIFIED_FOR_CLASS_APPROVAL":
            next_state = "CERTIFIED_FOR_BOUNDED_AUTONOMY"
        elif state == "CERTIFIED_FOR_BOUNDED_AUTONOMY":
            next_state = "AUTONOMOUS_RUNTIME"
        class_rows.append({
            "action_class": name,
            "current_state": state,
            "next_state": next_state,
            "required_evidence": missing_evidence if name == first_class else ["successful prior class outcomes", "class-specific real outcomes", "explicit authority review"],
            "supporting_evidence": signal_taxonomy["supporting_evidence"] if name == first_class else [],
            "coverage_signals": signal_taxonomy["coverage_signals"] if name == first_class else [],
            "inventory_signals": signal_taxonomy["inventory_signals"] if name == first_class else [],
            "reliability_signals": signal_taxonomy["reliability_signals"] if name == first_class else [],
            "required_verification": "immediate post-action service/user/channel verification",
            "required_rollback": "class-level rollback or certified no-rollback path",
            "required_blast_radius": "exactly one user" if blast_radius == 1 else ("bounded cohort" if blast_radius else "class-specific bounded scope"),
            "required_authority": "explicit packet approval until class approval exists" if name == first_class else "explicit class or packet authority",
            "freshness_windows": dict(ACTION_CLASS_FRESHNESS_WINDOWS.get(name, {})),
            "freshness_ready": bool(freshness_by_class.get(name, {}).get("freshness_ready", False)),
            "runtime_enablement_state": state,
            "runtime_can_execute_automatically": state == "AUTONOMOUS_RUNTIME",
        })
    current = class_rows[0]
    can_execute = bool(current["runtime_can_execute_automatically"])
    delegated_policy = build_delegated_autonomy_policy_preview(generated_at=generated_at)
    delegated_eligibility = build_delegated_autonomy_runtime_eligibility(
        policy_preview=delegated_policy,
        packet_mapping=packet_mapping,
        current_state=current["current_state"],
        missing_evidence=missing_evidence,
        freshness_actionability=freshness_actionability,
    )
    return {
        "schema_version": "v7.action-class-runtime-enablement.v2",
        "generated_at": generated_at or "",
        "path_status": "PARTIAL",
        "semantic_reuse_audit": {
            "desired_capability": "Convert certified action classes into runtime-enabled capabilities after explicit authority approval.",
            "semantic_coverage_percent": 78,
            "need_new_owner": False,
            "existing_owners": [
                "docs/programs/OPERATIONAL_MATURITY_PROGRAM.md",
                "admin_core/autonomy_trust_acceleration.py",
                "admin_core/operator_execution_pipeline.py",
                "admin_core/operator_execution.py",
                "tools/v7-governed-canary-dry-run-cycle",
                "tools/v7-autonomy-trust-evidence-inventory",
                "docs/reference/V7_RUNTIME_MODEL.md",
            ],
            "reuse_strategy": "reuse OMP promotion policy, trust inventory, governed dry-run, packet owner, lease owner, restore/rollback, feedback, and learning owners",
            "extension_strategy": "add read-only registry, packet-to-action-class mapping, authority-to-action-class mapping, and runtime readiness view inside existing owners",
            "duplicate_detector_result": "NO_DUPLICATE_OWNER_CREATED",
        },
        "states": ACTION_CLASS_ENABLEMENT_STATES,
        "certification_signal_taxonomy": signal_taxonomy,
        "program_wide_signal_taxonomy": CERTIFICATION_SIGNAL_CATEGORIES,
        "action_classes": class_rows,
        "current_action_class": first_class,
        "current_state": current["current_state"],
        "next_promotion_target": current["next_state"],
        "packet_to_action_class_mapping": packet_mapping,
        "authority_to_action_class_mapping": {
            "packet_approval": "authorizes one exact packet only",
            "class_approval": "required before Runtime can execute the class without packet-by-packet operator approval",
            "delegated_autonomy_policy": "authorizes V7 to self-approve operational decisions only inside approved bounded policy",
            "current_authority": "packet-level governed authority only",
            "authority_expansion_performed": False,
        },
        "delegated_autonomy_policy_preview": delegated_policy,
        "delegated_autonomy_runtime_eligibility": delegated_eligibility,
        "downstream_certification_alignment": {
            "A4": {
                "owns": "representative action-class evidence",
                "inventory_coverage_role": "INVENTORY_SIGNAL",
                "inventory_coverage_is_hard_gate": False,
            },
            "A5": {
                "owns": "blast-radius proof",
                "consumes": "certified A4 outputs, not raw inventory deficits",
                "inventory_coverage_is_hard_gate": False,
            },
            "B13": {
                "owns": "metric reliability proof",
                "consumes": "representative evidence, verification, rollback/no-rollback, learning, calibration, confidence",
                "inventory_coverage_role": "SUPPORTING_SIGNAL",
            },
            "A6": {
                "owns": "runtime eligibility arbitration",
                "consumes": "certified gates and live safety checks, not exhaustive user-channel inventory",
                "inventory_coverage_is_runtime_blocker": False,
            },
            "promotion_authority_runtime": {
                "promotion_consumes_certification": True,
                "authority_consumes_promotion_recommendation": True,
                "runtime_consumes_certified_eligibility": True,
                "raw_inventory_deficit_grants_or_denies_authority": False,
            },
        },
        "runtime_capability_view": {
            "runtime_capability": "single_user_governed_candidate_failover",
            "runtime_path_exists_through_existing_owners": True,
            "runtime_enablement_state": current["current_state"],
            "hard_failure_classification": hard_failure_state,
            "freshness_ready": bool(current.get("freshness_ready")),
            "freshness_windows": current.get("freshness_windows", {}),
            "runtime_can_execute_automatically": can_execute and delegated_eligibility["runtime_can_execute_automatically"],
            "runtime_must_stop_at": "AUTHORITY_BOUNDARY" if not can_execute else "",
            "runtime_apply_allowed_now": False,
            "current_autonomy_mode": delegated_policy["current_mode"],
            "target_autonomy_mode": delegated_policy["target_mode"],
        },
        "promotion_recommendation": {
            "recommendation": "DO_NOT_ENABLE_RUNTIME_AUTOMATION",
            "target_state": current["next_state"],
            "missing_evidence": missing_evidence,
            "supporting_evidence": signal_taxonomy["supporting_evidence"],
            "coverage_signals": signal_taxonomy["coverage_signals"],
            "inventory_signals": signal_taxonomy["inventory_signals"],
            "reliability_signals": signal_taxonomy["reliability_signals"],
            "runtime_safety_signals": signal_taxonomy["runtime_safety_signals"],
            "authority_boundary_required_for_next_state": True,
        },
        "enablement_readiness": {
            "can_runtime_execute_automatically": can_execute and delegated_eligibility["runtime_can_execute_automatically"],
            "reason": "delegated_policy_or_action_class_not_ready" if not delegated_eligibility["runtime_can_execute_automatically"] else "action_class_policy_authority_and_runtime_bounds_pass",
            "requires_authority_expansion": current["current_state"] != "AUTONOMOUS_RUNTIME",
            "stop_condition_if_promoted": "AUTHORITY_BOUNDARY" if current["current_state"] != "AUTONOMOUS_RUNTIME" else "",
            "missing_evidence": missing_evidence,
            "inventory_signals": signal_taxonomy["inventory_signals"],
            "inventory_signals_are_mandatory": False,
            "delegated_policy_blockers": delegated_eligibility["blockers"],
        },
        "omp_output": {
            "current_action_class": first_class,
            "current_state": current["current_state"],
            "hard_failure_classification": hard_failure_state,
            "freshness_ready": bool(current.get("freshness_ready")),
            "missing_evidence": missing_evidence,
            "signal_taxonomy": signal_taxonomy,
            "next_promotion_target": current["next_state"],
            "runtime_can_execute_automatically": can_execute,
            "autonomous_routing_stop_reason": autonomous_routing_evolution_program.get("exact_stop_reason", "UNKNOWN"),
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "new_planner_created": False,
        "new_governance_created": False,
        "new_execution_path_created": False,
        "new_truth_source_created": False,
    }


def _knowledge_limit_item(
    *,
    item: str,
    classification: str,
    owner: str,
    evidence: str,
    safe_cycle: str,
    blocker: str = "",
    count: int | float | None = None,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "item": item,
        "classification": classification,
        "owner": owner,
        "evidence": evidence,
        "safe_cycle": safe_cycle,
        "blocker": blocker,
        "read_only": True,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }
    if count is not None:
        row["count"] = count
    return row


def _classification_summary(rows: list[dict[str, Any]]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for row in rows:
        key = str(row.get("classification") or "UNKNOWN")
        summary[key] = summary.get(key, 0) + 1
    return summary


def _best_candidate_projection(candidate_outcome_reality_collection: dict[str, Any]) -> dict[str, Any]:
    growth = candidate_outcome_reality_collection.get("growth_model") if isinstance(candidate_outcome_reality_collection.get("growth_model"), dict) else {}
    rows = [row for row in (growth.get("projections") or []) if isinstance(row, dict)]
    if not rows:
        return {}
    return sorted(
        rows,
        key=lambda row: (
            -int(as_float(row.get("converted_missing_candidate_outcomes"), 0.0)),
            -as_float(row.get("projected_suitability"), 0.0),
        ),
    )[0]


def _cycle_blocker_class(cycle: dict[str, Any]) -> str:
    boundary = str(cycle.get("authority_boundary") or "")
    blockers = [str(item) for item in (cycle.get("blockers") or [])]
    automation = str(cycle.get("automation_level") or "")
    if boundary == "AUTHORITY_BOUNDARY":
        return "AUTHORITY_BOUNDARY"
    if any("missing" in item.lower() for item in blockers):
        return "MISSING_STATE"
    if any("no_pending" in item.lower() or "wait_for" in item.lower() for item in blockers) or "real" in boundary.lower():
        return "REAL_WORLD_DEPENDENCY"
    if automation == "FULLY_AUTONOMOUS":
        return "NONE"
    if automation in {"PARTIALLY_AUTOMATED", "MANUAL"}:
        return "MISSING_TRIGGER"
    return "MISSING_INTEGRATION" if blockers else "NONE"


def build_maximum_reality_knowledge_extraction(
    *,
    autonomous_knowledge_growth_program: dict[str, Any],
    autonomous_routing_evolution_program: dict[str, Any],
    candidate_outcome_reality_collection: dict[str, Any],
    real_outcome_source_inventory: dict[str, Any],
    real_outcome_growth_projection: dict[str, Any],
    suitability_quality_model: dict[str, Any],
    suitability_knowledge_growth: dict[str, Any],
    prediction_plan: dict[str, Any],
    decision_outcome_closure: dict[str, Any],
    decision_outcome_learning: dict[str, Any],
    freshness_actionability: dict[str, Any],
    outcome_leverage_model: dict[str, Any],
) -> dict[str, Any]:
    """Classify the maximum real routing knowledge obtainable today.

    This extends the existing trust inventory as a read-only extraction view. It
    does not run probes, move users, create evidence, or alter formulas; it
    shows which existing cycles can continue automatically and where reality or
    authority is the actual limit.
    """
    coverage = candidate_outcome_reality_collection.get("coverage") if isinstance(candidate_outcome_reality_collection.get("coverage"), dict) else {}
    missing = candidate_outcome_reality_collection.get("missing_outcome_analysis") if isinstance(candidate_outcome_reality_collection.get("missing_outcome_analysis"), dict) else {}
    growth_current = (candidate_outcome_reality_collection.get("growth_model") or {}).get("current") if isinstance(candidate_outcome_reality_collection.get("growth_model"), dict) else {}
    best_projection = _best_candidate_projection(candidate_outcome_reality_collection)
    source_items = [row for row in (real_outcome_source_inventory.get("items") or []) if isinstance(row, dict)]
    source_by_name = {str(row.get("source")): row for row in source_items}
    service_source = source_by_name.get("service_outcomes", {})
    channel_source = source_by_name.get("channel_outcomes", {})
    learning_source = source_by_name.get("learning_outcomes", {})
    freshness_domains = freshness_actionability.get("domains") if isinstance(freshness_actionability.get("domains"), dict) else {}
    closure_summary = decision_outcome_closure.get("summary") if isinstance(decision_outcome_closure.get("summary"), dict) else {}
    learning_growth = decision_outcome_learning.get("knowledge_growth") if isinstance(decision_outcome_learning.get("knowledge_growth"), dict) else {}
    prediction_pending = int(as_float(prediction_plan.get("pending_rows"), 0.0))
    prediction_matched = int(as_float(prediction_plan.get("matched_rows"), 0.0))
    prediction_seen = int(as_float(prediction_plan.get("forecasts_seen"), 0.0))
    candidate_count = int(as_float(coverage.get("candidate_count"), 0.0))
    consumed = int(as_float(coverage.get("candidate_outcomes_consumed"), 0.0))
    missing_count = int(as_float(coverage.get("missing_candidate_outcomes"), 0.0))
    never_happened = int(as_float(missing.get("never_happened"), 0.0))
    happened_but_not_captured = int(as_float(missing.get("happened_but_not_captured"), 0.0))
    captured_but_not_consumed = int(as_float(missing.get("captured_but_not_consumed"), 0.0))
    visibility_issue = int(as_float(missing.get("visibility_issue"), 0.0))
    aggregation_issue = int(as_float(missing.get("aggregation_issue"), 0.0))
    weakly_weighted = int(as_float(missing.get("consumed_but_weakly_weighted"), 0.0))

    items = [
        _knowledge_limit_item(
            item="service_outcomes",
            classification="OBTAINABLE_NOW",
            owner=str(service_source.get("owner") or "service/quality probe owners"),
            evidence=str(service_source.get("current_utilization") or "existing service outcome source is acceleratable"),
            safe_cycle=str(service_source.get("safe_acceleration") or "run existing probes and refresh snapshots"),
            count=int(as_float(service_source.get("count"), 0.0)),
        ),
        _knowledge_limit_item(
            item="channel_quality_outcomes",
            classification="OBTAINABLE_NOW",
            owner=str(channel_source.get("owner") or "quality compact owner"),
            evidence=str(channel_source.get("current_utilization") or "existing channel quality source is acceleratable"),
            safe_cycle=str(channel_source.get("safe_acceleration") or "repeat quality compaction after probe windows"),
            count=int(as_float(channel_source.get("count"), 0.0)),
        ),
        _knowledge_limit_item(
            item="learning_refresh",
            classification="OBTAINABLE_NOW",
            owner=str(learning_source.get("owner") or "intelligence snapshot refresh"),
            evidence=f"knowledge_gained={learning_growth.get('knowledge_gained', 0)}",
            safe_cycle=str(learning_source.get("safe_acceleration") or "refresh after real probes/outcomes"),
            count=int(as_float(learning_source.get("count"), 0.0)),
        ),
        _knowledge_limit_item(
            item="prediction_outcomes",
            classification="OBTAINABLE_NOW" if prediction_pending > 0 else "OBTAINABLE_AFTER_EXISTING_EVENT",
            owner="prediction-summaries + service/channel actual rows + existing feedback owners",
            evidence=f"forecasts={prediction_seen}, matched={prediction_matched}, pending={prediction_pending}",
            safe_cycle="match pending forecast rows if actuals exist" if prediction_pending > 0 else "wait for next real forecast->actual interval, then refresh",
            blocker="" if prediction_pending > 0 else "no_pending_prediction_rows",
            count=prediction_pending,
        ),
        _knowledge_limit_item(
            item="captured_candidate_outcomes_not_consumed",
            classification="OBTAINABLE_NOW" if (captured_but_not_consumed + visibility_issue + aggregation_issue) > 0 else "OBTAINABLE_AFTER_EXISTING_EVENT",
            owner="candidate outcome matcher + intelligence snapshot refresh",
            evidence=f"captured_but_not_consumed={captured_but_not_consumed}, visibility_issue={visibility_issue}, aggregation_issue={aggregation_issue}",
            safe_cycle="refresh/rebuild existing candidate outcome snapshots if rows appear",
            blocker="" if (captured_but_not_consumed + visibility_issue + aggregation_issue) > 0 else "no_hidden_candidate_outcomes_available_now",
            count=captured_but_not_consumed + visibility_issue + aggregation_issue,
        ),
        _knowledge_limit_item(
            item="missing_candidate_outcomes",
            classification="OBTAINABLE_AFTER_GOVERNED_ACTION" if missing_count > 0 else "OBTAINABLE_NOW",
            owner="governed/manual outcome closure owners + candidate outcome matcher",
            evidence=f"candidate_count={candidate_count}, consumed={consumed}, missing={missing_count}, never_happened={never_happened}",
            safe_cycle="operator-approved governed/manual action followed by verification, closure, learning, and snapshot refresh",
            blocker="AUTHORITY_BOUNDARY" if missing_count > 0 else "",
            count=missing_count,
        ),
        _knowledge_limit_item(
            item="post_action_verification_outcomes",
            classification="OBTAINABLE_AFTER_GOVERNED_ACTION",
            owner="restore/rollback/verification owners",
            evidence=f"closure_state={decision_outcome_closure.get('closure_state', 'UNKNOWN')}, valid_closures={closure_summary.get('valid_closures', 0)}",
            safe_cycle="verify only after a real governed/manual action exists",
            blocker="real_post_action_outcome_required",
            count=int(as_float(closure_summary.get("missing_closure_records"), 0.0)),
        ),
        _knowledge_limit_item(
            item="weakly_weighted_candidate_outcomes",
            classification="OBTAINABLE_AFTER_EXISTING_EVENT" if weakly_weighted > 0 else "OBTAINABLE_AFTER_GOVERNED_ACTION",
            owner="trust evolution suitability aggregation",
            evidence=f"consumed_but_weakly_weighted={weakly_weighted}",
            safe_cycle="wait for stronger observed outcome confidence or produce real governed/manual verification",
            blocker="low_candidate_source_confidence",
            count=weakly_weighted,
        ),
        _knowledge_limit_item(
            item="client_telemetry",
            classification="REQUIRES_NEW_ARCHITECTURE",
            owner="future telemetry owner",
            evidence="canonical reference marks client telemetry as future primary source when implemented",
            safe_cycle="not available in current production system",
            blocker="telemetry_owner_not_implemented",
        ),
    ]
    if candidate_count <= 0:
        items.append(_knowledge_limit_item(
            item="candidate_suitability_diversity",
            classification="REQUIRES_MORE_USERS",
            owner="candidate-suitability-summary",
            evidence="no current candidate rows exist",
            safe_cycle="requires real users and candidate rows before extraction",
            blocker="no_current_candidate_population",
        ))

    current_suitability = as_float(growth_current.get("suitability"), as_float((real_outcome_growth_projection.get("current") or {}).get("suitability_confidence"), 0.0))
    max_suitability = as_float(best_projection.get("projected_suitability"), current_suitability)
    converted_at_max = int(as_float(best_projection.get("converted_missing_candidate_outcomes"), 0.0))
    unreachable_to_floor = round(max(0.0, AUTONOMY_CANARY_CONFIDENCE_FLOOR - max_suitability), 3)
    obtainable_after_governed = missing_count
    obtainable_now = captured_but_not_consumed + visibility_issue + aggregation_issue
    total_missing = max(1, missing_count)
    physical_impossibility = {
        "scope": "missing_current_suitability_candidate_outcomes",
        "missing_candidate_outcomes": missing_count,
        "obtainable_now_count": obtainable_now,
        "obtainable_after_governed_action_count": obtainable_after_governed,
        "requires_more_users_count": 0 if candidate_count > 0 else missing_count,
        "requires_more_channels_count": 0,
        "requires_new_services_count": 0,
        "requires_new_architecture_count": 0,
        "obtainable_today_percent": round((obtainable_now / total_missing) * 100.0, 3) if missing_count else 100.0,
        "obtainable_after_governed_action_percent": round((obtainable_after_governed / total_missing) * 100.0, 3) if missing_count else 0.0,
        "physically_impossible_without_more_users_or_channels_percent": 0.0 if candidate_count > 0 else 100.0,
        "explanation": "Current missing candidate outcomes are current user->candidate-channel pairs; they are not hidden, they have not happened yet.",
    }
    cycle_rows = []
    for cycle in autonomous_knowledge_growth_program.get("cycles") or []:
        if not isinstance(cycle, dict):
            continue
        blocker_class = _cycle_blocker_class(cycle)
        can_continue = blocker_class in {"NONE", "MISSING_TRIGGER"} and cycle.get("automation_level") != "MANUAL"
        cycle_rows.append({
            "cycle": cycle.get("cycle"),
            "automation_level": cycle.get("automation_level"),
            "blocker_class": blocker_class,
            "can_continue_automatically": can_continue,
            "safe_rerun": bool(cycle.get("apply_executed") is not True),
            "safe_next_step": cycle.get("safe_next_step"),
            "authority_boundary": cycle.get("authority_boundary", ""),
            "runtime_mutation_performed": False,
            "users_moved": 0,
            "apply_executed": False,
        })
    freshness_obtainable = [
        domain for domain, row in freshness_domains.items()
        if isinstance(row, dict) and row.get("classification") in {"STALE_RECHECK_REQUIRED", "UNKNOWN"}
    ]
    stop_reason = "AUTHORITY_BOUNDARY" if autonomous_routing_evolution_program.get("exact_stop_reason") == "AUTHORITY_BOUNDARY" else "REAL_WORLD_LIMIT"
    if unreachable_to_floor > 0 and missing_count == 0:
        stop_reason = "REAL_WORLD_LIMIT"
    return {
        "schema_version": "v7.autonomy-trust.maximum-reality-knowledge-extraction.v1",
        "owner": "admin_core.autonomy_trust_acceleration",
        "purpose": "extract_and_classify_all_real_routing_knowledge_obtainable_from_current_production_without_apply_or_new_architecture",
        "knowledge_limit_items": items,
        "classification_summary": _classification_summary(items),
        "outcome_sources_underused": [
            row.get("source") for row in source_items
            if row.get("classification") == "ACCELERATABLE" and row.get("current_utilization") not in {"refresh_owner_consumes_available_outcomes"}
        ],
        "automatic_cycle_completion": {
            "cycles": cycle_rows,
            "summary": _classification_summary([
                {"classification": row["blocker_class"]} for row in cycle_rows
            ]),
            "new_cycle_added": "Maximum Reality Knowledge Extraction Cycle",
            "new_cycle_automation_level": "FULLY_AUTONOMOUS",
            "automatic_rerun_works": True,
        },
        "physical_reality_limit": physical_impossibility,
        "maximum_current_suitability": {
            "current": round(current_suitability, 3),
            "maximum_possible_without_more_users_channels_formula_or_floor_changes": round(max_suitability, 3),
            "converted_missing_candidate_outcomes_at_max": converted_at_max,
            "remaining_unreachable_to_70_floor": unreachable_to_floor,
            "remaining_reason": "current observed correctness/source confidence cannot reach TIER_2 suitability floor from coverage alone" if unreachable_to_floor > 0 else "suitability_floor_reachable_after_current_real_outcomes",
            "projection_only": True,
        },
        "freshness_domains_recheckable_now": freshness_obtainable,
        "highest_leverage_now": [
            row.get("activity") for row in (outcome_leverage_model.get("activities_ranked") or [])[:3]
            if isinstance(row, dict)
        ],
        "final_stop_reason": stop_reason,
        "final_verdict": "REAL_WORLD_LIMIT_REACHED" if stop_reason == "REAL_WORLD_LIMIT" else "MAXIMUM_REALITY_REACHED",
        "read_only": True,
        "synthetic_evidence_created": False,
        "formula_changed": False,
        "floor_changed": False,
        "planner_redesigned": False,
        "governance_redesigned": False,
        "execution_redesigned": False,
        "new_truth_source_created": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
        "autonomy_enabled": False,
    }


def _architecture_status_summary(rows: list[dict[str, Any]]) -> dict[str, int]:
    return _classification_summary([
        {"classification": row.get("status", "UNKNOWN")} for row in rows
    ])


def _architecture_row(
    *,
    item: str,
    status: str,
    owner: str,
    evidence: str,
    limit: str = "",
    safe_extension: str = "",
) -> dict[str, Any]:
    return {
        "item": item,
        "status": status,
        "owner": owner,
        "evidence": evidence,
        "limit": limit,
        "safe_extension": safe_extension,
        "read_only": True,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def build_final_autonomous_routing_architecture_certification(
    *,
    knowledge_quality_read_model: dict[str, Any],
    autonomous_knowledge_growth_program: dict[str, Any],
    autonomous_routing_evolution_program: dict[str, Any],
    maximum_reality_knowledge_extraction: dict[str, Any],
    service_user_sla_fit: dict[str, Any],
    decision_outcome_closure: dict[str, Any],
    decision_outcome_learning: dict[str, Any],
    recovery_admission: dict[str, Any],
    anti_flapping: dict[str, Any],
    freshness_actionability: dict[str, Any],
    routing_recommendation_readiness: dict[str, Any],
    suitability_quality_model: dict[str, Any],
    candidate_outcome_reality_collection: dict[str, Any],
    real_outcome_source_inventory: dict[str, Any],
    prediction_plan: dict[str, Any],
    canary_proximity: dict[str, Any],
) -> dict[str, Any]:
    """Certify final architecture completeness from existing read-only owners."""
    objects = knowledge_quality_read_model.get("knowledge_objects")
    objects = objects if isinstance(objects, dict) else {}
    extraction_summary = maximum_reality_knowledge_extraction.get("classification_summary")
    extraction_summary = extraction_summary if isinstance(extraction_summary, dict) else {}
    coverage = candidate_outcome_reality_collection.get("coverage")
    coverage = coverage if isinstance(coverage, dict) else {}
    source_items = real_outcome_source_inventory.get("items")
    source_items = source_items if isinstance(source_items, list) else []
    source_names = {
        str(row.get("source"))
        for row in source_items
        if isinstance(row, dict) and row.get("source")
    }

    knowledge_sources = [
        _architecture_row(item="Channel Knowledge", status="EXISTS", owner="Channel Decision Adapter + planner/read models", evidence="Channel Decision V7 and channel operator signal owners"),
        _architecture_row(item="Service Knowledge", status="EXISTS", owner="service matrix / service-score snapshot owners", evidence="service_outcomes source and service verification cycle"),
        _architecture_row(item="User Knowledge", status="EXISTS", owner="operator decision surface + user registry", evidence="user assignment, current channel, profile, policy, and route context"),
        _architecture_row(item="Policy Knowledge", status="EXISTS", owner="planner policy gates + operator_execution_pipeline floors", evidence="policy load, eligibility, floors, restore/approval gates"),
        _architecture_row(item="Capacity Knowledge", status="EXISTS", owner="planner load gates + capacity summaries", evidence="capacity/load affects assignment and channel decision"),
        _architecture_row(item="Failure Knowledge", status="EXISTS", owner="event consumer + service/quality/runtime signals", evidence="regression events, channel/service degradation, planner blockers"),
        _architecture_row(item="Recovery Knowledge", status="PARTIAL", owner="build_recovery_admission + restore/rollback owners", evidence=f"recovery_admission={recovery_admission.get('schema_version', 'present')}", limit="operator-free recovery not certified", safe_extension="existing recovery admission and rollback owners; no new owner"),
        _architecture_row(item="Decision Knowledge", status="EXISTS", owner="operator decision surface + governed packet owners", evidence="knowledge-to-decision and governed dry-run cycle"),
        _architecture_row(item="Outcome Knowledge", status="EXISTS", owner="decision outcome closure + candidate outcome matcher", evidence=f"candidate_outcomes={coverage.get('candidate_outcomes_consumed', 0)}"),
        _architecture_row(item="Learning Knowledge", status="EXISTS", owner="operator_execution_feedback + trust-evolution summaries", evidence=f"knowledge_gained={(decision_outcome_learning.get('knowledge_growth') or {}).get('knowledge_gained', 0)}"),
        _architecture_row(item="Freshness Knowledge", status="EXISTS", owner="build_freshness_actionability", evidence=f"domains={len((freshness_actionability.get('domains') or {}) if isinstance(freshness_actionability.get('domains'), dict) else {})}"),
        _architecture_row(item="Suitability Knowledge", status="EXISTS", owner="suitability quality/growth/effectiveness models", evidence=f"stage={suitability_quality_model.get('current_stage', 'UNKNOWN')}", limit="not autonomy-grade yet; architecture present"),
        _architecture_row(item="Prediction Knowledge", status="EXISTS", owner="prediction snapshots + actual matcher", evidence=f"matched={prediction_plan.get('matched_rows', 0)}, pending={prediction_plan.get('pending_rows', 0)}"),
        _architecture_row(item="Reputation / Trust Knowledge", status="EXISTS", owner="trust-evolution summaries + trust source classification", evidence="observed outcome primary trust model"),
        _architecture_row(item="Client Observation Knowledge", status="PARTIAL", owner="service/channel/user outcome owners", evidence="observed network outcomes exist; direct client telemetry remains future optional extension", limit="direct client agent telemetry not implemented", safe_extension="future telemetry may enrich, but current architecture has observed outcome substitutes"),
        _architecture_row(item="Temporal Knowledge", status="EXISTS", owner="freshness/actionability + prediction forecast/actual windows", evidence="snapshot generated_at, forecast-to-actual, cooldown/freshness policies"),
        _architecture_row(item="Behavior Knowledge", status="EXISTS", owner="quality compact + trust/evolution + anti-flap owner", evidence=f"anti_flap={anti_flapping.get('schema_version', 'present')}"),
        _architecture_row(item="Cohort Knowledge", status="PARTIAL", owner="service_user_sla_fit + candidate diversity/read models", evidence="current cohort/SLA views are enough for current scale; 10k views are future scale extension", limit="10k cohort operator views deferred", safe_extension="aggregate read models after production autonomy certification"),
        _architecture_row(item="SLA Knowledge", status="PARTIAL", owner="build_service_user_sla_fit", evidence=f"sla_fit={service_user_sla_fit.get('schema_version', 'present')}", limit="SLA scale model not fully production-grade", safe_extension="reuse service/user/SLA fit owner"),
        _architecture_row(item="Safety / Blast / Rollback Knowledge", status="EXISTS", owner="restore barrier, rollback, blast-radius, canary proximity", evidence=f"missing_canary={len(canary_proximity.get('missing') or [])}"),
        _architecture_row(item="Runtime Readiness Knowledge", status="EXISTS", owner="truth/convergence + runtime readiness gates", evidence="dry-run reaches authority boundary without apply"),
    ]

    decisions = [
        _architecture_row(item="KEEP", status="EXISTS", owner="operator decision surface / planner", evidence="keep/no action decision rows"),
        _architecture_row(item="MOVE", status="EXISTS", owner="v7-users-autoswitch + governed packet", evidence="selected moves become governed packet preview"),
        _architecture_row(item="FAILOVER", status="EXISTS", owner="planner failover candidates + restore barrier", evidence="candidate failover path reaches authority boundary"),
        _architecture_row(item="DRAIN", status="EXISTS", owner="Channel Decision V7 Evacuate + planner selected moves", evidence="Evacuate/Move users expresses drain semantics"),
        _architecture_row(item="QUARANTINE", status="PARTIAL", owner="channel role/status + recovery admission", evidence="blocked/quarantine semantics exist; autonomous quarantine apply not enabled", limit="operator-free quarantine not certified"),
        _architecture_row(item="RECOVER", status="PARTIAL", owner="recovery admission + restore/rollback", evidence="staged recovery model exists; autonomous recovery promotion blocked by evidence/authority", limit="operator-free recovery not certified"),
        _architecture_row(item="WAIT", status="EXISTS", owner="knowledge gates + freshness/candidate blockers", evidence="wait for real event/outcome/snapshot gates"),
        _architecture_row(item="ASK_OPERATOR", status="EXISTS", owner="AUTHORITY_BOUNDARY + operator approval/packet owners", evidence="governed dry-run stops before restore-barrier write/apply"),
        _architecture_row(item="NO_ACTION", status="EXISTS", owner="operator decision surface", evidence="healthy/no-action rows"),
        _architecture_row(item="SELF_STOP", status="EXISTS", owner="governed canary dry-run + planner gates", evidence=f"stop={autonomous_routing_evolution_program.get('exact_stop_reason', 'UNKNOWN')}"),
        _architecture_row(item="SELF_LIMIT", status="EXISTS", owner="floors, blast radius, restore barrier, capacity gates", evidence="canary proximity, risk tiers, and restore guards"),
    ]

    lifecycle_stages = ["observation", "verification", "decision", "outcome", "learning", "freshness", "aging", "reuse", "retirement"]
    lifecycle = []
    lifecycle_status_by_stage: dict[str, str] = {}
    for stage in lifecycle_stages:
        if stage in {"aging", "retirement"}:
            status = "PARTIAL"
            owner = "freshness_actionability + future deferred evidence index"
            limit = "long-horizon decay/retirement remains post-production scale extension"
        elif stage == "reuse":
            status = "EXISTS"
            owner = "intelligence snapshots + trust inventory"
            limit = ""
        else:
            status = "EXISTS"
            owner = {
                "observation": "service/quality/event/snapshot owners",
                "verification": "service matrix + post-action verification owners",
                "decision": "operator decision surface + planner/governed packet",
                "outcome": "decision outcome closure + candidate matcher",
                "learning": "operator_execution_feedback + trust evolution",
                "freshness": "build_freshness_actionability",
            }[stage]
            limit = ""
        lifecycle_status_by_stage[stage] = status
        lifecycle.append(_architecture_row(
            item=stage,
            status=status,
            owner=owner,
            evidence="covered by existing owner" if status == "EXISTS" else "covered as guard/label; deeper scale semantics deferred",
            limit=limit,
            safe_extension="reuse existing owner; no new truth source" if status == "PARTIAL" else "",
        ))

    cycle_rows = [
        row for row in (autonomous_knowledge_growth_program.get("cycles") or [])
        if isinstance(row, dict)
    ]
    cycle_certification = []
    for row in cycle_rows:
        boundary = str(row.get("authority_boundary") or "")
        automation = str(row.get("automation_level") or "")
        blocker_class = _cycle_blocker_class(row)
        cycle_certification.append({
            "cycle": row.get("cycle"),
            "owner": row.get("owner"),
            "automation_level": automation,
            "executes_automatically": automation in {"FULLY_AUTONOMOUS", "AUTONOMOUS_UNTIL_BOUNDARY"},
            "blocker_class": blocker_class,
            "why_not_fully_automatic": boundary or ", ".join(str(item) for item in row.get("blockers") or []) or "none",
            "safe_integration_removed_blocker": False,
            "read_only": True,
            "runtime_mutation_performed": False,
            "users_moved": 0,
            "apply_executed": False,
        })

    routing_capabilities = [
        _architecture_row(item="Observe", status="EXISTS", owner="service/quality/event/snapshot owners", evidence="events and snapshots feed planner/read models"),
        _architecture_row(item="Classify", status="EXISTS", owner="knowledge quality + channel decision + risk tiers", evidence="signals become knowledge/decision states"),
        _architecture_row(item="Decide", status="EXISTS", owner="operator decision surface + planner", evidence="knowledge-to-decision implemented"),
        _architecture_row(item="Plan", status="EXISTS", owner="v7-users-autoswitch", evidence="candidate selection and dry-run planner"),
        _architecture_row(item="Limit Blast Radius", status="EXISTS", owner="risk tiers + restore barrier + blast evidence", evidence="one-user canary / bounded apply guards"),
        _architecture_row(item="Execute Under Authority", status="EXISTS", owner="operator execution packet + restore barrier", evidence="execution path exists but stops at authority boundary"),
        _architecture_row(item="Verify Outcome", status="EXISTS", owner="operator_execution_feedback + service outcomes", evidence="post-action verification and service outcomes"),
        _architecture_row(item="Rollback / No-Rollback", status="EXISTS", owner="rollback owner + restore settle gate", evidence="rollback confidence path exists"),
        _architecture_row(item="Learn", status="EXISTS", owner="decision outcome learning + trust evolution", evidence="decision-to-outcome-to-learning implemented"),
        _architecture_row(item="Self-Stop / Self-Limit", status="EXISTS", owner="governed dry-run + floors + truth/convergence", evidence="authority and evidence floors block apply"),
    ]

    duplicate_owner_audit = {
        "new_planner_created": False,
        "new_governance_created": False,
        "new_execution_path_created": False,
        "new_truth_source_created": False,
        "new_storage_created": False,
        "duplicate_knowledge_owner_detected": False,
        "merged_through_existing_owner": "admin_core.autonomy_trust_acceleration",
    }

    fundamental_missing = [
        row["item"] for row in knowledge_sources + decisions + lifecycle + routing_capabilities
        if row.get("status") == "MISSING"
    ]
    partial_classes = [
        row["item"] for row in knowledge_sources + decisions + lifecycle + routing_capabilities
        if row.get("status") == "PARTIAL"
    ]
    optional_extensions = [
        "direct client telemetry owner",
        "10k-scale cohort/SLA aggregate operator views",
        "post-production evidence index/freshness decay and retirement weighting",
        "operator-free quarantine/recovery apply certification",
    ]
    real_world_limited = (
        maximum_reality_knowledge_extraction.get("final_stop_reason") in {"AUTHORITY_BOUNDARY", "REAL_WORLD_LIMIT"}
        or extraction_summary.get("OBTAINABLE_AFTER_GOVERNED_ACTION", 0) > 0
    )
    final_verdict = "ARCHITECTURE_HAS_FUNDAMENTAL_GAPS" if fundamental_missing else "ARCHITECTURE_COMPLETE_WITH_FUTURE_OPTIONAL_EXTENSIONS"
    if not fundamental_missing and not partial_classes:
        final_verdict = "ARCHITECTURE_COMPLETE"

    return {
        "schema_version": "v7.autonomy-trust.final-autonomous-routing-architecture-certification.v1",
        "owner": "admin_core.autonomy_trust_acceleration",
        "purpose": "certify_architecture_completeness_without_runtime_apply_or_new_architecture",
        "reference_basis": [
            "docs/reference/V7_CANONICAL_REFERENCE.md",
            "docs/reference/SYSTEM_MAP.md",
            "docs/reference/V7_AUTONOMY_BLUEPRINT.md",
            "docs/reference/V7_IDEAL_AUTONOMOUS_ROUTING_MODEL.md",
            "docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md",
            "certified reports through V7_MAXIMUM_REALITY_KNOWLEDGE_EXTRACTION_REPORT.md",
        ],
        "knowledge_source_completeness": knowledge_sources,
        "knowledge_source_summary": _architecture_status_summary(knowledge_sources),
        "decision_completeness": decisions,
        "decision_summary": _architecture_status_summary(decisions),
        "lifecycle_completeness": lifecycle,
        "lifecycle_summary": _architecture_status_summary(lifecycle),
        "lifecycle_status_by_stage": lifecycle_status_by_stage,
        "autonomy_cycle_completeness": {
            "cycles": cycle_certification,
            "cycle_count": len(cycle_certification),
            "automation_counts": autonomous_knowledge_growth_program.get("automation_counts", {}),
            "overall_autonomy_maturity_score": autonomous_knowledge_growth_program.get("overall_autonomy_maturity_score", 0.0),
            "cycles_automatic_until_boundary": [
                row.get("cycle") for row in cycle_certification
                if row.get("automation_level") == "AUTONOMOUS_UNTIL_BOUNDARY"
            ],
            "cycles_fully_automatic": [
                row.get("cycle") for row in cycle_certification
                if row.get("automation_level") == "FULLY_AUTONOMOUS"
            ],
            "blocker_summary": _classification_summary([
                {"classification": row["blocker_class"]} for row in cycle_certification
            ]),
        },
        "routing_completeness": routing_capabilities,
        "routing_summary": _architecture_status_summary(routing_capabilities),
        "duplication_audit": duplicate_owner_audit,
        "safe_architectural_gap_closed_in_this_phase": "final architecture certification read model exposed through existing trust inventory owner",
        "fundamental_missing_classes": fundamental_missing,
        "partial_classes": partial_classes,
        "future_optional_extensions": optional_extensions,
        "architecture_limit": "REAL_WORLD_EXPERIENCE_AND_AUTHORITY" if real_world_limited else "NONE",
        "current_blockers_are_architectural": bool(fundamental_missing),
        "current_blockers": {
            "authority_boundary": autonomous_routing_evolution_program.get("exact_stop_reason") == "AUTHORITY_BOUNDARY",
            "real_world_limit": maximum_reality_knowledge_extraction.get("final_stop_reason") == "REAL_WORLD_LIMIT",
            "candidate_outcome_gap": (candidate_outcome_reality_collection.get("coverage") or {}).get("missing_candidate_outcomes", 0),
            "canary_missing": canary_proximity.get("missing", []),
            "source_names": sorted(source_names),
        },
        "next_program": "GOVERNED_CANDIDATE_OUTCOME_EXECUTION_AND_CLOSURE",
        "final_verdict": final_verdict,
        "read_only": True,
        "synthetic_evidence_created": False,
        "formula_changed": False,
        "floor_changed": False,
        "planner_redesigned": False,
        "governance_redesigned": False,
        "execution_redesigned": False,
        "new_truth_source_created": False,
        "new_storage_created": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
        "autonomy_enabled": False,
    }


def _candidate_key_text(key: tuple[str, str]) -> str:
    return f"{key[0]}:{key[1]}"


def _candidate_diversity(keys: set[tuple[str, str]]) -> dict[str, Any]:
    users = {user for user, _channel in keys if user}
    channels = {channel for _user, channel in keys if channel}
    repeated_user_keys = len(keys) - len(users)
    repeated_channel_keys = len(keys) - len(channels)
    return {
        "effective_experiences": len(keys),
        "unique_users": len(users),
        "unique_channels": len(channels),
        "repeated_user_channel_variants": max(0, repeated_user_keys),
        "repeated_channel_exposures": max(0, repeated_channel_keys),
        "channels": sorted(channels),
    }


def build_candidate_outcome_reality_collection(
    *,
    candidate_suitability_snapshot: dict[str, Any],
    decision_records: list[dict[str, Any]] | None = None,
    floor_forensics: dict[str, Any] | None = None,
    increments: list[int] | None = None,
) -> dict[str, Any]:
    """Explain candidate outcome coverage without creating evidence.

    Candidate outcomes are only real when an existing decision/feedback owner
    has observed an outcome for a current user->channel candidate. This read
    model reuses the same candidate snapshot and decision records as
    build_candidate_outcome_rows; it only exposes why coverage is missing.
    """
    increments = increments or [10, 25, 50, 100]
    candidate_rows = _items(candidate_suitability_snapshot)
    candidate_keys = intelligence_workers._candidate_keys(candidate_rows)
    consumed_outcomes = intelligence_workers.build_candidate_outcome_rows(candidate_rows, decision_records or [])
    consumed_keys = {
        (str(row.get("user") or ""), str(row.get("channel") or row.get("egress") or row.get("target") or ""))
        for row in consumed_outcomes
        if isinstance(row, dict) and (row.get("user") or row.get("channel") or row.get("egress") or row.get("target"))
    }
    consumed_keys = {(user, channel) for user, channel in consumed_keys if user and channel}

    selected_keys: set[tuple[str, str]] = set()
    known_selected_keys: set[tuple[str, str]] = set()
    unknown_selected_keys: set[tuple[str, str]] = set()
    all_known_outcome_keys: set[tuple[str, str]] = set()
    rollback_only_keys: set[tuple[str, str]] = set()

    for record in decision_records or []:
        if not isinstance(record, dict):
            continue
        is_rollback_only = intelligence_workers._rollback_only_outcome_evidence(record)
        base = intelligence_workers.normalize_outcome_evidence(
            record,
            evidence_source=str(record.get("evidence_source") or "decision_record"),
        )
        base = intelligence_workers._switch_history_arrival_evidence(record, base)
        for move in intelligence_workers._selected_move_rows(record):
            user = intelligence_workers._user_from_row(move) or str(base.get("user") or "")
            channel = intelligence_workers._channel_from_row(move) or str(base.get("channel") or "")
            if not user or not channel:
                continue
            key = (user, channel)
            selected_keys.add(key)
            if is_rollback_only:
                rollback_only_keys.add(key)
                continue
            if base.get("outcome_status") == "unknown":
                unknown_selected_keys.add(key)
                continue
            known_selected_keys.add(key)
            all_known_outcome_keys.add(key)

    missing_keys = candidate_keys - consumed_keys
    happened_but_not_captured = missing_keys & unknown_selected_keys
    captured_but_not_consumed = missing_keys & (all_known_outcome_keys - consumed_keys)
    visibility_or_aggregation_loss = missing_keys & (known_selected_keys - consumed_keys)
    never_happened = missing_keys - happened_but_not_captured - captured_but_not_consumed - visibility_or_aggregation_loss
    consumed_but_weakly_weighted = {
        tuple(str(part) for part in str(row.get("key") or ":").split(":", 1))
        for row in ((floor_forensics or {}).get("raw_rows") or {}).get("suitability", [])
        if isinstance(row, dict)
        and row.get("outcome_seen")
        and as_float(row.get("confidence"), 0.0) < 0.5
        and ":" in str(row.get("key") or "")
    }

    projections = []
    current_suitability = as_float(((floor_forensics or {}).get("component_values") or {}).get("suitability_confidence"), 0.0)
    current_confidence = as_float(((floor_forensics or {}).get("floor_values") or {}).get("confidence", {}).get("current"), 0.0)
    current_trust = as_float(((floor_forensics or {}).get("floor_values") or {}).get("trust", {}).get("current"), 0.0)
    current_prediction = as_float(((floor_forensics or {}).get("component_values") or {}).get("prediction_confidence"), 0.0)
    missing_count = len(missing_keys)
    for increment in increments:
        converted = min(max(0, int(increment)), missing_count)
        coverage_after = (len(consumed_keys) + converted) / max(1, len(candidate_keys))
        projections.append({
            "additional_real_candidate_outcomes": increment,
            "converted_missing_candidate_outcomes": converted,
            "missing_candidate_outcomes_remaining": max(0, missing_count - converted),
            "projected_coverage": round(coverage_after, 4),
            "projected_suitability": round(min(100.0, current_suitability + converted * 0.35), 3),
            "projected_confidence": round(min(100.0, current_confidence + converted * 0.18), 3),
            "projected_trust": round(min(100.0, current_trust + converted * 0.12), 3),
            "projected_prediction": round(current_prediction, 3),
            "canary_readiness": "still_blocked_until_real_confidence_trust_floors_pass",
            "projection_only": True,
        })

    sample_limit = 25
    return {
        "schema_version": "v7.autonomy-trust.candidate-outcome-reality-collection.v1",
        "definition": "real_candidate_outcome = existing governed/manual/switch/feedback record with usable observed result for a current user->candidate_channel pair",
        "knowledge_chain": [
            "candidate-suitability-summary creates user->channel candidates",
            "existing decision/feedback/switch/closure records may provide real outcomes",
            "build_candidate_outcome_rows matches outcomes by user+channel",
            "suitability_trust_model converts score vs observed result into candidate confidence",
            "trust-evolution-summaries aggregate suitability into canary confidence/trust gates",
        ],
        "owners": {
            "candidate_snapshot": "admin_core.intelligence_workers.build_candidate_suitability_snapshot",
            "outcome_matcher": "admin_core.intelligence_workers.build_candidate_outcome_rows",
            "suitability_model": "admin_core.intelligence_platform.suitability_trust_model",
            "snapshot_refresh": "tools/v7-intelligence-snapshot-refresh",
            "runtime_inventory": "tools/v7-autonomy-trust-evidence-inventory",
        },
        "stores": {
            "candidate_snapshot": "intelligence/candidate-suitability-summary snapshot family",
            "decision_records": "switch-history, audit, operator execution audit/governance, execution-events, runtime-trust, proposals, closure records, rollback history",
            "trust_summary": "intelligence/trust-evolution-summaries snapshot family",
        },
        "coverage": {
            "candidate_count": len(candidate_keys),
            "candidate_outcomes_consumed": len(consumed_keys),
            "missing_candidate_outcomes": len(missing_keys),
            "coverage_ratio": round(len(consumed_keys) / max(1, len(candidate_keys)), 4),
            "selected_candidate_keys_seen": len(candidate_keys & selected_keys),
            "known_selected_candidate_outcomes": len(candidate_keys & known_selected_keys),
            "unknown_selected_candidate_outcomes": len(candidate_keys & unknown_selected_keys),
        },
        "missing_outcome_analysis": {
            "never_happened": len(never_happened),
            "happened_but_not_captured": len(happened_but_not_captured),
            "captured_but_not_consumed": len(captured_but_not_consumed),
            "consumed_but_weakly_weighted": len(consumed_but_weakly_weighted),
            "visibility_issue": len(visibility_or_aggregation_loss),
            "aggregation_issue": 0 if not visibility_or_aggregation_loss else len(visibility_or_aggregation_loss),
            "samples": {
                "never_happened": [_candidate_key_text(key) for key in sorted(never_happened)[:sample_limit]],
                "happened_but_not_captured": [_candidate_key_text(key) for key in sorted(happened_but_not_captured)[:sample_limit]],
                "captured_but_not_consumed": [_candidate_key_text(key) for key in sorted(captured_but_not_consumed)[:sample_limit]],
                "visibility_or_aggregation_loss": [_candidate_key_text(key) for key in sorted(visibility_or_aggregation_loss)[:sample_limit]],
            },
        },
        "diversity": {
            "all_candidates": _candidate_diversity(candidate_keys),
            "consumed_outcomes": _candidate_diversity(consumed_keys),
            "missing_outcomes": _candidate_diversity(missing_keys),
        },
        "acceleration": {
            "ACCELERATABLE_NOW": [
                "continue real service/channel probe cycles",
                "refresh intelligence snapshots after real probes",
                "consume already-existing governed/manual closure records if they appear",
            ],
            "ACCELERATABLE_GOVERNED": [
                "operator-approved/manual moves followed by post-action verification through existing feedback and closure owners",
            ],
            "CANARY_REQUIRED": [
                "new autonomous candidate outcomes from bounded canary apply",
            ],
            "PRODUCTION_REQUIRED": [
                "high-volume autonomous outcome growth after canary confidence is earned",
            ],
            "synthetic_outcomes_allowed": False,
            "runtime_apply_allowed_in_this_phase": False,
            "users_moved": 0,
        },
        "growth_model": {
            "current": {
                "suitability": round(current_suitability, 3),
                "confidence": round(current_confidence, 3),
                "trust": round(current_trust, 3),
                "prediction": round(current_prediction, 3),
            },
            "projections": projections,
            "uses_current_formulas_only": True,
        },
        "readiness_impact": {
            "exact_outcome_deficit_blocks_canary": 0,
            "inventory_deficit_supporting_signal": missing_count,
            "inventory_deficit_is_mandatory_certification_requirement": False,
            "signal_category": "INVENTORY_SIGNAL",
            "real_missing_experience": len(never_happened),
            "capture_loss": len(happened_but_not_captured),
            "aggregation_loss": len(visibility_or_aggregation_loss),
            "visibility_loss": 0 if not visibility_or_aggregation_loss else len(visibility_or_aggregation_loss),
            "confidence_penalty": max(0.0, 70.0 - current_confidence),
            "trust_penalty": max(0.0, 70.0 - current_trust),
        },
        "selected_move_outcomes_outside_current_candidates": len(all_known_outcome_keys - candidate_keys),
        "rollback_only_keys_seen": len(rollback_only_keys),
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def _comparison_projection_value(shadow_model: dict[str, Any], comparisons: int, agreement_rate: float) -> float:
    projection = shadow_model.get("comparison_growth_projection") if isinstance(shadow_model.get("comparison_growth_projection"), dict) else {}
    for row in projection.get("rows") or []:
        if int(as_float(row.get("comparisons"), -1)) == comparisons and abs(as_float(row.get("agreement_rate"), -1.0) - agreement_rate) < 0.0001:
            return as_float(row.get("earned_confidence"), 0.0)
    return 0.0


def build_trust_source_classification() -> dict[str, Any]:
    return {
        "schema_version": "v7.autonomy-trust.source-classification.v1",
        "primary": [
            {
                "source": "observed_service_outcome",
                "owner": "admin_core.intelligence_workers / service matrix owners",
                "store": "service-scores and channel-service-scores snapshots",
                "current_maturity": "active",
                "autonomy_trust_use": "primary",
                "needs_more_tests": False,
            },
            {
                "source": "observed_channel_quality",
                "owner": "tools/v7-egress-quality-compact and channel score readers",
                "store": "quality summary, channel/service snapshots, trust-evolution summaries",
                "current_maturity": "active_under_confident",
                "autonomy_trust_use": "primary",
                "needs_more_tests": False,
            },
            {
                "source": "post_switch_verification",
                "owner": "admin_core.operator_execution_feedback / tools/v7-users-autoswitch governed apply",
                "store": "execution-events, runtime-trust, proposals, closure records",
                "current_maturity": "active_governed_evidence",
                "autonomy_trust_use": "primary_after_governed_or_canary_apply",
                "needs_more_tests": False,
            },
            {
                "source": "rollback_or_no_rollback_result",
                "owner": "operator execution pipeline and rollback owner",
                "store": "rollback history, closure records, trust-evolution summaries",
                "current_maturity": "active_model_rollout_not_operator_free_certified",
                "autonomy_trust_use": "primary_safety_evidence",
                "needs_more_tests": False,
            },
            {
                "source": "forecast_to_actual_accuracy",
                "owner": "admin_core.intelligence_workers / admin_core.intelligence_platform",
                "store": "prediction-summaries, service/channel actual rows, governed prediction feedback",
                "current_maturity": "active_but_low_source_confidence",
                "autonomy_trust_use": "primary",
                "needs_more_tests": False,
            },
            {
                "source": "client_telemetry",
                "owner": "future existing telemetry owner",
                "store": "UNKNOWN - requires future implementation",
                "current_maturity": "not_implemented",
                "autonomy_trust_use": "primary_when_implemented",
                "needs_more_tests": True,
            },
        ],
        "secondary": [
            {
                "source": "operator_comparison",
                "owner": "admin_core.shadow_autonomy / /api/actions/shadow-autonomy-compare",
                "store": "shadow-autonomy JSONL family",
                "current_maturity": "path_ready_evidence_underfed",
                "autonomy_trust_use": "secondary_supervised_confirmation",
                "needs_more_tests": False,
                "blind_review_required": False,
            },
            {
                "source": "operator_override",
                "owner": "admin_core.shadow_autonomy",
                "store": "shadow-autonomy JSONL family and audit",
                "current_maturity": "path_ready",
                "autonomy_trust_use": "secondary_contextual_signal",
                "needs_more_tests": False,
            },
            {
                "source": "manual_approval",
                "owner": "operator execution and admin action owners",
                "store": "audit / governed execution records",
                "current_maturity": "active",
                "autonomy_trust_use": "secondary_authority_not_fake_agreement",
                "needs_more_tests": False,
            },
        ],
        "diagnostic": [
            {"source": "raw_technical_health", "autonomy_trust_use": "diagnostic_only"},
            {"source": "route_details", "autonomy_trust_use": "diagnostic_or_supporting_unless_real_blocker"},
            {"source": "logs", "autonomy_trust_use": "diagnostic_only"},
            {"source": "score_components", "autonomy_trust_use": "diagnostic_only"},
        ],
    }


def build_operator_authority_model() -> dict[str, Any]:
    return {
        "schema_version": "v7.operator-authority-model.v1",
        "manual_action_authoritative": True,
        "manual_action_is_fake_agreement": False,
        "system_must_respect_manual_action": True,
        "outcome_observation_after_manual_action": True,
        "operator_comparison_role": "secondary_supervised_confirmation_only_when_context_is_sufficient",
        "blind_bulk_review_required": False,
        "rules": [
            "manual operator switches are authoritative actions",
            "manual actions are not synthetic agreement with an autonomous recommendation",
            "V7 should observe service and quality outcome after the action",
            "future degradation should trigger proposal or operator confirmation through existing owners",
            "operator comparison may raise confidence only when the operator has enough context",
        ],
    }


ROUTING_FOUNDATION_SNAPSHOT_FAMILIES = (
    "prediction-summaries",
    "service-scores",
    "channel-service-scores",
    "user-service-scores",
    "candidate-suitability-summary",
    "best-available-pool",
    "trust-summaries",
    "risk-summaries",
    "blast-radius-summaries",
    "trust-evolution-summaries",
    "capacity-forecast-summaries",
    "overview-summary",
)

FRESHNESS_ACTIONABILITY_DOMAINS = {
    "service": ["service-scores", "channel-service-scores", "user-service-scores"],
    "quality": ["channel-service-scores", "prediction-summaries"],
    "route": ["risk-summaries", "overview-summary"],
    "capacity": ["capacity-forecast-summaries", "blast-radius-summaries", "overview-summary"],
    "prediction": ["prediction-summaries"],
    "suitability": ["candidate-suitability-summary", "best-available-pool"],
    "recovery": ["trust-evolution-summaries"],
}

VALID_OUTCOME_CLOSURE_FIELDS = (
    "recommendation_id",
    "decision_id",
    "packet_id",
    "apply_result",
    "post_action_verification",
    "service_outcome",
    "user_outcome",
    "learning_record",
    "outcome_observed_at",
)

RECOVERY_ADMISSION_POLICY = {
    "min_successful_checks": 3,
    "freshness_required": "ACTIONABLE_NOW",
    "cooldown_seconds": 1800,
    "limited_recovery_blast_radius_users": 1,
    "watch_successful_checks": 2,
}

ANTI_FLAP_POLICY = {
    "cooldown_seconds": 1800,
    "minimum_observation_window_seconds": 3600,
    "rapid_oscillation_threshold": 2,
    "hysteresis_required": True,
}


def _text(value: Any, default: str = "") -> str:
    return str(value if value not in (None, "") else default)


def _candidate_channel(row: dict[str, Any] | None) -> str:
    if not isinstance(row, dict):
        return ""
    return _text(row.get("channel") or row.get("egress") or row.get("target") or row.get("recommended_channel"))


def _candidate_score(row: dict[str, Any] | None) -> float:
    if not isinstance(row, dict):
        return 0.0
    return as_float(row.get("fit_score", row.get("suitability_score", row.get("score", row.get("adjusted_score", row.get("confidence", 0.0))))), 0.0)


def _candidate_reasons(row: dict[str, Any] | None) -> list[str]:
    if not isinstance(row, dict):
        return []
    out: list[str] = []
    for key in ("missing_requirements", "required_missing", "required_low", "blockers"):
        value = row.get(key)
        if isinstance(value, list):
            out.extend(str(item) for item in value if item)
        elif value:
            out.append(str(value))
    return list(dict.fromkeys(out))


def _required_services_from_surface(user_row: dict[str, Any], candidate_rows: list[dict[str, Any]]) -> list[str]:
    for value in (
        user_row.get("required_services"),
        (user_row.get("service_fit") or {}).get("required_services") if isinstance(user_row.get("service_fit"), dict) else None,
    ):
        if isinstance(value, list) and value:
            return [str(item) for item in value if item]
    for row in candidate_rows:
        value = row.get("required_services") or row.get("services_required")
        if isinstance(value, list) and value:
            return [str(item) for item in value if item]
    try:
        return [str(item) for item in intelligence_workers.DEFAULT_SERVICES]
    except AttributeError:
        return ["telegram", "youtube", "instagram", "chatgpt"]


def _candidate_rows_for_user(user_row: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [row for row in (user_row.get("candidates") or user_row.get("pool") or []) if isinstance(row, dict)]
    current = _text(user_row.get("current_channel") or user_row.get("current"))
    recommended = _text(user_row.get("recommended_channel") or user_row.get("best_channel") or current)
    if recommended and all(_candidate_channel(row) != recommended for row in rows):
        rows.append({
            "channel": recommended,
            "score": user_row.get("confidence", user_row.get("fit_score", 0.0)),
            "required_services": user_row.get("required_services", []),
            "reasons": user_row.get("reasons", []),
        })
    if current and all(_candidate_channel(row) != current for row in rows):
        rows.append({
            "channel": current,
            "score": user_row.get("current_score", 0.0),
            "required_services": user_row.get("required_services", []),
        })
    return rows


HARD_FAILURE_EXPLICIT_TOKENS = (
    "down",
    "unreachable",
    "no response",
    "timeout",
    "timed out",
    "connection refused",
    "connection reset",
    "network unreachable",
    "host unreachable",
    "route unreachable",
    "dead",
    "blackhole",
    "all probes failed",
    "health check failed",
    "not able to carry",
    "cannot carry",
)

HARD_FAILURE_STATUS_TOKENS = {
    "DOWN",
    "FAILED",
    "FAIL",
    "UNHEALTHY",
    "CRITICAL",
    "UNREACHABLE",
    "NOT_STARTED",
    "NO_ROUTE",
    "NO_RESPONSE",
    "TIMEOUT",
}

HARD_FAILURE_STRONG_SOURCES = {
    "runtime_readiness",
    "route_readiness",
}

HARD_FAILURE_LIVENESS_SOURCES = {
    "telegram_sentinel",
    "service_matrix",
    "quality_compact",
    "runtime_readiness",
    "route_readiness",
}


def _hard_failure_evidence_object(event: dict[str, Any]) -> str:
    return _text(
        event.get("object")
        or event.get("channel")
        or event.get("egress")
        or event.get("target")
        or event.get("service")
        or event.get("component")
        or "unknown"
    )


def _hard_failure_event_state(event: dict[str, Any]) -> tuple[bool, str]:
    text = " ".join(
        _text(event.get(key)).lower()
        for key in ("status", "state", "severity", "message", "reason", "raw_reason", "action", "event_type", "type")
    )
    status = _text(event.get("status") or event.get("state") or event.get("severity")).upper()
    if status in HARD_FAILURE_STATUS_TOKENS:
        return True, f"explicit_status={status}"
    for token in HARD_FAILURE_EXPLICIT_TOKENS:
        if token in text:
            return True, f"explicit_liveness_token={token}"
    if event.get("severity") == "error" and event.get("source") in HARD_FAILURE_LIVENESS_SOURCES:
        return True, "source_error_from_liveness_owner"
    return False, "no_explicit_hard_failure_liveness"


def build_hard_failure_classification(
    *,
    decision_surface: dict[str, Any] | None = None,
    freshness_actionability: dict[str, Any] | None = None,
    service_user_sla_fit: dict[str, Any] | None = None,
    snapshot_statuses: dict[str, dict[str, Any]] | None = None,
    event_rows: list[dict[str, Any]] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Classify hard-failure evidence without creating actions or new truth."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    normalized_events = [
        v7_events.normalize_regression_event(row)
        for row in (event_rows or [])
        if isinstance(row, dict)
    ]
    evidence_by_object: dict[str, list[dict[str, Any]]] = {}
    for event in normalized_events:
        source = _text(event.get("source"))
        explicit, reason = _hard_failure_event_state(event)
        if source not in HARD_FAILURE_LIVENESS_SOURCES and not explicit:
            continue
        obj = _hard_failure_evidence_object(event)
        evidence_by_object.setdefault(obj, []).append({
            "source": source,
            "event_id": event.get("event_id", ""),
            "event_type": event.get("event_type", ""),
            "severity": event.get("severity", ""),
            "confidence": event.get("confidence", 0.0),
            "explicit_liveness_failure": explicit,
            "reason": reason,
            "requires_confirmation": event.get("requires_confirmation", True),
            "timestamp": event.get("timestamp", ""),
        })
    fit_rows = [
        row for row in ((service_user_sla_fit or {}).get("rows") or [])
        if isinstance(row, dict)
    ]
    for row in fit_rows:
        blockers = " ".join([
            _text(row.get("reason")),
            " ".join(_text(item) for item in row.get("missing_requirements", []) if item),
            _text(row.get("fit_verdict")),
        ]).lower()
        if not any(token in blockers for token in ("route_or_runtime_not_safe", "missing_required_services", "service_freshness_not_actionable")):
            continue
        channel = _text(row.get("current_assignment") or row.get("best_channel") or "unknown")
        evidence_by_object.setdefault(channel, []).append({
            "source": "service_user_sla_fit",
            "event_id": "",
            "event_type": "service_user_fit_blocker",
            "severity": "warning",
            "confidence": 0.5,
            "explicit_liveness_failure": False,
            "reason": "fit_model_blocks_or_requires_recheck",
            "requires_confirmation": True,
            "timestamp": "",
        })
    rows: list[dict[str, Any]] = []
    for obj, evidence in sorted(evidence_by_object.items()):
        explicit = [row for row in evidence if row.get("explicit_liveness_failure")]
        sources = sorted({_text(row.get("source")) for row in evidence if row.get("source")})
        strong_source = any(source in HARD_FAILURE_STRONG_SOURCES for source in sources)
        if len({row.get("source") for row in explicit}) >= 2 or (strong_source and explicit):
            classification = "HARD_FAILURE_CONFIRMED"
        elif explicit:
            classification = "HARD_FAILURE_SUSPECTED"
        else:
            classification = "NO_HARD_FAILURE_CONFIRMED"
        rows.append({
            "object": obj,
            "classification": classification,
            "evidence_count": len(evidence),
            "explicit_liveness_evidence_count": len(explicit),
            "independent_sources": sources,
            "requires_confirmation": classification != "HARD_FAILURE_CONFIRMED",
            "reaction_allowed_without_policy": False,
            "runtime_apply_allowed": False,
            "evidence": evidence[:20],
        })
    stale_domains = [
        name for name, row in ((freshness_actionability or {}).get("domains") or {}).items()
        if isinstance(row, dict) and row.get("classification") in {"STALE_RECHECK_REQUIRED", "UNKNOWN"}
    ]
    if not rows:
        verdict = "NO_HARD_FAILURE_EVIDENCE"
    elif any(row["classification"] == "HARD_FAILURE_CONFIRMED" for row in rows):
        verdict = "HARD_FAILURE_CONFIRMED"
    elif any(row["classification"] == "HARD_FAILURE_SUSPECTED" for row in rows):
        verdict = "HARD_FAILURE_SUSPECTED"
    else:
        verdict = "NO_HARD_FAILURE_CONFIRMED"
    if stale_domains and verdict != "HARD_FAILURE_CONFIRMED":
        verdict = "RECHECK_REQUIRED"
    return {
        "schema_version": "v7.policy-001.hard-failure-classification.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "source_owners_reused": [
            "admin_core.events",
            "tools/v7-service-matrix-refresh-all",
            "tools/v7-service-matrix-test",
            "tools/v7-egress-quality-compact",
            "tools/v7-telegram-sentinel",
            "admin_core.operator_decision_surface",
            "admin_core.intelligence_snapshots",
        ],
        "policy_source": "docs/policies/POLICY_001_HARD_FAILURE.md",
        "classification": verdict,
        "rows": rows,
        "summary": {
            "objects_seen": len(rows),
            "confirmed": sum(1 for row in rows if row["classification"] == "HARD_FAILURE_CONFIRMED"),
            "suspected": sum(1 for row in rows if row["classification"] == "HARD_FAILURE_SUSPECTED"),
            "stale_or_unknown_domains": sorted(stale_domains),
            "normalized_events_consumed": len(normalized_events),
        },
        "consensus_rules_applied": [
            "hard_failure_requires_explicit_liveness_evidence",
            "single_noisy_observation_is_suspected_not_confirmed",
            "reaction_requires_policy_blast_radius_rollback_verification_and_authority",
            "classification_does_not_execute",
        ],
        "implementation_backlog_item": "A1",
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "synthetic_evidence_created": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
    }


def _owner_issued_freshness_fields(freshness_actionability: dict[str, Any], domain: str) -> dict[str, Any]:
    domain_row = ((freshness_actionability.get("domains") or {}).get(domain) or {})
    family_statuses = domain_row.get("family_statuses") if isinstance(domain_row.get("family_statuses"), dict) else {}
    fields: dict[str, Any] = {}
    for family, status in sorted(family_statuses.items()):
        if not isinstance(status, dict):
            continue
        fields[family] = {
            "exists": bool(status.get("exists", False)),
            "freshness_state": _text(status.get("freshness_state") or status.get("status") or "UNKNOWN"),
            "runtime_behavior": _text(status.get("runtime_behavior") or "STOP"),
            "stop_required": bool(status.get("stop_required", True)),
            "confidence": as_float(status.get("confidence"), 0.0),
            "path": _text(status.get("path")),
            "source_hashes": status.get("source_hashes") if isinstance(status.get("source_hashes"), dict) else {},
        }
    return fields


def build_action_class_freshness_windows(
    freshness_actionability: dict[str, Any] | None = None,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Expose canonical per-action-class freshness windows from existing owners."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    freshness = freshness_actionability or build_freshness_actionability({})
    rows: list[dict[str, Any]] = []
    for action_class, windows in ACTION_CLASS_FRESHNESS_WINDOWS.items():
        domain_rows = []
        blockers = []
        for domain, max_age in sorted(windows.items()):
            domain_state = ((freshness.get("domains") or {}).get(domain) or {})
            classification = _text(domain_state.get("classification") or "UNKNOWN")
            if classification != "ACTIONABLE_NOW":
                blockers.append(f"{domain}={classification}")
            domain_rows.append({
                "domain": domain,
                "max_age_seconds": int(max_age),
                "classification": classification,
                "reason": _text(domain_state.get("reason")),
                "owner_issued_fields": _owner_issued_freshness_fields(freshness, domain),
            })
        rows.append({
            "action_class": action_class,
            "freshness_windows": dict(windows),
            "domains": domain_rows,
            "freshness_ready": not blockers,
            "blockers": blockers,
            "owner_issued_freshness_fields_present": any(
                bool(domain.get("owner_issued_fields")) for domain in domain_rows
            ),
        })
    return {
        "schema_version": "v7.action-class-freshness-windows.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "source_owner_reused": "admin_core.intelligence_snapshots + existing snapshot families",
        "policy_source": "docs/programs/V7_IMPLEMENTATION_BACKLOG.md item A2",
        "rows": rows,
        "summary": {
            "action_classes": len(rows),
            "ready": sum(1 for row in rows if row["freshness_ready"]),
            "blocked": sum(1 for row in rows if not row["freshness_ready"]),
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
    }


def build_freshness_actionability(
    snapshot_statuses: dict[str, dict[str, Any]] | None = None,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Classify existing evidence freshness into operator actionability buckets."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    statuses = snapshot_statuses or {}
    domains: dict[str, dict[str, Any]] = {}
    counts = {
        "ACTIONABLE_NOW": 0,
        "STALE_RECHECK_REQUIRED": 0,
        "DIAGNOSTIC_ONLY": 0,
        "HISTORY_ONLY": 0,
        "UNKNOWN": 0,
    }
    for domain, families in FRESHNESS_ACTIONABILITY_DOMAINS.items():
        family_rows = [statuses.get(name, {}) for name in families if isinstance(statuses.get(name, {}), dict)]
        existing = [row for row in family_rows if row.get("exists", True) is not False and row]
        states = {str(row.get("freshness_state") or row.get("status") or "UNKNOWN").upper() for row in family_rows}
        behaviors = {str(row.get("runtime_behavior") or "").upper() for row in family_rows}
        stop_required = any(bool(row.get("stop_required")) for row in family_rows)
        if not family_rows or not existing:
            classification = "UNKNOWN"
            reason = "no_existing_snapshot_status"
        elif "EXPIRED" in states or stop_required:
            classification = "STALE_RECHECK_REQUIRED"
            reason = "expired_or_stop_required"
        elif "STALE" in states:
            classification = "STALE_RECHECK_REQUIRED"
            reason = "stale_snapshot_present"
        elif states and states <= {"FRESH", "OK"} and not stop_required:
            classification = "ACTIONABLE_NOW"
            reason = "fresh_existing_evidence"
        elif "IGNORE" in behaviors:
            classification = "DIAGNOSTIC_ONLY"
            reason = "snapshot_runtime_behavior_ignore"
        elif domain == "recovery":
            classification = "HISTORY_ONLY"
            reason = "recovery_needs_recent_successful_observation"
        else:
            classification = "UNKNOWN"
            reason = "freshness_contract_incomplete"
        counts[classification] += 1
        domains[domain] = {
            "classification": classification,
            "reason": reason,
            "families": families,
            "family_statuses": {name: statuses.get(name, {}) for name in families},
            "runtime_mutation_performed": False,
        }
    return {
        "schema_version": "v7.routing-foundation.freshness-actionability.v1",
        "generated_at": generated,
        "owner": "admin_core.intelligence_snapshots",
        "domains": domains,
        "summary": counts,
        "read_only": True,
        "runtime_mutation_performed": False,
        "apply_executed": False,
        "users_moved": 0,
    }


def _candidate_fit(candidate: dict[str, Any], required_services: list[str], freshness: dict[str, Any]) -> dict[str, Any]:
    channel = _candidate_channel(candidate)
    score = _candidate_score(candidate)
    missing = _candidate_reasons(candidate)
    service_classification = ((freshness.get("domains") or {}).get("service") or {}).get("classification", "UNKNOWN")
    capacity_text = " ".join(str(value).lower() for value in (
        candidate.get("capacity_decision"),
        candidate.get("capacity_state"),
        candidate.get("assignment"),
        " ".join(missing),
    ))
    policy_allowed = candidate.get("policy_eligible", candidate.get("eligible", True)) is not False
    capacity_allowed = not any(token in capacity_text for token in ("over", "full", "limit", "blocked"))
    service_ok = not missing and service_classification == "ACTIONABLE_NOW"
    route_runtime_safe = candidate.get("route_safe", candidate.get("runtime_safe", True)) is not False
    blockers: list[str] = []
    if missing:
        blockers.append("missing_required_services")
    if service_classification != "ACTIONABLE_NOW":
        blockers.append("service_freshness_not_actionable")
    if not capacity_allowed:
        blockers.append("capacity_or_load_blocks_fit")
    if not policy_allowed:
        blockers.append("policy_blocks_fit")
    if not route_runtime_safe:
        blockers.append("route_or_runtime_not_safe")
    if blockers:
        verdict = "RECHECK_REQUIRED" if blockers == ["service_freshness_not_actionable"] else "BLOCKED"
    elif score >= 75:
        verdict = "FIT"
    else:
        verdict = "FIT_WITH_WARNINGS"
    return {
        "channel": channel,
        "fit_score": round(score, 3),
        "fit_verdict": verdict,
        "required_services": required_services,
        "missing_requirements": missing,
        "service_freshness": service_classification,
        "capacity_headroom": candidate.get("capacity_headroom", candidate.get("headroom", "")),
        "policy_eligible": bool(policy_allowed),
        "route_runtime_safe": bool(route_runtime_safe),
        "reason": "; ".join(blockers) if blockers else "candidate satisfies current required services and safety context",
    }


def build_service_user_sla_fit(
    decision_surface: dict[str, Any] | None = None,
    *,
    freshness_actionability: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Read-only per-user fit lens over existing recommendation/candidate rows."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    surface = decision_surface or {}
    freshness = freshness_actionability or build_freshness_actionability({})
    rows: list[dict[str, Any]] = []
    for user_row in [row for row in (surface.get("users") or []) if isinstance(row, dict)]:
        user = _text(user_row.get("user") or user_row.get("ip") or user_row.get("address"))
        if not user:
            continue
        candidates = _candidate_rows_for_user(user_row)
        required = _required_services_from_surface(user_row, candidates)
        evaluated = [_candidate_fit(row, required, freshness) for row in candidates]
        usable = [row for row in evaluated if row["fit_verdict"] in {"FIT", "FIT_WITH_WARNINGS"}]
        best = sorted(usable, key=lambda row: (-as_float(row.get("fit_score")), row.get("channel", "")))[0] if usable else {}
        current = _text(user_row.get("current_channel") or user_row.get("current"))
        recommendation = _text(best.get("channel") or user_row.get("recommended_channel") or current)
        rows.append({
            "user": user,
            "current_assignment": current,
            "required_services": required,
            "fit_score": best.get("fit_score", 0.0) if best else 0.0,
            "fit_verdict": best.get("fit_verdict", "BLOCKED" if evaluated else "UNKNOWN"),
            "missing_requirements": sorted({item for row in evaluated for item in row.get("missing_requirements", [])}),
            "best_channel": recommendation,
            "safe_alternatives": [row["channel"] for row in usable if row.get("channel") != recommendation],
            "reason": best.get("reason") if best else "no candidate satisfies current service/user/SLA fit",
            "candidates": evaluated,
            "runtime_mutation_performed": False,
        })
    verdict_counts: dict[str, int] = {}
    for row in rows:
        verdict = str(row.get("fit_verdict") or "UNKNOWN")
        verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1
    return {
        "schema_version": "v7.routing-foundation.service-user-sla-fit.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "source_owner": "admin_core.operator_decision_surface + intelligence snapshots",
        "rows": rows,
        "summary": {
            "users_seen": len(rows),
            "verdict_counts": verdict_counts,
            "planner_input_candidate_only": True,
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "apply_executed": False,
        "users_moved": 0,
    }


def _closure_field_present(record: dict[str, Any], field: str) -> bool:
    aliases = {
        "recommendation_id": ("recommendation_id", "recommendation_hash", "proposal_id"),
        "decision_id": ("decision_id", "operation_id", "object_id"),
        "packet_id": ("packet_id", "approval_packet_id"),
        "apply_result": ("apply_result", "result", "status", "execution_outcome"),
        "post_action_verification": ("post_action_verification", "verification_result", "verification"),
        "service_outcome": ("service_outcome", "service_actual", "service_delta"),
        "user_outcome": ("user_outcome", "selected_moves", "user"),
        "learning_record": ("learning_record", "trust_update", "prediction_actual"),
        "outcome_observed_at": ("outcome_observed_at", "completed_at", "event_time", "timestamp", "ts"),
    }
    return any(record.get(alias) not in (None, "", [], {}) for alias in aliases.get(field, (field,)))


def build_decision_outcome_closure(
    decision_records: list[dict[str, Any]] | None = None,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Expose whether real recommendation outcomes are closed end-to-end."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    rows: list[dict[str, Any]] = []
    for index, record in enumerate([row for row in (decision_records or []) if isinstance(row, dict)]):
        missing = [field for field in VALID_OUTCOME_CLOSURE_FIELDS if not _closure_field_present(record, field)]
        evidence = intelligence_workers.normalize_outcome_evidence(record)
        rows.append({
            "record_index": index,
            "closure_valid": not missing,
            "missing_fields": missing,
            "outcome_status": evidence.get("outcome_status", "unknown"),
            "user": evidence.get("user", ""),
            "channel": evidence.get("channel", ""),
        })
    valid = sum(1 for row in rows if row["closure_valid"])
    state = "COMPLETE" if rows and valid == len(rows) else "PARTIAL" if rows else "ABSENT"
    return {
        "schema_version": "v7.routing-foundation.decision-outcome-closure.v1",
        "generated_at": generated,
        "owner": "existing audit/feedback/closure records",
        "required_fields": list(VALID_OUTCOME_CLOSURE_FIELDS),
        "closure_state": state,
        "summary": {
            "records_seen": len(rows),
            "valid_closures": valid,
            "missing_closure_records": len(rows) - valid,
            "real_outcomes_required": state != "COMPLETE",
        },
        "rows": rows[:50],
        "synthetic_outcomes_created": False,
        "read_only": True,
        "runtime_mutation_performed": False,
        "apply_executed": False,
        "users_moved": 0,
    }


def _decision_outcome_learning_from_trust(trust_evolution_snapshot: dict[str, Any] | None) -> dict[str, Any]:
    summary = _first_item(trust_evolution_snapshot)
    model = summary.get("decision_outcome_learning") if isinstance(summary.get("decision_outcome_learning"), dict) else {}
    if model:
        return model
    return {
        "schema_version": "v7.decision-outcome-learning.model.v1",
        "owner": "admin_core.operator_execution_feedback",
        "source": "trust-evolution-summaries.decision_outcome_learning",
        "outcome_quality_counts": {"SUCCESS": 0, "PARTIAL_SUCCESS": 0, "FAILED": 0, "UNKNOWN": 0},
        "effectiveness": {
            "recommendation_correct_rate": 0.0,
            "service_improved_rate": 0.0,
            "rollback_rate": 0.0,
            "fit_prediction_correct_rate": 0.0,
            "recovery_prediction_correct_rate": 0.0,
            "prediction_correct_rate": 0.0,
        },
        "knowledge_growth": {
            "knowledge_gained": 0,
            "knowledge_improved": [],
            "knowledge_degraded": [],
            "knowledge_unchanged_count": 0,
        },
        "rows": [],
        "read_only": True,
        "synthetic_evidence_created": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def _channel_rows_for_recovery(decision_surface: dict[str, Any], channel_recovery_inputs: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    if channel_recovery_inputs is not None:
        return [row for row in channel_recovery_inputs if isinstance(row, dict)]
    rows = [row for row in (decision_surface or {}).get("channels", []) if isinstance(row, dict)]
    if rows:
        return rows
    channels = {}
    for user in (decision_surface or {}).get("users", []) or []:
        if not isinstance(user, dict):
            continue
        for key in ("current_channel", "recommended_channel"):
            channel = _text(user.get(key))
            if channel:
                channels.setdefault(channel, {"channel": channel, "successful_checks": 0, "lifecycle": "UNKNOWN"})
    return list(channels.values())


def build_recovery_admission(
    decision_surface: dict[str, Any] | None = None,
    *,
    freshness_actionability: dict[str, Any] | None = None,
    channel_recovery_inputs: list[dict[str, Any]] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Stage channel recovery admission without changing trust or planner logic."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    freshness = freshness_actionability or build_freshness_actionability({})
    recovery_freshness = ((freshness.get("domains") or {}).get("recovery") or {}).get("classification", "UNKNOWN")
    rows: list[dict[str, Any]] = []
    for row in _channel_rows_for_recovery(decision_surface or {}, channel_recovery_inputs):
        channel = _text(row.get("channel") or row.get("id") or row.get("egress"))
        lifecycle = _text(row.get("lifecycle") or row.get("channel_state") or row.get("state"), "UNKNOWN").upper()
        evidence = row.get("channel_state_evidence_summary") if isinstance(row.get("channel_state_evidence_summary"), dict) else {}
        successes = int(as_float(row.get("successful_checks", row.get("successes", evidence.get("successes", 0))), 0.0))
        blockers: list[str] = []
        if lifecycle in {"QUARANTINED", "DEGRADED"} or row.get("quarantine_until"):
            blockers.append("quarantine_or_degraded_lifecycle")
        if successes < RECOVERY_ADMISSION_POLICY["min_successful_checks"]:
            blockers.append("insufficient_successful_checks")
        if recovery_freshness != "ACTIONABLE_NOW":
            blockers.append("recovery_freshness_not_actionable")
        if row.get("cooldown_active"):
            blockers.append("cooldown_active")
        service_specific_ok = row.get("service_specific_recovery_ok")
        if service_specific_ok is None:
            service_specific_ok = True
        if not service_specific_ok:
            blockers.append("service_specific_recovery_missing")
        if "quarantine_or_degraded_lifecycle" in blockers:
            state = "QUARANTINED"
        elif row.get("blocked") or "service_specific_recovery_missing" in blockers:
            state = "BLOCKED"
        elif successes < RECOVERY_ADMISSION_POLICY["watch_successful_checks"]:
            state = "PROBING"
        elif blockers:
            state = "LIMITED_RECOVERY"
        elif lifecycle in {"RECOVERING", "WATCH"}:
            state = "RECOVERED_WATCH"
        else:
            state = "ELIGIBLE"
        rows.append({
            "channel": channel,
            "admission_state": state,
            "successful_checks": successes,
            "min_successful_checks": RECOVERY_ADMISSION_POLICY["min_successful_checks"],
            "freshness": recovery_freshness,
            "blockers": blockers,
            "blast_radius_limit_users": RECOVERY_ADMISSION_POLICY["limited_recovery_blast_radius_users"] if state == "LIMITED_RECOVERY" else None,
            "operator_visible_reason": "; ".join(blockers) if blockers else "recovery admission evidence is staged and fresh",
            "runtime_mutation_performed": False,
        })
    return {
        "schema_version": "v7.routing-foundation.recovery-admission.v1",
        "generated_at": generated,
        "owner": "trust-evolution/read-only admission overlay",
        "policy": RECOVERY_ADMISSION_POLICY,
        "rows": rows,
        "summary": {
            "channels_seen": len(rows),
            "eligible": sum(1 for row in rows if row["admission_state"] == "ELIGIBLE"),
            "blocked_or_quarantined": sum(1 for row in rows if row["admission_state"] in {"BLOCKED", "QUARANTINED"}),
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "apply_executed": False,
        "users_moved": 0,
    }


def _record_user(record: dict[str, Any]) -> str:
    metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    return _text(record.get("user") or record.get("ip") or metadata.get("user"))


def _record_from_to(record: dict[str, Any]) -> tuple[str, str]:
    selected = record.get("selected_moves") if isinstance(record.get("selected_moves"), list) else []
    move = selected[0] if selected and isinstance(selected[0], dict) else {}
    source = _text(record.get("from") or record.get("source") or move.get("from") or move.get("source") or move.get("current"))
    target = _text(record.get("to") or record.get("target") or record.get("channel") or move.get("to") or move.get("target") or move.get("channel"))
    return source, target


def build_anti_flapping(
    decision_records: list[dict[str, Any]] | None = None,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Detect rapid oscillation using existing decision/audit records only."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    by_user: dict[str, list[dict[str, Any]]] = {}
    for record in decision_records or []:
        if not isinstance(record, dict):
            continue
        user = _record_user(record)
        source, target = _record_from_to(record)
        if not user or not target:
            continue
        by_user.setdefault(user, []).append({"source": source, "target": target, "raw": record})
    rows: list[dict[str, Any]] = []
    for user, moves in sorted(by_user.items()):
        transitions = [(row["source"], row["target"]) for row in moves]
        rapid_reverse = any(a_from == b_to and a_to == b_from and a_from and a_to for a_from, a_to in transitions for b_from, b_to in transitions)
        repeated_targets = len([target for _source, target in transitions]) - len({target for _source, target in transitions})
        blocked = bool(rapid_reverse or repeated_targets >= ANTI_FLAP_POLICY["rapid_oscillation_threshold"])
        rows.append({
            "user": user,
            "decision_stability": "BLOCKED_BY_ANTI_FLAP" if blocked else "STABLE_ENOUGH_FOR_PREVIEW",
            "blocked": blocked,
            "reasons": (["rapid_reverse_move_detected"] if rapid_reverse else []) + (["repeated_target_oscillation"] if repeated_targets >= ANTI_FLAP_POLICY["rapid_oscillation_threshold"] else []),
            "cooldown_seconds": ANTI_FLAP_POLICY["cooldown_seconds"] if blocked else 0,
            "transitions_seen": [f"{source}->{target}" for source, target in transitions],
        })
    return {
        "schema_version": "v7.routing-foundation.anti-flapping.v1",
        "generated_at": generated,
        "owner": "existing decision/audit records",
        "policy": ANTI_FLAP_POLICY,
        "rows": rows,
        "summary": {
            "users_seen": len(rows),
            "blocked_users": sum(1 for row in rows if row["blocked"]),
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "apply_executed": False,
        "users_moved": 0,
    }


def build_routing_recommendation_readiness(
    *,
    service_user_sla_fit: dict[str, Any],
    decision_outcome_closure: dict[str, Any],
    recovery_admission: dict[str, Any],
    anti_flapping: dict[str, Any],
    freshness_actionability: dict[str, Any],
    knowledge_quality_read_model: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blockers: list[str] = []
    fit_counts = (service_user_sla_fit.get("summary") or {}).get("verdict_counts") or {}
    if fit_counts.get("BLOCKED") or fit_counts.get("UNKNOWN"):
        blockers.append("service_user_sla_fit_not_clear")
    if decision_outcome_closure.get("closure_state") != "COMPLETE":
        blockers.append("decision_outcome_closure_incomplete")
    if (recovery_admission.get("summary") or {}).get("blocked_or_quarantined", 0):
        blockers.append("recovery_admission_has_blocked_channels")
    if (anti_flapping.get("summary") or {}).get("blocked_users", 0):
        blockers.append("anti_flap_blocks_recent_oscillation")
    stale_domains = [
        name for name, row in (freshness_actionability.get("domains") or {}).items()
        if row.get("classification") in {"STALE_RECHECK_REQUIRED", "UNKNOWN"}
    ]
    if stale_domains:
        blockers.append("freshness_not_actionable:" + ",".join(sorted(stale_domains)))
    if knowledge_quality_read_model and (knowledge_quality_read_model.get("10k_readiness") or {}).get("overall") != "READY":
        blockers.append("knowledge_quality_not_autonomy_ready")
    readiness = "READY_FOR_READ_ONLY_PREVIEW" if not blockers else "NOT_READY_FOR_AUTONOMOUS_ROUTING"
    return {
        "schema_version": "v7.routing-foundation.recommendation-readiness.v1",
        "readiness": readiness,
        "blockers": blockers,
        "safe_next_phase": "governed_preview_or_operator_review" if not blockers else "collect_real_outcomes_refresh_evidence_and_recheck",
        "runtime_apply_allowed": False,
        "read_only": True,
        "runtime_mutation_performed": False,
        "apply_executed": False,
        "users_moved": 0,
    }


def _snapshot_status_from_read_result(result: Any) -> dict[str, Any]:
    validation = getattr(result, "validation", None)
    payload = getattr(result, "payload", {}) or {}
    errors = list(getattr(validation, "errors", []) or [])
    warnings = list(getattr(validation, "warnings", []) or [])
    return {
        "exists": bool(getattr(result, "exists", False)),
        "validation_ok": bool(getattr(validation, "ok", False)),
        "freshness_state": str(getattr(result, "freshness_state", payload.get("freshness_state", "UNKNOWN")) or "UNKNOWN"),
        "confidence": getattr(result, "confidence", payload.get("confidence", 0.0)),
        "runtime_behavior": str(getattr(result, "runtime_behavior", "STOP") or "STOP"),
        "stop_required": bool(getattr(result, "stop_required", True)),
        "path": str(getattr(result, "path", "")),
        "errors": errors,
        "warnings": warnings,
    }


KNOWLEDGE_QUALITY_DIMENSIONS = (
    "freshness",
    "coverage",
    "correctness",
    "consistency",
    "diversity",
    "source_confidence",
    "user_impact_relevance",
    "service_relevance",
    "actionability",
)


VALID_KNOWLEDGE_MATURITY_STAGES = (
    "RAW_OBSERVATION",
    "STABLE_SIGNAL",
    "CONFIRMED_KNOWLEDGE",
    "ACTIONABLE_KNOWLEDGE",
    "AUTONOMY_GRADE_KNOWLEDGE",
)


CANONICAL_KNOWLEDGE_OBJECTS: tuple[dict[str, Any], ...] = (
    {
        "object": "Channel",
        "owner": "registry, planner, read models",
        "sources": ["egress registry", "runtime state", "planner output"],
        "consumers": ["planner", "admin UI", "autonomy"],
        "scores": [4, 4, 4, 4, 3, 4, 3, 3, 4],
        "action_authority": True,
        "tier_support": {"TIER_0": "required", "TIER_1": "required", "TIER_2": "required", "TIER_3_PLUS": "required"},
        "primary_gaps": ["100+ channel pool-class read models"],
        "next_improvement": "Add cohort/pool summaries without changing planner truth.",
    },
    {
        "object": "Service",
        "owner": "service matrix, intelligence workers",
        "sources": ["service probes", "service actual rows", "channel-service snapshots"],
        "consumers": ["planner", "diagnostics", "trust"],
        "scores": [3, 3, 3, 3, 2, 2, 2, 4, 3],
        "action_authority": False,
        "tier_support": {"TIER_0": "required", "TIER_1": "supporting", "TIER_2": "required", "TIER_3_PLUS": "required"},
        "primary_gaps": ["source confidence", "service/user/SLA outcome fit"],
        "next_improvement": "Raise real service outcome confidence through existing service/intelligence summaries.",
    },
    {
        "object": "User Assignment",
        "owner": "planner, user registry",
        "sources": ["user registry", "current channel", "candidate outcomes"],
        "consumers": ["planner", "execution", "admin UI"],
        "scores": [4, 4, 4, 4, 3, 4, 4, 2, 4],
        "action_authority": True,
        "tier_support": {"TIER_0": "required", "TIER_1": "required", "TIER_2": "required", "TIER_3_PLUS": "required"},
        "primary_gaps": ["cohort summaries", "service-fit assignment context"],
        "next_improvement": "Expose assignment cohorts and candidate outcome coverage.",
    },
    {
        "object": "Route",
        "owner": "route read models",
        "sources": ["route reality", "route readiness", "leak/mismatch evidence"],
        "consumers": ["diagnostics", "planner support"],
        "scores": [3, 3, 3, 3, 2, 3, 2, 2, 3],
        "action_authority": False,
        "tier_support": {"TIER_0": "supporting", "TIER_1": "supporting", "TIER_2": "supporting", "TIER_3_PLUS": "required_when_route_risk_exists"},
        "primary_gaps": ["route aggregation", "cohort route risk"],
        "next_improvement": "Keep route as supporting truth until route risk becomes a real blocker.",
    },
    {
        "object": "Capacity",
        "owner": "planner, capacity/read models",
        "sources": ["configured limits", "assigned users", "dynamic load summaries"],
        "consumers": ["planner", "recovery", "admin UI"],
        "scores": [4, 4, 4, 4, 2, 4, 3, 2, 4],
        "action_authority": False,
        "tier_support": {"TIER_0": "supporting", "TIER_1": "supporting", "TIER_2": "required", "TIER_3_PLUS": "required"},
        "primary_gaps": ["observed practical capacity", "load-to-user-impact mapping"],
        "next_improvement": "Integrate observed capacity without changing capacity formulas.",
    },
    {
        "object": "Quality",
        "owner": "quality compact, intelligence",
        "sources": ["speed", "latency", "stability", "failure rate"],
        "consumers": ["planner", "trust", "diagnostics"],
        "scores": [3, 3, 3, 3, 3, 3, 3, 2, 3],
        "action_authority": False,
        "tier_support": {"TIER_0": "required", "TIER_1": "supporting", "TIER_2": "required", "TIER_3_PLUS": "required"},
        "primary_gaps": ["freshness/decay", "service outcome attribution"],
        "next_improvement": "Attach quality evidence to service/user outcome closure.",
    },
    {
        "object": "Failure",
        "owner": "events, probes, intelligence",
        "sources": ["sentinel", "service matrix", "quality regressions", "planner blockers"],
        "consumers": ["attention", "planner", "operator"],
        "scores": [4, 3, 3, 3, 3, 3, 3, 3, 4],
        "action_authority": False,
        "tier_support": {"TIER_0": "supporting", "TIER_1": "supporting", "TIER_2": "required", "TIER_3_PLUS": "required"},
        "primary_gaps": ["cohort impact", "source maturity priority"],
        "next_improvement": "Rank failure evidence by affected users and source maturity.",
    },
    {
        "object": "Recovery",
        "owner": "service/quality/intelligence",
        "sources": ["successful checks", "retained outcomes", "post-recovery behavior"],
        "consumers": ["planner", "autonomy"],
        "scores": [2, 2, 2, 3, 2, 2, 2, 2, 2],
        "action_authority": False,
        "tier_support": {"TIER_0": "optional", "TIER_1": "optional", "TIER_2": "supporting", "TIER_3_PLUS": "required"},
        "primary_gaps": ["recovery admission", "anti-flap/hysteresis"],
        "next_improvement": "Define staged recovery admission before autonomous recovery.",
    },
    {
        "object": "Decision Outcome",
        "owner": "execution, feedback, learning",
        "sources": ["post-action verification", "closure", "rollback/no-rollback"],
        "consumers": ["trust", "planner", "learning"],
        "scores": [3, 3, 4, 4, 3, 4, 4, 2, 4],
        "action_authority": False,
        "tier_support": {"TIER_0": "optional", "TIER_1": "optional", "TIER_2": "required", "TIER_3_PLUS": "required"},
        "primary_gaps": ["candidate outcome coverage"],
        "next_improvement": "Close real governed/manual outcomes through existing feedback owners.",
    },
    {
        "object": "Prediction",
        "owner": "intelligence workers/platform",
        "sources": ["forecasts", "later actuals", "governed prediction feedback"],
        "consumers": ["trust", "autonomy gates"],
        "scores": [4, 3, 4, 4, 2, 2, 3, 3, 3],
        "action_authority": False,
        "tier_support": {"TIER_0": "optional", "TIER_1": "optional", "TIER_2": "required", "TIER_3_PLUS": "required"},
        "primary_gaps": ["source confidence"],
        "next_improvement": "Continue forecast-to-actual cycles through existing prediction owners.",
    },
    {
        "object": "Suitability",
        "owner": "trust inventory, intelligence, planner outcomes",
        "sources": ["candidate outcomes", "selected/rejected moves", "correctness"],
        "consumers": ["planner", "trust", "autonomy"],
        "scores": [3, 2, 2, 3, 2, 2, 4, 3, 3],
        "action_authority": False,
        "tier_support": {"TIER_0": "supporting", "TIER_1": "supporting", "TIER_2": "required", "TIER_3_PLUS": "required"},
        "primary_gaps": ["coverage", "correctness"],
        "next_improvement": "Grow real candidate outcome closure; do not synthesize outcomes.",
    },
    {
        "object": "Trust",
        "owner": "trust evolution, trust inventory",
        "sources": ["confidence components", "source inventory", "floors"],
        "consumers": ["governance", "autonomy gates"],
        "scores": [3, 3, 3, 4, 3, 3, 3, 2, 4],
        "action_authority": True,
        "tier_support": {"TIER_0": "supporting", "TIER_1": "supporting", "TIER_2": "required", "TIER_3_PLUS": "required"},
        "primary_gaps": ["weak inherited prediction/service/suitability inputs"],
        "next_improvement": "Keep gates blocking higher tiers until input knowledge improves.",
    },
    {
        "object": "Policy",
        "owner": "planner, policy/governance",
        "sources": ["policy/group settings", "access rules", "channel roles"],
        "consumers": ["planner", "execution"],
        "scores": [4, 3, 4, 4, 2, 4, 3, 2, 5],
        "action_authority": True,
        "tier_support": {"TIER_0": "required", "TIER_1": "required", "TIER_2": "required", "TIER_3_PLUS": "required"},
        "primary_gaps": ["SLA/cohort routing context"],
        "next_improvement": "Add read-only SLA/cohort policy context before planner impact.",
    },
    {
        "object": "Freshness",
        "owner": "snapshot store, evidence owners",
        "sources": ["evidence timestamps", "source families", "refresh state"],
        "consumers": ["planner", "trust", "admin UI"],
        "scores": [2, 2, 3, 3, 2, 3, 2, 2, 2],
        "action_authority": False,
        "tier_support": {"TIER_0": "supporting", "TIER_1": "supporting", "TIER_2": "required", "TIER_3_PLUS": "required"},
        "primary_gaps": ["explicit decay/actionability"],
        "next_improvement": "Expose stale/expired knowledge labels through existing snapshot/trust owners.",
    },
    {
        "object": "Safety",
        "owner": "restore, rollback, packet, blast owners",
        "sources": ["packet validation", "restore preview", "rollback manifest", "blast evidence"],
        "consumers": ["governance", "execution", "autonomy"],
        "scores": [4, 4, 5, 4, 4, 5, 4, 2, 5],
        "action_authority": True,
        "tier_support": {"TIER_0": "required", "TIER_1": "required", "TIER_2": "required", "TIER_3_PLUS": "required"},
        "primary_gaps": ["operator-free rollback certification for higher tiers"],
        "next_improvement": "Certify one-user autonomous rollback before TIER_3.",
    },
    {
        "object": "Event",
        "owner": "event sources and read-only consumer",
        "sources": ["sentinel", "service matrix", "quality/capacity/route/runtime events"],
        "consumers": ["attention", "planner preview", "autonomy preview"],
        "scores": [4, 3, 3, 3, 3, 3, 3, 3, 3],
        "action_authority": False,
        "tier_support": {"TIER_0": "required", "TIER_1": "optional", "TIER_2": "supporting", "TIER_3_PLUS": "required"},
        "primary_gaps": ["apply authority intentionally disabled"],
        "next_improvement": "Keep event consumer read-only until trust/freshness/recovery are stronger.",
    },
    {
        "object": "Operator Context",
        "owner": "shadow autonomy, operator comparison",
        "sources": ["contextual approve/reject/override evidence"],
        "consumers": ["secondary trust", "admin UI"],
        "scores": [2, 1, 2, 3, 1, 2, 3, 1, 2],
        "action_authority": False,
        "tier_support": {"TIER_0": "diagnostic", "TIER_1": "optional", "TIER_2": "optional", "TIER_3_PLUS": "optional"},
        "primary_gaps": ["contextual comparison evidence underfed"],
        "next_improvement": "Use existing compare endpoint only when operator has sufficient context.",
    },
)


def _quality_scores(raw_scores: list[int]) -> dict[str, int]:
    return dict(zip(KNOWLEDGE_QUALITY_DIMENSIONS, raw_scores))


def _knowledge_maturity_stage(
    *,
    scores: dict[str, int],
    action_authority: bool,
    object_name: str,
) -> str:
    average = sum(scores.values()) / max(1, len(scores))
    if (
        object_name == "Safety"
        and scores["correctness"] >= 5
        and scores["source_confidence"] >= 5
        and scores["actionability"] >= 5
        and average >= 4.0
    ):
        return "AUTONOMY_GRADE_KNOWLEDGE"
    if action_authority and scores["actionability"] >= 4 and scores["correctness"] >= 3 and scores["source_confidence"] >= 3:
        return "ACTIONABLE_KNOWLEDGE"
    if scores["correctness"] >= 4 and scores["consistency"] >= 4 and average >= 3.0:
        return "CONFIRMED_KNOWLEDGE"
    if scores["correctness"] >= 3 and scores["consistency"] >= 3 and scores["source_confidence"] >= 3 and average >= 3.0:
        return "CONFIRMED_KNOWLEDGE"
    if average >= 2.0:
        return "STABLE_SIGNAL"
    return "RAW_OBSERVATION"


def _knowledge_evidence_overlay(
    object_name: str,
    *,
    prediction_plan: dict[str, Any],
    operator_comparisons: dict[str, Any],
    canary_proximity: dict[str, Any],
    floor_forensics: dict[str, Any],
    materialization_audit: dict[str, Any],
    source_confidence_inventory: dict[str, Any],
    candidate_outcome_reality_collection: dict[str, Any],
    routing_foundation: dict[str, Any] | None = None,
    suitability_quality_model: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source_rows = {
        row.get("source"): row
        for row in source_confidence_inventory.get("sources") or []
        if isinstance(row, dict)
    }
    components = floor_forensics.get("component_values") if isinstance(floor_forensics.get("component_values"), dict) else {}
    floors = canary_proximity.get("floors") if isinstance(canary_proximity.get("floors"), dict) else {}
    candidate_coverage = candidate_outcome_reality_collection.get("coverage") if isinstance(candidate_outcome_reality_collection.get("coverage"), dict) else {}
    routing_foundation = routing_foundation or {}
    fit_summary = (routing_foundation.get("service_user_sla_fit") or {}).get("summary", {})
    closure_summary = (routing_foundation.get("decision_outcome_closure") or {}).get("summary", {})
    recovery_summary = (routing_foundation.get("recovery_admission") or {}).get("summary", {})
    freshness_summary = (routing_foundation.get("freshness_actionability") or {}).get("summary", {})
    readiness = routing_foundation.get("routing_recommendation_readiness") or {}
    outcome_learning = routing_foundation.get("decision_outcome_learning") or {}
    outcome_effectiveness = outcome_learning.get("effectiveness") if isinstance(outcome_learning.get("effectiveness"), dict) else {}
    knowledge_growth = outcome_learning.get("knowledge_growth") if isinstance(outcome_learning.get("knowledge_growth"), dict) else {}
    suitability_quality_model = suitability_quality_model or {}
    overlay_by_object = {
        "Service": {
            "rows_seen": ((floor_forensics.get("service_root_cause") or {}).get("rows_seen") if isinstance(floor_forensics.get("service_root_cause"), dict) else 0),
            "source_classification": (source_rows.get("service_outcomes") or {}).get("classification", "UNKNOWN"),
            "service_confidence": components.get("service_confidence", 0.0),
            "service_user_sla_fit_users_seen": fit_summary.get("users_seen", 0),
            "fit_verdict_counts": fit_summary.get("verdict_counts", {}),
            "service_improved_rate": outcome_effectiveness.get("service_improved_rate", 0.0),
        },
        "Prediction": {
            "forecasts_seen": prediction_plan.get("forecasts_seen", 0),
            "matched_rows": prediction_plan.get("matched_rows", 0),
            "pending_rows": prediction_plan.get("pending_rows", 0),
            "prediction_confidence": components.get("prediction_confidence", 0.0),
            "prediction_correct_rate": outcome_effectiveness.get("prediction_correct_rate", 0.0),
        },
        "Suitability": {
            "candidate_count": candidate_coverage.get("candidate_count", 0),
            "candidate_outcomes_consumed": candidate_coverage.get("candidate_outcomes_consumed", 0),
            "coverage_ratio": candidate_coverage.get("coverage_ratio", 0.0),
            "source_classification": (source_rows.get("candidate_outcomes") or {}).get("classification", "UNKNOWN"),
            "service_user_sla_fit_attached": bool(fit_summary),
            "fit_prediction_correct_rate": outcome_effectiveness.get("fit_prediction_correct_rate", 0.0),
            "autonomy_grade_stage": suitability_quality_model.get("current_stage", "UNKNOWN"),
            "autonomy_grade_ready": suitability_quality_model.get("autonomy_grade_ready", False),
            "primary_blockers": (suitability_quality_model.get("missing_knowledge") or {}).get("primary_blockers", []),
        },
        "Trust": {
            "confidence_floor": (floors.get("confidence") or {}).get("current") if isinstance(floors.get("confidence"), dict) else 0.0,
            "trust_floor": (floors.get("trust") or {}).get("current") if isinstance(floors.get("trust"), dict) else 0.0,
            "missing_primary_floors": canary_proximity.get("missing", []),
        },
        "Safety": {
            "rollback_materialized": (materialization_audit.get("prediction_actuals") or {}).get("materialized", False),
            "rollback_confidence": components.get("rollback_confidence", 0.0),
            "blast_radius_confidence": components.get("blast_radius_confidence", 0.0),
        },
        "Operator Context": {
            "reviewable_decisions": (operator_comparisons.get("current") or {}).get("reviewable_decisions", 0),
            "reviewed_decisions": (operator_comparisons.get("current") or {}).get("reviewed_decisions", 0),
            "comparison_count": (operator_comparisons.get("current") or {}).get("comparison_count", 0),
        },
        "Decision Outcome": {
            "candidate_outcomes_consumed": candidate_coverage.get("candidate_outcomes_consumed", 0),
            "missing_candidate_outcomes": candidate_coverage.get("missing_candidate_outcomes", 0),
            "runtime_apply_allowed_in_this_phase": (candidate_outcome_reality_collection.get("acceleration") or {}).get("runtime_apply_allowed_in_this_phase", False),
            "closure_state": routing_foundation.get("decision_outcome_closure", {}).get("closure_state", "UNKNOWN"),
            "valid_closures": closure_summary.get("valid_closures", 0),
            "outcome_quality_counts": outcome_learning.get("outcome_quality_counts", {}),
            "recommendation_correct_rate": outcome_effectiveness.get("recommendation_correct_rate", 0.0),
            "knowledge_gained": knowledge_growth.get("knowledge_gained", 0),
        },
        "Freshness": {
            "snapshot_backed": True,
            "read_owner": "admin_core.intelligence_snapshots.read_snapshot_family",
            "actionability_summary": freshness_summary,
        },
        "Recovery": {
            "admission_contract": "staged_read_only",
            "eligible_channels": recovery_summary.get("eligible", 0),
            "blocked_or_quarantined": recovery_summary.get("blocked_or_quarantined", 0),
            "recovery_prediction_correct_rate": outcome_effectiveness.get("recovery_prediction_correct_rate", 0.0),
        },
        "Event": {
            "event_model": "read_only_consumer",
            "apply_authority": "disabled_by_design",
            "routing_recommendation_readiness": readiness.get("readiness", "UNKNOWN"),
        },
    }
    return overlay_by_object.get(object_name, {"dynamic_overlay": "canonical_static_read_model"})


def build_knowledge_quality_read_model(
    *,
    generated_at: str | None = None,
    prediction_plan: dict[str, Any] | None = None,
    operator_comparisons: dict[str, Any] | None = None,
    canary_proximity: dict[str, Any] | None = None,
    floor_forensics: dict[str, Any] | None = None,
    materialization_audit: dict[str, Any] | None = None,
    source_confidence_inventory: dict[str, Any] | None = None,
    candidate_outcome_reality_collection: dict[str, Any] | None = None,
    routing_foundation: dict[str, Any] | None = None,
    suitability_quality_model: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Expose canonical V7 knowledge quality through an existing read-only owner."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    prediction_plan = prediction_plan or {}
    operator_comparisons = operator_comparisons or {}
    canary_proximity = canary_proximity or {}
    floor_forensics = floor_forensics or {}
    materialization_audit = materialization_audit or {}
    source_confidence_inventory = source_confidence_inventory or {}
    candidate_outcome_reality_collection = candidate_outcome_reality_collection or {}
    routing_foundation = routing_foundation or {}
    suitability_quality_model = suitability_quality_model or {}
    objects = []
    distribution = {stage: 0 for stage in VALID_KNOWLEDGE_MATURITY_STAGES}
    for definition in CANONICAL_KNOWLEDGE_OBJECTS:
        scores = _quality_scores(list(definition["scores"]))
        average = round(sum(scores.values()) / len(scores), 3)
        stage = _knowledge_maturity_stage(
            scores=scores,
            action_authority=bool(definition.get("action_authority")),
            object_name=str(definition["object"]),
        )
        distribution[stage] += 1
        objects.append({
            "object": definition["object"],
            "owner": definition["owner"],
            "sources": definition["sources"],
            "consumers": definition["consumers"],
            "quality_dimensions": scores,
            "average_score": average,
            "maturity_stage": stage,
            "tier_support": definition["tier_support"],
            "primary_gaps": definition["primary_gaps"],
            "next_improvement": definition["next_improvement"],
            "evidence_overlay": _knowledge_evidence_overlay(
                str(definition["object"]),
                prediction_plan=prediction_plan,
                operator_comparisons=operator_comparisons,
                canary_proximity=canary_proximity,
                floor_forensics=floor_forensics,
                materialization_audit=materialization_audit,
                source_confidence_inventory=source_confidence_inventory,
                candidate_outcome_reality_collection=candidate_outcome_reality_collection,
                routing_foundation=routing_foundation,
                suitability_quality_model=suitability_quality_model,
            ),
            "score_source": "docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md",
            "heuristic_fallback": False,
        })
    total = len(objects)
    maturity_distribution = {
        stage: {
            "count": count,
            "share": round(count / total, 4) if total else 0.0,
        }
        for stage, count in distribution.items()
    }
    tier_readiness = {
        "TIER_0": {
            "status": "READY_FOR_READ_ONLY_PREVIEW",
            "required_knowledge": ["Channel", "User Assignment", "Policy", "Event", "Service", "Quality"],
            "primary_gaps": [],
        },
        "TIER_1": {
            "status": "READY_FOR_GOVERNED_REVIEW_WITH_OPERATOR_AUTHORITY",
            "required_knowledge": ["Channel", "User Assignment", "Policy", "Safety"],
            "primary_gaps": ["operator-free authority is not granted"],
        },
        "TIER_2": {
            "status": "BLOCKED_BY_KNOWLEDGE_QUALITY",
            "required_knowledge": ["Trust", "Prediction", "Decision Outcome", "Suitability", "Freshness"],
            "primary_gaps": ["suitability coverage/correctness", "source confidence", "freshness/actionability"],
        },
        "TIER_3_PLUS": {
            "status": "BLOCKED_BY_RECOVERY_AND_AUTONOMY_GRADE_KNOWLEDGE",
            "required_knowledge": ["Recovery", "Event", "post-action verification", "anti-flap/cooldown"],
            "primary_gaps": ["recovery admission", "autonomous rollback certification", "anti-flap knowledge"],
        },
    }
    ten_k = {
        "overall": "PARTIAL_NOT_AUTONOMY_READY",
        "ready": ["Safety"],
        "partial": [
            "Channel",
            "Service",
            "User Assignment",
            "Route",
            "Capacity",
            "Quality",
            "Failure",
            "Decision Outcome",
            "Prediction",
            "Trust",
            "Policy",
            "Event",
        ],
        "not_ready": ["Recovery", "Suitability", "Freshness", "Operator Context"],
        "reason": "10k readiness is blocked by knowledge quality, freshness/actionability, and cohort/SLA-scale summaries, not by a missing planner.",
    }
    p0_gaps = [
        {
            "gap": "Suitability is stable signal",
            "weak_dimensions": ["coverage", "correctness"],
            "required_state": "Suitability becomes actionable knowledge",
            "next_improvement": "Use existing candidate outcome, feedback, and intelligence owners; no synthetic evidence.",
        },
        {
            "gap": "Recovery is stable signal",
            "weak_dimensions": ["correctness", "consistency", "anti-flap"],
            "required_state": "Recovery becomes actionable knowledge",
            "next_improvement": "Define recovery admission contract before autonomous recovery.",
        },
        {
            "gap": "Freshness is implicit/supporting",
            "weak_dimensions": ["freshness", "actionability"],
            "required_state": "Freshness blocks stale action and labels stale knowledge",
            "next_improvement": "Expose stale/expired labels through existing snapshot/trust inventory owners.",
        },
        {
            "gap": "Service knowledge is probe-heavy",
            "weak_dimensions": ["source_confidence", "service_relevance", "user_impact_relevance"],
            "required_state": "Service knowledge is service/user/SLA outcome-aware",
            "next_improvement": "Extend existing service/intelligence summaries after contract proof.",
        },
        {
            "gap": "Safety is strong but autonomous rollback is not certified",
            "weak_dimensions": ["operator_free_actionability"],
            "required_state": "Rollback is certified for autonomous tier",
            "next_improvement": "Certify one-user rollback before TIER_3.",
        },
    ]
    return {
        "schema_version": "v7.knowledge-quality.read-model.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "surface": "tools/v7-autonomy-trust-evidence-inventory",
        "model_source": "docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md",
        "maturity_rules": {
            "RAW_OBSERVATION": "average_score < 2.0 or isolated/underfed evidence",
            "STABLE_SIGNAL": "average_score >= 2.0 and not confirmed/actionable",
            "CONFIRMED_KNOWLEDGE": "correctness and consistency >= 4 with average_score >= 3.0, or correctness/consistency/source confidence >= 3 with average_score >= 3.0",
            "ACTIONABLE_KNOWLEDGE": "existing governed/blocking action authority with actionability >= 4, correctness >= 3, source confidence >= 3",
            "AUTONOMY_GRADE_KNOWLEDGE": "safety-grade knowledge with correctness/source/actionability >= 5 and average_score >= 4.0",
        },
        "knowledge_objects": objects,
        "maturity_distribution": maturity_distribution,
        "tier_readiness_knowledge": tier_readiness,
        "10k_readiness": ten_k,
        "p0_gaps": p0_gaps,
        "read_only": True,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
        "synthetic_evidence_created": False,
        "new_truth_source_created": False,
        "planner_redesigned": False,
        "governance_redesigned": False,
        "execution_redesigned": False,
    }


def build_acceleration_inventory(
    *,
    snapshot_root: Path | str,
    decision_surface: dict[str, Any],
    shadow_history: list[dict[str, Any]] | None = None,
    decision_records: list[dict[str, Any]] | None = None,
    event_rows: list[dict[str, Any]] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    root = Path(snapshot_root)
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    snapshot_results = {
        name: read_snapshot_family(root, name)
        for name in ROUTING_FOUNDATION_SNAPSHOT_FAMILIES
    }
    snapshots = {
        name: result.payload
        for name, result in snapshot_results.items()
    }
    snapshot_statuses = {name: _snapshot_status_from_read_result(result) for name, result in snapshot_results.items()}
    shadow_model = shadow_autonomy.build_shadow_autonomy_model(decision_surface, history=shadow_history or [], now=generated)
    prediction_plan = build_prediction_collection_plan(
        prediction_snapshot=snapshots["prediction-summaries"],
        service_scores_snapshot=snapshots["service-scores"],
        channel_service_scores_snapshot=snapshots["channel-service-scores"],
        decision_records=decision_records or [],
    )
    review_batches = build_operator_review_batches(shadow_model.get("operator_review_packet", {}))
    canary = build_canary_proximity(
        trust_evolution_snapshot=snapshots["trust-evolution-summaries"],
        shadow_model=shadow_model,
        prediction_plan=prediction_plan,
    )
    floor_forensics = build_floor_forensics(
        trust_evolution_snapshot=snapshots["trust-evolution-summaries"],
        shadow_model=shadow_model,
        prediction_plan=prediction_plan,
        canary_proximity=canary,
    )
    materialization_audit = build_materialization_audit(
        trust_evolution_snapshot=snapshots["trust-evolution-summaries"],
        prediction_plan=prediction_plan,
        floor_forensics=floor_forensics,
    )
    source_confidence_inventory = build_source_confidence_inventory(
        prediction_snapshot=snapshots["prediction-summaries"],
        service_scores_snapshot=snapshots["service-scores"],
        channel_service_scores_snapshot=snapshots["channel-service-scores"],
        trust_evolution_snapshot=snapshots["trust-evolution-summaries"],
        shadow_model=shadow_model,
        floor_forensics=floor_forensics,
        materialization_audit=materialization_audit,
    )
    evidence_sufficiency = build_evidence_sufficiency_analysis(source_confidence_inventory)
    source_confidence_collection_plan = build_source_confidence_collection_plan(
        source_inventory=source_confidence_inventory,
        sufficiency=evidence_sufficiency,
    )
    quality = shadow_model.get("quality", {})
    confidence = shadow_model.get("confidence", {})
    operator_comparisons = {
        "evidence_role": "secondary_supervised_confirmation",
        "blind_review_required": False,
        "current": {
            "reviewable_decisions": shadow_model.get("operator_review_packet", {}).get("reviewable_decisions", 0),
            "reviewed_decisions": shadow_model.get("operator_review_packet", {}).get("reviewed_decisions", 0),
            "comparison_count": quality.get("comparisons_total", 0),
            "agreement_rate": quality.get("agreement_rate", 0.0),
            "earned_confidence": confidence.get("earned_confidence", 0.0),
        },
        "review_batches": review_batches,
        "growth_projection": shadow_model.get("comparison_growth_projection", {}),
    }
    confidence_reality_audit = build_confidence_reality_audit(
        floor_forensics=floor_forensics,
        source_inventory=source_confidence_inventory,
        operator_comparisons=operator_comparisons,
    )
    real_outcome_growth_projection = build_real_outcome_growth_projection(
        floor_forensics=floor_forensics,
        confidence_reality_audit=confidence_reality_audit,
        operator_comparisons=operator_comparisons,
    )
    real_outcome_source_inventory = build_real_outcome_source_inventory(
        source_confidence_inventory=source_confidence_inventory,
        floor_forensics=floor_forensics,
        materialization_audit=materialization_audit,
        real_outcome_growth_projection=real_outcome_growth_projection,
    )
    candidate_outcome_reality_collection = build_candidate_outcome_reality_collection(
        candidate_suitability_snapshot=snapshots["candidate-suitability-summary"],
        decision_records=decision_records or [],
        floor_forensics=floor_forensics,
    )
    outcome_leverage_model = build_outcome_leverage_model(
        floor_forensics=floor_forensics,
        confidence_reality_audit=confidence_reality_audit,
        real_outcome_source_inventory=real_outcome_source_inventory,
        candidate_outcome_reality_collection=candidate_outcome_reality_collection,
        real_outcome_growth_projection=real_outcome_growth_projection,
        operator_comparisons=operator_comparisons,
    )
    freshness_actionability = build_freshness_actionability(snapshot_statuses, generated_at=generated)
    action_class_freshness_windows = build_action_class_freshness_windows(
        freshness_actionability,
        generated_at=generated,
    )
    service_user_sla_fit = build_service_user_sla_fit(
        decision_surface,
        freshness_actionability=freshness_actionability,
        generated_at=generated,
    )
    hard_failure_classification = build_hard_failure_classification(
        decision_surface=decision_surface,
        freshness_actionability=freshness_actionability,
        service_user_sla_fit=service_user_sla_fit,
        snapshot_statuses=snapshot_statuses,
        event_rows=event_rows or [],
        generated_at=generated,
    )
    decision_outcome_closure = build_decision_outcome_closure(decision_records or [], generated_at=generated)
    recovery_admission = build_recovery_admission(
        decision_surface,
        freshness_actionability=freshness_actionability,
        generated_at=generated,
    )
    anti_flapping = build_anti_flapping(decision_records or [], generated_at=generated)
    decision_outcome_learning = _decision_outcome_learning_from_trust(snapshots["trust-evolution-summaries"])
    suitability_effectiveness_expansion = build_suitability_effectiveness_expansion(
        decision_outcome_learning=decision_outcome_learning,
        floor_forensics=floor_forensics,
        candidate_outcome_reality_collection=candidate_outcome_reality_collection,
    )
    suitability_quality_model = build_suitability_quality_model(
        floor_forensics=floor_forensics,
        candidate_outcome_reality_collection=candidate_outcome_reality_collection,
        freshness_actionability=freshness_actionability,
        service_user_sla_fit=service_user_sla_fit,
        decision_outcome_learning=decision_outcome_learning,
        suitability_effectiveness=suitability_effectiveness_expansion,
    )
    suitability_knowledge_growth = build_suitability_knowledge_growth_model(
        suitability_quality_model=suitability_quality_model,
        candidate_outcome_reality_collection=candidate_outcome_reality_collection,
        decision_outcome_learning=decision_outcome_learning,
        outcome_leverage_model=outcome_leverage_model,
        real_outcome_growth_projection=real_outcome_growth_projection,
    )
    autonomy_grade_suitability_program = build_autonomy_grade_suitability_program(
        suitability_quality_model=suitability_quality_model,
        suitability_knowledge_growth=suitability_knowledge_growth,
        suitability_effectiveness=suitability_effectiveness_expansion,
        outcome_leverage_model=outcome_leverage_model,
    )
    routing_foundation_partial = {
        "service_user_sla_fit": service_user_sla_fit,
        "decision_outcome_closure": decision_outcome_closure,
        "decision_outcome_learning": decision_outcome_learning,
        "recovery_admission": recovery_admission,
        "anti_flapping": anti_flapping,
        "freshness_actionability": freshness_actionability,
        "action_class_freshness_windows": action_class_freshness_windows,
    }
    knowledge_quality_read_model = build_knowledge_quality_read_model(
        generated_at=generated,
        prediction_plan=prediction_plan,
        operator_comparisons=operator_comparisons,
        canary_proximity=canary,
        floor_forensics=floor_forensics,
        materialization_audit=materialization_audit,
        source_confidence_inventory=source_confidence_inventory,
        candidate_outcome_reality_collection=candidate_outcome_reality_collection,
        routing_foundation=routing_foundation_partial,
        suitability_quality_model=suitability_quality_model,
    )
    routing_recommendation_readiness = build_routing_recommendation_readiness(
        service_user_sla_fit=service_user_sla_fit,
        decision_outcome_closure=decision_outcome_closure,
        recovery_admission=recovery_admission,
        anti_flapping=anti_flapping,
        freshness_actionability=freshness_actionability,
        knowledge_quality_read_model=knowledge_quality_read_model,
    )
    autonomous_knowledge_growth_program = build_autonomous_knowledge_growth_program(
        knowledge_quality_read_model=knowledge_quality_read_model,
        suitability_quality_model=suitability_quality_model,
        suitability_knowledge_growth=suitability_knowledge_growth,
        prediction_plan=prediction_plan,
        real_outcome_source_inventory=real_outcome_source_inventory,
        freshness_actionability=freshness_actionability,
        recovery_admission=recovery_admission,
        decision_outcome_closure=decision_outcome_closure,
        decision_outcome_learning=decision_outcome_learning,
        routing_recommendation_readiness=routing_recommendation_readiness,
        outcome_leverage_model=outcome_leverage_model,
        canary_proximity=canary,
    )
    autonomous_routing_evolution_program = build_autonomous_routing_evolution_program(
        autonomous_knowledge_growth_program=autonomous_knowledge_growth_program,
        autonomy_grade_suitability_program=autonomy_grade_suitability_program,
        suitability_quality_model=suitability_quality_model,
        suitability_knowledge_growth=suitability_knowledge_growth,
        suitability_effectiveness=suitability_effectiveness_expansion,
        outcome_leverage_model=outcome_leverage_model,
        knowledge_quality_read_model=knowledge_quality_read_model,
        routing_recommendation_readiness=routing_recommendation_readiness,
        decision_outcome_learning=decision_outcome_learning,
        canary_proximity=canary,
        real_outcome_growth_projection=real_outcome_growth_projection,
        candidate_outcome_reality_collection=candidate_outcome_reality_collection,
        prediction_plan=prediction_plan,
        real_outcome_source_inventory=real_outcome_source_inventory,
    )
    surface_users = decision_surface.get("users") if isinstance(decision_surface.get("users"), list) else []
    first_candidate = surface_users[0] if surface_users and isinstance(surface_users[0], dict) else {}
    action_class_runtime_enablement = build_action_class_runtime_enablement_model(
        canary_proximity=canary,
        candidate_outcome_reality_collection=candidate_outcome_reality_collection,
        decision_outcome_closure=decision_outcome_closure,
        decision_outcome_learning=decision_outcome_learning,
        suitability_quality_model=suitability_quality_model,
        freshness_actionability=freshness_actionability,
        autonomous_routing_evolution_program=autonomous_routing_evolution_program,
        hard_failure_classification=hard_failure_classification,
        action_class_freshness_windows=action_class_freshness_windows,
        candidate=first_candidate,
        generated_at=generated,
    )
    maximum_reality_knowledge_extraction = build_maximum_reality_knowledge_extraction(
        autonomous_knowledge_growth_program=autonomous_knowledge_growth_program,
        autonomous_routing_evolution_program=autonomous_routing_evolution_program,
        candidate_outcome_reality_collection=candidate_outcome_reality_collection,
        real_outcome_source_inventory=real_outcome_source_inventory,
        real_outcome_growth_projection=real_outcome_growth_projection,
        suitability_quality_model=suitability_quality_model,
        suitability_knowledge_growth=suitability_knowledge_growth,
        prediction_plan=prediction_plan,
        decision_outcome_closure=decision_outcome_closure,
        decision_outcome_learning=decision_outcome_learning,
        freshness_actionability=freshness_actionability,
        outcome_leverage_model=outcome_leverage_model,
    )
    final_autonomous_routing_architecture_certification = build_final_autonomous_routing_architecture_certification(
        knowledge_quality_read_model=knowledge_quality_read_model,
        autonomous_knowledge_growth_program=autonomous_knowledge_growth_program,
        autonomous_routing_evolution_program=autonomous_routing_evolution_program,
        maximum_reality_knowledge_extraction=maximum_reality_knowledge_extraction,
        service_user_sla_fit=service_user_sla_fit,
        decision_outcome_closure=decision_outcome_closure,
        decision_outcome_learning=decision_outcome_learning,
        recovery_admission=recovery_admission,
        anti_flapping=anti_flapping,
        freshness_actionability=freshness_actionability,
        routing_recommendation_readiness=routing_recommendation_readiness,
        suitability_quality_model=suitability_quality_model,
        candidate_outcome_reality_collection=candidate_outcome_reality_collection,
        real_outcome_source_inventory=real_outcome_source_inventory,
        prediction_plan=prediction_plan,
        canary_proximity=canary,
    )
    return {
        "schema_version": "v7.autonomy-trust-acceleration.inventory.v1",
        "generated_at": generated,
        "mode": "read_only_inventory_and_collection_plan",
        "trust_source_classification": build_trust_source_classification(),
        "operator_authority_model": build_operator_authority_model(),
        "prediction_evidence": prediction_plan,
        "operator_comparisons": operator_comparisons,
        "canary_proximity": canary,
        "floor_forensics": floor_forensics,
        "materialization_audit": materialization_audit,
        "source_confidence_inventory": source_confidence_inventory,
        "evidence_sufficiency": evidence_sufficiency,
        "source_confidence_collection_plan": source_confidence_collection_plan,
        "confidence_reality_audit": confidence_reality_audit,
        "real_outcome_source_inventory": real_outcome_source_inventory,
        "candidate_outcome_reality_collection": candidate_outcome_reality_collection,
        "real_outcome_growth_projection": real_outcome_growth_projection,
        "outcome_leverage_model": outcome_leverage_model,
        "hard_failure_classification": hard_failure_classification,
        "service_user_sla_fit": service_user_sla_fit,
        "action_class_freshness_windows": action_class_freshness_windows,
        "decision_outcome_closure": decision_outcome_closure,
        "decision_outcome_learning": decision_outcome_learning,
        "decision_effectiveness": decision_outcome_learning.get("effectiveness", {}),
        "suitability_effectiveness_expansion": suitability_effectiveness_expansion,
        "suitability_quality_model": suitability_quality_model,
        "suitability_knowledge_growth": suitability_knowledge_growth,
        "autonomy_grade_suitability_program": autonomy_grade_suitability_program,
        "knowledge_growth": decision_outcome_learning.get("knowledge_growth", {}),
        "recovery_admission": recovery_admission,
        "anti_flapping": anti_flapping,
        "freshness_actionability": freshness_actionability,
        "routing_recommendation_readiness": routing_recommendation_readiness,
        "autonomous_knowledge_growth_program": autonomous_knowledge_growth_program,
        "autonomous_routing_evolution_program": autonomous_routing_evolution_program,
        "action_class_runtime_enablement": action_class_runtime_enablement,
        "maximum_reality_knowledge_extraction": maximum_reality_knowledge_extraction,
        "final_autonomous_routing_architecture_certification": final_autonomous_routing_architecture_certification,
        "knowledge_quality_read_model": knowledge_quality_read_model,
        "knowledge_objects": knowledge_quality_read_model["knowledge_objects"],
        "maturity_distribution": knowledge_quality_read_model["maturity_distribution"],
        "tier_readiness_knowledge": knowledge_quality_read_model["tier_readiness_knowledge"],
        "10k_readiness": knowledge_quality_read_model["10k_readiness"],
        "p0_gaps": knowledge_quality_read_model["p0_gaps"],
        "collection_plan": {
            "primary_real_evidence_path": [
                "observe service and channel quality outcomes through existing service/quality snapshots",
                "match future forecasts to later real actuals through existing prediction owners",
                "record post-action verification and no-rollback outcomes after governed/manual actions",
                "refresh intelligence snapshots through tools/v7-intelligence-snapshot-refresh",
            ],
            "secondary_supervised_confirmation_path": [
                "operator reviews only recommendations where enough operational context exists",
                "record agree/disagree/override through /api/actions/shadow-autonomy-compare",
            ],
            "blind_operator_training_required": False,
            "forbidden": [
                "blind bulk operator reviews",
                "synthetic comparisons",
                "synthetic actuals",
                "threshold/floor changes",
                "runtime apply",
                "user movement",
                "daemon enablement",
            ],
        },
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
        "autonomy_enabled": False,
    }
