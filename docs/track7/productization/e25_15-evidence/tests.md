# E25.15 Tests

## Local Tests

| Command | Result | Notes |
| --- | --- | --- |
| `PYTHONPYCACHEPREFIX=/tmp/v7-e25-15-pycache python3 -m py_compile tools/v7-second-canary-target-readiness admin_core/operator_execution.py admin_core/operator_observability.py tools/v7-operator-execution-packet` | PASS | Relevant Python files compile. |
| `python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_operator_execution_packet tests.unit.test_operator_observability` | PASS | `33` tests passed. |
| `python3 -m unittest discover tests` | PASS | `119` tests passed. |
| packet/readiness/restore-settle/sample JSON validation | PASS | Evidence JSON parses cleanly. |
| credential scan | PASS | No secrets found. |
| dangerous-call scan | PASS_WITH_EXPECTED_EXECUTION_REFERENCES | Found only the approved E25.15 `v7-user-switch` forward/rollback commands plus hidden-mover scan pattern. No autoswitch apply, broad routing sync, kill-switch toggle, canary, or cohort command found. |
| `git diff --check` | PASS | No whitespace errors. |

## Runtime Tests

Runtime checks passed before movement, after forward movement, after rollback, and during delayed monitoring:

- `v7-reconcile-check=OK`
- `v7-user-route-check=OK`
- `v7-killswitch-check=OK`
- `v7-provisioning-reconcile-check=OK`
- hidden movers absent
- selected moves zero
- restore-settle gate `GO`

## Movement Safety

- forward command executed: `v7-user-switch 10.7.0.11 amneziawg-exec-20260528-10-8-1-14`
- rollback command executed: `v7-user-switch 10.7.0.11 1`
- only approved user moved: `true`
- out-of-scope user `10.7.0.16` unchanged: `true`
- autoswitch apply: `false`
- canary/cohort: `false`
