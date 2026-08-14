# API.2 Test Results

## Registry View Unit Tests

```bash
python3 -m unittest tests.unit.test_admin_registry_views
```

Result: `OK`

- tests run: `5`

## Compile Check

```bash
PYTHONPYCACHEPREFIX=/tmp/api2_pycache python3 -m py_compile admin/v7-admin-api admin_core/admin_registry_views.py
```

Result: `OK`

Note: `PYTHONPYCACHEPREFIX` was used to keep bytecode writes outside the repository.

## Full Unit Suite

```bash
python3 -m unittest discover tests
```

Result: `OK`

- tests run: `205`

## Endpoint Inventory

Before and after endpoint inventory commands completed successfully.

- endpoint count unchanged: `true`
- stable endpoint definitions unchanged: `true`
