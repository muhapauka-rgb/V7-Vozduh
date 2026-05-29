# E30 Tests

date_utc=2026-05-29T12:04:00Z
runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

## Local Tests

command=PYTHONPYCACHEPREFIX=.pycache-e30 python3 -m compileall admin_core tools tests
result=PASS
warnings=none

command=python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate tests.unit.test_operator_execution_packet tests.unit.test_v7_reconcile_check
result=PASS
test_count=32
warnings=none

command=python3 -m json.tool docs/track7/productization/e30-evidence/capacity-probe/summary.json
result=PASS
warnings=none

command=python3 -m json.tool docs/track7/productization/e30-evidence/restore-settle/restore-settle.json
result=PASS
warnings=none

command=git diff --check
result=PASS
warnings=none

## Runtime Read-Only Checks

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
summary=no v7-user-switch, v7-routing-sync, or v7-users-autoswitch --apply process observed

command=v7-second-canary-target-readiness --execution-target-id amneziawg-exec-20260528-10-8-1-14 --candidate-user 10.7.0.11 --pretty
result=PASS
summary=approval_status=GO; second_canary_readiness=GO; execution_allowed_now=False

command=v7-restore-settle-gate --pre-restore --state-dir /tmp/e30/restore-settle --pretty
result=PASS
summary=gate_status=GO; sample_count=3; selected_moves_by_sample=[0,0,0]; checkers_ok=True; hidden_movers_observed=False

## Capacity Validation

command=bash /tmp/e30_remote.sh target-local 10-stream validation
result=PASS
summary=probe_streams_per_round=10; round_count=3; probe_count=30; aggregate_avg_mbps=142.73; aggregate_min_mbps=135.476; readiness_after=GO; runtime_checkers_ok=true; target_local_capacity_safe=true

## Scans

command=rg credential-like patterns over docs/track7/productization/e30-evidence
result=PASS
summary=no credential-like material found

command=rg dangerous-call patterns over docs/track7/productization/e30-evidence
result=PASS_WITH_EXPECTED_WARNINGS
summary=only hidden mover scan pattern and v7-killswitch-check references found; no v7-user-switch execution, autoswitch apply, broad routing sync, route mutation, or raw unsafe execution

## Mutation Statement For Tests

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false
autoswitch_apply_performed_manually=false
canary_performed=false
cohort_performed=false
