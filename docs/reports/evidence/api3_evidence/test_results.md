# API.3 Test Results

## Compile

```bash
PYTHONPYCACHEPREFIX=/tmp/api3_pycache python3 -m py_compile admin/v7-admin-api admin_core/operator_views.py admin_core/service_views.py admin_core/route_views.py admin_core/summary_builders.py
```

Result: `OK`

## Focused API.3 Tests

```bash
python3 -m unittest tests.unit.test_api3_read_only_views
```

Result: `OK`

- tests run: `6`

## Full Test Suite

```bash
python3 -m unittest discover tests
```

Result: `OK`

- tests run: `211`

## Endpoint Inventory

Before and after endpoint inventory commands completed successfully.

- endpoint count unchanged: `true`
- stable endpoint definitions unchanged: `true`
