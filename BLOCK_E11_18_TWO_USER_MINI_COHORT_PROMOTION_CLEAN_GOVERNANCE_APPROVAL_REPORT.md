# BLOCK E11.18 - Two-User Mini-Cohort Promotion-Clean Governance Approval Report

## Executive Verdict

E11.18 is a read-only governance decision block. No cohort execution, user
movement, routing mutation, deploy, systemd mutation, kill-switch mutation, or
manual autoswitch apply was performed.

The already executed two-user mini-cohort lifecycle can now be classified as
promotion-clean under bounded governance, and only under that exact bounded
shape:

- exact users: `10.7.0.11`, `10.7.0.12`
- exact target: `wireguard-1779454504-c43409`
- WireGuard hard cap: `2`
- sequential movement
- default rollback to target `1`
- staged restore
- restore barrier
- explicit generation clearance
- selected-move budget guard
- delayed monitoring
- final apply hold unless separately approved

This does not approve execution now and does not approve a larger cohort.

## Final Answers

two_user_promotion_clean=true
generation_governance_complete=true
delayed_movement_protection_complete=true
larger_cohort_blocked=true
operational_maturity_status=TWO_USER_PROMOTION_CLEAN_LARGER_COHORT_BLOCKED
remaining_blockers=NO_IMMUTABLE_GENERATION_TOKEN;NONZERO_CLEARANCE_BUDGET_NOT_PROVEN;WIREGUARD_HARD_LIMIT_2;RUNTIME_REPO_LINEAGE_PARTIAL
recommended_next_block=E11.19_GENERATION_TOKEN_OR_NONZERO_BUDGET_REHEARSAL
execution_allowed_now=false

## Current Snapshot

Fresh E11.18 current snapshot:

- apply timer: held
- planner timer: active
- users.registry hash:
  `bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- WireGuard users: `0`
- WireGuard reservation: `canary_reserved=true`
- switch-history count: `2698`
- runtime checkers: OK
- local copied-state selected moves: `0`
- copied-state candidate pressure: `candidate_moves_total=9`
- copied-state rebalance candidates: `9`
- clearance guard: `clearance_max_selected_moves=0`
- clearance selected moves before guard: `3`
- clearance budget exceeded: `true`

The current state proves the guard is meaningful: pressure exists, but the
approved movement budget keeps selected moves at zero.

## Promotion-Clean Decision

The E11.13 lifecycle was not promotion-clean by itself. E11.14-E11.17 closed
the missing governance surface:

- E11.14 proved the delayed movement root cause was fresh timer recompute under
  service-signal pressure.
- E11.15 proved active restore barrier suppresses timer-driven movement.
- E11.16 made expired barriers fail closed.
- E11.17 proved explicit clearance must be budgeted and deployed the selected
  move budget guard.

Therefore, the two-user lifecycle is promotion-clean only when paired with the
E11.17 budgeted clearance model.

## Larger Cohort Decision

larger_cohort_blocked=true

Reasons:

- WireGuard `hard_limit=2`, so a 3-user WireGuard cohort is forbidden.
- Plain clearance was proven unsafe.
- Nonzero clearance budgets are not yet proven.
- Planner/apply generation IDs are not immutable yet.
- Rollback and restore complexity do not scale linearly.
- Runtime/repo lineage remains partial.

## Mutation Statement

Runtime mutation performed: NO
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO

