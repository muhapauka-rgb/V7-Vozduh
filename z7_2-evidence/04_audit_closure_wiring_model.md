# Z7.2 Evidence 04 - Audit and Closure Wiring Model

## Operation to Audit Linkage

Audit owner remains:

- `tools/runtime-support/v7-audit-log`

Minimum runtime operation audit references:

| Audit Field | Value |
|---|---|
| `action` | `runtime_operation_started`, `runtime_operation_terminal`, `runtime_operation_rollback` |
| `component` | `autoswitch` |
| `object_type` | `runtime_operation` |
| `object_id` | `<operation_id>` |
| `result` | terminal or step verdict |
| `request_id` | correlation id for the operation cycle |
| `before_hash` | optional runtime snapshot hash before mutation |
| `after_hash` | optional runtime snapshot hash after mutation/verification |
| `metadata.operation_id` | `<operation_id>` |
| `metadata.planner_generation_id` | generation id |
| `metadata.selected_move_hash` | selected move hash |
| `metadata.selected_move_count` | selected move count |
| `metadata.runtime_snapshot_hash` | runtime snapshot hash |
| `metadata.restore_barrier_status` | barrier verdict/status |
| `metadata.rollback_verdict` | when rollback occurred |

## Audit Event Types

Required:

1. `runtime_operation_started`
2. `runtime_operation_terminal`

Conditional:

3. `runtime_operation_rollback`
4. `runtime_operation_denied`
5. `runtime_operation_noop`

Design choice:

- Terminal event is mandatory.
- Started event is strongly recommended because it creates an early audit anchor before mutation.
- No-op and denied may be represented either as separate event types or as terminal event results, but must be searchable by operation id.

## Runtime Verdict to Audit

Runtime terminal state becomes audit `result`.

Examples:

| Terminal State | Audit Result |
|---|---|
| `COMPLETED` | `COMPLETED` |
| `ROLLED_BACK` | `ROLLED_BACK` |
| `FAILED_CLOSED` | `FAILED_CLOSED` |
| `DENIED_POLICY` | `DENIED_POLICY` |
| `DENIED_RESTORE_BARRIER` | `DENIED_RESTORE_BARRIER` |
| `NO_OP_EMPTY_SELECTION` | `NO_OP_EMPTY_SELECTION` |
| `NO_OP_DRY_RUN` | `NO_OP_DRY_RUN` |

## Operation to Closure Linkage

Closure owner remains:

- `admin/v7-admin-api`
- `admin_core/operator_observability.py`

Closure key:

```text
object_type=runtime
object_id=<operation_id>
```

This reuses an existing allowed closure object type and avoids requiring a new closure truth source.

Minimum closure references:

| Closure Field | Value |
|---|---|
| `object_type` | `runtime` |
| `object_id` | `<operation_id>` |
| `closure_state` | `VERIFIED`, `CLOSED`, `EXPIRED`, or `OPEN` |
| `closure_reason` | terminal state + audit reference |
| `closure_actor` | operator/admin/system actor |
| `closure_timestamp` | closure time |

Minimum closure reason references:

- `operation_id`,
- terminal state,
- audit `request_id` or audit event reference,
- rollback verdict if present,
- selected move count,
- selected move hash,
- planner generation id.

## Audit to Closure

Closure must depend on audit presence:

```text
operation terminal verdict
  -> audit event exists
  -> closure record may be VERIFIED/CLOSED
```

If audit is missing:

- closure should remain `OPEN`, or
- closure should be `EXPIRED` with reason `audit_missing`, depending on lifecycle age.

## Operator Observability

Operator observability should consume:

- operation id,
- runtime verdict,
- audit refs,
- closure refs,
- rollback lineage,
- selected move lineage,
- restore-barrier lineage.

It must remain a reader/summary layer, not the operation truth source.

