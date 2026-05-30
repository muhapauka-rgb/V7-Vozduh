# E32.2.B Fail-Closed Matrix

batch_fail_closed_matrix_defined=true

| Failure Mode | Forward Allowed | Rollback Allowed | Containment Allowed | Human Review Required |
| --- | --- | --- | --- | --- |
| `BATCH_STALE` | false | false unless previous mutation scope exists | true if exact scope known | false |
| `BATCH_EXPIRED` | false | false unless previous mutation scope exists | true if exact scope known | false |
| `BATCH_REPLAY_ATTEMPT` | false | false | false unless separate incident exists | true if movement suspected |
| `BATCH_RUNTIME_DRIFT` | false | false unless drift followed mutation | true if exact scope known | true if drift unexplained |
| `BATCH_CAPACITY_CONFLICT` | false | true if rollback/containment | true if exact scope known | false unless ledger conflict |
| `BATCH_PARTIAL_FORWARD` | false | true if exact rollback manifest still valid | true | true |
| `BATCH_PARTIAL_ROLLBACK` | false | true for remaining exact users | true | true |
| `BATCH_AUDIT_INCONSISTENCY` | false | true only if exact runtime scope verified | true if scope known | true |
| `BATCH_ROLLBACK_SCOPE_UNKNOWN` | false | false until scope reconstructed | true only after human-approved containment plan | true |

## Matrix Rules

Forward movement is denied for every batch failure mode.

Rollback is allowed only when it reduces risk and exact rollback scope is known.

Containment is allowed only when it does not expand blast radius.

Human review is mandatory whenever audit lineage, runtime scope, or rollback scope is uncertain.
