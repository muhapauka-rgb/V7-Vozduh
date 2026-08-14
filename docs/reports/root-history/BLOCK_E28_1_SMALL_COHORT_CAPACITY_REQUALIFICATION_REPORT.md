# BLOCK E28.1 Small Cohort Capacity Requalification Report

## Summary

e28_1_completed=true

runtime_mutation_performed=true
runtime_mutation_scope=target capacity metadata `soft_limit/hard_limit` only

user_movement_performed=false
routing_mutation_performed=false

target_name=amneziawg-exec-20260528-10-8-1-14

E28.1 proved that the previous `soft_limit=2` and `hard_limit=2` were a governance metadata limit, not a demonstrated physical throughput/stability limit. After target-local four-stream validation, the target was safely requalified to `soft_limit=4` and `hard_limit=4`, then held a 20-sample long-window above quality floors with runtime checkers OK and no user movement.

small_cohort_readiness=GO
recommended_next_block=E28_2_FIRST_SMALL_COHORT_GOVERNED_MOVEMENT

## Evidence

- `docs/track7/productization/e28_1-evidence/capacity-root-cause.md`
- `docs/track7/productization/e28_1-evidence/four-user-capacity-model.md`
- `docs/track7/productization/e28_1-evidence/target-local-capacity-validation.md`
- `docs/track7/productization/e28_1-evidence/capacity-probe/summary.json`
- `docs/track7/productization/e28_1-evidence/capacity-requalification.md`
- `docs/track7/productization/e28_1-evidence/long-window-validation.md`
- `docs/track7/productization/e28_1-evidence/long-window/summary.json`
- `docs/track7/productization/e28_1-evidence/four-user-rollback-model.md`
- `docs/track7/productization/e28_1-evidence/governance-review.md`
- `docs/track7/productization/e28_1-evidence/readiness-decision.md`
- `docs/track7/productization/e28_1-evidence/restore-settle.pretty`
- `docs/track7/productization/e28_1-evidence/tests.md`

## Capacity Root Cause

capacity_limit_root_cause=GOVERNANCE_LIMIT_ONLY_PENDING_4_USER_VALIDATION

Before:

- soft_limit_before=2
- hard_limit_before=2
- egress_registry_hash_before=13ae747486e30b4ad527c28343529f580fc400867981557845708c34385dd4ed

The target was GO and zero-user before requalification. E28 had already found four eligible rollback-target users, but execution was blocked because the explicit target metadata still capped capacity at two users.

## Target-Local Capacity Validation

The block ran 5 rounds of 4 simultaneous target-local probe streams through `v7execwg0`, without moving users and without changing user route tables.

Results:

- probe_streams_per_round=4
- round_count=5
- probe_count=20
- all_rc_ok=true
- aggregate_avg_mbps=98.891
- aggregate_min_mbps=48.699
- aggregate_rounds=[83.481,142.491,111.745,48.699,108.039]
- no_aggregate_round_below_10=true
- target_local_capacity_safe=true

The minimum aggregate round stayed well above the 10 Mbps floor.

## Capacity Requalification

Backup:

- `/opt/v7/egress/state/e28_1-backups/egress.registry.20260529T063951Z`

Mutation performed:

```text
amneziawg-exec-20260528-10-8-1-14:
soft_limit=2 hard_limit=2 -> soft_limit=4 hard_limit=4
```

After:

- soft_limit_final=4
- hard_limit_final=4
- egress_registry_hash_after=0e92aae87c50da664424f51ff5ce83d0caedd9d835ba3e45fb41b1ba7237e689
- capacity_requalification_attempted=true
- capacity_requalification_successful=true

Only the execution target metadata row changed.

## Long Window Validation

20-sample validation after requalification:

- sample_count=20
- avg_mbps=45.647
- min_mbps=12.571
- max_mbps=69.912
- readiness_all_go=true
- no_sample_below_floor=true
- target_users_zero=true
- selected_moves_zero=true
- hidden_movers_absent=true
- runtime_checkers_ok=true
- users_registry_stable=true
- egress_registry_stable=true
- four_user_capacity_validated=true

## Restore-Settle

Fresh restore-settle:

- gate_status=GO
- sample_count=3
- apply_timer_intervals_covered=6.0
- selected_moves_by_sample=[0,0,0]
- movement_count_by_sample=[0,0,0]
- registry_stable=true
- egress_registry_stable=true
- checkers_ok=true
- hidden_movers_observed=false

## Rollback And Governance Model

Four-user rollback manifest:

- 10.7.0.11 -> 1 / table 1009
- 10.7.0.12 -> 1 / table 1010
- 10.7.0.14 -> 1 / table 1012
- 10.7.0.15 -> 1 / table 1013

Governance:

- blast_radius=4
- target_role=EXECUTION_ONLY
- autoswitch_allowed=false
- rebalance_allowed=false
- production_assignment_allowed=false
- selected_moves_count=0
- hidden_movers_present=false
- runtime_checkers_ok=true
- target_users=0
- governance_safe_for_four_users=true
- four_user_rollback_safe=true

## Tests

Test summary:

- py_compile/compileall: PASS
- targeted unit tests: PASS, 29 tests
- JSON validation: PASS
- runtime checkers: PASS
- readiness helper: PASS, GO
- restore-settle helper: PASS, GO
- hidden mover scan: PASS
- credential scan: PASS
- dangerous-call scan: PASS_WITH_EXPECTED_HITS, hidden mover scan pattern only
- git diff --check: PASS

## Final Answers

e28_1_completed=true

runtime_mutation_performed=true
runtime_mutation_scope=target_capacity_metadata_soft_limit_hard_limit_only

user_movement_performed=false
routing_mutation_performed=false

target_name=amneziawg-exec-20260528-10-8-1-14

capacity_limit_root_cause=GOVERNANCE_LIMIT_ONLY_PENDING_4_USER_VALIDATION

soft_limit_before=2
hard_limit_before=2

soft_limit_final=4
hard_limit_final=4

capacity_model_safe=true
target_local_capacity_safe=true

capacity_requalification_attempted=true
capacity_requalification_successful=true

four_user_capacity_validated=true

four_user_rollback_safe=true

governance_safe_for_four_users=true

selected_moves_zero=true
hidden_movers_absent=true
runtime_checkers_ok=true

capacity_safe_for_4_users=true

small_cohort_readiness=GO

remaining_blockers=NONE

recommended_next_block=E28_2_FIRST_SMALL_COHORT_GOVERNED_MOVEMENT

## Final Mutation Statement

Runtime mutation performed: YES

If YES: only target capacity metadata/validation changes

User movement performed: NO

Routing mutation performed: NO

Kill switch control/toggle mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO

