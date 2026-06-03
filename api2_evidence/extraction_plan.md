# API.2 Extraction Plan

Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`

## Discovery Result

API.1 identified `admin/v7-admin-api` as the admin monolith and marked the first safe extraction scope as read-only registry views. The registry helpers were local pure wrappers around `users.registry` and `egress.registry` parsing/redaction/default selection.

## Classification

### EXTRACT_NOW

- `parse_registry(path)`
- `egress_registry_rows(enabled_only=False)`
- `egress_registry_map(enabled_only=False)`
- `egress_exists(egress_id, enabled_only=False)`
- `default_egress_id()`
- `egress_interface(egress_id)`
- Users registry read helpers for tests and future read-only admin views
- Lightweight per-request snapshot foundation via `AdminRegistrySnapshot`

### EXTRACT_LATER

- Operator summaries
- Evidence/timeline read builders
- Service matrix summaries
- Route-class summaries
- Broader schema contracts
- Broader request snapshot integration inside HTTP handlers

Reason: these areas are still coupled to endpoint rendering and operational state readers. Extracting them in API.2 would increase parity risk beyond the read-only registry scope.

### DO_NOT_TOUCH

- Auth
- RBAC
- CSRF
- `run_action`
- Execution handlers
- Rollback handlers
- Governance mutation
- Audit writers
- Closure writers
- UI separation
- Runtime state mutation

## Decision

Proceed with read-only registry helper extraction only. Defer operator/service/route view extraction to API.3 after the registry extraction is certified stable.
