# E25.8 Tests

## Commands

| Command | Result | Notes |
|---|---:|---|
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache_e25_8 python3 -m py_compile admin_core/operator_execution.py admin_core/operator_observability.py tools/v7-restore-settle-gate tools/v7-second-canary-target-readiness` | PASS | Local pycache redirected to writable temp. |
| `python3 -m unittest tests.unit.test_operator_observability tests.contracts.endpoint_inventory_test` | PASS | 18 tests passed. |
| `python3 -m unittest discover tests` | PASS | 116 tests passed. |
| `tools/v7-admin-endpoint-inventory` | PASS | Inventory generated: 211 endpoints. Generated timestamp file was not retained as a source change. |
| `git diff --check` | PASS | No whitespace errors. |

## Scans

| Scan | Result | Notes |
|---|---:|---|
| credential scan | PASS_WITH_REDACTED_HITS | Only `<redacted>` placeholders were found. |
| dangerous-call scan | PASS | No `v7-user-switch`, autoswitch apply, kill switch mutation, or user route-table mutation found in generated evidence. |

## VPS Runtime Checks

Captured in raw evidence:

- `v7-reconcile-check`: OK
- `v7-user-route-check`: OK
- `v7-killswitch-check`: OK
- `v7-provisioning-reconcile-check`: OK
- selected moves: absent/zero
- hidden movers: absent

## Not Run

- Target readiness helper and long-window validation were not run because the profile never reached the required handshake/RX connectivity gate.
