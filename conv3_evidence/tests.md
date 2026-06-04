# CONV.3 Test Evidence

## Targeted Tests

Command:

```text
python3 -m unittest tests.unit.test_v7_sync_tools tests.unit.test_v7_truth_check
```

Observed result:

```text
Ran 37 tests
OK
```

## Full Regression

Command:

```text
PYTHONPYCACHEPREFIX=/private/tmp/conv3_pycache python3 -m unittest discover tests
```

Observed result:

```text
Ran 277 tests
OK
```
