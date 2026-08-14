# WG Capacity Owner Audit

## Runtime Planner Capacity Owner

Owner:

```text
tools/v7-users-autoswitch
```

Runtime functions:

- `DEFAULT_LOAD_POLICY`
- `_dynamic_load_summary`
- `_load_limits_for_egress`
- `_capacity_decision`
- `_pick_moves_with_projected_load`

Authoritative for:

- planner candidate capacity scoring;
- projected target load;
- soft/hard runtime load thresholds;
- selected move distribution in dry-run/apply path.

Current dynamic load evidence:

```json
{
  "active_users": 26,
  "healthy_channels": 1,
  "working_channels": 1,
  "avg_load": 26.0,
  "soft_limit": 30,
  "hard_limit": 38,
  "failover_hard_limit": 52,
  "wireguard": {
    "users": 0,
    "soft_limit": 30,
    "hard_limit": 38,
    "failover_hard_limit": 52,
    "capacity_users": 0,
    "status": "OK"
  }
}
```

## Registry Metadata

Current production registry row still contains:

```text
soft_limit=1 hard_limit=2
```

but `tools/v7-users-autoswitch::_load_egress` does not consume these fields into `Egress.capacity_users`.

The fields are visible to observability/admin surfaces, but they are not the current runtime planner capacity owner.

## Target-Specific Runtime Override

The runtime-recognized override is:

```text
capacity_users
```

or legacy:

```text
capacity
```

WireGuard currently has:

```text
capacity_users=0
capacity=absent
```

Therefore it uses dynamic load projection.

## Governance Capacity Owner

Owner:

```text
E32 capacity metadata/certification model
```

Governance capacity is a gate, not authority. Forward batches require fresh certified capacity metadata.

WireGuard does not currently have fresh capacity-class certification above the old two-user mini-cohort evidence.

## Owner Verdict

The conflict exists because two different layers are being compared:

| Layer | Value | Authority |
| --- | --- | --- |
| E11 canary governance metadata | `1/2` | historical bounded canary cap |
| current runtime planner load model | `30/38` | current autoswitch projection |
| formal capacity certification | not fresh above 2 | governance gate for larger movement |

