# Z6.7 Evidence 02 - Program Boundary and Orchestrator Loop

## Runtime Orchestrator Program Boundary

The Runtime Orchestrator Program is not a new process, service, or storage system in Z6.7. It is the formal ownership boundary around existing V7 components.

Canonical program root:

- `tools/v7-users-autoswitch`

Canonical scheduler:

- `systemd/v7-users-autoswitch.timer`
- `systemd/v7-users-autoswitch.service`

Canonical audit owner:

- `tools/runtime-support/v7-audit-log`

Canonical closure owner:

- Admin closure model in `admin/v7-admin-api`
- Closure/operation summaries in `admin_core/operator_observability.py`

## Responsibilities Owned by Runtime Orchestrator Program

| Responsibility | Owner Inside Program |
|---|---|
| Runtime cycle start | systemd autoswitch timer/service |
| Runtime operation creation/binding | autoswitch runtime owner, using canonical `operation_id` semantics |
| Planning | `tools/v7-users-autoswitch` |
| Selected move ownership | `tools/v7-users-autoswitch` |
| Restore barrier check | `tools/v7-users-autoswitch` |
| Runtime recheck | `tools/v7-users-autoswitch` |
| Normal execution | `tools/v7-users-autoswitch` through `v7-user-switch` |
| Verification | `tools/v7-users-autoswitch` |
| Movement rollback | `tools/v7-users-autoswitch` rollback branch for verify failure |
| Runtime terminal verdict | `tools/v7-users-autoswitch` |
| Audit completion | `tools/runtime-support/v7-audit-log` |
| Closure completion | Admin closure model and operator observability |

## Responsibilities Not Owned by Runtime Orchestrator Program

| Responsibility | Owner / Treatment |
|---|---|
| Signal production | Existing signal programs; they are inputs, not orchestrators. |
| Scheduler clock ownership | systemd only; autoswitch does not own timer mechanics. |
| Admin UX/API | Admin program; may invoke or observe orchestrator but is not the runtime owner. |
| Audit sink implementation | `v7-audit-log`; orchestrator emits or delegates audit, does not replace sink. |
| Closure store implementation | Admin closure model; orchestrator supplies terminal facts. |
| Generic rollback implementation | `v7-rollback-last-change`; primitive only, not lifecycle owner. |
| Direct manual mutation | Break-glass only, outside normal program path. |
| New storage/API/service creation | Out of scope for Z6.7. |

## Orchestrator Loop

Canonical loop design using existing components:

1. Signal programs refresh health/capacity/runtime evidence.
2. `systemd/v7-users-autoswitch.timer` starts the cycle.
3. `systemd/v7-users-autoswitch.service` invokes `tools/v7-users-autoswitch --apply`.
4. Autoswitch binds or creates the semantic runtime operation identity.
5. Autoswitch reads runtime truth, generation state, policy state, health state, and restore-barrier state.
6. Autoswitch plans candidate movement.
7. Autoswitch computes selected moves and selected move hash.
8. Autoswitch performs restore-barrier and generation clearance checks.
9. Autoswitch performs runtime recheck immediately before execution.
10. If blocked, denied, dry-run, disabled, observe-only, or no selected moves, autoswitch emits terminal no-op/deny result.
11. If allowed, autoswitch executes selected moves through `v7-user-switch`.
12. Autoswitch verifies route/proxy/runtime result.
13. If verification fails and rollback policy allows it, autoswitch enters rollback branch and invokes rollback movement to previous egress.
14. Autoswitch emits terminal runtime verdict.
15. Runtime verdict is audited through `v7-audit-log`.
16. Admin/operator closure consumes operation facts and records VERIFIED, CLOSED, EXPIRED, or reopened lifecycle facts.

## Program End

The runtime cycle does not truly end at process exit. Process exit is only command completion.

Program end is:

`runtime_terminal_state -> audit_recorded -> closure_state_resolved`

If audit or closure is missing, the runtime cycle is terminal from the executor perspective but incomplete from the program perspective.

