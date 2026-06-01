# P4.B Abort Specification

Project: V7 Vozduh
Block: P4.B First Controlled Runtime Action Specification

| Condition | Detection | Severity | Abort Reason | Operator Message | Recovery Path |
| --- | --- | --- | --- | --- | --- |
| Packet schema invalid | validator | Critical | `DENY_PACKET_INVALID` | Packet schema is invalid. | Regenerate packet. |
| Unsupported action | validator | Critical | `UNSUPPORTED_ACTION` | Selected action is not zero-move governance. | Use approved action type. |
| Runtime action invalid | validator | Critical | `RUNTIME_ACTION_NOT_ALLOWED` | Runtime action is outside P4.B scope. | Regenerate packet. |
| Dual approval missing | approval validation | Critical | `DUAL_CONFIRMATION_MISSING` | Two independent approvals are required. | Re-approve. |
| Same actor approves twice | approval validation | Critical | `DUAL_CONFIRMATION_SAME_ACTOR` | Author and reviewer must differ. | Re-approve with independent reviewer. |
| Approval expired | time check | High | `APPROVAL_EXPIRED` | Approval window expired. | Regenerate packet. |
| Runtime registry missing | file check | Critical | `DENY_STALE_RUNTIME` | Runtime registry is missing. | Refresh runtime evidence. |
| Users hash mismatch | hash check | Critical | `USERS_REGISTRY_HASH_MISMATCH` | Users registry changed. | Regenerate packet. |
| Egress hash mismatch | hash check | Critical | `EGRESS_REGISTRY_HASH_MISMATCH` | Egress registry changed. | Regenerate packet. |
| Selected moves changed | selected moves check | Critical | `SELECTED_MOVES_MISMATCH` | Selected moves are not empty. | Clear/refresh evidence; no action. |
| Runtime snapshot mismatch | hash check | Critical | `RUNTIME_SNAPSHOT_HASH_MISMATCH` | Runtime snapshot changed. | Regenerate packet. |
| Health degraded | health check | High | `HEALTH_DEGRADED` | Health changed since packet. | Refresh dry-run. |
| Capacity degraded | capacity check | High | `CAPACITY_DEGRADED` | Capacity changed since packet. | Refresh dry-run. |
| Trust degraded | trust check | High | `TRUST_DEGRADED` | Trust changed since packet. | Refresh trust evidence. |
| Verification stale | dry-run verification | High | `DRYRUN_VERIFICATION_STALE` | Verification expired. | Refresh verification. |
| Verification mismatch | dry-run verification | Critical | `DRYRUN_VERIFICATION_MISMATCH` | Prediction and observed reality diverged. | Stop and review. |
| Replay detected | audit search | Critical | `DENY_REPLAY` | Approval id already used. | New packet and approval. |

## Verdict

`abort_spec_complete=true`

