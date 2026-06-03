# API.4 Overview Dependency Map

## `overview()` Dependencies

`overview()` currently depends on:

- runtime state snapshot: `v7-state.json`
- `users.registry`
- `egress.registry`
- route reality rows
- service status checks
- stale/killswitch/capacity command reads
- client speed state
- client agent state
- user readiness and onboarding builders
- smart client profile builders
- service matrix state
- draft egress evidence
- service preferences
- direct routing quick status
- Trusted RU diagnostic and readiness state
- identity state
- proxy runtime state
- backup rows
- policy and org policy state
- admin safe mode
- smart mode route state
- service recommendations
- profile delivery overview
- audit and switch history tails
- maintenance summaries

## Expensive Reads

- per-user route probes in `route_status`
- direct routing command probes
- service status command checks
- stale/killswitch/capacity command checks
- traffic SQLite summaries
- JSONL tails for audit/switch history

## Repeated Reads

Before API.4, `overview()` could read `users.registry` twice:

- once for effective users when `v7-state.json` had no users
- once again for `registries.users`

After API.4, `overview()` reads `users.registry` once into the request-scoped overview snapshot and reuses the registry rows for the response.
