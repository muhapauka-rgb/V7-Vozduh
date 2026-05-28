# E21 Runtime Recheck Gates

## Required Execution-Time Gates

Every future first action must run these immediately before execution:

1. runtime_freshness
   - live snapshot collected within the approved freshness window.
2. registry_hashes
   - users.registry hash matches approval packet.
   - egress.registry hash matches approval packet.
3. selected_moves_hash
   - selected_moves hash matches approval packet.
   - selected_moves count is 0 for selected first action.
4. target_readiness
   - selected target state has not degraded.
5. restore_settle
   - restore-settle gate is GO if the action can affect apply lifecycle.
6. hidden_movers
   - no v7-user-switch, v7-routing-sync, or v7-users-autoswitch apply process.
7. rollback_target_health
   - not applicable for approval-record-only action.
   - required before any user movement action.
8. kill_switch_ok
   - required before any routing or user movement.
9. route_check_ok
   - required before any routing or user movement.
10. generation_token_match
   - generation id and selected-move fingerprint match approval.
11. approval_not_expired
   - current time is before expires_at.
12. replay_not_used
   - approval id has not been consumed or revoked.
13. blast_radius_unchanged
   - max_users=0 for selected first action.

## Recheck Verdicts

- EXECUTION_ALLOWED
- STALE_RUNTIME
- GENERATION_MISMATCH
- REPLAY_REJECTED
- BLAST_RADIUS_CHANGED
- RESTORE_INVALID
- APPROVAL_EXPIRED
- TARGET_NOT_READY
- HIDDEN_MOVER_FOUND
- KILL_SWITCH_FAIL

## Gate Verdict

runtime_recheck_gates_complete=true
real_boundary_recheck_required_in_next_block=true
execution_allowed_now=false
