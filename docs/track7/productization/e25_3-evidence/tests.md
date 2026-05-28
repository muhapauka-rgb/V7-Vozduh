# E25.3 Tests and Safety Checks

## py_compile

Command:

```text
PYTHONPYCACHEPREFIX=.pycache-e25_3 python3 -m py_compile tools/v7-second-canary-target-readiness tools/v7-restore-settle-gate tools/v7-operator-execution-packet admin_core/operator_execution.py
```

Result: PASS.

Temporary `.pycache-e25_3` was removed after the check.

## Targeted Unit Tests

Command:

```text
python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate tests.unit.test_operator_execution_packet
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

## Target Readiness Helper

Commands:

```text
tools/v7-second-canary-target-readiness --pretty
tools/v7-second-canary-target-readiness --json
```

Result: PASS.

## Restore-Settle Helper

Commands:

```text
tools/v7-restore-settle-gate --pre-restore --state-dir docs/track7/productization/e25_1-evidence/restore-settle-samples --pretty
tools/v7-restore-settle-gate --pre-restore --state-dir docs/track7/productization/e25_1-evidence/restore-settle-samples --json
```

Result: PASS.

## Runtime Checkers

Runtime checkers were run on VPS during the final read-only safety check:

- `V7_RECONCILE_RESULT=OK`
- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

## Hidden Mover Scan

The final VPS scan found no active process matching:

- `v7-user-switch`
- `v7-routing-sync`
- `v7-users-autoswitch --apply`

Result: PASS.

## Credential Scan

Command:

```text
rg -n "<credential/private-key/header patterns>" docs/track7/productization/e25_3-evidence BLOCK_E25_3_WIREGUARD_TARGET_STABILITY_RECOVERY_OR_RETARGETING_FOR_FIRST_MOVEMENT_REPORT.md
```

Result: PASS. No matches.

## Dangerous-Call Scan

Command:

```text
rg -n "<movement/routing/apply/service-control patterns>" docs/track7/productization/e25_3-evidence tools/v7-second-canary-target-readiness tools/v7-restore-settle-gate tools/v7-operator-execution-packet admin_core/operator_execution.py
```

Result: PASS with expected negative/documentation-only matches.

Matches were the helper docstrings and evidence text stating that those commands are not called.

## Git Diff Check

Command:

```text
git diff --check
```

Result: PASS.

## Mutation Statement

- Runtime mutation performed: NO
- User movement performed: NO
- Routing mutation performed: NO
- Autoswitch apply performed manually: NO
- Canary/cohort performed: NO
