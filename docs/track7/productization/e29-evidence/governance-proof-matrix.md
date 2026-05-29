# E29 Governance Proof Matrix

date_utc=2026-05-29T11:17:46Z
runtime_mutation_performed=false

| Capability | Status | Evidence |
|---|---|---|
| Approval packet system | CERTIFIED | E25.15, E27.2, and E28.2 generated bounded packets with explicit users, target, rollback, budget, blast radius, hashes, and denial semantics. |
| Execution-time recheck | CERTIFIED | E25.14 failed closed on registry drift; E25.15, E27.2, and E28.2 authorized only after fresh recheck. |
| Rollback | CERTIFIED | One-user, two-user, and four-user rollbacks restored users to egress 1 and route tables to rollback state. |
| Replay protection | CERTIFIED | E25.15, E27.2 final replay validation, and E28.2 produced DENY_REPLAY without movement or routing mutation. |
| Restore-settle | CERTIFIED | Post-rollback settle gates returned GO with selected_moves=[0,0,0], checkers OK, hidden movers absent. |
| Execution target isolation | CERTIFIED | Target role=EXECUTION_ONLY, reserve_only/manual_only, target users restored to zero after rollback. |
| Autoswitch exclusion | CERTIFIED | Target metadata autoswitch_allowed=false and rebalance_allowed=false; selected_moves stayed zero through observation and delayed monitoring. |
| Governance isolation | CERTIFIED | Only approved raw fallback commands executed; no autoswitch apply, UI execution, broad routing sync, or kill-switch toggle. |
| One-user movement | CERTIFIED | E25.15 moved only 10.7.0.11, then rolled back and replay-denied. |
| Two-user movement | CERTIFIED | E27.2 moved only 10.7.0.11 and 10.7.0.12, then rolled back and replay-denied. |
| Four-user movement | CERTIFIED | E28.2 moved only 10.7.0.11, 10.7.0.12, 10.7.0.14, and 10.7.0.15, then rolled back and replay-denied. |

approval_packet_system_certified=true
execution_time_recheck_certified=true
rollback_certified=true
replay_protection_certified=true
restore_settle_certified=true
governance_isolation_certified=true
one_user_governed_execution_certified=true
two_user_governed_execution_certified=true
small_cohort_governed_execution_certified=true
