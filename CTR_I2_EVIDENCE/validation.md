# CTR.I2 Validation Evidence

Date: 2026-06-11

Commands run:

- `python3 -m py_compile admin_core/operator_decision_surface.py admin_core/operator_execution_pipeline.py admin_core/operator_execution_feedback.py admin/v7-admin-api tools/v7-users-autoswitch tests/unit/test_ctr_i2_review_required.py tests/unit/test_ctr_i1_no_bypass.py tests/unit/test_operator_decision_surface.py tests/unit/test_operator_execution_pipeline.py tests/unit/test_operator_execution_feedback.py tests/unit/test_v7_users_autoswitch_policy.py`
- `python3 -m unittest tests.unit.test_ctr_i2_review_required tests.unit.test_ctr_i1_no_bypass tests.unit.test_operator_decision_surface tests.unit.test_operator_execution_pipeline tests.unit.test_operator_execution_feedback tests.unit.test_v7_users_autoswitch_policy tests.unit.test_operator_execution_packet`
- `python3 -m unittest discover tests`
- `git diff --check`

Results:

- py_compile: PASS
- targeted CTR/packet/operator/planner/governance tests: PASS, 135 tests
- full unit suite: PASS, 432 tests
- git diff whitespace check: PASS

Notes:

- Admin API still emits an existing DeprecationWarning for an invalid escape sequence in the large HTML string. This warning existed in the tested file area and is not introduced as a CTR runtime behavior change.

