# E11.18 Full Two-User Lifecycle Replay Analysis

## Scope

This is a read-only replay of the already executed two-user mini-cohort
lifecycle. No user movement, routing mutation, deploy, timer mutation, or manual
autoswitch apply was performed in E11.18.

approved_users=10.7.0.11,10.7.0.12
approved_target=wireguard-1779454504-c43409
rollback_targets=1,1
hard_blast_radius=2_users

## Lifecycle Chain

| Stage | Evidence | Verdict |
|---|---|---|
| E11.12 approval | two-user cap, WireGuard hard limit 2, selected users 10.7.0.11/10.7.0.12 | approved conditionally |
| E11.13 forward move user 1 | 10.7.0.11 moved to WireGuard and verified | clean |
| E11.13 forward move user 2 | 10.7.0.12 moved to WireGuard and verified; WireGuard users=2 | clean |
| E11.13 observation | route/checkers OK, only approved users in cohort | clean |
| E11.13 rollback | both approved users returned to target `1`; WireGuard users=0 | clean |
| E11.13 restore-settle | gate GO, selected_moves=0 in sampled window | clean but insufficient |
| E11.13 apply restore | timer restore later moved 10.7.0.9/10.7.0.10/10.7.0.13 | not promotion-clean at that time |
| E11.14 root cause | fresh apply-timer recompute under Telegram pressure, not stale replay | root cause proven |
| E11.14 fix | restore barrier failover quarantine | bounded mitigation |
| E11.15 rehearsal | apply timer under active barrier, selected_moves=0, no movement | clean |
| E11.16 post-TTL | expired barrier made fail-closed until explicit clearance | clean under fail-closed governance |
| E11.17 clearance guard | plain clearance unsafe; budget guard deployed; budget=0 selected no moves | clean bounded clearance |
| E11.18 current snapshot | copied live state: candidate_moves_total=9, selected_moves=0, budget guard active | current bounded state clean |

## Governance Chain

The exact two-user lifecycle is now bounded by:

1. Exact user manifest: only `10.7.0.11` and `10.7.0.12`.
2. Exact target: `wireguard-1779454504-c43409`.
3. WireGuard hard cap: `hard_limit=2`.
4. Sequential movement and per-user route verification.
5. Default rollback to target `1`.
6. Planner/apply split.
7. Restore-settle gate.
8. Restore barrier after rollback.
9. Post-TTL explicit generation clearance.
10. Selected-move budget guard.
11. Delayed monitoring across timer intervals.
12. Final apply timer hold unless a separate approval authorizes otherwise.

## Remaining Weak Points

- No immutable planner/apply generation token exists yet.
- Clearance is budget-guarded, not semantically bound to a specific immutable
  generation ID.
- Current copied live state still contains planner pressure:
  `candidate_moves_total=9`, `rebalance_candidates=9`.
- Larger cohorts would require a nonzero clearance budget and more complex
  rollback/restore semantics.
- Runtime/repo lineage remains partial, with known warnings.

## Replay Verdict

two_user_lifecycle_fully_bounded=true
two_user_promotion_clean=true
unattended_apply_proven=false
larger_cohort_blocked=true
execution_allowed_now=false
