# P4.A Abort Matrix

Project: V7 Vozduh
Block: P4.A First Controlled Runtime Action Design

| Condition | Abort reason | Severity | Operator visibility | Rollback requirement |
| --- | --- | --- | --- | --- |
| Packet expired | `APPROVAL_EXPIRED` | High | Approval Center | None; regenerate packet |
| Same actor approved twice | `DUAL_APPROVAL_INVALID` | High | Approval Center | None |
| Users registry hash changed | `USERS_REGISTRY_MISMATCH` | Critical | Checks / Execution drawer | None; abort before action |
| Egress registry hash changed | `EGRESS_REGISTRY_MISMATCH` | Critical | Checks / Execution drawer | None; abort before action |
| Runtime snapshot hash changed | `RUNTIME_SNAPSHOT_MISMATCH` | Critical | Checks | None; abort before action |
| Selected moves not empty | `SELECTED_MOVES_NOT_EMPTY` | Critical | Operator / Checks | None; abort before action |
| Service health degraded | `HEALTH_DEGRADED` | High | Checks | None; abort before action |
| Capacity degraded | `CAPACITY_CHANGED` | Medium | Checks | None; abort before action |
| Trust degraded | `TRUST_CHANGED` | High | Governance Preview | None; abort before action |
| Candidate/action scope changed | `SCOPE_CHANGED` | Critical | Execution drawer | None; new packet |
| Dry-run verification stale | `DRYRUN_STALE` | High | Dry-Run Verification | None; refresh dry-run |
| Dry-run verification mismatch | `VERIFICATION_MISMATCH` | Critical | Dry-Run Verification | None; abort before action |
| Rollback preview unavailable | `ROLLBACK_UNAVAILABLE` | High | Rollback Preview | None; abort before action |
| Observation unavailable | `OBSERVATION_UNAVAILABLE` | High | Logs / Operator timeline | None; abort before action |
| Replay detected | `REPLAY_DETECTED` | Critical | Audit / Operator | Compensating denial record only |

## Verdict

`abort_matrix_defined=true`

