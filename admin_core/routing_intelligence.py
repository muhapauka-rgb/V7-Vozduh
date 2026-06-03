"""Read-only Routing Intelligence foundation for V7.

This module builds intelligence read models from existing runtime truth inputs.
The runtime planner may consume it only through the bounded RI.3 advisory
contract. It must not mutate route state, governance state, users, services, or
runtime files.
"""

from __future__ import annotations

import hashlib
import json
import math
import statistics
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_SERVICES = (
    "telegram",
    "youtube",
    "instagram",
    "chatgpt",
    "google",
    "google_auth",
)
HISTORY_WINDOWS = ("1h", "24h", "7d", "30d")
SERVICE_HISTORY_SCHEMA = "ri1.service-history.v1"
USER_WEIGHTS_SCHEMA = "ri1.user-service-weights.v1"
SHADOW_SCHEMA = "ri1.shadow-replay.v1"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "ok", "up"}


def normalize_service_id(value: Any) -> str:
    return str(value or "").strip().lower().replace("-", "_")


def normalize_services(values: Any) -> list[str]:
    if values is None:
        return []
    if isinstance(values, str):
        parts = values.replace(",", " ").split()
    elif isinstance(values, dict):
        parts = values.keys()
    else:
        parts = values
    out: list[str] = []
    seen = set()
    for item in parts:
        service = normalize_service_id(item)
        if service and service not in seen:
            seen.add(service)
            out.append(service)
    return out


def read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except (FileNotFoundError, OSError):
        return rows
    for line in lines:
        text = line.strip()
        if not text:
            continue
        try:
            row = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def sha256_json(payload: Any) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def parse_ts(value: Any) -> float | None:
    if not value:
        return None
    try:
        text = str(value).replace("Z", "+00:00")
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()
    except (TypeError, ValueError):
        return None


def freshness_seconds(*values: Any, now: float | None = None) -> int:
    now_ts = time.time() if now is None else now
    timestamps = [parse_ts(value) for value in values]
    timestamps = [item for item in timestamps if item is not None]
    if not timestamps:
        return 0
    return max(0, int(now_ts - max(timestamps)))


def _latency_ms(row: dict[str, Any]) -> float:
    seconds = as_float(row.get("first_byte_sec") or row.get("total_sec") or row.get("latency_sec"), 0.0)
    if seconds:
        return seconds * 1000.0
    return as_float(row.get("latency_ms"), 0.0)


def _status_available(row: dict[str, Any]) -> bool:
    status = str(row.get("status") or row.get("state") or "").upper()
    if "ok" in row:
        return boolish(row.get("ok"))
    return status in {"OK", "UP", "WARN", "WARNING", "DEGRADED"}


def _window_metric(row: dict[str, Any], quality: dict[str, Any], metric: str, default: float) -> float:
    if metric == "throughput_mbps":
        return as_float(row.get("throughput_mbps") or quality.get("avg_mbps") or quality.get("mbps"), default)
    if metric == "error_rate":
        if row.get("error_rate") is not None:
            return clamp(as_float(row.get("error_rate"), default), 0.0, 1.0)
        fail_rate = as_float(quality.get("fail_rate"), default)
        return clamp(fail_rate, 0.0, 1.0)
    if metric == "stability":
        return clamp(as_float(row.get("stability") or quality.get("stability"), default), 0.0, 1.0)
    return default


