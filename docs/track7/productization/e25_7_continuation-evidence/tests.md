# E25.7 Continuation Tests

## Local Tests

| Command | Result | Notes |
|---|---:|---|
| `python3 -m py_compile ...` | FAIL | macOS Python tried to write cache under `/Users/ponch/Library/Caches/...`, outside sandbox. |
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache_e25_7_cont python3 -m py_compile admin_core/operator_execution.py admin_core/operator_observability.py tools/v7-restore-settle-gate tools/v7-second-canary-target-readiness` | PASS | Cache redirected to writable temp. |
| `python3 -m unittest tests.unit.test_operator_observability tests.contracts.endpoint_inventory_test` | PASS | 18 tests passed. |
| `python3 -m unittest discover tests` | PASS | 116 tests passed. |
| `tools/v7-admin-endpoint-inventory` | PASS | Inventory generated: 211 endpoints. |
| `git diff --check` | PASS | No whitespace errors in current diff. |

## Scans

| Scan | Result | Notes |
|---|---:|---|
| credential scan on continuation evidence | PASS_WITH_REDACTED_HITS | Only `<redacted>` placeholders were found. No raw private or preshared keys found. |
| dangerous-call scan | PASS_WITH_EXPECTED_EVIDENCE_REFERENCES | Hits were evidence lines for hidden mover scans (`pgrep`) and allowed `wg-quick up v7execwg0`; no `v7-user-switch`, autoswitch apply, kill switch mutation, or user route mutation was executed. |

## VPS Runtime Checks

Captured in raw evidence:

- `v7-reconcile-check`: OK
- `v7-user-route-check`: OK
- `v7-killswitch-check`: OK
- `v7-provisioning-reconcile-check`: OK
- hidden mover scan: absent
- selected moves: absent/zero

## Unavailable / Not Run

- Long-window validation: not run because connectivity never became usable.
- Target readiness GO validation: not applicable; target had no handshake/RX and remains NO-GO.
