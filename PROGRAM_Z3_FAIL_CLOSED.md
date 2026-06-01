# Program Z3 Fail Closed

Date: 2026-06-01

## Verdict

replay_protection_verified=true
fail_closed_verified=true

## Live Fail-Closed Event

The live runtime denied execution before movement:

- planner candidate moves: `12`
- planner selected moves: `0`
- restore barrier clearance max selected moves: `0`
- denial reason: `restore_barrier_clearance_selected_moves_exceed_budget`

## Z2 Contract Fail-Closed Coverage Reused

Z2 hybrid tests remain the contract-level proof for:

- replay denial
- expired packet denial
- stale fingerprint denial
- invalid budget denial
- exact target approval requirement for high-risk target classes

## Z3 Additional Fail-Closed Rule

Even if a candidate exists, Z3 denies movement when live planner selected moves are zero because the live restore barrier is authoritative.

## Safety

- fail_open_paths_found=false
- users_moved=false
- autoswitch_apply_outside_packet=false

