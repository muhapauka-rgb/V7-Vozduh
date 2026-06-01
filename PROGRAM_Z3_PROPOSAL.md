# Program Z3 Proposal

Date: 2026-06-01

## Verdict

proposal_generated=true
bounded_executable_proposal_generated=false

## Fresh Live Planner

Command:

`v7-users-autoswitch --mode guarded --route-class GLOBAL_STABLE`

Planner output:

- updated: `2026-06-01T17:33:03.390450+00:00`
- candidate moves: `12`
- selected moves: `0`
- apply requested: `false`
- apply result: `dry_run`

## Candidate Proposal

Best bounded candidate selected for review only:

- user: `10.7.0.16`
- from: `vless`
- to: `awg3`
- move type: `failover`
- budget: `1`
- rollback: `vless`

This candidate is not executable under live planner truth because selected moves remained `0`.

## Root Cause

The live restore barrier is an expired cleared zero-budget generation clearance:

- `clearance_max_selected_moves=0`
- `clearance_budget_exceeded=true`
- `clearance_guard_reason=restore_barrier_clearance_selected_moves_exceed_budget`

## Safety

- budget_over_1=false
- batch_autonomy=false
- cohort_autonomy=false
- users_moved=false

