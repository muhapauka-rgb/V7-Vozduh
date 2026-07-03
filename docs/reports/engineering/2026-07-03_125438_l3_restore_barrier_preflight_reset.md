# L3 Restore Barrier Preflight Reset

## Summary

Phase 4 MEDIUM_BATCH resumed after the committed L3 apply verification-scope fix.

Production run:

- `/tmp/v7_phase4_medium_batch_after_committed_scope_fix_20260703T084735.json`

Result:

- `final_verdict=L3_PRODUCTION_PROVEN`
- `requested_max_users=10`
- `users_moved=5`
- `verification_result=PASS`
- `rollback_result=NOT_REQUIRED`
- moved users: `10.7.0.36`, `10.7.0.37`, `10.7.0.38`, `10.7.0.39`, `10.7.0.40`

This proved the previous scoped-verification fix in production, but it did not certify MEDIUM_BATCH because the fresh validation attempt reused a completed 5-user Approved Plan Lock / Restore Barrier.

## Root Cause

`tools/v7-governed-canary-dry-run-cycle::execute_l3_production_validation()` planned the next L3 validation using the canonical restore barrier file:

- `/opt/v7/egress/state/autoswitch-restore-barrier.json`

That file still contained a completed previous Approved Plan Lock for five users.

`admin_core.operator_execution.selected_moves_from_plan()` then materialized packet moves from:

- `plan.safety.restore_barrier.approved_candidate_moves_before_guard`

instead of fresh Planner selected moves.

The next `--max-users 10` validation therefore executed the previous 5-user cohort.

## Owner

- Blocking owner: `tools/v7-governed-canary-dry-run-cycle`
- Consumer owner: `admin_core.operator_execution.selected_moves_from_plan`
- Runtime owner unchanged: `tools/v7-users-autoswitch`
- Restore Barrier owner unchanged: `admin_core/operator_execution.py`

## Classification

`OWNER_INVOCATION_MISSING`

The governed L3 validation owner did not prepare a fresh restore barrier planning surface after a previous execution lease had already terminalized.

This was not a Planner defect, Runtime defect, Restore Barrier bypass, or Authority bypass.

## Implementation

Added:

- `reset_completed_restore_barrier_for_fresh_l3_validation()`

Behavior:

- If an execution lease is active, preserve the restore barrier.
- If no execution lease is active and the restore barrier contains a canonical completed Approved Plan Lock, archive it and write an empty barrier before fresh L3 validation planning.
- If the barrier owner is not canonical, do not clear it.
- If reset fails, stop safe before planning.

The fresh transaction still creates a new Approved Plan Lock and Restore Barrier through existing owners.

## Tests

Commands:

```bash
python3 -m unittest tests.unit.test_governed_canary_cli.GovernedCanaryCliTest.test_l3_restore_barrier_preflight_reset_archives_completed_lock_when_lease_inactive tests.unit.test_governed_canary_cli.GovernedCanaryCliTest.test_l3_restore_barrier_preflight_reset_preserves_active_lease_lock tests.unit.test_governed_canary_cli.GovernedCanaryCliTest.test_l3_production_validation_resets_completed_barrier_before_fresh_batch_plan tests.unit.test_governed_canary_cli.GovernedCanaryCliTest.test_l3_production_validation_accepts_medium_budget_batch_without_single_user_override
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_governed_canary_cli
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tools/v7-governed-canary-dry-run-cycle tests/unit/test_v7_users_autoswitch_policy.py tests/unit/test_governed_canary_cli.py
```

Results:

- Targeted tests: PASS, 4 tests.
- Full relevant tests: PASS, 161 tests.
- Compile: PASS.

## Production Impact

- Production deploy: pending at report creation.
- Production users moved by this implementation step: 0.
- No new owner, Runtime, Planner, Authority, Restore Barrier, packet format, or execution path created.

## Phase 4 Continuation

After safe deploy, resume Phase 4 MEDIUM_BATCH from the interrupted certification mission.

Expected next proof:

- `restore_barrier_preflight_reset.reset_performed=true` if a completed old lock exists.
- fresh Planner selection is not hijacked by previous 5-user Approved Plan Lock.
- `requested_max_users=10`.
- `transition.selected_move_count` can reach 10 when enough eligible certification users exist.

