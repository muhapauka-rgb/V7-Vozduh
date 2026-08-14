# API.5 Duplication Audit

## Existing Ownership Reused

- `admin/v7-admin-api` remains the only admin HTTP handler and endpoint router.
- `run_readonly` remains owned by `admin/v7-admin-api`.
- Registry parsing remains owned by existing registry helpers.
- API.4 performance architecture remains owned by `admin_core.performance_summaries`.

## New Read-Only Owners

- `admin_core.runtime_read_views`
  - Runtime fingerprint payloads
  - Proxy runtime payload classification
  - Service status payload normalization

- `admin_core.route_reality_views`
  - Route reality rows
  - Direct-routing domain parsing
  - Direct-routing freshness and quick summaries

- `admin_core.diagnostic_views`
  - Traffic payloads
  - Client speed summaries
  - Killswitch summaries
  - Capacity plan summaries

## Duplicate Authority Check

- Duplicate execution paths: none added
- Duplicate schedulers: none added
- Duplicate state writers: none added
- Duplicate auth paths: none added
- Duplicate endpoint routers: none added
- Duplicate governance paths: none added

## Remaining Intentional Boundary

The monolith still performs runtime reads and command calls. This is intentional for API.5 because extracted modules are pure payload builders and do not execute commands.
