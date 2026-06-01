# Z7.1 Evidence 02 - Runtime to Operation Wiring

## Autoswitch Runtime Outputs

`tools/v7-users-autoswitch` currently outputs:

- `schema_version`
- `updated`
- `enabled`
- `mode`
- `apply_requested`
- `target_egress`
- `safety`
- `safety.generation.planner_generation_id`
- `safety.restore_barrier`
- `summary`
- `decisions`
- `selected_moves`
- `apply_result`
- per-move `rc`, `output`, `verify_rc`, `verify_output`, `rollback_rc`, `rollback_output`

## Connected Runtime Mechanics

| Runtime Mechanic | Code Reality | Status | Classification |
|---|---|---|---|
| Planning | `plan()` builds decisions and selected moves | CONNECTED | REUSE |
| Generation | `_generation_status()` computes `planner_generation_id` from state/input hashes | CONNECTED | REUSE |
| Restore barrier | `_restore_barrier_status()` reads barrier; plan applies barrier/clearance logic | CONNECTED | REUSE |
| Selected move hash | `_selected_moves_hash()` computes hash internally for restore barrier checks | CONNECTED internally | REUSE, EXTEND |
| Apply/no-op | `apply()` returns dry-run, disabled, observe, no-selected-moves, or applied results | CONNECTED | REUSE |
| Execution | `_run_switch()` calls `v7-user-switch` | CONNECTED | REUSE |
| Verification | `_verify_routes()` calls `v7-user-route-check` | CONNECTED | REUSE |
| Runtime rollback | `apply()` calls `_run_switch(ip, current, "rollback")` on verify failure | CONNECTED | REUSE |
| Safety update | `_update_safety_after_apply()` writes anti-flap/safety state after successful results | CONNECTED | REUSE |

## Missing Operation Wiring

| Runtime Output | Carries `operation_id`? | Status |
|---|---:|---|
| Plan root | No | MISSING |
| `selected_moves` | No | MISSING |
| `selected_move_hash` | Not emitted as top-level operation lineage; only present inside restore-barrier guard details when relevant | PARTIAL |
| `planner_generation_id` | Yes in safety generation, but not bound to `operation_id` | PARTIAL |
| `runtime_snapshot_hash` | No | MISSING |
| `apply_result` | No | MISSING |
| verification output | No | MISSING |
| rollback output | No | MISSING |
| terminal runtime verdict | No first-class operation terminal state | MISSING |

## Runtime to Operation Verdict

The runtime owner is connected, but runtime-to-operation identity wiring is not connected. Autoswitch should be reused and extended later; a parallel operation writer would duplicate runtime truth.

