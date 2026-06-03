"""Read-only diagnostic, capacity, traffic, and client-speed builders."""

from __future__ import annotations

import ipaddress
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class DiagnosticSnapshot:
    service_matrix: dict[str, Any]
    traffic: dict[str, Any]
    client_speed: dict[str, Any]
    route_reality: list[dict[str, Any]]


def traffic_zero_summary(entity_type: str = "", entity_id: str = "") -> dict[str, Any]:
    empty = {"rx_bytes": 0, "tx_bytes": 0, "total_bytes": 0}
    return {
        "entity_type": entity_type,
        "entity_id": entity_id,
        "today": dict(empty),
        "last_24h": dict(empty),
        "week": dict(empty),
        "month": dict(empty),
        "all_time": dict(empty),
        "updated_at": "",
        "snapshot": {},
    }


def traffic_entity_payload(
    *,
    entity_type: str,
    entity_id: str,
    today: dict[str, int],
    last_24h: dict[str, int],
    week: dict[str, int],
    month: dict[str, int],
    total: dict[str, Any] | None,
    snapshot: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "entity_type": entity_type,
        "entity_id": entity_id,
        "today": today,
        "last_24h": last_24h,
        "week": week,
        "month": month,
        "all_time": {
            "rx_bytes": int((total or {}).get("rx_bytes") or 0),
            "tx_bytes": int((total or {}).get("tx_bytes") or 0),
            "total_bytes": int((total or {}).get("total_bytes") or 0),
        },
        "updated_at": (total or {}).get("updated_at") if total else ((snapshot or {}).get("updated_at") if snapshot else ""),
        "snapshot": dict(snapshot or {}),
    }


def client_speed_summary(active_users: list[dict[str, Any]], client_data: dict[str, Any]) -> dict[str, Any]:
    by_egress = {}
    for user in active_users:
        ip = user.get("ip", "")
        egress = user.get("current", "")
        if not egress:
            continue
        row = by_egress.setdefault(egress, {"client_v7_values": [], "client_direct_values": [], "users": []})
        row["users"].append(ip)
        latest = ((client_data.get("users") or {}).get(ip) or {}).get("latest") or {}
        v7 = latest.get("v7") or {}
        if v7.get("egress") == egress and isinstance(v7.get("mbps"), (int, float)):
            row["client_v7_values"].append(float(v7["mbps"]))
        direct_items = latest.get("direct") or {}
        direct = direct_items.get(egress) or direct_items.get("_default") or {}
        if isinstance(direct.get("mbps"), (int, float)):
            row["client_direct_values"].append(float(direct["mbps"]))

    for row in by_egress.values():
        v7_values = row.pop("client_v7_values")
        direct_values = row.pop("client_direct_values")
        client_v7 = round(sum(v7_values) / len(v7_values), 2) if v7_values else None
        client_direct = round(sum(direct_values) / len(direct_values), 2) if direct_values else None
        degradation = None
        if client_v7 is not None and client_direct and client_direct > 0:
            degradation = round(max(0.0, (client_direct - client_v7) / client_direct * 100), 1)
        row.update({
            "client_v7_mbps": client_v7,
            "client_direct_mbps": client_direct,
            "degradation_pct": degradation,
            "client_v7_samples": len(v7_values),
            "client_direct_samples": len(direct_values),
        })
    return by_egress


def killswitch_summary(
    *,
    output: str,
    kv_data: dict[str, Any],
    check_rc: int | None,
    status_rc: int | None = None,
) -> dict[str, Any]:
    result = kv_data.get("V7_KILLSWITCH_CHECK", "UNKNOWN")
    warnings = [line for line in str(output or "").splitlines() if line.startswith("WARN:")]
    essential_rules = {
        "table": kv_data.get("table", ""),
        "client_source_set": kv_data.get("client_source_set", ""),
        "direct_leak_drop_rule": kv_data.get("direct_leak_drop_rule", ""),
        "direct_whitelist_rule": kv_data.get("direct_whitelist_rule", ""),
        "direct_fwmark_rule": kv_data.get("direct_fwmark_rule", ""),
        "direct_fwmark_precedes_user_rules": kv_data.get("direct_fwmark_precedes_user_rules", ""),
        "direct_route_table": kv_data.get("direct_route_table", ""),
        "direct_mark_rule": kv_data.get("direct_mark_rule", ""),
        "dns_capture_udp": kv_data.get("dns_capture_udp", ""),
        "dns_capture_tcp": kv_data.get("dns_capture_tcp", ""),
    }
    for ifname in str(kv_data.get("egress_ifs", "")).split():
        safe_ifname = "".join(ch if ch.isalnum() or ch in "_.-" else "_" for ch in ifname)
        essential_rules[f"nat_{safe_ifname}"] = kv_data.get(f"nat_{ifname}", "")
    rule_values = [value for value in essential_rules.values() if value]
    rules_present = bool(rule_values) and all(value in ("present", "OK") for value in rule_values)
    normalized = result
    if result in ("OK", "REBUILDING"):
        normalized = result
    elif check_rc == 0 and rules_present and not warnings:
        normalized = "OK"
    elif check_rc == 124:
        normalized = "TIMEOUT"
    elif check_rc == 127:
        normalized = "COMMAND_ERROR"
    elif result == "UNKNOWN":
        normalized = "CHECK"
    ok = normalized in ("OK", "REBUILDING")
    summary = {
        "result": result,
        "normalized_status": normalized,
        "ok": ok,
        "vpn_subnet": kv_data.get("vpn_subnet", kv_data.get("vpn_subnets", "")),
        "vpn_subnets": kv_data.get("vpn_subnets", kv_data.get("vpn_subnet", "")),
        "public_if": kv_data.get("public_if", ""),
        **essential_rules,
        "warnings": len(warnings),
        "rules_present": rules_present,
        "ssh_lockout_guard": "status_only_no_rule_changes",
        "admin_ssh_scope": "server_ssh_is_not_filtered_by_v7_forward_chain",
        "status_rc": status_rc,
        "check_rc": check_rc,
    }
    if not ok:
        summary["reason"] = " / ".join(warnings[:3]) or f"result={result} rc={check_rc}"
    return summary


