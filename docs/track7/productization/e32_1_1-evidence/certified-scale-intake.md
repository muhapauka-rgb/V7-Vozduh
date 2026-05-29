# E32.1.1 Certified Scale Intake

mode=ARCHITECTURE_MODELING
runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

## Source Reports Read

- `BLOCK_E25_15_REFRESH_APPROVAL_PACKET_AFTER_REGISTRY_DRIFT_AND_RETRY_MOVEMENT_REPORT.md`
- `BLOCK_E27_2_FIRST_TWO_USER_GOVERNED_MOVEMENT_REPORT.md`
- `BLOCK_E28_2_FIRST_SMALL_COHORT_GOVERNED_MOVEMENT_REPORT.md`
- `BLOCK_E30_2_TEN_USER_CAPACITY_REQUALIFICATION_AND_APPROVAL_PACKET_PREPARATION_REPORT.md`
- `BLOCK_E30_3_FIRST_TEN_USER_GOVERNED_MOVEMENT_REPORT.md`
- `BLOCK_E31_POST_TEN_USER_GOVERNANCE_REVIEW_REPORT.md`

full_e25_e31_chain_loaded=true

## Certified Execution Scales

### CLASS_1 Evidence

- block=E25.15
- users=1
- approved_user=`10.7.0.11`
- forward_target=`amneziawg-exec-20260528-10-8-1-14`
- rollback_target=`1`
- forward_success=true
- rollback_success=true
- only_approved_user_moved=true
- routing_mutation_limited_to_candidate=true
- delayed_movement_observed=false
- replay_rejection_verified=true
- runtime_checkers_ok=true
- restore_settle_gate_status=GO
- certified=true

### CLASS_2 Evidence

- block=E27.2
- users=2
- approved_users=`10.7.0.11,10.7.0.12`
- forward_target=`amneziawg-exec-20260528-10-8-1-14`
- rollback_target=`1`
- forward_success=true
- rollback_success=true
- only_approved_users_moved=true
- routing_mutation_limited_to_candidates=true
- delayed_movement_observed=false
- replay_rejection_verified=true
- runtime_checkers_ok=true
- restore_settle_gate_status=GO
- certified=true

### CLASS_4 Evidence

- block=E28.2
- users=4
- approved_users=`10.7.0.11,10.7.0.12,10.7.0.14,10.7.0.15`
- forward_target=`amneziawg-exec-20260528-10-8-1-14`
- rollback_target=`1`
- forward_success=true
- rollback_success=true
- only_approved_users_moved=true
- routing_mutation_limited_to_candidates=true
- delayed_movement_observed=false
- replay_rejection_verified=true
- runtime_checkers_ok=true
- restore_settle_gate_status=GO
- certified=true

### CLASS_10 Evidence

- block=E30.3
- users=10
- approved_users=`10.7.0.2,10.7.0.3,10.7.0.4,10.7.0.5,10.7.0.6,10.7.0.8,10.7.0.11,10.7.0.12,10.7.0.14,10.7.0.15`
- forward_target=`amneziawg-exec-20260528-10-8-1-14`
- rollback_target=`1`
- forward_success=true
- rollback_success=true
- only_approved_users_moved=true
- routing_mutation_limited_to_candidates=true
- delayed_movement_observed=false
- replay_rejection_verified=true
- runtime_checkers_ok=true
- restore_settle_gate_status=GO
- certified=true

## Capacity Requalification Evidence

E30.2 requalified `amneziawg-exec-20260528-10-8-1-14` from `soft_limit=4 hard_limit=4` to `soft_limit=10 hard_limit=10`.

Evidence:

- capacity_limit_root_cause=GOVERNANCE_LIMIT_ONLY_PENDING_10_USER_REQUALIFICATION
- ten-stream aggregate_avg_mbps=131.537
- ten-stream aggregate_min_mbps=119.541
- per_stream_min_mbps=10.923
- readiness_after_validation=GO
- target_local_capacity_safe=true
- long_window_sample_count=20
- long_window_avg_mbps=57.46
- long_window_min_mbps=11.334
- no_sample_below_floor=true
- runtime_checkers_ok=true
- selected_moves_zero=true
- hidden_movers_absent=true

## Mapping Into Capacity Classes

| Evidence Scale | Capacity Class | Status | Notes |
| --- | --- | --- | --- |
| 1 user | CLASS_1 | CERTIFIED | First production-grade governed movement and rollback. |
| 2 users | CLASS_2 | CERTIFIED | Two-user blast radius and rollback certified. |
| 4 users | CLASS_4 | CERTIFIED | Small-cohort execution certified. |
| 10 users | CLASS_10 | CERTIFIED | Current maximum certified scale. |
| 20 users | CLASS_20_CANDIDATE | NOT_CERTIFIED | Requires capacity proof and governed execution proof. |
| 50 users | CLASS_50_CANDIDATE | NOT_CERTIFIED | Requires prior lower class certification and new scale proof. |
| 100 users | CLASS_100_CANDIDATE | NOT_CERTIFIED | Requires dedicated production-pool model. |
| Production pool | PRODUCTION_POOL | NOT_CERTIFIED | Architecture target, not yet execution-certified. |

current_certified_class_for_amneziawg_exec=CLASS_10

