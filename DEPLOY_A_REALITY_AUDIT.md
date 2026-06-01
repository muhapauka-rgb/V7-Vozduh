# DEPLOY A Reality Audit

## Scope

Safe server synchronization from GitHub `v7-next` to the live server.

Code-only deployment was allowed. Runtime state, users, channels, routing, autoswitch, policy, rollback, and execution actions remained forbidden.

## Code Truth Source

- GitHub branch: `v7-next`
- remote hash: `12e51a5ad4a6c34b09e37c9343d7ee78cb7678d6`
- local branch: `v7-next`
- local hash: `12e51a5ad4a6c34b09e37c9343d7ee78cb7678d6`
- local worktree before packaging: clean

## Server Facts

- hostname: `v3119922.hosted-by-vdsina.ru`
- OS: Ubuntu 26.04 LTS, Linux `7.0.0-14-generic`
- active admin path: `/usr/local/bin/v7-admin-api`
- active admin process before deploy: `python3 /usr/local/bin/v7-admin-api`
- admin service: `v7-admin-api.service`
- admin service unit: `/etc/systemd/system/v7-admin-api.service`
- runtime state path: `/opt/v7/egress/state`
- users registry path: `/opt/v7/egress/state/users.registry`
- egress registry path: `/opt/v7/egress/state/egress.registry`

## Current Server Code Before Deploy

- `/usr/local/bin/v7-admin-api` hash before: `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04`
- no server git checkout was found under the inspected roots
- deploy model is filesystem-based under `/usr/local/bin`

## Active Service Context

Important active services observed:

- `v7-admin-api.service`: active/running
- `v7-api.service`: active/running
- `v7-health.service`: active/running
- `v7-routing-sync.service`: active/exited
- `v7-users-autoswitch.timer`: inactive/dead
- other V7 timers/services present but not modified

## Verdicts

- reality_audit_complete=true
- server_paths_clear=true
- v7_next_remote_hash_known=true
- server_git_checkout_found=false
