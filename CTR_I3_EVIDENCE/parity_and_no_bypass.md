# CTR.I3 Parity And No-Bypass Evidence

## Implemented dry-run simulation fields

For every candidate:

- `existing_score`
- `ctr_soft_adjustment`
- `simulated_score`
- `score_delta`
- `old_position`
- `new_position`
- `ranking_delta`
- `ctr_state`
- `service_impact`
- `capacity_impact`
- `trust_impact`
- `recovery_impact`

## Explicit non-authority flags

Every simulation row includes:

- `planner_score_applied=false`
- `planner_ranking_changed=false`
- `selected_moves_changed=false`
- `runtime_behavior_changed=false`
- `simulation_authority=none`

Routing summary includes:

- `pool_soft_influence=dry_run_score_simulation_only`
- `planner_score_applied=false`
- `hard_gate_applied=false`
- `target_suppression_applied=false`
- `execution_authority=none`
- `selected_moves_write_authority=none`

## Test evidence

Targeted tests passed:

- `test_ctr_advisory_is_visible_without_changing_candidate_score_or_selected_moves`
- `test_ctr_soft_score_simulation_can_detect_ranking_delta_without_runtime_change`
- `test_ctr_i1_no_bypass`
- `test_ctr_i2_review_required`

Full suite passed:

- `python3 -m unittest discover tests`
- 433 tests OK

Static validation passed:

- `py_compile` for changed runtime/admin modules
- `git diff --check`

