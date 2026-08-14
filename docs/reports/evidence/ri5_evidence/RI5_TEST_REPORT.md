# RI5_TEST_REPORT

## Commands

```bash
PYTHONPYCACHEPREFIX=/private/tmp/ri5_pycache python3 -m py_compile admin_core/routing_intelligence.py admin_core/intelligence_workers.py admin_core/intelligence_snapshots.py admin_core/routing_brain.py tools/v7-users-autoswitch
```

Result: PASS

```bash
PYTHONPYCACHEPREFIX=/private/tmp/ri5_pycache python3 -m unittest tests.unit.test_routing_intelligence tests.unit.test_intelligence_workers tests.unit.test_intelligence_snapshots tests.unit.test_runtime_snapshot_fast_path tests.unit.test_routing_brain
```

Result:

```text
Ran 55 tests in 0.418s
OK
```

```bash
PYTHONPYCACHEPREFIX=/private/tmp/ri5_pycache python3 -m unittest discover tests
```

Result:

```text
Ran 259 tests in 17.700s
OK
```

## Verdict

```text
tests_pass=true
```