@dataclass
class ServiceHistoryStore:
    """Non-authoritative RI.1 service history read model."""

    services: dict[str, dict[str, Any]] = field(default_factory=dict)
    sources: dict[str, str] = field(default_factory=dict)
    generated_at: str = field(default_factory=now_iso)
    schema_version: str = SERVICE_HISTORY_SCHEMA

    @classmethod
    def from_runtime_inputs(
        cls,
        service_matrix: dict[str, Any] | None,
        quality_summary: dict[str, Any] | None = None,
        generated_at: str | None = None,
    ) -> "ServiceHistoryStore":
        matrix_items = ((service_matrix or {}).get("items") or {})
        quality_items = ((quality_summary or {}).get("items") or {})
        store = cls(generated_at=generated_at or now_iso())
        observed_services = set(DEFAULT_SERVICES)
        for target in matrix_items.values():
            observed_services.update(normalize_services((target or {}).get("services") or {}))
        for target_id, target in matrix_items.items():
            target_services = (target or {}).get("services") or {}
            quality_windows = ((quality_items.get(target_id) or {}).get("windows") or {})
            for service in sorted(observed_services):
                row = target_services.get(service) or {}
                service_id = normalize_service_id(service)
                target_model = store.services.setdefault(service_id, {"targets": {}})["targets"].setdefault(
                    str(target_id),
                    {"windows": {}},
                )
                for window in HISTORY_WINDOWS:
                    qrow = quality_windows.get(window) or quality_windows.get("1h") or {}
                    available = _status_available(row) if row else False
                    status = str(row.get("status") or ("OK" if available else "UNKNOWN")).upper()
                    row_score = as_float(row.get("score"), 85.0 if available else 0.0)
                    latency_ms = _latency_ms(row)
                    confidence = clamp(
                        as_float(row.get("confidence"), (row_score / 100.0) if row else 0.0),
                        0.0,
                        1.0,
                    )
                    if row and available and confidence == 0.0:
                        confidence = 0.5
                    error_rate = _window_metric(row, qrow, "error_rate", 0.0 if available else 1.0)
                    stability = _window_metric(row, qrow, "stability", 0.8 if available else 0.0)
                    throughput = _window_metric(row, qrow, "throughput_mbps", 0.0)
                    freshness = freshness_seconds(
                        row.get("updated"),
                        row.get("checked_at"),
                        (service_matrix or {}).get("updated"),
                        (quality_summary or {}).get("updated"),
                    )
                    target_model["windows"][window] = {
                        "availability": available,
                        "status": status,
                        "latency_ms": round(latency_ms, 3),
                        "throughput_mbps": round(throughput, 3),
                        "error_rate": round(error_rate, 4),
                        "stability": round(stability, 4),
                        "confidence": round(confidence, 4),
                        "freshness_seconds": freshness,
                        "sample_count": as_int(row.get("sample_count") or qrow.get("samples"), 1 if row else 0),
                    }
        store.sources = {
            "service_matrix_hash": sha256_json(service_matrix or {}),
            "quality_summary_hash": sha256_json(quality_summary or {}),
            "authoritative_runtime_truth": "false_shadow_read_model_only",
        }
        return store

    @classmethod
    def load(cls, path: Path) -> "ServiceHistoryStore":
        data = read_json(path, {})
        return cls(
            services=data.get("services") or {},
            sources=data.get("sources") or {},
            generated_at=data.get("generated_at") or now_iso(),
            schema_version=data.get("schema_version") or SERVICE_HISTORY_SCHEMA,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "sources": self.sources,
            "services": self.services,
        }

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def metric(self, service: str, target_id: str, window: str = "1h") -> dict[str, Any]:
        return (
            ((self.services.get(normalize_service_id(service)) or {}).get("targets") or {})
            .get(str(target_id), {})
            .get("windows", {})
            .get(window, {})
        )


