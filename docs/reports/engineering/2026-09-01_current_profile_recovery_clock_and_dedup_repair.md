# Current profile recovery clock and de-duplication repair

Date: 2026-09-01

## Current evidence

The live health receipt showed a continuing source incident being consumed
repeatedly with its original incident clock. For example, the health owner
received source `1` with an original Matrix clock more than 2.5 million ms in
the past, then spent 18–34 seconds in a stopped governed attempt. The stop
reason was `ordinary_service_failure_selection_binding_invalid`; it performed
no route mutation.

This was not valid recovery-SLO evidence. It also occupied the ordinary
required-service recovery slot, delaying a later current profile failure on a
different source.

## Cause

The existing Matrix/profile join used a service row's immutable confirmed
incident time as the dispatch clock. It also included the rotating per-sample
`failure_event_id` and observation data in the exact-once identity. Therefore
a continuing failure could be redispatched for every fresh Matrix observation,
while a newly placed affected customer was measured against an old incident.

## Repair

The existing `v7-health-loop` now keeps two clocks from the same Matrix row:

- immutable incident time, retained in the health receipt for history;
- newest Matrix observation time, used as the live dispatch clock.

Its exact-once identity now consists only of source, currently affected
profile/service and immutable source-incident id. A rotating observation id
cannot resubmit the same unresolved scope. A changed profile scope (for
example, a newly placed customer) has a different identity and is still
consumed by the existing V7 health caller.

No Matrix owner, Planner, Authority, route writer, timer, registry or user
assignment was added or changed.

## Verification

- Focused health tests: 4 passed, including the new continuing-incident case.
- The new test proves that an updated observation changes the dispatch clock
  from 500 to 900 while preserving the exact-once identity and the immutable
  incident clock of 100.
- A broader pre-existing health timing harness has three failures caused by
  assertions that no longer match the already-deployed role-priority behaviour;
  none exercise the edited profile-binding code.
- The broader service-failure episode suite has one pre-existing source-text
  assertion that expects an older Planner call shape; it does not exercise
  this edit. These failures remain visible and are not counted as a pass.

## Production effect to observe

After safe deployment, an unchanged current profile failure can consume at
most one ordinary-recovery attempt for its same current scope. A later
operator placement on a continuing failed source must receive a new current
observation clock and be handled by V7 itself. The resulting receipt will
separate the immutable incident time from the customer-recovery clock.

## Next step

Publish and deploy this bounded repair, then observe the next live,
automatically originated required-service recovery. It is valid SLO evidence
only when the receipt contains all clocks through required-service S11 and no
manual recovery transition occurred.
