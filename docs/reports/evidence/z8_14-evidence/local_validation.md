# Z8.14 Evidence — Local Validation

## Syntax

Command:

`env PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache python3 -m py_compile tools/v7_sync_lib.py tools/v7-sync-status tools/v7-safe-commit tools/v7-safe-push tools/v7-safe-deploy tools/v7-release-sync`

Result: PASS.

## Unit Tests

Command:

`python3 -m unittest tests/unit/test_v7_sync_tools.py tests/unit/test_v7_truth_check.py`

Result:

`Ran 30 tests in 0.070s`

`OK`

## Dry Runs

`python3 tools/v7-safe-commit --message 'Z8.14 sync pipeline dry run' --allow-runtime-critical --json`

Result: PASS.

`python3 tools/v7-safe-push --json`

Result: expected NO-GO before commit because runtime-critical files were uncommitted.

`python3 tools/v7-safe-deploy --json`

Result: expected NO-GO before commit because GitHub/local truth could not pass while runtime-critical files were uncommitted.
