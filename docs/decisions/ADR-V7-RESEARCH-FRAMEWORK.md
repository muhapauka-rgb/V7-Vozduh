# ADR-V7-RESEARCH-FRAMEWORK

Status: Accepted
Date: 2026-06-25
Program: V7.RESEARCH.FRAMEWORK

## Context

V7 already contains research-derived engineering principles, cross-system comparisons, canonical references, and semantic reuse rules.
Those materials guide architectural thinking, but they do not define a permanent repeatable research process.

Without a stable research framework, architectural research can degrade into one-off prompts, over-broad context loading, vendor imitation, or recommendations that create new owners before reuse is proven.

## Decision

Architectural research becomes a permanent governed process rather than one-off prompts.

V7 will use `docs/programs/V7_RESEARCH_FRAMEWORK.md` as the permanent research methodology.
Operators will use `docs/reference/V7_RESEARCH_PROCESS.md` as the compact execution guide for future research.

Research tasks must resolve context first, collect and validate mature production sources, extract universal principles, compare those principles with V7, classify gaps, and update canonical documentation only when durable project meaning changes.

Research Framework is documentation-only.
It does not create runtime behavior, execution behavior, a new planner, new governance, a new truth source, synthetic evidence, apply behavior, floor changes, or user movement.

Need New Owner: FALSE

## Consequences

- Future architectural research starts from a short command such as `Start Research: <topic>`.
- Research recommendations must prove mature production use, purpose, problem solved, V7 equivalent owner, reuse path, extension path, and whether a new owner is required.
- New architecture cannot be recommended before existing-owner extension is proven impossible.
- OMP remains the implementation optimizer.
- Research Framework becomes the knowledge-acquisition methodology.
- Canonical Reference and SYSTEM_MAP remain the durable truth and ownership maps.

## Semantic Reuse Result

Existing V7 documents provided partial coverage through Context Resolver, Engineering Principles, Autonomy Blueprint, Ideal Autonomous Routing Model, Canonical Reference, and OMP semantic reuse gates.
No existing document was the permanent owner for research workflow.

Result:
Extend documentation only.
Need New Owner remains FALSE.

## Duplicate Detector Result

No duplicate planner, governance layer, execution path, truth source, runtime module, or OMP replacement is created.
Research Framework complements existing owners:

- Context Resolver selects research context;
- OMP optimizes implementation;
- Canonical Reference stores durable truth;
- SYSTEM_MAP maps ownership;
- ADRs record decisions.

## Verification

Required verification:

- `tools/v7-truth-check --all --json`
- `tools/v7-convergence-status --json`
