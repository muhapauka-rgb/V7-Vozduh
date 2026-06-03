"""Pure read-only service view and recommendation builders."""

from __future__ import annotations

from typing import Any


def telegram_status_is_hard(status: Any, hard_statuses: set[str] | tuple[str, ...] | None = None) -> bool:
    hard_statuses = set(hard_statuses or {"NOT_STARTED", "DOWN"})
    value = str(status or "").upper()
    return value in hard_statuses or value.startswith("TELEGRAM_DOWN_")


def service_matrix_telegram_state(
    matrix_row: dict[str, Any] | None,
    *,
    hard_statuses: set[str] | tuple[str, ...] | None = None,
    soft_statuses: set[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    soft_statuses = set(soft_statuses or {"DEGRADED", "DOWN_GRACE", "GRACE"})
    services = (matrix_row or {}).get("services") or {}
    row = services.get("telegram") or {}
    status = str(row.get("status") or "").upper()
    hard_down = bool(row) and (
        telegram_status_is_hard(status, hard_statuses)
        or (row.get("ok") is False and status in ("", "FAIL", "ERROR"))
    )
    degraded = bool(row) and status in soft_statuses
    return {
        "required": True,
        "status": status or "UNKNOWN",
        "ok": bool(row.get("ok")) and not hard_down,
        "hard_down": hard_down,
        "degraded": degraded,
        "score": row.get("score"),
        "ratio": row.get("ratio"),
        "reason": row.get("reason", ""),
    }


def service_matrix_route_fitness(
    matrix: dict[str, Any] | None,
    *,
    route_class_service_map: dict[str, tuple[str, ...]],
    hard_statuses: set[str] | tuple[str, ...] | None = None,
    soft_statuses: set[str] | tuple[str, ...] | None = None,
) -> dict[str, dict[str, Any]]:
    services = (matrix or {}).get("services") or {}
    fitness = {}
    for route_class, service_ids in route_class_service_map.items():
        tested = []
        missing = []
        for service_id in service_ids:
            row = services.get(service_id)
            if row:
                tested.append(row)
            else:
                missing.append(service_id)
        ok_count = sum(1 for row in tested if bool(row.get("ok")))
        fail_count = len(tested) - ok_count
        telegram = service_matrix_telegram_state(
            matrix,
            hard_statuses=hard_statuses,
            soft_statuses=soft_statuses,
        ) if "telegram" in service_ids else {}
        latencies = []
        for row in tested:
            value = row.get("first_byte_sec", row.get("total_sec", 0))
            try:
                latencies.append(float(value))
            except (TypeError, ValueError):
                pass
        if not tested:
            status = "UNKNOWN"
            reason = "ещё не проверялось"
        elif telegram.get("hard_down"):
            status = "FAIL"
            reason = "Telegram обязателен для пользователей и сейчас недоступен через этот канал"
        elif ok_count == len(tested) and not missing and not telegram.get("degraded"):
            status = "OK"
            reason = "все обязательные сервисы прошли проверку"
        elif telegram.get("degraded"):
            status = "WARN"
            reason = "Telegram работает нестабильно, канал можно держать, но не выбирать как лучший"
        elif ok_count and fail_count == 0:
            status = "WARN"
            reason = "проверенные сервисы работают, но часть ещё не проверялась"
        elif ok_count:
            status = "WARN"
            reason = "часть сервисов работает, часть не прошла проверку"
        else:
            status = "FAIL"
            reason = "проверенные сервисы не прошли проверку"
        fitness[route_class] = {
            "status": status,
            "reason": reason,
            "ok_count": ok_count,
            "tested_count": len(tested),
            "missing_count": len(missing),
            "total": len(service_ids),
            "avg_first_byte_sec": round(sum(latencies) / len(latencies), 3) if latencies else None,
            "services": list(service_ids),
            "missing": missing,
        }
    return fitness


def normalize_service_matrix_row(
    row: dict[str, Any] | Any,
    *,
    known_services: tuple[str, ...],
    route_class_service_map: dict[str, tuple[str, ...]],
    hard_statuses: set[str] | tuple[str, ...] | None = None,
    soft_statuses: set[str] | tuple[str, ...] | None = None,
) -> dict[str, Any] | Any:
    if not isinstance(row, dict):
        return row
    normalized = dict(row)
    services = normalized.get("services") or {}
    if not isinstance(services, dict):
        services = {}
    services = {service_id: item for service_id, item in services.items() if service_id in known_services}
    total = len(services)
    ok_count = sum(1 for item in services.values() if isinstance(item, dict) and bool(item.get("ok")))
    normalized["services"] = services
    normalized["ok_count"] = ok_count
    normalized["total"] = total
    normalized["count"] = total
    normalized["status"] = "OK" if total and ok_count == total else ("WARN" if ok_count else ("UNKNOWN" if not total else "FAIL"))
    normalized["route_class_fitness"] = service_matrix_route_fitness(
        normalized,
        route_class_service_map=route_class_service_map,
        hard_statuses=hard_statuses,
        soft_statuses=soft_statuses,
    )
    return normalized


def normalize_services(values: Any, *, known_services: tuple[str, ...]) -> list[str]:
    if isinstance(values, str):
        values = [part.strip() for part in values.split(",")]
    if not isinstance(values, list):
        return []
    return sorted({str(v).strip().lower() for v in values if str(v).strip().lower() in known_services})


def user_priority_services_from_pref(
    row: dict[str, Any] | Any,
    *,
    known_services: tuple[str, ...],
    default_user_priority_services: tuple[str, ...],
) -> list[str]:
    if isinstance(row, dict) and "services" in row:
        services = normalize_services(row.get("services") or [], known_services=known_services)
        if int(row.get("schema_version") or 0) < 2 and services == ["telegram"]:
            return list(default_user_priority_services)
        return services
    return list(default_user_priority_services)


def service_metric_float(value: Any, default: float = 999.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def service_recommendations(
    active_users: list[dict[str, Any]],
    matrix_data: dict[str, Any],
    prefs: dict[str, Any],
    *,
    known_services: tuple[str, ...],
    default_user_priority_services: tuple[str, ...],
) -> dict[str, Any]:
    items = matrix_data.get("items") or {}
    enabled = bool(prefs.get("enabled"))
    user_prefs = prefs.get("users") or {}
    service_ids = sorted({
        service_id
        for egress_item in items.values()
        for service_id in ((egress_item.get("services") or {}).keys())
    })
    best_by_service = {}
    for service_id in service_ids:
        candidates = []
        for egress_id, egress_item in items.items():
            row = (egress_item.get("services") or {}).get(service_id)
            if not row:
                continue
            candidates.append({
                "egress": egress_id,
                "ok": bool(row.get("ok")),
                "severity": row.get("severity"),
                "http_code": row.get("http_code"),
                "first_byte_sec": row.get("first_byte_sec"),
                "total_sec": row.get("total_sec"),
                "reason": row.get("reason"),
                "tested_at": row.get("tested_at"),
            })
        candidates.sort(key=lambda c: (
            0 if c["ok"] else 1,
            service_metric_float(c.get("first_byte_sec")),
            service_metric_float(c.get("total_sec")),
            c["egress"],
        ))
        best = candidates[0] if candidates else None
        best_by_service[service_id] = {
            "service": service_id,
            "best_egress": best.get("egress") if best else None,
            "status": "OK" if best and best.get("ok") else "NO_GOOD_EGRESS",
            "candidates": candidates,
        }

    user_warnings = []
    user_required_routes = []
    for user in active_users:
        ip = user.get("ip", "")
        current = user.get("current", "")
        important = user_priority_services_from_pref(
            user_prefs.get(ip),
            known_services=known_services,
            default_user_priority_services=default_user_priority_services,
        )
        if not enabled or not important:
            continue
        current_services = ((items.get(current) or {}).get("services") or {})
        current_missing = []
        current_failed = []
        for service_id, recommendation in best_by_service.items():
            if service_id not in important:
                continue
            current_row = current_services.get(service_id)
            best = recommendation.get("best_egress")
            current_ok = bool(current_row and current_row.get("ok"))
            if not current_row:
                current_missing.append(service_id)
            elif not current_ok:
                current_failed.append({
                    "service": service_id,
                    "reason": current_row.get("reason") or current_row.get("error") or "service_failed",
                    "status": current_row.get("status") or "FAIL",
                })
            if best and best != current and not current_ok:
                best_candidate = next((c for c in recommendation.get("candidates", []) if c.get("egress") == best), {})
                user_warnings.append({
                    "ip": ip,
                    "current_egress": current,
                    "service": service_id,
                    "current_status": "FAIL" if current_row else "UNKNOWN",
                    "current_reason": (current_row or {}).get("reason"),
                    "recommended_egress": best,
                    "recommended_first_byte_sec": best_candidate.get("first_byte_sec"),
                    "action": "manual_switch_available",
                })
        required_candidates = []
        for egress_id, egress_item in items.items():
            services = egress_item.get("services") or {}
            missing = [service_id for service_id in important if service_id not in services]
            failed = []
            latencies = []
            for service_id in important:
                row = services.get(service_id) or {}
                if not row:
                    continue
                if not row.get("ok"):
                    failed.append({
                        "service": service_id,
                        "reason": row.get("reason") or row.get("error") or "service_failed",
                        "status": row.get("status") or "FAIL",
                    })
                else:
                    for key in ("first_byte_sec", "total_sec"):
                        try:
                            value = float(row.get(key) or 0)
                        except (TypeError, ValueError):
                            value = 0
                        if value > 0:
                            latencies.append(value)
                            break
            ok = not missing and not failed
            required_candidates.append({
                "egress": egress_id,
                "ok": ok,
                "missing": missing,
                "failed": failed,
                "ok_count": len(important) - len(missing) - len(failed),
                "required_count": len(important),
                "avg_latency_sec": round(sum(latencies) / len(latencies), 3) if latencies else None,
                "updated": egress_item.get("updated") or egress_item.get("checked_at"),
            })
        required_candidates.sort(key=lambda c: (
            0 if c.get("ok") else 1,
            float(c.get("avg_latency_sec") or 999),
            -int(c.get("ok_count") or 0),
            c.get("egress", ""),
        ))
        best_required = next((c for c in required_candidates if c.get("ok")), None)
        current_ok = not current_missing and not current_failed
        user_required_routes.append({
            "ip": ip,
            "current_egress": current,
            "required_services": important,
            "current_ok": current_ok,
            "current_missing": current_missing,
            "current_failed": current_failed,
            "recommended_egress": best_required.get("egress") if best_required else "",
            "recommendation_status": "KEEP_CURRENT" if current_ok else ("SWITCH_AVAILABLE" if best_required else "NO_EGRESS_MATCHES_REQUIRED_SERVICES"),
            "action": "manual_review",
            "candidates": required_candidates[:6],
        })
    return {
        "enabled": enabled,
        "known_services": list(known_services),
        "user_preferences": user_prefs,
        "best_by_service": best_by_service,
        "user_warnings": user_warnings,
        "user_required_routes": user_required_routes,
    }
