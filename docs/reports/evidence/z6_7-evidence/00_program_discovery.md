# Z6.7 Evidence 00 - Program Discovery

Program: PROGRAM Z6.7 - Runtime Orchestrator Program Design  
Project: V7 Vozduh  
Branch target: v7-next  
Mode: READ ONLY discovery/design

## Gate 0 Result

DISCOVER -> REUSE -> EXTEND -> MERGE -> IMPLEMENT was applied before any program design.

Design conclusion:

- A separate full Runtime Orchestrator Program was not found.
- A strong partial Runtime Orchestrator already exists.
- The partial orchestrator is the active autoswitch runtime chain:
  `systemd/v7-users-autoswitch.timer` -> `systemd/v7-users-autoswitch.service` -> `tools/v7-users-autoswitch` -> `v7-user-switch` -> verify/rollback/result.
- Creating a new standalone orchestrator would duplicate existing runtime authority.
- Z6.7 must define the Runtime Orchestrator Program as an extension and formalization of the existing autoswitch-centered ownership chain.

## Program Inventory

| Program / Chain | Location | Current Purpose | Authority Level | Classification | Notes |
|---|---|---|---|---|---|
| Active autoswitch runtime program | `systemd/v7-users-autoswitch.timer`, `systemd/v7-users-autoswitch.service`, `tools/v7-users-autoswitch` | Periodic runtime cycle, planning, selected moves, restore barrier checks, guarded apply, verify, local rollback | Primary runtime/execution authority | REUSE, EXTEND | Closest existing orchestrator and must remain the root runtime owner. |
| User movement primitive | `v7-user-switch` invoked by `tools/v7-users-autoswitch` and Admin direct paths | Moves one user to selected egress | Low-level execution primitive | REUSE, WRAP UNDER OWNER | Must not become independent orchestrator authority. |
| Runtime audit sink | `tools/runtime-support/v7-audit-log` | Canonical audit append path | Primary audit authority | REUSE, EXTEND | Program audit must flow here, either directly or through existing Admin wrapper. |
| Admin operator program | `admin/v7-admin-api` | Operator UI/API, proposals, guarded autoswitch action, direct user switch, rollback, closure, audit wrapper | Operator and break-glass surface | REUSE, EXTEND | Must not replace primary runtime owner. Mutating direct paths must be modeled as break-glass or controlled invocations. |
| Operator execution governance | `admin_core/operator_execution.py`, `tools/v7-operator-execution-packet` | Zero-move packet validation, stale/hash/replay denial, append-only audit record | Governance/check authority only | REUSE, EXTEND | No runtime movement authority observed. |
| Operator observability and closure view | `admin_core/operator_observability.py` | Operation summaries, timeline, approval/rollback/closure previews, evidence references | Read-only observability/closure support | REUSE | Must become closure/readiness consumer, not executor. |
| Closure store and closure endpoint | `admin/v7-admin-api` closure model | Closure records: OPEN, VERIFIED, CLOSED, EXPIRED | Primary closure authority | REUSE, EXTEND | Closure owner remains Admin/operator model. |
| Generic rollback primitive | `tools/runtime-support/v7-rollback-last-change` | Restore latest backup target when applied | Generic rollback primitive | REUSE, CONSTRAIN | Useful primitive, not lifecycle rollback owner. |
| Signal programs | Telegram sentinel, service matrix refresh, egress quality compact timers/tools | Runtime health/signal refresh | Signal authority only | REUSE | Must feed runtime owner; must not execute movement in normal path. |
| Draft autoswitch planner | `systemd/drafts/v7-autoswitch-planner.timer`, `systemd/drafts/v7-autoswitch-planner.service` | Draft planner scheduling path | Latent scheduler/program duplicate | DO NOT TOUCH | Not active ownership target; preserve as evidence only. |
| New standalone orchestrator | Not present | Would coordinate all lifecycle stages independently | Would duplicate primary authority | REPLACE = FORBIDDEN | Do not create. |

## Existing Orchestrator Candidate Matrix

| Candidate | Location | Inputs | Outputs | Authority Level | Reuse Score | Risk Score |
|---|---|---|---|---|---|---|
| Autoswitch runtime chain | `systemd/v7-users-autoswitch.*`, `tools/v7-users-autoswitch` | Runtime state, generation, health, policy, restore barrier, egress capacity, selected move candidates | Plan, no-op/deny result, selected moves, user switch calls, verification, rollback result, runtime output | Primary runtime and execution owner | HIGH | MEDIUM |
| Admin operator chain | `admin/v7-admin-api` | Operator action, API auth, runtime previews, closure requests, rollback/apply requests | Admin audit, closure records, guarded autoswitch call, direct action results | Secondary operator/break-glass owner | HIGH | HIGH if allowed to bypass autoswitch |
| Operator execution governance chain | `admin_core/operator_execution.py` | Approval packet, generation/hash/runtime freshness facts | Validation verdict, audit record, no runtime movement | Governance-only | HIGH | LOW |
| Operator observability chain | `admin_core/operator_observability.py` | Historical reports, operation_id, evidence refs, closure/audit previews | Read-only operation summaries and closure support | Read-only observability | HIGH | LOW |
| Generic rollback chain | `tools/runtime-support/v7-rollback-last-change` | Backup target, latest backup, optional apply | Restore action and audit | Break-glass/primitive | MEDIUM | HIGH if used outside operation lifecycle |
| Draft planner chain | `systemd/drafts/v7-autoswitch-planner.*` | Timer/service draft | Planner invocation if activated | Latent duplicate | LOW | HIGH if activated without consolidation |

## Primary Finding

V7 already contains a partial Runtime Orchestrator ownership model. It is not a complete formal program because operation identity, lifecycle states, audit completion, closure completion, and break-glass lineage are not yet unified into a single documented program boundary. However, the active runtime/execution core already exists and must be reused.

