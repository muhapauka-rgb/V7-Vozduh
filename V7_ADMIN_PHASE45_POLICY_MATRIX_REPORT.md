# V7 Admin Phase 45: Policy diagnostics matrix

Date: 2026-05-07

## Goal

Add a matrix-style diagnostic for common service groups:

```text
domain -> route class -> desired path -> current direct engine -> note
```

This helps V7 move away from one-off manual fixes and toward class-based
service orchestration.

## Added

Command:

```text
/usr/local/bin/v7-policy-matrix
```

Default domains:

```text
www.gosuslugi.ru
esia.gosuslugi.ru
alfa-mobile.alfabank.ru
groupib-am.alfabank.ru
pushserver.edna.id
yandex.ru
ya.ru
ozon.ru
youtube.com
telegram.org
```

Admin action:

```text
POST /api/actions/policy-matrix-test
```

It runs:

```bash
v7-policy-matrix --write-state --user-ip <user_ip>
```

and writes:

```text
/opt/v7/egress/state/policy-domain-matrix.state
```

Minimum role:

```text
viewer
```

because the action is diagnostic and does not change routes.

## Admin UI

The `Service-aware Policy` section now has:

```text
Run Policy Matrix
```

The result is shown in the policy preview console.

## Validation Result

Command run on VPS:

```bash
v7-policy-matrix --write-state --user-ip 10.0.0.3
```

Important rows:

```text
www.gosuslugi.ru        TRUSTED_RU_SENSITIVE  desired=vless  direct_ready  policy_overrides_broad_direct
esia.gosuslugi.ru       TRUSTED_RU_SENSITIVE  desired=vless  direct_ready  policy_overrides_broad_direct
alfa-mobile.alfabank.ru TRUSTED_RU_SENSITIVE  desired=vless  vpn_preferred_excluded
yandex.ru               DIRECT_RU             desired=ens3   direct_ready  ordinary_ru_direct
ozon.ru                 DIRECT_RU             desired=ens3   direct_ready  ordinary_ru_direct
youtube.com             VIDEO_OPTIMIZED       desired=user_default
telegram.org            GLOBAL_STABLE         desired=user_default
```

This shows the important architecture distinction:

- ordinary `.ru` sites can stay direct through the VPS public interface;
- sensitive RU services override broad direct classification;
- global/video services stay on the user sticky egress.

## Health Check

Command run:

```bash
v7-killswitch-check
```

Result:

```text
V7_KILLSWITCH_CHECK=OK
```

No live route changes were made.

## Next Phase

The next route-policy step should be a controlled live rollout design, not an
immediate enable:

- create class-specific nft sets;
- define rule ordering;
- decide which class can be safely live first;
- keep TRUSTED_RU_SENSITIVE in preview until the temporary VLESS dependency is
  replaced or explicitly accepted as temporary.
