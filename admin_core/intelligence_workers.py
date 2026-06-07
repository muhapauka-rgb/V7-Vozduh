"""Heavy Brain snapshot producers for V7 intelligence.

Workers in this module compute compact intelligence snapshots. They do not
move users, write selected moves, approve governance, execute runtime actions,
restart services, or integrate with planner decisions.
"""

from __future__ import annotations

import json
import os
import statistics
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any

from admin_core.intelligence_snapshots import (
    SNAPSHOT_FAMILIES,
    build_snapshot_envelope,
    snapshot_path,
    validate_snapshot,
)
from admin_core.intelligence_platform import (
    explainability_framework,
    model_governance_framework,
    observability_model,
    trust_evolution_summary,
)
from admin_core.registry_readers import parse_registry_lines
from admin_core.routing_intelligence import (
    DEFAULT_SERVICES,
    DynamicBlastRadiusModel,
    ExecutionTrustModel,
    PredictiveFoundation,
    ServiceHistoryStore,
    ServiceIntelligenceEngine,
    UserServiceWeights,
    as_float,
    clamp,
    normalize_services,
    now_iso,
    service_quality_framework,
    sha256_json,
)
from admin_core.routing_brain import RoutingBrain


MAX_HISTORY_RECORDS = 1000
MAX_HISTORY_BYTES = 512_000
GENERATOR = "admin_core.intelligence_workers"


@dataclass(frozen=True)
class WorkerRunResult:
    snapshots: dict[str, dict[str, Any]]
    metrics: dict[str, Any]
    warnings: list[str]


def read_json(path: Path | str, default: Any) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


def read_registry(path: Path | str) -> list[dict[str, str]]:
    try:
        lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    except (FileNotFoundError, OSError):
        return []
    return parse_registry_lines(lines)


def read_jsonl_tail(path: Path | str, *, limit: int = MAX_HISTORY_RECORDS, max_bytes: int = MAX_HISTORY_BYTES) -> list[dict[str, Any]]:
    path_obj = Path(path)
    try:
        with path_obj.open("rb") as handle:
            handle.seek(0, os.SEEK_END)
            size = handle.tell()
            handle.seek(max(0, size - max_bytes))
            data = handle.read(max_bytes)
    except (FileNotFoundError, OSError):
        return []
    lines = data.decode("utf-8", errors="replace").splitlines()
    if size > max_bytes and lines:
        lines = lines[1:]
    rows: list[dict[str, Any]] = []
    for line in lines:
        text = line.strip()
        if not text:
            continue
        try:
            item = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            rows.append(item)
    return rows[-limit:]


def write_json_atomic(path: Path | str, payload: dict[str, Any]) -> None:
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    tmp = path_obj.with_name(f".{path_obj.name}.tmp.{os.getpid()}")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path_obj)


def mean(values: list[float], default: float = 0.0) -> float:
    return float(statistics.mean(values)) if values else default


def source_hashes(**items: Any) -> dict[str, str]:
    return {key: sha256_json(value) for key, value in items.items()}


def confidence_from_factors(**factors: float) -> tuple[float, dict[str, float]]:
    clean = {key: round(clamp(value, 0.0, 1.0), 4) for key, value in factors.items()}
    return round(mean(list(clean.values())), 4) if clean else 0.0, clean


def score_distribution(values: list[float]) -> dict[str, Any]:
    clean = [clamp(value) for value in values]
    if not clean:
        return {
            "count": 0,
            "min": 0.0,
            "max": 0.0,
            "mean": 0.0,
            "spread": 0.0,
            "stdev": 0.0,
            "distinct_rounded": 0,
            "calibration_state": "NO_DATA",
        }
    spread = max(clean) - min(clean)
    stdev = statistics.pstdev(clean) if len(clean) > 1 else 0.0
    distinct = len({round(value) for value in clean})
    state = "OK"
    if len(clean) >= 2 and spread < 8.0:
        state = "LOW_SPREAD"
    if len(clean) >= 3 and distinct <= 1:
        state = "COLLAPSED_IDENTICAL"
    if mean(clean) >= 90.0 and spread < 12.0:
        state = "HIGH_SCORE_COMPRESSION"
    if mean(clean) <= 50.0 and spread < 12.0:
        state = "LOW_SCORE_COMPRESSION"
    return {
        "count": len(clean),
        "min": round(min(clean), 3),
        "max": round(max(clean), 3),
        "mean": round(mean(clean), 3),
        "spread": round(spread, 3),
        "stdev": round(stdev, 3),
        "distinct_rounded": distinct,
        "calibration_state": state,
    }


