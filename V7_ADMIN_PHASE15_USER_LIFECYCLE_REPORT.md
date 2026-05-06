# V7 Admin Phase 15 - User Lifecycle

Date: 2026-05-06
Server: 195.2.79.116

## Goal

Add safer user lifecycle operations to V7 Admin without changing the current routing architecture:

- enable a disabled user;
- reissue an existing WireGuard config/QR without rotating keys;
- rotate a user key only with explicit confirmation;
- keep dry-run support for safe diagnostics;
- avoid exposing private keys or passwords in API output.

## Files Updated Locally

- `admin/v7-admin-api`
- `hardening/v7-user-disable`
- `hardening/v7-user-enable`
- `hardening/v7-user-reissue-config`
- `hardening/v7-user-rotate-key`
- `hardening/v7-safe-run`

## Installed On VPS

Installed to:

- `/usr/local/bin/v7-admin-api`
- `/usr/local/bin/v7-safe-run`
- `/usr/local/bin/v7-user-disable`
- `/usr/local/bin/v7-user-enable`
- `/usr/local/bin/v7-user-reissue-config`
- `/usr/local/bin/v7-user-rotate-key`

Restarted:

- `v7-admin-api`

No tunnel, routing, WireGuard, AmneziaWG, sing-box, or V7 health/benchmark service was restarted during this phase.

## Admin API Endpoints Added

- `POST /api/actions/user-enable`
- `POST /api/actions/user-reissue-config`
- `POST /api/actions/user-rotate-key`

Security behavior:

- all endpoints require auth and CSRF;
- IP input is validated as `10.0.0.x`;
- rotate requires `confirm=ROTATE` unless `dry_run=true`;
- command output is passed through the existing redaction layer.

## Admin UI Added

User rows now include:

- `Enable` for disabled users;
- `Reissue Config`;
- `Rotate Key`.

Rotate uses a typed browser confirmation: `ROTATE`.

## Lifecycle Safety Fix

Important issue found and fixed:

Older `v7-user-disable` removed the WireGuard peer from `wg0.conf`. For users without a saved client artifact, that could make later re-enable impossible because the public key would be gone.

Fix:

- `v7-user-disable` now saves the peer public key to:
  - `/opt/v7/egress/state/disabled-peers/<client-ip>.public.key`
- `v7-user-enable` can restore the peer from either:
  - `/root/v7-clients/<name>/public.key`, or
  - `/opt/v7/egress/state/disabled-peers/<client-ip>.public.key`

This preserves compatibility with future admin-created users and protects older manually migrated users after the next disable operation.

## Validation

Local validation:

- `python3 -m py_compile admin/v7-admin-api` - OK
- `bash -n hardening/v7-safe-run` - OK
- `bash -n hardening/v7-user-disable` - OK
- `bash -n hardening/v7-user-enable` - OK
- `bash -n hardening/v7-user-reissue-config` - OK
- `bash -n hardening/v7-user-rotate-key` - OK

VPS validation:

- `v7-admin-api` active - OK
- `v7-user-reissue-config 10.0.0.3 --dry-run` - OK
- `v7-user-rotate-key 10.0.0.3 --dry-run` - OK
- `v7-safe-run v7-user-rotate-key 10.0.0.3 --dry-run` - OK
- `v7-safe-run v7-user-rotate-key 10.0.0.3` - blocked with rc=2
- Admin API dry-run for reissue - OK
- Admin API dry-run for rotate - OK
- Admin API rotate without confirmation - HTTP 400
- `v7-user-disable 10.0.0.2 --dry-run` sees public key - OK
- `v7-system-check` - OK
- `v7-killswitch-check` - OK

Current users after phase:

- `10.0.0.2 current=awg2 table=100 enabled=1`
- `10.0.0.3 current=awg2 table=101 enabled=1`

Routes remained on `awg2`.

## Backups

Pre-install admin backup:

- `/root/v7-phase15-admin-lifecycle-backup-20260506-231658`

Lifecycle fix backup:

- `/root/v7-phase15-lifecycle-fix-backup-20260506-232119`

Final full V7 backup:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-232143.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-232143.tar.gz.sha256`

## Notes

No actual key rotation was performed.

For old user `10.0.0.2`, `v7-user-enable --dry-run` before disable still reports no saved public-key source. This is expected because the user is currently enabled and no client artifact exists under `/root/v7-clients`. If this user is disabled through the new script, its public key will be saved first and enable will be able to restore it.

