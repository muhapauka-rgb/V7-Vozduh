"""Read-only Intelligence Snapshot Store contracts for V7.

Brain computes snapshots. Runtime reads snapshots. This module defines the
contract between those layers without integrating snapshots into planner,
governance, execution, or admin mutation behavior.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CANONICAL_SNAPSHOT_ROOT = Path("/opt/v7/egress/state/intelligence")
SNAPSHOT_SCHEMA_VERSION = "v7.intelligence-snapshot-envelope.v1"
MAX_SNAPSHOT_BYTES = 1_000_000
FRESHNESS_STATES = ("FRESH", "STALE", "EXPIRED", "UNKNOWN")
RUNTIME_BEHAVIORS = ("ALLOW", "WARN", "IGNORE", "STOP")


@dataclass(frozen=True)
class SnapshotFamily:
    name: str
    filename: str
    schema: str
    producer: str
    consumer: str
    ttl_seconds: int
    stale_after_seconds: int
    runtime_requirement: str
    stale_runtime_behavior: str
    confidence_floor: float
    item_key: str = "items"
    retention: str = "latest_plus_24h_archive"


@dataclass(frozen=True)
class SnapshotValidation:
    ok: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SnapshotReadResult:
    family: str
    path: str
    exists: bool
    payload: dict[str, Any]
    validation: SnapshotValidation
    freshness_state: str
    confidence: float
    runtime_behavior: str
    stop_required: bool


SNAPSHOT_FAMILIES: dict[str, SnapshotFamily] = {
    "service-scores": SnapshotFamily(
        name="service-scores",
        filename="service-scores.json",
        schema="v7.intelligence.service-scores.v1",
        producer="PERF.3 service score worker",
        consumer="runtime planner advisory reader",
        ttl_seconds=120,
        stale_after_seconds=60,
        runtime_requirement="required_for_service_aware_apply",
        stale_runtime_behavior="WARN",
        confidence_floor=0.65,
    ),
    "channel-service-scores": SnapshotFamily(
        name="channel-service-scores",
        filename="channel-service-scores.json",
        schema="v7.intelligence.channel-service-scores.v1",
        producer="PERF.3 service score worker",
        consumer="runtime planner channel ranking reader",
        ttl_seconds=120,
        stale_after_seconds=60,
        runtime_requirement="required_for_service_aware_apply",
        stale_runtime_behavior="WARN",
        confidence_floor=0.65,
    ),
    "user-service-scores": SnapshotFamily(
        name="user-service-scores",
        filename="user-service-scores.json",
        schema="v7.intelligence.user-service-scores.v1",
        producer="PERF.3 user service weight worker",
        consumer="runtime planner advisory reader",
        ttl_seconds=600,
        stale_after_seconds=300,
        runtime_requirement="advisory_only",
        stale_runtime_behavior="IGNORE",
        confidence_floor=0.50,
    ),
    "risk-summaries": SnapshotFamily(
        name="risk-summaries",
        filename="risk-summaries.json",
        schema="v7.intelligence.risk-summaries.v1",
        producer="PERF.3 risk worker",
        consumer="runtime planner risk guard",
        ttl_seconds=120,
        stale_after_seconds=60,
        runtime_requirement="required_for_intelligence_apply",
        stale_runtime_behavior="STOP",
        confidence_floor=0.70,
    ),
    "trust-summaries": SnapshotFamily(
        name="trust-summaries",
        filename="trust-summaries.json",
        schema="v7.intelligence.trust-summaries.v1",
        producer="PERF.3 audit trust aggregation worker",
        consumer="runtime planner trust guard",
        ttl_seconds=600,
        stale_after_seconds=300,
        runtime_requirement="required_for_intelligence_apply",
        stale_runtime_behavior="STOP",
        confidence_floor=0.70,
    ),
    "blast-radius-summaries": SnapshotFamily(
        name="blast-radius-summaries",
        filename="blast-radius-summaries.json",
        schema="v7.intelligence.blast-radius-summaries.v1",
        producer="PERF.3 risk/trust worker",
        consumer="runtime planner blast radius guard",
        ttl_seconds=120,
        stale_after_seconds=60,
        runtime_requirement="required_for_intelligence_apply",
        stale_runtime_behavior="STOP",
        confidence_floor=0.70,
    ),
    "candidate-suitability-summary": SnapshotFamily(
        name="candidate-suitability-summary",
        filename="candidate-suitability-summary.json",
        schema="v7.intelligence.candidate-suitability-summary.v1",
        producer="RI4.B candidate suitability worker",
        consumer="runtime planner advisory reader",
        ttl_seconds=120,
        stale_after_seconds=60,
        runtime_requirement="advisory_only",
        stale_runtime_behavior="IGNORE",
        confidence_floor=0.55,
    ),
    "best-available-pool": SnapshotFamily(
        name="best-available-pool",
        filename="best-available-pool.json",
        schema="v7.intelligence.best-available-pool.v1",
        producer="RI4.B best available pool worker",
        consumer="runtime planner advisory reader",
        ttl_seconds=120,
        stale_after_seconds=60,
        runtime_requirement="advisory_only",
        stale_runtime_behavior="IGNORE",
        confidence_floor=0.55,
    ),
    "capacity-forecast-summaries": SnapshotFamily(
        name="capacity-forecast-summaries",
        filename="capacity-forecast-summaries.json",
        schema="v7.intelligence.capacity-forecast-summaries.v1",
        producer="PERF.3 capacity worker",
        consumer="runtime planner capacity guard",
        ttl_seconds=600,
        stale_after_seconds=300,
        runtime_requirement="required_for_capacity_apply",
        stale_runtime_behavior="WARN",
        confidence_floor=0.60,
    ),
    "prediction-summaries": SnapshotFamily(
        name="prediction-summaries",
        filename="prediction-summaries.json",
        schema="v7.intelligence.prediction-summaries.v1",
        producer="PERF.3 predictive worker",
        consumer="runtime planner advisory reader",
        ttl_seconds=900,
        stale_after_seconds=600,
        runtime_requirement="advisory_only",
        stale_runtime_behavior="IGNORE",
        confidence_floor=0.50,
    ),
    "overview-summary": SnapshotFamily(
        name="overview-summary",
        filename="overview-summary.json",
        schema="v7.intelligence.overview-summary.v1",
        producer="PERF.3 admin performance worker",
        consumer="admin API overview reader",
        ttl_seconds=60,
        stale_after_seconds=30,
        runtime_requirement="admin_only",
        stale_runtime_behavior="IGNORE",
        confidence_floor=0.50,
        item_key="summary",
        retention="latest_plus_1h_archive",
    ),
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_iso(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        text = str(value).replace("Z", "+00:00")
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def iso_after(value: str, seconds: int) -> str:
    parsed = parse_iso(value)
    if parsed is None:
        return ""
    return datetime.fromtimestamp(parsed.timestamp() + max(0, int(seconds)), tz=timezone.utc).isoformat()


def snapshot_store_architecture() -> dict[str, Any]:
    return {
        "schema": "v7.intelligence.snapshot-store-architecture.v1",
        "canonical_root": str(CANONICAL_SNAPSHOT_ROOT),
        "owner": "Heavy Brain producers write; Runtime and Admin read",
        "lifecycle": [
            "producer computes outside runtime",
            "producer writes complete envelope atomically",
            "runtime reads bounded JSON",
            "runtime validates schema, freshness, confidence, and stop conditions",
            "runtime consumes compact items only",
        ],
        "retention": {
            "runtime_required": "latest plus short archive for forensics",
            "raw_history": "outside snapshot store; never runtime input",
            "rotation": "producer-owned, bounded by file count and age",
        },
        "families": {name: family_contract(name) for name in SNAPSHOT_FAMILIES},
    }


def snapshot_envelope_schema() -> dict[str, Any]:
    return {
        "schema": SNAPSHOT_SCHEMA_VERSION,
        "required": [
            "schema",
            "generated_at",
            "expires_at",
            "ttl_seconds",
            "freshness_state",
            "confidence",
            "source_hashes",
            "generator",
            "item_count",
            "warnings",
        ],
        "optional": ["confidence_factors", "items", "summary", "metadata"],
        "confidence_range": [0.0, 1.0],
        "freshness_states": list(FRESHNESS_STATES),
        "max_snapshot_bytes": MAX_SNAPSHOT_BYTES,
    }


def family_contract(name: str) -> dict[str, Any]:
    family = SNAPSHOT_FAMILIES[name]
    return {
        "name": family.name,
        "filename": family.filename,
        "schema": family.schema,
        "producer": family.producer,
        "consumer": family.consumer,
        "ttl_seconds": family.ttl_seconds,
        "stale_after_seconds": family.stale_after_seconds,
        "runtime_requirement": family.runtime_requirement,
        "stale_runtime_behavior": family.stale_runtime_behavior,
        "confidence_floor": family.confidence_floor,
        "item_key": family.item_key,
        "retention": family.retention,
    }


def snapshot_family_contracts() -> dict[str, dict[str, Any]]:
    return {name: family_contract(name) for name in SNAPSHOT_FAMILIES}


def freshness_contract() -> dict[str, Any]:
    return {
        "states": {
            "FRESH": "Snapshot is inside stale_after_seconds and expires_at.",
            "STALE": "Snapshot is older than stale_after_seconds but not expired.",
            "EXPIRED": "Snapshot is past expires_at or ttl hard expiry.",
            "UNKNOWN": "Snapshot is missing, corrupt, invalid, or has unknown timestamps.",
        },
        "runtime_behavior": {
            "FRESH": "ALLOW",
            "STALE": "family-specific WARN, IGNORE, or STOP",
            "EXPIRED": "STOP",
            "UNKNOWN": "STOP",
        },
        "governance_behavior": {
            "FRESH": "may validate packet inputs",
            "STALE": "must record warning or deny when runtime-required",
            "EXPIRED": "deny intelligence-assisted live action",
            "UNKNOWN": "deny intelligence-assisted live action",
        },
        "admin_behavior": {
            "FRESH": "show normal",
            "STALE": "show stale badge",
            "EXPIRED": "show expired badge and refresh prompt",
            "UNKNOWN": "show unavailable",
        },
    }


def confidence_contract() -> dict[str, Any]:
    return {
        "score_range": [0.0, 1.0],
        "factors": [
            "source_completeness",
            "history_completeness",
            "probe_completeness",
            "service_completeness",
        ],
        "runtime_rules": {
            "below_family_floor": "IGNORE advisory or STOP when runtime-required",
            "unknown": "STOP for runtime-required snapshots",
            "advisory_only_low_confidence": "IGNORE",
        },
        "thresholds": {
            "normal": 0.80,
            "reduced_weight": 0.50,
            "ignore": 0.0,
        },
    }


def runtime_read_contract() -> dict[str, Any]:
    return {
        "schema": "v7.intelligence.runtime-read-contract.v1",
        "planner_may_read": [family.filename for family in SNAPSHOT_FAMILIES.values()],
        "perf4_integrated_runtime_families": [
            "service-scores",
            "channel-service-scores",
            "user-service-scores",
            "risk-summaries",
            "trust-summaries",
            "blast-radius-summaries",
        ],
        "ri4_b_advisory_runtime_families": [
            "candidate-suitability-summary",
            "best-available-pool",
        ],
        "planner_must_never_read": [
            "raw history",
            "large JSONL logs",
            "service probe commands",
            "prediction engines",
            "SQLite rollups",
            "network probes",
            "admin overview recomputation",
        ],
        "planner_must_validate": [
            "schema",
            "freshness_state",
            "expires_at",
            "confidence",
            "source_hashes",
            "item_count",
        ],
        "runtime_stop_states": ["UNKNOWN", "EXPIRED"],
        "planner_integration_status": "integrated_in_PERF4_runtime_fast_path",
    }


def stop_condition_matrix() -> dict[str, dict[str, str]]:
    matrix: dict[str, dict[str, str]] = {}
    for name, family in SNAPSHOT_FAMILIES.items():
        matrix[name] = {
            "FRESH": "ALLOW",
            "STALE": family.stale_runtime_behavior,
            "EXPIRED": "STOP",
            "UNKNOWN": "STOP",
            "LOW_CONFIDENCE": "STOP" if family.runtime_requirement.startswith("required") else "IGNORE",
        }
    return matrix


def perf3_worker_recommendations() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "worker": family.producer,
            "output": family.filename,
            "cadence_seconds": max(30, min(family.stale_after_seconds, family.ttl_seconds)),
            "inputs_required": snapshot_inputs_for_family(name),
            "writes_runtime_state": False,
            "mutates_users": False,
            "mutates_governance": False,
        }
        for name, family in SNAPSHOT_FAMILIES.items()
    }


def snapshot_inputs_for_family(name: str) -> list[str]:
    return {
        "service-scores": ["service-matrix.json", "egress-quality-summary.json", "service-preferences.json"],
        "channel-service-scores": ["service-matrix.json", "egress-quality-summary.json", "egress.registry"],
        "user-service-scores": ["users.registry", "service-preferences.json"],
        "risk-summaries": ["service-scores.json", "route-reality-summary", "quality-summary"],
        "trust-summaries": ["audit logs", "switch-history.jsonl"],
        "blast-radius-summaries": ["risk-summaries.json", "trust-summaries.json", "v7-state.json"],
        "candidate-suitability-summary": ["users.registry", "egress.registry", "service-matrix.json", "egress-quality-summary.json", "service-preferences.json", "risk-summaries.json", "trust-summaries.json", "blast-radius-summaries.json"],
        "best-available-pool": ["candidate-suitability-summary.json", "users.registry", "egress.registry", "v7-state.json"],
        "capacity-forecast-summaries": ["users.registry", "egress.registry", "traffic summary", "capacity state"],
        "prediction-summaries": ["service history", "quality summary", "traffic summary"],
        "overview-summary": ["runtime read views", "service summaries", "route reality summaries", "diagnostics summaries"],
    }.get(name, [])


def snapshot_path(root: Path | str, family_name: str) -> Path:
    return Path(root) / SNAPSHOT_FAMILIES[family_name].filename


def build_snapshot_envelope(
    family_name: str,
    *,
    generated_at: str,
    ttl_seconds: int | None = None,
    freshness_state: str = "FRESH",
    confidence: float = 1.0,
    source_hashes: dict[str, str] | None = None,
    generator: str = "unknown",
    item_count: int = 0,
    warnings: list[str] | None = None,
    content: Any | None = None,
) -> dict[str, Any]:
    family = SNAPSHOT_FAMILIES[family_name]
    ttl = family.ttl_seconds if ttl_seconds is None else int(ttl_seconds)
    payload = {
        "schema": family.schema,
        "generated_at": generated_at,
        "expires_at": iso_after(generated_at, ttl),
        "ttl_seconds": ttl,
        "freshness_state": freshness_state,
        "confidence": confidence,
        "source_hashes": source_hashes or {},
        "generator": generator,
        "item_count": item_count,
        "warnings": warnings or [],
    }
    payload[family.item_key] = content if content is not None else ([] if family.item_key == "items" else {})
    return payload


def validate_snapshot(payload: dict[str, Any], family_name: str) -> SnapshotValidation:
    errors: list[str] = []
    warnings: list[str] = []
    family = SNAPSHOT_FAMILIES[family_name]
    if not isinstance(payload, dict):
        return SnapshotValidation(False, ["snapshot_not_object"], [])
    required = snapshot_envelope_schema()["required"]
    for key in required:
        if key not in payload:
            errors.append(f"missing_{key}")
    if payload.get("schema") != family.schema:
        errors.append("schema_mismatch")
    if payload.get("freshness_state") not in FRESHNESS_STATES:
        errors.append("freshness_state_invalid")
    confidence = payload.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0.0 <= float(confidence) <= 1.0:
        errors.append("confidence_invalid")
    elif float(confidence) < family.confidence_floor:
        warnings.append("confidence_below_family_floor")
    if not isinstance(payload.get("source_hashes"), dict):
        errors.append("source_hashes_invalid")
    if not isinstance(payload.get("generator"), str) or not payload.get("generator"):
        errors.append("generator_invalid")
    if not isinstance(payload.get("item_count"), int) or int(payload.get("item_count", -1)) < 0:
        errors.append("item_count_invalid")
    if not isinstance(payload.get("warnings"), list):
        errors.append("warnings_invalid")
    if parse_iso(payload.get("generated_at")) is None:
        errors.append("generated_at_invalid")
    if parse_iso(payload.get("expires_at")) is None:
        errors.append("expires_at_invalid")
    ttl = payload.get("ttl_seconds")
    if not isinstance(ttl, int) or ttl <= 0:
        errors.append("ttl_seconds_invalid")
    factors = payload.get("confidence_factors")
    if factors is not None:
        if not isinstance(factors, dict):
            errors.append("confidence_factors_invalid")
        else:
            for key, value in factors.items():
                if not isinstance(value, (int, float)) or not 0.0 <= float(value) <= 1.0:
                    errors.append(f"confidence_factor_invalid:{key}")
    if family.item_key not in payload:
        warnings.append(f"missing_{family.item_key}")
    return SnapshotValidation(not errors, errors, warnings)


def evaluate_freshness(payload: dict[str, Any], family_name: str, *, now: datetime | None = None) -> str:
    family = SNAPSHOT_FAMILIES[family_name]
    declared = payload.get("freshness_state")
    if declared == "UNKNOWN":
        return "UNKNOWN"
    generated = parse_iso(payload.get("generated_at"))
    expires = parse_iso(payload.get("expires_at"))
    if generated is None or expires is None:
        return "UNKNOWN"
    current = now or utc_now()
    if generated.timestamp() - current.timestamp() > 60:
        return "UNKNOWN"
    if current.timestamp() >= expires.timestamp():
        return "EXPIRED"
    age = max(0, int(current.timestamp() - generated.timestamp()))
    if age > family.stale_after_seconds or declared == "STALE":
        return "STALE"
    if declared not in FRESHNESS_STATES:
        return "UNKNOWN"
    return "FRESH"


def runtime_behavior_for(family_name: str, freshness_state: str, confidence: float) -> str:
    family = SNAPSHOT_FAMILIES[family_name]
    if freshness_state in ("UNKNOWN", "EXPIRED"):
        return "STOP"
    if not isinstance(confidence, (int, float)):
        return "STOP"
    if float(confidence) < family.confidence_floor:
        return "STOP" if family.runtime_requirement.startswith("required") else "IGNORE"
    if freshness_state == "STALE":
        return family.stale_runtime_behavior
    return "ALLOW"


def read_snapshot(
    path: Path | str,
    family_name: str,
    *,
    now: datetime | None = None,
    max_bytes: int = MAX_SNAPSHOT_BYTES,
) -> SnapshotReadResult:
    path_obj = Path(path)
    if family_name not in SNAPSHOT_FAMILIES:
        validation = SnapshotValidation(False, ["unknown_snapshot_family"], [])
        return SnapshotReadResult(family_name, str(path_obj), False, {}, validation, "UNKNOWN", 0.0, "STOP", True)
    if not path_obj.exists():
        validation = SnapshotValidation(False, ["missing_snapshot"], [])
        return SnapshotReadResult(family_name, str(path_obj), False, {}, validation, "UNKNOWN", 0.0, "STOP", True)
    try:
        if path_obj.stat().st_size > max_bytes:
            validation = SnapshotValidation(False, ["snapshot_too_large"], [])
            return SnapshotReadResult(family_name, str(path_obj), True, {}, validation, "UNKNOWN", 0.0, "STOP", True)
        payload = json.loads(path_obj.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        validation = SnapshotValidation(False, ["snapshot_corrupt"], [])
        return SnapshotReadResult(family_name, str(path_obj), True, {}, validation, "UNKNOWN", 0.0, "STOP", True)
    validation = validate_snapshot(payload, family_name)
    freshness = evaluate_freshness(payload, family_name, now=now) if validation.ok else "UNKNOWN"
    confidence = float(payload.get("confidence") or 0.0) if isinstance(payload.get("confidence"), (int, float)) else 0.0
    behavior = runtime_behavior_for(family_name, freshness, confidence)
    return SnapshotReadResult(
        family_name,
        str(path_obj),
        True,
        payload if isinstance(payload, dict) else {},
        validation,
        freshness,
        confidence,
        behavior,
        behavior == "STOP",
    )


def read_snapshot_family(
    root: Path | str,
    family_name: str,
    *,
    now: datetime | None = None,
    max_bytes: int = MAX_SNAPSHOT_BYTES,
) -> SnapshotReadResult:
    return read_snapshot(snapshot_path(root, family_name), family_name, now=now, max_bytes=max_bytes)


def read_snapshot_bundle(
    root: Path | str,
    family_names: list[str] | None = None,
    *,
    now: datetime | None = None,
) -> dict[str, SnapshotReadResult]:
    names = family_names or list(SNAPSHOT_FAMILIES)
    return {name: read_snapshot_family(root, name, now=now) for name in names}
