# E25.5 Governance Isolation Validation

## Result

`governance_isolation_valid=false_FOR_NEW_TARGET`

No new dedicated execution target exists, so isolation cannot be validated for it.

## Existing Semantics

Existing reservation semantics remain valid:

- `canary_reserved=true` is blocked from production assignment in `tools/v7-users-autoswitch`.
- Targeted autoswitch policy tests passed.
- selected-move files are absent on VPS.
- hidden movers are absent.
- runtime checkers are OK.

## Required Future Validation

After a real dedicated execution target is provisioned:

- target metadata must include `execution_reserved=true` or equivalent;
- `manual_only=1`;
- `reserve_only=1`;
- `canary_reserved=true`;
- `autoswitch_allowed=false`;
- `rebalance_allowed=false`;
- production assignment blocked by source and tests;
- selected_moves remains `0`;
- hidden movers absent.

## Flags

- `governance_reserved=false`
- `autoswitch_excluded=false`
- `rebalance_excluded=false`
- `production_assignment_blocked=false`
- `accidental_assignment_possible=true`

These are false/true for the new target because it does not exist yet.
