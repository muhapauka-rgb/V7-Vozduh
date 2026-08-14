# Proposed bounded governance mutation for WG.PROMOTE.1

No production change was performed by this program.

## Before

```text
id=wireguard-1779454504-c43409 protocol=wireguard type=interface interface=v7e06a394c478 test=interface enabled=1 config=/etc/wireguard/v7e06a394c478.conf role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU canary_reserved=true reservation_reason=second_canary_target reservation_owner=control_plane_governance
```

## After

```text
id=wireguard-1779454504-c43409 protocol=wireguard type=interface interface=v7e06a394c478 test=interface enabled=1 config=/etc/wireguard/v7e06a394c478.conf role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU capacity_users=2
```

## Semantics

- removes canary reservation fields;
- adds `capacity_users=2` as the runtime-consumed per-egress cap;
- keeps `soft_limit=1 hard_limit=2` historical metadata unchanged for observability compatibility;
- bounded promotion only, not full production promotion.

## Required apply owner

```text
control_plane_governance
```

## Required deploy path

Only a later approved production program may mutate `/opt/v7/egress/state/egress.registry`.
