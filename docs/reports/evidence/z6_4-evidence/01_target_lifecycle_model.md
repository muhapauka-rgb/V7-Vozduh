# Target Lifecycle Ownership Model

## Future Lifecycle

Signals
-> Health
-> Capacity
-> Trust
-> Policy
-> Eligibility
-> Planner
-> Selected Moves
-> Restore Barrier
-> Runtime Recheck
-> Execution
-> Verification
-> Rollback
-> Audit
-> Closure

## Ownership Table

| Stage | Primary Owner | Secondary Owner | Supporting Owners | Read-only Participants | Legacy Participants |
|---|---|---|---|---|---|
| Signals | Specialized signal writers | Admin/observability | service matrix refresh, Telegram sentinel, quality compact, health/speed/client tooling | Autoswitch readers, Admin views | ad hoc/historical signal captures |
| Health | Existing health/state tooling | Autoswitch consumer | quality compact, speed/client tooling | Admin/operator views | unknown historical health scripts |
| Capacity | `tools/v7-users-autoswitch` for runtime capacity admission | Admin proposal/visibility | registries, load summary | Admin execution previews | historical packet checks |
| Trust | Admin runtime/release trust read model | Autoswitch as future consumer | release/runtime evidence | operator views | historical trust reports |
| Policy | policy/org policy files | Admin policy surface | operator-controlled policy changes | Autoswitch/Admin readers | manual file edits |
| Eligibility | `tools/v7-users-autoswitch` | Admin proposal/gates | service matrix, policy, capacity, trust | Admin/operator views | historical proposals |
| Planner | `tools/v7-users-autoswitch` | Admin dry-run view | signal writers | systemd stdout/journal, Admin plan readers | draft planner timer |
| Selected Moves | `tools/v7-users-autoswitch` | Admin selected-move visibility/gates | restore-settle samples | operator observability | persistent selected-move files |
| Restore Barrier | `tools/v7-users-autoswitch` for runtime barrier authority | Admin closure/visibility | restore-settle gate, operator observability | Admin restore-settle adapter | manual/historical barrier writes |
| Runtime Recheck | `tools/v7-users-autoswitch` | Admin/operator recheck evidence | `admin_core/operator_execution.py`, Admin gates | Admin execution previews | zero-move-only execution engine as movement owner |
| Execution | `tools/v7-users-autoswitch` | Admin controlled action surface | `v7-user-switch` primitive | Admin/operator views | direct CLI/manual authority |
| Verification | `tools/v7-users-autoswitch` | Admin/operator visibility | runtime checkers | operator timeline | manual verification reports |
| Rollback | `tools/v7-users-autoswitch` for movement lifecycle rollback | `v7-rollback-last-change` as generic primitive | Admin rollback surface, proxy guard rollback | rollback preview views | raw fallback rollback commands |
| Audit | `tools/runtime-support/v7-audit-log` | Admin audit wrapper/operator export | service event writers, autoswitch outcomes | Admin audit search | report-only audit |
| Closure | Admin closure model + `admin_core/operator_observability.py` | Autoswitch outcome + `v7-audit-log` | proposal/evidence closure controls | operator timeline/export | markdown closeouts |

## Target Lifecycle Rules

1. Signals may remain distributed, but they are advisory/supporting until consumed by the runtime owner.
2. Eligibility, planning, selected moves, runtime recheck, execution, verification, and movement rollback are runtime-owned.
3. Admin may display, approve, close, and wrap controlled operator actions, but should not own live runtime truth.
4. Audit is canonicalized at `v7-audit-log`; all other audit-like records are supplemental or historical evidence.
5. Closure truth lives in Admin/operator closure records, but must be backed by runtime outcomes and audit events.
6. Systemd starts the cycle; it never owns lifecycle truth.

