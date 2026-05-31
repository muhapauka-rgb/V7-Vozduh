# E35.0 User Pinning Audit

## Scope

Audit question: does V7 have pinned/preferred/persisted user channel assignment today.

## Current Assignment

persisted_assignment_exists=true

Runtime user assignment is stored in `users.registry` as:

- `ip`
- `current`
- `table`
- `enabled`

Tools and admin code repeatedly use `current` as the user's assigned egress/channel.

Manual movement through `v7-user-switch` changes this assignment and route table state.

## Pinning / Preferred Channel

explicit_pinned_field_found=false
explicit_preferred_channel_field_found=false
explicit_user_routing_mode_found=false

No separate `pinned=true`, `preferred_channel`, or per-user `AUTO/PINNED/MANUAL` field was found in the audited code paths.

The current channel is persistent, but persistence is not the same as a product-level pinning contract.

## Admin Surface

Users can see current channel and route table. Admin workflows can inspect and move users through guarded actions. The required services drawer shows current channel, but it does not define pinning.

## Audit Verdict

user_pinning_audit_complete=true
current_assignment_persisted=true
pinning_model_exists=false
preferred_channel_model_exists=false

## E35 Implication

E35 should introduce or document a clear distinction:

- current channel: what is true now
- preferred channel: operator preference
- pinned channel: hard constraint unless emergency rollback/containment
- automatic mode: eligible for proposal/scheduler

Without that distinction, admin users may interpret `current` as "pinned" when it is only current state.
