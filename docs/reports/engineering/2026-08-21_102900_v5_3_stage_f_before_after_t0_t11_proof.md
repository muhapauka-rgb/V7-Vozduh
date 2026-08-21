# V5.3 T0–T11 — Stage F before/after proof

Date: 2026-08-21 10:29 MSK  
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Stage: **F — before/after measurement**  
Status: `CONTROLLED_DELTA_PROVEN; PRODUCTION_DELTA_NOT_CLAIMED`

## Compared paths

**Before:** full Matrix observation for the selected source/target channels,
14 services per egress, with the existing full result as canonical.

**After candidate:** selected B+C path: exact required-service subset under the
existing Matrix owner, passive escalation through the same Matrix event path,
then the unchanged full Matrix comparison/fallback.

No production route or user was changed. The controlled caller used the actual
existing selection → Matrix refresh → writer → full confirmation chain.

## Measured delta

| Metric | Before/full | After short path | Delta | Evidence class |
| --- | ---: | ---: | ---: | --- |
| Required checks for 2 selected egresses | 28 | 6 | `-78.6%` | controlled caller Polygon |
| Caller elapsed time | 265.157 ms | 67.306 ms | `-74.6%` | bounded caller Polygon |
| Direct Matrix probe time | 49.868 ms | 21.868 ms | `-56.1%` | isolated Matrix Polygon |
| Synthetic governed Candidate→T11 fixture | 23.675 ms | not comparable | — | controlled fixture only |
| Latest production full Matrix lifecycle | 85.675 s | not enabled | — | production observation |
| Planned cadence wait | 15 min + up to 60 s jitter | unchanged | `0%` | production configuration |

The short path reduces decision-critical work, but the full Matrix still runs
and remains the final canonical observation. Therefore the measured delta is a
probe-cost/controlled-caller result, not yet a production T0→T11 recovery gain.

## Safety and correctness delta

- healthy short/full required-service verdicts agreed;
- required-service failure agreed in full and short Matrix;
- methodology-limited HTTP response remained non-failure;
- deliberate short/full disagreement forced full fallback and blocked action;
- stale/unknown state stopped before packet/apply;
- target readiness stayed separate from source health;
- ordinary scope excluded certification identities;
- post-switch verification and rollback planning remained in the path;
- `users_moved=0`, `routing_mutation=false`, `runtime_mutation=false`.

## What this proves

The selected architecture has a repeatable controlled benefit: fewer decision-
path probes and lower bounded caller time while preserving full fallback and
fail-closed gates. The full production Matrix cycle remains dominated by
serial egress traversal and cadence; the B+C path has not yet been admitted as
an automatic production consumer.

## What remains unproven

- a natural production failure from T0 through actual client T11 recovery;
- production short-path duration distribution under real remote endpoints;
- production CPU/RAM/network impact after consumer migration;
- exact ordinary production source/target action context at the time of a
  failure;
- production equivalence over a representative failure history.

These are Stage G evidence requirements. They are not manufactured in
Polygon and are not credited from the controlled numbers above.

## Exact next step and boundary

Proceed to Stage G with read-only production observation and existing CPS/OMP
consumers. If no natural ordinary failure and no coherent exact action/scope
context are available, retain `STOP_SAFE`, record the blocker and keep the
selected full fallback. Do not enable automatic FAST or move clients merely
to close the report.

## Verification

- Stage C/D candidate harness: `5/5 PASS`.
- Existing Matrix comparison + governed pipeline regression: `56/56 PASS`.
- Existing caller comparative-preflight suite: exit code `0`.
- No production mutation, deploy or client movement.
