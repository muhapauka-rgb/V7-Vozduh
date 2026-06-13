"""Read-only explainability adapters for operator-facing Why Cards."""

from __future__ import annotations

from collections import Counter
from typing import Any

from admin_core.intelligence_platform import authority_boundary, explainability_framework


SERVICE_SCORE_THRESHOLD = 80.0
STABILITY_THRESHOLD = 0.45
RECOMMENDATION_CONFIDENCE_THRESHOLD = 0.60
RECOMMENDATION_IMPROVEMENT_THRESHOLD = 1.0


def _as_float(value: Any, default: float | None = None) -> float | None:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _round(value: Any, digits: int = 3) -> float | None:
    number = _as_float(value)
    return round(number, digits) if number is not None else None


def _ratio(value: Any) -> float | None:
    number = _as_float(value)
    if number is None:
        return None
    if number > 1.0:
        number = number / 100.0
    return round(number, 3)


def _first_reason(row: dict[str, Any]) -> str:
    blockers = [str(item) for item in row.get("blockers") or [] if item]
    if blockers:
        return blockers[0]
    reasons = [str(item) for item in row.get("reasons") or [] if item]
    if reasons:
        text = " ".join(reasons).lower()
        if "sticky" in text:
            return "sticky_keep_current"
        if "current" in text and "best" in text:
            return "current_is_best"
        return reasons[0]
    if row.get("recommendation") == "move_recommended":
        return "better_candidate_found"
    return "current_is_best"


def canonical_metric(
    *,
    status: str,
    reason: str,
    value: Any,
    threshold: Any,
    source: str,
    updated_at: str | None = None,
    confidence: Any = None,
    next_action: str = "none",
) -> dict[str, Any]:
    return {
        "status": status,
        "reason": reason,
        "value": value,
        "threshold": threshold,
        "source": source,
        "updated_at": updated_at or None,
        "confidence": confidence,
        "next_action": next_action,
        "read_only": True,
        "authority": authority_boundary(),
    }


def _freshness_source(snapshot_statuses: dict[str, dict[str, Any]], *names: str) -> dict[str, Any]:
    for name in names:
        status = snapshot_statuses.get(name) or {}
        if status:
            return {
                "source": name,
                "updated_at": status.get("updated_at") or None,
                "confidence": status.get("confidence"),
                "freshness_state": status.get("freshness_state"),
                "path": status.get("path"),
            }
    return {"source": names[0] if names else "operator_decision_surface", "updated_at": None, "confidence": None}


