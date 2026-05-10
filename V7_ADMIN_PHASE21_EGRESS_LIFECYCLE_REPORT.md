# V7 Admin Phase 21: Egress Lifecycle

Date: 2026-05-07 00:05 MSK

## Goal

Add safe egress lifecycle management to V7 Admin:

- enable egress
- put egress into maintenance
- disable egress
- block risky changes when users are still assigned
- expose preview/apply flow in Admin UI
- keep safe mode read-only

## Installed On VPS

VPS: 195.2.79.116

Installed files:

- `/usr/local/bin/v7-egress-set-state`
- `/usr/local/bin/v7-safe-run`
- `/usr/local/bin/v7-admin-api`

Backup before install:

- `/root/v7-phase21-egress-lifecycle-backup-20260507-000401`

Fresh full backup after validation:

- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260507-000453.tar.gz`
- `/root/v7-backups/v7-backup-v3119922.hosted-by-vdsina.ru-20260507-000453.tar.gz.sha256`

Backup files count:

- `338`

## Backend Changes

### `v7-egress-set-state`

New lifecycle helper:

```bash
v7-egress-set-state <egress_id> <enabled|maintenance|disabled>
v7-egress-set-state <egress_id> <enabled|maintenance|disabled> --apply
```

Behavior:

- validates that egress exists in `egress.registry`
- supports dry-run preview by default
- writes lifecycle state to `/opt/v7/egress/state/egress-flags.state`
- updates `enabled=` in `/opt/v7/egress/state/egress.registry`
- creates timestamped backup before mutation
- logs structured audit event

Guard:

- `maintenance` and `disabled` are blocked if assigned users exist on that egress
- this protects active users from being stranded by an admin click

### `v7-safe-run`

Added `v7-egress-set-state` to the safe-mode allowlist.

Safe mode allows preview only and blocks `--apply`:

```text
BLOCKED: v7-egress-set-state apply is not allowed in safe mode
```

### `v7-admin-api`

New API endpoints:

- `POST /api/actions/egress-set-state-preview`
- `POST /api/actions/egress-set-state-apply`

Apply confirmation:

- `enabled` requires confirmation text `ENABLE`
- `maintenance` requires confirmation text `MAINTENANCE`
- `disabled` requires confirmation text `DISABLED`

The admin overview now includes:

- `overview.registries.egress_flags_map`

## Admin UI Changes

The Egress table now has:

- lifecycle/pool status column
- `Enable` button
- `Maintenance` button
- `Disable` button

The UI flow is:

1. Admin clicks lifecycle action.
2. Admin API runs preview first.
3. If preview is safe, browser asks typed confirmation.
4. Apply runs only after the correct confirmation text.
5. UI refreshes overview.

## Validation

### Current Users

```text
ip=10.0.0.2 current=awg2 table=100 enabled=1
ip=10.0.0.3 current=awg2 table=101 enabled=1
```

No users were moved during this phase.

### Current Egress Flags

```text
vless_state=enabled
```

Current `egress.registry` remains enabled for both egresses:

```text
id=vless ... enabled=1
id=awg2 ... enabled=1
```

### Guard Tests

`awg2 maintenance` preview was blocked because users are assigned:

```text
assigned users:
10.0.0.2 table=100
10.0.0.3 table=101
```

`vless maintenance` preview succeeded because no users are currently assigned to `vless`.

`v7-safe-run v7-egress-set-state vless enabled --apply` was blocked as expected.

Admin API apply without confirmation returned HTTP `400`.

Admin API apply with `ENABLE` succeeded for `vless enabled`.

### Routing

```text
V7_USER_ROUTE_CHECK=OK
```

Route reality:

- `10.0.0.2` uses table `100`, default dev `awg2`
- `10.0.0.3` uses table `101`, default dev `awg2`

### Services

All checked services are active:

- `v7-api`
- `v7-health`
- `v7-benchmark`
- `v7-killswitch`
- `dnsmasq`
- `v7-admin-api`
- `v7-client-speed-api`

### System Check

```text
V7_RESULT=OK
```

Direct egress checks:

- `vless_ip=77.110.103.131`
- `awg2_ip=94.241.139.241`

### Kill Switch

```text
V7_KILLSWITCH_CHECK=OK
```

Both user route checks do not leak to the public interface.

### Audit

Recent structured audit events include:

- `admin_action_egress_set_state_preview`
- `admin_action_egress_set_state_apply`
- `egress_set_state`

## Result

Phase 21 is complete.

Egress lifecycle management is now available in Admin with preview, typed confirmation, active-user protection, structured audit logging, and safe-mode protection.

No active users were moved.
No egress was accidentally disabled.
The final applied state only confirmed `vless` as `enabled`.

