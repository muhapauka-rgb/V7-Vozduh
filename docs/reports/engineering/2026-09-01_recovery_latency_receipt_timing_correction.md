# Recovery-latency receipt timing correction

Date: 2026-09-01

## Scope

The active `RECOVERY_LATENCY_SLO` contract measures the path from a fresh
failure observation to every affected user's required-service S11.  The
existing health-owner receipt previously exposed only one duration labelled
`t0_to_consumer_complete_ms`, but calculated it from consumer start.  It
could not distinguish scheduling delay from transaction execution.

## Change

The existing `v7-health` receipt now records, on its already-owned monotonic
clock:

- Matrix T0;
- consumer start;
- consumer completion;
- T0-to-start, T0-to-completion and consumer-execution durations.

No Matrix, Planner, Authority, route writer, timer, source selection,
assignment or user movement changed.  The receipt is observability only.

## Verification

- `test_persistent_consumer_emits_outcome_receipt_without_operational_effect` — PASS.
- `test_matrix_projection_retains_governed_execution_timing` — PASS.
- CPS/OMP active-mission identity and pointer reconciliation — PASS.

## Current result and next condition

The historical automatic three-user VLESS recovery remains evidence of a
roughly 39.5-second T0-to-consumer path before the latest terminal-classification
repair; it is not SLO credit for the current deployed fingerprint.  The normal
Runtime must now receive a fresh real or existing-owner-admitted Polygon
failure.  Its resulting receipt and governed transaction timing will show
whether the repaired path meets `P95 <= 7 s` and `max <= 8 s`.
