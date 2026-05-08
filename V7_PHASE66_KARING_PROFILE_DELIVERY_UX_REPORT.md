# V7 Phase 66: Karing Profile Delivery UX

Date: 2026-05-08

## Goal

Make Karing profile delivery clear enough for an operator to use without
opening raw diagnostics.

## Implemented

Updated:

- `admin/v7-admin-api`

In `Users -> Details`, the admin UI now shows a dedicated selected smart profile
panel with:

- selected adapter;
- selected mode;
- mode meaning;
- ready/not-ready state;
- `Generate Selected`;
- `Download Selected`;
- `Import Steps`.

Each smart profile row also has:

- `Generate`;
- `Select`;
- `Steps`;
- direct download link when the profile exists.

## Karing Import Steps

The operator can now open per-user import instructions directly in the admin
`Actions` panel.

The instructions include:

- which mode is being issued;
- when to use it;
- how to import JSON into Karing;
- what to test after import;
- key safety reminders.

## Safety

Karing JSON profiles contain client key material. The admin UI still does not
render profile contents. It only downloads the file through an authenticated
admin endpoint.

QR for JSON profiles is intentionally not shown yet because it would encode the
same secret-bearing profile body. A future version should use one-time delivery
links with TTL and download audit before exposing QR delivery.

## Next Step

Add controlled profile delivery:

- one-time download token;
- short TTL;
- download audit event;
- revoke delivery token;
- optional QR for the one-time delivery URL, not for the raw JSON body.

## VPS Deployment

Previous admin binary was backed up on the VPS as:

```text
/usr/local/bin/v7-admin-api.bak.20260508-124749
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
