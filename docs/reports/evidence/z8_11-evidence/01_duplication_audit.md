# Z8.11 Duplication Audit

## Production execution binaries

Authoritative production execution paths:

- `/usr/local/bin/v7-users-autoswitch`
- `/usr/local/bin/v7-admin-api`
- `/usr/local/bin/v7-audit-log`

Production services reference these paths:

- `v7-users-autoswitch.service`: `ExecStart=/usr/local/bin/v7-users-autoswitch --apply`
- `v7-admin-api.service`: `ExecStart=/usr/local/bin/v7-admin-api`

## Stale/backup copies

Additional autoswitch copies were found only under backup paths:

- `/opt/v7/backups/stable-state-split-20260505-233947/v7-users-autoswitch`
- `/opt/v7/backups/stable-core-20260505-230621/v7-users-autoswitch`
- `/opt/v7/backups/clean-core-20260505-234929/v7-users-autoswitch`
- `/opt/v7/backups/final-state-split-ok-20260505-234252/v7-users-autoswitch`

These were classified as BACKUP/DO_NOT_TOUCH.

## Runtime root

`/opt/v7` is the authoritative production runtime/state root, not a git checkout. The production deployment model is copied binaries plus provenance manifests.

