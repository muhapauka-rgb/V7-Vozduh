# Phase 7 - UI

Summary: Channel autoswitch UI now distinguishes recommendations to a channel from evacuation from a channel.

Files changed:
- `admin/v7-admin-api`

Tests:
- `python3 -m unittest tests.unit.test_api3_read_only_views` PASS

Observations:
- UI labels now separate recommendations, selected execution, and blocked execution.
- Restore barrier proposals are shown as proposals/blocked, not as already executable moves.

Production impact: no UI deploy performed in this step.

Canonical changes: NONE.

Next phase: regression validation.
