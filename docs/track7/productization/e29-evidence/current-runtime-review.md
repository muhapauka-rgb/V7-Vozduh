# E29 Current Runtime Review

date_utc=2026-05-29T11:17:46Z
runtime_mutation_performed=false

## Candidate Users

candidate_user_1=10.7.0.11 current=1 table=1009 enabled=1
candidate_user_2=10.7.0.12 current=1 table=1010 enabled=1
candidate_user_3=10.7.0.14 current=1 table=1012 enabled=1
candidate_user_4=10.7.0.15 current=1 table=1013 enabled=1
candidate_users_back_on_rollback_target=true

## Execution Target

target_name=amneziawg-exec-20260528-10-8-1-14
target_role=EXECUTION_ONLY
interface=v7execwg0
soft_limit=4
hard_limit=4
manual_only=1
reserve_only=1
execution_reserved=true
reservation_owner=operator_execution_governance
autoswitch_allowed=false
rebalance_allowed=false
production_assignment_allowed=false
execution_target_isolated=true
autoswitch_exclusion_intact=true

## Runtime Gates

selected_moves=0
hidden_movers_absent=true
runtime_checkers_ok=true
readiness_helper_status=GO
restore_settle_gate_status=GO

checker_results:
- V7_RECONCILE_RESULT=OK
- V7_USER_ROUTE_CHECK=OK
- V7_KILLSWITCH_CHECK=OK
- V7_PROVISIONING_RECONCILE_CHECK=OK

restore_settle_summary:
- gate_status=GO
- sample_count=3
- selected_moves_by_sample=[0, 0, 0]
- registry_stable=True
- egress_registry_stable=True
- checkers_ok=True
- hidden_movers_observed=False
- moved_users=[]

current_runtime_safe=true
