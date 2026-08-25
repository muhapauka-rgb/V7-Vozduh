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

## Publication and controlled Runtime proof

The correction was published as commit `e4106fd647978adf481d78201ed10a183a130fcb` and deployed only through `tools/v7-safe-deploy`, with its explicit `v7-health.service` restart requirement.  Local, GitHub, and Runtime hashes aligned; the health service was active and the old standalone Matrix/Telegram timers remained inactive.

Immediately after restart, the Runtime emitted:

```text
V7_HEALTH_ROLE_PREEMPTED role=other_required
  reason=PREPARED_PROJECTION_FRESHNESS_PRIORITY
V7_HEALTH_ROLE_START role=planner_projection
V7_HEALTH_ROLE_COMPLETE role=planner_projection duration_ms=12621
```

This proves the existing refresh was no longer starved.  One fresh cold controlled Matrix/Polygon transaction then completed automatically through the persistent health consumer.  The synthetic identity was returned to its original isolated source; `v7-health.service` remained active; ordinary-user delta was zero.

| Interval | Before correction | After correction | Change |
| --- | ---: | ---: | ---: |
| persistent consumer entry after T0 | 520.826 ms | 389.255 ms | -25% |
| prepared target validation | 4119.161 ms | 41.150 ms | -99% |
| failure to decision | 7259.000 ms | 1746.435 ms | -76% |
| complete control-plane/kernel cutover | 9664.864 ms | 2696.992 ms | -72% |

The later sample retained exact route/kernel and required-service verification.  Its terminal receipt was `verified_cutover_and_forward_recovery_and_controlled_source_reset_complete`; no `performance_fail` reason was recorded.  This is one valid cold measurement, not a five-sample SLO conclusion.

## Exact next frontier

1. Freeze this bounded arbitration correction: it has removed the measured stale-projection fallback without changing any safety contract.
2. Resume the current HARD_PATH evidence programme on the immutable fingerprint.  Collect the remaining homogeneous controlled cold/warm samples across two Matrix generations; retain every functionally valid slow sample.
3. Do not claim the programme SLO from this single cold result.  If the frozen series exposes a new material residual, report it as a new architecture/evidence decision rather than starting another unbounded micro-patch loop.
