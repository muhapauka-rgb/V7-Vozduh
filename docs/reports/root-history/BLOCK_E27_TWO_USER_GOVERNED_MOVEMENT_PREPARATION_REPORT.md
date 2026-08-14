# BLOCK E27 Two User Governed Movement Preparation Report

## Verdict

`e27_completed=true`

`runtime_mutation_performed=false`

`one_user_governed_execution_certified=true`

`two_user_readiness=NO-GO`

`candidate_user_A=10.7.0.11`

`candidate_user_B=10.7.0.12`

`capacity_safe_for_two_users=false`

`two_user_rollback_safe=true`

`audit_scales_to_two_users=true`

`delayed_movement_protection_scales=true`

## Summary

E27 completed the read-only preparation review for the first bounded two-user governed movement.

Two eligible users were found:

```text
10.7.0.11 current=1 table=1009 enabled=1
10.7.0.12 current=1 table=1010 enabled=1
```

Both users are stable, enabled, on rollback target `1`, and have sane route tables through `v7e356a192b79`.

However, the current execution target is still declared as one-user capacity:

```text
target=amneziawg-exec-20260528-10-8-1-14
role=EXECUTION_ONLY
soft_limit=1
hard_limit=1
target_users=0
```

Because a two-user movement requires `movement_budget=2`, using this target would exceed `hard_limit=1`. E27 therefore returns `NO-GO` for execution readiness.

## Runtime Snapshot

Fresh runtime state:

```text
users_registry_hash=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
egress_registry_hash=43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380
selected_moves_count=0
hidden_movers_absent=true
runtime_checkers_ok=true
```

Execution target readiness remains GO for one-user explicit target mode:

```text
approval_status=GO
second_canary_readiness=GO
avg_mbps=27.12
min_mbps=10.67
stability=1.0
diagnose=OK
```

This does not override `hard_limit=1`.

## Restore-Settle

Fresh E27 restore-settle window:

```text
gate_status=GO
sample_count=3
samples_span_seconds=56
apply_timer_intervals_covered=2.8
selected_moves_by_sample=[0, 0, 0]
registry_stable=true
egress_registry_stable=true
checkers_ok=true
hidden_movers_observed=false
```

## Blast Radius Model

Modeled forward action:

```text
10.7.0.11: 1 -> amneziawg-exec-20260528-10-8-1-14
10.7.0.12: 1 -> amneziawg-exec-20260528-10-8-1-14
```

Expected blast radius:

```text
blast_radius=2
allowed_users=["10.7.0.11","10.7.0.12"]
allowed_targets=["amneziawg-exec-20260528-10-8-1-14"]
```

Only route tables `1009` and `1010` would be allowed to change in a future execution block.

## Rollback Model

Rollback manifest:

```text
10.7.0.11 -> 1
10.7.0.12 -> 1
```

`two_user_rollback_safe=true` as a model verdict because both candidates currently start on rollback target `1` and route through the expected device. This is not an execution proof.

## Audit And Replay Model

`audit_scales_to_two_users=true`

`replay_model_scales_to_two_users=true`

Required future semantics:

- one packet with `movement_budget=2`;
- exact allowed users list;
- exact allowed target list;
- packet consumed after first forward execution attempt;
- replay denied if any forward record exists for that packet lineage;
- rollback records must cover both users.

## Delayed Movement Model

`delayed_movement_protection_scales=true`

The model scales if future execution captures both users in forward observation, rollback verification, post-rollback restore-settle, and delayed monitoring while continuing to enforce selected_moves=0 and hidden movers absent.

## Remaining Blockers

```text
EXECUTION_TARGET_CAPACITY_LIMIT_ONE_USER
```

The current target is certified for one-user governed movement, not two-user movement.

Required before execution:

- requalify `amneziawg-exec-20260528-10-8-1-14` with `hard_limit>=2` and sustained two-user capacity evidence; or
- prepare a different execution-only target with capacity `>=2`.

Do not generate or execute a two-user movement approval packet until this is resolved.

## Artifacts

- `docs/track7/productization/e27-evidence/fresh-runtime-snapshot.md`
- `docs/track7/productization/e27-evidence/user-eligibility.md`
- `docs/track7/productization/e27-evidence/target-capacity-review.md`
- `docs/track7/productization/e27-evidence/blast-radius-review.md`
- `docs/track7/productization/e27-evidence/rollback-model.md`
- `docs/track7/productization/e27-evidence/audit-replay-model.md`
- `docs/track7/productization/e27-evidence/delayed-movement-model.md`
- `docs/track7/productization/e27-evidence/readiness-decision.md`
- `docs/track7/productization/e27-evidence/restore-settle-samples/`
- `docs/track7/productization/e27-evidence/tests.md`

## Tests

- `PYTHONPYCACHEPREFIX=.pycache python3 -m compileall admin_core tools tests`: PASS
- `PYTHONPYCACHEPREFIX=.pycache python3 -m unittest tests.unit.test_operator_execution_packet tests.unit.test_v7_second_canary_target_readiness`: PASS, 20 tests
- `python3 -m unittest discover`: PASS, 119 tests
- Runtime checkers: PASS
- Hidden mover scan: PASS
- Readiness helper: PASS for one-user target mode
- Restore-settle helper: PASS
- Audit validation/model review: PASS
- Credential scan: PASS
- Dangerous-call scan: PASS with expected hidden-mover scan text reference only
- `git diff --check`: PASS

## Recommended Next Block

`recommended_next_block=E27_1_TWO_USER_EXECUTION_TARGET_CAPACITY_PREPARATION`

The expected execution block `E27_1_FIRST_TWO_USER_GOVERNED_MOVEMENT` should wait until target capacity is proven for two users.

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO

