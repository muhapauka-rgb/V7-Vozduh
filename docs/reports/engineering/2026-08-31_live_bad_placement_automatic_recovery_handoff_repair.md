# Live bad-placement automatic recovery handoff repair

## Scope

This report covers the ordinary VLESS profile-failure event observed on
2026-08-30/31 and one bounded repair to the existing V7 health caller.  It
does not credit a performance SLO and it does not record a Codex-operated
client move.

## Fresh production evidence before the repair

The Matrix owned fresh failure evidence for VLESS and three assigned ordinary
identities.  The source had a failed required-service set while the current
registry scope was `10.7.0.125`, `10.7.0.126` and `10.7.0.127`.

The normal V7 Runtime, not Codex, then completed one governed transaction to
`awg0`.  The registry and three assignment files showed `current=awg0` after
the transaction.  The route/history records attribute the action to
`autoswitch_failover` and `runtime_autoswitch_cac8c1761be250ed5a57f1cf`.

Observed timestamps from the existing Matrix, lease and switch-history
owners:

| Boundary | UTC time | Elapsed from Matrix T0 |
| --- | --- | ---: |
| Matrix T0 for the continuing VLESS failure | 21:20:24.026 | 0 ms |
| Canonical VLESS Matrix write completed | 21:20:56.150 | 32.124 s |
| Packet created | 21:21:09.988 | 45.962 s |
| Lease created | 21:21:10.182 | 46.156 s |
| First assignment committed | 21:21:12.643 | 48.617 s |
| Third assignment committed | 21:21:13.798 | 49.772 s |
| Existing execution receipt completed | 21:21:33.594 | 69.568 s |

The action was functionally successful, but it failed the binding seven-second
ordinary-recovery target.  It is retained as failure evidence, not hidden or
cherry-picked.

## Root cause

`other_required` runs the existing source-profile detector.  In its batch
mode, it waited for the whole set of unrelated source probes to finish before
the health loop examined the already-written Matrix result.  The health loop
therefore delayed its existing persistent Matrix consumer even after an exact
source/profile T0 existed.  The direct child and the older standalone unit
state were not used as a substitute caller; the normal health Runtime is the
relevant caller.

## Repair

`tools/runtime-support/v7-health-loop` now uses its existing parallel
source-scoped detector path.  A completed source probe can publish the
canonical Matrix result without waiting for unrelated sources.

While that detector is still running, the existing health loop now performs a
read-only check of the same canonical Matrix and current registry.  Only when
it finds a *new*, fresh, exact profile failure identity does it stop the
detector's remaining unrelated probes and invoke its already-existing
persistent Matrix consumer.  Matrix remains the sole writer; Planner,
Authority, Candidate, Packet, Lease, Barrier, route writer and required
service verification are unchanged.  A stale or previously consumed Matrix
identity does not interrupt the detector.

## Verification before deployment

- `tests.unit.test_v7_health_fast_deadline_loop`: 26 PASS.
- `tests.unit.test_v7_egress_diagnose`: 35 PASS.
- `tests.unit.test_v5_3_role_based_recovery`: 22 PASS.
- Python compilation and diff whitespace check: PASS.

The new focused health-loop test proves that a running detector with a newly
published Matrix T0 is preempted and handed to the existing persistent
consumer.  It does not create a client, incident, Candidate, Packet, Lease,
Barrier or route.

## Required post-deploy evidence

After safe deployment, verify source/tree/runtime hash alignment and that
`v7-health.service` is active.  A subsequent fresh current V7 failure may
only be credited when its full chain originates from the ordinary health
Runtime and records first valid observation, Matrix T0, governed action,
member S11 and all-affected completion.  No manual customer switch may supply
that credit.

## Deployment and immediate Runtime verification

The repair was committed as `093fcdcb6abc4230717af8d49436fef62432889a`,
published to `Updatesystem`, and deployed by the existing safe-deploy owner as
`deploy-z8-14-Updatesystem-093fcdc-20260831T003256`.

