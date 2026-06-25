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

Supersession note:
`docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` Version `4.0` is the single permanent production execution program for V7. This file remains a supporting implementation reference under OMP and must not be used as a separate roadmap authority.

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

Current HIL is volatile state and lives in `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

This supporting reference must not preserve an independent current-task queue.

## Expected Implementation Order

Expected implementation order is recalculated by OMP from Current Program State after every certification and authority evaluation.

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
