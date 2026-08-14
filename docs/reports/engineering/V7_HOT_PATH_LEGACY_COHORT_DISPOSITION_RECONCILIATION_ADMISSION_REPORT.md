# V7 Hot-Path Legacy Cohort Disposition Reconciliation — Admission Report

**Mission:** `V7_HOT_PATH_LEGACY_COHORT_DISPOSITION_RECONCILIATION_ADMISSION_V1`  
**Mode:** bounded read-only admission  
**CPS current stage / successor:** `RS6_RUNTIME_PACKAGE_MINIMIZATION` / `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`  
**Verdict:** `STOP_SAFE_NO_EXISTING_OWNER_BACKED_DISPOSITION_PATH`

## Question

Do existing L3, Matrix and closure owners already expose a lawful way to
materialize a terminal or superseded disposition for each open legacy cohort,
without inferring membership from missing history?

## Existing lawful mechanisms

| Existing owner path | Required predicate | Current result |
| --- | --- | --- |
| `reconcile_service_failure_execution_outcomes()` | exact causal Packet/execution feedback with verified result | no exact execution records for the open cohorts |
| `_reconcile_recovered_service_failure_intents()` | exact recovery terminal from the closure owner | no recovery or expiry terminal exists |
| `_reconcile_incident_scope_accounting()` legacy certification exclusion | current all-certification cohort plus already-protected users exactly equals immutable baseline | not satisfied; 21 cohorts lack a baseline and known baselines do not equal the current cohort |
| `_materialize_passive_incident_projection()` source-scope rotation | newer owner-backed scope for the same source incident with an accountable denominator | cannot turn broken/missing legacy denominator into terminality |

These are the only discovered existing materialization paths. Each preserves
the fundamental safety law: a missing baseline, absent current user or current
certification-only observation is not a cohort disposition.

## Admission evidence

The current read-only inventory contains 28 open cohorts. All retain valid
re-entry and exact source-event lineage. Their scope accounting is broken;
21 lack a reconstructible baseline, while the remaining known historical
baselines (15, 24 and 34) do not equal the current 11-user certification
cohort. No exact packet, lease, restore-barrier, verified execution, recovery
or expiry lineage is available.

Consequently no record meets:

```text
EXACT_PACKET_OR_RECOVERY_LINEAGE
| EXPLICIT_LEGACY_EXCLUSION_WITH_POINTER
| FRESH_MATRIX_GENERATION_SUPERSEDES_INTENT
```

All remain `STOP_SAFE_RETAINED_REENTRY`.

## Decision

No implementation Mission is admitted. Adding a new automatic disposition
rule would require a new semantic decision about historical cohort ownership;
it cannot be framed as a hot-path performance refactor or inferred from the
current Matrix state. The existing owners correctly fail closed.

## Exact next step for the V7 goal

Continue performance work only on a separately provable synchronous cost that
does not depend on disposing these cohorts. The next candidate must satisfy:

```text
EXISTING_OWNER
AND KNOWN_CONSUMERS
AND NO_CHANGE_TO_LEGACY_REENTRY
AND MEASURABLE_FAILURE_TO_DECISION_LATENCY_DELTA
```

The bounded event read and L3 compaction already meet that standard. The next
candidate should be an admission to profile the remaining advisory planner
substeps and identify a cost that can be removed while all 28 re-entry paths
continue unchanged; it must not bypass planner globally or implement a
certification fast return.

Runtime effects = `NONE`. Production effects = `NONE`. Authority effects =
`NONE`. No owner, truth source, state store, queue, worker, lifecycle, CPS
field or Runtime behavior changed.
