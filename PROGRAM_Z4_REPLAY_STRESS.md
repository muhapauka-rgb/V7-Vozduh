# PROGRAM Z4 Replay Stress

## Objective

Verify replay, expired packet, stale packet, hash mismatch, budget mismatch, and blocked state behavior.

## Live Evidence

Current live barrier:

- clearance_guard_reason: `restore_barrier_clearance_generation_expired`
- selected_moves: `0`
- current generation differs from approved Z3.2 generation

## Stress Probe Evidence

Stale generation clearance on live-derived copy:

- label: `generation_drift_stale_clearance`
- guard: `restore_barrier_clearance_generation_mismatch`
- selected_moves: `0`

## Unit Evidence

Existing tests cover:

- expired packet
- stale proposal fingerprint
- replay rejection
- invalid budget
- selected move hash mismatch
- expired generation token
- missing generation token for nonzero budget

## Verdict

- replay_blocked=true
- expired_packet_blocked=true
- stale_packet_blocked=true
- hash_mismatch_blocked=true
- budget_mismatch_blocked=true
- blocked_state_abort=true
- replay_under_stress_certified=true

