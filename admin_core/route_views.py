"""Pure read-only route and Trusted RU view builders."""

from __future__ import annotations

import re
from typing import Any, Callable


def trusted_ru_key(domain: Any) -> str:
    return re.sub(r"(^_+|_+$)", "", re.sub(r"[^a-z0-9]+", "_", str(domain or "").lower()))


def trusted_ru_domain_status(row: dict[str, Any]) -> str:
    direct_http = str(row.get("direct_http", ""))
    direct_openssl = str(row.get("direct_openssl", ""))
    browser_like = str(row.get("browser_like", ""))
    browser_like_http = str(row.get("browser_like_http", ""))
    vless_http = str(row.get("vless_http", ""))
    awg_http = str(row.get("awg_http", ""))
    if direct_http and direct_http != "000" and direct_openssl == "OK":
        return "LOCAL_DIRECT_OK"
    if browser_like == "OK" and browser_like_http and browser_like_http != "000":
        return "BROWSER_LIKE_DIRECT_OK"
    if vless_http and vless_http != "000":
        return "TEMP_VLESS_OK"
    if awg_http and awg_http != "000":
        return "AWG_OK"
    if direct_http == "000" and direct_openssl == "FAIL":
        if vless_http == "000" and awg_http == "000":
            return "NO_SERVER_PATH"
        return "DIRECT_BLOCKED"
    return "UNKNOWN"


def trusted_ru_parse_probe(value: Any, first_key: str) -> dict[str, str]:
    data = {}
    parts = str(value or "").split()
    if parts:
        data[first_key] = parts[0]
    for part in parts[1:]:
        if "=" in part:
            key, val = part.split("=", 1)
            data[key] = val
    return data


def trusted_ru_decision_summary(raw: dict[str, Any], *, decision_file: str, age_func: Callable[[Any], Any]) -> dict[str, Any]:
    items = []
    try:
        count = int(raw.get("count", "0") or "0")
    except ValueError:
        count = 0
    for idx in range(1, count + 1):
        domain = raw.get(f"item_{idx}_domain", "")
        if not domain:
            continue
        items.append({
            "domain": domain,
            "decision": raw.get(f"item_{idx}_decision", ""),
            "path": raw.get(f"item_{idx}_path", ""),
            "direct": raw.get(f"item_{idx}_direct", ""),
            "vless": raw.get(f"item_{idx}_vless", ""),
            "awg": raw.get(f"item_{idx}_awg", ""),
            "reason": raw.get(f"item_{idx}_reason", ""),
        })
    return {
        "file": decision_file,
        "updated": raw.get("updated", ""),
        "diagnostic_updated": raw.get("diagnostic_updated", ""),
        "age_sec": age_func(raw.get("updated")),
        "overall": raw.get("overall", "UNKNOWN"),
        "route_class": raw.get("route_class", "TRUSTED_RU_SENSITIVE"),
        "route_class_status": raw.get("route_class_status", "UNKNOWN"),
        "current_candidate": raw.get("current_candidate", ""),
        "candidate_result": raw.get("candidate_result", "UNKNOWN"),
        "required_action": raw.get("required_action", ""),
        "count": raw.get("count", "0"),
        "direct_ok": raw.get("direct_ok", "0"),
        "temporary_vless": raw.get("temporary_vless", "0"),
        "awg": raw.get("awg", "0"),
        "blocked": raw.get("blocked", "0"),
        "missing": raw.get("missing", "0"),
        "candidate_vless_failed": raw.get("candidate_vless_failed", "0"),
        "items": items,
    }


