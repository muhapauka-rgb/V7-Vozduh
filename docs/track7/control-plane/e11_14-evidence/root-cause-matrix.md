# BLOCK E11.14 Root-Cause Matrix

root_cause_matrix_completed=true

| Theory | Evidence | Reproduced | Operational impact | Regression risk | Fix complexity | Blast radius |
| --- | --- | --- | --- | --- | --- | --- |
| planner cache | No selected moves in planner/apply runs before 13:18:24; later run recomputed fresh service state. | NO | Low | Low | N/A | None |
| selected_moves cache | Runs before movement had selected_moves=0; movement run had fresh selected_moves=3. No persistent selected_moves artifact was needed. | NO | Low | Low | N/A | None |
| apply timer timing | Apply timer ran every ~20s after restore; movement occurred on a later cycle after transient service state changed. | YES | High | Medium | Medium | Non-cohort production users |
| restore ordering | Planner restore, settle GO, then apply restore followed documented order. The order was insufficient because apply cycles after GO were not quarantined. | YES | High | Medium | Medium | Non-cohort production users |
| rebalance | Movement type was failover; rebalance_candidates=0. | NO | Low | Low | N/A | None |
| fallback | Movement was failover from current ineligible target, not fallback to reserved target. | PARTIAL | Medium | Low | Low | Limited by failover cap |
| delayed recompute | 13:18:24 fresh recompute saw `telegram_required_telegram_down_14s` and selected 3 failovers. | YES | High | Medium | Medium | Three non-cohort users in observed run |
| stale planner output | No evidence of apply consuming stale planner output; service invokes `v7-users-autoswitch --apply` and recomputes. | NO | Low | Low | N/A | None |
| target pressure drift | Target `1` load was not hard/soft overloaded; trigger was Telegram service signal. | NO | Medium | Low | N/A | None |
| autoswitch persistence | Anti-flap state recorded incoming moves after the apply run but did not cause the initial selection. | NO | Low | Low | N/A | None |
| timer overlap | No overlapping apply process observed; service finished each cycle. | NO | Medium | Low | N/A | None |
| governance gap | Restore-settle did not protect against future apply-timer service-signal failover after GO. | YES | High | Medium | Medium | Non-cohort production users |
| restore-settle insufficiency | Gate sampled a past window only; it did not bind the next apply generations or service-signal state. | YES | High | Medium | Medium | Non-cohort production users |

## Classification

root_cause_classification=H_MIXED
primary_classification=GOVERNANCE_GAP
secondary_classification=DELAYED_RECOMPUTE_SERVICE_SIGNAL
confidence=HIGH

Supporting evidence:

- Movement was performed by `v7-users-autoswitch.timer`, not a manual command.
- The successful apply run selected failover because target `1` was blocked by `telegram_required_telegram_down_14s`.
- Restore-settle samples before apply restore were clean.
- Multiple apply timer cycles after restore were clean before the transient hard signal appeared.
- Existing restore-stage suppression did not cover `telegram_required_*` as service-signal-only and there was no active restore barrier for timer cycles after restore.
