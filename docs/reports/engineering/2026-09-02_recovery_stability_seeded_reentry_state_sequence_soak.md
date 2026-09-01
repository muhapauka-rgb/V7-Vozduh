# Recovery Stability — seeded re-entry state-sequence soak

Date: 2026-09-02
Mission: `V7_RECOVERY_STABILITY_HARDENING_AND_STATE_SEQUENCE_SOAK`
Block: seeded current/stale re-entry stress lane

## Purpose

Stress the existing level-triggered L3 re-entry owner with mixed current,
closed, stale and ambiguous state without touching Runtime.  The test is aimed
at the specific failure mode where historical completion either suppresses a
new real problem or causes a risky guessed continuation.

## Work performed

Added a deterministic seeded 1,000-transition test (`seed=20260902`) to the
existing Service Failure Automation suite.  Every transition varies source,
incident, scope size and one of five lifecycle shapes:

- exact closed current incident;
- exact already-open current incident;
- exact open incident with stale scope;
- no exact matching incident;
- duplicate matching incident.

One quarter of generated bindings deliberately has no current failed scope.
For each transition the existing owner must either reopen only the exact
current incident, retain an already-open exact incident, or stop safely.  An
unrelated incident must remain unchanged.

## Evidence

- 1,000/1,000 seeded re-entry transitions: PASS.
- Every lifecycle shape occurred at least 150 times.
- Focused companion tests (six total): PASS in 0.209 seconds.
- `git diff --check`: PASS.

The test performs no Matrix cycle, service restart, Candidate/Packet/Lease/
Barrier creation, Authority operation, route mutation or client move.

## Result and boundary

The existing owner reopened only exact current closed/stale-scope incidents.
It returned `CURRENT_SCOPE_ALREADY_OPEN` for a still-valid open scope and
failed closed for absent current scope or ambiguity.  This is a meaningful
seeded state-sequence result, but it does not claim the full
`RECOVERY_RANDOMIZED_STATE_SEQUENCE_SOAK_CONSUMED` terminal: it covers one
re-entry owner only.  Remaining lanes include other re-entry triggers,
post-terminal execution residue and normal Runtime ordinary-path evidence.

## Simplification assessment

The work reuses the existing L3 state projection and its existing
reconciliation method.  No production logic, extra process, state source,
timer or route writer was introduced; Runtime structural complexity remains
unchanged.
