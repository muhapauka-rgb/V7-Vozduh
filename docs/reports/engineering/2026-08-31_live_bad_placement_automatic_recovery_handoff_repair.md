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
