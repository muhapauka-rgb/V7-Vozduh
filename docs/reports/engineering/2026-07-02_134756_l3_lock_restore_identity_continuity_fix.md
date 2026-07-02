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

First bounded governed validation after deploy:

- service path: `v7-users-autoswitch.service`
- owner command: `/usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED --max-users 1`
- baseline affected users on `openvpn-1779388847-d2ad7c`: 10
- selected user: `10.7.0.2`
- source: `openvpn-1779388847-d2ad7c`
- target: `awg3`
- packet: `pkt_a649186324f24ab088d73e85`
- operation: `govexec_36a08f459f517b9820e9d28f`
- selected_move_hash: `a0eea5cccfabb892cf57ac29b13cd686b83e988a2e2df8c1377b7c602984779e`

Identity continuity result:

- approved plan lock validation: PASS
- committed apply identity validation: PASS
- selected user/source/target preserved: PASS
- restore barrier hash/generation mismatch: NOT PRESENT

New downstream breakpoint:

- `emergency_failover_autonomy.ok=false`
- blockers: `duplicate_apply_attempt`, `l3_retry_budget_exhausted`
- previous_attempts: 50
- retry_budget_per_incident: 1
- apply result: not applied
- users moved: 0

Root cause of second breakpoint:

`_l3_incident_attempt_count()` counted historical `DENIED` / no-execution attempts as retry-budget-consuming attempts. The production incident had accumulated many STOP_SAFE/no-execution records while the chain was being debugged, so the first post-fix approved one-user validation was blocked before apply even though the committed packet/lock identity was valid.

Second correction:

- `tools/v7-users-autoswitch::_l3_incident_attempt_count()` now counts only attempts that consumed Runtime retry budget.
- `duplicate_apply_attempt` now considers only attempts that consumed retry budget.
- `DENIED`, `DRY_RUN`, and `STOP_SAFE` no-execution attempts no longer burn the one approved production validation attempt.
- Real applied attempts still consume retry budget and still block duplicate retries.

Second correction tests:

- `test_l3_retry_budget_ignores_denied_no_execution_attempts`: PASS
- `test_l3_persistent_retry_budget_blocks_second_attempt`: PASS
- `tests.unit.test_v7_users_autoswitch_policy`: 113 tests PASS
- `tests.unit.test_governed_canary_cli tests.unit.test_operator_execution_packet`: 52 tests PASS
- full unit discover: 649 tests PASS

## Deployment

First deploy:

- commit: `a39791db4cbf08ac988e054eb80b6c3ef43001a5`
- safe-deploy preview: PASS
- safe-deploy apply: PASS
- production hashes matched local hashes for:
  - `/usr/local/bin/v7-users-autoswitch`
  - `/usr/local/bin/v7-governed-canary-dry-run-cycle`

Second deploy:

- commit: `d526759da40b7e20a98f5ecaa0cb03d17f04326b`
- safe-deploy apply: PASS
- production hash matched local hash for `/usr/local/bin/v7-users-autoswitch`

Second bounded governed validation after retry-budget correction:

- baseline affected users on `openvpn-1779388847-d2ad7c`: 10
- selected user: `10.7.0.2`
- source: `openvpn-1779388847-d2ad7c`
- target: `vless`
- selected_move_hash: `6bcd509336032e43e4a612d51229c536e46cf4b97f08c8733ebaac974d67db3b`
- runtime apply attempt: PERFORMED
- route verification rc: 0
- service verification rc: 1
- terminal_state: `ROLLED_BACK`
- terminal_reason: `verification_failed_rollback_completed`
- terminal_outcome_classification: `ROLLBACK_SUCCESS`
- users moved after rollback: 0
- affected users remaining on source: 10

Current breakpoint:

The execution chain now reaches Runtime apply and rollback correctly. It does not reach mission SUCCESS because the selected target `vless` failed post-apply service verification. Runtime correctly rolled back the user to `openvpn-1779388847-d2ad7c`.

Current production timer state:

- `v7-users-autoswitch.timer`: inactive / dead
- `v7-users-autoswitch.service`: inactive / dead

Timer was not re-enabled because the latest real execution ended in rollback, not success.
