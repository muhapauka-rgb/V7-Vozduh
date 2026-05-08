# V7 Phase 69: One-time Profile Delivery

Date: 2026-05-08

## Goal

Stop treating secret-bearing Karing JSON profiles as ordinary permanent
downloads. Add one-time delivery links with TTL and audit trail.

## Implemented

Updated:

- `admin/v7-admin-api`

Added state file:

```text
/opt/v7/egress/state/profile-delivery-tokens.json
```

Default TTL:

```text
V7_PROFILE_DELIVERY_TTL_SECONDS=1800
```

## Admin UX

In `Users -> Details -> Smart Client Profiles`:

- generated profiles now have `One-time Link`;
- selected ready profile has `One-time Link`;
- generated link is printed in the admin `Actions` panel with TTL and safety note.

## API

Authenticated admin action:

```text
POST /api/actions/profile-delivery-create
```

Body:

```json
{
  "ip": "10.0.0.3",
  "adapter": "karing",
  "mode": "RU_LOCAL"
}
```

Unauthenticated token download endpoint:

```text
GET /profile-delivery/<token>
```

The endpoint is protected by high-entropy token, TTL and one-time use. It is
still served by the local-only admin API unless the deployment explicitly adds a
public delivery layer later.

## Safety

Delivery token rows store the profile path only until use/expiry. After the
download, the row is converted into a tombstone and `profile_path` is removed.

The endpoint:

- rejects invalid tokens;
- rejects expired tokens;
- rejects already used tokens;
- restricts profile path under `/root/v7-smart-clients`;
- audits successful downloads;
- audits failed token use.

No profile contents are rendered in the admin UI.

## Important Operational Note

The admin API currently listens on `127.0.0.1:7080`. If the operator opens it
through SSH tunnel, the one-time URL works through that same tunnel. A future
public user-facing delivery service should expose only this token endpoint, not
the full admin UI.

## Validation

Local syntax:

```text
admin_syntax_ok
```

VPS validation:

```text
syntax_ok
v7-admin-api active
127.0.0.1:7080 listening
admin login page responds
V7_RESULT=OK
vless_ip=77.110.103.131
awg2_ip=94.241.139.241
```

One-time token behavior:

```text
first_download=200 2783
second_download=404 52
```

The profile body was not printed during validation.

Previous admin binary backup on VPS:

```text
/usr/local/bin/v7-admin-api.bak.20260508-141511
```
