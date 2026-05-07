# V7 Phase 61: Service-Aware Route Class Health

Date: 2026-05-07

## Goal

Make the `TRUSTED_RU_SENSITIVE` route class honest in state and admin.

The class must not look solved just because one candidate works for some domains. It needs a route-class health status that can say:

```text
current candidate: vless
candidate result: partial
route class status: needs trusted path
```

## Implemented

Updated:

- `/usr/local/bin/v7-trusted-ru-decision`
- `/usr/local/bin/v7-state-json`
- `/usr/local/bin/v7-policy-show`
- `/usr/local/bin/v7-admin-api`

New state fields:

- `route_class=TRUSTED_RU_SENSITIVE`
- `route_class_status`
- `current_candidate`
- `candidate_result`
- `required_action`
- `candidate_vless_failed`

New route-class statuses:

- `NEEDS_DIAGNOSTIC`
- `NEEDS_TRUSTED_PATH`
- `LOCAL_DIRECT_READY`
- `TEMPORARY_EGRESS_READY`
- `UNKNOWN`

New candidate results:

- `VLESS_PASSES_TESTED_DOMAINS`
- `VLESS_HAS_WORKING_SAMPLES`
- `VLESS_PARTIAL`
- `VLESS_FAILS_TESTED_DOMAINS`
- `UNKNOWN`

## Current VPS Result

Decision preview was refreshed for:

- `www.gosuslugi.ru`
- `alfabank.ru`
- `alfa-mobile.alfabank.ru`
- `groupib-am.alfabank.ru`

Result:

```text
www.gosuslugi.ru                 NO_SAFE_PATH       none   000/FAIL   000   000
alfabank.ru                      USE_TEMP_VLESS     vless  000/FAIL   200   200
alfa-mobile.alfabank.ru          USE_TEMP_VLESS     vless  000/FAIL   404   404
groupib-am.alfabank.ru           NO_SAFE_PATH       none   000/FAIL   000   000

overall=NEEDS_ATTENTION
route_class_status=NEEDS_TRUSTED_PATH
current_candidate=vless
candidate_result=VLESS_PARTIAL
required_action=add_or_build_server_side_route_candidate_that_passes_real_service_tests
candidate_vless_failed=2
```

## AlfaBank Route Finding

Before sync, `alfabank.ru` was in `TRUSTED_RU_SENSITIVE`, but its resolved IP was still present in the broad direct set without a direct-exclude entry.

Ran:

```bash
v7-policy-sync-direct-excludes --apply
```

After sync:

```text
alfabank.ru direct_set=yes direct_exclude=yes decision=VPN_PREFERRED_DIRECT_EXCLUDED
alfa-mobile.alfabank.ru direct_set=no direct_exclude=yes decision=VPN_PREFERRED_DIRECT_EXCLUDED
groupib-am.alfabank.ru direct_set=no direct_exclude=yes decision=VPN_PREFERRED_DIRECT_EXCLUDED
```

Current user `10.0.0.3` sticky route:

```text
ip=10.0.0.3 current=awg2 table=101 enabled=1
table 101: default dev awg2
```

Because live service-aware marks for `TRUSTED_RU_SENSITIVE -> vless` are still intentionally not enabled, current AlfaBank traffic falls back to the user's sticky egress after direct is excluded.

So the current practical route for user `10.0.0.3` is:

```text
AlfaBank sensitive domains -> direct excluded -> table 101 -> awg2
```

The preview candidate for the route class remains:

```text
TRUSTED_RU_SENSITIVE desired path -> vless
```

But that preview is not live yet.

## Validation

```text
v7-admin-api: active
v7-api: active
v7-health: active
v7-benchmark: active
V7_RESULT=OK
```

`/state` now exposes:

```json
"route_class_status": "NEEDS_TRUSTED_PATH",
"current_candidate": "vless",
"candidate_result": "VLESS_PARTIAL",
"required_action": "add_or_build_server_side_route_candidate_that_passes_real_service_tests"
```

## Decision

Do not enable live service-aware marks yet.

The current safe behavior is:

- ordinary RU domains can use `DIRECT_RU`;
- sensitive domains are excluded from broad direct;
- sensitive domains fall back to the user's current sticky egress until a server-side trusted route candidate is proven;
- admin/state clearly shows that `TRUSTED_RU_SENSITIVE` is not solved.

