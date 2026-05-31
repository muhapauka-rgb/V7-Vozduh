# E35.A0 Routing Mode Reality Audit

## Scope

This audit checks whether V7 already has a real routing-mode model that can be reused by E35.A Execution Authority.

Searched concepts:

- `AUTO`
- `OPERATOR_PINNED`
- `MANUAL`
- preferred channel
- channel lock
- user lock
- channel override
- manual assignment
- autoswitch exclusion / eligibility
- exclusive channel assignment
- group restrictions
- user routing ownership

No runtime mutation was performed.

## Reality Summary

V7 does not currently expose a complete per-user routing-mode model equivalent to:

```text
AUTO
OPERATOR_PINNED
MANUAL
```

There are partial routing ownership concepts:

- current live user assignment is stored in `users.registry`;
- autonomous routing decisions are planned by `tools/v7-users-autoswitch`;
- manual operator movement exists through the admin `user-switch` action;
- channel-level autoswitch eligibility exists through `manual_only`, `reserve_only`, `canary_reserved`, group ACLs, exclusive group controls, and execution-only target controls;
- group-level preference exists through `preferred_egress`;
- sticky/current-route scoring exists, but it is not a pin.

## Evidence

### Live Assignment Truth

`tools/v7-users-autoswitch` loads users from `users.registry` unless an injected state object is provided:

```text
state_dir/users.registry
ip
current
table
enabled
group/org/organization
```

Relevant implementation:

- `tools/v7-users-autoswitch`, `_load_users`
- `tools/v7-users-autoswitch`, `_sync_egress_user_counts`

### Routing Decision Engine

Current autonomous/guarded routing decisions are implemented in:

```text
tools/v7-users-autoswitch
```

Decision flow:

1. Load user assignment.
2. Determine important services.
3. Build candidates for all egresses.
4. Apply gates.
5. Score eligible candidates.
6. Compare best candidate against current.
7. Select moves only if policy thresholds pass.

Observed code areas:

- `_decision_for_user`
- `_candidate`
- `_gate_basic`
- `_gate_reservation`
- `_gate_org`
- `_gate_quality`
- `_gate_service`
- `_gate_load`
- `_gate_safety`
- `_score_parts`
- `_beats_current`

### Admin Manual Movement Path

Admin has a direct manual switch action:

```text
POST /api/actions/user-switch
```

It calls:

```text
v7-user-switch <ip> <egress>
```

with:

```text
V7_SWITCH_REASON=admin_manual
```

This is manual operator movement, but it is not persisted as a durable user routing mode such as `MANUAL` or `OPERATOR_PINNED`.

### Existing `route_mode`

`admin/v7-admin-api` contains `route_mode TEXT DEFAULT ''` in `pending_profiles`.

This appears tied to pending/provisioned profile/client creation and smart profile setup, not to runtime ownership of existing users. It is not the live assignment authority for `users.registry` rows.

### Channel-Level Eligibility

Existing channel controls include:

- `manual_only`
- `reserve_only`
- `canary_reserved`
- `exclusive_group`
- `groups`
- `autoswitch_allowed` for execution-only readiness

Admin exposes part of this as:

```text
Система может выбирать этот канал
Резервный канал
Эксклюзивная группа
```

This controls whether the system may consider a channel. It is not a per-user routing mode.

## Verdicts

```text
routing_mode_exists=false
preferred_channel_exists=false
pinned_semantics_exist=false
manual_semantics_exist=true
autoswitch_eligibility_controls_exist=true
assignment_truth_source_identified=true
routing_ownership_identified=true
e35_a_ready=true
```

## Interpretation

E35.A should not invent routing authority from scratch, but it also should not treat existing partial controls as a finished model.

The safe architecture is:

- reuse `users.registry` as current assignment truth;
- reuse `egress.registry` and org egress policy as channel eligibility truth;
- reuse autoswitch gates as admission inputs;
- introduce explicit user routing authority/mode metadata for E35.A;
- keep manual admin switch and governed execution distinct.
