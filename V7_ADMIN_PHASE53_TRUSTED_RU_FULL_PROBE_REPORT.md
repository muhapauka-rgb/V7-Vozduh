# V7 Admin Phase 53: Trusted RU Full Probe Map

Date: 2026-05-07

## Goal

Finish the current `TRUSTED_RU_SENSITIVE` probe map so the admin panel no longer shows unknown/missing diagnostic coverage for the initial sensitive RU domain set.

This remains diagnostics/preview only. No user routing, nft rules, live service-aware marks, or egress assignments were changed.

## VPS Validation

Ran incremental missing batches on VPS `195.2.79.116`.

Commands used:

```text
v7-trusted-ru-refresh-missing --limit 2
v7-trusted-ru-refresh-missing --limit 2
```

Then final batches:

```text
v7-trusted-ru-refresh-missing --limit 2
v7-trusted-ru-refresh-missing --limit 2
```

Final decision summary:

```text
overall=NEEDS_ATTENTION
count=11
direct_ok=2
temporary_vless=2
awg=0
blocked=7
missing=0
V7_TRUSTED_RU_DECISION=NEEDS_ATTENTION
```

Final `/state` summary:

```json
{
  "decision": "NEEDS_ATTENTION",
  "direct_ok": "2",
  "temporary_vless": "2",
  "awg": "0",
  "blocked": "7",
  "missing": "0"
}
```

Final health checks:

```text
v7-killswitch-check
V7_KILLSWITCH_CHECK=OK

v7-system-check
V7_RESULT=OK
```

## Final Domain Map

```text
gosuslugi.ru                     NO_SAFE_PATH       none
www.gosuslugi.ru                 NO_SAFE_PATH       none
esia.gosuslugi.ru                NO_SAFE_PATH       none
lk.gosuslugi.ru                  NO_SAFE_PATH       none
gu-st.ru                         DIRECT_OK          ens3
alfabank.ru                      USE_TEMP_VLESS     vless
alfa-mobile.alfabank.ru          USE_TEMP_VLESS     vless
metrics.alfabank.ru              NO_SAFE_PATH       none
groupib-am.alfabank.ru           NO_SAFE_PATH       none
edna.id                          NO_SAFE_PATH       none
pushserver.edna.id               DIRECT_OK          ens3
```

## Interpretation

The current single VPS can directly reach some supporting sensitive endpoints:

- `gu-st.ru`
- `pushserver.edna.id`

But the main Gosuslugi and ESIA endpoints tested here are not reachable through any current checked path:

- direct `ens3` fails before TLS;
- VLESS test returned timeout for these hosts;
- AWG test returned timeout for these hosts.

Alfa primary/app endpoints currently work through the temporary VLESS path:

- `alfabank.ru`
- `alfa-mobile.alfabank.ru`

This confirms the architecture direction:

1. `TRUSTED_RU_SENSITIVE` must remain a separate service-aware route class.
2. Broad `.ru direct` is not enough and is sometimes wrong.
3. The admin must keep showing per-domain evidence, not one global “RU works” flag.
4. Live service-aware routing for sensitive RU must stay disabled until a stable non-temporary path exists for the core government/banking domains.

## Next Step

The next implementation step should be a guarded service-aware route apply preview for `TRUSTED_RU_SENSITIVE` that refuses activation while:

- `missing > 0`;
- `blocked > 0` for required core domains;
- `active_egress` is marked temporary;
- kill switch verification is not `OK`.

