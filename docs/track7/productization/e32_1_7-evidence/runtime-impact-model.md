# E32.1.7 Runtime Impact Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

runtime_impact_model_defined=true

## Impact Matrix

| Failure Mode | Forward Movement | Rollback | Approval Packet | Scheduler | Operator Action |
| --- | --- | --- | --- | --- | --- |
| CAPACITY_STALE | Denied | Allowed if exact scope known | Draft/refresh only | Denied | Refresh validation |
| CAPACITY_DEGRADED | Denied | Allowed as containment | Denied except remediation/rollback plan | Denied | Diagnose/remediate |
| CAPACITY_EXPIRED | Denied | Allowed if exact scope known | Denied | Denied | Full recertification |
| CAPACITY_REVOKED | Denied | Incident containment only | Denied | Denied | Incident review |
| CAPACITY_UNKNOWN | Denied | Only if exact rollback manifest exists | Denied | Denied | Inspect/discover |
| CAPACITY_CONFLICT | Denied | Allowed only if conflict does not affect rollback scope | Denied | Denied | Reconcile metadata/evidence |
| CAPACITY_EVIDENCE_MISSING | Denied | Allowed if exact scope known | Denied | Denied | Reconstruct evidence or recertify |
| CAPACITY_CONFIDENCE_DROP | Denied for affected class | Allowed if exact scope known | Denied or lowered class draft | Denied for affected class | Recertify/downgrade |
| CAPACITY_POLICY_CAP_EXCEEDED | Denied for requested batch | Not affected | Denied for over-cap batch | Denied | Lower batch/request policy review |
| CAPACITY_RESERVATION_CONFLICT | Denied | Allowed for exact active rollback | Denied until conflict clears | Denied | Resolve ledger/packet state |

## Runtime Safety Rule

Every failure mode denies forward movement by default. Rollback is allowed only when it reduces or restores risk and the exact rollback scope is known.

## Scheduler Rule

Scheduler must treat all capacity failure modes as admission-deny conditions unless the scheduled action is explicit rollback/containment.

