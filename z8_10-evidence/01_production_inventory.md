# Z8.10 Production Inventory

Bounded read-only SSH checks were used. No deploy, restart, autoswitch apply, user movement, routing mutation, cleanup, deletion, service mutation or runtime state mutation was performed.

## Host

- Host: `195.2.79.116`
- Hostname: `v3119922.hosted-by-vdsina.ru`
- Production date sample: `2026-06-02T14:23:40+03:00`
- Login user for checks: `root`
- Default shell cwd for checks: `/root`

## Runtime/state tree

`/opt/v7` exists and contains:

- `admin`
- `audit`
- `backups`
- `egress`
- `events`
- `ipam`
- `legacy`
- `ops`
- `policy`
- `reports`
- `traffic`
- `v7.db`

`/opt/v7` is not a git checkout. The bounded git checks returned `fatal: not a git repository`.

## Runtime binaries

- `/usr/local/bin/v7-users-autoswitch`
- `/usr/local/bin/v7-audit-log`
- `/usr/local/bin/v7-admin-api`

All three production paths are executable. This confirms the runtime uses copied binaries in `/usr/local/bin`, not a live git checkout under `/opt/v7`.

