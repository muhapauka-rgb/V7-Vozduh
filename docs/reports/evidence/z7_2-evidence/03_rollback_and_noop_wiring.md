# Z7.2 Evidence 03 - Rollback and No-Op Wiring

## Rollback Wiring

Rollback remains part of the same operation.

Normal rollback branch:

```text
operation_id
  -> selected_move_hash
  -> selected_move_index
  -> execution result
  -> verification failure
  -> rollback attempt
  -> rollback verdict
  -> terminal runtime verdict
  -> audit
  -> closure
```

Required rollback fields:

| Field | Source |
|---|---|
| `operation_id` | Autoswitch operation envelope |
| `rollback_id` | Deterministic/reference id inside operation output, not a new truth source |
| `rollback_type` | `autoswitch_verify_failure` or `break_glass_generic` |
| `rollback_target` | Existing previous/current egress target |
| `rollback_reason` | Existing verify failure or operator reason |
| `selected_move_hash` | Autoswitch selected move hash |
| `planner_generation_id` | Autoswitch generation |
| `runtime_snapshot_hash` | Runtime recheck hash |
| `rollback_rc` | Existing apply result |
| `rollback_output_ref` | Existing rollback output excerpt/reference |
| `rollback_verdict` | `ROLLBACK_SUCCEEDED`, `ROLLBACK_FAILED`, `ROLLBACK_NOT_REQUIRED` |

## Generic Rollback Wiring

`v7-rollback-last-change` remains a generic break-glass primitive.

Design rule:

- It does not create a new operation.
- It receives or references an existing `operation_id` when invoked in an operation context.
- If used without operation context, Admin/break-glass wrapper must create or require a break-glass operation id before audit/closure.

Minimum references:

- `operation_id`,
- `rollback_target`,
- `backup_source`,
- `target_kind`,
- `restart_required`,
- `sensitive_material`,
- `actor`,
- `reason`,
- audit `request_id`.

## Rollback Audit Linkage

Every rollback event should audit:

```text
action=runtime_operation_rollback
component=autoswitch|rollback
object_type=runtime_operation
object_id=<operation_id>
result=<rollback verdict>
request_id=<audit correlation id>
metadata.operation_id=<operation_id>
metadata.rollback_id=<rollback id>
metadata.rollback_type=<type>
metadata.selected_move_hash=<hash>
```

## Rollback Closure Linkage

Closure remains operation-level:

```text
closure.object_type=runtime
closure.object_id=<operation_id>
closure.reason includes rollback verdict and audit reference
```

Rollback does not get a separate closure truth source. It is a lifecycle fact under the same operation.

## No-Op Wiring

Every no-op must be an operation with a terminal state and audit reference.

| No-Op / Denial | Terminal State | Required References |
|---|---|---|
| `selected_moves=0` | `NO_OP_EMPTY_SELECTION` | operation id, generation, selected move hash, selected move count |
| policy denied | `DENIED_POLICY` | operation id, policy mode, generation |
| trust denied | `DENIED_TRUST` | operation id, trust blocker, generation |
| capacity denied | `DENIED_CAPACITY` | operation id, target/capacity facts |
| restore barrier denied | `DENIED_RESTORE_BARRIER` | operation id, barrier reason, generation, selected move hash |
| replay denied | `DENIED_REPLAY` | operation id, approval id or packet id when present, record hash when present |
| dry-run | `NO_OP_DRY_RUN` | operation id, generation, selected move hash, selected move count |
| observe mode | `NO_OP_OBSERVE` | operation id, mode, generation |

## No-Op Audit

No-op audit should use the same audit sink:

```text
action=runtime_operation_terminal
component=autoswitch
object_type=runtime_operation
object_id=<operation_id>
result=<terminal_state>
metadata.terminal_reason=<reason>
```

No-op does not mean no operation. It means no mutation.

