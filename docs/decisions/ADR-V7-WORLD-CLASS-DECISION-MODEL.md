# ADR-V7-WORLD-CLASS-DECISION-MODEL

Status: Accepted
Date: 2026-06-25
Program: V7.WORLD_CLASS_DECISION_MODELS

## Context

V7 already has decision-related runtime and read-only owners: operator decision surface, knowledge-to-decision integration, decision-to-outcome-to-learning, knowledge quality, governed canary cycle, Safety-Bounded Authority, OMP, truth/convergence, and canonical action vocabulary.

Research into mature production systems showed a common pattern:

- reconcile current state against desired state;
- separate policy decision from enforcement;
- gate actions with health/readiness/freshness;
- stage risk by blast radius;
- preserve live decision state;
- escalate to humans when authority or ambiguity blocks automation;
- learn only from real outcomes;
- keep runtime thin.

V7 had these capabilities in pieces, but lacked a compact canonical decision model.

## Decision

Adopt `docs/reference/V7_DECISION_MODEL.md` as the canonical documentation-only V7 decision model.

The model defines the decision loop, decision inputs, action vocabulary, universal principles, V7 mapping, read-model output shape, reuse analysis, and extension boundary.

Need New Owner: FALSE

## Consequences

- Future research and execution can start from a shared decision vocabulary instead of re-auditing scattered decision reports.
- Existing owners remain authoritative.
- Future implementation may extend existing read-only surfaces only when a concrete task proves a missing field.
- New planner, governance, execution, runtime truth source, storage, synthetic evidence, apply authority, floor change, or user movement remains forbidden unless a future ADR proves `FUNDAMENTAL_ARCHITECTURE_GAP`.

## Semantic Reuse Result

Existing V7 decision capabilities are sufficient.
The gap was `READ_MODEL_MISSING`, with two `EXISTS_BUT_UNDERUSED` principles:

- make-before-break sequencing;
- live decision handoff state.

No fundamental architecture gap was found.

## Verification

Required verification:

- `tools/v7-truth-check --all --json`
- `tools/v7-convergence-status --json`
