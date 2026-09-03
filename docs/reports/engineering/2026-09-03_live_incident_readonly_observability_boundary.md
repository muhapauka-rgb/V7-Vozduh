# V7 live incident evidence and Admin rebind reconciliation

Date: 2026-09-03

## Request

Read the current reported incident only through existing health, Matrix, Planner
and Authority owners.  No client, route, state, Matrix, policy or service was
changed by this check.

## Fresh authenticated evidence

- Local CPS/OMP state is internally coherent and names
  `V7_RECOVERY_LATENCY_SLO_FINAL_EXECUTION_AND_CLOSURE` as the active frontier.
- GitHub `Updatesystem` resolved to
  `0c6e16b8bd57a0d32605f8fc98bac00a74e6e82a`; the former remote-read failure
  was an Engineering-session transport condition, not a GitHub outage.
- Authenticated Admin audit records prove one automatic ordinary recovery,
  without Codex operating the recovery chain:
  - `2026-09-03T07:23:59.584723+00:00` — `10.7.0.125` was explicitly rebound
    from `awg0` to `vless` by the operator path;
  - `2026-09-03T07:24:57.282547+00:00` — Matrix recorded a current Google
    profile-service failure for `vless` (the neighbouring required-service
    observations share the same generation window);
  - `2026-09-03T07:25:09.637024+00:00` — the live autoswitch caller moved the
    same user from `vless` to `awg0` with reason `autoswitch_failover`.
- Therefore the measured historical decomposition is approximately
  `57.7 s` rebind-to-first-Matrix-failure and `12.4 s` Matrix-to-final
  automatic assignment.  It is functionally automatic but fails the active
  `<=7 s` product contract.
- The current live Matrix projection reports no enabled ordinary user on
  `vless`; its VLESS service evidence is nevertheless unhealthy for multiple
  required services.  It is not valid evidence for a currently affected user
  and must not be used to manufacture a new recovery transaction.
- The production Runtime provenance is still commit
  `407682137352782cb977dea80648c5b71594369b`, while the local/remote branch
  is newer.  Runtime hashes for the health-loop artifacts match their local
  copies, but this provenance gap must be reconciled by the existing safe
  deploy owner before a new live claim.

## Proven Admin defect and contained correction

The same audit chain proves that `operator_profile_egress_rebind` may return
`writer_deadline_exceeded_7s` after `v7-user-switch` has already committed the
registry assignment and Core-primary route.  The Admin UI then rolls back its
optimistic row and tells the operator that the channel was not switched,
creating duplicate clicks despite a completed route change.

The correction reuses the existing `v7-routing-sync --core-primary-verify`
read-only verifier only after that timeout and only when the exact registry
and assignment already name the requested target.  It accepts the action only
when the verifier proves the live Core-primary map is exact.  It introduces no
route writer, target selection, queue, user mutation or automatic-recovery
caller.

Focused regression: `61 PASS` (`test_admin_realtime_truth` and
`test_v7_health_fast_deadline_loop`), including the late-confirmed route case.

## Result

`LIVE_INCIDENT_STATE = AUTOMATIC_RECOVERY_FUNCTIONAL_BUT_SLO_FAIL`.

The residual is not collapsed by the Admin reconciliation: it is a measured
ordinary profile-service detection/admission delay and remains on the current
Recovery Latency SLO frontier.  No current affected user was moved by Codex.

## Safe re-entry

Publish the contained Admin correction through `tools/v7-safe-deploy`, verify
the new Admin Runtime hash and retain normal V7 Runtime as the only recovery
caller.  The next automatic incident must be used to capture fresh
first-observation, Matrix T0, governed Apply and S11 timings before changing
the health-owner detector.
