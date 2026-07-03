# Committed L3 Apply Emergency Scope Fix

## Summary

Phase 4 MEDIUM_BATCH certification reached Runtime Apply and failed verification with:

- `verification_result=FAIL`
- `rollback_result=ROLLBACK_FAILED`
- `route_verification_scope=global`
- `route_verification_expected_egress=null`

Production artifact:

- `/tmp/v7_phase4_medium_batch_clean_after_scope_remark_20260703T083609.json`

The selected moves, packet identity, Approved Plan Lock, Restore Barrier, Wake, Authority, and committed apply identity were already proven valid. The breakpoint was inside Runtime Apply verification scope selection.

## Root Cause

`tools/v7-users-autoswitch::AutoswitchPlanner.apply()` selected emergency post-apply verification mode only from:

- `plan.summary.execution_mode == emergency_failover`

However, the production apply path rehydrates committed selected moves from:

- `safety.restore_barrier.approved_plan_lock_validation.selected_moves`

The rehydrated moves already receive:

- `execution_mode=emergency_failover`

from:

- `tools/v7-users-autoswitch::AutoswitchPlanner._committed_selected_moves_from_approved_plan_lock()`

But the apply payload did not preserve `summary.execution_mode`. Therefore Runtime Apply executed the global route verifier instead of selected-user target-scoped verification.

## Owner

- Owner: `tools/v7-users-autoswitch`
- Function changed: `AutoswitchPlanner.apply`
- Existing producer reused: `AutoswitchPlanner._committed_selected_moves_from_approved_plan_lock`

## Implementation

Runtime Apply now derives emergency verification mode from either:

- `summary.execution_mode == emergency_failover`
- committed selected moves with `execution_mode == emergency_failover` when L3 context is active

The L3 context guard prevents ordinary approved-lock applies from being reclassified as L3 emergency execution.

No new Runtime, Planner, Authority, Restore Barrier, Wake owner, packet format, or execution path was created.

## Regression Test

Added:

- `test_committed_emergency_moves_keep_scoped_verification_without_summary_mode`

The test proves:

- `plan.selected_moves` may be empty before apply.
- committed moves are rehydrated from approved lock.
- `summary.execution_mode` may be absent.
- Runtime Apply still calls selected-user scoped verification with `(user, target)`.
- global route verification is not used.
- ordinary approved-lock rehydration remains compatible.

## Tests

Commands:

```bash
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_apply_uses_valid_approved_lock_moves_when_fresh_plan_selected_moves_empty tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_committed_emergency_moves_keep_scoped_verification_without_summary_mode tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_emergency_batch_apply_uses_scoped_route_verification
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_governed_canary_cli
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py
```

Results:

- Targeted tests: PASS, 3 tests.
- Full relevant tests: PASS, 158 tests.
- Compile: PASS.

## Production Impact

- Production deploy: pending at report creation.
- Production users moved by this implementation step: 0.
- Production behavior changed only for existing governed L3 apply verification scope when committed emergency selected moves are rehydrated from Approved Plan Lock.

## Phase 4 Continuation

Resume the interrupted MEDIUM_BATCH certification from the same controlled incident after safe deploy, convergence check, certification pool restoration, and certification-scope re-materialization.

Expected next production proof:

- `route_verification_scope=selected_user`
- `route_verification_expected_egress=<committed target>`
- no global route verification for governed L3 emergency apply

