# E25.7 Tests And Safety Checks

## Summary

- `tests_passed=true`
- `profile_activation_attempted=true`
- `profile_activated_then_removed=true`
- `user_movement_performed=false`
- `routing_mutation_for_users=false`
- `autoswitch_apply_performed=false`
- `kill_switch_mutation_performed=false`
- `raw_profile_executed=false`

## Commands

| Command / Check | Result |
| --- | --- |
| `PYTHONPYCACHEPREFIX=.pycache-e25_7 python3 -m py_compile tools/v7-second-canary-target-readiness tools/v7-restore-settle-gate tools/v7-operator-execution-packet admin_core/operator_execution.py tools/v7-users-autoswitch` | PASS |
| `python3 -m unittest tests.unit.test_v7_second_canary_target_readiness tests.unit.test_v7_restore_settle_gate tests.unit.test_operator_execution_packet tests.unit.test_v7_users_autoswitch_policy` | PASS, 47 tests |
| `python3 -m unittest discover tests` | PASS, 116 tests |
| Credential scan on E25.7 evidence | PASS |
| Route/DNS side-effect scan | PASS: default route unchanged, resolver hash unchanged, candidate route unchanged |
| Normalized config safety scan | PASS: `Table=off`, no unsafe directives |
| Dangerous-call scan | PASS with expected checker-source references only; no `v7-user-switch`, autoswitch apply, kill-switch mutation, or user routing command executed |
| VPS runtime checkers after rollback | PASS: reconcile, user-route, killswitch, provisioning reconcile |
| Hidden mover scan | PASS |

## Target Connectivity

The target-local probe failed:

```text
ping -c 3 -W 3 -I v7execwg0 1.1.1.1
3 packets transmitted, 0 received
ping_exit=1
```

This is a validation failure for the candidate endpoint/profile, not a governance side-effect failure. The interface was removed immediately after this result.

