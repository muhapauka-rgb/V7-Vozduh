# Program Z1 Drift Handling

Date: 2026-06-01
Status: CERTIFIED_FAIL_CLOSED

## Stale Approval Denied

Prompt-approved packet:

- `10.7.0.16 vless -> awg0`

Fresh planner state:

- canonical proposal: `10.7.0.10 awg0 -> awg3`
- `10.7.0.16` fresh target: `awg3`
- `awg0` became ineligible with `stability_below_floor`
- healthy egress total dropped to `1`

Result:

- stale packet denied
- no movement performed
- no autoswitch apply performed

## Fresh Approval Candidate

Fresh canonical candidate requiring new approval:

- user: `10.7.0.10`
- movement: `awg0 -> awg3`
- rollback: `v7-user-switch 10.7.0.10 awg0`
- budget: `1`

## Verdict

drift_handling_certified=true

The system failed closed instead of executing a stale approved target.

