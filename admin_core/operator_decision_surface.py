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
        statuses[name] = {
            "exists": bool(getattr(result, "exists", False)),
            "freshness_state": getattr(result, "freshness_state", "UNKNOWN"),
            "confidence": getattr(result, "confidence", 0.0),
            "runtime_behavior": getattr(result, "runtime_behavior", "STOP"),
            "stop_required": bool(getattr(result, "stop_required", True)),
            "path": getattr(result, "path", ""),
            "errors": list(getattr(getattr(result, "validation", None), "errors", []) or []),
            "warnings": list(getattr(getattr(result, "validation", None), "warnings", []) or []),
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
        state, why = _channel_state(channel_id, combined, snapshots, len(assigned))
        rows.append({
            "channel": channel_id,
            "state": state,
            "state_reason": why,
            "users": len(assigned),
            "capacity": channel.get("capacity") or channel.get("hard_limit") or "",
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
            }
            for row in moves
        ],
        "source_target_groups": [{"path": key, "count": count} for key, count in sorted(groups.items())],
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
    return {
        "schema_version": "v7.operator-decision-surface.v1",
        "mode": "read_only_operator_surface",
        "preview_only": True,
        "execution_allowed_now": False,
        "users": user_rows,
        "users_by_ip": {row["user"]: row for row in user_rows},
        "channels": channel_rows,
        "channels_by_id": {row["channel"]: row for row in channel_rows},
        "batch_preview": build_batch_preview(user_rows),
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
