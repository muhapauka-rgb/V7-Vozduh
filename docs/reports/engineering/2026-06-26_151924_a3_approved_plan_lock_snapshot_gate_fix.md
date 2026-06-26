# Engineering Report: A3 Approved Plan Lock Snapshot Gate Fix

Status: HISTORICAL_EVIDENCE
Date: 2026-06-26T15:19:24+0700
Backlog item: A3

## Summary

The existing autoswitch owner was fixed so a valid approved plan lock is not suppressed by non-material intelligence snapshot gate drift. Material snapshot changes still fail closed before mutation.

## Action Performed

- Extended `tools/v7-users-autoswitch`.
- Reused the existing packet owner, execution lease owner, restore-barrier owner, and guarded apply owner.
- Added approved plan lock snapshot gate materiality diagnostics.
- Preserved approved selected moves when snapshot drift is non-material.
- Kept explicit fail-closed blockers for material source changes, missing approved snapshot, and wrong packet snapshot.
- Deployed commit `ca8514ae31c6a3536082298acc993c78efd36489` through the existing safe deploy owner.
- Reran the production governed canary dry-run.

## Objective Observations

- Previous blocker: `approved_plan_lock_snapshot_gate_stop_required`.
- Previous failure mode: selected moves were `1` before restore-barrier clearance and `0` after the intelligence snapshot gate.
- Fixed owner: `tools/v7-users-autoswitch`.
- New diagnostics:
  - `snapshot_gate_source`;
  - `snapshot_gate_decision`;
  - `snapshot_gate_changed_fields`;
  - `snapshot_gate_material_change`;
  - `approved_plan_lock_consumed`.
- Deploy id: `deploy-z8-14-Updatesystem-ca8514a-20260626T151701`.
- Truth: `PASS`; local, GitHub, and runtime aligned.
- Convergence: `PASS`; `ALIGNED`; runtime action guard `READY_FOR_RUNTIME_ACTION`.
- Production dry-run verdict: `AUTONOMOUS_DRY_RUN_CYCLE_REACHES_AUTHORITY_BOUNDARY`, normalized by OMP as `OPERATIONAL_AUTHORITY`.
- Current packet: `pkt_preview_4eb137c926917c2761faadb4`.
- User: `10.7.0.17`.
- Move: `vless -> awg0`.
- Selected move hash: `e1e09d2c95fc6c9b0b77e9ecaaf0def20e9759150eb35db8d70f95e107eb52cd`.
- Runtime mutation: `false`.
- Users moved: `0`.
- Authority expanded: `false`.

## Engineering Conclusions

The root cause was inside the existing autoswitch apply path. The implementation treated snapshot gate stop as a selected-move suppressor even when an approved immutable plan lock was valid, instead of distinguishing material state change from freshness-only or non-material snapshot drift.

The fix preserves locked selected moves only when the approved plan is semantically unchanged and safety gates pass. If the snapshot is materially unsafe, the apply path remains fail-closed.

## Impact

- A3 no longer stops at `UNSAFE_IMPLEMENTATION` for the approved plan lock snapshot gate path.
- Engineering is ready for the next A3 production action.
- A3 remains uncertified until a real governed movement produces verification, rollback/no-rollback classification, outcome closure, and learning evidence.
- Runtime automation remains disabled.
- No users were moved during the fix.

## Capability Progress

Movement Protection, Rollback, Runtime Eligibility, Authority Evolution, and Learning gained implementation evidence for the approved packet-to-apply safety path. Production outcome evidence did not increase because no movement occurred.

## Backlog Progress

A3 remains `IN_PROGRESS`. The current stop is `OPERATIONAL_AUTHORITY` for exact packet `pkt_preview_4eb137c926917c2761faadb4`.

## Production Maturity

Production Maturity remains `21.5%`. The fix improves implementation readiness but does not certify A3, because certification requires real observed production outcome evidence.

## Canonical Knowledge

No new canonical owner was required. The fix implements the existing material state change and approved packet identity rules through the existing autoswitch owner.

## Evidence

- Focused tests: `python3 -m unittest tests.unit.test_v7_users_autoswitch_policy`; `Ran 81 tests`; `OK`.
- Relevant tests: `python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_operator_execution_packet tests.unit.test_operator_execution_pipeline tests.unit.test_operator_observability tests.unit.test_v7_restore_settle_gate tests.unit.test_v7_second_canary_target_readiness`; `Ran 184 tests`; `OK`.
- Full tests: `python3 -m unittest discover tests`; `Ran 534 tests`; `OK`.
- Commit: `ca8514ae31c6a3536082298acc993c78efd36489`.
- Deploy id: `deploy-z8-14-Updatesystem-ca8514a-20260626T151701`.
- Truth: `PASS`.
- Convergence: `PASS`.
- Production dry-run: current A3 packet ready at operational authority boundary.

## Next Step

Approve or reject exact packet `pkt_preview_4eb137c926917c2761faadb4`. If approved, execute through existing owners only, verify immediately, rollback if verification fails, close outcome, feed learning, update Current Program State and OMP, then rerun truth/convergence.

## Re-audit Rule

Do not re-audit approved plan lock snapshot-gate consumption unless autoswitch apply semantics, execution lease semantics, restore-barrier semantics, or intelligence snapshot gate semantics materially change, or production evidence disproves this behavior.
