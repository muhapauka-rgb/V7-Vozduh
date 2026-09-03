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

## Publication and Runtime reconciliation

- Published commit: `c3fe79c9bab1717d0471cafbc2540d97e21f5de3` on
  `Updatesystem`; GitHub independently resolves that same commit.
- Safe deploy: `deploy-z8-14-Updatesystem-c3fe79c-20260903T110256`.
  The first deploy invocation correctly refused a mixed Runtime because the
  existing health-loop dependency also required a restart.  The second used
  the explicit existing health restart path.
- Post-deploy `v7-truth-check --all --json` is `FULLY_ALIGNED` with no
  blockers: Runtime, GitHub and local all identify `c3fe79c9`; Admin and
  `v7-health.service` are active and the live Matrix owner is proven.
- Fresh authenticated `/api/live-status` after deploy reports VLESS as
  `WARN`, one healthy service out of fourteen, and zero enabled ordinary users
  currently assigned to it.  This is not a live affected-scope acceptance
  case; no recovery transaction was manufactured.

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

## 2026-09-03 live contention reconciliation

Fresh read-only Runtime evidence identified a second, independent cause of
ordinary recovery instability:

- `v7-health.service` is active, but its `other_required` detector has both
  normal `2.6–3.3 s` cycles and measured outliers of `15.1 s`, `18.8 s` and
  `19.9 s`;
- those outliers create deadline misses and suppress the next source
  observation, so they are incompatible with the `<=7 s` product contract;
- the detector itself had no Receiver or consumer wake in the sampled state;
  the outlier is before Matrix/Planner/Apply, inside its observation batch;
- at the same instant, `v7-admin-api` consumed about `67%` CPU on the
  two-vCPU Runtime while an ordinary browser tab was open;
- the cause is the passive Admin overview: it synchronously ran one
  `ip route get` per enabled user on every full refresh.  With the current
  large registry, that fan-out can run for minutes and competes directly with
  the independent existing health owner.

Contained correction:

- the passive landing-page overview no longer executes per-user route probes;
- it continues to read current assignments and Matrix health through the
  existing `live-status` surface;
- the existing global kill-switch summary remains in the overview;
- the existing exact per-user route checker remains available in the user
  detail and explicit checks endpoints;
- absent passive route evidence is shown as `route_check_not_loaded`, not as
  a false route failure.

This changes neither Matrix, Planner, Authority, route writer, recovery
caller, service cadence nor any user assignment.  It removes an accidental
Admin read-model CPU competitor from the recovery path.

Focused regression: `26 PASS` in `tests.unit.test_admin_realtime_truth` and
`37 PASS` in `tests.unit.test_v7_health_fast_deadline_loop`.  The separately
run broad `test_v7_egress_diagnose` baseline has one pre-existing fixture
expectation failure (`test_fresh_matrix_failure_unblocks_batch_budget_unknown`)
outside these changed files; it expects a shadow receiver invocation even
though the fixture's fresh Matrix failure is already reused without a consumer
wake.  It is not accepted as evidence for this correction.

## Post-deploy measurement and bounded detector residual

Safe deploy `deploy-z8-14-Updatesystem-b86289d-20260903T114113` published the
Admin correction at `b86289daae67ef622eac576c633bc93e9c88a59d`.  The remote
`/usr/local/bin/v7-admin-api` SHA-256 exactly matched the deploy manifest and
both `v7-admin-api.service` and `v7-health.service` were active.

The catastrophic `15–20 s` detector cycles disappeared after the Admin fan-out
was removed.  The immediately following ordinary-detector receipts were
`2.147`, `2.314`, `2.607`, `2.772`, `2.649` seconds.  However, the same
post-deploy observation also proved a remaining bounded runtime residual:
occasional `3.48–5.04 s` runs still crossed the `3.5 s` role cadence and
produced `PREVIOUS_INVOCATION_RUNNING` receipts.  This is not a new recovery
owner or an Apply defect.  The live state decomposed a typical batch as:

- 12 source/profile service probes;
- `1.517 s` network wall time;
- `0.231 s` bounded post-processing;
- three timeout-like network attempts;
- no Matrix consumer wake or route mutation.

