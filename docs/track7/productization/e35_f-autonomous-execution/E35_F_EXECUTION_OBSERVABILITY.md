# E35.F Execution Observability

## Operator Questions

The operator must be able to answer:

- What happened?
- Why did it happen?
- Who or what authorized it?
- Which users were affected?
- Which target was used?
- Which services were required?
- What changed in routing?
- Was it verified?
- Is rollback available?
- Did any delayed movement occur?
- What is the next safe action?

## Admin Placement

No new top-level navigation section.

| Admin area | Execution surface |
|---|---|
| Главная | Execution Summary, Pending Executions, Failures, Rollback Activity |
| Пользователи | Execution History, Authority History, Rollback History, Verification Status |
| Каналы | Execution Impact, Target Readiness, Rollback State |
| Проверки | Execution Health, Validation Health, Verification Health |
| Логи | Execution Events, Validation Events, Verification Events, Rollback Events |
| Безопасность | Authority, conflict, emergency, trust and rollback risk summaries |

## Display Model

Operator-first display:

```text
Summary
-> Affected users
-> Authority
-> Validation result
-> Execution result
-> Verification result
-> Rollback state
-> Advanced details
```

Raw hashes, packet internals, registry diffs, and command outputs are hidden behind advanced details.

## Status Semantics

| Status | Operator meaning |
|---|---|
| READY | Contract exists but not executing |
| VALIDATED | Pre-execution gates passed |
| BLOCKED | Execution denied or review required |
| EXECUTING | Runtime action in progress |
| VERIFYING | Checking result |
| OBSERVING | Watching for delayed side effects |
| ROLLBACK_READY | Rollback can be executed |
| ROLLED_BACK | Rollback completed |
| COMPLETED | Closed successfully |
| FAILED_CLOSED | Stopped safely |

## Observability Verdict

observability_defined=true
runtime_mutation_performed=false
