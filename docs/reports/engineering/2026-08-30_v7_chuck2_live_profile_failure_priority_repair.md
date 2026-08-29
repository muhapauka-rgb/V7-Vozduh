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

## Production safety and next action

The repair is not deployed by this report.  After the standard safe deploy,
the live `v7-health.service` remains the sole operational caller.  It must
observe the current VLESS profile failure, select its owner-admitted target,
and complete governed recovery plus required-service S11 without Codex moving
Chuck2.  Capture the resulting Matrix T0, decision, Candidate/Packet/Lease/
Barrier, S11 and total time against the seven-second law.
