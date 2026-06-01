# PROGRAM Z7.3 - Minimal Implementation Plan Audit Report

Project: V7 Vozduh  
Branch target: v7-next  
Date: 2026-06-02  
Mode: READ ONLY implementation-readiness audit  
Evidence directory: `z7_3-evidence`

## Executive Verdict

The smallest implementation set to connect:

```text
Runtime -> Operation -> Audit -> Closure
```

is narrow.

The absolute minimum future code change should be limited to:

1. `tools/v7-users-autoswitch`
2. `tests/unit/test_v7_users_autoswitch_policy.py`

No new operation store, API, scheduler, orchestrator, audit sink, closure store, runtime owner, or rollback owner is required.

## Discovery Gate Result

Existing paths were inventoried before planning:

- runtime output structures,
- metadata helpers,
- hash helpers,
- audit metadata,
- closure metadata,
- existing `operation_id` use,
- tests and fixtures.

Main finding:

- `tools/v7-users-autoswitch` already has almost all raw facts needed for operation lineage.
- `v7-audit-log` already accepts metadata and object ids.
- Admin closure already accepts `object_type=runtime`.
- Missing work is wiring, not architecture.

## File Inventory

| File | Plan |
|---|---|
| `tools/v7-users-autoswitch` | Required minimal implementation file |
| `tests/unit/test_v7_users_autoswitch_policy.py` | Required minimal test file |
| `tools/runtime-support/v7-audit-log` | No change preferred |
| `admin/v7-admin-api` | Optional metadata pass-through only |
| `admin_core/operator_observability.py` | Optional future live runtime audit reader |
| `admin_core/operator_execution.py` | No change for minimal runtime wiring |
| systemd files | DO NOT TOUCH |

## Function Inventory

Required future touch points in `tools/v7-users-autoswitch`:

| Function / Area | Change Class |
|---|---|
| `AutoswitchPlanner.__init__` | LINEAGE EXTENSION |
| `plan()` | METADATA EXTENSION |
| `_selected_moves_hash(selected)` | REUSE |
| `_generation_status()` | REUSE |
| `_restore_barrier_status()` | REUSE |
| `_restore_clearance_generation_check(...)` | REUSE |
| `apply(plan)` | LINEAGE EXTENSION |
| `_run_switch(...)` | OPTIONAL EXTEND |
| `_verify_routes()` | REUSE |
| `main()` | METADATA EXTENSION |

Potential new helpers inside `tools/v7-users-autoswitch`:

- `_build_operation_context(...)`
- `_runtime_snapshot_hash(...)`
- `_terminal_state(...)`
- `_audit_runtime_operation(...)`

These are helper additions inside the existing runtime owner, not new truth sources.

## Metadata Inventory

Already exists:

- `planner_generation_id`
- selected moves
- selected move hash helper
- restore barrier facts
- apply result rows
- verification result rows
- rollback result rows
- audit `request_id`
- audit metadata
- closure `object_type/object_id`

Missing:

- autoswitch `operation_id`
- operation envelope
- runtime snapshot hash in autoswitch output
- terminal state/reason
- audit refs on operation
- closure target on operation

## Test Inventory

Existing tests that should be reused:

- `tests/unit/test_v7_users_autoswitch_policy.py`
- `tests/unit/test_operator_execution_packet.py`
- `tests/unit/test_operator_observability.py`

Minimum test extension target:

- `tests/unit/test_v7_users_autoswitch_policy.py`

Minimum new assertions:

- no-op/dry-run plan includes operation envelope,
- selected-move plan includes operation id and selected move hash,
- restore-barrier denied plan includes terminal reason/state,
- mocked apply result includes operation lineage,
- audit metadata construction uses existing `v7-audit-log` schema.

## Minimal Change Set

Absolute minimum:

1. `tools/v7-users-autoswitch`
   - create one `operation_id` per runtime cycle,
   - emit operation envelope in JSON plan output,
   - expose `selected_move_hash`,
   - expose `runtime_snapshot_hash`,
   - propagate `operation_id` to selected moves and apply result rows,
   - derive terminal state/reason,
   - emit terminal audit through existing `v7-audit-log` in mutating/runtime mode,
   - include closure target metadata: `object_type=runtime`, `object_id=<operation_id>`.

2. `tests/unit/test_v7_users_autoswitch_policy.py`
   - extend existing fixture-based tests for operation envelope and lineage.

No change:

- `v7-audit-log` schema,
- Admin closure schema,
- systemd,
- scheduler,
- operator execution governance.

Recommended but not absolute:

- Admin guarded autoswitch wrapper returns/audits the operation id from autoswitch plan.
- Operator observability later indexes live runtime operation audit events.

## Implementation Order

1. Add autoswitch operation context/id creation.
2. Add operation envelope to plan output.
3. Add selected move hash, runtime snapshot hash, and restore barrier lineage.
4. Propagate operation id into selected move rows.
5. Add terminal state/reason mapping in `apply(plan)`.
6. Propagate operation id into apply, verification, and rollback result rows.
7. Add terminal audit call through existing `v7-audit-log`, constrained to mutating/runtime mode.
8. Add closure target metadata to operation output.
9. Extend autoswitch unit tests.
10. Optional: extend Admin wrapper pass-through.
11. Optional: extend operator observability live audit indexing.

## Risk Analysis

| Risk Area | Risk |
|---|---|
| runtime risk | MEDIUM |
| audit risk | LOW/MEDIUM |
| closure risk | LOW |
| rollback risk | MEDIUM |
| scheduler risk | LOW if untouched, HIGH if touched |
| duplication risk | MEDIUM |
| test risk | LOW |

Risk control:

- keep operation fields output-only except terminal audit,
- do not change move selection,
- do not change scheduler,
- do not change `v7-audit-log`,
- do not change closure schema,
- test no-op, selected move, barrier-denied, apply, rollback, and audit metadata cases.

## Truth Source Audit

| Truth Source | Verdict |
|---|---|
| Operation truth | No new store; autoswitch owns runtime operation id |
| Runtime truth | Autoswitch remains owner |
| Lineage truth | Existing runtime facts referenced in operation envelope |
| Audit truth | `v7-audit-log` remains owner |
| Closure truth | Admin closure remains owner |
| Rollback truth | Autoswitch normal rollback remains owner |

## Final Verdicts

```text
implementation_plan_defined=true
file_inventory_complete=true
function_inventory_complete=true
metadata_inventory_complete=true
test_inventory_complete=true
minimal_change_set_defined=true
implementation_order_defined=true
implementation_risks_understood=true
safe_to_continue_to_Z7_4=true
```

## Safety Statement

Z7.3 performed no implementation, no code writing, no code patching, no API creation, no storage creation, no runtime mutation, no routing mutation, no user movement, no autoswitch apply, no deploy, no service restart, no systemd modification, no timer modification, no cleanup, no deletion, no merge, and no force push.

