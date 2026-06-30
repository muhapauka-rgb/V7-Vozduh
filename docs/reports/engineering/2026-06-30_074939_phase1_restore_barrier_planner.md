# Phase 1 - Restore Barrier Planner

Summary: Planner now exposes failover proposals when the current channel is unusable, even while restore barrier is active.

Files changed:
- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

Tests:
- `python3 -m unittest tests.unit.test_v7_users_autoswitch_policy` PASS

Observations:
- `decisions[]` can show `action=switch`, `move_type=failover`, and `recommended_egress`.
- Legacy `restore_barrier_failover_suppressed` contract was removed from live planner/tests.

Production impact: no production mutation performed.

Canonical changes: NONE.

Next phase: execution-only restore barrier gate.
