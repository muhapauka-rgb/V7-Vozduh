# V7 Hot-Path Advisory Planner Substep Profiling — Admission Report

**Mission:** `V7_HOT_PATH_ADVISORY_PLANNER_SUBSTEP_PROFILING_ADMISSION_V1`  
**Mode:** bounded read-only production observation and source mapping  
**CPS current stage / successor:** `RS6_RUNTIME_PACKAGE_MINIMIZATION` / `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`  
**Verdict:** `READY_FOR_DEEP_ADVISORY_SUBSTEP_PROFILE_READ_ONLY`

## Scope

This admission observes only the existing systemd planner cycle and maps the
existing `consume_service_failure_automation_only()` sequence. It does not
start a service, trigger failure, add instrumentation, mutate L3 or routing,
or create a new metric, worker, queue, owner or state source.

## Observed normal cycle

One completed current production cycle was already advisory-only:

| Existing substep | Duration | Meaning |
| --- | ---: | --- |
| Passive event consumer | 14.402 sec | bounded event/L3 reconciliation completed `PASS` |
| Service-failure automation advisory | 61.739 sec | dominant cost |
| OMP consumer | 3.473 sec | follows advisory and returned `NO_PENDING_OBLIGATION` |
| Whole systemd cycle immediately before the observation | 84.987 sec wall / 65.608 sec CPU / 540.5 MiB peak | no route action occurred |

Inside the advisory interval, the existing prepared class-decision projection
was produced after 23.726 sec. Approximately 38.012 sec therefore remained
between prepared decision availability and advisory completion.

The same cycle recorded `execution_allowed=false`, no Candidate, Packet,
lease, runtime mutation, routing mutation or user movement. It contained
certification-only Matrix scope and retained legacy re-entry obligations.

## Existing source sequence

```text
reconcile_bounded_cohort_closure_obligations
→ reconcile_service_failure_execution_outcomes
→ planner.plan
→ build_prepared_class_decision_projection
→ validate_prepared_class_decision_projection
→ materialize_service_failure_automation_advisory
```

The final materialization itself invokes the existing scope reconciler before
selecting a closure and again after writing its advisory obligation. These
operations have legitimate ownership; this admission does not classify any of
them as removable.

## Decision

The next evidence task is legally isolated from legacy cohort disposition:

```text
V7_HOT_PATH_ADVISORY_PLANNER_DEEP_PROFILE_V1
```

It must use existing logs/state and static call mapping to attribute the
approximately 38-second post-decision interval to existing calls, reads and
writes. It may not add runtime instrumentation or execute a synthetic failure.
It must distinguish a cost that is necessary for re-entry safety from an
Engineering/OMP/history projection that can later be deferred through an
existing owner.

No implementation is admitted yet. In particular, planner bypass,
certification fast return, Packet/lease/barrier changes and routing changes
remain prohibited.

## Exact next step for the V7 goal

Run `V7_HOT_PATH_ADVISORY_PLANNER_DEEP_PROFILE_V1` read-only. Its output must
name one measured, existing-owner substep with known callers, consumers,
re-entry impact and a before/after measurement plan. Only that can become the
next bounded optimisation Mission toward `FAILURE → CLIENT MOVED`.

Runtime effects = `NONE`. Production effects = `NONE`. Authority effects =
`NONE`. CPS is unchanged.
