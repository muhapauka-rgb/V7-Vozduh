# PROGRAM Z4 Rollback Stress

## Objective

Verify rollback path, rollback execution, and rollback observation under degraded conditions.

## Live Result

No Z4 movement occurred because live selected moves were zero. Therefore there was no new Z4 rollback to execute.

## Existing Rollback Evidence

Z3.2 certified the rollback authority for the same candidate:

- user: `10.7.0.16`
- rollback: `awg3 -> vless`
- final users hash returned to pre-move hash
- route/reconcile/killswitch checks were clean

## Stress Boundary

Rollback under current degraded target-pool conditions was not executed because executing movement first would require bypassing the planner. Z4 did not do that.

## Verdict

- rollback_path_exists=true
- rollback_stress_movement_available=false
- rollback_executed_in_z4=false
- rollback_under_stress_certified=false

