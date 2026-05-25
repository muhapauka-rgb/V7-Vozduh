# V7 Phase 8 Intelligence Auditability

## Purpose

Adaptive decisions and recommendations must be traceable.

## Audit Fields

- actor or component;
- timestamp;
- target;
- recommendation id;
- confidence;
- evidence;
- safety bounds;
- operator action;
- blocked automatic actions;
- before/after if action occurs;
- rollback context if action occurs.

## Recommendation Audit

Recommendations should be logged or exportable even when no action is taken.

## Action Audit

If an operator acts on intelligence, the action audit must link back to the recommendation and verification result.

## Boundary

No hidden adaptive behavior is allowed.

