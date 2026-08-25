# V7 prepared-decision freshness: contention correction

**Date:** 2026-08-26  
**Mission block:** bounded safe reduction after the HARD_PATH variance diagnosis.  
**Scope:** existing `v7-health` owner and its existing slow child roles only. No Matrix/Planner/Authority/route-writer/policy/cadence/state-owner change.

## Why this correction is needed

The controlled cold sample after the persistent Matrix handoff was functionally valid and returned the certification identity to its original isolated source.  It was not an SLO pass:

| Measured interval | Result |
| --- | ---: |
| hard T0 to persistent Matrix entry | 520.826 ms |
| prepared target validation | 4119.161 ms |
| failure to decision | 7259.000 ms |
| complete controlled cutover | 9664.864 ms |

The expensive target-validation span reported `PREPARED_CONTROLLED_TARGET_READY`, but only after the existing Planner subprocess fallback (`4103.303 ms`).  The prepared decision was rejected solely because `periodic_quality_rerank_due`; all current scope, Authority, capacity, and mutable checks passed.

## Reproduced Runtime cause

The existing prepared decision has a five-minute maximum reuse window and an existing 30-second `planner_projection` refresh role.  On the 2-vCPU Runtime, that role was repeatedly deferred behind serialized slow observations:

```text
02:29:31..02:32:01  planner_projection deferred
                         (hot_target_other / other_required / deep running)
02:32:18             controlled failure prepared
02:32:25             automatic persistent Matrix consumer starts
                         with projection past its 300-second window
02:32:36             fallback reconstruction completes
```

The scheduler trace contains the matching defer records; the new projection was only written after the controlled incident.  This is a deterministic owner-local starvation condition, not an unsafe reuse request and not an Authority/target-selection defect.

## Correction

When the already-due `planner_projection` role is about to start in the normal serialized Runtime, it now preempts only an existing disposable slow observation (`hot_target_other`, `other_required`, or `deep`).  The interrupted observation runs again on its unchanged cadence.

HARD remains higher priority and still preempts every child after Matrix confirms a failure.  The correction does not change:

- cadence, target eligibility, selection inputs, freshness window, or verifier;
- Matrix/Planner/Authority semantics or state ownership;
- route writing, clients, timers, or any ordinary-user assignment.

It ensures the already mandatory refresh is not indefinitely prevented from meeting its own existing freshness contract.

## Verification before publication

- Focused health-loop suite: **16 passed**.
- The new test proves that a due projection preempts a running disposable slow role and starts; controlled Polygon mode retains its former non-preemptive behavior.
- Syntax compilation and `git diff --check`: passed.

## Exact next frontier

1. Publish and safe-deploy this arbitration-only correction with the explicit existing health-service restart.
2. Prove one ordinary Runtime refresh starts at its due point even if a slow observation is running.
3. Run one fresh certification-only cold scenario.  Credit it only if the prepared decision is current and the full automatic chain preserves all S11 semantics.  Compare the target-validation and T0-to-decision spans with the 4119.161 ms / 7259.000 ms baseline.
4. If the prepared projection is current yet a material multi-second span remains, stop patching and report that next exact residual; do not weaken freshness or S11.
