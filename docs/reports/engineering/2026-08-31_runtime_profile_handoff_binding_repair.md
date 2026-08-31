# V7: repair of the live profile recovery handoff

Date: 2026-08-31

## Scope

This is a bounded repair of the existing Matrix -> autoswitch recovery path.
It does not create a new owner, planner, queue, state source or route writer.

## Live evidence that opened the repair

The operator placed three ordinary users on `vless`.  The normal V7 Runtime,
not Codex, detected the profile-required service failure and moved all three
to `awg0` through Candidate, Packet, Lease, Barrier, Apply and service
verification.

The event is not valid seven-second evidence:

| Interval | Observed |
| --- | ---: |
| Matrix T0 | 2026-08-31 09:25:17 MSK |
| governed action starts | 09:26:06 MSK |
| first route assignment | 09:26:16 MSK |
| all three assignments | 09:26:18 MSK |
| required-service verification receipt | 09:26:32 MSK |

The automatic caller was confirmed by the `v7-health.service` journal
(`PROFILE_MATRIX_T0_CONSUMED`) and the generated operation record.  No
operator command, Codex route-writer call, manually selected target, Candidate,
Packet, Lease or Barrier was used.

## Measured cause

The source was current and unambiguous, but the profile fast-path did not keep
that binding.  The existing runtime therefore fell through to the historical
advisory path:

- pre-obligation source reconciliation: 11,596.780 ms;
- final source reconciliation: 12,430.161 ms;
- advisory total: 25,168.937 ms.

These retrospective reads are not a safety prerequisite once current Matrix
evidence has uniquely identified a failed source with affected profiles.  The
existing Planner, Authority, Candidate/Packet/Lease/Barrier owners and exact
route/service verification remain mandatory.

## Repair

`runtime_profile_handoff_source_constraint` now consumes the existing health
binding when present.  If that label is unavailable, it reuses the existing
`automatically_prioritized_failed_source` reader only when its current
Matrix + assignment + required-service join yields one unambiguous source.

The fallback only restores the *source* binding.  It does not choose a target
or a user and cannot create a governed execution object.  A missing or tied
result remains fail-closed and uses the established non-fast path.

## Verification

Passed focused tests:

- exact Matrix source fallback when the environment label is unavailable;
- fast-path passive-history deferral law;
- obligation-before-passive-history ordering.

Focused tests passed: three tests, 0.497 s, no failures.  The committed change
is `46f57e9a Preserve runtime profile failure binding`; the independent GitHub
branch check returned the same commit.  After GitHub truth became available,
the existing safe-deploy gate returned `PASS` and deployed the approved
implementation.

Post-deploy Runtime evidence:

- local and deployed Matrix implementation SHA-256 both equal
  `2a24d21a63ff7cf38f35159b19ceeec526d1336e34163da5f51ca1c0e063a899`;
- `v7-health.service` is active;
- `v7-admin-api.service` is active;
- standalone Matrix and Telegram timers remain inactive.

## Current status and next frontier

The repair is deployed and the previous three-user event is complete: all three
identities are now on `awg0`.  It was completed before this repair and remains
functional evidence only, not 7-second acceptance evidence.

The next action is one new operator-created bad placement.  V7's normal health
caller, not Codex, must then discover and recover it.  The new live sample must
retain every slow result and will be judged against the 7 s / 8 s law.

## Follow-up: repeated placement on the same continuing failed source

At 13:20 MSK the normal `v7-health.service` caller emitted
`PROFILE_MATRIX_T0_CONSUMED` for three ordinary identities newly assigned to
the still-failed `vless` source. Matrix had a fresh three-member failed-source
scope and healthy eligible alternatives. No governed recovery was admitted.

Cause: the existing compact L3 incident for the *same* continuing source
incident remained closed after its earlier successful recovery. The runtime
hot path correctly avoids a slow historical scan, but consequently treated the
old zero-unresolved scope as current and passed no affected identities to the
existing governed executor.

Bounded repair prepared locally:

- Matrix passes its exact current source scope to the existing autoswitch
  advisory process only for the in-process profile handoff;
- autoswitch independently proves the source, incident, current Matrix scope
  count and registry-derived affected count agree;
- only the matching existing compact incident is reopened, with no stored raw
  user list, no target selection and no execution authority;
