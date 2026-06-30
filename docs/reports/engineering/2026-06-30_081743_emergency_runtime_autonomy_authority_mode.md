# Emergency Runtime Autonomy Authority Mode

## Summary

Implemented bounded `EMERGENCY_FAILOVER_AUTONOMY` as an explicit, default-disabled authority mode inside the existing autoswitch owner.

## Action Performed

Added emergency failover policy and authority gate for one-run bounded emergency failover.

## Files Changed

- `tools/v7-users-autoswitch`

## Users Moved

NO.

## Authority Impact

No broad authority expansion.
Authority is limited to emergency failover only and remains disabled unless explicitly enabled by policy or CLI flag.

## Runtime Impact

Runtime behavior is unchanged while emergency mode is disabled.
When enabled, only `move_type=failover` with `current_egress_not_eligible` may pass.

## Restore / Rollback Status

Emergency gate requires restore barrier, rollback readiness and verification readiness by default.

## Verification Result

Gate fails closed for stale service evidence, missing rollback, missing safe target, non-failover movement and cooldown.

## Tests

Covered in autoswitch unit tests.

## Production Impact

No production action.

## Canonical Changes

NONE.

## Next Step

Validate selected move materialization and apply behavior.

