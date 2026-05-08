# V7 Phase 63: Karing Smart Client Profile Generator

Date: 2026-05-08

## Goal

Create the first practical Smart Client Profile generator for Karing.

The generator converts an existing V7 WireGuard client config into a sing-box/Karing JSON profile with client-side service-aware routing.

## Implemented

Added:

- `client/v7-smart-client-profile-generate`

Updated:

- `.gitignore`

Generated secret profiles are ignored under:

- `admin/smart-profiles/`

## Supported Adapter

Current implemented adapter:

- `karing`

Planned later:

- `hiddify`
- `happ`
- `clash-verge-rev`

## Supported Modes

### RU_LOCAL

For users physically in Russia or on a network accepted by RU services.

```text
RU public domains      -> direct from device
RU sensitive domains   -> direct from device
video/global/default   -> V7 WireGuard endpoint
```

### ABROAD_RU_VIA_V7

For users abroad.

```text
RU public domains      -> V7
RU sensitive domains   -> V7
video/global/default   -> V7
```

Important: this is structurally ready, but government/sensitive sites still require a proven `RU_GOV_ABROAD` server-side path.

### AUTO_TRAVEL

Adds client selectors:

```text
ru-mode
ru-sensitive-mode
```

This is the future mode where a user/operator can switch RU behavior without regenerating the whole base profile.

## Generated On VPS

For test user:

- `v7-iphone`

Generated on VPS:

```text
/root/v7-smart-clients/v7-iphone/karing-ru_local.json
/root/v7-smart-clients/v7-iphone/karing-abroad_ru_via_v7.json
/root/v7-smart-clients/v7-iphone/karing-auto_travel.json
```

Also copied locally for import/testing:

```text
admin/smart-profiles/v7-iphone/karing-ru_local.json
admin/smart-profiles/v7-iphone/karing-abroad_ru_via_v7.json
admin/smart-profiles/v7-iphone/karing-auto_travel.json
```

These local files contain client secrets and are intentionally git-ignored.

## Validation

All generated Karing profiles passed `sing-box check` on VPS:

```text
karing-ru_local.json          OK
karing-abroad_ru_via_v7.json  OK
karing-auto_travel.json       OK
```

V7 health after generation:

```text
V7_RESULT=OK
vless_ip=77.110.103.131
awg2_ip=94.241.139.241
10.0.0.3 route_get uses awg2
```

## Implementation Notes

The generator uses the modern sing-box WireGuard `endpoint` structure rather than the deprecated WireGuard outbound.

During validation two compatibility issues were found and fixed:

1. `experimental.cache_file.store_dns` is not accepted by the current VPS sing-box `1.13.11`.
2. `route.override_android_vpn` is Android-only and must not be included in Karing/iOS profiles.

The generator now also sets:

```json
"route": {
  "default_domain_resolver": "local"
}
```

or `v7-dns` depending on mode, matching newer sing-box route requirements.

## Safety

The generator:

- does not change server routes;
- does not change users.registry;
- does not restart V7 services;
- writes secrets only to output files;
- does not print keys in normal output;
- writes sidecar `.meta` files for non-secret profile metadata.

## Next Step

Add admin UI/API actions:

- Generate Karing profile
- Download profile
- Show QR/import instructions
- Select route mode per user
- Store selected client adapter/mode in user metadata

