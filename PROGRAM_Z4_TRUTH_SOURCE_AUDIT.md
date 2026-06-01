# PROGRAM Z4 Truth Source Audit

## Truth Source Matrix

| Domain | Canonical source | Derived source | Presentation source |
| --- | --- | --- | --- |
| Proposal | live `v7-users-autoswitch` planner output | proposal cap tests and prior Z3 reports | Z4 reports |
| Movement | live planner selected moves plus existing apply authority | none in Z4 because selected moves were zero | Z4 repeatability and certification reports |
| Rollback | live `v7-user-switch` authority | Z3.2 rollback evidence | Z4 rollback stress report |
| Verification | live route/reconcile/killswitch rc values | stress probe on live-derived copy | Z4 runtime audit |
| Observation | live registry hashes and rows | temporary copy deltas | Z4 reality audit |

## Runtime Dominance

Runtime truth overrides prior certification reports. Z3.2 proved that one-user autonomy can work, but Z4 current reality shows no eligible failover target and `healthy_egress_total=0`.

## Derived Stress Evidence

Stress tests were performed on `/tmp/z4-stress-881sfifh`, copied from live state. These tests are valid for planner behavior under degraded inputs, but they are not a substitute for a production movement when the live planner refuses movement.

## Verdict

- canonical_proposal_source=live_planner
- canonical_movement_source=live_selected_moves
- canonical_rollback_source=live_v7_user_switch
- canonical_verification_source=live_route_reconcile_killswitch
- stale_report_used_as_truth=false
- truth_sources_clean=true

