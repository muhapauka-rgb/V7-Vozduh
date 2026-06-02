# Z8.12 Test Results

Command:

```text
python3 -m unittest tests/unit/test_v7_truth_check.py tests/unit/test_p2_7_candidate_workflow.py
```

Result:

```text
Ran 24 tests
OK
```

Additional checks:

```text
PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache python3 -m py_compile tools/v7-truth-check
git diff --check
```

Result: PASS.

## Required policy cases covered

- runtime file dirty -> FAIL
- autoswitch dirty -> FAIL
- admin API dirty -> FAIL
- systemd dirty -> FAIL
- report file dirty -> PASS with warning
- evidence file dirty -> PASS with warning
- docs dirty -> PASS with warning
- runtime-relevant test dirty -> PASS with warning
- mixed runtime + docs dirty -> FAIL

