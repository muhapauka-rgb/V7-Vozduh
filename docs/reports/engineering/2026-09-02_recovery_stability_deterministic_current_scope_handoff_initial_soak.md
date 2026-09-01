# Recovery Stability — deterministic current-scope handoff soak

Date: 2026-09-02
Mission: `V7_RECOVERY_STABILITY_HARDENING_AND_STATE_SEQUENCE_SOAK`
Block: deterministic state-sequence foundation

## Purpose

Prove in the existing isolated test/Polygon interface that an open current
ordinary incident is not hidden by an older ready obligation or a closed zero
scope.  This block uses the existing L3 direct-handoff reader only.  It does
not create an operational Runtime owner and does not start a recovery.

## Implementation

Added one data-driven test to the existing Service Failure Automation suite.
It drives 100 isolated current-scope transitions across three source labels
and four affected-scope sizes.  Every transition contains a conflicting
historical zero-scope obligation and an exact current open incident.  The
existing handoff owner must select only the current Matrix-bound obligation.

The first 50 transitions are the initial deterministic threshold; all 100
form the final current-scope handoff threshold for this narrow invariant.

## Evidence

- 100/100 deterministic handoff transitions: PASS.
- 4 focused current-scope/historical-residue regressions: PASS.
- `git diff --check`: PASS.

The tested owner is read-only at this stage: no Candidate, Packet, Lease,
Barrier, Authority, route mutation, client movement, Matrix cadence or timer
was created or changed.

## Scope boundary

This is not a claim that the full `RECOVERY_STATE_SEQUENCE_SOAK_CONSUMED`
terminal is complete.  It covers only the current-scope vs historical-ready
handoff invariant.  The next required portions remain the real
level-triggered/re-entry and post-terminal-residue sequence coverage, then the
existing time-control and seeded randomized test lanes.  Live ordinary-path
credit remains separate and cannot be inferred from this test.

## Simplification assessment

The test reuses the existing closure-record and L3 handoff owners.  It adds no
Runtime branch, state store, caller, consumer or locking scope; structural
Runtime complexity is unchanged.  Historical handling is asserted to remain
advisory when an exact current scope exists.
