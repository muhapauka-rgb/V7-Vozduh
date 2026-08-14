# API.4 Schema Contracts

Schema contracts are defined in:

- `admin_core.overview_views.overview_schema_contract()`
- `admin_core.overview_views.api4_schema_contracts()`

Contracts:

- `overview`
- `dashboard`
- `summary`
- `service_summary`
- `route_summary`
- `routing_intelligence_summary`

All contracts are read-only.

Purpose:

- protect overview parity
- define future cache boundaries
- make API.5 extraction safer
