# PROGRAM Z6.7 - Runtime Orchestrator Program Design Report

Project: V7 Vozduh  
Branch target: v7-next  
Date: 2026-06-02  
Mode: READ ONLY design/audit  
Evidence folder: `z6_7-evidence`

## Executive Verdict

V7 does not need a new standalone Runtime Orchestrator.

The existing autoswitch-centered chain is already the partial Runtime Orchestrator and must be reused:

```text
systemd/v7-users-autoswitch.timer
  -> systemd/v7-users-autoswitch.service
  -> tools/v7-users-autoswitch
  -> v7-user-switch
  -> verify / rollback
  -> v7-audit-log
  -> Admin closure / operator observability
```

Z6.7 defines the Runtime Orchestrator Program as a formal ownership program built only from existing V7 components. It does not introduce a new service, scheduler, execution engine, rollback engine, audit sink, closure store, lifecycle truth source, or operation identity.

## Gate 0 Compliance

Mandatory gate:

`DISCOVER -> REUSE -> EXTEND -> MERGE -> IMPLEMENT`

Result:

- Existing runtime execution authority was discovered first.
- Existing planner, selected move, restore-barrier, recheck, execution, rollback, audit, and closure ownership were mapped.
- The design reuses the existing partial orchestrator.
- Any future implementation must extend or merge into that ownership model.
- Parallel runtime programs and duplicate truth sources are forbidden.

## Existing Orchestrator Candidate

Primary candidate:

| Field | Value |
|---|---|
| Name | Autoswitch Runtime Program |
| Location | `systemd/v7-users-autoswitch.timer`, `systemd/v7-users-autoswitch.service`, `tools/v7-users-autoswitch` |
| Purpose | Start periodic runtime cycle, plan moves, own selected moves, check generation/restore barriers, execute through `v7-user-switch`, verify, rollback on verify failure, emit runtime result |
| Inputs | Runtime state, policy state, health signals, egress capacity, restore barrier, generation state, operator/admin mode |
| Outputs | Plans, no-op/deny reasons, selected moves, movement results, verification results, rollback results, terminal runtime verdict |
| Authority Level | Primary runtime and execution authority |
| Reuse Score | HIGH |
| Risk Score | MEDIUM |
| Classification | REUSE, EXTEND |

Conclusion:

- This is not a complete formal orchestrator program yet because audit/closure/operation identity are fragmented.
- It is already the runtime/execution core.
- Replacing it or creating a peer orchestrator would duplicate authority.

## Program Boundary

The Runtime Orchestrator Program boundary is:

```text
Scheduler
  -> Runtime owner
  -> Execution primitive
  -> Verification / rollback
  -> Audit owner
  -> Closure owner
```

Mapped to existing components:

| Layer | Existing Owner |
|---|---|
| Scheduler | `systemd/v7-users-autoswitch.timer/service` |
| Runtime owner | `tools/v7-users-autoswitch` |
| Execution primitive | `v7-user-switch`, controlled by autoswitch in normal path |
| Verification | `tools/v7-users-autoswitch` |
| Normal movement rollback | `tools/v7-users-autoswitch` rollback branch |
| Generic rollback primitive | `tools/runtime-support/v7-rollback-last-change`, break-glass only |
| Audit | `tools/runtime-support/v7-audit-log` |
| Closure | Admin closure model in `admin/v7-admin-api` |
| Observability | `admin_core/operator_observability.py` |
| Governance validation | `admin_core/operator_execution.py` |

## Operation Ownership Flow

Canonical operation identity:

- `operation_id`

Operation lineage owned by existing components:

| Fact | Owner |
|---|---|
| Operation identity | Runtime Orchestrator Program using Z6.6 `operation_id` model |
| Planning generation | `tools/v7-users-autoswitch` |
| Runtime snapshot | `tools/v7-users-autoswitch` |
| Selected move hash | `tools/v7-users-autoswitch` |
| Restore-barrier facts | `tools/v7-users-autoswitch` and existing restore-barrier tools as inputs |
| Approval/governance packet | Admin/operator governance modules |
| Audit event | `v7-audit-log` |
| Closure record | Admin closure model |

No new operation identity is allowed.

## Orchestrator Loop

The designed loop is:

1. Signal programs refresh runtime evidence.
2. Autoswitch systemd timer starts the runtime cycle.
3. Autoswitch service invokes `tools/v7-users-autoswitch --apply`.
4. Autoswitch binds operation identity and reads runtime truth.
5. Autoswitch plans candidate movement.
6. Autoswitch owns selected moves and selected move hash.
7. Autoswitch validates restore barrier, generation, and runtime recheck.
8. Autoswitch emits blocked/no-op/deny terminal result if execution is not allowed.
9. Autoswitch executes through `v7-user-switch` if execution is allowed.
10. Autoswitch verifies runtime result.
11. Autoswitch performs rollback branch if verification fails and rollback policy applies.
12. Autoswitch emits terminal runtime verdict.
13. Terminal verdict is recorded through `v7-audit-log`.
14. Admin/operator closure resolves the operation.

Program completion requires:

```text
runtime_terminal_state -> audit_recorded -> closure_resolved
```

Process exit alone is not program completion.

## Authority Model

| Authority | Canonical Owner |
|---|---|
| Runtime cycle start | systemd autoswitch timer/service |
| Planner execution | `tools/v7-users-autoswitch` |
| Selected moves | `tools/v7-users-autoswitch` |
| Restore barrier / generation clearance | `tools/v7-users-autoswitch` |
| Runtime recheck | `tools/v7-users-autoswitch` |
| Normal execution | `tools/v7-users-autoswitch` through `v7-user-switch` |
| Runtime verification | `tools/v7-users-autoswitch` |
| Normal movement rollback | `tools/v7-users-autoswitch` |
| Audit completion | `tools/runtime-support/v7-audit-log` |
| Closure completion | Admin closure model and operator observability |

