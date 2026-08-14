# Z7.6-Z8 Evidence 01 - Operation Wiring Map

## Operation Envelope

Owner: `tools/v7-users-autoswitch`

Fields added to the existing plan output:

- `operation.operation_id`
- `operation.operation_owner`
- `operation.operation_type`
- `operation.operation_started_at`
- `operation.planner_generation_id`
- `operation.selected_move_hash`
- `operation.selected_move_count`
- `operation.runtime_snapshot_hash`
- `operation.terminal_state`
- `operation.terminal_reason`
- `operation.rollback_verdict` when rollback is attempted

Selected moves also carry additive lineage:

- `operation_id`
- `selected_move_hash`
- `selected_move_index`

## Runtime Snapshot Hash

The runtime snapshot hash is derived from existing local truth sources:

- `users.registry`
- `egress.registry`
- selected move hash

No new state file is written for the operation envelope.

## Audit Wiring

Audit reference:

- `action=runtime_operation_terminal`
- `component=autoswitch`
- `object_type=runtime_operation`
- `object_id=<operation_id>`
- `result=<terminal_state>`

Dry-run behavior:

- audit reference is present
- `emitted=false`
- `status=ready_not_emitted_dry_run`
- no audit file write is performed

Apply behavior:

- existing `v7-audit-log` is invoked after operation finalization
- audit emission result is captured as additive metadata

## Closure Wiring

Closure target reference:

- `object_type=runtime`
- `object_id=<operation_id>`
- `closure_owner=admin/v7-admin-api`
- `observability_owner=admin_core/operator_observability.py`
- `closure_state=OPEN` when audit is not emitted
- `closure_blocker=audit_missing` when audit is not emitted
- `closure_state=VERIFIED_READY` when audit emission succeeds

No new closure storage is created.

## Rollback Wiring

Existing apply verification rollback rows now include additive operation lineage:

- `operation_id`
- `selected_move_hash`
- `selected_move_index`
- `rollback_attempted`
- `rollback_result`
- `rollback_verdict`

Rollback command behavior was not changed.

