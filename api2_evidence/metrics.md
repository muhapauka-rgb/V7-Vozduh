# API.2 Metrics

## Line Counts

- `admin/v7-admin-api` before: `36468`
- `admin/v7-admin-api` after: `36459`
- lines removed from monolith: `9`
- `admin_core/admin_registry_views.py`: `163`
- `tests/unit/test_admin_registry_views.py`: `97`

## Extracted Functions

- `read_text`
- `safe_egress_id`
- `safe_user_ip`
- `parse_registry`
- `registry_rows`
- `registry_map`
- `egress_registry_rows`
- `egress_registry_map`
- `egress_exists`
- `default_egress_id`
- `egress_interface`
- `users_registry_rows`
- `users_registry_map`
- `default_active_user_ip`
- `AdminRegistrySnapshot.load`
- `AdminRegistrySnapshot.egress_rows`
- `AdminRegistrySnapshot.egress_map`
- `AdminRegistrySnapshot.users_rows`
- `AdminRegistrySnapshot.users_map`
- `AdminRegistrySnapshot.default_egress_id`
- `AdminRegistrySnapshot.egress_interface`

## Remaining Monolith Size

`admin/v7-admin-api` remains large at `36459` lines. API.2 intentionally kept the extraction narrow to avoid mutation, auth, governance, execution, rollback, audit, closure, or UI changes.

## Next Safest API.3 Scope

API.3 should target read-only operator/service/route summaries only after adding parity fixtures for:

- operator summary payloads
- evidence/timeline read payloads
- service matrix summary payloads
- route-class summary payloads

No mutation handlers should be included in API.3.
