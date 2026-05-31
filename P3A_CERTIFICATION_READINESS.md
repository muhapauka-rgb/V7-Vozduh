# P3.A Certification Readiness

Project: V7 Vozduh
Block: P3.A Runtime Dry-Run Foundation

## Readiness Status

Status: `READY_WITH_BLOCKERS`

P3.A is safe to continue to Runtime Hook Dry-Run design only if the blockers below are treated as hard constraints.

## Ready Signals

- Existing branch baseline is `v7-next`.
- P2.9 reported `safe_to_continue_to_runtime_dry_run=true`.
- Existing preview architecture already separates candidate/review/approval/dry-run from execution.
- Runtime observers and previews already exist.
- Existing admin API uses preview-only and non-authoritative safety flags.
- Existing dry-run routing tools explicitly avoid routing changes and user movement.
- P3.A created architecture and audit reports only.

## Hard Blockers For P3.B

Runtime Hook Dry-Run design must prove:

- Hooks are passive observers only.
- Hooks have no action authority.
- Hooks cannot call autoswitch apply.
- Hooks cannot change routing.
- Hooks cannot move users.
- Hooks cannot write runtime decision state.
- Hooks cannot create an unbounded event stream.
- Hooks cannot become an execution engine.
- Hook output is derived, preview-only and retention-bound.

## Certification Conditions

P3.B may begin only as a design-only dry-run hook model with:

- No runtime mutation.
- No deploy.
- No systemd changes.
- No route apply.
- No autoswitch apply.
- No user movement.
- No execution engine.
- No authoritative runtime hooks.

## Readiness Verdict

`safe_to_continue_to_runtime_hook_dryrun=true`

