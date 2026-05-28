# E25.2 Tests and Safety Checks

## py_compile

Command:

```text
PYTHONPYCACHEPREFIX=.pycache-e25_2 python3 -m py_compile tools/v7-operator-execution-packet admin_core/operator_execution.py tools/v7-second-canary-target-readiness tools/v7-restore-settle-gate
```

Result: PASS.

Temporary `.pycache-e25_2` was removed after the check.

## Targeted Unit Tests

Command:

```text
python3 -m unittest tests.unit.test_operator_execution_packet tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate
```

Result: PASS.

Count: `26 tests`.

## Full Unit Suite

Command:

```text
python3 -m unittest discover tests
```

Result: PASS.

Count: `116 tests`.

## Restore-Settle Helper

Command:

```text
tools/v7-restore-settle-gate --pre-restore --state-dir docs/track7/productization/e25_1-evidence/restore-settle-samples --pretty
tools/v7-restore-settle-gate --pre-restore --state-dir docs/track7/productization/e25_1-evidence/restore-settle-samples --json
```

Result: PASS.

The gate remained `GO`.

## Packet JSON Validation

Command:

```text
python3 -m json.tool docs/track7/productization/e25_1-evidence/fresh-movement-approval-packet.json
```

Result: PASS.

## Runtime Checkers

Runtime checkers were executed during the VPS live recheck:

- `V7_RECONCILE_RESULT=OK`
- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

## Hidden Mover Scan

Runtime hidden mover scan was executed during the VPS live recheck and final no-mutation check.

Result: PASS. No active `v7-user-switch`, `v7-routing-sync`, or `v7-users-autoswitch --apply` process was observed.

## Target Readiness Helper

Runtime target readiness helper was executed on VPS.

Result: FAIL as execution gate, expected abort:

- `approval_status=NO-GO`
- `second_canary_readiness=NO-GO`
- WireGuard target `min_mbps=4.61`
- WireGuard target `stability=0.297919` / `0.300861`

## Credential Scan

Command:

```text
rg -n "<credential/private-key/header patterns>" docs/track7/productization/e25_2-evidence BLOCK_E25_2_FIRST_OPERATOR_DRIVEN_BOUNDED_USER_MOVEMENT_EXECUTION_RETRY_REPORT.md
```

Result: PASS. No matches.

## Dangerous-Call Scan

Command:

```text
rg -n "<movement/routing/apply/service-control patterns>" docs/track7/productization/e25_2-evidence BLOCK_E25_2_FIRST_OPERATOR_DRIVEN_BOUNDED_USER_MOVEMENT_EXECUTION_RETRY_REPORT.md tools/v7-operator-execution-packet admin_core/operator_execution.py
```

Result: PASS with expected documentation-only matches.

Expected matches were references to commands that were explicitly not executed, plus process-scan labels.

## Git Diff Check

Command:

```text
git diff --check
```

Result: PASS.

## Unavailable / Not Applicable

- Forward verification: not applicable because no forward movement occurred.
- Rollback verification after movement: not applicable because no rollback was needed.
- Audit success record validation: not applicable because no movement execution record was written.
