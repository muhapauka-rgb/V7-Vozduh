# API.3 Extraction Summary

## New Modules

- `admin_core/operator_views.py`
- `admin_core/service_views.py`
- `admin_core/route_views.py`
- `admin_core/summary_builders.py`

## Extracted Operator Views

`admin_core/operator_views.py` wraps and reuses the existing `admin_core.operator_observability` owner for:

- operator overview model
- approval preview
- lineage archive
- operation detail
- audit search
- audit export preview
- execution governance preview
- execution rehearsal preview
- evidence archive
- evidence file detail

## Extracted Service Views

`admin_core/service_views.py` owns pure builders for:

- Telegram service status interpretation
- service matrix Telegram state
- route-class service fitness
- service matrix row normalization
- service list normalization
- user priority service resolution
- service recommendation summaries

## Extracted Route Views

`admin_core/route_views.py` owns pure builders for:

- Trusted RU key normalization
- Trusted RU domain status
- Trusted RU probe parsing
- Trusted RU decision summary
- Trusted RU diagnostic summary
- Trusted RU readiness summary

## Extracted Shared Builders

`admin_core/summary_builders.py` owns:

- query value extraction
- pagination extraction
- bounded JSONL readers
- API.3 schema contracts

## What Remained

- `admin/v7-admin-api` still owns HTTP route dispatch, auth/session context, and runtime-bound reads.
- Runtime command readers such as `run_readonly` remain in the monolith.
- All mutation handlers remain untouched.
