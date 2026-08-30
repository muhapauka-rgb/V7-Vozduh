# Fresh L3 obligation direct-handoff repair

## Purpose

Restore the automatic V7 path from a current Matrix service failure to the
existing governed recovery executor.  This repair does not move a user,
select a target, or invoke a routing command.

## Measured current evidence

On 2026-08-30 the canonical Matrix recorded a current VLESS failure affecting
two ordinary users (`10.7.0.126`, `10.7.0.127`).  The existing Planner had
already produced compatible prepared targets.  The compact L3 incident was
OPEN, had an exact current scope of two unresolved users, and referenced one
`READY_FOR_OMP_CONSUMPTION` obligation.  Nevertheless the governed action
reported `STOP_SAFE_NO_CURRENT_SERVICE_FAILURE_OBLIGATION`.

The cause was a circular handoff requirement: the Runtime required
`direct_execution_handoff`, while that cache was created only after the
historical OMP receipt.  The same Runtime was intentionally avoiding that
receipt on the immediate path.

## Change

`service_failure_direct_execution_handoff` now accepts exactly one already
durable ready obligation when it matches the existing OPEN L3 incident.  It
still requires the exact source-incident identity, source-scope fingerprint,
unresolved current scope, and a unique ready obligation.  Any ambiguity or
drift remains fail-closed.

The change reuses the existing Matrix, L3 state and closure-record owners.  It
creates no new state source and performs no operational action itself.

## Verification

- New focused unit test: a fresh L3 incident plus one exact ready obligation
  produces a READY handoff before an OMP receipt exists.
- Existing direct-handoff scoped-selection and stale-cache tests pass.
- Existing terminal/reopen passive-incident tests pass.

## Runtime follow-up

After safe deployment, only the normal persistent V7 health caller may
consume the new handoff.  The next check must prove: fresh Matrix observation
→ exact L3 handoff → Planner/Authority/governed executor → S11, with no manual
user, target, Candidate, Packet, Lease, Barrier, or routing operation.
