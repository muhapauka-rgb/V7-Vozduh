# E32.1.2 Current Metadata Intake

mode=ARCHITECTURE_MODELING
runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

## Sources Reviewed

- `BLOCK_E32_1_1_CAPACITY_CLASS_MODEL_REPORT.md`
- `docs/track7/productization/e32_1_1-evidence/*`
- `BLOCK_E30_2_TEN_USER_CAPACITY_REQUALIFICATION_AND_APPROVAL_PACKET_PREPARATION_REPORT.md`
- `docs/track7/productization/e30_2-evidence/capacity-requalification.md`
- `BLOCK_E31_POST_TEN_USER_GOVERNANCE_REVIEW_REPORT.md`
- `tools/runtime-support/v7-capacity-check`
- `tools/runtime-support/v7-capacity-readiness`

current_metadata_intake_completed=true

## Current Target Metadata

Target:

```text
id=amneziawg-exec-20260528-10-8-1-14
protocol=amneziawg
type=interface
interface=v7execwg0
enabled=1
config=/etc/amnezia/v7execwg0.conf
role=EXECUTION_ONLY
route_table=1250
priority=10
weight=1
soft_limit=10
hard_limit=10
manual_only=1
reserve_only=1
canary_reserved=true
execution_reserved=true
reservation_owner=operator_execution_governance
autoswitch_allowed=false
rebalance_allowed=false
production_assignment_allowed=false
service_tags=governance,execution
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

## Current Capacity Evidence

From E30.2:

- capacity_limit_root_cause=GOVERNANCE_LIMIT_ONLY_PENDING_10_USER_REQUALIFICATION
- soft_limit_before=4
- hard_limit_before=4
- soft_limit_final=10
- hard_limit_final=10
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

From E30.3:

- first_ten_user_governed_movement_executed=true
- forward_success=true
- rollback_success=true
- only_approved_users_moved=true
- routing_mutation_limited_to_candidates=true
- delayed_movement_observed=false
- replay_rejection_verified=true
- runtime_checkers_ok=true
- restore_settle_gate_status=GO
- ten_user_governed_execution_certified=true

From E31:

- production_grade_governance=true
- current_certified_scale=10_users
- recommended_next_program=SHIFT_TO_PRODUCTION_POOL_GOVERNANCE

## Existing Metadata Classes

### Direct Registry Fields

- `soft_limit`
- `hard_limit`
- `role`
- `manual_only`
- `reserve_only`
- `execution_reserved`
- `reservation_owner`
- `autoswitch_allowed`
- `rebalance_allowed`
- `production_assignment_allowed`
- `service_tags`
- `exclude_route_classes`

### Runtime/Evidence Fields

- readiness status
- restore-settle status
- selected moves count
- hidden movers status
- runtime checker status
- target users count
- quality samples
- audit/replay proof

## Intake Conclusion

The current target has enough evidence to model metadata for `CLASS_10`, but the existing registry row does not yet encode a complete capacity metadata object. E32.1.2 should define a structured model that distinguishes:

- historical certification;
- active movement eligibility;
- freshness/expiration state;
- authority versus derived calculations;
- production-pool policy caps;
- future capacity reservation/concurrency handling.

