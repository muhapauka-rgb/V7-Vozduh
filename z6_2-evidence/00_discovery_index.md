# PROGRAM Z6.2 Evidence Index

Project: V7 Vozduh
Program: Z6.2 - Full Runtime Cycle Mapping
Mode: READ ONLY
Date: 2026-06-02

## Scope

This evidence set maps the existing runtime cycle from signal production to planner output, selected moves, restore barrier handling, execution, rollback, audit, bypass paths, and cycle closure.

No implementation, refactor, deploy, service restart, routing mutation, user movement, cleanup, deletion, merge, or force push was performed.

The audit is repository-local plus historical project documentation. Live VPS authentication was not used in this pass.

## Primary Sources

- `systemd/v7-users-autoswitch.timer`
- `systemd/v7-users-autoswitch.service`
- `systemd/v7-telegram-sentinel.timer`
- `systemd/v7-telegram-sentinel.service`
- `systemd/v7-service-matrix-refresh.timer`
- `systemd/v7-service-matrix-refresh.service`
- `systemd/v7-egress-quality-compact.timer`
- `systemd/v7-egress-quality-compact.service`
- `systemd/drafts/v7-autoswitch-planner.timer`
- `systemd/drafts/v7-autoswitch-planner.service`
- `tools/v7-users-autoswitch`
- `tools/v7-telegram-sentinel`
- `tools/v7-service-matrix-refresh-all`
- `tools/v7-egress-quality-compact`
- `tools/v7-observability-summary`
- `tools/v7-restore-settle-gate`
- `tools/runtime-support/v7-rollback-last-change`
- `tools/runtime-support/v7-audit-log`
- `admin/v7-admin-api`
- `admin_core/operator_execution.py`
- `admin_core/operator_observability.py`
- Historical reports `BLOCK_E11_14`, `BLOCK_E11_16`, `BLOCK_E11_17`, `BLOCK_E12`, `BLOCK_E25_1`, `BLOCK_E25_14`
- Prior Z6.1 report `PROGRAM_Z6_1_RUNTIME_EXECUTION_OWNERSHIP_AUDIT_REPORT.md`

## Evidence Files

- `01_signal_flow.md` - runtime signals, schedulers, and state readers/writers.
- `02_planner_selected_restore_flow.md` - planner, selected move lifecycle, restore barrier lifecycle.
- `03_execution_rollback_audit_bypass_flow.md` - execution, rollback, audit, and bypass authority.
- `04_end_to_end_timeline_and_gaps.md` - full cycle timeline and orchestration gaps.
- `05_final_verdicts.md` - Z6.2 verdict fields.

## Gate 0 Classification

| Component | Classification | Reason |
|---|---:|---|
| `tools/v7-users-autoswitch` | REUSE / EXTEND | Existing partial runtime orchestrator: reads policy/signals, plans selected moves, applies moves, verifies, rolls back locally, writes safety/reconnect/load state. |
| `systemd/v7-users-autoswitch.timer/service` | REUSE | Autonomous runtime-cycle scheduler and primary start owner. |
| `tools/v7-telegram-sentinel` + timer | REUSE / DO NOT TOUCH | Fast Telegram signal writer; production unit uses `--no-autoswitch`, but tool has latent autoswitch invocation path. |
| `tools/v7-service-matrix-refresh-all` + timer | REUSE | Service-matrix refresh signal owner. |
| `tools/v7-egress-quality-compact` + timer | REUSE | Historical quality summary owner. |
| `admin/v7-admin-api` autoswitch/apply/user-switch/rollback APIs | REUSE / EXTEND | Existing operator/manual authority surfaces; several mutate paths bypass preview-only execution contracts. |
| `admin/v7-admin-api` execution contract APIs | REUSE / EXTEND | Preview/read-only execution read model; explicitly non-executable. |
| `admin_core/operator_execution.py` | REUSE / EXTEND | Runtime recheck and append-only governance for zero-move packets; not a movement executor. |
| `tools/v7-restore-settle-gate` | REUSE | Read-only restore-settle evaluator and evidence classifier; not an executor. |
| `tools/runtime-support/v7-rollback-last-change` | REUSE / REFACTOR LATER | Broad latest-change rollback tool; authoritative only when invoked with `--apply`; not contract-scoped. |
| `tools/runtime-support/v7-audit-log` | REUSE | Generic audit event writer. |
| Persistent selected-move read adapters | REFACTOR LATER | Multiple readers and file-name conventions; active autoswitch selected moves are ephemeral, not queued files. |
| Restore barrier creation/clearance ownership | REFACTOR LATER | Enforcement is in autoswitch, but active writer/closure owner is not singular. |
| `systemd/drafts/v7-autoswitch-planner.*` | DO NOT TOUCH | Draft scheduler path, not active production owner in current evidence. |
| New parallel runtime orchestrator | REPLACE = NO | Forbidden by Gate 0; would duplicate the existing autoswitch partial orchestrator. |

