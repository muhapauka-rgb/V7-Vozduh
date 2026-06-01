# Program F2 Reality Audit

Date: 2026-06-01
Branch: `v7-next`
Status: STOPPED_STALE_APPROVED_TARGET

## Repository

- Current branch: `v7-next`
- HEAD: `d139c47d470055d8e61c3f40e7c4a2343d2538f4`
- `origin/v7-next`: `d139c47d470055d8e61c3f40e7c4a2343d2538f4`

## Runtime Evidence

Fresh read-only evidence was collected in:

`/private/tmp/v7-program-f2`

Key files:

- `users.before.registry`
- `egress.before.registry`
- `runtime-guard.before.txt`
- `safety.before.json`
- `shadow.before.json`
- `proposal.before.json`
- `move-preview.before.json`
- `rollback-preview.before.json`
- `target-drift-analysis.json`

## Current Runtime Distribution

- enabled users: `18`
- registry rows: `19`
- `amneziawg-exec-20260528-10-8-1-14`: `10`
- `awg0`: `3`
- `awg3`: `3`
- `vless`: `2`

## User State

- user: `10.7.0.16`
- current egress: `vless`
- route table: `1014`

## Approved Proposal From Prompt

- user: `10.7.0.16`
- movement: `vless -> awg3`
- rollback: `v7-user-switch 10.7.0.16 vless`
- budget: `1`

## Fresh Planner Proposal

Fresh bounded proposal now recommends:

- user: `10.7.0.16`
- movement: `vless -> awg0`
- score: `2051.26`

The prompt-approved target `awg3` is still eligible but no longer the top fresh recommendation:

- `awg0`: score `2051.26`
- `awg3`: score `2020.54`

## Reality Verdict

The approved target is stale relative to the fresh planner truth. Execution was blocked before movement.