- Candidate, Packet, Lease, Barrier, Apply and every route mutation remain
  exclusively with the normal existing V7 governed caller.

Focused verification passed: five tests, including scope re-entry isolation,
the process-local handoff boundary, source-fallback behavior, exact ordering
and fresh-obligation materialization. The full two-module historical suite
also exposed pre-existing fixture errors unrelated to these changed paths;
they access partially constructed planners without their required Matrix or
policy inputs. They do not fail in the focused repaired paths.

Deployment and live proof remain pending safe publication of the repair. The
required next action after deployment is to leave the three already placed
identities untouched and observe the normal V7 caller recover them; Codex must
not advance that recovery manually.

At 13:39:45 MSK the production registry still showed the three test identities
`10.7.0.125`, `10.7.0.126` and `10.7.0.127` on `vless`; `v7-health.service`
was active. They were deliberately left in place so that the next valid proof
can originate entirely from the deployed V7 caller. The safe-deploy gate was
locally aligned but returned `NO-GO` solely because GitHub truth was unreadable;
no deployment was attempted or bypassed.

Fresh Matrix reading at 13:40 MSK continued to show current VLESS failures for
Google, Google Auth, Instagram and YouTube under the same active source
incident. It also retained older failures for several other services. Thus the
three identities are correctly left as a live acceptance condition: the source
is not suitable for profiles requiring any of the currently failed services.

## Follow-up: stale fast-producer reuse boundary

After the first deployed scope repair, the ordinary required-service detector
continued to run every 3.5 seconds, but it reused a Matrix service row for up
to 120 seconds. The health handoff correctly admits a row for only 10 seconds.
That mismatch meant a newly placed profile could receive a stale reuse receipt
instead of a new canonical Matrix confirmation, so no valid current T0 reached
the normal recovery caller.

The bounded repair makes the fast-producer reuse interval exactly 10 seconds,
the same as the health consumer's existing live-evidence law. A result older
than that is never used to start recovery; it causes the existing exact Matrix
writer to reconfirm the affected source/service contract. The health service
also emits one startup line stating whether its existing in-process Matrix
consumer loaded successfully. No cadence, policy, target selection, Authority,
route writer or client assignment logic changed.

Focused tests prove both sides: a fresh Matrix result is reused, while an
11-second continuing result must invoke the canonical confirmation before it
can progress. A historical test expecting a shadow call after fresh reuse fails
unchanged against the pre-repair version and was not treated as evidence for
this repair.

## Follow-up: delayed profile detector after a fresh ordinary placement

The current three-user VLESS observation exposed a separate general defect.
Matrix correctly recorded a current three-member ordinary scope, but the
required-service detector's individual checks completed in roughly 2.1--2.3
seconds and then serialised their canonical confirmation.  The parent role
therefore remained active for 12--47 seconds, repeatedly missing its 3.5-second
deadline.  This can make a current Matrix binding stale before the governed
recovery handoff and is incompatible with the seven-second production limit.

The existing fast batch producer is now the Runtime command for the
`other_required` role.  It collects the current source/profile contracts into
one temporary source-aggregated workset and uses the same Matrix sentinel
owner with the existing 1-second bound.  The Matrix writer, health caller,
Planner, standing Authority, Candidate, Packet, Lease, Barrier, route writer
and S11 remain unchanged.  No client is selected or moved by this change.

Focused checks cover the new Runtime command, the one-second bounded batch
sentinel and reconfirmation of an older continuing Matrix failure.  The wider
historical scheduler suite has timing-sensitive expectations that assume the
former longer `other_required` invocation; those assertions require separate
reconciliation and are not claimed as a pass for this change.  The known
historical fresh-reuse test also remains unrelated to the new runtime command.

Next: safe-deploy this bounded detector replacement, verify the Runtime hash
and health service, then observe only the normal V7 caller.  The three VLESS
users remain untouched until that caller either creates the governed recovery
transaction or exposes one remaining generic blocker.

## Follow-up: exact health handoff survived a delayed consumer read

Live Runtime evidence after the batch deployment exposed the next causal
boundary.  The health owner accepted a fresh VLESS profile failure and passed
its exact monotonic T0 to the persistent Matrix consumer.  On the constrained
Runtime, the existing consumer reached its profile read after the normal
ten-second wall-clock freshness window and returned
`STOP_SAFE_NO_CURRENT_PROFILE_FAILURE`.  It therefore threw away the exact
fact that its own health caller had just admitted, while correctly leaving all
three ordinary users on the failed source.

