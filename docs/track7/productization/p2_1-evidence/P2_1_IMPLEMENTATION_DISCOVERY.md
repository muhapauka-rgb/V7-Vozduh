# P2.1 Implementation Discovery

## Scope

P2.1 implements read-only foundations for future execution visibility:

- Execution Contract Store
- Execution Event Store
- Execution Read Models
- Execution Read APIs
- Execution Admin Visibility

No execution engine, runtime hook, routing apply, autoswitch apply, policy apply, killswitch mutation, Direct/RU mutation, or Trusted RU mutation was implemented.

## Existing Patterns Reused

The implementation reuses the current `admin/v7-admin-api` architecture:

- JSON/JSONL file-backed stores.
- Read-only GET APIs protected by existing admin auth.
- Existing drawer-first V7 Admin UI.
- Existing operational metadata helpers where applicable.
- Existing Evidence, Proposal, Runtime Trust, and Release Trust surfaces.
- Existing low-noise admin placement inside current sections.

## Storage Decision

Execution contracts use JSON because contracts are object-shaped and need detail lookup by `contract_id`.

Execution events use JSONL because events are append-style records and fit the same operational pattern as audit/history stores.

## Reality-First Mapping

Product Capability:
read-only execution contract/event visibility.

Admin Surface:
Главная, Пользователи, Каналы, Маршруты, Проверки, Логи.

Runtime Service:
`admin/v7-admin-api` read-only helpers and GET handlers.

Storage:
`execution-contracts.json`, `execution-events.jsonl`.

API:
`/api/execution/*` read endpoints.

UI Component:
Execution trust card, execution chips, execution drawer, timeline, event table, consistency summary.

## Verdict

implementation_discovery_completed=true
runtime_mutation_performed=false
routing_changed=false
users_moved=false
autoswitch_apply_run=false
