# V7 VLESS 3 Clients Full Audit

## Summary

Observed question: why can `vless` be shown as overloaded/full with only 3 clients while another channel with 10 clients is OK?

Root finding: V7 currently exposes two capacity/load semantics:

1. Legacy per-channel load state from `tools/runtime-support/v7-egress-load`, defaulting to `soft=1`, `hard=2`.
2. Dynamic autoswitch capacity from `tools/v7-users-autoswitch`, computed from active users, healthy channels, reserve ratio, and per-channel capacity override.

The "vless full at 3 clients" behavior is explained by the legacy `hard=2` source. A channel with 3 users is `HARD_FULL` under legacy load state because `3 >= 2`. Another channel with 10 users can be OK under dynamic autoswitch capacity when the dynamic hard limit is 10, 14, 24, 27, etc.

This is not evidence that `vless` has a physical three-user limit. It is a load-source/semantics mismatch unless the same screen explicitly labels it as legacy assignment load.

Live admin API was not accessed in this audit. A read-only authenticated API attempt was blocked by the execution policy because it involved credentials and production data. Findings below are from source code and saved production snapshots.

## Exact Sources

### Legacy Load Source

Owner: `tools/runtime-support/v7-egress-load`

Relevant lines:

- `SOFT_LIMIT="${V7_LOAD_SOFT_LIMIT:-1}"`
- `HARD_LIMIT="${V7_LOAD_HARD_LIMIT:-2}"`
- `count=$(grep -c "current=${id}" "$USERS_REG")`
- `if count >= hard_limit -> HARD_FULL`

Effect:

```text
users >= 2 -> HARD_FULL
users >= 1 -> SOFT_FULL
```

So `vless` with 3 users is `HARD_FULL` if this source is used.

### Admin/UI Load Consumer

Owner: `admin/v7-admin-api`

Relevant functions:

- `channelLoad(id, st)` uses `st.load_status` or `egress_flags_map[id_load_status]`.
- `channelSuitabilityCapacity(row)` treats `HARD/OVER` load status as capacity problem.
- `channelLoadLimit(row)` falls back to registry/policy `soft=1`, `hard=2`.
- `openLoadMetricDetail()` displays `count / soft / hard`.

This means UI can display "на лимите/full" from the legacy status and legacy `1/2` limits.

### State Bridge

Owner: `tools/runtime-support/v7-state-json`

Relevant behavior:

- emits `"load_status"` from `${id}_load_status`.

This bridges legacy load state into the admin overview state.

### Dynamic Autoswitch Capacity

Owner: `tools/v7-users-autoswitch`

Relevant functions:

- `_dynamic_load_summary()`
- `_load_limits_for_egress()`
- `_capacity_decision()`
- `_gate_load()`

Default dynamic policy:

```text
mode=dynamic
reserve_ratio=0.15
soft_multiplier=1.15
hard_multiplier=1.45
failover_hard_multiplier=2.0
min_soft_limit=5
min_hard_limit=10
max_hard_limit=80
```

Dynamic limits are pool-relative. They are not the same as legacy `1/2`.

## Saved Production Evidence

From `full_egress_pool_large_capacity_evidence/production_state/egress-load.state`:

```text
vless users=14 soft=1 hard=2 status=HARD_FULL
awg0 users=1 soft=1 hard=2 status=SOFT_FULL
```

From the matching dynamic summary:

```text
vless users=13 soft=21 hard=27 status=OK
awg0 users=1 soft=21 hard=27 status=OK
```

From `awg3_forced_closure_large_escalation_evidence/production_state_before/egress-load.state`:

```text
vless users=14 soft=1 hard=2 status=HARD_FULL
```

From the matching dynamic summary:

```text
vless users=13 soft=11 hard=14 status=SOFT_FULL
```

From `docs/track7/control-plane/e10_3-evidence/current-state/egress-load-summary.json`:

```text
vless users=10 soft=19 hard=24 status=OK
```

Therefore the system already contains examples where `vless` or another channel is "full" under legacy `1/2`, but OK under dynamic capacity.

## Are Other Channels Affected?

Yes. The legacy source marks any enabled channel as:

- `SOFT_FULL` at 1 user.
- `HARD_FULL` at 2 or more users.

Saved snapshots show this affecting `awg0`, `awg3`, `amneziawg-exec-20260528-10-8-1-14`, `wireguard-1779454504-c43409`, numeric channel `1`, and `vless`.

This is not vless-specific.

## Why One Channel With 10 Can Be OK

Because that result is coming from the dynamic autoswitch capacity model:

```text
dynamic hard_limit = max(min_hard_limit, ceil(active_users / working_channels * hard_multiplier))
```

Examples from saved snapshots:

- `hard=10`, `vless users=10` can still display OK when status was computed before or below the hard boundary depending on exact per-snapshot count.
- `hard=14`, `vless users=13` -> not hard full.
- `hard=24`, `vless users=10` -> OK.
- `hard=27`, `vless users=13` -> OK.

## Is This Expected Behavior?

Partially.

It is expected that V7 has a dynamic capacity model for assignment safety.

It is not clean behavior for the operator surface to present legacy `1/2` load state and dynamic capacity state as if they were the same concept. That makes the UI look contradictory: "3 users full" next to "10 users OK".

## Is This A Bug?

Yes, if the UI is using legacy `load_status` to describe current production capacity while the runtime/planner uses dynamic capacity as the canonical assignment model.

More precise classification:

```text
READ_MODEL_SEMANTICS_MISMATCH
```

The runtime planner is not proven wrong by this audit. The visible operator interpretation is ambiguous because it mixes load sources.

## Existing Owners

- Legacy load producer: `tools/runtime-support/v7-egress-load`
- State bridge: `tools/runtime-support/v7-state-json`
- Admin read model/UI: `admin/v7-admin-api`
- Dynamic autoswitch capacity: `tools/v7-users-autoswitch`
- Decision surface capacity fields: `admin_core/operator_decision_surface.py`

## Minimal Correction Direction

Do not change formulas first.

Smallest correction direction:

1. Choose one canonical source for operator-facing assignment capacity.
2. Prefer dynamic autoswitch capacity for production assignment/load decisions.
3. Keep legacy `egress-load.state` only if explicitly labeled as legacy/static load health.
4. In UI, do not render legacy `hard=2` as the same "capacity full" concept as dynamic autoswitch hard limits.
5. Add a read-model check that reports both sources when they disagree:

```text
legacy_load_status=HARD_FULL, legacy_hard=2
dynamic_status=OK, dynamic_hard=24
```

## Need New Owner

FALSE.

## Need New Architecture

FALSE.

## Verdict

VLESS_THREE_CLIENT_FULL_EXPLAINED_BY_LEGACY_LOAD_SOURCE
