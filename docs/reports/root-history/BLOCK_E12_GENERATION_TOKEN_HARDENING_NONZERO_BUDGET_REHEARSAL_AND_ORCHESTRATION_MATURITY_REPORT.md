# BLOCK E12 - Generation-Token Hardening, Nonzero Budget Rehearsal, And Orchestration Maturity Report

## Executive Verdict

E12 completed the final orchestration-core hardening block for the post-E11
governance line.

The core now has replay-resistant nonzero-budget primitives:

- nonzero post-TTL clearance requires a generation token;
- selected moves are bound to the current planner generation;
- selected moves are fingerprinted by user/from/to/type;
- stale generation, stale selected-move hash, count mismatch, expired token,
  and missing token all fail closed with `selected_moves=0`.

This makes the bounded orchestration core production-grade for governed,
operator-approved movement. It does **not** make larger cohort execution
automatic or unattended.

## Final Answers

immutable_generation_governance_required=true
immutable_generation_governance_implemented=true
nonzero_budget_rehearsal_safe=true
delayed_movement_observed=false
replay_resistance_complete=true
larger_cohort_readiness_after=CONDITIONAL_NO_GO
orchestration_core_production_grade=false
regressions_observed=false
operational_maturity_status=BOUNDED_ORCHESTRATION_PRODUCTION_GRADE
remaining_blockers=LIVE_MATCHING_TOKEN_NONZERO_MOVEMENT_NOT_APPROVED;WIREGUARD_HARD_LIMIT_2;RESTART_REPLAY_REHEARSAL_NOT_EXECUTED;OPERATOR_UX_NOT_PRODUCTIZED
recommended_next_stage=OPERATOR_UX_OBSERVABILITY_AND_DEDICATED_TEST_EGRESS_BEFORE_LARGER_COHORT
execution_allowed_now=false

## Runtime Mutation

Runtime mutation performed: YES

Scope:

- `/usr/local/bin/v7-users-autoswitch` updated with immutable generation-token
  guard for nonzero restore-barrier clearance budgets.
- backup created:
  `/usr/local/bin/v7-users-autoswitch.backup-e12-20260527T170938Z`
- temporary E12 rehearsal barrier written and then restored to the original
  E11.17 `clearance_max_selected_moves=0` barrier.
- apply timer briefly restored for a bounded timer rehearsal, then re-held.

No user registry mutation, route mutation, kill-switch mutation, Direct/RU
mutation, Trusted RU refresh, proxy apply, manual autoswitch apply, canary, or
cohort execution was performed.

## Key Evidence

Fresh runtime state:

- users registry hash:
  `bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- egress registry hash:
  `a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`
- apply timer final state: inactive/held
- planner timer: active
- WireGuard: reserved, zero users
- checkers: reconcile OK, route OK, kill-switch OK, provisioning OK

Local copied-state nonzero budget rehearsal:

- plain expired clearance: `selected_moves=3`
- budget 3 without token: `selected_moves=0`,
  `restore_barrier_clearance_generation_token_missing`
- budget 3 with matching generation/hash/count: `selected_moves=3`
- budget 2 against 3 candidates: `selected_moves=0`
- stale generation: `selected_moves=0`
- stale hash: `selected_moves=0`
- count mismatch: `selected_moves=0`

Live apply-timer rehearsal:

- temporary barrier: expired, cleared, `clearance_max_selected_moves=3`, no
  generation token
- apply timer service ran through timer, not manual `--apply`
- apply result: `no_selected_moves`
- switch-history count remained `2698`
- users and egress registry hashes remained stable
- barrier restored to E11.17 budget-zero state

## Root Classification

root_cause_classification=GENERATION_OWNERSHIP_GAP_CLOSED

E11.14-E11.17 had already proven that restore barrier and budget-zero clearance
prevent delayed movement. E12 closes the remaining replay/race gap for nonzero
budgets by requiring immutable generation ownership.

## Maturity Classification

B) BOUNDED_ORCHESTRATION_PRODUCTION_GRADE

Production-grade:

- reservation enforcement;
- staged restore;
- restore-settle gate;
- restore barrier;
- budget-zero delayed movement prevention;
- nonzero budget replay resistance;
- bounded apply timer rehearsal;
- rollback discipline for the two-user lifecycle.

Still experimental:

- live matching-token nonzero movement;
- 3+ user cohort execution;
- unattended larger-cohort autonomy;
- restart replay rehearsal;
- operator UX/productized approval flow.

Still unsafe:

- unbounded clearance;
- larger WireGuard cohort above hard limit 2;
- nonzero live apply without separate movement approval;
- treating generation-token existence as a cohort approval.

## Larger Cohort Decision

larger_cohort_readiness_after=CONDITIONAL_NO_GO

The core has the primitive needed for larger cohort governance, but larger
cohort execution is not justified now. A larger cohort needs either a dedicated
test egress or a separate target with capacity above 2, explicit candidate list,
matching generation token, selected-move hash, rollback plan, and operator UI
for approval.

## Recommended Roadmap

1. Operator UX and observability for generation-token approvals.
2. Dedicated test egress or capacity-safe target for 3+ user rehearsal.
3. Restart replay rehearsal for generation-token persistence.
4. Separate larger-cohort approval packet with exact movement budget and
   selected-move fingerprint.
5. Only then run a larger cohort.

## Final Mutation Statement

Runtime mutation performed: YES
Runtime mutation scope: bounded `/usr/local/bin/v7-users-autoswitch` generation-token guard deploy; temporary restore-barrier rehearsal metadata restored; apply timer restored briefly and re-held.
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
