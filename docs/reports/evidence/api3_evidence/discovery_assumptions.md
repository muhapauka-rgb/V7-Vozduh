# API.3 Discovery Gate

Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`

## Rechecked Assumptions

- API.1 architecture map exists in `docs/reports/evidence/api1_evidence/`.
- API.2 registry extraction exists in `admin_core/admin_registry_views.py`.
- API.2 endpoint inventory was unchanged.
- Runtime mutation, governance mutation, rollback execution, auth, RBAC, CSRF, `run_action`, audit writers, and closure writers remain outside API.3 scope.

## Existing Owners

- Operator observability owner already existed: `admin_core/operator_observability.py`.
- Registry read-view owner exists from API.2: `admin_core/admin_registry_views.py`.
- Service view logic was still embedded in `admin/v7-admin-api`.
- Trusted RU route summary logic was still embedded in `admin/v7-admin-api`.
- Shared query/pagination/JSONL read helpers were still embedded in `admin/v7-admin-api`.

## Safe Extraction Candidates

### EXTRACT_NOW

- Operator facade wrappers over the existing operator observability owner
- Service matrix pure builders
- Service recommendation pure builder
- Trusted RU parse/status/summary builders
- Query/pagination helpers
- Bounded JSONL reader foundation
- Schema contracts for future view parity

### EXTRACT_LATER

- Full overview builder decomposition
- Traffic SQLite summaries
- Direct routing live checks
- Route dry-run helpers that call `run_readonly`
- UI-side separation

### DO_NOT_TOUCH

- HTTP handler dispatch
- Auth/RBAC/CSRF
- `run_action`
- POST apply handlers
- rollback apply
- governance mutation
- audit writers
- closure writers
