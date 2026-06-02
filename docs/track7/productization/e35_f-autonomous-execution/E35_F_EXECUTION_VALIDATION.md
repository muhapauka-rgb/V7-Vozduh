# E35.F Execution Validation

## Purpose

Execution Validation is the deterministic pre-execution gate set. It decides whether an execution contract may proceed to execution-time recheck.

Validation is not execution.

## Required Validation Inputs

| Input | Required condition |
|---|---|
| Authority State | readable, fresh, source hash matches contract |
| Evaluator Verdict | `ALLOW` for forward execution |
| Conflict Resolver | no unresolved blocking conflict |
| Routing Mode | AUTO for autonomous forward movement |
| Operator Boundary | no OPERATOR_PINNED or MANUAL override conflict |
| Group Boundary | group constraints satisfied |
| User Boundary | exact allowed users only |
| Required Services | target satisfies required services |
| Capacity | certified, fresh, available, sufficient |
| Policy | admission decision does not deny or require unresolved review |
| Concurrency | required locks/reservations valid |
| Runtime Trust | OK or permitted non-blocking warning |
| Release Trust | certified or permitted non-blocking warning |
| Restore-Settle | GO |
| Selected Moves | zero |
| Hidden Movers | absent |
| Target Readiness | GO |
| Target Users Count | within contract/capacity limit |
| Containment State | compatible with requested action |
| Rollback Manifest | complete |
| Audit Lineage | complete |
| Contract Expiry | non-expired |
| Replay State | not consumed |

## Validation Outcomes

| Outcome | Meaning | Runtime mutation |
|---|---|---|
| VALIDATED | Can proceed to execution-time recheck | No |
| DENIED | Cannot execute | No |
| REVIEW_REQUIRED | Human/governance review required | No |
| EMERGENCY_ONLY | Normal forward denied; bounded containment/rollback may be allowed | No |

## Determinism

Validation must produce the same result for the same input hashes. If a helper returns ambiguous or partial data, validation fails closed.

## Validation Verdict

validation_model_defined=true
runtime_mutation_performed=false
