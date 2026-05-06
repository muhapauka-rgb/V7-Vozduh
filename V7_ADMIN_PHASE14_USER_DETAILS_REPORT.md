# V7 Admin Phase 14: User Details View

Date: 2026-05-06

## Goal

Add a user details view so each user can be inspected without digging through multiple sections.

## Implemented

### Admin API

Added:

- `GET /api/user-detail?ip=<user_ip>`

The endpoint returns:

- registry row;
- state row;
- route reality;
- client speed freshness;
- client agent status;
- service preferences;
- service warnings;
- config/QR artifact links when available;
- switch history;
- pending/completed client commands.

### Admin UI

User rows now include:

- `Details` button;
- expandable JSON details row.

Existing controls remain:

- request speed;
- history;
- switch egress;
- disable user.

## Validation

### 10.0.0.2

Visible details:

- current egress: `awg2`
- table: `100`
- route reality: OK
- leak risk: false
- preferences: Telegram
- warning: Telegram fails on `awg2`, recommended `vless`
- pending command count: 1

### 10.0.0.3

Visible details:

- current egress: `awg2`
- table: `101`
- route reality: OK
- leak risk: false
- phone V7 speed: present and fresh
- phone direct speed: present and fresh
- config/QR artifact: `v7-iphone`
- no service warnings

### Secret Safety

Checked user detail JSON responses for secret patterns:

- `PrivateKey =`
- `PresharedKey =`
- `private_key`

Result:

- no secret patterns found.

## Final Checks

- All V7 services active.
- `v7-system-check` result:
  - `V7_RESULT=OK`
- `v7-killswitch-check` result:
  - `V7_KILLSWITCH_CHECK=OK`

## Backup

Post-phase backup was created on the VPS:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-230125.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260506-230125.tar.gz.sha256`

## Next Logical Step

Improve user lifecycle controls:

- regenerate QR/config;
- rotate user key;
- enable disabled user;
- safe delete user;
- show rollback target for last user change.
