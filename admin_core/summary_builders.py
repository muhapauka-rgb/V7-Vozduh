"""Shared read-only summary helpers and schema contracts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable


def query_value(params: dict[str, Any] | None, *names: str, default: str = "") -> str:
    params = params or {}
    for name in names:
        value = params.get(name)
        if isinstance(value, list) and value:
            return str(value[0] or "")
        if isinstance(value, str):
            return value
    return default


def pagination_from_query(params: dict[str, Any] | None, default_limit: int = 30) -> tuple[int, int]:
    try:
        limit = max(1, min(100, int(query_value(params, "limit", default=str(default_limit)))))
    except (TypeError, ValueError):
        limit = default_limit
    try:
        offset = max(0, int(query_value(params, "cursor", "offset", default="0")))
    except (TypeError, ValueError):
        offset = 0
    return limit, offset


def bounded_jsonl_records(
    path: Path | str,
    *,
    limit: int = 1000,
    redact_value: Callable[[Any], Any] | None = None,
) -> list[dict[str, Any]]:
    path = Path(path)
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[-int(limit or 1000):]
    except OSError:
        return []
    rows = []
    for line in lines:
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            rows.append(redact_value(item) if redact_value else item)
    return rows


def schema_contract(name: str, *, required: list[str], optional: list[str] | None = None, read_only: bool = True) -> dict[str, Any]:
    return {
        "schema": f"v7.admin.{name}.v1",
        "required": list(required),
        "optional": list(optional or []),
        "read_only": bool(read_only),
    }


def api3_schema_contracts() -> dict[str, dict[str, Any]]:
    return {
        "overview": schema_contract(
            "overview",
            required=["updated", "summary", "registries", "service_matrix", "route_reality", "checks"],
            optional=["cache", "trusted_ru_readiness", "service_recommendations", "operator"],
        ),
        "operator_summary": schema_contract(
            "operator_summary",
            required=["schema_version", "preview_only", "execution_allowed_now"],
            optional=["timeline", "evidence", "lineage", "operation"],
        ),
        "service_summary": schema_contract(
            "service_summary",
            required=["items"],
            optional=["updated", "known_services", "best_by_service", "user_required_routes"],
        ),
        "route_summary": schema_contract(
            "route_summary",
            required=["validation", "checks", "blockers", "warnings"],
            optional=["trusted_ru", "route_class", "diagnostic_summary"],
        ),
        "routing_intelligence_summary": schema_contract(
            "routing_intelligence_summary",
            required=["read_only"],
            optional=["service_scores", "user_service_weights", "prediction"],
        ),
    }
