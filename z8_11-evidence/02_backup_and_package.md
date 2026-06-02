# Z8.11 Backup And Package

## Backup certification

Backup path:

`/root/v7-deploy-backups/z8-11-pre-convergence-20260602T144500MSK`

Backed up:

- `/usr/local/bin/v7-users-autoswitch`
- `/usr/local/bin/v7-admin-api`
- `/usr/local/bin/v7-audit-log`
- previous deploy metadata from `/opt/v7/ops/deploy-a-v7-next-12e51a5-20260601T093725Z`

Pre-deploy hashes:

- `v7-users-autoswitch`: `8eedfae073f756d0c70a893b477cf1c19996e467a9e9e3d4bacb116cc20d4c4c`
- `v7-admin-api`: `acbdce035c6f33ad28bd40abb8b76ac1887db9e57f87d696eae98633d760345a`
- `v7-audit-log`: `c2a524d4b5b2023dfd3a2923c1f3148ad647853fd00e50454d3cd7095d3f0a86`

Rollback instruction:

Copy the backed-up files from `usr-local-bin/` back to `/usr/local/bin/` with preserved permissions, then restart only affected services if approved.

## Deployment package

Package id:

`z8-11-Updatesystem-ff91005-20260602T144500MSK`

Authoritative package hashes:

- `tools/v7-users-autoswitch`: `a5480fdfe33c3618aeea345899b98cfad259001576069e9f3721ce01add5d0d3`
- `admin/v7-admin-api`: `8da1e5479723891f8619bbf5296239afb7e41d27f456b9601bd9799d289b705e`
- `tools/runtime-support/v7-audit-log`: `c2a524d4b5b2023dfd3a2923c1f3148ad647853fd00e50454d3cd7095d3f0a86`

Remote staging path:

`/tmp/v7-z811-package-ff91005`

Remote staging hashes and py_compile checks passed before replacement.

