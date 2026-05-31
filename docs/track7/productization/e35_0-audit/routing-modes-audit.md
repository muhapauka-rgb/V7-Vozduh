# E35.0 Routing Modes Audit

## Scope

Audit question: do AUTO/PINNED/MANUAL equivalents exist today.

## Existing Modes

routing_modes_exist=true

Current system has smart client/route modes:

- `RU_LOCAL`
- `ABROAD_RU_VIA_V7`
- `AUTO_TRAVEL`
- `STRICT_V7`

These are displayed in `Маршруты` and `Настройки` as route/client modes.

Current system also has policy/autoswitch modes:

- `observe`
- `guarded`
- `active`

And egress-level flags:

- `manual_only`
- `reserve_only`

## Missing Per-User Routing Mode

per_user_auto_pinned_manual_exists=false

No explicit per-user mode was found that means:

- AUTO: eligible for scheduler/proposals/execution batches
- PINNED: keep on preferred channel except containment
- MANUAL: only operator-initiated movement

The closest current pieces are:

- `current` assignment in users.registry
- global autoswitch mode
- group route_policy for smart client mode
- channel manual_only/reserve_only flags

## Audit Verdict

routing_modes_audit_complete=true
smart_client_modes_exist=true
global_autoswitch_modes_exist=true
per_user_auto_pinned_manual_exists=false

## E35 Implication

E35 should not reuse "routing mode" ambiguously. It should name the new per-user behavior explicitly, for example:

- `user_routing_control_mode`
- values: `AUTO`, `PINNED`, `MANUAL`

and keep it separate from smart client route modes.
