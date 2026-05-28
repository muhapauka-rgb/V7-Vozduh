# BLOCK E11.14 Full Regression Matrix

full_regression_matrix_completed=true

| Check | Result | Evidence |
| --- | --- | --- |
| No delayed non-cohort movement after containment/fix | YES | Post-fix samples A/B/C have identical `users.registry` hash `bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`; switch-history tail unchanged. |
| Restore-settle still works | YES | `tools/v7-restore-settle-gate --pre-restore` tests and live pretty/json checks. |
| Planner still works | YES | Live dry-run selected_moves=0, restore_barrier active, no apply. |
| Apply remains contained | YES | `v7-users-autoswitch.timer=inactive` across post-fix samples. |
| Reservation enforcement still works | YES | WireGuard candidate remains blocked by `canary_reserved_production_assignment_blocked`. |
| WireGuard clean target remains clean | YES | WireGuard users=0 in target readiness checks. |
| Autoswitch regression observed | NO | Targeted autoswitch tests pass; live dry-run selected_moves=0. |
| Delayed reassignment observed after fix | NO | No new switch-history rows after E11.13 delayed moves. |
| Stale selected_moves observed | NO | selected_moves=0 in all post-fix samples. |
| AWG regression observed | NO | Route checks OK for awg0/awg3/target 1 users. |
| Target readiness regression observed | NO | target readiness tests pass; WireGuard remains reserved and clean. |
| Hidden movers observed | NO | Process scans show no hidden `v7-user-switch`, `v7-routing-sync`, or active apply service. |
| Kill switch regression observed | NO | `V7_KILLSWITCH_CHECK=OK` in samples A/B/C. |
| Provisioning reconcile regression observed | NO | `V7_PROVISIONING_RECONCILE_CHECK=OK` in samples A/B/C. |

regressions_observed=false
runtime_checks_ok=true