def trusted_ru_diagnostic_summary(
    raw: dict[str, Any],
    *,
    decision: dict[str, Any],
    flow_trace: dict[str, Any],
    domains: list[str],
    diag_file: str,
    age_func: Callable[[Any], Any],
) -> dict[str, Any]:
    decisions_by_domain = {item.get("domain"): item for item in decision.get("items", [])}
    if not domains:
        domains = ["www.gosuslugi.ru", "gosuslugi.ru", "esia.gosuslugi.ru", "lk.gosuslugi.ru", "alfa-mobile.alfabank.ru"]
    rows = []
    for domain in domains:
        key = trusted_ru_key(domain)
        direct = trusted_ru_parse_probe(raw.get(f"{key}_direct_http", ""), "direct_http")
        direct_tls = trusted_ru_parse_probe(raw.get(f"{key}_direct_openssl", ""), "direct_openssl")
        browser_like = trusted_ru_parse_probe(raw.get(f"{key}_browser_like", ""), "browser_like")
        vless = trusted_ru_parse_probe(raw.get(f"{key}_vless_http", ""), "vless_http")
        awg = trusted_ru_parse_probe(raw.get(f"{key}_awg_http", ""), "awg_http")
        row = {
            "domain": domain,
            "resolved_ips": raw.get(f"{key}_resolved_ips", ""),
            "policy_decision": raw.get(f"{key}_policy_decision", ""),
            "direct_http": direct.get("direct_http", ""),
            "direct_remote": direct.get("direct_remote", ""),
            "direct_connect": direct.get("direct_connect", ""),
            "direct_tls": direct.get("direct_tls", ""),
            "direct_err": direct.get("direct_err", ""),
            "direct_openssl": direct_tls.get("direct_openssl", ""),
            "direct_openssl_reason": direct_tls.get("direct_openssl_reason", ""),
            "browser_like": browser_like.get("browser_like", ""),
            "browser_like_tool": browser_like.get("browser_like_tool", ""),
            "browser_like_http": browser_like.get("browser_like_http", ""),
            "browser_like_err": browser_like.get("browser_like_err", ""),
            "vless_http": vless.get("vless_http", ""),
            "vless_remote": vless.get("vless_remote", ""),
            "vless_err": vless.get("vless_err", ""),
            "awg_http": awg.get("awg_http", ""),
            "awg_remote": awg.get("awg_remote", ""),
            "awg_err": awg.get("awg_err", ""),
        }
        row["status"] = trusted_ru_domain_status(row)
        row["decision"] = decisions_by_domain.get(domain, {})
        rows.append(row)
    return {
        "file": diag_file,
        "updated": raw.get("updated", ""),
        "age_sec": age_func(raw.get("updated")),
        "direct_if": raw.get("direct_if", ""),
        "socks": raw.get("socks", ""),
        "awg_if": raw.get("awg_if", ""),
        "local_ok": sum(1 for row in rows if row["status"] in ("LOCAL_DIRECT_OK", "BROWSER_LIKE_DIRECT_OK")),
        "temporary_ok": sum(1 for row in rows if row["status"] == "TEMP_VLESS_OK"),
        "blocked": sum(1 for row in rows if row["status"] in ("TCP_OR_TLS_BLOCKED", "NO_SERVER_PATH", "DIRECT_BLOCKED")),
        "no_server_path": sum(1 for row in rows if row["status"] == "NO_SERVER_PATH"),
        "total": len(rows),
        "decision": decision,
        "flow_trace": flow_trace,
        "items": rows,
    }


