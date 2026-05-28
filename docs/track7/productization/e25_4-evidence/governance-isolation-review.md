# E25.4 Governance Isolation Review

## Existing Reservation Enforcement

Code and tests show that `canary_reserved=true` blocks production assignment:

- `tools/v7-users-autoswitch` gates `canary_reserved` in `_gate_reservation`.
- `tests/unit/test_v7_users_autoswitch_policy.py` includes `test_canary_reserved_target_is_not_used_as_production_failover`.
- `tests/unit/test_v7_users_autoswitch_policy.py` includes `test_current_user_on_canary_reserved_target_is_not_auto_drained`.

Relevant block reasons:

- `canary_reserved_production_assignment_blocked`
- `canary_reserved_current_hold_requires_separate_drain_approval`

## Live Isolation Evidence

Live selected-move state:

- selected-move files absent under `/opt/v7/egress/state`
- interpreted as `selected_moves=0`

Hidden mover scan:

- no active `v7-user-switch`
- no active `v7-routing-sync`
- no active `v7-users-autoswitch --apply`

Runtime checkers:

- `V7_RECONCILE_RESULT=OK`
- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

## Planner Dry-Run

Live `v7-users-autoswitch --mode observe --pretty` was not run. The sandbox escalation was rejected because even observe-mode autoswitch may write planning or load artifacts on live VPS.

This was treated as the safer outcome for E25.4. Governance isolation was therefore reviewed through source gates, unit tests, selected-move absence, and hidden-mover/runtime checker evidence.

## Gap For New Dedicated Target

No new dedicated execution target exists yet, so isolation cannot be validated for it specifically.

Required future validation after provisioning:

- target has `canary_reserved=true` or stronger `execution_reserved=true`;
- target has `manual_only=1` and `reserve_only=1`;
- autoswitch planning produces `selected_moves=0`;
- production assignment to that egress is blocked;
- rebalance cannot select the target;
- hidden mover scan remains empty.

## Status Flags

- `reservation_enforcement_valid=true` for existing reserved semantics.
- `autoswitch_assignment_blocked=true` for existing canary-reserved semantics by tests/source review.
- `rebalance_assignment_blocked=true` for existing canary-reserved semantics by tests/source review.
- `accidental_assignment_possible=true` for a future dedicated target until it is actually provisioned and validated.
