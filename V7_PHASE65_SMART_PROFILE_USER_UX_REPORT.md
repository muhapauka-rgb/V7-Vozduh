# V7 Phase 65: Smart Profile User UX

Date: 2026-05-08

## Goal

Make smart client profiles usable from the admin UI for an operator, not only
available as raw API output.

## Implemented

Updated:

- `admin/v7-admin-api`

Admin user details now show:

- WireGuard config and QR download links;
- generated smart client profiles;
- Karing JSON download links;
- per-mode explanations;
- generate action per mode;
- selected adapter/mode metadata.

## New Metadata

Selected smart profile mode is stored in:

```text
/opt/v7/egress/state/client-profile-preferences.json
```

This is metadata only. Selecting a smart mode does not rewrite the user's
server-side route and does not restart services.

## New API

```text
POST /api/actions/smart-client-profile-select
```

POST body:

```json
{
  "ip": "10.0.0.3",
  "adapter": "karing",
  "mode": "RU_LOCAL"
}
```

The action is:

- admin-only;
- blocked by Admin Safe Mode;
- audited in the admin audit log.

## Operator Meaning

The selected mode is the intended client profile for the user:

- `RU_LOCAL`: RU domains leave directly from the device, global/video goes to V7.
- `ABROAD_RU_VIA_V7`: ordinary RU goes to V7 Moscow route, sensitive RU still
  needs a proven `RU_GOV_ABROAD` route.
- `AUTO_TRAVEL`: profile contains selectors for travel mode.
- `STRICT_V7`: all traffic goes through V7.

## Safety

The admin UI still does not render profile secrets. Downloaded JSON profiles do
contain client keys by design, so downloads remain authenticated admin-only.

## VPS Deployment

Previous admin binary was backed up on the VPS as:

```text
/usr/local/bin/v7-admin-api.bak.20260508-120404
```

Validation:

```text
syntax_ok
v7-admin-api active
127.0.0.1:7080 listening
admin login page responds
V7_RESULT=OK
vless_ip=77.110.103.131
awg2_ip=94.241.139.241
```
