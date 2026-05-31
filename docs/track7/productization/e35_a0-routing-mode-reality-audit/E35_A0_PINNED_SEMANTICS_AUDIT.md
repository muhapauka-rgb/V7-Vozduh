# E35.A0 Pinned Semantics Audit

## Question

Does V7 already have `OPERATOR_PINNED` or equivalent pinned-user semantics?

## Findings

No complete pinned-user semantics were found.

Existing related concepts:

| Existing Concept | Looks Like Pinning? | Reality |
|---|---:|---|
| `sticky` score | Partially | Keeps current route harder to beat, but does not forbid movement. |
| `sticky_keep_current` reason | Partially | Explains why current route remains, but not an explicit operator pin. |
| Admin manual switch | Partially | Moves a user manually, but does not persist a pin. |
| Group `preferred_egress` | Partially | Adds group preference score/reason, not a hard pin. |
| `manual_only` channel | No | Channel-level autoswitch exclusion, not user pinning. |
| `exclusive_group` | No | Group/channel access control, not user pinning. |
| Execution-only reservation | No | Target isolation for governed execution, not user pinning. |

## Sticky Behavior

Autoswitch scoring includes:

```text
sticky = 50.0 if egress.id == user.current else 0.0
```

This is a soft score preference. A better candidate can still win if it beats current by policy thresholds.

Decision logic can return:

```text
sticky_keep_current
```

This means:

```text
the current route remains because no candidate beat it enough
```

It does not mean:

```text
the route is pinned
```

## Preferred Egress

Group policy can define:

```text
preferred_egress
```

Autoswitch adds:

```text
group_preferred
org_preference = 60.0
```

This is a soft preference and not equivalent to `OPERATOR_PINNED`.

## Missing Pinned Fields

No durable fields were identified for:

- `pinned=true`;
- `pinned_egress`;
- `pin_owner`;
- `pin_reason`;
- `pin_expires_at`;
- `operator_pinned`;
- `routing_mode=OPERATOR_PINNED` on live user assignment.

## Required Semantics For E35.A

If E35.A introduces pinned routing, it should define:

| Field | Purpose |
|---|---|
| `routing_mode=OPERATOR_PINNED` | Hard block autonomous forward movement away from pinned target unless explicitly overridden. |
| `pinned_target` | Target egress. |
| `pin_owner` | Operator/system that set the pin. |
| `pin_reason` | Human-readable reason. |
| `pin_created_at` | Audit lineage. |
| `pin_expires_at` | Optional expiry. |
| `pin_override_policy` | Whether rollback/containment can override. |

## Verdict

```text
pinned_semantics_exist=false
sticky_semantics_exist=true
group_preferred_semantics_exist=true
operator_pinned_mode_exists=false
```
