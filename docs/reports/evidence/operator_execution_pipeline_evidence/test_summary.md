# Test Summary

## Commands

`PYTHONPYCACHEPREFIX=/private/tmp/v7-pycache python3 -m py_compile admin/v7-admin-api admin_core/operator_execution_pipeline.py admin_core/operator_execution.py`

Result: PASS

`PYTHONPYCACHEPREFIX=/private/tmp/v7-pycache python3 -m unittest tests.unit.test_operator_execution_pipeline tests.unit.test_operator_execution_packet tests.unit.test_operator_decision_surface tests.contracts.test_endpoint_inventory`

Result: PASS, 27 tests

`python3 - <<'PY' ... deploy_allowlist_validation() ...`

Result: PASS

`PYTHONPYCACHEPREFIX=/private/tmp/v7-pycache python3 -m unittest discover tests`

Result: PASS, 306 tests

`git diff --check`

Result: PASS

## Endpoint inventory

Generated: `docs/reports/evidence/operator_execution_pipeline_evidence/endpoint_inventory.json`

Summary:

- endpoint_count: 267
- GET: 120
- POST: 139
- HEAD: 8
- read_api: 111
- action: 134
- csrf_required_count: 134
- safe_mode_blocked_count: 86

