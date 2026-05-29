# E26 Tests And Safety Checks

## Read-Only Runtime Checks

| Check | Result | Evidence |
|---|---:|---|
| `v7-reconcile-check` | PASS | `post-movement-runtime-review.md` |
| `v7-user-route-check` | PASS | `post-movement-runtime-review.md` |
| `v7-killswitch-check` | PASS | `post-movement-runtime-review.md` |
| `v7-provisioning-reconcile-check` | PASS | `post-movement-runtime-review.md` |
| Hidden mover scan | PASS | No matching active mover processes in `post-movement-runtime-review.md`. |
| Readiness helper explicit execution target | PASS | `approval_status=GO`, `second_canary_readiness=GO`. |
| Restore-settle helper fresh samples | PASS | `gate_status=GO`, `sample_count=3`, `apply_timer_intervals_covered=2.85`. |
| Audit validation | PASS | Forward, rollback, and replay denial records found in operator execution audit. |

## Local Checks

| Command | Result |
|---|---:|
| `PYTHONPYCACHEPREFIX=.pycache python3 -m compileall admin_core tools tests` | PASS |
| `PYTHONPYCACHEPREFIX=.pycache python3 -m unittest tests.unit.test_operator_execution_packet tests.unit.test_v7_second_canary_target_readiness` | PASS, 20 tests |
| `python3 -m unittest discover` | PASS, 119 tests |
| Credential scan on E26 evidence | PASS |
| Dangerous-call scan on E26 evidence | PASS with expected hidden-mover scan and report text references only |
| `git diff --check` | PASS |

Initial `compileall` without `PYTHONPYCACHEPREFIX` failed because the sandbox blocked writes to the default macOS Python cache under `~/Library/Caches`. The command was rerun with workspace-local pycache and passed.

## Mutation Statement

`runtime_mutation_performed=false`

No user movement, user route mutation, kill switch mutation, autoswitch apply, canary, or cohort execution was performed during E26.
