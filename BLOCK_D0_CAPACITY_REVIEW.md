# Block D0 Capacity Review

Project: V7 Vozduh

Block: D0 - Execution Cohort Decision Program

Date: 2026-06-01

## Current Capacity

Execution target:

- Current users: `10`
- Soft limit: `10`
- Hard limit: `10`
- Headroom: `0`

## Future Growth

The current target is not suitable for future autoswitch testing or additional cohort expansion because it is already at hard limit.

Autoswitch remains forbidden for this execution target because:

- `autoswitch_allowed=false`
- `rebalance_allowed=false`
- `production_assignment_allowed=false`
- `manual_only=1`
- `reserve_only=1`

## Review

The current cohort can be held for observation, but the current execution target cannot safely absorb new users or support the next expansion decision.

## Verdict

- `capacity_review_complete=true`
- Future autoswitch testing on current target: not suitable

