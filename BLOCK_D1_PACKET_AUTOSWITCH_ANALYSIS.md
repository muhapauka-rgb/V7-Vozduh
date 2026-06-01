# Block D1 Packet Autoswitch Analysis

Project: V7 Vozduh

Block: D1 - Autoswitch Safety Remediation And Decision Tree

Date: 2026-06-01

## Feasibility

Packet-oriented autoswitch is feasible.

## Model

Raw autoswitch output:

- Advisory only
- No execution
- No selected moves as authority

Proposal packet:

- Planner generation ID
- Input hashes
- Candidate list
- Candidate scores
- Cap
- Exclusions
- Safety status
- Target capacity state

Approval packet:

- Exact users
- Exact target
- TTL
- Dual approval
- Runtime recheck
- Replay protection
- Rollback manifest

Bounded packet:

- `movement_budget`
- `allowed_users`
- `allowed_target`
- `max_scope`
- `observation_plan`
- `fail_closed_reasons`

## Operator Flow

```text
shadow -> proposal packet -> operator approval -> runtime recheck -> bounded execution -> observation
```

## Verdict

`packet_autoswitch_feasible=true`

