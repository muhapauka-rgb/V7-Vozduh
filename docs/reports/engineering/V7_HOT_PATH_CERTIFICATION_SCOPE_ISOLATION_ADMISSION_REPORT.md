# V7 Hot-Path Certification-Scope Isolation — Admission Report

**Mission:** `V7_HOT_PATH_CERTIFICATION_SCOPE_ISOLATION_V1`  
**Mode:** bounded admission only; no implementation  
**CPS current stage / successor:** `RS6_RUNTIME_PACKAGE_MINIMIZATION` / `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`  
**Verdict:** `STOP_SAFE_NOT_READY`

## Scope

This admission consumes the existing Hot-Path baseline, current-state
compaction, source-linkage and legacy-scope reports. It inspected only the
existing L3, Matrix-event, closure and execution owners. No L3/Matrix/event
record, Packet, lease, barrier, route, service, timer, CPS field or Authority
was changed.

## Current hot path and responsibility boundary

| Step | Existing owner | Hot-path role | Admission result |
| --- | --- | --- | --- |
| Failure detection / Matrix event | Matrix owner | required source observation | retained |
| L3 incident state | `tools/v7-users-autoswitch` | required re-entry and scope guard | retained |
| Planner advisory | existing Autoswitch Planner | not proven necessary when an exact terminal has no ordinary action | candidate for future isolation only |
| Packet / lease / barrier | existing governed execution owners | required whenever an executable move exists | non-bypassable |
| Apply / verify | existing routing owners | required whenever an executable move exists | non-bypassable |

The measured slow planner cycles remain advisory in the observed situation:
they create no Candidate, Packet or lease and perform no routing mutation.
That does not by itself authorize a fast return.

## Current passive-incident evidence

| Property | Current result |
| --- | ---: |
| Passive L3 incidents | 365 |
| Terminal incidents | 338 |
| Open incidents | 27 |
| Open incidents with valid re-entry invariant | 27 / 27 |
| Open incidents with explicit scope classification | 0 / 27 |
| Open incidents with `INCIDENT_SCOPE_ACCOUNTING_BROKEN` | 27 / 27 |
| Open incidents with unresolved scope | 27 / 27 |
| Exact verified packet success for those open incidents | 0 |
| Recovery / expiry terminal for those open incidents | 0 |

The existing current Matrix observation may be `CERTIFICATION_ONLY`, but that
fact is not an incident-level disposition for the open legacy cohorts. The
existing source-linkage evidence also proves that a current observation must
not be substituted for an older incident without exact lineage.

## Fast-return safety proof

The requested fast return requires all of the following:

```text
EXACT_CURRENT_MATRIX_INCIDENT_LINK
AND CERTIFICATION_ONLY_CONFIRMED
AND NO_ORDINARY_AFFECTED_USERS
AND NO_OPEN_ORDINARY_OR_LEGACY_REENTRY_OBLIGATION
AND NO_PENDING_OMP_CONSUMER
AND NO_PACKET_OR_LEASE_OR_APPLY_REQUIRED
```

The fourth predicate is false: all 27 current records retain an existing
re-entry obligation and unresolved/broken scope accounting. The final three
execution predicates therefore cannot be inferred as true. A global
`CERTIFICATION_ONLY -> skip planner` branch is rejected.

## Ordinary versus certification separation

| Work item | Hot-path required now? | Why | Owner | Safe to defer? |
| --- | --- | --- | --- | --- |
| Fresh ordinary failure with exact current scope | Yes | must retain normal governed decision and apply path | existing Matrix / Planner / execution owners | No |
| Exact terminal certification-only incident with no legacy re-entry | Potentially no | no ordinary movement or executable obligation | existing consumer only | Not yet proven for this state |
| Historical/legacy incident reconciliation | No direct route apply, but required before shortcut | preserves cohort disposition and future re-entry | existing L3 / closure owners | No until disposition exists |
| Reports, learning and analytics | No | engineering evidence, not route application | existing Engineering owners | Yes |

## Required next bounded work

`V7_HOT_PATH_LEGACY_COHORT_DISPOSITION_DISCOVERY_V1` — read-only lookup of
existing Matrix, closure and execution evidence for each open legacy cohort.
It must emit compact pointers only and classify each record as:

```text
EXACT_PACKET_OR_RECOVERY_LINEAGE
| EXPLICIT_LEGACY_EXCLUSION_WITH_POINTER
| FRESH_MATRIX_GENERATION_SUPERSEDES_INTENT
| STOP_SAFE_RETAINED_REENTRY
```

Only after every record relevant to a prospective shortcut has an
owner-backed disposition can `V7_HOT_PATH_CERTIFICATION_SCOPE_ISOLATION_V1`
receive an implementation admission. Its future validation plan must measure
event publication, decision readiness, apply start and verification completion
separately; reduced state size alone is not a failover-latency claim.

## Effects

Runtime effects = `NONE`. Production effects = `NONE`. Authority effects =
`NONE`. No new owner, truth source, state store, queue, worker or lifecycle
was created. CPS is unchanged.
