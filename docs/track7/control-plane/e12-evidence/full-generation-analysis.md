# E12 Full Generation Governance Analysis

## Scope

E12 analyzed whether V7 can safely move from the bounded two-user lifecycle to
nonzero selected-move clearance and larger-cohort governance.

## Current Ownership Before E12

- Restore barrier ownership existed as a mutable JSON file.
- Explicit post-TTL clearance existed.
- `clearance_max_selected_moves=0` was proven in E11.17/E11.18.
- Nonzero clearance budget had no immutable binding to planner state.
- Apply timer recomputed live state independently on every run.

## Replay And Race Risks

| Risk | Evidence | E12 classification |
| --- | --- | --- |
| Plain clearance replay | Local copied-state rehearsal selected 3 moves with no budget. | `UNSAFE` |
| Nonzero budget without generation | Budget 3 without token selected 0 after E12 fix. | `FIXED` |
| Stale generation replay | Budget 3 with stale generation selected 0. | `FIXED` |
| Stale selected-move hash replay | Budget 3 with stale hash selected 0. | `FIXED` |
| Count drift | Budget 3 with expected count 2 selected 0. | `FIXED` |
| Budget too small | Budget 2 against 3 selected candidates selected 0. | `FIXED` |
| Apply timer recompute | Live timer rehearsal had `apply_result.reason=no_selected_moves`. | `CONTROLLED` |
| Restart durability | Generation is recomputed from persisted state hashes. | `CONTROLLED`, restart rehearsal still recommended before broad autonomy |

## Implemented Generation Semantics

E12 added planner generation metadata to `v7-users-autoswitch`.

Generation inputs:

- `users.registry`
- `egress.registry`
- `v7-state.json`
- `egress-speed.json`
- `client-speed.json`
- `service-matrix.json`
- `route-classes.state`
- `service-preferences.json`
- `egress-quality-summary.json`
- `telegram-sentinel.json`
- `autoswitch-safety.json`
- `policy.json`
- `org-egress-policy.json`

For expired cleared restore barriers with `clearance_max_selected_moves > 0`,
apply/planner output is allowed only when:

- `generation_token` is present;
- current `planner_generation_id` matches `clearance_generation_id`;
- `approved_selected_moves_hash` matches current selected move fingerprint;
- optional `clearance_expected_selected_moves` matches the current count;
- optional clearance expiry has not elapsed;
- selected move count is not above `clearance_max_selected_moves`.

Any mismatch is fail-closed with `selected_moves=0`.

## Verdict

immutable_generation_governance_required=true
immutable_generation_governance_implemented=true
replay_resistance_complete=true for selected-move replay under restore-barrier clearance

The remaining unsafe area is not replay resistance. It is operational scope:
current live pressure can still produce multi-user selected moves when explicitly
approved, and larger-cohort rollout remains a blast-radius decision.
