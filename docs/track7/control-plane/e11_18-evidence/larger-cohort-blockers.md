# E11.18 Larger Cohort Blockers

## Verdict

larger_cohort_blocked=true
three_user_wireguard_cohort_forbidden=true
current_model_scales_linearly=false

## Exact Blockers

1. WireGuard hard capacity is `hard_limit=2`; a 3-user WireGuard cohort would
   violate the target cap.
2. E11.17 proved plain clearance is unsafe; copied live state selected 3 moves
   before the budget guard.
3. E11.18 copied live state still shows nonzero pressure:
   `candidate_moves_total=9`, `rebalance_candidates=9`.
4. The current clearance budget is count-based, not bound to immutable
   planner/apply generation IDs.
5. Rollback complexity is nonlinear: partial rollback and delayed apply restore
   windows increase with more users.
6. Restore-settle alone is not sufficient; E11.13 proved a later timer
   generation can recompute unsafe movement.
7. Runtime/repo lineage remains partial; larger blast radius requires stronger
   reproducibility.

## Required Before 3+ Users

- Either provision or reserve a target with `hard_limit>=3`, or explicitly
  approve a multi-target cohort design.
- Add immutable generation-token governance or an equivalent apply ownership
  model.
- Define nonzero selected-move budget semantics and prove them in rehearsal.
- Add partial rollback playbooks for 3+ users.
- Prove longer delayed monitoring under realistic pressure.
- Resolve or formally waive runtime/repo lineage gaps for cohort-critical
  tools.

## Recommendation

recommended_next_block=E11.19_GENERATION_TOKEN_OR_NONZERO_BUDGET_REHEARSAL

Do not execute a larger cohort yet.