The deployment gate reported GitHub alignment and no blockers.  The deployed
`/usr/local/bin/v7-health-loop` SHA-256 is
`486a6af86a91f1bd66dc8131cc1fe0744e2b226450e71af41416d86b91525071`,
matching the approved local binary.  `v7-health.service` restarted normally
and is active.  No standalone Matrix or Telegram timer is installed.

The three users from the pre-repair VLESS event remain on `awg0`; the deploy
did not create or manually advance any new user operation.  There is no fresh
ordinary failed-source event after deployment yet, so a seven-second result is
not claimed.  The next new current Matrix failure must be observed through the
normal V7 caller and retained in the full distribution whether it passes or
fails.

The first post-restart normal detector observation had three active sources,
six profile contracts and three source-scoped observations.  Its first result
was 1.826 s, P95 was 1.979 s and the maximum was 1.979 s.  This confirms the
new streaming detector is active under the existing caller; it is not a
failure/recovery sample and does not establish the seven-second SLO.

## Controlled-polygon readiness reconciliation

The existing controlled-certification preflight was run read-only after the
deployment.  It made no routing, client, Authority or state change.  It
returned `STOP_SAFE`: its old one-use certification Authority and exact
identity/source context are terminal or stale.  In particular, the preflight
could not derive one unique certification identity on a distinct restorable
controlled source, and it correctly rejected the expired/used Authority
request rather than reusing it.

This is not an ordinary-recovery defect and it does not invalidate the live
three-user automatic recovery evidence.  It means that a new isolated Polygon
sample cannot honestly be started until the existing certification lifecycle
owner has created a new exact one-user context and a new one-use Authority
contract.  Codex did not choose a source or target, move a user, inject a
failure, or manually call the ordinary recovery consumer.

The live Runtime remains healthy (`v7-health.service` active since
2026-08-31 00:33:07 MSK).  Local-to-Runtime deployment alignment is proven;
independent GitHub revalidation remains unavailable from this environment
because `v7-truth-check` reports the remote as unreadable.  The precise next
step is therefore: use the existing certification lifecycle to establish a
fresh, owner-selected one-user Polygon context, then let the normal health
caller observe its controlled Matrix failure.  That controlled result may
validate the handoff repair, but it cannot replace a fresh ordinary-production
seven-second sample.

## Repeated live measurement after deployment

A new ordinary VLESS event was observed after deployment; no action was
started by Codex.  The three ordinary identities were already on VLESS through
operator-originated profile rebinds.  The normal health Runtime then produced
a new owner-backed correlated required-service failure for that current scope.

The detector began at monotonic time `10054111500290338`.  Matrix confirmed
the profile failure at `10054116135418789`, a 4.635 s source-scoped probe
interval.  The health Runtime preempted the remaining unrelated detector work
at the recorded 4.722 s duration.  Therefore the Matrix-to-consumer handoff
was approximately 87 ms, rather than the old full-batch wait.

This validates the narrow handoff repair, but the full recovery result is a
failure: the same fresh event was classified `capture_only` with
`candidate_or_execution_forbidden=true`.  The existing consumer therefore
created no Candidate, Packet or Lease and performed no Apply.  More than
thirty seconds after Matrix T0, all three identities were still on VLESS.

The seven-second ordinary recovery target is consequently still **not met**.
The dominant remaining blocker is now exact and separate from detection:
the existing live-health event is incorrectly ineligible for the existing
ordinary recovery Authority/Planner path despite its current ordinary scope.
The next engineering action is to repair that generic admission classification
through its existing owner, then observe a new live V7-originated event end to
end.  No historical event, target or user assignment may be reused to claim
the result.

The repeated owner records make the failure point specific.  The Planner did
derive two bounded classes and healthy target contracts for all three users,
but marked both `execution_allowed=false`.  The live service-failure advisory
then found `no_open_unmaterialized_passive_terminal`: its current-source
incident could not be matched to any of 63 retained passive projection rows.
Consequently the existing bounded-delegated action owner returned
`STOP_SAFE_NO_CURRENT_SERVICE_FAILURE_OBLIGATION`; no Candidate, Packet,
Lease or Apply was created.  This is the generic current-incident binding
defect to repair.  It is not a target-capacity, routing, Matrix-write or
detector-handoff failure.

