# Emergency Runtime Autonomy Apply / Verification / Rollback

## Summary

Emergency apply now verifies route and required services after movement.
If required service verification fails, existing rollback-on-verify-fail path rolls the user back and stops safely.

## Action Performed

Extended existing apply path to call required service verification only for `execution_mode=emergency_failover`.

## Files Changed

- `tools/v7-users-autoswitch`

## Users Moved

NO in local validation.

## Authority Impact

No authority expansion.

## Runtime Impact

No generic autoswitch behavior changed.
Emergency path remains bounded and fail-closed.

## Restore / Rollback Status

Rollback is required by default and tested.
Rollback success records terminal state `ROLLED_BACK` when service verification fails.

## Verification Result

Route verification and required-service verification both remain live gates.

## Tests

Added tests:

- emergency apply succeeds and verifies required services;
- emergency service verification failure rolls back and stops.

## Production Impact

No production action.

## Canonical Changes

NONE.

## Next Step

Expose emergency status in admin UI and run full relevant tests.

