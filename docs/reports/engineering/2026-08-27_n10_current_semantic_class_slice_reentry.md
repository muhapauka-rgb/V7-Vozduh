# N10 current semantic-class slice re-entry

Date: 2026-08-27  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Frontier: `N10_BOUNDED_PRODUCTION_AUTHORITY_CONTRACT_REQUIRED`

## Current fact reconciliation

The fresh Matrix projection is valid and has three ordinary semantic classes.
None has a total membership of two to four, so the prior request adapter
correctly found no whole small class.  Two classes nevertheless have current,
coherent bounded four-member slices already emitted by the existing Matrix /
Planner owner:

- a 13-member `awg0 -> awg3` class;
- a 44-member `wireguard-1779454504-c43409 -> awg0` class.

The Program's N10 contract permits bounded ordinary rollout with no manufactured
ordinary failure.  The existing request schema explicitly records
`N10_SMALL_COHORT_NO_FAILURE_INJECTION`; the deployed Core-primary commit is
limited to two to four members and verifies both the affected scope and the
whole system.  A bounded current semantic-class slice is therefore lawful;
reusing a stale historical cohort is not.

## Bounded owner correction

The existing N10 Authority-request adapter now accepts a current semantic class
with at least two members when it carries an existing two-to-four-member
ordinary slice.  It selects only the uniquely smallest class by membership.
Equal smallest classes remain `STOP_SAFE`; the adapter never uses lexical
tie-breaking, operator-supplied identities, source or target.

This narrows blast radius from a large live class to its Matrix-owned bounded
slice without adding an owner, Planner, state store, route writer, timer or
Authority mechanism.

## Verification before publication

- Focused N10 / Authority / Core-primary / writer suites: `344` passed.
- New regression coverage proves that a larger semantic class can contribute
  its bounded slice and that equal smallest classes stay ambiguous.
- Fresh Runtime observation before the change: `v7-health.service` active;
  legacy standalone Matrix and Telegram timers inactive; Core-primary
  verification `125/125` user-class and `4/4` class-egress; whole-system route
  check passed.

## Next action

Publish and safely deploy the bounded selection correction.  Then the existing
Matrix owner will rebuild the projection, the existing Authority owner will
issue one exact one-use contract for the owner-selected smallest slice, and the
existing governed lifecycle will execute the N10 transaction.  If any current
generation, target, capacity, policy, Packet, Lease, Barrier or verification
gate fails, it must stop and contain without a manual substitute.
