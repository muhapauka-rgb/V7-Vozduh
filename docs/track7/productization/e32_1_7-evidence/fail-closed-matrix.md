# E32.1.7 Fail-Closed Matrix

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

fail_closed_matrix_defined=true

| Failure Mode | Forward Allowed | Rollback Allowed | Operator Next Action | Automation Allowed | Requires Human Review |
| --- | --- | --- | --- | --- | --- |
| CAPACITY_STALE | false | true if exact scope known | Refresh validation | Refresh checks only | false unless refresh fails |
| CAPACITY_DEGRADED | false | true as containment | Diagnose/remediate | Diagnostics only | true for recertification |
| CAPACITY_EXPIRED | false | true if exact scope known | Full recertification | Discovery/validation only | true |
| CAPACITY_REVOKED | false | incident containment only | Incident review | Containment diagnostics only | true |
| CAPACITY_UNKNOWN | false | only with exact manifest | Inspect/discover | Metadata discovery only | false unless conflict found |
| CAPACITY_CONFLICT | false | conditional | Reconcile metadata/evidence | Consistency checks only | true |
| CAPACITY_EVIDENCE_MISSING | false | true if exact scope known | Reconstruct evidence/recertify | Evidence scan only | true if reconstruction fails |
| CAPACITY_CONFIDENCE_DROP | false for affected class | true if exact scope known | Recertify/downgrade | Confidence recompute only | true |
| CAPACITY_POLICY_CAP_EXCEEDED | false for requested batch | not affected | Lower batch/request policy review | Denial only | true for policy override |
| CAPACITY_RESERVATION_CONFLICT | false | true for exact active rollback | Resolve reservation conflict | Release expired reservations only | true on ledger/audit mismatch |

## Default

If a failure mode is not recognized:

```text
forward_allowed=false
approval_packet_allowed=false
scheduler_allowed=false
rollback_allowed=only_if_exact_scope_known
requires_human_review=true
```

