# Block A Implementation Conflict Audit

Project: V7 Vozduh

Block: A - Single User Completion Program

Date: 2026-06-01

## Existing Implementation Found

Existing runtime movement implementation:

- `v7-user-switch`
- `v7-route-movement-preview`
- `v7-user-route-check`
- `v7-killswitch-check`
- `v7-provisioning-reconcile-check`

## Decision

Reuse existing implementation.

No parallel movement engine, no runtime hook, no autoswitch apply, and no new execution engine were introduced.

## Behavior

`v7-user-switch` performs the actual movement by:

- Reading `/opt/v7/egress/state/users.registry`
- Validating user and egress IDs
- Resolving target interface from `/opt/v7/egress/state/egress.registry`
- Replacing default route for the user's routing table
- Updating `/opt/v7/egress/state/user-<ip>.assign`
- Rewriting the user row in `users.registry`
- Appending normal audit and switch-history records when available

`v7-route-movement-preview` is non-mutating and emits the route and file changes that would occur.

## Owner

Runtime owner: existing V7 egress runtime toolchain under `/usr/local/bin` and `/opt/v7/egress/state`.

## Conflict Notes

Two early Block A attempts stopped before mutation:

- Attempt using SQLite stopped because `sqlite3` CLI was not available.
- Attempt using Python SQLite stopped because `/opt/v7/v7.db` had no `users` table.

Both attempts occurred before `v7-user-switch` and did not mutate runtime state.

## Final Path

The final implementation path used the existing registry-based truth source and existing movement command:

```text
v7-user-switch 10.7.0.11 1
```

## Conflict Verdict

- Parallel system created: false
- New runtime hook created: false
- Existing implementation reused: true
- Stop condition triggered: false, because implementation existed and was reused rather than duplicated

