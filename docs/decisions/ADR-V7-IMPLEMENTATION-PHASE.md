# ADR-V7-IMPLEMENTATION-PHASE

Status: Accepted
Date: 2026-06-25
Program: `V7.IMPLEMENTATION.PROGRAM`

## Context

V7 Architecture Phase is complete.
Research Phase is complete.
Decision Model is complete.
Runtime Model is complete.
System Architecture is complete.

The final system architecture verdict is:

```text
ARCHITECTURE_COMPLETE
```

Remaining architectural weaknesses: `0`.
Need New Owner: `FALSE`.

Future work must stop re-asking architecture questions and start implementing production leverage through existing owners.

## Decision

Future work is implementation-first.

OMP becomes an implementation-first optimizer.
The operating question changes to:

```text
What implementation gives the highest production leverage right now?
```

Architecture changes require implementation evidence proving `FUNDAMENTAL_ARCHITECTURE_GAP`.

## Consequences

- No more architecture research unless implementation proves a real `FUNDAMENTAL_ARCHITECTURE_GAP`.
- No architecture redesign.
- No planner redesign.
- No governance redesign.
- No execution redesign.
- No Runtime redesign.
- No new truth source.
- No synthetic evidence.
- OMP optimizes Production Leverage instead of Architectural Completeness.
- Implementation tasks must be classified before work begins.
- Existing owner implementation, integration, and optimization come before read-model improvements, tests, and certification.

## Current Highest Implementation Leverage

| Field | Value |
| --- | --- |
| Task | `IMPLEMENT_RUNTIME_READONLY_LIFECYCLE_PREVIEW` |
| Class | `IMPLEMENT_RUNTIME` |
| Owner | Governed Canary Knowledge-Gated Dry-Run Cycle / Runtime Model composition |
| Module | `admin_core/operator_execution_pipeline.py::governed_canary_knowledge_gated_dry_run_cycle` |
| Files | `admin_core/operator_execution_pipeline.py`, `tools/v7-governed-canary-dry-run-cycle`, focused tests for governed dry-run lifecycle output |
| Why first | It implements the completed Runtime Model as a read-only lifecycle preview inside an existing owner, preserving no-apply/no-movement authority boundaries. |
| Expected maturity gain | High production leverage; it turns architecture-complete Runtime into implementable, testable, certifiable runtime behavior without runtime mutation. |

## Forbidden

This ADR does not authorize:

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

## Affected Modules

- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/programs/V7_IMPLEMENTATION_PROGRAM.md`
- `docs/reference/V7_IMPLEMENTATION_MODEL.md`
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`

## Verification

Required verification:

- `tools/v7-truth-check --all --json`
- `tools/v7-convergence-status --json`

No runtime mutation, no apply, and no user movement.