class ServiceIntelligenceEngine:
    """Converts service history into RI.1 suitability scores."""

    def __init__(self, history: ServiceHistoryStore):
        self.history = history

    def score_service(self, service: str, target_id: str, window: str = "1h") -> dict[str, Any]:
        metric = self.history.metric(service, target_id, window)
        if not metric:
            return {
                "service": normalize_service_id(service),
                "target": str(target_id),
                "window": window,
                "score": 0.0,
                "status": "UNKNOWN",
                "confidence": 0.0,
                "explainability": ["service_history_missing"],
            }
        availability = 45.0 if metric.get("availability") else 0.0
        latency = as_float(metric.get("latency_ms"), 0.0)
        latency_score = 20.0 if latency <= 0 else 20.0 * clamp(1.0 - (latency / 5000.0), 0.0, 1.0)
        throughput = as_float(metric.get("throughput_mbps"), 0.0)
        throughput_score = 10.0 * clamp(throughput / 50.0, 0.0, 1.0)
        error_score = 10.0 * (1.0 - clamp(as_float(metric.get("error_rate"), 1.0), 0.0, 1.0))
        stability_score = 10.0 * clamp(as_float(metric.get("stability"), 0.0), 0.0, 1.0)
        confidence_score = 3.0 * clamp(as_float(metric.get("confidence"), 0.0), 0.0, 1.0)
        freshness = as_int(metric.get("freshness_seconds"), 0)
        freshness_score = 2.0 if freshness == 0 or freshness <= 900 else (1.0 if freshness <= 3600 else 0.0)
        score = clamp(availability + latency_score + throughput_score + error_score + stability_score + confidence_score + freshness_score)
        explainability = [
            f"availability={'ok' if metric.get('availability') else 'not_ok'}",
            f"latency_ms={round(latency, 3)}",
            f"throughput_mbps={round(throughput, 3)}",
            f"error_rate={metric.get('error_rate')}",
            f"stability={metric.get('stability')}",
            f"confidence={metric.get('confidence')}",
            f"freshness_seconds={freshness}",
        ]
        if score < 50:
            explainability.append("score_below_foundation_floor")
        return {
            "service": normalize_service_id(service),
            "target": str(target_id),
            "window": window,
            "score": round(score, 3),
            "status": metric.get("status", "UNKNOWN"),
            "confidence": metric.get("confidence", 0.0),
            "explainability": explainability,
        }

    def score_target(
        self,
        target_id: str,
        required_services: list[str] | None = None,
        service_weights: dict[str, float] | None = None,
        window: str = "1h",
    ) -> dict[str, Any]:
        services = normalize_services(required_services) or sorted(self.history.services.keys())
        weights = service_weights or {}
        normalized_weights = normalize_weights({service: weights.get(service, 1.0) for service in services})
        per_service = [self.score_service(service, target_id, window) for service in services]
        aggregate = 0.0
        required_missing = []
        required_low = []
        for item in per_service:
            service = item["service"]
            aggregate += as_float(item["score"]) * (normalized_weights.get(service, 0.0) / 100.0)
            if "service_history_missing" in item["explainability"]:
                required_missing.append(service)
            elif as_float(item["score"]) < 50.0:
                required_low.append(service)
        verdict = "OK"
        if required_missing:
            verdict = "REVIEW_REQUIRED_MISSING_SERVICE_HISTORY"
        elif required_low:
            verdict = "REVIEW_REQUIRED_LOW_SERVICE_SCORE"
        return {
            "target": str(target_id),
            "window": window,
            "aggregate_score": round(clamp(aggregate), 3),
            "verdict": verdict,
            "weights": normalized_weights,
            "per_service": per_service,
            "required_missing": required_missing,
            "required_low": required_low,
            "runtime_decision_authority": "none_shadow_only",
        }

    def score_all_targets(
        self,
        required_services: list[str] | None = None,
        service_weights: dict[str, float] | None = None,
        window: str = "1h",
    ) -> dict[str, Any]:
        targets = set()
        for service in self.history.services.values():
            targets.update((service.get("targets") or {}).keys())
        return {
            target: self.score_target(target, required_services=required_services, service_weights=service_weights, window=window)
            for target in sorted(targets)
        }


def normalize_weights(weights: dict[str, Any]) -> dict[str, float]:
    cleaned: dict[str, float] = {}
    for service, value in (weights or {}).items():
        service_id = normalize_service_id(service)
        amount = max(0.0, as_float(value, 0.0))
        if service_id and amount > 0.0:
            cleaned[service_id] = amount
    total = sum(cleaned.values())
    if not total:
        services = sorted(cleaned.keys()) if cleaned else list(DEFAULT_SERVICES)
        equal = 100.0 / len(services)
        return {service: round(equal, 3) for service in services}
    return {service: round((value / total) * 100.0, 3) for service, value in sorted(cleaned.items())}


@dataclass
class UserServiceWeights:
    users: dict[str, dict[str, float]] = field(default_factory=dict)
    defaults: dict[str, float] = field(default_factory=dict)
    schema_version: str = USER_WEIGHTS_SCHEMA

    @classmethod
    def from_service_preferences(cls, prefs: dict[str, Any] | None, default_services: list[str] | None = None) -> "UserServiceWeights":
        data = prefs or {}
        defaults = normalize_weights(data.get("weights") or data.get("default_weights") or {service: 1 for service in (default_services or DEFAULT_SERVICES)})
        users: dict[str, dict[str, float]] = {}
        for user_id, row in ((data.get("users") or {}).items()):
            if not isinstance(row, dict):
                continue
            weights = row.get("weights") or row.get("service_weights")
            if not weights:
                weights = {service: weight for service, weight in row.items() if service not in {"required_services", "priority_services"}}
            if row.get("priority_services") and not weights:
                services = normalize_services(row.get("priority_services"))
                weights = {service: 1 for service in services}
            users[str(user_id)] = normalize_weights(weights or defaults)
        return cls(users=users, defaults=defaults)

    def for_user(self, user_id: str, required_services: list[str] | None = None) -> dict[str, float]:
        if user_id in self.users:
            return self.users[user_id]
        if required_services:
            return normalize_weights({service: self.defaults.get(service, 1.0) for service in normalize_services(required_services)})
        return dict(self.defaults)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "defaults": self.defaults,
            "users": self.users,
            "runtime_decision_authority": "none_shadow_only",
        }