Admin guarded autoswitch apply is acceptable only as a controlled entry into the canonical runtime owner. Admin direct switch, CLI direct switch, and generic rollback apply are break-glass paths, not normal program authority.

## Break-Glass Model

Break-glass paths must not become duplicate runtime programs.

| Path | Treatment |
|---|---|
| Admin direct `user-switch` | Break-glass; require operation lineage, audit, closure |
| CLI direct `v7-user-switch` | Break-glass; require operation lineage, audit, closure |
| Generic `v7-rollback-last-change --apply` | Break-glass primitive; require rollback lineage, audit, closure |
| Emergency runtime/proxy rollback | Break-glass; require before/after evidence, audit, closure |
| Admin guarded autoswitch apply | Controlled invocation of autoswitch owner |

## Runtime Program States

| State | Owner | Meaning |
|---|---|---|
| IDLE | systemd scheduler | Waiting for next runtime cycle |
| PLANNING | autoswitch | Reading truth, binding operation, planning selected moves |
| EXECUTION | autoswitch | Applying selected moves |
| ROLLBACK | autoswitch or constrained primitive | Rolling back failed movement or emergency state |
| AUDIT | `v7-audit-log` | Recording terminal runtime facts |
| CLOSURE | Admin closure model | Resolving operation after audit |
| BLOCKED | autoswitch/governance condition | Execution denied or no-op terminal path |
| DEGRADED | runtime/Admin visibility | Signals or lifecycle facts stale/conflicted/incomplete |

Normal transitions:

```text
IDLE -> PLANNING -> EXECUTION -> AUDIT -> CLOSURE -> IDLE
IDLE -> PLANNING -> BLOCKED -> AUDIT -> CLOSURE -> IDLE
IDLE -> PLANNING -> EXECUTION -> ROLLBACK -> AUDIT -> CLOSURE -> IDLE
IDLE -> PLANNING -> DEGRADED -> BLOCKED -> AUDIT -> CLOSURE -> IDLE
```

## Final Program Map

### Runtime Orchestrator Program

```text
Signal programs
  -> autoswitch scheduler
  -> autoswitch runtime owner
  -> selected moves / restore barrier / runtime recheck
  -> execution / verification / rollback
  -> runtime terminal verdict
  -> audit
  -> closure
```

### Component Ownership Map

| Component | Classification | Program Role |
|---|---|---|
| `systemd/v7-users-autoswitch.timer/service` | REUSE | Scheduler |
| `tools/v7-users-autoswitch` | REUSE, EXTEND | Runtime orchestrator core |
| `v7-user-switch` | REUSE, CONSTRAIN | Movement primitive |
| `tools/runtime-support/v7-audit-log` | REUSE, EXTEND | Audit truth |
| `admin/v7-admin-api` | REUSE, EXTEND | Operator, guarded invocation, closure, break-glass surface |
| `admin_core/operator_execution.py` | REUSE, EXTEND | Governance validation |
| `admin_core/operator_observability.py` | REUSE | Operation and closure visibility |
| `tools/runtime-support/v7-rollback-last-change` | REUSE, CONSTRAIN | Generic rollback primitive |
| Signal timers/tools | REUSE | Evidence inputs |
| `systemd/drafts/v7-autoswitch-planner.*` | DO NOT TOUCH | Latent duplicate |

### Lifecycle Map

`START -> OPERATION_BOUND -> PLANNED -> GUARDED -> EXECUTED_OR_BLOCKED -> VERIFIED_OR_ROLLED_BACK -> TERMINAL -> AUDITED -> CLOSED`

### Operation Map

`operation_id` is the semantic root. All proposal, approval, selected move, snapshot, restore-barrier, audit, closure, and evidence identifiers are lineage under it.

### Audit Map

`runtime_terminal_result -> v7-audit-log -> Admin audit views -> operator observability`

### Closure Map

`audited_terminal_result -> Admin closure record -> operator observability -> CLOSED/VERIFIED/EXPIRED/reopened`

### Rollback Map

Normal rollback is autoswitch-owned. Generic rollback is a break-glass primitive and must be bound to operation lineage.

### Break-Glass Map

Direct Admin/CLI mutation and generic rollback are allowed only as exceptional paths with operation lineage, canonical audit, and closure. They must not be normal runtime cycle paths.

## Truth Source Audit

| Truth Source | Canonical Owner | Verdict |
|---|---|---|
| Runtime orchestrator | Autoswitch-centered chain | Reuse existing partial owner |
| Scheduler | systemd autoswitch timer/service | No new scheduler |
| Operation identity | `operation_id` | No duplicate identity |
| Runtime lifecycle | Autoswitch terminal result + audit + closure | Consolidate by wiring |
| Audit | `v7-audit-log` | No duplicate sink |
| Closure | Admin closure model | No duplicate closure source |
| Rollback | Autoswitch branch; generic primitive break-glass only | No duplicate rollback owner |
| Governance | Operator execution/observability | No movement authority |

## Final Verdicts

```text
runtime_orchestrator_program_defined=true
existing_orchestrator_reused=true
duplicate_orchestrator_risk=LOW
duplicate_program_risk=MEDIUM
operation_flow_defined=true
authority_flow_defined=true
lifecycle_flow_defined=true
audit_flow_defined=true
closure_flow_defined=true
implementation_scope_understood=true
safe_to_continue_to_Z6_8=true
```

## Safety Statement

No implementation was performed. No API, storage, service, scheduler, runtime mutation, routing mutation, user movement, systemd modification, timer modification, service restart, cleanup, deletion, merge, or force push was performed.

