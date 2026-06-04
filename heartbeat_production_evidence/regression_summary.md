# Regression Summary

Program: PROGRAM_HEARTBEAT_PRODUCTION_MATERIALIZATION_AND_OPERATOR_VISIBLE_CERTIFICATION
Date: 2026-06-04

## Targeted Closure Tests

Commands:

```text
PYTHONPYCACHEPREFIX=/private/tmp/heartbeat_prod_pycache python3 -m py_compile tools/v7_sync_lib.py tools/v7-safe-deploy
PYTHONPYCACHEPREFIX=/private/tmp/heartbeat_prod_pycache python3 -m unittest tests.unit.test_v7_sync_tools tests.unit.test_runtime_snapshot_fast_path
```

Result:

```text
Ran 24 tests in 1.456s
OK
```

## Full Regression

Command:

```text
PYTHONPYCACHEPREFIX=/private/tmp/heartbeat_prod_pycache python3 -m unittest discover tests
```

Result:

```text
Ran 295 tests in 18.939s
OK
```

## Safety Scan

- runtime_behavior_changed=false for dry-run verification
- governance_behavior_changed=false
- execution_behavior_changed=false
- users_moved=false
- autoswitch_apply_run=false
- new_truth_sources_created=false
- duplicate_systems_created=false