class ExecutionTrustModel:
    """Scores historical execution safety for future blast-radius intelligence."""

    @staticmethod
    def from_records(records: list[dict[str, Any]]) -> dict[str, Any]:
        counters = {
            "successful_executions": 0,
            "successful_rollbacks": 0,
            "failed_executions": 0,
            "failed_rollbacks": 0,
            "governance_violations": 0,
            "blast_radius_expansions": 0,
            "records_seen": len(records),
        }
        blast_values: list[int] = []
        for record in records:
            text = json.dumps(record, ensure_ascii=False, sort_keys=True).lower()
            result = str(record.get("result") or record.get("status") or record.get("terminal_state") or "").lower()
            record_type = str(record.get("record_type") or record.get("action") or "").lower()
            if "rollback" in text:
                if any(token in text for token in ("rollback_executed=true", "rollback_success", "rollback_performed", "rollback_result_ok")) or result in {"rollback_success", "rolled_back", "ok"}:
                    counters["successful_rollbacks"] += 1
                elif any(token in text for token in ("rollback_failed", "failed_rollback")):
                    counters["failed_rollbacks"] += 1
            if result in {"ok", "success", "executed", "approved", "completed"} or "success" in result:
                counters["successful_executions"] += 1
            if result in {"fail", "failed", "error", "denied"} or "failed" in result or "error" in result:
                counters["failed_executions"] += 1
            if "governance_violation" in text or "scope_expands" in text or "deny_packet_invalid" in text:
                counters["governance_violations"] += 1
            blast = record.get("blast_radius") or record.get("effective_blast_radius")
            if isinstance(blast, dict):
                blast = blast.get("effective") or blast.get("users") or blast.get("selected_move_count")
            blast_int = as_int(blast, 0)
            if blast_int:
                blast_values.append(blast_int)
            if "blast_radius_violation" in text or "scope_expanded" in text:
                counters["blast_radius_expansions"] += 1
            if record_type == "replay_denial":
                counters["governance_violations"] += 0
        score = 70.0
        score += min(counters["successful_executions"], 20) * 1.0
        score += min(counters["successful_rollbacks"], 10) * 1.0
        score -= counters["failed_executions"] * 10.0
        score -= counters["failed_rollbacks"] * 15.0
        score -= counters["governance_violations"] * 20.0
        score -= counters["blast_radius_expansions"] * 20.0
        median_blast = statistics.median(blast_values) if blast_values else 0
        if median_blast > 10:
            score -= 5.0
        explanation = [
            f"records_seen={counters['records_seen']}",
            f"successful_executions={counters['successful_executions']}",
            f"successful_rollbacks={counters['successful_rollbacks']}",
            f"failed_executions={counters['failed_executions']}",
            f"failed_rollbacks={counters['failed_rollbacks']}",
            f"governance_violations={counters['governance_violations']}",
            f"blast_radius_expansions={counters['blast_radius_expansions']}",
            f"median_blast_radius={median_blast}",
        ]
        return {
            "score": round(clamp(score), 3),
            "counters": counters,
            "median_blast_radius": median_blast,
            "explainability": explanation,
            "runtime_decision_authority": "none_shadow_only",
        }

    @staticmethod
    def from_jsonl_paths(paths: list[Path]) -> dict[str, Any]:
        records: list[dict[str, Any]] = []
        for path in paths:
            records.extend(read_jsonl(path))
        return ExecutionTrustModel.from_records(records)


class DynamicBlastRadiusModel:
    """Foundation-only recommendation model for future governed use."""

    @staticmethod
    def recommend(
        total_users: int,
        affected_users: int,
        execution_trust: float,
        service_risk: float,
        platform_health: float,
    ) -> dict[str, Any]:
        total = max(0, as_int(total_users, 0))
        affected = max(0, as_int(affected_users, 0))
        trust = clamp(as_float(execution_trust), 0.0, 100.0)
        risk = clamp(as_float(service_risk), 0.0, 100.0)
        health = clamp(as_float(platform_health), 0.0, 100.0)
        if total == 0 or affected == 0:
            budget = 0
            reason = "no_affected_users"
        elif trust < 50 or health < 50 or risk > 80:
            budget = 1
            reason = "conservative_low_trust_or_high_risk"
        else:
            trust_ratio = trust / 100.0
            health_ratio = health / 100.0
            risk_ratio = 1.0 - (risk / 100.0)
            ratio = clamp(0.05 + (0.25 * trust_ratio * health_ratio * risk_ratio), 0.01, 0.30)
            budget = max(1, math.ceil(total * ratio))
            budget = min(budget, affected, 25)
            reason = "foundation_recommendation_shadow_only"
        return {
            "recommended_budget": budget,
            "reason": reason,
            "inputs": {
                "total_users": total,
                "affected_users": affected,
                "execution_trust": round(trust, 3),
                "service_risk": round(risk, 3),
                "platform_health": round(health, 3),
            },
            "runtime_decision_authority": "none_shadow_only",
        }


