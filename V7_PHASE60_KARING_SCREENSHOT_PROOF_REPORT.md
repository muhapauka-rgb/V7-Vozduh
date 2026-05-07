# V7 Phase 60: Karing Screenshot Proof

Date: 2026-05-07

## Input

The user provided two consecutive screenshots from Karing while Gosuslugi was opening successfully through the direct VLESS app setup.

## Observed Karing Connections

The screenshots show the following Gosuslugi-related connections:

- `elections.gosuslugi.ru:443`
- `esia.gosuslugi.ru:443`
- `gu-st.ru:443`
- `www.gosuslugi.ru:443`

For these connections Karing shows:

```text
ru[geosite]
Напрямую
```

`Напрямую` means `DIRECT`.

## Conclusion

This proves that Karing was not opening Gosuslugi through the VLESS proxy node.

Karing was using rule-based split routing:

```text
generic IP check, for example ifconfig.me -> VLESS
Gosuslugi / ESIA / gu-st.ru -> DIRECT from the phone network
```

This explains the apparent contradiction:

- `ifconfig.me` showed `77.110.103.131`;
- Gosuslugi opened in Karing;
- but V7-mediated Gosuslugi through VLESS failed.

The two tests were not using the same route for the target service.

## Impact On V7

The current V7 diagnosis is now confirmed:

- V7 policy correctly detects Gosuslugi as sensitive RU.
- V7 prevents broad `.ru` direct from capturing it accidentally.
- V7 routes it through the temporary `vless` path.
- The VLESS path fails for main Gosuslugi/ESIA domains.
- Karing succeeds because it uses phone-side direct routing for RU geosite domains.

## Important Product Constraint

The user does not want a mobile-side bypass solution.

Therefore V7 must solve sensitive RU routing inside the V7 server-side architecture, not by relying on Karing's phone-side `DIRECT` behavior.

## Next Architecture Decision

Mark `TRUSTED_RU_SENSITIVE` as not solved by the current `vless` egress.

V7 should represent this honestly in state/admin:

```text
TRUSTED_RU_SENSITIVE
status: NEEDS_TRUSTED_PATH
current_candidate: vless
candidate_result: FAILS_GOSUSLUGI_TLS
direct_vps_result: TCP_TIMEOUT_BEFORE_TLS
phone_karing_result: WORKS_VIA_PHONE_DIRECT
```

Do not label VLESS as a working sensitive RU route.

## Next Implementation Direction

1. Add a service-aware route-class health state.
2. Show sensitive RU as degraded/unsolved in admin.
3. Keep normal `.ru` domains on `DIRECT_RU`.
4. Keep Gosuslugi/banks in `TRUSTED_RU_SENSITIVE`.
5. Do not auto-route sensitive RU to a candidate until that candidate passes a real service test from the V7 node.

