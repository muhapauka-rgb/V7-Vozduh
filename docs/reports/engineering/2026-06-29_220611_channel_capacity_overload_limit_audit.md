# Engineering Report: Channel Capacity / Overload Limit Audit

Summary:
This report explains why a V7 channel may be shown as overloaded, full, or "на лимите" even when it has a small number of users, for example around 10 users.

Action Performed:
- Audited existing capacity/load owners.
- Read canonical capacity documents and current C7 pool-health/capacity mapping.
- Read relevant runtime/planner/UI code paths.
- Did not change code, thresholds, formulas, Runtime behavior, authority, or users.

## Short Answer

In current V7, `HARD_FULL`, `SOFT_FULL`, `FAILOVER_FULL`, "full", "overloaded", "на лимите", or similar UI wording usually means:

```text
This channel reached an assignment / planner safety limit.
```

It does **not** necessarily mean:

```text
The physical tunnel/server/provider is actually overloaded.
```

A channel with 10 users can be marked as full because `10` is currently the default minimum dynamic hard limit:

```text
DEFAULT_LOAD_POLICY.min_hard_limit = 10
```

So if a channel has `users >= hard_limit`, planner marks it:

```text
HARD_FULL
```

That blocks new planned assignments to the channel unless explicitly allowed.

## Existing Owners

| Area | Existing owner |
| --- | --- |
| Planner capacity/load model | `tools/v7-users-autoswitch` |
| Dynamic load policy defaults | `tools/v7-users-autoswitch.DEFAULT_LOAD_POLICY` |
| Per-channel capacity status | `tools/v7-users-autoswitch._load_limits_for_egress` |
| Candidate load gate | `tools/v7-users-autoswitch._gate_load` |
| Capacity scoring/explanation | `tools/v7-users-autoswitch._capacity_decision` |
| UI rendering / labels | `admin/v7-admin-api` |
| Explainability why-card | `admin_core/explainability_adapter.py` |
| Capacity canonical docs | `docs/capacity_2/` |
| Pool-health / capacity-blast mapping | `docs/reports/engineering/2026-06-29_190713_continue_omp_c7_pool_health_capacity_blast_bounds.md` |
| Canonical reference entry | `docs/reference/V7_CANONICAL_REFERENCE.md` |

Need New Owner: `FALSE`.

Need New Backlog Item: `FALSE`.

## Current Load Policy Values

Source:

```text
tools/v7-users-autoswitch.DEFAULT_LOAD_POLICY
```

Current defaults:

| Field | Value | Meaning |
| --- | ---: | --- |
| `mode` | `dynamic` | Limits are derived from active users and healthy working channels. |
| `reserve_ratio` | `0.15` | Some healthy channels are kept as reserve/headroom. |
| `soft_multiplier` | `1.15` | Soft limit is based on average load times multiplier. |
| `hard_multiplier` | `1.45` | Hard limit is based on average load times multiplier. |
| `failover_hard_multiplier` | `2.0` | Emergency/failover ceiling. |
| `failover_capacity_multiplier` | `1.25` | If explicit `capacity_users` exists, failover cap is also bounded. |
| `min_soft_limit` | `5` | Dynamic soft limit never goes below 5. |
| `min_hard_limit` | `10` | Dynamic hard limit never goes below 10. |
| `max_hard_limit` | `80` | Dynamic hard limit is capped above. |
| `soft_limit` | `15` | Static-mode fallback. |
| `hard_limit` | `30` | Static-mode fallback. |
| `failover_hard_limit` | `60` | Static-mode fallback. |

Important:
The `min_hard_limit = 10` value is a planner safety floor, not a measured physical capacity number.

## How V7 Calculates Dynamic Load

Owner:

```text
tools/v7-users-autoswitch._dynamic_load_summary
```

Simplified logic:

```text
active_users = number of active users
healthy_channels = enabled, non-manual, non-canary, non-hard-blocked channels
reserve_channels = some healthy channels reserved for headroom
working_channels = healthy_channels - reserve_channels
avg_load = active_users / working_channels

soft_limit = max(min_soft_limit, ceil(avg_load * soft_multiplier))
hard_limit = max(min_hard_limit, ceil(avg_load * hard_multiplier), soft_limit)
hard_limit = min(max_hard_limit, hard_limit)
failover_hard_limit = max(hard_limit, ceil(avg_load * failover_hard_multiplier))
```

Then each channel can also be capped by explicit per-egress `capacity_users`.

