# V7 Phase: Happ Subscription Delivery

Date: 2026-05-09

## Goal

Use the now-enabled public V7 proxy inbound to generate client profiles for
`happ` without exposing proxy UUIDs in logs or permanent UI output.

## Implemented

Updated:

- `client/v7-smart-client-profile-generate`
- `admin/v7-admin-api`

## Behavior

`happ` is now a supported smart client adapter.

For `happ`, the generator writes a VLESS subscription text file:

```text
/root/v7-smart-clients/<client>/happ-<mode>.txt
```

The file contains the actual VLESS link and is secret-bearing. The command
prints only metadata and never prints the UUID.

The generator reads:

```text
/etc/v7/inbound-runtime/happ-test/bindings/user-<ip>.json
/etc/v7/inbound-runtime/happ-test/public-candidate/metadata.json
```

It requires the public proxy service to be active:

```text
v7-proxy-inbound-happ-test.service
```

## Admin Delivery

The existing one-time delivery mechanism now supports `.txt` profiles:

- `GET /api/smart-client-profile` returns `text/plain` for happ profiles;
- `GET /profile-delivery/<token>` returns `text/plain` for one-time happ delivery;
- delivery still uses TTL, one-time use, and audit tombstones.

## Safety

- The VLESS UUID is written only into the profile file.
- Metadata stores only a redacted UUID hint.
- UI/API downloads set `Cache-Control: no-store`.
- The profile can be revoked through the existing delivery revoke flow.

## Validation

VPS checks:

```text
v7-admin-api active
V7_SMART_CLIENT_PROFILE=OK
adapter=happ
mode=RU_LOCAL
profile_path=/root/v7-smart-clients/user-10-0-0-2/happ-ru_local.txt
profile_prefix=vless://
metadata_json=OK
V7_RESULT=OK
```

Do not paste the generated VLESS link into chat or logs.
