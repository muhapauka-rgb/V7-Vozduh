# E32.1.7 Operator Action Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

operator_action_model_defined=true

## Next Safe Actions

| Failure Mode | Next Safe Action | Secondary Actions |
| --- | --- | --- |
| CAPACITY_STALE | Refresh validation | View evidence, run readiness/restore-settle, recertify if refresh fails |
| CAPACITY_DEGRADED | Diagnose and remediate | Rollback if during execution, recertify after fix |
| CAPACITY_EXPIRED | Full recertification | Rebuild evidence, validate target, reissue class decision |
| CAPACITY_REVOKED | Escalate incident | Quarantine target, audit review, restart certification from CANDIDATE |
| CAPACITY_UNKNOWN | Inspect/discover | Build metadata, classify target |
| CAPACITY_CONFLICT | Reconcile metadata/evidence | Freeze execution, compare hashes, repair docs or metadata only after review |
| CAPACITY_EVIDENCE_MISSING | Reconstruct evidence or recertify | Mark expired if evidence cannot be reconstructed |
| CAPACITY_CONFIDENCE_DROP | Recertify or downgrade | Review incident and confidence inputs |
| CAPACITY_POLICY_CAP_EXCEEDED | Lower batch or request policy review | Do not override policy cap ad hoc |
| CAPACITY_RESERVATION_CONFLICT | Resolve ledger/packet conflict | Release expired reservations, incident review on audit mismatch |

## Forbidden Operator Actions

Operators must not:

- override failure mode to permit forward movement;
- lower quality floors to force eligibility;
- ignore missing evidence;
- use stale capacity for production-pool scheduling;
- reuse revoked certification without incident review.

## Containment Actions

Containment actions remain possible:

- exact rollback;
- target quarantine;
- class downgrade;
- policy cap lowering;
- scheduler pause.

