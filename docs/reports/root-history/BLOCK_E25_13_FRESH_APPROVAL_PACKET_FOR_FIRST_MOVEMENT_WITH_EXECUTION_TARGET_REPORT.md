# BLOCK E25.13 Fresh Approval Packet For First Movement With Execution Target Report

## Verdict

`e25_13_completed=true`

`runtime_mutation_performed=false`

`runtime_mutation_scope=none; approval packet and evidence generated locally only`

`user_movement_performed=false`

`routing_mutation_for_users=false`

`candidate_user=10.7.0.11`

`candidate_still_on_1=true`

`execution_target=amneziawg-exec-20260528-10-8-1-14`

`execution_target_role=EXECUTION_ONLY`

`target_readiness_final_status=GO`

`target_connectivity_usable=true`

`sustained_go=true`

`selected_moves_zero=true`

`hidden_movers_absent=true`

`runtime_checkers_ok=true`

`restore_settle_gate_status=GO`

`fresh_approval_packet_created=true`

`packet_non_expired=true`

`replay_denial_semantics_valid=true`

`first_real_movement_authorizable=true`

## Summary

E25.13 created a fresh bounded movement approval packet for the first governed movement:

```text
10.7.0.11
1 -> amneziawg-exec-20260528-10-8-1-14
```

The packet is bounded to one user, one target, one rollback target, and one movement budget. It does not allow immediate execution and requires a fresh execution-time recheck in the next block.

## Fresh Runtime Truth

Fresh VPS snapshot:

```text
users_registry_hash=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
egress_registry_hash=43dbba0e138d9ee33556801640e15968cebe5b58e6866802e0538d98b72af380
candidate=ip=10.7.0.11 current=1 table=1009 enabled=1
route_table_1009=default dev v7e356a192b79 scope link
selected_moves_count=0
selected_moves_hash=NONE
hidden_movers_count=0
```

Runtime checkers:

```text
v7_reconcile_check=OK
v7_user_route_check=OK
v7_killswitch_check=OK
v7_provisioning_reconcile_check=OK
```

## Execution Target

```text
target=amneziawg-exec-20260528-10-8-1-14
interface=v7execwg0
protocol=amneziawg
role=EXECUTION_ONLY
target_users=0
autoswitch_allowed=false
rebalance_allowed=false
production_assignment_allowed=false
```

Readiness:

```text
selected_target=amneziawg-exec-20260528-10-8-1-14
approval_status=GO
execution_allowed_now=False
avg_mbps=27.12
min_mbps=10.67
stability=1.000
```

Restore-settle:

```text
gate_status=GO
sample_count=3
samples_span_seconds=47
apply_timer_intervals_covered=2.35
selected_moves_by_sample=[0, 0, 0]
checkers_ok=True
hidden_movers_observed=False
```

## Approval Packet

Packet:

- `docs/track7/productization/e25_13-evidence/fresh-approval-packet.json`
- `docs/track7/productization/e25_13-evidence/fresh-approval-packet.md`

Packet identifiers:

```text
packet_id=packet-6cda2c9e4c42133eedfebd5b
approval_id=approval-563b285df7f4429eaa3ed9ee
operation_id=e25-13-first-movement-20260528T181217Z
packet_hash=b5b9484ff1ccd1f78b3eded361dce38348327518f36c657c2ea3087a2dc2b939
```

Boundaries:

```text
runtime_action=BOUNDED_USER_MOVEMENT
execution_method=APPROVED_RAW_FALLBACK_PREPARED
ui_execution_allowed=false
execution_allowed_now=false
movement_budget=1
allowed_users=["10.7.0.11"]
allowed_targets=["amneziawg-exec-20260528-10-8-1-14"]
rollback_target=1
blast_radius=1 user
```

Approved raw fallback for the next execution block only:

```bash
v7-user-switch 10.7.0.11 amneziawg-exec-20260528-10-8-1-14
```

Rollback:

```bash
v7-user-switch 10.7.0.11 1
```

These commands were not executed in E25.13.

## Recheck Contract

Created:

`docs/track7/productization/e25_13-evidence/execution-time-recheck-contract.md`

The next block must deny execution unless a fresh runtime recheck confirms:

- packet not expired;
- packet not replayed;
- candidate still on `1`;
- target still `GO`;
- selected moves remain `0`;
- hidden movers absent;
- runtime checkers OK;
- restore-settle `GO`;
- target remains `EXECUTION_ONLY`;
- target remains zero-user before movement;
- movement budget remains exactly `1`;
- allowed user/target sets remain exact.

## Replay / Denial Tests

`replay_denial_semantics_valid=true`

Denied cases tested:

- expired packet
- unauthorized user
- unauthorized target
- movement budget greater than `1`
- stale users hash
- stale egress hash
- stale selected-move hash
- execution target not `GO`
- execution target not execution-only
- autoswitch exclusion missing
- missing second confirmation
- wrong generation
- replay attempt

## Artifacts

- `docs/track7/productization/e25_13-evidence/fresh-runtime-snapshot.md`
- `docs/track7/productization/e25_13-evidence/execution-target-validation.md`
- `docs/track7/productization/e25_13-evidence/fresh-approval-packet.json`
- `docs/track7/productization/e25_13-evidence/fresh-approval-packet.md`
- `docs/track7/productization/e25_13-evidence/execution-time-recheck-contract.md`
- `docs/track7/productization/e25_13-evidence/replay-denial-tests.md`
- `docs/track7/productization/e25_13-evidence/governance-safety-validation.md`
- `docs/track7/productization/e25_13-evidence/tests.md`
- `docs/track7/productization/e25_13-evidence/readiness.json`
- `docs/track7/productization/e25_13-evidence/readiness.pretty`
- `docs/track7/productization/e25_13-evidence/restore-settle.json`
- `docs/track7/productization/e25_13-evidence/restore-settle.pretty`
- `docs/track7/productization/e25_13-evidence/restore-settle-samples/`

## Tests

- py_compile relevant files: PASS
- targeted unit tests: PASS, `33 tests`
- full unittest discover: PASS, `119 tests`
- packet/readiness/restore-settle JSON validation: PASS
- replay/denial semantic tests: PASS, `13 cases`
- runtime checkers: PASS
- hidden mover scan: PASS
- restore-settle helper: PASS
- readiness helper: PASS
- credential scan: PASS
- dangerous-call scan: PASS with expected documented next-block fallback strings only
- `git diff --check`: PASS

## Remaining Blockers

`ACTUAL_USER_MOVEMENT_NOT_EXECUTED`

`FRESH_EXECUTION_TIME_RECHECK_REQUIRED_IN_NEXT_BLOCK`

`RAW_FALLBACK_EXECUTION_ONLY; MOVEMENT_PACKET_CONSUMER_STILL_NOT_CONNECTED`

## Recommendation

`recommended_next_block=E25_14_FIRST_OPERATOR_DRIVEN_MOVEMENT_WITH_EXECUTION_TARGET`

E25.14 may attempt the first governed movement only after fresh execution-time recheck. E25.13 does not authorize immediate execution.

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation for users performed: NO

Kill switch control/toggle mutation performed: NO

Autoswitch apply performed manually: NO

Raw unsafe profile executed: NO

Canary performed: NO

Cohort performed: NO
