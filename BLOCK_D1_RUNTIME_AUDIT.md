# Block D1 Runtime Audit

Project: V7 Vozduh

Block: D1 - Autoswitch Safety Remediation And Decision Tree

Date: 2026-06-01

## Users

Execution target users: `10`

Other channels:

- `awg0`: `3`
- `awg3`: `3`
- `vless`: `3` registry rows, with one disabled user excluded from planner enabled-user totals

## Channels

Enabled egress channels in registry: `7`

Execution-only channels: `1`

Second execution target: none

## Capacity

Execution target:

- Current count: `10`
- Soft limit: `10`
- Hard limit: `10`
- Headroom: `0`

Policy dynamic load:

- `max_hard_limit=80`
- dynamic autoswitch load can show OK even when the governance execution target is full.

## Trust

Trusted RU remains `NEEDS_ATTENTION`.

## Selected Moves

- `selected_count=0`

## Health

Runtime checkers OK.

Admin API unavailable.

## Verdict

Runtime is stable for analysis and shadowing, not ready for autoswitch execution.

