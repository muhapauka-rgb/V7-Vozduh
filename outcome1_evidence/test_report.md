# Test Report

## Py Compile

Command:

`PYTHONPYCACHEPREFIX=/private/tmp/outcome1_pycache python3 -m py_compile admin_core/intelligence_workers.py admin_core/intelligence_platform.py tools/v7-intelligence-snapshot-refresh`

Result: PASS.

## Targeted Tests

Command:

`PYTHONPYCACHEPREFIX=/private/tmp/outcome1_pycache python3 -m unittest tests.unit.test_intelligence_workers`

Result:

`Ran 25 tests in 0.226s`

`OK`

## Full Regression

Command:

`PYTHONPYCACHEPREFIX=/private/tmp/outcome1_pycache python3 -m unittest discover tests`

Result:

`Ran 290 tests in 20.056s`

`OK`
