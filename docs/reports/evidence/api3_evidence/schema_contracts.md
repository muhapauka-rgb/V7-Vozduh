# API.3 Schema Contracts

Schema contracts are defined in `admin_core.summary_builders.api3_schema_contracts()`.

Contracts:

- `overview`
- `operator_summary`
- `service_summary`
- `route_summary`
- `routing_intelligence_summary`

Purpose:

- protect future refactors
- keep extracted builders read-only
- make API.4 parity tests easier to define

All contracts are marked `read_only=true`.
