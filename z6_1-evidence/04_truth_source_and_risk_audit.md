# Z6.1 Truth Source And Risk Audit

## Duplicate Authority

| Area | Duplicate / Split Owners | Risk |
|---|---|---|
| Runtime movement | Autoswitch timer, Admin autoswitch apply, Admin manual user-switch, manual CLI `v7-user-switch` if available | HIGH |
| Rollback | Autoswitch verify rollback, Admin manual-switch rollback, generic latest-backup rollback, read-only contract rollback summaries | HIGH |
| Governance | Admin roles/CSRF, zero-move operator packet model, observability approval previews, historical control-plane governance check/docs | MEDIUM |
| Restore barrier | Autoswitch enforcement, Admin/observability read adapters, historical evidence flows; no singular active writer identified | MEDIUM/HIGH |
| Execution lifecycle | P2 execution contracts model statuses, but actual movement is owned by autoswitch/Admin action paths | HIGH |

## Duplicate Execution Paths

- `systemd/v7-users-autoswitch.service` executes `v7-users-autoswitch --apply`.
- Admin `/api/actions/autoswitch-apply-guarded` executes `v7-users-autoswitch --mode guarded --apply`.
- Admin `/api/actions/user-switch` executes `v7-user-switch` directly.
- `tools/v7-users-autoswitch` executes `v7-user-switch` directly for selected moves and rollback-on-verify-fail.
- Admin `/api/actions/rollback-apply` executes `v7-rollback-last-change --apply`.
- `tools/v7-telegram-sentinel` can execute `v7-users-autoswitch --mode guarded --apply` if run without `--no-autoswitch`; the production systemd unit includes `--no-autoswitch`.

## Duplicate State Writers

- `service-matrix.json`: service matrix test/refresh plus Telegram sentinel.
- `autoswitch-safety.json`: autoswitch owns writes; Admin/observability read it.
- `client-reconnect-state.json`: autoswitch plus client observers.
- `audit.jsonl`: generic `v7-audit-log`, Admin action audit, runtime tools.
- Operator execution audit JSONL: separate append-only governance/audit store.
- Restore barrier and selected move files: readers are present, but singular active writers were not identified in the local code scan.

## Duplicate Schedulers

- Active autoswitch timer: every 20 seconds.
- Active Telegram sentinel timer: every 4 seconds.
- Active service matrix timer: every 15 minutes.
- Active quality compact timer: every 5 minutes.
- Draft autoswitch planner timer: every 30 seconds, under `systemd/drafts`.

## Duplicate Orchestration Logic

- `tools/v7-users-autoswitch` performs real planner/apply/verify/rollback-on-verify-fail logic.
- Admin execution APIs model future execution contracts/statuses/events, but are read-only.
- Operator execution module validates zero-move governance packets and writes audit records.
- Operator observability builds preview/rehearsal/readiness views.

The overlap is conceptual rather than functionally identical. It becomes dangerous if a new Runtime Orchestrator is implemented as a parallel path instead of coordinating these existing owners.

## Legacy / Stale / Orphan Ownership

- `systemd/drafts/v7-autoswitch-planner.*` is a draft scheduler for read-only planner refresh and must not be activated during Z6.1.
- `systemd/drafts/v7-health.service` is a draft dependency target, not proven active in local evidence.
- Restore barrier writer/lifecycle completion is not singular in active local code.
- Selected moves file writer is not singular in active local code; readers accept multiple live/historical paths.
- Generic rollback selects the latest backup from broad roots rather than a contract-specific manifest.

## Risk Summary

duplicate_authority_risk=HIGH

manual_bypass_risk=HIGH

Primary reason: the system already contains movement-capable paths outside the read-only execution contract model, including autoswitch timer apply and Admin manual user switch.
