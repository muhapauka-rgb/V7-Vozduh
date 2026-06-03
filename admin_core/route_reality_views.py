"""Read-only route reality and direct-route summary builders."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from admin_core.registry_readers import parse_kv_line


@dataclass(frozen=True)
class RouteRealitySnapshot:
    users: list[dict[str, Any]]
    route_rows: list[dict[str, Any]]
    direct_routing: dict[str, Any]
    trusted_ru: dict[str, Any]


def route_status_row(user: dict[str, Any], *, expected_dev: str, route_output: str) -> dict[str, Any]:
    output = str(route_output or "").strip()
    return {
        "ip": user.get("ip", ""),
        "table": user.get("table", ""),
        "current": user.get("current", ""),
        "expected_dev": expected_dev,
        "route_get": output,
        "ok": bool(expected_dev and f" dev {expected_dev} " in f" {output} "),
        "leak_risk": " dev ens3 " in f" {output} ",
    }


def parse_direct_domain_test(output: Any) -> dict[str, Any]:
    domain = ""
    user_ip = ""
    resolved_ips = []
    rows = []
    current = {}
    for line in str(output or "").splitlines():
        line = line.strip()
        if not line:
            if current:
                rows.append(current)
                current = {}
            continue
        if line.startswith("domain="):
            domain = line.split("=", 1)[1]
            continue
        if line.startswith("user_ip="):
            user_ip = line.split("=", 1)[1]
            continue
        if line.startswith("resolved_ips="):
            resolved_ips = [item for item in line.split("=", 1)[1].split(",") if item]
            continue
        if line.startswith("ip="):
            if current:
                rows.append(current)
            current = parse_kv_line(line)
            continue
        if line.startswith("decision="):
            current["decision"] = line.split("=", 1)[1]
            continue
    if current:
        rows.append(current)

    rows = [row for row in rows if row.get("ip")]
    missing = [row for row in rows if row.get("direct_set") != "yes" and row.get("direct_exclude") != "yes"]
    excluded = [row for row in rows if row.get("direct_exclude") == "yes"]
    route_wrong = [row for row in rows if row.get("direct_set") == "yes" and row.get("decision") not in ("DIRECT_READY", "VPN_PREFERRED_DIRECT_EXCLUDED")]
    if not resolved_ips and not rows:
        status = "DNS_FAIL"
        plain = "служебное правило не разрешилось через DNS V7"
    elif missing:
        status = "STALE_SET"
        plain = "категория должна идти напрямую, но часть IP ещё не попала в direct-набор"
    elif route_wrong:
        status = "ROUTE_MISMATCH"
        plain = "IP есть в direct-наборе, но маршрут не выглядит прямым"
    elif excluded and not any(row.get("decision") == "DIRECT_READY" for row in rows):
        status = "EXCLUDED"
        plain = "категория исключена из прямого RU и должна идти через отдельный путь"
    else:
        status = "OK"
        plain = "категория готова идти напрямую"

    return {
        "domain": domain,
        "user_ip": user_ip,
        "resolved_ips": resolved_ips,
        "ips": rows,
        "status": status,
        "plain": plain,
        "missing_count": len(missing),
        "excluded_count": len(excluded),
        "route_mismatch_count": len(route_wrong),
    }


def direct_routing_freshness_summary(*, user_ip: str, items: list[dict[str, Any]], updated: str) -> dict[str, Any]:
    stale = [item for item in items if item.get("status") in ("STALE_SET", "ROUTE_MISMATCH")]
    failed = [item for item in items if item.get("status") == "DNS_FAIL"]
    excluded = [item for item in items if item.get("status") == "EXCLUDED"]
    ok = [item for item in items if item.get("status") == "OK"]
    status = "OK"
    if stale:
        status = "STALE"
    elif failed:
        status = "WARN"
    return {
        "updated": updated,
        "user_ip": user_ip,
        "status": status,
        "ok_count": len(ok),
        "stale_count": len(stale),
        "failed_count": len(failed),
        "excluded_count": len(excluded),
        "total": len(items),
        "items": items,
        "stale_domains": [item.get("domain") for item in stale if item.get("domain")],
        "plain": "обычная RU-категория готова идти напрямую" if status == "OK" else "часть RU-категории может уйти через VPN из-за устаревшего direct-набора",
        "next_step": "обновить direct-наборы и проверить RU-категорию повторно" if status == "STALE" else "наблюдать",
    }


def direct_routing_quick_summary(
    *,
    user_ip: str,
    status_result: dict[str, Any],
    freshness: dict[str, Any],
    domains_state: dict[str, Any],
    fallback_domain: str,
) -> dict[str, Any]:
    first = (freshness.get("items") or [{}])[0]
    route_ok = freshness.get("stale_count", 0) == 0 and freshness.get("failed_count", 0) == 0 and freshness.get("ok_count", 0) > 0
    return {
        "user_ip": user_ip,
        "status": status_result,
        "quick_domain": first.get("domain") or fallback_domain,
        "quick_test": first.get("check", {}),
        "domains": domains_state,
        "route_ok": route_ok,
        "freshness": freshness,
        "stale_count": freshness.get("stale_count", 0),
        "stale_domains": freshness.get("stale_domains", []),
        "summary": "direct route ready" if route_ok else freshness.get("plain", "direct route needs check"),
        "next_step": freshness.get("next_step", "наблюдать"),
    }


def route_reality_schema_contracts() -> dict[str, dict[str, Any]]:
    return {
        "route_reality": {
            "schema": "v7.admin.route-reality.v1",
            "read_only": True,
            "required": ["ip", "current", "expected_dev", "route_get", "ok", "leak_risk"],
            "optional": ["table"],
        },
        "trusted_ru": {
            "schema": "v7.admin.trusted-ru-summary.v1",
            "read_only": True,
            "required": ["validation", "checks", "blockers", "warnings"],
            "optional": ["diagnostic_summary", "services"],
        },
    }
