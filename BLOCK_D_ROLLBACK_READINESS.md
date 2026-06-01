# Block D Rollback Readiness

Project: V7 Vozduh

Block: D - Autoswitch Shadow And Operator Program

Date: 2026-06-01

## Rollback State

Rollback is known from prior Blocks A, B, and C and uses existing `v7-user-switch` movement preview and execution path.

For Block D, rollback was not executed.

## Readiness

Rollback is technically available for individual users, but a bulk rollback of the current ten-user cohort to egress `1` remains capacity-risky under the D0 decision.

## Requirement For Future Operator Execution

Any approved autoswitch execution must include:

- Per-user rollback target
- Rollback preview
- Rollback route table expectation
- Observation plan
- Capacity impact review

## Verdict

`rollback_ready=true`

