# V7 Hot-Path Cost Tree — Natural Runtime Refresh

**Type:** read-only natural-runtime measurement  
**Verdict:** `CERTIFICATION_ONLY_ADVISORY_WORK_IS_THE_CURRENT_PRIMARY_LATENCY_CANDIDATE`

## Natural observations

Recent production Matrix cycles had no ordinary active source scope and no
execution permission. They reported only `CERTIFICATION_ONLY` failed-source
cohorts and `RECONCILE_CONTROLLED_CERTIFICATION_SCOPE_ONLY`.

| Segment | Natural observation |
| --- | ---: |
| Passive consumer | 12.99–20.92 s |
| Advisory planner total | 57.22–63.15 s; one timeout at 90 s before substep timing was exposed |
| Advisory → prepared decision | 22.82–22.96 s |
| Prepared decision → advisory completion | ~34.4–40.3 s |
| OMP consumer | 2.15–4.73 s, after advisory; no execution obligation |
| Whole planner service wall time | 80.97–120.64 s |

The currently prepared classes all had `execution_allowed=false`. The bounded
executor correctly returned `STOP_SAFE_NO_CURRENT_SERVICE_FAILURE_OBLIGATION`;
there was no Packet, lease, routing apply, user move or Authority expansion.

## Cost tree

```text
Matrix cycle
├─ passive consumer                         13–21 s
├─ advisory planner                         57–63 s
│  ├─ closure/outcome reconciliation
│  ├─ plan and prepared-decision projection 22–23 s
│  └─ advisory materialization              34–40 s
├─ OMP receipt consumer                      2–5 s
└─ executor                                 stop-safe / no action
```

The source entrypoint invokes, in order:

```text
reconcile_bounded_cohort_closure_obligations
→ reconcile_service_failure_execution_outcomes
→ plan
→ prepared_class_decision projection
→ materialize_service_failure_automation_advisory
```

## Current measured refinement

The deployed compact advisory timeline subsequently isolated the repeated
scope scans. One natural baseline contained 12.024 s at entry, 12.789 s
post-plan and 13.103 s after a durable write. The entry result had no consumer
between it and the post-plan reconciliation. It was removed in
`a8be3166` while the two safety rechecks remained; the first post-deploy
receipt contains no entry span and retains a 9.489-s post-plan recheck.

This is a real removed synchronous operation. It is not an end-to-end client
failover result, and it does not authorize removal of either retained recheck.

## Decision

A global `CERTIFICATION_ONLY` fast return is **not admitted**: 28 legacy open
cohorts retain owner-backed re-entry and lack terminal/superseding disposition.
Current Matrix scope cannot replace their individual lineage.

The next admissible optimization is therefore not a generic Planner rewrite
or a certification bypass. It is a bounded read-only consumer proof for the
two retained post-plan/final scope reconciliations: establish whether their
freshness and durable-write consumers can share one result in a specific
semantic branch, without changing legacy re-entry, Packet, lease, barrier,
apply or verification.

## Next step

`V7_HOT_PATH_POST_PLAN_SCOPE_RECONCILIATION_CONSUMER_PROOF_V1`:
map only the post-plan and final scope recheck inputs, writers and consumers;
admit a change only if one has an exact existing-owner replacement. In
parallel, collect a natural **ordinary** service-failure event to measure
`failure → decision → Packet → lease → apply → verify`; no synthetic failure
or user movement is permitted.

## Effects

- Runtime effects: `NONE`.
- Production effects: `NONE`.
- Authority effects: `NONE`.
