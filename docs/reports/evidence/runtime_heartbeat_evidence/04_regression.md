# Runtime Heartbeat Evidence 04 - Regression

Commands:

```text
PYTHONPYCACHEPREFIX=/private/tmp/runtime_heartbeat_pycache python3 -m unittest tests.unit.test_runtime_snapshot_fast_path
PYTHONPYCACHEPREFIX=/private/tmp/runtime_heartbeat_pycache python3 -m py_compile tools/v7-users-autoswitch tools/v7-intelligence-snapshot-refresh
PYTHONPYCACHEPREFIX=/private/tmp/runtime_heartbeat_pycache python3 -m unittest discover tests
```

Results:

```text
Ran 7 tests in 0.579s
OK

Ran 295 tests in 19.109s
OK
```

Regression verdict:

```text
tests_pass=true
```

