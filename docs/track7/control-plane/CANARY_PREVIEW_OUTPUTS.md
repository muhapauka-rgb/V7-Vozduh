# Canary Preview Outputs

Generated locally with `tools/v7-route-movement-preview` against a copied read-only runtime snapshot. The planner did not execute runtime commands and emitted `mutation=false` and `runtime_commands_executed=false`.

## Artifacts

```text
docs/track7/control-plane/canary-previews/user-switch-preview.json
docs/track7/control-plane/canary-previews/rollback-preview.json
docs/track7/control-plane/canary-previews/routing-sync-preview.json
```

## Forward Preview

Candidate:

```text
user=10.7.0.13
from_egress=awg0
to_egress=awg3
table=1011
target_interface=awg3
```

Planned live route change, if separately approved later:

```text
ip route replace default dev awg3 table 1011
```

The planner reports:

```text
mutation=false
runtime_commands_executed=false
blast_radius=one_user
errors=[]
```

## Rollback Preview

Rollback command for the future canary:

```text
v7-user-switch 10.7.0.13 awg0
```

The rollback preview was generated from a synthetic local post-canary registry copy where only `10.7.0.13` was set to `current=awg3`. It is not a runtime mutation.

Rollback route plan:

```text
ip route replace default dev awg0 table 1011
```

## Routing-Sync Preview

The registry-wide preview shows:

```text
blast_radius=all_enabled_users_in_registry
enabled route plans=16
routes_would_change=16
ip_rules_would_change=32
errors=0
```

This confirms that `v7-routing-sync` is not an acceptable first canary action. Its blast radius is all enabled users, not one user.
