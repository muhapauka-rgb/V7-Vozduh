# Selected-User Verification Attribution Fix

## Summary

After deploying the scoped post-apply verifier fix, Phase 4 MEDIUM_BATCH was resumed.

Execution stopped before Runtime Apply:

- artifact: `/tmp/v7_phase4_medium_batch_after_scoped_expected_target_fix_20260703T082244.json`
- `final_verdict = GOVERNED_TRANSACTION_STOPPED`
- `transaction_status = STOP_SAFE`
- `stop_reason = l3_production_validation_transition_blocked`
- `transition_errors = ["l3_validation_selected_move_count_missing"]`
- `selected_move_count = 0`
- Authority budget: `POOL`

## Root Cause

Previous false selected-user route verification failures were still recorded in `autoswitch-safety.json` as attributed target failures:

- `verification_scope = selected_user_route_check`
- no committed `verification_expected_egress`
- quarantine held on `awg0`, `awg3`, and `vless`

Those records were produced by the earlier verifier contract defect:

Runtime Apply moved users to their committed targets, but scoped verification expected the incident-source registry interface.

After that verifier was corrected, the legacy safety records still remained indistinguishable from real selected-user target failures because they did not carry the expected target identity.

## Production Evidence

Safety file:

`/opt/v7/egress/state/autoswitch-safety.json`

Target `awg0`:

- `failed_verifications_1h = 3`
- `failed_verifications_1h_unattributed = 4`
- `quarantine_until = 2026-07-03T06:15:28.655054+00:00`
- records at `2026-07-03T05:15:28Z` had `verification_scope = selected_user_route_check`
- those records had no `verification_expected_egress`

Target `awg3`:

- `failed_verifications_1h = 4`
- `failed_verifications_1h_unattributed = 2`
- `quarantine_until = 2026-07-03T06:15:28.655076+00:00`
- no `verification_expected_egress` on selected-user records

Target `vless`:

- `failed_verifications_1h = 3`
- `failed_verifications_1h_unattributed = 4`
- `quarantine_until = 2026-07-03T06:15:28.655152+00:00`
- no `verification_expected_egress` on selected-user records

Planner result:

Remaining users on `wireguard-1779454504-c43409` were visible, but decisions for `10.7.0.36` through `10.7.0.40` were:

`reason = ["no_eligible_failover_target"]`

## Correction

Existing owner:

`tools/v7-users-autoswitch`

Functions changed:

- `apply()`
- `_update_safety_after_apply()`
- `_compact_safety()`

Behavior:

- post-apply emergency verification result now records `route_verification_expected_egress`;
- safety failed-verification records persist `verification_expected_egress`;
- target quarantine counts selected-user route failures only when `verification_expected_egress` matches the target egress id;
- legacy selected-user failures without expected target identity are treated as unattributed and cannot keep target quarantine active.

Safety semantics preserved:

Real future selected-user route verification failures still quarantine the target when the failure is attributed to the committed expected target.

No retry budget was reset.
No Authority bypass was introduced.
No Restore Barrier bypass was introduced.
No Runtime bypass was introduced.
No production batch size was changed.

## Tests

Targeted:

```text
python3 -m unittest \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_scoped_post_apply_route_verification_uses_expected_target \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_selected_user_route_verification_failure_still_quarantines_target \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_legacy_selected_user_failures_without_expected_target_do_not_keep_quarantine \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_legacy_unscoped_failed_verifications_do_not_keep_quarantine
```

Result:

```text
Ran 4 tests
OK
```

Affected suite:

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_governed_canary_cli
```

Result:

```text
Ran 157 tests
OK
```

Compile:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py
```

Result:

```text
OK
```

## Current Certification Position

Interrupted phase:

`Phase 4 - MEDIUM_BATCH Certification`

Current state:

`IMPLEMENTATION_DEFECT_RESOLVED_LOCALLY`

Required next step:

safe deploy, verify convergence, restore controlled certification state, and resume Phase 4.
