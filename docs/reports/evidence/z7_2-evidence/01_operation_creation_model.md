# Z7.2 Evidence 01 - Operation Creation Model

## Creation Owner

Canonical creator:

- `tools/v7-users-autoswitch`

Reason:

- It is the runtime owner.
- It starts the actual runtime cycle after systemd invocation.
- It owns planning, selected moves, recheck, execution, verification, rollback, and terminal verdict.

No other component may create the canonical runtime operation id for an autoswitch runtime cycle.

## Creation Time

`operation_id` must be created once per autoswitch runtime cycle:

1. after autoswitch has initialized runtime context and loaded state inputs,
2. before planning output is finalized,
3. before any selected moves are treated as executable,
4. before any terminal no-op/denial/dry-run result is returned.

This ensures every outcome has identity:

- applied operation,
- no-op operation,
- denied operation,
- dry-run operation,
- observe-mode operation,
- restore-barrier-denied operation,
- replay-denied operation when a replay context exists,
- failed/rolled-back operation.

## Creation Inputs

The operation identity should be derived from existing fields only:

Required inputs:

- runtime owner: `tools/v7-users-autoswitch`,
- timestamp: operation start time,
- mode,
- apply_requested,
- target_egress if present,
- `planner_generation_id`,
- restore barrier status digest or referenced fields,
- selected move hash once selected moves are computed.

Allowed correlation:

- `request_id` may be created for audit correlation, but must not replace `operation_id`.

Not allowed:

- new external ID service,
- new storage table,
- new operation truth source,
- Admin-created runtime operation id for autoswitch cycle,
- `contract_id` as canonical runtime operation id.

## Operation Envelope

Every runtime cycle should produce an operation envelope in the autoswitch JSON output.

Minimum design:

```json
{
  "operation": {
    "operation_id": "<canonical runtime operation id>",
    "operation_owner": "tools/v7-users-autoswitch",
    "operation_kind": "autoswitch_runtime_cycle",
    "operation_started_at": "<iso timestamp>",
    "operation_mode": "observe|guarded|active|disabled",
    "apply_requested": true,
    "target_egress": "",
    "planner_generation_id": "",
    "selected_move_hash": "",
    "selected_move_count": 0,
    "runtime_snapshot_hash": "",
    "terminal_state": "",
    "terminal_reason": ""
  }
}
```

This is output wiring, not a new store.

## First Copy

First copy belongs in autoswitch runtime output:

```text
tools/v7-users-autoswitch JSON root
  -> operation.operation_id
```

Secondary copies are references:

- selected move entries,
- apply result entries,
- audit metadata,
- closure object id,
- rollback metadata.

## No-Op and Denial Identity

No-op and denial operations must receive identity before returning terminal result.

Examples:

| Outcome | Identity Rule |
|---|---|
| `selected_moves=0` | Same operation id as runtime cycle |
| policy disabled | Same operation id |
| observe mode blocks apply | Same operation id |
| dry-run | Same operation id |
| restore barrier denied | Same operation id |
| generation mismatch | Same operation id |
| replay denied | Same operation id if replay packet exists; otherwise deny event references supplied operation id or emits a denial operation id |

## Verdict

The operation creation model is owner-preserving: autoswitch creates runtime operation identity, and all other components reference it.

