"""Read-only overview view builders for the V7 admin API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class OverviewSnapshot:
    state: dict[str, Any]
    users_registry: list[dict[str, Any]]
    egress_registry: list[dict[str, Any]]
    draft_evidence: dict[str, Any]

    @property
    def users(self) -> list[dict[str, Any]]:
        users = self.state.get("users")
        return users if isinstance(users, list) else self.users_registry

    @property
    def active_users(self) -> list[dict[str, Any]]:
        return [user for user in self.users if str(user.get("enabled", "1")) == "1"]

    @property
    def egress_state(self) -> dict[str, Any]:
        egress = self.state.get("egress", {})
        return egress if isinstance(egress, dict) else {}


def create_snapshot(
    *,
    state: dict[str, Any],
    users_registry: list[dict[str, Any]],
    egress_registry: list[dict[str, Any]],
    draft_evidence: dict[str, Any] | None = None,
) -> OverviewSnapshot:
    return OverviewSnapshot(
        state=state if isinstance(state, dict) else {},
        users_registry=list(users_registry or []),
        egress_registry=list(egress_registry or []),
        draft_evidence=draft_evidence if isinstance(draft_evidence, dict) else {},
    )


def egress_health_summary(egress: dict[str, Any], draft_evidence: dict[str, Any]) -> dict[str, Any]:
    healthy = 0
    healthy_ids = set()
    for egress_id, item in (egress or {}).items():
        if str(item.get("code")) == "200" and str(item.get("diagnose_severity", "")).upper() in ("OK", ""):
            healthy += 1
            healthy_ids.add(egress_id)
    for egress_id, evidence in ((draft_evidence or {}).get("items") or {}).items():
        if egress_id not in healthy_ids and evidence.get("ready"):
            healthy += 1
            healthy_ids.add(egress_id)
    return {"healthy": healthy, "healthy_ids": sorted(healthy_ids)}


def build_summary(
    *,
    users: list[dict[str, Any]],
    active_users: list[dict[str, Any]],
    egress: dict[str, Any],
    healthy: int,
    route_rows: list[dict[str, Any]],
    killswitch_state: dict[str, Any],
    capacity_plan: dict[str, Any],
    stale: dict[str, Any],
    client_speed_users: dict[str, dict[str, Any]],
    active_readiness: dict[str, dict[str, Any]],
    active_onboarding: dict[str, dict[str, Any]],
    direct_routing: dict[str, Any],
    identity: dict[str, Any],
    proxy_runtime: dict[str, Any],
) -> dict[str, Any]:
    killswitch_status = killswitch_state.get("normalized_status") or "CHECK"
    killswitch_ok = bool(killswitch_state.get("ok"))
    return {
        "users_total": len(active_users),
        "users_registry_total": len(users),
        "egress_total": len(egress),
        "egress_healthy": healthy,
        "route_ok": sum(1 for row in route_rows if row["ok"]),
        "route_leak_risk": any(row["leak_risk"] for row in route_rows),
        "killswitch_ok": killswitch_ok,
        "killswitch_status": killswitch_status,
        "killswitch_reason": killswitch_state.get("reason", ""),
        "killswitch_check_rc": killswitch_state.get("check_rc"),
        "capacity_ok": capacity_plan.get("readiness_result") in ("OK", "WARN"),
        "capacity_status": capacity_plan.get("readiness_result", "UNKNOWN"),
        "stale_ok": "V7_STALE_RESULT=OK" in stale["output"],
        "client_agents_online": sum(1 for row in client_speed_users.values() if row["agent_online"]),
        "users_ready": sum(1 for row in active_readiness.values() if row.get("status") == "READY"),
        "users_waiting": sum(1 for row in active_readiness.values() if row.get("status") == "WAITING"),
        "users_blocked": sum(1 for row in active_readiness.values() if row.get("status") == "BLOCKED"),
        "users_ready_to_deliver": sum(1 for row in active_onboarding.values() if row.get("stage") == "ready_to_deliver"),
        "users_link_sent": sum(1 for row in active_onboarding.values() if row.get("stage") == "link_sent"),
        "users_downloaded_waiting": sum(1 for row in active_onboarding.values() if row.get("stage") == "downloaded_waiting_connection"),
        "direct_ru_route_ok": bool(direct_routing.get("route_ok")),
        "identity_users": int((identity.get("summary") or {}).get("identity_users") or 0),
        "identity_allowed_users": int((identity.get("summary") or {}).get("allowed_users") or 0),
        "proxy_runtime_status": proxy_runtime.get("status", "UNKNOWN"),
        "proxy_runtime_ok": proxy_runtime.get("status") == "OK",
        "proxy_runtime_needs_refresh": bool(proxy_runtime.get("needs_refresh")),
    }


def build_registries(
    *,
    users_registry: list[dict[str, Any]],
    egress_registry: list[dict[str, Any]],
    egress_flags: str,
    egress_flags_map: dict[str, Any],
) -> dict[str, Any]:
    return {
        "users": users_registry,
        "egress": egress_registry,
        "egress_flags": egress_flags,
        "egress_flags_map": egress_flags_map,
    }


def build_checks(
    *,
    stale: dict[str, Any],
    killswitch: dict[str, Any],
    killswitch_state: dict[str, Any],
    capacity: dict[str, Any],
    capacity_readiness: dict[str, Any],
    ipam_preview: dict[str, Any],
    direct_routing: dict[str, Any],
    trusted_ru: dict[str, Any],
    rebalance: dict[str, Any],
) -> dict[str, Any]:
    return {
        "stale": stale,
        "killswitch": killswitch,
        "killswitch_summary": killswitch_state,
        "capacity": capacity,
        "capacity_readiness": capacity_readiness,
        "ipam_preview": ipam_preview,
        "direct_routing": direct_routing.get("quick_test", {}),
        "trusted_ru": {
            "rc": 0,
            "output": f"updated={trusted_ru.get('updated', '')}\nlocal_ok={trusted_ru.get('local_ok', 0)}/{trusted_ru.get('total', 0)}\ntemporary_ok={trusted_ru.get('temporary_ok', 0)}\nblocked={trusted_ru.get('blocked', 0)}",
        },
        "rebalance_preview": rebalance,
    }


def overview_schema_contract() -> dict[str, Any]:
    return {
        "schema": "v7.admin.overview.v1",
        "read_only": True,
        "required": [
            "updated",
            "host",
            "bind",
            "access",
            "state_age_sec",
            "services",
            "summary",
            "state",
            "registries",
            "service_matrix",
            "route_reality",
            "checks",
            "events",
        ],
        "snapshot_foundation": {
            "state": "single_read_per_overview_request",
            "users_registry": "single_read_per_overview_request",
            "egress_registry": "single_read_per_overview_request",
            "draft_evidence": "single_builder_result_reused",
        },
    }


def api4_schema_contracts() -> dict[str, dict[str, Any]]:
    return {
        "overview": overview_schema_contract(),
        "dashboard": {
            "schema": "v7.admin.dashboard.v1",
            "read_only": True,
            "required": ["summary", "checks", "route_reality", "service_matrix"],
            "optional": ["operator", "cache", "performance"],
        },
        "summary": {
            "schema": "v7.admin.summary.v1",
            "read_only": True,
            "required": ["users_total", "egress_total", "route_ok", "capacity_status", "proxy_runtime_status"],
            "optional": ["client_agents_online", "direct_ru_route_ok", "identity_users"],
        },
        "service_summary": {
            "schema": "v7.admin.service-summary.v1",
            "read_only": True,
            "required": ["service_matrix", "service_recommendations"],
            "optional": ["service_preferences", "draft_egress_evidence"],
        },
        "route_summary": {
            "schema": "v7.admin.route-summary.v1",
            "read_only": True,
            "required": ["route_reality", "direct_routing", "trusted_ru", "trusted_ru_readiness"],
            "optional": ["policy_domains", "smart_mode_routes"],
        },
        "routing_intelligence_summary": {
            "schema": "v7.admin.routing-intelligence-summary.v1",
            "read_only": True,
            "required": ["service_recommendations"],
            "optional": ["routing_brain_advice", "service_intelligence_scores"],
        },
    }
