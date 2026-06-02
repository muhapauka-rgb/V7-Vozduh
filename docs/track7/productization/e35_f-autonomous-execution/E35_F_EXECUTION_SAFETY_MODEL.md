# E35.F Execution Safety Model

## Safety Invariants

Forward execution is forbidden if any invariant fails:

1. No execution without Evidence.
2. No execution without Proposal.
3. No execution without Authority verdict.
4. No execution without Conflict Resolver result.
5. No execution without Execution Contract.
6. No execution without complete rollback manifest.
7. No execution without fresh runtime trust.
8. No execution without acceptable release trust.
9. No execution without certified capacity.
10. No execution without policy admission.
11. No execution without concurrency reservation/locks.
12. No execution without restore-settle GO.
13. No execution with selected moves.
14. No execution with hidden movers.
15. No execution with stale registry hashes.
16. No execution with unreadable authority store.
17. No execution with unresolved conflict.
18. No execution if routing mode is OPERATOR_PINNED or MANUAL unless exact operator/governance authority permits that action.
19. No execution outside allowed user set.
20. No execution outside allowed target set.

## Fail-Closed Rules

| Condition | Forward execution |
|---|---|
| Missing evidence | DENY |
| Missing proposal | DENY |
| Missing authority | DENY |
| Authority unreadable | DENY |
| Evaluator mismatch | DENY or REVIEW_REQUIRED |
| Conflict unknown | REVIEW_REQUIRED |
| Runtime trust stale | DENY |
| Release trust unknown | REVIEW_REQUIRED or DENY by policy |
| Capacity stale/degraded/expired | DENY |
| Policy conflict | DENY or REVIEW_REQUIRED |
| Lock conflict | DENY |
| Selected moves nonzero | DENY |
| Hidden movers present | DENY |
| Rollback incomplete | DENY |
| Contract expired | DENY |
| Replay attempt | DENY |

## Emergency Handling

Emergency does not permit arbitrary forward movement.

Emergency can permit bounded rollback or containment only if:

- scope is exact;
- action reduces risk;
- audit is created;
- human review follows.

## Safety Verdict

safety_model_defined=true
runtime_mutation_performed=false
routing_changed=false
users_moved=false