def trusted_ru_readiness_summary(
    *,
    route: dict[str, Any],
    active_egress: str,
    egress: dict[str, Any],
    services: dict[str, Any],
    diagnostic: dict[str, Any],
    required_services: tuple[str, ...],
    updated: str,
) -> dict[str, Any]:
    checks = []

    def add_check(key: str, label: str, status: str, detail: str = "") -> None:
        checks.append({"key": key, "label": label, "status": status, "detail": detail})

    if route:
        add_check("route_class_exists", "Группа маршрутов есть", "OK", "Правило для Госуслуг и банков найдено")
    else:
        add_check("route_class_exists", "Группа маршрутов есть", "BLOCKED", "Группа Госуслуги и банки не найдена в реестре маршрутов")

    add_check("route_class_enabled", "Группа включена", "OK" if str(route.get("enabled", "0")) == "1" else "BLOCKED", "правило включено" if str(route.get("enabled", "0")) == "1" else "правило выключено")
    add_check("not_temporary", "Путь не временный", "OK" if str(route.get("temporary", "0")) != "1" else "BLOCKED", "постоянный путь" if str(route.get("temporary", "0")) != "1" else "сейчас используется временный путь")
    add_check("active_egress_present", "Выбран отдельный канал", "OK" if active_egress and active_egress != "user_default" else "BLOCKED", f"выбран {active_egress}" if active_egress else "канал не выбран")
    add_check("active_egress_exists", "Канал есть в пуле", "OK" if egress else "BLOCKED", f"{active_egress} найден" if egress else "канал не найден")
    add_check("active_egress_enabled", "Канал включён", "OK" if egress and str(egress.get("enabled", "0")) == "1" else "BLOCKED", "канал включён" if egress and str(egress.get("enabled", "0")) == "1" else "канал выключен или не найден")
    add_check("active_egress_role", "Канал подходит для Госуслуг и банков", "OK" if egress.get("role") == "TRUSTED_RU_SENSITIVE" else "BLOCKED", "роль подходит" if egress.get("role") == "TRUSTED_RU_SENSITIVE" else "канал не помечен как доверенный RU")
    add_check("active_egress_interface", "У канала есть интерфейс", "OK" if egress.get("interface") else "BLOCKED", f"интерфейс {egress.get('interface')}" if egress.get("interface") else "интерфейс не найден")

    service_rows = []
    for service_id in required_services:
        row = services.get(service_id) or {}
        if not row:
            status = "WARN"
            detail = "не проверялось"
        else:
            status = "OK" if row.get("ok") else "BLOCKED"
            detail = f"HTTP={row.get('http_code', 'н/д')} первый ответ={row.get('first_byte_sec', row.get('total_sec', 'н/д'))}"
        service_rows.append({"service": service_id, "status": status, "detail": detail})

    if not service_rows:
        add_check("service_matrix", "Проверка Госуслуг и банков", "WARN", "нет образцов проверки сервисов")
    elif all(row["status"] == "OK" for row in service_rows):
        add_check("service_matrix", "Проверка Госуслуг и банков", "OK", "все обязательные сервисы прошли проверку")
    elif any(row["status"] == "BLOCKED" for row in service_rows):
        add_check("service_matrix", "Проверка Госуслуг и банков", "BLOCKED", "один или несколько сервисов не прошли проверку")
    else:
        add_check("service_matrix", "Проверка Госуслуг и банков", "WARN", "один или несколько сервисов ещё не проверялись")

    if int(diagnostic.get("temporary_ok", 0) or 0) > 0:
        add_check("temporary_vless_observed", "Временный VLESS замечен", "WARN", "подходит для диагностики, но не считается постоянным доверенным путём")
    if int(diagnostic.get("blocked", 0) or 0) > 0:
        add_check("server_direct_blocked", "Прямой путь сервера", "WARN", "часть чувствительной RU-категории блокирует прямой путь VPS")

    blocked = [row for row in checks if row.get("status") == "BLOCKED"]
    warnings = [row for row in checks if row.get("status") == "WARN"]
    validation = "BLOCKED" if blocked else ("WARN" if warnings else "READY")
    return {
        "updated": updated,
        "validation": validation,
        "route_class": route,
        "active_egress": active_egress,
        "egress": egress,
        "checks": checks,
        "services": service_rows,
        "blockers": blocked,
        "warnings": warnings,
        "diagnostic_summary": {
            "local_direct_ok": diagnostic.get("local_ok", 0),
            "temporary_vless_ok": diagnostic.get("temporary_ok", 0),
            "blocked": diagnostic.get("blocked", 0),
            "total": diagnostic.get("total", 0),
        },
        "next_step": "add_dedicated_trusted_ru_route" if blocked else "run_live_rollout_preview",
    }
