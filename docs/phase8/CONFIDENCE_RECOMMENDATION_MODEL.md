# V7 Phase 8 Confidence-Based Recommendation Model

## Purpose

Recommendations must be explainable, auditable, and bounded.

## Confidence Levels

low:

- single weak signal;
- recommend observation or diagnostics only.

medium:

- persistent signal or two correlated signals;
- recommend guarded workflow or operator review.

high:

- multi-signal persistent degradation with verified safe alternative;
- recommend bounded action with rollback context.

## Required Fields

Every recommendation must include:

- id;
- category;
- target;
- confidence;
- explanation;
- evidence list;
- safety bounds;
- operator action;
- blocked automatic actions;
- generated timestamp.

## Bad Recommendation

`AI recommends migration`

## Good Recommendation

`Telegram degraded for 42s; reconnects increased; target GLOBAL_STABLE path verified; confidence medium; run autoswitch safety review before guarded apply.`

