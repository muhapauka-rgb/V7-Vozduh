# V7 Phase101: Proxy protocol adapter foundation

## Human Meaning

V7 can now understand common proxy share links well enough to prepare disabled
sing-box runtime profiles.

This does not make a new channel active. It only prepares the profile that can
later be tested, quarantined, and explicitly enabled.

## Terms

- Share link: a VPN/proxy URI such as `vless://...`, `trojan://...`, `ss://...`.
- Adapter: code that converts a protocol format into V7's runtime model.
- sing-box profile: a JSON config V7 can later run for proxy-mode egress.
- socks inbound: local `127.0.0.1:<port>` entry point used by V7 tests/routing.

## What Changed

Updated:

- `admin/v7-admin-api`

Added share-link parsing for:

```text
VLESS
VMess
Trojan
Shadowsocks
```

Added sing-box runtime profile generation for proxy-mode drafts.

For new proxy egresses, pool preview now proposes:

```text
test=socks5://127.0.0.1:<managed-port>
config=/etc/v7/egress-runtime/<egress_id>/config.json
enabled=0
```

The managed local port is deterministic from the egress id, so preview/apply
remain stable.

## Current Adapter Scope

Implemented:

- parse required fields;
- build a sing-box JSON profile;
- write profile root-only during runtime provisioning;
- keep channel disabled;
- keep technical output available for audit/debugging.

Not yet implemented:

- starting those proxy profiles through dedicated systemd units;
- isolated runtime launch for proxy profiles;
- live service matrix through newly provisioned proxy profiles;
- collision handling for managed local ports beyond deterministic selection.

These are intentionally later steps.

## Safety Model

Proxy adapter provisioning is blocked unless:

- the draft exists;
- it was added to pool as disabled;
- the pool entry still has `enabled=0`;
- the share link or sing-box JSON can be parsed;
- a valid local listen port can be assigned;
- the target runtime profile path is empty or already identical.

It does not:

- start sing-box;
- enable the egress;
- move users;
- change routes;
- alter kill switch.

## Local Validation

Compile with warnings as errors:

```text
python3 -W error -m py_compile admin/v7-admin-api hardening/v7-egress-draft-runtime-helper
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

Temporary-path VLESS provisioning test:

```json
{
  "preview_protocol": "vless",
  "preview_missing": [],
  "pool_error": null,
  "provision_error": null,
  "status": "READY",
  "target_exists": true,
  "inbound_type": "socks",
  "outbound_type": "vless",
  "enabled": true
}
```

## VPS Validation

Deployed to:

```text
/usr/local/bin/v7-admin-api
```

Backup created before replacement:

```text
/usr/local/bin/v7-admin-api.bak.phase101.<timestamp>
```

Validation:

```text
python3 -W error -m py_compile /usr/local/bin/v7-admin-api
systemctl restart v7-admin-api
systemctl is-active v7-admin-api
curl -fsS http://127.0.0.1:7080/health
```

Result:

```text
active
status=OK
```

VPS temporary-path Trojan provisioning test:

```json
{
  "pool_error": null,
  "provision_error": null,
  "status": "READY",
  "target_under_tmp": true,
  "outbound_type": "trojan"
}
```

The VPS test used temporary paths and did not modify production routing,
production users, or production egress registry.

## Current Status

Phase101 is complete as adapter foundation.

The add-channel pipeline can now convert interface-mode configs and common
proxy share links into disabled runtime profiles.

## Next Step

Phase102 should add egress roles and usage policy metadata.

Human meaning:

- a channel should not just be "a VPN";
- it should have a role such as `GLOBAL_FAST`, `VIDEO_OPTIMIZED`,
  `GLOBAL_STABLE`, `RESERVE`, or `MANUAL_ONLY`;
- V7 can then decide where the channel belongs before it ever receives users.