## Current-incident admission repair

The second reconciliation isolated the defective condition.  A fresh,
source-bound profile Matrix observation was deliberately allowed to defer the
existing passive/L3 consumer even when no exact current L3 obligation existed.
That made the following sequence impossible:

```text
fresh Matrix event -> existing passive/L3 projection -> existing advisory
-> existing governed executor
```

Both later readers then failed closed, correctly, because neither a current
projection nor an obligation had been materialized.  Historical passive rows
were not used as a substitute.

The repair is limited to the existing Matrix scheduler.  It now defers the
passive/L3 consumer for a runtime profile event **only when** the exact current
L3 obligation is already durable.  For a newly observed exact event it first
uses the existing passive/L3 consumer, then the existing advisory and governed
execution owners.  It creates no new state owner, Planner, Authority, route
writer, queue, timer or target-selection path.

Focused validation passed:

- the new scheduling predicate accepts deferral only with an exact current L3
  handoff;
- the same fresh profile event without that handoff proceeds to existing
  passive/L3 materialization;
- the current-profile event admission regression remains green;
- `git diff --check` passed.

This change has not yet been deployed at the time of this report update.  The
next step is safe deployment, alignment verification, then passive observation
of the normal V7 Runtime handling the already-current VLESS failure.  Codex
will not manually advance its transaction or move any user.

## Continuing-incident reconciliation repair

The first deployed scheduling correction exposed one further generic condition:
the existing passive/L3 consumer successfully created the current VLESS
closure, but its work took longer than the advisory's ten-second freshness
window.  The advisory then discarded the same still-open Matrix incident as
if it were historical, even though the Matrix continued to show that the
remaining ordinary user required failed VLESS services and the closure carried
the same source incident and current one-user scope.

The second repair does not relax source or service safety.  When the narrow
ten-second observation window has elapsed during that existing owner work, the
same advisory may continue only if the **current Matrix** still confirms an
explicitly required failed service for a user still assigned to that exact
source.  It remains bound to the current incident and compact scope; the
existing Authority, Planner target selection, Packet, Lease, Barrier, Apply
and S11 checks are unchanged.  No old closure can qualify without a matching
current Matrix incident.

Three focused regressions pass, including the strict fresh-binding case, the
continuing-current-Matrix case, and the profile-event admission case.  This
second repair is pending safe deployment and normal Runtime observation.

## Deployed continuing-incident result and Packet-to-Apply repair

The continuing-incident repair was committed as
`d265e5c9f005098dcbacfa146873c90bfa3da61f` and safely deployed as
`deploy-z8-14-Updatesystem-d265e5c-20260831T010249`.  Local, GitHub and
Runtime copies of `v7-users-autoswitch` were then verified to have the same
SHA-256 (`b1f22fbeb9a7165bb9e15e3b3f751264d09c0b4f2dcb62fe112df8ad02ba9d43`);
`v7-health.service` remained active.

The next normal V7 cycle proved the repair reached its intended consumer:
Matrix kept the same current VLESS incident and one-user ordinary scope,
the passive/L3 owner completed, the advisory created a one-user obligation,
and the governed executor began an automatic transaction.  Codex did not
select a target, create an incident, or invoke a route mutation.

That transaction stopped safely before Apply.  Its exact child diagnosis was
`l3_execution_eligibility_stop_safe` with the apparent blockers
`fresh_profile_or_channel_failure_evidence_required`,
`required_service_failure_required`, and `safe_target_required`.  This was
not a real loss of the Matrix fact: the parent had already validated the
current Matrix incident, source scope, Candidate and target before creating
the Packet.  The independent route-writer recheck then tried to reconstruct
the fact solely from a lossy per-service Matrix row, which does not retain
the event identity used by the parent.  The immutable Packet did not carry
that compact causal binding into its approved lock, so the route writer could
not independently reconcile it and correctly stopped.

