# E30.1 Tests

date_utc=2026-05-29T14:10:30Z

## Local Tests

command=PYTHONPYCACHEPREFIX=.pycache-e30_1 python3 -m compileall admin_core tools tests
result=PASS
warnings=none

command=python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate tests.unit.test_operator_execution_packet tests.unit.test_v7_reconcile_check
result=PASS
test_count=32
warnings=none

command=python3 -m json.tool docs/track7/productization/e30_1-evidence/pre-normalization-settle/restore-settle.json
result=PASS
warnings=none

command=python3 -m json.tool docs/track7/productization/e30_1-evidence/post-normalization-settle/restore-settle.json
result=PASS
warnings=none

command=python3 -m json.tool docs/track7/productization/e30_1-evidence/rollback-target-1-probe/summary.json
result=PASS
warnings=none

command=git diff --check
result=PASS
warnings=none

## Runtime Checks

command=v7-reconcile-check
result=PASS
summary=V7_RECONCILE_RESULT=OK

command=v7-user-route-check
result=PASS
summary=V7_USER_ROUTE_CHECK=OK

command=v7-killswitch-check
result=PASS
summary=V7_KILLSWITCH_CHECK=OK

command=v7-provisioning-reconcile-check
result=PASS
summary=V7_PROVISIONING_RECONCILE_CHECK=OK

command=hidden mover scan
result=PASS
summary=no v7-user-switch, v7-routing-sync, or v7-users-autoswitch --apply process observed after normalization

command=v7-second-canary-target-readiness --execution-target-id amneziawg-exec-20260528-10-8-1-14 --candidate-user 10.7.0.11 --pretty
result=PASS
summary=approval_status=GO; second_canary_readiness=GO; target_1_current_user contains exactly the frozen 10-user pool; execution_allowed_now=False

command=v7-restore-settle-gate --pre-restore --state-dir /tmp/e30_1/post-normalization-settle --pretty
result=PASS
summary=gate_status=GO; sample_count=3; selected_moves_by_sample=[0,0,0]; checkers_ok=True; hidden_movers_observed=False

## Route Table Validation

route_tables_validated=1000,1001,1002,1003,1004,1006,1009,1010,1012,1013
expected_default_dev=v7e356a192b79
result=PASS

## Scans

command=rg credential-like patterns over docs/track7/productization/e30_1-evidence
result=PASS
summary=no credential-like material found

command=rg dangerous-call patterns over docs/track7/productization/e30_1-evidence
result=PASS_WITH_EXPECTED_WARNINGS
summary=hits are approved normalization v7-user-switch commands to target 1, documented rollback-if-failed plan strings, hidden mover scan pattern, and killswitch checker references; no autoswitch apply, execution-target movement, broad routing sync, or unrelated route mutation found

## Safety Assertions

autoswitch_apply_performed_manually=false
execution_target_movement_performed=false
unrelated_user_movement=false
normalization_user_movement_only=true
normalization_routing_mutation_only=true
