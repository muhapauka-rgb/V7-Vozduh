# V7 Live Profile Recovery: Fast-Producer Contention Repair

Date: 2026-08-30 (MSK)  
Scope: ordinary live recovery only; no user was moved by Codex.

## Trigger and observed behaviour

The operator manually placed two ordinary identities (Lisa `10.7.0.125` and
Chuck `10.7.0.126`) on VLESS while their required-service contracts could not
be satisfied there.  This is valid live acceptance input.  The V7 Runtime,
not Codex, automatically moved Lisa from VLESS to `awg0` at
`2026-08-29T22:15:45.193744+00:00` with reason
`autoswitch_governed_canary`.  Chuck remained on VLESS while the detector
became delayed.

## Root cause

The `other_required` five-second health role launched 128 simultaneous
one-second network checks on a 2-vCPU Runtime.  Fresh Runtime evidence showed
mass timeout bursts for healthy source and target contracts and role durations
of roughly 94 s and 139 s.  The same role then launched ordinary-duration
Matrix shadow confirmations, making a seven-second recovery physically
impossible.  This is a generic producer scheduling defect, not a Chuck-specific
exception and not a target-selection decision.

## Repair

1. Bound the existing batch producer to eight concurrent checks.
2. Keep the existing Matrix as the independent failure owner, but run an exact
   source/profile shadow confirmation with its supported one-second fast
   verifier.  Timeout or unknown remains fail-closed: it creates no recovery
   admission.
3. Do not change the Planner, Authority, route writer, user registry,
   service contract, Matrix owner, cadence, or target-selection rules.

## Second live finding and repair

After the first repair reached Runtime, the ordinary Matrix consumer correctly
identified VLESS as failed, found Chuck as its sole affected ordinary user,
and derived owner-selected healthy candidates.  It still stopped because all
pre-warmed targets had been marked not ready.  Runtime process evidence showed
that the advisory target-prewarming role expanded an empty/narrow profile into
the whole current Matrix inventory (13 non-Telegram services) and ran it with
16-way target fan-out every five seconds.  This competed with the live
detector and caused target timeout observations.

The second repair keeps that advisory role within its declared selected-profile
services only and caps its target fan-out at two.  Empty prepared contracts no
longer trigger an all-service probe.  Exact live target validation before
governed apply remains mandatory and is unchanged.

## Verification before deploy

- First repair: 77 focused checks PASS.
- Second repair: 61 focused checks PASS (`pre-ready`, health deadline, and
  role-based recovery suites).

## Live acceptance status

The repair is not credited as success merely from tests.  After safe deploy,
control returns to the normal V7 health caller.  The required evidence is a
fresh VLESS source failure followed by automatic affected-scope discovery,
Authority, Planner target choice, governed route apply, and exact required
service S11 for both current ordinary identities.  No manual operational
transition is permitted.  The measured first-valid-observation to
all-affected-recovered interval must be at most seven seconds; over eight
seconds is a failure.

## Third live finding and repair

The fresh VLESS Matrix contains exact failure events for services required by
Chuck's profile, including a confirmed `youtube` timeout. The ordinary
governed path nevertheless treated the source as eligible until the generic
three-sample/persistence classifier completed. Its prior executor attempts
therefore stopped with `fresh_profile_or_channel_failure_evidence_required`.
This contradicts the product law for a fresh, unambiguous failure of a
profile-required service.

The repair does not make normal placement react to one uncertain probe. Only
the existing ordinary service-failure path may use a Matrix row when all of
the following are true: the service belongs to the user's declared profile,
the row is currently failed, it has an `OBSERVED_*` state, an incident and
event identity, a confirmed monotonic failure timestamp, and is no more than
ten seconds old. That exact Matrix fact makes only the current source
ineligible for this recovery transaction; Planner still selects the target,
and Candidate/Packet/Lease/Barrier/Apply/S11 retain their existing gates.

The source-bounded read-only advisory now explicitly enters that same ordinary
recovery context. Without a fresh exact Matrix fact it produces no move.

## Verification for the third repair

- New regression: a fresh single Matrix MODE_A event for a profile-required
  service creates an ordinary failover candidate.
- Existing regression: an ordinary single ambiguous failure remains degraded
  and does not create a failover.
