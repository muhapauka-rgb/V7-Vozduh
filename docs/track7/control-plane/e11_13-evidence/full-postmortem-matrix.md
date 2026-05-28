# E11.13 Full Postmortem Matrix

postmortem_completed=true
execution_allowed_now=false

| Risk | Evidence | Observed | Verdict |
| --- | --- | --- | --- |
| Target overload | User2 verification showed `registry_wireguard_users=2`; WireGuard hard limit is `2` | NO | Hard limit reached but not exceeded |
| WireGuard instability under 2-user load | Observation A/B/C kept `wireguard_users=2`, route/checkers OK | NO | No cohort-load regression observed during window |
| Route mismatch | User1/user2 verification and observation routes used `v7e06a394c478`; rollback routes restored `v7e356a192b79` | NO | Candidate routes correct |
| Kill-switch regression | Checkers OK after user1, user2, rollback, delayed monitoring | NO | `V7_KILLSWITCH_CHECK=OK` |
| Planner/apply race during hold | Hold verification: planner/apply timers inactive, health active, selected_moves=0 | NO during hold | Hold window worked |
| Hidden routing-sync/user-switch | Hidden scans empty in precheck, hold, observation, rollback, delayed monitoring | NO | No hidden process observed |
| Reservation enforcement regression | WireGuard planner candidate remained blocked by `canary_reserved_production_assignment_blocked`; final target readiness GO as reserved zero-user target | NO | Reservation still enforced |
| Stale selected_moves | Precheck, observation, restore-settle, delayed monitoring all showed selected_moves=0 | NO | No stale selected move at sample points |
| Rollback partial failure | Both rollback commands succeeded; only approved users changed; routes restored | NO | Rollback clean |
| Restore-settle regression | Restore-settle gate after planner restore was GO with 3 samples and stable registry | NO before apply restore | Gate worked |
| Apply restore churn | After apply timer restore, delayed monitoring sample C changed registry hash and switch-history showed three autoswitch movements | YES | Apply restore still can produce delayed movement |
| Delayed autoswitch movement | Switch history: `10.7.0.9`, `10.7.0.10`, `10.7.0.13` moved `1 -> awg0` at `2026-05-27T10:18:25-29Z` | YES | Lifecycle not clean for promotion |
| Delayed reassignment to WireGuard | Final state and delayed samples show WireGuard users=0 | NO | Reserved target remained clean |
| Target readiness regression | Final target readiness selected WireGuard GO for governed readiness | NO | Target readiness after rollback remains GO |
| Autoswitch churn | Non-cohort autoswitch movement occurred after apply restore | YES | Apply timer was re-held for containment |
| Target starvation | WireGuard returned to zero users and production assignment remains blocked | NO | Clean reserved target recovered |
| Capacity edge cases | Two-user max exercised; no third WireGuard user appeared | NO | 3-user cohort remains forbidden |
| Restore timing overlap | Movement occurred after apply timer restore despite pre-restore gate GO | YES | Need stricter post-apply guard/root cause |
| Planner cache | Planner read-only after containment reports selected_moves=0 | NO active stale move | Cache not currently selecting moves |
| Runtime checks | Final checkers OK in delayed classification and probe | NO failure | Runtime is operational but apply held |

postmortem_verdict=MINI_COHORT_EXECUTED_ROLLED_BACK_DELAYED_APPLY_MOVEMENT_OBSERVED_CONTAINED
recommended_next_block=E11.14_DELAYED_APPLY_RESTORE_MOVEMENT_ROOT_CAUSE_AND_APPLY_TIMER_GOVERNANCE_FIX
