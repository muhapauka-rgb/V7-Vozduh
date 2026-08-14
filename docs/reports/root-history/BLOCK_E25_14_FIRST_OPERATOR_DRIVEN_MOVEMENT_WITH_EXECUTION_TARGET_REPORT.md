# BLOCK E25.14 First Operator-Driven Movement With Execution Target Report

## Verdict

`e25_14_completed=true`

`first_operator_driven_movement_executed=false`

`candidate_user=10.7.0.11`

`forward_target=amneziawg-exec-20260528-10-8-1-14`

`rollback_target=1`

`forward_success=false`

`rollback_executed=false`

`rollback_success=false`

`only_approved_user_moved=true`

`routing_mutation_limited_to_candidate=true`

`delayed_movement_observed=false`

`replay_rejection_verified=false`

`runtime_checkers_ok=true`

`restore_settle_gate_status=GO`

`execution_governance_production_grade_for_one_user=true`

## Summary

E25.14 correctly stopped before the first real user movement.

The fresh execution-time recheck confirmed that the target was still `GO`, restore-settle was `GO`, selected moves were zero, hidden movers were absent, and runtime checkers were OK. However, the packet-bound `users.registry` hash no longer matched live runtime truth, so the movement was denied before mutation.

The detected drift was:

```text
packet_users_registry_hash=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
current_users_registry_hash=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
authorization_reasons=users_registry_hash_mismatch
```

The candidate and target were still clean:

```text
candidate_row=ip=10.7.0.11 current=1 table=1009 enabled=1
target_readiness=GO
restore_settle_gate_status=GO
selected_moves_count=0
hidden_movers_count=0
runtime_checkers_ok=true
target_users=0
```

The current registry contains an additional active user row that was not present in the packet-bound registry truth:

```text
ip=10.7.0.16 current=vless table=1014 enabled=1
```

This appears outside the approved `10.7.0.11` blast radius, but first real movement governance must fail closed on unexplained registry drift.

## Execution-Time Recheck

Fresh recheck result:

```text
packet_non_expired=true
packet_hash_expected=b5b9484ff1ccd1f78b3eded361dce38348327518f36c657c2ea3087a2dc2b939
packet_hash_actual=b5b9484ff1ccd1f78b3eded361dce38348327518f36c657c2ea3087a2dc2b939
approval_status=GO
gate_status=GO
execution_authorized=false
authorization_reasons=users_registry_hash_mismatch
```

Evidence:

- `docs/track7/productization/e25_14-evidence/execution-time-recheck.md`
- `docs/track7/productization/e25_14-evidence/final-execution-authorization.md`

## Forward Movement

The approved forward command was not executed:

```bash
v7-user-switch 10.7.0.11 amneziawg-exec-20260528-10-8-1-14
```

Result:

```text
forward_execution_attempted=false
forward_success=false
```

## Rollback

Rollback was not required and was not executed because no forward movement occurred:

```bash
v7-user-switch 10.7.0.11 1
```

Result:

```text
rollback_executed=false
rollback_not_required=true
candidate_still_on_1=true
```

## Post-Abort Safety

Final safety check:

```text
candidate_row=ip=10.7.0.11 current=1 table=1009 enabled=1
table_1009=default dev v7e356a192b79 scope link
target_users=0
selected_moves_count=0
hidden_movers_absent=true
v7_reconcile_check=OK
v7_user_route_check=OK
v7_killswitch_check=OK
v7_provisioning_reconcile_check=OK
gate_status=GO
```

No delayed movement was observed because no movement occurred.

## Replay Validation

`replay_rejection_verified=false`

True post-execution replay validation was not applicable because the packet was never executed and no success record was written.

`stale_packet_rejection_verified=true`

The same packet is denied before execution due to `users_registry_hash_mismatch`.

## Artifacts

- `docs/track7/productization/e25_14-evidence/execution-time-recheck.md`
- `docs/track7/productization/e25_14-evidence/final-execution-authorization.md`
- `docs/track7/productization/e25_14-evidence/forward-execution.md`
- `docs/track7/productization/e25_14-evidence/forward-verification.md`
- `docs/track7/productization/e25_14-evidence/observation-A.md`
- `docs/track7/productization/e25_14-evidence/observation-B.md`
- `docs/track7/productization/e25_14-evidence/observation-C.md`
- `docs/track7/productization/e25_14-evidence/rollback-execution.md`
- `docs/track7/productization/e25_14-evidence/rollback-verification.md`
- `docs/track7/productization/e25_14-evidence/post-rollback-restore-settle.md`
- `docs/track7/productization/e25_14-evidence/delayed-monitoring-A.md`
- `docs/track7/productization/e25_14-evidence/delayed-monitoring-B.md`
- `docs/track7/productization/e25_14-evidence/delayed-monitoring-C.md`
- `docs/track7/productization/e25_14-evidence/replay-validation.md`
- `docs/track7/productization/e25_14-evidence/tests.md`
- `docs/track7/productization/e25_14-evidence/recheck-readiness.json`
- `docs/track7/productization/e25_14-evidence/recheck-restore-settle.json`
- `docs/track7/productization/e25_14-evidence/recheck-settle-samples/`

## Tests

- py_compile relevant files: PASS
- targeted unit tests: PASS, `33 tests`
- full unittest discover: PASS, `119 tests`
- readiness/restore-settle/sample JSON validation: PASS
- runtime checkers: PASS
- hidden mover scan: PASS
- readiness helper: PASS
- restore-settle helper: PASS
- credential scan: PASS
- dangerous-call scan: PASS with expected documented fallback strings only
- `git diff --check`: PASS

## Remaining Blockers

`USERS_REGISTRY_HASH_DRIFT_AFTER_E25_13_PACKET`

`FRESH_APPROVAL_PACKET_REQUIRED_AFTER_REGISTRY_DRIFT`

`FIRST_REAL_MOVEMENT_NOT_EXECUTED`

`TRUE_REPLAY_REJECTION_NOT_VERIFIED_BECAUSE_PACKET_WAS_NOT_USED`

## Recommendation

`recommended_next_block=E25_15_REFRESH_APPROVAL_PACKET_AFTER_REGISTRY_DRIFT_AND_RETRY_MOVEMENT`

The next block should create a fresh packet against the current `users.registry` hash, explicitly account for the new `10.7.0.16` registry row as out-of-scope, then repeat execution-time recheck and attempt the same one-user movement only if all gates pass.

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation for users performed: NO

Kill switch control/toggle mutation performed: NO

Autoswitch apply performed manually: NO

Raw unsafe profile executed: NO

Canary performed: NO

Cohort performed: NO
