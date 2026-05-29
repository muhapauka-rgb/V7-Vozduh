# E25.9 Tests

## Commands

| Command | Result | Notes |
|---|---:|---|
| `PYTHONPYCACHEPREFIX=/tmp/v7_pycache_e25_9 python3 -m py_compile admin_core/operator_execution.py admin_core/operator_observability.py tools/v7-restore-settle-gate tools/v7-second-canary-target-readiness` | PASS | Pycache redirected to writable temp. |
| `python3 -m unittest tests.unit.test_operator_observability tests.contracts.endpoint_inventory_test` | PASS | 18 tests passed. |
| `python3 -m unittest discover tests` | PASS | 116 tests passed. |
| `tools/v7-admin-endpoint-inventory` | PASS | Inventory generated: 211 endpoints. Generated timestamp change was reverted to avoid metadata churn. |
| `git diff --check` | PASS | No whitespace errors. |

## Scans

| Scan | Result | Notes |
|---|---:|---|
| credential scan on E25.9 evidence | PASS | No private keys or preshared keys found. |
| dangerous-call scan | PASS_WITH_EXPECTED_EVIDENCE_REFERENCE | Only the hidden mover `pgrep` evidence line matched command names. No `v7-user-switch`, autoswitch apply, kill switch mutation, profile activation, or user route mutation was executed. |

## VPS Runtime Checks

Captured in `profile-acquisition-check.raw.md`:

- `v7-reconcile-check`: OK
- `v7-user-route-check`: OK
- `v7-killswitch-check`: OK
- `v7-provisioning-reconcile-check`: OK
- `selected_moves=0/absent`
- hidden movers absent
- `v7execwg0` absent
- candidate `10.7.0.11` still on egress `1`

## Not Run

No normalization, activation, target readiness, or long-window tests were run because no new external profile was provided.