The repair preserves one exact Matrix fact only for that existing in-process
transaction: if the environment contains the health owner's profile T0, an
otherwise aged row is eligible solely when its Matrix monotonic T0 is exactly
equal.  A different T0, missing T0, non-health caller, unknown state and all
ordinary historical reads still fail closed.  The binding disappears when the
existing consumer process returns; it is neither persisted nor a new state
source.  Planner, Authority, Candidate, Packet, Lease, Barrier, route writer
and S11 validation remain unchanged and independently revalidate before any
movement.

Focused tests prove both branches: the precise health handoff remains usable
after a delayed read, whereas an older record with a different T0 remains
ineligible.  The next action is publication, safe deployment and observation
of the ordinary V7 Runtime caller; no manual client recovery is permitted.

## Follow-up: current scope was not keyed to its incident during re-entry

After the exact-T0 deployment, V7 independently produced an eligible
three-user VLESS recovery obligation and planned healthy targets for all three
profiles.  The bounded executor then returned
`STOP_SAFE_CURRENT_SOURCE_SCOPE_EMPTY`: its compact L3 record still held the
old terminal `unresolved=0` count even though the current registry and Matrix
both proved three users remain on the failed source.

Cause: the profile handoff carried a compatibility list of Matrix incident
identities but omitted the single exact `source_incident_id` required by the
existing L3 re-entry owner.  That owner consequently rejected the otherwise
exact source scope rather than reopening it.  The repair supplies that field
only when the Matrix evidence has exactly one incident identity and requires
the forwarded Matrix source scope to match it exactly.  Multiple identities
remain STOP_SAFE; no target, Authority, route or user is selected here.

Focused regression now proves that the live handoff gives the existing L3
owner the exact VLESS incident identity.  After safe deployment V7, not Codex,
must reconcile the three current assignments and decide whether to execute the
already governed bounded recovery.

## Outcome: automatic ordinary recovery after the incident-bound repair

The repair was committed as `8b843851 Bind profile handoff to source incident`,
published on `Updatesystem`, and safely deployed.  The local and deployed
`v7-users-autoswitch` SHA-256 both equal
`cda852c824d77c455f1c9d105063157eb69b5efa86b9c4bef1bc1e3f9663813e`;
`v7-health.service` is active.

With no operator or Codex execution command, the normal health Runtime
received the fresh VLESS profile failure at **14:55:07.873 MSK**.  Its existing
Matrix consumer created one governed operation at **14:55:40.315 MSK** and
automatically moved all three affected ordinary identities:

| Identity | Source | Automatically selected target | Route and required-service result |
| --- | --- | --- | --- |
| `10.7.0.125` | `vless` | `awg0` | pass |
| `10.7.0.126` | `vless` | `awg0` | pass |
| `10.7.0.127` | `vless` | `awg0` | pass |

The current canonical registry confirms all three are now on `awg0`.  This is
valid functional evidence of the live V7 caller: no target was selected,
Candidate/Packet/Lease/Barrier created, or route written by Codex.

It is **not** seven-second acceptance evidence.  The observed confirmed
Matrix T0 to operation completion is about **32.4 seconds**.  The operation
feedback did not retain the original monotonic clocks, so first-observation to
S11 cannot be reconstructed honestly from this record.  The measured causal
gap is that the current hot path still performs full Planner/advisory
construction before it can turn the exact re-opened source scope into the
existing governed transaction.  The next bounded repair must remove that
full-world advisory work from the already exact current-source path while
retaining the existing Planner's current target admission, Authority,
Candidate, Packet, Lease, Barrier, route and S11 gates.

## Prepared source-target handoff: implementation awaiting live Runtime proof

The next repair is intentionally a **source-scoped Planner mode**, not a new
Planner, target registry or execution path. Once Matrix has already supplied a
fresh failed source and exact affected scope, the existing Planner now defers
ranking, trust and prediction snapshot reconstruction out of the recovery
critical path. It consumes the current Matrix-owned prepared classes only when
their declared generations still match, matches each user's required-service
class to the existing prepared target order, and applies the existing mutable
source and target checks. If preparation is missing, stale, ambiguous or a
target no longer passes a mutable check, the existing Planner performs its
normal reconstruction for that same failed source only.

