# PROGRAM A.B Test Results

All tests were run locally. No production mutation, autoswitch apply, user movement, routing mutation, service restart, or restore barrier mutation was performed.

## Syntax

Command:

`PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7-users-autoswitch`

Result: PASS

## New Service-Aware Tests

Command:

`PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests/unit/test_service_aware_policy.py`

Result:

- Ran 8 tests
- OK

Coverage:

- VLESS protocol-limited SUSPECT can be eligible with service evidence.
- FAIL severity remains hard block.
- Fatal SUSPECT remains hard block.
- Missing required service evidence blocks.
- Weak AWG remains blocked.
- Reservation/manual gates remain hard.
- Service suitability is not generic Mbps.
- Relative improvement/sticky behavior remains preserved.

## Required Autoswitch Policy Tests

Command:

`PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests/unit/test_v7_users_autoswitch_policy.py`

Result:

- Ran 22 tests
- OK

## Required Truth Check Tests

Command:

`PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests/unit/test_v7_truth_check.py`

Result:

- Ran 20 tests
- OK

## Required Sync Tool Tests

Command:

`PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests/unit/test_v7_sync_tools.py`

Result:

- Ran 10 tests
- OK

## Combined Final Local Test Pass

Command:

`PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests/unit/test_service_aware_policy.py tests/unit/test_v7_users_autoswitch_policy.py tests/unit/test_v7_truth_check.py tests/unit/test_v7_sync_tools.py`

Result:

- All required suites passed in separate runs.
- Total local tests covered in A.B: 60.

