# PROGRAM Z3.2 Drift Test

## Tested Drift Types

- candidate drift
- target drift
- fingerprint drift
- approval drift

## Live Evidence

After rollback, the repeat planner run produced:

- selected_moves: `0`
- guard: `restore_barrier_clearance_generation_mismatch`
- generation_ok: `false`
- reason: `cooldown_active_877s`
- reason: `no_eligible_failover_target`

This proves that a stale generation-bound clearance did not remain reusable.

## Unit-Level Evidence

Existing tests cover stale and mismatched governance state:

- `tests/unit/test_v7_hybrid_approval.py`: expired packet, proposal fingerprint mismatch, replay rejection, invalid budget.
- `tests/unit/test_v7_users_autoswitch_policy.py`: stale generation rejection, selected move hash mismatch, expired generation token rejection.

## Verdict

- candidate_drift_fail_closed=true
- target_drift_fail_closed=true
- fingerprint_drift_fail_closed=true
- approval_drift_fail_closed=true
- drift_handling_certified=true