## How One Channel Becomes `HARD_FULL`

Owner:

```text
tools/v7-users-autoswitch._load_limits_for_egress
```

Simplified logic:

```text
if egress.capacity_users > 0:
    soft_limit = min(dynamic_soft_limit, capacity_users)
    hard_limit = min(dynamic_hard_limit, capacity_users)

if egress.users >= failover_hard_limit:
    status = FAILOVER_FULL
elif egress.users >= hard_limit:
    status = HARD_FULL
elif egress.users >= soft_limit:
    status = SOFT_FULL
else:
    status = OK
```

So if:

```text
users = 10
hard_limit = 10
```

then:

```text
status = HARD_FULL
```

This is expected under current semantics.

## Why This Exists

The limits exist to protect V7 from unsafe movement:

- avoid putting too many users on one egress;
- preserve failover headroom;
- keep reserve/canary/manual channels from being treated as ordinary capacity;
- block planned movement to a target that is already full by policy;
- keep current users distinct from new movement;
- prevent autoswitch/rebalance from concentrating users too aggressively.

This is a safety rail, not a provider capacity measurement.

## Why It Can Look Wrong To An Operator

The operator sees:

```text
channel overloaded / full / на лимите
```

But the system means:

```text
the channel has reached the current assignment safety limit for new movement
```

That wording can feel wrong when the channel has only 8-11 users and still works well.

Canonical docs already confirm this mismatch:

```text
Current V7 capacity is an assignment/load safety model.
It is not a measured physical tunnel-capacity model.
```

Source:

```text
docs/capacity_2/CURRENT_CAPACITY_MODEL.md
```

## Evidence From Existing Capacity Audit

`docs/capacity_2/CURRENT_CAPACITY_MODEL.md` records production evidence where channels were marked `HARD_FULL` despite good observed quality:

| Channel | Users | Avg Mbps | Stability | Load status |
| --- | ---: | ---: | ---: | --- |
| `vless` | `11` | `37.453` | `0.946787` | `HARD_FULL` |
| `awg3` | `8` | `46.6283` | `0.805948` | `HARD_FULL` |
| `wireguard-1779454504-c43409` | `8` | `45.5093` | `0.845102` | `HARD_FULL` |
| `awg0` | `0` | `43.4387` | `0.737131` | `OK` |

The audit verdict:

```text
Current capacity model remains valid as a safety rail for assignment and failover.
It is insufficient as a real practical-capacity model for third-party tunnels because it does not learn a channel's observed degradation point.
```

## Two Different Capacity Concepts

### 1. IP Pool Capacity

This answers:

```text
Do we have enough IP addresses / registry capacity?
```

Example from `docs/capacity_1/evidence/production_capacity_summary.json`:

```text
target_users = 500
total_capacity = 1275
free_capacity = 1248
```

This is large and not the same as channel load.

### 2. Channel Assignment Capacity

This answers:

```text
Should planner put more users onto this specific egress now?
```

This can be low by design, for example:

```text
soft_limit = 1
hard_limit = 2
```

or:

```text
hard_limit = 10
```

Those are safety / rollout / governance numbers, not measured tunnel throughput.

## Explicit Per-Channel Limits

Some channels have explicit registry limits:

```text
soft_limit
hard_limit
capacity_users
```

Examples from existing production evidence:

```text
soft_limit=1
hard_limit=2
```

for some GLOBAL_FAST interface channels, and:

```text
soft_limit=10
hard_limit=10
```

for an execution-reserved channel.

These values can come from:

- early channel onboarding;
- bounded rollout metadata;
- canary / execution-only constraints;
- manual/reserve/governance configuration;
- explicit production safety limits.

`docs/capacity_2/LIMIT_ORIGIN_REPORT.md` says some explicit `soft_limit: 1` / `hard_limit: 2` values are historical or bounded rollout metadata and must not be read as measured tunnel throughput.

## What The Planner Does With This

Owner:

```text
tools/v7-users-autoswitch._gate_load
```

If a target channel is already at/above hard limit:

```text
planned movement is blocked with planned_hard_full
```

For failover:

```text
failover movement is blocked only at failover_hard_limit
```

So the system distinguishes normal planned movement from emergency failover.

## UI / Language Issue

Current UI mappings include:

```text
HARD_FULL -> "на лимите"
SOFT_FULL -> "контроль"
```

Older or adjacent UI/report surfaces may still use wording such as:

```text
перегружен
overloaded
full
```

This can be misleading if the operator reads it as physical overload.

