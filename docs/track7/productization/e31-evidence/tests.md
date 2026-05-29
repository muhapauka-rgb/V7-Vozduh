# E31 Tests

date_utc=2026-05-29T17:53:40Z

## Local Validation

- command: `PYTHONPYCACHEPREFIX=.pycache-e31 python3 -m compileall admin_core tools tests`
  - result: PASS
- command: `python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate tests.unit.test_operator_execution_packet tests.unit.test_v7_reconcile_check`
  - result: PASS
  - detail: 32 tests passed
- command: audit validation script over E25.15, E27.2, E28.2, E30.3 evidence
  - result: PASS
  - detail: forward, rollback, and replay markers were present for all certified scales

## Remote Read-Only Runtime Validation

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
  - detail: `second_canary_readiness=GO`
- command: `v7-restore-settle-gate --pre-restore --state-dir /tmp/e30_3/post-rollback-settle --pretty`
  - result: PASS
  - detail: `gate_status=GO`

## Static Scans

- command: credential scan over `docs/track7/productization/e31-evidence`
  - result: PASS
  - detail: no credential-like evidence hits
- command: dangerous-call scan over `docs/track7/productization/e31-evidence`
  - result: PASS
  - detail: no movement/apply/routing/kill-switch mutation strings present in E31 evidence
- command: `git diff --check`
  - result: PASS

## Boundary Assertions

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false
autoswitch_apply_performed_manually=false
canary_performed=false
cohort_performed=false
