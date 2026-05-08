# V7 Phase96: Guarded egress draft add-to-pool

## Human Meaning

V7 can now take a tested draft VPN channel and add it to the channel pool safely.

Important: this does not make the channel carry user traffic immediately.
The new channel is added with `enabled=0`, which means "known to V7, but
disabled". Enabling it remains a separate operator action.

## Terms

- Draft: a saved VPN config that is still isolated from the live system.
- Pool: the active egress registry at `/opt/v7/egress/state/egress.registry`.
- Add disabled: write the egress into the pool with `enabled=0`.
- Backup: timestamped copies of files created before any mutation.
- Guarded apply: an apply action that refuses to run unless required checks pass.

## What Changed

Updated:

- `admin/v7-admin-api`

Added admin API action:

```text
POST /api/actions/egress-draft-pool-apply
```

Added UI button in the egress draft modal:

```text
Add Disabled
```

## Safety Rules

The action is blocked unless the draft has:

- `last_preflight_status=PASS`
- `last_runtime_status=PASS`
- `last_quarantine_status=PASS`
- no duplicate egress id in `egress.registry`
- a supported protocol

When it does run, it:

- creates a backup of `egress.registry`;
- creates a backup of the draft metadata;
- appends one registry line with `enabled=0`;
- updates draft metadata to `pool_added_disabled`;
- does not move users;
- does not change routes;
- does not restart V7 services.

## Local Validation

Local compile:

```text
python3 -m py_compile admin/v7-admin-api hardening/v7-egress-draft-runtime-helper
```

Result:

```text
OK
```

Diff whitespace check:

```text
git diff --check
```

Result:

```text
OK
```

Functional temporary-path test:

```json
{
  "err": null,
  "pool_action": "added_disabled",
  "enabled": "0",
  "line_present": true,
  "users_moved": false,
  "status": "pool_added_disabled",
  "backup_count": 1
}
```

Blocked temporary-path test:

```json
{
  "error": "egress_draft_not_ready_for_pool",
  "blockers": [
    "runtime_not_passed",
    "quarantine_not_passed"
  ],
  "line_absent": true
}
```

## VPS Validation

Deployed to:

```text
/usr/local/bin/v7-admin-api
```

Backup created before replacement:

```text
/usr/local/bin/v7-admin-api.bak.phase96.<timestamp>
```

Validation:

```text
python3 -m py_compile /usr/local/bin/v7-admin-api
systemctl restart v7-admin-api
systemctl is-active v7-admin-api
curl -fsS http://127.0.0.1:7080/health
```

Result:

```text
active
status=OK
```

VPS temporary-path apply test:

```json
{
  "err": null,
  "pool_action": "added_disabled",
  "enabled": "0",
  "line_present": true,
  "users_moved": false,
  "status": "pool_added_disabled",
  "backup_count": 1
}
```

Production registry safety check:

```text
grep -R phase96-vps-test /opt/v7/egress/state/egress.registry /opt/v7/egress/state/users.registry
```

Result:

```text
no matches
```

## Current Status

Phase96 is complete.

V7 now has a staged egress onboarding flow:

1. Preview config.
2. Save inactive draft.
3. Run preflight.
4. Run isolated runtime.
5. Run quarantine.
6. Preview add-to-pool.
7. Add to pool disabled.
8. Enable later as a separate explicit action.

## Next Step

Phase97 should add disabled-profile provisioning visibility.

Human meaning:

- after a draft is added to the pool, the admin should clearly show what runtime
  profile/config belongs to that channel;
- V7 should explain whether the channel is ready to be enabled;
- if runtime provisioning is missing, the UI should show that before an operator
  tries to enable the channel.
