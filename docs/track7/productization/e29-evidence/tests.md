# E29 Tests

date_utc=2026-05-29T11:17:46Z
runtime_mutation_performed=false

## Local Tests

command=PYTHONPYCACHEPREFIX=.pycache-e29 python3 -m compileall admin_core tools tests
result=PASS
warnings=none

command=python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate tests.unit.test_operator_execution_packet tests.unit.test_v7_reconcile_check
result=PASS
test_count=32
warnings=none

command=python3 -m json.tool docs/track7/productization/e28_2-evidence/fresh-approval-packet.json
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

command=hidden mover scan for v7-user-switch, v7-routing-sync, v7-users-autoswitch --apply
result=PASS
summary=no hidden movers observed

command=v7-second-canary-target-readiness --execution-target-id amneziawg-exec-20260528-10-8-1-14 --candidate-user 10.7.0.11 --pretty
result=PASS
summary=approval_status=GO; second_canary_readiness=GO; execution_allowed_now=False

command=v7-restore-settle-gate --pre-restore --state-dir /tmp/e28_2/post-rollback-settle --pretty
result=PASS
summary=gate_status=GO; selected_moves_by_sample=[0,0,0]; checkers_ok=True; hidden_movers_observed=False

## Audit Validation

command=grep audit records for E25.15, E27.2, E28.2 in /opt/v7/audit/operator-execution-audit.jsonl
result=PASS
summary=forward, rollback, and final replay denial records found for certified one-user, two-user, and four-user executions
warnings=E27.2 retained an earlier REPLAY_NOT_CONSUMED audit nuance before final DENY_REPLAY; append-only behavior preserved and final denial exists

## Scans

command=rg credential-like patterns over certified movement reports and evidence
result=PASS_WITH_SELF_REFERENTIAL_WARNINGS
summary=only regex command text in tests evidence was found; no credential material found in movement evidence

command=rg dangerous-call patterns over certified movement reports and evidence
result=PASS_WITH_EXPECTED_WARNINGS
summary=hits are approved v7-user-switch forward/rollback commands, hidden mover scan patterns, and checker references; no autoswitch apply, broad routing sync, kill-switch toggle, raw unsafe profile execution, or unapproved movement found

## Mutation Statement For Tests

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false
autoswitch_apply_performed_manually=false
canary_performed=false
cohort_performed=false
