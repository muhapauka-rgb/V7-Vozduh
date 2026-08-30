# V7 owner-backed health-event handoff repair

Date: 2026-08-30

## Scope

Repair the current automatic ordinary failed-source recovery path without
manually choosing a user or target, writing routes, or advancing an operation.

## Live finding

The current Matrix marked `vless` failed with two enabled ordinary users in its
affected scope.  V7 automatically created current obligations and invoked the
existing governed executor, but every attempt stopped before Candidate/Packet
creation with `standing_delegated_cohort_service_failure_binding_invalid`.

The exact cause was a provenance mismatch in the executor's causal binding:
the canonical health runtime emits fresh capture-only Matrix events as
`V7_HEALTH_RUNTIME`, while the consumer accepted only the older
`EXTERNAL_UNATTRIBUTED` spelling.  The event identity, source incident, scope
fingerprint and current affected count were otherwise present.

## Change

`tools/v7-governed-canary-dry-run-cycle` now accepts exactly two canonical
Matrix evidence producers for governed failure recovery:

- `EXTERNAL_UNATTRIBUTED`;
- `V7_HEALTH_RUNTIME`.

This is not an Authority expansion.  The consumer still requires a fresh,
capture-only failure event with the exact source, incident and affected-scope
fingerprint.  Existing Packet, Lease, Barrier, mutable safety and route-owner
checks remain unchanged.

## Verification

- syntax compilation passed;
- focused new and existing causal-binding tests: 3 passed;
- governed executor and service-failure episode suites: 294 passed;
- `git diff --check` passed.

## Deployment and next proof

After safe deployment, no user is moved by this repair.  The still-open VLESS
incident is level-triggered, so the regular V7 health/Matrix caller must create
a fresh governed transaction itself.  The next observation must show the
automatic chain through Candidate, Packet, Lease, Barrier, Apply and required
service verification; it must then be timed against the 7-second product
limit.  A pre-fix stopped attempt is not timing credit.
