# N10 ordinary-like single-device entry — pre-deploy reconciliation

**Date:** 2026-08-27  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Mission:** `V7_N10_ORDINARY_LIKE_SINGLE_DEVICE_PRODUCTION_ENTRY`  
**Status:** `N10_FOREIGN_EXPIRED_CLEARANCE_REPAIR_READY_FOR_SAFE_DEPLOY`

## Fresh reality

The stale VLESS record was reconciled through the existing passive-event
consumer.  It did not move a user or create Candidate, Packet or Lease.

VLESS is not the current source of the active failure scope.  Its new Matrix
observation is `WARN`: Telegram and the base Google services are reachable,
while several non-universal services have connection-reset observations.  The
current owner-backed active source is instead
`openvpn-1779388847-d2ad7c`, with an exact two-identity affected scope.  Pasha
`10.7.0.5` is on `wireguard-1779454504-c43409` and is outside that scope.

The existing Planner correctly found an ordinary rebalance candidate for Pasha
but then removed it because its incident filter globally serialised all moves
behind the unrelated OpenVPN incident.  That was stricter than the stated
product boundary: a one-user action with its own exact Authority, Candidate,
Packet, Lease, Barrier and sole route writer can coexist while the unrelated
incident remains protected.

## Implemented bounded correction

The existing policy/Authority owner and `tools/v7-users-autoswitch` now support
the exact action class `N10_ORDINARY_LIKE_SINGLE_DEVICE`.

- It binds only one named identity, its current source, canonical owner hashes,
  an expiry, one-use consumption, rollback and S11 requirements.
- It deliberately does **not** bind a target at issuance.  The target must be
  selected fresh by the existing Planner at consumption and must still pass the
  existing Candidate/Packet/Lease/Barrier checks.
- Its scope remains one user and one concurrent operation.  No other Pasha
  device and no other ordinary user can enter it.
- An unrelated active incident remains open and unchanged; N10 uses the same
  governed apply serialization rather than bypassing it.
- The route writer remains only `v7-user-switch`; no direct route command was
  added.

The new request-only entry point is
`v7-users-autoswitch --n10-ordinary-like-authority-request-only --user <IP>`.
It only registers the Authority preimage in the existing audit owner.  It
cannot issue Authority, select a target, create execution objects or move a
user.

## Verification

Focused automated checks passed:

- `tests.unit.test_operator_execution_packet`: 105 passed;
- `tests.unit.test_v7_users_autoswitch_policy`: 203 passed, including a new
  exact N10 request test;
- combined focused run: 308 passed;
- Python compilation and diff whitespace checks passed.

The broader historical service-failure module was also started.  Its result is
not a release veto for this change: one test cannot open a localhost HTTP
socket in the desktop sandbox, and a separate pre-existing test has an
obsolete fixed-date standing-policy fixture.  Neither executes the changed N10
path.  They remain visible rather than being hidden or changed in this Mission.

## Effects so far

- route changes: `0`;
- ordinary-user assignment changes: `0`;
- Candidate/Packet/Lease creation: `0`;
- Matrix/Planner/timer changes: `0`;
- OpenVPN incident state: retained.

## Second fresh-planning reconciliation

The deployed N10 Authority request and fresh Planner run proved that the
Planner can select one current target for `10.7.0.5` without borrowing the
historical recommendation.  It correctly stopped before Apply because the
canonical restore-barrier file still contained an expired Packet lock for the
previous certification identity `10.7.0.108`.

That lock is not a live operation, is past its one-use expiry and names a
different user.  It must stay visible for audit, but it cannot prevent a new
product-scoped transaction forever.  The correction therefore does only two
things in the existing Planner and existing Packet/Lease/Barrier lifecycle:

- an N10 plan may retain its fresh one-device Candidate when the only blocking
  clearance is an expired Packet lock for another identity;
- N10 Apply is still impossible until the existing Packet owner has created a
  new, matching Packet/Lease/Barrier for that exact fresh Planner decision.

The correction neither deletes nor overwrites the historical lock, nor allows
direct Apply from the fresh plan.  Any current, unexpired or same-user lock
continues to block as before.

Focused verification after this correction: `205 passed` (the complete
autoswitch policy suite plus the N10 Authority contract test).  The new test
proves both halves: a foreign expired clearance is ignored only for Candidate
creation, and a route move remains refused until a new Packet-bound Barrier
exists.

