# V7 profile-required-service live recovery reconciliation

Date: 2026-08-29

## Scope

Read the live ordinary profile-required-service recovery chain, explain why
Chuck2 was not moved, and repair the generic scheduling defect that made the
ordinary detector exceed the current seven-second recovery envelope.  No user
was moved and no recovery transaction was started manually.

## Current source truth

The initially observed Matrix row for Chuck2 (`10.7.0.127`, source `awg3`)
still showed Instagram `FAIL` from `18:38:12Z`.  The active health loop's
ordinary detector subsequently made a fresh, isolated observation and found
no failed service for Chuck2.  The normal Matrix deep owner then refreshed the
canonical row at `19:49:11Z`: Instagram is `OK`, HTTP 200, and the failure
state is `HEALTHY`.

Therefore V7 did not have current confirmed failure evidence on which it could
lawfully start an automatic recovery.  Moving Chuck2 in that state would have
been a manual or false-positive action.  The earlier old Matrix display was a
stale historical failure, not a current reason to switch.

## Real generic latency defect

Runtime journal evidence showed the ordinary required-service detector
(`other_required`) often taking 8--26 seconds while the non-critical prepared
target application-service refresh (`hot_target_other`) ran concurrently at
the same scheduler priority.  The detector's own bounded probe batch completed
in about 1.24 seconds; the excess was host scheduling contention on the
two-vCPU Runtime.  This is incompatible with the current ordinary recovery
envelope and could delay a real event.

## Bounded repair

The existing health owner now gives `other_required` normal priority and makes
`hot_target_other` the lowest normal priority.  Both existing roles, cadence,
Matrix ownership, target evidence, Planner, Authority, Candidate, Packet,
Lease, Barrier, route writer and S11 semantics are unchanged.  The change does
not create a worker, queue, timer or state source.  It merely prevents
background target refresh from taking an equal CPU share from the ordinary
failure detector.

Focused tests passed:

- `tests.unit.test_v7_health_fast_deadline_loop`: 20 passed;
- `tests.unit.test_v7_egress_diagnose` plus
  `tests.unit.test_v5_3_role_based_recovery`: 52 passed;
- `git diff --check`: passed.

The local implementation is committed as `4e595965`.

## Deployment boundary

The safe-deploy preflight allowlist passed, but deployment is correctly held:
the external GitHub remote could not be independently read and the execution
environment rejected publication of the new runtime commit pending explicit
confirmation of this particular external code transfer.  No Runtime binary
was changed.  Once publication is permitted and remote truth becomes readable,
the exact next action is safe deploy with health restart, followed by measured
normal health cycles and then observation of the live V7-originated recovery
chain on the next genuine confirmed profile-service failure.
