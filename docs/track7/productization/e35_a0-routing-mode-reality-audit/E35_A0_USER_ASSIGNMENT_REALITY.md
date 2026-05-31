# E35.A0 User Assignment Reality

## Assignment Truth Source

The current live assignment source is:

```text
users.registry
```

Observed fields used by routing logic:

| Field | Meaning | Used By |
|---|---|---|
| `ip` | user identity | autoswitch planner, admin switch, route checks |
| `current` | current egress/channel | autoswitch planner, route verification, admin overview |
| `table` | route table | route checks and user movement verification |
| `enabled` | eligible active user flag | autoswitch planner |
| `group` / `org` / `organization` | optional group source | autoswitch org policy mapping |

## Runtime Loader

`tools/v7-users-autoswitch` uses `_load_users` to load active users. It resolves group ownership in this order:

1. row `group`
2. row `org`
3. row `organization`
4. org policy `user_groups`
5. org policy `groups[*].users`
6. org policy `default_group`
7. `default`

This means assignment is user-first, with group policy layered on top.

## Current Assignment Mutation Paths

Known mutation paths, not executed during this audit:

| Path | Mechanism | Notes |
|---|---|---|
| Admin manual switch | `POST /api/actions/user-switch` -> `v7-user-switch` | Operator-triggered user movement. |
| Autoswitch apply | `tools/v7-users-autoswitch` apply path -> `v7-user-switch` | Guarded autonomous/assisted movement path. |
| Governed execution blocks | approval packet + raw fallback movement | Proven in E25-E31. |

## Assignment Model Gaps

The current assignment row does not appear to contain:

- explicit per-user routing mode;
- explicit per-user pin owner;
- explicit manual assignment expiry;
- explicit operator-pinned target;
- explicit per-user autoswitch exclusion;
- explicit per-user required routing authority.

## Reality Verdict

```text
assignment_truth_source_identified=true
assignment_truth_source=users.registry
assignment_mutation_paths_identified=true
per_user_routing_mode_found=false
per_user_pin_found=false
per_user_manual_mode_found=false
```

## E35.A Implication

E35.A should treat `users.registry.current` as current state, not as policy intent.

For Execution Authority, V7 needs a separate intent/ownership layer that can say:

```text
this user is AUTO
this user is OPERATOR_PINNED
this user is MANUAL
this authority owns this assignment
this assignment expires or remains until explicitly changed
```
