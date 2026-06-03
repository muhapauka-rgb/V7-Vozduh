# PROGRAM API.4 OVERVIEW LAYER SNAPSHOT FOUNDATION AND PERFORMANCE SUMMARY ARCHITECTURE REPORT

Project: V7 Vozduh
Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`

## Human Explanation

API.4 created the first overview-specific performance architecture layer without changing runtime, governance, execution, rollback, auth, CSRF, audit writers, or closure writers.

The important change is structural: `overview()` now has a request-scoped snapshot boundary and delegates summary, registry payload, checks payload, schema contracts, and performance planning to `admin_core`. This prepares a future cache/background aggregation layer while preserving current behavior.

## Overview Architecture

New module:

- `admin_core.overview_views`

Responsibilities:

- `OverviewSnapshot`
- request-scoped overview snapshot creation
- active user derivation
- egress health summary
- overview summary builder
- registry payload builder
- checks payload builder
- overview/API.4 schema contracts

`admin/v7-admin-api` still owns orchestration and runtime-bound reads. This keeps behavior stable while reducing duplicated reads and separating pure payload construction.

## Snapshot Architecture

The API.4 snapshot is request-scoped only. It does not cache across requests.

Snapshot inputs:

- runtime state
- users registry
- egress registry
- draft evidence

Derived values:

- effective users
- active users
- egress state

Applied improvement:

- `overview()` now reads `users.registry` once and reuses it for fallback users and `registries.users`.

## Summary Architecture

New module:

- `admin_core.performance_summaries`

Responsibilities:

- runtime path map
- admin path map
- overview dependency map
- cache candidates
- background aggregation candidates
- async candidates
- request-path forbidden items

This is a planning layer for future fast operator UX. It does not execute runtime commands or mutate state.

## Performance Findings

Before API.4:

- `overview()` could parse `users.registry` twice in one request.
- summary/check/registry payload construction was inline in the monolith.

After API.4:

- `users.registry` parse inside `overview()` is one request-scoped read.
- pure builders are separated.
- schema boundaries are explicit.
- future cache/aggregation targets are documented.

Pure builder timing sample:

- `overview_summary_builder`: `0.035 ms`
- `egress_health_summary`: `0.011 ms`

Live `overview()` benchmarking was not performed because it invokes read-only runtime/probe commands. API.4 remained behavior-preserving and did not add production measurement actions.

## Cache Opportunities

- overview payload by state/registry/policy mtimes
- service matrix by file mtime
- route reality by registry mtimes
- Trusted RU by state file mtimes
- traffic summary by SQLite mtime
- audit tail by file size/mtime

## Async Opportunities

- direct routing probe
- Trusted RU live diagnostic
- route status per-user probe
- traffic live probe
- capacity command reads

## Remaining Hotspots

- `html_page_v2`
- `Handler`
- `overview()` orchestration
- per-user route probes
- direct/trusted live checks
- traffic SQLite summaries
- mutation/action response wrappers

## API.5 Recommendation

API.5 should extract read-only runtime command read adapters and route reality snapshots.

Suggested modules:

- `admin_core.runtime_read_views`
- `admin_core.route_reality_views`

Required guardrails:

- no runtime execution
- no rollback execution
- no governance mutation
- no auth/RBAC/CSRF movement
- no audit or closure writers
- endpoint inventory unchanged
- overview fixture parity

## Tests

Commands:

```bash
PYTHONPYCACHEPREFIX=/tmp/api4_pycache python3 -m py_compile admin/v7-admin-api admin_core/overview_views.py admin_core/performance_summaries.py
python3 -m unittest tests.unit.test_api4_overview_performance
python3 -m unittest discover tests
```

Results:

- compile: `OK`
- focused API.4 tests: `OK`, `5` tests
- full suite: `OK`, `216` tests
- endpoint inventory unchanged: `264` -> `264`

## Metrics

- monolith before API.4: `36046`
- monolith after API.4: `36034`
- lines removed from monolith: `12`
- new API.4 admin_core lines: `354`
- API.4 test lines: `108`

## Final Verdicts

- `overview_views_extracted=true`
- `snapshot_foundation_created=true`
- `performance_summary_layer_created=true`
- `schema_contracts_created=true`
- `performance_audit_complete=true`
- `runtime_behavior_preserved=true`
- `governance_behavior_preserved=true`
- `tests_pass=true`
- `safe_to_begin_API5=true`