The first live read-only use of this correction exposed one further bounded
detail: adding the diagnostic explanation before the existing snapshot check
made that check see its own in-memory explanation as a change.  No route was
changed.  The explanation is now attached only after the canonical snapshot
comparison, preserving the same safety decision without a self-created
staleness signal.  The autoswitch policy suite then passed again (`204 passed`).

The next fresh Candidate showed that the expired foreign Packet lock was also
being treated as a source-bundle lease by the snapshot gate.  This is not a
live lease and cannot authorize an Apply.  The Planner now permits only the
fresh Candidate needed to make a replacement Packet; direct Apply remains
blocked until the existing Packet owner writes a new exact Lease/Barrier and
the one-use contract is rechecked.  The full autoswitch policy suite passed
after that correction (`205 passed`).

## Exact next action

Publish and deploy this bounded correction.  The exact N10 Authority for
`10.7.0.5` is already issued and remains one-use.  Then run the Planner without
a target argument, create the normal governed Candidate → Packet → Lease →
Barrier transaction, and continue only if all fresh owners still agree.  Any
generation drift, capacity loss or service failure remains `STOP_SAFE`.

## Execution reconciliation and bounded N10 repairs (2026-08-27)

### Deployed revisions and truth

The ordinary-like one-device transaction was continued on the deployed
`Updatesystem` Runtime.  Every deployment used `tools/v7-safe-deploy` and
finished with `v7-truth-check` `PASS`, no blockers and an active
`v7-health.service`.

| Revision | Bounded correction | Verification |
| --- | --- | --- |
| `9794da55` | A Planner-derived Packet may create its matching Lease in the same existing Packet owner call. | Focused Packet/Lease test passed. |
| `4e3081f9` | Fresh exact Matrix recovery closes only genuinely historical L3 VLESS records. | 3 focused tests passed; VLESS historical records closed through the existing owner with zero moves. |
| `0b0de8fb` | An expired same-device N10 Packet lock cannot permanently suppress a fresh Candidate; it never becomes an Apply exemption. | 206 autoswitch-policy tests passed. |
| `a9a9ad7c` | A valid N10 Packet/Lease/Barrier opens one operation-scoped existing execution-control window and finalizes it back to global fail-closed state. | 206 autoswitch-policy tests passed. |
| `ab5e2d3a` | The execution-control window now binds the existing route-projection owner while the Packet/Barrier continues to bind its independent approval bundle. | 206 autoswitch-policy tests passed. |

No new Matrix, Planner, route writer, queue, registry, state source or
Authority owner was created.  `v7-user-switch` remains the only route writer.

### What the live owner path proved

1. Old VLESS L3 records were historical rather than an active failure of
   Pasha's source.  The current owner consumed fresh recovery evidence and
   closed those records; it did not delete or suppress them.  User movement:
   `0`.
2. The fresh N10 Planner selected `awg3` automatically for `10.7.0.5` from
   `wireguard-1779454504-c43409`.  It retained the actual profile services
   `telegram`, `youtube`, `google`; both source and selected target passed
   current capacity and service suitability gates.
3. Two initial live applies stopped before the route writer:
   first because no Packet-bound execution-control window was made for the
   N10 action; second because the control window compared the Packet bundle
   hash with a different, route-projection hash.  Both stops returned the
   control state to global `OPEN` (fail-closed), changed no user route, and
   were terminalized through the existing Lease owner.
4. The old one-use contract and both non-applied Leases were closed through
   their owners.  The last closed Lease recorded `apply_executed=false` and
   `users_moved=0`.

### Current safe re-entry

The exact current one-use N10 contract is `acc_898a5c58e6ccbdd1575b5b05` for
only `10.7.0.5`; it is target-unbound and requires fresh Planner selection.
The fresh candidate selected `awg3` again.  The most recent Packet/Lease
attempt was safely terminalized before the route writer because of the
now-fixed projection-binding defect.  Its old Barrier is left to its own
expiry; it is not removed or edited directly.

Before another Packet is created, the normal Packet/Lease/Barrier lifecycle
must observe that expiry and build a wholly fresh transaction.  The next
action is therefore: fresh Matrix-backed snapshot -> fresh Planner -> fresh
Packet/Lease/Barrier -> exactly one governed apply for `10.7.0.5` -> exact
route/kernel and `telegram,youtube,google` server-side S11 verification.
