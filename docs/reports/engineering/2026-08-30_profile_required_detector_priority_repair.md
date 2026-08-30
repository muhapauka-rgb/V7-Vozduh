# Profile-required recovery detector priority repair

## Purpose

Restore the bounded ordinary-recovery detection path: advisory preparation
must not delay detection that a current user's required services are unavailable
on their assigned source.

## Fresh evidence

After the prior execution-window repair, the live V7 Runtime independently
recovered `10.7.0.126` and `10.7.0.127` from `vless` to `awg0`.  Its operation
`runtime_autoswitch_ce0acc08349ce5af6fe17a7a` recorded successful governed
apply, route verification and required-service verification for both members;
Codex invoked no user-specific recovery command or route writer.  The bounded
operation was created at `2026-08-30T19:07:55.358665+00:00` and its verified
Core-primary cohort checkpoint completed at `2026-08-30T19:08:01.205574+00:00`
(`5.847 s`).  This is not credited as a T0-to-S11 seven-second result because
the incident was already ongoing when the repair was deployed.

The same live health logs showed the remaining generic defect: the
`other_required` profile-required detector, despite a five-second cadence,
could complete in 43--78 seconds while `hot_target_other` advisory warming or
`deep` analysis remained running.  That violates the production law that
advisory work is not a synchronous prerequisite for ordinary service-failure
recovery.

## Change

The existing `v7-health-loop` recovery-critical takeover now preempts every
non-critical slow child before the existing `other_required` detector starts.
It therefore also preempts `hot_target_other` (advisory non-critical target
warming) and `deep` analysis.  The existing recovery-critical PATH/Telegram
target lane, Matrix ownership, Planner ownership, cadence, Authority, route
writer and service-verification contract are unchanged.  Interrupted advisory
roles resume only on their ordinary due schedule.

## Tests

- `tests.unit.test_v7_health_fast_deadline_loop`: 25 PASS.
- The focused test proves both advisory target warming and deep analysis are
  terminated before the client-contract detector proceeds.

## Deployment and acceptance frontier

This report accompanies the focused scheduling repair.  After safe deployment,
observe a fresh ordinary service-mismatch generation from the normal V7 caller
only.  Measure first valid Matrix failure observation through all affected
users' required-service S11.  The acceptance limit is `<= 7 s`; `> 8 s` fails.
No synthetic replay, manual user movement or manual execution transition may
receive credit.
