# INTELLIGENCE_TEST_REPORT

## Commands

```bash
PYTHONPYCACHEPREFIX=/private/tmp/intel_platform_pycache python3 -m py_compile admin_core/intelligence_platform.py admin_core/intelligence_workers.py admin_core/routing_intelligence.py admin_core/intelligence_snapshots.py tools/v7-users-autoswitch
```

Result: PASS

```bash
PYTHONPYCACHEPREFIX=/private/tmp/intel_platform_pycache python3 -m unittest tests.unit.test_intelligence_platform tests.unit.test_intelligence_workers tests.unit.test_routing_intelligence tests.unit.test_intelligence_snapshots tests.unit.test_runtime_snapshot_fast_path tests.unit.test_routing_brain
```

Result:

```text
Ran 60 tests in 0.372s
OK
```

```bash
PYTHONPYCACHEPREFIX=/private/tmp/intel_platform_pycache python3 -m unittest discover tests
```

Initial result: failed due deploy allowlist gap for new `admin_core/intelligence_platform.py`.

Closure:

- added `admin_core/intelligence_platform.py` to `tools/v7_sync_lib.APPROVED_DEPLOY_FILES`;
- added regression assertions in `tests/unit/test_v7_sync_tools.py`.

Final result:

```text
Ran 264 tests in 15.676s
OK
```

## Verdict

```text
tests_pass=true
problem_closure_rule_applied=true
```

