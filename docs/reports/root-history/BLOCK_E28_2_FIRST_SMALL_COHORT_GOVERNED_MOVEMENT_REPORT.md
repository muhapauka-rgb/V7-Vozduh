# BLOCK E28.2 - First Small Cohort Governed Movement Report

date_utc=2026-05-29T10:26:16Z
mode=FIRST_REAL_SMALL_COHORT_GOVERNED_EXECUTION

## Verdict

e28_2_completed=true
first_small_cohort_governed_movement_executed=true
small_cohort_governed_execution_certified=true

cohort_size=4
candidate_user_1=10.7.0.11
candidate_user_2=10.7.0.12
candidate_user_3=10.7.0.14
candidate_user_4=10.7.0.15

forward_target=amneziawg-exec-20260528-10-8-1-14
rollback_target=1

forward_success=true
rollback_executed=true
rollback_success=true

only_approved_users_moved=true
routing_mutation_limited_to_candidates=true
delayed_movement_observed=false
replay_rejection_verified=true
runtime_checkers_ok=true
restore_settle_gate_status=GO

remaining_blockers=none
recommended_next_block=E29_POST_SMALL_COHORT_GOVERNANCE_REVIEW

## Approval Packet

packet_id=packet-4b17f2916f76e61a74b46154
approval_id=approval-9999aec73533846fba1463ec
operation_id=e28-2-small-cohort-20260529T100529Z
packet_hash=836009e5a08291f838909342743051ea9406d9edff23eae182b1a10c245785ce
movement_budget=4
blast_radius=4
approval_created_at=2026-05-29T10:05:29Z
approval_expires_at=2026-05-29T10:35:29Z
packet_non_expired_at_authorization=true

fresh_users_registry_hash=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
fresh_egress_registry_hash=0e92aae87c50da664424f51ff5ce83d0caedd9d835ba3e45fb41b1ba7237e689
selected_moves_hash=NONE

packet_files:
- docs/track7/productization/e28_2-evidence/fresh-approval-packet.json
- docs/track7/productization/e28_2-evidence/fresh-approval-packet.md

## Execution-Time Recheck

execution_recheck_passed=true
execution_authorized=true
target_readiness=GO
target_users_before_forward=0
target_soft_limit=4
target_hard_limit=4
restore_settle_gate_status=GO
selected_moves_count=0
hidden_movers_present=false
runtime_checkers_ok=true

evidence:
- docs/track7/productization/e28_2-evidence/execution-time-recheck.md
- docs/track7/productization/e28_2-evidence/final-execution-authorization.md
- docs/track7/productization/e28_2-evidence/recheck-settle/restore-settle.pretty

## Forward Movement

approved_commands:
- v7-user-switch 10.7.0.11 amneziawg-exec-20260528-10-8-1-14
- v7-user-switch 10.7.0.12 amneziawg-exec-20260528-10-8-1-14
- v7-user-switch 10.7.0.14 amneziawg-exec-20260528-10-8-1-14
- v7-user-switch 10.7.0.15 amneziawg-exec-20260528-10-8-1-14

exit_codes=0,0,0,0
users_before_forward_hash=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
users_after_forward_hash=c8346e4e11d4bbf03866795cca2e0522d74a4777e83031446b60b840b3a421cc
forward_audit_record_hash=8d2d6a7ba121dc077ad4ed477161bbe5a1cbdc11ae99ff52b4519291c26c963e

forward_verification:
- all_4_approved_users_on_target=true
- target_users=4
- route_tables_1009_1010_1012_1013_use_v7execwg0=true
- no_other_users_moved=true
- selected_moves_count=0
- hidden_movers_present=false
- runtime_checkers_ok=true

evidence:
- docs/track7/productization/e28_2-evidence/forward-execution.md
- docs/track7/productization/e28_2-evidence/forward-verification.md

## Observation Window

observation_samples=3
all_4_users_remained_on_target=true
no_fifth_user_moved=true
target_users=4
selected_moves_count=0
hidden_movers_present=false
runtime_checkers_ok=true

evidence:
- docs/track7/productization/e28_2-evidence/observation-A.md
- docs/track7/productization/e28_2-evidence/observation-B.md
- docs/track7/productization/e28_2-evidence/observation-C.md

## Rollback

approved_rollback_commands:
- v7-user-switch 10.7.0.11 1
- v7-user-switch 10.7.0.12 1
- v7-user-switch 10.7.0.14 1
- v7-user-switch 10.7.0.15 1

rollback_exit_codes=0,0,0,0
rollback_audit_record_hash=dfe8fce3edb88657c3d89056621bf2da7805bb533b41094ab5de8e04e979894a
users_after_rollback_hash=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
users_registry_restored_to_pre_forward=true

rollback_verification:
- all_4_approved_users_back_on_1=true
- target_users=0
- route_tables_1009_1010_1012_1013_restored_to_v7e356a192b79=true
- no_other_users_changed=true
- selected_moves_count=0
- hidden_movers_present=false
- runtime_checkers_ok=true

evidence:
- docs/track7/productization/e28_2-evidence/rollback-execution.md
- docs/track7/productization/e28_2-evidence/rollback-verification.md

## Post-Rollback Restore-Settle

restore_settle_gate_status=GO
sample_count=3
samples_span_seconds=120
apply_timer_intervals_covered=6.0
selected_moves_by_sample=[0, 0, 0]
registry_stable=true
egress_registry_stable=true
checkers_ok=true
hidden_movers_observed=false
moved_users=[]

evidence:
- docs/track7/productization/e28_2-evidence/post-rollback-restore-settle.md
- docs/track7/productization/e28_2-evidence/post-rollback-settle/restore-settle.pretty
- docs/track7/productization/e28_2-evidence/post-rollback-settle/restore-settle.json

## Delayed Monitoring

delayed_samples=3
delayed_movement_observed=false
unapproved_user_movement=false
routing_drift=false
runtime_checkers_ok=true
target_users=0
selected_moves_count=0
hidden_movers_present=false

evidence:
- docs/track7/productization/e28_2-evidence/delayed-monitoring-A.md
- docs/track7/productization/e28_2-evidence/delayed-monitoring-B.md
- docs/track7/productization/e28_2-evidence/delayed-monitoring-C.md

## Replay Validation

replay_verdict=DENY_REPLAY
used_forward_records=1
movement_executed_during_replay=false
routing_mutation_during_replay=false
before_users_hash=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
after_users_hash=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
before_target_users=0
after_target_users=0
replay_denial_audit_record_hash=9674ddc40f6880a86d678a3be41b7ce0c58fac04b1e1da93a097246fb7f197a4

evidence:
- docs/track7/productization/e28_2-evidence/replay-validation.md

## Tests

tests_summary:
- py_compile=PASS
- targeted_execution_tests=PASS
- targeted_unit_tests=PASS,29_tests
- runtime_checkers=PASS
- hidden_mover_scan=PASS
- readiness_helper=PASS
- restore_settle_helper=PASS
- credential_scan=PASS
- dangerous_call_scan=PASS_WITH_EXPECTED_APPROVED_MOVEMENT_HITS
- git_diff_check=PASS

evidence:
- docs/track7/productization/e28_2-evidence/tests.md

## Commands Run

remote_orchestration:
- scp docs/track7/productization/e28_2-evidence/e28_2_remote.sh v7-vps:/tmp/e28_2_remote.sh
- ssh v7-vps 'bash /tmp/e28_2_remote.sh recheck'
- ssh v7-vps 'bash /tmp/e28_2_remote.sh authorize'
- ssh v7-vps 'bash /tmp/e28_2_remote.sh forward'
- ssh v7-vps 'bash /tmp/e28_2_remote.sh verify-forward'
- ssh v7-vps 'bash /tmp/e28_2_remote.sh observe'
- ssh v7-vps 'bash /tmp/e28_2_remote.sh rollback'
- ssh v7-vps 'bash /tmp/e28_2_remote.sh verify-rollback'
- ssh v7-vps 'bash /tmp/e28_2_remote.sh post-rollback-settle'
- ssh v7-vps 'bash /tmp/e28_2_remote.sh delayed-monitoring'
- ssh v7-vps 'bash /tmp/e28_2_remote.sh replay'
- scp -r v7-vps:/tmp/e28_2/* docs/track7/productization/e28_2-evidence/

local_tests:
- PYTHONPYCACHEPREFIX=.pycache-e28_2 python3 -m compileall admin_core tools tests
- python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate tests.unit.test_operator_execution_packet
- python3 -m json.tool docs/track7/productization/e28_2-evidence/fresh-approval-packet.json
- rg credential scan over docs/track7/productization/e28_2-evidence
- rg dangerous-call scan over docs/track7/productization/e28_2-evidence
- git diff --check

## Final Mutation Statement

Runtime mutation performed: YES
If YES: only approved 4-user forward movement and rollback

User movement performed: YES
If YES: only 10.7.0.11, 10.7.0.12, 10.7.0.14, 10.7.0.15

Routing mutation for users performed: YES
If YES: only route tables 1009, 1010, 1012, 1013

Kill switch control/toggle mutation performed: NO
Autoswitch apply performed manually: NO
Raw unsafe profile executed: NO
Canary performed: NO
Cohort beyond approved 4 users performed: NO