The existing detector's one-wave, 12-process burst is therefore the exact
remaining CPU/scheduling tail.  The contained next correction keeps the same
12 probes, one-second sentinel semantics, Matrix confirmation and 3.5-second
cadence, but bounds the existing batch to six concurrent probes (two
one-second I/O waves).  It removes the avoidable 12-process scheduling peak
while remaining under the existing five-second batch capacity law.  No route,
user, Matrix, Planner, Authority or automatic caller is changed.

Focused proof for this second correction: the exact cadence, ordinary-detector
takeover and bounded-contract tests pass, and the batch concurrency invariant
passes.  One full local timing-suite run experienced a host-side 1.311-second
scheduler pause in an unrelated synthetic fast-phase test; its isolated rerun
passed, so it is recorded as test-host noise rather than treated as runtime
evidence.

### Live rejection of the six-probe hypothesis

The six-probe cap was deployed as `1e22104503cab730325b2cf922e3201c4b47c5aa`
through `deploy-z8-14-Updatesystem-1e22104-20260903T115230` and then measured
on the live two-vCPU Runtime.  It is **rejected**: two waves produced a
`2.773 s` network span and subsequent `3.851`, `3.410`, `4.672`, `4.923`,
`5.087`, `4.093` and `4.099 s` detector runs, with repeated
`PREVIOUS_INVOCATION_RUNNING` receipts.  The operational correction is
therefore to restore the previously proven twelve-probe one-wave cap
immediately; no recovery semantics, user assignment or Matrix state was
altered during this negative experiment.

### Exact remaining postprocess repair

The restored twelve-probe receipt then exposed the causal residual directly:
network sampling was bounded (`2.837 s`), but postprocess reached `7.152 s`.
The batch had six current profile contracts on three sources.  When multiple
contracts on one source reported the same current suspicion, the existing
shell consumer called the canonical Matrix confirmation once *per profile*,
serially.  This was duplicate work before T0, not a valid safety requirement.

The repair batches the exact failed-service union per source into one existing
canonical Matrix call, refreshes the same ephemeral fresh-failure index, and
lets each profile consume only its own matching current Matrix result.  If
that source confirmation itself has no exact failure, every affected profile
stops safe for that generation rather than repeating the same confirmation.
An unavailable source confirmation keeps the previous per-profile fail-closed
fallback.  Matrix remains the only persistent writer; no Planner, Authority,
user assignment, route operation or new queue is introduced.

Focused regressions prove both the one-source/one-confirmation law and the
existing stale-failure, fresh-Matrix reuse and health-detector takeover laws.

### Source-confirmation wave residual

The first deployed source-union version reduced duplicate confirmation from six
profile calls to three source calls, but a live failure-bearing batch still
measured `4.637 s` post-processing (`3` receiver invocations across `3`
sources).  The calls were still started serially even though their network
observations are independent; only the canonical Matrix write is shared.

The current correction launches the bounded source confirmations concurrently
within the already-existing fast-producer cap, waits for that finite wave, then
rebuilds the ephemeral Matrix index once.  Matrix's existing lock still
serializes its short write and each non-confirmed source follows the existing
fail-closed profile fallback.  No users, routes, Authority, Planner, Matrix
schema, timer, queue, or recovery caller changes.  Focused regressions remain
`4 PASS`; the next required evidence is a live failure-bearing detector cycle
on the deployed fingerprint.

Safe deploy `deploy-z8-14-Updatesystem-f4322cb-20260903T121009` published
commit `f4322cbd362a02f79f9d505821a014fb5b58d11d`; the remote
`v7-egress-diagnose` SHA-256 is
`b06d52cbc37fe11724ddd264c9e43ad9857de4c738cb64b38e9ebbadad01ad61` and
`v7-health.service` is active.  Immediately after deployment, no source had a
fresh raw failure (`receiver_invocation_count=0`), so no invented event was
used to claim the parallel failure result.  The ordinary healthy baseline was
`2.242`, `2.582`, `2.283`, `2.769`, `2.404`, `2.991`, `2.549`, `2.344`,
`2.480` and `2.468 s` from contract build through receipt, without a new
`other_required` deadline miss in that interval.  The next actual failed
source will provide the required failure-bearing evidence.

### Admin access reconciliation

The existing V7 Admin session was opened directly at `/admin-v2` on
2026-09-03.  It reached the live overview without a new login prompt and its
browser console had zero current errors.  This is an access/read-surface check
only: it did not create a user, save a profile, select a channel, or invoke an
operator recovery action.
