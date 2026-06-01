# Program Z1 Reality Audit

Date: 2026-06-01
Branch: `v7-next`
Status: STOPPED_DYNAMIC_DRIFT

## Repository

- Current branch: `v7-next`
- HEAD: `d139c47d470055d8e61c3f40e7c4a2343d2538f4`
- `origin/v7-next`: `d139c47d470055d8e61c3f40e7c4a2343d2538f4`

## Runtime Evidence

Fresh evidence was collected into:

`/private/tmp/v7-program-z1`

Key files:

- `users.before.registry`
- `egress.before.registry`
- `runtime-guard.before.txt`
- `safety.before.json`
- `shadow.before.json`
- `proposal.before.json`
- `move-preview.before.json`
- `rollback-preview.before.json`
- `precheck-summary.json`
- `target-drift-analysis.json`

## User Distribution Before Execution

- `amneziawg-exec-20260528-10-8-1-14`: `10`
- `awg0`: `3`
- `awg3`: `3`
- `vless`: `2`

## Prompt-Approved Movement

- user: `10.7.0.16`
- movement: `vless -> awg0`
- rollback: `v7-user-switch 10.7.0.16 vless`
- budget: `1`

## Fresh Canonical Proposal

Fresh proposal cap returned:

- user: `10.7.0.10`
- movement: `awg0 -> awg3`
- rollback: `v7-user-switch 10.7.0.10 awg0`
- budget: `1`

Fresh planner also now recommends `10.7.0.16 -> awg3`, not `awg0`.

## Reality Verdict

The approved movement was stale before execution. No movement was performed.

