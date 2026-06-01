# Authority Reduction Plan

This is an ownership design, not an implementation plan.

## Future Authority Classification

| Path / Component | Future Role | Remain Authority | Become Secondary | Become Advisory | Become Legacy | Become Break-Glass Only |
|---|---|---:|---:|---:|---:|---:|
| `tools/v7-users-autoswitch` | Primary runtime/execution owner | yes | no | no | no | no |
| systemd autoswitch timer/service | Scheduler-only | yes, scheduler only | no | no | no | no |
| Admin autoswitch apply | Controlled operator surface invoking runtime owner | no as lifecycle owner | yes | no | no | no |
| Admin direct user switch | Controlled/manual operator surface | no as lifecycle owner | limited | no | no | yes for exceptional movement |
| CLI `v7-user-switch` | Low-level primitive | no as lifecycle owner | no | no | no | yes |
| Sentinel execution path | Signal path only | no | no | yes | no | no |
| Draft planner | Dormant draft | no | no | no | yes / do not touch | no |
| Persistent selected-move files | Read/evidence adapters | no | no | yes as evidence | yes as authority | no |
| Generic rollback | Low-level rollback primitive | no as lifecycle owner | yes | no | no | yes for emergency |
| Admin execution contracts | Preview/governance/read model | no current execution authority | yes | yes until connected | no | no |
| Operator execution zero-move engine | Governance/recheck support | no movement authority | yes | no | no | no |
| Historical reports/packets | Evidence | no | no | yes | yes as authority | no |

## Reduction Rules

1. Direct movement authority should converge behind the runtime owner.
2. Admin should remain the surface for humans, not the source of live movement truth.
3. CLI mutation tools should be primitives or break-glass paths only.
4. Sentinel must be advisory/signal-only.
5. Draft planner must not become an active scheduler/planner truth.
6. Persistent selected-move files must not become canonical selected-move truth.
7. Generic rollback must remain a primitive, not the owner of operation rollback lifecycle.
8. Audit and closure should reuse existing `v7-audit-log` and Admin closure records.

