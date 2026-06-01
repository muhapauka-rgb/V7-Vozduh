# Block D2 Planner Cap

Date: 2026-06-01

## Implementation

Added `tools/v7-autoswitch-proposal-cap`.

This helper:

- reads existing `v7-users-autoswitch` shadow JSON
- rejects any shadow where `apply_requested=true`
- optionally checks safety-review JSON status
- accepts bounded budgets only: `1`, `2`, `5`, `10`
- applies hold filters before selecting proposal moves
- emits a preview-only operator proposal
- never calls `v7-user-switch`
- never calls `v7-users-autoswitch --apply`
- never writes runtime state

## D2 Runtime Shadow Input

- Raw candidate moves: `12`
- Shadow selected moves: `0`
- Reason selected moves stayed zero: existing restore barrier with zero movement budget.

## D2 Proposal Cap Output

Run parameters:

- budget: `1`
- hold current egress: `amneziawg-exec-20260528-10-8-1-14`
- safety JSON: fixed safety-review, `status=ok`

Result:

- raw candidates: `12`
- held candidates: `10`
- eligible candidates: `2`
- proposal count: `1`
- ready for operator review: `true`

## Verdict

planner_cap_working=true

