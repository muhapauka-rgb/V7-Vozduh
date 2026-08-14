# Z7.2 Evidence 02 - Autoswitch Wiring Model

## Wiring Principle

`tools/v7-users-autoswitch` remains the only normal runtime owner. Wiring adds lineage fields to its existing outputs; it does not create a new planner, executor, state store, or scheduler.

## Required Autoswitch Operation Fields

| Field | Source | Required |
|---|---|---|
| `operation_id` | Created by autoswitch runtime cycle | Required |
| `operation_owner` | Static value `tools/v7-users-autoswitch` | Required |
| `operation_kind` | Static value `autoswitch_runtime_cycle` | Required |
| `operation_started_at` | Runtime cycle start timestamp | Required |
| `operation_mode` | Existing `mode` | Required |
| `apply_requested` | Existing `apply_requested` | Required |
| `target_egress` | Existing `target_egress` | Optional |
| `planner_generation_id` | Existing `safety.generation.planner_generation_id` | Required |
| `selected_move_hash` | Existing `_selected_moves_hash(selected)` | Required |
| `selected_move_count` | Existing selected move length | Required |
| `runtime_snapshot_hash` | Digest of existing runtime truth inputs | Required for audit/governance parity |
| `restore_barrier_ref` | Existing restore barrier status/digest | Required when barrier file exists |
| `terminal_state` | Derived from `apply_result` and guards | Required |
| `terminal_reason` | Existing reason/guard reason | Required |

## Planner Wiring

Plan root:

```text
plan.operation.operation_id
plan.safety.generation.planner_generation_id
plan.operation.planner_generation_id
```

Design rule:

- `planner_generation_id` remains owned by autoswitch.
- `operation_id` references the generation.
- Generation must not become operation truth.

## Selected Move Wiring

Plan root:

```text
plan.operation.selected_move_hash
plan.operation.selected_move_count
plan.selected_moves[]
```

Each selected move should reference:

```json
{
  "operation_id": "<same operation id>",
  "selected_move_index": 0,
  "selected_move_hash": "<root selected move hash>",
  "user_ip": "",
  "current_egress": "",
  "recommended_egress": "",
  "move_type": ""
}
```

Design rule:

- Autoswitch still owns selected moves.
- Admin/operator adapters remain readers only.

## Restore Barrier Wiring

Existing restore barrier facts remain in:

```text
plan.safety.restore_barrier
```

Operation linkage should add:

```text
plan.operation.restore_barrier_ref.file
plan.operation.restore_barrier_ref.clearance_generation_id
plan.operation.restore_barrier_ref.current_generation_id
plan.operation.restore_barrier_ref.current_selected_moves_hash
plan.operation.restore_barrier_ref.clearance_generation_reason
```

Design rule:

- Restore barrier lifecycle remains owned by existing barrier/autoswitch logic.
- Operation only references barrier facts.

## Runtime Recheck Wiring

Autoswitch runtime recheck should be represented as an operation lineage step:

```json
{
  "step": "runtime_recheck",
  "operation_id": "<operation id>",
  "planner_generation_id": "",
  "runtime_snapshot_hash": "",
  "selected_move_hash": "",
  "restore_barrier_status": "",
  "verdict": "ALLOW|DENY|NO_OP",
  "reason": ""
}
```

Design rule:

- Operator packet recheck remains governance-only.
- Runtime recheck remains autoswitch-owned.
- Both can share `operation_id`, `selected_move_hash`, and `runtime_snapshot_hash` as references.

## Execution and Verification Wiring

Each apply result row should reference:

- `operation_id`,
- `selected_move_hash`,
- `selected_move_index`,
- `planner_generation_id`,
- execution command result,
- verification result.

Verification lineage:

```text
operation_id
  -> selected_move_hash
  -> user_ip/from/to
  -> switch rc
  -> verify rc
  -> rollback rc if present
```

## Terminal Verdict Wiring

Autoswitch should produce a terminal operation verdict:

| Runtime Case | Terminal State |
|---|---|
| applied and all verified | `COMPLETED` |
| selected move execution failed | `FAILED_CLOSED` |
| verification failed and rollback succeeded | `ROLLED_BACK` |
| verification failed and rollback failed | `FAILED_CLOSED` |
| dry-run | `NO_OP_DRY_RUN` |
| observe mode | `NO_OP_OBSERVE` |
| autoswitch disabled | `DENIED_POLICY` |
| no selected moves | `NO_OP_EMPTY_SELECTION` |
| restore barrier/generation guard blocks | `DENIED_RESTORE_BARRIER` |

This terminal state is an operation fact, not a closure fact.

