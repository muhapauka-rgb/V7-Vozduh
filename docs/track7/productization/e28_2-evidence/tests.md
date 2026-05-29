# E28.2 Tests And Safety Checks

date_utc=2026-05-29T10:26:16Z
runtime_mutation_scope=approved_forward_and_rollback_only
user_movement_scope=10.7.0.11,10.7.0.12,10.7.0.14,10.7.0.15
routing_mutation_scope=route_tables_1009_1010_1012_1013_only

## Local Tests

command=PYTHONPYCACHEPREFIX=.pycache-e28_2 python3 -m compileall admin_core tools tests
result=PASS
warnings=none

command=python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate tests.unit.test_operator_execution_packet
result=PASS
test_count=29
warnings=none

command=python3 -m json.tool docs/track7/productization/e28_2-evidence/fresh-approval-packet.json
result=PASS
warnings=none

command=git diff --check
result=PASS
warnings=none

## Runtime Checks

command=v7-reconcile-check
result=PASS
evidence=runtime checker output collected at 2026-05-29T13:26:13+03:00
summary=V7_RECONCILE_RESULT=OK; warnings=0; errors=0

command=v7-user-route-check
result=PASS
evidence=runtime checker output collected at 2026-05-29T13:26:14+03:00
summary=V7_USER_ROUTE_CHECK=OK; approved users restored to egress 1 tables 1009/1010/1012/1013

command=v7-killswitch-check
result=PASS
evidence=runtime checker output collected at 2026-05-29T13:26:15+03:00
summary=V7_KILLSWITCH_CHECK=OK; NAT/MSS for v7execwg0 present; no kill switch control/toggle mutation performed

command=v7-provisioning-reconcile-check
result=PASS
evidence=runtime checker output collected at 2026-05-29T13:26:16+03:00
summary=V7_PROVISIONING_RECONCILE_CHECK=OK

command=ps -eo pid,ppid,etime,command | grep -E 'v7-user-switch|v7-routing-sync|v7-users-autoswitch.*--apply' | grep -v grep
result=PASS
summary=no hidden movers observed after rollback

command=v7-second-canary-target-readiness --execution-target-id amneziawg-exec-20260528-10-8-1-14 --candidate-user 10.7.0.11 --pretty
result=PASS
summary=approval_status=GO; second_canary_readiness=GO; selected_target=amneziawg-exec-20260528-10-8-1-14; execution_allowed_now=False

command=v7-restore-settle-gate --pre-restore --state-dir /tmp/e28_2/post-rollback-settle --pretty
result=PASS
summary=gate_status=GO; sample_count=3; selected_moves_by_sample=[0, 0, 0]; checkers_ok=True; hidden_movers_observed=False

## Safety Scans

command=rg -n "(PrivateKey|BEGIN .*PRIVATE|password=|token=|secret=|Authorization:|api[_-]?key)" docs/track7/productization/e28_2-evidence
result=PASS
summary=no credential-like material found in E28.2 evidence

command=rg -n "(PrivateKey|BEGIN .*PRIVATE|password=|token=|secret=|Authorization:|api[_-]?key)" docs/track7/productization/e28_2-evidence admin_core tools tests
result=PASS_WITH_EXPECTED_WARNINGS
warnings=expected test/template/helper references outside E28.2 evidence only; no E28.2 evidence leak

command=rg -n "v7-user-switch|v7-users-autoswitch --apply|v7-routing-sync|kill switch|killswitch|Direct/RU refresh|Trusted RU refresh|proxy apply|raw unsafe" docs/track7/productization/e28_2-evidence
result=PASS_WITH_EXPECTED_WARNINGS
warnings=approved v7-user-switch forward/rollback commands for exactly four approved users; hidden mover scan pattern; killswitch checker outputs only

## Movement Safety Assertions

no_unauthorized_movement=true
no_autoswitch_apply=true
no_broad_routing_sync=true
no_kill_switch_control_toggle_mutation=true
no_raw_unsafe_profile_execution=true
approved_forward_only=true
approved_rollback_only=true
