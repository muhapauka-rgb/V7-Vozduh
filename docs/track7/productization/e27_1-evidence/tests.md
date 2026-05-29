# E27.1 Tests And Safety Checks

## Runtime Checks

| Check | Result | Evidence |
|---|---:|---|
| `v7-reconcile-check` | PASS | `capacity-requalification.md`, `governance-review.md`, long-window samples |
| `v7-user-route-check` | PASS | `capacity-requalification.md`, `governance-review.md`, long-window samples |
| `v7-killswitch-check` | PASS | `capacity-requalification.md`, `governance-review.md`, long-window samples |
| `v7-provisioning-reconcile-check` | PASS | `capacity-requalification.md`, `governance-review.md`, long-window samples |
| Hidden mover scan | PASS | No active mover processes in snapshot, long-window, or restore-settle samples. |
| Readiness helper | PASS | Explicit execution target mode returned GO after requalification. |
| Restore-settle helper | PASS | `gate_status=GO`, `sample_count=3`, `apply_timer_intervals_covered=2.95`. |
| Target-local capacity probes | PASS | 5MB two-probe min `13.02 Mbps`; long-window min `19.037 Mbps`. |

## Local Checks

| Command | Result |
|---|---:|
| `PYTHONPYCACHEPREFIX=.pycache python3 -m compileall admin_core tools tests` | PASS |
| `PYTHONPYCACHEPREFIX=.pycache python3 -m unittest tests.unit.test_operator_execution_packet tests.unit.test_v7_second_canary_target_readiness` | PASS, 20 tests |
| `python3 -m unittest discover` | PASS, 119 tests |
| Credential scan on E27.1 evidence | PASS |
| Dangerous-call scan on E27.1 evidence | PASS with expected hidden-mover scan text reference only |
| `git diff --check` | PASS |

## Mutation Statement

`runtime_mutation_performed=true`

Mutation scope:

```text
only target capacity metadata for amneziawg-exec-20260528-10-8-1-14:
soft_limit=1 hard_limit=1 -> soft_limit=2 hard_limit=2
```

No user movement, user route mutation, kill switch control/toggle mutation, autoswitch apply, canary, or cohort execution was performed.

