# API.4 Test Results

## Compile

```bash
PYTHONPYCACHEPREFIX=/tmp/api4_pycache python3 -m py_compile admin/v7-admin-api admin_core/overview_views.py admin_core/performance_summaries.py
```

Result: `OK`

## Focused API.4 Tests

```bash
python3 -m unittest tests.unit.test_api4_overview_performance
```

Result: `OK`

- tests run: `5`

## Full Test Suite

```bash
python3 -m unittest discover tests
```

Result: `OK`

- tests run: `216`

## Endpoint Inventory

- endpoint count unchanged: `true`
- stable endpoint definitions unchanged: `true`
