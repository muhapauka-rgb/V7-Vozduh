# E25.13 Tests And Safety Checks

## Local Tests

| Command | Result | Notes |
| --- | --- | --- |
| `PYTHONPYCACHEPREFIX=/tmp/v7-e25-13-pycache python3 -m py_compile tools/v7-second-canary-target-readiness admin_core/operator_execution.py admin_core/operator_observability.py tools/v7-operator-execution-packet` | PASS | Relevant Python files compile. |
| `python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_operator_execution_packet tests.unit.test_operator_observability` | PASS | `33` tests passed. |
| `python3 -m unittest discover tests` | PASS | `119` tests passed. |
| packet/readiness/restore-settle JSON validation with `python3 -m json.tool` | PASS | Packet and evidence JSON parse cleanly. |
| replay/denial semantic tests | PASS | `13` denial cases passed. |
| credential scan | PASS | No private keys, preshared keys, passwords, bearer tokens, or authorization headers found. |
| dangerous-call scan | PASS_WITH_EXPECTED_REFERENCES | Found only documented next-block raw fallback strings and read-only helper disclaimer; no command was executed. |
| `git diff --check` | PASS | No whitespace errors. |

## VPS Runtime Tests

| Command | Result | Notes |
| --- | --- | --- |
| `v7-reconcile-check` | PASS | OK. |
| `v7-user-route-check` | PASS | OK. |
| `v7-killswitch-check` | PASS | OK. |
| `v7-provisioning-reconcile-check` | PASS | OK. |
| hidden mover scan | PASS | `hidden_movers_absent=true`. |
| `v7-second-canary-target-readiness --execution-target-id amneziawg-exec-20260528-10-8-1-14 --pretty` | PASS | `selected_target=amneziawg-exec-20260528-10-8-1-14`, `approval_status=GO`, `execution_allowed_now=False`. |
| `v7-restore-settle-gate --pre-restore --state-dir /tmp/e25_13_restore_settle_samples --pretty` | PASS | `gate_status=GO`, `sample_count=3`, `checkers_ok=True`, `hidden_movers_observed=False`. |
| candidate route check | PASS | `10.7.0.11` still on `1`; table `1009` unchanged. |

## Safety Confirmation

No E25.13 test executed:

- `v7-user-switch`
- `v7-users-autoswitch --apply`
- broad `v7-routing-sync`
- kill-switch control/toggle
- user route mutation
- canary/cohort movement

## Unavailable Tests

None required for E25.13 were skipped. UI smoke was not applicable because UI was not touched.
