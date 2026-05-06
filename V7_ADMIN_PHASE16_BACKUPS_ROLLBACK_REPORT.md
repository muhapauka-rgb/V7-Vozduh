# V7 Admin Phase 16 - Backups And Rollback

Date: 2026-05-06
Server: 195.2.79.116

## Goal

Add a safer backup/rollback control layer to V7 Admin:

- create backup from the UI;
- verify a selected backup;
- download a selected backup;
- preview restore impact without extracting files;
- preview the latest single-file rollback;
- apply the latest single-file rollback only with explicit confirmation.

## Files Updated Locally

- `admin/v7-admin-api`
- `hardening/v7-safe-run`
- `hardening/v7-backup-restore-preview`

## Installed On VPS

Installed to:

- `/usr/local/bin/v7-admin-api`
- `/usr/local/bin/v7-safe-run`
- `/usr/local/bin/v7-backup-restore-preview`

Restarted:

- `v7-admin-api`

No V7 routing, VPN interface, benchmark, health, kill switch, WireGuard, sing-box, or AmneziaWG service was restarted.

## Admin API Added

- `GET /api/backup-download?name=<backup-name>`
- `POST /api/actions/backup-verify`
- `POST /api/actions/backup-restore-preview`
- `POST /api/actions/rollback-preview`
- `POST /api/actions/rollback-apply`

Security behavior:

- all API actions require auth and CSRF;
- backup names must match `v7-backup-...-YYYYMMDD-HHMMSS.tar.gz`;
- backup download is restricted to `/root/v7-backups`;
- rollback apply requires typed confirmation `ROLLBACK`;
- full archive restore is preview-only for now.

## Admin UI Added

Backup rows now have:

- `Verify`;
- `Restore Preview`;
- `Download`.

Global actions now have:

- `Rollback Preview`;
- `Apply Last Rollback`.

## Restore Preview

New read-only script:

- `v7-backup-restore-preview <archive>`

It verifies:

- sha256 when present;
- tar readability;
- total file count;
- impact by category:
  - `/usr/local/bin/`
  - `/etc/systemd/system/`
  - `/etc/wireguard/`
  - `/etc/amnezia/`
  - `/etc/amneziawg/`
  - `/etc/sing-box/`
  - `/etc/v7/`
  - `/opt/v7/`

It does not extract or modify files.

## Validation

Local validation:

- `python3 -m py_compile admin/v7-admin-api` - OK
- `bash -n hardening/v7-safe-run` - OK
- `bash -n hardening/v7-backup-restore-preview` - OK

VPS validation:

- `v7-admin-api` active - OK
- `/api/actions/backup-verify` on latest backup - OK
- `/api/actions/backup-restore-preview` on latest backup - OK
- `/api/backup-download` on latest backup - HTTP 200
- `/api/actions/rollback-preview` - OK
- `/api/actions/rollback-apply` without confirmation - HTTP 400
- `v7-system-check` - OK
- `v7-killswitch-check` - OK

Restore preview sample:

- `/usr/local/bin/ files=90`
- `/etc/systemd/system/ files=8`
- `/etc/wireguard/ files=8`
- `/etc/amnezia/ files=2`
- `/etc/amneziawg/ files=1`
- `/etc/sing-box/ files=2`
- `/etc/v7/ files=6`
- `/opt/v7/ files=213`

## Backups

Pre-install backup:

- `/root/v7-phase16-backup-admin-backup-20260506-232726`

Restore-preview fix backup:

- `/root/v7-phase16-restore-preview-fix-backup-20260506-232857`

Final full V7 backup:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-233010.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-233010.tar.gz.sha256`

## Notes

Full archive restore remains intentionally preview-only. A real full restore should be implemented as a staged wizard later:

1. verify archive;
2. create emergency backup;
3. show exact files to restore;
4. stop only required services;
5. restore selected categories;
6. daemon-reload if needed;
7. run `v7-system-check`;
8. allow rollback if checks fail.

