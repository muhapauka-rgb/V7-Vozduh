# Program Z1 Runtime Audit

Date: 2026-06-01

## Runtime Guard

- `v7-users-autoswitch.timer`: inactive
- no `v7-user-switch`, `v7-users-autoswitch --apply`, `v7-routing-sync`, policy apply, or rebalance process observed preflight
- deploy performed: false
- systemd changed: false

## Safety

Safety-review:

- status: `ok`
- critical: `0`
- warning: `0`
- enabled egress: `7`

## Capacity And Planner

Fresh shadow:

- users total: `18`
- egress total: `7`
- healthy egress total: `1`
- raw candidate moves: `15`
- selected moves: `0`

Fresh proposal:

- raw candidates: `15`
- held candidates: `10`
- eligible candidates: `5`
- proposal count: `1`
- proposal user: `10.7.0.10`
- proposal movement: `awg0 -> awg3`

## Target Readiness

Prompt-approved movement preview:

- `10.7.0.16 vless -> awg0`
- preview errors: `[]`
- target interface: `awg0`

But fresh planner now marks `awg0` ineligible due `stability_below_floor`, and recommends `awg3`.

## Runtime Verdict

Runtime is not safe to execute the stale approved packet. Fresh approval is required.

