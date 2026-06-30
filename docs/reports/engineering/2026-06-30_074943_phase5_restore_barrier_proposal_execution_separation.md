# Phase 5 - Proposal / Execution Separation

Summary: Proposal fields and execution fields are explicitly separated.

Files changed:
- `tools/v7-users-autoswitch`
- `admin/v7-admin-api`

Tests:
- `python3 -m unittest tests.unit.test_v7_users_autoswitch_policy` PASS
- `python3 -m unittest tests.unit.test_api3_read_only_views` PASS

Observations:
- Proposal: `decisions`, `recommended_egress`, `proposal_moves_total`.
- Execution: `selected_moves`, `selected_move_count`, `selected_move_hash`, `operation_id`, `execution_blocked`, `execution_blocker`.

Production impact: no users moved.

Canonical changes: NONE.

Next phase: source evacuation.
