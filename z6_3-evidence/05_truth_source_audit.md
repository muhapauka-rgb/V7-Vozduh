# Z6.3 Truth Source Audit

## Ownership Conflicts

| Conflict | Components | Severity |
|---|---|---:|
| Runtime execution owner conflict | Autoswitch, Admin apply, Admin direct switch, CLI switch | HIGH |
| Selected-move authority conflict | Autoswitch in-process selected moves, persistent selected-move file readers | HIGH |
| Restore-barrier lifecycle conflict | Autoswitch enforcement, fragmented/manual writers, Admin gates | HIGH |
| Runtime recheck conflict | Autoswitch path-local checks, operator zero-move recheck, Admin preview gates | HIGH |
| Rollback ownership conflict | Autoswitch local rollback, Admin rollback, generic rollback, proxy rollback | HIGH |
| Audit completion conflict | `v7-audit-log`, Admin audit, operator audit, event JSONL, reports | HIGH |
| Closure conflict | Admin closure records, operator timeline, autoswitch command completion, reports | HIGH |
| Scheduler/planner latent conflict | Active autoswitch timer, draft planner timer | MEDIUM/HIGH latent |

## Duplicate Execution Authority

- `v7-users-autoswitch --apply`
- Admin autoswitch apply endpoint
- Admin direct user-switch endpoint
- CLI `v7-user-switch`
- Latent `v7-telegram-sentinel` autoswitch invocation when not run with `--no-autoswitch`

## Duplicate Rollback Authority

- Autoswitch verification rollback.
- Admin direct-switch rollback.
- Admin rollback endpoint.
- `v7-rollback-last-change --apply`.
- Proxy runtime guard rollback.
- Historical raw fallback rollback instructions.

## Duplicate Audit Authority

- `v7-audit-log`.
- Admin `audit_admin`.
- Operator execution chained audit.
- Service matrix refresh event JSONL.
- Telegram sentinel event JSONL.
- Markdown report closeouts.
- Systemd/stdout command results.

## Duplicate Closure Authority

- Admin closure records.
- Operator observability operation timeline/runtime verdicts.
- Execution contract event names, preview-only.
- Autoswitch process completion.
- Historical reports.

## Duplicate Truth Sources

| Truth Area | Duplicate / Conflicting Sources |
|---|---|
| selected moves | Autoswitch in-process plan, selected-move files, historical evidence copies. |
| runtime execution state | Autoswitch JSON, Admin action result, audit log, operator timeline. |
| rollback state | Autoswitch local result, generic rollback output, Admin rollback response, contract rollback preview. |
| closure | Admin closure records, operator historical timeline, markdown reports. |
| service health | service matrix refresh and Telegram sentinel updates. |

## Orphan Lifecycle Stages

- Restore-barrier creation/write/closure.
- Unified runtime-cycle closure.
- Final audit completion for autonomous cycles.
- Contract-scoped rollback execution.
- Global runtime admission/recheck across autonomous and manual paths.

## Truth Source Verdict

The ownership conflicts and authority conflicts are understood. Consolidation can proceed to Z6.4 only if it reuses existing owners and does not create duplicate truth sources.

