# BLOCK E35.F Autonomous Execution Architecture Report

## 1. Discovery Summary

E35.F audited the certified V7 execution-adjacent architecture:

- Evidence and Proposal surfaces exist.
- Runtime Trust and Release Trust surfaces exist.
- Approval packets, execution-time recheck, rollback, restore-settle, selected moves, hidden movers and replay denial were proven through 1, 2, 4, and 10-user governed movements.
- Capacity, Execution Batches, Policy, Concurrency and Scheduling foundations are certified as governance inputs.
- Routing Authority, Boundary Evaluator, Conflict Resolver, Authority Store and Authority Read Path are certified through E35.A-E.

Missing before autonomy: execution contract store, autonomous lifecycle, deterministic validation, verification, rollback trigger rules, execution observability, event model and final certification gates.

## 2. Autonomous Execution Model

Autonomous execution is a bounded system action that consumes existing authority. It never creates authority.

It may execute only after:

```text
Evidence -> Proposal -> Authority -> Conflict Resolver -> Batch -> Capacity -> Policy -> Concurrency -> Trust -> Contract -> Recheck
```

Any blocking verdict denies forward execution.

## 3. Execution Lifecycle

Final lifecycle:

```text
Problem
-> Evidence Bundle
-> Proposal
-> Authority Evaluation
-> Conflict Resolution
-> Batch Candidate
-> Capacity / Policy / Concurrency Admission
-> Execution Candidate
-> Execution Contract
-> Operator Visibility Window
-> Runtime Validation
-> Execution-Time Recheck
-> Execution
-> Verification
-> Observation
-> Rollback Ready
-> Closure
```

Terminal states include `COMPLETED`, `FAILED_CLOSED`, `ROLLED_BACK`, `CANCELLED`, `EXPIRED`, and `REPLAY_DENIED`.

## 4. Execution Contract

Execution without a contract must be impossible.

The contract must bind:

- exact action;
- exact users;
- exact targets;
- rollback manifest;
- movement budget;
- blast radius;
- Evidence and Proposal lineage;
- Authority and Conflict lineage;
- Capacity, Policy and Concurrency snapshots;
- Runtime and Release trust hashes;
- users.registry, egress.registry and selected_moves hashes;
- validation, verification, observation and audit requirements;
- expiry and replay nonce.

## 5. Validation Model

Pre-execution validation checks Authority, Evaluator, Conflict Resolver, Runtime Trust, Release Trust, Required Services, Capacity, Policy, Concurrency, Restore-Settle, selected moves, hidden movers, target readiness, group/user/routing-mode constraints, containment state, rollback manifest, audit lineage, contract expiry and replay state.

Validation outcomes:

- `VALIDATED`
- `DENIED`
- `REVIEW_REQUIRED`
- `EMERGENCY_ONLY`

## 6. Verification Model

Post-execution verification proves:

- approved users moved as contracted;
- no unapproved users moved;
- route tables changed only within scope;
- target users count changed by exact count;
- required services remain available;
- runtime checkers, selected moves and hidden movers remain clean;
- audit record references the contract.

Rollback verification proves exact restoration to rollback manifest.

## 7. Rollback Architecture

Rollback is mandatory before forward execution. The rollback manifest survives forward contract expiry until closure.

Rollback triggers include verification failure, observation failure, required service failure, target readiness loss, operator rollback, governance rollback and containment emergency.

Rollback scope is always exact:

```text
contract.allowed_users -> contract.rollback_manifest
```

## 8. Observability

Existing `/admin-v2` is extended without new top-level navigation:

- Главная: Execution Summary, Pending Executions, Failures, Rollback Activity.
- Пользователи: Execution History, Authority History, Rollback History, Verification Status.
- Каналы: Execution Impact, Target Readiness, Rollback State.
- Проверки: Execution Health, Validation Health, Verification Health.
- Логи: Execution, Validation, Verification and Rollback Events.
- Безопасность: denied, review-required, emergency and trust block summaries.

## 9. Autonomy Levels

Defined levels:

- Level 0: Observation Only.
- Level 1: Proposal Only.
- Level 2: Review Required.
- Level 3: Bounded Autonomous Execution.
- Level 4: Certified Autonomous Execution.

Current V7 is architecture-ready for Level 2 and must implement/certify P2 before Level 3.

## 10. Safety Model

Safety invariants:

- no execution without Evidence;
- no execution without Proposal;
- no execution without Authority;
- no execution without Conflict Resolver result;
- no execution without complete rollback;
- no execution with stale trust;
- no execution with stale/degraded/expired capacity;
- no execution with selected moves or hidden movers;
- no execution outside exact users/targets;
- no execution if authority store is unreadable;
- no execution through OPERATOR_PINNED or MANUAL without explicit compatible authority.

## 11. Certification Model

Before live autonomy, V7 must certify:

- read path;
- authority;
- boundary evaluator;
- conflict resolver;
- evidence/proposal linkage;
- execution contract;
- validation engine;
- verification engine;
- rollback;
- observability;
- audit;
- replay protection;
- runtime hook in dry-run before enforce.

## 12. Implementation Readiness

P2 may begin with:

1. Execution Contract Store.
2. Execution Event Store.
3. Read Models and APIs.
4. Admin read-only visibility.
5. Contract generator from Proposal + Authority verdict.
6. Validation preview.
7. Verification preview.
8. Rollback preview.
9. Runtime hook dry-run.
10. Runtime hook enforce mode only after certification.

## 13. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Autonomy mistaken for authority | Critical | contract consumes authority only |
| Runtime hook executes without contract | Critical | hard fail-closed invariant |
| OPERATOR_PINNED bypass | Critical | routing mode gate |
| Rollback omitted | Critical | contract invalid |
| Trust stale but execution continues | High | validation DENY |
| Conflict unknown but ALLOW emitted | High | REVIEW_REQUIRED |
| Admin hides why action happened | Medium | observability contract |
| Partial execution not rolled back | High | verification failure -> rollback/containment |

## 14. Recommendations For P2

P2 should start as read-only implementation:

```text
P2.1_EXECUTION_CONTRACT_AND_EVENT_STORE
```

Do not start with live autonomous mutation.

## Required Verdicts

```text
autonomous_execution_model_defined=true
execution_lifecycle_defined=true
execution_contract_defined=true
validation_model_defined=true
verification_model_defined=true
rollback_architecture_defined=true
observability_defined=true
autonomy_levels_defined=true
safety_model_defined=true
certification_model_defined=true
implementation_ready=true
p2_ready=true
```

## Safety Verdict

```text
runtime_mutation_performed=false
routing_changed=false
users_moved=false
autoswitch_apply_run=false
policy_apply_run=false
killswitch_changed=false
```
