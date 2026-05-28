# E25.2 Post-Rollback Restore-Settle

## Result

`not_applicable_no_forward_movement`

No forward movement occurred, so no rollback and no post-rollback restore operation were required.

The pre-execution restore-settle gate remained GO using the latest approved E25.1 sample window:

- `gate_status=GO`
- `sample_count=3`
- `apply_timer_intervals_covered=5.1`
- `selected_moves_by_sample=[0,0,0]`
- `registry_stable=true`
- `egress_registry_stable=true`
- `checkers_ok=true`
- `hidden_movers_observed=false`

E25.2 did not restore planner/apply timers, did not run autoswitch apply, and did not mutate runtime.
