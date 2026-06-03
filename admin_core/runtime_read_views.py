"""Read-only runtime summary builders for admin surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RuntimeReadSnapshot:
    state: dict[str, Any]
    components: list[dict[str, Any]]
    service_status: dict[str, str]


def runtime_fingerprint_payload(
    components: list[dict[str, Any]],
    *,
    include_advanced: bool = False,
    storage_path: str = "",
) -> dict[str, Any]:
    present = sum(1 for item in components if item.get("present"))
    missing = [item for item in components if not item.get("present")]
    stale = [
        item for item in components
        if item.get("name") == "runtime_state" and item.get("age_sec") is not None and item.get("age_sec") > 180
    ]
    public_components = [
        {key: value for key, value in item.items() if key != "hash"}
        for item in components
    ]
    payload = {
        "status": "OK" if present and not stale else ("UNKNOWN" if not present else "STALE"),
        "summary": {
            "components_total": len(components),
            "components_present": present,
            "components_missing": len(missing),
            "stale_components": len(stale),
        },
        "components": public_components,
        "advanced_details_available": True,
        "advanced_details_role_required": "admin",
        "read_only": True,
        "non_authoritative": True,
        "storage_backend": "jsonl",
        "storage_path": storage_path,
    }
    if include_advanced:
        payload["advanced_details"] = {
            "raw_hashes_hidden_by_default": True,
            "components": components,
        }
    return payload


def service_status_payload(names: list[str], outputs: dict[str, str]) -> dict[str, str]:
    return {name: str(outputs.get(name, "")).strip() for name in names}


def proxy_runtime_payload(
    *,
    inbound_id: str,
    unit: str,
    bindings: list[dict[str, Any]],
    runtime_users: int,
    auth_user_rules: int,
    legacy_user_rules: int,
    inbound_fallback_rules: int,
    service_active: bool,
    candidate_meta: dict[str, Any],
) -> dict[str, Any]:
    binding_count = len(bindings)
    runtime_fresh = binding_count == runtime_users
    candidate_fresh = binding_count == auth_user_rules and not legacy_user_rules and not inbound_fallback_rules
    needs_refresh = binding_count > 0 and (not runtime_fresh or not candidate_fresh or not service_active)
    status = "REFRESH_REQUIRED" if needs_refresh else ("OK" if binding_count > 0 and service_active else "NOT_READY")
    reasons = []
    if binding_count != runtime_users:
        reasons.append(f"runtime_users_mismatch:bindings={binding_count}:runtime={runtime_users}")
    if binding_count != auth_user_rules:
        reasons.append(f"candidate_rules_mismatch:bindings={binding_count}:auth_user_rules={auth_user_rules}")
    if legacy_user_rules:
        reasons.append("candidate_has_legacy_user_rules")
    if inbound_fallback_rules:
        reasons.append("candidate_has_inbound_fallback")
    if not service_active:
        reasons.append("public_proxy_service_inactive")
    return {
        "inbound_id": inbound_id,
        "unit": unit,
        "status": status,
        "needs_refresh": needs_refresh,
        "binding_count": binding_count,
        "runtime_users": runtime_users,
        "candidate_auth_user_rules": auth_user_rules,
        "candidate_legacy_user_rules": legacy_user_rules,
        "candidate_inbound_fallback_rules": inbound_fallback_rules,
        "service_active": service_active,
        "candidate_status": candidate_meta.get("status", ""),
        "candidate_rendered_at": candidate_meta.get("rendered_at", ""),
        "reasons": reasons,
        "bindings": bindings[:100],
    }


def runtime_read_schema_contracts() -> dict[str, dict[str, Any]]:
    return {
        "runtime_summary": {
            "schema": "v7.admin.runtime-summary.v1",
            "read_only": True,
            "required": ["status", "summary", "components", "read_only"],
            "optional": ["advanced_details", "storage_path"],
        },
        "runtime_snapshot": {
            "schema": "v7.admin.runtime-snapshot.v1",
            "read_only": True,
            "required": ["state", "components"],
            "optional": ["service_status"],
        },
    }
