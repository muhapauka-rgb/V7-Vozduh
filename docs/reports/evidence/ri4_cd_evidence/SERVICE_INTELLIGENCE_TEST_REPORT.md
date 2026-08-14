# SERVICE_INTELLIGENCE_TEST_REPORT

## Commands

```bash
PYTHONPYCACHEPREFIX=/private/tmp/ri4cd_pycache python3 -m py_compile admin_core/routing_intelligence.py admin_core/intelligence_workers.py admin_core/intelligence_snapshots.py admin_core/routing_brain.py tools/v7-users-autoswitch
```

Result: PASS

```bash
PYTHONPYCACHEPREFIX=/private/tmp/ri4cd_pycache python3 -m unittest tests.unit.test_routing_intelligence tests.unit.test_intelligence_workers tests.unit.test_routing_brain tests.unit.test_intelligence_snapshots tests.unit.test_runtime_snapshot_fast_path
```

Result:

```text
Ran 52 tests in 0.331s
OK
```

```bash
PYTHONPYCACHEPREFIX=/private/tmp/ri4cd_pycache python3 -m unittest discover tests
```

Result:

```text
Ran 256 tests in 15.739s
OK
```

## Coverage Areas

- service scoring tests;
- service history tests;
- snapshot tests;
- routing brain tests;
- planner advisory tests;
- calibration tests;
- full regression suite.

## Verdict

```text
tests_pass=true
```

