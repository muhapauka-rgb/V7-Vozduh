# Emergency Batch Scoped Route Verification

Timestamp: 2026-07-03 12:02:50

## Summary

After deploying `1d835f95` the interrupted Phase 4 MEDIUM_BATCH certification was resumed against the same controlled source:

- controlled source: `wireguard-1779454504-c43409`
- payload: `/tmp/v7_phase4_medium_batch_after_controlled_evidence_fix_20260703T075551.json`
- selected moves: 10
- selected source: `wireguard-1779454504-c43409`
- Runtime Apply: executed
- switch command rc: `0` for all 10 selected users
- verification result: `FAIL`
- rollback result: `ROLLBACK_FAILED`

The previous blocker was resolved: Runtime Apply no longer stopped at `source_recovered_before_apply`.

## New Breakpoint

Verification failed after successful apply because `tools/v7-users-autoswitch.apply()` called global `v7-user-route-check` for every selected move.

Global route verification checks every enabled user in `users.registry`. During an active controlled failed-source incident, remaining certification users are intentionally still assigned to the degraded source until future bounded cycles move them.

The failed verification output did not identify selected users `10.7.0.16` through `10.7.0.25` as the first failing rows. It showed remaining users such as `10.7.0.31` through `10.7.0.35` still assigned to `wireguard-1779454504-c43409` and leaking to `ens3` while the source was intentionally in controlled maintenance.

## Root Cause

Owner:

- `tools/v7-users-autoswitch`

Function:

- `apply()`
- `_verify_routes()`

Root cause:

- emergency batch apply used global route verification instead of operation-scoped verification for the selected moved user;
- unrelated remaining users on the same active incident source caused false verification failure;
- false verification failure triggered rollback;
- rollback attempted to return selected users to the controlled failed source and failed with `egress disabled: wireguard-1779454504-c43409`.

Rollback failure was a downstream consequence, not the first defect.

## Fix

Added scoped route verification inside the existing owner:

- `_verify_routes(user_ip="")`
- `_verify_routes_for_apply(user_ip="")`
- `_verify_user_route(user_ip)`

Behavior:

- ordinary/non-emergency apply keeps global `v7-user-route-check`;
- emergency failover apply verifies only the selected moved user for each row;
- scoped verification reads the same production state files and Linux route reality:
  - `users.registry`
  - `user-<ip>.assign`
  - `egress.registry`
  - `ip route show table <table>`
  - `ip route get 8.8.8.8 from <ip> iif wg0`

This does not create a new Runtime, Planner, Authority, Restore Barrier, Wake owner, or execution path.

## Tests

Added regression:

- `test_emergency_batch_apply_uses_scoped_route_verification`

The test proves:

- emergency batch apply calls route verification with selected user identity;
- global route verification failure does not fail the selected move;
- no rollback is attempted when scoped selected-user verification passes;
- all selected rows reach `SUCCESS`.

Executed:

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_emergency_batch_apply_uses_scoped_route_verification
Ran 1 test in 0.381s
OK
```

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_governed_canary_cli
Ran 152 tests in 11.045s
OK
```

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py
OK
```

## Production State

After the failed Phase 4 run, controlled source and certification user routes were restored:

- `v7-egress-set-state wireguard-1779454504-c43409 enabled --apply`
- `v7-user-reconcile-apply --repair routing` for certification users `10.7.0.16` through `10.7.0.40`
- final route check: `V7_USER_ROUTE_CHECK=OK`

## Resume Point

Interrupted phase:

- Phase 4 MEDIUM_BATCH certification

Next step:

- safe deploy scoped route verification;
- convergence check;
- re-run Phase 4 MEDIUM_BATCH against the same controlled source;
- continue the certification ladder only after Phase 4 reaches a terminal engineering outcome.

