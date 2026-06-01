# Z6.1 Evidence Index

Program: PROGRAM Z6.1 - Runtime Execution Ownership Audit
Project: V7 Vozduh
Date: 2026-06-01
Mode: read-only local repository audit

## Safety Boundary

No deploy, autoswitch apply, user movement, routing mutation, runtime mutation, service restart, systemd modification, timer modification, cleanup, deletion, merge, or force push was performed.

Live VPS validation was not performed in this evidence set. A read-only key-based SSH probe was attempted earlier in the thread and failed with `Permission denied`; no password was passed through shell/tool input.

## Primary Repository Sources Reviewed

- `systemd/v7-users-autoswitch.service`
- `systemd/v7-users-autoswitch.timer`
- `systemd/v7-telegram-sentinel.service`
- `systemd/v7-telegram-sentinel.timer`
- `systemd/v7-service-matrix-refresh.timer`
- `systemd/v7-egress-quality-compact.timer`
- `systemd/drafts/v7-autoswitch-planner.service`
- `systemd/drafts/v7-autoswitch-planner.timer`
- `tools/v7-users-autoswitch`
- `tools/v7-telegram-sentinel`
- `tools/v7-service-matrix-refresh-all`
- `tools/v7-egress-quality-compact`
- `tools/v7-restore-settle-gate`
- `tools/v7-second-canary-target-readiness`
- `tools/v7-observability-summary`
- `tools/v7-control-plane-governance-check`
- `tools/runtime-support/v7-rollback-last-change`
- `tools/runtime-support/v7-audit-log`
- `admin/v7-admin-api`
- `admin_core/operator_execution.py`
- `admin_core/operator_observability.py`

## Evidence Files

- `01_ownership_map.md` - component-level ownership classification.
- `02_authority_and_state_map.md` - authority, state writer, and lifecycle maps.
- `03_orchestrator_candidates.md` - candidate table with reuse and risk scores.
- `04_truth_source_and_risk_audit.md` - duplicate authority/path/state/scheduler audit.
- `05_critical_questions.md` - required Q1-Q10 answers and final verdict inputs.

## High-Signal Line Evidence

- Active autoswitch scheduler: `systemd/v7-users-autoswitch.timer:5-8` starts `v7-users-autoswitch.service` every 20 seconds after boot.
- Active autoswitch executor: `systemd/v7-users-autoswitch.service:7-9` runs `/usr/local/bin/v7-users-autoswitch --apply`.
- Autoswitch default state and barrier inputs: `tools/v7-users-autoswitch:26-36`.
- Autoswitch restore-barrier reader/enforcer: `tools/v7-users-autoswitch:361-426`.
- Autoswitch generation hash inputs: `tools/v7-users-autoswitch:428-448`.
- Autoswitch selected move planning: `tools/v7-users-autoswitch:938-1018`.
- Autoswitch apply and rollback-on-verify-fail path: `tools/v7-users-autoswitch:1775-1810`.
- Autoswitch state writers after apply: `tools/v7-users-autoswitch:1815-1873`.
- Autoswitch movement primitive call: `tools/v7-users-autoswitch:1875-1885`.
- Admin mutating action surface: `admin/v7-admin-api:504-591`.
- Admin role authority for rollback/user-switch/autoswitch: `admin/v7-admin-api:604-668`.
- Admin execution read-only contract foundation: `admin/v7-admin-api:12210-12228`, `admin/v7-admin-api:12645-12670`.
- Admin selected moves and restore barrier read adapters: `admin/v7-admin-api:12916-12963`.
- Admin autoswitch action wrapper: `admin/v7-admin-api:15548-15585`.
- Admin rollback apply wrapper: `admin/v7-admin-api:33968-33981`.
- Admin manual user-switch wrapper: `admin/v7-admin-api:34338-34364`.
- Operator execution explicit no-runtime-action scope: `admin_core/operator_execution.py:1-7`.
- Operator execution zero-move packet validation: `admin_core/operator_execution.py:89-135`.
- Operator runtime recheck: `admin_core/operator_execution.py:156-214`.
- Operator append-only governance/audit: `admin_core/operator_execution.py:239-345`.
- Telegram sentinel signal writer and latent autoswitch launcher: `tools/v7-telegram-sentinel:1-9`, `tools/v7-telegram-sentinel:388-407`, `tools/v7-telegram-sentinel:421-422`, `tools/v7-telegram-sentinel:450-478`.
- Production Telegram sentinel is no-autoswitch: `systemd/v7-telegram-sentinel.service:7-9`.
- Generic rollback tool search/apply scope: `tools/runtime-support/v7-rollback-last-change:9-16`, `tools/runtime-support/v7-rollback-last-change:99-128`.
- Audit writer: `tools/runtime-support/v7-audit-log:135-149`.
