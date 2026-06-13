"""Read-only operator decision surface derived from existing V7 truth.

This module does not plan, approve, execute, roll back, or write runtime state.
It only turns existing registries and intelligence snapshots into UI-safe
operator rows.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from admin_core.explainability_adapter import build_why_cards
from admin_core.intelligence_snapshots import read_snapshot_bundle


DECISION_SNAPSHOT_FAMILIES = [
    "service-scores",
    "channel-service-scores",
    "risk-summaries",
    "trust-summaries",
    "blast-radius-summaries",
    "candidate-suitability-summary",
    "best-available-pool",
    "prediction-summaries",
    "trust-evolution-summaries",
    "overview-summary",
]


SERVICE_DISPLAY = {
    "telegram": "Telegram",
    "youtube": "YouTube",
    "instagram": "Instagram",
    "chatgpt": "ChatGPT",
    "openai": "ChatGPT",
    "openai_auth": "ChatGPT",
}


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if number != number:
        return default
    return number


def _clip(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows = payload.get("items")
    if isinstance(rows, list):
        return [row for row in rows if isinstance(row, dict)]
    if isinstance(rows, dict):
        return [row for row in rows.values() if isinstance(row, dict)]
    summary = payload.get("summary")
    return [summary] if isinstance(summary, dict) else []


def _snapshot_payloads(snapshot_results: dict[str, Any]) -> dict[str, dict[str, Any]]:
    payloads: dict[str, dict[str, Any]] = {}
    for name, result in (snapshot_results or {}).items():
        payload = getattr(result, "payload", {}) or {}
        payloads[name] = payload if isinstance(payload, dict) else {}
    return payloads


def _snapshot_statuses(snapshot_results: dict[str, Any]) -> dict[str, dict[str, Any]]:
    statuses: dict[str, dict[str, Any]] = {}
    for name, result in (snapshot_results or {}).items():
        validation = getattr(result, "validation", None)
        errors = list(getattr(validation, "errors", []) or [])
        warnings = list(getattr(validation, "warnings", []) or [])
        exists = bool(getattr(result, "exists", False))
        freshness = str(getattr(result, "freshness_state", "UNKNOWN") or "UNKNOWN")
        runtime_behavior = str(getattr(result, "runtime_behavior", "STOP") or "STOP")
        stop_required = bool(getattr(result, "stop_required", True))
        validation_ok = bool(getattr(validation, "ok", False))
        if not exists:
            status = "MISSING"
        elif errors or not validation_ok:
            status = "INVALID"
        elif stop_required:
            status = "STOP"
        elif freshness == "FRESH" and runtime_behavior == "ALLOW":
            status = "OK"
        elif runtime_behavior in {"WARN", "IGNORE"}:
            status = runtime_behavior
        else:
            status = freshness
        payload = getattr(result, "payload", {}) or {}
        source_hashes = payload.get("source_hashes") if isinstance(payload, dict) else {}
        statuses[name] = {
            "status": status,
            "exists": exists,
            "validation_ok": validation_ok,
            "freshness_state": freshness,
            "confidence": getattr(result, "confidence", 0.0),
            "runtime_behavior": runtime_behavior,
            "stop_required": stop_required,
            "path": getattr(result, "path", ""),
            "errors": errors,
            "validation_errors": errors,
            "warnings": warnings,
            "validation_warnings": warnings,
            "source_hashes": dict(source_hashes) if isinstance(source_hashes, dict) else {},
        }
    return statuses


def request_decision_snapshot(
    *,
    snapshot_root: Path | str,
    users: list[dict[str, Any]],
    egress: list[dict[str, Any]],
    runtime_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Load all read-only inputs once for a single admin request."""
    snapshot_results = read_snapshot_bundle(Path(snapshot_root), DECISION_SNAPSHOT_FAMILIES)
    return {
        "users": list(users or []),
        "egress": list(egress or []),
        "runtime_state": runtime_state if isinstance(runtime_state, dict) else {},
        "snapshots": _snapshot_payloads(snapshot_results),
        "snapshot_statuses": _snapshot_statuses(snapshot_results),
    }


