# API.4 Recommendation

## Recommended Scope

API.4 should extract the overview aggregation layer into a dedicated read-only module.

Suggested module:

- `admin_core.overview_views`

## Safe First Candidates

- overview summary aggregation
- overview registry snapshot assembly
- service/route/trusted RU aggregation from already extracted view modules
- cache metadata shaping
- schema parity fixtures for `/api/overview`

## Required API.4 Guards

- no HTTP handler movement
- no auth/RBAC/CSRF movement
- no `run_action`
- no POST handlers
- no audit writers
- no closure writers
- no rollback execution
- no governance mutation

## Precondition

Create stable `/api/overview` fixture/parity tests before moving large overview sections.
