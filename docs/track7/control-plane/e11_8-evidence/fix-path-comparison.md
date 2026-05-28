# E11.8 Fix Path Comparison

| Fix path | Pros | Cons | Runtime mutation scope | Production risk | Decision |
|---|---|---|---|---|---|
| metadata-only `manual_only=1` | simple and existing code honors it | overloads canary semantics; could affect admin UI meaning; still no explicit reservation audit | egress.registry | medium | rejected |
| metadata-only `reserve_only=1` | existing planned path honors it | failover path can still use reserve targets; not a hard canary reservation | egress.registry | medium | rejected |
| planner destination hard-block | explicit; blocks all selected destination paths before apply; testable | does not drain existing users | `v7-users-autoswitch` only | low | selected |
| apply revalidation only | safety backstop | planner output still misleading; load summary still counts reserved target | `v7-users-autoswitch` only | low | future hardening |
| drain semantics in same block | returns target to zero-user | moves 10 users; broad production movement | users/routes via autoswitch | high | rejected for E11.8 |
| dedicated canary egress | clean long-term | provisioning work; not immediate enforcement fix | future infra | low after build | fallback |
| routing-sync/reconcile change | not causal | wrong layer | routing tooling | unnecessary | rejected |

Selected fix:

`planner_destination_hard_block_without_drain`

Semantics:

- `canary_reserved=true` is parsed into `Egress.canary_reserved`.
- Reserved targets are excluded from production dynamic load pool.
- Reserved targets are blocked for production destination candidates with `canary_reserved_production_assignment_blocked`.
- Existing users currently on a reserved target are held if the target is healthy and marked `canary_reserved_current_hold_requires_separate_drain_approval`.
- Any drain must be approved in a separate bounded block.
