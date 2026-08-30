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

## Fourth live reconciliation: the same operation window was opened twice

The third repair was deployed as `c2f367f6`. The live Runtime then created new
ordinary-recovery Packet/Lease/Barrier records itself; the three acceptance
inputs remained on VLESS and no engineering route action occurred. Each new
operation nevertheless ended at the same terminal reason before Apply.

The exact cause was inside the existing L3 ordinary-recovery executor, not a
foreign transaction: it already creates a valid, exact operation-scoped
window while binding the Packet. Later, after Lease and Barrier, it called the
same helper as if the window had to be opened again. That helper correctly
sees the existing window as `CLOSED`, but before this repair it treated even
the exact same operation as absent. Thus the transaction cancelled itself.

## Implemented fourth generic repair

* The packet-bound helper now reuses a `CLOSED` window only when every bound
  field agrees exactly: operation id, selected-move hash, source hash,
  snapshot hash, action class, and cohort size.
* It performs the existing forward-mutation validation against that same
  generation and never rewrites it.
* A foreign, partial, stale, or otherwise mismatched window remains
  `STOP_SAFE` and is never adopted.

This is a minimal repair of the existing control owner. It does not select a
target, move a user, widen authority, or create a new execution path.

## Verification for the fourth repair

* New exact-match reuse test: passed.
* Existing first-open ordering and bounded-cohort tests: passed (3 total).
* Service-failure episode regression: 128 passed.
* Whitespace/diff validation: passed.

## Current next step

Publish and safely deploy the fourth repair, verify code/runtime alignment,
then return control only to the normal `v7-health -> Matrix -> L3 executor`
caller. The current Matrix condition must be re-read at that point: if the
operator-provided source failure has recovered, it is closed without an
unnecessary user move and cannot be counted as seven-second acceptance. If a
fresh required-service failure remains actionable, V7—not Codex—must complete
the automatic recovery and produce the full last-member timing record.

## Fifth live reconciliation: the route consumer rejected its own lawful cohort

The fourth repair was deployed as `066c18d7`. The normal `v7-health` caller
then created a new current ordinary VLESS recovery operation itself. It passed
Matrix, affected-scope discovery, Planner, Candidate, Packet, Lease, Barrier,
and its exact operation window. The existing Planner selected four ordinary
members from the same failed source, within the current delegated tier of
four, and the existing owner selected `awg0` as target.

No client was moved. The route consumer stopped the operation before calling
`v7-user-switch` with `l3_execution_eligibility_stop_safe`. Its per-operation
reason was `ordinary_service_failure_requires_exactly_one_move`.

This was an internal contract contradiction: the existing source-scoped
Planner and Packet/Lease/Barrier owners lawfully authorize a bounded cohort,
but the final mutable pre-Apply check still insisted on exactly one member.
It violates the product requirement to recover a compatible failed-source
cohort rather than serializing every member into separate lifecycles.

## Implemented fifth generic repair

* The final ordinary service-failure check now accepts one through the exact
  already-authorized delegated cohort size. The allowed size is the smaller of
  the live ordinary-production policy ceiling and the existing caller's
  `--max-selected-moves` narrowing value.
* A missing, zero, or non-engineering-qualified tier remains `STOP_SAFE`.
  The repair does not raise a policy ceiling or allow an arbitrary batch.
* Every member still receives the same live mutable checks: enabled ordinary
  identity, unchanged source, eligible distinct target, fresh required-service
  failure, target readiness, and certification exclusion.
* Planner, Matrix, Authority, Packet, Lease, Barrier, Core-primary, and
  `v7-user-switch` remain the existing owners. The repair selects neither
  clients nor targets and makes no direct runtime mutation.

## Verification for the fifth repair

* New focused test proves that a four-member ordinary profile-failure packet
  passes only when every individual member's current evidence is valid and the
  existing authorized tier is four.
* Existing exact Matrix profile-failure and tier-four scope tests pass.
* Focused result: 3 passed.
* Service-failure episode regression: 128 passed.
* Whitespace/diff validation: pass.

## Next step

Publish and safely deploy this fifth repair. Then observe only the normal
`v7-health -> Matrix -> automatic governed recovery` chain. If the current
Matrix evidence remains actionable, V7 must recover the selected current
cohort itself and emit the last-member timing. If it does not, no one is moved
and the current observation remains an invalid/non-creditable seven-second
sample; the next fresh live owner-backed failure is required.
