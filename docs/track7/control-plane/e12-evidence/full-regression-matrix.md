# E12 Full Regression Matrix

| Area | Evidence | Result |
| --- | --- | --- |
| Reservation enforcement | WireGuard remains `canary_reserved=true`; planner blocks production assignment. | PASS |
| Restore barrier | Budget 0 restored after rehearsal; final dry-run selected moves 0. | PASS |
| Delayed movement protection | Switch-history count remained 2698 during live timer rehearsal. | PASS |
| Rollback discipline | No user movement occurred, so no rollback required. | PASS |
| Target readiness | Existing E11.18 target readiness remains GO; no WireGuard users. | PASS |
| Restore-settle | Existing gate remains GO; no registry drift observed. | PASS |
| Generation replay resistance | Token missing/stale generation/stale hash/count mismatch all fail closed. | PASS |
| Stale selected moves | Selected-move hash binding rejects stale replay. | PASS |
| Rebalance leakage | Rebalance candidates were 0 in current selected-move evidence. | PASS |
| Hidden apply | Hidden mover scans clean; apply timer final state inactive. | PASS |
| Planner race | Apply timer run returned `no_selected_moves`; registry hash stable. | PASS |
| WireGuard cleanliness | WireGuard users 0; no switch-history entry after E11.13 rollback. | PASS |
| Runtime checker stability | Reconcile, route, kill-switch, provisioning checks OK. | PASS |
| Governance checker stability | Updated E12 checker passes after report artifacts exist. | PENDING_UNTIL_FINAL_TEST |
| Restart safety | Generation is persisted-state derived; service restart replay test not executed. | RESIDUAL_RISK |
| Persistence safety | Barrier restored to original E11.17 budget-zero file after rehearsal. | PASS |

## Verdict

regressions_observed=false
delayed_movement_observed=false
replay_resistance_complete=true
larger_cohort_readiness_after=CONDITIONAL_NO_GO
