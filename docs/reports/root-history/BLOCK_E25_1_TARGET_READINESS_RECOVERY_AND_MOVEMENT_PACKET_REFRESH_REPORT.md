# BLOCK E25.1 — Target Readiness Recovery and Movement Packet Refresh Report

## Verdict

`e25_1_completed=true`

`ready_for_e25_2_execution_retry=true`

E25.1 recovered the E25 blockers without moving users or mutating routing. WireGuard readiness recovered to GO, restore-settle was revalidated with fresh samples, a new non-expired movement packet was created, and an E25.2-only raw fallback path was prepared because the current packet consumer remains zero-movement only.

Execution remains forbidden now.

## Final Answers

- `runtime_mutation_performed=false`
- `user_movement_performed=false`
- `routing_mutation_performed=false`
- `candidate_user=10.7.0.11`
- `candidate_still_on_1=true`
- `forward_target=wireguard-1779454504-c43409`
- `rollback_target=1`
- `target_readiness_recovered_to_go=true`
- `target_readiness_final_status=GO`
- `readiness_root_cause=REAL_TARGET_DEGRADATION_TRANSIENT_RECOVERED`
- `fresh_movement_packet_created=true`
- `fresh_movement_packet_non_expired=true`
- `movement_packet_consumer_connected=false`
- `approved_raw_switch_fallback_prepared=true`
- `restore_settle_gate_status=GO`
- `selected_moves_zero=true`
- `hidden_movers_absent=true`
- `runtime_checkers_ok=true`
- `recommended_next_block=E25_2_FIRST_OPERATOR_DRIVEN_BOUNDED_USER_MOVEMENT_EXECUTION_RETRY`

## Evidence Artifacts

- `docs/track7/productization/e25_1-evidence/e25-intake.md`
- `docs/track7/productization/e25_1-evidence/live-runtime-safety-snapshot.md`
- `docs/track7/productization/e25_1-evidence/target-readiness-root-cause.md`
- `docs/track7/productization/e25_1-evidence/readiness-recovery.md`
- `docs/track7/productization/e25_1-evidence/restore-settle-samples/sample-01.json`
- `docs/track7/productization/e25_1-evidence/restore-settle-samples/sample-02.json`
- `docs/track7/productization/e25_1-evidence/restore-settle-samples/sample-03.json`
- `docs/track7/productization/e25_1-evidence/restore-settle-revalidation.md`
- `docs/track7/productization/e25_1-evidence/restore-settle-revalidation.json`
- `docs/track7/productization/e25_1-evidence/fresh-movement-approval-packet.json`
- `docs/track7/productization/e25_1-evidence/fresh-movement-approval-packet.md`
- `docs/track7/productization/e25_1-evidence/execution-path-decision.md`
- `docs/track7/productization/e25_1-evidence/packet-denial-tests.md`
- `docs/track7/productization/e25_1-evidence/final-safety-confirmation.md`
- `docs/track7/productization/e25_1-evidence/tests-and-safety-checks.md`

## E25 Intake

E25 stopped correctly before mutation. The blockers were:

1. `target_readiness_not_go`: WireGuard stability was below floor `0.45` with observed values `0.422735`, `0.431723`, `0.438413`.
2. `approval_packet_expired`: E24 packet expired at `2026-05-28T09:22:47.888963+00:00`.
3. `movement_packet_consumer_not_connected`: `tools/v7-operator-execution-packet` is intentionally zero-movement only.

Clean state preserved from E25:

- `10.7.0.11` stayed on `1`.
- registry hashes unchanged.
- `selected_moves=0`.
- hidden movers absent.
- restore-settle GO.
- runtime checkers OK.
- no user movement.
- no routing mutation.

## Live Runtime Baseline

Collected from VPS:

- hostname: `v3119922.hosted-by-vdsina.ru`
- `users.registry=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`
- candidate row: `ip=10.7.0.11 current=1 table=1009 enabled=1`
- candidate route table: `default dev v7e356a192b79 scope link`
- candidate `route_get`: `8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009`
- WireGuard target users: `0`
- selected-move files: absent, interpreted as zero selected moves
- runtime checkers: OK

## Readiness Root Cause

Classification:

`REAL_TARGET_DEGRADATION_TRANSIENT_RECOVERED`

The E25 NO-GO was not hidden by threshold relaxation. E25.1 found the target had naturally recovered:

- `v7-second-canary-target-readiness` returned `GO`.
- WireGuard target remained zero-user.
- load OK.
- diagnose OK.
- interface up/lower-up.
- stability recovered above the `0.45` floor.
- latest final safety check saw WireGuard stability `0.830617`.

