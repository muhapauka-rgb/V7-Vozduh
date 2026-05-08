# V7 Phase99: Runtime profile provisioning

## Human Meaning

V7 can now prepare the real runtime profile for a tested draft channel after it
has been added to the pool as disabled.

This means the channel can move from:

```text
pooled_disabled but not technically ready
```

to:

```text
pooled_disabled and ready for explicit enable
```

The channel is still not started, users are not moved, and routing is not
changed.

## Terms

- Runtime profile: the root-only config file V7 can use later to start a channel.
- Provisioning: writing that runtime profile into a managed path.
- Managed path: a predictable V7-owned location such as `/etc/wireguard/<if>.conf`.
- Enable readiness: whether V7 can prove the channel is technically ready before enabling it.

## What Changed

Updated:

- `admin/v7-admin-api`

Added configurable runtime paths:

```text
V7_WIREGUARD_DIR=/etc/wireguard
V7_AMNEZIAWG_DIR=/etc/amnezia/amneziawg
V7_EGRESS_RUNTIME_DIR=/etc/v7/egress-runtime
```

Added deterministic short interface names for new interface-mode draft channels:

```text
v7e<10-char-hash>
```

This keeps generated interface names under Linux's interface-name limit.

Added admin API action:

```text
POST /api/actions/egress-draft-runtime-provision
```

Added UI action in the draft table:

```text
Provision Runtime
```

## Current Protocol Support

Implemented in this phase:

```text
WireGuard
AmneziaWG
```

Not yet provisioned in this phase:

```text
VLESS / VMess / Trojan / Shadowsocks / sing-box JSON / xray JSON
```

Those need protocol-specific runtime adapters in later phases.

## Safety Rules

Runtime provisioning is blocked unless:

- the draft exists;
- the draft was already added to pool as disabled;
- the pool entry exists in `egress.registry`;
- the pool entry still has `enabled=0`;
- protocol adapter is supported;
- target interface name is valid and short enough;
- sanitized config passes validation;
- target profile path is empty or already contains identical content.

It does not:

- start the tunnel;
- enable the channel;
- move users;
- change routes;
- restart V7 routing services;
- update kill switch.

## Files Written

For WireGuard:

```text
/etc/wireguard/<managed-interface>.conf
```

For AmneziaWG:

```text
/etc/amnezia/amneziawg/<managed-interface>.conf
```

Draft metadata is updated with:

```text
runtime_profile_status
runtime_profile_path
runtime_profile_interface
runtime_profile_provisioned_at
runtime_profile_provisioned_by
```

## Local Validation

Compile:

```text
python3 -m py_compile admin/v7-admin-api hardening/v7-egress-draft-runtime-helper
```

Result:

```text
OK
```

Whitespace check:

```text
git diff --check
```

Result:

```text
OK
```

Temporary-path functional test:

```json
{
  "pool_error": null,
  "provision_error": null,
  "pool_action": "added_disabled",
  "profile_status": "READY",
  "target_exists": true,
  "target_under_tmp": true,
  "enabled": true,
  "metadata_status": "READY",
  "readiness": "READY"
}
```

Blocked case:

```json
{
  "res": null,
  "error": "runtime_provision_requires_added_disabled_pool_entry",
  "target_count": 0
}
```

## VPS Validation

Deployed to:

```text
/usr/local/bin/v7-admin-api
```

Backup created before replacement:

```text
/usr/local/bin/v7-admin-api.bak.phase99.<timestamp>
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

VPS temporary-path provisioning test:

```json
{
  "pool_error": null,
  "provision_error": null,
  "profile_status": "READY",
  "target_exists": true,
  "target_under_tmp": true,
  "readiness": "READY"
}
```

The VPS functional test used temporary environment paths, so production
`/etc/wireguard`, production `egress.registry`, users, routes, and services were
not modified by the test.

## Current Status

Phase99 is complete.

The staged onboarding chain is now:

```text
Save Draft
Preflight
Runtime Test
Quarantine
Pool Preview
Add Disabled
Provision Runtime Profile
Enable Readiness
Guarded Enable
```

## Next Step

Phase100 should improve the Add Egress Wizard UI.

Human meaning:

- replace raw JSON-heavy draft workflow with a clearer step-by-step wizard;
- show statuses in plain language;
- keep technical details expandable;
- make the operator path obvious:
  upload, detect, test, quarantine, add disabled, provision runtime, enable.
