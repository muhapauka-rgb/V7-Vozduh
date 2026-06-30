# Phase 2 - Restore Barrier Execution Gate

Summary: Restore barrier now blocks executable selection instead of hiding proposals.

Files changed:
- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

Tests:
- `python3 -m unittest tests.unit.test_v7_users_autoswitch_policy` PASS

Observations:
- Active restore barrier sets `selected_moves=[]`.
- Summary exposes `execution_blocked=true` and `execution_blocker=restore_barrier`.
- Apply remains fail-closed with no selected moves.

Production impact: no users moved.

Canonical changes: NONE.

Next phase: execution identity verification.
