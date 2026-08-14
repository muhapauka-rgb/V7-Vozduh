# BLOCK E30.1 - Ten User Candidate Pool Preparation Report

date_utc=2026-05-29T14:10:30Z
mode=TEN_USER_CANDIDATE_POOL_PREPARATION

## Verdict

e30_1_completed=true

runtime_mutation_performed=true
runtime_mutation_scope=only_candidate_pool_normalization_to_rollback_target_1

user_movement_performed=true
user_movement_scope=10.7.0.2,10.7.0.3,10.7.0.4,10.7.0.5,10.7.0.6,10.7.0.8 moved from awg3 to 1

routing_mutation_performed=true
routing_mutation_scope=route_tables_1000,1001,1002,1003,1004,1006 changed from awg3 to v7e356a192b79

enabled_user_count=17
rollback_target_1_user_count_before=4
rollback_target_1_user_count_after=10

normalization_needed=true
normalization_performed=true
normalization_user_count=6

ten_user_candidate_pool_ready=true
candidate_count_final=10

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

selected_moves_zero=true
hidden_movers_absent=true
runtime_checkers_ok=true
restore_settle_gate_status=GO

remaining_blockers=EXECUTION_TARGET_CAPACITY_METADATA_STILL_4
recommended_next_block=E30_2_TEN_USER_CAPACITY_REQUALIFICATION_AND_APPROVAL_PACKET_PREPARATION

## Inventory And Classification

E30 found only four users on rollback target `1`. E30.1 classified six additional enabled 10.7 users on `awg3` as eligible for minimum candidate-pool normalization:

- 10.7.0.2 / table 1000
- 10.7.0.3 / table 1001
- 10.7.0.4 / table 1002
- 10.7.0.5 / table 1003
- 10.7.0.6 / table 1004
- 10.7.0.8 / table 1006

Not selected:
- 10.7.0.7 because disabled
- 10.7.0.16 because vless special path and not required
- 10.0.0.2, 10.0.0.3, 10.0.0.6 because older 10.0 subnet was not required for this 10.7 candidate pool
- 10.7.0.9, 10.7.0.10, 10.7.0.13 because awg0 pool was not required after awg3 provided the exact six needed users

evidence:
- docs/track7/productization/e30_1-evidence/full-user-inventory.md
- docs/track7/productization/e30_1-evidence/candidate-classification.md

## Normalization Plan And Authorization

normalization_plan_safe=true
normalization_execution_authorized=true

Pre-normalization gates:
- users_registry_hash=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
- egress_registry_hash=0e92aae87c50da664424f51ff5ce83d0caedd9d835ba3e45fb41b1ba7237e689
- selected_moves_count=0
- hidden_movers_present=false
- runtime_checkers_ok=true
- restore_settle_gate_status=GO
- autoswitch_apply_performed=false

Rollback target 1 probe:
- iface=v7e356a192b79
- probe_streams_per_round=10
- probe_count=30
- aggregate_avg_mbps=319.624
- aggregate_min_mbps=306.711
- rollback_target_capacity_probe_safe=true

evidence:
- docs/track7/productization/e30_1-evidence/normalization-plan.md
- docs/track7/productization/e30_1-evidence/pre-normalization-recheck.md
- docs/track7/productization/e30_1-evidence/rollback-target-1-probe/summary.json
- docs/track7/productization/e30_1-evidence/pre-normalization-settle/restore-settle.pretty

## Candidate Pool Normalization

Executed commands:
- v7-user-switch 10.7.0.2 1
- v7-user-switch 10.7.0.3 1
- v7-user-switch 10.7.0.4 1
- v7-user-switch 10.7.0.5 1
- v7-user-switch 10.7.0.6 1
- v7-user-switch 10.7.0.8 1

exit_codes=0,0,0,0,0,0
diff_status=OK
audit_record_hash=a39c9fc75d1b41e2cf2eba9b081b7a97af79c6f8dc46fbe45f7f51570f67b70e

Only the selected six users changed from `awg3` to `1`. Only their route tables changed from `default dev awg3` to `default dev v7e356a192b79`.