def _by_user(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        user = str(row.get("user") or row.get("ip") or row.get("address") or "")
        if user:
            out[user] = row
    return out


def _by_channel(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        channel = str(row.get("channel") or row.get("egress") or row.get("id") or row.get("target") or "")
        if channel:
            out[channel] = row
    return out


def _candidate_channel(row: dict[str, Any]) -> str:
    return str(row.get("channel") or row.get("egress") or row.get("target") or "")


def _candidate_score(row: dict[str, Any]) -> float:
    return _as_float(
        row.get("suitability_score", row.get("score", row.get("adjusted_score", row.get("confidence", 0.0)))),
        0.0,
    )


def _best_candidate(best_pool_row: dict[str, Any], candidate_row: dict[str, Any]) -> dict[str, Any]:
    pool = [row for row in (best_pool_row.get("pool") or []) if isinstance(row, dict)]
    if pool:
        return sorted(pool, key=lambda row: (-_candidate_score(row), _candidate_channel(row)))[0]
    candidates = [row for row in (candidate_row.get("candidates") or []) if isinstance(row, dict)]
    if candidates:
        return sorted(candidates, key=lambda row: (-_candidate_score(row), _candidate_channel(row)))[0]
    return {}


def _current_candidate(channel: str, best_pool_row: dict[str, Any], candidate_row: dict[str, Any]) -> dict[str, Any]:
    rows = list(best_pool_row.get("pool") or []) + list(candidate_row.get("candidates") or [])
    return next((row for row in rows if isinstance(row, dict) and _candidate_channel(row) == channel), {})


def _reason_breakdown(candidate: dict[str, Any]) -> dict[str, Any]:
    breakdown = candidate.get("reason_breakdown")
    if isinstance(breakdown, dict):
        return breakdown
    components = candidate.get("components")
    return components if isinstance(components, dict) else {}


def _reason_text(candidate: dict[str, Any], current: str, recommended: str) -> list[str]:
    raw = []
    for key in ("reasons", "explainability", "why"):
        value = candidate.get(key)
        if isinstance(value, list):
            raw.extend(str(item) for item in value if item)
        elif value:
            raw.append(str(value))
    if recommended and current and recommended != current:
        raw.insert(0, "best available channel has higher advisory suitability")
    return list(dict.fromkeys(raw))[:8]


def _source_hash(snapshots: dict[str, dict[str, Any]], *families: str) -> str:
    data = {family: (snapshots.get(family, {}).get("source_hashes") or {}) for family in families}
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=True).encode("utf-8")).hexdigest()[:16]


def recommendation_fingerprint(user: str, current: str, recommended: str, source_hash: str) -> str:
    raw = json.dumps(
        {"user": user, "current": current, "recommended": recommended, "source_hash": source_hash},
        sort_keys=True,
        ensure_ascii=True,
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]


def _prediction_summary_for(channel: str, snapshots: dict[str, dict[str, Any]]) -> dict[str, Any]:
    prediction = _items(snapshots.get("prediction-summaries", {}))
    summary = prediction[0] if prediction else {}
    forecasts = list(summary.get("channel_forecasts") or []) + list(summary.get("service_forecasts") or [])
    channel_rows = [
        row for row in forecasts
        if isinstance(row, dict) and str(row.get("channel") or row.get("egress") or row.get("target") or "") == channel
    ]
    if channel_rows:
        confidence = sum(_as_float(row.get("confidence"), 0.0) for row in channel_rows) / len(channel_rows)
        return {
            "available": True,
            "confidence": round(confidence, 3),
            "summary": channel_rows[0].get("summary") or channel_rows[0].get("prediction") or "prediction evidence available",
        }
    return {"available": bool(summary), "confidence": _as_float(summary.get("confidence"), 0.0), "summary": "general prediction evidence"}