- Existing persistent-profile failure behavior remains unchanged.
- Full focused policy suite: 223 PASS.
- A broader combined run exposed only unrelated environment/history failures:
  one sandbox-disallowed local HTTP bind and two fixtures with already-expired
  standing contracts. They are not treated as regressions of this repair.

## Current live state before deploy

V7 has not moved Chuck by Codex action. Chuck remains assigned to VLESS;
Lisa remains on `awg0` after the earlier V7-initiated recovery. The current
Matrix reports one ordinary VLESS affected scope and a fresh failed required
service. The prior health role spent 49–60 seconds in repeated governed
attempts, so that observation is a failed SLO sample, not success evidence.

## Exact next step

Publish and safely deploy this third generic repair, then return control to
the live V7 health caller. Observe whether V7 itself creates a fresh
source-bounded recovery transaction, selects a ready target, and reaches
required-service S11 inside the seven-second contract. No manual client or
route action is allowed.

## Fourth live finding and repair

The next live observation showed a separate scheduling defect: the health
loop's `other_required` consumer joined every historical `OBSERVED_*` Matrix
row to the current user registry, without checking its wall-clock freshness.
Those old rows repeatedly launched the existing governed executor and held the
five-second service role for 54--57 seconds. This is invalid recovery work and
can delay a genuinely fresh profile failure.

The repair keeps historical Matrix evidence intact but excludes rows older
than ten seconds from the *live handoff only*. The ten-second bound is already
the Planner's required-service freshness bound. Legacy isolated fixtures with
no ISO wall-clock timestamp retain their existing behavior; production Matrix
rows always carry that timestamp. No user, source, target, Authority, Planner,
route writer, timer, or Matrix state was changed.

## Verification for the fourth repair

- New regression: a stale production Matrix row is ignored while a concurrent
  fresh exact failure is handed to the existing live consumer.
- Health-loop focused suite and the autoswitch policy suite pass after the
  change.

## Live observation after the user-operated assignment test

At `2026-08-30T02:02+03:00`, the current assignments were Lisa on `awg0`,
Chuck on `vless`, and Chuck2 on `wireguard-1779454504-c43409`. Chuck's declared
profile is `google`, `google_auth`, `instagram`, `telegram`, and `youtube`.
The latest bounded profile-probe batch reported no current failed service for
that VLESS profile. A nearly contemporaneous Matrix row recorded an Instagram
timeout, so the two observations are inconsistent rather than a safe recovery
fact. The system must not move a customer on the stale/contradictory row; a
new exact Matrix confirmation is required. This is not credited as a recovery
success or failure sample.

## Exact next step (updated)

Publish and safely deploy the fourth generic repair. The normal health caller
then remains the sole source of action. On the next fresh, unambiguous
profile-required service failure for either user-operated assignment, it must
discover the affected scope, choose the target itself, apply the governed
change, and produce exact required-service S11 within seven seconds. Any
longer automatic attempt remains visible as a failed SLO sample.

## Fifth live finding and repair

The first live post-deploy transaction exposed a causality mismatch, not a
route decision defect. The fresh VLESS Matrix failure was correctly detected,
and the source-bounded advisory completed in about two seconds. However its
passive-history selector bound the governed executor to an older VLESS
incident from the same channel. That old incident had no valid prepared
handoff, so the executor rebuilt the full Planner for about 30 seconds. The
result was a 61.437 s `other_required` run and is an explicit failed SLO
sample.

The repair adds no state or owner. For a source-bound ordinary health wake,
the existing passive-history selection may now use only a closure whose
incident identity is also present in a fresh, profile-required Matrix failure
for a user currently assigned to that source. An older incident on the same
channel is ignored. Historical ranking remains available unchanged for
non-live Engineering projections.

## Verification for the fifth repair

- New regression: a current Matrix incident and an older incident on the same
  source yield only the current identity for a live recovery handoff.
- Existing profile-failure priority behavior remains unchanged.
- Autoswitch policy and health-loop regression suites pass together with the
  new focused test.

## Exact next step (updated again)

Publish and deploy the source-incident binding repair. V7 then owns the next
step completely: a new fresh profile failure must bind to its matching current
incident, use the prepared decision when valid, and either reach required
service S11 within seven seconds or emit an honest STOP_SAFE/SLO failure. No
manual route operation is permitted.

