# V7 Hot-Path Direct Handoff Regression Gate — Reconciliation Report

**Mission:** `V7_HOT_PATH_DIRECT_HANDOFF_REGRESSION_GATE_RECONCILIATION_V1`  
**Type:** read-only test-failure classification  
**Verdict:** `DIRECT_SLICE_PASS; HISTORICAL_FULL_SUITE_NOT_GREEN`

## Evidence

The full relevant historical suite ran 167 tests: 152 passed, 15 failed.
Focused direct-handoff validation remains green: compile, valid direct handoff,
stale direct rejection, legacy receipt compatibility, fresh source order and
direct source order all pass.

## Failure classification

| Group | Count | Root cause | Relation to direct handoff |
| --- | ---: | --- | --- |
| Service-failure source CPS fixtures | 4 | fixtures expect Service Failure to be `ACTIVE_PROGRAM`; current CPS is RS6 | orthogonal |
| Standing-policy CPS fixtures | 4 | fixtures expect historical active-program/frontier policy state | orthogonal |
| Atomic functional-footprint fixtures | 3 | current CPS rejects old AEP/completion fields | orthogonal |
| Controlled target fixture | 1 | historical controlled-pool fixture sees no current safe target | orthogonal |
| CT-M0F live-owner fixtures | 2 | fixture assumptions differ from current live-owner/CPS state | orthogonal |
| Passive idempotency fixture | 1 | third reconciliation records one change instead of zero | **unclassified; do not waive** |

The single unclassified failure does not exercise the new direct handoff
reader. Its assertion concerns passive-event reconciliation after an appended
execution outcome. It must be traced to an exact writer and state field before
any expectation is changed.

## Safety conclusion

There is no focused evidence of a direct-handoff regression. The full suite is
not declared green and its failures are not converted into a blanket waiver.
The deployed direct handoff remains protected by its own focused tests and by
the existing safe-deploy truth checks.

## Next actions

1. `V7_PASSIVE_IDEMPOTENCY_RECONCILIATION_DELTA_DISCOVERY_V1` — read-only
   producer/writer trace for the one unclassified idempotency change.
2. Independently, wait only for a natural valid direct-fallback cycle and
   record its timestamps. Do not manufacture a failure or user movement.

## Effects

- Runtime effects: `NONE`.
- Production effects: `NONE`.
- Authority effects: `NONE`.
- CPS unchanged; successor remains
  `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`.