def _trust_evolution_advice(snapshots: dict[str, dict[str, Any]]) -> dict[str, Any]:
    trust_evolution = _items(snapshots.get("trust-evolution-summaries", {}))
    summary = trust_evolution[0] if trust_evolution else {}
    confidence = summary.get("confidence_summary") if isinstance(summary.get("confidence_summary"), dict) else {}
    readiness = summary.get("autonomy_readiness") if isinstance(summary.get("autonomy_readiness"), dict) else {}
    mapper_counts = summary.get("outcome_mapper_counts") if isinstance(summary.get("outcome_mapper_counts"), dict) else {}
    rollback = summary.get("rollback_intelligence") if isinstance(summary.get("rollback_intelligence"), dict) else {}
    bridge = summary.get("governed_to_autonomy_trust_bridge") if isinstance(summary.get("governed_to_autonomy_trust_bridge"), dict) else {}
    return {
        "schema_version": "v7.operator-decision-surface.trust-evolution-advice.v1",
        "mode": "snapshot_backed_outcome_evidence_only",
        "available": bool(summary),
        "overall_confidence": round(_as_float(summary.get("overall_confidence"), 0.0), 3),
        "decision_confidence": round(_as_float(confidence.get("decision_confidence"), 0.0), 3),
        "prediction_confidence": round(_as_float(confidence.get("prediction_confidence"), 0.0), 3),
        "service_confidence": round(_as_float(confidence.get("service_confidence"), 0.0), 3),
        "suitability_confidence": round(_as_float(confidence.get("suitability_confidence"), 0.0), 3),
        "rollback_confidence": round(_as_float(confidence.get("rollback_confidence"), 0.0), 3),
        "blast_radius_confidence": round(_as_float(confidence.get("blast_radius_confidence"), 0.0), 3),
        "live_calibrated": bool(confidence.get("live_calibrated")),
        "autonomy_readiness": readiness.get("current_level", "NOT_READY"),
        "candidate_outcomes_count": int(_as_float(mapper_counts.get("candidate_outcomes_count"), 0.0)),
        "prediction_actuals_count": int(_as_float(mapper_counts.get("prediction_actuals_count"), 0.0)),
        "service_actuals_count": int(_as_float(mapper_counts.get("service_actuals_count"), 0.0)),
        "rollback_validation_status": rollback.get("validation_status", "UNKNOWN"),
        "governed_to_autonomy_trust_bridge": bridge,
        "governed_evidence_score": round(_as_float(bridge.get("governed_execution_evidence_score"), 0.0), 3),
        "inherited_execution_trust": round(_as_float(bridge.get("inherited_execution_trust"), 0.0), 3),
        "autonomy_specific_gap_score": round(_as_float(bridge.get("autonomy_specific_gap_score"), 0.0), 3),
        "autonomy_boundary_cap": bridge.get("autonomy_boundary_cap", "SHADOW_READY"),
        "approval_autonomy_review_ready": bool(bridge.get("approval_autonomy_review_ready")),
        "bounded_autonomy_blockers": list(bridge.get("bounded_autonomy_blockers") or []),
        "operator_summary_ru": bridge.get("operator_summary_ru", ""),
        "runtime_decision_authority": "none_evidence_only",
        "planner_decision_owner": "tools/v7-users-autoswitch",
        "execution_authority": "none",
        "selected_moves_write_authority": "none",
        "autonomy_enabled": False,
    }


def _global_metric(snapshots: dict[str, dict[str, Any]], family: str, key: str, default: float = 0.0) -> float:
    rows = _items(snapshots.get(family, {}))
    row = rows[0] if rows else {}
    return _as_float(row.get(key, row.get("score", row.get("confidence", default))), default)


def _service_scores_for(channel: str, snapshots: dict[str, dict[str, Any]]) -> dict[str, str]:
    row = _by_channel(_items(snapshots.get("channel-service-scores", {}))).get(channel, {})
    services = row.get("services") or row.get("service_scores") or row.get("scores") or {}
    result: dict[str, str] = {}
    if isinstance(services, dict):
        for service_key, display in SERVICE_DISPLAY.items():
            service_row = services.get(service_key, {})
            if isinstance(service_row, dict):
                ok = service_row.get("ok")
                status = str(service_row.get("status") or service_row.get("state") or "")
                score = _as_float(service_row.get("score"), 0.0)
                ready = ok is True or status.upper() == "OK" or score >= 70.0
            else:
                ready = _as_float(service_row, 0.0) >= 70.0 if service_row != "" else False
            result[display] = "OK" if ready else "unknown"
    return result


CHANNEL_STATE_LABELS = {
    "NEW": "NEW",
    "TRUSTED": "TRUSTED",
    "WATCH": "WATCH",
    "DEGRADED": "DEGRADED",
    "RECOVERING": "RECOVERING",
    "QUARANTINED": "QUARANTINED",
}

