# Regression

## Commands Run

```bash
PYTHONPYCACHEPREFIX=/private/tmp/prod_cal_pycache python3 -m py_compile admin_core/intelligence_platform.py
```

Result: PASS.

```bash
PYTHONPYCACHEPREFIX=/private/tmp/prod_cal_pycache python3 -m unittest tests.unit.test_intelligence_platform
```

Result: PASS.

- Ran 14 tests.

```bash
PYTHONPYCACHEPREFIX=/private/tmp/prod_cal_pycache python3 -m unittest discover tests
```

Result: PASS.

- Ran 274 tests.

## Safety Confirmation

- runtime mutation performed: false
- users moved: false
- autoswitch apply performed: false
- deploy performed: false
- commit performed by this program: false
- governance changed: false
- planner ownership changed: false
- execution ownership changed: false
- rollback ownership changed: false
