# Program Z3.1 Autonomy Gate Retry

Date: 2026-06-01

## Verdict

autonomy_gate_passed=true

## Gate Retried

Filtered final autonomy gate:

`v7-users-autoswitch --mode guarded --route-class GLOBAL_STABLE --user 10.7.0.16 --target-egress awg3`

Final immediate retest:

- candidate moves: `1`
- selected moves: `1`
- generation ok: `true`
- guard: `restore_barrier_clearance_budget_and_generation_ok`
- apply requested: `false`
- apply result: `dry_run`

## Unfiltered Safety Check

Unfiltered planner remained blocked:

- candidate moves: `12`
- selected moves before guard: `3`
- clearance max selected moves: `1`
- selected moves after guard: `0`
- guard: `restore_barrier_clearance_selected_moves_exceed_budget`

This confirms Z3.1 did not unlock cohort movement.

## Safety

- users_moved_count=0
- scope_expanded=false
- autoswitch_apply_outside_governance=false
- routing_changed_outside_scope=false

