# V7 Chuck2 live blocker sweep and automatic recovery

Date: 2026-08-29

## Purpose

Repair generic blockers on the ordinary profile-required-service recovery
path. Chuck2 (`10.7.0.127`) was used only as a read-only production witness;
no operator or Codex route action was taken.

## Current live evidence before the repair

- `v7-health.service` was active and its existing health loop was the only
  production caller.
- Chuck2 remained on `awg3`, with Instagram and Telegram last observed healthy
  but aging. Therefore there was no fresh persistent required-service failure
  that could lawfully start automatic recovery.
- No currently eligible target supported both required services: VLESS and
  `awg0` had Instagram failure evidence, OpenVPN had Telegram/Instagram
  failure evidence, WireGuard was hard-capacity full, and the certification
  source was not an ordinary target.
- Health-loop evidence showed the one-second prepared-target PATH role taking
  4--10 seconds and returning non-zero; `other_required` had an observed
  65-second overrun. The dominant PATH cause was synchronous Planner projection
  rebuilding after an expired prepared projection.

## Repair

1. `tools/v7-service-matrix-refresh-all` now keeps prepared-target PATH
   observation bounded. When its prepared Planner projection is expired, PATH
   records a deferral to the existing `planner_projection` role rather than
   synchronously launching a Planner rebuild. The current Matrix facts remain
   the source of target readiness; all mutable Matrix, Authority,
   Candidate/Packet/Lease/Barrier, route and S11 checks remain mandatory.
2. `tools/v7-users-autoswitch` now permits a fresh current ordinary
   profile-required-service failure to create a candidate when only an
   intelligence/trust/prediction snapshot is stale. This is candidate-only:
   no Apply exemption exists and the normal governed owners revalidate before
   route mutation.
3. Updated stale test expectations to the current bounded ordinary-member
   slice contract and current direct-L3 outcome provenance contract.

## Verification

- `tests.unit.test_v7_users_autoswitch_policy`: 222 passed.
- Combined focused regression: 157 passed across autoswitch policy,
  prepared-target readiness, service-failure episode and health deadline loop.
- No test or diagnostic call created a Candidate, Packet, Lease, Barrier,
  Authority, incident, route mutation or user move.

## Production effect and next step

The initial repair was deployed as `5d52309b` and the full truth check passed.
The first post-restart health observation then exposed a second bounded cause:
the prepared-target role inherited the general 90-second Matrix writer-lock
wait. The existing health role has therefore been corrected in the current
workspace to use a one-second lock wait for both prepared-target lanes. A
busy writer consequently leaves the target unproven rather than blocking the
recovery path; it does not make a stale target eligible.

After this follow-up deploy,
the existing health-loop caller—not Codex—must observe either a real fresh
profile-required-service failure or the existing lawful Polygon controlled
falsification. It must then prove the full automatic Matrix-to-S11 chain for
Chuck2-equivalent ordinary scope within the 7-second contract. The current
live Chuck2 state is not such an event and must not be fabricated.

## Follow-up Runtime reconciliation

The follow-up package (`55064460`) was published and deployed with an explicit
health restart. The running `/usr/local/bin/v7-health-loop` contains the
one-second writer-lock bound for both prepared-target lanes. The old
pre-restart 8--12-second samples are therefore not evidence against the new
package.

Fresh post-restart observations no longer wait on the inherited 90-second
writer lock, but PATH still varied between about 1.0 and 4.0 seconds. Existing
Matrix path evidence itself was short (for example, `awg3` path projection was
143 ms), so the remaining delay cannot be responsibly attributed to the
network-path probe alone.

To distinguish owner/module loading, parallel path reads and the one atomic
Matrix write, the existing health process now retains the already emitted
prepared-PATH receipt in memory only until the child exits and writes its
compact timing split to the existing service journal. It creates no state
file, timer, queue, owner or routing action. Focused regression after this
instrumentation passed (health-loop, prepared target, failure-episode and
autoswitch-policy suites; `git diff --check` passed).

The first deployed instrumented process confirmed normal post-restart PATH
completions around 0.4--1.1 seconds. Its compact timing line was not emitted,
because a zero-duration pipe read could discard the already completed child
receipt before Python drained it. This bounded instrumentation defect is
corrected to drain only after `poll()` has confirmed exit; it does not change
the Matrix command, target scope, user state or recovery semantics.

Further live scope reconciliation showed that the repeatedly failing OpenVPN
source contained only a certification identity (`certification_user=1`), not
an ordinary customer. The ordinary five-second profile detector nevertheless
kept treating it as an ordinary source and repeatedly launched bounded Matrix
confirmation/consumer work. That self-inflicted load delayed unrelated health
roles. The ordinary producer now excludes certification-only identities; their
existing controlled owner retains all Matrix visibility and responsibility.

After the owner-only scope correction, production telemetry fell from four
active sources/six observations plus a repeated receiver wake to three active
ordinary sources/five observations and zero receiver wakes; first ordinary
profile result was 607 ms. Initial live measurement after a one-second
per-service cap still showed 7.4--24.2-second ordinary-detector runs: the
batch finished in 0.3--0.7 seconds, but the parent then repeated several stale
profile probes serially. This was duplicate work on historical evidence, not a
fresh-failure confirmation. The FAST producer now records that stale evidence
for the existing normal Matrix reconciliation and returns `UNKNOWN` without a
synchronous repeat. It cannot authorize recovery or conceal a fresh failure;
a current Matrix failure remains required for every downstream trigger.
Full/deep diagnostic revalidation is unchanged.

The next live cycle exposed one final duplicate: when the fast batch returned
`UNKNOWN` but the canonical Matrix already held a fresh confirmed failure, the
producer correctly reused that failure for eligibility but then synchronously
ran the same Matrix confirmation again before waking the existing consumer.
The repeat was the observed long span. The correction reuses the fresh
canonical confirmation only when the existing governed consumer is available;
otherwise it preserves the old confirmation path. This preserves Matrix,
Authority, Candidate/Packet/Lease/Barrier and S11 ownership while removing no
safety check and no ordinary-user route action.

Final profiling of that caller showed a further mechanical cost: it parsed the
same 310-KB canonical Matrix file once for every active profile while the host
was contended. The fast producer now builds one temporary, process-local index
of fresh identified Matrix failures and reuses it for its current batch.
Historical failures are deliberately absent. The index is discarded before
exit and creates neither durable state nor a second health owner.

Runtime also showed that the old 500-ms parallel sentinel frequently returned
`UNKNOWN` under normal host contention. That is safe but cannot establish a
failure for recovery. Its bounded observation budget is now 1,000 ms; cadence,
target selection, Authority, Matrix ownership and route execution are
unchanged. `UNKNOWN` remains a no-move result.

Next: deploy this bounded detector correction, verify its ordinary-role timing
in Runtime, then return control to the normal V7 caller for the automatic
Chuck2-equivalent seven-second proof. No manual user movement is admissible.
