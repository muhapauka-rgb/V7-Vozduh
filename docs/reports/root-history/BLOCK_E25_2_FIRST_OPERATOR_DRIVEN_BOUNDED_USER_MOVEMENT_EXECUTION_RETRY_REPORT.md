# BLOCK E25.2 — First Operator-Driven Bounded User Movement Execution Retry Report

## Verdict

`first_operator_driven_bounded_user_movement_executed=false`

E25.2 correctly aborted before runtime mutation. The fresh execution-time target readiness gate returned NO-GO for the approved WireGuard target. No `v7-user-switch` command was executed.

## Final Answers

- `candidate_user=10.7.0.11`
- `forward_target=wireguard-1779454504-c43409`
- `rollback_target=1`
- `forward_success=false`
- `rollback_executed=false`
- `rollback_success=false`
- `only_approved_user_moved=true` because nobody moved
- `routing_mutation_limited_to_candidate=true` because no routing mutation occurred
- `delayed_movement_observed=false`
- `runtime_checkers_ok=true`
- `execution_governance_production_grade_for_one_user=false`
- `execution_allowed_now=false`

## Blocking Reason

`target_readiness_not_go`

Fresh VPS target readiness at execution time:

- `approval_status=NO-GO`
- `second_canary_readiness=NO-GO`
- `selected_target=NONE`
- WireGuard target users: `0`
- WireGuard load: `OK`
- WireGuard diagnose: `OK`
- WireGuard `min_mbps=4.61`, below floor `10.0`
- WireGuard `stability=0.297919` and `0.300861`, below floor `0.45`

This is classified as:

`REAL_TARGET_DEGRADATION_RECURRED`

E25.1 showed a recovery to GO, but E25.2 proved the target was not stable enough at execution time. The correct governance behavior was to abort before movement.

## Evidence Artifacts

- `docs/track7/productization/e25_2-evidence/pre-execution-recheck.md`
- `docs/track7/productization/e25_2-evidence/target-readiness-blocker-investigation.md`
- `docs/track7/productization/e25_2-evidence/final-execution-authorization.md`
- `docs/track7/productization/e25_2-evidence/forward-execution.md`
- `docs/track7/productization/e25_2-evidence/rollback-verification.md`
- `docs/track7/productization/e25_2-evidence/post-rollback-restore-settle.md`
- `docs/track7/productization/e25_2-evidence/delayed-monitoring-not-run.md`
- `docs/track7/productization/e25_2-evidence/tests.md`

## Pre-Execution Runtime State

VPS:

- hostname: `v3119922.hosted-by-vdsina.ru`
- timestamp: `2026-05-28T11:01:21Z`

Repo:

- branch: `Updatesystem`
- HEAD: `5de30074356771beef8d5b750415a38c78dbb28a`

Packet:

- packet id: `pkt_e25_1_first_bounded_user_move_10_7_0_11_20260528T103331Z`
- packet hash: `589aca11bdfa1c69db86e9d16d9a90f0588787d8ea5594f17486902f0ebf9829`
- packet expiry: `2026-05-28T12:33:31.168538+00:00`
- packet was not expired at execution-time recheck.

Registry hashes:

- `users.registry=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

Candidate row:

```text
ip=10.7.0.11 current=1 table=1009 enabled=1
```

Route table before execution:

```text
default dev v7e356a192b79 scope link
```

## Authorization Matrix

| Gate | Result |
|---|---:|
| Packet valid | PASS |
| Packet non-expired | PASS |
| Dual confirmation valid | PASS |
| Allowed users exact match | PASS |
| Allowed targets exact match | PASS |
| Movement budget = 1 | PASS |
| Candidate still on `1` | PASS |
| Selected moves = 0 | PASS |
| Hidden movers absent | PASS |
| Restore-settle GO | PASS |
| Runtime checkers OK | PASS |
| Blast radius = 1 user | PASS |
| Target readiness GO | FAIL |

Final authorization:

`execution_authorized=false`

## Forward Execution

`forward_executed=false`

The approved command was not run:

```text
v7-user-switch 10.7.0.11 wireguard-1779454504-c43409
```

## Rollback

`rollback_executed=false`

No rollback was required because no forward movement occurred. The rollback command was not run:

```text
v7-user-switch 10.7.0.11 1
```

## Post-Abort Safety Verification

Final no-mutation check at `2026-05-28T11:02:43Z`:

- `users.registry=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`
- `10.7.0.11` remained on `1`
- no users were on `wireguard-1779454504-c43409`
- hidden movers absent
- no runtime mutation observed

## Tests

- `py_compile`: PASS.
- targeted operator/helper tests: PASS, `26 tests`.
- full unittest discovery: PASS, `116 tests`.
- restore-settle helper: PASS, `GO`.
- packet JSON validation: PASS.
- runtime checkers: PASS.
- hidden mover scan: PASS.
- target readiness helper: FAIL as execution gate, causing safe abort.

## Remaining Execution Blockers

- `WIREGUARD_TARGET_READINESS_UNSTABLE`: the target moved from GO in E25.1 back to NO-GO in E25.2.
- `TARGET_QUALITY_BELOW_FLOOR`: `min_mbps=4.61` and stability around `0.30`.
- `MOVEMENT_PACKET_CONSUMER_NOT_CONNECTED_PRODUCTION_GRADE`: raw fallback remains prepared but was not reached because readiness failed.

## Recommended Next Block

`E25_3_WIREGUARD_TARGET_STABILITY_RECOVERY_OR_RETARGETING_FOR_FIRST_MOVEMENT`

Recommended scope:

- observe WireGuard target readiness over a longer stability window;
- decide whether to wait/recover, select a different zero-user target, or create a dedicated test egress;
- refresh packet only after target readiness is stable GO;
- do not run user movement until fresh target readiness is GO at execution time.

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Kill switch mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO
