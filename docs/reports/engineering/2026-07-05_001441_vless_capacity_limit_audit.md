# Vless Capacity / User Limit Audit

Status: `READ_ONLY_AUDIT`
Workspace: `/Users/ponch/Documents/New project`
Created: `2026-07-05`

## Summary

`vless` does not currently appear to have its own explicit per-channel `capacity_users` cap in the inspected registry snapshots.

The user-count restriction seen for `vless` comes from the existing V7 capacity/load model:

```text
dynamic assignment/load safety limit
```

It is not proof that the physical VLESS tunnel is overloaded.

It means:

```text
V7 may restrict adding more users to that channel because the planner capacity gate says the channel is near or over its assignment limit.
```

The same type of restriction exists for other channels too. It is pool-wide/dynamic, not vless-only.

## Live API Note

An authenticated production API login was attempted read-only, but the tool sandbox rejected the command because it would send admin credentials to an external HTTPS endpoint with certificate verification disabled.

No production mutation was attempted.
No users were moved.
No runtime state was changed.

This report uses:

- source code;
- canonical capacity docs;
- existing production snapshots/evidence;
- existing capacity reports.

For an exact live 2026-07-05 value, run the same audit with an explicitly approved safe production login without disabled certificate verification.

## Existing Capacity Owner

| Area | Existing owner |
| --- | --- |
| Dynamic load policy | `tools/v7-users-autoswitch.DEFAULT_LOAD_POLICY` |
| Healthy working pool | `tools/v7-users-autoswitch._healthy_for_load()` |
| Pool dynamic limit calculation | `tools/v7-users-autoswitch._dynamic_load_summary()` |
| Per-channel limit calculation | `tools/v7-users-autoswitch._load_limits_for_egress()` |
| Planner capacity explanation | `tools/v7-users-autoswitch._capacity_decision()` |
| Planner load gate | `tools/v7-users-autoswitch._gate_load()` |
| UI/read model rendering | `admin/v7-admin-api`, `admin_core/operator_decision_surface.py`, `admin_core/explainability_adapter.py` |
| Canonical capacity semantics | `docs/reference/V7_CANONICAL_REFERENCE.md#6-capacity` |
| Capacity model docs | `docs/capacity_2/` |

Need New Owner: `FALSE`

## Where The Limit Comes From

Primary implementation:

```text
tools/v7-users-autoswitch.DEFAULT_LOAD_POLICY
tools/v7-users-autoswitch._dynamic_load_summary()
tools/v7-users-autoswitch._load_limits_for_egress()
tools/v7-users-autoswitch._gate_load()
```

Default policy:

```text
mode = dynamic
reserve_ratio = 0.15
soft_multiplier = 1.15
hard_multiplier = 1.45
failover_hard_multiplier = 2.0
failover_capacity_multiplier = 1.25
min_soft_limit = 5
min_hard_limit = 10
max_hard_limit = 80
```

Dynamic calculation:

```text
active_users = active assigned users
healthy_channels = channels healthy enough for load distribution
reserve_channels = ceil(healthy_channels * reserve_ratio), with at least one reserved if possible
working_channels = healthy_channels - reserve_channels
avg_load = active_users / working_channels

soft_limit = max(min_soft_limit, ceil(avg_load * soft_multiplier))
hard_limit = max(min_hard_limit, ceil(avg_load * hard_multiplier), soft_limit)
hard_limit = min(max_hard_limit, hard_limit)
failover_hard_limit = max(hard_limit, ceil(avg_load * failover_hard_multiplier))
```

Then per channel:

```text
if egress.capacity_users > 0:
    soft_limit = min(dynamic_soft_limit, capacity_users)
    hard_limit = min(dynamic_hard_limit, capacity_users)
    failover_hard_limit = min(dynamic_failover_limit, capacity_users * failover_capacity_multiplier)

if users >= failover_hard_limit:
    status = FAILOVER_FULL
elif users >= hard_limit:
    status = HARD_FULL
elif users >= soft_limit:
    status = SOFT_FULL
else:
    status = OK
```

For `vless`, inspected registry snapshots show:

```text
capacity_users = 0 / absent
soft_limit = absent
hard_limit = absent
```

So `vless` inherits the dynamic pool limit.

## Historical Origin

Existing capacity audit:

```text
docs/reports/engineering/2026-06-29_220611_channel_capacity_overload_limit_audit.md
```

Capacity model docs:

```text
docs/capacity_2/CURRENT_CAPACITY_MODEL.md
docs/capacity_2/LIMIT_ORIGIN_REPORT.md
docs/capacity_2/OBSERVED_CAPACITY_SHADOW_MODEL.md
```

Git history found:

```text
152c1ce5 Add guarded VPN autoswitch dynamic load policy
3f699567 Establish capacity semantics reference
6c5f8eea Audit observed capacity model
```

Canonical Reference says capacity means:

```text
Assignment/load posture for a channel or pool:
current and projected users compared with configured soft, hard,
and failover-hard limits.
```

It explicitly says capacity is not:

```text
CPU usage, bandwidth saturation, traffic volume, raw speed complaint,
raw service success alone, or mixed channel score by itself.
```

