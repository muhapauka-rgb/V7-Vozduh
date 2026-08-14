# Program A.C Test Results

Date: 2026-06-02

## Commands

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch
```

Result: PASS

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests/unit/test_best_available_pool_policy.py
```

Result: PASS, 6 tests OK

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests/unit/test_service_aware_policy.py tests/unit/test_best_available_pool_policy.py
```

Result: PASS, 14 tests OK

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests/unit/test_v7_users_autoswitch_policy.py
```

Result: PASS, 22 tests OK

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests/unit/test_v7_truth_check.py tests/unit/test_v7_sync_tools.py
```

Result: PASS, 30 tests OK

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests/unit/test_service_aware_policy.py tests/unit/test_best_available_pool_policy.py tests/unit/test_v7_users_autoswitch_policy.py tests/unit/test_v7_truth_check.py tests/unit/test_v7_sync_tools.py
```

Result: PASS, 66 tests OK

## Coverage Summary

Program A.B service-aware safety coverage remains active:

- VLESS protocol-limited suspect can be eligible only with service evidence and contextual quality proof.
- FAIL/fatal suspect remains hard-blocked.
- Missing explicit required service evidence remains hard-blocked.
- Weak AWG remains blocked by quality/service gates.
- Reservation/manual-only hard gates remain preserved.
- Service suitability is scored as service evidence, not generic Mbps.
- Relative improvement and sticky preservation remain covered.

Program A.C pool/capacity coverage:

- Best available pool includes close suitable candidates.
- Unsafe route-class FAIL candidate is excluded from pool and movement.
- Capacity signal does not admit unsafe candidates.
- Projected move selection distributes across multiple close suitable pool members.
- Reserved canary pool candidate remains blocked.
- Sticky behavior is preserved when improvement is weak.

## Test Verdict

tests_pass=true