The current bounded repair preserves the existing owners and the fail-closed
law:

```text
Matrix current event
-> existing obligation binding revalidated by governed executor
-> immutable Packet + approved Packet lock
-> route writer re-reads lock, current Matrix and canonical event ledger
-> Apply only when all identities still match
```

It adds neither a new health truth source nor an alternate route writer.  The
Packet lock now carries only compact incident/event/scope identity (never raw
user lists); the route writer accepts it only for its exact locked
user/source/target and only while both the event ledger and current Matrix
still prove a failed required service.  A changed scope, source, target,
event, stale event or recovered Matrix remains a safe refusal.

Focused verification for the repair passed: five focused regression tests
cover Packet-lock propagation, current Matrix/event revalidation, strict
fresh handoff, continuing incident admission and existing tier-4 binding.
`git diff --check` passed.

## Packet-to-Apply repair deployment and repeated measurement status

The bounded repair was committed as
`2f4cc76dd427ed81a61c3eff58e1cb9690fc5c40`, published to `Updatesystem`,
and deployed through `tools/v7-safe-deploy` as
`deploy-z8-14-Updatesystem-2f4cc76-20260831T011648`.

The deployment gate had no blockers.  The exact deployed SHA-256 values match
the published sources for all three changed Runtime members:

- `v7-users-autoswitch` — `5c60f8238473da1e67b89a7ed06e9ca1349a9bc1e10a758383b5ee07d4da2f79`;
- `v7-governed-canary-dry-run-cycle` — `271eb43f781e0cbbaf20011e11e126b3e37837a160994ba6d8740d93f330951f`;
- `admin_core/operator_execution.py` — `6847a9e3b8a39fd351168e0ae4df72c005a5ce10104d8a70ff0f6a4e7ef75227`.

`v7-health.service` and `v7-admin-api.service` are active.  The repair keeps
the existing route writer as the only writer: it can now consume an immutable,
compact Packet binding only after it independently confirms the same current
Matrix failure and canonical event.  A changed source, changed scope, stale
event, recovered Matrix row, or absent required-service failure still blocks
the route mutation.

The requested repeated live measurement cannot truthfully be credited yet.
At the observation time, the only `users.registry` entry still on VLESS was
disabled (`10.7.0.7`); every active ordinary user had already left the source.
The current Matrix summary therefore reports
`STOP_SAFE_NO_CURRENT_SERVICE_FAILURE_OBLIGATION`, which is the correct
non-action result.  Codex did not manufacture a failure or move an ordinary
user to obtain a measurement.

The exact next step is a new real operator-originated incompatible placement
of an enabled ordinary user.  The unmodified V7 Runtime must then originate
the whole chain (fresh Matrix T0 -> obligation -> Packet/Lease/Barrier ->
Apply -> required-service S11).  Its full timing distribution, including any
result above seven seconds, must be retained before the seven-second target
can be claimed.

## Correction: full observed operator-to-recovery latency

The earlier `69.568 s` figure was an internal interval from a later Matrix T0
in a different VLESS episode.  It was not the requested end-to-end time from
the operator's incompatible placement.  It must not be used as the ordinary
recovery result.

For the last three-user live placement, the canonical switch history records:

| User | Operator placed on VLESS (UTC) | V7 automatic return (UTC) | Full observed delay |
| --- | --- | --- | ---: |
| `10.7.0.125` | 21:43:29.384 | 21:51:37.969 | 488.585 s (8m 08.585s) |
| `10.7.0.126` | 21:43:37.446 | 21:51:38.943 | 481.497 s (8m 01.497s) |
| `10.7.0.127` | 21:43:41.366 | 21:51:39.847 | 478.482 s (7m 58.482s) |

The first relevant Matrix observation was at `21:45:22.262 UTC`, around
1m 41s to 1m 53s after placement.  The first actual automatic route change
then happened 6m 15.707s after that observation.  Until that point, the
passive consumer repeatedly recorded `STOP_SAFE_NO_ACTION` with the reason
that a current Authority/Packet could not be reused.  Only later did the
separate governed automatic transaction apply the recovery.