def _ip_in_cidr(ip_value: Any, cidr_value: Any) -> bool:
    try:
        return ipaddress.ip_address(str(ip_value)) in ipaddress.ip_network(str(cidr_value), strict=False)
    except ValueError:
        return False


def capacity_pool_row(label: str, cidr: str, capacity: int, users: list[dict[str, Any]], mode: str) -> dict[str, Any]:
    rows = [row for row in users if row.get("ip") and _ip_in_cidr(row.get("ip"), cidr)]
    active = [row for row in rows if str(row.get("enabled", "1")) == "1"]
    used = len(rows)
    free = max(int(capacity) - used, 0)
    pct = round((used / int(capacity)) * 100, 1) if int(capacity) > 0 else 0
    return {
        "label": label,
        "cidr": cidr,
        "mode": mode,
        "capacity": int(capacity),
        "registered": used,
        "active": len(active),
        "free": free,
        "used_pct": pct,
        "sample_ips": [row.get("ip") for row in rows[:5]],
    }


def capacity_state(
    *,
    capacity_kv: dict[str, Any],
    readiness_kv: dict[str, Any],
    ipam_kv: dict[str, Any],
    users: list[dict[str, Any]],
) -> dict[str, Any]:
    readiness = readiness_kv.get("V7_CAPACITY_READINESS", "UNKNOWN")
    legacy_capacity = int(readiness_kv.get("legacy_capacity") or ipam_kv.get("current_limit_10_0_0_0_24") or 253)
    ipam_capacity = int(readiness_kv.get("planned_ipam_capacity") or ipam_kv.get("target_limit_10_7_0_0_22") or 1022)
    ipam_cidr = readiness_kv.get("planned_ipam_pool") or ipam_kv.get("target_cidr") or "10.7.0.0/22"
    target_users = int(readiness_kv.get("target_users") or capacity_kv.get("target_users") or 500)
    active_users = len([row for row in users if str(row.get("enabled", "1")) == "1"])
    total_capacity = legacy_capacity + ipam_capacity
    total_registered = len(users)
    pools = [
        capacity_pool_row("Current users", "10.0.0.0/24", legacy_capacity, users, "existing clients stay here"),
        capacity_pool_row("New users IPAM", ipam_cidr, ipam_capacity, users, "new clients are allocated here"),
    ]
    warnings = []
    if readiness == "WARN":
        warnings.append("legacy /24 alone is intentionally too small for 500 users; staged IPAM pool is required")
    elif readiness not in ("OK", "WARN"):
        warnings.append("capacity readiness check needs attention")
    if active_users > total_capacity:
        warnings.append("registered active users exceed planned capacity")
    next_allocation = {
        "ip": readiness_kv.get("next_ip") or ipam_kv.get("sample_01_ip", "").split(" ")[0],
        "table": readiness_kv.get("next_table") or "",
    }
    return {
        "status": readiness,
        "target_users": target_users,
        "active_users": active_users,
        "registered_users": total_registered,
        "total_capacity": total_capacity,
        "free_capacity": max(total_capacity - total_registered, 0),
        "pools": pools,
        "next_allocation": next_allocation,
        "capacity_result": capacity_kv.get("V7_CAPACITY_RESULT", "UNKNOWN"),
        "readiness_result": readiness,
        "plain": "Existing users remain in 10.0.0.0/24. New users should be issued from the IPAM pool 10.7.0.0/22 after preview.",
        "warnings": warnings,
    }


def diagnostic_schema_contracts() -> dict[str, dict[str, Any]]:
    return {
        "diagnostic": {
            "schema": "v7.admin.diagnostic.v1",
            "read_only": True,
            "required": ["status"],
            "optional": ["warnings", "checks", "summary"],
        },
        "traffic_summary": {
            "schema": "v7.admin.traffic-summary.v1",
            "read_only": True,
            "required": ["entity_type", "entity_id", "today", "last_24h", "week", "month", "all_time"],
            "optional": ["snapshot", "updated_at"],
        },
    }
