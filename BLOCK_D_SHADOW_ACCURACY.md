# Block D Shadow Accuracy

Project: V7 Vozduh

Block: D - Autoswitch Shadow And Operator Program

Date: 2026-06-01

## Comparison

Shadow recommendation:

- Move `12` users by failover.
- Most recommended target: `awg3`.
- Reason included `current_egress_not_eligible` for execution cohort users.

Actual runtime governance state:

- Execution target intentionally holds a certified ten-user cohort.
- D0 decision recommended `CREATE_NEW_EXECUTION_TARGET`, not moving the cohort out.
- Current execution target is full but stable.
- Safety review is `critical`.
- Admin API is unavailable.

## Quality Assessment

The planner can produce recommendations in shadow mode, but the recommendation is not accurate enough for operator execution because:

- The proposed scope exceeds an acceptable operator packet for first autoswitch approval.
- It treats the certified execution cohort as failover candidates rather than governance-held cohort members.
- Safety review blocks apply.
- Selected moves remain `0`.

## Verdict

`shadow_accuracy_acceptable=false`

