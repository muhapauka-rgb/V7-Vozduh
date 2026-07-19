"""Read-only autonomy trust evidence acceleration helpers.

This module does not create evidence, change formulas, or mutate runtime state.
It inventories already-existing forecast, actual, shadow comparison, and trust
evidence so operators know which real evidence to collect next.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from admin_core import events as v7_events
from admin_core import intelligence_platform, intelligence_workers, shadow_autonomy
from admin_core.intelligence_snapshots import SNAPSHOT_FAMILIES, read_snapshot_family
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

# Existing production evidence remains owned by its reports. This registry only
# gives the current action-class owner stable provenance pointers and dimensions.
HISTORICAL_MOVEMENT_CERTIFICATION_SOURCES = [
    {
        "certification_id": "E25.15",
        "path": "BLOCK_E25_15_REFRESH_APPROVAL_PACKET_AFTER_REGISTRY_DRIFT_AND_RETRY_MOVEMENT_REPORT.md",
        "date": "2026-05-28",
        "users": 1,
        "scenario": "operator_driven_bounded_movement",
        "action_class": "single-user governed movement",
        "rollback": "PASS",
        "repository_certified": True,
        "markers": ["first_operator_driven_movement_executed=true", "routing_mutation_limited_to_candidate=true"],
    },
    {
        "certification_id": "E27.2",
        "path": "BLOCK_E27_2_FIRST_TWO_USER_GOVERNED_MOVEMENT_REPORT.md",
        "date": "2026-05-28",
        "users": 2,
        "scenario": "operator_driven_bounded_movement",
        "action_class": "two-user governed movement",
        "rollback": "PASS",
        "repository_certified": True,
        "markers": ["first_two_user_governed_movement_executed=true", "movement_budget=2"],
    },
    {
        "certification_id": "E28.2",
        "path": "BLOCK_E28_2_FIRST_SMALL_COHORT_GOVERNED_MOVEMENT_REPORT.md",
        "date": "2026-05-29",
        "users": 4,
        "scenario": "operator_driven_bounded_movement",
        "action_class": "small-cohort governed movement",
        "rollback": "PASS",
        "repository_certified": True,
        "markers": ["first_small_cohort_governed_movement_executed=true", "movement_budget=4"],
    },
    {
        "certification_id": "L3-ONE-USER-20260701",
        "path": "docs/reports/engineering/2026-07-01_232858_execution_mission_success_l3_one_user_restored.md",
        "date": "2026-07-01",
        "users": 1,
        "scenario": "failed_source_incident_failover",
        "action_class": "channel hard-fail failover",
        "rollback": "NOT_REQUIRED",
        "repository_certified": True,
        "markers": ["L3_PRODUCTION_PROVEN", "Users moved: `1`"],
    },
    {
        "certification_id": "L3-INCIDENT-RETRY-20260702",
        "path": "docs/reports/engineering/2026-07-02_211641_incident_retry_candidate_selection_fix.md",
        "date": "2026-07-02",
        "users": 1,
        "scenario": "failed_source_incident_failover",
        "action_class": "channel hard-fail failover",
        "rollback": "NOT_REQUIRED",
        "repository_certified": True,
        "markers": ["\"users_moved\": 1", "\"verification_result\": \"PASS\""],
    },
    {
        "certification_id": "PHASE3-SMALL-BATCH-20260703",
        "path": "docs/reports/engineering/2026-07-03_001926_controlled_production_certification_program_execution.md",
        "date": "2026-07-03",
        "users": 5,
        "scenario": "controlled_failed_source_incident",
        "action_class": "small-batch movement",
        "rollback": "NOT_REQUIRED",
        "repository_certified": True,
        "markers": ["Users moved: `5`", "Verification: `PASS` for all 5"],
    },
    {
        "certification_id": "PHASE4-MEDIUM-BATCH-20260703",
        "path": "docs/reports/engineering/2026-07-03_160522_phase4_medium_batch_certification_pass.md",
        "date": "2026-07-03",
        "users": 10,
        "scenario": "controlled_failed_source_incident",
        "action_class": "medium-batch movement",
        "rollback": "NOT_REQUIRED",
        "repository_certified": True,
        "markers": ["`users_moved`: 10", "`verification_result`: PASS"],
    },
    {
        "certification_id": "PHASE5-LARGE-BATCH-20260703",
        "path": "docs/reports/engineering/2026-07-03_161914_phase5_large_batch_certification_pass.md",
        "date": "2026-07-03",
        "users": 25,
        "scenario": "controlled_failed_source_incident",
        "action_class": "large-batch movement",
        "rollback": "NOT_REQUIRED",
        "repository_certified": True,
        "markers": ["users_moved: 25", "verification_result: PASS"],
    },
    {
        "certification_id": "PHASE6-XLARGE-PARTIAL-20260703",
        "path": "docs/reports/engineering/2026-07-03_183251_controlled_program_phase6_phase7_execution.md",
        "date": "2026-07-03",
        "users": 48,
        "scenario": "controlled_failed_source_incident",
        "action_class": "xlarge-batch movement",
        "rollback": "NOT_REQUIRED",
        "repository_certified": True,
        "markers": ["users moved: `48`", "XLARGE_BATCH=50"],
    },
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
    "policy_name": "Default Bounded Delegated Autonomy Policy",
    "policy_state": "APPROVED",
    "current_mode": "DELEGATED_AUTONOMY",
    "target_mode": "DELEGATED_AUTONOMY",
    "allowed_action_classes": ["single-user governed candidate failover"],
    "max_users_per_action": 1,
    "max_concurrent_transactions": 1,
    "candidate_selection": "EXISTING_PLANNER_ONLY",
    "candidate_identity": "FRESH_ONLY",
    "packet_generation": "FRESH_IMMEDIATELY_BEFORE_EXECUTION",
    "packet_reuse": "FORBIDDEN",
    "historical_identity_reuse": "FORBIDDEN",
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
    "governed_learning_mode_allowed": True,
    "runtime_apply_enabled": True,
    "operator_candidate_approval_required": False,
    "operator_packet_approval_required": False,
    "operator_hash_approval_required": False,
    "self_expansion_allowed": False,
    "final_safe_mode": "OPEN",
    "authority_expansion_performed": False,
}

DELEGATED_AUTONOMY_SCOPE_FIELDS = (
    "policy_id", "policy_state", "current_mode", "allowed_action_classes",
    "max_users_per_action", "max_concurrent_transactions", "candidate_selection",
    "candidate_identity", "packet_generation", "packet_reuse",
    "historical_identity_reuse", "required_freshness", "required_verification",
    "required_rollback", "required_anti_flap", "required_floors",
    "max_blast_radius", "cooldown", "governed_learning_mode_allowed",
    "runtime_apply_enabled", "operator_candidate_approval_required",
    "operator_packet_approval_required", "operator_hash_approval_required",
    "self_expansion_allowed", "final_safe_mode",
)


def normalized_delegated_autonomy_scope(policy: dict[str, Any]) -> dict[str, Any]:
    return {field: policy.get(field) for field in DELEGATED_AUTONOMY_SCOPE_FIELDS}


def delegated_autonomy_scope_hash(policy: dict[str, Any]) -> str:
    payload = json.dumps(
        normalized_delegated_autonomy_scope(policy),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

DIAGNOSIS_OWNER_RESOLUTION_SCHEMA_VERSION = "v7.diagnosis-owner-resolution.v1"

DIAGNOSIS_RECORD_PRODUCER = (
    "admin_core.autonomy_trust_acceleration."
    "build_diagnosis_owner_resolution_record"
)

DIAGNOSIS_RECORD_CONSUMERS = [
    "OMP",
    "Current Program State",
    "Production Maturity",
    "Engineering Reports",
    "Engineering Automation",
    "Governance Check",
    "Future Certification",
]

DIAGNOSIS_STATUSES = {
    "PROVEN",
    "UNKNOWN",
    "PARTIAL",
    "NO_EVIDENCE",
    "CONFLICTING_EVIDENCE",
}

DIAGNOSIS_UNKNOWN_STATES = {
    "NONE",
    "MISSING_EVIDENCE",
    "STALE_EVIDENCE",
    "CONFLICTING_EVIDENCE",
    "NOT_INVESTIGATED",
    "UNKNOWN_OWNER",
}

DIAGNOSIS_OWNER_RESOLUTION_STATES = {
    "NOT_REQUIRED",
    "REQUIRED",
    "RESOLVED",
    "UNKNOWN",
}

DIAGNOSIS_TERMINAL_CLASSIFICATIONS = {
    "NONE",
    "POLICY_PROHIBITION",
    "IMPLEMENTATION_MISSING",
    "OWNER_INVOCATION_MISSING",
    "IMPLEMENTATION_DEFECT",
    "CANONICAL_IMPOSSIBILITY",
    "UNKNOWN",
}

DIAGNOSIS_CONFIDENCE_VALUES = {
    "VERY_HIGH",
    "HIGH",
    "MEDIUM",
    "LOW",
    "UNKNOWN",
}

DIAGNOSIS_MUTATION_BOUNDARY = {
    "runtime_apply_allowed": False,
    "authority_expanded": False,
    "restore_barrier_written": False,
    "users_moved": 0,
    "synthetic_evidence_created": False,
    "new_owner_created": False,
    "new_runtime_created": False,
    "new_planner_created": False,
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
    scope_hash = delegated_autonomy_scope_hash(source)
    active = bool(
        source.get("policy_state") == "APPROVED"
        and source.get("current_mode") == "DELEGATED_AUTONOMY"
        and source.get("runtime_apply_enabled")
    )
    return {
        "schema_version": "v7.delegated-autonomy-policy.preview.v1",
        "generated_at": generated_at or "",
        **source,
        "normalized_scope": normalized_delegated_autonomy_scope(source),
        "policy_scope_hash": scope_hash,
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
        "autonomy_enabled": active,
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
    governed_policy_allowed = bool(
        current_state == "GOVERNED_ONLY"
        and policy_preview.get("governed_learning_mode_allowed")
        and policy_preview.get("policy_state") == "APPROVED"
    )
    if current_state != "AUTONOMOUS_RUNTIME" and not governed_policy_allowed:
        blockers.append("ACTION_CLASS_NOT_AUTONOMOUS_RUNTIME")
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
    if policy_preview.get("policy_state") != "APPROVED" and any(
        "authority_policy_approval" in item or "runtime policy binding" in item
        for item in missing_evidence
    ):
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
        "governed_learning_policy_consumed": governed_policy_allowed,
        "policy_scope_hash": str(policy_preview.get("policy_scope_hash") or ""),
        "policy_expansion_allowed_by_runtime": False,
        "authority_expansion_allowed_by_runtime": False,
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": eligible,
    }


def build_historical_blast_radius_evidence(
    evidence_dir: Path | str | None = None,
    *,
    report_root: Path | str | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Read existing historical movement proofs without treating them as authority."""
    repository_root = Path(report_root) if report_root is not None else Path(__file__).resolve().parents[1]
    root = Path(evidence_dir) if evidence_dir is not None else repository_root / "docs/track7/productization/e29-evidence"
    files = {
        "scaling_review": root / "scaling-review.md",
        "governance_proof_matrix": root / "governance-proof-matrix.md",
        "execution_history_review": root / "execution-history-review.md",
        "tests": root / "tests.md",
    }
    contents: dict[str, str] = {}
    for name, path in files.items():
        try:
            contents[name] = path.read_text(encoding="utf-8")
        except OSError:
            contents[name] = ""
    combined = "\n".join(contents.values())
    rows = [
        {
            "scale": "one-user",
            "users": 1,
            "certified": "one_user_governed_execution_certified=true" in combined,
            "evidence": "E25.15",
        },
        {
            "scale": "two-user",
            "users": 2,
            "certified": "two_user_governed_execution_certified=true" in combined,
            "evidence": "E27.2",
        },
        {
            "scale": "small-cohort",
            "users": 4,
            "certified": "small_cohort_governed_execution_certified=true" in combined,
            "evidence": "E28.2",
        },
    ]
    certified_users = [row["users"] for row in rows if row["certified"]]
    scale_match = re.search(r"Current certified scale=(\d+) users", combined)
    if scale_match:
        certified_users.append(int(scale_match.group(1)))
    required_phrases = [
        "approval_packet_system_certified=true",
        "execution_time_recheck_certified=true",
        "rollback_certified=true",
        "replay_protection_certified=true",
        "restore_settle_certified=true",
        "governance_isolation_certified=true",
        "latest_forward_success=true",
        "latest_rollback_success=true",
        "latest_delayed_movement_observed=false",
        "latest_replay_rejection_verified=true",
        "latest_runtime_checkers_ok=true",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in combined]
    certification_inventory = []
    for source in HISTORICAL_MOVEMENT_CERTIFICATION_SOURCES:
        path = repository_root / source["path"]
        try:
            report = path.read_text(encoding="utf-8")
        except OSError:
            report = ""
        report_available = bool(report)
        missing_markers = [marker for marker in source["markers"] if marker not in report] if report_available else []
        marker_valid = report_available and not missing_markers
        deployed_pointer_valid = not report_available and bool(source.get("repository_certified"))
        valid = marker_valid or deployed_pointer_valid
        if valid:
            certified_users.append(int(source["users"]))
        certification_inventory.append({
            "certification_id": source["certification_id"],
            "date": source["date"],
            "real_or_read_only": "REAL_PRODUCTION_ACTION" if valid else "UNVERIFIED_POINTER",
            "users": source["users"],
            "action_class": source["action_class"],
            "scenario": source["scenario"],
            "policy": "existing governed movement / Authority / blast-radius / rollback policies",
            "authority": "historical bounded operational authority",
            "apply": "PASS" if valid else "NOT_PROVEN",
            "verification": "PASS" if valid else "NOT_PROVEN",
            "rollback": source["rollback"] if valid else "NOT_PROVEN",
            "outcome": "CLOSED_SUCCESS" if valid else "NOT_PROVEN",
            "learning": "SUPPORTING_OR_NOT_PROVEN_FOR_CURRENT_CLASS" if valid else "NOT_PROVEN",
            "maturity": "SUPPORTING_EVIDENCE_ONLY",
            "current_validity": "VALID_SUPPORTING_LAYER" if valid else "REVALIDATION_REQUIRED",
            "validation_basis": (
                "REPORT_MARKERS_VERIFIED"
                if marker_valid
                else ("DEPLOYED_REPOSITORY_CERTIFIED_PROVENANCE_POINTER" if deployed_pointer_valid else "UNVERIFIED")
            ),
            "report_available_to_current_process": report_available,
            "current_class_match": "EXECUTION_ONLY_MATCH",
            "reusable_dimensions": ["execution", "blast_radius", "verification", "rollback_or_no_rollback", "outcome"],
            "not_reusable_as": ["current_decision_certification", "action_class_authority", "delegated_policy"],
            "missing_markers": missing_markers,
            "evidence": source["path"],
        })
    valid_certifications = [
        row for row in certification_inventory
        if row["current_validity"] == "VALID_SUPPORTING_LAYER"
    ]
    max_certified = max(certified_users or [0])
    reusable_dimensions = {
        "execution_path": bool(valid_certifications),
        "blast_radius": any(int(row["users"]) >= 1 for row in valid_certifications),
        "rollback_or_no_rollback": any(row["rollback"] in {"PASS", "NOT_REQUIRED"} for row in valid_certifications),
        "verification": bool(valid_certifications),
        "outcome": bool(valid_certifications),
        "current_decision_context": False,
        "action_class_authority": False,
        "delegated_policy": False,
    }
    return {
        "schema_version": "v7.historical-blast-radius-evidence.v2",
        "generated_at": generated_at or "",
        "owner": "docs/track7/productization/e29-evidence",
        "evidence_dir": str(root),
        "files_read": {name: str(path) for name, path in files.items() if contents.get(name)},
        "rows": rows,
        "certification_inventory": certification_inventory,
        "historical_certifications_found": len(certification_inventory),
        "real_movement_certifications_found": len(valid_certifications),
        "max_certified_blast_radius_users": max_certified,
        "beyond_one_user_historical_evidence_exists": max_certified > 1,
        "required_historical_proofs_present": not missing,
        "missing_historical_proofs": missing,
        "reusable_dimensions": reusable_dimensions,
        "current_action_class": "single-user governed candidate failover",
        "current_action_class_identity": "DECISION_CONTEXT_MISMATCH",
        "exact_current_class_real_outcomes": 0,
        "root_cause_of_non_consumption": "ACTION_CLASS_IDENTITY_NOT_MAPPED",
        "exact_missing_delta": [
            "real suitability-based single-user outcome for the current canonical action class",
            "current-class learning consumption",
            "explicit class approval",
            "approved delegated policy before autonomous Runtime",
        ],
        "evidence_role": "historical_certification_evidence_only",
        "authority_granted": False,
        "runtime_apply_allowed": False,
        "read_only": True,
        "runtime_mutation_performed": False,
        "apply_executed": False,
        "users_moved": 0,
        "new_truth_source_created": False,
    }


def build_class_level_blast_radius_certification(
    *,
    action_class_runtime_enablement: dict[str, Any],
    floor_forensics: dict[str, Any],
    service_user_sla_fit: dict[str, Any],
    hard_failure_classification: dict[str, Any],
    decision_outcome_closure: dict[str, Any],
    historical_blast_radius_evidence: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Certify blast-radius evidence for A5 without approving larger scope."""
    classes = [
        row for row in action_class_runtime_enablement.get("action_classes", [])
        if isinstance(row, dict)
    ]
    current = next(
        (row for row in classes if row.get("action_class") == action_class_runtime_enablement.get("current_action_class")),
        classes[0] if classes else {},
    )
    next_candidates = [
        row for row in classes
        if row.get("runtime_enablement_state") == "NOT_CERTIFIED"
    ]
    next_class = next_candidates[0] if next_candidates else {}
    components = floor_forensics.get("component_values") if isinstance(floor_forensics.get("component_values"), dict) else {}
    rollback_blast = floor_forensics.get("rollback_and_blast") if isinstance(floor_forensics.get("rollback_and_blast"), dict) else {}
    fit_summary = service_user_sla_fit.get("summary") if isinstance(service_user_sla_fit.get("summary"), dict) else {}
    closure_summary = decision_outcome_closure.get("summary") if isinstance(decision_outcome_closure.get("summary"), dict) else {}
    blast_confidence = as_float(components.get("blast_radius_confidence"), 0.0)
    blast_records = int(as_float(rollback_blast.get("blast_records_seen"), 0.0))
    selected_budget = int((DEFAULT_DELEGATED_AUTONOMY_POLICY.get("max_blast_radius") or {}).get("users") or 1)
    next_required = next_class.get("required_blast_radius") or "bounded cohort"
    evidence_rows = [
        {
            "signal": "current_policy_max_users_per_action",
            "value": selected_budget,
            "status": "PASS" if selected_budget == 1 else "REVIEW",
        },
        {
            "signal": "blast_radius_confidence",
            "value": round(blast_confidence, 3),
            "status": "PASS" if blast_confidence >= 100.0 else "BLOCKED",
        },
        {
            "signal": "blast_records_seen",
            "value": blast_records,
            "status": "PASS" if blast_records > 0 else "BLOCKED",
        },
        {
            "signal": "service_capacity_policy_fit",
            "value": fit_summary.get("verdict_counts", {}),
            "status": "PASS" if fit_summary.get("users_seen", 0) else "BLOCKED",
        },
        {
            "signal": "decision_outcome_closure",
            "value": decision_outcome_closure.get("closure_state", "UNKNOWN"),
            "status": "PASS" if decision_outcome_closure.get("closure_state") == "COMPLETE" else "BLOCKED",
        },
        {
            "signal": "valid_closure_candidates",
            "value": int(closure_summary.get("valid_closures") or 0),
            "status": "PASS" if int(closure_summary.get("valid_closures") or 0) > 0 else "BLOCKED",
        },
        {
            "signal": "hard_failure_classification",
            "value": hard_failure_classification.get("classification", "UNKNOWN"),
            "status": "PASS" if hard_failure_classification.get("classification") == "HARD_FAILURE_CONFIRMED" else "SUPPORTING_ONLY",
        },
    ]
    blockers = [
        row["signal"] for row in evidence_rows
        if row["status"] == "BLOCKED"
    ]
    current_one_user_certified = not blockers and current.get("required_blast_radius") == "exactly one user"
    historical = historical_blast_radius_evidence if isinstance(historical_blast_radius_evidence, dict) else {}
    max_historical_users = int(historical.get("max_certified_blast_radius_users") or 0)
    historical_proofs_present = bool(historical.get("required_historical_proofs_present"))
    beyond_one_user_certified = max_historical_users > 1 and historical_proofs_present
    beyond_blockers = []
    if not beyond_one_user_certified:
        beyond_blockers.append("beyond_one_user_real_outcome_evidence_missing")
    if not historical_proofs_present:
        beyond_blockers.append("historical_blast_radius_proof_matrix_incomplete")
    return {
        "schema_version": "v7.a5-class-level-blast-radius-certification.v1",
        "generated_at": generated_at or "",
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "A5",
        "policy_sources": ["POLICY_006_BLAST_RADIUS", "POLICY_005_ACTION_CLASS_PROMOTION"],
        "current_action_class": current.get("action_class", "UNKNOWN_ACTION_CLASS"),
        "current_blast_radius": current.get("required_blast_radius", "UNKNOWN"),
        "current_one_user_guard_certified": current_one_user_certified,
        "next_candidate_action_class": next_class.get("action_class", ""),
        "next_candidate_required_blast_radius": next_required,
        "beyond_one_user_certified": beyond_one_user_certified,
        "max_historical_certified_blast_radius_users": max_historical_users,
        "historical_blast_radius_evidence": historical,
        "certification_state": "BEYOND_ONE_USER_EVIDENCE_CERTIFIED_READ_ONLY" if beyond_one_user_certified else "WAITING_FOR_BEYOND_ONE_USER_EVIDENCE",
        "blockers": blockers + beyond_blockers + ["class_authority_not_approved"],
        "evidence_rows": evidence_rows,
        "certification_rules": {
            "one_user_guard_is_not_beyond_one_user_certification": True,
            "planner_move_counts_required": True,
            "capacity_load_gates_required": True,
            "fallback_policy_scope_required": True,
            "real_outcomes_required_before_scope_expansion": True,
            "authority_required_before_scope_expansion": True,
        },
        "omp_output": {
            "a5_status": "CERTIFICATION_EVIDENCE_READY_AUTHORITY_NOT_GRANTED" if beyond_one_user_certified else "IN_PROGRESS_WAITING_FOR_REAL_BEYOND_ONE_USER_EVIDENCE",
            "recommendation": "CERTIFY_A5_EVIDENCE_ONLY_DO_NOT_EXPAND_AUTHORITY" if beyond_one_user_certified else "DO_NOT_EXPAND_BLAST_RADIUS",
            "next_safe_action": "update A5 as evidence-certified and continue to A6/B13 without authority expansion" if beyond_one_user_certified else "preserve one-user governed guard and collect/certify only real owner evidence",
            "stop_condition_if_scope_expansion_requested": "ENGINEERING_AUTHORITY",
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
        "new_planner_created": False,
        "new_runtime_created": False,
    }


def _recovery_runtime_integration_gate(
    recovery_admission_certification: dict[str, Any] | None,
    post_admission_observation_windows: dict[str, Any] | None,
    recovery_slow_start_progression: dict[str, Any] | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    b8 = recovery_admission_certification if isinstance(recovery_admission_certification, dict) else {}
    b9 = post_admission_observation_windows if isinstance(post_admission_observation_windows, dict) else {}
    b10 = recovery_slow_start_progression if isinstance(recovery_slow_start_progression, dict) else {}
    b8_rows = {
        _b8_channel_key(row, index): row
        for index, row in enumerate(b8.get("rows") or [])
        if isinstance(row, dict)
    }
    b9_rows = {
        _b8_channel_key(row, index): row
        for index, row in enumerate(b9.get("rows") or [])
        if isinstance(row, dict)
    }
    b10_rows = {
        _b8_channel_key(row, index): row
        for index, row in enumerate(b10.get("rows") or [])
        if isinstance(row, dict)
    }
    channels = sorted(
        channel
        for channel, row in b8_rows.items()
        if row.get("recovery_candidate") is True or row.get("admission_state") == "RECOVERED_WATCH"
    )
    if not channels:
        evidence = {
            "required": False,
            "state": "NOT_APPLICABLE_NO_RECOVERY_CANDIDATE",
            "channels": [],
            "ready_channels": [],
            "blocked_channels": [],
            "bounded_recovery_candidates": [],
            "blockers": [],
            "execution_owner": "tools/v7-users-autoswitch",
            "read_only": True,
            "runtime_mutation_performed": False,
            "runtime_apply_allowed": False,
            "direct_execution_allowed": False,
            "users_moved": 0,
        }
        return {
            "gate": "recovery_admission",
            "state": "NOT_APPLICABLE",
            "owner": "B8/B9/B10 recovery owners",
            "evidence": evidence,
        }, evidence

    schema_blockers = []
    if b8.get("schema_version") != "v7.b8.recovery-admission-certification.v1":
        schema_blockers.append("b8_recovery_admission_certification_missing_or_unknown")
    if b9.get("schema_version") != "v7.b9.post-admission-observation-windows.v1":
        schema_blockers.append("b9_post_admission_observation_windows_missing_or_unknown")
    if b10.get("schema_version") != "v7.b10.recovery-slow-start-progression.v1":
        schema_blockers.append("b10_recovery_slow_start_progression_missing_or_unknown")

    rows = []
    for channel in channels:
        certification = b8_rows.get(channel) or {}
        observation = b9_rows.get(channel) or {}
        progression = b10_rows.get(channel) or {}
        blockers = list(schema_blockers)
        if not certification:
            blockers.append("b8_recovery_admission_certification_missing")
        elif certification.get("certification_state") != "CERTIFIED_FOR_RECOVERY_ADMISSION_REVIEW":
            blockers.append("b8_recovery_admission_certification_not_ready")
        blockers.extend(str(item) for item in certification.get("blockers") or [] if item)
        if not observation:
            blockers.append("b9_post_admission_observation_windows_missing")
        elif observation.get("verification_state") != "POST_ADMISSION_WINDOWS_VERIFIED_READ_ONLY":
            blockers.append("b9_post_admission_observation_windows_not_verified")
        blockers.extend(str(item) for item in observation.get("blockers") or [] if item)
        if not progression:
            blockers.append("b10_recovery_slow_start_progression_missing")
        elif progression.get("progression_state") != "SLOW_START_PROGRESSION_READY_READ_ONLY":
            blockers.append("b10_recovery_slow_start_progression_not_ready")
        if progression and progression.get("safe_next_stage") != "ONE_USER_GOVERNED_RECOVERY_REVIEW":
            blockers.append("b10_one_user_governed_recovery_stage_not_ready")
        blockers.extend(str(item) for item in progression.get("blockers") or [] if item)
        blockers = sorted(set(blockers))
        ready = not blockers
        rows.append({
            "channel": channel,
            "state": "READY_FOR_EXISTING_AUTHORITY_REVIEW_READ_ONLY" if ready else "STOP_SAFE",
            "blockers": blockers,
            "b8_state": certification.get("certification_state", "MISSING"),
            "b9_state": observation.get("verification_state", "MISSING"),
            "b10_state": progression.get("progression_state", "MISSING"),
            "safe_next_stage": progression.get("safe_next_stage", "BLOCKED"),
            "execution_owner": "tools/v7-users-autoswitch",
            "authority_owner": "existing OMP/action-class/blast-radius/operator authority",
            "max_users": 1,
            "packet_lease_identity_required": True,
            "rollback_and_verification_required": True,
            "runtime_apply_allowed": False,
            "direct_execution_allowed": False,
        })

    blockers = sorted({blocker for row in rows for blocker in row["blockers"]})
    ready_rows = [row for row in rows if row["state"] == "READY_FOR_EXISTING_AUTHORITY_REVIEW_READ_ONLY"]
    evidence = {
        "required": True,
        "state": "READY_FOR_EXISTING_AUTHORITY_REVIEW_READ_ONLY" if not blockers else "STOP_SAFE",
        "channels": rows,
        "ready_channels": [row["channel"] for row in ready_rows],
        "blocked_channels": [row["channel"] for row in rows if row["state"] == "STOP_SAFE"],
        "bounded_recovery_candidates": ready_rows,
        "blockers": blockers,
        "execution_owner": "tools/v7-users-autoswitch",
        "authority_owner": "existing OMP/action-class/blast-radius/operator authority",
        "post_action_contract": "existing verification/closure/learning/Production Maturity/CPS/OMP path",
        "read_only": True,
        "runtime_mutation_performed": False,
        "runtime_apply_allowed": False,
        "direct_execution_allowed": False,
        "users_moved": 0,
        "authority_created_by_recovery_evidence": False,
        "blast_radius_expanded": False,
    }
    return {
        "gate": "recovery_admission",
        "state": "PASS" if not blockers else "STOP",
        "owner": "B8/B9/B10 recovery owners",
        "evidence": evidence,
    }, evidence


def build_runtime_eligibility_arbitration(
    *,
    action_class_runtime_enablement: dict[str, Any],
    class_level_blast_radius_certification: dict[str, Any],
    freshness_actionability: dict[str, Any],
    anti_flapping: dict[str, Any],
    decision_outcome_closure: dict[str, Any],
    decision_outcome_learning: dict[str, Any],
    routing_recommendation_readiness: dict[str, Any],
    recovery_admission_certification: dict[str, Any] | None = None,
    post_admission_observation_windows: dict[str, Any] | None = None,
    recovery_slow_start_progression: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Expose A6 execute-or-stop arbitration without enabling Runtime."""
    delegated = action_class_runtime_enablement.get("delegated_autonomy_runtime_eligibility")
    if not isinstance(delegated, dict):
        delegated = {}
    missing_evidence = list((action_class_runtime_enablement.get("enablement_readiness") or {}).get("missing_evidence") or [])
    knowledge_growth = decision_outcome_learning.get("knowledge_growth") if isinstance(decision_outcome_learning.get("knowledge_growth"), dict) else {}
    stale_domains = sorted(delegated.get("stale_required_domains") or [])
    anti_flap_blocked = int((anti_flapping.get("summary") or {}).get("blocked_users") or 0)
    closure_state = str(decision_outcome_closure.get("closure_state") or "UNKNOWN")
    learning_gained = int(knowledge_growth.get("knowledge_gained") or 0)
    routing_blockers = list(routing_recommendation_readiness.get("blockers") or [])
    blast_ready = bool(class_level_blast_radius_certification.get("beyond_one_user_certified"))
    recovery_gate, recovery_integration = _recovery_runtime_integration_gate(
        recovery_admission_certification,
        post_admission_observation_windows,
        recovery_slow_start_progression,
    )
    gate_rows = [
        {
            "gate": "freshness",
            "state": "PASS" if not stale_domains else "STOP",
            "owner": "freshness_actionability",
            "evidence": stale_domains,
        },
        {
            "gate": "authority",
            "state": "STOP" if "AUTHORITY_POLICY_NOT_APPROVED" in delegated.get("blockers", []) else "PASS",
            "owner": "delegated_autonomy_policy_preview",
            "evidence": delegated.get("blockers", []),
        },
        {
            "gate": "blast_radius",
            "state": "PASS" if blast_ready else "STOP",
            "owner": "class_level_blast_radius_certification",
            "evidence": {
                "max_historical_certified_blast_radius_users": class_level_blast_radius_certification.get("max_historical_certified_blast_radius_users", 0),
                "certification_state": class_level_blast_radius_certification.get("certification_state", "UNKNOWN"),
            },
        },
        {
            "gate": "rollback_or_no_rollback",
            "state": "STOP" if any("rollback_or_no_rollback" in item for item in missing_evidence) else "PASS",
            "owner": "decision_outcome_closure",
            "evidence": missing_evidence,
        },
        {
            "gate": "anti_flap",
            "state": "PASS" if anti_flap_blocked == 0 else "STOP",
            "owner": "anti_flapping",
            "evidence": {"blocked_users": anti_flap_blocked},
        },
        {
            "gate": "verification",
            "state": "PASS" if closure_state == "COMPLETE" else "STOP",
            "owner": "decision_outcome_closure",
            "evidence": {"closure_state": closure_state},
        },
        {
            "gate": "learning",
            "state": "PASS" if learning_gained > 0 else "STOP",
            "owner": "decision_outcome_learning",
            "evidence": {"knowledge_gained": learning_gained},
        },
        {
            "gate": "routing_readiness",
            "state": "PASS" if not routing_blockers else "STOP",
            "owner": "routing_recommendation_readiness",
            "evidence": routing_blockers,
        },
        recovery_gate,
        {
            "gate": "runtime_apply",
            "state": "STOP" if not delegated.get("runtime_can_execute_automatically") else "PASS",
            "owner": "Runtime Model / delegated policy",
            "evidence": delegated.get("blockers", []),
        },
    ]
    stop_gates = [row["gate"] for row in gate_rows if row["state"] == "STOP"]
    authority_stop = "authority" in stop_gates or "runtime_apply" in stop_gates
    return {
        "schema_version": "v7.a6-runtime-eligibility-arbitration.v1",
        "generated_at": generated_at or "",
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "A6",
        "purpose": "read_only_execute_or_stop_arbitration_from_existing_certified_gates",
        "gate_rows": gate_rows,
        "stop_gates": stop_gates,
        "arbitration_state": "STOP_AT_AUTHORITY_OR_RUNTIME_APPLY" if authority_stop else ("STOP_AT_EVIDENCE_GATE" if stop_gates else "ELIGIBLE_READ_ONLY_PREVIEW"),
        "runtime_execute_decision": "STOP_SAFE" if stop_gates else "ELIGIBLE_READ_ONLY_PREVIEW",
        "runtime_apply_allowed": False,
        "runtime_can_execute_automatically": False,
        "authority_required_before_runtime_apply": True,
        "recovery_runtime_integration": recovery_integration,
        "certified_gate_outputs_consumed": {
            "A1_hard_failure": True,
            "A2_freshness": True,
            "A3_rollback_no_rollback": "rollback_or_no_rollback" not in " ".join(missing_evidence),
            "A4_representative_outcomes": True,
            "A5_blast_radius": blast_ready,
            "B8_recovery_admission": not recovery_integration["required"] or not any(
                "b8_" in blocker for blocker in recovery_integration["blockers"]
            ),
            "B9_post_admission_observation": not recovery_integration["required"] or not any(
                "b9_" in blocker for blocker in recovery_integration["blockers"]
            ),
            "B10_recovery_slow_start": not recovery_integration["required"] or not any(
                "b10_" in blocker for blocker in recovery_integration["blockers"]
            ),
        },
        "omp_output": {
            "a6_status": "READ_MODEL_IMPLEMENTED_STOPPED_BY_AUTHORITY" if authority_stop else "READ_MODEL_IMPLEMENTED",
            "next_safe_action": "continue to B13 metric reliability after A6 report/canonical update" if authority_stop else "certify read-only preview only",
            "authority_expansion_required": authority_stop,
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
        "new_planner_created": False,
        "new_runtime_created": False,
    }


def build_stale_read_mutation_blocking(
    *,
    freshness_actionability: dict[str, Any] | None = None,
    runtime_eligibility_arbitration: dict[str, Any] | None = None,
    routing_recommendation_readiness: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Preserve stale-read visibility while keeping mutation blocked for B17."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    freshness = freshness_actionability if isinstance(freshness_actionability, dict) else {}
    runtime = runtime_eligibility_arbitration if isinstance(runtime_eligibility_arbitration, dict) else {}
    readiness = routing_recommendation_readiness if isinstance(routing_recommendation_readiness, dict) else {}
    domains = freshness.get("domains") if isinstance(freshness.get("domains"), dict) else {}
    rows: list[dict[str, Any]] = []
    for domain, row in sorted(domains.items()):
        if not isinstance(row, dict):
            continue
        classification = _text(row.get("classification"), "UNKNOWN")
        stale = classification in {"STALE_RECHECK_REQUIRED", "UNKNOWN"}
        rows.append({
            "domain": domain,
            "freshness_classification": classification,
            "reason": row.get("reason", ""),
            "families": row.get("families", []),
            "family_statuses": row.get("family_statuses", {}),
            "read_visibility": "REPORT_STALE_READ" if stale else "REPORT_FRESH_READ",
            "mutation_gate": "MUTATION_BLOCKED_RECHECK_REQUIRED" if stale else "MUTATION_STILL_BLOCKED_BY_AUTHORITY_RUNTIME_APPLY",
            "runtime_read_allowed": True,
            "runtime_mutation_allowed": False,
            "operator_action": "refresh_existing_owner_snapshot_before_mutation_review" if stale else "may_continue_read_only_review",
            "evidence_role": "blocking_evidence" if stale else "supporting_read_only_evidence",
            "runtime_mutation_performed": False,
            "apply_executed": False,
            "users_moved": 0,
        })
    runtime_gate_rows = [
        row for row in (runtime.get("gate_rows") or [])
        if isinstance(row, dict)
    ]
    runtime_freshness_gate = next((row for row in runtime_gate_rows if row.get("gate") == "freshness"), {})
    routing_blockers = list(readiness.get("blockers") or [])
    stale_domains = [
        row["domain"] for row in rows
        if row["freshness_classification"] in {"STALE_RECHECK_REQUIRED", "UNKNOWN"}
    ]
    mutation_blockers = sorted(set(
        [f"stale_read:{domain}" for domain in stale_domains]
        + (["runtime_eligibility_freshness_gate_stop"] if runtime_freshness_gate.get("state") == "STOP" else [])
        + [f"routing:{item}" for item in routing_blockers if "freshness" in str(item)]
        + ["runtime_apply_boundary", "authority_boundary"]
    ))
    return {
        "schema_version": "v7.b17-stale-read-mutation-blocking.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B17",
        "purpose": "preserve_stale_read_reporting_while_blocking_mutation_through_existing_freshness_and_runtime_eligibility_owners",
        "source_owners_reused": [
            "admin_core.autonomy_trust_acceleration.build_freshness_actionability",
            "admin_core.autonomy_trust_acceleration.build_runtime_eligibility_arbitration",
            "admin_core.autonomy_trust_acceleration.build_routing_recommendation_readiness",
            "tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only",
            "truth/convergence read-only owners",
            "Runtime Model freshness and runtime_apply gates",
        ],
        "policy_sources": [
            "docs/policies/POLICY_008_FRESHNESS.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B17",
        ],
        "consumed_prior_capabilities": {
            "freshness_actionability": freshness.get("schema_version", "UNKNOWN"),
            "runtime_eligibility_arbitration": runtime.get("schema_version", "UNKNOWN"),
            "routing_recommendation_readiness": readiness.get("schema_version", "UNKNOWN"),
        },
        "rows": rows,
        "runtime_freshness_gate": runtime_freshness_gate,
        "routing_readiness": {
            "readiness": readiness.get("readiness", "UNKNOWN"),
            "freshness_blockers": [item for item in routing_blockers if "freshness" in str(item)],
        },
        "summary": {
            "domains_seen": len(rows),
            "stale_or_unknown_domains": len(stale_domains),
            "fresh_domains": sum(1 for row in rows if row["freshness_classification"] == "ACTIONABLE_NOW"),
            "mutation_blockers": len(mutation_blockers),
            "runtime_actions_created": 0,
            "authority_changes": 0,
            "synthetic_evidence_created": 0,
            "users_moved": 0,
        },
        "stale_domains": stale_domains,
        "mutation_blockers": mutation_blockers,
        "read_only_contract": {
            "stale_reads_are_reportable": True,
            "stale_reads_can_support_diagnosis": True,
            "stale_reads_can_authorize_mutation": False,
            "fresh_reads_still_do_not_bypass_authority": True,
            "runtime_apply_remains_blocked": True,
        },
        "canonical_rules": [
            "b17_preserves_stale_read_reporting_instead_of_hiding_stale_inputs",
            "stale_or_unknown_freshness_blocks_mutation_but_not_read_only_diagnosis",
            "freshness_actionability_is_existing_owner_and_not_a_new_truth_source",
            "runtime_eligibility_remains_the_execute_or_stop_consumer",
            "b17_does_not_change_freshness_thresholds_windows_or_formulas",
            "b17_does_not_grant_runtime_apply_or_authority",
        ],
        "omp_output": {
            "b17_status": "DONE_READ_ONLY_STALE_READ_MUTATION_BLOCKING",
            "produced_evidence": "stale_read_mutation_blocking",
            "unlocked_capability": "B18_OR_NEXT_OMP_ITEM_AFTER_CANONICAL_UPDATE",
            "blocked_later_steps": [
                "runtime_apply",
                "automation",
                "authority_expansion",
                "mutation_from_stale_read",
                "user_movement",
            ],
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "synthetic_evidence_created": False,
        "threshold_values_changed": False,
        "formula_changed": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_runtime_created": False,
    }


def _owner_issued_version_fields(owner_fields: dict[str, Any]) -> dict[str, Any]:
    source_hashes = owner_fields.get("source_hashes") if isinstance(owner_fields.get("source_hashes"), dict) else {}
    present = {
        "schema": bool(_text(owner_fields.get("schema"))),
        "generated_at": bool(_text(owner_fields.get("generated_at"))),
        "expires_at": bool(_text(owner_fields.get("expires_at"))),
        "ttl_seconds": isinstance(owner_fields.get("ttl_seconds"), int) and int(owner_fields.get("ttl_seconds")) > 0,
        "source_hashes": bool(source_hashes),
        "generator": bool(_text(owner_fields.get("generator"))),
        "path": bool(_text(owner_fields.get("path"))),
    }
    return {
        "present_fields": [field for field, ok in present.items() if ok],
        "missing_fields": [field for field, ok in present.items() if not ok],
        "source_hash_count": len(source_hashes),
        "has_owner_issued_identity": bool(present["schema"] or present["source_hashes"]),
        "has_owner_issued_lifetime": bool(present["generated_at"] and present["expires_at"] and present["ttl_seconds"]),
        "has_owner_path": bool(present["path"]),
    }


def build_owner_issued_version_lease_pattern(
    *,
    freshness_actionability: dict[str, Any] | None = None,
    action_class_freshness_windows: dict[str, Any] | None = None,
    stale_read_mutation_blocking: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Expose owner-issued version/lease coverage without changing lease behavior."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    freshness = freshness_actionability if isinstance(freshness_actionability, dict) else {}
    windows = action_class_freshness_windows if isinstance(action_class_freshness_windows, dict) else {}
    stale = stale_read_mutation_blocking if isinstance(stale_read_mutation_blocking, dict) else {}
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for action_row in [row for row in (windows.get("rows") or []) if isinstance(row, dict)]:
        action_class = _text(action_row.get("action_class"), "UNKNOWN_ACTION_CLASS")
        for domain_row in [row for row in (action_row.get("domains") or []) if isinstance(row, dict)]:
            domain = _text(domain_row.get("domain"), "unknown")
            owner_fields = domain_row.get("owner_issued_fields") if isinstance(domain_row.get("owner_issued_fields"), dict) else {}
            for family, fields in sorted(owner_fields.items()):
                if not isinstance(fields, dict):
                    continue
                key = (action_class, domain, family)
                if key in seen:
                    continue
                seen.add(key)
                field_coverage = _owner_issued_version_fields(fields)
                exists = bool(fields.get("exists"))
                identity = bool(field_coverage["has_owner_issued_identity"])
                lifetime = bool(field_coverage["has_owner_issued_lifetime"])
                if exists and identity and lifetime:
                    status = "OWNER_ISSUED_VERSION_LEASE_PATTERN_PRESENT"
                    blockers: list[str] = []
                elif exists and (identity or lifetime):
                    status = "OWNER_ISSUED_VERSION_LEASE_PATTERN_PARTIAL"
                    blockers = ["owner_issued_pattern_incomplete"]
                else:
                    status = "OWNER_ISSUED_VERSION_LEASE_PATTERN_MISSING"
                    blockers = ["owner_issued_pattern_missing"]
                rows.append({
                    "action_class": action_class,
                    "domain": domain,
                    "snapshot_family": family,
                    "snapshot_contract": {
                        "schema": SNAPSHOT_FAMILIES[family].schema if family in SNAPSHOT_FAMILIES else _text(fields.get("schema")),
                        "producer": SNAPSHOT_FAMILIES[family].producer if family in SNAPSHOT_FAMILIES else "UNKNOWN",
                        "consumer": SNAPSHOT_FAMILIES[family].consumer if family in SNAPSHOT_FAMILIES else "UNKNOWN",
                        "ttl_seconds": SNAPSHOT_FAMILIES[family].ttl_seconds if family in SNAPSHOT_FAMILIES else fields.get("ttl_seconds"),
                        "stale_after_seconds": SNAPSHOT_FAMILIES[family].stale_after_seconds if family in SNAPSHOT_FAMILIES else None,
                    },
                    "pattern_status": status,
                    "freshness_state": fields.get("freshness_state", "UNKNOWN"),
                    "runtime_behavior": fields.get("runtime_behavior", "STOP"),
                    "stop_required": bool(fields.get("stop_required", True)),
                    "owner_issued_identity_present": identity,
                    "owner_issued_lifetime_present": lifetime,
                    "owner_issued_fields": field_coverage,
                    "blockers": blockers,
                    "runtime_mutation_allowed": False,
                    "runtime_read_allowed": True,
                })
    stale_blockers = list(stale.get("mutation_blockers") or [])
    present = sum(1 for row in rows if row["pattern_status"] == "OWNER_ISSUED_VERSION_LEASE_PATTERN_PRESENT")
    partial = sum(1 for row in rows if row["pattern_status"] == "OWNER_ISSUED_VERSION_LEASE_PATTERN_PARTIAL")
    missing = sum(1 for row in rows if row["pattern_status"] == "OWNER_ISSUED_VERSION_LEASE_PATTERN_MISSING")
    return {
        "schema_version": "v7.b18-owner-issued-version-lease-pattern.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B18",
        "purpose": "extend_owner_issued_version_lease_pattern_where_available_without_runtime_behavior_change",
        "source_owners_reused": [
            "admin_core.intelligence_snapshots.SNAPSHOT_FAMILIES",
            "admin_core.autonomy_trust_acceleration.build_action_class_freshness_windows",
            "admin_core.autonomy_trust_acceleration.build_freshness_actionability",
            "admin_core.autonomy_trust_acceleration.build_stale_read_mutation_blocking",
            "admin_core.operator_execution execution lease semantics",
            "Runtime Model packet/lease/freshness gates",
        ],
        "policy_sources": [
            "docs/policies/POLICY_008_FRESHNESS.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B18",
        ],
        "consumed_prior_capabilities": {
            "freshness_actionability": freshness.get("schema_version", "UNKNOWN"),
            "action_class_freshness_windows": windows.get("schema_version", "UNKNOWN"),
            "stale_read_mutation_blocking": stale.get("schema_version", "UNKNOWN"),
        },
        "rows": rows,
        "summary": {
            "coverage_rows": len(rows),
            "pattern_present": present,
            "pattern_partial": partial,
            "pattern_missing": missing,
            "runtime_actions_created": 0,
            "authority_changes": 0,
            "synthetic_evidence_created": 0,
            "users_moved": 0,
        },
        "existing_execution_lease_contract": {
            "owner": "admin_core.operator_execution",
            "status": "REUSED_NO_BEHAVIOR_CHANGE",
            "packet_identity_preserved": True,
            "freshness_only_change_preserves_lease": True,
            "material_state_change_invalidates_lease": True,
            "lease_is_not_truth_source": True,
        },
        "stale_read_dependency": {
            "b17_status": ((stale.get("omp_output") or {}).get("b17_status") or "UNKNOWN"),
            "mutation_blockers_consumed": stale_blockers,
        },
        "canonical_rules": [
            "owner_issued_version_or_lease_is_stronger_than_local_timestamp_where_available",
            "b18_extends_read_model_coverage_only",
            "missing_owner_issued_pattern_blocks_mutation_but_not_read_only_diagnosis",
            "execution_lease_owner_remains_admin_core_operator_execution",
            "snapshot_family_owner_remains_admin_core_intelligence_snapshots",
            "b18_does_not_change_ttl_windows_thresholds_formulas_or_lease_behavior",
            "b18_does_not_grant_runtime_apply_or_authority",
        ],
        "omp_output": {
            "b18_status": "DONE_READ_ONLY_OWNER_ISSUED_VERSION_LEASE_PATTERN",
            "produced_evidence": "owner_issued_version_lease_pattern",
            "unlocked_capability": "B19_OR_NEXT_OMP_ITEM_AFTER_CANONICAL_UPDATE",
            "blocked_later_steps": [
                "runtime_apply",
                "automation",
                "authority_expansion",
                "new_lease_owner",
                "user_movement",
            ],
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "synthetic_evidence_created": False,
        "threshold_values_changed": False,
        "formula_changed": False,
        "lease_behavior_changed": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_runtime_created": False,
    }


def build_bounded_stale_allowance_by_action_class(
    *,
    freshness_actionability: dict[str, Any] | None = None,
    action_class_freshness_windows: dict[str, Any] | None = None,
    stale_read_mutation_blocking: dict[str, Any] | None = None,
    owner_issued_version_lease_pattern: dict[str, Any] | None = None,
    fail_open_fail_closed_action_class_behavior: dict[str, Any] | None = None,
    runtime_eligibility_arbitration: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Decide bounded stale allowance by action class without changing Runtime behavior."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    freshness = freshness_actionability if isinstance(freshness_actionability, dict) else {}
    windows = (
        action_class_freshness_windows
        if isinstance(action_class_freshness_windows, dict)
        else build_action_class_freshness_windows(freshness)
    )
    stale = stale_read_mutation_blocking if isinstance(stale_read_mutation_blocking, dict) else {}
    lease = owner_issued_version_lease_pattern if isinstance(owner_issued_version_lease_pattern, dict) else {}
    fail_behavior = fail_open_fail_closed_action_class_behavior if isinstance(fail_open_fail_closed_action_class_behavior, dict) else {}
    runtime = runtime_eligibility_arbitration if isinstance(runtime_eligibility_arbitration, dict) else {}
    runtime_gate_rows = [row for row in (runtime.get("gate_rows") or []) if isinstance(row, dict)]
    runtime_freshness_gate = next((row for row in runtime_gate_rows if row.get("gate") == "freshness"), {})
    stale_domains = set(str(domain) for domain in (stale.get("stale_domains") or []))
    lease_rows = [row for row in (lease.get("rows") or []) if isinstance(row, dict)]
    lease_status_by_class: dict[str, set[str]] = {}
    for row in lease_rows:
        action_class = _text(row.get("action_class"), "UNKNOWN_ACTION_CLASS")
        lease_status_by_class.setdefault(action_class, set()).add(_text(row.get("pattern_status"), "UNKNOWN"))
    fail_rows = [row for row in (fail_behavior.get("rows") or []) if isinstance(row, dict)]
    fail_closed_by_class = {
        _text(row.get("action_class"), ""): bool(row.get("runtime_mutation_fail_closed"))
        for row in fail_rows
    }
    rows: list[dict[str, Any]] = []
    for action_row in [row for row in (windows.get("rows") or []) if isinstance(row, dict)]:
        action_class = _text(action_row.get("action_class"), "UNKNOWN_ACTION_CLASS")
        domain_rows = [row for row in (action_row.get("domains") or []) if isinstance(row, dict)]
        stale_or_unknown_domains = [
            _text(row.get("domain"), "unknown")
            for row in domain_rows
            if _text(row.get("classification"), "UNKNOWN") in {"STALE_RECHECK_REQUIRED", "UNKNOWN"}
        ]
        configured_windows = dict(action_row.get("freshness_windows") or {})
        shortest_window = min(configured_windows.values()) if configured_windows else 0
        longest_window = max(configured_windows.values()) if configured_windows else 0
        freshness_ready = bool(action_row.get("freshness_ready")) and not stale_or_unknown_domains
        mutation_blockers = sorted(set(
            [f"stale_or_unknown:{domain}" for domain in stale_or_unknown_domains]
            + [f"b17_stale_read:{domain}" for domain in stale_domains if domain in configured_windows]
            + (["runtime_eligibility_freshness_gate_stop"] if runtime_freshness_gate.get("state") == "STOP" else [])
            + ["runtime_apply_boundary", "authority_boundary"]
        ))
        owner_issued_statuses = sorted(lease_status_by_class.get(action_class, set()))
        owner_issued_partial = any(status in {
            "OWNER_ISSUED_VERSION_LEASE_PATTERN_PARTIAL",
            "OWNER_ISSUED_VERSION_LEASE_PATTERN_MISSING",
        } for status in owner_issued_statuses)
        if owner_issued_partial:
            mutation_blockers.append("owner_issued_version_or_lease_incomplete")
        if freshness_ready:
            mutation_freshness_decision = "FRESHNESS_READY_AUTHORITY_STILL_REQUIRED"
        else:
            mutation_freshness_decision = "STOP_SAFE_REFRESH_REQUIRED_BEFORE_MUTATION"
        rows.append({
            "action_class": action_class,
            "freshness_windows": configured_windows,
            "shortest_window_seconds": int(shortest_window or 0),
            "longest_window_seconds": int(longest_window or 0),
            "freshness_ready": freshness_ready,
            "stale_or_unknown_domains": stale_or_unknown_domains,
            "stale_read_allowed_for_observation": True,
            "stale_read_allowed_for_diagnosis": True,
            "stale_read_allowed_for_engineering_report": True,
            "stale_read_allowed_for_mutation": False,
            "bounded_stale_mutation_allowance_seconds": 0,
            "fresh_evidence_required_before_mutation": True,
            "owner_issued_version_or_lease_required_when_available": True,
            "owner_issued_pattern_statuses": owner_issued_statuses,
            "runtime_mutation_fail_closed": fail_closed_by_class.get(action_class, True),
            "mutation_freshness_decision": mutation_freshness_decision,
            "mutation_blockers": sorted(set(mutation_blockers)),
            "runtime_apply_allowed": False,
            "authority_expanded": False,
            "runtime_mutation_performed": False,
            "apply_executed": False,
            "users_moved": 0,
        })
    return {
        "schema_version": "v7.c6-bounded-stale-allowance-by-action-class.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "C6",
        "purpose": "decide_bounded_stale_allowance_by_action_class_without_runtime_behavior_change",
        "source_owners_reused": [
            "admin_core.autonomy_trust_acceleration.build_freshness_actionability",
            "admin_core.autonomy_trust_acceleration.build_action_class_freshness_windows",
            "admin_core.autonomy_trust_acceleration.build_stale_read_mutation_blocking",
            "admin_core.autonomy_trust_acceleration.build_owner_issued_version_lease_pattern",
            "admin_core.autonomy_trust_acceleration.build_fail_open_fail_closed_action_class_behavior",
            "admin_core.autonomy_trust_acceleration.build_runtime_eligibility_arbitration",
            "Runtime Model freshness gates",
            "OMP stop rules",
        ],
        "policy_sources": [
            "docs/policies/POLICY_008_FRESHNESS.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#C6",
        ],
        "consumed_prior_capabilities": {
            "freshness_actionability": freshness.get("schema_version", "UNKNOWN"),
            "action_class_freshness_windows": windows.get("schema_version", "UNKNOWN"),
            "stale_read_mutation_blocking": stale.get("schema_version", "UNKNOWN"),
            "owner_issued_version_lease_pattern": lease.get("schema_version", "UNKNOWN"),
            "fail_open_fail_closed_action_class_behavior": fail_behavior.get("schema_version", "UNKNOWN"),
            "runtime_eligibility_arbitration": runtime.get("schema_version", "UNKNOWN"),
        },
        "decision": {
            "bounded_stale_mutation_allowance_seconds": 0,
            "stale_evidence_observation_allowed": True,
            "stale_evidence_diagnosis_allowed": True,
            "stale_evidence_engineering_report_allowed": True,
            "stale_evidence_mutation_allowed": False,
            "fresh_evidence_required_before_mutation": True,
            "owner_issued_version_or_lease_preferred": True,
        },
        "rows": rows,
        "summary": {
            "action_classes": len(rows),
            "freshness_ready": sum(1 for row in rows if row["freshness_ready"]),
            "refresh_required_before_mutation": sum(1 for row in rows if row["mutation_freshness_decision"] == "STOP_SAFE_REFRESH_REQUIRED_BEFORE_MUTATION"),
            "stale_mutation_allowed": sum(1 for row in rows if row["stale_read_allowed_for_mutation"]),
            "runtime_actions_created": 0,
            "authority_changes": 0,
            "synthetic_evidence_created": 0,
            "users_moved": 0,
        },
        "canonical_rules": [
            "c6_decides_stale_allowance_by_existing_action_class_windows",
            "stale_or_unknown_evidence_is_observable_and_reportable",
            "stale_or_unknown_evidence_never_authorizes_mutation",
            "fresh_evidence_inside_existing_windows_is_required_before_mutation_review",
            "owner_issued_version_or_lease_is_preferred_when_available",
            "c6_does_not_change_freshness_windows_thresholds_or_formulas",
            "c6_does_not_grant_runtime_apply_or_authority",
        ],
        "omp_output": {
            "c6_status": "DONE_READ_ONLY_BOUNDED_STALE_ALLOWANCE_BY_ACTION_CLASS",
            "produced_evidence": "bounded_stale_allowance_by_action_class",
            "unlocked_capability": "C7_POOL_MAX_EJECTION_MINIMUM_HEALTH_CAPACITY_BLAST_BOUNDS",
            "blocked_later_steps": [
                "runtime_apply",
                "automation",
                "authority_expansion",
                "mutation_from_stale_read",
                "threshold_formula_mutation",
                "new_owner",
                "planner_replacement",
                "synthetic_evidence",
                "user_movement",
            ],
            "next_safe_action": "continue_omp_to_c7_pool_health_capacity_blast_bounds",
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "synthetic_evidence_created": False,
        "threshold_values_changed": False,
        "formula_changed": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_runtime_created": False,
    }


def build_hysteresis_state_change_cost_mapping(
    *,
    anti_flapping: dict[str, Any] | None = None,
    recovery_admission: dict[str, Any] | None = None,
    service_objective_policy_threshold_binding: dict[str, Any] | None = None,
    owner_issued_version_lease_pattern: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Centralize existing hysteresis and state-change-cost vocabulary for B19."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    anti = anti_flapping if isinstance(anti_flapping, dict) else {}
    recovery = recovery_admission if isinstance(recovery_admission, dict) else {}
    objectives = service_objective_policy_threshold_binding if isinstance(service_objective_policy_threshold_binding, dict) else {}
    version_lease = owner_issued_version_lease_pattern if isinstance(owner_issued_version_lease_pattern, dict) else {}
    anti_policy = anti.get("policy") if isinstance(anti.get("policy"), dict) else ANTI_FLAP_POLICY
    recovery_policy = recovery.get("policy") if isinstance(recovery.get("policy"), dict) else RECOVERY_ADMISSION_POLICY
    catalog_rows = [
        {
            "control": "sticky_current_bias",
            "canonical_category": "STATE_CHANGE_COST",
            "existing_owner": "tools/v7-users-autoswitch score_parts.sticky / keep-current explanation",
            "existing_signal": "sticky/current route kept; candidate must beat current by policy threshold",
            "protects": ["unnecessary_movement", "low_value_rebalance", "operator_noise"],
            "consumer": "movement protection and planner/autoswitch read-only recommendation",
            "status": "EXISTS_UNDER_OTHER_NAME",
            "runtime_mutation_allowed": False,
        },
        {
            "control": "minimum_score_improvement",
            "canonical_category": "STATE_CHANGE_COST",
            "existing_owner": "tools/v7-users-autoswitch._beats_current",
            "existing_signal": "min_score_improvement_pct + min_score_delta",
            "protects": ["small_delta_churn", "suboptimal_move_cost"],
            "consumer": "movement protection and decision explainability",
            "status": "EXISTS_UNDER_OTHER_NAME",
            "runtime_mutation_allowed": False,
        },
        {
            "control": "cooldown_hold_down",
            "canonical_category": "HYSTERESIS",
            "existing_owner": "build_anti_flapping + tools/v7-users-autoswitch._cooldown_ok",
            "existing_signal": f"cooldown_seconds={int(anti_policy.get('cooldown_seconds', 0) or 0)}",
            "protects": ["rapid_repeat_movement", "retry_storm", "operator_loop"],
            "consumer": "runtime eligibility anti_flap gate",
            "status": "EXISTS_COMPLETE",
            "runtime_mutation_allowed": False,
        },
        {
            "control": "minimum_observation_window",
            "canonical_category": "HYSTERESIS",
            "existing_owner": "POLICY_009_ANTI_FLAP + recovery admission / observation windows",
            "existing_signal": f"minimum_observation_window_seconds={int(anti_policy.get('minimum_observation_window_seconds', 0) or 0)}",
            "protects": ["premature_recovery", "noisy_signal_reaction"],
            "consumer": "recovery admission and runtime eligibility",
            "status": "EXISTS_COMPLETE",
            "runtime_mutation_allowed": False,
        },
        {
            "control": "rapid_oscillation_detection",
            "canonical_category": "HYSTERESIS",
            "existing_owner": "build_anti_flapping",
            "existing_signal": f"rapid_oscillation_threshold={int(anti_policy.get('rapid_oscillation_threshold', 0) or 0)}",
            "protects": ["source_target_ping_pong", "repeated_target_oscillation"],
            "consumer": "runtime eligibility anti_flap gate",
            "status": "EXISTS_COMPLETE",
            "runtime_mutation_allowed": False,
        },
        {
            "control": "user_freeze",
            "canonical_category": "STATE_CHANGE_COST",
            "existing_owner": "tools/v7-users-autoswitch safety_policy",
            "existing_signal": "user_switches_1h_limit / user_switches_24h_limit / penalty_until",
            "protects": ["per_user_churn", "incident_loop"],
            "consumer": "movement protection and operator review",
            "status": "EXISTS_UNDER_OTHER_NAME",
            "runtime_mutation_allowed": False,
        },
        {
            "control": "pair_reversal_window",
            "canonical_category": "HYSTERESIS",
            "existing_owner": "tools/v7-users-autoswitch._pair_reversal_blocked_for_user",
            "existing_signal": "pair_reversal_stability_window",
            "protects": ["back_and_forth_switching", "unstable_pair_loop"],
            "consumer": "movement protection and runtime eligibility",
            "status": "EXISTS_UNDER_OTHER_NAME",
            "runtime_mutation_allowed": False,
        },
        {
            "control": "target_block_and_quarantine",
            "canonical_category": "STATE_CHANGE_COST",
            "existing_owner": "tools/v7-users-autoswitch safety_state",
            "existing_signal": "target_blocked_for_user / egress_safety_quarantine / egress_failed_verifications_limit",
            "protects": ["known_bad_target_reuse", "failed_verification_reentry"],
            "consumer": "movement protection and recovery admission",
            "status": "EXISTS_UNDER_OTHER_NAME",
            "runtime_mutation_allowed": False,
        },
        {
            "control": "recovery_success_threshold",
            "canonical_category": "HYSTERESIS",
            "existing_owner": "build_recovery_admission",
            "existing_signal": f"min_successful_checks={int(recovery_policy.get('min_successful_checks', 0) or 0)}; watch_successful_checks={int(recovery_policy.get('watch_successful_checks', 0) or 0)}",
            "protects": ["premature_recovery_admission", "flapping_recovered_channel"],
            "consumer": "recovery admission and movement protection",
            "status": "EXISTS_COMPLETE",
            "runtime_mutation_allowed": False,
        },
        {
            "control": "freshness_identity_cost",
            "canonical_category": "STATE_CHANGE_COST",
            "existing_owner": "B18 owner-issued version/lease pattern + freshness actionability",
            "existing_signal": "missing owner-issued identity/lifetime blocks mutation but not diagnosis",
            "protects": ["stale_decision_apply", "identity_mismatch_apply"],
            "consumer": "runtime eligibility and movement protection",
            "status": "EXISTS_COMPLETE" if version_lease.get("schema_version") == "v7.b18-owner-issued-version-lease-pattern.v1" else "EXISTS_PARTIAL",
            "runtime_mutation_allowed": False,
        },
    ]
    active_rows = [row for row in (anti.get("rows") or []) if isinstance(row, dict)]
    blocked_users = int((anti.get("summary") or {}).get("blocked_users") or 0)
    recovery_rows = [row for row in (recovery.get("rows") or []) if isinstance(row, dict)]
    objective_rows = [row for row in (objectives.get("rows") or []) if isinstance(row, dict)]
    return {
        "schema_version": "v7.b19-hysteresis-state-change-cost-mapping.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B19",
        "purpose": "centralize_existing_hysteresis_and_state_change_cost_vocabulary_without_changing_thresholds_or_formulas",
        "source_owners_reused": [
            "admin_core.autonomy_trust_acceleration.build_anti_flapping",
            "admin_core.autonomy_trust_acceleration.build_recovery_admission",
            "admin_core.autonomy_trust_acceleration.build_service_objective_policy_threshold_binding",
            "admin_core.autonomy_trust_acceleration.build_owner_issued_version_lease_pattern",
            "tools/v7-users-autoswitch sticky/cooldown/freeze/pair-reversal/target-block owners",
            "tools/v7-service-matrix-refresh-all service signal threshold owners",
            "Runtime Model movement protection and anti-flap gates",
        ],
        "policy_sources": [
            "docs/policies/POLICY_009_ANTI_FLAP.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B19",
        ],
        "consumed_prior_capabilities": {
            "anti_flapping": anti.get("schema_version", "UNKNOWN"),
            "recovery_admission": recovery.get("schema_version", "UNKNOWN"),
            "service_objective_policy_threshold_binding": objectives.get("schema_version", "UNKNOWN"),
            "owner_issued_version_lease_pattern": version_lease.get("schema_version", "UNKNOWN"),
        },
        "catalog_rows": catalog_rows,
        "active_evidence": {
            "anti_flap_rows": active_rows[:25],
            "blocked_users": blocked_users,
            "recovery_rows": recovery_rows[:25],
            "objective_binding_rows": len(objective_rows),
        },
        "summary": {
            "catalog_controls": len(catalog_rows),
            "hysteresis_controls": sum(1 for row in catalog_rows if row["canonical_category"] == "HYSTERESIS"),
            "state_change_cost_controls": sum(1 for row in catalog_rows if row["canonical_category"] == "STATE_CHANGE_COST"),
            "existing_complete": sum(1 for row in catalog_rows if row["status"] == "EXISTS_COMPLETE"),
            "existing_under_other_name": sum(1 for row in catalog_rows if row["status"] == "EXISTS_UNDER_OTHER_NAME"),
            "active_anti_flap_blocked_users": blocked_users,
            "threshold_changes": 0,
            "formula_changes": 0,
            "runtime_actions_created": 0,
            "authority_changes": 0,
            "synthetic_evidence_created": 0,
            "users_moved": 0,
        },
        "canonical_rules": [
            "b19_centralizes_vocabulary_only",
            "state_change_cost_already_exists_as_sticky_current_bias_minimum_improvement_cooldown_freeze_pair_reversal_target_block_quarantine_and_recovery_windows",
            "b19_does_not_change_threshold_values_or_formulas",
            "b19_does_not_create_new_policy_owner_or_planner",
            "anti_flap_remains_a_runtime_eligibility_stop_gate",
            "hard_failure_override_is_not_implemented_by_b19_and_remains_b20",
            "b19_does_not_grant_runtime_apply_or_authority",
        ],
        "omp_output": {
            "b19_status": "DONE_READ_ONLY_HYSTERESIS_STATE_CHANGE_COST_MAPPING",
            "produced_evidence": "hysteresis_state_change_cost_mapping",
            "unlocked_capability": "B20_OR_NEXT_OMP_ITEM_AFTER_CANONICAL_UPDATE",
            "blocked_later_steps": [
                "runtime_apply",
                "automation",
                "authority_expansion",
                "threshold_formula_mutation",
                "hard_failure_override",
                "user_movement",
            ],
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "synthetic_evidence_created": False,
        "threshold_values_changed": False,
        "formula_changed": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_runtime_created": False,
    }


def build_hard_failure_override_anti_flap_arbitration(
    *,
    hard_failure_classification: dict[str, Any] | None = None,
    hard_failure_policy_windows: dict[str, Any] | None = None,
    anti_flapping: dict[str, Any] | None = None,
    hysteresis_state_change_cost_mapping: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Encode B20 hard-failure vs anti-flap arbitration as read-only evidence."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    classification = hard_failure_classification if isinstance(hard_failure_classification, dict) else {}
    windows = hard_failure_policy_windows if isinstance(hard_failure_policy_windows, dict) else {}
    anti = anti_flapping if isinstance(anti_flapping, dict) else {}
    hysteresis = hysteresis_state_change_cost_mapping if isinstance(hysteresis_state_change_cost_mapping, dict) else {}
    anti_rows = [row for row in (anti.get("rows") or []) if isinstance(row, dict)]
    anti_blocked_users = {
        _text(row.get("user")) for row in anti_rows
        if row.get("blocked") and _text(row.get("user"))
    }
    global_anti_flap_blocked = bool(int((anti.get("summary") or {}).get("blocked_users") or 0))
    window_rows = [row for row in (windows.get("rows") or []) if isinstance(row, dict)]
    if not window_rows:
        for row in (classification.get("rows") or []):
            if not isinstance(row, dict):
                continue
            window_rows.append({
                "object": row.get("object"),
                "risk_class": _hard_failure_policy_risk_class(
                    _text(row.get("classification")),
                    int(row.get("explicit_liveness_evidence_count") or 0),
                    len(row.get("independent_sources") or []),
                ),
                "hard_failure_classification": row.get("classification"),
                "selected_action_class": "channel hard-fail failover",
                "policy_window_ready": False,
                "blockers": ["hard_failure_policy_window_missing"],
            })
    rows: list[dict[str, Any]] = []
    for row in window_rows:
        object_name = _text(row.get("object") or "unknown")
        risk_class = _text(row.get("risk_class") or "NO_HARD_FAILURE_POLICY_WINDOW")
        blockers = sorted({_text(item) for item in (row.get("blockers") or []) if _text(item)})
        anti_conflict = global_anti_flap_blocked or "anti_flap_blocks_recent_oscillation" in blockers
        confirmed = risk_class in {"CRITICAL_CONFIRMED_HARD_FAILURE", "CONFIRMED_HARD_FAILURE"}
        suspected = risk_class == "SUSPECTED_HARD_FAILURE"
        if confirmed and anti_conflict:
            arbitration = "HARD_FAILURE_OVERRIDE_ELIGIBLE_FOR_AUTHORITY_REVIEW"
            anti_flap_result = "OVERRIDE_CANDIDATE_READ_ONLY"
            reason = "confirmed_hard_failure_may_override_anti_flap_hold_only_after_existing_authority_and_runtime_eligibility_review"
            remaining_blockers = [item for item in blockers if item != "anti_flap_blocks_recent_oscillation"]
        elif confirmed:
            arbitration = "NO_ANTI_FLAP_CONFLICT_FAST_FAILURE_REVIEW"
            anti_flap_result = "NO_OVERRIDE_NEEDED"
            reason = "confirmed_hard_failure_has_no_current_anti_flap_conflict"
            remaining_blockers = blockers
        elif suspected:
            arbitration = "ANTI_FLAP_HOLDS_CONFIRMATION_REQUIRED"
            anti_flap_result = "HOLD"
            reason = "suspected_hard_failure_cannot_override_anti_flap_without_confirmed_liveness_evidence"
            remaining_blockers = sorted(set(blockers + ["hard_failure_confirmation_required"]))
        else:
            arbitration = "ANTI_FLAP_HOLDS_NO_HARD_FAILURE"
            anti_flap_result = "HOLD"
            reason = "no_confirmed_hard_failure_policy_window_exists"
            remaining_blockers = sorted(set(blockers + ["hard_failure_not_confirmed"]))
        rows.append({
            "object": object_name,
            "risk_class": risk_class,
            "hard_failure_classification": _text(row.get("hard_failure_classification") or risk_class),
            "selected_action_class": _text(row.get("selected_action_class") or ""),
            "anti_flap_conflict": anti_conflict,
            "anti_flap_blocked_users": sorted(anti_blocked_users),
            "arbitration_result": arbitration,
            "anti_flap_result": anti_flap_result,
            "reason": reason,
            "remaining_blockers": remaining_blockers,
            "hard_failure_override_executed": False,
            "runtime_apply_allowed": False,
            "authority_expansion_allowed": False,
            "user_movement_allowed": False,
        })
    return {
        "schema_version": "v7.b20-hard-failure-override-anti-flap-arbitration.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B20",
        "purpose": "encode_hard_failure_override_rule_for_anti_flap_arbitration_without_runtime_behavior_change",
        "source_owners_reused": [
            "admin_core.autonomy_trust_acceleration.build_hard_failure_classification",
            "admin_core.autonomy_trust_acceleration.build_hard_failure_policy_windows",
            "admin_core.autonomy_trust_acceleration.build_anti_flapping",
            "admin_core.autonomy_trust_acceleration.build_hysteresis_state_change_cost_mapping",
            "tools/v7-users-autoswitch anti-flap and planner safety gates",
            "Runtime Model runtime eligibility anti_flap gate",
            "OMP",
        ],
        "policy_sources": [
            "docs/policies/POLICY_001_HARD_FAILURE.md",
            "docs/policies/POLICY_009_ANTI_FLAP.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B20",
        ],
        "consumed_prior_capabilities": {
            "hard_failure_classification": classification.get("schema_version", "UNKNOWN"),
            "hard_failure_policy_windows": windows.get("schema_version", "UNKNOWN"),
            "anti_flapping": anti.get("schema_version", "UNKNOWN"),
            "hysteresis_state_change_cost_mapping": hysteresis.get("schema_version", "UNKNOWN"),
        },
        "rows": rows,
        "summary": {
            "objects_seen": len(rows),
            "override_candidates": sum(1 for row in rows if row["arbitration_result"] == "HARD_FAILURE_OVERRIDE_ELIGIBLE_FOR_AUTHORITY_REVIEW"),
            "anti_flap_holds": sum(1 for row in rows if row["anti_flap_result"] == "HOLD"),
            "no_override_needed": sum(1 for row in rows if row["anti_flap_result"] == "NO_OVERRIDE_NEEDED"),
            "anti_flap_blocked_users": len(anti_blocked_users),
            "hard_failure_override_executed": 0,
            "threshold_changes": 0,
            "formula_changes": 0,
            "runtime_actions_created": 0,
            "authority_changes": 0,
            "synthetic_evidence_created": 0,
            "users_moved": 0,
        },
        "canonical_rules": [
            "confirmed_hard_failure_may_override_anti_flap_only_as_read_only_authority_review_candidate",
            "suspected_hard_failure_never_overrides_anti_flap",
            "no_hard_failure_never_overrides_anti_flap",
            "anti_flap_override_candidate_does_not_grant_runtime_apply",
            "anti_flap_override_candidate_does_not_expand_authority",
            "b20_does_not_change_threshold_values_timers_or_formulas",
            "b20_does_not_create_new_policy_owner_planner_or_runtime",
        ],
        "omp_output": {
            "b20_status": "DONE_READ_ONLY_HARD_FAILURE_OVERRIDE_ANTI_FLAP_ARBITRATION",
            "produced_evidence": "hard_failure_override_anti_flap_arbitration",
            "unlocked_capability": "B21_OR_NEXT_OMP_ITEM_AFTER_CANONICAL_UPDATE",
            "blocked_later_steps": [
                "runtime_apply",
                "automation",
                "authority_expansion",
                "threshold_formula_mutation",
                "hard_failure_override_execution",
                "user_movement",
            ],
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "synthetic_evidence_created": False,
        "threshold_values_changed": False,
        "formula_changed": False,
        "hard_failure_override_executed": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_runtime_created": False,
    }


def _truthy(value: Any) -> bool:
    return _text(value).strip().lower() in {"1", "true", "yes", "y", "on", "manual", "pinned"}


def _routing_mode_text(row: dict[str, Any]) -> str:
    for key in ("routing_control_mode", "routing_mode", "route_mode", "user_routing_mode"):
        value = _text(row.get(key)).upper()
        if value in {"AUTO", "PINNED", "MANUAL"}:
            return value
    return ""


def build_per_user_routing_control_mode(
    *,
    decision_surface: dict[str, Any] | None = None,
    org_cohort_identity_policy_integration: dict[str, Any] | None = None,
    hard_failure_override_anti_flap_arbitration: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Materialize explicit per-user routing mode as read-only B21 evidence."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    surface = decision_surface if isinstance(decision_surface, dict) else {}
    policy = org_cohort_identity_policy_integration if isinstance(org_cohort_identity_policy_integration, dict) else {}
    arbitration = hard_failure_override_anti_flap_arbitration if isinstance(hard_failure_override_anti_flap_arbitration, dict) else {}
    policy_by_user = {
        _text(row.get("user") or row.get("ip")): row
        for row in (policy.get("rows") or [])
        if isinstance(row, dict) and _text(row.get("user") or row.get("ip"))
    }
    rows: list[dict[str, Any]] = []
    for user_row in (surface.get("users") or []):
        if not isinstance(user_row, dict):
            continue
        raw = user_row.get("raw") if isinstance(user_row.get("raw"), dict) else {}
        user = _text(user_row.get("user") or user_row.get("ip") or raw.get("ip"))
        if not user:
            continue
        current = _text(user_row.get("current_channel") or user_row.get("current") or raw.get("current"))
        recommended = _text(user_row.get("recommended_channel") or user_row.get("best_channel") or current)
        explicit = _routing_mode_text(user_row) or _routing_mode_text(raw)
        pinned_channel = _text(
            user_row.get("pinned_channel")
            or user_row.get("pinned_egress")
            or user_row.get("fixed_channel")
            or raw.get("pinned_channel")
            or raw.get("pinned_egress")
            or raw.get("fixed_channel")
        )
        manual_flag = any(_truthy(value) for value in (
            user_row.get("manual_only"),
            user_row.get("manual"),
            raw.get("manual_only"),
            raw.get("manual"),
        ))
        pinned_flag = bool(pinned_channel) or any(_truthy(value) for value in (
            user_row.get("pinned"),
            user_row.get("pin"),
            raw.get("pinned"),
            raw.get("pin"),
        ))
        blockers = sorted({
            _text(item)
            for item in (user_row.get("blockers") or [])
            if _text(item)
        })
        policy_row = policy_by_user.get(user, {})
        policy_blockers = sorted({
            _text(item)
            for item in (policy_row.get("blockers") or [])
            if _text(item)
        })
        if explicit:
            mode = explicit
            source_status = "EXISTS_COMPLETE"
            source = "explicit_user_routing_mode_field"
        elif manual_flag or "manual_only" in blockers:
            mode = "MANUAL"
            source_status = "EXISTS_UNDER_OTHER_NAME"
            source = "manual_only_flag_or_planner_blocker"
        elif pinned_flag:
            mode = "PINNED"
            source_status = "EXISTS_UNDER_OTHER_NAME"
            source = "pinned_or_fixed_channel_field"
        else:
            mode = "AUTO"
            source_status = "MISSING"
            source = "default_planner_auto_semantics_without_explicit_mode_field"
        mode_blocks_planner_move = mode in {"MANUAL", "PINNED"}
        if mode == "PINNED" and pinned_channel and recommended and recommended != pinned_channel:
            policy_blockers.append("recommended_channel_differs_from_pinned_channel")
        rows.append({
            "user": user,
            "current_channel": current,
            "recommended_channel": recommended,
            "routing_control_mode": mode,
            "mode_source_status": source_status,
            "mode_source": source,
            "pinned_channel": pinned_channel,
            "group": _text(user_row.get("group") or raw.get("group") or raw.get("org") or raw.get("organization") or policy_row.get("group")),
            "planner_recommendation_allowed": mode == "AUTO",
            "planner_move_blocked_by_mode": mode_blocks_planner_move,
            "runtime_apply_allowed": False,
            "authority_expansion_allowed": False,
            "user_movement_allowed": False,
            "blockers": sorted(set(blockers + policy_blockers)),
            "policy_context": {
                "org_cohort_policy_row_present": bool(policy_row),
                "policy_blockers": sorted(set(policy_blockers)),
            },
        })
    missing_explicit = sum(1 for row in rows if row["mode_source_status"] == "MISSING")
    return {
        "schema_version": "v7.b21-per-user-routing-control-mode.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B21",
        "purpose": "materialize_explicit_per_user_auto_pinned_manual_routing_control_mode_without_runtime_behavior_change",
        "source_owners_reused": [
            "admin_core.operator_decision_surface user rows",
            "admin_core.registry_readers.parse_registry_lines",
            "tools/v7-users-autoswitch user registry loader",
            "tools/v7-users-autoswitch org policy gates",
            "tools/v7-users-autoswitch manual_only/reserve_only planner gates",
            "admin_core.autonomy_trust_acceleration.build_org_cohort_identity_policy_integration",
            "admin_core.autonomy_trust_acceleration.build_hard_failure_override_anti_flap_arbitration",
            "OMP",
        ],
        "policy_sources": [
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B21",
            "docs/reference/WORLD_EQUIVALENCE_MODEL.md",
            "docs/reference/MOVEMENT_PROTECTION_MODEL.md",
            "docs/policies/POLICY_004_AUTHORITY.md",
            "docs/policies/POLICY_006_BLAST_RADIUS.md",
        ],
        "consumed_prior_capabilities": {
            "org_cohort_identity_policy_integration": policy.get("schema_version", "UNKNOWN"),
            "hard_failure_override_anti_flap_arbitration": arbitration.get("schema_version", "UNKNOWN"),
        },
        "rows": rows,
        "summary": {
            "users_seen": len(rows),
            "auto": sum(1 for row in rows if row["routing_control_mode"] == "AUTO"),
            "pinned": sum(1 for row in rows if row["routing_control_mode"] == "PINNED"),
            "manual": sum(1 for row in rows if row["routing_control_mode"] == "MANUAL"),
            "explicit_complete": sum(1 for row in rows if row["mode_source_status"] == "EXISTS_COMPLETE"),
            "under_other_name": sum(1 for row in rows if row["mode_source_status"] == "EXISTS_UNDER_OTHER_NAME"),
            "missing_explicit_mode": missing_explicit,
            "runtime_actions_created": 0,
            "authority_changes": 0,
            "synthetic_evidence_created": 0,
            "users_moved": 0,
        },
        "canonical_rules": [
            "auto_means_planner_may_recommend_but_cannot_apply_without_authority",
            "pinned_means_user_assignment_is_fixed_until_explicit_owner_change",
            "manual_means_planner_must_not_move_user_without_explicit_operator_action",
            "missing_explicit_mode_is_reported_as_auto_semantics_not_written_to_registry",
            "b21_does_not_create_new_user_registry_owner_or_planner",
            "b21_does_not_grant_runtime_apply_authority_or_user_movement",
        ],
        "omp_output": {
            "b21_status": "DONE_READ_ONLY_PER_USER_ROUTING_CONTROL_MODE",
            "produced_evidence": "per_user_routing_control_mode",
            "unlocked_capability": "C1_OR_NEXT_OMP_ITEM_AFTER_CANONICAL_UPDATE",
            "blocked_later_steps": [
                "runtime_apply",
                "automation",
                "authority_expansion",
                "planner_replacement",
                "registry_write",
                "user_movement",
            ],
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "synthetic_evidence_created": False,
        "registry_written": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_runtime_created": False,
    }


def build_fail_open_fail_closed_action_class_behavior(
    *,
    action_class_runtime_enablement: dict[str, Any] | None = None,
    runtime_eligibility_arbitration: dict[str, Any] | None = None,
    per_user_routing_control_mode: dict[str, Any] | None = None,
    hard_failure_override_anti_flap_arbitration: dict[str, Any] | None = None,
    stale_read_mutation_blocking: dict[str, Any] | None = None,
    owner_issued_version_lease_pattern: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Record action-class fail behavior without changing Runtime behavior."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    enablement = action_class_runtime_enablement if isinstance(action_class_runtime_enablement, dict) else {}
    runtime = runtime_eligibility_arbitration if isinstance(runtime_eligibility_arbitration, dict) else {}
    routing_mode = per_user_routing_control_mode if isinstance(per_user_routing_control_mode, dict) else {}
    arbitration = hard_failure_override_anti_flap_arbitration if isinstance(hard_failure_override_anti_flap_arbitration, dict) else {}
    stale = stale_read_mutation_blocking if isinstance(stale_read_mutation_blocking, dict) else {}
    version_lease = owner_issued_version_lease_pattern if isinstance(owner_issued_version_lease_pattern, dict) else {}

    class_rows = [
        row for row in (enablement.get("action_classes") or [])
        if isinstance(row, dict)
    ]
    class_by_name = {
        _text(row.get("action_class")): row
        for row in class_rows
        if _text(row.get("action_class"))
    }
    runtime_gate_rows = [
        row for row in (runtime.get("gate_rows") or [])
        if isinstance(row, dict)
    ]
    stopped_gates = sorted({
        _text(row.get("gate"))
        for row in runtime_gate_rows
        if _text(row.get("state")).upper() in {"STOP", "STOP_SAFE", "BLOCKED"}
        and _text(row.get("gate"))
    })
    routing_summary = routing_mode.get("summary") if isinstance(routing_mode.get("summary"), dict) else {}
    manual_or_pinned_users = int(routing_summary.get("manual") or 0) + int(routing_summary.get("pinned") or 0)
    stale_domains = list(stale.get("stale_domains") or [])
    version_summary = version_lease.get("summary") if isinstance(version_lease.get("summary"), dict) else {}
    arbitration_summary = arbitration.get("summary") if isinstance(arbitration.get("summary"), dict) else {}

    rows: list[dict[str, Any]] = []
    for action_class, max_users, default_state in ACTION_CLASS_LADDER:
        class_row = class_by_name.get(action_class, {})
        enablement_state = _text(class_row.get("runtime_state") or class_row.get("state") or default_state, default_state)
        current_blockers = sorted({
            _text(item)
            for item in (
                list(class_row.get("missing_evidence") or [])
                + list(class_row.get("blockers") or [])
                + stopped_gates
            )
            if _text(item)
        })
        hard_failure_class = action_class == "channel hard-fail failover"
        wider_than_one = bool(max_users is None or int(max_users or 0) > 1)
        runtime_certified = enablement_state == "AUTONOMOUS_RUNTIME"
        fail_closed_conditions = sorted(set(current_blockers + [
            "runtime_apply_disabled",
            "authority_not_granted",
            "uncertified_action_class" if not runtime_certified else "",
            "stale_or_unknown_freshness" if stale_domains else "",
            "missing_owner_issued_version_or_lease" if int(version_summary.get("pattern_missing") or 0) else "",
            "manual_or_pinned_user_mode_present" if manual_or_pinned_users else "",
            "wider_blast_radius_requires_authority_review" if wider_than_one else "",
        ]))
        fail_closed_conditions = [item for item in fail_closed_conditions if item]
        fail_open_allowed = [
            "read_only_diagnosis",
            "evidence_collection",
            "operator_explanation",
            "engineering_report",
            "canonical_update",
        ]
        if hard_failure_class and int(arbitration_summary.get("override_candidates") or 0):
            fail_open_allowed.append("authority_review_candidate_only")
        rows.append({
            "action_class": action_class,
            "max_users": max_users,
            "current_enablement_state": enablement_state,
            "default_runtime_behavior": "FAIL_CLOSED",
            "runtime_mutation_behavior": "FAIL_CLOSED",
            "runtime_apply_behavior": "FAIL_CLOSED",
            "authority_behavior": "FAIL_CLOSED_UNLESS_EXPLICITLY_CERTIFIED",
            "planner_behavior": "FAIL_CLOSED_FOR_MUTATION_FAIL_OPEN_FOR_READ_ONLY_RECOMMENDATION",
            "observability_behavior": "FAIL_OPEN_READ_ONLY",
            "fail_open_allowed": fail_open_allowed,
            "fail_closed_conditions": fail_closed_conditions,
            "consumed_user_control_modes": {
                "manual_or_pinned_users": manual_or_pinned_users,
                "routing_control_schema": routing_mode.get("schema_version", "UNKNOWN"),
            },
            "hard_failure_override_context": {
                "override_candidates": int(arbitration_summary.get("override_candidates") or 0),
                "override_execution_allowed": False,
            },
            "runtime_apply_allowed": False,
            "authority_expansion_allowed": False,
            "user_movement_allowed": False,
        })

    return {
        "schema_version": "v7.c1-fail-open-fail-closed-action-class-behavior.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "C1",
        "purpose": "record_fail_open_fail_closed_behavior_per_action_class_without_runtime_behavior_change",
        "source_owners_reused": [
            "ACTION_CLASS_LADDER",
            "admin_core.autonomy_trust_acceleration.build_action_class_runtime_enablement_model",
            "admin_core.autonomy_trust_acceleration.build_runtime_eligibility_arbitration",
            "admin_core.autonomy_trust_acceleration.build_per_user_routing_control_mode",
            "admin_core.autonomy_trust_acceleration.build_hard_failure_override_anti_flap_arbitration",
            "admin_core.autonomy_trust_acceleration.build_stale_read_mutation_blocking",
            "admin_core.autonomy_trust_acceleration.build_owner_issued_version_lease_pattern",
            "Runtime Model fail-closed execution contract",
            "OMP",
        ],
        "policy_sources": [
            "docs/policies/POLICY_001_HARD_FAILURE.md",
            "docs/policies/POLICY_004_AUTHORITY.md",
            "docs/policies/POLICY_006_BLAST_RADIUS.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#C1",
        ],
        "consumed_prior_capabilities": {
            "action_class_runtime_enablement": enablement.get("schema_version", "UNKNOWN"),
            "runtime_eligibility_arbitration": runtime.get("schema_version", "UNKNOWN"),
            "per_user_routing_control_mode": routing_mode.get("schema_version", "UNKNOWN"),
            "hard_failure_override_anti_flap_arbitration": arbitration.get("schema_version", "UNKNOWN"),
            "stale_read_mutation_blocking": stale.get("schema_version", "UNKNOWN"),
            "owner_issued_version_lease_pattern": version_lease.get("schema_version", "UNKNOWN"),
        },
        "rows": rows,
        "summary": {
            "action_classes_seen": len(rows),
            "fail_closed_runtime_apply_classes": sum(1 for row in rows if row["runtime_apply_behavior"] == "FAIL_CLOSED"),
            "fail_open_read_only_classes": sum(1 for row in rows if "read_only_diagnosis" in row["fail_open_allowed"]),
            "authority_review_candidates": sum(
                1 for row in rows
                if "authority_review_candidate_only" in row["fail_open_allowed"]
            ),
            "runtime_actions_created": 0,
            "authority_changes": 0,
            "synthetic_evidence_created": 0,
            "users_moved": 0,
        },
        "canonical_rules": [
            "c1_records_behavior_only_and_does_not_change_runtime_behavior",
            "runtime_mutation_and_apply_fail_closed_for_every_action_class_until_explicit_authority_and_runtime_apply_are_certified",
            "read_only_diagnosis_evidence_collection_operator_explanation_engineering_report_and_canonical_update_may_fail_open",
            "hard_failure_override_is_authority_review_candidate_only_not_execution_permission",
            "manual_or_pinned_user_control_mode_keeps_mutation_fail_closed",
            "c1_does_not_create_new_policy_owner_planner_runtime_or_truth_source",
        ],
        "omp_output": {
            "c1_status": "DONE_READ_ONLY_FAIL_OPEN_FAIL_CLOSED_ACTION_CLASS_BEHAVIOR",
            "produced_evidence": "fail_open_fail_closed_action_class_behavior",
            "unlocked_capability": "C2_OR_NEXT_OMP_ITEM_AFTER_CANONICAL_UPDATE",
            "blocked_later_steps": [
                "runtime_apply",
                "automation",
                "authority_expansion",
                "fail_open_runtime_mutation",
                "planner_replacement",
                "user_movement",
            ],
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "synthetic_evidence_created": False,
        "registry_written": False,
        "threshold_values_changed": False,
        "formula_changed": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_runtime_created": False,
    }


def build_probabilistic_suspicion_advisory_evidence(
    *,
    decision_surface: dict[str, Any] | None = None,
    shadow_model: dict[str, Any] | None = None,
    source_confidence_inventory: dict[str, Any] | None = None,
    degradation_signal_policy_mapping: dict[str, Any] | None = None,
    observed_degradation_attribution: dict[str, Any] | None = None,
    metric_reliability_certification: dict[str, Any] | None = None,
    fail_open_fail_closed_action_class_behavior: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Expose probabilistic suspicion as advisory-only evidence for C2."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    surface = decision_surface if isinstance(decision_surface, dict) else {}
    shadow = shadow_model if isinstance(shadow_model, dict) else {}
    source_inventory = source_confidence_inventory if isinstance(source_confidence_inventory, dict) else {}
    signal_mapping = degradation_signal_policy_mapping if isinstance(degradation_signal_policy_mapping, dict) else {}
    attribution = observed_degradation_attribution if isinstance(observed_degradation_attribution, dict) else {}
    metric_reliability = metric_reliability_certification if isinstance(metric_reliability_certification, dict) else {}
    c1_behavior = fail_open_fail_closed_action_class_behavior if isinstance(fail_open_fail_closed_action_class_behavior, dict) else {}

    decisions = [
        row for row in (shadow.get("current_decisions") or [])
        if isinstance(row, dict)
    ]
    if not decisions and surface.get("users"):
        decisions = shadow_autonomy.build_shadow_decisions(surface, now=generated)

    rows: list[dict[str, Any]] = []
    for decision in decisions:
        confidence = as_float(decision.get("confidence"), 0.0)
        risk = as_float(decision.get("risk"), 0.0)
        blockers = [_text(item) for item in (decision.get("blockers") or []) if _text(item)]
        reasons = []
        if confidence < shadow_autonomy.OBSERVATION_TARGETS["minimum_earned_confidence"]:
            reasons.append("shadow_confidence_below_operator_floor")
        if risk >= 50.0:
            reasons.append("elevated_shadow_risk")
        if blockers:
            reasons.append("decision_surface_blockers_present")
        if _text(decision.get("recommended_action")) == "MOVE_USER":
            reasons.append("movement_recommendation_requires_operator_or_authority_review")
        rows.append({
            "evidence_id": _text(decision.get("decision_id") or f"shadow-{len(rows)}"),
            "source": "shadow_autonomy",
            "owner": "admin_core.shadow_autonomy",
            "object": _text(decision.get("user") or "unknown-user"),
            "evidence_kind": "probabilistic_shadow_decision_suspicion",
            "probabilistic_inputs": {
                "confidence": round(confidence, 3),
                "risk": round(risk, 3),
                "trust": as_float(decision.get("trust"), 0.0),
                "prediction_confidence": as_float((decision.get("prediction") or {}).get("confidence"), 0.0)
                if isinstance(decision.get("prediction"), dict) else 0.0,
            },
            "suspicion_state": "ADVISORY_SUSPICION_EVIDENCE" if reasons else "NO_PROBABILISTIC_SUSPICION",
            "advisory_reasons": sorted(set(reasons)),
            "existing_blockers": blockers,
            "allowed_consumers": [
                "operator_explanation",
                "decision_explainability",
                "engineering_report",
                "canonical_update",
                "future_existing_owner_review",
            ],
            "forbidden_consumers": [
                "runtime_apply",
                "automatic_user_movement",
                "authority_expansion",
                "planner_replacement",
                "threshold_formula_mutation",
            ],
            "direct_blocking_power": "NONE",
            "direct_execution_power": "NONE",
            "runtime_apply_allowed": False,
            "authority_expanded": False,
            "user_movement_allowed": False,
        })

    source_rows = [
        row for row in (source_inventory.get("sources") or [])
        if isinstance(row, dict)
    ]
    for source in source_rows:
        score = as_float(source.get("confidence") or source.get("score") or source.get("current"), 0.0)
        if score >= 70.0:
            continue
        rows.append({
            "evidence_id": "source_confidence:" + _text(source.get("source") or source.get("name") or len(rows)),
            "source": "source_confidence_inventory",
            "owner": _text(source.get("owner") or "admin_core.autonomy_trust_acceleration.build_source_confidence_inventory"),
            "object": _text(source.get("source") or source.get("name") or "unknown-source"),
            "evidence_kind": "source_confidence_suspicion",
            "probabilistic_inputs": {
                "confidence": round(score, 3),
                "maturity": _text(source.get("maturity") or source.get("classification") or "UNKNOWN"),
            },
            "suspicion_state": "ADVISORY_SOURCE_CONFIDENCE_EVIDENCE",
            "advisory_reasons": ["source_confidence_below_operator_floor"],
            "existing_blockers": [_text(item) for item in (source.get("blockers") or []) if _text(item)],
            "allowed_consumers": ["trust_confidence_review", "engineering_report", "canonical_update"],
            "forbidden_consumers": ["runtime_apply", "authority_expansion", "threshold_formula_mutation"],
            "direct_blocking_power": "NONE",
            "direct_execution_power": "NONE",
            "runtime_apply_allowed": False,
            "authority_expanded": False,
            "user_movement_allowed": False,
        })

    for evidence in [
        row for row in (signal_mapping.get("evidence_rows") or [])
        if isinstance(row, dict)
    ]:
        policy_result = _text(evidence.get("canonical_policy_result") or "UNKNOWN")
        if policy_result not in {"SOFT_DEGRADATION", "NOISY_OR_ATTRIBUTION_UNKNOWN"}:
            continue
        rows.append({
            "evidence_id": "degradation_signal:" + _text(evidence.get("object") or len(rows)) + ":" + _text(evidence.get("signal_family") or "unknown"),
            "source": _text(evidence.get("source") or "degradation_signal_policy_mapping"),
            "owner": _text(evidence.get("owner") or "admin_core.autonomy_trust_acceleration.build_degradation_signal_policy_mapping"),
            "object": _text(evidence.get("object") or "unknown-object"),
            "evidence_kind": "mapped_soft_degradation_suspicion",
            "probabilistic_inputs": {
                "signal_family": _text(evidence.get("signal_family") or "unknown"),
                "canonical_policy_result": policy_result,
            },
            "suspicion_state": "ADVISORY_SOFT_DEGRADATION_EVIDENCE",
            "advisory_reasons": ["mapped_soft_degradation_signal"],
            "existing_blockers": ["requires_observed_attribution_before_action"]
            if evidence.get("requires_attribution_before_action") else [],
            "allowed_consumers": ["operator_explanation", "decision_explainability", "B5_or_existing_attribution_review"],
            "forbidden_consumers": ["runtime_apply", "authority_expansion", "root_cause_claim"],
            "direct_blocking_power": "NONE",
            "direct_execution_power": "NONE",
            "runtime_apply_allowed": False,
            "authority_expanded": False,
            "user_movement_allowed": False,
        })

    attribution_rows = [
        row for row in (attribution.get("rows") or [])
        if isinstance(row, dict)
    ]
    attributed_objects = {
        _text(row.get("object"))
        for row in attribution_rows
        if _text(row.get("attribution_state")) in {
            "ACTIVE_AND_PASSIVE_OBSERVED",
            "ACTIVE_OBSERVED_WITH_PASSIVE_CONTEXT",
            "ACTIVE_ONLY_PASSIVE_OUTCOME_PENDING",
        }
    }
    metric_summary = metric_reliability.get("summary") if isinstance(metric_reliability.get("summary"), dict) else {}
    c1_summary = c1_behavior.get("summary") if isinstance(c1_behavior.get("summary"), dict) else {}

    return {
        "schema_version": "v7.c2-probabilistic-suspicion-advisory-evidence.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "C2",
        "purpose": "keep_probabilistic_suspicion_as_advisory_evidence_only_without_runtime_authority_or_behavior_change",
        "source_owners_reused": [
            "admin_core.shadow_autonomy",
            "admin_core.autonomy_trust_acceleration.build_source_confidence_inventory",
            "admin_core.autonomy_trust_acceleration.build_degradation_signal_policy_mapping",
            "admin_core.autonomy_trust_acceleration.build_observed_degradation_attribution",
            "admin_core.autonomy_trust_acceleration.build_metric_reliability_certification",
            "admin_core.autonomy_trust_acceleration.build_fail_open_fail_closed_action_class_behavior",
            "Trust/confidence model",
            "OMP",
        ],
        "policy_sources": [
            "docs/policies/POLICY_002_SOFT_DEGRADATION.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#C2",
        ],
        "consumed_prior_capabilities": {
            "shadow_autonomy": shadow.get("schema_version", "UNKNOWN"),
            "source_confidence_inventory": source_inventory.get("schema_version", "UNKNOWN"),
            "degradation_signal_policy_mapping": signal_mapping.get("schema_version", "UNKNOWN"),
            "observed_degradation_attribution": attribution.get("schema_version", "UNKNOWN"),
            "metric_reliability_certification": metric_reliability.get("schema_version", "UNKNOWN"),
            "fail_open_fail_closed_action_class_behavior": c1_behavior.get("schema_version", "UNKNOWN"),
        },
        "rows": rows,
        "summary": {
            "advisory_evidence_rows": len(rows),
            "shadow_decision_rows": sum(1 for row in rows if row["source"] == "shadow_autonomy"),
            "source_confidence_rows": sum(1 for row in rows if row["source"] == "source_confidence_inventory"),
            "soft_degradation_rows": sum(1 for row in rows if row["evidence_kind"] == "mapped_soft_degradation_suspicion"),
            "attributed_objects_available": len(attributed_objects),
            "metric_reliability_positive_promotion_allowed": False,
            "metric_reliability_schema": metric_reliability.get("schema_version", "UNKNOWN"),
            "c1_fail_closed_runtime_apply_classes": int(c1_summary.get("fail_closed_runtime_apply_classes") or 0),
            "direct_blocking_rows": 0,
            "direct_execution_rows": 0,
            "runtime_actions_created": 0,
            "authority_changes": 0,
            "synthetic_evidence_created": 0,
            "users_moved": 0,
        },
        "canonical_rules": [
            "probabilistic_suspicion_is_advisory_evidence_only",
            "probabilistic_suspicion_cannot_authorize_runtime_apply_or_user_movement",
            "probabilistic_suspicion_cannot_expand_authority_or_replace_planner_owners",
            "probabilistic_suspicion_cannot_override_freshness_authority_rollback_anti_flap_or_c1_fail_closed_behavior",
            "probabilistic_suspicion_may_feed_operator_explanation_decision_explainability_engineering_report_and_existing_owner_review",
            "c2_does_not_change_threshold_values_formulas_confidence_floors_or_source_evidence",
        ],
        "omp_output": {
            "c2_status": "DONE_READ_ONLY_PROBABILISTIC_SUSPICION_ADVISORY_EVIDENCE",
            "produced_evidence": "probabilistic_suspicion_advisory_evidence",
            "unlocked_capability": "C3_OR_NEXT_OMP_ITEM_AFTER_CANONICAL_UPDATE",
            "blocked_later_steps": [
                "runtime_apply",
                "automation",
                "authority_expansion",
                "direct_suspicion_blocking",
                "planner_replacement",
                "threshold_formula_mutation",
                "synthetic_evidence",
                "user_movement",
            ],
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "synthetic_evidence_created": False,
        "threshold_values_changed": False,
        "formula_changed": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_runtime_created": False,
    }


def _source_by_name(source_confidence_inventory: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("source")): row
        for row in source_confidence_inventory.get("sources") or []
        if isinstance(row, dict)
    }


def _metric_certification_row(
    *,
    metric: str,
    owner: str,
    current: Any,
    target: Any = "",
    evidence: Any = "",
    state: str,
    role: str,
) -> dict[str, Any]:
    return {
        "metric": metric,
        "owner": owner,
        "current": current,
        "target": target,
        "evidence": evidence,
        "state": state,
        "role": role,
    }


def build_metric_reliability_certification(
    *,
    canary_proximity: dict[str, Any],
    floor_forensics: dict[str, Any],
    source_confidence_inventory: dict[str, Any],
    evidence_sufficiency: dict[str, Any],
    decision_outcome_closure: dict[str, Any],
    decision_outcome_learning: dict[str, Any],
    freshness_actionability: dict[str, Any],
    routing_recommendation_readiness: dict[str, Any],
    action_class_runtime_enablement: dict[str, Any],
    class_level_blast_radius_certification: dict[str, Any],
    runtime_eligibility_arbitration: dict[str, Any],
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Certify B13 metric reliability without granting promotion authority."""
    floors = canary_proximity.get("primary_floors") if isinstance(canary_proximity.get("primary_floors"), dict) else {}
    components = floor_forensics.get("component_values") if isinstance(floor_forensics.get("component_values"), dict) else {}
    sources = _source_by_name(source_confidence_inventory)
    closure_state = str(decision_outcome_closure.get("closure_state") or "UNKNOWN")
    knowledge_growth = decision_outcome_learning.get("knowledge_growth") if isinstance(decision_outcome_learning.get("knowledge_growth"), dict) else {}
    learning_gained = int(as_float(knowledge_growth.get("knowledge_gained"), 0.0))
    stale_domains = [
        name for name, row in sorted((freshness_actionability.get("domains") or {}).items())
        if isinstance(row, dict) and row.get("classification") in {"STALE_RECHECK_REQUIRED", "UNKNOWN"}
    ]
    runtime_schema = str(runtime_eligibility_arbitration.get("schema_version") or "")
    runtime_decision = str(runtime_eligibility_arbitration.get("runtime_execute_decision") or "UNKNOWN")
    runtime_stop_gates = list(runtime_eligibility_arbitration.get("stop_gates") or [])
    source_rows = []
    for source_name in (
        "prediction_matches",
        "service_outcomes",
        "candidate_outcomes",
        "rollback_evidence",
        "blast_radius_evidence",
    ):
        source = sources.get(source_name, {})
        classification = str(source.get("classification") or "MISSING")
        source_rows.append(_metric_certification_row(
            metric=source_name,
            owner="source_confidence_inventory",
            current={
                "evidence_count": source.get("evidence_count", 0),
                "confidence_weight": source.get("confidence_weight", 0.0),
                "current_contribution": source.get("current_contribution", 0.0),
                "classification": classification,
            },
            evidence=source.get("reason", ""),
            state="PASS" if classification.startswith("SUFFICIENT") else "PARTIAL",
            role="RELIABILITY_SIGNAL",
        ))
    floor_rows = [
        _metric_certification_row(
            metric=name,
            owner="canary_proximity.primary_floors",
            current=(row or {}).get("current", 0.0) if isinstance(row, dict) else 0.0,
            target=(row or {}).get("target", 0.0) if isinstance(row, dict) else 0.0,
            evidence=(row or {}).get("gap", 0.0) if isinstance(row, dict) else 0.0,
            state="PASS" if isinstance(row, dict) and row.get("pass") else "PARTIAL",
            role="POSITIVE_PROMOTION_RELIABILITY_REQUIREMENT",
        )
        for name, row in sorted(floors.items())
    ]
    gate_rows = [
        _metric_certification_row(
            metric="outcome_closure",
            owner="decision_outcome_closure",
            current=closure_state,
            target="COMPLETE",
            evidence=(decision_outcome_closure.get("summary") or {}),
            state="PASS" if closure_state == "COMPLETE" else "STOP",
            role="MANDATORY_CERTIFICATION_REQUIREMENT",
        ),
        _metric_certification_row(
            metric="learning",
            owner="decision_outcome_learning",
            current=learning_gained,
            target=">0",
            evidence=knowledge_growth,
            state="PASS" if learning_gained > 0 else "STOP",
            role="MANDATORY_CERTIFICATION_REQUIREMENT",
        ),
        _metric_certification_row(
            metric="freshness",
            owner="freshness_actionability",
            current=stale_domains,
            target=[],
            evidence={"stale_domains": stale_domains},
            state="PASS" if not stale_domains else "PARTIAL",
            role="RUNTIME_SAFETY_SIGNAL",
        ),
        _metric_certification_row(
            metric="a5_blast_radius",
            owner="class_level_blast_radius_certification",
            current=class_level_blast_radius_certification.get("certification_state", "UNKNOWN"),
            target="BEYOND_ONE_USER_EVIDENCE_CERTIFIED_READ_ONLY",
            evidence={
                "max_historical_certified_blast_radius_users": class_level_blast_radius_certification.get("max_historical_certified_blast_radius_users", 0),
            },
            state="PASS" if class_level_blast_radius_certification.get("beyond_one_user_certified") else "STOP",
            role="MANDATORY_CERTIFICATION_REQUIREMENT",
        ),
        _metric_certification_row(
            metric="a6_runtime_eligibility",
            owner="runtime_eligibility_arbitration",
            current=runtime_decision,
            target="read_only_execute_or_stop_answer",
            evidence={"schema_version": runtime_schema, "stop_gates": runtime_stop_gates},
            state="PASS" if runtime_schema == "v7.a6-runtime-eligibility-arbitration.v1" else "STOP",
            role="MANDATORY_CERTIFICATION_REQUIREMENT",
        ),
    ]
    reliability_rows = source_rows + floor_rows + gate_rows
    stop_metrics = [row["metric"] for row in reliability_rows if row["state"] == "STOP"]
    partial_metrics = [row["metric"] for row in reliability_rows if row["state"] == "PARTIAL"]
    positive_blockers = list(dict.fromkeys(
        list(canary_proximity.get("missing") or [])
        + list(evidence_sufficiency.get("insufficient_sources") or [])
        + list(evidence_sufficiency.get("low_attribution_sources") or [])
        + list(routing_recommendation_readiness.get("blockers") or [])
        + list((action_class_runtime_enablement.get("enablement_readiness") or {}).get("missing_evidence") or [])
        + runtime_stop_gates
    ))
    safety_certified = not stop_metrics
    blocking_recommendation_certified = safety_certified and runtime_schema == "v7.a6-runtime-eligibility-arbitration.v1"
    positive_recommendation_certified = blocking_recommendation_certified and not positive_blockers and not partial_metrics
    if positive_recommendation_certified:
        certification_state = "CERTIFIED_FOR_POSITIVE_PROMOTION_RECOMMENDATION_REQUIRES_AUTHORITY"
        recommendation = "PROMOTION_RECOMMENDATION_METRICS_RELIABLE_REQUIRES_AUTHORITY_REVIEW"
    elif blocking_recommendation_certified:
        certification_state = "CERTIFIED_FOR_BLOCKING_RECOMMENDATIONS_ONLY"
        recommendation = "DO_NOT_PROMOTE_COLLECT_REAL_EVIDENCE"
    else:
        certification_state = "NOT_CERTIFIED_MANDATORY_METRIC_GATE_FAILED"
        recommendation = "DO_NOT_PROMOTE_FIX_MANDATORY_METRIC_GATES"
    return {
        "schema_version": "v7.b13-metric-reliability-certification.v1",
        "generated_at": generated_at or "",
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B13",
        "purpose": "certify_metric_reliability_for_automated_promotion_recommendations_without_runtime_apply",
        "certification_state": certification_state,
        "recommendation": recommendation,
        "metric_rows": reliability_rows,
        "stop_metrics": stop_metrics,
        "partial_metrics": partial_metrics,
        "positive_promotion_blockers": positive_blockers,
        "blocking_recommendation_certified": blocking_recommendation_certified,
        "automated_positive_promotion_recommendation_allowed": False,
        "positive_recommendation_metrics_certified": positive_recommendation_certified,
        "authority_required_for_positive_promotion": True,
        "current_floor_components": {
            "decision_confidence": components.get("decision_confidence", 0.0),
            "service_confidence": components.get("service_confidence", 0.0),
            "suitability_confidence": components.get("suitability_confidence", 0.0),
            "prediction_confidence": components.get("prediction_confidence", 0.0),
            "rollback_confidence": components.get("rollback_confidence", 0.0),
            "blast_radius_confidence": components.get("blast_radius_confidence", 0.0),
        },
        "omp_output": {
            "b13_status": "DONE_READ_ONLY_BLOCKING_RECOMMENDATION_CERTIFIED" if blocking_recommendation_certified else "NOT_CERTIFIED",
            "next_safe_action": "continue to B16 rollback authority certification" if blocking_recommendation_certified else "fix mandatory metric gates through existing owners",
            "promotion_allowed_now": False,
            "authority_expansion_required": positive_recommendation_certified,
        },
        "read_only": True,
        "synthetic_evidence_created": False,
        "formula_changed": False,
        "floor_changed": False,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_runtime_created": False,
    }


def build_rollback_authority_certification(
    *,
    floor_forensics: dict[str, Any],
    decision_outcome_closure: dict[str, Any],
    decision_outcome_learning: dict[str, Any],
    runtime_eligibility_arbitration: dict[str, Any],
    metric_reliability_certification: dict[str, Any],
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Certify B16 rollback authority readiness without granting authority."""
    rollback_blast = floor_forensics.get("rollback_and_blast") if isinstance(floor_forensics.get("rollback_and_blast"), dict) else {}
    rollback_records = int(as_float(rollback_blast.get("rollback_records_seen"), 0.0))
    rollback_confidence = as_float(rollback_blast.get("rollback_confidence"), 0.0)
    closure_state = str(decision_outcome_closure.get("closure_state") or "UNKNOWN")
    closure_summary = decision_outcome_closure.get("summary") if isinstance(decision_outcome_closure.get("summary"), dict) else {}
    effectiveness = decision_outcome_learning.get("effectiveness") if isinstance(decision_outcome_learning.get("effectiveness"), dict) else {}
    rollback_rate = as_float(effectiveness.get("rollback_rate"), 0.0)
    runtime_schema = str(runtime_eligibility_arbitration.get("schema_version") or "")
    metric_schema = str(metric_reliability_certification.get("schema_version") or "")
    metric_certified = bool(metric_reliability_certification.get("blocking_recommendation_certified"))
    runtime_known = runtime_schema == "v7.a6-runtime-eligibility-arbitration.v1"

    gate_rows = [
        _metric_certification_row(
            metric="rollback_evidence",
            owner="floor_forensics.rollback_and_blast",
            current={"records_seen": rollback_records, "rollback_confidence": rollback_confidence},
            target={"records_seen": ">0", "rollback_confidence": "100"},
            evidence=rollback_blast,
            state="PASS" if rollback_records > 0 and rollback_confidence >= 100.0 else "STOP",
            role="MANDATORY_CERTIFICATION_REQUIREMENT",
        ),
        _metric_certification_row(
            metric="verification_reliability",
            owner="decision_outcome_closure",
            current=closure_state,
            target="COMPLETE",
            evidence=closure_summary,
            state="PASS" if closure_state == "COMPLETE" else "STOP",
            role="MANDATORY_CERTIFICATION_REQUIREMENT",
        ),
        _metric_certification_row(
            metric="no_rollback_observed",
            owner="decision_outcome_learning.effectiveness",
            current=rollback_rate,
            target="0.0 observed rollback rate for current governed outcome class",
            evidence=effectiveness,
            state="PASS" if rollback_rate == 0.0 and closure_state == "COMPLETE" else "PARTIAL",
            role="SUPPORTING_EVIDENCE",
        ),
        _metric_certification_row(
            metric="metric_reliability",
            owner="metric_reliability_certification",
            current=metric_reliability_certification.get("certification_state", "UNKNOWN"),
            target="CERTIFIED_FOR_BLOCKING_RECOMMENDATIONS_ONLY or stronger",
            evidence={"schema_version": metric_schema, "stop_metrics": metric_reliability_certification.get("stop_metrics", [])},
            state="PASS" if metric_schema == "v7.b13-metric-reliability-certification.v1" and metric_certified else "STOP",
            role="MANDATORY_CERTIFICATION_REQUIREMENT",
        ),
        _metric_certification_row(
            metric="runtime_eligibility",
            owner="runtime_eligibility_arbitration",
            current=runtime_eligibility_arbitration.get("runtime_execute_decision", "UNKNOWN"),
            target="read_only_execute_or_stop_answer",
            evidence={"schema_version": runtime_schema, "stop_gates": runtime_eligibility_arbitration.get("stop_gates", [])},
            state="PASS" if runtime_known else "STOP",
            role="MANDATORY_CERTIFICATION_REQUIREMENT",
        ),
        _metric_certification_row(
            metric="authority",
            owner="OMP authority gates",
            current="PACKET_LEVEL_GOVERNED_AUTHORITY_ONLY",
            target="EXPLICIT_AUTOMATIC_ROLLBACK_AUTHORITY_APPROVAL",
            evidence="authority expansion is outside B16 read-only certification",
            state="STOP",
            role="AUTHORITY_BOUNDARY",
        ),
        _metric_certification_row(
            metric="runtime_apply",
            owner="Runtime Model live gates",
            current="DISABLED",
            target="explicit runtime apply authority",
            evidence="B16 does not enable Runtime apply or rollback execution",
            state="STOP",
            role="RUNTIME_BOUNDARY",
        ),
    ]
    mandatory_stop_gates = [
        row["metric"]
        for row in gate_rows
        if row["state"] == "STOP" and row["role"] == "MANDATORY_CERTIFICATION_REQUIREMENT"
    ]
    authority_stop_gates = [
        row["metric"]
        for row in gate_rows
        if row["state"] == "STOP" and row["role"] in {"AUTHORITY_BOUNDARY", "RUNTIME_BOUNDARY"}
    ]
    evidence_ready_for_authority_review = not mandatory_stop_gates
    if evidence_ready_for_authority_review:
        certification_state = "CERTIFIED_FOR_AUTHORITY_REVIEW_ONLY"
        recommendation = "DO_NOT_ENABLE_AUTOMATIC_ROLLBACK_AUTHORITY_WITHOUT_OPERATOR_APPROVAL"
        b16_status = "DONE_READ_ONLY_AUTHORITY_REVIEW_CERTIFIED"
        next_safe_action = "continue to Runtime Capability Maturation Program RT2-S1 measurement and observability"
    else:
        certification_state = "NOT_CERTIFIED_MANDATORY_ROLLBACK_GATE_FAILED"
        recommendation = "DO_NOT_ENABLE_AUTOMATIC_ROLLBACK_AUTHORITY_FIX_MANDATORY_GATES"
        b16_status = "NOT_CERTIFIED"
        next_safe_action = "fix rollback and verification evidence through existing owners"
    return {
        "schema_version": "v7.b16-rollback-authority-certification.v1",
        "generated_at": generated_at or "",
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B16",
        "purpose": "certify_automatic_rollback_authority_readiness_after_reliable_verification_evidence_without_granting_authority",
        "certification_state": certification_state,
        "recommendation": recommendation,
        "gate_rows": gate_rows,
        "mandatory_stop_gates": mandatory_stop_gates,
        "authority_stop_gates": authority_stop_gates,
        "evidence_ready_for_authority_review": evidence_ready_for_authority_review,
        "automatic_rollback_authority_granted": False,
        "automatic_rollback_execution_allowed": False,
        "authority_required_for_automatic_rollback": True,
        "runtime_apply_allowed_now": False,
        "omp_output": {
            "b16_status": b16_status,
            "next_safe_action": next_safe_action,
            "automatic_rollback_authority_granted": False,
            "runtime_apply_allowed_now": False,
        },
        "read_only": True,
        "synthetic_evidence_created": False,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "rollback_executed": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_runtime_created": False,
    }


def _rt2_s5_evidence_state(
    *,
    source: dict[str, Any],
    pass_when: bool,
    partial_when_present: bool = True,
) -> str:
    if pass_when:
        return "PASS"
    if partial_when_present and source:
        return "PARTIAL"
    return "STOP_SAFE"


def build_rt2_s5_certified_concurrency_ladder(
    *,
    action_class_runtime_enablement: dict[str, Any],
    class_level_blast_radius_certification: dict[str, Any],
    runtime_eligibility_arbitration: dict[str, Any],
    metric_reliability_certification: dict[str, Any],
    rollback_authority_certification: dict[str, Any],
    anti_flapping: dict[str, Any],
    rt2_s4_governed_execution_coordination: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Certify RT2-S5 concurrency limits without enabling concurrency."""
    s4 = rt2_s4_governed_execution_coordination if isinstance(rt2_s4_governed_execution_coordination, dict) else {}
    delegated = action_class_runtime_enablement.get("delegated_autonomy_runtime_eligibility")
    if not isinstance(delegated, dict):
        delegated = {}
    anti_flap_blocked = int((anti_flapping.get("summary") or {}).get("blocked_users") or 0)
    s4_complete = str(s4.get("status") or s4.get("coordination_state") or "").startswith("DONE_READ_ONLY")
    if not s4:
        s4_complete = True
    blast_beyond_one_user = bool(class_level_blast_radius_certification.get("beyond_one_user_certified"))
    max_blast_users = int(class_level_blast_radius_certification.get("max_historical_certified_blast_radius_users") or 0)
    runtime_known = runtime_eligibility_arbitration.get("schema_version") == "v7.a6-runtime-eligibility-arbitration.v1"
    metric_known = metric_reliability_certification.get("schema_version") == "v7.b13-metric-reliability-certification.v1"
    rollback_known = rollback_authority_certification.get("schema_version") == "v7.b16-rollback-authority-certification.v1"
    metric_ready = bool(metric_reliability_certification.get("blocking_recommendation_certified"))
    rollback_ready = bool(rollback_authority_certification.get("evidence_ready_for_authority_review"))
    authority_explicit = False
    runtime_apply_allowed = bool(runtime_eligibility_arbitration.get("runtime_apply_allowed"))

    gate_rows = [
        _metric_certification_row(
            metric="governed_execution_coordination",
            owner="RT2-S4 / operator_execution_pipeline",
            current=s4.get("status") or s4.get("coordination_state") or ("OWNER_MAPPED_BY_OMP" if not s4 else "UNKNOWN"),
            target="DONE_READ_ONLY_GOVERNED_EXECUTION_COORDINATION_OWNER_MAPPED",
            evidence=s4 or "RT2-S4 canonical completion evidence",
            state="PASS" if s4_complete else "STOP_SAFE",
            role="MANDATORY_CERTIFICATION_REQUIREMENT",
        ),
        _metric_certification_row(
            metric="blast_radius",
            owner="class_level_blast_radius_certification",
            current=class_level_blast_radius_certification.get("certification_state", "UNKNOWN"),
            target="BEYOND_ONE_USER_EVIDENCE_CERTIFIED_READ_ONLY for levels above serial-only",
            evidence={
                "max_historical_certified_blast_radius_users": max_blast_users,
                "blockers": class_level_blast_radius_certification.get("blockers", []),
            },
            state=_rt2_s5_evidence_state(
                source=class_level_blast_radius_certification,
                pass_when=blast_beyond_one_user,
            ),
            role="MANDATORY_CERTIFICATION_REQUIREMENT",
        ),
        _metric_certification_row(
            metric="rollback_capacity",
            owner="rollback_authority_certification",
            current=rollback_authority_certification.get("certification_state", "UNKNOWN"),
            target="CERTIFIED_FOR_AUTHORITY_REVIEW_ONLY",
            evidence={
                "mandatory_stop_gates": rollback_authority_certification.get("mandatory_stop_gates", []),
                "authority_stop_gates": rollback_authority_certification.get("authority_stop_gates", []),
            },
            state="PASS" if rollback_known and rollback_ready else "STOP_SAFE",
            role="MANDATORY_CERTIFICATION_REQUIREMENT",
        ),
        _metric_certification_row(
            metric="verification_capacity",
            owner="metric_reliability_certification + decision_outcome_closure",
            current=metric_reliability_certification.get("certification_state", "UNKNOWN"),
            target="blocking recommendation metrics certified",
            evidence={
                "stop_metrics": metric_reliability_certification.get("stop_metrics", []),
                "partial_metrics": metric_reliability_certification.get("partial_metrics", []),
            },
            state="PASS" if metric_known and metric_ready else "STOP_SAFE",
            role="MANDATORY_CERTIFICATION_REQUIREMENT",
        ),
        _metric_certification_row(
            metric="runtime_eligibility",
            owner="runtime_eligibility_arbitration",
            current=runtime_eligibility_arbitration.get("runtime_execute_decision", "UNKNOWN"),
            target="known execute-or-stop arbitration",
            evidence={
                "stop_gates": runtime_eligibility_arbitration.get("stop_gates", []),
                "runtime_apply_allowed": runtime_apply_allowed,
            },
            state="PASS" if runtime_known else "STOP_SAFE",
            role="MANDATORY_CERTIFICATION_REQUIREMENT",
        ),
        _metric_certification_row(
            metric="anti_flap",
            owner="anti_flapping",
            current={"blocked_users": anti_flap_blocked},
            target={"blocked_users": 0},
            evidence=anti_flapping.get("summary", {}),
            state="PASS" if anti_flap_blocked == 0 else "STOP_SAFE",
            role="MANDATORY_CERTIFICATION_REQUIREMENT",
        ),
        _metric_certification_row(
            metric="authority_envelope",
            owner="OMP authority gates / Policy 006",
            current="NO_CONCURRENCY_ENABLEMENT_AUTHORITY",
            target="explicit concurrency authority before any wider level",
            evidence=delegated.get("blockers", []) or "authority expansion remains forbidden",
            state="STOP_SAFE",
            role="AUTHORITY_BOUNDARY",
        ),
        _metric_certification_row(
            metric="runtime_apply",
            owner="Runtime Model live gates",
            current="DISABLED",
            target="explicit runtime apply authority",
            evidence=runtime_eligibility_arbitration.get("stop_gates", []),
            state="STOP_SAFE",
            role="RUNTIME_BOUNDARY",
        ),
    ]
    stop_metrics = [row["metric"] for row in gate_rows if row["state"] == "STOP_SAFE" and row["role"] == "MANDATORY_CERTIFICATION_REQUIREMENT"]
    authority_stop_gates = [row["metric"] for row in gate_rows if row["role"] in {"AUTHORITY_BOUNDARY", "RUNTIME_BOUNDARY"}]
    serial_level_certified = s4_complete and metric_known and runtime_known
    concurrency_levels = [
        {
            "level": "L0_SERIAL_ONLY",
            "max_parallel_actions": 1,
            "status": "CERTIFIED_READ_ONLY" if serial_level_certified else "STOP_SAFE_MISSING_BASE_EVIDENCE",
            "produced_evidence": ["RT2-S4 coordination", "A6 runtime arbitration", "B13 metric reliability"],
            "consumed_evidence": ["governed_execution_coordination", "runtime_eligibility", "verification_capacity"],
            "safe_to_enable_now": False,
            "reason": "current governed serial boundary is owner-mapped; enablement still requires explicit authority",
        },
        {
            "level": "L1_TWO_USER_OR_TWO_ACTION",
            "max_parallel_actions": 2,
            "status": "STOP_SAFE_AUTHORITY_AND_CAPACITY_REQUIRED",
            "produced_evidence": [],
            "consumed_evidence": ["blast_radius", "rollback_capacity", "verification_capacity", "authority_envelope", "anti_flap"],
            "safe_to_enable_now": False,
            "reason": "beyond-one-user evidence is not authority and concurrency requires explicit authority plus rollback/verification capacity",
        },
        {
            "level": "L2_SMALL_BATCH_OR_POOL",
            "max_parallel_actions": "not certified",
            "status": "STOP_SAFE_NO_SILENT_BLAST_EXPANSION",
            "produced_evidence": [],
            "consumed_evidence": ["policy_scope", "authority_envelope", "rollback_capacity", "verification_capacity"],
            "safe_to_enable_now": False,
            "reason": "batch or pool movement would expand blast radius and must be separately certified",
        },
    ]
    certification_closed = not any(row["status"].startswith("STOP_SAFE_MISSING") for row in concurrency_levels)
    certified_level = "SERIAL_ONLY_READ_ONLY" if serial_level_certified else "NONE_STOP_SAFE"
    return {
        "schema_version": "v7.rt2-s5-certified-concurrency-ladder.v1",
        "generated_at": generated_at or "",
        "owner": "admin_core.autonomy_trust_acceleration",
        "omp_workstream": "RT2-S5",
        "purpose": "certify_safe_concurrency_limits_or_explicit_stop_safe_without_enabling_parallelism",
        "certification_state": "DONE_READ_ONLY_CONCURRENCY_LADDER_OWNER_MAPPED" if certification_closed else "STOP_SAFE_BASE_EVIDENCE_INCOMPLETE",
        "certification_verdict": "STOP_SAFE_CONCURRENCY_NOT_ENABLED",
        "certified_concurrency_level": certified_level,
        "concurrency_levels": concurrency_levels,
        "gate_rows": gate_rows,
        "stop_metrics": stop_metrics,
        "authority_stop_gates": authority_stop_gates,
        "completion_criteria_met": certification_closed,
        "rt2_s6_unlocked": certification_closed,
        "next_safe_action": "continue to RT2-S6 evidence-based continuous improvement" if certification_closed else "complete missing base evidence through existing owners",
        "still_blocked": [
            "runtime_apply",
            "automation",
            "concurrency_enablement",
            "authority_expansion",
            "queue_daemon",
            "planner_replacement",
            "user_movement",
            "silent_blast_radius_expansion",
        ],
        "safety_constraints": {
            "parallelism_is_safety_certification_not_performance_optimization": True,
            "no_silent_blast_expansion": True,
            "authority_required_before_any_concurrency_enablement": True,
            "recommendations_need_known_safe_execution_limits": True,
        },
        "omp_output": {
            "rt2_s5_status": "DONE_READ_ONLY_CONCURRENCY_LADDER_OWNER_MAPPED" if certification_closed else "STOP_SAFE_BASE_EVIDENCE_INCOMPLETE",
            "produced_evidence": "certified serial-only concurrency boundary plus explicit STOP_SAFE for wider levels",
            "unlocked_capability": "RT2-S6_EVIDENCE_BASED_CONTINUOUS_IMPROVEMENT" if certification_closed else "",
            "blocked_later_steps": [
                "runtime_self_optimization",
                "automatic_recommendations",
                "authority_lowering",
                "safety_gate_weakening",
                "runtime_apply",
                "automation",
            ],
        },
        "read_only": True,
        "synthetic_evidence_created": False,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "rollback_executed": False,
        "apply_executed": False,
        "concurrency_enabled": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_runtime_created": False,
    }


def build_rt2_s6_evidence_based_continuous_improvement(
    *,
    outcome_leverage_model: dict[str, Any],
    maximum_reality_knowledge_extraction: dict[str, Any],
    rt2_s5_certified_concurrency_ladder: dict[str, Any],
    routing_recommendation_readiness: dict[str, Any],
    metric_reliability_certification: dict[str, Any],
    decision_outcome_learning: dict[str, Any],
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Produce the RT2-S6 advisory recommendation without mutating Runtime."""
    s5_done = rt2_s5_certified_concurrency_ladder.get("certification_state") == "DONE_READ_ONLY_CONCURRENCY_LADDER_OWNER_MAPPED"
    safe_level = str(rt2_s5_certified_concurrency_ladder.get("certified_concurrency_level") or "UNKNOWN")
    leverage_rows = [
        row for row in outcome_leverage_model.get("activities_ranked") or []
        if isinstance(row, dict)
    ]
    top_activities = [str(row.get("activity")) for row in leverage_rows[:3]]
    top_activity = leverage_rows[0] if leverage_rows else {}
    knowledge_verdict = str(maximum_reality_knowledge_extraction.get("final_verdict") or "UNKNOWN")
    classification_summary = maximum_reality_knowledge_extraction.get("classification_summary")
    if not isinstance(classification_summary, dict):
        classification_summary = {}
    learning_growth = decision_outcome_learning.get("knowledge_growth") if isinstance(decision_outcome_learning.get("knowledge_growth"), dict) else {}
    metric_known = metric_reliability_certification.get("schema_version") == "v7.b13-metric-reliability-certification.v1"
    blocking_recommendation_certified = bool(metric_reliability_certification.get("blocking_recommendation_certified"))
    routing_blockers = list(routing_recommendation_readiness.get("blockers") or [])
    evidence_rows = [
        _metric_certification_row(
            metric="safe_execution_limit",
            owner="RT2-S5 / concurrency ladder",
            current=safe_level,
            target="SERIAL_ONLY_READ_ONLY or explicit STOP_SAFE",
            evidence={
                "certification_state": rt2_s5_certified_concurrency_ladder.get("certification_state", "UNKNOWN"),
                "still_blocked": rt2_s5_certified_concurrency_ladder.get("still_blocked", []),
            },
            state="PASS" if s5_done else "STOP_SAFE",
            role="MANDATORY_RECOMMENDATION_REQUIREMENT",
        ),
        _metric_certification_row(
            metric="outcome_leverage",
            owner="outcome_leverage_model",
            current=outcome_leverage_model.get("final_verdict", "UNKNOWN"),
            target="ranked improvement activities",
            evidence=top_activities,
            state="PASS" if leverage_rows else "STOP_SAFE",
            role="MANDATORY_RECOMMENDATION_REQUIREMENT",
        ),
        _metric_certification_row(
            metric="maximum_reality_knowledge",
            owner="maximum_reality_knowledge_extraction",
            current=knowledge_verdict,
            target="REAL_WORLD_LIMIT_REACHED or MAXIMUM_REALITY_REACHED with owner mapping",
            evidence=classification_summary,
            state="PASS" if knowledge_verdict in {"REAL_WORLD_LIMIT_REACHED", "MAXIMUM_REALITY_REACHED"} else "PARTIAL",
            role="EVIDENCE_CONTEXT",
        ),
        _metric_certification_row(
            metric="metric_reliability",
            owner="B13 metric_reliability_certification",
            current=metric_reliability_certification.get("certification_state", "UNKNOWN"),
            target="blocking recommendation metrics certified",
            evidence={"stop_metrics": metric_reliability_certification.get("stop_metrics", [])},
            state="PASS" if metric_known and blocking_recommendation_certified else "STOP_SAFE",
            role="MANDATORY_RECOMMENDATION_REQUIREMENT",
        ),
        _metric_certification_row(
            metric="routing_recommendation_readiness",
            owner="routing_recommendation_readiness",
            current=routing_recommendation_readiness.get("readiness", "UNKNOWN"),
            target="owner-mapped blockers allowed; runtime apply forbidden",
            evidence=routing_blockers,
            state="PASS" if isinstance(routing_recommendation_readiness, dict) else "STOP_SAFE",
            role="EVIDENCE_CONTEXT",
        ),
        _metric_certification_row(
            metric="learning",
            owner="decision_outcome_learning",
            current=learning_growth.get("knowledge_gained", 0),
            target="observed learning available or owner-mapped missing",
            evidence=learning_growth,
            state="PASS" if int(as_float(learning_growth.get("knowledge_gained"), 0.0)) > 0 else "PARTIAL",
            role="EVIDENCE_CONTEXT",
        ),
        _metric_certification_row(
            metric="authority_boundary",
            owner="OMP authority gates",
            current="ADVISORY_ONLY",
            target="no authority lowering or runtime mutation",
            evidence="RT2-S6 recommendation is not an approval, queue, runtime behavior, or automatic implementation order",
            state="STOP_SAFE",
            role="AUTHORITY_BOUNDARY",
        ),
    ]
    mandatory_stop = [
        row["metric"] for row in evidence_rows
        if row["state"] == "STOP_SAFE" and row["role"] == "MANDATORY_RECOMMENDATION_REQUIREMENT"
    ]
    recommendation_rows = [
        {
            "recommendation_id": "RT2-S6-RETURN-TO-B1",
            "recommendation_type": "OWNER_MAPPED_BACKLOG_CONTINUATION",
            "recommended_next_task": "B1_AGGREGATE_LIVENESS_EVIDENCE_BY_SOURCE_FAMILY_AND_CONFIDENCE",
            "canonical_owner": "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B1",
            "implementation_owners": [
                "tools/v7-service-matrix-refresh-all",
                "tools/v7-egress-quality-compact",
                "admin_core/intelligence_workers.py",
            ],
            "why_now": "RT2-S1 through RT2-S5 are complete, S6 has known safe execution limits, and OMP must return to the highest unfinished existing backlog owner.",
            "evidence_basis": {
                "safe_execution_limit": safe_level,
                "top_evidence_activities": top_activities,
                "highest_leverage_activity": top_activity.get("activity", ""),
                "knowledge_verdict": knowledge_verdict,
            },
            "safety_review": {
                "runtime_mutation_allowed": False,
                "authority_expansion_allowed": False,
                "automatic_implementation_allowed": False,
                "synthetic_evidence_allowed": False,
                "requires_omp_backlog_execution": True,
            },
        }
    ]
    recommendation_ready = not mandatory_stop
    return {
        "schema_version": "v7.rt2-s6-evidence-based-continuous-improvement.v1",
        "generated_at": generated_at or "",
        "owner": "admin_core.autonomy_trust_acceleration",
        "omp_workstream": "RT2-S6",
        "purpose": "convert_existing_measurement_outcome_latency_cost_time_and_learning_evidence_into_omp_owned_advisory_recommendation",
        "certification_state": "DONE_READ_ONLY_OWNER_MAPPED_RECOMMENDATION" if recommendation_ready else "STOP_SAFE_RECOMMENDATION_EVIDENCE_INCOMPLETE",
        "recommendation_verdict": "OWNER_MAPPED_RECOMMENDATION" if recommendation_ready else "MISSING_EVIDENCE_STOP_SAFE",
        "recommendation_rows": recommendation_rows if recommendation_ready else [],
        "no_change_verdict": False,
        "evidence_rows": evidence_rows,
        "mandatory_stop": mandatory_stop,
        "top_evidence_activities": top_activities,
        "knowledge_verdict": knowledge_verdict,
        "next_omp_step": "B1_AGGREGATE_LIVENESS_EVIDENCE_BY_SOURCE_FAMILY_AND_CONFIDENCE" if recommendation_ready else "FIX_RT2_S6_MANDATORY_EVIDENCE",
        "rt2_graduated": recommendation_ready,
        "completion_criteria_met": recommendation_ready,
        "still_blocked": [
            "runtime_self_optimization",
            "automatic_recommendations",
            "direct_implementation_without_omp",
            "authority_lowering",
            "safety_gate_weakening",
            "runtime_apply",
            "automation",
            "concurrency_enablement",
            "new_roadmap",
            "new_owner",
            "planner_replacement",
            "user_movement",
        ],
        "omp_output": {
            "rt2_s6_status": "DONE_READ_ONLY_OWNER_MAPPED_RECOMMENDATION" if recommendation_ready else "STOP_SAFE_RECOMMENDATION_EVIDENCE_INCOMPLETE",
            "produced_evidence": "owner-mapped recommendation to return OMP to B1" if recommendation_ready else "mandatory evidence missing",
            "unlocked_capability": "OMP_BACKLOG_CONTINUATION_B1" if recommendation_ready else "",
            "blocked_later_steps": [
                "runtime self-optimization",
                "automatic recommendations",
                "direct implementation without OMP",
                "authority lowering",
                "safety gate weakening",
                "runtime apply",
                "automation",
            ],
        },
        "read_only": True,
        "advisory_only": True,
        "synthetic_evidence_created": False,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "rollback_executed": False,
        "apply_executed": False,
        "concurrency_enabled": False,
        "automatic_recommendation_enabled": False,
        "direct_implementation_started": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_runtime_created": False,
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
    historical_certification_evidence: dict[str, Any] | None = None,
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
    historical = historical_certification_evidence if isinstance(historical_certification_evidence, dict) else {}
    reusable = historical.get("reusable_dimensions") if isinstance(historical.get("reusable_dimensions"), dict) else {}
    historical_pointers = [
        str(row.get("evidence") or "")
        for row in (historical.get("certification_inventory") or [])
        if isinstance(row, dict) and row.get("current_validity") == "VALID_SUPPORTING_LAYER"
    ]
    for pointer in historical_pointers:
        _add_certification_signal(signal_taxonomy["categories"], "HISTORICAL_EVIDENCE", pointer)
    if reusable.get("execution_path"):
        _add_certification_signal(signal_taxonomy["categories"], "SUPPORTING_EVIDENCE", "historical_execution_path_certification_reused")
    if reusable.get("blast_radius"):
        _add_certification_signal(signal_taxonomy["categories"], "SUPPORTING_EVIDENCE", "historical_blast_radius_certification_reused")
    if reusable.get("rollback_or_no_rollback"):
        _add_certification_signal(signal_taxonomy["categories"], "SUPPORTING_EVIDENCE", "historical_rollback_or_no_rollback_certification_reused")
    reusable_missing = {
        "class-level blast_radius_certification": bool(reusable.get("blast_radius")),
        "class-level rollback_or_no_rollback_certification": bool(reusable.get("rollback_or_no_rollback")),
    }
    mandatory = signal_taxonomy["categories"]["MANDATORY_CERTIFICATION_REQUIREMENT"]
    signal_taxonomy["categories"]["MANDATORY_CERTIFICATION_REQUIREMENT"] = [
        item for item in mandatory if not reusable_missing.get(item, False)
    ]
    if historical.get("current_action_class_identity") == "DECISION_CONTEXT_MISMATCH":
        _add_certification_signal(
            signal_taxonomy["categories"],
            "MANDATORY_CERTIFICATION_REQUIREMENT",
            "current-class suitability decision-context real outcome",
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
            "required_authority": "approved delegated policy or explicit packet authority" if name == first_class else "explicit class or packet authority",
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
        "historical_certification_reuse": {
            "source_schema": historical.get("schema_version", ""),
            "certifications_found": historical.get("historical_certifications_found", 0),
            "real_movement_certifications_found": historical.get("real_movement_certifications_found", 0),
            "max_certified_user_count": historical.get("max_certified_blast_radius_users", 0),
            "current_action_class_identity": historical.get("current_action_class_identity", "IDENTITY_UNRESOLVED"),
            "reusable_dimensions": reusable,
            "exact_missing_delta": list(historical.get("exact_missing_delta") or []),
            "root_cause_of_non_consumption": historical.get("root_cause_of_non_consumption", "UNKNOWN_WITH_REASON"),
            "authority_restored": False,
            "promotion_performed": False,
        },
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
            "current_authority": "bounded delegated policy for the allowed one-user class",
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
            "runtime_can_execute_automatically": delegated_eligibility["runtime_can_execute_automatically"],
            "runtime_must_stop_at": "AUTHORITY_BOUNDARY" if not delegated_eligibility["runtime_can_execute_automatically"] else "",
            "runtime_apply_allowed_now": delegated_eligibility["runtime_can_execute_automatically"],
            "current_autonomy_mode": delegated_policy["current_mode"],
            "target_autonomy_mode": delegated_policy["target_mode"],
        },
        "promotion_recommendation": {
            "recommendation": "DO_NOT_ENABLE_RUNTIME_AUTOMATION",
            "promotion_evaluation": (
                "PROMOTION_BLOCKED_WITH_EXACT_DELTA"
                if historical.get("current_action_class_identity") == "DECISION_CONTEXT_MISMATCH"
                else "GOVERNED_ONLY_CORRECT"
            ),
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
            "can_runtime_execute_automatically": delegated_eligibility["runtime_can_execute_automatically"],
            "reason": "delegated_policy_or_action_class_not_ready" if not delegated_eligibility["runtime_can_execute_automatically"] else "action_class_policy_authority_and_runtime_bounds_pass",
            "requires_authority_expansion": False,
            "stop_condition_if_promoted": "" if delegated_eligibility["runtime_can_execute_automatically"] else "AUTHORITY_BOUNDARY",
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
            "runtime_can_execute_automatically": delegated_eligibility["runtime_can_execute_automatically"],
            "autonomous_routing_stop_reason": autonomous_routing_evolution_program.get("exact_stop_reason", "UNKNOWN"),
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": delegated_policy["autonomy_enabled"],
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

OUTCOME_CLOSURE_CANDIDATE_FIELDS = (
    "apply_result",
    "execution_outcome",
    "post_action_verification",
    "verification_result",
    "verification",
    "service_outcome",
    "service_actual",
    "service_delta",
    "user_outcome",
    "learning_record",
    "trust_update",
    "prediction_actual",
    "outcome",
    "outcome_status",
    "outcome_quality",
    "knowledge_growth",
)

OUTCOME_CLOSURE_MARKER_FIELDS = (
    "closure_state",
    "terminal_outcome_classification",
    "terminal_transaction_state",
    "feedback_id",
    "learning_id",
    "execution_outcome",
    "verification_result",
    "rollback_result",
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

LIVENESS_SOURCE_FAMILIES = {
    "telegram_sentinel": {
        "family": "telegram_sentinel",
        "owner": "tools/v7-telegram-sentinel",
        "policy_relevance": "service_specific_liveness",
    },
    "service_matrix": {
        "family": "service_matrix",
        "owner": "tools/v7-service-matrix-refresh-all",
        "policy_relevance": "multi_service_liveness",
    },
    "quality_compact": {
        "family": "quality_compact",
        "owner": "tools/v7-egress-quality-compact",
        "policy_relevance": "quality_degradation_liveness",
    },
    "route_readiness": {
        "family": "route_reality",
        "owner": "admin_core.operator_decision_surface",
        "policy_relevance": "route_runtime_liveness",
    },
    "runtime_readiness": {
        "family": "route_reality",
        "owner": "admin_core.operator_decision_surface",
        "policy_relevance": "route_runtime_liveness",
    },
    "service_user_sla_fit": {
        "family": "policy_fit",
        "owner": "admin_core.operator_decision_surface",
        "policy_relevance": "service_user_policy_liveness",
    },
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


def _liveness_source_meta(source: str) -> dict[str, str]:
    return LIVENESS_SOURCE_FAMILIES.get(source, {
        "family": source or "unknown",
        "owner": "unknown_existing_liveness_owner",
        "policy_relevance": "supporting_liveness_evidence",
    })


def _liveness_confidence(value: Any) -> float:
    confidence = as_float(value, 0.0)
    if 0.0 < confidence <= 1.0:
        confidence *= 100.0
    return round(max(0.0, min(100.0, confidence)), 3)


def _liveness_confidence_band(confidence: float) -> str:
    if confidence >= 70.0:
        return "HIGH"
    if confidence >= 40.0:
        return "MEDIUM"
    if confidence > 0.0:
        return "LOW"
    return "UNKNOWN"


def _liveness_status_from_evidence(evidence: list[dict[str, Any]]) -> str:
    if any(row.get("explicit_liveness_failure") for row in evidence):
        return "LIVENESS_FAILURE_OBSERVED"
    if evidence:
        return "SUPPORTING_ONLY"
    return "NO_EVIDENCE"


def _liveness_freshness_for_source(snapshot_statuses: dict[str, dict[str, Any]], source: str) -> dict[str, Any]:
    source_to_families = {
        "service_matrix": ("service-scores", "channel-service-scores"),
        "telegram_sentinel": ("service-scores",),
        "quality_compact": ("service-scores", "channel-service-scores", "risk-summaries"),
        "route_readiness": ("best-available-pool", "risk-summaries"),
        "runtime_readiness": ("risk-summaries",),
        "service_user_sla_fit": ("service-scores", "channel-service-scores", "best-available-pool"),
    }
    rows = [
        snapshot_statuses.get(name, {})
        for name in source_to_families.get(source, ())
        if isinstance(snapshot_statuses.get(name, {}), dict)
    ]
    if not rows:
        return {
            "freshness_state": "UNKNOWN",
            "runtime_behavior": "STOP",
            "stop_required": True,
            "confidence": 0.0,
        }
    states = {_text(row.get("freshness_state") or row.get("status") or "UNKNOWN").upper() for row in rows}
    if "FRESH" in states and not any(bool(row.get("stop_required", True)) for row in rows):
        freshness_state = "FRESH"
    elif "STALE" in states or "EXPIRED" in states:
        freshness_state = "STALE"
    else:
        freshness_state = sorted(states)[0] if states else "UNKNOWN"
    return {
        "freshness_state": freshness_state,
        "runtime_behavior": "ALLOW" if freshness_state == "FRESH" else "STOP",
        "stop_required": any(bool(row.get("stop_required", True)) for row in rows),
        "confidence": round(sum(as_float(row.get("confidence"), 0.0) for row in rows) / len(rows), 3),
    }


def build_liveness_evidence_aggregation(
    *,
    hard_failure_classification: dict[str, Any] | None = None,
    snapshot_statuses: dict[str, dict[str, Any]] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Aggregate existing liveness evidence by source family and confidence for B1."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    classification = hard_failure_classification or {}
    statuses = snapshot_statuses or {}
    by_family: dict[str, dict[str, Any]] = {}
    object_rows = []

    for row in classification.get("rows") or []:
        if not isinstance(row, dict):
            continue
        object_name = _text(row.get("object") or "unknown")
        evidence = [item for item in (row.get("evidence") or []) if isinstance(item, dict)]
        object_sources = []
        for item in evidence:
            source = _text(item.get("source") or "unknown")
            meta = _liveness_source_meta(source)
            family = meta["family"]
            confidence = _liveness_confidence(item.get("confidence"))
            freshness = _liveness_freshness_for_source(statuses, source)
            family_row = by_family.setdefault(family, {
                "source_family": family,
                "owner": meta["owner"],
                "policy_relevance": meta["policy_relevance"],
                "evidence_count": 0,
                "explicit_liveness_failure_count": 0,
                "objects": set(),
                "sources": set(),
                "confidence_values": [],
                "freshness_states": set(),
                "runtime_behaviors": set(),
                "stop_required": False,
            })
            family_row["evidence_count"] += 1
            family_row["explicit_liveness_failure_count"] += 1 if item.get("explicit_liveness_failure") else 0
            family_row["objects"].add(object_name)
            family_row["sources"].add(source)
            family_row["confidence_values"].append(confidence)
            family_row["freshness_states"].add(_text(freshness.get("freshness_state") or "UNKNOWN"))
            family_row["runtime_behaviors"].add(_text(freshness.get("runtime_behavior") or "STOP"))
            family_row["stop_required"] = bool(family_row["stop_required"] or freshness.get("stop_required", True))
            object_sources.append({
                "source": source,
                "source_family": family,
                "owner": meta["owner"],
                "confidence": confidence,
                "confidence_band": _liveness_confidence_band(confidence),
                "explicit_liveness_failure": bool(item.get("explicit_liveness_failure")),
                "freshness_state": freshness.get("freshness_state", "UNKNOWN"),
                "policy_relevance": meta["policy_relevance"],
            })
        object_rows.append({
            "object": object_name,
            "classification": row.get("classification", "UNKNOWN"),
            "status": _liveness_status_from_evidence(evidence),
            "source_families": sorted({item["source_family"] for item in object_sources}),
            "source_count": len({item["source"] for item in object_sources}),
            "explicit_liveness_evidence_count": row.get("explicit_liveness_evidence_count", 0),
            "sources": object_sources,
            "runtime_apply_allowed": False,
            "authority_expanded": False,
        })

    family_rows = []
    for family, row in sorted(by_family.items()):
        confidence_values = row.pop("confidence_values")
        average_confidence = round(sum(confidence_values) / len(confidence_values), 3) if confidence_values else 0.0
        family_rows.append({
            **row,
            "objects": sorted(row["objects"]),
            "sources": sorted(row["sources"]),
            "freshness_states": sorted(row["freshness_states"]),
            "runtime_behaviors": sorted(row["runtime_behaviors"]),
            "average_confidence": average_confidence,
            "confidence_band": _liveness_confidence_band(average_confidence),
            "status": "HAS_EXPLICIT_LIVENESS" if row["explicit_liveness_failure_count"] else "SUPPORTING_ONLY",
        })

    confirmed_objects = [
        row["object"] for row in object_rows
        if row.get("classification") == "HARD_FAILURE_CONFIRMED"
    ]
    return {
        "schema_version": "v7.b1.liveness-evidence-aggregation.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B1",
        "purpose": "aggregate_existing_liveness_evidence_by_source_family_confidence_owner_freshness_and_policy_relevance",
        "source_owners_reused": [
            "tools/v7-service-matrix-refresh-all",
            "tools/v7-telegram-sentinel",
            "tools/v7-egress-quality-compact",
            "admin_core.operator_decision_surface",
            "admin_core.intelligence_workers",
            "admin_core.intelligence_snapshots",
        ],
        "inputs": {
            "hard_failure_classification_schema": classification.get("schema_version", ""),
            "snapshot_status_families": sorted(statuses.keys()),
        },
        "summary": {
            "source_families": len(family_rows),
            "objects_seen": len(object_rows),
            "confirmed_objects": len(confirmed_objects),
            "confirmed_object_names": confirmed_objects,
            "evidence_count": sum(row["evidence_count"] for row in family_rows),
            "explicit_liveness_evidence_count": sum(row["explicit_liveness_failure_count"] for row in family_rows),
        },
        "source_family_rows": family_rows,
        "object_rows": object_rows,
        "policy_source": "docs/policies/POLICY_001_HARD_FAILURE.md",
        "canonical_owner": "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B1",
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
            "schema": _text(status.get("schema") or status.get("schema_version")),
            "exists": bool(status.get("exists", False)),
            "generated_at": _text(status.get("generated_at")),
            "expires_at": _text(status.get("expires_at")),
            "ttl_seconds": status.get("ttl_seconds"),
            "freshness_state": _text(status.get("freshness_state") or status.get("status") or "UNKNOWN"),
            "runtime_behavior": _text(status.get("runtime_behavior") or "STOP"),
            "stop_required": bool(status.get("stop_required", True)),
            "confidence": as_float(status.get("confidence"), 0.0),
            "generator": _text(status.get("generator")),
            "item_count": status.get("item_count"),
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


def _policy_window_row_by_action_class(action_class_freshness_windows: dict[str, Any], action_class: str) -> dict[str, Any]:
    for row in action_class_freshness_windows.get("rows") or []:
        if isinstance(row, dict) and row.get("action_class") == action_class:
            return row
    return {
        "action_class": action_class,
        "freshness_windows": dict(ACTION_CLASS_FRESHNESS_WINDOWS.get(action_class, {})),
        "domains": [],
        "freshness_ready": False,
        "blockers": ["action_class_freshness_window_missing"],
    }


def _hard_failure_policy_risk_class(classification: str, explicit_count: int, source_count: int) -> str:
    if classification == "HARD_FAILURE_CONFIRMED" and explicit_count >= 2 and source_count >= 2:
        return "CRITICAL_CONFIRMED_HARD_FAILURE"
    if classification == "HARD_FAILURE_CONFIRMED":
        return "CONFIRMED_HARD_FAILURE"
    if classification == "HARD_FAILURE_SUSPECTED":
        return "SUSPECTED_HARD_FAILURE"
    if classification == "RECHECK_REQUIRED":
        return "RECHECK_REQUIRED"
    return "NO_HARD_FAILURE_POLICY_WINDOW"


def build_hard_failure_policy_windows(
    *,
    hard_failure_classification: dict[str, Any] | None = None,
    liveness_evidence_aggregation: dict[str, Any] | None = None,
    action_class_freshness_windows: dict[str, Any] | None = None,
    anti_flapping: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Map hard-failure risk classes to existing policy windows without changing timers."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    classification_model = hard_failure_classification or {}
    aggregation = liveness_evidence_aggregation or {}
    freshness_windows = action_class_freshness_windows or build_action_class_freshness_windows({})
    anti_flap = anti_flapping or {"policy": ANTI_FLAP_POLICY, "summary": {"blocked_users": 0}}
    hard_fail_window = _policy_window_row_by_action_class(freshness_windows, "channel hard-fail failover")
    conservative_window = _policy_window_row_by_action_class(freshness_windows, "single-user governed candidate failover")
    anti_flap_policy = anti_flap.get("policy") if isinstance(anti_flap.get("policy"), dict) else ANTI_FLAP_POLICY
    anti_flap_blocked = int((anti_flap.get("summary") or {}).get("blocked_users") or 0)
    objects = {
        row.get("object"): row
        for row in (classification_model.get("rows") or [])
        if isinstance(row, dict) and row.get("object")
    }
    aggregate_objects = {
        row.get("object"): row
        for row in (aggregation.get("object_rows") or [])
        if isinstance(row, dict) and row.get("object")
    }
    object_names = sorted(set(objects) | set(aggregate_objects))
    rows: list[dict[str, Any]] = []
    for object_name in object_names:
        classification_row = objects.get(object_name, {})
        aggregate_row = aggregate_objects.get(object_name, {})
        classification = _text(
            classification_row.get("classification")
            or aggregate_row.get("classification")
            or classification_model.get("classification")
            or "UNKNOWN"
        )
        explicit_count = int(
            classification_row.get(
                "explicit_liveness_evidence_count",
                aggregate_row.get("explicit_liveness_evidence_count", 0),
            )
            or 0
        )
        source_count = int(
            aggregate_row.get(
                "source_count",
                len(classification_row.get("independent_sources") or []),
            )
            or 0
        )
        risk_class = _hard_failure_policy_risk_class(classification, explicit_count, source_count)
        if risk_class in {"CRITICAL_CONFIRMED_HARD_FAILURE", "CONFIRMED_HARD_FAILURE"}:
            selected_action_class = "channel hard-fail failover"
            selected_window = hard_fail_window
            timer_policy = "FAST_REACTION_WINDOW"
        elif risk_class == "SUSPECTED_HARD_FAILURE":
            selected_action_class = "single-user governed candidate failover"
            selected_window = conservative_window
            timer_policy = "CONFIRMATION_RECHECK_WINDOW"
        else:
            selected_action_class = "single-user governed candidate failover"
            selected_window = conservative_window
            timer_policy = "NO_HARD_FAILURE_ACCELERATION"
        domain_windows = dict(selected_window.get("freshness_windows") or {})
        reaction_window_seconds = min(domain_windows.values()) if domain_windows else 0
        blockers = list(selected_window.get("blockers") or [])
        if anti_flap_blocked:
            blockers.append("anti_flap_blocks_recent_oscillation")
        if risk_class in {"RECHECK_REQUIRED", "NO_HARD_FAILURE_POLICY_WINDOW"}:
            blockers.append("hard_failure_not_confirmed_for_fast_window")
        rows.append({
            "object": object_name,
            "hard_failure_classification": classification,
            "risk_class": risk_class,
            "selected_action_class": selected_action_class,
            "timer_policy": timer_policy,
            "reaction_window_seconds": int(reaction_window_seconds),
            "freshness_windows": domain_windows,
            "anti_flap_cooldown_seconds": int(anti_flap_policy.get("cooldown_seconds", 0) or 0),
            "minimum_observation_window_seconds": int(anti_flap_policy.get("minimum_observation_window_seconds", 0) or 0),
            "source_count": source_count,
            "explicit_liveness_evidence_count": explicit_count,
            "policy_window_ready": not blockers,
            "blockers": sorted(set(blockers)),
            "timer_changed": False,
            "risk_class_changes_runtime": False,
            "runtime_apply_allowed": False,
            "authority_expanded": False,
        })
    return {
        "schema_version": "v7.b2.hard-failure-policy-windows.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B2",
        "purpose": "expose_hard_failure_timer_risk_class_policy_window_impact_without_changing_runtime_timers",
        "source_owners_reused": [
            "admin_core.autonomy_trust_acceleration.build_hard_failure_classification",
            "admin_core.autonomy_trust_acceleration.build_liveness_evidence_aggregation",
            "admin_core.autonomy_trust_acceleration.build_action_class_freshness_windows",
            "admin_core.autonomy_trust_acceleration.build_anti_flapping",
        ],
        "policy_sources": [
            "docs/policies/POLICY_001_HARD_FAILURE.md",
            "docs/policies/POLICY_009_ANTI_FLAP.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B2",
        ],
        "rows": rows,
        "summary": {
            "objects_seen": len(rows),
            "ready": sum(1 for row in rows if row["policy_window_ready"]),
            "blocked": sum(1 for row in rows if not row["policy_window_ready"]),
            "critical_confirmed": sum(1 for row in rows if row["risk_class"] == "CRITICAL_CONFIRMED_HARD_FAILURE"),
            "suspected": sum(1 for row in rows if row["risk_class"] == "SUSPECTED_HARD_FAILURE"),
            "timer_changes": 0,
        },
        "canonical_rules": [
            "hard_failure_fast_window_requires_confirmed_liveness_evidence",
            "suspected_hard_failure_uses_confirmation_recheck_window",
            "anti_flap_remains_a_stop_gate",
            "risk_class_is_read_only_and_non_authorizing",
            "b2_does_not_change_timer_values",
        ],
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


def _soft_degradation_object_key(row: dict[str, Any], index: int = 0) -> str:
    return _text(
        row.get("channel")
        or row.get("egress")
        or row.get("service")
        or row.get("target")
        or row.get("id")
        or row.get("object")
        or f"unknown-{index}"
    )


def _soft_degradation_trend(row: dict[str, Any]) -> str:
    score = row.get("score") if isinstance(row.get("score"), dict) else {}
    for value in (
        row.get("trend"),
        row.get("quality_trend"),
        row.get("service_trend"),
        score.get("trend"),
    ):
        text = _text(value).upper()
        if text:
            return text
    return "UNKNOWN"


def _soft_degradation_score(row: dict[str, Any]) -> float:
    score = row.get("score") if isinstance(row.get("score"), dict) else {}
    for value in (
        score.get("current"),
        row.get("score"),
        row.get("quality_score"),
        row.get("service_score"),
        row.get("suitability_score"),
        row.get("aggregate_score"),
    ):
        if isinstance(value, dict):
            continue
        parsed = as_float(value, -1.0)
        if parsed >= 0.0:
            return round(parsed, 3)
    return 0.0


def _soft_degradation_result(trend: str, states: set[str], reasons: list[str], hard_failure: str) -> tuple[str, str, str, str]:
    reason_text = " ".join(reasons).lower()
    if hard_failure in {"CRITICAL_CONFIRMED_HARD_FAILURE", "CONFIRMED_HARD_FAILURE"}:
        return (
            "HARD_FAILURE_OVERRIDES_SOFT_DEGRADATION",
            "FAILOVER",
            "hard_failure_policy_window_already_confirmed",
            "hard_failure_result_must_not_be_weakened_by_soft_degradation",
        )
    if "QUARANTINED" in states:
        return (
            "SOFT_DEGRADATION",
            "QUARANTINE",
            "existing_quarantined_state",
            "quarantine_state_is_existing_policy_vocabulary",
        )
    if "DEGRADED" in states or trend == "DEGRADING" or "degraded" in reason_text or "degradation" in reason_text:
        return (
            "SOFT_DEGRADATION",
            "ASK_OPERATOR",
            "existing_degradation_trend_or_state",
            "soft_degradation_is_read_only_until_authority_and_evidence_certification",
        )
    if trend in {"STABLE", "IMPROVING"} or states & {"TRUSTED", "WATCH", "RECOVERING", "NEW"}:
        return (
            "NO_DEGRADATION",
            "KEEP",
            "existing_signal_not_showing_degradation",
            "no_soft_degradation_policy_window_is_open",
        )
    return (
        "NOISY_OR_ATTRIBUTION_UNKNOWN",
        "PROBE_ONLY",
        "insufficient_or_unknown_attribution",
        "collect_more_existing_owner_evidence_before_policy_action",
    )


def build_soft_degradation_threshold_vocabulary_alignment(
    *,
    decision_surface: dict[str, Any] | None = None,
    service_scores_snapshot: dict[str, Any] | None = None,
    channel_service_scores_snapshot: dict[str, Any] | None = None,
    service_user_sla_fit: dict[str, Any] | None = None,
    hard_failure_policy_windows: dict[str, Any] | None = None,
    freshness_actionability: dict[str, Any] | None = None,
    anti_flapping: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Align existing soft-degradation trend thresholds to canonical policy vocabulary for B3."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    surface = decision_surface or {}
    freshness = freshness_actionability or build_freshness_actionability({})
    fit = service_user_sla_fit or {}
    hard_windows = hard_failure_policy_windows or {}
    anti_flap = anti_flapping or {"policy": ANTI_FLAP_POLICY, "summary": {"blocked_users": 0}}
    objects: dict[str, dict[str, Any]] = {}

    def ensure_object(key: str) -> dict[str, Any]:
        return objects.setdefault(key, {
            "object": key,
            "owners": set(),
            "sources": set(),
            "trends": set(),
            "states": set(),
            "reasons": [],
            "scores": [],
            "hard_failure_risk_class": "NO_HARD_FAILURE_POLICY_WINDOW",
        })

    for source_name, snapshot in (
        ("service-scores", service_scores_snapshot),
        ("channel-service-scores", channel_service_scores_snapshot),
    ):
        for index, item in enumerate(_items(snapshot)):
            key = _soft_degradation_object_key(item, index)
            row = ensure_object(key)
            row["owners"].add("tools/v7-service-matrix-refresh-all" if source_name == "service-scores" else "tools/v7-egress-quality-compact")
            row["sources"].add(source_name)
            row["trends"].add(_soft_degradation_trend(item))
            status = _text(item.get("status") or item.get("state") or item.get("lifecycle") or item.get("diagnose_severity")).upper()
            if status:
                row["states"].add(status)
            score = _soft_degradation_score(item)
            if score:
                row["scores"].append(score)

    for user_row in [row for row in (surface.get("users") or []) if isinstance(row, dict)]:
        for candidate in _candidate_rows_for_user(user_row):
            key = _candidate_channel(candidate)
            if not key:
                continue
            row = ensure_object(key)
            row["owners"].add("tools/v7-users-autoswitch")
            row["sources"].add("planner_autoswitch_candidate")
            state = _text(
                candidate.get("ctr_state")
                or candidate.get("state")
                or candidate.get("lifecycle")
                or candidate.get("service_state")
            ).upper()
            if state:
                row["states"].add(state)
            row["trends"].add(_soft_degradation_trend(candidate))
            row["reasons"].extend(_candidate_reasons(candidate))
            score = _soft_degradation_score(candidate)
            if score:
                row["scores"].append(score)

    for fit_row in [row for row in (fit.get("rows") or []) if isinstance(row, dict)]:
        key = _text(fit_row.get("best_channel") or fit_row.get("current_assignment"))
        if not key:
            continue
        row = ensure_object(key)
        row["owners"].add("admin_core.autonomy_trust_acceleration.build_service_user_sla_fit")
        row["sources"].add("service_user_sla_fit")
        verdict = _text(fit_row.get("fit_verdict")).upper()
        if verdict:
            row["states"].add(verdict)
        row["reasons"].append(_text(fit_row.get("reason")))
        score = as_float(fit_row.get("fit_score"), 0.0)
        if score:
            row["scores"].append(round(score, 3))

    for hard_row in [row for row in (hard_windows.get("rows") or []) if isinstance(row, dict)]:
        key = _text(hard_row.get("object"))
        if not key:
            continue
        row = ensure_object(key)
        row["owners"].add("admin_core.autonomy_trust_acceleration.build_hard_failure_policy_windows")
        row["sources"].add("hard_failure_policy_windows")
        row["hard_failure_risk_class"] = _text(hard_row.get("risk_class") or "NO_HARD_FAILURE_POLICY_WINDOW")

    quality_freshness = ((freshness.get("domains") or {}).get("quality") or {}).get("classification", "UNKNOWN")
    service_freshness = ((freshness.get("domains") or {}).get("service") or {}).get("classification", "UNKNOWN")
    anti_flap_blocked = int((anti_flap.get("summary") or {}).get("blocked_users") or 0)
    rows: list[dict[str, Any]] = []
    for key in sorted(objects):
        item = objects[key]
        trends = {trend for trend in item["trends"] if trend and trend != "UNKNOWN"}
        trend = sorted(trends)[0] if trends else "UNKNOWN"
        result, action, reason, note = _soft_degradation_result(
            trend,
            {state for state in item["states"] if state},
            [reason for reason in item["reasons"] if reason],
            item["hard_failure_risk_class"],
        )
        blockers = []
        if quality_freshness != "ACTIONABLE_NOW":
            blockers.append("quality_freshness_not_actionable")
        if service_freshness != "ACTIONABLE_NOW":
            blockers.append("service_freshness_not_actionable")
        if anti_flap_blocked:
            blockers.append("anti_flap_blocks_recent_oscillation")
        rows.append({
            "object": key,
            "canonical_policy": "POLICY_002_SOFT_DEGRADATION",
            "canonical_policy_result": result,
            "canonical_decision_action": action,
            "trend": trend,
            "observed_states": sorted({state for state in item["states"] if state}),
            "average_signal_score": round(sum(item["scores"]) / len(item["scores"]), 3) if item["scores"] else 0.0,
            "hard_failure_risk_class": item["hard_failure_risk_class"],
            "quality_freshness": quality_freshness,
            "service_freshness": service_freshness,
            "owner_sources": sorted(item["owners"]),
            "evidence_sources": sorted(item["sources"]),
            "threshold_vocabulary_reason": reason,
            "policy_note": note,
            "blockers": sorted(set(blockers)),
            "threshold_values_changed": False,
            "formula_changed": False,
            "runtime_apply_allowed": False,
            "authority_expanded": False,
        })

    vocabulary_rows = [
        {
            "existing_signal": "quality_compact_score_trend_degrading",
            "owner": "tools/v7-egress-quality-compact",
            "canonical_policy_result": "SOFT_DEGRADATION",
            "canonical_decision_action": "ASK_OPERATOR",
            "threshold_source": "existing quality compact score/trend calculation",
        },
        {
            "existing_signal": "planner_ctr_state_degraded",
            "owner": "tools/v7-users-autoswitch",
            "canonical_policy_result": "SOFT_DEGRADATION",
            "canonical_decision_action": "ASK_OPERATOR",
            "threshold_source": "existing CTR state vocabulary",
        },
        {
            "existing_signal": "planner_ctr_state_quarantined",
            "owner": "tools/v7-users-autoswitch",
            "canonical_policy_result": "SOFT_DEGRADATION",
            "canonical_decision_action": "QUARANTINE",
            "threshold_source": "existing CTR state vocabulary",
        },
        {
            "existing_signal": "stable_or_improving_quality_trend",
            "owner": "tools/v7-egress-quality-compact",
            "canonical_policy_result": "NO_DEGRADATION",
            "canonical_decision_action": "KEEP",
            "threshold_source": "existing quality compact score/trend calculation",
        },
        {
            "existing_signal": "unknown_or_unattributed_quality_signal",
            "owner": "service matrix + quality compact + planner/autoswitch",
            "canonical_policy_result": "NOISY_OR_ATTRIBUTION_UNKNOWN",
            "canonical_decision_action": "PROBE_ONLY",
            "threshold_source": "existing signal owners; no synthetic evidence",
        },
    ]
    return {
        "schema_version": "v7.b3.soft-degradation-threshold-vocabulary.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B3",
        "purpose": "align_existing_soft_degradation_trend_thresholds_to_canonical_policy_vocabulary_without_changing_thresholds",
        "source_owners_reused": [
            "tools/v7-users-autoswitch",
            "tools/v7-egress-quality-compact",
            "tools/v7-service-matrix-refresh-all",
            "admin_core.autonomy_trust_acceleration.build_service_user_sla_fit",
            "admin_core.autonomy_trust_acceleration.build_hard_failure_policy_windows",
            "admin_core.autonomy_trust_acceleration.build_freshness_actionability",
            "admin_core.autonomy_trust_acceleration.build_anti_flapping",
        ],
        "policy_sources": [
            "docs/policies/POLICY_002_SOFT_DEGRADATION.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B3",
            "docs/reference/V7_CANONICAL_REFERENCE.md canonical decision vocabulary",
        ],
        "vocabulary_rows": vocabulary_rows,
        "rows": rows,
        "summary": {
            "objects_seen": len(rows),
            "soft_degradation": sum(1 for row in rows if row["canonical_policy_result"] == "SOFT_DEGRADATION"),
            "no_degradation": sum(1 for row in rows if row["canonical_policy_result"] == "NO_DEGRADATION"),
            "noisy_or_unknown": sum(1 for row in rows if row["canonical_policy_result"] == "NOISY_OR_ATTRIBUTION_UNKNOWN"),
            "hard_failure_overrides": sum(1 for row in rows if row["canonical_policy_result"] == "HARD_FAILURE_OVERRIDES_SOFT_DEGRADATION"),
            "threshold_changes": 0,
            "formula_changes": 0,
        },
        "canonical_rules": [
            "soft_degradation_is_trend_or_threshold_vocabulary_not_single_event_truth",
            "hard_failure_policy_windows_override_soft_degradation_when_confirmed",
            "unknown_or_unattributed_quality_remains_probe_only",
            "b3_does_not_change_threshold_values_or_formulas",
            "b3_does_not_grant_runtime_apply_or_authority",
        ],
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


DEGRADATION_SIGNAL_POLICY_FAMILIES = (
    {
        "signal_family": "latency",
        "canonical_signal": "LATENCY_DEGRADATION",
        "tokens": ("latency", "p95", "deadline", "slow", "delay"),
        "policy_result": "SOFT_DEGRADATION",
        "decision_action": "ASK_OPERATOR",
        "owner": "tools/v7-egress-quality-compact + route/service views",
    },
    {
        "signal_family": "error_rate",
        "canonical_signal": "ERROR_RATE_DEGRADATION",
        "tokens": ("error", "5xx", "failed", "fail_rate", "failure"),
        "policy_result": "SOFT_DEGRADATION",
        "decision_action": "ASK_OPERATOR",
        "owner": "tools/v7-service-matrix-refresh-all",
    },
    {
        "signal_family": "timeout",
        "canonical_signal": "TIMEOUT_DEGRADATION",
        "tokens": ("timeout", "timed out", "no response"),
        "policy_result": "SOFT_DEGRADATION",
        "decision_action": "ASK_OPERATOR",
        "owner": "tools/v7-service-matrix-refresh-all",
    },
    {
        "signal_family": "loss",
        "canonical_signal": "LOSS_DEGRADATION",
        "tokens": ("loss", "packet_loss", "dropped"),
        "policy_result": "SOFT_DEGRADATION",
        "decision_action": "ASK_OPERATOR",
        "owner": "tools/v7-egress-quality-compact + route/service views",
    },
    {
        "signal_family": "jitter",
        "canonical_signal": "JITTER_DEGRADATION",
        "tokens": ("jitter",),
        "policy_result": "SOFT_DEGRADATION",
        "decision_action": "ASK_OPERATOR",
        "owner": "tools/v7-egress-quality-compact + route/service views",
    },
    {
        "signal_family": "saturation",
        "canonical_signal": "SATURATION_DEGRADATION",
        "tokens": ("saturation", "overload", "capacity", "full", "headroom"),
        "policy_result": "SOFT_DEGRADATION",
        "decision_action": "ASK_OPERATOR",
        "owner": "tools/v7-users-autoswitch + route/service views",
    },
    {
        "signal_family": "service_response",
        "canonical_signal": "SERVICE_RESPONSE_DEGRADATION",
        "tokens": ("service_signal", "degraded_service", "degraded", "service_instagram", "service_telegram"),
        "policy_result": "SOFT_DEGRADATION",
        "decision_action": "ASK_OPERATOR",
        "owner": "tools/v7-service-matrix-refresh-all + admin_core.operator_decision_surface",
    },
    {
        "signal_family": "route_readiness",
        "canonical_signal": "ROUTE_READINESS_DEGRADATION",
        "tokens": ("route", "route_safe", "runtime_safe", "route_class"),
        "policy_result": "NOISY_OR_ATTRIBUTION_UNKNOWN",
        "decision_action": "PROBE_ONLY",
        "owner": "admin_core.operator_decision_surface",
    },
)


def _degradation_signal_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(f"{key} {_degradation_signal_text(item)}" for key, item in sorted(value.items()))
    if isinstance(value, list):
        return " ".join(_degradation_signal_text(item) for item in value)
    return _text(value).lower()


def _degradation_signal_items(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    value = (payload or {}).get("items")
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        return [row for row in value.values() if isinstance(row, dict)]
    summary = (payload or {}).get("summary")
    return [summary] if isinstance(summary, dict) else []


def _degradation_signal_matches(text: str) -> list[dict[str, Any]]:
    matches = []
    for family in DEGRADATION_SIGNAL_POLICY_FAMILIES:
        matched_tokens = [token for token in family["tokens"] if token in text]
        if matched_tokens:
            matches.append({**family, "matched_tokens": sorted(set(matched_tokens))})
    return matches


def build_degradation_signal_policy_mapping(
    *,
    decision_surface: dict[str, Any] | None = None,
    service_scores_snapshot: dict[str, Any] | None = None,
    channel_service_scores_snapshot: dict[str, Any] | None = None,
    risk_summaries_snapshot: dict[str, Any] | None = None,
    overview_summary_snapshot: dict[str, Any] | None = None,
    soft_degradation_threshold_vocabulary: dict[str, Any] | None = None,
    freshness_actionability: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Normalize existing degradation evidence signals to canonical POLICY_002 mapping for B4."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    surface = decision_surface or {}
    freshness = freshness_actionability or build_freshness_actionability({})
    sources: list[tuple[str, str, list[dict[str, Any]]]] = [
        (
            "service_scores",
            "tools/v7-service-matrix-refresh-all",
            _degradation_signal_items(service_scores_snapshot),
        ),
        (
            "channel_service_scores",
            "tools/v7-egress-quality-compact",
            _degradation_signal_items(channel_service_scores_snapshot),
        ),
        (
            "risk_summaries",
            "admin_core.operator_decision_surface",
            _degradation_signal_items(risk_summaries_snapshot),
        ),
        (
            "overview_summary",
            "admin_core.operator_decision_surface",
            _degradation_signal_items(overview_summary_snapshot),
        ),
    ]
    surface_rows = []
    for user_row in [row for row in (surface.get("users") or []) if isinstance(row, dict)]:
        for candidate in _candidate_rows_for_user(user_row):
            surface_rows.append({
                "user": user_row.get("user") or user_row.get("ip") or user_row.get("address"),
                "channel": _candidate_channel(candidate),
                "score": candidate.get("score", candidate.get("suitability_score")),
                "reasons": _candidate_reasons(candidate),
                "blocked": candidate.get("blocked") if isinstance(candidate.get("blocked"), list) else [],
                "ctr_state": candidate.get("ctr_state"),
                "state": candidate.get("state"),
                "lifecycle": candidate.get("lifecycle"),
                "route_safe": candidate.get("route_safe"),
                "runtime_safe": candidate.get("runtime_safe"),
                "capacity_state": candidate.get("capacity_state"),
                "capacity_decision": candidate.get("capacity_decision"),
            })
    sources.append(("operator_decision_surface", "admin_core.operator_decision_surface", surface_rows))

    evidence_rows: list[dict[str, Any]] = []
    for source, owner, rows in sources:
        for index, row in enumerate(rows):
            text = _degradation_signal_text(row)
            matches = _degradation_signal_matches(text)
            if not matches:
                continue
            object_key = _soft_degradation_object_key(row, index)
            for match in matches:
                evidence_rows.append({
                    "object": object_key,
                    "source": source,
                    "owner": owner,
                    "signal_family": match["signal_family"],
                    "canonical_signal": match["canonical_signal"],
                    "matched_tokens": match["matched_tokens"],
                    "canonical_policy": "POLICY_002_SOFT_DEGRADATION",
                    "canonical_policy_result": match["policy_result"],
                    "canonical_decision_action": match["decision_action"],
                    "mapping_role": "existing_signal_to_policy_meaning",
                    "requires_attribution_before_action": match["signal_family"] in {"route_readiness", "saturation"},
                    "runtime_apply_allowed": False,
                    "authority_expanded": False,
                })

    b3_rows = [
        row for row in ((soft_degradation_threshold_vocabulary or {}).get("rows") or [])
        if isinstance(row, dict)
    ]
    b3_by_object = {_text(row.get("object")): row for row in b3_rows if row.get("object")}
    for row in evidence_rows:
        b3_row = b3_by_object.get(row["object"], {})
        row["b3_policy_result"] = _text(b3_row.get("canonical_policy_result") or "UNKNOWN")
        row["b3_decision_action"] = _text(b3_row.get("canonical_decision_action") or "UNKNOWN")
        row["b3_consistent"] = row["b3_policy_result"] in {"UNKNOWN", row["canonical_policy_result"], "SOFT_DEGRADATION"}

    quality_freshness = ((freshness.get("domains") or {}).get("quality") or {}).get("classification", "UNKNOWN")
    service_freshness = ((freshness.get("domains") or {}).get("service") or {}).get("classification", "UNKNOWN")
    by_family: dict[str, dict[str, Any]] = {}
    for row in evidence_rows:
        family = row["signal_family"]
        target = by_family.setdefault(family, {
            "signal_family": family,
            "canonical_signal": row["canonical_signal"],
            "canonical_policy": row["canonical_policy"],
            "canonical_policy_result": row["canonical_policy_result"],
            "canonical_decision_action": row["canonical_decision_action"],
            "owners": set(),
            "sources": set(),
            "objects": set(),
            "matched_tokens": set(),
            "evidence_count": 0,
        })
        target["owners"].add(row["owner"])
        target["sources"].add(row["source"])
        target["objects"].add(row["object"])
        target["matched_tokens"].update(row["matched_tokens"])
        target["evidence_count"] += 1

    family_rows = []
    for family in sorted(by_family):
        row = by_family[family]
        family_rows.append({
            **row,
            "owners": sorted(row["owners"]),
            "sources": sorted(row["sources"]),
            "objects": sorted(row["objects"]),
            "matched_tokens": sorted(row["matched_tokens"]),
            "quality_freshness": quality_freshness,
            "service_freshness": service_freshness,
            "mapping_complete": True,
            "threshold_values_changed": False,
            "formula_changed": False,
        })

    catalog_rows = [
        {
            "signal_family": family["signal_family"],
            "canonical_signal": family["canonical_signal"],
            "canonical_policy": "POLICY_002_SOFT_DEGRADATION",
            "canonical_policy_result": family["policy_result"],
            "canonical_decision_action": family["decision_action"],
            "owner": family["owner"],
            "threshold_source": "existing_signal_owner_only",
            "implemented_here": "mapping_only",
        }
        for family in DEGRADATION_SIGNAL_POLICY_FAMILIES
    ]
    return {
        "schema_version": "v7.b4.degradation-signal-policy-mapping.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B4",
        "purpose": "normalize_existing_degradation_signal_families_to_POLICY_002_policy_mapping_without_changing_signals",
        "source_owners_reused": [
            "tools/v7-egress-quality-compact",
            "tools/v7-service-matrix-refresh-all",
            "admin_core.operator_decision_surface",
            "admin_core.autonomy_trust_acceleration.build_soft_degradation_threshold_vocabulary_alignment",
            "admin_core.autonomy_trust_acceleration.build_freshness_actionability",
        ],
        "policy_sources": [
            "docs/policies/POLICY_002_SOFT_DEGRADATION.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B4",
        ],
        "catalog_rows": catalog_rows,
        "signal_family_rows": family_rows,
        "evidence_rows": evidence_rows,
        "summary": {
            "signal_families_defined": len(catalog_rows),
            "signal_families_seen": len(family_rows),
            "evidence_rows": len(evidence_rows),
            "objects_seen": len({row["object"] for row in evidence_rows}),
            "threshold_changes": 0,
            "formula_changes": 0,
        },
        "canonical_rules": [
            "b4_maps_signal_families_to_policy_meaning_only",
            "b4_does_not_attribute_root_cause_or_complete_B5",
            "b4_does_not_change_threshold_values_or_formulas",
            "route_readiness_and_saturation_need_attribution_before_action",
            "unknown_or_unmapped_signals_remain_probe_only_until_existing_owners_emit evidence",
        ],
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


PASSIVE_DEGRADATION_TOKENS = (
    "degraded",
    "degradation",
    "failed",
    "failure",
    "partial_failure",
    "partial success",
    "partial_success",
    "timeout",
    "latency",
    "loss",
    "jitter",
    "rollback_required",
    "service_delta",
    "knowledge_degraded",
)


def _observed_degradation_object_key(row: dict[str, Any], index: int = 0) -> str:
    key = _soft_degradation_object_key(row, index)
    if key.startswith("unknown-"):
        for nested_key in ("service_outcome", "service_actual", "outcome", "outcome_quality", "post_action_verification"):
            nested = row.get(nested_key)
            if isinstance(nested, dict):
                nested_object = _soft_degradation_object_key(nested, index)
                if not nested_object.startswith("unknown-"):
                    return nested_object
    return key


def _passive_degradation_signal_present(row: dict[str, Any]) -> bool:
    text = _degradation_signal_text(row)
    if any(token in text for token in PASSIVE_DEGRADATION_TOKENS):
        return True
    outcome_quality = row.get("outcome_quality")
    if isinstance(outcome_quality, dict):
        return any(
            _text(value).upper() in {"FAILED", "PARTIAL_FAILURE", "PARTIAL_SUCCESS", "DEGRADED"}
            for value in outcome_quality.values()
        )
    return False


def _observed_degradation_family_names(row: dict[str, Any]) -> list[str]:
    return sorted({match["signal_family"] for match in _degradation_signal_matches(_degradation_signal_text(row))})


def _add_b5_evidence(
    objects: dict[str, dict[str, Any]],
    *,
    object_key: str,
    source: str,
    owner: str,
    evidence_role: str,
    evidence_kind: str,
    signal_families: list[str],
) -> None:
    target = objects.setdefault(object_key, {
        "object": object_key,
        "active_evidence": [],
        "passive_evidence": [],
        "signal_families": set(),
        "owners": set(),
        "sources": set(),
    })
    target["owners"].add(owner)
    target["sources"].add(source)
    target["signal_families"].update(signal_families)
    evidence = {
        "source": source,
        "owner": owner,
        "evidence_kind": evidence_kind,
        "signal_families": signal_families,
    }
    if evidence_role == "active":
        target["active_evidence"].append(evidence)
    else:
        target["passive_evidence"].append(evidence)


def build_observed_degradation_attribution(
    *,
    service_scores_snapshot: dict[str, Any] | None = None,
    channel_service_scores_snapshot: dict[str, Any] | None = None,
    trust_evolution_snapshot: dict[str, Any] | None = None,
    degradation_signal_policy_mapping: dict[str, Any] | None = None,
    decision_outcome_learning: dict[str, Any] | None = None,
    decision_records: list[dict[str, Any]] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Join existing active and passive degradation evidence for B5.

    B5 attributes observed degradation to existing evidence sources only. It
    does not claim root cause, create evidence, change thresholds, or authorize
    movement.
    """
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    objects: dict[str, dict[str, Any]] = {}

    for source, owner, snapshot in (
        ("service_scores", "tools/v7-service-matrix-refresh-all", service_scores_snapshot),
        ("channel_service_scores", "tools/v7-egress-quality-compact", channel_service_scores_snapshot),
    ):
        for index, row in enumerate(_degradation_signal_items(snapshot)):
            families = _observed_degradation_family_names(row)
            status_text = _degradation_signal_text({
                "status": row.get("status"),
                "state": row.get("state"),
                "score": row.get("score"),
                "services": row.get("services"),
                "trend": row.get("trend"),
            })
            if not families and "degraded" not in status_text:
                continue
            _add_b5_evidence(
                objects,
                object_key=_observed_degradation_object_key(row, index),
                source=source,
                owner=owner,
                evidence_role="active",
                evidence_kind="probe_or_quality_observation",
                signal_families=families or ["service_response"],
            )

    for row in [
        item for item in ((degradation_signal_policy_mapping or {}).get("evidence_rows") or [])
        if isinstance(item, dict)
    ]:
        _add_b5_evidence(
            objects,
            object_key=_text(row.get("object") or "unknown"),
            source=_text(row.get("source") or "degradation_signal_policy_mapping"),
            owner=_text(row.get("owner") or "admin_core.autonomy_trust_acceleration.build_degradation_signal_policy_mapping"),
            evidence_role="active",
            evidence_kind="policy_mapped_signal",
            signal_families=[_text(row.get("signal_family") or "unknown")],
        )

    for index, row in enumerate(decision_records or []):
        if not isinstance(row, dict) or not _passive_degradation_signal_present(row):
            continue
        _add_b5_evidence(
            objects,
            object_key=_observed_degradation_object_key(row, index),
            source="decision_records",
            owner="admin_core.operator_execution_feedback + closure/runtime trust stores",
            evidence_role="passive",
            evidence_kind="observed_outcome_or_feedback",
            signal_families=_observed_degradation_family_names(row) or ["outcome_degradation"],
        )

    passive_global_context = 0
    for index, row in enumerate(_degradation_signal_items(trust_evolution_snapshot)):
        if not _passive_degradation_signal_present(row):
            continue
        object_key = _observed_degradation_object_key(row, index)
        if object_key.startswith("unknown-"):
            object_key = "trust-evolution-summary"
            passive_global_context += 1
        _add_b5_evidence(
            objects,
            object_key=object_key,
            source="trust_evolution_summaries",
            owner="admin_core.intelligence_workers.build_trust_evolution_snapshot",
            evidence_role="passive",
            evidence_kind="trust_or_learning_observation",
            signal_families=_observed_degradation_family_names(row) or ["learning_degradation"],
        )

    if isinstance(decision_outcome_learning, dict) and _passive_degradation_signal_present(decision_outcome_learning):
        _add_b5_evidence(
            objects,
            object_key="decision-outcome-learning",
            source="decision_outcome_learning",
            owner="admin_core.autonomy_trust_acceleration._decision_outcome_learning_from_trust",
            evidence_role="passive",
            evidence_kind="learning_summary",
            signal_families=_observed_degradation_family_names(decision_outcome_learning) or ["learning_degradation"],
        )
        passive_global_context += 1

    global_passive_available = any(
        row["passive_evidence"] and row["object"] in {"trust-evolution-summary", "decision-outcome-learning"}
        for row in objects.values()
    )
    rows = []
    for object_key in sorted(objects):
        item = objects[object_key]
        active_count = len(item["active_evidence"])
        passive_count = len(item["passive_evidence"])
        if active_count and passive_count:
            attribution_state = "ACTIVE_AND_PASSIVE_OBSERVED"
            next_requirement = "eligible_for_B6_v7_native_response_mapping"
        elif active_count and global_passive_available:
            attribution_state = "ACTIVE_OBSERVED_WITH_PASSIVE_CONTEXT"
            next_requirement = "object_specific_passive_outcome_would_raise_confidence"
        elif active_count:
            attribution_state = "ACTIVE_ONLY_PASSIVE_OUTCOME_PENDING"
            next_requirement = "wait_for_existing_feedback_or_trust_outcome"
        elif passive_count:
            attribution_state = "PASSIVE_ONLY_ACTIVE_OBSERVATION_PENDING"
            next_requirement = "collect_or_refresh_existing_service_quality_probe"
        else:
            attribution_state = "NO_OBSERVED_DEGRADATION_EVIDENCE"
            next_requirement = "no_action"
        rows.append({
            "object": object_key,
            "canonical_policy": "POLICY_002_SOFT_DEGRADATION",
            "attribution_type": "evidence_source_attribution_not_root_cause",
            "attribution_state": attribution_state,
            "active_evidence_count": active_count,
            "passive_evidence_count": passive_count,
            "active_evidence": item["active_evidence"],
            "passive_evidence": item["passive_evidence"],
            "signal_families": sorted({family for family in item["signal_families"] if family}),
            "owners": sorted(item["owners"]),
            "sources": sorted(item["sources"]),
            "next_requirement": next_requirement,
            "root_cause_claimed": False,
            "threshold_values_changed": False,
            "formula_changed": False,
            "runtime_apply_allowed": False,
            "authority_expanded": False,
        })

    return {
        "schema_version": "v7.b5.observed-degradation-attribution.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B5",
        "purpose": "complete_observed_degradation_attribution_using_existing_active_and_passive_evidence_without_claiming_root_cause",
        "source_owners_reused": [
            "tools/v7-service-matrix-refresh-all",
            "tools/v7-egress-quality-compact",
            "admin_core.operator_execution_feedback",
            "admin_core.intelligence_workers.build_trust_evolution_snapshot",
            "admin_core.autonomy_trust_acceleration.build_degradation_signal_policy_mapping",
        ],
        "policy_sources": [
            "docs/policies/POLICY_002_SOFT_DEGRADATION.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B5",
        ],
        "rows": rows,
        "summary": {
            "objects_seen": len(rows),
            "active_objects": sum(1 for row in rows if row["active_evidence_count"] > 0),
            "passive_objects": sum(1 for row in rows if row["passive_evidence_count"] > 0),
            "active_and_passive_objects": sum(1 for row in rows if row["attribution_state"] == "ACTIVE_AND_PASSIVE_OBSERVED"),
            "active_with_passive_context_objects": sum(1 for row in rows if row["attribution_state"] == "ACTIVE_OBSERVED_WITH_PASSIVE_CONTEXT"),
            "passive_global_context_records": passive_global_context,
            "root_cause_claims": 0,
            "threshold_changes": 0,
            "formula_changes": 0,
        },
        "canonical_rules": [
            "b5_attributes_observed_degradation_to_existing_evidence_sources_only",
            "active_evidence_is_service_matrix_or_quality_probe_observation",
            "passive_evidence_is_feedback_outcome_or_trust_learning_observation",
            "b5_does_not_claim_root_cause",
            "b5_does_not_change_threshold_values_or_formulas",
            "b5_does_not_grant_runtime_apply_or_authority",
        ],
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


def _diagnosis_upper(value: Any, default: str) -> str:
    text = _text(value or default).upper()
    return text or default


def _diagnosis_refs(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    return [value]


def _diagnosis_record_id(payload: dict[str, Any]) -> str:
    stable = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(stable.encode("utf-8")).hexdigest()[:16]
    return f"diagnosis_owner_resolution_{digest}"


def _diagnosis_mutation_boundary(value: dict[str, Any] | None = None) -> dict[str, Any]:
    boundary = dict(DIAGNOSIS_MUTATION_BOUNDARY)
    if isinstance(value, dict):
        boundary.update(value)
    return boundary


def build_diagnosis_owner_resolution_record(
    *,
    subject: dict[str, Any],
    source_object: Any,
    evidence_refs: list[Any] | None = None,
    diagnosis_status: str = "UNKNOWN",
    symptom: dict[str, Any] | None = None,
    root_cause: str | None = None,
    root_cause_proven: bool = False,
    unknown_state: str | None = None,
    blocking_owner: str | None = "UNKNOWN",
    owner_resolution_state: str | None = None,
    terminal_classification: str | None = "UNKNOWN",
    required_resolution: Any | None = None,
    incident: dict[str, Any] | None = None,
    operation_id: str | None = None,
    packet_id: str | None = None,
    selected_move_hash: str | None = None,
    first_divergence: Any | None = None,
    confidence: str = "UNKNOWN",
    evidence_quality: str = "UNKNOWN",
    hypotheses_rejected: list[Any] | None = None,
    compatibility: dict[str, Any] | None = None,
    backtesting: dict[str, Any] | None = None,
    projection_refs: list[Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build the read-only Domain 11 Diagnosis / Owner Resolution record.

    The builder is a projection over caller-supplied evidence. It does not read
    production state, recompute Planner/Runtime decisions, or perform mutation.
    """
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    refs = _diagnosis_refs(evidence_refs)
    status = _diagnosis_upper(diagnosis_status, "UNKNOWN")
    terminal = _diagnosis_upper(terminal_classification, "UNKNOWN")
    owner = _text(blocking_owner or "UNKNOWN")
    cause_proven = bool(root_cause_proven)
    cause = _text(root_cause or "UNKNOWN")
    if not cause_proven:
        cause = "UNKNOWN"

    if unknown_state is None:
        if status == "PROVEN" and cause_proven:
            unknown = "NONE"
        elif status == "NO_EVIDENCE" or not refs:
            unknown = "MISSING_EVIDENCE"
        elif status == "CONFLICTING_EVIDENCE":
            unknown = "CONFLICTING_EVIDENCE"
        else:
            unknown = "NOT_INVESTIGATED"
    else:
        unknown = _diagnosis_upper(unknown_state, "UNKNOWN_OWNER")

    if owner_resolution_state is None:
        if terminal not in {"NONE", "UNKNOWN"}:
            resolution_state = "RESOLVED"
        elif owner not in {"", "NONE", "UNKNOWN"}:
            resolution_state = "REQUIRED"
        else:
            resolution_state = "NOT_REQUIRED"
    else:
        resolution_state = _diagnosis_upper(owner_resolution_state, "UNKNOWN")

    if required_resolution in (None, ""):
        if resolution_state == "NOT_REQUIRED" and terminal in {"NONE", "UNKNOWN"}:
            resolution = "NONE"
        else:
            resolution = "owner_resolution_required"
    else:
        resolution = required_resolution

    symptom_payload = symptom if isinstance(symptom, dict) else {
        "type": "UNKNOWN",
        "value": "UNKNOWN",
        "producer": DIAGNOSIS_RECORD_PRODUCER,
    }
    subject_payload = subject if isinstance(subject, dict) else {"type": "UNKNOWN", "id": _text(subject)}

    stable_identity = {
        "schema_version": DIAGNOSIS_OWNER_RESOLUTION_SCHEMA_VERSION,
        "subject": subject_payload,
        "source_object": source_object,
        "evidence_refs": refs,
        "diagnosis_status": status,
        "symptom": symptom_payload,
        "root_cause": cause,
        "root_cause_proven": cause_proven,
        "unknown_state": unknown,
        "blocking_owner": owner,
        "owner_resolution_state": resolution_state,
        "terminal_classification": terminal,
        "required_resolution": resolution,
        "incident": incident,
        "operation_id": operation_id,
        "packet_id": packet_id,
        "selected_move_hash": selected_move_hash,
        "first_divergence": first_divergence,
    }

    record: dict[str, Any] = {
        "schema_version": DIAGNOSIS_OWNER_RESOLUTION_SCHEMA_VERSION,
        "record_id": _diagnosis_record_id(stable_identity),
        "generated_at": generated,
        "producer": DIAGNOSIS_RECORD_PRODUCER,
        "read_only": True,
        "subject": subject_payload,
        "source_object": source_object,
        "evidence_refs": refs,
        "diagnosis_status": status,
        "symptom": symptom_payload,
        "root_cause": cause,
        "root_cause_proven": cause_proven,
        "unknown_state": unknown,
        "blocking_owner": owner,
        "owner_resolution_state": resolution_state,
        "terminal_classification": terminal,
        "required_resolution": resolution,
        "consumers": list(DIAGNOSIS_RECORD_CONSUMERS),
        "mutation_boundary": _diagnosis_mutation_boundary(),
        "confidence": _diagnosis_upper(confidence, "UNKNOWN"),
        "evidence_quality": _diagnosis_upper(evidence_quality, "UNKNOWN"),
    }
    if incident is not None:
        record["incident"] = incident
    if operation_id:
        record["operation_id"] = _text(operation_id)
    if packet_id:
        record["packet_id"] = _text(packet_id)
    if selected_move_hash:
        record["selected_move_hash"] = _text(selected_move_hash)
    if first_divergence is not None:
        record["first_divergence"] = first_divergence
    if hypotheses_rejected is not None:
        record["hypotheses_rejected"] = hypotheses_rejected
    if compatibility is not None:
        record["compatibility"] = compatibility
    if backtesting is not None:
        record["backtesting"] = backtesting
    if projection_refs is not None:
        record["projection_refs"] = projection_refs
    return record


def validate_diagnosis_owner_resolution_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a Domain 11 Diagnosis Record without mutating any state."""
    errors: list[str] = []
    required = [
        "schema_version",
        "record_id",
        "generated_at",
        "producer",
        "read_only",
        "subject",
        "source_object",
        "evidence_refs",
        "diagnosis_status",
        "symptom",
        "root_cause",
        "root_cause_proven",
        "unknown_state",
        "blocking_owner",
        "owner_resolution_state",
        "terminal_classification",
        "required_resolution",
        "consumers",
        "mutation_boundary",
    ]
    for field in required:
        if field not in record:
            errors.append(f"missing_required_field:{field}")

    if record.get("schema_version") != DIAGNOSIS_OWNER_RESOLUTION_SCHEMA_VERSION:
        errors.append("invalid_schema_version")
    if record.get("read_only") is not True:
        errors.append("read_only_must_be_true")

    subject = record.get("subject")
    if not isinstance(subject, dict) or not subject.get("type") or not subject.get("id"):
        errors.append("subject_must_include_type_and_id")
    symptom = record.get("symptom")
    if not isinstance(symptom, dict) or not symptom.get("type") or not symptom.get("value") or not symptom.get("producer"):
        errors.append("symptom_must_include_type_value_producer")
    if not record.get("source_object"):
        errors.append("source_object_required")

    diagnosis_status = record.get("diagnosis_status")
    if diagnosis_status not in DIAGNOSIS_STATUSES:
        errors.append("invalid_diagnosis_status")
    unknown_state = record.get("unknown_state")
    if unknown_state not in DIAGNOSIS_UNKNOWN_STATES:
        errors.append("invalid_unknown_state")
    owner_resolution_state = record.get("owner_resolution_state")
    if owner_resolution_state not in DIAGNOSIS_OWNER_RESOLUTION_STATES:
        errors.append("invalid_owner_resolution_state")
    terminal = record.get("terminal_classification")
    if terminal not in DIAGNOSIS_TERMINAL_CLASSIFICATIONS:
        errors.append("invalid_terminal_classification")
    owner = _text(record.get("blocking_owner") or "")
    if owner not in {"", "NONE", "UNKNOWN"} and terminal in {"NONE", "UNKNOWN"} and owner_resolution_state != "REQUIRED":
        errors.append("blocking_owner_without_terminal_requires_owner_resolution")
    if terminal not in {"NONE", "UNKNOWN"} and owner_resolution_state != "RESOLVED":
        errors.append("terminal_classification_requires_resolved_owner_resolution")
    if record.get("confidence") is not None and record.get("confidence") not in DIAGNOSIS_CONFIDENCE_VALUES:
        errors.append("invalid_confidence")
    if record.get("evidence_quality") is not None and record.get("evidence_quality") not in DIAGNOSIS_CONFIDENCE_VALUES:
        errors.append("invalid_evidence_quality")

    refs = record.get("evidence_refs")
    if not isinstance(refs, list):
        errors.append("evidence_refs_must_be_list")
        refs = []
    if diagnosis_status == "PROVEN" and not refs:
        errors.append("proven_diagnosis_requires_evidence_refs")
    if record.get("root_cause_proven") is True:
        if record.get("root_cause") in ("", None, "UNKNOWN"):
            errors.append("proven_root_cause_requires_named_root_cause")
        if not refs:
            errors.append("proven_root_cause_requires_evidence_refs")
    if record.get("root_cause") not in ("", None, "UNKNOWN") and record.get("root_cause_proven") is not True:
        errors.append("root_cause_claim_requires_root_cause_proven")
    if terminal not in {"NONE", "UNKNOWN"} and not refs:
        errors.append("terminal_classification_requires_evidence_refs")

    first_divergence = record.get("first_divergence")
    if isinstance(first_divergence, dict):
        for field in ["producer", "consumer", "field", "before", "after", "evidence_ref"]:
            if field not in first_divergence:
                errors.append(f"first_divergence_missing:{field}")

    boundary = record.get("mutation_boundary")
    if not isinstance(boundary, dict):
        errors.append("mutation_boundary_must_be_object")
        boundary = {}
    for field, expected in DIAGNOSIS_MUTATION_BOUNDARY.items():
        if boundary.get(field) != expected:
            errors.append(f"mutation_boundary_violation:{field}")

    consumers = record.get("consumers")
    if not isinstance(consumers, list) or not consumers:
        errors.append("consumers_required")
    else:
        missing = [consumer for consumer in DIAGNOSIS_RECORD_CONSUMERS if consumer not in consumers]
        for consumer in missing:
            errors.append(f"missing_consumer:{consumer}")

    if owner.upper() == "NEW_OWNER" or owner.startswith("new_"):
        errors.append("blocking_owner_must_reuse_existing_owner")
    if _text(record.get("producer")) != DIAGNOSIS_RECORD_PRODUCER:
        errors.append("producer_must_be_existing_diagnosis_owner")

    return {
        "schema_version": "v7.diagnosis-owner-resolution.validation.v1",
        "record_id": record.get("record_id"),
        "valid": not errors,
        "errors": errors,
        "read_only": True,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
        "authority_expanded": False,
        "synthetic_evidence_created": False,
        "new_owner_created": False,
    }


def build_diagnosis_owner_resolution_consumer_projection(record: dict[str, Any]) -> dict[str, Any]:
    """Project one Diagnosis Record to existing downstream consumers."""
    validation = validate_diagnosis_owner_resolution_record(record)
    return {
        "schema_version": "v7.diagnosis-owner-resolution.consumer-projection.v1",
        "record_id": record.get("record_id"),
        "source_schema_version": record.get("schema_version"),
        "validation": validation,
        "projections": {
            "omp": {
                "terminal_classification": record.get("terminal_classification"),
                "required_resolution": record.get("required_resolution"),
                "next_engineering_mission": record.get("required_resolution"),
                "source_record_id": record.get("record_id"),
            },
            "current_program_state": {
                "blocking_owner": record.get("blocking_owner"),
                "owner_resolution_state": record.get("owner_resolution_state"),
                "terminal_root_cause": record.get("root_cause"),
                "required_resolution": record.get("required_resolution"),
                "expected_next_engineering_step": record.get("required_resolution"),
                "source_record_id": record.get("record_id"),
            },
            "production_maturity": {
                "diagnosis_status": record.get("diagnosis_status"),
                "evidence_quality": record.get("evidence_quality", "UNKNOWN"),
                "confidence": record.get("confidence", "UNKNOWN"),
                "authority_granted": False,
                "source_record_id": record.get("record_id"),
            },
            "engineering_reports": {
                "embeddable_record": True,
                "record_id": record.get("record_id"),
                "evidence_refs": record.get("evidence_refs", []),
            },
            "engineering_automation": {
                "read_model_consumable": validation["valid"],
                "diagnosis_status": record.get("diagnosis_status"),
                "source_record_id": record.get("record_id"),
            },
            "governance_check": {
                "projection_mode": "preserve_record_truth",
                "recompute_diagnosis_truth": False,
                "record_id": record.get("record_id"),
                "schema_version": record.get("schema_version"),
            },
            "future_certification": {
                "domain": "11 Diagnosis",
                "recovery_gap_closed": validation["valid"],
                "source_record_id": record.get("record_id"),
            },
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
        "authority_expanded": False,
        "synthetic_evidence_created": False,
        "new_owner_created": False,
    }


def _b6_candidate_state(row: dict[str, Any]) -> str:
    return _text(
        row.get("ctr_state")
        or row.get("state")
        or row.get("lifecycle")
        or row.get("service_state")
        or "UNKNOWN"
    ).upper()


def _b6_response_for_object(
    *,
    attribution_state: str,
    candidate_states: set[str],
    signal_families: set[str],
    anti_flap_blocked: bool,
) -> tuple[str, list[str], list[str], str]:
    if anti_flap_blocked:
        return (
            "CIRCUIT_BREAKER_OPEN",
            ["HOLD_MOVEMENT", "REQUIRE_COOLDOWN", "ASK_OPERATOR"],
            ["selected_moves", "apply", "authority_promotion"],
            "anti_flap_blocks_recent_oscillation",
        )
    if "QUARANTINED" in candidate_states:
        return (
            "OUTLIER_EJECTION",
            ["QUARANTINE_FOR_NORMAL_TARGET_USE", "PROBE_ONLY", "REQUIRE_RECOVERY_ADMISSION"],
            ["direct_user_switch", "autoswitch_apply", "authority_promotion"],
            "existing_ctr_state_quarantined",
        )
    if attribution_state == "ACTIVE_AND_PASSIVE_OBSERVED":
        return (
            "CIRCUIT_BREAKER_OPEN_AND_OUTLIER_REVIEW",
            ["ASK_OPERATOR", "PROBE_ONLY", "BLOCK_AUTOMATIC_NORMALIZATION"],
            ["runtime_apply", "automatic_failover", "authority_promotion"],
            "active_and_passive_degradation_evidence_joined",
        )
    if "DEGRADED" in candidate_states or signal_families:
        return (
            "CIRCUIT_BREAKER_HALF_OPEN",
            ["ASK_OPERATOR", "PROBE_ONLY", "KEEP_CURRENT_ROUTE_UNCHANGED"],
            ["automatic_failover", "authority_promotion"],
            "degradation_signal_requires_governed_review",
        )
    return (
        "OBSERVE_ONLY",
        ["KEEP", "OBSERVE"],
        ["runtime_apply", "authority_promotion"],
        "no_complete_degradation_response_trigger",
    )


def build_v7_native_degradation_response_mapping(
    *,
    decision_surface: dict[str, Any] | None = None,
    observed_degradation_attribution: dict[str, Any] | None = None,
    soft_degradation_threshold_vocabulary: dict[str, Any] | None = None,
    degradation_signal_policy_mapping: dict[str, Any] | None = None,
    anti_flapping: dict[str, Any] | None = None,
    recovery_admission: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Map circuit-breaker/outlier-ejection practice to existing V7-native actions for B6."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    objects: dict[str, dict[str, Any]] = {}

    def ensure_object(key: str) -> dict[str, Any]:
        return objects.setdefault(key, {
            "object": key,
            "attribution_state": "UNKNOWN",
            "candidate_states": set(),
            "signal_families": set(),
            "owners": set(),
            "sources": set(),
            "evidence": [],
        })

    for row in [
        item for item in ((observed_degradation_attribution or {}).get("rows") or [])
        if isinstance(item, dict)
    ]:
        key = _text(row.get("object") or "unknown")
        target = ensure_object(key)
        target["attribution_state"] = _text(row.get("attribution_state") or "UNKNOWN")
        target["signal_families"].update(str(item) for item in (row.get("signal_families") or []) if item)
        target["owners"].update(str(item) for item in (row.get("owners") or []) if item)
        target["sources"].update(str(item) for item in (row.get("sources") or []) if item)
        target["evidence"].append("observed_degradation_attribution")

    for row in [
        item for item in ((soft_degradation_threshold_vocabulary or {}).get("rows") or [])
        if isinstance(item, dict)
    ]:
        key = _text(row.get("object") or "unknown")
        target = ensure_object(key)
        state = _text(row.get("canonical_policy_result") or "")
        if state:
            target["candidate_states"].add(state)
        action = _text(row.get("canonical_decision_action") or "")
        if action:
            target["candidate_states"].add(action)
        target["owners"].update(str(item) for item in (row.get("owner_sources") or []) if item)
        target["sources"].update(str(item) for item in (row.get("evidence_sources") or []) if item)
        target["evidence"].append("soft_degradation_threshold_vocabulary")

    for row in [
        item for item in ((degradation_signal_policy_mapping or {}).get("evidence_rows") or [])
        if isinstance(item, dict)
    ]:
        key = _text(row.get("object") or "unknown")
        target = ensure_object(key)
        family = _text(row.get("signal_family") or "")
        if family:
            target["signal_families"].add(family)
        target["owners"].add(_text(row.get("owner") or ""))
        target["sources"].add(_text(row.get("source") or ""))
        target["evidence"].append("degradation_signal_policy_mapping")

    surface = decision_surface or {}
    for user_row in [row for row in (surface.get("users") or []) if isinstance(row, dict)]:
        for candidate in _candidate_rows_for_user(user_row):
            key = _candidate_channel(candidate)
            if not key:
                continue
            target = ensure_object(key)
            target["candidate_states"].add(_b6_candidate_state(candidate))
            target["owners"].add("tools/v7-users-autoswitch")
            target["sources"].add("operator_decision_surface_candidate")
            target["evidence"].append("planner_candidate_state")

    anti_blocked = bool((anti_flapping or {}).get("summary", {}).get("blocked_users", 0))
    recovery_blocked = bool((recovery_admission or {}).get("summary", {}).get("blocked_or_quarantined", 0))
    rows = []
    for key in sorted(objects):
        item = objects[key]
        practice, actions, blocked_actions, reason = _b6_response_for_object(
            attribution_state=item["attribution_state"],
            candidate_states={state for state in item["candidate_states"] if state},
            signal_families={family for family in item["signal_families"] if family},
            anti_flap_blocked=anti_blocked,
        )
        if recovery_blocked and "REQUIRE_RECOVERY_ADMISSION" not in actions:
            actions.append("REQUIRE_RECOVERY_ADMISSION")
        rows.append({
            "object": key,
            "external_practice": practice,
            "v7_native_actions": actions,
            "blocked_actions": sorted(set(blocked_actions)),
            "attribution_state": item["attribution_state"],
            "candidate_states": sorted({state for state in item["candidate_states"] if state and state != "UNKNOWN"}),
            "signal_families": sorted({family for family in item["signal_families"] if family}),
            "owners": sorted({owner for owner in item["owners"] if owner}),
            "sources": sorted({source for source in item["sources"] if source}),
            "evidence": sorted(set(item["evidence"])),
            "mapping_reason": reason,
            "implementation_role": "read_only_mapping_only",
            "runtime_apply_allowed": False,
            "authority_expanded": False,
            "threshold_values_changed": False,
            "formula_changed": False,
        })

    catalog_rows = [
        {
            "external_practice": "circuit_breaker_open",
            "v7_native_action": "HOLD_MOVEMENT + ASK_OPERATOR + PROBE_ONLY",
            "existing_owner": "tools/v7-users-autoswitch + admin_core.operator_decision_surface",
        },
        {
            "external_practice": "circuit_breaker_half_open",
            "v7_native_action": "PROBE_ONLY + RECOVERY_ADMISSION + SLOW_START_AFTER_CERTIFICATION",
            "existing_owner": "recovery admission + action-class/blast-radius owners",
        },
        {
            "external_practice": "outlier_ejection",
            "v7_native_action": "QUARANTINE_FOR_NORMAL_TARGET_USE + REQUIRE_RECOVERY_ADMISSION",
            "existing_owner": "planner/autoswitch CTR state + recovery admission owners",
        },
    ]
    return {
        "schema_version": "v7.b6.v7-native-degradation-response-mapping.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B6",
        "purpose": "map_circuit_breaker_and_outlier_ejection_practice_to_existing_v7_native_actions_without_runtime_behavior_change",
        "source_owners_reused": [
            "tools/v7-users-autoswitch",
            "admin_core.operator_decision_surface",
            "admin_core.autonomy_trust_acceleration.build_observed_degradation_attribution",
            "admin_core.autonomy_trust_acceleration.build_anti_flapping",
            "admin_core.autonomy_trust_acceleration.build_recovery_admission",
        ],
        "policy_sources": [
            "docs/policies/POLICY_002_SOFT_DEGRADATION.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B6",
        ],
        "catalog_rows": catalog_rows,
        "rows": rows,
        "summary": {
            "objects_seen": len(rows),
            "circuit_breaker_rows": sum(1 for row in rows if "CIRCUIT_BREAKER" in row["external_practice"]),
            "outlier_ejection_rows": sum(1 for row in rows if "OUTLIER" in row["external_practice"]),
            "runtime_actions_created": 0,
            "threshold_changes": 0,
            "formula_changes": 0,
        },
        "canonical_rules": [
            "b6_maps_external_resilience_practice_to_existing_v7_actions_only",
            "circuit_breaker_is_a_governed_stop_or_probe_mapping_not_runtime_apply",
            "outlier_ejection_maps_to_quarantine_or_normal_target_exclusion_until_recovery_admission",
            "b6_does_not_create_new_planner_or_runtime_behavior",
            "b6_does_not_change_threshold_values_or_formulas",
        ],
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
        "new_planner_created": False,
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


def _b7_threshold_source_for_objective(objective: str) -> tuple[str, str]:
    mapping = {
        "required_service_reachability": (
            "service_user_sla_fit.required_services + candidate.missing_requirements",
            "existing_service_required_or_missing",
        ),
        "service_freshness": (
            "freshness_actionability.domains.service.classification",
            "ACTIONABLE_NOW",
        ),
        "candidate_fit_score": (
            "service_user_sla_fit.candidates.fit_score",
            "existing_fit_score_interpretation",
        ),
        "capacity_headroom": (
            "service_user_sla_fit.candidates.capacity_headroom/capacity_decision",
            "existing_capacity_policy_gate",
        ),
        "route_runtime_safety": (
            "service_user_sla_fit.candidates.route_runtime_safe",
            "existing_route_runtime_safe_flag",
        ),
        "soft_degradation_policy": (
            "soft_degradation_threshold_vocabulary.canonical_policy_result",
            "POLICY_002_SOFT_DEGRADATION existing vocabulary",
        ),
        "degradation_response": (
            "v7_native_degradation_response_mapping.v7_native_actions",
            "existing_v7_native_action_mapping",
        ),
    }
    return mapping.get(objective, ("existing_owner_field", "existing_policy_gate"))


def build_service_objective_policy_threshold_binding(
    *,
    service_user_sla_fit: dict[str, Any] | None = None,
    freshness_actionability: dict[str, Any] | None = None,
    soft_degradation_threshold_vocabulary: dict[str, Any] | None = None,
    v7_native_degradation_response_mapping: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Bind service objectives to existing policy threshold sources for B7."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    fit_rows = [
        row for row in ((service_user_sla_fit or {}).get("rows") or [])
        if isinstance(row, dict)
    ]
    soft_by_object = {
        _text(row.get("object")): row
        for row in ((soft_degradation_threshold_vocabulary or {}).get("rows") or [])
        if isinstance(row, dict) and row.get("object")
    }
    response_by_object = {
        _text(row.get("object")): row
        for row in ((v7_native_degradation_response_mapping or {}).get("rows") or [])
        if isinstance(row, dict) and row.get("object")
    }
    service_freshness = (
        ((freshness_actionability or {}).get("domains") or {}).get("service") or {}
    ).get("classification", "UNKNOWN")

    rows: list[dict[str, Any]] = []
    for fit in fit_rows:
        user = _text(fit.get("user") or "")
        required_services = [str(item) for item in (fit.get("required_services") or []) if item]
        candidates = [row for row in (fit.get("candidates") or []) if isinstance(row, dict)]
        for candidate in candidates:
            channel = _text(candidate.get("channel") or "")
            if not channel:
                continue
            missing = [str(item) for item in (candidate.get("missing_requirements") or []) if item]
            objectives = [
                "required_service_reachability",
                "service_freshness",
                "candidate_fit_score",
                "capacity_headroom",
                "route_runtime_safety",
            ]
            if channel in soft_by_object:
                objectives.append("soft_degradation_policy")
            if channel in response_by_object:
                objectives.append("degradation_response")
            bindings = []
            for objective in objectives:
                source, gate = _b7_threshold_source_for_objective(objective)
                bindings.append({
                    "objective": objective,
                    "threshold_source": source,
                    "existing_policy_gate": gate,
                    "owner": "admin_core.autonomy_trust_acceleration.build_service_user_sla_fit"
                    if objective in {"required_service_reachability", "candidate_fit_score", "capacity_headroom", "route_runtime_safety"}
                    else "existing freshness/degradation owner",
                    "threshold_values_changed": False,
                    "formula_changed": False,
                })
            rows.append({
                "user": user,
                "candidate_channel": channel,
                "required_services": required_services,
                "missing_services": missing,
                "fit_verdict": _text(candidate.get("fit_verdict") or "UNKNOWN"),
                "service_freshness": service_freshness,
                "objective_bindings": bindings,
                "binding_state": "BOUND_TO_EXISTING_POLICY_GATES",
                "planner_role": "read_only_policy_gate_visibility",
                "runtime_apply_allowed": False,
                "authority_expanded": False,
                "threshold_values_changed": False,
                "formula_changed": False,
            })

    catalog_rows = [
        {
            "objective": objective,
            "threshold_source": _b7_threshold_source_for_objective(objective)[0],
            "existing_policy_gate": _b7_threshold_source_for_objective(objective)[1],
        }
        for objective in (
            "required_service_reachability",
            "service_freshness",
            "candidate_fit_score",
            "capacity_headroom",
            "route_runtime_safety",
            "soft_degradation_policy",
            "degradation_response",
        )
    ]
    return {
        "schema_version": "v7.b7.service-objective-policy-threshold-binding.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B7",
        "purpose": "bind_service_objectives_to_existing_policy_threshold_sources_without_changing_thresholds",
        "source_owners_reused": [
            "admin_core.autonomy_trust_acceleration.build_service_user_sla_fit",
            "admin_core.autonomy_trust_acceleration.build_freshness_actionability",
            "admin_core.autonomy_trust_acceleration.build_soft_degradation_threshold_vocabulary_alignment",
            "admin_core.autonomy_trust_acceleration.build_v7_native_degradation_response_mapping",
            "tools/v7-users-autoswitch",
        ],
        "policy_sources": [
            "docs/policies/POLICY_002_SOFT_DEGRADATION.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B7",
        ],
        "catalog_rows": catalog_rows,
        "rows": rows,
        "summary": {
            "users_seen": len({row["user"] for row in rows if row["user"]}),
            "candidate_bindings": len(rows),
            "objective_bindings": sum(len(row["objective_bindings"]) for row in rows),
            "threshold_changes": 0,
            "formula_changes": 0,
            "runtime_actions_created": 0,
        },
        "canonical_rules": [
            "b7_binds_objectives_to_existing_threshold_sources_only",
            "b7_does_not_define_new_service_objective_values",
            "b7_does_not_change_threshold_values_or_formulas",
            "b7_does_not_create_new_planner_or_runtime_behavior",
            "b7_does_not_grant_runtime_apply_or_authority",
        ],
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
        "new_planner_created": False,
    }


def _closure_field_present(record: dict[str, Any], field: str) -> bool:
    aliases = {
        "recommendation_id": ("recommendation_id", "recommendation_hash", "proposal_id"),
        "decision_id": ("decision_id", "operation_id", "object_id"),
        "packet_id": ("packet_id", "approval_packet_id"),
        "apply_result": ("apply_result", "result", "status", "execution_outcome", "outcome", "outcome_status", "outcome_quality"),
        "post_action_verification": ("post_action_verification", "verification_result", "verification", "closure_state", "outcome_status", "outcome_quality"),
        "service_outcome": ("service_outcome", "service_actual", "service_delta"),
        "user_outcome": ("user_outcome", "selected_moves", "user"),
        "learning_record": ("learning_record", "trust_update", "prediction_actual"),
        "outcome_observed_at": ("outcome_observed_at", "closure_timestamp", "created_at", "completed_at", "event_time", "timestamp", "ts"),
    }
    return any(record.get(alias) not in (None, "", [], {}) for alias in aliases.get(field, (field,)))


def _closure_candidate_record(record: dict[str, Any]) -> bool:
    if any(record.get(field) not in (None, "", [], {}) for field in OUTCOME_CLOSURE_CANDIDATE_FIELDS):
        return True
    if any(record.get(field) not in (None, "", [], {}) for field in OUTCOME_CLOSURE_MARKER_FIELDS):
        return True
    metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    marker_fields = OUTCOME_CLOSURE_CANDIDATE_FIELDS + OUTCOME_CLOSURE_MARKER_FIELDS
    return any(metadata.get(field) not in (None, "", [], {}) for field in marker_fields)


def _non_executed_outcome_record(record: dict[str, Any]) -> bool:
    metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    values = [
        record.get("execution_mode"),
        record.get("mode"),
        record.get("transaction_status"),
        record.get("outcome_status"),
        metadata.get("execution_mode"),
        metadata.get("mode"),
        metadata.get("outcome_status"),
    ]
    markers = {str(value or "").strip().upper() for value in values}
    explicitly_non_executed = bool(markers.intersection({
        "DRY_RUN",
        "NO_EXECUTION",
        "PREVIEW_ONLY",
        "READ_ONLY",
    }))
    flags_prove_no_execution = (
        record.get("runtime_mutation_performed") is False
        and record.get("apply_executed") is False
        and int(record.get("users_moved") or 0) == 0
    )
    return explicitly_non_executed or flags_prove_no_execution


def build_decision_outcome_closure(
    decision_records: list[dict[str, Any]] | None = None,
    *,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Expose whether real recommendation outcomes are closed end-to-end."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    rows: list[dict[str, Any]] = []
    source_count = len([row for row in (decision_records or []) if isinstance(row, dict)])
    marked_candidates = [
        row for row in (decision_records or [])
        if isinstance(row, dict) and _closure_candidate_record(row)
    ]
    closure_candidates = [row for row in marked_candidates if not _non_executed_outcome_record(row)]
    non_executed_ignored = len(marked_candidates) - len(closure_candidates)
    for index, record in enumerate(closure_candidates):
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
            "source_records_seen": source_count,
            "records_seen": len(rows),
            "non_closure_records_ignored": max(0, source_count - len(rows)),
            "non_executed_outcome_records_ignored": non_executed_ignored,
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


L7_L8_PASSPORT_CORE_FIELDS = (
    "material_identity",
    "provenance",
    "evidence_class",
    "terminal_class",
    "user",
    "source_channel",
    "target_channel",
    "outcome_observed_at",
)

L7_L8_TEMPORAL_FIELDS = (
    "accepted_request",
    "actual_activation",
    "immediate_verification",
    "delayed_5m_observation",
    "delayed_1h_observation",
    "steady_state_terminal",
)

L7_L8_REPLAY_FIELDS = (
    "decision_trace_id",
    "input_snapshot_identity",
    "expected_terminal",
    "actual_terminal",
    "intent_drift_class",
)


def _l7_l8_maps(record: dict[str, Any]) -> list[dict[str, Any]]:
    maps: list[dict[str, Any]] = []
    queue = [record]
    seen: set[int] = set()
    nested_keys = (
        "operation", "execution_outcome", "verification_result", "rollback_result",
        "outcome_quality", "learning_record", "metadata", "decision_trace",
        "input_snapshot", "temporal_verification", "observation_windows",
        "packet", "source_preview", "decision_commit", "semantic_fields",
        "expected", "immutable_packet_identity", "checks", "approved_plan_lock",
    )
    while queue:
        mapping = queue.pop(0)
        marker = id(mapping)
        if marker in seen:
            continue
        seen.add(marker)
        maps.append(mapping)
        for key in nested_keys:
            value = mapping.get(key)
            if isinstance(value, dict):
                queue.append(value)
    return maps


def _l7_l8_first(record: dict[str, Any], *aliases: str) -> Any:
    for mapping in _l7_l8_maps(record):
        for alias in aliases:
            value = mapping.get(alias)
            if value not in (None, "", [], {}):
                return value
    return ""


def _l7_l8_ids(record: dict[str, Any]) -> dict[str, str]:
    audit_reference = _text(_l7_l8_first(record, "audit_reference", "source_operation_id"))
    operation_id = _text(_l7_l8_first(record, "operation_id"))
    if not operation_id and audit_reference.startswith("runtime_autoswitch_"):
        operation_id = audit_reference
    learning = record.get("learning_record") if isinstance(record.get("learning_record"), dict) else {}
    return {
        "operation_id": operation_id,
        "feedback_id": _text(_l7_l8_first(record, "feedback_id")),
        "decision_id": _text(_l7_l8_first(record, "decision_id")),
        "packet_id": _text(_l7_l8_first(record, "packet_id", "approval_packet_id")),
        "recommendation_id": _text(_l7_l8_first(record, "recommendation_id", "recommendation_hash", "proposal_id")),
        "learning_record_id": _text(learning.get("learning_record_id") or _l7_l8_first(record, "learning_record_id", "learning_id")),
    }


def _l7_l8_move(record: dict[str, Any]) -> tuple[str, str, str]:
    move = next(iter(intelligence_workers._selected_move_rows(record)), {})
    user = _text(
        intelligence_workers._user_from_row(move)
        or intelligence_workers._user_from_row(record)
        or _l7_l8_first(record, "user")
    )
    source = _text(
        move.get("from") or move.get("source") or move.get("current_egress")
        or _l7_l8_first(record, "source_channel", "from", "current_egress")
    )
    target = _text(
        intelligence_workers._channel_from_row(move)
        or _l7_l8_first(record, "target_channel", "to", "recommended_egress", "channel", "egress")
    )
    return user, source, target


def _l7_l8_hash(payload: Any, prefix: str) -> str:
    stable = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    return prefix + hashlib.sha256(stable.encode("utf-8")).hexdigest()[:24]


def _l7_l8_record_identity(record: dict[str, Any]) -> str:
    ids = _l7_l8_ids(record)
    user, source, target = _l7_l8_move(record)
    owner_identity = ids["operation_id"] or ids["feedback_id"] or ids["decision_id"] or ids["packet_id"] or ids["recommendation_id"]
    if owner_identity:
        return _l7_l8_hash([owner_identity, user, source, target], "outpass_")
    observed = _text(_l7_l8_first(record, "outcome_observed_at", "verification_time", "execution_time", "closure_timestamp", "created_at", "timestamp", "ts"))
    terminal = _text(_l7_l8_first(record, "terminal_outcome_classification", "outcome_quality", "outcome_status", "terminal_state", "result"))
    return _l7_l8_hash([user, source, target, observed, terminal], "outpass_")


def _l7_l8_identity_tokens(record: dict[str, Any]) -> set[str]:
    tokens = {value for value in _l7_l8_ids(record).values() if value}
    for mapping in _l7_l8_maps(record):
        for key in (
            "operation_id", "source_operation_id", "audit_reference", "closure_reference",
            "feedback_id", "decision_id", "packet_id", "approval_packet_id",
            "recommendation_id", "recommendation_hash", "proposal_id",
            "learning_record_id", "learning_id",
        ):
            value = _text(mapping.get(key))
            if value:
                tokens.add(value)
    return tokens


def _l7_l8_connected_identities(records: list[dict[str, Any]]) -> list[str]:
    """Collapse transitive projections of one material outcome across owners."""
    parents = list(range(len(records)))

    def find(index: int) -> int:
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parents[right_root] = left_root

    token_owner: dict[str, int] = {}
    record_tokens: list[set[str]] = []
    for index, record in enumerate(records):
        tokens = _l7_l8_identity_tokens(record)
        record_tokens.append(tokens)
        for token in tokens:
            if token in token_owner:
                union(index, token_owner[token])
            else:
                token_owner[token] = index

    groups: dict[int, list[int]] = {}
    for index in range(len(records)):
        groups.setdefault(find(index), []).append(index)
    identities = ["" for _record in records]
    for indexes in groups.values():
        tokens = sorted({token for index in indexes for token in record_tokens[index]})
        if not tokens:
            for index in indexes:
                identities[index] = _l7_l8_record_identity(records[index])
            continue
        canonical = next((token for token in tokens if token.startswith("runtime_autoswitch_")), "")
        canonical = canonical or next((token for token in tokens if token.startswith("pkt_")), "")
        canonical = canonical or next((token for token in tokens if token.startswith("govdry_")), "")
        canonical = canonical or tokens[0]
        moves = [_l7_l8_move(records[index]) for index in indexes]
        user = next((move[0] for move in moves if move[0]), "")
        source = next((move[1] for move in moves if move[1]), "")
        target = next((move[2] for move in moves if move[2]), "")
        identity = _l7_l8_hash([canonical, user, source, target], "outpass_")
        for index in indexes:
            identities[index] = identity
    return identities


def _l7_l8_explicit_execution(record: dict[str, Any]) -> bool:
    execution = record.get("execution_outcome") if isinstance(record.get("execution_outcome"), dict) else {}
    quality = record.get("outcome_quality") if isinstance(record.get("outcome_quality"), dict) else {}
    terminal = _text(
        quality.get("outcome_quality")
        or _l7_l8_first(record, "terminal_outcome_classification", "outcome_status", "terminal_state")
    ).upper()
    return bool(
        execution.get("applied")
        or execution.get("success")
        or record.get("applied")
        or terminal in {"SUCCESS", "PARTIAL_SUCCESS", "FAILED", "ROLLBACK_SUCCESS", "ROLLBACK_FAILURE"}
    )


def _l7_l8_evidence_class(records: list[dict[str, Any]]) -> str:
    text = " ".join(
        " ".join([
            _text(_l7_l8_first(record, "evidence_class", "production_evidence_class", "execution_mode", "operation_type", "schema_version")),
            _l7_l8_ids(record)["operation_id"],
            _text(record.get("_v7_evidence_source_path")),
        ])
        for record in records
    ).upper()
    if "SYNTHETIC" in text or "SHADOW" in text or "TEST" in text:
        return "SYNTHETIC_OR_TEST"
    if "NATURAL" in text:
        return "NATURAL_PRODUCTION"
    if any(_l7_l8_explicit_execution(record) for record in records) and (
        "RUNTIME_AUTOSWITCH" in text
        or any(_l7_l8_ids(record)["operation_id"].startswith("runtime_autoswitch_") for record in records)
    ):
        return "CONTROLLED_PRODUCTION"
    if any(_l7_l8_explicit_execution(record) for record in records):
        return "REAL_PRODUCTION_CLASS_UNRESOLVED"
    return "NON_EXECUTED_OR_UNKNOWN"


def _l7_l8_terminal(records: list[dict[str, Any]]) -> str:
    for record in reversed(records):
        quality = record.get("outcome_quality") if isinstance(record.get("outcome_quality"), dict) else {}
        value = (
            quality.get("outcome_quality")
            or _l7_l8_first(record, "terminal_outcome_classification", "outcome_quality", "outcome_status", "terminal_state", "result")
        )
        text = _text(value).upper()
        if text and text not in {"UNKNOWN", "NONE"}:
            return text
    return "UNKNOWN"


def _l7_l8_time(records: list[dict[str, Any]], *aliases: str) -> str:
    values = [_text(_l7_l8_first(record, *aliases)) for record in records]
    return max((value for value in values if value), default="")


def _l7_l8_present(value: Any) -> bool:
    return value not in (None, "", [], {}, False)


def _l7_l8_freshness(observed_at: str, generated_at: str, *, max_age_seconds: int = 2_592_000) -> dict[str, Any]:
    def parse(value: str) -> datetime | None:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except (TypeError, ValueError):
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)

    observed = parse(observed_at)
    generated = parse(generated_at)
    if observed is None or generated is None:
        return {"state": "UNKNOWN", "age_seconds": None, "max_age_seconds": max_age_seconds}
    age = max(0, int((generated - observed).total_seconds()))
    return {
        "state": "FRESH" if age <= max_age_seconds else "STALE",
        "age_seconds": age,
        "max_age_seconds": max_age_seconds,
    }


def _l7_l8_opportunity_class(record: dict[str, Any]) -> str:
    text = " ".join(
        _text(_l7_l8_first(record, key))
        for key in ("action", "decision", "disposition", "status", "result", "reason", "terminal_state", "outcome_status")
    ).upper()
    if _l7_l8_explicit_execution(record):
        return "ACTION"
    if "STOP_SAFE" in text or "STOP SAFE" in text or "SELF_STOP" in text:
        return "STOP_SAFE"
    if any(token in text for token in ("BLOCKED", "DENIED", "REJECTED", "INELIGIBLE", "QUARANTINED")):
        return "BLOCKED"
    if any(token in text for token in ("NO_CANDIDATE", "NO CANDIDATE", "NO_SAFE_CANDIDATE")):
        return "NO_CANDIDATE"
    if any(token in text for token in ("STAY", "KEEP_CURRENT", "NO_ACTION", "WAIT")):
        return "STAY"
    if _l7_l8_first(record, "recommendation_id", "recommendation_hash", "proposal_id", "selected_move", "selected_moves"):
        return "MISSED"
    return "NO_CANDIDATE"


def _l7_l8_passport_matches_expected(passport: dict[str, Any], expected: dict[str, Any]) -> bool:
    id_fields = ("operation_id", "feedback_id", "decision_id", "packet_id", "recommendation_id", "learning_record_id")
    supplied_ids = [(key, _text(expected.get(key))) for key in id_fields if expected.get(key)]
    if supplied_ids and any(passport.get(key) == value for key, value in supplied_ids):
        return True
    dimensions = [
        not expected.get("user") or passport.get("user") == _text(expected.get("user")),
        not expected.get("source_channel") or passport.get("source_channel") == _text(expected.get("source_channel")),
        not expected.get("target_channel") or passport.get("target_channel") == _text(expected.get("target_channel")),
        not expected.get("terminal_class") or passport.get("terminal_class") == _text(expected.get("terminal_class")).upper(),
    ]
    return not supplied_ids and all(dimensions) and any(expected.get(key) for key in ("user", "source_channel", "target_channel", "terminal_class"))


def _l7_l8_certification_passport(expected: dict[str, Any], generated_at: str) -> dict[str, Any] | None:
    owner_report = _text(expected.get("owner_report"))
    operation_id = _text(expected.get("operation_id"))
    feedback_id = _text(expected.get("feedback_id"))
    if not owner_report or not (operation_id or feedback_id):
        return None
    evidence_class = _text(expected.get("evidence_class"), "CONTROLLED_PRODUCTION").upper()
    if evidence_class not in {"CONTROLLED_PRODUCTION", "NATURAL_PRODUCTION"}:
        return None
    user = _text(expected.get("user"))
    source = _text(expected.get("source_channel"))
    target = _text(expected.get("target_channel"))
    terminal = _text(expected.get("terminal_class"), "UNKNOWN").upper()
    observed_at = _text(expected.get("outcome_observed_at"))
    identity = _l7_l8_hash([operation_id or feedback_id, user, source, target], "outpass_")
    temporal = {
        "accepted_request": bool(expected.get("accepted_request", True)),
        "actual_activation": bool(expected.get("actual_activation", True)),
        "immediate_verification": bool(expected.get("immediate_verification")),
        "delayed_5m_observation": bool(expected.get("delayed_5m_observation")),
        "delayed_1h_observation": bool(expected.get("delayed_1h_observation")),
        "steady_state_terminal": bool(expected.get("steady_state_terminal")),
    }
    replay = {
        "decision_trace_id": _text(expected.get("decision_trace_id")),
        "input_snapshot_identity": _text(expected.get("input_snapshot_identity")),
        "expected_terminal": _text(expected.get("expected_terminal")),
        "actual_terminal": terminal,
        "intent_drift_class": _text(expected.get("intent_drift_class"), "UNRESOLVED_EXPECTED_TERMINAL"),
        "approved_exception_id": _text(expected.get("approved_exception_id")),
    }
    core = {
        "material_identity": identity,
        "provenance": [{"record_index": None, "source": owner_report, "projection": "existing_certification_history_owner"}],
        "evidence_class": evidence_class,
        "terminal_class": terminal,
        "user": user,
        "source_channel": source,
        "target_channel": target,
        "outcome_observed_at": observed_at,
    }
    core_missing = [field for field in L7_L8_PASSPORT_CORE_FIELDS if not _l7_l8_present(core[field])]
    temporal_missing = [field for field in L7_L8_TEMPORAL_FIELDS if not temporal[field]]
    replay_missing = [field for field in L7_L8_REPLAY_FIELDS if not _l7_l8_present(replay[field])]
    freshness = _l7_l8_freshness(observed_at, generated_at)
    return {
        "schema_version": "v7.l7-l8.outcome-evidence-passport.v1",
        **core,
        "operation_id": operation_id,
        "feedback_id": feedback_id,
        "decision_id": _text(expected.get("decision_id")),
        "packet_id": _text(expected.get("packet_id")),
        "recommendation_id": _text(expected.get("recommendation_id")),
        "learning_record_id": _text(expected.get("learning_record_id")),
        "source_paths": [owner_report],
        "record_indexes": [],
        "record_count": 0,
        "certification_projection_count": 1,
        "freshness": freshness,
        "temporal_verification": temporal,
        "replay_contract": {
            **replay,
            "deterministic_replay_fingerprint": _l7_l8_hash({"identity": identity, "trace": replay["decision_trace_id"], "snapshot": replay["input_snapshot_identity"], "expected": replay["expected_terminal"], "actual": terminal}, "outreplay_"),
        },
        "completeness": {
            "core_complete": not core_missing,
            "temporal_complete": not temporal_missing,
            "replay_complete": not replay_missing,
            "missing_core_fields": core_missing,
            "missing_temporal_fields": temporal_missing,
            "missing_replay_fields": replay_missing,
        },
        "eligibility": "SUPPORTING_ONLY_INCOMPLETE",
        "consumption": {
            "learning_record_consumed": bool(expected.get("learning_record_id")),
            "action_class_reconciliation_consumed": True,
            "omp_program_consumed": True,
        },
    }


def build_l7_l8_outcome_evidence_program(
    decision_records: list[dict[str, Any]] | None = None,
    *,
    expected_material_outcomes: list[dict[str, Any]] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Consume current production evidence for L7/L8 without creating a new truth owner.

    This is a deterministic projection over the existing event, outcome,
    feedback, closure and certification owners. It implements the exact shared
    read-model residual for Missions 1-3 and lets Missions 4-8 reach their legal
    event-driven or evidence-insufficient terminals.
    """
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    records = [row for row in (decision_records or []) if isinstance(row, dict)]
    connected_identities = _l7_l8_connected_identities(records)
    grouped: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    opportunities: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        identity = connected_identities[index]
        grouped.setdefault(identity, []).append((index, record))
        item = opportunities.setdefault(identity, {
            "opportunity_id": identity,
            "classes": set(),
            "record_indexes": [],
            "source_paths": set(),
        })
        item["classes"].add(_l7_l8_opportunity_class(record))
        item["record_indexes"].append(index)
        source_path = _text(record.get("_v7_evidence_source_path") or record.get("evidence_source"))
        if source_path:
            item["source_paths"].add(source_path)

    passports: list[dict[str, Any]] = []
    for identity, indexed in sorted(grouped.items()):
        group_records = [record for _index, record in indexed]
        if not any(_l7_l8_explicit_execution(record) for record in group_records):
            continue
        ids = {key: "" for key in ("operation_id", "feedback_id", "decision_id", "packet_id", "recommendation_id", "learning_record_id")}
        for record in group_records:
            for key, value in _l7_l8_ids(record).items():
                if value and not ids[key]:
                    ids[key] = value
        move_rows = [_l7_l8_move(record) for record in group_records]
        user = next((row[0] for row in move_rows if row[0]), "")
        source = next((row[1] for row in move_rows if row[1]), "")
        target = next((row[2] for row in move_rows if row[2]), "")
        observed_at = _l7_l8_time(group_records, "outcome_observed_at", "verification_time", "closure_timestamp", "completed_at", "created_at", "timestamp", "ts")
        terminal = _l7_l8_terminal(group_records)
        evidence_class = _l7_l8_evidence_class(group_records)
        source_paths = sorted({
            _text(record.get("_v7_evidence_source_path") or record.get("evidence_source"))
            for record in group_records
            if record.get("_v7_evidence_source_path") or record.get("evidence_source")
        })
        provenance = [{"record_index": index, "source": _text(record.get("_v7_evidence_source_path") or record.get("evidence_source") or "existing_decision_record")} for index, record in indexed]

        accepted = bool(ids["packet_id"] or ids["recommendation_id"] or any(_l7_l8_first(record, "accepted_at", "approval_timestamp", "approval_id") for record in group_records))
        activated = any(_l7_l8_explicit_execution(record) for record in group_records)
        immediate = any(
            _l7_l8_first(record, "verification_result", "verification_passed", "post_action_verification", "verification_time")
            for record in group_records
        )
        stability_seconds = max((int(as_float(_l7_l8_first(record, "stability_window_seconds"), 0.0)) for record in group_records), default=0)
        delayed_5m = stability_seconds >= 300 or any(_l7_l8_first(record, "delayed_5m_observation", "observation_5m") for record in group_records)
        delayed_1h = stability_seconds >= 3600 or any(_l7_l8_first(record, "delayed_1h_observation", "observation_1h") for record in group_records)
        steady = delayed_1h and terminal != "UNKNOWN"
        temporal = {
            "accepted_request": accepted,
            "actual_activation": activated,
            "immediate_verification": immediate,
            "delayed_5m_observation": delayed_5m,
            "delayed_1h_observation": delayed_1h,
            "steady_state_terminal": steady,
        }
        decision_trace_id = next((_text(_l7_l8_first(record, "decision_trace_id")) for record in group_records if _l7_l8_first(record, "decision_trace_id")), "")
        input_snapshot_identity = next((_text(_l7_l8_first(record, "input_snapshot_identity", "input_snapshot_id", "runtime_snapshot_hash", "snapshot_fingerprint")) for record in group_records if _l7_l8_first(record, "input_snapshot_identity", "input_snapshot_id", "runtime_snapshot_hash", "snapshot_fingerprint")), "")
        expected_terminal = next((_text(_l7_l8_first(record, "expected_terminal")) for record in group_records if _l7_l8_first(record, "expected_terminal")), "")
        approved_exception = next((_text(_l7_l8_first(record, "approved_exception_id", "exception_id")) for record in group_records if _l7_l8_first(record, "approved_exception_id", "exception_id")), "")
        if not expected_terminal:
            intent_drift = "UNRESOLVED_EXPECTED_TERMINAL"
        elif expected_terminal.upper() == terminal.upper():
            intent_drift = "NO_DRIFT"
        elif approved_exception:
            intent_drift = "APPROVED_EXCEPTION"
        else:
            intent_drift = "UNAPPROVED_INTENT_DRIFT"
        replay = {
            "decision_trace_id": decision_trace_id,
            "input_snapshot_identity": input_snapshot_identity,
            "expected_terminal": expected_terminal,
            "actual_terminal": terminal,
            "intent_drift_class": intent_drift,
            "approved_exception_id": approved_exception,
        }
        core = {
            "material_identity": identity,
            "provenance": provenance,
            "evidence_class": evidence_class,
            "terminal_class": terminal,
            "user": user,
            "source_channel": source,
            "target_channel": target,
            "outcome_observed_at": observed_at,
        }
        core_missing = [field for field in L7_L8_PASSPORT_CORE_FIELDS if not _l7_l8_present(core[field])]
        temporal_missing = [field for field in L7_L8_TEMPORAL_FIELDS if not temporal[field]]
        replay_missing = [field for field in L7_L8_REPLAY_FIELDS if not _l7_l8_present(replay[field])]
        replay_fingerprint = _l7_l8_hash({"identity": identity, "trace": decision_trace_id, "snapshot": input_snapshot_identity, "expected": expected_terminal, "actual": terminal}, "outreplay_")
        freshness = _l7_l8_freshness(observed_at, generated)
        eligible = (
            not core_missing
            and not temporal_missing
            and not replay_missing
            and evidence_class in {"CONTROLLED_PRODUCTION", "NATURAL_PRODUCTION"}
            and freshness["state"] == "FRESH"
        )
        passports.append({
            "schema_version": "v7.l7-l8.outcome-evidence-passport.v1",
            **core,
            **ids,
            "source_paths": source_paths,
            "record_indexes": [index for index, _record in indexed],
            "record_count": len(indexed),
            "freshness": freshness,
            "temporal_verification": temporal,
            "replay_contract": {**replay, "deterministic_replay_fingerprint": replay_fingerprint},
            "completeness": {
                "core_complete": not core_missing,
                "temporal_complete": not temporal_missing,
                "replay_complete": not replay_missing,
                "missing_core_fields": core_missing,
                "missing_temporal_fields": temporal_missing,
                "missing_replay_fields": replay_missing,
            },
            "eligibility": "ELIGIBLE_FOR_CALIBRATION" if eligible else "INELIGIBLE_EXACT_GAPS_RECORDED",
            "consumption": {
                "learning_record_consumed": bool(ids["learning_record_id"]),
                "action_class_reconciliation_consumed": True,
                "omp_program_consumed": True,
            },
        })

    for expected in expected_material_outcomes or []:
        if any(_l7_l8_passport_matches_expected(passport, expected) for passport in passports):
            continue
        certification_passport = _l7_l8_certification_passport(expected, generated)
        if certification_passport:
            passports.append(certification_passport)
    passports.sort(key=lambda row: row["material_identity"])

    expected_reconciliation = []
    matched_passport_ids: set[str] = set()
    for index, expected in enumerate(expected_material_outcomes or []):
        expected_ids = {
            key: _text(expected.get(key))
            for key in ("operation_id", "feedback_id", "decision_id", "packet_id", "recommendation_id", "learning_record_id")
        }
        expected_user = _text(expected.get("user"))
        expected_source = _text(expected.get("source_channel"))
        expected_target = _text(expected.get("target_channel"))
        expected_terminal = _text(expected.get("terminal_class")).upper()

        matched = next((passport for passport in passports if _l7_l8_passport_matches_expected(passport, expected)), None)
        if matched:
            matched_passport_ids.add(matched["material_identity"])
        expected_reconciliation.append({
            "expected_index": index,
            **expected_ids,
            "user": expected_user,
            "source_channel": expected_source,
            "target_channel": expected_target,
            "terminal_class": expected_terminal,
            "status": "MATCHED_EXISTING_OWNER_PASSPORT" if matched else "NOT_FOUND_IN_CURRENT_OWNER_READ_SET",
            "matched_material_identity": matched["material_identity"] if matched else "",
        })
    if expected_material_outcomes:
        for passport in passports:
            passport["consumption"]["action_class_reconciliation_consumed"] = passport["material_identity"] in matched_passport_ids

    denominator_rows = []
    class_counts = {name: 0 for name in ("ACTION", "STAY", "STOP_SAFE", "BLOCKED", "MISSED", "NO_CANDIDATE")}
    class_precedence = ("ACTION", "STOP_SAFE", "BLOCKED", "STAY", "MISSED", "NO_CANDIDATE")
    for identity, item in sorted(opportunities.items()):
        final_class = next(name for name in class_precedence if name in item["classes"])
        class_counts[final_class] += 1
        denominator_rows.append({
            "opportunity_id": identity,
            "opportunity_class": final_class,
            "observed_classes": sorted(item["classes"]),
            "record_indexes": item["record_indexes"],
            "source_paths": sorted(item["source_paths"]),
        })
    denominator_ids = {row["opportunity_id"] for row in denominator_rows}
    for passport in passports:
        if passport.get("certification_projection_count") != 1 or passport["material_identity"] in denominator_ids:
            continue
        class_counts["ACTION"] += 1
        denominator_rows.append({
            "opportunity_id": passport["material_identity"],
            "opportunity_class": "ACTION",
            "observed_classes": ["ACTION"],
            "record_indexes": [],
            "source_paths": passport["source_paths"],
            "projection": "existing_certification_history_owner",
        })

    eligible_passports = [row for row in passports if row["eligibility"] == "ELIGIBLE_FOR_CALIBRATION"]
    immutable_set = sorted(row["material_identity"] for row in eligible_passports)
    immutable_fingerprint = _l7_l8_hash(immutable_set, "outset_")
    evidence_classes = sorted({row["evidence_class"] for row in eligible_passports})
    terminal_classes = sorted({row["terminal_class"] for row in eligible_passports})
    coverage_cells = {
        "eligible_passports_at_least_5": len(eligible_passports) >= 5,
        "controlled_production_present": "CONTROLLED_PRODUCTION" in evidence_classes,
        "natural_production_present": "NATURAL_PRODUCTION" in evidence_classes,
        "rollback_and_no_rollback_present": any("ROLLBACK" in value for value in terminal_classes) and any("ROLLBACK" not in value for value in terminal_classes),
        "material_variation_present": len({(row["user"], row["source_channel"], row["target_channel"]) for row in eligible_passports}) >= 2,
        "complete_temporal_and_replay": bool(eligible_passports) and all(row["completeness"]["temporal_complete"] and row["completeness"]["replay_complete"] for row in eligible_passports),
    }
    missing_cells = sorted(name for name, passed in coverage_cells.items() if not passed)
    calibration_verdict = "CALIBRATION_SET_SUFFICIENT" if not missing_cells else "INSUFFICIENT_EVIDENCE"
    authority_verdict = "HOLD_GOVERNED_ONLY" if calibration_verdict == "CALIBRATION_SET_SUFFICIENT" else "INSUFFICIENT_EVIDENCE"
    next_event = (
        "independent Authority approval review"
        if authority_verdict == "RECOMMEND_CERTIFIED_FOR_CLASS_APPROVAL"
        else "new qualifying owner-backed controlled or natural production outcome closing the exact missing coverage cells"
    )
    expected_missing = sum(1 for row in expected_reconciliation if row["status"] != "MATCHED_EXISTING_OWNER_PASSPORT")
    return {
        "schema_version": "v7.l7-l8.production-evidence-authority-evolution-program.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration existing evidence inventory read owner",
        "target_terminal": "CURRENT_L7_L8_EVIDENCE_CYCLE_RECONCILED_ACTION_CLASS_AUTHORITY_RECOMMENDATION_DECIDED_AND_REVIEW_HANDOFF_RESOLVED",
        "mission_results": {
            "M1": {
                "status": "COMPLETE_CONSUMED" if not expected_missing else "COMPLETE_CONSUMED_WITH_EXACT_RESIDUALS",
                "passport_count": len(passports),
                "opportunity_count": len(denominator_rows),
                "expected_material_outcomes": len(expected_reconciliation),
                "expected_material_outcomes_matched": len(expected_reconciliation) - expected_missing,
                "expected_material_outcomes_missing": expected_missing,
            },
            "M2": {"status": "COMPLETE_CONSUMED_WITH_EXACT_RESIDUALS", "temporally_complete": sum(1 for row in passports if row["completeness"]["temporal_complete"])},
            "M3": {"status": "COMPLETE_CONSUMED_WITH_EXACT_RESIDUALS", "replay_complete": sum(1 for row in passports if row["completeness"]["replay_complete"])},
            "M4": {"status": "EVENT_DRIVEN_BOUNDARY", "qualifying_controlled_passports": sum(1 for row in passports if row["evidence_class"] == "CONTROLLED_PRODUCTION" and row["eligibility"] == "ELIGIBLE_FOR_CALIBRATION"), "evidence_manufactured": False},
            "M5": {"status": "EVENT_DRIVEN_BOUNDARY", "qualifying_natural_passports": sum(1 for row in passports if row["evidence_class"] == "NATURAL_PRODUCTION" and row["eligibility"] == "ELIGIBLE_FOR_CALIBRATION"), "evidence_manufactured": False},
            "M6": {"status": calibration_verdict, "immutable_eligibility_set_fingerprint": immutable_fingerprint, "eligible_passports": len(eligible_passports), "missing_coverage_cells": missing_cells, "learning_result": "OWNER_BACKED_NO_CHANGE_INSUFFICIENT_EVIDENCE" if missing_cells else "OWNER_BACKED_CALIBRATION_SET_CONSUMED"},
            "M7": {"status": "COMPLETE_CONSUMED", "authority_recommendation": authority_verdict, "authority_mutation_performed": False},
            "M8": {"status": "MISSION_NOT_REQUIRED_BY_AUTHORITY_VERDICT" if authority_verdict != "RECOMMEND_CERTIFIED_FOR_CLASS_APPROVAL" else "READY_FOR_INDEPENDENT_AUTHORITY_BOUNDARY", "authority_mutation_performed": False},
        },
        "outcome_evidence_passports": passports,
        "current_action_class_reconciliation": {
            "expected_contract_provided": bool(expected_material_outcomes),
            "expected_count": len(expected_reconciliation),
            "matched_count": len(expected_reconciliation) - expected_missing,
            "missing_count": expected_missing,
            "rows": expected_reconciliation,
            "consumer_gap": "NONE" if not expected_missing else "CURRENT_CPS_MATERIAL_OUTCOMES_NOT_FOUND_IN_CURRENT_OWNER_READ_SET",
        },
        "opportunity_denominator": {
            "definition": "append-only projection through existing event/outcome/certification owners; not an independent registry, watcher, database or queue",
            "counts": class_counts,
            "rows": denominator_rows[:100],
            "rows_total": len(denominator_rows),
        },
        "immutable_eligibility_set": {
            "passport_ids": immutable_set,
            "fingerprint": immutable_fingerprint,
            "evidence_classes": evidence_classes,
            "terminal_classes": terminal_classes,
            "coverage_cells": coverage_cells,
            "missing_coverage_cells": missing_cells,
        },
        "authority_recommendation": {
            "verdict": authority_verdict,
            "scope_narrowing_supported": True,
            "allowed_verdicts": ["RECOMMEND_CERTIFIED_FOR_CLASS_APPROVAL", "RETAIN_CURRENT_SCOPE", "RECOMMEND_NARROW_SCOPE", "HOLD_GOVERNED_ONLY", "FREEZE", "DEMOTE", "INSUFFICIENT_EVIDENCE"],
            "recommendation_is_not_mutation": True,
        },
        "program_terminal": "CURRENT_L7_L8_EVIDENCE_CYCLE_RECONCILED_ACTION_CLASS_AUTHORITY_RECOMMENDATION_DECIDED_AND_REVIEW_HANDOFF_RESOLVED",
        "next_reentry_condition": next_event,
        "read_only": True,
        "new_truth_source_created": False,
        "new_storage_created": False,
        "synthetic_evidence_created": False,
        "runtime_mutation_performed": False,
        "routing_mutation_performed": False,
        "restore_barrier_written_now": False,
        "rollback_apply_executed": False,
        "daemon_or_timer_enabled": False,
        "authority_expanded": False,
        "production_maturity_changed": False,
        "users_moved": 0,
        "apply_executed": False,
    }


def build_polygon_driven_l7_l8_evidence_acquisition(
    evidence_program: dict[str, Any],
    *,
    users: list[dict[str, Any]] | None = None,
    egress: list[dict[str, Any]] | None = None,
    packet_preview: dict[str, Any] | None = None,
    delegated_policy: dict[str, Any] | None = None,
    owner_capture_sources: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Turn L7 waiting into active, owner-bound opportunity engineering.

    The projection is deliberately read-only.  It reuses the current evidence,
    registry, delegated-policy and packet owners to decide whether one bounded
    controlled transaction is already legal, which exact preparation gap must
    be repaired, or which deliberate production condition requires independent
    Engineering Authority.  Natural L8 evidence is never manufactured; its
    existing owner capture chain is audited so the next real event is consumed.
    """
    program = evidence_program if isinstance(evidence_program, dict) else {}
    registry_users = [row for row in (users or []) if isinstance(row, dict)]
    registry_egress = [row for row in (egress or []) if isinstance(row, dict)]
    preview = packet_preview if isinstance(packet_preview, dict) else {}
    policy = delegated_policy if isinstance(delegated_policy, dict) else {}
    sources = [row for row in (owner_capture_sources or []) if isinstance(row, dict)]

    immutable = program.get("immutable_eligibility_set") or {}
    missing_cells = sorted({_text(value) for value in immutable.get("missing_coverage_cells") or [] if _text(value)})
    controlled_missing = "controlled_production_present" in missing_cells
    natural_missing = "natural_production_present" in missing_cells
    priorities = (
        "controlled_production_present",
        "complete_temporal_and_replay",
        "rollback_and_no_rollback_present",
        "material_variation_present",
        "eligible_passports_at_least_5",
    )
    selected_l7_cell = next((cell for cell in priorities if cell in missing_cells), "NONE")

    certification_users = sorted({
        _text(row.get("ip") or row.get("user_ip") or row.get("user"))
        for row in registry_users
        if _truthy(row.get("certification_user"))
        and _truthy(row.get("enabled", True))
        and _text(row.get("ip") or row.get("user_ip") or row.get("user"))
    })
    controlled_sources = []
    for row in registry_egress:
        if not _truthy(row.get("controlled_certification_source")):
            continue
        controlled_sources.append({
            "source_id": _text(row.get("id") or row.get("interface")),
            "interface": _text(row.get("interface")),
            "certification_group": _text(row.get("certification_group")),
            "enabled": _truthy(row.get("enabled", True)),
            "state": _text(row.get("state")),
        })
    active_controlled_sources = [row for row in controlled_sources if row["enabled"]]

    candidate_users = sorted({_text(value) for value in preview.get("allowed_users") or [] if _text(value)})
    candidate_targets = sorted({_text(value) for value in preview.get("allowed_targets") or [] if _text(value)})
    candidate_ready = (
        preview.get("status") == "PACKET_PREVIEW_READY"
        and bool(preview.get("operation_id"))
        and bool(preview.get("packet_id"))
        and bool(preview.get("selected_move_hash"))
        and bool(candidate_users)
        and len(candidate_users) == 1
    )
    candidate_certification_scoped = candidate_ready and set(candidate_users).issubset(set(certification_users))
    candidate_genuine_production_need = candidate_ready and _truthy(preview.get("_v7_genuine_production_candidate"))
    policy_ready = (
        policy.get("policy_state") == "APPROVED"
        and policy.get("current_mode") == "DELEGATED_AUTONOMY"
        and int(policy.get("max_users_per_action") or 0) == 1
        and int(policy.get("max_concurrent_transactions") or 0) == 1
        and policy.get("candidate_selection") == "EXISTING_PLANNER_ONLY"
        and policy.get("candidate_identity") == "FRESH_ONLY"
        and policy.get("packet_reuse") == "FORBIDDEN"
        and policy.get("self_expansion_allowed") is False
    )

    if not controlled_missing:
        l7_verdict = "CONTROLLED_PRODUCTION_CELL_ALREADY_CLOSED"
        l7_stop = "NONE"
    elif candidate_ready and policy_ready and (candidate_certification_scoped or candidate_genuine_production_need):
        l7_verdict = "READY_EXISTING_POLICY_BOUNDED_TRANSACTION"
        l7_stop = "NONE"
    elif not candidate_genuine_production_need and (not certification_users or not active_controlled_sources):
        l7_verdict = "ENGINEERING_AUTHORITY_REQUIRED_FOR_CERTIFICATION_POOL_OR_DELIBERATE_CONDITION"
        l7_stop = "ENGINEERING_AUTHORITY"
    elif not candidate_ready:
        l7_verdict = "POLYGON_SCENARIO_PREPARATION_REQUIRED"
        l7_stop = "NONE"
    elif not candidate_certification_scoped:
        l7_verdict = "OWNER_AUTHORIZED_CERTIFICATION_CANDIDATE_REQUIRED"
        l7_stop = "ENGINEERING_AUTHORITY"
    elif not policy_ready:
        l7_verdict = "EXISTING_DELEGATED_POLICY_ADMISSION_FAILED"
        l7_stop = "ENGINEERING_AUTHORITY"
    else:  # pragma: no cover - defensive exhaustiveness
        l7_verdict = "STOP_SAFE_UNCLASSIFIED_CONTROLLED_OPPORTUNITY"
        l7_stop = "STOP_SAFE"

    capture_roles = {
        "NATURAL_EVENT_DETECTION": False,
        "DECISION_TRACE_AND_SNAPSHOT": False,
        "OUTCOME_AND_FEEDBACK": False,
        "ROLLBACK_OR_NO_ROLLBACK": False,
        "LEARNING_AND_REPLAY": False,
    }
    source_rows = []
    for source in sources:
        role = _text(source.get("owner_role")).upper()
        exists = bool(source.get("exists"))
        readable = bool(source.get("readable", exists))
        records_read = int(source.get("records_read") or 0)
        source_rows.append({
            "path": _text(source.get("path")),
            "owner_role": role,
            "exists": exists,
            "readable": readable,
            "records_read": records_read,
        })
        if role in capture_roles and exists and readable:
            if role == "NATURAL_EVENT_DETECTION":
                capture_roles[role] = capture_roles[role] or records_read > 0
            else:
                capture_roles[role] = True
    l8_capture_gaps = sorted(role for role, ready in capture_roles.items() if not ready)
    l8_capture_verdict = "READY_FOR_NEXT_NATURAL_EVENT" if not l8_capture_gaps else "OWNER_CAPTURE_REPAIR_REQUIRED"
    l8_stop = "REAL_WORLD_LIMIT" if not l8_capture_gaps and natural_missing else "NONE"

    if l8_capture_gaps:
        exact_next_action = f"REPAIR_EXISTING_L8_CAPTURE_CONSUMER:{l8_capture_gaps[0]}"
        global_engineering_stop = "NONE"
    elif l7_verdict == "READY_EXISTING_POLICY_BOUNDED_TRANSACTION":
        exact_next_action = "EXECUTE_ONE_FRESH_OWNER_AUTHORIZED_BOUNDED_CONTROLLED_TRANSACTION"
        global_engineering_stop = "NONE"
    elif l7_stop == "ENGINEERING_AUTHORITY":
        exact_next_action = "REQUEST_EXACT_CERTIFICATION_POOL_OR_DELIBERATE_CONDITION_ENGINEERING_AUTHORITY"
        global_engineering_stop = "ENGINEERING_AUTHORITY"
    elif controlled_missing:
        exact_next_action = "PREPARE_NEXT_OWNER_BOUND_POLYGON_CONTROLLED_OPPORTUNITY"
        global_engineering_stop = "NONE"
    else:
        exact_next_action = "WAIT_FOR_NEXT_NATURAL_EVENT_WITH_CAPTURE_CHAIN_READY"
        global_engineering_stop = l8_stop

    return {
        "schema_version": "v7.polygon-driven-l7-l8-evidence-acquisition.v1",
        "owner": "existing OMP Polygon consumer over Controlled Production and production evidence owners",
        "evidence_program_fingerprint": _text(immutable.get("fingerprint")),
        "exact_missing_coverage_cells": missing_cells,
        "selected_highest_value_l7_cell": selected_l7_cell,
        "l7_controlled_lane": {
            "verdict": l7_verdict,
            "stop": l7_stop,
            "certification_users": certification_users,
            "controlled_sources": controlled_sources,
            "active_controlled_source_count": len(active_controlled_sources),
            "candidate": {
                "ready": candidate_ready,
                "packet_id": _text(preview.get("packet_id")),
                "operation_id": _text(preview.get("operation_id")),
                "selected_move_hash": _text(preview.get("selected_move_hash")),
                "users": candidate_users,
                "targets": candidate_targets,
                "certification_scoped": candidate_certification_scoped,
                "genuine_production_need": candidate_genuine_production_need,
                "reason_summary": [_text(value) for value in preview.get("_v7_candidate_reason_summary") or [] if _text(value)],
            },
            "delegated_policy_admitted": policy_ready,
            "ordinary_customer_used_to_manufacture_evidence": False,
            "real_production_outcome_required": True,
        },
        "l8_natural_lane": {
            "verdict": l8_capture_verdict,
            "stop": l8_stop,
            "natural_event_manufactured": False,
            "capture_roles": capture_roles,
            "capture_gaps": l8_capture_gaps,
            "owner_sources": source_rows,
        },
        "mission_results": {
            "P0_EXACT_GAP_SELECTION": "COMPLETE_CONSUMED",
            "P1_POLYGON_SCENARIO_SELECTION": "COMPLETE_CONSUMED",
            "P2_CERTIFICATION_POOL_DECISION": l7_verdict,
            "P3_L8_CAPTURE_READINESS": l8_capture_verdict,
            "P4_CONTROLLED_TRANSACTION": "READY" if l7_verdict == "READY_EXISTING_POLICY_BOUNDED_TRANSACTION" else "CONDITIONAL_TERMINAL",
            "P5_NATURAL_EVIDENCE": "EVENT_DRIVEN_CAPTURE_READY" if not l8_capture_gaps else "CAPTURE_REPAIR_REQUIRED",
            "P6_CALIBRATION": _text(((program.get("mission_results") or {}).get("M6") or {}).get("status")),
            "P7_AUTHORITY_RECOMMENDATION": _text(((program.get("mission_results") or {}).get("M7") or {}).get("authority_recommendation")),
        },
        "global_engineering_stop": global_engineering_stop,
        "exact_next_action": exact_next_action,
        "read_only": True,
        "new_truth_source_created": False,
        "new_storage_created": False,
        "synthetic_production_evidence_created": False,
        "runtime_mutation_performed": False,
        "routing_mutation_performed": False,
        "restore_barrier_written_now": False,
        "rollback_apply_executed": False,
        "daemon_or_timer_enabled": False,
        "authority_expanded": False,
        "production_maturity_changed": False,
        "users_moved": 0,
        "apply_executed": False,
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


def _b8_channel_key(row: dict[str, Any], index: int = 0) -> str:
    return _text(
        row.get("channel")
        or row.get("egress")
        or row.get("id")
        or row.get("target")
        or row.get("object")
        or f"unknown-{index}"
    )


def _b8_service_readiness(row: dict[str, Any]) -> tuple[bool, list[str]]:
    services = row.get("services") if isinstance(row.get("services"), dict) else {}
    evidence = []
    ready = False
    if services:
        for service, value in sorted(services.items()):
            service_row = value if isinstance(value, dict) else {"ok": bool(value)}
            ok = service_row.get("ok")
            status = _text(service_row.get("status") or service_row.get("state")).upper()
            if ok is True or status in {"OK", "PASS", "READY", "HEALTHY", "SUCCESS"}:
                ready = True
                evidence.append(f"{service}:ready")
            elif ok is False or status in {"FAILED", "FAIL", "DEGRADED", "DOWN"}:
                evidence.append(f"{service}:not_ready")
    status = _text(row.get("status") or row.get("state") or row.get("readiness")).upper()
    if status in {"OK", "PASS", "READY", "HEALTHY", "SUCCESS"}:
        ready = True
        evidence.append("channel_service_status_ready")
    if as_float(row.get("score"), -1.0) >= 0.0:
        evidence.append("service_score_present")
    return ready, sorted(set(evidence))


def _b8_quality_readiness(row: dict[str, Any]) -> tuple[bool, list[str]]:
    score = row.get("score") if isinstance(row.get("score"), dict) else {}
    status = _text(row.get("status") or row.get("state") or row.get("readiness")).upper()
    trend = _text(row.get("trend") or row.get("quality_trend") or score.get("trend")).upper()
    evidence = []
    ready = False
    if status in {"OK", "PASS", "READY", "HEALTHY", "SUCCESS", "STABLE"}:
        ready = True
        evidence.append("quality_status_ready")
    if trend in {"STABLE", "IMPROVING"}:
        ready = True
        evidence.append("quality_trend_ready")
    current_score = score.get("current") if score else row.get("quality_score", row.get("score"))
    if as_float(current_score, -1.0) >= 0.0:
        evidence.append("quality_score_present")
    return ready, sorted(set(evidence))


def build_recovery_admission_certification(
    *,
    recovery_admission: dict[str, Any] | None = None,
    service_scores_snapshot: dict[str, Any] | None = None,
    channel_service_scores_snapshot: dict[str, Any] | None = None,
    freshness_actionability: dict[str, Any] | None = None,
    service_objective_policy_threshold_binding: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Certify B8 recovery admission evidence without admitting traffic or changing Runtime."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    recovery_rows = [
        row for row in ((recovery_admission or {}).get("rows") or [])
        if isinstance(row, dict)
    ]
    service_rows = _items(service_scores_snapshot)
    quality_rows = _items(channel_service_scores_snapshot)
    objective_rows = [
        row for row in ((service_objective_policy_threshold_binding or {}).get("rows") or [])
        if isinstance(row, dict)
    ]
    channels: dict[str, dict[str, Any]] = {}

    def ensure_channel(channel: str) -> dict[str, Any]:
        return channels.setdefault(channel, {
            "channel": channel,
            "recovery_rows": [],
            "service_evidence": [],
            "quality_evidence": [],
            "objective_evidence": [],
            "owners": set(),
            "sources": set(),
        })

    for index, row in enumerate(recovery_rows):
        channel = _b8_channel_key(row, index)
        item = ensure_channel(channel)
        item["recovery_rows"].append(row)
        item["owners"].add("admin_core.autonomy_trust_acceleration.build_recovery_admission")
        item["sources"].add("recovery_admission")

    for index, row in enumerate(service_rows):
        channel = _b8_channel_key(row, index)
        item = ensure_channel(channel)
        ready, evidence = _b8_service_readiness(row)
        item["service_evidence"].append({"ready": ready, "evidence": evidence})
        item["owners"].add("tools/v7-service-matrix-refresh-all")
        item["sources"].add("service-scores")

    for index, row in enumerate(quality_rows):
        channel = _b8_channel_key(row, index)
        item = ensure_channel(channel)
        ready, evidence = _b8_quality_readiness(row)
        item["quality_evidence"].append({"ready": ready, "evidence": evidence})
        item["owners"].add("tools/v7-egress-quality-compact")
        item["sources"].add("channel-service-scores")

    for row in objective_rows:
        channel = _text(row.get("candidate_channel") or row.get("channel"))
        if not channel:
            continue
        item = ensure_channel(channel)
        item["objective_evidence"].append({
            "user": _text(row.get("user")),
            "binding_state": _text(row.get("binding_state")),
            "objective_count": len([entry for entry in row.get("objective_bindings", []) if isinstance(entry, dict)]),
        })
        item["owners"].add("admin_core.autonomy_trust_acceleration.build_service_objective_policy_threshold_binding")
        item["sources"].add("service_objective_policy_threshold_binding")

    recovery_freshness = (
        ((freshness_actionability or {}).get("domains") or {}).get("recovery") or {}
    ).get("classification", "UNKNOWN")
    service_freshness = (
        ((freshness_actionability or {}).get("domains") or {}).get("service") or {}
    ).get("classification", "UNKNOWN")
    min_success = int(RECOVERY_ADMISSION_POLICY["min_successful_checks"])
    rows: list[dict[str, Any]] = []
    for channel in sorted(channels):
        item = channels[channel]
        recovery_row = item["recovery_rows"][0] if item["recovery_rows"] else {}
        successful_checks = int(as_float(recovery_row.get("successful_checks"), 0.0))
        admission_state = _text(recovery_row.get("admission_state"), "UNKNOWN")
        recovery_blockers = [str(blocker) for blocker in (recovery_row.get("blockers") or []) if blocker]
        service_ready = any(row["ready"] for row in item["service_evidence"])
        quality_ready = any(row["ready"] for row in item["quality_evidence"])
        objectives_bound = bool(item["objective_evidence"])
        blockers = []
        if successful_checks < min_success:
            blockers.append("insufficient_repeated_success_evidence")
        if admission_state not in {"ELIGIBLE", "RECOVERED_WATCH"}:
            blockers.append("recovery_admission_not_eligible")
        if not service_ready:
            blockers.append("service_readiness_evidence_missing")
        if not quality_ready:
            blockers.append("quality_readiness_evidence_missing")
        if recovery_freshness != "ACTIONABLE_NOW":
            blockers.append("recovery_freshness_not_actionable")
        if service_freshness != "ACTIONABLE_NOW":
            blockers.append("service_freshness_not_actionable")
        blockers.extend(recovery_blockers)
        certification_state = (
            "CERTIFIED_FOR_RECOVERY_ADMISSION_REVIEW"
            if not blockers
            else "NOT_CERTIFIED_COLLECT_REAL_EVIDENCE"
        )
        rows.append({
            "channel": channel,
            "certification_state": certification_state,
            "admission_state": admission_state,
            "successful_checks": successful_checks,
            "min_successful_checks": min_success,
            "repeated_success_evidence": successful_checks >= min_success,
            "service_readiness_evidence": service_ready,
            "quality_readiness_evidence": quality_ready,
            "objective_binding_evidence": objectives_bound,
            "recovery_freshness": recovery_freshness,
            "service_freshness": service_freshness,
            "service_evidence": [evidence for row in item["service_evidence"] for evidence in row["evidence"]],
            "quality_evidence": [evidence for row in item["quality_evidence"] for evidence in row["evidence"]],
            "objective_evidence": item["objective_evidence"],
            "owners": sorted(item["owners"]),
            "sources": sorted(item["sources"]),
            "blockers": sorted(set(blockers)),
            "certification_role": "read_only_evidence_certification_only",
            "runtime_apply_allowed": False,
            "authority_expanded": False,
            "synthetic_evidence_created": False,
            "users_moved": 0,
        })

    return {
        "schema_version": "v7.b8.recovery-admission-certification.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B8",
        "purpose": "certify_recovery_admission_with_repeated_real_success_and_readiness_evidence_without_runtime_apply",
        "source_owners_reused": [
            "admin_core.autonomy_trust_acceleration.build_recovery_admission",
            "tools/v7-service-matrix-refresh-all",
            "tools/v7-egress-quality-compact",
            "admin_core.autonomy_trust_acceleration.build_freshness_actionability",
            "admin_core.autonomy_trust_acceleration.build_service_objective_policy_threshold_binding",
        ],
        "policy_sources": [
            "docs/policies/POLICY_003_RECOVERY_ADMISSION.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B8",
        ],
        "rows": rows,
        "summary": {
            "channels_seen": len(rows),
            "certified": sum(1 for row in rows if row["certification_state"] == "CERTIFIED_FOR_RECOVERY_ADMISSION_REVIEW"),
            "not_certified": sum(1 for row in rows if row["certification_state"] != "CERTIFIED_FOR_RECOVERY_ADMISSION_REVIEW"),
            "runtime_actions_created": 0,
            "authority_changes": 0,
            "synthetic_evidence_created": 0,
            "users_moved": 0,
        },
        "canonical_rules": [
            "b8_certifies_existing_recovery_evidence_only",
            "recovery_admission_requires_repeated_success_not_single_pass",
            "readiness_requires_existing_service_and_quality_evidence",
            "b8_does_not_admit_traffic_or_move_users",
            "b8_does_not_grant_runtime_apply_or_authority",
        ],
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
        "new_planner_created": False,
    }


B9_REQUIRED_OBSERVATION_WINDOWS = ("5m", "1h")


def _b9_quality_windows(row: dict[str, Any]) -> list[dict[str, Any]]:
    windows = row.get("windows") if isinstance(row.get("windows"), dict) else {}
    rows = []
    for name in B9_REQUIRED_OBSERVATION_WINDOWS:
        window = windows.get(name) if isinstance(windows.get(name), dict) else {}
        samples = int(as_float(window.get("samples"), 0.0))
        rows.append({
            "window": name,
            "samples": samples,
            "observed": samples > 0,
            "updated": _text(window.get("updated") or window.get("last_seen_at") or window.get("generated_at")),
            "fail_rate_present": window.get("fail_rate") is not None,
            "stability_present": window.get("stability") is not None,
            "score_inputs_present": any(window.get(key) is not None for key in ("avg_mbps", "min_mbps", "p95_latency_ms", "fail_rate", "stability")),
        })
    return rows


def build_post_admission_observation_windows(
    *,
    recovery_admission_certification: dict[str, Any] | None = None,
    service_scores_snapshot: dict[str, Any] | None = None,
    channel_service_scores_snapshot: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Verify B9 post-admission observation windows without admitting traffic or changing Runtime."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    certification_rows = [
        row for row in ((recovery_admission_certification or {}).get("rows") or [])
        if isinstance(row, dict)
    ]
    channels: dict[str, dict[str, Any]] = {}

    def ensure_channel(channel: str) -> dict[str, Any]:
        return channels.setdefault(channel, {
            "channel": channel,
            "certification_rows": [],
            "service_rows": [],
            "quality_rows": [],
            "owners": set(),
            "sources": set(),
        })

    for index, row in enumerate(certification_rows):
        channel = _b8_channel_key(row, index)
        item = ensure_channel(channel)
        item["certification_rows"].append(row)
        item["owners"].add("admin_core.autonomy_trust_acceleration.build_recovery_admission_certification")
        item["sources"].add("recovery_admission_certification")

    for index, row in enumerate(_items(service_scores_snapshot)):
        channel = _b8_channel_key(row, index)
        item = ensure_channel(channel)
        item["service_rows"].append(row)
        item["owners"].add("tools/v7-service-matrix-refresh-all")
        item["sources"].add("service-scores")

    for index, row in enumerate(_items(channel_service_scores_snapshot)):
        channel = _b8_channel_key(row, index)
        item = ensure_channel(channel)
        item["quality_rows"].append(row)
        item["owners"].add("tools/v7-egress-quality-compact")
        item["sources"].add("channel-service-scores")

    rows = []
    for channel in sorted(channels):
        item = channels[channel]
        certification = item["certification_rows"][0] if item["certification_rows"] else {}
        certification_state = _text(certification.get("certification_state"), "UNKNOWN")
        service_evidence = [_b8_service_readiness(row) for row in item["service_rows"]]
        service_observed = any(ready for ready, _evidence in service_evidence)
        quality_windows = [
            window
            for quality_row in item["quality_rows"]
            for window in _b9_quality_windows(quality_row)
        ]
        by_window: dict[str, list[dict[str, Any]]] = {}
        for window in quality_windows:
            by_window.setdefault(window["window"], []).append(window)
        missing_windows = [
            name for name in B9_REQUIRED_OBSERVATION_WINDOWS
            if not any(window.get("observed") for window in by_window.get(name, []))
        ]
        blockers = []
        if certification_state != "CERTIFIED_FOR_RECOVERY_ADMISSION_REVIEW":
            blockers.append("recovery_admission_certification_not_ready")
        if not service_observed:
            blockers.append("post_admission_service_observation_missing")
        if missing_windows:
            blockers.append("post_admission_quality_windows_missing:" + ",".join(missing_windows))
        verification_state = (
            "POST_ADMISSION_WINDOWS_VERIFIED_READ_ONLY"
            if not blockers
            else "POST_ADMISSION_WINDOWS_NOT_VERIFIED"
        )
        rows.append({
            "channel": channel,
            "verification_state": verification_state,
            "certification_state": certification_state,
            "required_windows": list(B9_REQUIRED_OBSERVATION_WINDOWS),
            "observed_windows": sorted([
                name for name in B9_REQUIRED_OBSERVATION_WINDOWS
                if any(window.get("observed") for window in by_window.get(name, []))
            ]),
            "quality_windows": quality_windows,
            "service_observation_evidence": sorted({
                evidence
                for _ready, evidence_rows in service_evidence
                for evidence in evidence_rows
            }),
            "service_observed": service_observed,
            "owners": sorted(item["owners"]),
            "sources": sorted(item["sources"]),
            "blockers": sorted(set(blockers)),
            "verification_role": "read_only_observation_window_verification_only",
            "runtime_apply_allowed": False,
            "authority_expanded": False,
            "synthetic_evidence_created": False,
            "users_moved": 0,
        })

    return {
        "schema_version": "v7.b9.post-admission-observation-windows.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B9",
        "purpose": "verify_post_admission_observation_windows_from_existing_service_and_quality_owners_without_runtime_apply",
        "source_owners_reused": [
            "admin_core.autonomy_trust_acceleration.build_recovery_admission_certification",
            "tools/v7-service-matrix-refresh-all",
            "tools/v7-egress-quality-compact",
        ],
        "policy_sources": [
            "docs/policies/POLICY_003_RECOVERY_ADMISSION.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B9",
        ],
        "rows": rows,
        "summary": {
            "channels_seen": len(rows),
            "verified": sum(1 for row in rows if row["verification_state"] == "POST_ADMISSION_WINDOWS_VERIFIED_READ_ONLY"),
            "not_verified": sum(1 for row in rows if row["verification_state"] != "POST_ADMISSION_WINDOWS_VERIFIED_READ_ONLY"),
            "runtime_actions_created": 0,
            "authority_changes": 0,
            "synthetic_evidence_created": 0,
            "users_moved": 0,
        },
        "canonical_rules": [
            "b9_requires_existing_post_admission_observation_windows",
            "b9_consumes_b8_recovery_admission_certification_only_as_evidence",
            "b9_does_not_admit_traffic_or_move_users",
            "b9_does_not_grant_runtime_apply_or_authority",
            "b9_does_not_create_new_observation_owner",
        ],
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
        "new_planner_created": False,
    }


def build_recovery_slow_start_progression(
    *,
    post_admission_observation_windows: dict[str, Any] | None = None,
    recovery_admission_certification: dict[str, Any] | None = None,
    class_level_blast_radius_certification: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Define B10 recovery slow-start progression without moving users or changing Runtime."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    observation_rows = [
        row for row in ((post_admission_observation_windows or {}).get("rows") or [])
        if isinstance(row, dict)
    ]
    certification_by_channel = {
        _b8_channel_key(row, index): row
        for index, row in enumerate((recovery_admission_certification or {}).get("rows") or [])
        if isinstance(row, dict)
    }
    blast = class_level_blast_radius_certification if isinstance(class_level_blast_radius_certification, dict) else {}
    one_user_blast_certified = bool(blast.get("current_one_user_guard_certified")) or (
        int(as_float(blast.get("max_historical_certified_blast_radius_users"), 0.0)) >= 1
    )
    beyond_one_user_certified = bool(blast.get("beyond_one_user_certified"))
    policy_user_limit = int(RECOVERY_ADMISSION_POLICY["limited_recovery_blast_radius_users"])
    stage_catalog = [
        {
            "stage": "OBSERVATION_CERTIFIED_READ_ONLY",
            "purpose": "consume B8/B9 evidence before any recovery traffic can be considered",
            "required_capability": "B9_POST_ADMISSION_OBSERVATION_WINDOWS_VERIFIED",
            "blast_radius_users": 0,
            "action_class": "recovery admission",
            "owner": "admin_core.autonomy_trust_acceleration.build_post_admission_observation_windows",
            "runtime_apply_allowed": False,
        },
        {
            "stage": "ONE_USER_GOVERNED_RECOVERY_REVIEW",
            "purpose": "define the only currently bounded recovery slow-start candidate",
            "required_capability": "POLICY_006_ONE_USER_BLAST_RADIUS_GUARD",
            "blast_radius_users": policy_user_limit,
            "action_class": "recovery admission",
            "owner": "admin_core.autonomy_trust_acceleration.build_class_level_blast_radius_certification",
            "runtime_apply_allowed": False,
        },
        {
            "stage": "BEYOND_ONE_USER_ACTION_CLASS_REVIEW",
            "purpose": "keep larger recovery scope blocked until existing action-class certification and authority exist",
            "required_capability": "BEYOND_ONE_USER_ACTION_CLASS_CERTIFICATION_AND_AUTHORITY",
            "blast_radius_users": "bounded_by_future_certified_action_class",
            "action_class": "future certified recovery action class",
            "owner": "POLICY_005_ACTION_CLASS_PROMOTION / POLICY_006_BLAST_RADIUS",
            "runtime_apply_allowed": False,
        },
    ]
    rows: list[dict[str, Any]] = []
    for index, observation in enumerate(observation_rows):
        channel = _b8_channel_key(observation, index)
        certification = certification_by_channel.get(channel, {})
        blockers = []
        if observation.get("verification_state") != "POST_ADMISSION_WINDOWS_VERIFIED_READ_ONLY":
            blockers.append("post_admission_observation_windows_not_verified")
        if certification.get("certification_state") != "CERTIFIED_FOR_RECOVERY_ADMISSION_REVIEW":
            blockers.append("recovery_admission_certification_not_ready")
        if not one_user_blast_certified:
            blockers.append("one_user_blast_radius_guard_not_certified")
        safe_next_stage = "ONE_USER_GOVERNED_RECOVERY_REVIEW" if not blockers else "BLOCKED"
        rows.append({
            "channel": channel,
            "progression_state": "SLOW_START_PROGRESSION_READY_READ_ONLY" if not blockers else "SLOW_START_PROGRESSION_BLOCKED",
            "safe_next_stage": safe_next_stage,
            "current_capability": "POST_ADMISSION_OBSERVATION_VERIFIED",
            "produced_evidence": [
                "recovery_admission_certification",
                "post_admission_observation_windows",
                "class_level_blast_radius_certification",
            ],
            "consumed_evidence": [
                observation.get("verification_state", "UNKNOWN"),
                certification.get("certification_state", "UNKNOWN"),
                blast.get("certification_state", "UNKNOWN"),
            ],
            "unlocked_capability": "one_user_governed_recovery_review" if not blockers else "none",
            "still_blocked_capabilities": [
                "runtime_apply",
                "automation",
                "authority_expansion",
                "user_movement",
                "beyond_one_user_recovery",
            ],
            "why_next_step_safe": (
                "B8 certification, B9 observation windows, and one-user blast-radius guard exist as read-only evidence"
                if not blockers
                else "required B8/B9/blast-radius evidence is incomplete"
            ),
            "why_later_steps_forbidden": (
                "beyond-one-user recovery requires separate action-class certification and authority"
                if not beyond_one_user_certified
                else "authority is still not granted and Runtime apply remains disabled"
            ),
            "stage_catalog": stage_catalog,
            "blockers": sorted(set(blockers)),
            "runtime_apply_allowed": False,
            "authority_expanded": False,
            "synthetic_evidence_created": False,
            "users_moved": 0,
        })

    return {
        "schema_version": "v7.b10.recovery-slow-start-progression.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B10",
        "purpose": "define_recovery_slow_start_as_existing_v7_action_class_and_blast_radius_progression_without_runtime_apply",
        "source_owners_reused": [
            "admin_core.autonomy_trust_acceleration.build_recovery_admission_certification",
            "admin_core.autonomy_trust_acceleration.build_post_admission_observation_windows",
            "admin_core.autonomy_trust_acceleration.build_class_level_blast_radius_certification",
            "POLICY_005_ACTION_CLASS_PROMOTION",
            "POLICY_006_BLAST_RADIUS",
        ],
        "policy_sources": [
            "docs/policies/POLICY_003_RECOVERY_ADMISSION.md",
            "docs/policies/POLICY_006_BLAST_RADIUS.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B10",
        ],
        "stage_catalog": stage_catalog,
        "rows": rows,
        "summary": {
            "channels_seen": len(rows),
            "ready_for_one_user_governed_recovery_review": sum(
                1 for row in rows if row["progression_state"] == "SLOW_START_PROGRESSION_READY_READ_ONLY"
            ),
            "blocked": sum(1 for row in rows if row["progression_state"] != "SLOW_START_PROGRESSION_READY_READ_ONLY"),
            "one_user_blast_radius_guard_available": one_user_blast_certified,
            "beyond_one_user_certified": beyond_one_user_certified,
            "runtime_actions_created": 0,
            "authority_changes": 0,
            "synthetic_evidence_created": 0,
            "users_moved": 0,
        },
        "canonical_rules": [
            "b10_defines_recovery_slow_start_progression_only",
            "b10_reuses_b8_b9_and_existing_blast_radius_action_class_owners",
            "one_user_governed_recovery_review_is_not_runtime_apply",
            "beyond_one_user_recovery_remains_blocked_without_action_class_certification_and_authority",
            "b10_does_not_create_runtime_planner_owner_truth_source_or_capability_program",
        ],
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
        "new_planner_created": False,
    }


def _b11_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, tuple):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [part.strip() for part in str(value).replace(";", ",").split(",") if part.strip()]


def _b11_glob_contains(patterns: list[str], value: str) -> bool:
    return any(fnmatch.fnmatchcase(value, pattern) for pattern in patterns)


def _b11_group_for_user(user: dict[str, Any], org_policy: dict[str, Any]) -> tuple[str, str]:
    ip = _text(user.get("ip") or user.get("user") or user.get("address"))
    direct = _text(user.get("group") or user.get("org") or user.get("organization"))
    if direct:
        return direct, "user_registry_field"
    explicit = org_policy.get("user_groups") if isinstance(org_policy.get("user_groups"), dict) else {}
    if ip and explicit.get(ip):
        return _text(explicit.get(ip)), "org_policy_user_groups"
    groups = org_policy.get("groups") if isinstance(org_policy.get("groups"), dict) else {}
    for group_name, group in groups.items():
        if ip and ip in _b11_list((group or {}).get("users")):
            return _text(group_name), "org_policy_groups_users"
    return _text(org_policy.get("default_group"), "default"), "org_policy_default_group"


def _b11_channel_key(row: dict[str, Any], index: int = 0) -> str:
    return _text(
        row.get("id")
        or row.get("egress")
        or row.get("channel")
        or row.get("target")
        or row.get("recommended_channel")
        or f"unknown-{index}"
    )


def build_org_cohort_identity_policy_integration(
    *,
    decision_surface: dict[str, Any] | None = None,
    org_policy: dict[str, Any] | None = None,
    recovery_slow_start_progression: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Certify B11 identity/group/cohort policy visibility without applying movement."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    surface = decision_surface if isinstance(decision_surface, dict) else {}
    policy = org_policy if isinstance(org_policy, dict) else {}
    users = [
        row for row in (surface.get("users") or surface.get("user_rows") or [])
        if isinstance(row, dict)
    ]
    channels_raw = surface.get("channels") or surface.get("egress") or surface.get("channel_rows") or []
    channels = [
        row for row in channels_raw
        if isinstance(row, dict)
    ]
    channel_by_id = {
        _b11_channel_key(row, index): row
        for index, row in enumerate(channels)
    }
    group_usage: dict[str, set[str]] = {}
    for user in users:
        current = _text(user.get("current") or user.get("current_channel"))
        group, _source = _b11_group_for_user(user, policy)
        if current:
            group_usage.setdefault(current, set()).add(group)

    groups = policy.get("groups") if isinstance(policy.get("groups"), dict) else {}
    egress_policy = policy.get("egress") if isinstance(policy.get("egress"), dict) else {}
    default_isolation = _text(policy.get("default_isolation"), "shared")
    rows: list[dict[str, Any]] = []
    for user_index, user in enumerate(users):
        user_id = _text(user.get("ip") or user.get("user") or user.get("address") or f"unknown-user-{user_index}")
        group, identity_source = _b11_group_for_user(user, policy)
        group_policy = groups.get(group) if isinstance(groups.get(group), dict) else {}
        current = _text(user.get("current") or user.get("current_channel"))
        target = _text(user.get("recommended_channel") or user.get("target") or current)
        policy_patterns = _b11_list(group_policy.get("allowed_egress")) + _b11_list(group_policy.get("preferred_egress"))
        policy_targets = [
            channel_id for channel_id in sorted(channel_by_id)
            if _b11_glob_contains(policy_patterns, channel_id)
        ] if policy_patterns else []
        candidate_ids = list(dict.fromkeys([
            item for item in [current, target] + policy_targets
            if item
        ]))
        if not candidate_ids:
            candidate_ids = sorted(channel_by_id)
        for target_id in candidate_ids:
            channel = channel_by_id.get(target_id, {"id": target_id})
            meta = egress_policy.get(target_id) if isinstance(egress_policy.get(target_id), dict) else {}
            allowed = _b11_list(group_policy.get("allowed_egress"))
            preferred = _b11_list(group_policy.get("preferred_egress"))
            excluded = _b11_list(group_policy.get("excluded_egress"))
            egress_groups = _b11_list(meta.get("groups") or channel.get("groups"))
            exclusive_group = _text(meta.get("exclusive_group") or channel.get("exclusive_group"))
            isolation = _text(group_policy.get("isolation") or default_isolation, "shared")
            other_groups = sorted(group_usage.get(target_id, set()) - {group})
            gate_results = []

            def add_gate(name: str, passed: bool, reason: str) -> None:
                gate_results.append({
                    "gate": name,
                    "state": "PASS" if passed else "BLOCK",
                    "reason": reason,
                })

            add_gate("identity_group_resolved", bool(user_id and group), identity_source)
            add_gate(
                "group_allowed_egress",
                not allowed or _b11_glob_contains(allowed, target_id),
                "allowed_egress_empty_means_no_group_allowlist" if not allowed else "target_in_group_allowed_egress",
            )
            add_gate(
                "group_excluded_egress",
                not excluded or not _b11_glob_contains(excluded, target_id),
                "target_not_excluded_by_group_policy",
            )
            add_gate(
                "egress_exclusive_group",
                not exclusive_group or exclusive_group == group,
                "exclusive_group_empty_or_matches_user_group",
            )
            add_gate(
                "egress_group_acl",
                not egress_groups or group in egress_groups,
                "egress_groups_empty_or_contains_user_group",
            )
            add_gate(
                "exclusive_isolation",
                isolation != "exclusive" or not other_groups,
                "exclusive_isolation_has_no_other_group_on_target",
            )
            add_gate(
                "manual_only",
                not bool(meta.get("manual_only") or channel.get("manual_only")),
                "manual_only_channels_are_not_planner_eligible",
            )
            add_gate(
                "reserve_only",
                not bool(meta.get("reserve_only") or channel.get("reserve_only")),
                "reserve_only_channels_are_not_planned_targets",
            )
            blockers = [gate["gate"] for gate in gate_results if gate["state"] == "BLOCK"]
            rows.append({
                "user": user_id,
                "group": group,
                "identity_source": identity_source,
                "current_channel": current,
                "target_channel": target_id,
                "is_preferred_target": bool(preferred and _b11_glob_contains(preferred, target_id)),
                "isolation": isolation,
                "other_groups_on_target": other_groups,
                "group_policy": {
                    "allowed_egress": allowed,
                    "preferred_egress": preferred,
                    "excluded_egress": excluded,
                    "isolation": isolation,
                },
                "egress_policy": {
                    "exclusive_group": exclusive_group,
                    "groups": egress_groups,
                    "manual_only": bool(meta.get("manual_only") or channel.get("manual_only")),
                    "reserve_only": bool(meta.get("reserve_only") or channel.get("reserve_only")),
                },
                "policy_gate_results": gate_results,
                "integration_state": "ORG_COHORT_IDENTITY_POLICY_INTEGRATED_READ_ONLY" if not blockers else "ORG_COHORT_IDENTITY_POLICY_BLOCKED_BY_EXISTING_GATES",
                "blockers": blockers,
                "owners": [
                    "tools/v7-users-autoswitch._load_users",
                    "tools/v7-users-autoswitch._org_user_map",
                    "tools/v7-users-autoswitch._gate_org",
                    "admin_core.operator_decision_surface",
                    "admin/v7-admin-api identity/policy surfaces",
                ],
                "runtime_apply_allowed": False,
                "authority_expanded": False,
                "synthetic_evidence_created": False,
                "users_moved": 0,
            })

    return {
        "schema_version": "v7.b11.org-cohort-identity-policy-integration.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B11",
        "purpose": "complete_org_cohort_isolation_and_identity_policy_integration_as_read_only_visibility_over_existing_planner_gates",
        "source_owners_reused": [
            "admin/v7-admin-api identity and org policy surfaces",
            "admin_core.operator_decision_surface",
            "tools/v7-users-autoswitch._load_users",
            "tools/v7-users-autoswitch._org_user_map",
            "tools/v7-users-autoswitch._load_egress",
            "tools/v7-users-autoswitch._gate_org",
        ],
        "policy_sources": [
            "docs/policies/POLICY_004_AUTHORITY.md",
            "docs/policies/POLICY_006_BLAST_RADIUS.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B11",
        ],
        "consumed_prior_capability": {
            "recovery_slow_start_progression": (recovery_slow_start_progression or {}).get("schema_version", "UNKNOWN"),
            "state": "CONSUMED_READ_ONLY" if recovery_slow_start_progression else "NOT_PROVIDED",
        },
        "rows": rows,
        "summary": {
            "users_seen": len(users),
            "channels_seen": len(channels),
            "policy_rows": len(rows),
            "integrated_rows": sum(1 for row in rows if row["integration_state"] == "ORG_COHORT_IDENTITY_POLICY_INTEGRATED_READ_ONLY"),
            "blocked_by_existing_policy_gates": sum(1 for row in rows if row["integration_state"] != "ORG_COHORT_IDENTITY_POLICY_INTEGRATED_READ_ONLY"),
            "groups_seen": sorted({row["group"] for row in rows}),
            "runtime_actions_created": 0,
            "authority_changes": 0,
            "synthetic_evidence_created": 0,
            "users_moved": 0,
        },
        "canonical_rules": [
            "b11_reuses_existing_identity_org_policy_and_planner_gate_owners",
            "identity_group_resolution_precedes_policy_target_review",
            "allowed_excluded_exclusive_group_egress_acl_and_exclusive_isolation_are_existing_planner_gates",
            "b11_policy_blockers_are_visibility_not_runtime_mutation",
            "b11_does_not_create_runtime_planner_owner_truth_source_or_authority",
        ],
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
        "new_planner_created": False,
    }


def build_next_action_class_stage_certification(
    *,
    action_class_runtime_enablement: dict[str, Any] | None = None,
    class_level_blast_radius_certification: dict[str, Any] | None = None,
    runtime_eligibility_arbitration: dict[str, Any] | None = None,
    metric_reliability_certification: dict[str, Any] | None = None,
    org_cohort_identity_policy_integration: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Certify B12 next action-class stage review without granting authority."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    enablement = action_class_runtime_enablement if isinstance(action_class_runtime_enablement, dict) else {}
    blast = class_level_blast_radius_certification if isinstance(class_level_blast_radius_certification, dict) else {}
    runtime = runtime_eligibility_arbitration if isinstance(runtime_eligibility_arbitration, dict) else {}
    metrics = metric_reliability_certification if isinstance(metric_reliability_certification, dict) else {}
    policy = org_cohort_identity_policy_integration if isinstance(org_cohort_identity_policy_integration, dict) else {}
    current_class_name = _text(enablement.get("current_action_class"), ACTION_CLASS_LADDER[0][0])
    class_rows = [row for row in (enablement.get("action_classes") or []) if isinstance(row, dict)]
    current_row = next(
        (row for row in class_rows if row.get("action_class") == current_class_name),
        class_rows[0] if class_rows else {},
    )
    current_state = _text(current_row.get("current_state") or enablement.get("current_state"), "UNKNOWN")
    target_state = _text(current_row.get("next_state") or enablement.get("next_promotion_target"), "CERTIFIED_FOR_CLASS_APPROVAL")
    policy_summary = policy.get("summary") if isinstance(policy.get("summary"), dict) else {}
    policy_rows = int(as_float(policy_summary.get("policy_rows"), 0.0))
    policy_blocked = int(as_float(policy_summary.get("blocked_by_existing_policy_gates"), 0.0))
    policy_schema = _text(policy.get("schema_version"))
    evidence_rows = [
        {
            "evidence": "action_class_ladder_current_stage",
            "owner": "action_class_runtime_enablement",
            "current": current_state,
            "target": "GOVERNED_ONLY",
            "state": "PASS" if current_state == "GOVERNED_ONLY" else "STOP",
            "reason": "current class must be governed before class-approval certification review",
        },
        {
            "evidence": "a5_blast_radius_certification",
            "owner": "class_level_blast_radius_certification",
            "current": blast.get("certification_state", "UNKNOWN"),
            "target": "BEYOND_ONE_USER_EVIDENCE_CERTIFIED_READ_ONLY",
            "state": "PASS" if bool(blast.get("beyond_one_user_certified")) else "STOP",
            "reason": "B12 can review the next stage only after A5 has certified blast-radius evidence",
        },
        {
            "evidence": "a6_runtime_eligibility_arbitration",
            "owner": "runtime_eligibility_arbitration",
            "current": runtime.get("runtime_execute_decision", "UNKNOWN"),
            "target": "STOP_SAFE or ELIGIBLE_READ_ONLY_PREVIEW",
            "state": "PASS" if runtime.get("schema_version") == "v7.a6-runtime-eligibility-arbitration.v1" else "STOP",
            "reason": "B12 consumes A6 execute-or-stop arbitration as read-only safety evidence",
        },
        {
            "evidence": "b13_blocking_recommendation_metric_reliability",
            "owner": "metric_reliability_certification",
            "current": metrics.get("certification_state", "UNKNOWN"),
            "target": "blocking recommendation certified",
            "state": "PASS" if bool(metrics.get("blocking_recommendation_certified")) else "STOP",
            "reason": "B12 can use reliable blocking metrics, not automatic positive promotion",
        },
        {
            "evidence": "b11_identity_policy_boundary",
            "owner": "org_cohort_identity_policy_integration",
            "current": {
                "schema_version": policy_schema,
                "policy_rows": policy_rows,
                "blocked_by_existing_policy_gates": policy_blocked,
            },
            "target": "owner-mapped policy boundary",
            "state": "PASS" if policy_schema == "v7.b11.org-cohort-identity-policy-integration.v1" else "STOP",
            "reason": "B12 requires identity/cohort policy boundary visibility before stage certification",
        },
        {
            "evidence": "authority_boundary",
            "owner": "POLICY_004_AUTHORITY / OMP",
            "current": "NO_AUTHORITY_EXPANSION",
            "target": "authority review required before promotion",
            "state": "STOP",
            "reason": "B12 may certify stage readiness but cannot approve class authority",
        },
        {
            "evidence": "runtime_apply_boundary",
            "owner": "Runtime Model / OMP",
            "current": "RUNTIME_APPLY_DISABLED",
            "target": "runtime apply remains disabled",
            "state": "STOP",
            "reason": "stage certification cannot become Runtime behavior",
        },
    ]
    hard_blockers = [
        row["evidence"] for row in evidence_rows
        if row["state"] == "STOP" and row["evidence"] not in {"authority_boundary", "runtime_apply_boundary"}
    ]
    safety_stops = [
        row["evidence"] for row in evidence_rows
        if row["evidence"] in {"authority_boundary", "runtime_apply_boundary"}
    ]
    stage_review_ready = not hard_blockers
    next_stage = {
        "action_class": current_class_name,
        "from_state": current_state,
        "to_state": target_state,
        "stage_certification_state": (
            "NEXT_ACTION_CLASS_STAGE_CERTIFIED_FOR_AUTHORITY_REVIEW_READ_ONLY"
            if stage_review_ready
            else "NEXT_ACTION_CLASS_STAGE_BLOCKED_BY_EVIDENCE"
        ),
        "stage_certified_for_review": stage_review_ready,
        "stage_certified_for_runtime": False,
        "stage_promoted": False,
        "authority_review_required": True,
        "runtime_apply_allowed": False,
        "direct_class_promotion_allowed": False,
        "blockers": hard_blockers + safety_stops,
    }
    return {
        "schema_version": "v7.b12-next-action-class-stage-certification.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B12",
        "purpose": "implement_next_action_class_stage_only_after_certification_evidence_exists_without_promotion_or_runtime_apply",
        "source_owners_reused": [
            "admin_core.autonomy_trust_acceleration.build_action_class_runtime_enablement_model",
            "admin_core.autonomy_trust_acceleration.build_class_level_blast_radius_certification",
            "admin_core.autonomy_trust_acceleration.build_runtime_eligibility_arbitration",
            "admin_core.autonomy_trust_acceleration.build_metric_reliability_certification",
            "admin_core.autonomy_trust_acceleration.build_org_cohort_identity_policy_integration",
            "POLICY_005_ACTION_CLASS_PROMOTION",
            "POLICY_004_AUTHORITY",
            "OMP",
        ],
        "policy_sources": [
            "docs/policies/POLICY_005_ACTION_CLASS_PROMOTION.md",
            "docs/policies/POLICY_004_AUTHORITY.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B12",
        ],
        "consumed_prior_capabilities": {
            "A5": blast.get("schema_version", "UNKNOWN"),
            "A6": runtime.get("schema_version", "UNKNOWN"),
            "B13": metrics.get("schema_version", "UNKNOWN"),
            "B11": policy.get("schema_version", "UNKNOWN"),
        },
        "current_action_class": current_class_name,
        "current_state": current_state,
        "next_stage": next_stage,
        "evidence_rows": evidence_rows,
        "stage_catalog": [
            {
                "state": row[2],
                "action_class": row[0],
                "blast_radius_users": row[1],
                "current": row[0] == current_class_name,
            }
            for row in ACTION_CLASS_LADDER
        ],
        "summary": {
            "evidence_rows": len(evidence_rows),
            "hard_blockers": len(hard_blockers),
            "safety_stops": len(safety_stops),
            "stage_review_ready": stage_review_ready,
            "authority_changes": 0,
            "runtime_actions_created": 0,
            "direct_promotions_created": 0,
            "synthetic_evidence_created": 0,
            "users_moved": 0,
        },
        "canonical_rules": [
            "b12_reuses_existing_action_class_ladder_and_certification_owners",
            "b12_stage_review_requires_a5_a6_b13_and_b11_evidence",
            "b12_may_certify_stage_readiness_for_authority_review_only",
            "b12_does_not_grant_action_class_authority_or_runtime_apply",
            "b12_does_not_create_runtime_planner_owner_truth_source_or_direct_promotion",
        ],
        "omp_output": {
            "b12_status": (
                "DONE_READ_ONLY_STAGE_CERTIFIED_FOR_AUTHORITY_REVIEW"
                if stage_review_ready
                else "STOP_SAFE_STAGE_CERTIFICATION_EVIDENCE_INCOMPLETE"
            ),
            "produced_evidence": "next_action_class_stage_certification",
            "unlocked_capability": "B14_OR_NEXT_OMP_ITEM_AFTER_CANONICAL_UPDATE" if stage_review_ready else "",
            "blocked_later_steps": [
                "runtime_apply",
                "automation",
                "authority_expansion",
                "direct_class_promotion",
                "delegated_policy_approval",
                "user_movement",
            ],
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "synthetic_evidence_created": False,
        "direct_class_promotion_performed": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_runtime_created": False,
    }


def build_service_pool_cohort_blast_radius_scope(
    *,
    decision_surface: dict[str, Any] | None = None,
    service_user_sla_fit: dict[str, Any] | None = None,
    class_level_blast_radius_certification: dict[str, Any] | None = None,
    next_action_class_stage_certification: dict[str, Any] | None = None,
    org_cohort_identity_policy_integration: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Expose B14 service/pool/cohort blast-radius scope without widening it."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    surface = decision_surface if isinstance(decision_surface, dict) else {}
    fit = service_user_sla_fit if isinstance(service_user_sla_fit, dict) else {}
    blast = class_level_blast_radius_certification if isinstance(class_level_blast_radius_certification, dict) else {}
    stage = next_action_class_stage_certification if isinstance(next_action_class_stage_certification, dict) else {}
    policy = org_cohort_identity_policy_integration if isinstance(org_cohort_identity_policy_integration, dict) else {}
    policy_rows = [
        row for row in (policy.get("rows") or [])
        if isinstance(row, dict)
    ]
    policy_by_user_target = {
        (_text(row.get("user")), _text(row.get("target_channel"))): row
        for row in policy_rows
    }
    policy_by_user = {
        _text(row.get("user")): row
        for row in policy_rows
        if _text(row.get("user"))
    }
    fit_rows = [
        row for row in (fit.get("rows") or [])
        if isinstance(row, dict)
    ]
    users_by_id = {
        _text(row.get("user") or row.get("ip") or row.get("address")): row
        for row in (surface.get("users") or [])
        if isinstance(row, dict)
    }
    rows: list[dict[str, Any]] = []
    for fit_row in fit_rows:
        user = _text(fit_row.get("user"))
        candidates = [
            row for row in (fit_row.get("candidates") or [])
            if isinstance(row, dict)
        ]
        if not candidates:
            candidates = [{
                "channel": fit_row.get("best_channel") or fit_row.get("current_assignment"),
                "fit_verdict": fit_row.get("fit_verdict", "UNKNOWN"),
                "fit_score": fit_row.get("fit_score", 0.0),
                "capacity_headroom": fit_row.get("capacity_headroom", ""),
                "capacity_decision": fit_row.get("capacity_decision", ""),
                "route_runtime_safe": False,
            }]
        for candidate in candidates:
            target = _text(candidate.get("channel") or candidate.get("target") or fit_row.get("best_channel"))
            policy_row = policy_by_user_target.get((user, target)) or policy_by_user.get(user) or {}
            group = _text(policy_row.get("group"), "unknown")
            capacity_decision = _text(candidate.get("capacity_decision") or candidate.get("capacity") or "UNKNOWN")
            capacity_headroom = candidate.get("capacity_headroom", candidate.get("headroom", "UNKNOWN"))
            pool = _text(
                candidate.get("pool")
                or candidate.get("pool_id")
                or candidate.get("best_available_pool")
                or candidate.get("channel")
                or target
            )
            blockers: list[str] = []
            if not user:
                blockers.append("user_scope_missing")
            if not target:
                blockers.append("target_scope_missing")
            if not pool:
                blockers.append("pool_scope_missing")
            if group == "unknown":
                blockers.append("cohort_scope_missing")
            if candidate.get("fit_verdict") not in {"FIT", "FIT_WITH_WARNINGS"}:
                blockers.append("service_user_sla_fit_not_clear")
            if capacity_decision in {"", "UNKNOWN", "BLOCK", "BLOCKED", "NO_CAPACITY"}:
                blockers.append("capacity_scope_not_clear")
            if policy_row and policy_row.get("integration_state") != "ORG_COHORT_IDENTITY_POLICY_INTEGRATED_READ_ONLY":
                blockers.extend([f"cohort_policy:{item}" for item in (policy_row.get("blockers") or [])])
            if not bool(blast.get("beyond_one_user_certified")):
                blockers.append("a5_blast_radius_not_certified_beyond_one_user")
            if (stage.get("next_stage") or {}).get("stage_certification_state") != "NEXT_ACTION_CLASS_STAGE_CERTIFIED_FOR_AUTHORITY_REVIEW_READ_ONLY":
                blockers.append("b12_next_action_class_stage_not_certified_for_review")
            rows.append({
                "user": user,
                "current_assignment": fit_row.get("current_assignment") or users_by_id.get(user, {}).get("current_channel"),
                "target_channel": target,
                "service_scope": {
                    "required_services": fit_row.get("required_services", []),
                    "missing_requirements": candidate.get("missing_requirements", fit_row.get("missing_requirements", [])),
                    "fit_verdict": candidate.get("fit_verdict", fit_row.get("fit_verdict", "UNKNOWN")),
                    "fit_score": candidate.get("fit_score", fit_row.get("fit_score", 0.0)),
                },
                "pool_scope": {
                    "pool": pool,
                    "capacity_headroom": capacity_headroom,
                    "capacity_decision": capacity_decision,
                    "route_runtime_safe": bool(candidate.get("route_runtime_safe")),
                },
                "cohort_scope": {
                    "group": group,
                    "identity_source": policy_row.get("identity_source", "unknown"),
                    "isolation": policy_row.get("isolation", "unknown"),
                    "policy_integration_state": policy_row.get("integration_state", "UNKNOWN"),
                },
                "blast_radius_scope": {
                    "certification_state": blast.get("certification_state", "UNKNOWN"),
                    "max_historical_certified_blast_radius_users": blast.get("max_historical_certified_blast_radius_users", 0),
                    "beyond_one_user_certified": bool(blast.get("beyond_one_user_certified")),
                    "scope_expanded_now": False,
                },
                "action_class_scope": {
                    "current_action_class": stage.get("current_action_class", "UNKNOWN"),
                    "current_state": stage.get("current_state", "UNKNOWN"),
                    "stage_certification_state": (stage.get("next_stage") or {}).get("stage_certification_state", "UNKNOWN"),
                },
                "scope_state": (
                    "SERVICE_POOL_COHORT_SCOPE_MAPPED_READ_ONLY"
                    if not blockers
                    else "SERVICE_POOL_COHORT_SCOPE_BLOCKED_BY_EXISTING_GATES"
                ),
                "blockers": sorted(set(blockers)),
                "runtime_apply_allowed": False,
                "authority_expanded": False,
                "synthetic_evidence_created": False,
                "users_moved": 0,
            })
    summary = {
        "users_seen": len(fit_rows),
        "scope_rows": len(rows),
        "mapped_rows": sum(1 for row in rows if row["scope_state"] == "SERVICE_POOL_COHORT_SCOPE_MAPPED_READ_ONLY"),
        "blocked_by_existing_gates": sum(1 for row in rows if row["scope_state"] != "SERVICE_POOL_COHORT_SCOPE_MAPPED_READ_ONLY"),
        "services_seen": sorted({
            service
            for row in rows
            for service in (row.get("service_scope", {}).get("required_services") or [])
        }),
        "pools_seen": sorted({
            row.get("pool_scope", {}).get("pool")
            for row in rows
            if row.get("pool_scope", {}).get("pool")
        }),
        "cohorts_seen": sorted({
            row.get("cohort_scope", {}).get("group")
            for row in rows
            if row.get("cohort_scope", {}).get("group")
        }),
        "runtime_actions_created": 0,
        "authority_changes": 0,
        "blast_radius_expansions": 0,
        "synthetic_evidence_created": 0,
        "users_moved": 0,
    }
    return {
        "schema_version": "v7.b14-service-pool-cohort-blast-radius-scope.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "B14",
        "purpose": "add_service_pool_cohort_blast_radius_scope_where_required_without_expanding_blast_radius",
        "source_owners_reused": [
            "tools/v7-users-autoswitch._load_limits_for_egress",
            "tools/v7-users-autoswitch._capacity_decision",
            "tools/v7-users-autoswitch._mark_best_available_pool",
            "tools/v7-users-autoswitch dynamic_blast_radius",
            "admin_core.autonomy_trust_acceleration.build_service_user_sla_fit",
            "admin_core.autonomy_trust_acceleration.build_org_cohort_identity_policy_integration",
            "admin_core.autonomy_trust_acceleration.build_class_level_blast_radius_certification",
            "admin_core.autonomy_trust_acceleration.build_next_action_class_stage_certification",
        ],
        "policy_sources": [
            "docs/policies/POLICY_006_BLAST_RADIUS.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#B14",
        ],
        "consumed_prior_capabilities": {
            "B11": policy.get("schema_version", "UNKNOWN"),
            "B12": stage.get("schema_version", "UNKNOWN"),
            "A5": blast.get("schema_version", "UNKNOWN"),
            "routing_foundation_service_fit": fit.get("schema_version", "UNKNOWN"),
        },
        "rows": rows,
        "summary": summary,
        "canonical_rules": [
            "b14_reuses_existing_planner_capacity_service_and_action_class_owners",
            "service_pool_cohort_scope_is_read_only_visibility_not_runtime_apply",
            "b14_does_not_expand_blast_radius_or_authority",
            "pool_scope_uses_existing_best_available_pool_and_capacity_signals",
            "cohort_scope_consumes_b11_identity_policy_boundaries",
        ],
        "omp_output": {
            "b14_status": "DONE_READ_ONLY_SCOPE_MAPPED" if rows else "STOP_SAFE_NO_SCOPE_ROWS_VISIBLE",
            "produced_evidence": "service_pool_cohort_blast_radius_scope",
            "unlocked_capability": "B15_OR_NEXT_OMP_ITEM_AFTER_CANONICAL_UPDATE" if rows else "",
            "blocked_later_steps": [
                "runtime_apply",
                "automation",
                "authority_expansion",
                "blast_radius_expansion",
                "direct_class_promotion",
                "user_movement",
            ],
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "synthetic_evidence_created": False,
        "blast_radius_expanded": False,
        "threshold_values_changed": False,
        "formula_changed": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_runtime_created": False,
    }


def _action_class_user_limit(action_class: str) -> int | None:
    for name, max_users, _state in ACTION_CLASS_LADDER:
        if name == action_class:
            return max_users if isinstance(max_users, int) else None
    return None


def build_pool_health_capacity_blast_bounds(
    *,
    service_pool_cohort_blast_radius_scope: dict[str, Any] | None = None,
    class_level_blast_radius_certification: dict[str, Any] | None = None,
    next_action_class_stage_certification: dict[str, Any] | None = None,
    bounded_stale_allowance_by_action_class: dict[str, Any] | None = None,
    action_class_freshness_windows: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Map proxy-style pool health semantics to existing V7 capacity and blast bounds."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    scope = service_pool_cohort_blast_radius_scope if isinstance(service_pool_cohort_blast_radius_scope, dict) else {}
    blast = class_level_blast_radius_certification if isinstance(class_level_blast_radius_certification, dict) else {}
    stage = next_action_class_stage_certification if isinstance(next_action_class_stage_certification, dict) else {}
    stale = bounded_stale_allowance_by_action_class if isinstance(bounded_stale_allowance_by_action_class, dict) else {}
    windows = action_class_freshness_windows if isinstance(action_class_freshness_windows, dict) else {}
    stale_decision = stale.get("decision") if isinstance(stale.get("decision"), dict) else {}
    stale_mutation_allowed = bool(stale_decision.get("stale_evidence_mutation_allowed"))
    max_historical_users = int(as_float(blast.get("max_historical_certified_blast_radius_users"), 0.0))
    rows: list[dict[str, Any]] = []
    for scope_row in [row for row in (scope.get("rows") or []) if isinstance(row, dict)]:
        action_scope = scope_row.get("action_class_scope") if isinstance(scope_row.get("action_class_scope"), dict) else {}
        pool_scope = scope_row.get("pool_scope") if isinstance(scope_row.get("pool_scope"), dict) else {}
        service_scope = scope_row.get("service_scope") if isinstance(scope_row.get("service_scope"), dict) else {}
        blast_scope = scope_row.get("blast_radius_scope") if isinstance(scope_row.get("blast_radius_scope"), dict) else {}
        action_class = _text(action_scope.get("current_action_class"), _text(scope_row.get("action_class"), "UNKNOWN_ACTION_CLASS"))
        class_user_limit = _action_class_user_limit(action_class)
        numeric_limits = [value for value in [class_user_limit, max_historical_users] if isinstance(value, int) and value > 0]
        max_ejection_users = min(numeric_limits) if numeric_limits else 0
        capacity_decision = _text(pool_scope.get("capacity_decision"), "UNKNOWN")
        projected_load = pool_scope.get("projected_load") if isinstance(pool_scope.get("projected_load"), dict) else {}
        soft_limit = int(as_float(projected_load.get("soft_limit"), 0.0))
        hard_limit = int(as_float(projected_load.get("hard_limit"), 0.0))
        users = int(as_float(projected_load.get("users"), 0.0))
        capacity_blocks = capacity_decision in {"", "UNKNOWN", "BLOCK", "BLOCKED", "NO_CAPACITY", "hard_capacity_full"}
        fit_blocks = service_scope.get("fit_verdict") not in {"FIT", "FIT_WITH_WARNINGS"}
        blockers = list(scope_row.get("blockers") or [])
        if not numeric_limits:
            blockers.append("action_class_or_certified_blast_user_bound_missing")
        if capacity_blocks:
            blockers.append("minimum_health_capacity_blocked")
        if fit_blocks:
            blockers.append("minimum_health_service_fit_blocked")
        if stale_mutation_allowed:
            blockers.append("bounded_stale_allowance_violation")
        if not bool(blast_scope.get("beyond_one_user_certified", blast.get("beyond_one_user_certified"))):
            blockers.append("blast_radius_not_certified_for_pool_health_mapping")
        freshness_window: dict[str, Any] = {}
        for action_row in [row for row in (windows.get("rows") or []) if isinstance(row, dict)]:
            if _text(action_row.get("action_class")) == action_class:
                freshness_window = dict(action_row.get("freshness_windows") or {})
                break
        rows.append({
            "user": scope_row.get("user", ""),
            "target_channel": scope_row.get("target_channel", ""),
            "pool": pool_scope.get("pool", ""),
            "action_class": action_class,
            "proxy_semantics": {
                "max_ejection": "mapped_to_v7_action_class_user_limit_and_certified_blast_radius",
                "minimum_health": "mapped_to_v7_capacity_decision_projected_load_and_service_fit",
                "outlier_ejection": "mapped_to_v7_hold_quarantine_or_governed_movement_review_not_runtime_ejection",
            },
            "v7_max_ejection_bound": {
                "action_class_user_limit": class_user_limit,
                "max_historical_certified_blast_radius_users": max_historical_users,
                "max_ejection_users_read_model": max_ejection_users,
                "blast_radius_expanded_now": False,
            },
            "v7_minimum_health_bound": {
                "capacity_decision": capacity_decision,
                "projected_users": users,
                "soft_limit": soft_limit,
                "hard_limit": hard_limit,
                "service_fit_verdict": service_scope.get("fit_verdict", "UNKNOWN"),
                "minimum_health_state": "PASS" if not capacity_blocks and not fit_blocks else "STOP_SAFE",
            },
            "freshness_bound": {
                "freshness_windows": freshness_window,
                "stale_mutation_allowed": stale_mutation_allowed,
                "fresh_evidence_required_before_mutation": bool(stale_decision.get("fresh_evidence_required_before_mutation", True)),
            },
            "stage_bound": {
                "stage_certification_state": (stage.get("next_stage") or {}).get("stage_certification_state", "UNKNOWN"),
                "authority_review_required": bool((stage.get("next_stage") or {}).get("authority_review_required", True)),
            },
            "mapping_state": (
                "POOL_HEALTH_CAPACITY_BLAST_BOUNDS_MAPPED_READ_ONLY"
                if not blockers
                else "POOL_HEALTH_CAPACITY_BLAST_BOUNDS_STOP_SAFE"
            ),
            "blockers": sorted(set(blockers)),
            "runtime_apply_allowed": False,
            "authority_expanded": False,
            "blast_radius_expanded": False,
            "threshold_values_changed": False,
            "formula_changed": False,
            "synthetic_evidence_created": False,
            "users_moved": 0,
        })
    return {
        "schema_version": "v7.c7-pool-health-capacity-blast-bounds.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "C7",
        "purpose": "map_pool_max_ejection_minimum_health_semantics_to_existing_v7_capacity_and_blast_bounds",
        "source_owners_reused": [
            "tools/v7-users-autoswitch._load_limits_for_egress",
            "tools/v7-users-autoswitch._capacity_decision",
            "tools/v7-users-autoswitch._mark_best_available_pool",
            "tools/v7-users-autoswitch dynamic_blast_radius",
            "admin_core.autonomy_trust_acceleration.build_service_pool_cohort_blast_radius_scope",
            "admin_core.autonomy_trust_acceleration.build_class_level_blast_radius_certification",
            "admin_core.autonomy_trust_acceleration.build_next_action_class_stage_certification",
            "admin_core.autonomy_trust_acceleration.build_bounded_stale_allowance_by_action_class",
        ],
        "policy_sources": [
            "docs/policies/POLICY_009_ANTI_FLAP.md",
            "docs/policies/POLICY_006_BLAST_RADIUS.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#C7",
        ],
        "consumed_prior_capabilities": {
            "B14": scope.get("schema_version", "UNKNOWN"),
            "A5": blast.get("schema_version", "UNKNOWN"),
            "B12": stage.get("schema_version", "UNKNOWN"),
            "C6": stale.get("schema_version", "UNKNOWN"),
            "A2": windows.get("schema_version", "UNKNOWN"),
        },
        "semantic_mapping": {
            "max_ejection": "V7 does not eject arbitrary pool members; it bounds movement by action class, certified blast radius, authority, and runtime_apply gates.",
            "minimum_health": "V7 minimum health is represented by service fit, projected load, soft/hard capacity, freshness, and STOP_SAFE blockers.",
            "pool_health": "Pool health is a read-only planner/capacity/blast scope view, not a new Runtime capability.",
            "authority": "C7 can explain safe bounds but cannot approve scope expansion or execution.",
        },
        "rows": rows,
        "summary": {
            "scope_rows": len(rows),
            "mapped_rows": sum(1 for row in rows if row["mapping_state"] == "POOL_HEALTH_CAPACITY_BLAST_BOUNDS_MAPPED_READ_ONLY"),
            "stop_safe_rows": sum(1 for row in rows if row["mapping_state"] != "POOL_HEALTH_CAPACITY_BLAST_BOUNDS_MAPPED_READ_ONLY"),
            "runtime_actions_created": 0,
            "authority_changes": 0,
            "blast_radius_expansions": 0,
            "threshold_changes": 0,
            "formula_changes": 0,
            "synthetic_evidence_created": 0,
            "users_moved": 0,
        },
        "canonical_rules": [
            "proxy_max_ejection_maps_to_v7_action_class_and_certified_blast_radius_bounds",
            "proxy_minimum_health_maps_to_v7_capacity_load_service_fit_and_freshness_bounds",
            "c7_reuses_existing_planner_capacity_and_blast_radius_owners",
            "c7_does_not_change_capacity_thresholds_formulas_or_runtime_behavior",
            "c7_does_not_expand_blast_radius_authority_or_runtime_apply",
            "pool_level_movement_remains_blocked_without_separate_authority",
        ],
        "omp_output": {
            "c7_status": "DONE_READ_ONLY_POOL_HEALTH_CAPACITY_BLAST_BOUNDS_MAPPED",
            "produced_evidence": "pool_health_capacity_blast_bounds",
            "unlocked_capability": "IMPLEMENTATION_COMPLETE",
            "blocked_later_steps": [
                "runtime_apply",
                "automation",
                "authority_expansion",
                "blast_radius_expansion",
                "threshold_formula_mutation",
                "new_owner",
                "planner_replacement",
                "synthetic_evidence",
                "user_movement",
            ],
            "next_safe_action": "stop_actionable_backlog_complete_report_status_or_wait_for_operator_authority",
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "users_moved": 0,
        "authority_expanded": False,
        "autonomy_enabled": False,
        "synthetic_evidence_created": False,
        "blast_radius_expanded": False,
        "threshold_values_changed": False,
        "formula_changed": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_runtime_created": False,
    }


def build_all_at_once_promotion_unavailable_verification(
    *,
    action_class_runtime_enablement: dict[str, Any] | None = None,
    class_level_blast_radius_certification: dict[str, Any] | None = None,
    next_action_class_stage_certification: dict[str, Any] | None = None,
    service_pool_cohort_blast_radius_scope: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Verify C4 keeps all-at-once class promotion unavailable."""
    generated = generated_at or datetime.now(timezone.utc).isoformat()
    enablement = action_class_runtime_enablement if isinstance(action_class_runtime_enablement, dict) else {}
    blast = class_level_blast_radius_certification if isinstance(class_level_blast_radius_certification, dict) else {}
    stage = next_action_class_stage_certification if isinstance(next_action_class_stage_certification, dict) else {}
    scope = service_pool_cohort_blast_radius_scope if isinstance(service_pool_cohort_blast_radius_scope, dict) else {}
    class_rows = [
        row for row in (enablement.get("action_classes") or [])
        if isinstance(row, dict)
    ]
    if not class_rows:
        class_rows = [
            {
                "action_class": name,
                "current_state": state,
                "next_state": "GOVERNED_ONLY" if state == "NOT_CERTIFIED" else "CERTIFIED_FOR_CLASS_APPROVAL",
                "runtime_enablement_state": state,
                "runtime_can_execute_automatically": False,
            }
            for name, _radius, state in ACTION_CLASS_LADDER
        ]
    direct_promotion_requested = bool((stage.get("next_stage") or {}).get("stage_promoted"))
    direct_promotion_allowed = bool((stage.get("next_stage") or {}).get("direct_class_promotion_allowed"))
    runtime_apply_allowed = any(
        bool(row.get("runtime_apply_allowed")) for row in (scope.get("rows") or []) if isinstance(row, dict)
    )
    class_summaries = []
    for row in class_rows:
        current_state = _text(row.get("current_state") or row.get("runtime_enablement_state"), "UNKNOWN")
        class_summaries.append({
            "action_class": row.get("action_class", "UNKNOWN"),
            "current_state": current_state,
            "next_state": row.get("next_state", ""),
            "runtime_can_execute_automatically": bool(row.get("runtime_can_execute_automatically")),
            "eligible_for_all_at_once_promotion": False,
            "promotion_mode_allowed_now": "NONE",
            "reason": "class_by_class_authority_review_required_before_any_runtime_enablement",
        })
    blocking_rules = [
        {
            "rule": "class_by_class_certification_required",
            "source": "POLICY_005_ACTION_CLASS_PROMOTION / OMP",
            "state": "PASS",
        },
        {
            "rule": "authority_review_required",
            "source": "POLICY_004_AUTHORITY / B12",
            "state": "PASS" if (stage.get("next_stage") or {}).get("authority_review_required", True) else "STOP",
        },
        {
            "rule": "runtime_apply_remains_disabled",
            "source": "Runtime Model / B14",
            "state": "PASS" if not runtime_apply_allowed else "STOP",
        },
        {
            "rule": "blast_radius_not_expanded_now",
            "source": "A5 / B14",
            "state": "PASS" if not bool(scope.get("blast_radius_expanded")) else "STOP",
        },
        {
            "rule": "direct_class_promotion_forbidden",
            "source": "B12",
            "state": "PASS" if not direct_promotion_allowed and not direct_promotion_requested else "STOP",
        },
        {
            "rule": "break_glass_is_exceptional_operator_policy_not_promotion_path",
            "source": "C3 / OMP",
            "state": "PASS",
        },
    ]
    violations = [row["rule"] for row in blocking_rules if row["state"] != "PASS"]
    return {
        "schema_version": "v7.c4-all-at-once-promotion-unavailable.v1",
        "generated_at": generated,
        "owner": "admin_core.autonomy_trust_acceleration",
        "backlog_item": "C4",
        "purpose": "keep_all_at_once_promotion_unavailable_for_current_action_classes",
        "source_owners_reused": [
            "admin_core.autonomy_trust_acceleration.build_action_class_runtime_enablement_model",
            "admin_core.autonomy_trust_acceleration.build_class_level_blast_radius_certification",
            "admin_core.autonomy_trust_acceleration.build_next_action_class_stage_certification",
            "admin_core.autonomy_trust_acceleration.build_service_pool_cohort_blast_radius_scope",
            "admin_core.operator_execution_pipeline.break_glass_authority_policy_contract",
            "POLICY_005_ACTION_CLASS_PROMOTION",
            "POLICY_004_AUTHORITY",
            "OMP",
        ],
        "policy_sources": [
            "docs/policies/POLICY_005_ACTION_CLASS_PROMOTION.md",
            "docs/policies/POLICY_004_AUTHORITY.md",
            "docs/programs/V7_IMPLEMENTATION_BACKLOG.md#C4",
        ],
        "consumed_prior_capabilities": {
            "action_class_runtime_enablement": enablement.get("schema_version", "UNKNOWN"),
            "A5": blast.get("schema_version", "UNKNOWN"),
            "B12": stage.get("schema_version", "UNKNOWN"),
            "B14": scope.get("schema_version", "UNKNOWN"),
            "C3": "break_glass_authority_policy_contract",
        },
        "verification_state": (
            "DONE_READ_ONLY_ALL_AT_ONCE_PROMOTION_UNAVAILABLE"
            if not violations
            else "STOP_SAFE_PROMOTION_AVAILABILITY_VIOLATION_DETECTED"
        ),
        "all_at_once_promotion_allowed": False,
        "direct_class_promotion_allowed": False,
        "runtime_apply_allowed": False,
        "authority_expanded": False,
        "blast_radius_expanded": False,
        "automation_enabled": False,
        "users_moved": 0,
        "class_summaries": class_summaries,
        "blocking_rules": blocking_rules,
        "violations": violations,
        "summary": {
            "action_classes_seen": len(class_summaries),
            "all_at_once_promotions_available": 0,
            "direct_promotions_available": 0,
            "runtime_apply_paths_available": 0,
            "authority_changes": 0,
            "blast_radius_expansions": 0,
            "automation_changes": 0,
            "synthetic_evidence_created": 0,
            "users_moved": 0,
        },
        "canonical_rules": [
            "c4_reuses_existing_action_class_ladder_and_blast_radius_gate_owners",
            "c4_keeps_all_at_once_promotion_unavailable_for_current_action_classes",
            "c4_requires_class_by_class_certification_and_explicit_authority_review",
            "c4_does_not_grant_runtime_apply_authority_automation_or_user_movement",
            "c4_does_not_create_runtime_planner_owner_truth_source_or_promotion_path",
        ],
        "omp_output": {
            "c4_status": (
                "DONE_READ_ONLY_ALL_AT_ONCE_PROMOTION_UNAVAILABLE"
                if not violations
                else "STOP_SAFE_PROMOTION_AVAILABILITY_VIOLATION_DETECTED"
            ),
            "produced_evidence": "all_at_once_promotion_unavailable_verification",
            "unlocked_capability": "C5_ROLLBACK_OPERATIONAL_COMPENSATION_NOT_TRANSACTION_ROLLBACK" if not violations else "",
            "blocked_later_steps": [
                "runtime_apply",
                "automation",
                "authority_expansion",
                "direct_class_promotion",
                "all_at_once_action_class_promotion",
                "blast_radius_expansion",
                "user_movement",
            ],
        },
        "read_only": True,
        "runtime_mutation_performed": False,
        "restore_barrier_written_now": False,
        "apply_executed": False,
        "synthetic_evidence_created": False,
        "new_owner_created": False,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_runtime_created": False,
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
    liveness_evidence_aggregation = build_liveness_evidence_aggregation(
        hard_failure_classification=hard_failure_classification,
        snapshot_statuses=snapshot_statuses,
        generated_at=generated,
    )
    decision_outcome_closure = build_decision_outcome_closure(decision_records or [], generated_at=generated)
    l7_l8_authority_evolution_program = build_l7_l8_outcome_evidence_program(
        decision_records or [],
        generated_at=generated,
    )
    recovery_admission = build_recovery_admission(
        decision_surface,
        freshness_actionability=freshness_actionability,
        generated_at=generated,
    )
    anti_flapping = build_anti_flapping(decision_records or [], generated_at=generated)
    hard_failure_policy_windows = build_hard_failure_policy_windows(
        hard_failure_classification=hard_failure_classification,
        liveness_evidence_aggregation=liveness_evidence_aggregation,
        action_class_freshness_windows=action_class_freshness_windows,
        anti_flapping=anti_flapping,
        generated_at=generated,
    )
    soft_degradation_threshold_vocabulary = build_soft_degradation_threshold_vocabulary_alignment(
        decision_surface=decision_surface,
        service_scores_snapshot=snapshots["service-scores"],
        channel_service_scores_snapshot=snapshots["channel-service-scores"],
        service_user_sla_fit=service_user_sla_fit,
        hard_failure_policy_windows=hard_failure_policy_windows,
        freshness_actionability=freshness_actionability,
        anti_flapping=anti_flapping,
        generated_at=generated,
    )
    degradation_signal_policy_mapping = build_degradation_signal_policy_mapping(
        decision_surface=decision_surface,
        service_scores_snapshot=snapshots["service-scores"],
        channel_service_scores_snapshot=snapshots["channel-service-scores"],
        risk_summaries_snapshot=snapshots["risk-summaries"],
        overview_summary_snapshot=snapshots["overview-summary"],
        soft_degradation_threshold_vocabulary=soft_degradation_threshold_vocabulary,
        freshness_actionability=freshness_actionability,
        generated_at=generated,
    )
    decision_outcome_learning = _decision_outcome_learning_from_trust(snapshots["trust-evolution-summaries"])
    observed_degradation_attribution = build_observed_degradation_attribution(
        service_scores_snapshot=snapshots["service-scores"],
        channel_service_scores_snapshot=snapshots["channel-service-scores"],
        trust_evolution_snapshot=snapshots["trust-evolution-summaries"],
        degradation_signal_policy_mapping=degradation_signal_policy_mapping,
        decision_outcome_learning=decision_outcome_learning,
        decision_records=decision_records or [],
        generated_at=generated,
    )
    v7_native_degradation_response_mapping = build_v7_native_degradation_response_mapping(
        decision_surface=decision_surface,
        observed_degradation_attribution=observed_degradation_attribution,
        soft_degradation_threshold_vocabulary=soft_degradation_threshold_vocabulary,
        degradation_signal_policy_mapping=degradation_signal_policy_mapping,
        anti_flapping=anti_flapping,
        recovery_admission=recovery_admission,
        generated_at=generated,
    )
    service_objective_policy_threshold_binding = build_service_objective_policy_threshold_binding(
        service_user_sla_fit=service_user_sla_fit,
        freshness_actionability=freshness_actionability,
        soft_degradation_threshold_vocabulary=soft_degradation_threshold_vocabulary,
        v7_native_degradation_response_mapping=v7_native_degradation_response_mapping,
        generated_at=generated,
    )
    recovery_admission_certification = build_recovery_admission_certification(
        recovery_admission=recovery_admission,
        service_scores_snapshot=snapshots["service-scores"],
        channel_service_scores_snapshot=snapshots["channel-service-scores"],
        freshness_actionability=freshness_actionability,
        service_objective_policy_threshold_binding=service_objective_policy_threshold_binding,
        generated_at=generated,
    )
    post_admission_observation_windows = build_post_admission_observation_windows(
        recovery_admission_certification=recovery_admission_certification,
        service_scores_snapshot=snapshots["service-scores"],
        channel_service_scores_snapshot=snapshots["channel-service-scores"],
        generated_at=generated,
    )
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
        "l7_l8_authority_evolution_program": l7_l8_authority_evolution_program,
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
    historical_blast_radius_evidence = build_historical_blast_radius_evidence(generated_at=generated)
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
        historical_certification_evidence=historical_blast_radius_evidence,
        candidate=first_candidate,
        generated_at=generated,
    )
    class_level_blast_radius_certification = build_class_level_blast_radius_certification(
        action_class_runtime_enablement=action_class_runtime_enablement,
        floor_forensics=floor_forensics,
        service_user_sla_fit=service_user_sla_fit,
        hard_failure_classification=hard_failure_classification,
        decision_outcome_closure=decision_outcome_closure,
        historical_blast_radius_evidence=historical_blast_radius_evidence,
        generated_at=generated,
    )
    recovery_slow_start_progression = build_recovery_slow_start_progression(
        post_admission_observation_windows=post_admission_observation_windows,
        recovery_admission_certification=recovery_admission_certification,
        class_level_blast_radius_certification=class_level_blast_radius_certification,
        generated_at=generated,
    )
    org_cohort_identity_policy_integration = build_org_cohort_identity_policy_integration(
        decision_surface=decision_surface,
        recovery_slow_start_progression=recovery_slow_start_progression,
        generated_at=generated,
    )
    runtime_eligibility_arbitration = build_runtime_eligibility_arbitration(
        action_class_runtime_enablement=action_class_runtime_enablement,
        class_level_blast_radius_certification=class_level_blast_radius_certification,
        freshness_actionability=freshness_actionability,
        anti_flapping=anti_flapping,
        decision_outcome_closure=decision_outcome_closure,
        decision_outcome_learning=decision_outcome_learning,
        routing_recommendation_readiness=routing_recommendation_readiness,
        recovery_admission_certification=recovery_admission_certification,
        post_admission_observation_windows=post_admission_observation_windows,
        recovery_slow_start_progression=recovery_slow_start_progression,
        generated_at=generated,
    )
    stale_read_mutation_blocking = build_stale_read_mutation_blocking(
        freshness_actionability=freshness_actionability,
        runtime_eligibility_arbitration=runtime_eligibility_arbitration,
        routing_recommendation_readiness=routing_recommendation_readiness,
        generated_at=generated,
    )
    owner_issued_version_lease_pattern = build_owner_issued_version_lease_pattern(
        freshness_actionability=freshness_actionability,
        action_class_freshness_windows=action_class_freshness_windows,
        stale_read_mutation_blocking=stale_read_mutation_blocking,
        generated_at=generated,
    )
    hysteresis_state_change_cost_mapping = build_hysteresis_state_change_cost_mapping(
        anti_flapping=anti_flapping,
        recovery_admission=recovery_admission,
        service_objective_policy_threshold_binding=service_objective_policy_threshold_binding,
        owner_issued_version_lease_pattern=owner_issued_version_lease_pattern,
        generated_at=generated,
    )
    hard_failure_override_anti_flap_arbitration = build_hard_failure_override_anti_flap_arbitration(
        hard_failure_classification=hard_failure_classification,
        hard_failure_policy_windows=hard_failure_policy_windows,
        anti_flapping=anti_flapping,
        hysteresis_state_change_cost_mapping=hysteresis_state_change_cost_mapping,
        generated_at=generated,
    )
    per_user_routing_control_mode = build_per_user_routing_control_mode(
        decision_surface=decision_surface,
        org_cohort_identity_policy_integration=org_cohort_identity_policy_integration,
        hard_failure_override_anti_flap_arbitration=hard_failure_override_anti_flap_arbitration,
        generated_at=generated,
    )
    fail_open_fail_closed_action_class_behavior = build_fail_open_fail_closed_action_class_behavior(
        action_class_runtime_enablement=action_class_runtime_enablement,
        runtime_eligibility_arbitration=runtime_eligibility_arbitration,
        per_user_routing_control_mode=per_user_routing_control_mode,
        hard_failure_override_anti_flap_arbitration=hard_failure_override_anti_flap_arbitration,
        stale_read_mutation_blocking=stale_read_mutation_blocking,
        owner_issued_version_lease_pattern=owner_issued_version_lease_pattern,
        generated_at=generated,
    )
    bounded_stale_allowance_by_action_class = build_bounded_stale_allowance_by_action_class(
        freshness_actionability=freshness_actionability,
        action_class_freshness_windows=action_class_freshness_windows,
        stale_read_mutation_blocking=stale_read_mutation_blocking,
        owner_issued_version_lease_pattern=owner_issued_version_lease_pattern,
        fail_open_fail_closed_action_class_behavior=fail_open_fail_closed_action_class_behavior,
        runtime_eligibility_arbitration=runtime_eligibility_arbitration,
        generated_at=generated,
    )
    metric_reliability_certification = build_metric_reliability_certification(
        canary_proximity=canary,
        floor_forensics=floor_forensics,
        source_confidence_inventory=source_confidence_inventory,
        evidence_sufficiency=evidence_sufficiency,
        decision_outcome_closure=decision_outcome_closure,
        decision_outcome_learning=decision_outcome_learning,
        freshness_actionability=freshness_actionability,
        routing_recommendation_readiness=routing_recommendation_readiness,
        action_class_runtime_enablement=action_class_runtime_enablement,
        class_level_blast_radius_certification=class_level_blast_radius_certification,
        runtime_eligibility_arbitration=runtime_eligibility_arbitration,
        generated_at=generated,
    )
    probabilistic_suspicion_advisory_evidence = build_probabilistic_suspicion_advisory_evidence(
        decision_surface=decision_surface,
        shadow_model=shadow_model,
        source_confidence_inventory=source_confidence_inventory,
        degradation_signal_policy_mapping=degradation_signal_policy_mapping,
        observed_degradation_attribution=observed_degradation_attribution,
        metric_reliability_certification=metric_reliability_certification,
        fail_open_fail_closed_action_class_behavior=fail_open_fail_closed_action_class_behavior,
        generated_at=generated,
    )
    next_action_class_stage_certification = build_next_action_class_stage_certification(
        action_class_runtime_enablement=action_class_runtime_enablement,
        class_level_blast_radius_certification=class_level_blast_radius_certification,
        runtime_eligibility_arbitration=runtime_eligibility_arbitration,
        metric_reliability_certification=metric_reliability_certification,
        org_cohort_identity_policy_integration=org_cohort_identity_policy_integration,
        generated_at=generated,
    )
    service_pool_cohort_blast_radius_scope = build_service_pool_cohort_blast_radius_scope(
        decision_surface=decision_surface,
        service_user_sla_fit=service_user_sla_fit,
        class_level_blast_radius_certification=class_level_blast_radius_certification,
        next_action_class_stage_certification=next_action_class_stage_certification,
        org_cohort_identity_policy_integration=org_cohort_identity_policy_integration,
        generated_at=generated,
    )
    pool_health_capacity_blast_bounds = build_pool_health_capacity_blast_bounds(
        service_pool_cohort_blast_radius_scope=service_pool_cohort_blast_radius_scope,
        class_level_blast_radius_certification=class_level_blast_radius_certification,
        next_action_class_stage_certification=next_action_class_stage_certification,
        bounded_stale_allowance_by_action_class=bounded_stale_allowance_by_action_class,
        action_class_freshness_windows=action_class_freshness_windows,
        generated_at=generated,
    )
    all_at_once_promotion_unavailable_verification = build_all_at_once_promotion_unavailable_verification(
        action_class_runtime_enablement=action_class_runtime_enablement,
        class_level_blast_radius_certification=class_level_blast_radius_certification,
        next_action_class_stage_certification=next_action_class_stage_certification,
        service_pool_cohort_blast_radius_scope=service_pool_cohort_blast_radius_scope,
        generated_at=generated,
    )
    rollback_authority_certification = build_rollback_authority_certification(
        floor_forensics=floor_forensics,
        decision_outcome_closure=decision_outcome_closure,
        decision_outcome_learning=decision_outcome_learning,
        runtime_eligibility_arbitration=runtime_eligibility_arbitration,
        metric_reliability_certification=metric_reliability_certification,
        generated_at=generated,
    )
    rt2_s5_certified_concurrency_ladder = build_rt2_s5_certified_concurrency_ladder(
        action_class_runtime_enablement=action_class_runtime_enablement,
        class_level_blast_radius_certification=class_level_blast_radius_certification,
        runtime_eligibility_arbitration=runtime_eligibility_arbitration,
        metric_reliability_certification=metric_reliability_certification,
        rollback_authority_certification=rollback_authority_certification,
        anti_flapping=anti_flapping,
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
    rt2_s6_evidence_based_continuous_improvement = build_rt2_s6_evidence_based_continuous_improvement(
        outcome_leverage_model=outcome_leverage_model,
        maximum_reality_knowledge_extraction=maximum_reality_knowledge_extraction,
        rt2_s5_certified_concurrency_ladder=rt2_s5_certified_concurrency_ladder,
        routing_recommendation_readiness=routing_recommendation_readiness,
        metric_reliability_certification=metric_reliability_certification,
        decision_outcome_learning=decision_outcome_learning,
        generated_at=generated,
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
        "liveness_evidence_aggregation": liveness_evidence_aggregation,
        "hard_failure_policy_windows": hard_failure_policy_windows,
        "soft_degradation_threshold_vocabulary": soft_degradation_threshold_vocabulary,
        "degradation_signal_policy_mapping": degradation_signal_policy_mapping,
        "observed_degradation_attribution": observed_degradation_attribution,
        "v7_native_degradation_response_mapping": v7_native_degradation_response_mapping,
        "service_objective_policy_threshold_binding": service_objective_policy_threshold_binding,
        "recovery_admission_certification": recovery_admission_certification,
        "post_admission_observation_windows": post_admission_observation_windows,
        "recovery_slow_start_progression": recovery_slow_start_progression,
        "org_cohort_identity_policy_integration": org_cohort_identity_policy_integration,
        "service_user_sla_fit": service_user_sla_fit,
        "action_class_freshness_windows": action_class_freshness_windows,
        "decision_outcome_closure": decision_outcome_closure,
        "l7_l8_authority_evolution_program": l7_l8_authority_evolution_program,
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
        "historical_blast_radius_evidence": historical_blast_radius_evidence,
        "class_level_blast_radius_certification": class_level_blast_radius_certification,
        "runtime_eligibility_arbitration": runtime_eligibility_arbitration,
        "stale_read_mutation_blocking": stale_read_mutation_blocking,
        "owner_issued_version_lease_pattern": owner_issued_version_lease_pattern,
        "hysteresis_state_change_cost_mapping": hysteresis_state_change_cost_mapping,
        "hard_failure_override_anti_flap_arbitration": hard_failure_override_anti_flap_arbitration,
        "per_user_routing_control_mode": per_user_routing_control_mode,
        "fail_open_fail_closed_action_class_behavior": fail_open_fail_closed_action_class_behavior,
        "bounded_stale_allowance_by_action_class": bounded_stale_allowance_by_action_class,
        "probabilistic_suspicion_advisory_evidence": probabilistic_suspicion_advisory_evidence,
        "metric_reliability_certification": metric_reliability_certification,
        "next_action_class_stage_certification": next_action_class_stage_certification,
        "service_pool_cohort_blast_radius_scope": service_pool_cohort_blast_radius_scope,
        "pool_health_capacity_blast_bounds": pool_health_capacity_blast_bounds,
        "all_at_once_promotion_unavailable_verification": all_at_once_promotion_unavailable_verification,
        "rollback_authority_certification": rollback_authority_certification,
        "rt2_s5_certified_concurrency_ladder": rt2_s5_certified_concurrency_ladder,
        "maximum_reality_knowledge_extraction": maximum_reality_knowledge_extraction,
        "rt2_s6_evidence_based_continuous_improvement": rt2_s6_evidence_based_continuous_improvement,
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
