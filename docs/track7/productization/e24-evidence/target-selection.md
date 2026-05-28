# E24 Target Selection

## Target Review

| Target | Users | Capacity | Reservation | Interface | Verdict |
|---|---:|---|---|---|---|
| awg3 | 9 | legacy no explicit hard_limit in registry | none | UP | not selected; crowded current stable pool |
| awg0 | 3 | legacy no explicit hard_limit in registry | none | UP | not selected; delayed-move target from E11.13 |
| 1 | 4 | soft=1 hard=2 | none | UP | rollback target, not target |
| openvpn-1779388847-d2ad7c | 0 | soft=1 hard=2 | none | UP | not selected; historical suspect/waiver complexity |
| vless | 0 enabled users | no explicit capacity | none | UP | not selected; disabled user history and proxy complexity |
| wireguard-1779454504-c43409 | 0 | soft=1 hard=2 | canary_reserved=true | UP | selected as explicit governed target only |

## Selected Target

```text
selected_target=wireguard-1779454504-c43409
interface=v7e06a394c478
protocol=wireguard
users=0
soft_limit=1
hard_limit=2
canary_reserved=true
target_capacity_safe=true for movement_budget=1
```

Read-only diagnostics:

```text
ip_link=v7e06a394c478 UNKNOWN <POINTOPOINT,NOARP,UP,LOWER_UP>
ip_addr=10.8.0.17/24
wg_show_latest_handshake=27 seconds ago at collection time
transfer=9.46 GiB received, 382.08 MiB sent
```

## Reservation Semantics

WireGuard is reserved for governed testing. That is acceptable only if E25 uses an explicit operator-approved packet with:

```text
allowed_users=["10.7.0.11"]
allowed_targets=["wireguard-1779454504-c43409"]
movement_budget=1
rollback_target=1
```

Autoswitch production assignment to this target remains forbidden.

## Target Verdict

```text
target_ready=conditional
target_capacity_safe=true
target_execution_blocker=VPS_TARGET_READINESS_TOOL_MISSING
```

The target can be selected for a conditional approval packet, but E25 must not execute until target readiness is verified with the missing VPS governance helper or an explicitly approved equivalent.
