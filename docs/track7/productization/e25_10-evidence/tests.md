# E25.10 Tests And Safety Checks

## Local Tests

| Command | Result | Notes |
| --- | --- | --- |
| `PYTHONPYCACHEPREFIX=/tmp/v7-e25-10-pycache python3 -m py_compile admin_core/operator_execution.py admin_core/operator_observability.py tools/v7-operator-execution-packet` | PASS | Relevant admin/operator files compile. |
| `python3 -m unittest tests.unit.test_operator_execution_packet tests.unit.test_operator_observability tests.contracts.endpoint_inventory_test` | PASS | `Ran 25 tests in 0.371s`. |
| `python3 -m unittest discover tests` | PASS | `Ran 116 tests in 7.553s`. |
| `tools/v7-admin-endpoint-inventory` | PASS | Inventory command completed; generated timestamp-only diff was restored to avoid metadata churn. |
| `git diff --check` | PASS | No whitespace errors. |

## Runtime Checks

| Command | Result | Notes |
| --- | --- | --- |
| `v7-reconcile-check` | PASS | OK after metadata/interface rollback. |
| `v7-user-route-check` | PASS | OK after metadata/interface rollback. |
| `v7-killswitch-check` | PASS | OK after metadata/interface rollback. |
| `v7-provisioning-reconcile-check` | PASS | OK after metadata/interface rollback. |
| hidden mover scan | PASS | No persistent hidden movers observed; pgrep output during commands matched the current inspection command itself. |
| selected moves scan | PASS | No selected-move files found in the checked runtime state path. |

## Profile And Side-Effect Checks

| Check | Result | Notes |
| --- | --- | --- |
| endpoint self-reference check | PASS | Endpoint routed externally via `ens3`, not `lo`. |
| raw profile execution check | PASS | Raw operator-provided profile was not executed. |
| normalized activation check | PASS | `v7execwg0` activated only through `/etc/amnezia/v7execwg0.conf`. |
| route side-effect scan | PASS | Default route and user table `1009` stayed unchanged during activation. |
| DNS side-effect scan | PASS | Global DNS state stayed unchanged; normalized config removed `DNS`. |
| credential scan | PASS_WITH_REDACTED_MATCHES | Only `<redacted>` placeholders and endpoint port were found in evidence; no raw private key or preshared key was written. |
| dangerous-call scan | PASS_WITH_DOCUMENTED_ACTIVATION | Evidence documents `awg-quick up` for normalized activation only; no `v7-user-switch`, autoswitch apply, kill-switch mutation, or user routing mutation occurred. |

## Unavailable Or Not Applicable

- Static `/admin-v2` render smoke: not applicable; no UI files were touched in E25.10.
- Long-window readiness validation: not run because active egress metadata caused checker failures until NAT/MSS/checker integration exists.
