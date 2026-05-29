# E30.2 Tests

date_utc=2026-05-29T15:12:05Z

## Local validation

- command: `PYTHONPYCACHEPREFIX=.pycache-e30_2 python3 -m compileall admin_core tools tests`
  - result: PASS
- command: `python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate tests.unit.test_operator_execution_packet tests.unit.test_v7_reconcile_check`
  - result: PASS
  - detail: 32 tests passed
- command: `python3 -m json.tool docs/track7/productization/e30_2-evidence/fresh-approval-packet.json`
  - result: PASS
- command: `python3 -m json.tool docs/track7/productization/e30_2-evidence/long-window/summary.json`
  - result: PASS
- command: `python3 -m json.tool docs/track7/productization/e30_2-evidence/final-settle/restore-settle.json`
  - result: PASS

## Remote runtime validation

- command: `v7-reconcile-check`
  - result: PASS
  - detail: `V7_RECONCILE_RESULT=OK`
- command: `v7-user-route-check`
  - result: PASS
  - detail: `V7_USER_ROUTE_CHECK=OK`
- command: `v7-killswitch-check`
  - result: PASS
  - detail: `V7_KILLSWITCH_CHECK=OK`
- command: `v7-provisioning-reconcile-check`
  - result: PASS
  - detail: `V7_PROVISIONING_RECONCILE_CHECK=OK`
- command: hidden mover scan
  - result: PASS
  - detail: no active `v7-user-switch`, `v7-routing-sync`, or `v7-users-autoswitch --apply` process observed
- command: `v7-second-canary-target-readiness --execution-target-id amneziawg-exec-20260528-10-8-1-14 --candidate-user 10.7.0.11 --pretty`
  - result: PASS
  - detail: `second_canary_readiness=GO`, selected target is the execution target
- command: `v7-restore-settle-gate --pre-restore --state-dir /tmp/e30_2/final-settle --pretty`
  - result: PASS
  - detail: `gate_status=GO`, selected moves `[0, 0, 0]`, checkers OK

## Static scans

- command: credential scan over `docs/track7/productization/e30_2-evidence`
  - result: PASS
  - detail: no credential-like evidence hits
- command: dangerous-call scan over `docs/track7/productization/e30_2-evidence`
  - result: PASS_WITH_EXPECTED_HITS
  - detail: hits are limited to hidden-mover scan patterns inside `e30_2_remote.sh` and `v7-killswitch-check` checker references; no candidate `v7-user-switch`, autoswitch apply, routing-sync apply, route mutation, nft mutation, or iptables mutation was executed
- command: `git diff --check`
  - result: PASS

## Boundary assertions

no_execution_target_movement=true
no_autoswitch_apply=true
no_unauthorized_movement=true
user_movement_performed=false
routing_mutation_performed=false
kill_switch_control_toggle_mutation_performed=false
