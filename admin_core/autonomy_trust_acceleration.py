"""Read-only autonomy trust evidence acceleration helpers.

This module does not create evidence, change formulas, or mutate runtime state.
It inventories already-existing forecast, actual, shadow comparison, and trust
evidence so operators know which real evidence to collect next.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from admin_core import intelligence_platform, intelligence_workers, shadow_autonomy
from admin_core.intelligence_snapshots import read_snapshot_family
from admin_core.operator_execution_pipeline import (
    AUTONOMY_CANARY_CONFIDENCE_FLOOR,
    AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR,
    AUTONOMY_CANARY_TRUST_FLOOR,
)


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
    return {
        "schema_version": "v7.autonomy-trust.canary-proximity.v1",
        "autonomy_canary_1_ready": False,
        "readiness_model": "observed_outcome_primary_operator_comparison_secondary",
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
            "exact_outcome_deficit_blocks_canary": missing_count,
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


def build_acceleration_inventory(
    *,
    snapshot_root: Path | str,
    decision_surface: dict[str, Any],
    shadow_history: list[dict[str, Any]] | None = None,
    decision_records: list[dict[str, Any]] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    root = Path(snapshot_root)
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    snapshots = {
        name: read_snapshot_family(root, name).payload
        for name in [
            "prediction-summaries",
            "service-scores",
            "channel-service-scores",
            "candidate-suitability-summary",
            "trust-evolution-summaries",
        ]
    }
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
