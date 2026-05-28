# BLOCK E25 First Operator-Driven Bounded User Movement Execution Report

Date: 2026-05-28

## Executive Verdict

`first_operator_driven_bounded_user_movement_executed=false`

E25 did not execute the approved movement. The block stopped correctly before runtime mutation because the fresh pre-execution gates failed.

Hard blockers:

1. `target_readiness_not_go`
   - `v7-second-canary-target-readiness` returned `NO-GO`.
   - WireGuard was clean and zero-user, but `stability.state` stayed below the required `0.45` floor.
2. `approval_packet_expired`
   - E24 packet expired at `2026-05-28T09:22:47.888963+00:00`.
3. `movement_packet_consumer_not_connected`
   - current `tools/v7-operator-execution-packet` supports zero-move governance packets only.
   - it rejects E24 movement packet shape and nonzero movement budget by design.
   - VPS also does not have `v7-operator-execution-packet` in PATH.

No user movement was performed.
No routing mutation was performed.
No rollback was needed.

## Pre-Execution Live Snapshot

Evidence:

- `docs/track7/productization/e25-evidence/pre-execution-live-snapshot.md`

Runtime:

- `hostname=v3119922.hosted-by-vdsina.ru`
- initial timestamp: `2026-05-28T10:16:05Z`

Registry hashes:

- `users.registry=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

Candidate:

- `10.7.0.11 current=1 table=1009 enabled=1`
- route table: `default dev v7e356a192b79`
- route_get: `8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009`

Target:

- `wireguard-1779454504-c43409`
- users count: `0`
- load status: `OK`
- diagnose: `OK`
- readiness helper status: `NO-GO`

## Target Readiness Investigation

Readiness samples:

- `2026-05-28T10:16:05Z`: WireGuard stability `0.422735`, NO-GO.
- `2026-05-28T10:17:08Z`: WireGuard stability `0.431723`, NO-GO.
- `2026-05-28T10:18:43Z`: WireGuard stability `0.438413`, NO-GO.

Required floor:

- `stability >= 0.45`

Direct source divergence:

- `stability.state` remained below floor.
- `egress-quality-summary.json` showed more favorable 5m/1h stability.

Operational decision:

- E25 honors `v7-second-canary-target-readiness` as the movement-critical gate from E24.1/E24.2.
- Movement is forbidden while that helper returns `NO-GO`.

## Restore-Settle Gate

Evidence:

- `docs/track7/productization/e24_2-evidence/restore-settle-samples/`
- `docs/track7/productization/e25-evidence/tests-and-safety-checks.md`

Result:

- `gate_status=GO`
- `sample_count=3`
- `apply_timer_intervals_covered=5.75`
- `selected_moves_by_sample=[0,0,0]`
- `registry_stable=true`
- `checkers_ok=true`
- `hidden_movers_observed=false`

Restore-settle was not the blocker.

## Execution-Time Recheck

Evidence:

- `docs/track7/productization/e25-evidence/execution-time-recheck.md`
- `docs/track7/productization/e25-evidence/execution-time-recheck.json`

Local packet consumer result:

- verdict: `DENY_PACKET_INVALID`
- record written: `false`
- runtime action performed: `false`

Errors:

- `schema_version_invalid`
- `unsupported_action`
- `runtime_action_not_allowed`
- `selected_move_budget_not_zero`
- `user_movement_not_forbidden`
- `routing_mutation_not_forbidden`
- `approval_expired`
- `selected_move_hash_invalid_for_zero_budget`
- `generation_id_missing`

Interpretation:

- current packet consumer is fail-closed and zero-move only.
- fallback raw movement could not be justified because target readiness was also NO-GO and packet expired.

## Hold Window

Evidence:

- `docs/track7/productization/e25-evidence/hold-window.md`

Observed:

- planner timer inactive
- apply timer inactive
- hidden movers absent

No timer hold mutation was performed.

## Movement / Rollback

Forward movement:

- not executed.

Rollback:

- not executed.
- not required because no forward movement occurred.

Approved command was not run:

- `v7-user-switch 10.7.0.11 wireguard-1779454504-c43409`: NOT RUN
- `v7-user-switch 10.7.0.11 1`: NOT RUN

## Tests

Evidence:

- `docs/track7/productization/e25-evidence/tests-and-safety-checks.md`

Results:

- `py_compile`: PASS
- targeted operator/helper tests: PASS, `26` tests
- full unittest discovery: PASS, `116` tests
- packet JSON validation: PASS
- restore-settle helper JSON: PASS
- runtime checkers: PASS
- hidden mover scan: PASS
- `git diff --check`: PASS

Unavailable/not applicable:

- forward verification: not applicable, no movement.
- rollback verification: not applicable, no movement.
- replay tests against valid movement packet: not applicable, no valid movement packet consumer and packet expired.

## Postmortem Matrix

Evidence:

- `docs/track7/productization/e25-evidence/full-postmortem-matrix.md`

Classification:

- `E25_NO_GO_PRE_EXECUTION`

Root blockers:

1. `TARGET_READINESS_NO_GO_STABILITY_BELOW_FLOOR`
2. `APPROVAL_PACKET_EXPIRED`
3. `MOVEMENT_PACKET_CONSUMER_NOT_CONNECTED`

## Required Next Step

Recommended next block:

`E25_1_TARGET_READINESS_RECOVERY_AND_MOVEMENT_PACKET_REFRESH`

Required before another movement attempt:

1. Re-establish `v7-second-canary-target-readiness=GO`.
2. Decide/readjust target readiness source semantics only in a separate bounded governance block if `stability.state` is stale or overly conservative.
3. Generate a fresh non-expired movement approval packet with real E25 confirmation timestamps.
4. Implement/connect a movement-capable packet consumer, or explicitly approve raw `v7-user-switch` fallback in the next execution block after fresh gates are GO.
5. Re-run restore-settle and runtime checks immediately before movement.

## Mandatory Answers

- `first_operator_driven_bounded_user_movement_executed=false`
- `candidate_user=10.7.0.11`
- `forward_target=wireguard-1779454504-c43409`
- `rollback_target=1`
- `forward_success=false`
- `rollback_executed=false`
- `rollback_success=false`
- `only_approved_user_moved=true` because no user moved
- `routing_mutation_limited_to_candidate=true` because no routing mutation occurred
- `delayed_movement_observed=false`
- `replay_rejection_verified=false`
- `audit_chain_verified=true` for readable prior E23 audit chain; no E25 record written
- `runtime_checkers_ok=true`
- `execution_governance_production_grade_for_one_user=false`
- `remaining_execution_blockers=TARGET_READINESS_NO_GO_STABILITY_BELOW_FLOOR, APPROVAL_PACKET_EXPIRED, MOVEMENT_PACKET_CONSUMER_NOT_CONNECTED`
- `recommended_next_block=E25_1_TARGET_READINESS_RECOVERY_AND_MOVEMENT_PACKET_REFRESH`
- `execution_allowed_now=false`

## Final Mutation Statement

- Runtime mutation performed: NO
- User movement performed: NO
- Routing mutation performed: NO
- Kill switch mutation performed: NO
- Autoswitch apply performed manually: NO
- Canary performed: NO
- Cohort performed: NO
