# E25.14 Tests

## Local Tests

| Command | Result | Notes |
| --- | --- | --- |
| `PYTHONPYCACHEPREFIX=/tmp/v7-e25-14-pycache python3 -m py_compile tools/v7-second-canary-target-readiness admin_core/operator_execution.py admin_core/operator_observability.py tools/v7-operator-execution-packet` | PASS | Relevant Python files compile. |
| `python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_operator_execution_packet tests.unit.test_operator_observability` | PASS | `33` tests passed. |
| `python3 -m unittest discover tests` | PASS | `119` tests passed. |
| readiness/restore-settle/sample JSON validation | PASS | Evidence JSON parses cleanly. |
| credential scan | PASS | No secrets found. |
| dangerous-call scan | PASS_WITH_EXPECTED_REFERENCES | Only documented fallback command strings and hidden-mover scan pattern were found; no movement command executed. |
| `git diff --check` | PASS | No whitespace errors. |

## Runtime Tests

Runtime tests were executed during the fresh recheck and final safety check:

- `v7-reconcile-check=OK`
- `v7-user-route-check=OK`
- `v7-killswitch-check=OK`
- `v7-provisioning-reconcile-check=OK`
- readiness helper: `GO`
- restore-settle helper: `GO`
- hidden mover scan: absent

## Movement Safety

- authorized forward command executed: `false`
- rollback command executed: `false`
- unauthorized movement: `false`
- autoswitch apply: `false`
- kill-switch control/toggle mutation: `false`

## Unavailable / Not Applicable

True post-execution replay validation was not applicable because the movement was not executed and no success record was written for the packet. Stale-packet denial was verified instead.
