# E21 Denial / Replay Matrix

| Case | Expected denial | Operator message | Audit record | Next safe action |
|---|---|---|---|---|
| stale runtime | STALE_RUNTIME | Runtime truth changed. Refresh packet. | denial_stale_runtime | regenerate approval packet |
| generation mismatch | GENERATION_MISMATCH | Generation token no longer matches. | denial_generation_mismatch | re-run governance preview |
| hash mismatch | REPLAY_REJECTED | Selected-move or runtime hash changed. | denial_hash_mismatch | regenerate packet |
| expired approval | APPROVAL_EXPIRED | Approval window expired. | denial_expired | request fresh dual confirmation |
| replayed approval | REPLAY_REJECTED | Approval already consumed or revoked. | denial_replay | create new approval id |
| target not ready | TARGET_NOT_READY | Target readiness changed. | denial_target_not_ready | investigate readiness |
| restore-settle fail | RESTORE_INVALID | Restore-settle is not GO. | denial_restore_invalid | keep fail-closed |
| hidden mover found | HIDDEN_MOVER_FOUND | Hidden mover detected. | denial_hidden_mover | contain and classify |
| rollback target unhealthy | ROLLBACK_INVALID | Rollback target unhealthy. | denial_rollback_invalid | do not execute movement |
| blast radius changed | BLAST_RADIUS_CHANGED | Scope expanded beyond packet. | denial_blast_radius | regenerate packet |
| kill switch fail | KILL_SWITCH_FAIL | Traffic safety check failed. | denial_killswitch | stop and investigate |

## Verdict

denial_replay_matrix_complete=true
replay_protection_sufficient_for_packet=true
execution_allowed_now=false