CHANNEL_STATE_COPY = {
    "NEW": {
        "reason": "Мало успешной истории.",
        "explanation": "Канал выглядит новым для модели доверия. Текущие проверки могут быть нормальными, но успешных governed-исходов ещё мало.",
        "next_step": "Наблюдать и дождаться свежих успешных исходов.",
        "safe_now": "Только с вниманием оператора.",
        "recovery_path": "После успешных наблюдений канал перейдёт в WATCH или TRUSTED.",
        "blocked_action_summary": "Нельзя расширять нагрузку без review.",
    },
    "TRUSTED": {
        "reason": "Проверки и исходы хорошие.",
        "explanation": "Канал недавно работал стабильно, сервисы здоровы, governed-история положительная.",
        "next_step": "Оставить обычный мониторинг.",
        "safe_now": "Да, в пределах planner/governance.",
        "recovery_path": "Восстановление не требуется.",
        "blocked_action_summary": "Прямой обход planner/governance всё равно запрещён.",
    },
    "WATCH": {
        "reason": "Работает, но истории мало.",
        "explanation": "Канал сейчас выглядит рабочим, но успешных исходов пока недостаточно для статуса TRUSTED.",
        "next_step": "Держать под наблюдением 24-72 часа или до успешного feedback.",
        "safe_now": "Обычно да, но с вниманием оператора.",
        "recovery_path": "После подтверждённых успехов перейдёт в TRUSTED.",
        "blocked_action_summary": "Массовое расширение требует review.",
    },
    "DEGRADED": {
        "reason": "Качество или сервисы просели.",
        "explanation": "У канала есть текущие проблемы качества или обязательных сервисов. Нельзя считать его здоровым, пока проверки не восстановятся.",
        "next_step": "Обновить проверки сервисов и качества.",
        "safe_now": "Нет, не для обычной маршрутизации без review.",
        "recovery_path": "После стабильных проверок перейдёт в RECOVERING или WATCH.",
        "blocked_action_summary": "Нельзя выбирать как обычную цель без operator review.",
    },
    "RECOVERING": {
        "reason": "Канал восстанавливается.",
        "explanation": "Раньше были плохие сигналы, но свежие проверки лучше. Модель ждёт чистые наблюдения перед возвратом доверия.",
        "next_step": "Дождаться 24-72 часов стабильности или двух успешных наблюдений.",
        "safe_now": "Только через operator review.",
        "recovery_path": "После подтверждения вернётся в WATCH или TRUSTED.",
        "blocked_action_summary": "Нельзя расширять нагрузку автоматически.",
    },
    "QUARANTINED": {
        "reason": "Жёсткий негатив или провал сервисов.",
        "explanation": "Канал исключён из нормального доверия: есть повторные сбои, rollback-проблема, отсутствующие обязательные сервисы или очень низкое качество.",
        "next_step": "Починить причину, обновить проверки и дождаться recovery evidence.",
        "safe_now": "Нет.",
        "recovery_path": "Сначала устранить причину, затем RECOVERING, потом WATCH/TRUSTED.",
        "blocked_action_summary": "Нельзя выбирать как обычную цель; только emergency/rollback review.",
    },
}

CTR_REVIEW_MATRIX = {
    "TRUSTED": {
        "review_required": False,
        "review_reason": "Review не требуется.",
        "review_category": "normal",
        "review_severity": "info",
        "review_recommendation": "Можно продолжать штатный review без дополнительных CTR условий.",
        "review_warning": "Прямой обход planner/governance всё равно запрещён.",
        "next_action": "Продолжить штатный путь approval packet.",
        "emergency_only": False,
    },
    "WATCH": {
        "review_required": True,
        "review_reason": "Канал работает, но истории пока мало.",
        "review_category": "expansion_review",
        "review_severity": "low",
        "review_recommendation": "Проверь свежие сигналы перед расширением.",
        "review_warning": "Не расширять нагрузку вслепую.",
        "next_action": "Открыть packet preview и проверить свежие доказательства.",
        "emergency_only": False,
    },
    "NEW": {
        "review_required": True,
        "review_reason": "Недостаточно успешной истории.",
        "review_category": "new_channel_review",
        "review_severity": "medium",
        "review_recommendation": "Использовать только после явного review.",
        "review_warning": "Новый канал нельзя расширять автоматически.",
        "next_action": "Проверить сервисы, доверие и recovery path.",
        "emergency_only": False,
    },
    "RECOVERING": {
        "review_required": True,
        "review_reason": "Канал ещё восстанавливается.",
        "review_category": "recovery_review",
        "review_severity": "medium",
        "review_recommendation": "Дождаться стабильности или подтвердить review.",
        "review_warning": "Не расширять нагрузку автоматически.",
        "next_action": "Проверить recovery state и последние успешные наблюдения.",
        "emergency_only": False,
    },
    "DEGRADED": {
        "review_required": True,
        "review_reason": "Есть просадка качества или сервисов.",
        "review_category": "degraded_channel_review",
        "review_severity": "high",
        "review_recommendation": "Не использовать как обычную цель без review.",
        "review_warning": "Сначала проверить причину деградации.",
        "next_action": "Обновить проверки и подтвердить, что риск понятен.",
        "emergency_only": False,
    },
    "QUARANTINED": {
        "review_required": True,
        "review_reason": "Канал в карантине.",
        "review_category": "emergency_only_review",
        "review_severity": "critical",
        "review_recommendation": "Только emergency или rollback review.",
        "review_warning": "Нельзя использовать как обычную цель.",
        "next_action": "Починить причину и пройти recovery path.",
        "emergency_only": True,
    },
    "UNKNOWN": {
        "review_required": True,
        "review_reason": "CTR состояние неизвестно.",
        "review_category": "unknown_ctr_review",
        "review_severity": "medium",
        "review_recommendation": "Проверить свежесть snapshot.",
        "review_warning": "Не принимать решение без понятных доказательств.",
        "next_action": "Обновить intelligence snapshots.",
        "emergency_only": False,
    },
}


