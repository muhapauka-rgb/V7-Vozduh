# E25.11 Execution-Only Metadata Integration

## Result

`dedicated_execution_target_created=true`

`target_name=amneziawg-exec-20260528-10-8-1-14`

`interface_name=v7execwg0`

`target_users_zero=true`

`autoswitch_excluded=true`

`rebalance_excluded=true`

`production_assignment_blocked=true`

## Metadata

The E25.10 target name in evidence is `amneziawg-exec-20260528-10-8-1-14`, because the operator-provided profile is AmneziaWG and has target-local address `10.8.1.14/32`.

The following execution-only row was added to `/opt/v7/egress/state/egress.registry`:

```text
id=amneziawg-exec-20260528-10-8-1-14
protocol=amneziawg
type=interface
interface=v7execwg0
test=interface
enabled=1
config=/etc/amnezia/v7execwg0.conf
role=EXECUTION_ONLY
route_table=1250
priority=10
weight=1
soft_limit=1
hard_limit=1
manual_only=1
reserve_only=1
canary_reserved=true
execution_reserved=true
reservation_owner=operator_execution_governance
autoswitch_allowed=false
rebalance_allowed=false
production_assignment_allowed=false
service_tags=governance,execution
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

## Safety Semantics

- `manual_only=1`: blocks normal planner/autoswitch use.
- `reserve_only=1`: blocks reserve consumption for planned movement.
- `autoswitch_allowed=false`: explicit autoswitch exclusion.
- `rebalance_allowed=false`: explicit rebalance exclusion.
- `production_assignment_allowed=false`: explicit production assignment exclusion.
- `reservation_owner=operator_execution_governance`: binds ownership to the operator execution governance path.

## User State

- candidate user: `10.7.0.11`
- candidate current egress: `1`
- user table `1009`: unchanged
- user movement performed: `false`
