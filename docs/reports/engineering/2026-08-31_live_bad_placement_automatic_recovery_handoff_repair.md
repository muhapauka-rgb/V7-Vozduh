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
