"""Shared read-only summary helpers and schema contracts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable


DEFAULT_JSONL_TAIL_MAX_BYTES = 8 * 1024 * 1024


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
    """Return the latest JSONL records without materialising an archive.

    Admin summaries call this helper for current history.  Reading a large
    append-only store with ``read_text().splitlines()`` briefly retains the
    whole file, its decoded text and a list of every line.  Repeating that for
    several summary rows can exhaust the small Runtime substrate even though
    callers only need a bounded tail.
    """
    path = Path(path)
    if not path.exists():
        return []
    wanted = max(1, int(limit or 1000))
    try:
        size = path.stat().st_size
        if not size:
            return []
        budget = min(
            size,
            max(256 * 1024, min(DEFAULT_JSONL_TAIL_MAX_BYTES, wanted * 8192)),
        )
        with path.open("rb") as handle:
            handle.seek(max(0, size - budget))
            payload = handle.read(budget)
    except OSError:
        return []
    # The first row may start before the bounded read.  It is deliberately
    # dropped rather than parsed as a malformed current record.
    if size > budget:
        newline = payload.find(b"\n")
        payload = payload[newline + 1:] if newline >= 0 else b""
    lines = payload.decode("utf-8", errors="replace").splitlines()[-wanted:]
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
