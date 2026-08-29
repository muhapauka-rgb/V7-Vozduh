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

Next: deploy this measurement-only receipt, collect its live timing split, fix
only the measured generic blocker, and return control to the normal V7 caller
for the automatic Chuck2-equivalent seven-second proof. No manual user
movement is admissible.