Matrix remains the health owner and the existing Planner remains the selection
owner. Authority, Candidate, Packet, Lease, Barrier, `v7-user-switch`, route
verification and required-service S11 remain mandatory. This change has no
user movement by itself and does not make advisory data an Apply exemption.

Focused tests cover prepared target reuse, stale-preparation fallback, exact
scope re-entry and Matrix handoff. The first pre-deploy gate correctly stayed
`NO-GO` while the workspace was dirty; its GitHub read was temporarily
unavailable, so no deployment claim is made from it. Next: commit and publish,
re-run the safe-deploy gate, deploy only if its GitHub and Runtime checks pass,
then obtain a fresh normal V7 recovery event. That event must retain monotonic
clocks from first observation through S11 before the seven-second objective
can be assessed.

### Deployment result

Commit `3520eaaa046e38774720df0511ce3cfe5d03d82d` passed the safe-deploy
GitHub and local truth gates, was deployed through `tools/v7-safe-deploy`, and
restarted the existing health service. The local and deployed
`v7-users-autoswitch` SHA-256 are both
`3371e45c3db1594c81e555f4597549d903715c2e3c433dc2f7ff7c22fb561a81`.
`v7-health.service` is `active` and `enabled`. No client assignment or route
was changed during deployment. The next valid evidence must come from the
normal V7 health caller after a fresh current bad-placement or source-failure
event; Codex must only observe it.

### Current live-evidence boundary

After deployment, Matrix has no active ordinary failed-source scope. VLESS has
one registry row (`10.7.0.7`), but that row is disabled and has no
service-preferences profile, so it is not a lawful ordinary recovery subject.
The remaining active Matrix failure belongs only to a certification source and
is deliberately excluded from ordinary recovery. No route was changed during
this inspection. A seven-second ordinary result therefore cannot be claimed
until the live Runtime receives a newly current affected ordinary scope.

## Live ordinary recovery correction: immutable Packet binding survived the final Apply boundary

### Observed live Runtime evidence

On 2026-08-31 an operator placed ordinary identity `10.7.0.125` onto `vless`.
This was an operator input, not a Codex route mutation.  The normal
`v7-health.service` then independently consumed a fresh Matrix failure:

- Matrix T0: `2026-08-31T15:50:30.702548+00:00`;
- one ordinary affected identity on `vless`;
- existing Planner selected `awg3`;
- the normal V7 caller created Candidate, Packet
  `pkt_ff31e038914e613b7717c59d`, Lease and Barrier;
- the Packet held the exact ordinary-service-failure binding for the current
  source incident and one-member scope.

No route was changed because the final executor returned
`l3_execution_eligibility_stop_safe`.  Its generic L3 incident projection was
empty even though the immutable Packet and current Matrix proved the ordinary
profile-service failure.  This was a false rejection at the final process
boundary, not an unsafe target, missing Authority or a failed service gate.

### Repair

`v7-users-autoswitch` now restores the transient ordinary-failure context only
from an immutable Packet that proves all of the following: the exact binding
kind, source incident and event identities, ordinary-only scope, non-empty
affected count, and a non-empty set of moves from that exact failed source to
distinct targets.  The marker is recovered before broad state reconstruction
and recorded in the revalidated plan.  It creates no owner, state source,
target or Authority.  The existing Matrix, registry, current target,
Authority, Lease, Barrier, execution control, route writer and required-service
S11 checks remain mandatory.

Focused tests passed for loss of the transient marker, immutable Packet
rehydration without replanning, target-loss STOP_SAFE behaviour and caller flag
forwarding.  The broader role and episode suites ran 160 relevant tests
successfully; one existing source-format assertion failed because it expects a
single-line source-code call that was already formatted across lines before
this repair.  It does not exercise or fail runtime behaviour.

The first observed event remains a failed seven-second acceptance attempt:
V7 detected and prepared recovery but did not route the user because of this
now-repaired defect.  After safe deployment, the live V7 caller—not Codex—must
consume the still-current Matrix scope.  The resulting route and S11 evidence
will be recorded separately, with no retroactive seven-second claim.
