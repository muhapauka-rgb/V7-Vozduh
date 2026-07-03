# L3 Batch Apply Timeout Proof Capture Fix

## Summary

Phase 4 MEDIUM_BATCH certification advanced past Planner, Authority, packet materialization, Approved Plan Lock, Restore Barrier, and transition:

- transition status: `READY`
- selected_move_count: `10`
- selected users: `10.7.0.16` through `10.7.0.25`

The governed owner then timed out the Runtime Apply command after 90 seconds:

- final_verdict: `STOP_SAFE`
- stop_reason: `l3_production_validation_downstream_proof_failed`
- autoswitch_apply.returncode: `124`
- autoswitch_apply error: command timed out after 90 seconds
- verification_result: `NOT_RUN` in the certification wrapper
- apply_executed: `false` in the certification wrapper

Production state showed the child Runtime process completed later and moved the selected users, but the governed owner had already stopped and did not capture canonical proof for the exact governed operation.

## Root Cause

Owner: `tools/v7-governed-canary-dry-run-cycle`

Function: `run_autoswitch_apply`

Field: hardcoded `timeout=90`

The timeout was sufficient for CANARY/SMALL_BATCH paths but not sufficient for a 10-user Runtime Apply + Verification path. Because the parent process timed out before the child completed, the certification wrapper lost the canonical output and marked the operation as proof-failed even though production movement occurred.

## Correction

Added:

- `autoswitch_apply_timeout_seconds(max_users)`

Timeout behavior:

- 1 user: 90 seconds
- 10 users: 360 seconds
- capped at 900 seconds

`run_autoswitch_apply` now passes the batch-aware timeout into `subprocess.run` and records `timeout_seconds` in success and timeout outputs.

## Changed Files

- `tools/v7-governed-canary-dry-run-cycle`
- `tests/unit/test_governed_canary_cli.py`

## Tests

Targeted:

```text
python3 -m unittest tests.unit.test_governed_canary_cli

Ran 28 tests
OK
```

Affected suites:

```text
python3 -m unittest \
  tests.unit.test_v7_users_autoswitch_policy \
  tests.unit.test_operator_execution_packet \
  tests.unit.test_governed_canary_cli \
  tests.unit.test_operator_execution_pipeline

Ran 242 tests in 10.734s
OK
```

Compile:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile \
  tools/v7-governed-canary-dry-run-cycle \
  tests/unit/test_governed_canary_cli.py

OK
```

## Production Evidence

Timed-out artifact:

- `/tmp/v7_phase4_medium_batch_after_move_continuity_fix_20260703T061407.json`

The artifact proved:

- packet and restore barrier were materialized;
- transition was READY;
- selected move count was 10;
- apply was invoked;
- parent timeout prevented proof capture.

Current production assignments after the timed-out child completed:

- selected users `10.7.0.16` through `10.7.0.25` were moved to healthy targets;
- 15 certification users remained on `wireguard-1779454504-c43409`.

The run cannot certify Phase 4 because exact-operation proof was not captured. Phase 4 must be rerun after deployment from a clean controlled pool.

## Current Phase Position

Current Phase: Phase 4 MEDIUM_BATCH certification

Interrupted breakpoint resolved: governed owner timeout was not batch-aware and lost Runtime/Verification proof.

Next step: deploy through the standard safe deployment path, restore the controlled certification pool to the controlled source, and resume the same Phase 4 certification run with `--max-users 10`.

## Automation Debt

No new automation debt created.

## Workflow Debt

The certification execution workflow still requires manual breakpoint recovery. This remains Workflow Debt for the certification program to close in a later pipeline mission.
