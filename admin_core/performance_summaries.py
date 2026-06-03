"""Read-only performance summary architecture for admin decomposition."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ReadCounter:
    counts: dict[str, int] = field(default_factory=dict)

    def mark(self, name: str) -> None:
        self.counts[name] = self.counts.get(name, 0) + 1

    def snapshot(self) -> dict[str, int]:
        return dict(sorted(self.counts.items()))


def measure(label: str, fn: Callable[[], Any]) -> tuple[Any, dict[str, Any]]:
    started = time.perf_counter()
    value = fn()
    elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
    return value, {"label": label, "elapsed_ms": elapsed_ms}


def overview_dependency_map() -> dict[str, Any]:
    return {
        "overview": [
            "state_snapshot",
            "users_registry",
            "egress_registry",
            "route_reality",
            "service_matrix",
            "draft_egress_evidence",
            "service_preferences",
            "direct_routing",
            "trusted_ru",
            "identity",
            "proxy_runtime",
            "capacity_plan",
            "client_speed",
            "profile_delivery",
            "audit_tail",
            "switch_history_tail",
            "maintenance",
        ],
        "expensive_reads": [
            "route_reality_per_user_probe",
            "direct_routing_probe",
            "service_status_systemctl",
            "capacity_command_reads",
            "traffic_sqlite_summary",
            "audit_jsonl_tail",
        ],
        "repeated_reads_reduced_in_api4": [
            "users_registry",
        ],
        "read_only_payload_builders_extracted_in_api5": [
            "runtime_fingerprint",
            "proxy_runtime",
            "route_status",
            "direct_routing",
            "traffic_summary",
            "client_speed",
            "killswitch",
            "capacity_plan",
        ],
    }


def runtime_path_map() -> dict[str, Any]:
    return {
        "runtime_platform": "server_owned",
        "runtime_state": "read_only_in_admin_request",
        "execution": "not_owned_by_overview_layer",
        "rollback": "not_owned_by_overview_layer",
        "governance_mutation": "not_owned_by_overview_layer",
    }


def admin_path_map() -> dict[str, Any]:
    return {
        "request_entry": "admin/v7-admin-api Handler",
        "overview_orchestration": "admin/v7-admin-api overview",
        "overview_builders": "admin_core.overview_views",
        "registry_views": "admin_core.admin_registry_views",
        "service_views": "admin_core.service_views",
        "route_views": "admin_core.route_views",
        "runtime_read_views": "admin_core.runtime_read_views",
        "route_reality_views": "admin_core.route_reality_views",
        "diagnostic_views": "admin_core.diagnostic_views",
        "operator_views": "admin_core.operator_views",
        "shared_summaries": "admin_core.summary_builders",
        "performance_architecture": "admin_core.performance_summaries",
    }


def cache_candidates() -> list[dict[str, Any]]:
    return [
        {"name": "overview", "key": "state_registry_policy_mtimes", "ttl_seconds": 10},
        {"name": "service_matrix", "key": "service_matrix_file_mtime", "ttl_seconds": 30},
        {"name": "route_reality", "key": "users_registry_and_egress_registry_mtimes", "ttl_seconds": 15},
        {"name": "trusted_ru", "key": "trusted_ru_state_files_mtime", "ttl_seconds": 60},
        {"name": "traffic_summary", "key": "traffic_db_mtime", "ttl_seconds": 30},
        {"name": "runtime_fingerprint", "key": "runtime_component_mtimes", "ttl_seconds": 15},
        {"name": "proxy_runtime", "key": "proxy_runtime_file_mtimes_and_service_state", "ttl_seconds": 10},
        {"name": "direct_routing", "key": "direct_domain_state_and_user_ip", "ttl_seconds": 30},
        {"name": "audit_tail", "key": "audit_file_size_and_mtime", "ttl_seconds": 10},
    ]


def background_aggregation_candidates() -> list[str]:
    return [
        "route_reality_snapshot",
        "traffic_summary_snapshot",
        "trusted_ru_diagnostic_snapshot",
        "service_matrix_refresh",
        "client_speed_rollup",
        "overview_boot_payload",
    ]


def async_candidates() -> list[str]:
    return [
        "direct_routing_probe",
        "trusted_ru_live_diagnostic",
        "route_status_per_user_probe",
        "traffic_live_probe",
        "capacity_command_reads",
        "proxy_runtime_service_probe",
        "runtime_fingerprint_hash_reads",
    ]


def forbidden_request_path_items() -> list[str]:
    return [
        "runtime_execution",
        "rollback_execution",
        "governance_mutation",
        "audit_append",
        "closure_append",
        "service_restart",
        "autoswitch_apply",
        "user_movement",
    ]


def performance_architecture_summary() -> dict[str, Any]:
    return {
        "runtime_path_map": runtime_path_map(),
        "admin_path_map": admin_path_map(),
        "cache_candidates": cache_candidates(),
        "background_aggregation_candidates": background_aggregation_candidates(),
        "async_candidates": async_candidates(),
        "forbidden_request_path_items": forbidden_request_path_items(),
        "dependency_map": overview_dependency_map(),
    }


def api5_performance_foundation() -> dict[str, Any]:
    return {
        "schema": "v7.admin.api5-performance-foundation.v1",
        "read_only": True,
        "request_snapshot_extension": [
            "RuntimeReadSnapshot",
            "RouteRealitySnapshot",
            "DiagnosticSnapshot",
        ],
        "payload_builder_modules": [
            "admin_core.runtime_read_views",
            "admin_core.route_reality_views",
            "admin_core.diagnostic_views",
        ],
        "no_cache_enabled": True,
        "cache_candidates": cache_candidates(),
        "async_candidates": async_candidates(),
        "forbidden_request_path_items": forbidden_request_path_items(),
    }
