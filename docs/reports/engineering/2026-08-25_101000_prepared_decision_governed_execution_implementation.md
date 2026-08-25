# Prepared Decision Governed Execution — Implementation

Date: 2026-08-25  
Scope: V5.3 HARD_PATH `T0 -> decision`; existing Matrix, Planner, Candidate,
Packet, Lease, Barrier and Apply owners only.

## Decision consumed

The owner approved the smallest remaining architectural change: a fresh,
Matrix-prepared source/target decision may be consumed after T0 by bounded
mutable validation.  This is not a new Planner, owner, Authority grant,
state store or ordinary-user path.

## Implemented change

`tools/v7-users-autoswitch` now activates
`PREPARED_TARGET_MUTABLE_VALIDATION_ONLY` only when all of these are true:

* governed candidate-only and emergency-failover modes are both present;
* one exact certification identity, source, target and move budget are bound;
* the Matrix projection is freshly reread and its source, target, capacity
  contract and fingerprint match the governed handoff;
* the source is still currently ineligible and the prepared target passes
  current basic, reservation, organization, quality, required-service, load
  and safety gates.

The path deliberately skips only advisory scoring and world reranking.  It
does not skip mutable safety gates or the existing downstream
Candidate -> Packet -> Lease -> Barrier -> Apply verification chain.

Any absent, stale, ambiguous or drifted handoff returns
`EXISTING_FULL_PLANNER_FALLBACK`.  The new path cannot be entered by an
ordinary user or an unbounded operation.

## Verification before deploy

* `tests.unit.test_service_failure_episode`,
  `tests.unit.test_v7_users_autoswitch_policy`, and
  `tests.unit.test_governed_canary_cli`: **453 passed**.
* V5.3 regression suites for pre-ready/staggered, causal Polygon and scale
  tournament: **26 passed**.
* New tests prove the bounded path is used for a fresh exact handoff and that
  in-process fingerprint drift falls back to the full Planner.

No runtime, configuration, cadence, priority, Matrix writer, verifier,
Authority policy, route or client was changed by this local implementation.

## Deploy gate and next action

The initial read-only deploy gate correctly refused publication because CPS
and OMP still exposed the earlier owner-decision stop while the owner decision
had already been consumed.  That is a documentation/state-pointer
reconciliation, not a defect in the execution change.  It must be reconciled
before a safe deploy can be admitted.

Next action: reconcile the official current-state pointers to the approved
implementation-and-Polygon-proof frontier; rerun the deploy gate; then deploy
and collect a new frozen HARD_PATH series on the resulting fingerprint.
