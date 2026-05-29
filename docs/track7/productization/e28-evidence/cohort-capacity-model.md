# E28 Cohort Capacity Model

date_utc=2026-05-29T06:18:00Z

target=amneziawg-exec-20260528-10-8-1-14
current_soft_limit=2
current_hard_limit=2
current_target_users=0
target_readiness=GO
avg_mbps=27.12
min_mbps=10.67
stability=1.0

## Four User Model

candidate_users=10.7.0.11,10.7.0.12,10.7.0.14,10.7.0.15
modeled_blast_radius=4
required_capacity=4
hard_limit_allows=false
capacity_safe_for_4_users=false

The current quality signal is GO for the execution target at zero assigned users, but the target metadata remains capped at `hard_limit=2`. A four-user movement would exceed the explicit governance capacity bound. E28 is read-only, so it must not requalify or raise limits inside this block.

## Five User Model

candidate_users=10.7.0.11,10.7.0.12,10.7.0.14,10.7.0.15
optional_candidate_user_5=NONE
modeled_blast_radius=5
required_capacity=5
hard_limit_allows=false
eligible_fifth_candidate_available=false
capacity_safe_for_5_users=false

## Complexity Review

throughput_headroom=CONDITIONAL
quality_degradation=UNKNOWN_FOR_4_OR_5_USERS
readiness_impact=UNPROVEN_FOR_4_OR_5_USERS
rollback_complexity=MANAGEABLE_FOR_4_USERS
audit_complexity=MODEL_READY
replay_complexity=MODEL_READY

cohort_capacity_model_safe=false
capacity_blocker=EXECUTION_TARGET_CAPACITY_LIMIT_TWO_USERS
required_next_action=capacity_requalification_before_small_cohort_execution

