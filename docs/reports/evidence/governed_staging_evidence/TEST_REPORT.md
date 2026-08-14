# TEST_REPORT

Status: PASS

Commands:

```text
PYTHONPYCACHEPREFIX=/private/tmp/gov_pycache python3 -m py_compile admin_core/intelligence_platform.py
```

Result: PASS

```text
PYTHONPYCACHEPREFIX=/private/tmp/gov_pycache python3 -m unittest tests.unit.test_intelligence_platform
```

Result: 10 tests passed.

```text
PYTHONPYCACHEPREFIX=/private/tmp/gov_pycache python3 -m unittest discover tests
```

Result: 270 tests passed.