## Sixth live finding and repair

The user-operated assignment check then revealed the remaining blocker. The
current Matrix and current users.registry correctly described VLESS (Chuck)
and awg0 (Lisa) as profile-impacting, source-bound failures. Yet the passive
consumer admitted only generic failures after three samples or 180 seconds.
It therefore returned `no_passive_capture_event` for a fresh one-sample
profile failure and never created the existing durable incident projection or
its downstream recovery obligation. This was an incorrect generic delay on
the ordinary recovery hot path, not a missing target or a reason to move a
client manually.

The repair leaves generic failure persistence unchanged. It admits a first
sample only when all of the following existing facts agree at consumption
time: the event is external Matrix evidence, the same exact source incident
is still present in current Matrix, one currently assigned ordinary user's
declared required service is failed, and the Matrix observation is no more
than ten seconds old. A stale event, a recovered service, a changed incident,
an unrelated service, a certification identity, or ambiguous evidence remains
ineligible and cannot produce a recovery action.

## Verification for the sixth repair

- New regression: a one-sample current Matrix failure for a currently
  assigned user's required service is admitted to the existing passive/L3
  consumer.
- New regression: an otherwise identical historical incident is rejected.
- Existing generic transient-versus-persistent behavior and exact-Matrix
  profile recovery behavior still pass.

## Exact next step (current)

Publish and safely deploy this generic consumer repair. Then return control
only to the normal `v7-health.service` caller. It must itself turn a newly
fresh profile-required failure into Matrix -> affected scope -> Authority ->
Planner target selection -> governed Apply -> required-service S11. The two
user-operated placements remain valid real-world checks, but no successful
automatic movement or seven-second timing claim is made until that live chain
has actually completed.

## Seventh live finding and repair

After the sixth repair was deployed, the Matrix emitted fresh exact VLESS
profile-failure events for the currently assigned ordinary client, but the
passive consumer still did not create an obligation. The remaining mismatch
was inside the existing Planner intake: Matrix resolves the affected source
against canonical `users.registry`, while this source-bound ordinary recovery
path still overlaid the lagging diagnostic `v7-state` user projection. A
recent operator assignment could therefore disappear only for the consumer
which must react to it.

The bounded repair makes a source-bound ordinary service-failure transaction
read the same canonical current user registry as Matrix and the existing
pre-Apply verifier. It does not affect broad planning, target eligibility,
Matrix, Authority, routing, cadence, or user records. This removes one
contradictory current-state view; V7 remains the sole originator of any
recovery operation.

## Verification for the seventh repair

- New regression: an ordinary source-bound failure uses the current registry
  assignment even when the diagnostic state projection still names a previous
  channel.
- Existing exact certification incident behavior retains the same registry
  truth rule.

## Exact next step (current)

Safely deploy this reconciliation. The normal health caller must then either
create a governed recovery from the fresh VLESS profile incident, or expose a
new exact safety stop. No client is moved by Engineering; the first automatic
operation and its T0-to-S11 timing are the acceptance evidence.

## Eighth live finding and repair

The seventh repair aligned the Planner with the registry, but live tracing
showed an earlier issue in the passive Matrix consumer. Its intentionally
small entrypoint skipped the full Planner constructor, yet it also skipped
loading the current ordinary assignments and service preferences. The
first-sample exact-profile predicate consequently evaluated every Matrix event
against an empty user/profile set and fell back to the generic three-sample or
180-second delay.

The passive entrypoint now reads only the canonical inputs required by that
predicate: `users.registry`, `service-matrix.json`, and
`service-preferences.json`. It still cannot plan, issue Authority, create a
Candidate/Packet/Lease, alter routes, or move users. This gives the existing
live runtime enough current truth to create the established bounded recovery
handoff when Matrix records a fresh required-service failure.

## Verification for the eighth repair

- New regression: one fresh Matrix failure of a service required by a current
  ordinary user is consumed by the passive owner despite only one sample.
- Existing capture-only no-route behavior remains unchanged.
- Existing current-registry and exact-incident tests remain green.

## Exact next step (current)

Deploy this repair and return to the normal health caller. The next fresh
Matrix confirmation of either user-operated incompatible placement must be
captured immediately by the existing automatic chain; its own governed
executor, not Engineering, must select and apply any safe replacement.
