# Z7.3 Evidence 02 - Metadata and Duplication Inventory

## Existing Runtime Metadata

`tools/v7-users-autoswitch` already emits:

- `schema_version`
- `updated`
- `enabled`
- `mode`
- `apply_requested`
- `target_egress`
- `safety`
- `safety.generation.planner_generation_id`
- `safety.restore_barrier`
- `summary.selected_moves`
- `decisions`
- `selected_moves`
- `apply_result`

Missing:

- `operation.operation_id`
- `operation.selected_move_hash`
- `operation.runtime_snapshot_hash`
- `operation.terminal_state`
- `operation.terminal_reason`
- `operation.audit_refs`
- per-result `operation_id`

## Existing Audit Metadata

`v7-audit-log` already supports:

- `request_id`
- `object_type`
- `object_id`
- `user_ip`
- `result`
- `before_hash`
- `after_hash`
- arbitrary metadata fields.

Missing:

- no autoswitch runtime operation audit call observed.
- no first-class `operation_id`, but metadata is sufficient.

Minimum plan:

- do not change `v7-audit-log`.
- call it with `object_type=runtime`, `object_id=<operation_id>`, `metadata.operation_id=<operation_id>`, and lineage metadata.

## Existing Closure Metadata

Admin closure already supports:

- allowed object type `runtime`,
- object id,
- closure state,
- closure reason,
- closure actor,
- closure timestamp,
- Admin audit on closure-set.

Missing:

- autoswitch does not emit a closure target.

Minimum plan:

- no Admin closure schema change.
- autoswitch output includes `operation.closure_ref` or `operation.closure_target` with `object_type=runtime`, `object_id=<operation_id>`.

## Existing Lineage Metadata

Reusable lineage:

- `planner_generation_id`
- selected move list
- selected move hash helper
- restore barrier fields
- apply result rows
- verify result rows
- rollback result rows
- audit `request_id`
- closure object id

Existing parallel/legacy lineage:

- operator execution `operation_id`, `approval_id`, `packet_id`, `record_hash`
- Admin execution `contract_id`, `event_id`
- historical `BLOCK_*.md` operation ids

Duplication verdict:

- Do not introduce a new lineage store.
- Do not promote `contract_id` or `record_hash` to runtime operation truth.
- Do not create a second selected-move owner.

## Duplication Risk Per Planned Area

| Planned Area | Duplication Risk | Required Constraint |
|---|---|---|
| Operation id creation | MEDIUM | Must be created only by autoswitch for runtime cycles |
| Runtime snapshot hash | LOW/MEDIUM | Reuse existing hash helpers and generation inputs |
| Audit references | LOW | Use existing `v7-audit-log` metadata |
| Closure references | LOW | Use existing `runtime` closure object type |
| Rollback references | MEDIUM | Keep rollback under same operation id |
| Admin wrapper correlation | MEDIUM | Do not create Admin-owned runtime operation id |
| Operator observability | LOW | Reader only |

