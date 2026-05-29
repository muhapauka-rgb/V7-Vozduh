# BLOCK E25.15 Refresh Approval Packet After Registry Drift And Retry Movement Report

## Verdict

`e25_15_completed=true`

`registry_drift_classified=true`

`drift_user=10.7.0.16`

`drift_user_out_of_scope=true`

`unsafe_registry_drift=false`

`fresh_approval_packet_created=true`

`execution_authorized=true`

`first_operator_driven_movement_executed=true`

`candidate_user=10.7.0.11`

`forward_target=amneziawg-exec-20260528-10-8-1-14`

`rollback_target=1`

`forward_success=true`

`rollback_executed=true`

`rollback_success=true`

`only_approved_user_moved=true`

`out_of_scope_user_10_7_0_16_unchanged=true`

`routing_mutation_limited_to_candidate=true`

`delayed_movement_observed=false`

`replay_rejection_verified=true`

`runtime_checkers_ok=true`

`restore_settle_gate_status=GO`

`execution_governance_production_grade_for_one_user=true`

## Summary

E25.15 completed the first real governed one-user movement and default rollback.

The E25.14 registry drift was classified as safe and out-of-scope:

```text
ip=10.7.0.16 current=vless table=1014 enabled=1
```

The drift user remained on `vless` through the full block and was not touched.

Fresh packet was created against the current registry hash:

```text
packet_id=packet-0671c44ea5024978724e11e9
users_registry_hash=f4e6bc1a4daa07e463019817a958a0050d69c97591c31f55f0ed1d61e2042042
egress_registry_hash=43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380
```

Execution-time recheck passed, then the approved forward movement executed:

```bash
v7-user-switch 10.7.0.11 amneziawg-exec-20260528-10-8-1-14
```

Default rollback then executed:

```bash
v7-user-switch 10.7.0.11 1
```

## Forward Movement

Forward result:

```text
exit_code=0
candidate_before=ip=10.7.0.11 current=1 table=1009 enabled=1
candidate_after=ip=10.7.0.11 current=amneziawg-exec-20260528-10-8-1-14 table=1009 enabled=1
target_users_before=0
target_users_after=1
route_table_1009_before=default dev v7e356a192b79 scope link
route_table_1009_after=default dev v7execwg0 scope link
```

Only the candidate row changed in `users.registry`.

## Forward Observation

Three observation samples confirmed:

- `10.7.0.11` remained on the execution target;
- `10.7.0.16` remained on `vless`;
- target users stayed `1`;
- selected moves stayed `0`;
- hidden movers stayed absent;
- runtime checkers stayed OK.

The readiness helper returned `NO-GO` during forward observation because the target was occupied by the test user, which is expected after movement and before rollback.

## Rollback

Rollback result:

```text
exit_code=0
candidate_before=ip=10.7.0.11 current=amneziawg-exec-20260528-10-8-1-14 table=1009 enabled=1
candidate_after=ip=10.7.0.11 current=1 table=1009 enabled=1
target_users_before=1
target_users_after=0
route_table_1009_before=default dev v7execwg0 scope link
route_table_1009_after=default dev v7e356a192b79 scope link
```

Rollback verification:

```text
rollback_success=true
out_of_scope_user_10_7_0_16_unchanged=true
target_users_restored=true
route_table_1009_restored=true
selected_moves_zero=true
hidden_movers_absent=true
runtime_checkers_ok=true
```

## Post-Rollback Settle

Fresh restore-settle:

```text
gate_status=GO
sample_count=3
selected_moves_by_sample=[0, 0, 0]
registry_stable=True
egress_registry_stable=True
checkers_ok=True
hidden_movers_observed=False
```

## Delayed Monitoring

Delayed samples A/B/C confirmed:

- candidate back on `1`;
- `10.7.0.16` unchanged on `vless`;
- target users `0`;
- selected moves `0`;
- hidden movers absent;
- runtime checkers OK;
- delayed movement observed `false`;
- routing drift `false`.

## Replay Validation

Replay validation result:

```text
packet_id=packet-0671c44ea5024978724e11e9
used_forward_records=1
verdict=DENY_REPLAY
reason=packet_id_already_has_forward_movement_record
movement_executed_during_replay=false
routing_mutation_during_replay=false
```

## Audit Records

Forward audit record:

```text
record_hash=f4fd62bec6fff288d951876f6dfd62be3ff19a209e486998c0df022900bc4537
event=forward_movement
```

Rollback audit record:

```text
record_hash=792c6d82b6d8ced4b96b68b1562fd2bde601cb0e6af91c37a07f54295e9865c1
event=rollback_movement
```

Replay denial audit record:

```text
record_hash=c105e00b2eed112271f87b337b5375185672a53fd3687dc351eb687e70b20e55
event=replay_validation
verdict=DENY_REPLAY
```

## Artifacts

- `docs/track7/productization/e25_15-evidence/registry-drift-classification.md`
- `docs/track7/productization/e25_15-evidence/fresh-runtime-snapshot.md`
- `docs/track7/productization/e25_15-evidence/fresh-approval-packet.json`
- `docs/track7/productization/e25_15-evidence/fresh-approval-packet.md`
- `docs/track7/productization/e25_15-evidence/execution-time-recheck.md`
- `docs/track7/productization/e25_15-evidence/forward-execution.md`
- `docs/track7/productization/e25_15-evidence/forward-verification.md`
- `docs/track7/productization/e25_15-evidence/observation-A.md`
- `docs/track7/productization/e25_15-evidence/observation-B.md`
- `docs/track7/productization/e25_15-evidence/observation-C.md`
- `docs/track7/productization/e25_15-evidence/rollback-execution.md`
- `docs/track7/productization/e25_15-evidence/rollback-verification.md`
- `docs/track7/productization/e25_15-evidence/post-rollback-restore-settle.md`
- `docs/track7/productization/e25_15-evidence/delayed-monitoring-A.md`
- `docs/track7/productization/e25_15-evidence/delayed-monitoring-B.md`
- `docs/track7/productization/e25_15-evidence/delayed-monitoring-C.md`
- `docs/track7/productization/e25_15-evidence/replay-validation.md`
- `docs/track7/productization/e25_15-evidence/tests.md`

## Tests

- py_compile relevant files: PASS
- targeted unit tests: PASS, `33 tests`
- full unittest discover: PASS, `119 tests`
- packet/readiness/restore-settle/sample JSON validation: PASS
- runtime checkers: PASS
- hidden mover scan: PASS
- readiness helper: PASS
- restore-settle helper: PASS
- credential scan: PASS
- dangerous-call scan: PASS with expected approved E25.15 movement/rollback references only
- `git diff --check`: PASS

## Remaining Blockers

None for one-user governed execution proof.

The movement packet consumer remains raw-fallback based; productization can later replace raw fallback with a fully connected movement-capable packet consumer.

## Recommendation

`recommended_next_block=E26_POST_MOVEMENT_GOVERNANCE_REVIEW`

## Final Mutation Statement

Runtime mutation performed: YES

If YES: only fresh packet generation, approved forward movement, approved rollback, and append-only audit records.

User movement performed: YES

If YES: only `10.7.0.11` forward and rollback.

Routing mutation for users performed: YES

If YES: only `10.7.0.11` route table `1009`.

Kill switch control/toggle mutation performed: NO

Autoswitch apply performed manually: NO

Raw unsafe profile executed: NO

Canary performed: NO

Cohort performed: NO
