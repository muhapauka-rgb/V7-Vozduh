# E25.11 Governance Isolation Validation

## Result

`governance_isolation_valid=true`

`accidental_assignment_possible=false`

`autoswitch_excluded=true`

`rebalance_excluded=true`

`production_assignment_blocked=true`

`target_users_zero=true`

`selected_moves_zero=true`

`hidden_movers_absent=true`

## Isolation Controls

The execution target is isolated by metadata:

- `role=EXECUTION_ONLY`
- `manual_only=1`
- `reserve_only=1`
- `autoswitch_allowed=false`
- `rebalance_allowed=false`
- `production_assignment_allowed=false`
- `reservation_owner=operator_execution_governance`

`tools/v7-users-autoswitch` already blocks `manual_only` targets and blocks `reserve_only` targets for planned movement. No autoswitch apply or unsafe observe mode was run in E25.11.

## Readiness Helper Boundary

Default readiness mode still rejects the execution target:

- rejection reason: `manual_only`
- rejection reason: `reserve_only`

The target is selected only with explicit operator intent:

```text
v7-second-canary-target-readiness --execution-target-id amneziawg-exec-20260528-10-8-1-14
```

## Runtime Isolation

- no user movement occurred
- no user route table changed
- selected moves remained absent/zero
- hidden mover scan did not show persistent hidden movement process
- runtime checkers stayed OK after integration

The target is platform-integrated but remains excluded from automated assignment.
