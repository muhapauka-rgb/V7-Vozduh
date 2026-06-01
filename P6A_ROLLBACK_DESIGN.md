# P6.A Rollback Design

Project: V7 Vozduh

Block: P6.A

## Rollback Trigger

Rollback is triggered if post-movement verification or observation detects:

- candidate not on target when expected;
- route table `1009` does not use `v7execwg0`;
- checker failure;
- destination instability;
- hidden mover;
- selected moves nonzero;
- unapproved routing drift;
- operator manual abort.

## Rollback Action

Future rollback action:

`v7-user-switch 10.7.0.11 1`

P6.A did not execute rollback.

## Rollback Verification

Verify after rollback:

- user `10.7.0.11` current egress is `1`
- route table `1009` points to source interface for `1`
- destination users count returns to `0`
- selected moves remain `0`
- no other users changed
- checkers pass

## Rollback Observation

Observation after rollback:

- immediate sample
- delayed sample after at least one autoswitch/planner interval if timers are active
- final registry/route hash comparison

## Rollback Confidence

Confidence is high for this design because historical E27.2/E28.2 evidence rolled this candidate family back to `1`, and read-only preview identifies the exact rollback target.

## Verdict

- rollback_defined=true
- rollback_executed=false