Therefore the current full-path result is **about eight minutes**, not seven
seconds and not 69 seconds.  It is an SLO failure.  The next repair must treat
both the delayed first Matrix observation and the multi-minute
Matrix-to-governed-execution gap as one end-to-end latency defect, while
retaining normal V7-originated operation and all safety checks.

## Eight-minute causal repair: first bounded Runtime correction

The initial diagnosis disproved the idea of a single slow timer.  During the
same production window, source-health roles configured for one-to-five-second
cadence repeatedly ran for roughly 31--65 seconds and missed their next
deadlines.  The first raw VLESS failure appeared about 33 seconds after the
first incompatible placement, while the exact profile-relevant source scope
was not available until later.  The record also shows repeated capture-only
`STOP_SAFE_NO_ACTION` outcomes before the governed transaction finally ran.

One avoidable synchronous cost was proven in the ordinary path: every ordinary
failure was first running the certification-only target-selection diagnostic.
That diagnostic reconstructs a broad controlled-test target view, is not a
safety condition for an ordinary customer recovery, and was observed consuming
almost a full CPU core alongside the health loop.  The current correction:

- skips that diagnostic only for a source scope explicitly classified as
  ordinary-only with zero certification members;
- leaves its existing execution intact for every controlled/certification or
  ambiguous scope;
- lets the existing advisory owner materialize one exact current profile
  obligation before capture-only passive history, but only when source,
  incident and affected-scope fingerprints all match the fresh Matrix binding;
- keeps Candidate, Packet, Lease, Barrier, Apply, route verification and S11
  with their existing governed owners; and
- keeps the former capture-first flow whenever the bounded advisory cannot
  return a matching obligation inside five seconds.

This is a generic Runtime repair, not a Codex-operated recovery.  It does not
choose a user or target, create an incident, mutate a registry, or invoke the
route writer.  Five focused regressions pass, including ordinary diagnostic
exclusion, exact fresh-profile handoff ordering, direct-L3 ordering, and the
existing passive-deferral guard.  Syntax and whitespace checks also pass.

At this checkpoint the repair is **not yet deployed and the seven-second SLO
is not claimed**.  The next action is safe deployment followed by observation
of the normal V7 caller on current owner-backed state.  The full historic test
module was also sampled but has pre-existing independent failures; it is not
being represented as verification of this repair.

## Post-deploy observation: scheduler read-amplification repair

The first correction was committed as `daf1b02eb7f55b94c2654e647e365d37a19b29c8`,
published to `Updatesystem`, and safely deployed.  The safe-deploy gate passed;
the deployed Matrix executable SHA-256 is
`6fc783133e52d18e6a357c16b10f4f4e35996a887aa7ac1505a4691c0c97a057`,
matching the published source.  `v7-health.service` is active after its
required governed restart.

Fresh Runtime observation exposed a second direct cause.  While a single
`other_required` detector process was running, the health parent was parsing
the full Matrix and users registry every 25 ms to discover a newly written
profile binding.  On the two-vCPU server, that parent consumed roughly one
third of a CPU core at the same time as the detector and the Admin process.
The ordinary detector completed in 18--32 seconds despite its five-second
cadence; Telegram, HARD and target roles also missed their one-second
deadlines.  This is an implementation scheduling defect, not a safe reason
to delay a customer.

The next bounded correction keeps the same health loop and the same Matrix
reader, but limits that *in-memory polling decision* to once per 250 ms while
the child is live.  It adds at most 250 ms to discovering a current Matrix T0,
is not persisted, and does not change Matrix, Authority, Planner, routing or
S11 semantics.  A focused regression proves that the first fresh binding is
still handed to the existing consumer while repeated 25 ms parent ticks no
longer continuously re-read the full registry.  This second correction awaits
its own safe deployment and Runtime measurement; the seven-second target is
still unproven.
