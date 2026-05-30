# E34.E Diagnostic Flow Model

diagnostic_flow_defined=true

## Official Flow

```text
Problem
-> Evidence
-> Diagnosis
-> Action
-> Verification
-> Closure
```

This is the required operator workflow for every commercial operational issue.

## Stage Definitions

| Stage | Meaning | Exit requirement |
| --- | --- | --- |
| Problem | A concrete symptom, alert, failed gate, drift, or operator-reported issue. | Problem is named and scoped. |
| Evidence | Relevant runtime, release, backup, policy, capacity, scheduler, routing, and audit state is collected. | Evidence set is complete enough to compare causes. |
| Diagnosis | Plausible causes are enumerated and tested against evidence. | Root cause is selected or escalation reason is documented. |
| Action | A safe, scoped, reversible remediation or containment is selected. | Action is authorized by runbook/governance. |
| Verification | Post-action state is checked against expected outcome. | Pass/fail result is recorded. |
| Closure | Final verdict is produced. | Closure verdict is explicit and auditable. |

## Diagnostic Rules

- Operator never starts from action.
- Operator never stops at the first plausible theory.
- Operator compares all plausible causes that are in scope and safe to investigate.
- Unknown evidence causes fail-closed behavior for forward execution.
- Rollback and containment may remain allowed when forward action is denied.

## Evidence Ordering

Recommended evidence order:

1. Runtime safety state.
2. Affected user, target, batch, policy, or release scope.
3. Current fingerprints and lineage.
4. Health and readiness.
5. Locks and reservations.
6. Audit lineage.
7. Recent operator actions.

## Diagnosis Output

Diagnosis must produce:

```text
root_cause=<known cause or UNKNOWN>
confidence=LOW|MEDIUM|HIGH
safe_action=<action or NONE>
blocked_reason=<reason if no action>
rollback_available=true|false
escalation_required=true|false
```
