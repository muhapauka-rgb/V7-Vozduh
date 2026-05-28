# BLOCK E11.17 - Generation Clearance Rehearsal And Post-TTL Apply Governance Report

## Executive Verdict

E11.17 completed a bounded generation-clearance rehearsal without user
movement, routing mutation, manual autoswitch apply, canary, or cohort
execution.

The block proved two separate facts:

1. Expired uncleared restore barrier is fail-closed under live apply timer.
2. Plain explicit clearance is unsafe in the current live pressure state unless
   it is bounded by an approved selected-move budget.

Because copied live state showed that plain clearance would select 3 failover
moves, E11.17 deployed a bounded generation-clearance budget guard. The live
rehearsal then used `clearance_max_selected_moves=0`; apply timer intervals
observed recurrent movement pressure but selected and applied zero moves.

## Final Answers

fail_closed_rehearsal_clean=true
generation_clearance_consumed=true
user_movement_observed=false
delayed_movement_after_clearance_observed=false
selected_moves_after_clearance=0
apply_timer_final_state=held
runtime_checks_ok=true
regressions_observed=false
mini_cohort_readiness_after=GO
larger_cohort_readiness_after=NO-GO
unattended_apply_lifecycle_status=GENERATION_GOVERNANCE_CONDITIONAL
operational_maturity_status=BOUNDED_APPLY_GOVERNANCE_REHEARSED_BUT_UNBOUNDED_CLEARANCE_FORBIDDEN
recommended_next_block=E11.18_TWO_USER_MINI_COHORT_PROMOTION_CLEAN_APPROVAL_OR_GENERATION_TOKEN_DESIGN
execution_allowed_now=false

## Live Runtime Result

Pre-rehearsal:

- apply timer held
- planner active
- users.registry hash:
  `bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- egress.registry hash:
  `a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`
- WireGuard users: 0
- WireGuard reservation: enforced by `canary_reserved=true`
- selected_moves: 0
- switch-history count: 2698
- runtime checkers: OK

Fail-closed rehearsal:

- live barrier set to expired and uncleared
- apply timer restored through systemd
- timer fired under fail-closed barrier
- selected_moves remained 0
- users.registry hash stayed stable
- switch-history count stayed 2698

Generation-clearance rehearsal:

- clearance token set:
  `allow_post_ttl_apply=true`
- generation clearance set:
  `generation_clearance=true`
- movement budget set:
  `clearance_max_selected_moves=0`
- live planner saw recurrent pressure in final sample:
  `candidate_moves_total=7`
- selected moves before guard:
  `clearance_selected_moves_before_guard=3`
- budget guard status:
  `clearance_budget_exceeded=true`
- final selected_moves after guard:
  `0`
- users.registry hash stayed stable
- switch-history count stayed 2698
- final runtime checkers OK

## Root Cause And Fix

root_cause=PLAIN_CLEARANCE_REOPENS_FRESH_APPLY_RECOMPUTE
fix_path_selected=GENERATION_CLEARANCE_SELECTED_MOVE_BUDGET_GUARD
runtime_fix_executed=true
rollback_performed=false

The issue was not stale selected_moves replay. The apply timer recomputes a
fresh plan, and if the restore barrier is expired and cleared, real service
pressure can produce selected failover moves. E11.17 therefore made clearance
auditable and bounded by an explicit selected-move budget.

## Readiness

Mini-cohort readiness is GO only for the previously proven two-user bounded
lifecycle shape: exact approved users, planner/apply governance, restore-settle,
rollback, delayed monitoring, and no unbounded autoswitch apply.

Larger cohort remains NO-GO because unbounded post-clearance apply is still not
approved and the live system has recurrent failover pressure.

## Mutation Statement

Runtime mutation performed: YES
Runtime mutation scope: bounded `/usr/local/bin/v7-users-autoswitch` clearance selected-move budget guard; restore barrier metadata updated for E11.17 rehearsal; apply timer restored for rehearsal and re-held.
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO

