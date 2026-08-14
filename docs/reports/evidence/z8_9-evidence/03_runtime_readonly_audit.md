# Runtime Read-Only Audit

Date: 2026-06-02

## Access Mode

Interactive broad root shell was rejected by the approval reviewer as too risky. The audit used bounded SSH commands with the exact command in the command line. No deploy, service restart, systemd modification, runtime mutation, autoswitch apply, routing mutation, user movement, rollback, cleanup, deletion, or state mutation was performed.

## Runtime Truth

| Item | Result |
| --- | --- |
| Hostname | `v3119922.hosted-by-vdsina.ru` |
| Runtime root | `/opt/v7` exists |
| `/opt/v7` git repo | false |
| Runtime branch | UNKNOWN |
| Runtime commit | UNKNOWN |
| `v7-users-autoswitch` hash | `8eedfae073f756d0c70a893b477cf1c19996e467a9e9e3d4bacb116cc20d4c4c` |
| `v7-audit-log` hash | `c2a524d4b5b2023dfd3a2923c1f3148ad647853fd00e50454d3cd7095d3f0a86` |
| Autoswitch service | loaded, inactive dead since 2026-05-27 20:13:14 MSK |
| Autoswitch timer | loaded/enabled, inactive dead since 2026-05-27 20:13:19 MSK |
| State root | `/opt/v7/egress/state` exists |
| Audit path | `/opt/v7/audit` exists; audit files present |
| Events path | `/opt/v7/events` exists |
| Admin path | `/opt/v7/admin` exists |

## Unsafe Legacy Minimum Command

`/usr/local/bin/v7-users-autoswitch --pretty` was not executed. The approval reviewer rejected it because local code inspection indicates dry-run/pretty paths can write runtime state. Therefore this command cannot be considered safe read-only access until the tool is changed or a forced-command wrapper proves no writes.

## Restore Barrier

`/opt/v7/egress/state/autoswitch-restore-barrier.json` exists and was read. It reports:

```text
enabled=true
expires_at=2000-01-01T00:00:00+00:00
owner=control_plane_governance
reason=Z3.2 one-user live hybrid autonomy execution clearance budget=1
```

## Missing Runtime Stores

The expected closure/execution/selected-move stores were not found:

```text
/opt/v7/egress/state/closure-records.jsonl: missing
/opt/v7/egress/state/execution-contracts.json: missing
/opt/v7/egress/state/execution-events.jsonl: missing
/opt/v7/egress/state/selected-moves.json: missing
/opt/v7/egress/state/autoswitch-selected-moves.json: missing
```

## Exact Runtime Blockers

```text
runtime_branch_unknown
runtime_commit_unknown
runtime_root_not_git_repository=/opt/v7
autoswitch_pretty_not_readonly_safe
service_inactive=v7-users-autoswitch.service
timer_inactive=v7-users-autoswitch.timer
closure_path_missing=/opt/v7/egress/state/closure-records.jsonl
execution_contract_store_missing=/opt/v7/egress/state/execution-contracts.json
execution_event_store_missing=/opt/v7/egress/state/execution-events.jsonl
selected_moves_missing
operation_wiring_not_confirmed_on_runtime
```
