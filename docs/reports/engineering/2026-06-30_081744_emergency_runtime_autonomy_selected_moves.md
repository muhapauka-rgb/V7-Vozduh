# Emergency Runtime Autonomy Selected Moves

## Summary

Emergency mode now converts already-planned failover proposals into bounded executable selected moves only when all emergency gates pass.

## Action Performed

Integrated emergency authority gate into the existing autoswitch planning pipeline.

## Files Changed

- `tools/v7-users-autoswitch`

## Users Moved

NO.

## Authority Impact

No new authority owner.
Emergency selected moves are scoped to one-run failover and do not authorize rebalance, optimization, reconnect rotation or future movement.

## Runtime Impact

Emergency selected moves carry `execution_mode=emergency_failover`.
Restore barrier execution gate allows them only when the emergency gate has authorized the bounded failover.

## Restore / Rollback Status

Restore barrier remains active and visible.
Emergency authorization is recorded separately from generic restore-barrier approval.

## Verification Result

Selected moves are capped by `max_users_per_run` and `max_users_per_channel`.
Cooldown is enforced.

## Tests

Added tests for emergency ON/OFF, stale evidence, no safe target, rollback missing, cooldown and non-failover blocking.

## Production Impact

No production action.

## Canonical Changes

NONE.

## Next Step

Validate apply, verification and rollback behavior.

