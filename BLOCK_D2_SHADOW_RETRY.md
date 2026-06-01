# Block D2 Shadow Retry

Date: 2026-06-01

## Command Class

Shadow retry used `v7-users-autoswitch` without `--apply`.

No execution, routing mutation, or user movement was requested.

## Shadow Summary

- `enabled=true`
- `mode=guarded`
- `apply_requested=false`
- `users_total=18`
- `egress_total=7`
- `healthy_egress_total=2`
- `candidate_moves=12`
- `candidate_moves_total=12`
- `selected_moves=0`
- `reconnect_rotation_candidates=0`
- `rebalance_candidates=0`

## Restore Barrier

Existing restore barrier state:

- `expired=true`
- `cleared=true`
- `clearance_max_selected_moves=0`
- `clearance_selected_moves_before_guard=3`
- `clearance_budget_exceeded=true`
- `clearance_guard_reason=restore_barrier_clearance_selected_moves_exceed_budget`

This confirms the existing zero-budget barrier continues to suppress selected moves.

## Verdict

shadow_retry_completed=true

