# Test Evidence

## Targeted Tests

Command:

```text
PYTHONPYCACHEPREFIX=/private/tmp/prod_shadow_pycache python3 -m unittest tests.unit.test_intelligence_platform
```

Observed:

```text
Ran 17 tests
OK
```

## Compile Check

Command:

```text
PYTHONPYCACHEPREFIX=/private/tmp/prod_shadow_pycache python3 -m py_compile admin_core/intelligence_platform.py
```

Observed:

```text
PASS
```

## Full Regression

Command:

```text
PYTHONPYCACHEPREFIX=/private/tmp/prod_shadow_pycache python3 -m unittest discover tests
```

Observed:

```text
Ran 280 tests
OK
```

