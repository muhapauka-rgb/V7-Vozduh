# Convergence E Deferred API Decision

Project: V7 Vozduh
Block: Convergence E

## Deferred Public API Family

Deferred routes found in local dirty source but not integrated in convergence branch:

- `/api/execution/outcome-preview`
- `/api/execution/blast-radius`
- `/api/execution/service-impact`

## Decision

Decision: Defer with explicit blocker.

## Rationale

The convergence branch already contains internal derived helpers for candidate outcome, service
impact, blast radius, rollback impact, and readiness forecast. Promoting the local dirty public API
family now would create a risk of duplicate public semantics unless the next block explicitly maps:

- route names
- canonical truth source
- response schema
- UI placement
- retention behavior
- tests

No route alias was added in Convergence E because an alias would still create a public API contract.
No route was retired because the local dirty source is outside the convergence worktree and must not
be overwritten from this block.

## Required Next Step

Convergence F should choose one canonical simulation/impact API shape and either integrate these
routes as aliases to existing derived models or retire them from the local dirty source before merge.

deferred_api_decision_complete=true
