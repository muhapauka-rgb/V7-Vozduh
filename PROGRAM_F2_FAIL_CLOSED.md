# Program F2 Fail Closed

Date: 2026-06-01

## Verified Fail-Closed Case

Stale packet denied.

Prompt-approved target:

- `awg3`

Fresh planner target:

- `awg0`

Action:

- no movement
- no autoswitch apply
- no routing mutation

## Other Cases

Not live-exercised in F2 because execution stopped safely before movement:

- duplicate packet
- replay
- expired packet
- invalid packet
- blocked packet

replay_protection_verified=false
fail_closed_verified=true

