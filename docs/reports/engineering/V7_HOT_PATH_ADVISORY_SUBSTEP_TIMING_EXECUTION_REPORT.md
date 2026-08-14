# V7 Hot-Path Advisory Substep Timing — Execution Report

**Mission:** `V7_HOT_PATH_ADVISORY_SUBSTEP_TIMING_V1`  
**Program / CPS frontier:** unchanged — `RS6_RUNTIME_PACKAGE_MINIMIZATION` → `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`  
**Verdict:** `IMPLEMENTED_AWAITING_NATURAL_OBSERVATION`

## Why this change

Natural production observations already prove that advisory work consumes
57–63 seconds, with 34–40 seconds after the prepared decision exists. Static
mapping showed several distinct operations in that interval, but not which one
dominates. Changing or bypassing any of them before measuring it would risk
legacy re-entry correctness.

The existing `AutoswitchPlanner` already emits a monotonic in-process
performance timeline. This Mission extends that existing output only; it adds
no profiler, log, state projection, owner, service, timer, queue, registry or
truth source.

## Change performed

`tools/v7-users-autoswitch` now emits existing-owner monotonic spans for the
advisory entry and materialization sequence:

```text
bounded closure reconciliation
→ entry scope reconciliation
→ plan and decision construction
→ prepared-decision projection and validation
→ shadow outcome reconciliation
→ pre-obligation scope reconciliation
→ L3 + closure-history load
→ passive candidate selection
→ obligation semantic construction
→ durable advisory projection materialization
→ final scope reconciliation
```

`consume_service_failure_automation_only()` returns this existing performance
timeline in its normal JSON result. The existing Matrix lifecycle projection
then retains only compact scalar advisory spans (stage, owner, parent, duration
and status). It deliberately excludes monotonic timestamps, raw child output,
identities and history. The spans are observational and use
`time.monotonic_ns`; they do not affect decision selection, obligation
semantics, re-entry, Packet, lease, barrier, apply, routing or verification.

## Safety and validation

| Check | Result |
| --- | --- |
| In-memory source compilation | PASS |
| Exact advisory materialization timing-sequence unit test | PASS |
| Compact Matrix lifecycle timing-projection test | PASS |
| Two existing service-failure test modules | 152 / 167 PASS; 15 existing unrelated CPS/legacy-fixture failures remain | 
| New owner / truth source / runtime dependency | NONE |
| CPS change | NONE |

The 15 broader-suite failures are the previously recorded fixture/CPS frontier
mismatches plus one pre-existing passive idempotency delta. This Mission does
not change their code path or waive them.

## Before / after / delta

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Advisory post-decision aggregate latency | 34.4–40.3 s | awaiting a natural cycle | not yet claimed |
| Observable materialization substeps | aggregate only | 8 named materialization spans + 4 entry spans | +12 evidence fields in existing output |
| Decision / Packet / lease / routing semantics | existing | unchanged | 0 |
| New files / modules / services / timers | 0 | 0 | 0 |

## Effects

- **Runtime behavior:** unchanged except bounded observational timing in the
  existing advisory JSON output.
- **Production routing effect:** `NONE`.
- **Authority effect:** `NONE`.
- **OMP role:** unchanged; no OMP dependency has been added to switching.

## Exact next step

Let existing normal Matrix/planner cycles produce the new timing output, then
classify the single largest post-decision substep. Only an existing-owner,
consumer-preserving reduction with a rollback and residue plan may become the
next implementation Mission. A global certification-only early return remains
blocked by the 28 owner-backed legacy re-entry cohorts.
