# E24 Denial / Replay Matrix

| Case | Expected Denial | Audit Record | Operator Message | Next Safe Action |
|---|---|---|---|---|
| stale runtime | `DENY_STALE_RUNTIME` | denial_record | Runtime changed after approval. | Regenerate packet from fresh state. |
| selected_move_hash mismatch | `DENY_HASH_MISMATCH` | denial_record | Movement fingerprint changed. | Rebuild preview and approval. |
| generation mismatch | `DENY_GENERATION_MISMATCH` | denial_record | Generation token does not match packet. | Reissue packet. |
| target not ready | `DENY_TARGET_NOT_READY` | denial_record | Target readiness is not GO. | Fix target or select another target. |
| candidate moved already | `DENY_CANDIDATE_STATE_CHANGED` | denial_record | Candidate is no longer on expected source. | Re-run candidate selection. |
| rollback target unhealthy | `DENY_ROLLBACK_TARGET_UNHEALTHY` | denial_record | Rollback path is unsafe. | Restore rollback target first. |
| hidden mover active | `DENY_HIDDEN_MOVER_ACTIVE` | denial_record | Runtime mutation path already active. | Contain timers/processes and investigate. |
| checker fail | `DENY_RUNTIME_CHECK_FAILED` | denial_record | Runtime checker failed. | Investigate and do not move. |
| approval expired | `DENY_APPROVAL_EXPIRED` | denial_record | Approval expired. | Reconfirm approvals. |
| replayed packet | `DENY_REPLAY` | denial_record | Approval already used. | New packet required. |
| movement budget changed | `DENY_BUDGET_CHANGED` | denial_record | Movement budget is no longer 1. | Reissue packet. |
| unauthorized user added | `DENY_BLAST_RADIUS_CHANGED` | denial_record | Packet includes unauthorized user. | Reject and regenerate. |
| unauthorized target changed | `DENY_BLAST_RADIUS_CHANGED` | denial_record | Packet includes unauthorized target. | Reject and regenerate. |

denial_matrix_complete=true
