# CONV.1 Verification Evidence

## Commands Run

```text
PYTHONPYCACHEPREFIX=.pycache_tmp python3 -m py_compile tools/v7_sync_lib.py tools/v7-truth-check tools/v7-convergence-status tools/v7-safe-deploy tools/v7-release-sync
```

Result: PASS

```text
PYTHONPYCACHEPREFIX=.pycache_tmp python3 -m unittest tests.unit.test_v7_sync_tools tests.unit.test_v7_truth_check
```

Result: PASS, 34 tests

```text
PYTHONPYCACHEPREFIX=.pycache_tmp python3 -m unittest discover tests
```

Result: PASS, 249 tests

```text
git diff --check
```

Result: PASS

## Safety

No deploy was run.
No users were moved.
No autoswitch apply was run.
No runtime routes were mutated.
No timers were created.
No services were restarted.

