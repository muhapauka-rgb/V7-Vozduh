# BLOCK E28 Small Cohort Governed Movement Preparation Report

## Summary

e28_completed=true
runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

E28 prepared the first small-cohort governed movement model. Four clean candidate users were found, rollback is deterministic, audit/replay semantics scale in model, delayed movement protection scales, and governance isolation is intact.

Execution is not ready yet because the current execution target remains capped at `soft_limit=2` and `hard_limit=2`, while a small cohort requires at least 4 users.

small_cohort_readiness=NO-GO
recommended_next_block=E28_1_SMALL_COHORT_CAPACITY_REQUALIFICATION

## Evidence

- `docs/track7/productization/e28-evidence/runtime-snapshot.md`
- `docs/track7/productization/e28-evidence/cohort-candidate-discovery.md`
- `docs/track7/productization/e28-evidence/target-capacity-review.md`
- `docs/track7/productization/e28-evidence/cohort-capacity-model.md`
- `docs/track7/productization/e28-evidence/blast-radius-model.md`
- `docs/track7/productization/e28-evidence/cohort-rollback-model.md`
- `docs/track7/productization/e28-evidence/audit-replay-model.md`
- `docs/track7/productization/e28-evidence/delayed-movement-model.md`
- `docs/track7/productization/e28-evidence/governance-review.md`
- `docs/track7/productization/e28-evidence/readiness-decision.md`
- `docs/track7/productization/e28-evidence/tests.md`

## Runtime Snapshot

hostname=v3119922.hosted-by-vdsina.ru
users_registry_hash=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
egress_registry_hash=13ae747486e30b4ad527c28343529f580fc400867981557845708c34385dd4ed
target=amneziawg-exec-20260528-10-8-1-14
target_users=0
target_readiness=GO
restore_settle_gate_status=GO
selected_moves_zero=true
hidden_movers_absent=true
runtime_checkers_ok=true

## Candidate Discovery

candidate_count=4
candidate_user_1=10.7.0.11
candidate_user_2=10.7.0.12
candidate_user_3=10.7.0.14
candidate_user_4=10.7.0.15
candidate_user_5=NONE

All four selected users are enabled, currently on rollback target `1`, and have known route tables:

- 10.7.0.11 table=1009
- 10.7.0.12 table=1010
- 10.7.0.14 table=1012
- 10.7.0.15 table=1013

## Capacity Review

target_name=amneziawg-exec-20260528-10-8-1-14
soft_limit=2
hard_limit=2
target_current_user_count=0
avg_mbps=27.12
min_mbps=10.67
stability=1.0

capacity_safe_for_4_users=false
capacity_safe_for_5_users=false
cohort_capacity_model_safe=false
capacity_blocker=EXECUTION_TARGET_CAPACITY_LIMIT_TWO_USERS

The target is currently GO, but its explicit hard capacity bound is 2. E28 is read-only and did not requalify capacity.

## Governance And Rollback

blast_radius_model_safe=true
cohort_rollback_safe=true
audit_scales_to_small_cohort=true
replay_scales_to_small_cohort=true
delayed_movement_protection_scales=true
governance_safe_for_small_cohort=true

Rollback manifest:

- 10.7.0.11 -> 1
- 10.7.0.12 -> 1
- 10.7.0.14 -> 1
- 10.7.0.15 -> 1

Execution-only isolation:

- role=EXECUTION_ONLY
- autoswitch_allowed=false
- rebalance_allowed=false
- production_assignment_allowed=false
- selected_moves=0
- hidden_movers_absent=true

## Tests

py_compile=PASS
runtime_checkers=PASS
readiness_helper=PASS_GO
restore_settle_helper=PASS_GO
hidden_mover_scan=PASS
audit_validation=PASS
credential_scan=PASS
dangerous_call_scan=PASS_WITH_EXPECTED_HITS
git_diff_check=PASS

## Final Answers

e28_completed=true

runtime_mutation_performed=false

candidate_count=4

candidate_user_1=10.7.0.11
candidate_user_2=10.7.0.12
candidate_user_3=10.7.0.14
candidate_user_4=10.7.0.15
candidate_user_5=NONE

capacity_safe_for_4_users=false
capacity_safe_for_5_users=false

cohort_capacity_model_safe=false

blast_radius_model_safe=true

cohort_rollback_safe=true

audit_scales_to_small_cohort=true

replay_scales_to_small_cohort=true

delayed_movement_protection_scales=true

governance_safe_for_small_cohort=true

small_cohort_readiness=NO-GO

recommended_cohort_size=4_AFTER_CAPACITY_REQUALIFICATION

remaining_blockers=EXECUTION_TARGET_CAPACITY_LIMIT_TWO_USERS

recommended_next_block=E28_1_SMALL_COHORT_CAPACITY_REQUALIFICATION

## Final Mutation Statement

Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
Cohort performed: NO

