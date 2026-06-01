# PROGRAM Z4 Generation Drift

## Objective

Verify generation changes, proposal drift, approval drift, and fingerprint drift.

## Live Evidence

The current live restore barrier is expired:

- current_generation_id: `1e342e0ca505bb0d5ae5328ad911f33d48f50fd2ca8fc1427a993f205222a934`
- approved_generation_id: `c4a2bfa3637a1cd69ecab5ec10b0cf4da4be16aece95630c7a2161eeaffff2d8`
- clearance_guard_reason: `restore_barrier_clearance_generation_expired`
- selected_moves: `0`

## Stress Probe

Live-derived copy with explicit stale clearance:

- label: `generation_drift_stale_clearance`
- guard: `restore_barrier_clearance_generation_mismatch`
- selected_moves: `0`
- decision: `no_eligible_failover_target`

## Verdict

- generation_changes_detected=true
- proposal_drift_fail_closed=true
- approval_drift_fail_closed=true
- fingerprint_drift_fail_closed=true
- generation_drift_certified=true

