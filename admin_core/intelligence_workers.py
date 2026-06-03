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
from admin_core.registry_readers import parse_registry_lines
from admin_core.routing_intelligence import (
    DEFAULT_SERVICES,
    DynamicBlastRadiusModel,
    ExecutionTrustModel,
    ServiceHistoryStore,
    ServiceIntelligenceEngine,
    UserServiceWeights,
    as_float,
    clamp,
    normalize_services,
    now_iso,
    sha256_json,
)


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
    for service_id in sorted(history.services):
        target_scores = []
        for target_id in sorted(matrix_items):
            row = engine.score_service(service_id, target_id, "1h")
            target_scores.append(row)
            confidence_values.append(as_float(row.get("confidence"), 0.0))
        scores = [as_float(row.get("score"), 0.0) for row in target_scores]
        service_rows.append({
            "service": service_id,
            "target_count": len(target_scores),
            "average_score": round(mean(scores), 3),
            "confidence": round(mean([as_float(row.get("confidence"), 0.0) for row in target_scores]), 4),
            "low_targets": [row["target"] for row in target_scores if as_float(row.get("score"), 0.0) < 50.0],
            "runtime_decision_authority": "none_snapshot_only",
        })

    channel_items = []
    for target_id, row in sorted(channel_scores.items()):
        per_confidence = [as_float(item.get("confidence"), 0.0) for item in (row.get("per_service") or [])]
        confidence_values.extend(per_confidence)
        channel_items.append({
            "channel": target_id,
            "aggregate_score": row.get("aggregate_score", 0.0),
            "verdict": row.get("verdict", "UNKNOWN"),
            "confidence": round(mean(per_confidence), 4),
            "required_missing": row.get("required_missing", []),
            "required_low": row.get("required_low", []),
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
    return {
        "service-scores": envelope(
            "service-scores",
            generated_at=generated,
            confidence=confidence,
            confidence_factors=factors,
            source_hashes_value=hashes,
            content=service_rows,
            item_count=len(service_rows),
            warnings=warnings,
        ),
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
