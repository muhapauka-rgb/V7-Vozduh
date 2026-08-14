# WG Capacity Conflict Analysis

## Observed Conflict

Historical governance:

```text
soft_limit=1
hard_limit=2
```

Current planner projection:

```text
soft_limit=30
hard_limit=38
```

## Why They Differ

The `1/2` values are registry metadata from the canary/governance era.

The `30/38` values are derived by the current dynamic runtime load policy:

```text
active_users=26
working_channels=1
avg_load=26.0
soft_limit=ceil(26.0 * 1.15)=30
hard_limit=ceil(26.0 * 1.45)=38
```

The runtime can reduce these per target only if `capacity_users` is set.

WireGuard has no `capacity_users` override, so the dynamic projection remains `30/38`.

## Correct Interpretation

The `1/2` limit is not the active planner capacity source.

It is also not useless: it is still governance history proving the last explicit WireGuard movement certification stopped at two users.

Therefore:

- as a planner runtime capacity limit, `1/2` is stale/non-authoritative;
- as historical governance evidence, `1/2` is still meaningful;
- as full-production proof, neither `1/2` nor `30/38` is sufficient alone.

## Operational Consequence

WireGuard can be prepared for limited production promotion, but full promotion should require fresh capacity certification or an explicit `capacity_users`/capacity metadata decision.

