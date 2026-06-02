# E35.F Autonomous Execution Model

## Definition

Autonomous Execution means:

```text
Автономное действие системы
```

In V7, autonomous execution is a bounded runtime action initiated by the system after all certified governance layers have produced compatible ALLOW verdicts.

It is not independent authority.

## Core Rule

Autonomous execution consumes authority. It never creates authority.

```text
Evidence
-> Proposal
-> Authority Evaluation
-> Conflict Resolution
-> Batch Admission
-> Capacity Gate
-> Policy Gate
-> Concurrency Gate
-> Runtime Trust Gate
-> Release Trust Gate
-> Execution Contract
-> Execution-Time Recheck
-> Action
```

## What Autonomous Execution May Do

Only after all gates pass, autonomous execution may:

- execute an approved bounded movement;
- execute an approved rollback;
- execute approved containment action;
- produce execution, verification, observation, rollback, and closure events.

## What Autonomous Execution May Not Do

Autonomous execution may not:

- change routing mode;
- override OPERATOR_PINNED or MANUAL ownership;
- bypass conflict resolver;
- ignore REVIEW_REQUIRED;
- create approval authority;
- change policy;
- change capacity metadata;
- create or clear locks outside concurrency rules;
- execute if runtime trust is stale or drifted;
- execute if rollback is missing;
- move any user outside the contract.

## Authority Relationship

Autonomous execution is downstream of:

- Safety;
- Containment;
- Governance;
- Operator;
- Group;
- User;
- Autoswitch;
- Scheduler;
- Boundary Evaluator;
- Conflict Resolver.

If any upstream layer returns `DENY`, `REVIEW_REQUIRED`, or incompatible `EMERGENCY_ONLY`, autonomous forward execution is denied.

## Execution Classes

| Execution class | Meaning | Allowed before P2 implementation |
|---|---|---|
| Forward Movement | Move users to approved target | Architecture only |
| Rollback | Return exact users to rollback targets | Architecture only |
| Containment | Emergency bounded safety action | Architecture only |
| Observation | Read-only monitoring | Already allowed |
| Verification | Read-only validation | Already allowed |

## Model Verdict

autonomous_execution_model_defined=true
runtime_mutation_performed=false