def user_why_card(row: dict[str, Any], snapshot_statuses: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    snapshot_statuses = snapshot_statuses or {}
    source = _freshness_source(snapshot_statuses, "candidate-suitability-summary", "best-available-pool")
    breakdown = row.get("reason_breakdown") if isinstance(row.get("reason_breakdown"), dict) else {}
    recommendation = str(row.get("recommendation") or "keep").upper()
    status = "MOVE_RECOMMENDED" if recommendation == "MOVE_RECOMMENDED" else "KEEP"
    reason = _first_reason(row)
    improvement = _round(row.get("improvement_score"), 3)
    confidence = _ratio(row.get("confidence"))
    service_score = _round(
        breakdown.get("service_suitability", breakdown.get("service_score", breakdown.get("service"))),
        3,
    )
    suitability = _ratio(
        breakdown.get("suitability", breakdown.get("service_suitability", row.get("confidence"))),
    )
    next_action = "review_recommendation" if status == "MOVE_RECOMMENDED" else "none"
    required_to_move = [
        canonical_metric(
            status="REQUIRED",
            reason="score_delta_required",
            value=improvement,
            threshold=RECOMMENDATION_IMPROVEMENT_THRESHOLD,
            source="operator_decision_surface.improvement_score",
            updated_at=source.get("updated_at"),
            confidence=confidence,
            next_action=next_action,
        ),
        canonical_metric(
            status="REQUIRED",
            reason="confidence_floor",
            value=confidence,
            threshold=RECOMMENDATION_CONFIDENCE_THRESHOLD,
            source="recommendation_engine_contract.confidence_floor.operator_visible",
            updated_at=source.get("updated_at"),
            confidence=confidence,
            next_action=next_action,
        ),
    ]
    metrics = [
        canonical_metric(
            status="OK" if service_score is not None and service_score >= SERVICE_SCORE_THRESHOLD else "UNKNOWN" if service_score is None else "REVIEW_REQUIRED",
            reason="service_score",
            value=service_score,
            threshold=SERVICE_SCORE_THRESHOLD,
            source="candidate-suitability-summary.reason_breakdown",
            updated_at=source.get("updated_at"),
            confidence=confidence,
            next_action=next_action,
        ),
        canonical_metric(
            status="OK" if suitability is not None else "UNKNOWN",
            reason="suitability",
            value=suitability,
            threshold=None,
            source="candidate-suitability-summary.reason_breakdown",
            updated_at=source.get("updated_at"),
            confidence=confidence,
            next_action=next_action,
        ),
        canonical_metric(
            status="OK" if confidence is not None and confidence >= RECOMMENDATION_CONFIDENCE_THRESHOLD else "REVIEW_REQUIRED",
            reason="confidence",
            value=confidence,
            threshold=RECOMMENDATION_CONFIDENCE_THRESHOLD,
            source="operator_decision_surface.confidence",
            updated_at=source.get("updated_at"),
            confidence=confidence,
            next_action=next_action,
        ),
        canonical_metric(
            status="OK",
            reason="risk",
            value=_round(row.get("risk"), 3),
            threshold=None,
            source="risk-summaries/operator_decision_surface",
            updated_at=source.get("updated_at"),
            confidence=confidence,
            next_action=next_action,
        ),
        canonical_metric(
            status="OK",
            reason="trust",
            value=_round(row.get("trust"), 3),
            threshold=None,
            source="trust-summaries/operator_decision_surface",
            updated_at=source.get("updated_at"),
            confidence=confidence,
            next_action=next_action,
        ),
    ]
    return {
        "schema_version": "v7.explainability.why-card.user.v1",
        "object_type": "user",
        "object_id": row.get("user") or "",
        "current_channel": row.get("current_channel") or "",
        "recommended_channel": row.get("recommended_channel") or row.get("current_channel") or "",
        "recommended_state": status,
        "reason": reason,
        "metrics": metrics,
        "required_to_move": required_to_move,
        "summary": "Move recommended by existing decision surface." if status == "MOVE_RECOMMENDED" else "No move required.",
        "source": source.get("source") or "operator_decision_surface",
        "updated_at": source.get("updated_at"),
        "confidence": confidence,
        "next_action": next_action,
        "read_only": True,
        "authority": authority_boundary(),
    }


def channel_why_card(row: dict[str, Any], snapshot_statuses: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    snapshot_statuses = snapshot_statuses or {}
    source = _freshness_source(snapshot_statuses, "channel-service-scores", "trust-evolution-summaries")
    label = str(row.get("channel_state_label") or row.get("channel_state") or row.get("state") or "UNKNOWN").upper()
    if label in {"EXCELLENT", "GOOD", "TRUSTED"}:
        status = "ELIGIBLE"
    elif label in {"DEGRADED", "QUARANTINED"}:
        status = "EXCLUDED"
    else:
        status = "REVIEW_REQUIRED"
    users = int(_as_float(row.get("users"), 0) or 0)
    soft_limit = _as_float(row.get("soft_limit"))
    hard_limit = _as_float(row.get("hard_limit", row.get("capacity")))
    headroom = int(max((hard_limit or 0) - users, 0)) if hard_limit is not None else None
    confidence = _ratio(row.get("confidence", source.get("confidence")))
    service_score = _round(row.get("service_score"), 3)
    stability = _ratio(row.get("stability"))
    metrics = [
        canonical_metric(
            status="OK" if service_score is not None and service_score >= SERVICE_SCORE_THRESHOLD else "UNKNOWN" if service_score is None else "REVIEW_REQUIRED",
            reason="service_score",
            value=service_score,
            threshold=SERVICE_SCORE_THRESHOLD,
            source="channel-service-scores",
            updated_at=source.get("updated_at"),
            confidence=confidence,
            next_action=row.get("channel_state_next_step") or "none",
        ),
        canonical_metric(
            status="OK" if stability is not None and stability >= STABILITY_THRESHOLD else "UNKNOWN" if stability is None else "REVIEW_REQUIRED",
            reason="stability",
            value=stability,
            threshold=STABILITY_THRESHOLD,
            source="trust-evolution-summaries",
            updated_at=source.get("updated_at"),
            confidence=confidence,
            next_action=row.get("channel_state_next_step") or "none",
        ),
        canonical_metric(
            status="OK" if hard_limit is None or users <= hard_limit else "BLOCKED",
            reason="capacity",
            value=users,
            threshold=hard_limit,
            source="egress.registry",
            updated_at=None,
            confidence=confidence,
            next_action=row.get("channel_state_next_step") or "none",
        ),
    ]
    return {
        "schema_version": "v7.explainability.why-card.channel.v1",
        "object_type": "channel",
        "object_id": row.get("channel") or "",
        "status": status,
        "reason": row.get("state_reason") or row.get("channel_state_reason_short") or label.lower(),
        "metrics": metrics,
        "users": users,
        "soft_limit": soft_limit,
        "hard_limit": hard_limit,
        "headroom": headroom,
        "source": source.get("source") or "operator_decision_surface",
        "updated_at": source.get("updated_at"),
        "confidence": confidence,
        "next_action": row.get("channel_state_next_step") or "none",
        "read_only": True,
        "authority": authority_boundary(),
    }


def _no_move_reason(row: dict[str, Any]) -> str:
    if row.get("recommendation") == "move_recommended":
        return "move_recommended"
    text = " ".join(str(item) for item in row.get("reasons") or []).lower()
    blockers = " ".join(str(item) for item in row.get("blockers") or []).lower()
    combined = f"{text} {blockers}"
    if "capacity" in combined or "hard_limit" in combined:
        return "blocked_by_capacity"
    if "service" in combined or "matrix" in combined:
        return "blocked_by_service"
    if "stability" in combined or "mbps" in combined:
        return "blocked_by_stability"
    if "governance" in combined or "restore" in combined or "snapshot" in combined:
        return "blocked_by_governance"
    if "reserve" in combined or "canary" in combined:
        return "blocked_by_reserve"
    if "sticky" in combined:
        return "sticky_keep_current"
    return "current_is_best"


def planner_why_card(
    user_rows: list[dict[str, Any]],
    batch_preview: dict[str, Any],
    snapshot_statuses: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    snapshot_statuses = snapshot_statuses or {}
    source = _freshness_source(snapshot_statuses, "best-available-pool", "candidate-suitability-summary")
    counts = Counter(_no_move_reason(row) for row in user_rows if row.get("recommendation") != "move_recommended")
    moves = len((batch_preview or {}).get("users_to_move") or [])
    for key in (
        "current_is_best",
        "sticky_keep_current",
        "blocked_by_capacity",
        "blocked_by_service",
        "blocked_by_stability",
        "blocked_by_governance",
        "blocked_by_reserve",
    ):
        counts.setdefault(key, 0)
    status = "NO_MOVES_REQUIRED" if moves == 0 else "MOVES_AVAILABLE"
    return {
        "schema_version": "v7.explainability.why-card.planner.v1",
        "object_type": "planner",
        "object_id": "autoswitch",
        "status": status,
        "reason": "no_moves_required" if moves == 0 else "candidate_moves_available",
        "candidate_moves_total": moves,
        "reason_counts": dict(counts),
        "summary": "No moves required." if moves == 0 else f"{moves} move candidates available.",
        "metrics": [
            canonical_metric(
                status=status,
                reason="candidate_moves_total",
                value=moves,
                threshold=1,
                source="operator_decision_surface.batch_preview",
                updated_at=source.get("updated_at"),
                confidence=source.get("confidence"),
                next_action="none" if moves == 0 else "review_batch_preview",
            )
        ],
        "source": source.get("source") or "operator_decision_surface",
        "updated_at": source.get("updated_at"),
        "confidence": source.get("confidence"),
        "next_action": "none" if moves == 0 else "review_batch_preview",
        "read_only": True,
        "authority": authority_boundary(),
    }


def build_why_cards(
    *,
    users: list[dict[str, Any]],
    channels: list[dict[str, Any]],
    batch_preview: dict[str, Any],
    snapshot_statuses: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    user_cards = [user_why_card(row, snapshot_statuses) for row in users]
    channel_cards = [channel_why_card(row, snapshot_statuses) for row in channels]
    planner_card = planner_why_card(users, batch_preview, snapshot_statuses)
    return {
        "schema_version": "v7.explainability.why-cards.v1",
        "canonical_shape": explainability_framework(),
        "users": user_cards,
        "users_by_ip": {row["object_id"]: row for row in user_cards if row.get("object_id")},
        "channels": channel_cards,
        "channels_by_id": {row["object_id"]: row for row in channel_cards if row.get("object_id")},
        "planner": planner_card,
        "read_only": True,
        "new_truth_source_created": False,
        "new_planner_created": False,
        "new_governance_created": False,
        "authority": authority_boundary(),
    }
