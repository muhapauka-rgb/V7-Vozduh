# Phase 3 - Execution Identity

Summary: Execution identity remains tied to executable selected moves only.

Files changed:
- `tools/v7-users-autoswitch`

Tests:
- `python3 -m unittest tests.unit.test_v7_users_autoswitch_policy` PASS

Observations:
- `selected_move_hash`, `operation_id`, and atomic envelope are computed after restore-barrier execution gating.
- When execution is blocked, selected move count is zero.
- Approved plan lock and existing clearance behavior remain in the existing owner path.

Production impact: no packet, rollback, or authority change.

Canonical changes: NONE.

Next phase: API parsing and diagnostics.
