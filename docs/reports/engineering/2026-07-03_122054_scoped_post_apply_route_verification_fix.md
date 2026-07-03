# Scoped Post-Apply Route Verification Fix

## Summary

Phase 4 MEDIUM_BATCH certification resumed after target quarantine attribution was deployed.

Production execution reached the governed downstream path:

- Authority budget: `POOL`
- selected move count: `10`
- selected source: `wireguard-1779454504-c43409`
- Runtime Apply: executed
- per-user switch rc: `0`

The new breakpoint was downstream proof failure:

- `final_verdict = STOP_SAFE`
- `stop_reason = l3_production_validation_downstream_proof_failed`
- `verification_result = FAIL`
- `rollback_result = ROLLBACK_FAILED`
- `users_moved = 0`

## Production Evidence

Artifact:

`/tmp/v7_phase4_medium_batch_after_quarantine_attribution_fix_20260703T081507.json`

First failed row:

- user: `10.7.0.26`
- from: `wireguard-1779454504-c43409`
- to: `awg3`
- Runtime switch rc: `0`
- Runtime output: `user 10.7.0.26 -> awg3 / table 1024 / dev awg3`
- route_get after apply: `dev awg3 table 1024`
- verify rc: `1`
- verifier expected dev: `v7e06a394c478`
- verifier assignment: `ASSIGN_EGRESS=awg3`
- verifier registry: `REGISTRY_EGRESS=wireguard-1779454504-c43409`

Objective divergence:

Runtime Apply correctly moved the selected user to the committed target, but scoped route verification evaluated the expected interface from the registry incident source instead of the committed post-apply target.

## Root Cause

Owner:

`tools/v7-users-autoswitch`

Functions:

- `apply()`
- `_verify_routes_for_apply()`
- `_verify_routes()`
- `_verify_user_route()`

Exact defect:

`_verify_user_route(user_ip)` always resolved expected egress from `user.current`, which is registry state. During controlled incident continuation the registry may still preserve the incident source while the per-user assignment and Linux route have already been moved to the committed selected target.

This caused a false `route_verify_failed` even though Runtime Apply succeeded and the selected user's route used the target interface.

## Correction

Minimal extension of the existing verifier contract:

- `apply()` now passes the committed selected target to post-apply emergency scoped verification.
- `_verify_routes_for_apply(user_ip, expected_egress)` forwards the expected target.
- `_verify_routes(user_ip, expected_egress)` forwards the expected target.
- `_verify_user_route(user_ip, expected_egress)` resolves `EXPECTED_DEV` from `expected_egress` when provided; standalone verification remains registry-based when no expected target is provided.

No new owner was created.
No Runtime bypass was introduced.
No Authority bypass was introduced.
No Restore Barrier bypass was introduced.
No production batch size was changed.

## Tests

Regression added:

- `test_scoped_post_apply_route_verification_uses_expected_target`

Updated existing regression:

- `test_emergency_batch_apply_uses_scoped_route_verification`

Commands:

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_scoped_post_apply_route_verification_uses_expected_target
```

Result:

```text
Ran 1 test
OK
```

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_governed_canary_cli
```

Result:

```text
Ran 156 tests
OK
```

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py
```

Result:

```text
OK
```

## Production Recovery

After the failed controlled certification attempt:

- controlled source restored to `enabled`;
- all certification users `10.7.0.16` through `10.7.0.40` reconciled;
- `v7-user-route-check = OK`.

## Current Certification Position

Interrupted phase:

`Phase 4 - MEDIUM_BATCH Certification`

Current state:

`IMPLEMENTATION_DEFECT_RESOLVED_LOCALLY`

Required next step:

safe deploy this fix, verify convergence, restore controlled certification state, and resume Phase 4 from the same interrupted certification mission.
