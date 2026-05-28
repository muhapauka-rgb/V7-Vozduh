# E25.6 Tests and Safety Checks

## Summary

- `tests_passed=true`
- `profile_activated=false`
- `user_movement_performed=false`
- `routing_mutation_performed=false`
- `autoswitch_apply_performed=false`
- `kill_switch_mutation_performed=false`

## Commands

| Command | Result |
| --- | --- |
| `PYTHONPYCACHEPREFIX=.pycache-e25_6 python3 -m py_compile tools/v7-second-canary-target-readiness tools/v7-restore-settle-gate tools/v7-operator-execution-packet admin_core/operator_execution.py tools/v7-users-autoswitch` | PASS |
| `python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate tests.unit.test_operator_execution_packet tests.unit.test_v7_users_autoswitch_policy` | PASS, 47 tests |
| `python3 -m unittest discover tests` | PASS, 116 tests |
| Redacted quarantine hook scan | PASS: no `PostUp`, `PostDown`, `PreUp`, `PreDown`, `ip route`, `ip rule`, `nft`, `iptables`, or `wg-quick` directives in redacted quarantined candidates |
| Disabled draft JSON extraction/validation | PASS |
| VPS runtime checkers | PASS: `v7-reconcile-check`, `v7-user-route-check`, `v7-killswitch-check`, `v7-provisioning-reconcile-check` |
| VPS hidden mover scan | PASS: no active `v7-user-switch`, `v7-routing-sync`, or `v7-users-autoswitch --apply` process |
| Candidate profile offline structural validation | PASS: complete WG client fields, no route hooks; raw full-tunnel detected and blocked from activation |
| Secret scan on E25.6 evidence and final report | PASS |
| Dangerous-call scan | PASS with expected documentation/raw-evidence references only; no execution performed |
| `git diff --check` | PASS |

## Notes

`wg-quick strip` was intentionally not forced against a copied raw key file. It returned a basename/interface-name error for the original candidate path. E25.6 keeps this as an activation-block validation requirement for a normalized `v7execwg0.conf` path instead of copying raw secrets into temporary locations.