def ctr_review_semantics(state: str) -> dict[str, Any]:
    normalized = str(state or "UNKNOWN").upper()
    return dict(CTR_REVIEW_MATRIX.get(normalized) or CTR_REVIEW_MATRIX["UNKNOWN"])


def _channel_trust_rows(snapshots: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for item in _items(snapshots.get("trust-evolution-summaries", {})):
        model = item.get("channel_trust_recovery") if isinstance(item.get("channel_trust_recovery"), dict) else {}
        for row in model.get("channels") or []:
            if not isinstance(row, dict):
                continue
            channel = str(row.get("channel") or "")
            if channel:
                rows[channel] = row
    return rows


def _channel_state_from_trust_model(channel: str, snapshots: dict[str, dict[str, Any]]) -> dict[str, Any]:
    row = _channel_trust_rows(snapshots).get(channel, {})
    lifecycle = str(row.get("lifecycle") or "").upper()
    if lifecycle not in CHANNEL_STATE_COPY:
        return {}
    copy = CHANNEL_STATE_COPY[lifecycle]
    feedback = row.get("feedback") if isinstance(row.get("feedback"), dict) else {}
    recovery = row.get("recovery") if isinstance(row.get("recovery"), dict) else {}
    return {
        "channel_state": lifecycle,
        "channel_state_label": CHANNEL_STATE_LABELS[lifecycle],
        "channel_state_reason_short": copy["reason"],
        "channel_state_explanation": copy["explanation"],
        "channel_state_next_step": copy["next_step"],
        "channel_state_safe_now": copy["safe_now"],
        "channel_state_recovery_path": copy["recovery_path"],
        "channel_state_blocked_action_summary": copy["blocked_action_summary"],
        "channel_state_source": "trust-evolution-summaries.channel_trust_recovery",
        "channel_state_policy": {
            "maximum_practical_trust_window_days": 7,
            "current_health_window": "5-15 minutes",
            "recent_stability_window": "6-24 hours",
            "initial_recovery_window": "24-72 hours",
        },
        "channel_state_evidence_summary": {
            "current_service_score": row.get("current_service_score"),
            "trust_score": row.get("trust_score"),
            "confidence": row.get("confidence"),
            "successes": feedback.get("successes", 0),
            "failures": feedback.get("failures", 0),
            "rollback_successes": feedback.get("rollback_successes", 0),
            "rollback_failures": feedback.get("rollback_failures", 0),
            "recovery_state": recovery.get("state", ""),
        },
        "channel_state_raw_reason": row.get("lifecycle_reason", ""),
    }


def _ctr_governance_evidence(channel: str, snapshots: dict[str, dict[str, Any]]) -> dict[str, Any]:
    state_payload = _channel_state_from_trust_model(channel, snapshots)
    state = str(state_payload.get("channel_state") or "UNKNOWN").upper()
    review = ctr_review_semantics(state)
    evidence = state_payload.get("channel_state_evidence_summary", {})
    return {
        "schema_version": "v7.ctr.governance-evidence.v1",
        "channel": channel,
        "state": state,
        "reason": state_payload.get("channel_state_reason_short", "Состояние CTR неизвестно."),
        "confidence": evidence.get("confidence", 0),
        "recovery_state": evidence.get("recovery_state", ""),
        "recovery_path": state_payload.get("channel_state_recovery_path", "Нужны свежие проверки и успешные исходы."),
        "evidence_summary": evidence,
        "blocked_actions": state_payload.get("channel_state_blocked_action_summary", "Прямой обход planner/governance запрещён."),
        "recommended_action": state_payload.get("channel_state_next_step", "Проверить свежие доказательства."),
        "review_required": bool(review["review_required"]),
        "review_required_reason": "ctr_state_requires_operator_review" if review["review_required"] else "NONE",
        "review_reason": review["review_reason"],
        "review_category": review["review_category"],
        "review_severity": review["review_severity"],
        "review_recommendation": review["review_recommendation"],
        "review_warning": review["review_warning"],
        "review_next_action": review["next_action"],
        "emergency_only": bool(review["emergency_only"]),
        "packet_preview": {
            "ctr_state": state,
            "ctr_confidence": evidence.get("confidence", 0),
            "ctr_review_status": "REVIEW_REQUIRED" if review["review_required"] else "NO_EXTRA_REVIEW",
            "ctr_review_reason": review["review_reason"],
            "ctr_recovery_state": evidence.get("recovery_state", ""),
            "ctr_recovery_path": state_payload.get("channel_state_recovery_path", ""),
            "ctr_blocked_actions": state_payload.get("channel_state_blocked_action_summary", ""),
            "ctr_recommended_action": review["review_recommendation"],
            "emergency_only": bool(review["emergency_only"]),
        },
        "approval_authority": "none",
        "denial_authority": "none",
        "runtime_mutation_performed": False,
    }


def _legacy_channel_state(channel: str, row: dict[str, Any], snapshots: dict[str, dict[str, Any]], users_count: int) -> dict[str, Any]:
    state, why = _channel_state(channel, row, snapshots, users_count)
    normalized = {
        "Excellent": "TRUSTED",
        "Good": "WATCH",
        "Warning": "NEW",
        "Degraded": "DEGRADED",
    }.get(state, "NEW")
    copy = CHANNEL_STATE_COPY[normalized]
    return {
        "channel_state": normalized,
        "channel_state_label": normalized,
        "channel_state_reason_short": copy["reason"],
        "channel_state_explanation": copy["explanation"],
        "channel_state_next_step": copy["next_step"],
        "channel_state_safe_now": copy["safe_now"],
        "channel_state_recovery_path": copy["recovery_path"],
        "channel_state_blocked_action_summary": copy["blocked_action_summary"],
        "channel_state_source": "legacy_operator_decision_surface_fallback",
        "channel_state_evidence_summary": {},
        "channel_state_raw_reason": why,
    }


def build_user_decision_rows(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    users = snapshot.get("users") or []
    snapshots = snapshot.get("snapshots") or {}
    statuses = snapshot.get("snapshot_statuses") or {}
    best_by_user = _by_user(_items(snapshots.get("best-available-pool", {})))
    candidates_by_user = _by_user(_items(snapshots.get("candidate-suitability-summary", {})))
    source = _source_hash(snapshots, "best-available-pool", "candidate-suitability-summary", "prediction-summaries")
    rows: list[dict[str, Any]] = []
    for user in users:
        ip = str(user.get("ip") or user.get("user") or "")
        if not ip:
            continue
        current = str(user.get("current") or user.get("current_channel") or "")
        best_row = best_by_user.get(ip, {})
        candidate_row = candidates_by_user.get(ip, {})
        best = _best_candidate(best_row, candidate_row)
        recommended = _candidate_channel(best) or current
        current_row = _current_candidate(current, best_row, candidate_row)
        best_score = _candidate_score(best)
        current_score = _candidate_score(current_row)
        ctr_evidence = _ctr_governance_evidence(recommended or current, snapshots)
        improvement = round(max(0.0, best_score - current_score), 3)
        confidence = _clip(_as_float(best.get("confidence"), best_score))
        breakdown = _reason_breakdown(best)
        recommendation = "move_recommended" if recommended and current and recommended != current and improvement >= 1.0 else "keep"
        stale = [
            name for name, status in statuses.items()
            if name in {"best-available-pool", "candidate-suitability-summary"} and status.get("freshness_state") in {"UNKNOWN", "EXPIRED"}
        ]
        blockers = []
        if not best:
            blockers.append("best_candidate_missing")
        blockers.extend(f"{name}_not_fresh" for name in stale)
        fingerprint = recommendation_fingerprint(ip, current, recommended, source)
        rows.append({
            "user": ip,
            "current_channel": current,
            "recommended_channel": recommended or current,
            "recommendation": recommendation,
            "operator_state": "Recommendation" if recommendation == "move_recommended" else ("Warning" if blockers else "OK"),
            "highlight": recommendation == "move_recommended",
            "confidence": round(confidence, 3),
            "expected_improvement": "HIGH" if improvement >= 20 else "MEDIUM" if improvement >= 10 else "LOW",
            "improvement_score": improvement,
            "risk": round(_as_float(breakdown.get("risk_penalty", breakdown.get("risk", _global_metric(snapshots, "risk-summaries", "risk_score")))), 3),
            "trust": round(_as_float(breakdown.get("trust", breakdown.get("execution_trust", _global_metric(snapshots, "trust-summaries", "trust_score")))), 3),
            "prediction": _prediction_summary_for(recommended or current, snapshots),
            "reasons": _reason_text(best, current, recommended),
            "reason_breakdown": breakdown,
            "recommendation_hash": fingerprint,
            "source_hash": source,
            "blockers": sorted(set(blockers)),
            "ctr_governance_evidence": ctr_evidence,
            "review_required": bool(ctr_evidence.get("review_required")),
            "review_required_reasons": [ctr_evidence["review_required_reason"]] if ctr_evidence.get("review_required") else [],
            "review_reason": ctr_evidence.get("review_reason", ""),
            "review_category": ctr_evidence.get("review_category", ""),
            "review_severity": ctr_evidence.get("review_severity", ""),
            "review_recommendation": ctr_evidence.get("review_recommendation", ""),
            "review_warning": ctr_evidence.get("review_warning", ""),
            "review_next_action": ctr_evidence.get("review_next_action", ""),
            "emergency_only": bool(ctr_evidence.get("emergency_only")),
            "action_chain": ["recommendation", "approval_packet", "snapshot_gate", "restore_barrier", "rollback_packet", "governance", "execution", "audit", "closure"],
            "runtime_mutation_performed": False,
        })
    return rows


def _channel_state(channel: str, row: dict[str, Any], snapshots: dict[str, dict[str, Any]], users_count: int) -> tuple[str, str]:
    state = row.get("state") if isinstance(row.get("state"), dict) else {}
    code_ok = str(state.get("code") or "") == "200" or str(state.get("diagnose_severity") or "").upper() == "OK"
    score_row = _by_channel(_items(snapshots.get("channel-service-scores", {}))).get(channel, {})
    service_score = _as_float(score_row.get("score", score_row.get("service_score", score_row.get("confidence", 0.0))), 0.0)
    risk = _global_metric(snapshots, "risk-summaries", "risk_score", 0.0)
    trust = _global_metric(snapshots, "trust-summaries", "trust_score", 50.0)
    if not code_ok and state:
        return "Degraded", "runtime health evidence is not OK"
    if risk >= 70:
        return "Degraded", "risk snapshot is high"
    if service_score >= 90 and trust >= 70:
        return "Excellent", "service score and trust evidence are strong"
    if service_score >= 65 or code_ok:
        return "Good", "channel is usable with current evidence"
    if users_count:
        return "Warning", "assigned users exist but intelligence evidence is incomplete"
    return "Warning", "channel evidence is incomplete"


def build_channel_decision_rows(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    users = snapshot.get("users") or []
    egress = snapshot.get("egress") or []
    runtime_state = snapshot.get("runtime_state") or {}
    snapshots = snapshot.get("snapshots") or {}
    egress_state = runtime_state.get("egress") if isinstance(runtime_state.get("egress"), dict) else {}
    rows: list[dict[str, Any]] = []
    for channel in egress:
        channel_id = str(channel.get("id") or channel.get("egress") or "")
        if not channel_id:
            continue
        assigned = [user for user in users if str(user.get("current") or "") == channel_id]
        combined = {"registry": channel, "state": egress_state.get(channel_id, {}) if isinstance(egress_state.get(channel_id), dict) else {}}
        score_row = _by_channel(_items(snapshots.get("channel-service-scores", {}))).get(channel_id, {})
        service_score = _as_float(score_row.get("score", score_row.get("service_score", score_row.get("confidence", 0.0))), 0.0)
        state_payload = _channel_state_from_trust_model(channel_id, snapshots) or _legacy_channel_state(channel_id, combined, snapshots, len(assigned))
        state = state_payload["channel_state"]
        why = state_payload["channel_state_reason_short"]
        rows.append({
            "channel": channel_id,
            "state": state,
            "state_reason": why,
            **state_payload,
            "users": len(assigned),
            "capacity": channel.get("capacity") or channel.get("hard_limit") or "",
            "soft_limit": channel.get("soft_limit") or "",
            "hard_limit": channel.get("hard_limit") or channel.get("capacity") or "",
            "service_score": service_score,
            "stability": _global_metric(snapshots, "trust-evolution-summaries", "stability_score", 0.0),
            "risk": _global_metric(snapshots, "risk-summaries", "risk_score", 0.0),
            "trust": _global_metric(snapshots, "trust-summaries", "trust_score", 50.0),
            "prediction": _prediction_summary_for(channel_id, snapshots),
            "services": _service_scores_for(channel_id, snapshots),
            "reasons": [why],
            "runtime_mutation_performed": False,
        })
    return rows


def build_batch_preview(user_rows: list[dict[str, Any]]) -> dict[str, Any]:
    moves = [row for row in user_rows if row.get("recommendation") == "move_recommended"]
    groups: dict[str, int] = {}
    for row in moves:
        key = f"{row.get('current_channel') or 'unknown'}->{row.get('recommended_channel') or 'unknown'}"
        groups[key] = groups.get(key, 0) + 1
    review_required = [row for row in moves if row.get("review_required")]
    avg_confidence = round(sum(_as_float(row.get("confidence")) for row in moves) / len(moves), 3) if moves else 0.0
    return {
        "preview_only": True,
        "execution_allowed_now": False,
        "users_to_move": [
            {
                "user": row.get("user"),
                "from": row.get("current_channel"),
                "to": row.get("recommended_channel"),
                "confidence": row.get("confidence"),
                "risk": row.get("risk"),
                "recommendation_hash": row.get("recommendation_hash"),
                "ctr_governance_evidence": row.get("ctr_governance_evidence", {}),
                "review_required": row.get("review_required", False),
                "review_reason": row.get("review_reason", ""),
                "review_category": row.get("review_category", ""),
                "review_severity": row.get("review_severity", ""),
                "review_recommendation": row.get("review_recommendation", ""),
                "review_warning": row.get("review_warning", ""),
                "review_next_action": row.get("review_next_action", ""),
                "emergency_only": row.get("emergency_only", False),
            }
            for row in moves
        ],
        "source_target_groups": [{"path": key, "count": count} for key, count in sorted(groups.items())],
        "ctr_review_summary": {
            "schema_version": "v7.ctr.batch-review-summary.v1",
            "review_required_count": len(review_required),
            "emergency_only_count": sum(1 for row in review_required if row.get("emergency_only")),
            "review_categories": sorted({str(row.get("review_category") or "") for row in review_required if row.get("review_category")}),
            "review_severities": sorted({str(row.get("review_severity") or "") for row in review_required if row.get("review_severity")}),
            "packet_authority_changed": False,
            "approval_authority": "none",
            "denial_authority": "none",
            "runtime_execution_authority": "none",
        },
        "blast_radius": {"users": len(moves), "bounded": len(moves) <= 10, "mode": "preview_only"},
        "rollback_readiness": "packet_required_before_execution" if moves else "not_required",
        "confidence": avg_confidence,
        "risk": "MEDIUM" if len(moves) > 1 else ("LOW" if moves else "NONE"),
        "workflow": ["approval_packet", "blast_radius_validation", "governance", "rollback_prep", "execution", "audit", "closure"],
    }


def build_decision_action_matrix() -> list[dict[str, Any]]:
    return [
        {"decision": "ignore_recommendation", "action": "write audit/evidence fingerprint; hide current fingerprint in UI", "runtime_mutation": False},
        {"decision": "move_user", "action": "open approval packet and governance preview; no direct switch", "runtime_mutation": False},
        {"decision": "apply_best_recommendations", "action": "open batch preview; execution remains disabled until approval chain", "runtime_mutation": False},
        {"decision": "recommendation_changed", "action": "new fingerprint restores highlight", "runtime_mutation": False},
        {"decision": "recommendation_expired", "action": "show warning and require fresh snapshots", "runtime_mutation": False},
        {"decision": "recommendation_rejected", "action": "audit outcome and keep runtime unchanged", "runtime_mutation": False},
        {"decision": "recommendation_approved", "action": "must pass approval packet, snapshot gate, restore barrier, rollback packet, governance, execution, audit, closure", "runtime_mutation": "governed path only"},
    ]


def build_operator_decision_surface(
    *,
    snapshot_root: Path | str,
    users: list[dict[str, Any]],
    egress: list[dict[str, Any]],
    runtime_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    request_snapshot = request_decision_snapshot(
        snapshot_root=snapshot_root,
        users=users,
        egress=egress,
        runtime_state=runtime_state,
    )
    user_rows = build_user_decision_rows(request_snapshot)
    channel_rows = build_channel_decision_rows(request_snapshot)
    batch_preview = build_batch_preview(user_rows)
    why_cards = build_why_cards(
        users=user_rows,
        channels=channel_rows,
        batch_preview=batch_preview,
        snapshot_statuses=request_snapshot["snapshot_statuses"],
    )
    return {
        "schema_version": "v7.operator-decision-surface.v1",
        "mode": "read_only_operator_surface",
        "preview_only": True,
        "execution_allowed_now": False,
        "users": user_rows,
        "users_by_ip": {row["user"]: row for row in user_rows},
        "channels": channel_rows,
        "channels_by_id": {row["channel"]: row for row in channel_rows},
        "batch_preview": batch_preview,
        "why_cards": why_cards,
        "trust_evolution_advice": _trust_evolution_advice(request_snapshot["snapshots"]),
        "decision_action_matrix": build_decision_action_matrix(),
        "snapshot_statuses": request_snapshot["snapshot_statuses"],
        "authority": {
            "planner_authority_changed": False,
            "governance_changed": False,
            "execution_path_changed": False,
            "rollback_path_changed": False,
            "new_truth_sources_created": False,
            "duplicate_systems_created": False,
        },
        "reuse": {
            "recommendations": ["candidate-suitability-summary", "best-available-pool"],
            "prediction": ["prediction-summaries"],
            "trust": ["trust-summaries", "trust-evolution-summaries"],
            "governance": "existing operator approval/governance preview endpoints",
            "execution": "existing governed execution owner only; no direct UI switch",
            "rollback": "existing rollback preview/manifest owner",
        },
    }
