# PROGRAM Z6.4 Gate 0 Revalidation

Project: V7 Vozduh
Program: Z6.4 - Runtime Ownership Consolidation Design
Mode: READ ONLY
Date: 2026-06-02

## Constraint

This is an ownership design artifact only. It does not implement, refactor, deploy, restart services, modify systemd, mutate routing, move users, clean up, merge, force push, or create a Runtime Orchestrator.

## Revalidated Facts

| Fact | Status |
|---|---|
| existing_full_orchestrator=false | confirmed from Z6.1/Z6.2/Z6.3 |
| existing_partial_orchestrator=true | confirmed |
| primary_runtime_owner=tools/v7-users-autoswitch | confirmed |
| primary_execution_owner=tools/v7-users-autoswitch | confirmed |
| primary_audit_owner=tools/runtime-support/v7-audit-log | confirmed |
| primary_closure_owner=admin/v7-admin-api + admin_core/operator_observability.py | confirmed |
| scheduler_owner=systemd/v7-users-autoswitch.timer/service | confirmed as scheduler-only |
| duplicate_authority_risk=HIGH | confirmed |
| manual_bypass_risk=HIGH | confirmed |
| safe_to_continue_to_Z6_4=true | confirmed by Z6.3 |

## Gate 0 Component Classification

| Component | Future Design Role | Classification |
|---|---|---|
| `tools/v7-users-autoswitch` | Primary runtime owner: planner, selected moves, restore-barrier consumption/validation, runtime recheck, execution, verification, movement rollback, runtime outcome | REUSE / EXTEND |
| `systemd/v7-users-autoswitch.timer/service` | Scheduler-only owner: start autoswitch process on timer | REUSE |
| `v7-user-switch` | Low-level movement primitive owned through autoswitch or controlled operator surface | REUSE / REFACTOR LATER |
| `admin/v7-admin-api` | Operator surface, approval/visibility/closure owner, controlled manual invocation surface | REUSE / EXTEND |
| `admin_core/operator_observability.py` | Operation timeline, audit export, closure evidence, runtime verdict display | REUSE / EXTEND |
| `tools/runtime-support/v7-audit-log` | Canonical audit sink | REUSE / EXTEND |
| `tools/runtime-support/v7-rollback-last-change` | Low-level generic rollback primitive, not lifecycle owner | REUSE / REFACTOR LATER |
| `tools/v7-telegram-sentinel` | Advisory fast Telegram signal writer only | REUSE / REFACTOR LATER |
| `tools/v7-service-matrix-refresh-all` | Service-health signal owner | REUSE |
| `tools/v7-egress-quality-compact` | Historical quality signal owner | REUSE |
| `tools/v7-restore-settle-gate` | Restore-settle validation/evidence participant | REUSE |
| Admin execution contracts | Preview/governance/read-only model until connected through ownership boundaries | REUSE / EXTEND |
| `admin_core/operator_execution.py` | Runtime governance/recheck support; not current movement executor | REUSE / EXTEND |
| Persistent selected-move files | Legacy/evidence/read adapters; not canonical live selected-move truth | REFACTOR LATER |
| `systemd/drafts/v7-autoswitch-planner.*` | Dormant draft scheduler/planner path | DO NOT TOUCH |
| New orchestrator/planner/scheduler/execution engine/rollback engine/truth source | Forbidden | REPLACE = NO |

## Design Principle

The final ownership model must consolidate around existing components:

- Runtime truth belongs to `tools/v7-users-autoswitch`.
- Clock/launch belongs to systemd only.
- Operator visibility, approval surface, and closure belong to Admin/operator observability.
- Audit truth belongs to `v7-audit-log`.
- Low-level mutation tools remain primitives, not lifecycle owners.

