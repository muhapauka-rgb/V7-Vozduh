# Phase 6 - Source Evacuation

Summary: Planner/API now support source/current-egress scoped plans while preserving target-egress behavior.

Files changed:
- `tools/v7-users-autoswitch`
- `admin/v7-admin-api`
- `tests/unit/test_v7_users_autoswitch_policy.py`
- `tests/unit/test_api3_read_only_views.py`

Tests:
- source-egress planner unit test PASS
- API source/target command unit test PASS

Observations:
- `--target-egress` still means move TO target.
- `--source-egress` / `--current-egress` means evacuate FROM source.

Production impact: no runtime apply.

Canonical changes: NONE.

Next phase: UI wording.
