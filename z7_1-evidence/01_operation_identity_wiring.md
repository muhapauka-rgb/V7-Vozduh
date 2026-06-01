# Z7.1 Evidence 01 - Operation Identity Wiring

## Identity Inventory

| Identity | Found In | Reality Status | Classification |
|---|---|---|---|
| `operation_id` | `admin_core/operator_execution.py`, `admin_core/operator_observability.py`, `admin/v7-admin-api` operator APIs and P2.7 candidate surfaces | PARTIAL | REUSE, EXTEND |
| `proposal_id` | Admin proposal model | CONNECTED to proposal/evidence layer | REUSE |
| `approval_id` | Operator execution packet audit and observability previews | CONNECTED to governance audit, not runtime movement | REUSE |
| `packet_id` | Operator execution packet audit | CONNECTED to governance audit, not runtime movement | REUSE |
| `contract_id` | Admin execution contract store | CONNECTED to read-only execution contract/event layer | REUSE, DO NOT PROMOTE AS OPERATION ROOT |
| `event_id` | Admin execution event store | CONNECTED to read-only execution event layer | REUSE |
| `selected_move_hash` | Autoswitch internal selected move hash; operator execution expected selected hash; observability preview | PARTIAL | REUSE, EXTEND |
| `planner_generation_id` | Autoswitch `_generation_status`; restore barrier generation check; observability generation preview | PARTIAL | REUSE, EXTEND |
| `runtime_snapshot_hash` | Operator execution runtime recheck | PARTIAL | REUSE, EXTEND |
| audit `request_id` | `v7-audit-log`, Admin audit surfaces | CONNECTED audit identity, not operation root | REUSE |
| `record_hash` | Operator execution append-only records and rehearsal preview | CONNECTED governance identity, not runtime root | REUSE |

## Where `operation_id` Exists

`operation_id` exists in working code in these areas:

- `admin_core/operator_execution.py`: packet-derived governance/audit records include `operation_id`.
- `admin_core/operator_observability.py`: historical operation summaries derive `operation_id` from report filenames and pass it through detail/search/audit export/governance/rehearsal preview functions.
- `admin/v7-admin-api`: operator endpoints accept/query operation detail, audit export preview, execution governance preview, and execution rehearsal preview by `operation_id`.
- P2.7 candidate surfaces derive candidate `operation_id` values and feed operator previews.

## Where `operation_id` Does Not Exist

`operation_id` was not found in:

- `tools/v7-users-autoswitch`.
- `tools/runtime-support/v7-audit-log` as a first-class field.
- `tools/runtime-support/v7-rollback-last-change`.

This is the main runtime wiring gap.

## Propagation Reality

| Flow | Status | Notes |
|---|---|---|
| Historical report -> operator operation summary | CONNECTED | `operation_id` is derived from report path/block id. |
| Operator operation -> audit export preview | CONNECTED | Preview-only, historical/read-only. |
| Operator packet -> governance audit record | CONNECTED | Append-only governance audit includes `operation_id`. |
| Autoswitch runtime -> `operation_id` | MISSING | Autoswitch output does not carry operation identity. |
| Autoswitch runtime -> canonical audit `operation_id` | MISSING | No runtime audit call with operation metadata observed. |
| Autoswitch runtime -> closure `operation_id` | MISSING | Closure can close object type `runtime`, but autoswitch does not emit closure object id. |
| Generic rollback -> `operation_id` | MISSING | Rollback primitive has no operation lineage. |

## Verdict

Operation identity wiring is understood and partial.

Canonical `operation_id` exists, but it is currently an operator/governance/historical identity, not an end-to-end autoswitch runtime identity.

