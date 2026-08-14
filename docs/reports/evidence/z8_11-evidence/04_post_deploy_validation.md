# Z8.11 Post-Deploy Validation

## Binary hashes

- `/usr/local/bin/v7-users-autoswitch`: `a5480fdfe33c3618aeea345899b98cfad259001576069e9f3721ce01add5d0d3`
- `/usr/local/bin/v7-admin-api`: `8da1e5479723891f8619bbf5296239afb7e41d27f456b9601bd9799d289b705e`
- `/usr/local/bin/v7-audit-log`: `c2a524d4b5b2023dfd3a2923c1f3148ad647853fd00e50454d3cd7095d3f0a86`

All match authoritative hashes for `Updatesystem@ff91005945bd6d35216bbe4fa6627f9df009597c`.

## Operation wiring

Production `/usr/local/bin/v7-users-autoswitch` contains:

- `operation_id`
- `operation_owner`
- `runtime_operation_terminal`
- `closure_target`
- audit linkage through `v7-audit-log`

## Services

- `v7-admin-api.service`: active/running since `2026-06-02 14:47:01 MSK`
- `v7-users-autoswitch.service`: inactive/dead, intentionally not started
- `v7-users-autoswitch.timer`: enabled but inactive/dead, intentionally not started

Scheduler truth is confirmed as manual/paused for convergence. It is not active because enabling or starting it could execute autoswitch `--apply`.

