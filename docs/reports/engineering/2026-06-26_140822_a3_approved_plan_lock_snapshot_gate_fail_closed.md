# Engineering Report: A3 Approved Plan Lock Snapshot Gate Fail-Closed

Status: HISTORICAL_EVIDENCE
Date: 2026-06-26T14:08:22+0700
Backlog item: A3

## Summary

The operator approved exact governed packet `pkt_preview_4eb137c926917c2761faadb4`. V7 consumed the approved packet, created an execution lease, wrote restore-barrier clearance through the existing owner, and then failed closed before user movement because the existing autoswitch owner suppressed approved locked selected moves at the intelligence snapshot gate.

## Action Performed

- Created execution lease `execlease_19550ea3b6750ed163344f8a`.
- Preserved approved packet identity for packet `pkt_preview_4eb137c926917c2761faadb4`.
- Wrote restore-barrier clearance `rbclear_1951ca727830c155efc8cf0e`.
- Entered guarded apply through `tools/v7-users-autoswitch`.
- Verified the user route after the failed-closed apply path.
- Closed the failed-closed outcome and refreshed learning from observed evidence only.

## Objective Observations

- Packet id: `pkt_preview_4eb137c926917c2761faadb4`.
- Decision id: `decision_preview_0febce4f948e1d1a2c966b72`.
- Operation id: `govdry_5570f5503f3e320172e7785b`.
- Selected move hash: `e1e09d2c95fc6c9b0b77e9ecaaf0def20e9759150eb35db8d70f95e107eb52cd`.
- Subject: `10.7.0.17`.
- Source: `vless`.
- Target: `awg0`.
- Apply result: `DENIED`.
- Terminal reason: `approved_plan_lock_selected_moves_missing`.
- Unsafe blocker: `approved_plan_lock_snapshot_gate_stop_required`.
- Selected moves before restore-barrier clearance: `1`.
- Selected moves after intelligence snapshot gate: `0`.
- User movement: `0`.
- Rollback: `NOT_ATTEMPTED`, because no movement occurred.
- Route verification: user remained on `vless` / `tun0`.

## Engineering Conclusions

Approved packet identity, lease binding, and restore-barrier clearance now work through existing owners. The remaining defect is inside the existing autoswitch apply owner: a valid approved plan lock can lose selected moves after the intelligence snapshot gate and before mutation.

This is an implementation defect, not an authority boundary and not a fundamental architecture gap.

## Impact

- No user was moved.
- No authority was expanded.
- No daemon or timer was enabled.
- A3 remains incomplete.
- The next highest leverage action is `A3_FIX_APPROVED_PLAN_LOCK_SNAPSHOT_GATE_CONSUMPTION_IN_EXISTING_AUTOSWITCH_OWNER`.

## Capability Progress

Movement Protection and Runtime Eligibility gained real fail-closed evidence. Production movement evidence did not increase because no user movement occurred.

## Backlog Progress

A3 remains `IN_PROGRESS`. The current blocker is `UNSAFE_IMPLEMENTATION`.

## Production Maturity

Production Maturity should not increase from this failed-closed attempt. Engineering confidence increases only for fail-closed safety behavior.

## Canonical Knowledge

The approved plan lock path must preserve selected moves through the intelligence snapshot gate unless a material state change is proven. Snapshot or freshness drift alone must not erase an approved locked move.

## Evidence

- Restore-barrier clearance: `rbclear_1951ca727830c155efc8cf0e`.
- Approved plan lock: `apl_dad64e7a36d0191f189eeb92`.
- Execution feedback: `execfb_ade2aec764e439ee470f9f7e`.
- Learning record: `learn_56ea36bb3218df76944653ed`.
- Snapshot refresh: `PASS`.
- Trust after observed outcome: `44.465`.

## Next Step

Extend existing `tools/v7-users-autoswitch` so approved plan lock selected moves remain available at mutation time when no material state change is proven. Missing selected moves must remain an explicit unsafe blocker, not a silent NOOP.

## Re-audit Rule

Do not re-audit packet authority or lease binding for this issue unless planner, lease, restore-barrier, or autoswitch apply semantics materially change. Future work must extend the existing autoswitch owner.
