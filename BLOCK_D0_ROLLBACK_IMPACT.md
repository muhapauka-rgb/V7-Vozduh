# Block D0 Rollback Impact

Project: V7 Vozduh

Block: D0 - Execution Cohort Decision Program

Date: 2026-06-01

## Rollback Option

Rollback target for the cohort would be egress `1`.

Current egress `1` count:

- `0`

Rollback of all ten users would result in:

- Egress `1` count: `10`
- Execution target count: `0`

## Capacity Impact

Egress `1` has policy fields:

- Soft limit: `1`
- Hard limit: `2`

Returning all ten users to egress `1` would exceed that policy hard limit. Although egress `1` has historically carried the cohort, the current decision should not choose rollback unless there is a separate rollback necessity or a new capacity waiver.

## Trust Impact

Trust state remains `NEEDS_ATTENTION` for trusted-RU sensitive routing. Rollback does not resolve that trust risk; it only changes where the cohort resides.

## Risk

Rollback is operationally available but capacity-negative as a default decision.

## Verdict

`rollback_impact_review_complete=true`

