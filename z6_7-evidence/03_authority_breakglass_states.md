# Z6.7 Evidence 03 - Authority, Break-Glass, and Program States

## Authority Model

| Authority | Canonical Owner | Allowed Delegates | Forbidden Duplicate |
|---|---|---|---|
| Runtime scheduling | systemd autoswitch timer/service | None | Draft planner timer as active scheduler |
| Runtime planning | `tools/v7-users-autoswitch` | None | Admin or standalone planner owning selected moves |
| Operation identity binding | Autoswitch-centered runtime program using `operation_id` | Admin/operator may reference existing operation | New operation identity source |
| Selected moves | `tools/v7-users-autoswitch` | None | Approval packet or Admin endpoint as independent move owner |
| Restore barrier generation/check | `tools/v7-users-autoswitch` and existing barrier tools as inputs | None | Separate restore-barrier lifecycle owner |
| Runtime recheck | `tools/v7-users-autoswitch` | Operator governance may validate packets read-only | Admin/API recheck as execution owner |
| Execution | `tools/v7-users-autoswitch` through `v7-user-switch` | Admin guarded apply as controlled invocation | Direct switch as normal path |
| Verification | `tools/v7-users-autoswitch` | Read-only Admin/observability views | Independent verification closure |
| Movement rollback | `tools/v7-users-autoswitch` rollback branch | Low-level primitive under operation lineage | Generic rollback as normal lifecycle owner |
| Audit | `tools/runtime-support/v7-audit-log` | Admin `audit_admin(...)`, operator execution audit producer | Separate audit truth |
| Closure | Admin closure model + operator observability | None | Command exit/report as closure truth |

## Break-Glass Model

Break-glass means an operator or emergency path performs a mutation outside the normal autoswitch-owned cycle. It is allowed only as an exception model, not as the normal Runtime Orchestrator Program.

| Break-Glass Path | Normal Program Authority | Required Lineage | Required Audit | Required Closure |
|---|---|---|---|---|
| Admin direct `user-switch` action | No | `operation_id`, actor, reason, affected user, from/to egress, runtime snapshot | `v7-audit-log` via Admin wrapper | Admin closure record |
| CLI direct `v7-user-switch` | No | `operation_id`, actor, reason, affected user, from/to egress | `v7-audit-log` | Admin/operator closure after fact |
| Generic `v7-rollback-last-change --apply` | No | `operation_id`, rollback target, backup source, reason | `v7-audit-log` rollback action | Closure record with rollback outcome |
| Emergency proxy/runtime guard rollback | No | `operation_id`, affected proxy/runtime object, before/after hash | `v7-audit-log` | Closure record with verification |
| Admin guarded autoswitch apply | Yes, only because it invokes autoswitch owner | `operation_id`, actor, mode, selected move hash | `v7-audit-log` | Closure record if terminal operation |

## Runtime Program States

| State | Meaning | Owner | Exit Condition |
|---|---|---|---|
| IDLE | No active runtime cycle; scheduler waiting | systemd scheduler | Timer/service starts autoswitch |
| PLANNING | Autoswitch is reading facts, binding operation identity, planning moves | `tools/v7-users-autoswitch` | Selected moves/no-op/deny produced |
| EXECUTION | Autoswitch is applying selected moves | `tools/v7-users-autoswitch` | Verification starts or command fails |
| ROLLBACK | Autoswitch rollback branch or constrained rollback primitive is active | `tools/v7-users-autoswitch`; primitive if break-glass | Rollback verified or failed terminal result emitted |
| AUDIT | Runtime terminal result exists and must be recorded | `v7-audit-log` | Audit record exists |
| CLOSURE | Audited runtime result awaits operator closure | Admin closure model | CLOSED, VERIFIED, EXPIRED, or reopened state recorded |
| BLOCKED | Policy, trust, capacity, generation, restore barrier, replay, stale runtime, or governance condition prevents execution | Blocking owner depends on condition; terminal verdict owned by autoswitch/governance | Audit and closure of blocked/no-op operation |
| DEGRADED | Runtime signals are stale/conflicted or audit/closure facts are incomplete | Runtime owner and Admin/operator visibility | Recovered to normal loop or blocked/no-op terminal result |

## State Transition Rules

Allowed normal path:

`IDLE -> PLANNING -> EXECUTION -> AUDIT -> CLOSURE -> IDLE`

Allowed no-op/blocked path:

`IDLE -> PLANNING -> BLOCKED -> AUDIT -> CLOSURE -> IDLE`

Allowed rollback path:

`IDLE -> PLANNING -> EXECUTION -> ROLLBACK -> AUDIT -> CLOSURE -> IDLE`

Allowed degraded path:

`IDLE -> PLANNING -> DEGRADED -> BLOCKED -> AUDIT -> CLOSURE -> IDLE`

Forbidden normal path:

- `Admin direct action -> movement -> closure` without runtime operation lineage and audit.
- `Generic rollback -> done` without operation lineage, audit, and closure.
- `Draft planner scheduler -> autoswitch` as a second active scheduler.

