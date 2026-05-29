# E25.11 Tests And Safety Checks

## Local Tests

| Command | Result | Notes |
| --- | --- | --- |
| `PYTHONPYCACHEPREFIX=/tmp/v7-e25-11-pycache python3 -m py_compile tools/v7-second-canary-target-readiness admin_core/operator_execution.py admin_core/operator_observability.py tools/v7-operator-execution-packet` | PASS | Relevant helper/operator files compile. |
| `python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_operator_execution_packet tests.unit.test_operator_observability tests.contracts.endpoint_inventory_test` | PASS | `Ran 38 tests in 0.334s`. |
| `python3 -m unittest discover tests` | PASS | `Ran 119 tests in 7.226s`. |
| `tools/v7-admin-endpoint-inventory` | PASS | Inventory command completed; timestamp-only generated diff was restored. |
| `git diff --check` | PASS | No whitespace errors. |

## Runtime Tests

| Command / Check | Result | Notes |
| --- | --- | --- |
| `v7-reconcile-check` | PASS | OK with `v7execwg0` active and metadata present. |
| `v7-user-route-check` | PASS | OK; `10.7.0.11` table still routes through `v7e356a192b79`. |
| `v7-killswitch-check` | PASS | OK after `v7execwg0` NAT/MSS integration. |
| `v7-provisioning-reconcile-check` | PASS | OK after `v7execwg0` NAT/MSS integration. |
| `v7-second-canary-target-readiness --execution-target-id amneziawg-exec-20260528-10-8-1-14` | PASS_WITH_NO_GO | Helper supports execution-only mode; final target status is `NO-GO` after long-window quality metrics. |
| `v7-restore-settle-gate --pre-restore --state-dir docs/track7/productization/e25_11-evidence/restore-settle-samples` | PASS | Gate status `GO`. |

## Scans

| Scan | Result | Notes |
| --- | --- | --- |
| credential scan | PASS | No raw private key, preshared key, or endpoint secret was found in E25.11 evidence. |
| dangerous-call scan | PASS_WITH_EXPECTED_PROFILE_ACTIVATION | Evidence includes normalized `awg-quick up`; no `v7-user-switch`, no autoswitch apply, no kill-switch toggle, no user route mutation. |
| route side-effect scan | PASS | Default route and user table `1009` remained unchanged during activation and integration. |
| DNS side-effect scan | PASS | DNS remained unchanged; normalized profile has no DNS setting. |

## Unavailable / Not Applicable

- Static `/admin-v2` render smoke: not applicable; E25.11 touched no UI.
- Dedicated long-window sustained GO: attempted and completed as 19 valid samples after SSH reset before sample 20; result is `NO-GO` due quality below floor.
