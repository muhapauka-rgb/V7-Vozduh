# V7 Phase100: Add egress wizard UI foundation

## Human Meaning

The add-channel flow is now clearer for an operator.

Instead of showing only raw JSON, the admin UI now explains the staged path:

```text
Detect -> Draft -> Preflight -> Runtime -> Quarantine -> Add Disabled -> Provision -> Enable
```

The technical JSON is still available, but it is hidden behind an expandable
technical section.

## Terms

- Wizard: a guided step-by-step UI flow.
- Source: where the config comes from: file, pasted text, or share URI.
- Detect: protocol recognition and required-field preview.
- Technical JSON: exact backend response kept for debugging.

## What Changed

Updated:

- `admin/v7-admin-api`

Added to the Add Egress Draft modal:

- file upload for `.conf`, `.json`, `.ovpn`, `.yaml`, `.yml`, `.txt`;
- automatic label suggestion from uploaded filename;
- clear Safe Path panel with each onboarding step;
- readable result rendering for preview/check/action responses;
- required fields table;
- checks table;
- pool preview summary;
- enable readiness summary;
- expandable `Technical JSON` details.

## Safety Model

This phase is UI-only.

It does not:

- change routing;
- enable channels;
- start tunnels;
- move users;
- alter kill switch;
- change backend safety rules.

The existing backend guards from Phases 91-99 remain the authority.

## Validation

Local compile with warnings treated as errors:

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

VPS deploy validation:

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

UI markers verified in deployed file:

```text
Upload config file
Safe Path
Provision Runtime
Technical JSON
```

## Current Status

Phase100 is complete.

The add-egress flow now has a clearer operator-facing UI foundation while still
keeping exact technical output available.

## Next Step

Phase101 should expand protocol adapters.

Human meaning:

- V7 already handles WireGuard and AmneziaWG provisioning;
- next we should teach the draft pipeline to convert VLESS, VMess, Trojan,
  Shadowsocks, sing-box JSON, and xray JSON into isolated runtime profiles;
- each adapter should stay quarantined until its own direct tests pass.
