# E25.5 Tests and Safety Checks

## py_compile

Command:

```text
PYTHONPYCACHEPREFIX=.pycache-e25_5 python3 -m py_compile tools/v7-second-canary-target-readiness tools/v7-restore-settle-gate tools/v7-operator-execution-packet admin_core/operator_execution.py tools/v7-users-autoswitch
```

Result: PASS.

Temporary `.pycache-e25_5` was removed after the check.

## Targeted Unit Tests

Command:

```text
python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate tests.unit.test_operator_execution_packet tests.unit.test_v7_users_autoswitch_policy
```

Result: PASS.

Count: `47 tests`.

## Full Unit Suite

Command:

```text
python3 -m unittest discover tests
```

Result: PASS.

Count: `116 tests`.

## Helper Smoke Checks

Commands:

```text
tools/v7-second-canary-target-readiness --pretty
tools/v7-second-canary-target-readiness --json
tools/v7-restore-settle-gate --pre-restore --state-dir docs/track7/productization/e25_1-evidence/restore-settle-samples --pretty
tools/v7-restore-settle-gate --pre-restore --state-dir docs/track7/productization/e25_1-evidence/restore-settle-samples --json
```

Result: PASS.

## Runtime Checkers

Runtime checkers were run on VPS during final safety validation:

- `V7_RECONCILE_RESULT=OK`
- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

## Hidden Mover Scan

Final VPS hidden mover scan found no active:

- `v7-user-switch`
- `v7-routing-sync`
- `v7-users-autoswitch --apply`

Result: PASS.

## Governance Isolation Tests

Covered by:

- `tests.unit.test_v7_users_autoswitch_policy`
- source review of reservation gates in `tools/v7-users-autoswitch`

Result: PASS for existing reservation semantics.

No live autoswitch apply or live autoswitch dry-run was executed.

## Credential Scan

Command:

```text
rg -n "<credential/private-key/header patterns>" docs/track7/productization/e25_5-evidence BLOCK_E25_5_DEDICATED_EXECUTION_EGRESS_PROVISIONING_AND_VALIDATION_REPORT.md
```

Result: PASS. No matches.

## Dangerous-Call Scan

Command:

```text
rg -n "<movement/routing/apply/service-control patterns>" docs/track7/productization/e25_5-evidence tools/v7-second-canary-target-readiness tools/v7-restore-settle-gate tools/v7-operator-execution-packet admin_core/operator_execution.py tools/v7-users-autoswitch
```

Result: PASS with expected source/evidence matches.

Expected matches:

- helper docstrings stating forbidden commands are not called;
- redacted test profiles showing why they were rejected as unsafe;
- autoswitch source contains an apply path, but E25.5 did not run it.

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
