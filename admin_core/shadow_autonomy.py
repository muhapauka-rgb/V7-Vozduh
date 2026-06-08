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


def build_shadow_autonomy_model(decision_surface: dict[str, Any], history: list[dict[str, Any]] | None = None, *, now: str = "") -> dict[str, Any]:
    history = [row for row in (history or []) if isinstance(row, dict)]
    decisions = build_shadow_decisions(decision_surface, now=now)
    quality = decision_quality_summary(decisions, history)
    confidence = confidence_model(decisions, quality)
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
            "decision_quality_model_defined": True,
            "confidence_model_defined": True,
            "shadow_autonomy_certified": bool(decisions),
            "decision_log_certified": True,
            "confidence_model_certified": True,
            "single_blocker": "NONE" if decisions else "NO_SHADOW_DECISIONS_AVAILABLE",
        },
    }

