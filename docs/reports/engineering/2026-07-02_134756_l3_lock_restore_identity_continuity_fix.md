# L3 Lock / Restore Identity Continuity Fix

Generated: 2026-07-02 13:47:56 +07

## Summary

Implemented a narrow identity-continuity fix for the existing governed L3 execution chain.

The first proven break was between `tools/v7-governed-canary-dry-run-cycle` and `tools/v7-users-autoswitch --apply`: the governed owner materialized a packet, approved plan lock, and restore barrier containing committed `packet_id`, `operation_id`, `selected_move_hash`, `user`, `source`, and `target`, but Runtime apply was invoked only with `user` and `target`.

That allowed the apply-side pre-planner refresh / Runtime planning pass to consume a recomputed or unbound selected move instead of the committed selected move.

## Scope

Changed files:

- `tools/v7-governed-canary-dry-run-cycle`
- `tools/v7-users-autoswitch`
- `tests/unit/test_governed_canary_cli.py`
- `tests/unit/test_v7_users_autoswitch_policy.py`

No new Runtime, Planner, Authority, Restore Barrier, owner, packet owner, or architecture was created.

## Fix

`tools/v7-governed-canary-dry-run-cycle` now passes committed identity into existing Runtime apply:

- `--source-egress`
- `--approved-packet-id`
- `--approved-operation-id`
- `--approved-selected-move-hash`
- `--approved-authority-generation`

`tools/v7-users-autoswitch` now fails closed when committed apply identity is provided and does not match the existing approved plan lock / restore barrier.

The pre-planner refresh gate remains allowed only for bounded one-user apply or governed envelope scope, and now also requires committed identity match when committed identity is supplied.

## Contract Preservation

Authority is not bypassed.

Restore Barrier is not bypassed.

Runtime eligibility is not bypassed.

Planner decisions are not invented.

Blast radius remains `max-selected-moves=1`.

The fix binds apply to the already approved packet/lock identity instead of permitting unbound recomputation to replace it.

## Tests

Commands executed:

- `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-governed-canary-dry-run-cycle tools/v7-users-autoswitch`
- `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_governed_canary_cli.GovernedCanaryCliTest.test_l3_production_validation_routes_through_pipeline_before_apply tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_committed_apply_identity_must_match_approved_plan_lock tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_committed_apply_identity_mismatch_blocks_approved_plan_lock`
- `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_governed_canary_cli`
- `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_v7_users_autoswitch_policy`
- `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests.unit.test_operator_execution_packet`
- `PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest discover tests/unit`

Results:

- compile: PASS
- focused identity tests: PASS
- governed canary CLI: 17 tests PASS
- users autoswitch policy: 112 tests PASS
- operator execution packet: 35 tests PASS
- full unit discover: 648 tests PASS

## Production Hold

Before local implementation, the production timer was held:

- `v7-users-autoswitch.timer`: inactive / dead
- `v7-users-autoswitch.service`: inactive / dead

No users were moved during implementation.

## Production Validation

Pending deploy and one bounded governed validation cycle.

## Deployment

Pending.

