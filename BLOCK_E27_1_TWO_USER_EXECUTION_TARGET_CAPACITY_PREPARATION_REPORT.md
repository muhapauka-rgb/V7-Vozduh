# BLOCK E27.1 Two User Execution Target Capacity Preparation Report

## Verdict

`e27_1_completed=true`

`runtime_mutation_performed=true`

`runtime_mutation_scope=target capacity metadata only`

`user_movement_performed=false`

`routing_mutation_for_users=false`

`candidate_user_A=10.7.0.11`

`candidate_user_B=10.7.0.12`

`target_name=amneziawg-exec-20260528-10-8-1-14`

`capacity_limit_root_cause=GOVERNANCE_LIMIT_ONLY_WITH_METADATA_DRIFT`

`soft_limit_final=2`

`hard_limit_final=2`

`capacity_model_safe=true`

`capacity_requalification_attempted=true`

`capacity_requalification_successful=true`

`two_user_capacity_validated=true`

`two_user_rollback_safe=true`

`governance_safe_for_two_users=true`

`selected_moves_zero=true`

`hidden_movers_absent=true`

`runtime_checkers_ok=true`

`two_user_readiness=GO`

## Summary

E27.1 resolved the E27 capacity blocker for the execution-only target.

The previous blocker was:

```text
EXECUTION_TARGET_CAPACITY_LIMIT_ONE_USER
soft_limit=1
hard_limit=1
```

Investigation showed this was not a real throughput or stability limit. Runtime load state already modeled the execution target with `hard_limit=2`, and fresh target quality had strong headroom.

After target-local validation, E27.1 performed the only runtime mutation in this block:

```text
amneziawg-exec-20260528-10-8-1-14:
soft_limit=1 hard_limit=1 -> soft_limit=2 hard_limit=2
```

No users moved. No user route tables changed.

## Capacity Evidence

Fresh quality state before requalification:

```text
avg_mbps=65.7833
min_mbps=55.30
stability=0.840639
samples=30
```

Target-local parallel 5MB validation:

```text
probe_count=10
avg_mbps=38.192
min_mbps=13.02
all_samples_above_10=true
```

Post-requalification 20-sample long-window:

```text
sample_count=20
avg_mbps=68.561
min_mbps=19.037
max_mbps=99.305
no_sample_below_floor=true
readiness_all_go=true
selected_moves_zero=true
hidden_movers_absent=true
runtime_checkers_ok=true
target_users_zero=true
users_registry_stable=true
egress_registry_stable=true
two_user_capacity_validated=true
```

Fresh restore-settle after requalification:

```text
gate_status=GO
sample_count=3
samples_span_seconds=59
apply_timer_intervals_covered=2.95
selected_moves_by_sample=[0, 0, 0]
checkers_ok=true
hidden_movers_observed=false
```

## Requalification

Backup:

```text
/opt/v7/egress/state/e27_1-backups/egress.registry.20260528T214002Z
```

Before:

```text
egress_registry_hash=43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380
soft_limit=1
hard_limit=1
```

After:

```text
egress_registry_hash=13ae747486e30b4ad527c28343529f580fc400867981557845708c34385dd4ed
soft_limit=2
hard_limit=2
```

Only the execution target metadata row changed.

## Candidate Pair

```text
candidate_user_A=10.7.0.11 current=1 table=1009 enabled=1
candidate_user_B=10.7.0.12 current=1 table=1010 enabled=1
```

Both candidates remained on `1` throughout E27.1.

## Rollback Model

Rollback manifest:

```text
10.7.0.11 -> 1
10.7.0.12 -> 1
```

`two_user_rollback_safe=true`

The actual rollback proof remains for the execution block.

## Governance Review

Governance remained safe for two-user preparation:

```text
blast_radius=2
autoswitch_allowed=false
rebalance_allowed=false
production_assignment_allowed=false
selected_moves=0
hidden_movers_absent=true
runtime_checkers_ok=true
```

## Artifacts

- `docs/track7/productization/e27_1-evidence/capacity-snapshot.md`
- `docs/track7/productization/e27_1-evidence/limit-root-cause-review.md`
- `docs/track7/productization/e27_1-evidence/two-user-target-local-probe.md`
- `docs/track7/productization/e27_1-evidence/two-user-target-local-probe-5mb.md`
- `docs/track7/productization/e27_1-evidence/two-user-capacity-model.md`
- `docs/track7/productization/e27_1-evidence/capacity-requalification.md`
- `docs/track7/productization/e27_1-evidence/long-window-validation.md`
- `docs/track7/productization/e27_1-evidence/long-window/`
- `docs/track7/productization/e27_1-evidence/two-user-rollback-model.md`
- `docs/track7/productization/e27_1-evidence/governance-review.md`
- `docs/track7/productization/e27_1-evidence/restore-settle-samples/`
- `docs/track7/productization/e27_1-evidence/tests.md`

## Tests

- `PYTHONPYCACHEPREFIX=.pycache python3 -m compileall admin_core tools tests`: PASS
- `PYTHONPYCACHEPREFIX=.pycache python3 -m unittest tests.unit.test_operator_execution_packet tests.unit.test_v7_second_canary_target_readiness`: PASS, 20 tests
- `python3 -m unittest discover`: PASS, 119 tests
- Runtime checkers: PASS
- Hidden mover scan: PASS
- Readiness helper: PASS
- Restore-settle helper: PASS
- Target-local capacity probes: PASS
- Credential scan: PASS
- Dangerous-call scan: PASS with expected hidden-mover scan text reference only
- `git diff --check`: PASS

## Remaining Blockers

None for two-user target capacity preparation.

This block does not execute movement. A fresh two-user approval packet and fresh execution-time recheck are still required before any movement.

## Recommended Next Block

`recommended_next_block=E27_2_FIRST_TWO_USER_GOVERNED_MOVEMENT`

## Final Mutation Statement

Runtime mutation performed: YES

If YES: only target capacity metadata/validation changes for `amneziawg-exec-20260528-10-8-1-14`.

User movement performed: NO

Routing mutation for users performed: NO

Kill switch control/toggle mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO

