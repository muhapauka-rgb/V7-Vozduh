# V7 Implementation Program

Status: ACTIVE
Program: `V7.IMPLEMENTATION.PROGRAM`
Phase: IMPLEMENTATION
Architecture Phase: CLOSED
Research Phase: CLOSED
Decision Model: COMPLETE
Runtime Model: COMPLETE
System Architecture: COMPLETE
Need New Owner: FALSE

## Purpose

V7 Implementation Program drives implementation until Production Autonomy.

Architecture is complete.
Research is complete.
Future work is implementation-first.

The program does not redesign architecture, planner, governance, execution, Runtime, truth sources, or evidence sources.
Architecture research may restart only when a real implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP`.

## Operating Question

```text
What implementation gives the highest production leverage right now?
```

Not:

```text
What architecture is missing?
```

## Program Loop

```text
Read OMP
  -> Read Current Program State
  -> Choose highest implementation leverage
  -> Semantic Reuse Audit
  -> Reuse
  -> Extend
  -> Implement
  -> Test
  -> Verify
  -> Truth
  -> Convergence
  -> Certification
  -> Update Current Program State
  -> Update OMP
  -> Continue automatically
```

Stop only at:

- `AUTHORITY_BOUNDARY`
- `REAL_WORLD_LIMIT`
- `UNSAFE_IMPLEMENTATION`
- `FUNDAMENTAL_ARCHITECTURE_GAP`

## Implementation Prioritization Rules

Always choose work in this order:

| Priority | Work type | Meaning |
| --- | --- | --- |
| A | Existing owner implementation | Implement missing production behavior inside an existing owner. |
| B | Existing owner integration | Connect existing owners that already contain the needed behavior. |
| C | Existing owner optimization | Improve safety, clarity, speed, correctness, or operator usefulness inside an existing owner. |
| D | Read-model improvements | Add read-only state needed by existing owners to decide, verify, stop, or learn. |
| E | Testing | Add or improve tests for the implemented behavior. |
| F | Certification | Certify the implemented behavior after tests and verification. |

Never redesign architecture unless implementation evidence proves `FUNDAMENTAL_ARCHITECTURE_GAP`.

## Implementation Classes

Every task must be classified as one primary class:

| Class | Scope |
| --- | --- |
| `IMPLEMENT_RUNTIME` | Runtime lifecycle, wakeup, stop, idempotency, verification, rollback, OMP notification, or runtime preview behavior. |
| `IMPLEMENT_BACKGROUND` | Background knowledge, intelligence, trust, suitability, prediction, service, route, capacity, or evidence processing. |
| `IMPLEMENT_READ_MODEL` | Read-only surfaces for decisions, stop reasons, safety, authority, verification, learning, or operator visibility. |
| `IMPLEMENT_TEST` | Tests, fixtures, regression coverage, state-machine coverage, or safety/idempotency coverage. |
| `IMPLEMENT_VERIFICATION` | Verification checks, convergence checks, readiness checks, post-action validation, or truth-safe verification. |
| `IMPLEMENT_OBSERVABILITY` | Lifecycle ids, stages, stop reasons, audit traces, or operator-visible non-truth-source observability. |
| `IMPLEMENT_UI` | Operator-facing UI over existing truth/read models. |
| `IMPLEMENT_DOCUMENTATION` | Documentation required by implemented behavior. |
| `IMPLEMENT_CERTIFICATION` | Certification after implementation, tests, truth, and convergence. |

## Implementation Optimizer

Implementation optimizer maximizes Production Leverage.

Production Leverage is the expected gain in production autonomy, safety, verifiability, learning, operator effectiveness, or implementation readiness per unit of risk and effort.

The optimizer must consider:

1. current bottleneck;
2. current reality limit;
3. current authority boundary;
4. existing owner reuse;
5. implementation safety;
6. testability;
7. reversibility;
8. truth/convergence impact;
9. whether the task moves V7 toward Production Autonomy.

## Current Highest Implementation Leverage Task

| Field | Value |
| --- | --- |
| Task | `IMPLEMENT_RUNTIME_READONLY_LIFECYCLE_PREVIEW` |
| Class | `IMPLEMENT_RUNTIME` |
| Exact owner | Governed Canary Knowledge-Gated Dry-Run Cycle / Runtime Model composition |
| Exact module | `admin_core/operator_execution_pipeline.py::governed_canary_knowledge_gated_dry_run_cycle` |
| Exact files | `admin_core/operator_execution_pipeline.py`, `tools/v7-governed-canary-dry-run-cycle`, focused tests for governed dry-run runtime lifecycle output |
| Production leverage | Converts completed Runtime Model into read-only executable lifecycle output through an existing owner. |
| Why first | It is the first implementation that moves V7 from architecture-complete to runtime-implementation-ready without apply, user movement, daemon, timer, planner redesign, governance redesign, execution redesign, or truth-source creation. |
| Expected maturity gain | High production leverage; no direct autonomy-floor increase until real outcomes exist, but it makes the exact runtime path implementable, testable, idempotent, and certifiable. |

## Expected Implementation Order

1. `IMPLEMENT_RUNTIME_READONLY_LIFECYCLE_PREVIEW`
2. `IMPLEMENT_TEST` for lifecycle state machine, stop conditions, idempotency key, stale packet, duplicate work, and OMP notification fields.
3. `IMPLEMENT_VERIFICATION` for read-only runtime preview verification and truth/convergence certification.
4. `IMPLEMENT_OBSERVABILITY` for lifecycle ids, stage, owner, input generation, stop reason, authority, packet freshness, verification, rollback, outcome, and learning status.
5. `IMPLEMENT_RUNTIME` manual authority-gated invocation preview, still no apply.
6. Only after explicit approval: bounded execution integration through existing owners.

## Safety Boundary

This program does not authorize:

- restore-barrier writes;
- runtime apply;
- user movement;
- rollback apply;
- daemon or timer enablement;
- event consumer mutation;
- authority expansion;
- floor changes;
- synthetic evidence;
- new planner, governance, execution, storage, runtime owner, or truth source.

## Completion Rule

Implementation work finishes only when:

1. the existing owner is reused or a real `FUNDAMENTAL_ARCHITECTURE_GAP` is proven;
2. code is implemented in the existing owner;
3. tests pass;
4. verification passes;
5. truth passes;
6. convergence passes;
7. certification is recorded when required;
8. Current Program State is updated;
9. OMP is updated only if optimizer meaning changed.
