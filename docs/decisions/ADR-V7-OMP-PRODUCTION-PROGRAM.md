# ADR-V7-OMP-PRODUCTION-PROGRAM

Status: Accepted
Date: 2026-06-25
Program: `V7.OMP.FINAL.PRODUCTION_PROGRAM`

## Context

V7 Architecture Phase is complete.
Research Phase is complete.
Decision Model is complete.
Runtime Model is complete.
System Architecture is complete.

V7 already has OMP, Current Program State, Decision Model, Runtime Model, System Architecture, Research Framework, Canonical Reference, and SYSTEM_MAP.

Future work must be implementation and authority evolution only unless real implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP`.

Creating more roadmap documents would duplicate OMP and risk phase-first execution returning.

## Decision

OMP becomes the permanent production operating program and single execution program for V7.

The complete autonomy roadmap and production maturity ladder live inside OMP.

Future work proceeds through:

1. `Continue OMP`;
2. `Approve packet`;
3. `Approve authority expansion`.

OMP owns:

- production maturity ladder;
- highest implementation leverage selection;
- implementation loop;
- authority evaluation;
- continuous optimization;
- research-to-implementation gate;
- Current Program State pointer;
- allowed stop conditions.

Authority expansion is never automatic.

OMP may recommend authority expansion only after certified outcomes.

Operator approval or certified policy approval is required before expansion.

## Consequences

- No additional roadmap documents are required.
- Implementation Program and Implementation Model remain supporting references under OMP.
- Research changes implementation only through Research -> Decision Model -> OMP -> Implementation.
- Research never creates architecture directly.
- Architecture changes require real implementation evidence proving `FUNDAMENTAL_ARCHITECTURE_GAP`.
- Otherwise V7 must reuse, extend, and implement through existing owners.
- OMP continues until `AUTHORITY_BOUNDARY`, `REAL_WORLD_LIMIT`, `UNSAFE_IMPLEMENTATION`, or `FUNDAMENTAL_ARCHITECTURE_GAP`.

## Forbidden

This ADR does not authorize:

- runtime implementation;
- daemon or timer enablement;
- restore-barrier writes;
- runtime apply;
- user movement;
- rollback apply;
- authority expansion;
- planner redesign;
- governance redesign;
- execution redesign;
- new truth source;
- synthetic evidence;
- new owner creation.

## Affected Modules

- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/programs/V7_IMPLEMENTATION_PROGRAM.md`
- `docs/reference/V7_IMPLEMENTATION_MODEL.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`

## Verification

Required verification:

- `tools/v7-truth-check --all --json`
- `tools/v7-convergence-status --json`

No runtime mutation, no apply, and no user movement.
