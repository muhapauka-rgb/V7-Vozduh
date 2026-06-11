# CTR.I1 Validation Evidence

Date: 2026-06-11

Commands run:

- `env PYTHONPYCACHEPREFIX=/Users/ponch/Documents/New\ project/.pycache-codex python3 -m py_compile tools/v7-users-autoswitch admin_core/operator_decision_surface.py admin_core/operator_execution_pipeline.py admin/v7-admin-api tests/unit/test_ctr_i1_no_bypass.py tests/unit/test_operator_decision_surface.py tests/unit/test_operator_execution_pipeline.py tests/unit/test_v7_users_autoswitch_policy.py`
- `env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.unit.test_ctr_i1_no_bypass tests.unit.test_operator_decision_surface tests.unit.test_operator_execution_pipeline tests.unit.test_v7_users_autoswitch_policy`
- `env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover tests`
- `git diff --check`

Results:

- py_compile: PASS
- targeted CTR/operator/autoswitch tests: PASS, 109 tests
- full unit suite: PASS, 427 tests
- git diff whitespace check: PASS

Runtime actions:

- users_moved=0
- autoswitch_apply_run=false
- runtime_mutation_performed=false
- deploy_performed=false