class PredictiveFoundation:
    """Disabled prediction scaffolding and trend examples."""

    @staticmethod
    def analyze_service_trends(history: ServiceHistoryStore) -> dict[str, Any]:
        examples = []
        for service_id, service in sorted(history.services.items()):
            for target_id, target in sorted((service.get("targets") or {}).items()):
                windows = target.get("windows") or {}
                one = windows.get("1h") or {}
                day = windows.get("24h") or {}
                week = windows.get("7d") or {}
                score_now = _raw_health_score(one)
                baseline_values = [_raw_health_score(item) for item in (day, week) if item]
                baseline = statistics.mean(baseline_values) if baseline_values else score_now
                trend = "stable"
                if score_now + 10 < baseline:
                    trend = "degrading"
                elif score_now > baseline + 10:
                    trend = "improving"
                examples.append(
                    {
                        "service": service_id,
                        "target": target_id,
                        "trend": trend,
                        "current_health": round(score_now, 3),
                        "baseline_health": round(baseline, 3),
                    }
                )
        return {
            "prediction_enabled": False,
            "model_status": "storage_and_examples_only",
            "examples": examples,
            "runtime_decision_authority": "none_shadow_only",
        }


def _raw_health_score(metric: dict[str, Any]) -> float:
    if not metric:
        return 0.0
    score = 0.0
    score += 45.0 if metric.get("availability") else 0.0
    score += 20.0 * clamp(as_float(metric.get("confidence")), 0.0, 1.0)
    score += 20.0 * clamp(as_float(metric.get("stability")), 0.0, 1.0)
    score += 15.0 * (1.0 - clamp(as_float(metric.get("error_rate"), 1.0), 0.0, 1.0))
    return clamp(score)


class RoutingIntelligenceShadow:
    """End-to-end RI.1 shadow replay wrapper."""

    @staticmethod
    def replay(
        service_matrix: dict[str, Any] | None,
        quality_summary: dict[str, Any] | None = None,
        service_preferences: dict[str, Any] | None = None,
        audit_records: list[dict[str, Any]] | None = None,
        total_users: int = 0,
        affected_users: int = 0,
        required_services: list[str] | None = None,
    ) -> dict[str, Any]:
        history = ServiceHistoryStore.from_runtime_inputs(service_matrix or {}, quality_summary or {})
        weights = UserServiceWeights.from_service_preferences(service_preferences or {}, required_services or list(DEFAULT_SERVICES))
        required = normalize_services(required_services or (service_preferences or {}).get("required_services") or list(DEFAULT_SERVICES))
        engine = ServiceIntelligenceEngine(history)
        service_scores = engine.score_all_targets(required_services=required, service_weights=weights.defaults)
        trust = ExecutionTrustModel.from_records(audit_records or [])
        aggregate_scores = [as_float(row.get("aggregate_score")) for row in service_scores.values()]
        average_score = statistics.mean(aggregate_scores) if aggregate_scores else 0.0
        service_risk = clamp(100.0 - average_score)
        platform_health = clamp(average_score)
        blast = DynamicBlastRadiusModel.recommend(
            total_users=total_users,
            affected_users=affected_users,
            execution_trust=as_float(trust.get("score")),
            service_risk=service_risk,
            platform_health=platform_health,
        )
        prediction = PredictiveFoundation.analyze_service_trends(history)
        return {
            "schema_version": SHADOW_SCHEMA,
            "generated_at": now_iso(),
            "mode": "shadow_read_only",
            "non_authority_guards": {
                "no_runtime_mutation": True,
                "no_routing_decision_change": True,
                "no_user_movement": True,
                "no_governance_change": True,
            },
            "history": history.to_dict(),
            "user_service_weights": weights.to_dict(),
            "service_intelligence_scores": service_scores,
            "execution_trust": trust,
            "dynamic_blast_radius_recommendation": blast,
            "predictive_foundation": prediction,
        }