evidence=docs/track7/productization/e30_1-evidence/candidate-pool-normalization.md

## Post-Normalization Verification

rollback_target_1_user_count_after=10
ten_user_candidate_pool_ready=true

Frozen candidate set:
- 10.7.0.2 / table 1000 / current=1
- 10.7.0.3 / table 1001 / current=1
- 10.7.0.4 / table 1002 / current=1
- 10.7.0.5 / table 1003 / current=1
- 10.7.0.6 / table 1004 / current=1
- 10.7.0.8 / table 1006 / current=1
- 10.7.0.11 / table 1009 / current=1
- 10.7.0.12 / table 1010 / current=1
- 10.7.0.14 / table 1012 / current=1
- 10.7.0.15 / table 1013 / current=1

Post-normalization gates:
- selected_moves_count=0
- hidden_movers_present=false
- runtime_checkers_ok=true
- restore_settle_gate_status=GO
- readiness_still_go=true

evidence:
- docs/track7/productization/e30_1-evidence/post-normalization-verification.md
- docs/track7/productization/e30_1-evidence/ten-user-candidate-set.md
- docs/track7/productization/e30_1-evidence/governance-safety-review.md
- docs/track7/productization/e30_1-evidence/post-normalization-settle/restore-settle.pretty

## Governance Safety

blast_radius_model=10
rollback_manifest:
- 10.7.0.2 -> 1
- 10.7.0.3 -> 1
- 10.7.0.4 -> 1
- 10.7.0.5 -> 1
- 10.7.0.6 -> 1
- 10.7.0.8 -> 1
- 10.7.0.11 -> 1
- 10.7.0.12 -> 1
- 10.7.0.14 -> 1
- 10.7.0.15 -> 1

execution_target_role=EXECUTION_ONLY
execution_target_autoswitch_allowed=false
execution_target_rebalance_allowed=false
execution_target_movement_performed=false
autoswitch_apply_performed=false
governance_safe_for_ten_user_candidate_pool=true

## Tests

py_compile=PASS
targeted_unit_tests=PASS
targeted_unit_test_count=32
runtime_checkers=PASS
hidden_mover_scan=PASS
readiness_helper=PASS
restore_settle_helper=PASS
route_table_validation=PASS
credential_scan=PASS
dangerous_call_scan=PASS_WITH_EXPECTED_APPROVED_NORMALIZATION_REFERENCES
git_diff_check=PASS

evidence=docs/track7/productization/e30_1-evidence/tests.md

## Final Answers

e30_1_completed=true

runtime_mutation_performed=true
runtime_mutation_scope=only_candidate_pool_normalization_to_rollback_target_1

user_movement_performed=true
user_movement_scope=10.7.0.2,10.7.0.3,10.7.0.4,10.7.0.5,10.7.0.6,10.7.0.8

routing_mutation_performed=true
routing_mutation_scope=route_tables_1000,1001,1002,1003,1004,1006

enabled_user_count=17
rollback_target_1_user_count_before=4
rollback_target_1_user_count_after=10

normalization_needed=true
normalization_performed=true
normalization_user_count=6

ten_user_candidate_pool_ready=true
candidate_count_final=10

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

selected_moves_zero=true
hidden_movers_absent=true
runtime_checkers_ok=true
restore_settle_gate_status=GO

remaining_blockers=EXECUTION_TARGET_CAPACITY_METADATA_STILL_4
recommended_next_block=E30_2_TEN_USER_CAPACITY_REQUALIFICATION_AND_APPROVAL_PACKET_PREPARATION

## Final Mutation Statement

Runtime mutation performed: YES
If YES: only candidate-pool normalization to rollback target `1`

User movement performed: YES
If YES: only selected normalization users moved to rollback target `1`

Routing mutation performed: YES
If YES: only selected normalization user route tables changed

Kill switch control/toggle mutation performed: NO
Autoswitch apply performed manually: NO
Execution-target movement performed: NO
Canary performed: NO
Cohort movement performed: NO
