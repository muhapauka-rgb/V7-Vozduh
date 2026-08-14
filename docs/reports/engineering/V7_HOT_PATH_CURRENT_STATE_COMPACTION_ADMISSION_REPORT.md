# V7 Hot-Path Current-State Compaction — Admission Report

**Mission:** `V7_HOT_PATH_CURRENT_STATE_COMPACTION_ADMISSION_V1`  
**Program:** `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`  
**CPS frontier:** unchanged — `RS6_RUNTIME_PACKAGE_MINIMIZATION` / `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`  
**Verdict:** `NOT_READY_FOR_COMPACTION_OR_CERTIFICATION_FAST_RETURN`

## Scope and evidence

This is a bounded, read-only admission following the deployed
`V7_HOT_PATH_EVENT_LEDGER_BOUNDING_V1` change. It checked the existing
`tools/v7-users-autoswitch` and `tools/v7-service-matrix-refresh-all` owners
and aggregate production state only. No code, Runtime, production routing,
Authority, CPS, service or timer was changed.

| Fact | Evidence | Meaning |
| --- | --- | --- |
| Current Matrix scope reader | `current_failed_source_scope()` uses the existing bounded JSONL-tail reader (2,000 rows / 16 MiB maximum) | The 92 MiB event-ledger full-read defect was already removed by `497b4e06`; a duplicate projection is not justified. |
| Existing compact-state owner | `l3-runtime-state.json` via `tools/v7-users-autoswitch` | This is the existing current-state projection; creating another state source would duplicate ownership. |
| Current L3 size | 27,272,117 bytes | The current projection is no longer compact enough to assume a cheap synchronous load. |
| Historical consumption index | 37,783 `passive_event_consumptions` entries | Exact-once consumption currently retains substantial history in the current-state file. |
| Passive incident projections | 363 total; 25 open | Historical state cannot be discarded by file size alone. |
| Open ordinary scope | 7 passive incident projections | A certification-only shortcut must not starve an older ordinary protection intent. |
| Open unresolved scope | 25 passive incident projections | Their owner-backed re-entry/disposition must be proven before retention or execution-path changes. |

## What the current slow cycle does

The event-only planner service first invokes the passive consumer. For an
already-consumed event that consumer performs the existing exact outcome/scope
reconciliation without entering the Planner. The same service then enters
`consume_service_failure_automation_only`, which constructs
`AutoswitchPlanner`, reconciles closure state, executes `plan()`, produces a
prepared class projection and materializes advisory/OMP evidence.

Live observations show this advisory cycle takes 78.562–115.761 seconds wall
time, 54.239–60.435 seconds CPU time and about 551–581 MiB peak memory while
`active=false` for the *current* ordinary source scope and no Candidate,
Packet, lease, routing mutation or user move occurs.

That is a real hot-consumer contention problem, but it is **not** proof that
Packet, lease, barrier, route apply or verification are slow. Those safety
owners remain unchanged and non-bypassable.

## Admission result

The desired behaviour is valid only under this stronger predicate:

```text
CURRENT_ORDINARY_SCOPE_EMPTY
AND CERTIFICATION_ONLY_TERMINAL_IS_CURRENT
AND ALL_OLDER_ORDINARY_PASSIVE_INTENTS_HAVE_OWNER_BACKED_DISPOSITION
AND NO_READY_EXECUTION_OR_OMP_OBLIGATION_REQUIRES_THE_ADVISORY
```

Only the first predicate is currently evidenced for the observed Matrix
generation. The other predicates are not yet established for the 25 open
passive incident projections, including seven with ordinary scope. Therefore
the following change is **not admitted** yet:

```text
CERTIFICATION_ONLY -> unconditional fast return
```

It could leave an older ordinary incident without the exact reconciliation or
re-entry it still owns.

## Exact next bounded action

Run `V7_HOT_PATH_PASSIVE_INCIDENT_REENTRY_CLASSIFICATION_V1` read-only through
the existing L3/closure owners. For each of the 25 open passive incident
projections, classify only:

```text
CURRENT_ORDINARY_REENTRY_REQUIRED
| CURRENT_CERTIFICATION_RECONCILIATION_REQUIRED
| TERMINAL_OWNER_BACKED
| STALE_OR_INCOMPLETE_EVIDENCE_STOP_SAFE
```

The follow-up may not create a state store, rewrite history, close an incident,
change routing, remove Packet/lease/barrier, or modify CPS. A certification
fast-return implementation is admissible only if the resulting classification
proves the predicate above and preserves exact changed-generation re-entry.

## Effects and delta

| Metric | Result |
| --- | ---: |
| Runtime source files changed | 0 |
| Runtime LOC changed | 0 |
| Services/timers changed | 0 |
| Routing changes | 0 |
| Production effects | `NONE` |
| Authority effects | `NONE` |
| CPS changes | 0 |