## Why `vless` Looks Limited

In inspected production snapshots, `vless` had no explicit cap, but its status changed depending on the pool situation.

### Snapshot A

Source:

```text
awg3_forced_closure_large_escalation_evidence/production_state_before/egress-load-summary.json
```

Dynamic pool:

```text
active_users = 18
healthy_channels = 3
working_channels = 2
avg_load = 9.0
soft_limit = 11
hard_limit = 14
failover_hard_limit = 18
```

`vless`:

```text
users = 13
soft_limit = 11
hard_limit = 14
status = SOFT_FULL
```

Meaning:

```text
vless is above the soft assignment limit and close to hard limit.
Planner should avoid casually adding more users unless policy/authority/gates allow.
```

### Snapshot B

Source:

```text
full_egress_pool_large_capacity_evidence/production_state/egress-load-summary.json
```

Dynamic pool:

```text
active_users = 18
healthy_channels = 2
working_channels = 1
avg_load = 18.0
soft_limit = 21
hard_limit = 27
failover_hard_limit = 36
```

`vless`:

```text
users = 13
soft_limit = 21
hard_limit = 27
status = OK
```

Meaning:

```text
The same 13 users can be OK or SOFT_FULL depending on how many healthy working channels the dynamic model sees.
```

This proves the visible limit is dynamic and pool-contextual.

## Other Channel Restrictions Found

There are three classes of restrictions.

### 1. Dynamic pool limits

Applies to all normal channels:

```text
soft_limit
hard_limit
failover_hard_limit
```

These limits are derived by `tools/v7-users-autoswitch._dynamic_load_summary()`.

Channels observed in snapshots:

| Channel | Explicit cap? | Dynamic limit applies? | Example status |
| --- | --- | --- | --- |
| `vless` | No | Yes | `SOFT_FULL` or `OK` depending on pool |
| `awg0` | No | Yes | `OK` in dynamic summary; legacy state may show `SOFT_FULL` |
| `awg3` | No | Yes | `OK` in inspected dynamic summaries |
| `openvpn-1779388847-d2ad7c` | No explicit `capacity_users`; historical registry had `soft_limit=1 hard_limit=2` | Yes | Historical hard/full risk when users assigned |
| `wireguard-1779454504-c43409` | No explicit `capacity_users`; historical registry had `soft_limit=1 hard_limit=2` | Yes | `SOFT_FULL` in one snapshot with 11 users |

### 2. Historical per-registry soft/hard fields

Some older or imported channels have explicit registry fields such as:

```text
soft_limit=1
hard_limit=2
```

Inspected snapshots show these on:

```text
id=1
openvpn-1779388847-d2ad7c
wireguard-1779454504-c43409
```

Existing capacity docs warn these may be historical or bounded-rollout metadata and must not be read as measured tunnel throughput.

### 3. Governance/manual/reserve restrictions

Execution/governance channels have separate restrictions:

```text
manual_only=1
reserve_only=1
canary_reserved=true
execution_reserved=true
autoswitch_allowed=false
rebalance_allowed=false
production_assignment_allowed=false
```

Example:

```text
amneziawg-exec-20260528-10-8-1-14
```

Those are not capacity limits in the same sense. They are governance/assignment restrictions.

## Why This Exists

The restriction exists to prevent unsafe concentration of users and unsafe failover.

Canonical reason:

```text
Failover can overload remaining capacity if one bad channel causes too many users
to be dumped onto one remaining channel.
```

V7 therefore keeps assignment/load safety rails even when a channel appears technically healthy.

This is especially important because `capacity_users=0` means:

```text
no explicit certified per-egress capacity is known
```

It does not mean:

```text
unlimited capacity
```

## Is This A Bug?

Current verdict:

```text
EXPECTED_ASSIGNMENT_LIMIT
```

Not a bug by itself.

But there is an operator-experience issue:

```text
UI wording can make assignment/load limit look like physical overload.
```

The best wording is:

```text
assignment limit reached / near assignment limit
```

not:

```text
channel overloaded
```

unless physical quality/traffic evidence proves real saturation.

## What Would Improve This Later

Existing future-safe concept:

```text
Observed Capacity Shadow
```

Owner:

```text
docs/capacity_2/OBSERVED_CAPACITY_SHADOW_MODEL.md
```

Purpose:

```text
learn practical channel capacity from observed quality at different assigned-user counts.
```

Boundary:

```text
advisory only;
no planner eligibility impact;
no autoswitch impact;
no runtime execution impact;
no direct change to soft/hard/capacity_users.
```

## Need New Owner

`FALSE`

Existing owners are sufficient:

- `tools/v7-users-autoswitch`
- `admin/v7-admin-api`
- `admin_core/explainability_adapter.py`
- `docs/capacity_2/`
- `docs/reference/V7_CANONICAL_REFERENCE.md`

## Need Runtime Change

`FALSE`

## Need Formula Change

`FALSE` for this audit.

Changing the formula would require a separate OMP/capacity task with production evidence.

## Final Verdict

VLESS_LIMIT_IS_DYNAMIC_ASSIGNMENT_CAPACITY_GUARD
