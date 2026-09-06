# Autonomous Recovery Polygon E2E measurement correction — 2026-09-06

## Result

`AUTONOMOUS_RECOVERY FULL_CAMPAIGN` no longer has a lawful path from an
isolated Docker/receipt-assembler result to a `Section 8` or `<7s` recovery
claim.  That historical evidence remains `ISOLATED_POLYGON_ENGINEERING_ONLY`.
It is not `POLYGON_E2E`, Runtime, Production, or user evidence.

## Discovered owner path and gap

The real production chain is owned by existing components:

`v7-health-loop` → `v7-egress-diagnose` → `v7-service-matrix-test` →
`v7-service-matrix-refresh-all` → `v7-users-autoswitch` → existing required
service S11 verification.

The present Docker path instead starts a local stopwatch immediately before
`tc` and executes a bespoke HTTP loop.  Its controlled health-loop mode can
read a temporary Matrix file, but it does not bind that temporary state/event
context into the persistent Matrix consumer.  Therefore it cannot presently
produce one immutable ledger spanning physical failure, real health detection,
current Matrix scope, governed mutation, kernel-route verification, and last
affected required-service S11.

## Implemented fail-closed correction

`autonomous_recovery_polygon_e2e_baseline_binding` now requires a one-client
ledger with monotonic timestamps, all existing owner identities, a physical
trigger origin, no synthetic receipt, `POLYGON_E2E` evidence label, and an
explicit non-Production label.  Absent or incomplete evidence returns:

`STOP_SAFE_POLYGON_E2E_BASELINE_REQUIRED`

with the exact missing connection:

`existing_v7_health_detector_to_isolated_matrix_current_state_event_governed_executor_required_service_s11_ledger`.

No 1K or 10K run is admitted before that baseline passes.  A later result can
be only `VERIFIED_E2E_WITHIN_7S`, an over-7s causal ledger, or this exact
STOP_SAFE boundary.

## Verification

`python3 -m unittest -v tests.unit.test_autonomous_recovery_agent_profile`

Result: 15 tests passed.

`PYTHONPYCACHEPREFIX=/tmp/v7-e2e-pyc python3 -m py_compile tools/v7_sync_lib.py`

Result: passed.  No Runtime, Production, user, Authority, Docker campaign, or
deployment action was performed by this correction.
