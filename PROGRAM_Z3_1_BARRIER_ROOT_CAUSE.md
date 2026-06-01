# Program Z3.1 Barrier Root Cause

Date: 2026-06-01

## Verdict

barrier_root_cause_known=true

## Exact Source

Source rule:

- `tools/v7-users-autoswitch`
- `plan()` restore barrier clearance guard
- `_restore_clearance_generation_check()`

## Exact Rule

When a restore barrier is:

- expired
- cleared
- has `clearance_max_selected_moves`

the planner first computes selected moves, then compares:

`len(selected) > clearance_max_selected_moves`

If true:

- `clearance_budget_exceeded=true`
- `clearance_guard_reason=restore_barrier_clearance_selected_moves_exceed_budget`
- selected moves are replaced with `[]`

For nonzero clearance budgets, the planner then requires:

- non-empty generation token
- matching planner generation id
- matching selected moves hash
- matching selected move count
- non-expired clearance timestamp

## Exact State

Initial live barrier:

- `clearance_max_selected_moves=0`
- unfiltered selected moves before guard: `3`
- filtered one-user selected moves before guard: `1`

## Exact Comparison

Unfiltered:

`3 > 0` => denied

Filtered one-user before remediation:

`1 > 0` => denied

Filtered one-user after remediation:

`1 > 1` => false, then generation/hash/count checks passed

