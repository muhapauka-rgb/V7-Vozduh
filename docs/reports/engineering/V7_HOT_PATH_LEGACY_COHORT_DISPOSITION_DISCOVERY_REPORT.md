# V7 Hot-Path Legacy Cohort Disposition — Discovery Report

**Mission:** `V7_HOT_PATH_LEGACY_COHORT_DISPOSITION_DISCOVERY_V1`  
**Mode:** bounded read-only Engineering Plane discovery  
**CPS current stage / successor:** `RS6_RUNTIME_PACKAGE_MINIMIZATION` / `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`  
**Verdict:** `BLOCKED_BY_OWNER_BACKED_COHORT_DISPOSITION_EVIDENCE`

## Scope and reproducibility

Only open `PASSIVE_SERVICE_FAILURE_CAPTURE` cohorts in the existing L3 owner
were evaluated. The analysis read existing Matrix, L3, execution and closure
evidence once; it did not enter Runtime handling and made no write.

| Evidence owner | Rows | SHA-256 |
| --- | ---: | --- |
| Matrix service-failure events | 39,251 | `ba3c50ad4ec6f24a662a703320b336b4baf7a1aaae79bb81fab630eb1ac043ff` |
| Execution events | 24,458 | `474ea1b8fb36a405773839718265ef1f4c4e036f8c5a2d6e5eefd6034d658baf` |
| Closure records | 13,217 | `1df311a3b39d287c7234125347c8ec148b655d3ee05a84e2b554322211b99dd9` |

No raw identity, incident ID or membership list is included in this report.

## Current open-cohort summary

| Property | Result |
| --- | ---: |
| Open passive cohorts | 28 |
| Cohorts with a valid re-entry invariant | 28 / 28 |
| Exact source-event lineage found | 28 / 28 |
| Scope accounting `INCIDENT_SCOPE_ACCOUNTING_BROKEN` | 28 / 28 |
| Baseline unavailable | 21 |
| Available baselines | 15: 1; 24: 3; 34: 3 |
| Latest exact source event `CERTIFICATION_ONLY` | 21 |
| Latest exact source event legacy/empty classification | 7 |
| Exact OMP obligation retained | 28 |

## Causal evidence matrix

An artifact was accepted only where it was causally bound to the same source
incident. Mere artifact presence was not treated as disposition evidence.

| Evidence type | Exact result | Disposition consequence |
| --- | ---: | --- |
| Matrix source event | 28 linked | establishes lineage, not terminality |
| Packet / lease / restore-barrier link | 0 | no governed movement disposition |
| Exact execution record / verified success | 0 | no protected-cohort disposition |
| Recovery or expiry terminal | 0 | no recovery disposition |
| Closure records | 236 linked | `STOP_SAFE_NO_ACTION` / non-executing history; not terminal cohort disposition |
| Explicit exclusion pointers | 3 | insufficient: corresponding accounting remains broken, so they cannot close a cohort |

## Classification

| Classification | Cohorts | Reason |
| --- | ---: | --- |
| `EXACT_PACKET_OR_RECOVERY_LINEAGE` | 0 | No exact verified execution, recovery or expiry terminal exists. |
| `EXPLICIT_LEGACY_EXCLUSION_WITH_POINTER` | 0 | Three pointers exist, but none completes valid scope accounting. |
| `FRESH_MATRIX_GENERATION_SUPERSEDES_INTENT` | 0 | An exact current generation is not a supersession disposition for an open legacy cohort without resolving its historical denominator. |
| `STOP_SAFE_RETAINED_REENTRY` | 28 | Existing successor/re-entry invariant is valid; no owner-backed terminal or superseding disposition exists. |

## Hot-path impact

| Category | Blocks governed failover? | Why | Safe to defer? |
| --- | --- | --- | --- |
| Fresh ordinary scope with exact current generation | Yes | requires the normal decision → Packet → lease → apply path | No |
| Current certification-only observation | Not itself | has no ordinary movement requirement | Only after unrelated legacy re-entry is preserved |
| Open legacy cohort reconciliation | No direct apply, but blocks a global shortcut | its exact disposition remains unknown | No |
| Reports, learning, analytics | No | Engineering Plane work | Yes |

## Fast-return readiness

`READY_FOR_CERTIFICATION_SCOPE_ISOLATION` is not satisfied. The following
required predicate is false for all 28 open cohorts:

```text
NO_PENDING_REENTRY
AND OWNER_BACKED_TERMINAL_OR_SUPERSEDED_STATE
```

The completed bounded event/L3 compaction remains valid. A global planner
bypass, reconciliation skip or certification fast return would be unsafe.

## Exact next step for the V7 goal

The next bounded work is not routing optimisation. It is
`V7_HOT_PATH_LEGACY_COHORT_DISPOSITION_RECONCILIATION_ADMISSION_V1`, limited to
the existing L3/Matrix/closure owners. It must determine whether those owners
already expose a lawful way to materialize, **without inference**, one of the
four disposition classes above. If not, the legal outcome remains
`STOP_SAFE_RETAINED_REENTRY`; no hot-path implementation is admitted.

Runtime effects = `NONE`. Production effects = `NONE`. Authority effects =
`NONE`. No owner, truth source, state store, queue, worker, lifecycle, CPS
field or Runtime behavior changed.
