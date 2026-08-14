# V7 Hot-Path Direct Handoff Invariant — Discovery Report

**Mission:** `V7_HOT_PATH_DIRECT_HANDOFF_INVARIANT_DISCOVERY_V1`  
**Type:** read-only existing-owner analysis  
**Verdict:** `NO_EXISTING_DIRECT_HANDOFF_PREDICATE; MINIMAL_EXISTING_L3_PROJECTION_EXTENSION_REQUIRED`

## Question

Can the receipt-bound fallback invoke the existing governed executor without
reading an OMP receipt, while preserving identity, current scope, exact-once
and fail-closed behavior?

## Proven current data model

| Invariant | Current owner and field | Available without OMP receipt? |
| --- | --- | --- |
| Obligation identity | closure obligation `automation_obligation_id` | yes |
| Current semantic revision | closure obligation `automation_consumption_fingerprint` | yes |
| Current scope/accounting | existing L3 incident projection | yes |
| Active incident state | existing L3 incident projection | yes |
| Exact-once consumption of this revision | OMP receipt `closure_state=OMP_CONSUMED` | no |
| Active drain successor for this revision | OMP receipt `next_action` | no |
| Atomic receipt → L3/CPS reconciliation | `consume_service_failure_automation_frontier` | no |

The L3 `service_failure_automation_obligations` projection is not an equivalent
handoff contract: it stores only `status`, `source_incident_id`,
`classification` and `updated_at`. The linked incident declares the OMP
consumer and OMP-lock re-entry explicitly. It does not retain the consumption
fingerprint, a direct successor, or a linearization/consumption state.

## Decision

There is no existing deterministic `DIRECT_HANDOFF_READY` predicate. Reading
only closure obligation plus L3 scope would lose the proof that this semantic
revision has been consumed once and authorized for the active-incident drain.
The result is therefore `NOT_READY_FOR_OMP_FALLBACK_REMOVAL`.

## Minimal safe design boundary

The only admissible future implementation is an extension of the **existing L3
runtime-state projection owner**. It must compactly carry the existing
obligation fingerprint, the active-drain successor and a monotonic
consumption/execution status under the existing closure lock. It must be
derived from the existing closure obligation and current L3 scope; it is not a
new truth source, queue, worker, registry, Planner or Authority.

The implementation must prove equivalence to the current receipt-bound join:

```text
same identity + same fingerprint + ACCOUNTED current scope + OPEN incident
    + existing-owner exact-once state + active-drain successor
    → direct executor handoff
```

Any missing, stale or inconsistent field must produce the current fail-closed
result and force fresh Matrix revalidation. Packet, lease, restore barrier,
apply and verify remain executor-owned and unchanged.

## Exact next step

`V7_HOT_PATH_EXISTING_L3_DIRECT_HANDOFF_CONTRACT_ADMISSION_V1`:
prepare a bounded implementation contract for that existing L3 projection
extension. Required before any code edit: consumer migration proof, atomic
lock/write order, interruption recovery, existing receipt compatibility,
rollback, and source-order plus state-fixture tests. It must not alter CPS
frontier or launch routing changes.

## Effects

- Runtime effects: `NONE`.
- Production effects: `NONE`.
- Authority effects: `NONE`.
- CPS remains unchanged with successor
  `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`.
