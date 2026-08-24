# CT-M0F controlled transaction reservation handoff

Date: 2026-08-25 (MSK)  
Scope: existing V5.3 controlled Polygon certification path only.

## Purpose

Prevent the normal health/recovery lifecycle from independently reassigning the
one synthetic certification identity between controlled setup/T0 and the
governed `Candidate -> Packet -> Lease -> Apply` handoff.  This is not a user
pin, a health shutdown, or a new owner.

## Evidence before the change

Read-only production observation found the synthetic identity `10.7.0.92` on
the dedicated execution source with an active existing controlled-source
reservation.  `switch-history.jsonl` nevertheless recorded repeated
`autoswitch_failover` assignments from that source to `awg3`/`awg0`, including
the latest run shortly after governed setup.  The subsequent governed bind then
correctly stopped with `availability_first_planner_identity_missing:10.7.0.92`:
the Planner no longer had a decision for `(identity, prepared source)`.

`v7-health.service` remained active and the Matrix timer remained disabled as
previously configured.  No ordinary identity was queried or changed.

## Implemented contract

The existing `admin_core.operator_execution` reservation/audit owner now has a
short-lived (five minute) CT-M0F transaction reservation:

```text
exact healthy synthetic source + source reservation + binding fingerprint
  -> transaction reservation (before controlled failure)
  -> Matrix/Planner handoff
  -> exact Packet + Lease + operation bind
  -> governed Apply only
  -> terminal release / STOP_SAFE cleanup / expiry
```

The existing `v7-users-autoswitch` Planner consumes that reservation immediately
before route application.  While it is active, a normal recovery/rebalance move
for the same identity and source is rejected without a route write.  After
Packet/Lease binding, only the matching operation and target may proceed.
Every other identity and ordinary health processing remain unaffected.

The condition record was also corrected: controlled source failure changes
runtime source state but moves zero users and does not itself apply a user route.

## Safety properties

- No new Matrix, Planner, Runtime, registry, queue, watcher, state source or
  Authority was created.
- The source reservation remains the existing topology owner; the new rows are
  durable lifecycle records in its existing operator-execution audit.
- Conflicting, ambiguous, expired or unbound reservations fail closed.
- The reservation ends on governed terminal handling, explicit recovery/rollback
  handling, failed condition activation, or expiry.
- The exact governed path still requires Candidate, Packet, Lease, Barrier,
  Apply, route/kernel verification and required-service S11; none was relaxed.

## Verification

- Focused owner/consumer suite: **552 passing**.
- V5.3 Polygon/scale suite: **26 passing**.
- Syntax compilation and whitespace validation: passed.
- Added tests prove:
  1. unbound reservation blocks independent reassignment;
  2. exact Packet/Lease operation is permitted;
  3. terminal release restores normal eligibility;
  4. the Planner reaches the guard before invoking the route writer;
  5. controlled-condition preparation records the reservation.

## Deployment and production observation

This report records the local implementation block.  At report creation the
change has not yet been committed, deployed or exercised on Polygon; therefore
it is not SLO evidence and no production route/client has changed in this block.

## Exact next step

Commit, publish and safe-deploy this bounded owner-consumption change.  Then run
one synthetic cold controlled transaction.  Accept it only if the identity
remains on the prepared source until the exact governed operation binds it, and
then reaches governed Apply/S11 without any ordinary-user effect.  If it fails,
retain the terminal evidence and stop rather than weakening the reservation or
S11 semantics.
