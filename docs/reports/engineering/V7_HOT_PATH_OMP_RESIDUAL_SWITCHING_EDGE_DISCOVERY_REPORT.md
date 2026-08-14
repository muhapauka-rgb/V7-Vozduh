# V7 Hot-Path OMP Residual Switching Edge — Discovery Report

**Scope:** read-only post-implementation boundary check  
**Verdict:** `FRESH_PATH_OMP_REMOVED; RECEIPT_BOUND_FALLBACK_REQUIRES_SEPARATE_ADMISSION`

## Answer

OMP must be an Engineering Plane system, not a synchronous requirement for a
client switch. The deployed fresh-obligation path now satisfies that rule:

```text
failure advisory → existing governed executor → Packet / lease / barrier / apply / verify
                                      ↓
                                OMP receipt afterwards
```

No fresh executor argument, Packet, lease, barrier, routing call or verification
step reads an OMP receipt.

## Remaining edge

There is one intentionally preserved legacy/fallback branch:

```text
no fresh advisory obligation
    → existing OMP-consumed receipt
    → service_failure_automation_consumed_execution_handoff
    → existing governed executor
```

It is not the fresh failure path. It exists to recover a scope-matching
exact-once handoff in a later Matrix generation. The bridge verifies the
obligation, receipt, source incident, decision trace and current scope
fingerprint against existing `closure-records.jsonl` and current L3 scope. A
stale or mismatched receipt fails closed.

## Why it cannot be deleted mechanically

The fallback executor receives an obligation only after the bridge proves that
the durable receipt has the active-incident successor. Removing this read now
would turn a known fail-closed recovery boundary into an unproven path. That
would violate the Product Contract and the existing owner boundary.

## Required next bounded step

`V7_HOT_PATH_RECEIPT_BOUND_HANDOFF_DECOUPLING_ADMISSION_V1` must be read-only
first. It must prove whether the existing closure/L3 owners already contain an
equivalent direct, identity-and-scope-bound handoff that the executor can
validate without OMP receipt. It may not create a state store, queue, worker,
Planner, owner or truth source.

Admission is allowed only when all of the following are proven:

1. exact obligation identity and source incident;
2. current source-scope fingerprint and generation;
3. exact-once/re-entry semantics;
4. same fail-closed behavior on stale or mismatched data;
5. Packet/lease/barrier/apply/verify unchanged;
6. OMP still receives an Engineering receipt after execution, never as a
   switching prerequisite.

Until then, the fallback remains isolated and unchanged. This does not reduce
the fresh-path gain already deployed.

## Effects

- Runtime effects: `NONE` (read-only discovery).
- Production effects: `NONE`.
- Authority effects: `NONE`.
- CPS: unchanged; successor remains
  `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`.