No helper threshold was weakened. No helper fix was applied.

## Restore-Settle Revalidation

Fresh E25.1 samples:

- sample 1: `2026-05-28T10:34:05.349211+00:00`
- sample 2: `2026-05-28T10:35:12.098821+00:00`
- sample 3: `2026-05-28T10:35:48.041558+00:00`

Gate output:

- `gate_status=GO`
- `sample_count=3`
- `samples_span_seconds=102`
- `apply_timer_intervals_covered=5.1`
- `selected_moves_by_sample=[0,0,0]`
- registry stable: true
- egress registry stable: true
- runtime checkers OK: true
- hidden movers observed: false

## Fresh Packet

Created:

`docs/track7/productization/e25_1-evidence/fresh-movement-approval-packet.json`

Packet summary:

- `packet_id=pkt_e25_1_first_bounded_user_move_10_7_0_11_20260528T103331Z`
- `approval_id=appr_e25_1_first_bounded_user_move_10_7_0_11_20260528T103331Z`
- created: `2026-05-28T10:33:31.168538+00:00`
- expires: `2026-05-28T12:33:31.168538+00:00`
- `runtime_action=BOUNDED_USER_MOVEMENT`
- `execution_method=APPROVED_RAW_FALLBACK_PREPARED`
- `ui_execution_allowed=false`
- `execution_allowed_now=false`
- `candidate_user=10.7.0.11`
- `from_egress=1`
- `to_egress=wireguard-1779454504-c43409`
- `rollback_target=1`
- `movement_budget=1`
- `allowed_users=["10.7.0.11"]`
- `allowed_targets=["wireguard-1779454504-c43409"]`
- `target_readiness_status=GO`
- `restore_settle_gate_status=GO`

Hashes:

- `fresh_users_registry_hash=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `fresh_egress_registry_hash=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`
- `live_selected_moves_hash=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- `selected_move_hash=8e643a26d0645043a20c28a8037cef50416a48c3ae0587e8d0d2453fb822e785`
- `runtime_snapshot_hash=c5f58e490844e1ddb8cb29ba143a26a1479a45fc94cf08140ffb0931f199b2d5`

## Execution Path Decision

`movement_packet_consumer_connected=false`

`approved_raw_switch_fallback_prepared=true`

The zero-move packet consumer remains unchanged. It was not extended to invoke movement in this recovery block.

The only approved E25.2 fallback commands are:

Forward:

```text
v7-user-switch 10.7.0.11 wireguard-1779454504-c43409
```

Rollback:

```text
v7-user-switch 10.7.0.11 1
```

These commands are not approved for E25.1 and were not executed.

## Denial Tests

Movement packet denial validation passed for:

- expired packet
- unauthorized user
- unauthorized target
- movement budget `2`
- stale users registry hash
- stale egress registry hash
- stale selected-move hash
- missing second confirmation
- wrong generation
- UI execution enabled
- autoswitch apply allowed
- kill switch mutation allowed

An initial harness gap around wrong-generation denial was found and corrected in the test harness. The corrected matrix passed. No runtime state was touched.

## Test Summary

- JSON validation: PASS.
- `py_compile`: PASS.
- target readiness helper pretty/json: PASS.
- restore-settle helper pretty/json: PASS.
- targeted unit tests: PASS, `26 tests`.
- full unit suite: PASS, `116 tests`.
- credential scan: PASS.
- dangerous-call scan: PASS with expected documentation-only `v7-user-switch` strings.
- `git diff --check`: PASS.

Unavailable/not applicable:

- Endpoint inventory: not run because no routes were changed.
- Static `/admin-v2` smoke: not run because no UI was changed.
- Audit chain validation: not applicable because no audit records were written.

## Residual Blockers

- `MOVEMENT_PACKET_CONSUMER_NOT_CONNECTED_PRODUCTION_GRADE`: E25.2 must use the explicitly approved raw fallback unless a movement-capable consumer is implemented in a separate block.
- `FRESH_E25_2_EXECUTION_TIME_RECHECK_REQUIRED`: readiness and restore-settle must be checked again immediately before movement.
- `UI_EXECUTION_DISABLED`: expected and required.

## Recommendation

Proceed to:

`E25_2_FIRST_OPERATOR_DRIVEN_BOUNDED_USER_MOVEMENT_EXECUTION_RETRY`

E25.2 must begin with a fresh live runtime recheck and abort on any drift.

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Kill switch mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO
