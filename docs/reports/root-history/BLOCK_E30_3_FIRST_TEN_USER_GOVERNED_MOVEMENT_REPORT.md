# BLOCK E30.3 First Ten User Governed Movement Report

e30_3_completed=true

first_ten_user_governed_movement_executed=true

cohort_size=10

candidate_user_1=10.7.0.2
candidate_user_2=10.7.0.3
candidate_user_3=10.7.0.4
candidate_user_4=10.7.0.5
candidate_user_5=10.7.0.6
candidate_user_6=10.7.0.8
candidate_user_7=10.7.0.11
candidate_user_8=10.7.0.12
candidate_user_9=10.7.0.14
candidate_user_10=10.7.0.15

forward_target=amneziawg-exec-20260528-10-8-1-14

forward_success=true

rollback_executed=true
rollback_success=true

only_approved_users_moved=true

routing_mutation_limited_to_candidates=true

delayed_movement_observed=false

replay_rejection_verified=true

runtime_checkers_ok=true

restore_settle_gate_status=GO

ten_user_governed_execution_certified=true

remaining_blockers=none

recommended_next_block=E31_POST_TEN_USER_GOVERNANCE_REVIEW

## Authorization

The original E30.2 packet had expired before E30.3 execution resumed. A fresh equivalent E30.3 packet was generated inside the block after a new execution-time recheck.

- packet_id=`packet-dc93ce740f00ee8ad7733be9`
- approval_id=`approval-031a998f5a5b2a18612c7574`
- movement_budget=10
- blast_radius=10
- approval_created_at=`2026-05-29T17:02:19Z`
- approval_expires_at=`2026-05-29T17:32:19Z`
- execution_authorized=true
- restore_settle_gate_status=GO
- target_capacity_ge_10=true
- all_candidates_on_1=true
- target_users_zero=true

## Forward Proof

The approved forward commands executed successfully for exactly the 10 approved users.

- commands_executed=10
- all exit codes were `0`
- all_10_approved_users_moved=true
- route_get_for_all_10_uses_target=true
- target_users_count=10
- no_other_users_moved=true
- selected_moves_count=0
- hidden_movers_absent=true
- runtime_checkers_ok=true

During the observation window the approved cohort remained on the execution target, no 11th user moved, selected moves remained zero, hidden movers remained absent, and runtime checkers remained OK.

## Rollback Proof

The default rollback executed successfully for exactly the same 10 approved users.

- commands_executed=10
- all exit codes were `0`
- all_10_users_back_on_1=true
- route_get_for_all_10_restored=true
- target_users_count=0
- selected_moves_count=0
- hidden_movers_absent=true
- runtime_checkers_ok=true
- rollback_success=true

Post-rollback restore-settle returned `GO` with 3 samples, selected moves `[0, 0, 0]`, hidden movers absent, registry stable, egress registry stable, and checkers OK.

## Delayed Monitoring And Replay

Delayed monitoring samples A, B, and C all showed:

- all approved users remained on `1`
- target_users_count=0
- selected_moves_count=0
- hidden_movers_present=false
- runtime_checkers_ok=true
- readiness_status=GO

Replay validation:

- expected=DENY_REPLAY
- actual=DENY_REPLAY
- no_movement=true
- no_routing_mutation=true
- replay_rejection_verified=true

## Tests

- `compileall`: PASS
- targeted unit tests: PASS, 32 tests
- JSON validation: PASS
- remote runtime checkers: PASS
- hidden mover scan: PASS
- readiness helper: PASS
- restore-settle helper: PASS
- credential scan: PASS
- dangerous-call scan: PASS_WITH_EXPECTED_HITS limited to the hidden-mover scan pattern in the evidence helper
- `git diff --check`: PASS

## Final Mutation Statement

Runtime mutation performed: YES

If YES:
only approved 10-user forward movement and rollback

User movement performed: YES

If YES:
only approved 10 users

Routing mutation for users performed: YES

If YES:
only route tables 1000,1001,1002,1003,1004,1006,1009,1010,1012,1013

Kill switch control/toggle mutation performed: NO

Autoswitch apply performed manually: NO

Raw unsafe profile executed: NO

Canary performed: NO

Cohort beyond approved 10 users performed: NO
