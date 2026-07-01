# Final Root Cause Experiment

Date: 2026-07-01 04:14 UTC

## Summary

The original L3 Production Validation authority-envelope rejection was narrowed and patched.
The patch was committed, pushed, safely deployed, and verified by truth/convergence.

The production run did not reach `_run_switch()`.
It stopped at the next executable gate:

`l3_wake_decision = REJECT_WAKE`

with blocker:

`confirmed_l3_wake_required`

Final result:

`STOP_SAFE_NEXT_GATE`

## Patch

Commit:

`9ef40a8a1cb17a30325a9653b823ffeb5126415d`

Files changed:

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

Minimal change:

L3 one-user Production Validation may consume `CURRENT_APPROVED_EMERGENCY_ENVELOPE` as execution authority only when the approved lock, restore barrier, selected move identity, one-user scope, verify, rollback, and no-broad-autonomy invariants all hold.

No new Runtime, Planner, owner, authority model, or execution path was created.

## Gate Truth Table

Real production run:

| Condition | Expected | Actual | Result |
|---|---:|---:|---|
| L3 Production Validation mode | true | true | PASS |
| one user exactly | 1 | 1 | PASS |
| approved plan lock valid | true | true | PASS |
| restore barrier written now | true | true | PASS |
| selected move hash matches | true | true | PASS |
| user/source/target scope matches | true | true | PASS |
| verify enabled | true | true | PASS |
| rollback-on-verify-fail enabled | true | true | PASS |
| max users = 1 | true | true | PASS |
| broad automation disabled | true | true | PASS |
| certified autonomy not granted | true | true | PASS |
| L3 wake accepted | true | false | STOP_SAFE |

## False Conditions

The false condition was not the approved emergency envelope.

False condition:

`confirmed_l3_wake_required`

Classification:

`STOP_SAFE_NEXT_GATE`

Current implementation still requires a confirmed L3 wake source before the emergency failover authority gate may pass. The one-user Production Validation envelope does not itself satisfy wake acceptance.

## Tests

Passed:

- `python3 -m unittest tests.unit.test_v7_users_autoswitch_policy`
- `python3 -m unittest tests.unit.test_governed_canary_cli tests.unit.test_operator_execution_pipeline tests.unit.test_operator_execution_packet`
- `PYTHONPYCACHEPREFIX=/tmp/v7-pycache python3 -m py_compile tools/v7-users-autoswitch tools/v7-governed-canary-dry-run-cycle admin_core/operator_execution.py admin_core/operator_execution_pipeline.py`

Negative coverage added for:

- no approved envelope
- expired envelope
- wrong user
- wrong source
- wrong target
- selected move hash mismatch
- two users
- missing verify
- missing rollback
- target unsafe
- source recovered
- timer/broad autoswitch path

Positive coverage added for:

- valid one-user L3 Production Validation envelope survives authority gate and reaches fake `_run_switch()`

## Deploy / Truth / Convergence

Safe deploy completed.

Truth:

`PASS`

Convergence:

`PASS`

Runtime commit:

`9ef40a8a1cb17a30325a9653b823ffeb5126415d`

## Production Run

Command:

```bash
/usr/local/bin/v7-governed-canary-dry-run-cycle \
  --execute-l3-production-validation \
  --confirm-l3-production-validation EXECUTE_L3_PRODUCTION_VALIDATION_APPROVED \
  --max-users 1
```

Result:

- transaction_status: `STOP_SAFE`
- apply_executed: `false`
- users_moved: `0`
- verification_result: `NOT_RUN`
- terminal_reason: `approved_plan_lock_selected_moves_missing`
- selected_moves_before_restore_barrier: `1`
- selected_moves_after_gate: `0`
- execution_blocker: `emergency_failover_autonomy`
- next blocker: `confirmed_l3_wake_required`

## Next Exact Blocker

`confirmed_l3_wake_required`

The next executable question is whether an explicitly approved one-user L3 Production Validation transaction should satisfy the wake requirement for that transaction only, or whether a separate confirmed wake source must be present before the first production validation rung may execute.

No further architecture conclusion is made in this report.

## Final Verdict

STOP_SAFE_NEXT_GATE
