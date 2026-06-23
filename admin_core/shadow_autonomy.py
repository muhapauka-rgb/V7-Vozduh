"""Shadow autonomy decision records and comparison metrics.

This module is pure. It derives shadow decisions from the existing operator
decision surface and computes quality metrics from append-only records provided
by the caller. It does not execute, approve, roll back, move users, or write
runtime state.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any


SCHEMA_VERSION = "v7.shadow-autonomy.v1"
DECISION_RECORD_TYPE = "shadow_decision"
COMPARISON_RECORD_TYPE = "operator_comparison"
COMPARISON_CATEGORIES = {"trust", "service", "capacity", "risk", "manual_preference", "other"}
OBSERVATION_TARGETS = {
    "minimum_window_hours": 24,
    "minimum_decisions": 10,
    "minimum_comparisons": 5,
    "minimum_agreement_rate": 0.75,
    "maximum_override_rate": 0.2,
    "minimum_earned_confidence": 70.0,
}


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


def clip(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _prediction_confidence(prediction: dict[str, Any]) -> float:
    if not isinstance(prediction, dict):
        return 0.0
    confidence = as_float(prediction.get("confidence"), 0.0)
    return confidence * 100.0 if confidence <= 1.0 else confidence


def _decision_confidence(row: dict[str, Any]) -> float:
    confidence = as_float(row.get("confidence"), 0.0)
    if confidence <= 1.0:
        confidence *= 100.0
    inputs = [
        confidence,
        as_float(row.get("trust"), 0.0),
        clip(100.0 - as_float(row.get("risk"), 0.0)),
        _prediction_confidence(row.get("prediction") if isinstance(row.get("prediction"), dict) else {}),
    ]
    return round(clip(sum(inputs) / len(inputs)), 3)


def shadow_decision_record(row: dict[str, Any], *, now: str = "") -> dict[str, Any]:
    ts = now or utc_now()
    user = str(row.get("user") or "")
    current = str(row.get("current_channel") or "")
    target = str(row.get("recommended_channel") or current)
    recommendation = str(row.get("recommendation") or "")
    recommended_action = "MOVE_USER" if recommendation == "move_recommended" and target and target != current else "KEEP_USER"
    prediction = row.get("prediction") if isinstance(row.get("prediction"), dict) else {}
    reason_items = [str(item) for item in (row.get("reasons") or []) if item]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "record_type": DECISION_RECORD_TYPE,
        "timestamp": ts,
        "user": user,
        "current_channel": current,
        "recommended_action": recommended_action,
        "recommended_target": target,
        "reason": "; ".join(reason_items[:4]) or "existing operator decision surface recommendation",
        "trust": as_float(row.get("trust"), 0.0),
        "prediction": prediction,
        "risk": as_float(row.get("risk"), 0.0),
        "confidence": _decision_confidence(row),
        "expected_outcome": "better_route_quality" if recommended_action == "MOVE_USER" else "stay_stable",
        "recommendation_hash": str(row.get("recommendation_hash") or ""),
        "source_hash": str(row.get("source_hash") or ""),
        "blockers": list(row.get("blockers") or []),
        "runtime_mutation_performed": False,
        "execution_allowed_now": False,
        "users_moved": 0,
        "apply_executed": False,
        "autonomy_enabled": False,
    }
    payload["decision_id"] = "shadow_" + stable_hash({
        "user": user,
        "current_channel": current,
        "recommended_action": recommended_action,
        "recommended_target": target,
        "recommendation_hash": payload["recommendation_hash"],
        "source_hash": payload["source_hash"],
    })[:24]
    return payload


def build_shadow_decisions(decision_surface: dict[str, Any], *, now: str = "") -> list[dict[str, Any]]:
    rows = decision_surface.get("users") if isinstance(decision_surface.get("users"), list) else []
    decisions = [shadow_decision_record(row, now=now) for row in rows if isinstance(row, dict)]
    return sorted(decisions, key=lambda row: (row.get("recommended_action") != "MOVE_USER", row.get("user", "")))


def operator_comparison_record(
    decision: dict[str, Any],
    *,
    operator_decision: str,
    category: str = "other",
    reason: str = "",
    actor: str = "operator",
    now: str = "",
) -> dict[str, Any]:
    normalized = str(operator_decision or "").strip().lower()
    if normalized not in {"agree", "disagree", "override"}:
        normalized = "disagree"
    category = str(category or "other").strip().lower()
    if category not in COMPARISON_CATEGORIES:
        category = "other"
    agreed = normalized == "agree"
    record = {
        "schema_version": SCHEMA_VERSION,
        "record_type": COMPARISON_RECORD_TYPE,
        "timestamp": now or utc_now(),
        "decision_id": str(decision.get("decision_id") or ""),
        "user": str(decision.get("user") or ""),
        "recommended_action": str(decision.get("recommended_action") or ""),
        "recommended_target": str(decision.get("recommended_target") or ""),
        "operator_decision": normalized,
        "operator_agreed": agreed,
        "override": normalized == "override",
        "category": category,
        "reason": str(reason or "")[:600],
        "actor": str(actor or "operator"),
        "runtime_mutation_performed": False,
        "execution_allowed_now": False,
        "users_moved": 0,
        "apply_executed": False,
        "autonomy_enabled": False,
    }
    record["comparison_id"] = "shadowcmp_" + stable_hash(record)[:24]
    return record


def _latest_comparisons(history: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for row in history:
        if not isinstance(row, dict) or row.get("record_type") != COMPARISON_RECORD_TYPE:
            continue
        decision_id = str(row.get("decision_id") or "")
        if decision_id:
            latest[decision_id] = row
    return latest


def _parse_ts(value: Any) -> datetime | None:
    if not value:
        return None
    raw = str(value)
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(raw)
    except ValueError:
        return None


def _records_of(history: list[dict[str, Any]], record_type: str) -> list[dict[str, Any]]:
    return [row for row in history if isinstance(row, dict) and row.get("record_type") == record_type]


def decision_quality_summary(decisions: list[dict[str, Any]], history: list[dict[str, Any]]) -> dict[str, Any]:
    comparisons = _latest_comparisons(history)
    compared = [comparisons[row["decision_id"]] for row in decisions if row.get("decision_id") in comparisons]
    total = len(compared)
    agreements = sum(1 for row in compared if row.get("operator_agreed") is True)
    overrides = sum(1 for row in compared if row.get("override") is True)
    confidence_values = [as_float(row.get("confidence"), 0.0) for row in decisions]
    return {
        "schema_version": "v7.shadow-autonomy-quality.v1",
        "decisions_total": len(decisions),
        "comparisons_total": total,
        "agreement_count": agreements,
        "disagreement_count": max(0, total - agreements),
        "override_count": overrides,
        "agreement_rate": round(agreements / total, 4) if total else 0.0,
        "disagreement_rate": round((total - agreements) / total, 4) if total else 0.0,
        "override_rate": round(overrides / total, 4) if total else 0.0,
        "prediction_accuracy": "INSUFFICIENT_OUTCOME_HISTORY",
        "trust_accuracy": round(agreements / total, 4) if total else 0.0,
        "recommendation_accuracy": round((agreements - overrides) / total, 4) if total else 0.0,
        "average_decision_confidence": round(sum(confidence_values) / len(confidence_values), 3) if confidence_values else 0.0,
    }


def confidence_model(decisions: list[dict[str, Any]], quality: dict[str, Any]) -> dict[str, Any]:
    base = as_float(quality.get("average_decision_confidence"), 0.0)
    agreement = as_float(quality.get("agreement_rate"), 0.0) * 100.0
    compared = as_float(quality.get("comparisons_total"), 0.0)
    evidence_weight = min(1.0, compared / 20.0)
    earned = round((base * (1.0 - evidence_weight)) + (agreement * evidence_weight), 3)
    blockers = []
    if compared < 5:
        blockers.append("shadow_comparison_history_below_minimum")
    if earned < 70.0:
        blockers.append("shadow_confidence_below_operator_floor")
    return {
        "schema_version": "v7.shadow-autonomy-confidence.v1",
        "earned_confidence": clip(earned),
        "base_decision_confidence": round(base, 3),
        "operator_agreement_influence": round(agreement, 3),
        "comparison_history_count": int(compared),
        "confidence_earned_by": [
            "operator agreement",
            "correct trust interpretation",
            "successful prediction feedback",
            "recommendation not overridden",
        ],
        "certified": not blockers,
        "blockers": blockers,
    }


def observation_window(decisions: list[dict[str, Any]], history: list[dict[str, Any]]) -> dict[str, Any]:
    decision_history = _records_of(history, DECISION_RECORD_TYPE)
    comparisons = _records_of(history, COMPARISON_RECORD_TYPE)
    timestamps = [
        parsed
        for parsed in (_parse_ts(row.get("timestamp")) for row in decision_history + comparisons)
        if parsed is not None
    ]
    first = min(timestamps).isoformat() if timestamps else ""
    last = max(timestamps).isoformat() if timestamps else ""
    hours = 0.0
    if len(timestamps) >= 2:
        hours = round((max(timestamps) - min(timestamps)).total_seconds() / 3600.0, 3)
    observed_decisions = len({str(row.get("decision_id") or "") for row in decision_history if row.get("decision_id")})
    observed_decisions = max(observed_decisions, len(decisions))
    targets = dict(OBSERVATION_TARGETS)
    return {
        "schema_version": "v7.shadow-observation-window.v1",
        "mode": "production_shadow_evidence_only",
        "window_started_at": first,
        "window_last_seen_at": last,
        "observed_window_hours": hours,
        "minimum_window_hours": targets["minimum_window_hours"],
        "minimum_decisions": targets["minimum_decisions"],
        "minimum_comparisons": targets["minimum_comparisons"],
        "minimum_agreement_rate": targets["minimum_agreement_rate"],
        "maximum_override_rate": targets["maximum_override_rate"],
        "minimum_earned_confidence": targets["minimum_earned_confidence"],
        "decisions_observed": observed_decisions,
        "comparisons_observed": len(comparisons),
        "enough_window": hours >= targets["minimum_window_hours"],
        "enough_decisions": observed_decisions >= targets["minimum_decisions"],
        "enough_comparisons": len(comparisons) >= targets["minimum_comparisons"],
        "autonomy_review_evidence_needed": [
            "real shadow decisions",
            "operator comparisons",
            "low override rate",
            "stable earned confidence",
            "closed apply and rollback loop certification",
        ],
    }


def disagreement_analysis(history: list[dict[str, Any]]) -> dict[str, Any]:
    comparisons = _records_of(history, COMPARISON_RECORD_TYPE)
    disagreements = [
        row
        for row in comparisons
        if row.get("operator_agreed") is not True
    ]
    by_category: dict[str, int] = {category: 0 for category in sorted(COMPARISON_CATEGORIES)}
    for row in disagreements:
        category = str(row.get("category") or "other")
        if category not in by_category:
            category = "other"
        by_category[category] += 1
    primary = "NONE"
    if disagreements:
        primary = max(by_category.items(), key=lambda item: (item[1], item[0]))[0]
    return {
        "schema_version": "v7.shadow-disagreement-analysis.v1",
        "disagreements_total": len(disagreements),
        "by_category": by_category,
        "primary_disagreement_reason": primary,
        "latest_disagreements": disagreements[-20:],
        "classification_complete": True,
    }


def confidence_evolution(decisions: list[dict[str, Any]], history: list[dict[str, Any]], confidence: dict[str, Any]) -> dict[str, Any]:
    decision_history = _records_of(history, DECISION_RECORD_TYPE)
    values = [as_float(row.get("confidence"), 0.0) for row in decision_history if row.get("confidence") is not None]
    values.extend(as_float(row.get("confidence"), 0.0) for row in decisions if row.get("confidence") is not None)
    first = values[0] if values else 0.0
    latest = values[-1] if values else 0.0
    delta = round(latest - first, 3) if values else 0.0
    if not values:
        trend = "INSUFFICIENT_HISTORY"
    elif abs(delta) < 1.0:
        trend = "STABLE"
    elif delta > 0:
        trend = "GROWING"
    else:
        trend = "DECLINING"
    return {
        "schema_version": "v7.shadow-confidence-evolution.v1",
        "samples": len(values),
        "first_confidence": round(first, 3),
        "latest_confidence": round(latest, 3),
        "delta": delta,
        "trend": trend,
        "earned_confidence": confidence.get("earned_confidence", 0.0),
        "reflects_reality": "REQUIRES_OPERATOR_COMPARISONS" if confidence.get("comparison_history_count", 0) < OBSERVATION_TARGETS["minimum_comparisons"] else "OPERATOR_COMPARISON_BACKED",
    }


def explainability_review(decisions: list[dict[str, Any]], history: list[dict[str, Any]]) -> dict[str, Any]:
    comparisons = _records_of(history, COMPARISON_RECORD_TYPE)
    explained_decisions = sum(1 for row in decisions if str(row.get("reason") or "").strip())
    explained_comparisons = sum(1 for row in comparisons if str(row.get("reason") or "").strip())
    return {
        "schema_version": "v7.shadow-explainability-review.v1",
        "shadow_explanations_present": explained_decisions == len(decisions) if decisions else False,
        "shadow_explanations_total": explained_decisions,
        "operator_explanations_total": explained_comparisons,
        "operator_helpfulness": "NOT_ENOUGH_OPERATOR_FEEDBACK" if explained_comparisons < OBSERVATION_TARGETS["minimum_comparisons"] else "OPERATOR_FEEDBACK_PRESENT",
        "understandable_for_operator": explained_decisions > 0,
    }


def operator_behavior(quality: dict[str, Any]) -> dict[str, Any]:
    total = int(as_float(quality.get("comparisons_total"), 0.0))
    agreements = int(as_float(quality.get("agreement_count"), 0.0))
    overrides = int(as_float(quality.get("override_count"), 0.0))
    if total == 0:
        pattern = "NO_OPERATOR_COMPARISONS_YET"
    elif agreements / total >= OBSERVATION_TARGETS["minimum_agreement_rate"]:
        pattern = "MOSTLY_AGREEING"
    elif overrides / total > OBSERVATION_TARGETS["maximum_override_rate"]:
        pattern = "MOSTLY_OVERRIDING"
    else:
        pattern = "MIXED_REVIEW"
    return {
        "schema_version": "v7.shadow-operator-behavior.v1",
        "comparisons_total": total,
        "agreement_count": agreements,
        "override_count": overrides,
        "behavior_pattern": pattern,
        "operators_trusting_recommendations": pattern == "MOSTLY_AGREEING",
        "operators_ignoring_recommendations": total == 0,
    }


def comparison_eligibility(decision: dict[str, Any], latest_comparison: dict[str, Any] | None = None) -> dict[str, Any]:
    decision_id = str(decision.get("decision_id") or "")
    already_reviewed = bool(latest_comparison)
    blockers = []
    if not decision_id:
        blockers.append("decision_id_missing")
    return {
        "schema_version": "v7.shadow-comparison-eligibility.v1",
        "decision_id": decision_id,
        "eligible": bool(decision_id) and not already_reviewed,
        "already_reviewed": already_reviewed,
        "latest_comparison_id": str((latest_comparison or {}).get("comparison_id") or ""),
        "operator_decision": str((latest_comparison or {}).get("operator_decision") or ""),
        "blockers": blockers,
        "requires_real_operator_judgement": True,
        "synthetic_agreement_allowed": False,
        "runtime_mutation_performed": False,
        "users_moved": 0,
        "apply_executed": False,
        "autonomy_enabled": False,
    }


def build_operator_review_packet(decisions: list[dict[str, Any]], history: list[dict[str, Any]]) -> dict[str, Any]:
    comparisons = _latest_comparisons(history)
    items: list[dict[str, Any]] = []
    for decision in decisions:
        if not isinstance(decision, dict):
            continue
        decision_id = str(decision.get("decision_id") or "")
        latest = comparisons.get(decision_id)
        current = str(decision.get("current_channel") or "")
        target = str(decision.get("recommended_target") or "")
        action = str(decision.get("recommended_action") or "")
        items.append({
            "decision_id": decision_id,
            "user": str(decision.get("user") or ""),
            "source_channel": current,
            "target_channel": target,
            "recommendation": action,
            "operator_summary": f"{current} -> {target}" if action == "MOVE_USER" else "keep current channel",
            "confidence": as_float(decision.get("confidence"), 0.0),
            "trust": as_float(decision.get("trust"), 0.0),
            "risk": as_float(decision.get("risk"), 0.0),
            "blockers": list(decision.get("blockers") or []),
            "reason": str(decision.get("reason") or ""),
            "expected_outcome": str(decision.get("expected_outcome") or ""),
            "comparison_eligibility": comparison_eligibility(decision, latest),
        })
    reviewable = [row for row in items if row.get("comparison_eligibility", {}).get("eligible")]
    reviewed = [row for row in items if row.get("comparison_eligibility", {}).get("already_reviewed")]
    return {
        "schema_version": "v7.shadow-operator-review-packet.v1",
        "mode": "operator_review_only",
        "items": items,
        "reviewable_decisions": len(reviewable),
        "reviewed_decisions": len(reviewed),
        "comparison_categories": sorted(COMPARISON_CATEGORIES),
        "allowed_operator_decisions": ["agree", "disagree", "override"],
        "requires_real_operator_judgement": True,
        "synthetic_agreement_allowed": False,
        "runtime_mutation_performed": False,
        "execution_allowed_now": False,
        "users_moved": 0,
        "apply_executed": False,
        "autonomy_enabled": False,
    }


def comparison_growth_projection(base_decision_confidence: float, *, counts: list[int] | None = None, agreement_rates: list[float] | None = None) -> dict[str, Any]:
    counts = counts or [5, 10, 15, 20]
    agreement_rates = agreement_rates or [1.0, 0.9, 0.8, 0.75]
    rows: list[dict[str, Any]] = []
    for count in counts:
        evidence_weight = min(1.0, max(0.0, float(count)) / 20.0)
        for agreement_rate in agreement_rates:
            agreement_percent = clip(float(agreement_rate) * 100.0)
            earned = round((base_decision_confidence * (1.0 - evidence_weight)) + (agreement_percent * evidence_weight), 3)
            rows.append({
                "comparisons": int(count),
                "agreement_rate": round(float(agreement_rate), 4),
                "earned_confidence": clip(earned),
                "minimum_comparisons_met": int(count) >= OBSERVATION_TARGETS["minimum_comparisons"],
                "earned_confidence_floor_met": earned >= OBSERVATION_TARGETS["minimum_earned_confidence"],
                "canary_readiness_impact": "operator_comparison_floor_met" if earned >= OBSERVATION_TARGETS["minimum_earned_confidence"] and int(count) >= OBSERVATION_TARGETS["minimum_comparisons"] else "operator_comparison_evidence_still_needed",
            })
    return {
        "schema_version": "v7.shadow-comparison-growth-projection.v1",
        "formula": "earned = base_decision_confidence*(1-min(comparisons/20,1)) + agreement_percent*min(comparisons/20,1)",
        "base_decision_confidence": round(base_decision_confidence, 3),
        "minimum_comparisons": OBSERVATION_TARGETS["minimum_comparisons"],
        "minimum_earned_confidence": OBSERVATION_TARGETS["minimum_earned_confidence"],
        "rows": rows,
        "synthetic_agreement_created": False,
        "projection_only": True,
    }


def autonomy_evidence_model(quality: dict[str, Any], confidence: dict[str, Any], observation: dict[str, Any]) -> dict[str, Any]:
    agreement_ok = as_float(quality.get("agreement_rate"), 0.0) >= OBSERVATION_TARGETS["minimum_agreement_rate"]
    override_ok = as_float(quality.get("override_rate"), 0.0) <= OBSERVATION_TARGETS["maximum_override_rate"]
    confidence_ok = as_float(confidence.get("earned_confidence"), 0.0) >= OBSERVATION_TARGETS["minimum_earned_confidence"]
    enough = bool(observation.get("enough_decisions") and observation.get("enough_comparisons"))
    return {
        "schema_version": "v7.shadow-autonomy-evidence.v1",
        "decision_count": quality.get("decisions_total", 0),
        "comparison_count": quality.get("comparisons_total", 0),
        "agreement_count": quality.get("agreement_count", 0),
        "override_count": quality.get("override_count", 0),
        "earned_confidence": confidence.get("earned_confidence", 0.0),
        "trust_quality": quality.get("trust_accuracy", 0.0),
        "prediction_quality": quality.get("prediction_accuracy", "INSUFFICIENT_OUTCOME_HISTORY"),
        "recommendation_quality": quality.get("recommendation_accuracy", 0.0),
        "evidence_targets_met": bool(enough and agreement_ok and override_ok and confidence_ok),
        "missing_targets": [
            name
            for name, ok in [
                ("minimum_decisions", observation.get("enough_decisions")),
                ("minimum_comparisons", observation.get("enough_comparisons")),
                ("agreement_rate_floor", agreement_ok),
                ("override_rate_ceiling", override_ok),
                ("earned_confidence_floor", confidence_ok),
            ]
            if not ok
        ],
    }


def autonomy_readiness_review(evidence: dict[str, Any]) -> dict[str, Any]:
    if evidence.get("evidence_targets_met"):
        stage = "APPROVAL_AUTONOMY_REVIEW_READY"
        blocker = "AUTONOMOUS_APPLY_AND_ROLLBACK_LOOP_NOT_CERTIFIED"
    else:
        stage = "SHADOW_ONLY"
        blocker = "SHADOW_OBSERVATION_EVIDENCE_BELOW_MINIMUM"
    return {
        "schema_version": "v7.shadow-autonomy-readiness-review.v1",
        "closest_stage": stage,
        "shadow_only_ready": True,
        "approval_autonomy_review_ready": evidence.get("evidence_targets_met", False),
        "bounded_autonomy_ready": False,
        "production_autonomy_ready": False,
        "single_blocker": blocker,
    }


def autonomy_gap_analysis(readiness: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    gaps = []
    if evidence.get("missing_targets"):
        gaps.extend(evidence["missing_targets"])
    if not readiness.get("bounded_autonomy_ready"):
        gaps.append("rollback")
        gaps.append("execution_confidence")
        gaps.append("governance")
    deduped = []
    for gap in gaps:
        if gap not in deduped:
            deduped.append(gap)
    return {
        "schema_version": "v7.shadow-autonomy-gap-analysis.v1",
        "bounded_autonomy_blocked": True,
        "gap_classes": deduped,
        "single_blocker": readiness.get("single_blocker", "UNKNOWN"),
    }


def build_shadow_autonomy_model(decision_surface: dict[str, Any], history: list[dict[str, Any]] | None = None, *, now: str = "") -> dict[str, Any]:
    history = [row for row in (history or []) if isinstance(row, dict)]
    decisions = build_shadow_decisions(decision_surface, now=now)
    quality = decision_quality_summary(decisions, history)
    confidence = confidence_model(decisions, quality)
    observation = observation_window(decisions, history)
    disagreements = disagreement_analysis(history)
    evolution = confidence_evolution(decisions, history, confidence)
    explainability = explainability_review(decisions, history)
    behavior = operator_behavior(quality)
    review_packet = build_operator_review_packet(decisions, history)
    growth_projection = comparison_growth_projection(as_float(quality.get("average_decision_confidence"), 0.0))
    evidence = autonomy_evidence_model(quality, confidence, observation)
    readiness = autonomy_readiness_review(evidence)
    gaps = autonomy_gap_analysis(readiness, evidence)
    return {
        "schema_version": SCHEMA_VERSION,
        "mode": "shadow_only",
        "read_only": True,
        "preview_only": True,
        "current_decisions": decisions,
        "decision_history": [row for row in history if row.get("record_type") == DECISION_RECORD_TYPE][-50:],
        "comparison_history": [row for row in history if row.get("record_type") == COMPARISON_RECORD_TYPE][-50:],
        "quality": quality,
        "confidence": confidence,
        "observation_window": observation,
        "disagreement_analysis": disagreements,
        "confidence_evolution": evolution,
        "explainability_review": explainability,
        "operator_behavior": behavior,
        "operator_review_packet": review_packet,
        "comparison_growth_projection": growth_projection,
        "autonomy_evidence": evidence,
        "autonomy_readiness": readiness,
        "gap_analysis": gaps,
        "models": {
            "operator_comparison_categories": sorted(COMPARISON_CATEGORIES),
            "decision_quality_metrics": [
                "agreement_rate",
                "disagreement_rate",
                "override_rate",
                "prediction_accuracy",
                "trust_accuracy",
                "recommendation_accuracy",
            ],
        },
        "safety": {
            "execution_allowed_now": False,
            "runtime_mutation_performed": False,
            "users_moved": 0,
            "apply_executed": False,
            "autonomy_enabled": False,
            "second_planner_created": False,
            "second_recommendation_engine_created": False,
        },
        "certification": {
            "shadow_decision_model_defined": True,
            "shadow_decision_log_implemented": True,
            "operator_comparison_model_defined": True,
            "operator_review_packet_defined": True,
            "decision_quality_model_defined": True,
            "confidence_model_defined": True,
            "observation_window_defined": True,
            "autonomy_evidence_model_defined": True,
            "shadow_autonomy_certified": bool(decisions),
            "decision_log_certified": True,
            "confidence_model_certified": bool(confidence.get("certified")),
            "single_blocker": gaps.get("single_blocker") if decisions else "NO_SHADOW_DECISIONS_AVAILABLE",
        },
    }
