# E35.F Implementation Readiness

## P2 Transition

E35.F prepares P2. It does not start P2.

## Recommended Implementation Order

1. Execution Contract Store.
2. Execution Event Store.
3. Read Models and APIs.
4. Admin read-only visibility.
5. Contract generator from Proposal + Authority verdict.
6. Validation engine preview mode.
7. Verification model preview mode.
8. Rollback model preview mode.
9. Runtime hook dry-run.
10. Runtime hook enforce mode after certification.

## Component Classification

| Component | Action |
|---|---|
| Authority Store | Reuse |
| Boundary Evaluator | Extend with execution contract input |
| Conflict Resolver | Extend with execution conflict classes |
| Admin | Extend existing sections |
| Autoswitch | Do not touch until hooks are certified |
| Governance | Reuse as authority input |
| Execution Engine | New bounded implementation in P2 |
| Rollback | Extend certified rollback manifests |
| Observability | Extend Evidence/Proposal/Trust drawers |
| Policy | Reuse as admission input |
| Capacity | Reuse as admission input |
| Concurrency | Reuse as lock/reservation input |

## Build Readiness

P2 can begin with read-only execution contract and event surfaces.

P2 must not begin with live autonomous runtime mutation.

implementation_ready=true
p2_ready=true
runtime_mutation_performed=false
