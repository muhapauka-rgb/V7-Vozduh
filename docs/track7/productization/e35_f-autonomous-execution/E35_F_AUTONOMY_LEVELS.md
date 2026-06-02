# E35.F Autonomy Levels

## Level Taxonomy

| Level | Name | Meaning | Runtime mutation |
|---|---|---|---|
| Level 0 | Observation Only | System only observes, records evidence, and displays status | No |
| Level 1 | Proposal Only | System creates proposals from evidence | No |
| Level 2 | Review Required | System prepares executable contract, but operator/governance must approve | No until approval |
| Level 3 | Bounded Autonomous Execution | System may execute exact contract after all gates pass | Yes, contract-limited |
| Level 4 | Certified Autonomous Execution | System may execute policy-scheduled bounded contracts in certified production pool | Yes, policy/scheduler/contract-limited |

## Current V7 Position

Current certified operator chain:

```text
Problem -> Evidence -> Proposal -> Runtime Trust -> Release Trust
```

Current architecture chain now adds:

```text
Authority -> Boundary Evaluation -> Conflict Resolution -> Execution Contract
```

Before P2 implementation, V7 remains at:

```text
Level 1 / Level 2 architecture-ready
```

Level 3 and Level 4 require implementation and certification.

## Level Promotion Conditions

| Promotion | Required proof |
|---|---|
| L1 -> L2 | Execution contract can be generated read-only and shown in admin |
| L2 -> L3 | Contract validation, runtime hooks, rollback, verification, audit and fail-closed tests pass |
| L3 -> L4 | Scheduler, production-pool policy, concurrency, observability, rollback and incident drills certified |

## Autonomy Verdict

autonomy_levels_defined=true
runtime_mutation_performed=false
