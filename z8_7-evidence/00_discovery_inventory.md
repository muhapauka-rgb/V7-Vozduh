# Z8.7 Evidence 00 - Discovery Inventory

Program: Z8.7 - Canonical Source Of Truth Establishment
Date: 2026-06-02

## Local Repositories / Worktrees

```text
worktree /Users/ponch/Documents/New project
HEAD d61480dea6de67ea9d2cfd5c3440d93896076178
branch refs/heads/Updatesystem

worktree /private/tmp/v7-convergence-c
HEAD c40cae13298594b7ad7040df4b19306c4e2c29d4
branch refs/heads/v7-next

worktree /private/tmp/v7-vozduh-main
HEAD 593619d494e215d11fd826086593527a4a555690
detached
prunable gitdir file points to non-existent location
```

## Current Workspace Status

```text
path=/Users/ponch/Documents/New project
branch=Updatesystem
commit=d61480dea6de67ea9d2cfd5c3440d93896076178
tracking=origin/Updatesystem ahead 1
```

Dirty state:

- `admin/v7-admin-api` modified
- many untracked reports/evidence folders

## Remote

```text
origin=https://github.com/muhapauka-rgb/V7-Vozduh.git
```

Read-only remote refs:

```text
7c843545271e903b5017cac583b8571870f05629 refs/heads/Updatesystem
593619d494e215d11fd826086593527a4a555690 refs/heads/main
c40cae13298594b7ad7040df4b19306c4e2c29d4 refs/heads/v7-next
afcdd9cc61b7a1302c8785489991b0eac217b395 refs/heads/convergence/admin-api-2026-05
0ea6d4ef82abaad26b0609d254bb6cf297db6432 refs/heads/codex/dynamic-load-autoswitch
a0e689c67ef7d47e7f04e5c30e5430acd05752cb refs/heads/codex/integratsiya-tunelya
```

## Runtime / Deploy Paths Known From Repo And Docs

- production host candidate: `195.2.79.116`
- production hostname candidate: `v3119922.hosted-by-vdsina.ru`
- runtime root: `/opt/v7`
- state root: `/opt/v7/egress/state`
- events root: `/opt/v7/events`
- audit root: `/opt/v7/audit`
- admin root: `/opt/v7/admin`
- release root: `/opt/v7/releases`
- current release link: `/opt/v7/releases/current`
- deploy manifest: `/opt/v7/deploy-manifest.json`
- autoswitch binary: `/usr/local/bin/v7-users-autoswitch`
- audit binary: `/usr/local/bin/v7-audit-log`
- autoswitch service: `/etc/systemd/system/v7-users-autoswitch.service`
- autoswitch timer: `/etc/systemd/system/v7-users-autoswitch.timer`
