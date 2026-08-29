# V7 Chuck2 live profile-failure priority repair

## Objective

Observe the real, operator-induced Chuck2 assignment to `vless` and repair a
generic V7 defect only if the live Runtime did not automatically select a
healthy channel for the profile's required services.  Codex must not move
Chuck2, select a target, create an operation, or invoke a recovery command.

## Current evidence

Fresh Matrix observation showed `vless` with an active `google` failure for
its current source incident.  Chuck2 (`10.7.0.127`) is assigned to `vless` and
has Google in the profile service contract.  Other legacy sources also have
open failures.  The existing Matrix/Planner path was repeatedly consuming an
older broad-source obligation before the newer profile-relevant VLESS failure.

## Root cause

The existing advisory selector ranked current open incidents by unresolved
scope, observation time and cohort size.  It had no explicit profile-impact
priority when several sources were simultaneously open.  A broad continuing
incident could therefore occupy the one bounded automatic transaction while a
newer failed service required by an assigned user waited behind it.

## Repair

`tools/v7-users-autoswitch` now derives a read-only priority from the existing
Matrix, users registry and service preferences.  It ranks an open source ahead
of another only when it currently impacts an ordinary user's declared required
service; ties use the exact newest Matrix failure monotonic timestamp.  The
existing Planner, Authority, Candidate, Packet, Lease, Barrier, route writer
and S11 owners are unchanged.  No state source, timer, queue, target or manual
recovery path was added.

## Verification

- Syntax compilation: PASS.
- Focused priority test: PASS; a newer VLESS Google failure required by a
  current profile outranks an older AWG0 Telegram failure.
- Existing current-source scope test: PASS.
- A wider historical test collection contains pre-existing fixture failures
  where a deliberately partially constructed Planner has no Matrix attribute;
  those fail before this priority helper is reached and do not justify hiding
  or changing the new Runtime behavior.

## Live Runtime result before the latency repair

The first repair was deployed as `54606ff5`.  The live Runtime—not Codex—then
selected `wireguard-1779454504-c43409` for Chuck2 and completed the governed
transaction.  The durable receipt records one user moved, terminal `SUCCESS`,
and the required Google, Google Auth, Instagram and Telegram checks passed.

This is valid functional recovery evidence, but it is not latency acceptance:
the current VLESS revalidation was observed at `2026-08-29T21:06:47Z`, the
governed action began at `21:09:13Z`, and required-service closure completed
at `21:09:17Z`—about 150 seconds.  The 7-second law therefore remains unmet.

## Residual root cause and second repair

The governed route/apply portion was approximately four seconds.  The dominant
delay was the pre-action all-user advisory rebuild: the live receipt exposes
`prepared_validation_ms = 37931.327`, 129 planner rows scanned, and a stale
prepared projection caused a full Planner fallback.  Multiple unrelated failed
sources also prevented the direct source-specific handoff from being used.

`tools/v7-service-matrix-refresh-all` now performs only a read-only selection
among already Matrix-failed sources: it chooses a source only when its current
failed service affects declared services of ordinary users, preferring the
newest exact failure evidence; an equal tie remains STOP_SAFE.  That existing
Matrix choice is passed to the existing advisory Planner as `--source-egress`.
The Planner still selects the target and the existing Candidate, Packet, Lease,
Barrier, route writer and S11 checks remain unchanged.  No route is written,
no user is selected by Codex, and no new worker, timer, queue or state source
is created.

## Verification and next action

- Focused unit tests: 17 PASS.
- Syntax compilation and whitespace validation: PASS.
- Existing function tests retain the one-source and certification-only
  fail-closed behavior.
- The second repair requires safe deployment and a future live automatic
  profile-service failure to measure the full T0→S11 path.  Codex must not
  recreate or manually advance that incident.  Acceptance remains `<=7s`;
  `>8s` is a failure and requires further generic diagnosis.

## Deployment and final live observation

The second repair was published as `fbc8d59f516b5744539a248593f76464d8b176f3`
and deployed by the existing safe deployer as
`deploy-z8-14-Updatesystem-fbc8d59-20260830T002034`.  Runtime verification
confirmed the deployed Matrix consumer hash
`1a72661f71d...`, `v7-health.service=active`, and
`v7-admin-api.service=active`.

No user was moved during deployment.  Chuck2 remained on
`wireguard-1779454504-c43409`, the channel selected by the earlier live V7
recovery, and its four declared services stayed available.  This was an
observation only: Codex did not invoke the route writer or any user-specific
recovery command.

During the follow-up live check, `10.7.0.5` briefly looked affected because
its required YouTube check had failed on the same WireGuard source.  The next
fresh Matrix observation at `2026-08-29T21:27:52Z` marked that service
`RECOVERY_OBSERVED` and `OK`; the current failed-source selector consequently
returned no source.  V7 correctly made no new assignment: moving a user after
the required service has recovered would be unnecessary churn, not recovery.

The new source-specific path is therefore deployed and the live Chuck2
functional recovery is proven.  A new, naturally occurring profile-required
failure is still required to measure this deployed path against the seven
second law.  The previous 150-second event remains a failed latency sample and
is not reused as evidence of the new version.
