# Final Implementation Decision

## Summary

`approved_plan_lock.selected_moves` semantic reduction was an implementation defect, not an intentional serialization contract.

The defect was fixed and deployed. Planner semantic evidence now survives into `approved_plan_lock.selected_moves`.

Production validation did not move a user. It stopped at the next live L3 gate:

`required_service_failure_required` -> `confirmed_l3_wake_required`

## Design Verification

No canonical document, ADR, code comment, or observed commit history established semantic stripping as intentional architecture, security/privacy behavior, or performance optimization.

The identity-only lock behavior predates L3 emergency failover runtime semantics. Later code already attempted to rehydrate semantics from live decisions, proving Runtime needed this evidence.

Classification:

`IMPLEMENTATION_DEFECT`

## Reason For Serialization

The original serialization preserved only identity fields:

- `user_ip`
- `current_egress`
- `recommended_egress`
- `move_type`

No documented canonical reason was found for dropping Planner evidence fields already produced by the same plan.

## Files Changed

- `admin_core/operator_execution.py`
- `tools/v7-governed-canary-dry-run-cycle`
- `tests/unit/test_governed_canary_cli.py`

## Implementation

Preserved existing selected move object.

No new packet, wake object, event, runtime state, planner output, owner, or architecture was introduced.

Semantic fields preserved:

- `reason`
- `important_services`
- `candidates`
- `scores`
- `service_failover`

`selected_moves_from_plan()` now enriches identity-only selected rows from matching `plan.decisions` when needed.

## Safety

Unchanged:

- identity hash basis
- selected move hash semantics
- replay protection
- approved plan lock identity
- restore barrier identity
- packet identity
- authority semantics

Only missing Planner evidence is now available to Runtime.

## Tests

PASS:

```text
python3 -m unittest \
  tests.unit.test_operator_execution_packet \
  tests.unit.test_v7_users_autoswitch_policy \
  tests.unit.test_governed_canary_cli \
  tests.unit.test_operator_execution_pipeline

Ran 202 tests
OK
```

PASS:

```text
python3 -m py_compile \
  admin_core/operator_execution.py \
  tools/v7-users-autoswitch \
  tools/v7-governed-canary-dry-run-cycle \
  admin_core/operator_execution_pipeline.py
```

## Deployment

Commit deployed:

`478b66f329158eb5611150c1f17dd26bf64bb6ab`

Safe deploy:

`PASS`

Truth:

`PASS`

Convergence:

`FULLY_ALIGNED`

## Production Validation

Command:

```text
/usr/local/bin/v7-governed-canary-dry-run-cycle \
  --execute-l3-production-validation \
  --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED \
  --max-users 1
```

Result:

- `final_verdict`: `STOP_SAFE`
- `apply_executed`: `false`
- `users_moved`: `0`
- `verification_result`: `NOT_RUN`
- `rollback_result`: `NOT_REQUIRED`
- selected user: `10.7.0.5`
- source: `awg0`
- target: `vless`

## Post-Fix Evidence

Latest restore barrier approved plan lock contains semantic selected move fields:

- `candidates`
- `current_egress`
- `important_services`
- `move_type`
- `reason`
- `recommended_egress`
- `user_ip`

`approved_plan_lock_validation.ok = true`

## Remaining Blocker

The serialization defect is fixed.

Execution is now blocked by L3 live evidence semantics:

- `gate_blockers`: `confirmed_l3_wake_required`, `required_service_failure_required`
- `move_evidence.current_failures`: empty
- selected move reason: `current_egress_not_eligible`
- selected move does not prove required service failure for the current source

Exact next executable blocker:

`required_service_failure_required`

Responsible owner:

`tools/v7-users-autoswitch._emergency_failover_move_evidence`

## Final State

No user was moved.

No runtime automation was enabled.

No authority was expanded.

No new owner was created.

No new architecture was introduced.

