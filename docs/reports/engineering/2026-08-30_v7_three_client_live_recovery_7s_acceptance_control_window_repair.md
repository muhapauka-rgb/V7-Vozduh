# V7: three-client live recovery — control-window sequencing repair

**Date:** 2026-08-30  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Mission:** `V7_THREE_CLIENT_LIVE_RECOVERY_7S_ACCEPTANCE`

## Purpose

Restore the existing automatic ordinary-user recovery chain for a real failed
source without manually moving a user or creating a recovery transaction. The
live input is the current VLESS assignment of `10.7.0.125`, `10.7.0.126`, and
`10.7.0.127`. Their required-service profiles were read from the canonical
registry; no user, route, Matrix state, Candidate, Packet, Lease, or Barrier
was written by the engineering session.

## Evidence before the repair

The normal `v7-health` / Matrix consumer did discover VLESS as a failed source
and did start a governed ordinary-recovery transaction. Its durable result was
`GOVERNED_TRANSACTION_STOPPED`, with
`packet_bound_execution_control_window_not_open` before Apply. Therefore the
runtime had not moved any user (`users_moved=0`).

The root cause was sequencing, not target selection: the parent governed
Packet/Lease/Barrier executor checked for a short exact execution-control
window before invoking `v7-user-switch`. The only code that could open that
same window was in the child route writer, so it could never be reached. The
resting global state is intentionally fail-closed (`OPEN`), which made every
otherwise valid automatic recovery stop safely.

## Implemented generic repair

* The existing governed executor now opens a short-lived, Packet/Lease/Barrier
  bound `EMERGENCY_FAILOVER` operation window only after its final mutable
  checks and immediately before its existing pre-Apply decision.
* `v7-user-switch` remains the sole route/Core-primary writer. It can only
  adopt the already-opened window when operation id, selected-move hash, source
  and snapshot hashes, action class, and exact selected count all match.
* The existing control owner permits only an exact emergency-recovery cohort of
  two through four users. This does not create general batch authority.
* The parent binds the actual Packet selection count, not the standing policy
  ceiling; a policy limit of four cannot turn a three-user transaction into a
  four-user one.
* A mismatched, stale, or non-operation-scoped window remains STOP_SAFE and is
  finalized through the existing owner.

No Planner, Matrix owner, timer, route writer, registry, queue, or alternative
truth source was added.

## Verification before publication

* syntax compilation: pass;
* new exact-window ordering and bounded-cohort tests: 4 passed;
* `tests.unit.test_v7_users_autoswitch_policy`: 226 passed.

The broader combined governed test selection retained two pre-existing,
time-dependent failures caused by an expired standing delegated-policy contract;
the six failures introduced during the first unscoped draft were eliminated by
restricting the parent-window behavior to the ordinary-service-failure path.

## Second live reconciliation: Matrix-to-executor receipt cycle

After the control-window repair and the existing Authority owner activated the
authorized four-user ordinary-recovery policy, the normal `v7-health` caller
again detected the live VLESS required-service failure. Current Matrix scope
was four ordinary users (the three acceptance inputs plus one already present
ordinary user); the three inputs split into two profile-compatible prepared
classes. The Matrix owner created the exact durable obligation
`sfaob_05e23cd981a93d7b51b0ab29` for incident
`sfinc_3215856daf5e8b44f637f349e057b841`.

The governed executor then correctly stopped before Candidate/Packet/Lease or
route mutation with `standing_delegated_cohort_service_failure_binding_invalid`.
Its precise cause was a circular lifecycle condition: a fresh Matrix obligation
was deliberately passed to execution before its OMP receipt (so the receipt
does not add seconds to recovery), while the executor still required that same
receipt before it could start.

## Implemented second generic repair

* Only the existing Matrix caller may mark the newly materialized exact
  obligation as a fresh runtime handoff.
* The governed executor may then proceed without the deferred OMP receipt, but
  still independently requires the durable obligation, exact source incident,
  unchanged current scope fingerprint, actionable classification, and a fresh
  capture-only Matrix event with the expected provenance.
* Direct L3 handoffs and already-consumed OMP obligations retain their prior
  paths. Certification bindings cannot use the fresh ordinary handoff flag.
* OMP receipt persistence remains required afterwards as history/evidence; it
  is no longer a circular synchronous prerequisite.

This changes no route, client, Matrix fact, Candidate, Packet, Lease, Barrier,
authority policy, or target. It removes one generic wait/deadlock in the
already existing owner chain.

## Verification before publication

* new receipt-cycle causal-binding test: passed;
* Matrix command propagation test: passed;
* focused execution tests: 2 passed;
* targeted governed/Matrix test set: 281 tests ran, with two pre-existing
  expiry-fixture failures caused by a standing contract dated before the
  current clock;
* broader legacy automation suite also exposes pre-existing fixtures that do
  not initialize `AutoswitchPlanner.matrix`; this failure precedes and is
  outside the changed path;
* diff whitespace check: passed.

## Third live reconciliation: competing executor must not reopen another operation

Both prior repairs were deployed and the normal `v7-health` caller then proved
the next stage with no engineering route action. It created a real bounded
four-member Packet/Lease/Barrier transaction for VLESS to `awg0`:

* source incident: `sfinc_3215856daf5e8b44f637f349e057b841`;
* exact selected scope: `10.7.0.13`, `10.7.0.125`, `10.7.0.126`,
  `10.7.0.127`;
* target: `awg0`, selected by the existing Planner;
* capacity: `33/148`, therefore not a capacity or target-eligibility stop.

The transaction still stopped at
`packet_bound_execution_control_window_not_open`. Investigation of the
existing control owner showed a cross-process race: a second normal Matrix
generation could encounter the first transaction's valid, operation-scoped
closed window. Its generic "recovery" path then force-opened that window,
invalidating the first transaction before `v7-user-switch` could consume it.
This is an executor-ownership defect, not a client or target-selection issue.

## Implemented third generic repair

* A valid closed operation window is now treated as being owned by the
  transaction named in it. A competing transaction stops safely and does not
  reopen, finalize, or otherwise alter it.
* A finalizer also preserves a later valid operation window owned by another
  transaction instead of force-opening it.
* Only invalid control state can use the existing fail-closed recovery path.

This preserves the existing control owner and fail-closed policy. It adds no
timer, queue, planner, route writer, state source, or authority. It is the
necessary ownership isolation for the normal V7 Runtime to complete one
automatic recovery while background Matrix generations continue.

## Verification for the third repair

* New unit test proves a competing governed transaction cannot invoke either
  the executor or the control-window finalizer when a valid foreign operation
  window is active: pass.
* Existing exact control-window ordering test: pass.
* Full governed CLI suite: 154 tests run; 152 pass. The two failures remain
  pre-existing, time-dependent fixtures whose standing policy expired before
  the current clock.
* Service-failure episode suite: 128 passed.
* Whitespace/diff validation: pass.

## Current next step

Publish and deploy this third repair, then return control exclusively to the
normal `v7-health -> Matrix -> governed executor` caller. Observe the current
VLESS condition until the first valid automatic operation completes or a new,
distinct owner blocker is evidenced. The previously observed attempts already
exceed the seven-second KPI; they remain explicit product failures and are not
credited. No manual recovery is valid acceptance evidence.
