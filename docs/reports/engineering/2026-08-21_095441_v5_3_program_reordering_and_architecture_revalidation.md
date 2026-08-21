# V5.3 T0–T11 — program reordering and architecture revalidation

Date: 2026-08-21 09:54 MSK  
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Scope: reorder the existing V5.3 workstream; no production change.

## Decision

The proposed reordering is accepted and applied to the existing Program. The
workstream now follows:

```text
CURRENT V7 FACTS
→ PROVEN BOTTLENECKS
→ STRONGEST-SYSTEM PATTERNS
→ V7 CANDIDATE ARCHITECTURES
→ POLYGON TOURNAMENT + SCALE TOURNAMENT
→ ARCHITECTURE DECISION
→ IMPLEMENTATION
→ T0→T11 BEFORE/AFTER
→ CONTROLLED/PRODUCTION PROOF
```

The former `TARGET_ARCHITECTURE_REFINED_EXISTING_OWNER_VARIANT` is retained as
one evidence-backed candidate. The former `TARGET_ARCHITECTURE_MODEL_B_PLUS_C`
is also treated as historical candidate input. Neither is the winner of the
reopened comparison.

## Why the change is justified

The current baseline is sufficient to start synthesis and does not require a
new generic provenance investigation:

- the live Matrix cycle is known and completes;
- the full path is about 86 seconds end-to-end in the latest timing evidence;
- cadence can add up to about 15 minutes of waiting;
- the short path is materially cheaper (the bounded caller measurement showed
  74.6% lower elapsed time and 78.6% fewer checks than the full path);
- the downstream synthetic transaction is short compared with Matrix work.

The proven bottlenecks are therefore cadence, serial/full egress traversal and
probe volume—not an unbounded lack of documentation. Provenance remains a
deploy/evidence gate, not a reason to delay architecture selection.

## What changes in the Program

`docs/programs/V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md` now states:

1. L8 forms distinct candidates and selects no winner.
2. L9 runs one common failure matrix for every candidate in Polygon.
3. L10 runs the scale tournament at 7/50/100/1000 egresses.
4. Phase E makes the architecture decision only after L9 and L10 are
   consumed.
5. Phase H implementation starts only after that decision and its safety
   constraints.
6. T0→T11 before/after and controlled/production proof remain post-
   implementation gates.

The tournament must compare the same cases and record T0→T11, probe count,
false-positive/false-negative behavior, recovery, stale/unknown/conflict
handling, CPU/RAM/network, complexity and safety. Existing Matrix, Planner,
CPS, Runtime and routing owners remain unchanged.

## Reuse boundary

The existing Envoy, HAProxy, Google Cloud, FRR/BFD, Cisco, Fortinet and
MikroTik research is reused as a mechanism library. No new broad vendor survey
is required. The next synthesis must map each already-proven V7 bottleneck to:

```text
mature mechanism → reason it fits → existing V7 owner
→ REUSE / ADAPT / REJECT → measurable tournament hypothesis
```

Candidate construction must include the retained existing-owner variant and
real A/B/C alternatives. Role-aware/adaptive behavior is a separate candidate
or dimension only if the measurements prove that A–C cannot cover the gap.

## Production boundary

Production `STOP_SAFE` caused by exact action context, scope or Runtime
provenance is a later implementation/proof-layer condition. It does not block
read-only synthesis, candidate construction or Polygon/scale tournaments. No
route, client, cadence, timer, Matrix owner or Runtime behavior was changed by
this turn.

## Evidence used

- `docs/reports/engineering/2026-08-21_020500_v5_3_t0_t11_timing_breakdown_and_bottleneck.md`
- `docs/reports/engineering/2026-08-21_021500_v5_3_omp_cps_frontier_and_runtime_provenance.md`
- `docs/reports/engineering/2026-08-20_130000_v5_3_matrix_health_phase_c_d_e_decision.md`
- `docs/reports/engineering/2026-08-20_225000_v5_3_system_level_weighted_architecture_decision.md`
- `docs/reports/engineering/2026-08-18_134035_v5_3_phase_c_commercial_health_benchmark_contract.md`
- `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`

## Verification

- Documentation-only change; no code, timer, Matrix, Runtime or route files
  changed.
- `git diff --check` passed.
- `python3 tools/v7-truth-check --continue-omp --json` passed with
  `authority_impact=NONE`, `production_impact=NONE`, `routing_mutation=false`,
  `runtime_mutation=false`, `user_movement=0`; the existing next action remains
  `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`.
- No deploy or client movement was attempted.

## Current position and exact next step

Position: **Block 2 of 6 — PROVEN BOTTLENECKS → MATURE-SYSTEM SYNTHESIS**.

Exact next deliverable: one compact bottleneck-to-pattern synthesis matrix for
cadence delay, serial/full traversal, probe budget, liveness confirmation,
degraded-state handling, target eligibility, recovery/re-admission and
hysteresis. Each row must name the mature mechanism, existing V7 owner,
REUSE/ADAPT/REJECT disposition and the Polygon measurement that can falsify it.

After that matrix is consumed, the next block is **V7 CANDIDATE
ARCHITECTURES**, followed by the common Polygon and scale tournaments. No
architecture implementation is admitted before those blocks and the new Phase
E decision.
