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
| Advisory planner total | 57.22–63.15 s; one timeout at 90 s |
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

## Decision

The next admissible optimization is not a generic Planner rewrite. It is a
bounded certification-only fast-return: when the existing Matrix owner proves
there are no ordinary affected users, no fresh/legacy/direct handoff and no
Packet/lease/apply obligation, it must return the existing certification
re-entry work without running full advisory materialization in the synchronous
Matrix cycle.

This must preserve re-entry, current scope lineage and the existing controlled
certification owner. It may not classify `CERTIFICATION_ONLY` from a stale
historical row or treat zero current users as an incident closure.

## Next step

`V7_HOT_PATH_CERTIFICATION_ONLY_FAST_RETURN_ADMISSION_V1`:
prove the exact current-owner predicate and migration/rollback contract before
implementing any early return.

## Effects

- Runtime effects: `NONE`.
- Production effects: `NONE`.
- Authority effects: `NONE`.
