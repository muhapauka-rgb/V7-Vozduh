# PROGRAM Z3.2 Fail-Closed Certification

## Verified Abort Classes

| Abort class | Evidence |
| --- | --- |
| unknown | planner and approval contracts default unknown/missing state to rejection or no selected moves |
| missing | nonzero generation clearance without token is blocked in unit tests |
| stale | live repeat blocked by generation mismatch |
| expired | expired packet and expired generation token blocked in unit tests |
| invalid | invalid budget blocked in unit tests |
| blocked | safety critical and restore barrier blocked states covered in unit tests |
| mismatched | proposal fingerprint and selected move hash mismatch blocked |

## Live Fail-Closed Event

Immediate repeat after rollback:

- candidate_moves: `0`
- selected_moves: `0`
- guard: `restore_barrier_clearance_generation_mismatch`
- reason: `cooldown_active_877s`
- reason: `no_eligible_failover_target`

## Runtime Safety

Final state after rollback:

- route_check_rc: `0`
- reconcile_rc: `0`
- killswitch_rc: `0`
- users hash restored to pre-move value

## Verdict

- fail_closed_verified=true
- unsafe_repeat_apply_prevented=true
- stale_generation_prevented=true
- invalid_budget_prevented=true
- replay_prevented=true

