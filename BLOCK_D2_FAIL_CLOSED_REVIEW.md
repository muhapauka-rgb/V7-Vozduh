# Block D2 Fail-Closed Review

Date: 2026-06-01

## Fail-Closed Conditions Implemented

`v7-autoswitch-proposal-cap` returns no proposal when:

- budget is not one of `1`, `2`, `5`, `10`
- shadow JSON has `apply_requested=true`
- safety JSON status is not `ok` or `warn`
- shadow decisions are missing or invalid
- candidate pool is fully removed by hold filters
- input files are unreadable or invalid

## Tests

Added `tests/unit/test_v7_autoswitch_proposal_cap.py`.

Covered:

- budget cap with current egress hold
- safety critical fail-closed
- invalid budget fail-closed
- `apply_requested=true` fail-closed

## Safety Fields

Proposal output explicitly includes:

- `runtime_mutation_performed=false`
- `autoswitch_apply_run=false`
- `routing_changed=false`
- `users_moved=false`

## Verdict

fail_closed_verified=true

