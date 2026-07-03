# Target Quarantine Attribution Fix

Timestamp: 2026-07-03 12:11:37

## Summary

After deploying scoped route verification, Phase 4 MEDIUM_BATCH was resumed:

- payload: `/tmp/v7_phase4_medium_batch_after_scoped_verify_fix_20260703T080502.json`
- final verdict: `GOVERNED_TRANSACTION_STOPPED`
- stop reason: `l3_production_validation_transition_blocked`
- transition error: `l3_validation_selected_move_count_missing`
- selected moves: 0

The previous Runtime verification-scope defect was fixed, but the earlier false global verification failures had already polluted autoswitch safety state.

## Root Cause

Remaining controlled-source users were correctly visible:

- incident source: `wireguard-1779454504-c43409`
- remaining affected users: `10.7.0.26` through `10.7.0.40`
- incident source continuity: active
- affected users count: 15

However every remaining user received:

- action: `keep`
- reason: `no_eligible_failover_target`

Candidate target blockers:

- `awg0`: `egress_safety_quarantine`, `egress_failed_verifications_limit`
- `awg3`: `egress_safety_quarantine`, `egress_failed_verifications_limit`
- `vless`: `egress_safety_quarantine`, `egress_failed_verifications_limit`

The safety quarantine entries came from the previous unscoped global route verification failure:

- `awg0` failed verification records: 4
- `awg3` failed verification records: 2
- `vless` failed verification records: 4
- quarantine until: `2026-07-03T05:56:46+00:00`

Those records were not proof of target failure. The failed verification output referenced remaining users still on the intentionally degraded controlled source, not the selected users on the target channels.

## Owner And Functions Changed

Owner:

- `tools/v7-users-autoswitch`

Functions:

- `apply()`
- `_update_safety_after_apply()`
- `_compact_safety()`

Change:

- route verification rows now record `route_verification_scope`;
- target failed-verification accounting stores `verification_scope`;
- only `selected_user_route_check` failures count toward target failed-verification quarantine;
- global route-check failures are retained as evidence but are not target-failure proof;
- legacy unscoped failed-verification records no longer keep target quarantine active.

## Why This Preserves Safety

- selected-user route verification failures still quarantine a target;
- global route verification failures are still visible as unattributed evidence;
- ordinary anti-flap, user freeze, target block, Authority, Restore Barrier, Runtime, Verification, and Rollback contracts remain unchanged;
- this does not bypass target safety; it requires target quarantine to be based on attributed target evidence.

## Tests

Added regressions:

- `test_global_route_verification_failure_does_not_quarantine_target`
- `test_selected_user_route_verification_failure_still_quarantines_target`
- `test_legacy_unscoped_failed_verifications_do_not_keep_quarantine`

Executed:

```text
python3 -m unittest \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_global_route_verification_failure_does_not_quarantine_target \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_selected_user_route_verification_failure_still_quarantines_target \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_legacy_unscoped_failed_verifications_do_not_keep_quarantine
Ran 3 tests in 0.087s
OK
```

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_governed_canary_cli
Ran 155 tests in 11.442s
OK
```

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py
OK
```

## Production State

After the stopped Phase 4 attempt:

- controlled source restored to enabled;
- certification user routes repaired;
- final route check: `V7_USER_ROUTE_CHECK=OK`.

## Resume Point

Interrupted phase:

- Phase 4 MEDIUM_BATCH certification

Next step:

- safe deploy target quarantine attribution fix;
- convergence check;
- re-run Phase 4 MEDIUM_BATCH against the same controlled source;
- continue certification ladder only after Phase 4 reaches a terminal engineering outcome.

