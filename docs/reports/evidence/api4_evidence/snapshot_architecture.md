# API.4 Snapshot Architecture

## Snapshot Type

`admin_core.overview_views.OverviewSnapshot`

Fields:

- `state`
- `users_registry`
- `egress_registry`
- `draft_evidence`

Derived read-only properties:

- `users`
- `active_users`
- `egress_state`

## Purpose

The snapshot is request-scoped. It does not cache across requests.

Goal:

- one read
- many consumers
- no behavior change
- future cache boundary becomes clear

## API.4 Applied Improvement

`overview()` now reads `users.registry` once and reuses it for:

- fallback effective user list
- `registries.users` response payload

Before API.4, `overview()` could parse the users registry twice in a single request.
