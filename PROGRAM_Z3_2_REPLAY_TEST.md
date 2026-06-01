# PROGRAM Z3.2 Replay Test

## Objective

Verify duplicate packet, replay, expired packet, stale packet, hash mismatch, and blocked state behavior.

## Live Evidence

After the first movement and rollback, the immediate repeat planner run failed closed:

- selected_moves: `0`
- guard: `restore_barrier_clearance_generation_mismatch`
- generation_ok: `false`
- reason: `cooldown_active_877s`
- reason: `no_eligible_failover_target`

This shows the previous generation clearance was not reusable for another apply.

## Unit-Level Evidence

`tests/unit/test_v7_hybrid_approval.py` verifies:

- expired packet rejection
- proposal fingerprint mismatch rejection
- invalid budget rejection
- approval replay rejection

`tests/unit/test_v7_users_autoswitch_policy.py` verifies:

- stale generation rejection
- selected move hash mismatch rejection
- expired generation token rejection
- missing generation token rejection for nonzero clearance budget

## Verdict

- duplicate_packet_blocked=true
- replay_blocked=true
- expired_packet_blocked=true
- stale_packet_blocked=true
- hash_mismatch_blocked=true
- blocked_state_abort=true
- replay_protection_verified=true

