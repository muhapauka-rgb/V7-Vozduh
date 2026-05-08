# V7 Phase 64: Smart Client Profile Admin Actions

Date: 2026-05-08

## Goal

Expose smart client profile generation in V7 Admin without leaking client
secrets into the API response or audit log.

## Implemented

Updated:

- `admin/v7-admin-api`
- `V7_PHASE63_KARING_PROFILE_GENERATOR_REPORT.md`

Admin now supports:

- generating Karing smart profiles from an existing WireGuard client config;
- validating generated JSON with `sing-box check`;
- listing generated smart profiles in `user_detail`;
- downloading generated smart profiles through an authenticated admin endpoint;
- blocking smart profile generation when Admin Safe Mode is enabled;
- auditing profile generation as an admin action.

## New API

```text
POST /api/actions/smart-client-profile-generate
GET  /api/smart-client-profile
```

POST body:

```json
{
  "ip": "10.0.0.3",
  "adapter": "karing",
  "mode": "RU_LOCAL"
}
```

Supported modes:

- `RU_LOCAL`
- `ABROAD_RU_VIA_V7`
- `AUTO_TRAVEL`
- `STRICT_V7`

## Safety

The API response returns only metadata and a download URL. It does not return
the generated profile body because the profile contains WireGuard private
material.

Generated files remain under:

```text
/root/v7-smart-clients/<client>/
```

Local exchanged copies remain ignored under:

```text
admin/smart-profiles/
```

## ABROAD_RU_VIA_V7 Clarification

`ABROAD_RU_VIA_V7` does not mean "all RU goes through one generic route".

It means:

```text
ordinary RU        -> V7 DIRECT_RU / Moscow public route
government/banks   -> V7 RU_GOV_ABROAD / separate trusted sensitive route
global/video       -> V7 global orchestration
```

The `RU_GOV_ABROAD` path is still a required future route candidate. Until it is
tested and marked healthy, the mode is useful as a profile structure, but it is
not a guarantee that Gosuslugi or banking will work from abroad.

## VPS Deployment

```text
python3 -m py_compile /usr/local/bin/v7-admin-api
systemctl restart v7-admin-api
systemctl is-active v7-admin-api
sing-box check -c /root/v7-smart-clients/v7-iphone/karing-ru_local.json
```

Validation result:

```text
syntax_ok
v7-admin-api active
admin login page responds on 127.0.0.1:7080
V7_RESULT=OK
vless_ip=77.110.103.131
awg2_ip=94.241.139.241
```

Before deploy, the previous admin binary was backed up on the VPS as:

```text
/usr/local/bin/v7-admin-api.bak.20260508-114731
```

## Next Step

Add richer import/download UX for smart profiles:

- show ready profiles as links in the expanded user details;
- add QR/import instructions for Karing;
- store selected client adapter/mode as user metadata.
