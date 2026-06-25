# ADR-V7-RESEARCH-STANDARD

Status: Accepted
Date: 2026-06-25
Program: V7.RESEARCH.STANDARD

## Context

V7 created a permanent Research Framework to make architectural research repeatable instead of one-off prompts.
The completed World-Class Decision Model research proved the next required standard: future research must not stop at general principles.
It must extract engineering laws, compare mature system families, map V7, classify gaps, prove reuse, and produce canonical recommendations.

## Decision

Every future architectural research must follow the same research methodology and output structure.

No research may finish without:

- Universal Engineering Laws;
- Cross-System Comparison Matrix;
- V7 Mapping;
- Gap Classification;
- Reuse Analysis;
- Canonical Recommendations.

No research may finish without engineering laws and comparison matrix.

The Research Framework owns:

- research workflow;
- engineering law extraction;
- comparison matrix generation;
- V7 mapping process.

## Consequences

- Future research has one permanent output structure.
- Research cannot finish with only narrative recommendations.
- Engineering laws must be observed across multiple mature systems and must not be invented.
- Cross-system comparison becomes mandatory before V7 recommendations.
- V7 reuse analysis remains mandatory before new architecture is proposed.
- Need New Owner remains `FALSE` unless a future research proves `FUNDAMENTAL_ARCHITECTURE_GAP`.

## Safety Boundary

This ADR does not create runtime behavior, execution behavior, a planner, governance layer, truth source, storage, synthetic evidence, apply behavior, floor change, or user movement authority.

## Verification

Required verification:

- `tools/v7-truth-check --all --json`
- `tools/v7-convergence-status --json`
