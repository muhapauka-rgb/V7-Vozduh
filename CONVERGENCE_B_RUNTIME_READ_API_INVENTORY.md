# Convergence B Runtime Read API Inventory

Project: V7 Vozduh
Block: Convergence B

## Scope

Runtime-only execution read APIs are deployed in runtime Admin API and absent from `origin/Updatesystem`.

| API | Purpose | Inputs | Outputs | Dependencies | Storage | UI | Tests | Retention impact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `/api/execution/summary` | summary of execution contracts/events | query params | counts, recent contracts/events, consistency | execution contract/event readers | execution contracts JSON, events JSONL | execution summary drawer | future Wave 1 API/read-only test | reads only; no growth |
| `/api/execution/contracts` | list contracts | query params, pagination | contract summaries | contract normalization helpers | execution contracts JSON | contract list UI | future list/filter tests | reads only |
| `/api/execution/contracts/` | contract detail by id | path id | contract, timeline, events, verification, rollback | contract lookup, event lookup | execution contracts/events | contract detail drawer | future detail tests | reads only |
| `/api/execution/events` | list execution events | query params | event summaries | event normalization helpers | execution events JSONL | timeline/event UI | future event tests | reads only |
| `/api/execution/timeline` | timeline view | query params or contract id | normalized timeline items | contracts/events | execution stores | `executionTimelineHtml` | future ordering tests | reads only |
| `/api/execution/verification` | verification state read model | query/contract | verification summary | contract normalization | execution contracts/events | verification panel | future state tests | reads only |
| `/api/execution/rollback` | rollback state read model | query/contract | rollback summary | contract rollback manifest | execution contracts | rollback panel | future rollback read tests | reads only |
| `/api/execution/explain` | explain contract/read model | query/contract | explanation payload | contracts/events/verification/rollback helpers | execution stores | explain/detail UI | future explain tests | reads only |

## Runtime Helper Set

Core runtime read API helpers include:

- `safe_execution_id`
- `execution_contract_store_rows`
- `normalize_execution_contract`
- `execution_contracts`
- `normalize_execution_event`
- `execution_events`
- `execution_contract_by_id`
- `execution_events_for_contract`
- `execution_contract_summary_item`
- `execution_store_consistency`
- `execution_summary_response`
- `execution_contracts_response`
- `execution_contract_detail_response`
- `execution_timeline_items`
- `execution_timeline_response`
- `execution_events_response`
- `execution_verification_summary`
- `execution_verification_response`
- `execution_rollback_summary`
- `execution_rollback_response`
- `execution_explain_response`

runtime_read_api_inventory_complete=true
