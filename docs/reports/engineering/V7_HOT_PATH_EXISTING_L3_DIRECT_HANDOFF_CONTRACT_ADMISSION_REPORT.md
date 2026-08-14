# V7 Hot-Path Existing L3 Direct Handoff Contract — Admission Report

**Mission:** `V7_HOT_PATH_EXISTING_L3_DIRECT_HANDOFF_CONTRACT_ADMISSION_V1`  
**Verdict:** `READY_FOR_BOUNDED_IMPLEMENTATION`

## Admitted objective

Remove the OMP receipt as a prerequisite for the **receipt-bound fallback**
only. The implementation may extend the existing L3 incident projection under
the existing `closure-records.lock` so it contains an equivalent compact direct
handoff proof. It must not create a new state source, owner, queue, worker,
Planner, CPS lifecycle, Packet, lease, barrier or routing path.

## Exact scope

| Component | Permitted responsibility change |
| --- | --- |
| `tools/v7_sync_lib.py` | derive and validate the direct compact handoff projection from existing closure obligation + L3 incident state; preserve legacy OMP receipt reader |
| `tools/v7-users-autoswitch` | populate the already-existing L3 obligation/incident projection with direct handoff fields under its existing atomic write path |
| `tools/v7-service-matrix-refresh-all` | prefer a valid direct handoff when no fresh obligation exists; retain legacy receipt fallback if direct proof is absent |
| focused existing unit tests | fixtures for exact-match, stale, interrupted and legacy receipt behavior |

`tools/v7-truth-check --consume-service-failure-automation-only` remains an
Engineering Plane compatibility consumer, but is not called before either
fresh or direct-fallback execution after migration.

## Direct handoff contract

The existing L3 incident may be considered `DIRECT_HANDOFF_READY` only when
all values are present and mutually equal:

```text
obligation_id
automation_consumption_fingerprint
source_incident_id
incident_key
situation_id
decision_trace_id
current_source_scope.affected_scope_fingerprint
current_source_scope.status = ACCOUNTED
current_source_scope.unresolved_scope_count > 0
incident_state = OPEN
next_action = CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN
direct_handoff_state = READY
```

The direct state must be derived while `closure-records.lock` is held and
persisted by the existing atomic L3 write. A missing, stale, mismatched,
interrupted or previously executed projection returns `NO_CURRENT_DIRECT_HANDOFF`
and leaves the present legacy receipt-bound bridge unchanged.

## Required migration and compatibility

1. Fresh obligation behavior remains executor → OMP receipt after execution.
2. Direct fallback uses only a valid current direct L3/closure projection.
3. Legacy `OMP_CONSUMED` receipt fallback remains readable while historical
   records exist; it is not deleted or reinterpreted.
4. The direct projection must not invoke CPS persistence or OMP continuation.
5. Packet/lease/restore-barrier/apply/verify remain exclusively in the existing
   governed executor.

## Validation and rollback

Required proofs before closure:

- direct valid projection reaches the same executor obligation as the legacy
  receipt-bound bridge;
- stale fingerprint, changed scope, recovered incident, missing lock-created
  projection and duplicate state all fail closed;
- legacy receipt handoff still works without direct fields;
- source-order proof: no `run_service_failure_omp_consumer` before fresh or
  direct executor invocation;
- compile and focused unit suite pass;
- no CPS, Authority or routing behavior change in fixture validation.

Rollback is one implementation commit revert followed by existing safe deploy.

## Admission boundaries

This admission authorizes a single bounded implementation Mission only. It does
not authorize any generic OMP removal, CPS rewrite, artificial failure, user
movement, routing mutation or physical runtime-package minimization.

## Effects at admission

- Runtime effects: `NONE`.
- Production effects: `NONE`.
- Authority effects: `NONE`.
- CPS unchanged; successor remains
  `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`.
