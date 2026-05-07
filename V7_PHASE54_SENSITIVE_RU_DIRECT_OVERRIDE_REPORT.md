# V7 Phase 54: Sensitive RU Direct Override Guard

Date: 2026-05-07

## Goal

Prevent broad `.ru` direct routing from capturing services that must use the
`TRUSTED_RU_SENSITIVE` route class, such as Gosuslugi, ESIA, and banking
domains.

## Diagnosis

Before the fix, `gosuslugi.ru`, `www.gosuslugi.ru`, and `esia.gosuslugi.ru`
were resolved into the direct RU nft set and were not present in
`/etc/v7/direct/exclude.conf`.

Observed decision before:

```text
domain=gosuslugi.ru
direct_set=yes
direct_exclude=no
decision=DIRECT_READY
```

This meant broad `.ru` direct could override the intended
`TRUSTED_RU_SENSITIVE -> vless` policy.

## Server Hotfix Applied

The following sensitive domains were added to the direct-exclude list using the
existing audited command path:

```text
gosuslugi.ru
www.gosuslugi.ru
esia.gosuslugi.ru
lk.gosuslugi.ru
gu-st.ru
```

Existing sensitive banking domains remained excluded.

## Code Changes

Added:

```text
hardening/v7-policy-sync-direct-excludes
```

This command syncs all `TRUSTED_RU_SENSITIVE` domains into
`/etc/v7/direct/exclude.conf`. Default mode is dry-run. Apply mode never removes
existing excludes.

Updated:

```text
hardening/v7-policy-domain-lib
admin/v7-admin-api
```

Policy domain changes now run the sensitive direct-exclude sync as part of the
rebuild pipeline. The admin panel also has a `Sync Sensitive Overrides` action
under Service-aware Policy.

## Validation

After applying the server hotfix and installing the code:

```text
gosuslugi.ru        -> VPN_PREFERRED_DIRECT_EXCLUDED
www.gosuslugi.ru    -> VPN_PREFERRED_DIRECT_EXCLUDED
esia.gosuslugi.ru   -> VPN_PREFERRED_DIRECT_EXCLUDED
lk.gosuslugi.ru     -> VPN_PREFERRED_DIRECT_EXCLUDED
gu-st.ru            -> VPN_PREFERRED_DIRECT_EXCLUDED
yandex.ru           -> DIRECT_READY
```

System checks:

```text
dnsmasq active
v7-admin-api active
http://127.0.0.1:7077/health -> OK
v7-system-check -> V7_RESULT=OK
vless external IP -> 77.110.103.131
awg2 external IP -> 94.241.139.241
```

## Rollback

Backups were created on the VPS before replacing admin/policy files:

```text
/usr/local/bin/v7-admin-api.backup.phase54.<timestamp>
/usr/local/lib/v7-policy-domain-lib.backup.phase54.<timestamp>
```

Direct exclude backups are created automatically by the direct-exclude command.
