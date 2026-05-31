# E35.C Test Plan

## Core Verdict Tests

- AUTO allowed when all gates pass.
- OPERATOR_PINNED denies autoswitch forward movement.
- MANUAL denies autoswitch forward movement.
- Containment emergency returns EMERGENCY_ONLY.
- Governance block returns DENY.
- Group conflict returns DENY or REVIEW_REQUIRED.
- Expired authority returns REVIEW_REQUIRED.
- Unknown conflict returns REVIEW_REQUIRED.
- Safety block returns DENY.

## Expiration Tests

- emergency verdict expires;
- review remains pending until closed;
- stale input fails closed;
- stale packet denies.

## Determinism Tests

- same input produces same verdict;
- rule priority stable;
- conflict resolver deterministic;
- missing required input never returns ALLOW.

## Audit/Event Tests

- verdict event generated;
- conflict event generated;
- review event generated;
- emergency event generated;
- event has evidence/proposal links when present.

## Admin Tests

- Users show verdict and explanation.
- Channels show conflicts/emergency usage.
- Checks show evaluator health/review queue.
- Logs show verdicts/reviews/emergency decisions.
- Home shows summary counts.

## Safety Scans

- evaluator code contains no `v7-user-switch`;
- evaluator code contains no autoswitch apply;
- evaluator code contains no routing sync;
- evaluator APIs are read-only;
- git diff clean.

## Verdict

```text
test_plan_defined=true
```