def envelope(
    family_name: str,
    *,
    generated_at: str,
    confidence: float,
    confidence_factors: dict[str, float],
    source_hashes_value: dict[str, str],
    content: Any,
    item_count: int,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    payload = build_snapshot_envelope(
        family_name,
        generated_at=generated_at,
        confidence=confidence,
        source_hashes=source_hashes_value,
        generator=GENERATOR,
        item_count=item_count,
        warnings=warnings or [],
        content=content,
    )
    payload["confidence_factors"] = confidence_factors
    validation = validate_snapshot(payload, family_name)
    if not validation.ok:
        payload.setdefault("warnings", []).extend(validation.errors)
    return payload


def worker_architecture() -> dict[str, Any]:
    return {
        "schema": "v7.intelligence.worker-architecture.v1",
        "owner": "Heavy Brain snapshot producers",
        "runtime_integration": "none_in_PERF3",
        "producers": {
            "service_score_worker": {
                "inputs": ["service-matrix.json", "egress-quality-summary.json", "service-preferences.json"],
                "outputs": ["service-scores.json", "channel-service-scores.json"],
                "cadence_seconds": 60,
            },
            "trust_worker": {
                "inputs": ["audit history", "switch history", "rollback history"],
                "outputs": ["trust-summaries.json"],
                "cadence_seconds": 300,
                "bounded_records": MAX_HISTORY_RECORDS,
            },
            "risk_worker": {
                "inputs": ["service-scores.json", "channel-service-scores.json", "quality summary"],
                "outputs": ["risk-summaries.json"],
                "cadence_seconds": 60,
            },
            "blast_radius_worker": {
                "inputs": ["trust-summaries.json", "risk-summaries.json", "runtime counts"],
                "outputs": ["blast-radius-summaries.json"],
                "cadence_seconds": 60,
            },
            "user_service_score_worker": {
                "inputs": ["users.registry", "service-matrix.json", "egress-quality-summary.json", "service-preferences.json"],
                "outputs": ["user-service-scores.json"],
                "cadence_seconds": 300,
            },
            "candidate_suitability_worker": {
                "inputs": ["users.registry", "egress.registry", "service-matrix.json", "egress-quality-summary.json", "service-preferences.json", "risk-summaries.json", "trust-summaries.json"],
                "outputs": ["candidate-suitability-summary.json"],
                "cadence_seconds": 60,
            },
            "best_available_pool_worker": {
                "inputs": ["candidate-suitability-summary.json", "users.registry", "egress.registry", "v7-state.json"],
                "outputs": ["best-available-pool.json"],
                "cadence_seconds": 60,
            },
            "prediction_worker": {
                "inputs": ["service-matrix.json", "egress-quality-summary.json", "risk-summaries.json", "trust-summaries.json", "blast-radius-summaries.json"],
                "outputs": ["prediction-summaries.json"],
                "cadence_seconds": 300,
            },
            "trust_evolution_worker": {
                "inputs": ["trust-summaries.json", "prediction-summaries.json", "service-scores.json", "channel-service-scores.json", "candidate-suitability-summary.json", "best-available-pool.json", "blast-radius-summaries.json", "bounded audit/switch/rollback outcomes"],
                "outputs": ["trust-evolution-summaries.json"],
                "cadence_seconds": 300,
                "runtime_authority": "none_advisory_snapshot_only",
            },
            "overview_worker": {
                "inputs": ["runtime state", "registries", "intelligence snapshots"],
                "outputs": ["overview-summary.json"],
                "cadence_seconds": 30,
            },
        },
        "forbidden": [
            "user movement",
            "selected move writes",
            "governance approval",
            "runtime actions",
            "service restarts",
            "planner integration",
        ],
    }


def user_ip(row: dict[str, Any]) -> str:
    return str(row.get("ip") or row.get("user") or row.get("id") or "").strip()


def user_enabled(row: dict[str, Any]) -> bool:
    return str(row.get("enabled", "1")).strip().lower() not in {"0", "false", "no", "disabled"}


def egress_id(row: dict[str, Any]) -> str:
    return str(row.get("id") or row.get("egress") or row.get("channel") or "").strip()


def egress_available(row: dict[str, Any]) -> bool:
    state = str(row.get("state") or row.get("status") or "enabled").strip().lower()
    if str(row.get("enabled", "1")).strip().lower() in {"0", "false", "no", "disabled"}:
        return False
    if state in {"maintenance", "disabled", "quarantine", "down"}:
        return False
    if str(row.get("manual_only", "")).strip().lower() in {"1", "true", "yes"}:
        return False
    if str(row.get("canary_reserved", "")).strip().lower() in {"1", "true", "yes"}:
        return False
    return True


def _text_value(value: Any) -> str:
    return str(value or "").strip()


def _lower_value(value: Any) -> str:
    return _text_value(value).lower()


def _first_value(row: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = row.get(key)
        if value not in (None, ""):
            return value
    return ""


def _event_time(row: dict[str, Any]) -> str:
    operation = row.get("operation") if isinstance(row.get("operation"), dict) else {}
    return _text_value(_first_value(
        row,
        "event_time",
        "timestamp",
        "time",
        "created_at",
        "updated_at",
        "generated_at",
    ) or _first_value(operation, "event_time", "timestamp", "time", "created_at"))


def _user_from_row(row: dict[str, Any]) -> str:
    return _text_value(_first_value(row, "user", "username", "peer", "ip", "user_ip", "client", "client_ip"))


def _channel_from_row(row: dict[str, Any]) -> str:
    return _text_value(_first_value(
        row,
        "channel",
        "egress",
        "target",
        "to",
        "to_egress",
        "new_egress",
        "target_egress",
        "routing_table",
    ))


def normalize_outcome_evidence(row: dict[str, Any], *, evidence_source: str = "decision_record") -> dict[str, Any]:
    if not isinstance(row, dict):
        return {}
    operation = row.get("operation") if isinstance(row.get("operation"), dict) else {}
    result = _lower_value(row.get("result") or operation.get("result"))
    terminal = _lower_value(row.get("terminal_state") or operation.get("terminal_state"))
    text = " ".join(
        _lower_value(value)
        for value in (
            result,
            terminal,
            row.get("status"),
            row.get("action"),
            row.get("message"),
            row.get("reason"),
        )
    )
    rollback = bool(row.get("rollback") or row.get("rollback_required") or row.get("rollback_completed") or "rollback" in text)
    failed = bool(row.get("failed") or row.get("error") or "failed" in text or "failure" in text or "error" in text or "denied" in text)
    applied = bool(
        row.get("applied")
        or row.get("success")
        or result in {"ok", "success", "applied", "pass", "passed"}
        or terminal in {"ok", "success", "applied", "complete", "completed"}
        or "verification pass" in text
    )
    if rollback and failed:
        status = "rollback_failure"
        confidence = 0.85
    elif rollback:
        status = "rollback"
        confidence = 0.8
    elif applied:
        status = "success"
        confidence = 0.9 if result or terminal else 0.75
    elif failed:
        status = "failure"
        confidence = 0.85
    elif row.get("apply") or "apply" in text or "governance approval" in text:
        status = "partial_success"
        confidence = 0.6
    else:
        status = "unknown"
        confidence = 0.35
    return {
        "outcome_status": status,
        "result": "success" if status in {"success", "partial_success"} else "failed" if "failure" in status else status,
        "success": status in {"success", "partial_success"},
        "evidence_source": evidence_source,
        "evidence_confidence": confidence,
        "evidence_status": "complete" if status not in {"unknown", "partial_success"} else "partial",
        "event_time": _event_time(row),
        "user": _user_from_row(row),
        "channel": _channel_from_row(row),
    }


def _selected_move_rows(record: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in ("selected_move", "selected_moves"):
        value = record.get(key)
        if isinstance(value, dict):
            rows.append(value)
        elif isinstance(value, list):
            rows.extend(item for item in value if isinstance(item, dict))
    operation = record.get("operation") if isinstance(record.get("operation"), dict) else {}
    for key in ("selected_move", "selected_moves"):
        value = operation.get(key)
        if isinstance(value, dict):
            rows.append(value)
        elif isinstance(value, list):
            rows.extend(item for item in value if isinstance(item, dict))
    if not rows and (_user_from_row(record) or _channel_from_row(record)):
        rows.append(record)
    return rows


def _candidate_keys(candidate_rows: list[dict[str, Any]] | None) -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    for row in candidate_rows or []:
        if not isinstance(row, dict):
            continue
        user = _text_value(row.get("user"))
        candidates = row.get("candidates") if isinstance(row.get("candidates"), list) else [row]
        for candidate in candidates:
            if not isinstance(candidate, dict):
                continue
            candidate_user = _text_value(candidate.get("user") or user)
            channel = _channel_from_row(candidate)
            if candidate_user and channel:
                keys.add((candidate_user, channel))
    return keys


def build_candidate_outcome_rows(
    candidate_rows: list[dict[str, Any]] | None,
    decision_records: list[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    wanted = _candidate_keys(candidate_rows)
    outcomes: dict[tuple[str, str], dict[str, Any]] = {}
    for record in decision_records or []:
        if not isinstance(record, dict):
            continue
        base = normalize_outcome_evidence(record, evidence_source=_text_value(record.get("evidence_source")) or "decision_record")
        for move in _selected_move_rows(record):
            user = _user_from_row(move) or base.get("user", "")
            channel = _channel_from_row(move) or base.get("channel", "")
            key = (user, channel)
            if not user or not channel or (wanted and key not in wanted):
                continue
            outcomes[key] = {
                **base,
                "user": user,
                "channel": channel,
                "egress": channel,
                "evidence_source": base.get("evidence_source") or "selected_move_audit",
            }
    return list(outcomes.values())[-MAX_HISTORY_RECORDS:]


def _actual_score_from_row(row: dict[str, Any]) -> float | None:
    for key in ("quality", "score", "aggregate_score", "average_score", "forecast_quality", "future_quality"):
        if row.get(key) not in (None, ""):
            return as_float(row.get(key), 0.0)
    return None


def build_service_actual_rows(
    service_rows: list[dict[str, Any]] | None,
    decision_records: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    actuals: list[dict[str, Any]] = []
    decision_evidence = [normalize_outcome_evidence(row) for row in (decision_records or []) if isinstance(row, dict)]
    evidence_confidence = mean([as_float(row.get("evidence_confidence"), 0.0) for row in decision_evidence], 0.0)
    for row in service_rows or []:
        if not isinstance(row, dict):
            continue
        score = _actual_score_from_row(row)
        if score is None:
            continue
        item = {
            "score": round(score, 3),
            "quality": round(score, 3),
            "evidence_source": "service_channel_snapshot",
            "evidence_confidence": round(max(as_float(row.get("confidence"), 0.0), evidence_confidence), 4),
            "evidence_status": "complete" if row.get("confidence") not in (None, "") else "partial",
            "event_time": _event_time(row),
        }
        if row.get("channel") not in (None, ""):
            item["channel"] = _text_value(row.get("channel"))
        if row.get("service") not in (None, ""):
            item["service"] = _text_value(row.get("service"))
        if row.get("target") not in (None, ""):
            item["target"] = _text_value(row.get("target"))
        actuals.append(item)
    return actuals[-MAX_HISTORY_RECORDS:]


def build_prediction_actual_rows(
    prediction_forecasts: list[dict[str, Any]] | None,
    service_rows: list[dict[str, Any]] | None,
    decision_records: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    service_actuals = build_service_actual_rows(service_rows, decision_records)
    actual_by_key: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(service_actuals):
        key = _text_value(row.get("id") or row.get("channel") or row.get("service") or row.get("target") or index)
        actual_by_key[key] = row
    rows: list[dict[str, Any]] = []
    for index, forecast in enumerate(prediction_forecasts or []):
        if not isinstance(forecast, dict):
            continue
        key = _text_value(forecast.get("id") or forecast.get("channel") or forecast.get("service") or forecast.get("target") or index)
        actual = actual_by_key.get(key)
        if not actual:
            continue
        rows.append({
            **actual,
            "id": key,
            "evidence_source": "prediction_actual_from_existing_service_channel_evidence",
        })
    return rows[-MAX_HISTORY_RECORDS:]


CHANNEL_TRUST_TIME_WINDOWS = {
    "current_service_window": "snapshot_current",
    "short_quality_window": "1h_existing_quality_summary",
    "feedback_window": f"last_{MAX_HISTORY_RECORDS}_audit_switch_rollback_records",
    "recovery_window": "two_successful_observations_after_failure",
    "decay_window": "bounded_history_without_recent_success",
}

CHANNEL_LIFECYCLE_POLICY = {
    "NEW": "limited evidence and no negative history",
    "TRUSTED": "high current score, strong confidence, and successful feedback",
    "WATCH": "usable current score but trust is not yet strong",
    "DEGRADED": "service score, verdict, or required-service evidence is weak",
    "RECOVERING": "previous negative evidence exists but current signal has improved",
    "QUARANTINED": "rollback/failure evidence or hard service gaps require operator review",
}

CHANNEL_TRUST_DECAY_POLICY = {
    "mode": "advisory_only_no_runtime_weight_applied",
    "positive_feedback_delta": 6.0,
    "failure_feedback_delta": -14.0,
    "rollback_success_feedback_delta": -4.0,
    "rollback_failure_feedback_delta": -24.0,
    "no_recent_live_success_delta": -2.0,
    "recovery_successes_required": 2,
}


def _channel_feedback_summary(decision_records: list[dict[str, Any]] | None) -> dict[str, dict[str, Any]]:
    summaries: dict[str, dict[str, Any]] = {}
    for record in decision_records or []:
        if not isinstance(record, dict):
            continue
        base = normalize_outcome_evidence(record, evidence_source=_text_value(record.get("evidence_source")) or "decision_record")
        moves = _selected_move_rows(record) or [record]
        for move in moves:
            channel = _channel_from_row(move) or base.get("channel", "")
            if not channel:
                continue
            summary = summaries.setdefault(channel, {
                "successes": 0,
                "failures": 0,
                "rollbacks": 0,
                "rollback_successes": 0,
                "rollback_failures": 0,
                "partial": 0,
                "last_outcome": "unknown",
                "last_event_time": "",
                "evidence_confidence_values": [],
            })
            status = _text_value(base.get("outcome_status")) or "unknown"
            if status == "success":
                summary["successes"] += 1
            elif status in {"failure", "rollback_failure"}:
                summary["failures"] += 1
                if status == "rollback_failure":
                    summary["rollback_failures"] += 1
            elif status == "rollback":
                summary["rollbacks"] += 1
                summary["rollback_successes"] += 1
            elif status == "partial_success":
                summary["partial"] += 1
            summary["last_outcome"] = status
            summary["last_event_time"] = base.get("event_time", "")
            summary["evidence_confidence_values"].append(as_float(base.get("evidence_confidence"), 0.0))
    for summary in summaries.values():
        values = summary.pop("evidence_confidence_values", [])
        summary["evidence_confidence"] = round(mean(values, 0.0), 4)
    return summaries


def _candidate_scores_by_channel(candidate_suitability_snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for user_row in candidate_suitability_snapshot.get("items") or []:
        if not isinstance(user_row, dict):
            continue
        for candidate in user_row.get("candidates") or []:
            if not isinstance(candidate, dict):
                continue
            channel = _channel_from_row(candidate)
            if not channel:
                continue
            row = grouped.setdefault(channel, {"scores": [], "confidences": [], "reasons": []})
            row["scores"].append(as_float(candidate.get("suitability_score"), 0.0))
            row["confidences"].append(as_float(candidate.get("confidence"), 0.0))
            row["reasons"].extend(str(item) for item in (candidate.get("explainability") or []) if item)
    return {
        channel: {
            "average_suitability": round(mean(values["scores"], 0.0), 3),
            "confidence": round(mean(values["confidences"], 0.0), 4),
            "explainability": sorted(set(values["reasons"]))[:8],
        }
        for channel, values in grouped.items()
    }


def _best_pool_channels(best_available_pool_snapshot: dict[str, Any]) -> set[str]:
    channels: set[str] = set()
    for row in best_available_pool_snapshot.get("items") or []:
        if not isinstance(row, dict):
            continue
        if row.get("best_channel"):
            channels.add(_text_value(row.get("best_channel")))
        for key in ("available_channels", "healthy_channels", "eligible_channels", "pool"):
            value = row.get(key)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        channel = _channel_from_row(item) or _text_value(item.get("channel") or item.get("id"))
                    else:
                        channel = _text_value(item)
                    if channel:
                        channels.add(channel)
    return channels


def _channel_lifecycle(
    *,
    current_score: float,
    confidence: float,
    verdict: str,
    required_low: list[Any],
    required_missing: list[Any],
    feedback: dict[str, Any],
) -> tuple[str, str]:
    failures = int(feedback.get("failures") or 0)
    rollback_failures = int(feedback.get("rollback_failures") or 0)
    successes = int(feedback.get("successes") or 0)
    last = _text_value(feedback.get("last_outcome"))
    if rollback_failures or failures >= 2 or required_missing or current_score < 45.0:
        return "QUARANTINED", "hard_negative_feedback_or_service_gap"
    if failures and current_score >= 70.0 and last == "success":
        return "RECOVERING", "negative_history_with_current_success"
    if verdict != "OK" or required_low or current_score < 60.0:
        return "DEGRADED", "current_service_signal_below_floor"
    if current_score >= 80.0 and confidence >= 0.70 and successes > 0:
        return "TRUSTED", "high_score_high_confidence_successful_feedback"
    if successes == 0 and confidence < 0.50:
        return "NEW", "insufficient_live_feedback"
    return "WATCH", "usable_but_not_certified_trusted"


def _routing_impact_for_lifecycle(lifecycle: str, trust_score: float) -> dict[str, Any]:
    recommended_bias = {
        "TRUSTED": "prefer_when_planner_scores_are_close",
        "WATCH": "neutral",
        "NEW": "neutral_with_observation",
        "RECOVERING": "allow_only_with_operator_attention",
        "DEGRADED": "avoid_until_recovered",
        "QUARANTINED": "block_until_operator_review",
    }.get(lifecycle, "neutral")
    return {
        "mode": "advisory_only_no_runtime_weight_applied",
        "recommended_bias": recommended_bias,
        "trust_score": round(trust_score, 3),
        "planner_behavior_changed": False,
        "runtime_decision_authority": "none_evidence_only",
    }


def build_channel_trust_recovery_model(
    *,
    channel_service_scores_snapshot: dict[str, Any],
    candidate_suitability_snapshot: dict[str, Any],
    best_available_pool_snapshot: dict[str, Any],
    decision_records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    feedback_by_channel = _channel_feedback_summary(decision_records)
    suitability_by_channel = _candidate_scores_by_channel(candidate_suitability_snapshot)
    pool_channels = _best_pool_channels(best_available_pool_snapshot)
    channel_rows = {
        _text_value(row.get("channel")): row
        for row in channel_service_scores_snapshot.get("items") or []
        if isinstance(row, dict) and _text_value(row.get("channel"))
    }
    channels = sorted(set(channel_rows) | set(suitability_by_channel) | set(feedback_by_channel) | pool_channels)
    rows: list[dict[str, Any]] = []
    lifecycle_counts: dict[str, int] = {}
    for channel in channels:
        row = channel_rows.get(channel, {})
        feedback = feedback_by_channel.get(channel, {})
        suitability = suitability_by_channel.get(channel, {})
        current_score = clamp(as_float(row.get("aggregate_score"), 0.0), 0.0, 100.0)
        suitability_score = clamp(as_float(suitability.get("average_suitability"), current_score), 0.0, 100.0)
        confidence = clamp(max(as_float(row.get("confidence"), 0.0), as_float(suitability.get("confidence"), 0.0)), 0.0, 1.0)
        successes = int(feedback.get("successes") or 0)
        failures = int(feedback.get("failures") or 0)
        rollback_successes = int(feedback.get("rollback_successes") or 0)
        rollback_failures = int(feedback.get("rollback_failures") or 0)
        rollbacks = rollback_successes + rollback_failures
        feedback_score = clamp(
            60.0
            + (successes * 6.0)
            - (failures * 14.0)
            - (rollback_successes * 4.0)
            - (rollback_failures * 24.0),
            0.0,
            100.0,
        )
        no_recent_success_delta = CHANNEL_TRUST_DECAY_POLICY["no_recent_live_success_delta"] if successes == 0 else 0.0
        trust_score = clamp(
            (current_score * 0.45)
            + (suitability_score * 0.20)
            + ((confidence * 100.0) * 0.15)
            + (feedback_score * 0.20)
            + no_recent_success_delta
        )
        required_low = row.get("required_low") if isinstance(row.get("required_low"), list) else []
        required_missing = row.get("required_missing") if isinstance(row.get("required_missing"), list) else []
        lifecycle, lifecycle_reason = _channel_lifecycle(
            current_score=current_score,
            confidence=confidence,
            verdict=_text_value(row.get("verdict") or "UNKNOWN"),
            required_low=required_low,
            required_missing=required_missing,
            feedback=feedback,
        )
        lifecycle_counts[lifecycle] = lifecycle_counts.get(lifecycle, 0) + 1
        if lifecycle == "RECOVERING":
            recovery_state = "IN_PROGRESS" if successes < CHANNEL_TRUST_DECAY_POLICY["recovery_successes_required"] else "RECOVERED"
        elif failures or rollback_failures:
            recovery_state = "BLOCKED" if lifecycle in {"DEGRADED", "QUARANTINED"} else "REVIEW"
        else:
            recovery_state = "NOT_NEEDED"
        explanations = [
            f"current_service_score={round(current_score, 3)}",
            f"candidate_suitability={round(suitability_score, 3)}",
            f"confidence={round(confidence, 4)}",
            f"feedback_successes={successes}",
            f"feedback_failures={failures}",
            f"feedback_rollback_successes={rollback_successes}",
            f"feedback_rollback_failures={rollback_failures}",
            f"lifecycle_reason={lifecycle_reason}",
        ]
        explanations.extend(suitability.get("explainability") or [])
        rows.append({
            "channel": channel,
            "lifecycle": lifecycle,
            "lifecycle_reason": lifecycle_reason,
            "trust_score": round(trust_score, 3),
            "current_service_score": round(current_score, 3),
            "candidate_suitability": round(suitability_score, 3),
            "confidence": round(confidence, 4),
            "feedback": {
                "successes": successes,
                "failures": failures,
                "rollbacks": rollbacks,
                "rollback_successes": rollback_successes,
                "rollback_failures": rollback_failures,
                "partial": int(feedback.get("partial") or 0),
                "last_outcome": feedback.get("last_outcome", "unknown"),
                "last_event_time": feedback.get("last_event_time", ""),
                "evidence_confidence": feedback.get("evidence_confidence", 0.0),
            },
            "recovery": {
                "state": recovery_state,
                "successes_required": CHANNEL_TRUST_DECAY_POLICY["recovery_successes_required"],
                "safe_to_restore_eligibility": lifecycle in {"TRUSTED", "WATCH"},
                "operator_review_required": lifecycle in {"DEGRADED", "QUARANTINED", "RECOVERING"},
            },
            "decay": {
                "applied_delta": no_recent_success_delta,
                "reason": "no_recent_live_success" if no_recent_success_delta else "recent_success_or_neutral",
                "runtime_behavior_changed": False,
            },
            "routing_impact": _routing_impact_for_lifecycle(lifecycle, trust_score),
            "explainability": explanations[:12],
            "runtime_decision_authority": "none_evidence_only",
        })
    return {
        "schema": "v7.intelligence.channel-trust-recovery-explainability.v1",
        "owner": "admin_core.intelligence_workers.trust-evolution-summaries",
        "truth_source": "existing_intelligence_snapshots_and_feedback_records",
        "routing_behavior_changed": False,
        "runtime_decision_authority": "none_evidence_only",
        "time_windows": CHANNEL_TRUST_TIME_WINDOWS,
        "lifecycle_policy": CHANNEL_LIFECYCLE_POLICY,
        "decay_policy": CHANNEL_TRUST_DECAY_POLICY,
        "summary": {
            "channel_count": len(rows),
            "lifecycle_counts": lifecycle_counts,
            "trusted_or_watch_count": sum(1 for row in rows if row["lifecycle"] in {"TRUSTED", "WATCH"}),
            "degraded_or_quarantined_count": sum(1 for row in rows if row["lifecycle"] in {"DEGRADED", "QUARANTINED"}),
            "recovering_count": sum(1 for row in rows if row["lifecycle"] == "RECOVERING"),
        },
        "channels": rows,
    }


def build_service_score_snapshots(
    *,
    service_matrix: dict[str, Any],
    quality_summary: dict[str, Any],
    service_preferences: dict[str, Any],
    generated_at: str | None = None,
) -> dict[str, dict[str, Any]]:
    generated = generated_at or now_iso()
    warnings: list[str] = []
    matrix_items = (service_matrix.get("items") or {}) if isinstance(service_matrix, dict) else {}
    quality_items = (quality_summary.get("items") or {}) if isinstance(quality_summary, dict) else {}
    if not matrix_items:
        warnings.append("service_matrix_missing_or_empty")
    if not quality_items:
        warnings.append("quality_summary_missing_or_empty")

    required = normalize_services((service_preferences or {}).get("required_services") or list(DEFAULT_SERVICES))
    history = ServiceHistoryStore.from_runtime_inputs(service_matrix, quality_summary, generated_at=generated)
    weights = UserServiceWeights.from_service_preferences(service_preferences or {}, required)
    engine = ServiceIntelligenceEngine(history)
    channel_scores = engine.score_all_targets(required_services=required, service_weights=weights.defaults, window="1h")

    service_rows = []
    confidence_values = []
    service_distributions: dict[str, dict[str, Any]] = {}
    for service_id in sorted(history.services):
        target_scores = []
        for target_id in sorted(matrix_items):
            row = engine.score_service(service_id, target_id, "1h")
            target_scores.append(row)
            confidence_values.append(as_float(row.get("confidence"), 0.0))
        scores = [as_float(row.get("score"), 0.0) for row in target_scores]
        service_distributions[service_id] = score_distribution(scores)
        trends = [
            row.get("quality_trend") or {}
            for row in target_scores
            if isinstance(row.get("quality_trend"), dict)
        ]
        degrading_targets = [
            row["target"]
            for row in target_scores
            if isinstance(row.get("quality_trend"), dict) and row["quality_trend"].get("quality_trend") == "degrading"
        ]
        service_rows.append({
            "service": service_id,
            "target_count": len(target_scores),
            "average_score": round(mean(scores), 3),
            "confidence": round(mean([as_float(row.get("confidence"), 0.0) for row in target_scores]), 4),
            "low_targets": [row["target"] for row in target_scores if as_float(row.get("score"), 0.0) < 50.0],
            "degrading_targets": degrading_targets,
            "score_distribution": service_distributions[service_id],
            "quality_model_schema": target_scores[0].get("schema_version") if target_scores else "ri4cd.service-quality-score.v1",
            "criteria_seen": sorted({
                key
                for row in target_scores
                for key in ((row.get("quality_components") or {}).keys())
            }),
            "trend_summary": {
                "degradation_frequency": round(mean([as_float(row.get("degradation_frequency"), 0.0) for row in trends]), 4),
                "recovery_speed": round(mean([as_float(row.get("recovery_speed"), 0.0) for row in trends]), 3),
                "stability_trend_delta": round(mean([as_float(row.get("stability_trend_delta"), 0.0) for row in trends]), 4),
            },
            "runtime_decision_authority": "none_snapshot_only",
        })

    channel_items = []
    channel_aggregate_scores: list[float] = []
    for target_id, row in sorted(channel_scores.items()):
        per_confidence = [as_float(item.get("confidence"), 0.0) for item in (row.get("per_service") or [])]
        confidence_values.extend(per_confidence)
        channel_aggregate_scores.append(as_float(row.get("aggregate_score"), 0.0))
        channel_items.append({
            "channel": target_id,
            "aggregate_score": row.get("aggregate_score", 0.0),
            "verdict": row.get("verdict", "UNKNOWN"),
            "confidence": round(mean(per_confidence), 4),
            "required_missing": row.get("required_missing", []),
            "required_low": row.get("required_low", []),
            "score_distribution": score_distribution([as_float(item.get("score"), 0.0) for item in (row.get("per_service") or [])]),
            "runtime_decision_authority": "none_snapshot_only",
        })

    source_completeness = 1.0 if matrix_items else 0.0
    history_completeness = 1.0 if quality_items else 0.5 if matrix_items else 0.0
    service_completeness = min(1.0, len(service_rows) / max(1, len(required)))
    confidence, factors = confidence_from_factors(
        source_completeness=source_completeness,
        history_completeness=history_completeness,
        probe_completeness=mean(confidence_values, 0.0),
        service_completeness=service_completeness,
    )
    hashes = source_hashes(
        service_matrix=service_matrix or {},
        quality_summary=quality_summary or {},
        service_preferences=service_preferences or {},
    )
    calibration = {
        "schema": "ri4cd.service-calibration.v1",
        "service_distributions": service_distributions,
        "channel_distribution": score_distribution(channel_aggregate_scores),
        "distribution_quality": "PASS" if score_distribution(channel_aggregate_scores).get("calibration_state") not in {"COLLAPSED_IDENTICAL"} else "REVIEW",
        "runtime_decision_authority": "none_snapshot_only",
    }
    service_payload = envelope(
        "service-scores",
        generated_at=generated,
        confidence=confidence,
        confidence_factors=factors,
        source_hashes_value=hashes,
        content=service_rows,
        item_count=len(service_rows),
        warnings=warnings,
    )
    service_payload["metadata"] = {
        "framework": service_quality_framework(),
        "calibration": calibration,
        "model_governance": model_governance_framework(),
        "explainability": explainability_framework(),
    }
    return {
        "service-scores": service_payload,
        "channel-service-scores": envelope(
            "channel-service-scores",
            generated_at=generated,
            confidence=confidence,
            confidence_factors=factors,
            source_hashes_value=hashes,
            content=channel_items,
            item_count=len(channel_items),
            warnings=warnings,
        ),
    }


def build_user_service_scores_snapshot(
    *,
    service_matrix: dict[str, Any],
    quality_summary: dict[str, Any],
    service_preferences: dict[str, Any],
    users_registry: list[dict[str, Any]],
    trust_summary_snapshot: dict[str, Any] | None = None,
    risk_summary_snapshot: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated = generated_at or now_iso()
    warnings: list[str] = []
    active_users = [row for row in (users_registry or []) if user_enabled(row) and user_ip(row)]
    required = normalize_services((service_preferences or {}).get("required_services") or list(DEFAULT_SERVICES))
    history = ServiceHistoryStore.from_runtime_inputs(service_matrix or {}, quality_summary or {}, generated_at=generated)
    weights = UserServiceWeights.from_service_preferences(service_preferences or {}, required)
    engine = ServiceIntelligenceEngine(history)
    trust_items = (trust_summary_snapshot or {}).get("items") or []
    trust_row = trust_items[0] if trust_items and isinstance(trust_items[0], dict) else {}
    trust = trust_row.get("trust") if isinstance(trust_row.get("trust"), dict) else {}
    trust_score = clamp(as_float(trust.get("score"), 50.0), 0.0, 100.0)
    risk_items = (risk_summary_snapshot or {}).get("items") or []
    risk_row = risk_items[0] if risk_items and isinstance(risk_items[0], dict) else {}
    service_risk = clamp(as_float(risk_row.get("service_risk"), 50.0), 0.0, 100.0)
    target_ids = sorted({
        target
        for service in history.services.values()
        for target in ((service.get("targets") or {}).keys())
    })
    rows = []
    confidence_values: list[float] = []
    for user_row in active_users:
        uid = user_ip(user_row)
        user_weights = weights.for_user(uid, required)
        service_rows = []
        for service in normalize_services(required or user_weights.keys()):
            per_target = [
                engine.score_service(service, target_id, "1h")
                for target_id in target_ids
            ]
            scores = [as_float(row.get("score"), 0.0) for row in per_target]
            confidences = [as_float(row.get("confidence"), 0.0) for row in per_target]
            confidence_values.extend(confidences)
            best = max(per_target, key=lambda row: as_float(row.get("score"), 0.0), default={})
            raw_score = mean(scores)
            importance_weight = as_float(user_weights.get(service, 0.0), 0.0)
            required_influence = 5.0 if service in required else 0.0
            history_influence = round((raw_score - 50.0) * 0.25, 3)
            risk_influence = round((50.0 - service_risk) * 0.10, 3)
            trust_influence = round((trust_score - 50.0) * 0.10, 3)
            suitability_influence = round((as_float(best.get("score"), 0.0) - raw_score) * 0.10, 3)
            adjusted_score = clamp(
                raw_score
                + required_influence
                + history_influence
                + risk_influence
                + trust_influence
                + suitability_influence
            )
            service_rows.append({
                "service": service,
                "score": round(adjusted_score, 3),
                "raw_quality_score": round(raw_score, 3),
                "best_channel": best.get("target", ""),
                "best_score": best.get("score", 0.0),
                "weight": importance_weight,
                "importance_influence": round((importance_weight - 50.0) * 0.10, 3),
                "required_service_influence": required_influence,
                "history_influence": history_influence,
                "risk_influence": risk_influence,
                "trust_influence": trust_influence,
                "service_suitability_influence": suitability_influence,
                "quality_trend": best.get("quality_trend", {}),
                "confidence": round(mean(confidences), 4),
                "runtime_decision_authority": "none_snapshot_only",
            })
        aggregate = sum(as_float(row["score"]) * (as_float(row["weight"]) / 100.0) for row in service_rows)
        rows.append({
            "user": uid,
            "required_services": required,
            "weighted_service_score": round(clamp(aggregate), 3),
            "services": service_rows,
            "runtime_decision_authority": "none_snapshot_only",
        })
    if not active_users:
        warnings.append("users_registry_missing_or_empty")
    if not target_ids:
        warnings.append("service_history_missing")
    confidence, factors = confidence_from_factors(
        source_completeness=1.0 if active_users else 0.0,
        history_completeness=1.0 if target_ids else 0.0,
        probe_completeness=mean(confidence_values, 0.0),
        service_completeness=1.0 if required else 0.5,
    )
    return envelope(
        "user-service-scores",
        generated_at=generated,
        confidence=confidence,
        confidence_factors=factors,
        source_hashes_value=source_hashes(
            users_registry=users_registry or [],
            service_matrix=service_matrix or {},
            quality_summary=quality_summary or {},
            service_preferences=service_preferences or {},
            trust_summary=trust_summary_snapshot or {},
            risk_summary=risk_summary_snapshot or {},
        ),
        content=rows,
        item_count=len(rows),
        warnings=warnings,
    )


def build_trust_snapshot(
    *,
    audit_records: list[dict[str, Any]] | None = None,
    switch_records: list[dict[str, Any]] | None = None,
    rollback_records: list[dict[str, Any]] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated = generated_at or now_iso()
    records = list(audit_records or []) + list(switch_records or []) + list(rollback_records or [])
    bounded = records[-MAX_HISTORY_RECORDS:]
    trust = ExecutionTrustModel.from_records(bounded)
    source_completeness = 1.0 if records else 0.0
    history_completeness = min(1.0, len(bounded) / 50.0)
    confidence, factors = confidence_from_factors(
        source_completeness=source_completeness,
        history_completeness=history_completeness,
        probe_completeness=1.0,
        service_completeness=1.0,
    )
    warnings = []
    if len(records) > len(bounded):
        warnings.append("history_records_truncated_to_bound")
    if not records:
        warnings.append("history_missing")
    content = [{
        "trust": trust,
        "records_seen": len(bounded),
        "records_available": len(records),
        "bounded": True,
        "runtime_decision_authority": "none_snapshot_only",
    }]
    return envelope(
        "trust-summaries",
        generated_at=generated,
        confidence=confidence,
        confidence_factors=factors,
        source_hashes_value=source_hashes(records=bounded),
        content=content,
        item_count=len(content),
        warnings=warnings,
    )


def build_risk_snapshot(
    *,
    service_scores_snapshot: dict[str, Any],
    channel_service_scores_snapshot: dict[str, Any],
    quality_summary: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated = generated_at or now_iso()
    channels = channel_service_scores_snapshot.get("items") or []
    service_rows = service_scores_snapshot.get("items") or []
    channel_scores = [as_float(row.get("aggregate_score"), 0.0) for row in channels if isinstance(row, dict)]
    service_scores = [as_float(row.get("average_score"), 0.0) for row in service_rows if isinstance(row, dict)]
    average_channel_score = mean(channel_scores, 0.0)
    average_service_score = mean(service_scores, average_channel_score)
    service_risk = round(clamp(100.0 - average_channel_score), 3)
    platform_health = round(clamp((average_channel_score * 0.7) + (average_service_score * 0.3)), 3)
    high_risk_channels = [
        row.get("channel")
        for row in channels
        if isinstance(row, dict) and (as_float(row.get("aggregate_score"), 0.0) < 50.0 or row.get("verdict") != "OK")
    ]
    source_confidence = mean([
        as_float(service_scores_snapshot.get("confidence"), 0.0),
        as_float(channel_service_scores_snapshot.get("confidence"), 0.0),
    ])
    confidence, factors = confidence_from_factors(
        source_completeness=1.0 if channels or service_rows else 0.0,
        history_completeness=1.0 if quality_summary else 0.5,
        probe_completeness=source_confidence,
        service_completeness=1.0 if service_rows else 0.0,
    )
    content = [{
        "service_risk": service_risk,
        "platform_health": platform_health,
        "average_channel_score": round(average_channel_score, 3),
        "average_service_score": round(average_service_score, 3),
        "high_risk_channels": high_risk_channels,
        "runtime_decision_authority": "none_snapshot_only",
    }]
    warnings = []
    if not channels:
        warnings.append("channel_service_scores_missing")
    return envelope(
        "risk-summaries",
        generated_at=generated,
        confidence=confidence,
        confidence_factors=factors,
        source_hashes_value=source_hashes(
            service_scores=service_scores_snapshot,
            channel_service_scores=channel_service_scores_snapshot,
            quality_summary=quality_summary or {},
        ),
        content=content,
        item_count=len(content),
        warnings=warnings,
    )


def build_blast_radius_snapshot(
    *,
    trust_summary_snapshot: dict[str, Any],
    risk_summary_snapshot: dict[str, Any],
    total_users: int,
    affected_candidates: int,
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated = generated_at or now_iso()
    trust_items = trust_summary_snapshot.get("items") or []
    risk_items = risk_summary_snapshot.get("items") or []
    trust_row = trust_items[0] if trust_items and isinstance(trust_items[0], dict) else {}
    risk_row = risk_items[0] if risk_items and isinstance(risk_items[0], dict) else {}
    trust = trust_row.get("trust") if isinstance(trust_row.get("trust"), dict) else {}
    recommendation = DynamicBlastRadiusModel.recommend(
        total_users=total_users,
        affected_users=affected_candidates,
        execution_trust=as_float(trust.get("score"), 0.0),
        service_risk=as_float(risk_row.get("service_risk"), 100.0),
        platform_health=as_float(risk_row.get("platform_health"), 0.0),
    )
    confidence, factors = confidence_from_factors(
        source_completeness=1.0 if trust_row and risk_row else 0.0,
        history_completeness=as_float(trust_summary_snapshot.get("confidence"), 0.0),
        probe_completeness=as_float(risk_summary_snapshot.get("confidence"), 0.0),
        service_completeness=1.0 if risk_row else 0.0,
    )
    content = [{
        "recommendation": recommendation,
        "total_users": total_users,
        "affected_candidates": affected_candidates,
        "runtime_decision_authority": "none_snapshot_only",
    }]
    return envelope(
        "blast-radius-summaries",
        generated_at=generated,
        confidence=confidence,
        confidence_factors=factors,
        source_hashes_value=source_hashes(trust_summary=trust_summary_snapshot, risk_summary=risk_summary_snapshot),
        content=content,
        item_count=len(content),
        warnings=[] if trust_row and risk_row else ["trust_or_risk_summary_missing"],
    )


def build_candidate_suitability_snapshot(
    *,
    service_matrix: dict[str, Any],
    quality_summary: dict[str, Any],
    service_preferences: dict[str, Any],
    users_registry: list[dict[str, Any]],
    egress_registry: list[dict[str, Any]],
    trust_summary_snapshot: dict[str, Any],
    risk_summary_snapshot: dict[str, Any],
    blast_radius_snapshot: dict[str, Any],
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated = generated_at or now_iso()
    active_users = [row for row in (users_registry or []) if user_enabled(row) and user_ip(row)]
    channels = [egress_id(row) for row in (egress_registry or []) if egress_id(row) and egress_available(row)]
    trust_items = trust_summary_snapshot.get("items") or []
    trust_row = trust_items[0] if trust_items and isinstance(trust_items[0], dict) else {}
    trust = trust_row.get("trust") if isinstance(trust_row.get("trust"), dict) else {}
    risk_items = risk_summary_snapshot.get("items") or []
    risk_row = risk_items[0] if risk_items and isinstance(risk_items[0], dict) else {}
    blast_items = blast_radius_snapshot.get("items") or []
    blast_row = blast_items[0] if blast_items and isinstance(blast_items[0], dict) else {}
    audit_seed = [{
        "result": "OK",
        "blast_radius": ((blast_row.get("recommendation") or {}).get("recommended_budget") if isinstance(blast_row.get("recommendation"), dict) else 1) or 1,
        "execution_trust_score": trust.get("score", 70.0),
    }] if trust else []
    brain = RoutingBrain(
        service_matrix=service_matrix or {},
        quality_summary=quality_summary or {},
        service_preferences=service_preferences or {},
        audit_records=audit_seed,
    )
    rows = []
    confidence_values: list[float] = []
    for user_row in active_users:
        uid = user_ip(user_row)
        advice = brain.candidate_suitability_advice(
            total_users=len(active_users),
            affected_users=len(channels),
            required_services=normalize_services((service_preferences or {}).get("required_services") or list(DEFAULT_SERVICES)),
            user_id=uid,
            candidate_targets=channels,
        )
        candidates = list(advice.get("candidates") or [])
        high_risk_channels = set(risk_row.get("high_risk_channels") or [])
        for candidate in candidates:
            channel = str(candidate.get("channel") or "")
            if channel in high_risk_channels:
                candidate["suitability_score"] = round(max(0.0, as_float(candidate.get("suitability_score")) - 7.0), 3)
                candidate.setdefault("reason_breakdown", {})["risk"] = round(as_float((candidate.get("reason_breakdown") or {}).get("risk")) - 7.0, 3)
                candidate.setdefault("explainability", []).append("risk_high_channel_penalty=-7")
            confidence_values.append(as_float(candidate.get("confidence"), 0.0))
        rows.append({
            "user": uid,
            "candidates": candidates,
            "candidate_count": len(candidates),
            "runtime_decision_authority": "none_snapshot_only",
        })
    warnings = []
    if not active_users:
        warnings.append("users_registry_missing_or_empty")
    if not channels:
        warnings.append("egress_registry_missing_or_no_available_channels")
    confidence, factors = confidence_from_factors(
        source_completeness=1.0 if active_users and channels else 0.0,
        history_completeness=mean([
            as_float(trust_summary_snapshot.get("confidence"), 0.0),
            as_float(risk_summary_snapshot.get("confidence"), 0.0),
            as_float(blast_radius_snapshot.get("confidence"), 0.0),
        ]),
        probe_completeness=mean(confidence_values, 0.0),
        service_completeness=1.0 if service_matrix else 0.0,
    )
    return envelope(
        "candidate-suitability-summary",
        generated_at=generated,
        confidence=confidence,
        confidence_factors=factors,
        source_hashes_value=source_hashes(
            users_registry=users_registry or [],
            egress_registry=egress_registry or [],
            service_matrix=service_matrix or {},
            quality_summary=quality_summary or {},
            service_preferences=service_preferences or {},
            trust_summary=trust_summary_snapshot,
            risk_summary=risk_summary_snapshot,
            blast_radius=blast_radius_snapshot,
        ),
        content=rows,
        item_count=len(rows),
        warnings=warnings,
    )


def build_best_available_pool_snapshot(
    *,
    candidate_suitability_snapshot: dict[str, Any],
    runtime_state: dict[str, Any],
    egress_registry: list[dict[str, Any]],
    pool_size: int = 3,
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated = generated_at or now_iso()
    egress_rows = {egress_id(row): row for row in (egress_registry or []) if egress_id(row)}
    egress_state = runtime_state.get("egress") if isinstance(runtime_state.get("egress"), dict) else {}
    rows = []
    for user_row in candidate_suitability_snapshot.get("items") or []:
        if not isinstance(user_row, dict):
            continue
        suitability_rows = []
        for candidate in user_row.get("candidates") or []:
            if not isinstance(candidate, dict):
                continue
            channel = str(candidate.get("channel") or "")
            reg = egress_rows.get(channel) or {}
            state = egress_state.get(channel) if isinstance(egress_state.get(channel), dict) else {}
            if not egress_available(reg):
                continue
            projected_users = as_float(state.get("users") or reg.get("users"), 0.0)
            hard_limit = max(1.0, as_float(reg.get("hard_limit") or reg.get("capacity") or 100.0, 100.0))
            capacity_penalty = max(0.0, (projected_users / hard_limit) - 0.8) * 50.0
            row = dict(candidate)
            row["suitability_score"] = round(max(0.0, as_float(row.get("suitability_score")) - capacity_penalty), 3)
            row.setdefault("reason_breakdown", {})["capacity"] = round(-capacity_penalty, 3)
            row.setdefault("explainability", []).append("capacity_constraints_considered")
            suitability_rows.append(row)
        pool = RoutingBrain.best_available_pool_advice(suitability_rows, pool_size=pool_size)
        rows.append({
            "user": user_row.get("user", ""),
            "pool": pool.get("pool", []),
            "pool_size": pool.get("pool_size", 0),
            "single_best_channel_authority": "none",
            "runtime_decision_authority": "none_snapshot_only",
        })
    warnings = []
    if not rows:
        warnings.append("candidate_suitability_missing_or_empty")
    confidence, factors = confidence_from_factors(
        source_completeness=1.0 if candidate_suitability_snapshot.get("items") else 0.0,
        history_completeness=as_float(candidate_suitability_snapshot.get("confidence"), 0.0),
        probe_completeness=1.0,
        service_completeness=1.0 if egress_registry else 0.0,
    )
    return envelope(
        "best-available-pool",
        generated_at=generated,
        confidence=confidence,
        confidence_factors=factors,
        source_hashes_value=source_hashes(
            candidate_suitability=candidate_suitability_snapshot,
            runtime_state=runtime_state or {},
            egress_registry=egress_registry or [],
        ),
        content=rows,
        item_count=len(rows),
        warnings=warnings,
    )


def build_prediction_snapshot(
    *,
    service_matrix: dict[str, Any],
    quality_summary: dict[str, Any],
    risk_summary_snapshot: dict[str, Any],
    trust_summary_snapshot: dict[str, Any],
    blast_radius_snapshot: dict[str, Any],
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated = generated_at or now_iso()
    history = ServiceHistoryStore.from_runtime_inputs(service_matrix or {}, quality_summary or {}, generated_at=generated)
    risk_items = risk_summary_snapshot.get("items") or []
    risk_row = risk_items[0] if risk_items and isinstance(risk_items[0], dict) else {}
    trust_items = trust_summary_snapshot.get("items") or []
    trust_row = trust_items[0] if trust_items and isinstance(trust_items[0], dict) else {}
    blast_items = blast_radius_snapshot.get("items") or []
    blast_row = blast_items[0] if blast_items and isinstance(blast_items[0], dict) else {}
    summary = PredictiveFoundation.prediction_summary(
        history,
        risk_summary=risk_row,
        trust_summary=trust_row,
        blast_radius_summary=blast_row,
    )
    channel_count = len(summary.get("channel_forecasts") or [])
    service_count = len(summary.get("service_forecasts") or [])
    warnings = []
    if not channel_count:
        warnings.append("channel_forecasts_missing")
    if not service_count:
        warnings.append("service_forecasts_missing")
    source_confidence = mean([
        as_float(risk_summary_snapshot.get("confidence"), 0.0),
        as_float(trust_summary_snapshot.get("confidence"), 0.0),
        as_float(blast_radius_snapshot.get("confidence"), 0.0),
        as_float(summary.get("confidence"), 0.0),
    ])
    confidence, factors = confidence_from_factors(
        source_completeness=1.0 if service_matrix else 0.0,
        history_completeness=1.0 if quality_summary else 0.5 if service_matrix else 0.0,
        probe_completeness=source_confidence,
        service_completeness=1.0 if service_count else 0.0,
    )
    payload = envelope(
        "prediction-summaries",
        generated_at=generated,
        confidence=confidence,
        confidence_factors=factors,
        source_hashes_value=source_hashes(
            service_matrix=service_matrix or {},
            quality_summary=quality_summary or {},
            risk_summary=risk_summary_snapshot or {},
            trust_summary=trust_summary_snapshot or {},
            blast_radius=blast_radius_snapshot or {},
        ),
        content=[summary],
        item_count=1 if summary else 0,
        warnings=warnings,
    )
    payload["metadata"] = {
        "prediction_architecture": PredictiveFoundation.architecture_model(),
        "model_governance": model_governance_framework(),
        "observability": observability_model(),
        "channel_forecast_count": channel_count,
        "service_forecast_count": service_count,
        "runtime_forecasting_performed": False,
    }
    return payload


def _prediction_forecast_rows(prediction_summary_snapshot: dict[str, Any] | None) -> list[dict[str, Any]]:
    items = (prediction_summary_snapshot or {}).get("items") or []
    summary = items[0] if items and isinstance(items[0], dict) else {}
    rows: list[dict[str, Any]] = []
    for row in summary.get("channel_forecasts") or []:
        if isinstance(row, dict):
            rows.append(row)
    for row in summary.get("service_forecasts") or []:
        if isinstance(row, dict):
            rows.append(row)
    return rows


def build_trust_evolution_snapshot(
    *,
    audit_records: list[dict[str, Any]] | None = None,
    switch_records: list[dict[str, Any]] | None = None,
    rollback_records: list[dict[str, Any]] | None = None,
    service_scores_snapshot: dict[str, Any],
    channel_service_scores_snapshot: dict[str, Any],
    trust_summary_snapshot: dict[str, Any],
    prediction_summary_snapshot: dict[str, Any],
    candidate_suitability_snapshot: dict[str, Any],
    best_available_pool_snapshot: dict[str, Any],
    blast_radius_snapshot: dict[str, Any],
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated = generated_at or now_iso()
    decision_records = list(audit_records or []) + list(switch_records or []) + list(rollback_records or [])
    bounded_decisions = decision_records[-MAX_HISTORY_RECORDS:]
    service_rows = list(service_scores_snapshot.get("items") or []) + list(channel_service_scores_snapshot.get("items") or [])
    prediction_forecasts = _prediction_forecast_rows(prediction_summary_snapshot)
    service_actuals = build_service_actual_rows(service_rows, bounded_decisions)
    prediction_actuals = build_prediction_actual_rows(prediction_forecasts, service_rows, bounded_decisions)
    candidate_rows = candidate_suitability_snapshot.get("items") or []
    candidate_outcomes = build_candidate_outcome_rows(candidate_rows, bounded_decisions)
    blast_items = blast_radius_snapshot.get("items") or []
    blast_row = blast_items[0] if blast_items and isinstance(blast_items[0], dict) else {}
    summary = trust_evolution_summary(
        decision_records=bounded_decisions,
        prediction_forecasts=prediction_forecasts,
        prediction_actuals=prediction_actuals,
        service_rows=service_rows,
        service_actuals=service_actuals,
        candidate_rows=candidate_rows,
        candidate_outcomes=candidate_outcomes,
        rollback_records=rollback_records or [],
        blast_radius_records=bounded_decisions,
        blast_radius_metrics=blast_row,
    )
    summary["channel_trust_recovery"] = build_channel_trust_recovery_model(
        channel_service_scores_snapshot=channel_service_scores_snapshot,
        candidate_suitability_snapshot=candidate_suitability_snapshot,
        best_available_pool_snapshot=best_available_pool_snapshot,
        decision_records=bounded_decisions,
    )
    summary["explainability_foundation"] = {
        "schema": "v7.intelligence.channel-explainability-foundation.v1",
        "owner": "admin_core.intelligence_workers.trust-evolution-summaries",
        "scope": "channel_trust_recovery_advisory_only",
        "generated_fields": [
            "channel.lifecycle",
            "channel.lifecycle_reason",
            "channel.trust_score",
            "channel.recovery",
            "channel.decay",
            "channel.routing_impact",
            "channel.explainability",
        ],
        "routing_behavior_changed": False,
        "runtime_decision_authority": "none_evidence_only",
    }
    summary["outcome_mapper_counts"] = {
        "prediction_actuals_count": len(prediction_actuals),
        "service_actuals_count": len(service_actuals),
        "candidate_outcomes_count": len(candidate_outcomes),
    }
    source_confidence = mean([
        as_float(service_scores_snapshot.get("confidence"), 0.0),
        as_float(channel_service_scores_snapshot.get("confidence"), 0.0),
        as_float(trust_summary_snapshot.get("confidence"), 0.0),
        as_float(prediction_summary_snapshot.get("confidence"), 0.0),
        as_float(candidate_suitability_snapshot.get("confidence"), 0.0),
        as_float(best_available_pool_snapshot.get("confidence"), 0.0),
        as_float(blast_radius_snapshot.get("confidence"), 0.0),
    ])
    confidence, factors = confidence_from_factors(
        source_completeness=1.0 if service_rows else 0.0,
        history_completeness=min(1.0, len(bounded_decisions) / 50.0) if bounded_decisions else 0.0,
        probe_completeness=source_confidence,
        service_completeness=1.0 if service_rows else 0.0,
    )
    summary["snapshot_confidence"] = confidence
    warnings = []
    if not bounded_decisions:
        warnings.append("decision_outcomes_missing")
    if summary["prediction_accuracy"]["validation_status"] == "LIVE_OUTCOME_REQUIRED":
        warnings.append("prediction_actual_outcomes_missing")
    if summary["suitability_trust"]["validation_status"] == "LIVE_OUTCOME_REQUIRED":
        warnings.append("candidate_outcomes_missing")
    return envelope(
        "trust-evolution-summaries",
        generated_at=generated,
        confidence=confidence,
        confidence_factors=factors,
        source_hashes_value=source_hashes(
            decisions=bounded_decisions,
            rollback_records=rollback_records or [],
            prediction_actuals=prediction_actuals,
            service_actuals=service_actuals,
            candidate_outcomes=candidate_outcomes,
            service_scores=service_scores_snapshot,
            channel_service_scores=channel_service_scores_snapshot,
            trust_summary=trust_summary_snapshot,
            prediction_summary=prediction_summary_snapshot,
            candidate_suitability=candidate_suitability_snapshot,
            best_available_pool=best_available_pool_snapshot,
            blast_radius=blast_radius_snapshot,
        ),
        content=[summary],
        item_count=1,
        warnings=warnings,
    )


def build_overview_snapshot(
    *,
    runtime_state: dict[str, Any],
    users_registry: list[dict[str, Any]],
    egress_registry: list[dict[str, Any]],
    snapshot_statuses: dict[str, dict[str, Any]],
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated = generated_at or now_iso()
    active_users = [row for row in users_registry if str(row.get("enabled", "1")) == "1"]
    egress_state = runtime_state.get("egress") if isinstance(runtime_state.get("egress"), dict) else {}
    ok_snapshots = [
        name for name, row in snapshot_statuses.items()
        if isinstance(row, dict) and row.get("freshness_state") == "FRESH" and row.get("runtime_behavior") in {"ALLOW", "WARN", "IGNORE"}
    ]
    summary = {
        "users_total": len(users_registry),
        "users_active": len(active_users),
        "egress_total": len(egress_registry),
        "runtime_egress_total": len(egress_state),
        "snapshot_families_seen": len(snapshot_statuses),
        "snapshot_families_fresh": len(ok_snapshots),
        "snapshot_statuses": snapshot_statuses,
        "runtime_decision_authority": "none_admin_snapshot_only",
    }
    confidence, factors = confidence_from_factors(
        source_completeness=1.0 if runtime_state else 0.0,
        history_completeness=1.0,
        probe_completeness=len(ok_snapshots) / max(1, len(snapshot_statuses)) if snapshot_statuses else 0.5,
        service_completeness=1.0 if egress_registry else 0.5,
    )
    return envelope(
        "overview-summary",
        generated_at=generated,
        confidence=confidence,
        confidence_factors=factors,
        source_hashes_value=source_hashes(
            runtime_state=runtime_state,
            users_registry=users_registry,
            egress_registry=egress_registry,
            snapshot_statuses=snapshot_statuses,
        ),
        content=summary,
        item_count=1,
        warnings=[] if runtime_state else ["runtime_state_missing"],
    )


def build_all_snapshots(
    *,
    service_matrix: dict[str, Any],
    quality_summary: dict[str, Any],
    service_preferences: dict[str, Any],
    audit_records: list[dict[str, Any]] | None = None,
    switch_records: list[dict[str, Any]] | None = None,
    rollback_records: list[dict[str, Any]] | None = None,
    runtime_state: dict[str, Any] | None = None,
    users_registry: list[dict[str, Any]] | None = None,
    egress_registry: list[dict[str, Any]] | None = None,
    total_users: int = 0,
    affected_candidates: int = 0,
    generated_at: str | None = None,
) -> WorkerRunResult:
    started = perf_counter()
    generated = generated_at or now_iso()
    warnings: list[str] = []
    snapshots = build_service_score_snapshots(
        service_matrix=service_matrix,
        quality_summary=quality_summary,
        service_preferences=service_preferences,
        generated_at=generated,
    )
    trust = build_trust_snapshot(
        audit_records=audit_records or [],
        switch_records=switch_records or [],
        rollback_records=rollback_records or [],
        generated_at=generated,
    )
    snapshots["trust-summaries"] = trust
    risk = build_risk_snapshot(
        service_scores_snapshot=snapshots["service-scores"],
        channel_service_scores_snapshot=snapshots["channel-service-scores"],
        quality_summary=quality_summary,
        generated_at=generated,
    )
    snapshots["risk-summaries"] = risk
    snapshots["blast-radius-summaries"] = build_blast_radius_snapshot(
        trust_summary_snapshot=trust,
        risk_summary_snapshot=risk,
        total_users=total_users or len(users_registry or []),
        affected_candidates=affected_candidates,
        generated_at=generated,
    )
    snapshots["user-service-scores"] = build_user_service_scores_snapshot(
        service_matrix=service_matrix,
        quality_summary=quality_summary,
        service_preferences=service_preferences,
        users_registry=users_registry or [],
        trust_summary_snapshot=trust,
        risk_summary_snapshot=risk,
        generated_at=generated,
    )
    snapshots["candidate-suitability-summary"] = build_candidate_suitability_snapshot(
        service_matrix=service_matrix,
        quality_summary=quality_summary,
        service_preferences=service_preferences,
        users_registry=users_registry or [],
        egress_registry=egress_registry or [],
        trust_summary_snapshot=trust,
        risk_summary_snapshot=risk,
        blast_radius_snapshot=snapshots["blast-radius-summaries"],
        generated_at=generated,
    )
    snapshots["best-available-pool"] = build_best_available_pool_snapshot(
        candidate_suitability_snapshot=snapshots["candidate-suitability-summary"],
        runtime_state=runtime_state or {},
        egress_registry=egress_registry or [],
        generated_at=generated,
    )
    snapshots["prediction-summaries"] = build_prediction_snapshot(
        service_matrix=service_matrix,
        quality_summary=quality_summary,
        risk_summary_snapshot=risk,
        trust_summary_snapshot=trust,
        blast_radius_snapshot=snapshots["blast-radius-summaries"],
        generated_at=generated,
    )
    snapshots["trust-evolution-summaries"] = build_trust_evolution_snapshot(
        audit_records=audit_records or [],
        switch_records=switch_records or [],
        rollback_records=rollback_records or [],
        service_scores_snapshot=snapshots["service-scores"],
        channel_service_scores_snapshot=snapshots["channel-service-scores"],
        trust_summary_snapshot=trust,
        prediction_summary_snapshot=snapshots["prediction-summaries"],
        candidate_suitability_snapshot=snapshots["candidate-suitability-summary"],
        best_available_pool_snapshot=snapshots["best-available-pool"],
        blast_radius_snapshot=snapshots["blast-radius-summaries"],
        generated_at=generated,
    )
    snapshot_statuses = {
        name: {
            "schema": payload.get("schema"),
            "freshness_state": payload.get("freshness_state"),
            "confidence": payload.get("confidence"),
            "runtime_behavior": "ALLOW",
            "warnings": payload.get("warnings", []),
        }
        for name, payload in snapshots.items()
    }
    snapshots["overview-summary"] = build_overview_snapshot(
        runtime_state=runtime_state or {},
        users_registry=users_registry or [],
        egress_registry=egress_registry or [],
        snapshot_statuses=snapshot_statuses,
        generated_at=generated,
    )
    for name, payload in snapshots.items():
        validation = validate_snapshot(payload, name)
        if not validation.ok:
            warnings.extend(f"{name}:{error}" for error in validation.errors)
    elapsed_ms = round((perf_counter() - started) * 1000.0, 3)
    sizes = {name: len(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")) for name, payload in snapshots.items()}
    return WorkerRunResult(
        snapshots=snapshots,
        metrics={
            "elapsed_ms": elapsed_ms,
            "snapshot_count": len(snapshots),
            "snapshot_sizes": sizes,
            "total_snapshot_bytes": sum(sizes.values()),
            "max_snapshot_bytes": max(sizes.values()) if sizes else 0,
        },
        warnings=warnings,
    )


def write_snapshots(root: Path | str, snapshots: dict[str, dict[str, Any]]) -> dict[str, str]:
    written: dict[str, str] = {}
    for name, payload in snapshots.items():
        if name not in SNAPSHOT_FAMILIES:
            continue
        path = snapshot_path(root, name)
        write_json_atomic(path, payload)
        written[name] = str(path)
    return written
