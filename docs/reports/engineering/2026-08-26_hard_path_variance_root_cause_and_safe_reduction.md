# V7 Hard-path variance: root cause and safe reduction

**Date:** 2026-08-26  
**Mission:** `V7_HARD_PATH_VARIANCE_ROOT_CAUSE_AND_SAFE_REDUCTION`  
**Scope:** controlled certification identity only; no ordinary-user route, assignment, Matrix cadence, or policy change.

## Baseline

The deployed 2-vCPU Runtime was active.  The standalone Full/Telegram timers remained intentionally inactive; `v7-health.service` was active.  CPU pressure and active Matrix/gateway work were observed, so contention remained a performance-variance hypothesis.  It was not treated as a causal conclusion.

The controlled identity was `10.7.0.124`, on isolated source `amneziawg-exec-20260528-10-8-1-14`.  Its official owner-selected distinct target was `awg0`.  All evidence below remained inside this certification scope.

## Controlled diagnosis

Two independent controlled source-failure transactions reached a fresh Matrix-confirmed hard-failure state and a ready selection result, but the ordinary persistent health consumer did not create Candidate, Packet, Lease, or a sample reservation.  Both fixtures were returned through existing state, Matrix, routing, and operation-cleanup owners.  No ordinary identity moved.

A direct call to the existing Matrix consumer before Matrix had recorded T0 safely made no transaction.  The same existing entry point after fresh canonical T0 completed the governed chain and closed cleanly.  Its timing record was **functional only**, not latency evidence: it was started 122.878 s after T0.  It therefore receives no SLO credit.  The resulting decomposition was planner 293.458 ms, packet/lease 22.839 ms, barrier 766.681 ms, apply/verification 5014.541 ms, feedback 68.943 ms, total 6166.462 ms.

This separates the problem from target eligibility and from the governed chain itself: the chain works when consumed; the automatic Runtime wake could be suppressed.

## Measured root cause

`v7-health-loop` has one existing process-local persistent-consumer de-duplication cursor.  Its canonical hard-failure helper selected the first affected source in `users.registry`.  Registry order is not incident order.  With more than one active Matrix failure, an older source listed first could hide a newer confirmed T0; the scalar cursor then suppressed the only Runtime wake for that newer incident.

This is one bounded incomplete handoff defect (classification **A**), not a new owner or architecture decision.  The Matrix consumer continues to re-read and admit the full current scope.

## Minimal correction

The helper now takes the maximum confirmed T0 among currently affected registry assignments.  It changes only which exact Matrix-owned wake advances the existing scalar cursor.  It adds no state, owner, queue, timer, route writer, Planner, Matrix logic, policy, or new source of truth.

Focused regression coverage deliberately lists an older failed source first and confirms that the newer active assignment's T0 is returned.

## Verification before publication

- Focused unit suite: **15 passed**.
- Source syntax compilation and `git diff --check`: passed.
- Safe-deploy preflight before commit correctly returned **NO-GO** because the runtime-critical fix was uncommitted and the remote truth check was unreadable.  No deployment was attempted from that state.

## Runtime effect and safety

The correction only affects the decision to invoke the existing persistent Matrix consumer after a fresher current confirmation.  Stale, missing, or unassigned failures remain rejected by the same canonical checks.  The prior controlled fixture is restored: the certification identity is back on its isolated source with its expected policy rule/table/default route; there are no active controlled operations.

## Limits

This report does not claim a HARD_PATH SLO result and does not attribute the observed latency variance to CPU contention.  The only live functional sample was deliberately late relative to T0 and is excluded from performance acceptance.

## Exact next frontier

1. Commit, publish, and safe-deploy this bounded handoff correction; verify local/GitHub/Runtime hashes and service/timer state.
2. Run **one** fresh cold certification-only incident through `v7-health.service`, without direct Matrix invocation, and prove automatic Candidate/Packet/Lease creation and safe closure.
3. If automatic consumption is proven, freeze this handoff fix and resume the measured HARD_PATH variance experiment with homogeneous samples.  If it is not, stop and report the next exact existing-owner boundary; do not add a parallel consumer.
