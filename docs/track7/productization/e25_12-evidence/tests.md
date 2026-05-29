# E25.12 Tests And Safety Checks

## Local Tests

| Command | Result | Notes |
| --- | --- | --- |
| `PYTHONPYCACHEPREFIX=/tmp/v7-e25-12-pycache python3 -m py_compile tools/v7-second-canary-target-readiness admin_core/operator_execution.py admin_core/operator_observability.py tools/v7-operator-execution-packet` | PASS | Relevant Python files compile. |
| `python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_operator_execution_packet tests.unit.test_operator_observability` | PASS | `33` tests passed. |
| `python3 -m unittest discover tests` | PASS | `119` tests passed. |
| `tools/v7-admin-endpoint-inventory` | PASS | Endpoint count `211`; POST count `137`; safe-mode blocked count `86`. Generated timestamp-only inventory change was reverted. |
| `rg` credential scan on E25.12 evidence and touched code | PASS | No secrets found. A broad first pass matched shell `awk BEGIN` syntax only; stricter credential scan was clean. |
| `rg` dangerous-call scan on E25.12 evidence and touched code | PASS | No executable movement/apply/route mutation path found. Matches were docs/probe scans only. |
| `git diff --check` | PASS | No whitespace errors. |

## VPS Runtime Tests

| Command | Result | Notes |
| --- | --- | --- |
| `v7-second-canary-target-readiness --execution-target-id amneziawg-exec-20260528-10-8-1-14 --pretty` | PASS | `selected_target=amneziawg-exec-20260528-10-8-1-14`, `approval_status=GO`, `execution_allowed_now=False`. |
| `v7-second-canary-target-readiness --execution-target-id amneziawg-exec-20260528-10-8-1-14 --json` | PASS | JSON parsed with `python3 -m json.tool`. |
| `v7-restore-settle-gate --pre-restore --state-dir /tmp/e25_12_restore_settle_samples --pretty` | PASS | `gate_status=GO`, `sample_count=20`, selected moves all `0`, hidden movers observed `False`. |
| `v7-reconcile-check` | PASS | OK. |
| `v7-user-route-check` | PASS | OK. |
| `v7-killswitch-check` | PASS | OK. |
| `v7-provisioning-reconcile-check` | PASS | OK. |
| hidden mover scan | PASS | `hidden_movers_absent=true`. |
| route/DNS side-effect scan | PASS | Default route via `ens3`; DNS hash stable; table `1009` remains `default dev v7e356a192b79`. |

## Safety Verification

```text
candidate_row=ip=10.7.0.11 current=1 table=1009 enabled=1
table_1009=default dev v7e356a192b79 scope link
selected_moves_zero=true
hidden_movers_absent=true
runtime_checkers_ok=true
```

## Unavailable Tests

None required for E25.12 were skipped. This block did not touch UI or API routes, so no browser render smoke was required.
