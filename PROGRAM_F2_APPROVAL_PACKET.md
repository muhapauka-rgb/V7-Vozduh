# Program F2 Approval Packet

Date: 2026-06-01
Status: DENIED_STALE_TARGET

## Prompt-Approved Packet

- user: `10.7.0.16`
- movement: `vless -> awg3`
- budget: `1`
- rollback: `v7-user-switch 10.7.0.16 vless`

## Fresh Recheck Result

Fresh bounded proposal returns:

- user: `10.7.0.16`
- movement: `vless -> awg0`
- budget: `1`
- proposal count: `1`
- fail-closed reasons: `[]`

## Drift Evidence

Target scoring for `10.7.0.16`:

| Target | Eligible | Score | Notes |
| --- | --- | ---: | --- |
| `awg0` | true | `2051.26` | fresh recommended target |
| `awg3` | true | `2020.54` | prompt-approved stale target |
| `vless` | false | `0.0` | current egress not eligible |

## Packet Verdict

approval_packet_created=false

Reason:

Creating an executable packet for `awg3` would knowingly approve a stale target that no longer matches fresh planner truth.

## Safe Next Packet

If operator wants to continue, a new approval must explicitly approve the fresh target:

`APPROVE PROGRAM F2: move 10.7.0.16 from vless to awg0 with budget=1 and rollback=v7-user-switch 10.7.0.16 vless`