More accurate operator wording would be:

```text
на лимите новых назначений
```

or:

```text
достигнут лимит распределения
```

instead of:

```text
перегружен
```

No UI change was made by this report.

## What V7 Does Not Yet Know

V7 does not yet have certified practical-capacity curves per channel.

It does not yet know with high confidence:

- this channel is stable up to 15 users;
- starts degrading around 18 users;
- breaks around 22 users;
- or can safely carry 50 users.

The current static/dynamic assignment limits are therefore intentionally conservative.

## Existing Future Direction

Existing capacity audit already defines a future advisory model:

```text
Observed Capacity Shadow
```

Purpose:

```text
Learn practical channel capacity from real observations without changing planner eligibility or runtime behavior.
```

Shadow fields include:

- observed users;
- quality state;
- quality signals;
- baseline users;
- degradation users;
- practical capacity estimate;
- confidence;
- recommendation.

Important boundary:

```text
Observed Capacity Shadow must not directly affect Runtime, planner eligibility, assignment decisions, autoswitch, governance, or existing capacity limits until separately approved/certified.
```

## Risk Assessment

| Risk | Explanation |
| --- | --- |
| Operator confusion | "Перегружен" can sound like physical server overload, while V7 means assignment safety limit. |
| Over-conservative routing | Low historical limits can block useful distribution even when observed quality is good. |
| Unsafe limit increase | Raising limits manually without observed capacity evidence could overload a weak channel later. |
| Mixed semantics | IP pool capacity, channel assignment capacity, and observed physical capacity are different but easy to confuse. |

## Current Verdict

The current behavior is mostly intentional:

```text
HARD_FULL at 10 users is an assignment safety state.
```

It is not proof of physical overload.

The confusing part is mostly semantic/operator-facing:

```text
"overloaded" / "перегружен" is too strong if the true state is "new assignment hard limit reached".
```

## What To Discuss With GPT

Questions worth discussing:

1. Should the UI rename `HARD_FULL` from overload language to assignment-limit language?
2. Should V7 show both:
   - assignment limit status;
   - observed quality / practical capacity confidence?
3. Should low historical `soft_limit=1` / `hard_limit=2` be reviewed channel by channel?
4. Should `Observed Capacity Shadow` be promoted from audit design into an approved future implementation?
5. What evidence is enough before increasing per-channel limits?
6. Should limits differ by protocol, provider, role, service class, or cohort?

## Minimal Recommendation

Do not remove limits.

Do not raise thresholds blindly.

Minimal safe next step:

```text
Create an operator-facing distinction between:

1. Assignment limit reached.
2. Observed physical degradation.
3. Unknown practical capacity.
```

Then, if desired, use the existing `Observed Capacity Shadow` owner path to learn practical channel capacity from real production observations.

## OMP Mapping

Existing owner covers the finding:

```text
C7 Pool Health Capacity And Blast Bounds
Capacity.2 Observed Capacity Model
tools/v7-users-autoswitch capacity/load owners
Canonical Reference capacity sections
```

Need New Owner: `FALSE`.

Need New Backlog Item: `FALSE`.

Runtime behavior changed: `NO`.

Authority expanded: `NO`.

Users moved: `NO`.

## Evidence Files

Primary evidence:

- `docs/capacity_2/CURRENT_CAPACITY_MODEL.md`
- `docs/capacity_2/LIMIT_ORIGIN_REPORT.md`
- `docs/capacity_2/OBSERVED_CAPACITY_THEORY.md`
- `docs/capacity_2/OBSERVED_CAPACITY_SHADOW_MODEL.md`
- `docs/capacity_1/evidence/production_capacity_summary.json`
- `docs/capacity_1/evidence/production_decision_summary.json`
- `docs/reports/engineering/2026-06-29_190713_continue_omp_c7_pool_health_capacity_blast_bounds.md`

Primary code owners:

- `tools/v7-users-autoswitch.DEFAULT_LOAD_POLICY`
- `tools/v7-users-autoswitch._dynamic_load_summary`
- `tools/v7-users-autoswitch._load_limits_for_egress`
- `tools/v7-users-autoswitch._capacity_decision`
- `tools/v7-users-autoswitch._gate_load`
- `admin/v7-admin-api`
- `admin_core/explainability_adapter.py`

Final Verdict:

```text
CHANNEL_OVERLOAD_IS_ASSIGNMENT_LIMIT_NOT_PHYSICAL_SATURATION
```
