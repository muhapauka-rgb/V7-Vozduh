# PROGRAM POOL PROMOTION EQUIVALENCE RULE DESIGN IMPLEMENTATION AND REVIEW REPORT

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Date: 2026-06-07

Mode: governance rule design, implementation, test, deploy, and read-only production review. No user movement. No autoswitch apply. No automatic POOL promotion.

Evidence folder: `pool_equivalence_rule_evidence/`

## Executive Verdict

The POOL equivalence rule is safe, implemented, tested, pushed, and deployed.

POOL promotion is still denied.

Single material blocker:

`pool_equivalence_requires_3600s_large_stability_window`

Why:

The production feedback records for the successful LARGE operation `runtime_autoswitch_0425741b308df19ccc0c1e03` prove:

- one successful LARGE operation: true
- 10 users: true
- feedback complete: true
- rollback clean: true
- 25 planner-visible users: true
- balanced pool: true
- load status ok: true
- zero planner candidate moves: true
- snapshot gate clean after refresh: true

But they do not prove the required 3600 second stability window in the canonical promotion owner input:

`observed_stability_window_seconds=0`

Therefore the new equivalence rule correctly refuses to replace the second LARGE requirement until the stability window is materialized into canonical promotion evidence.

## Phase 1 - Rule Intent Review

Reviewed rule:

`two_successful_large_batch_operation_ids_required`

Owner:

`tools/v7-users-autoswitch`

The rule protects:

- repeatability of LARGE_BATCH execution;
- rollback cleanliness at 10-user scale;
- feedback closure at 10-user scale;
- planner/snapshot stability;
- pool readiness before 25-user authority;
- explicit operator approval before authority expansion.

Evidence:

`pool_equivalence_rule_evidence/rule_intent_review.json`

Verdict:

`rule_intent_understood=true`

## Phase 2 - Evidence Equivalence Review

Reviewed equivalence:

`one successful LARGE + 3600s stability + 25-user preparation + healthy planner + healthy governance + healthy feedback + zero rollback + zero rebalance demand`

Decision:

This can safely replace the second LARGE requirement only if every condition is canonical and machine-checkable by the existing promotion owner.

The important safety decision:

The rule does not accept reports or prose as stability evidence. It accepts only the existing feedback/policy fields already read by the promotion owner.

Verdict:

`equivalence_review_complete=true`

## Phase 3 - Safety Review

The equivalence rule is safe because it preserves:

- existing promotion owner;
- existing truth check;
- existing feedback requirements;
- existing rollback requirements;
- existing operator approval requirement;
- existing audit flow;
- no user movement;
- no autoswitch apply;
- no new truth source;
- no new governance path.

Verdict:

`equivalence_safe=true`

## Phase 4 - Rule Design

Implemented rule:

`one_successful_large_3600s_no_regression_25_users_balanced_zero_move_pool`

Requirements:

| Requirement | Status in final production review |
|---|---|
| one successful LARGE_BATCH | true |
| required stability window seconds | 3600 |
| observed stability window seconds | 0 |
| active users >= 25 | true |
| balanced pool | true |
| load status ok | true |
| active working channels >= 2 | true |
| zero planner candidate moves | true |
| snapshot gate clean | true |
| explicit operator approval still required | true |

Verdict:

`equivalence_rule_defined=true`

## Phase 5 - Implementation

Implementation commit:

`9c36f0f Add POOL promotion equivalence rule`

Refinement commit:

`6e8eb4e Refine POOL equivalence stability review`

Changed owner:

`tools/v7-users-autoswitch`

Added behavior:

- `_pool_equivalence_distribution_review`
- `_pool_equivalence_planner_review`
- `_pool_authority_equivalence_review`
- POOL evidence review can accept equivalence only when current evidence is complete.

No new governance owner was created.

No new truth source was created.

Verdict:

`equivalence_rule_implemented=true`

## Phase 6 - Tests

Evidence:

- `pool_equivalence_rule_evidence/py_compile.txt`
- `pool_equivalence_rule_evidence/targeted_unittest.txt`
- `pool_equivalence_rule_evidence/full_unittest_discover.txt`
- `pool_equivalence_rule_evidence/py_compile_after_success_split.txt`
- `pool_equivalence_rule_evidence/targeted_unittest_after_success_split.txt`
- `pool_equivalence_rule_evidence/full_unittest_discover_after_success_split.txt`

Final local tests:

| Check | Result |
|---|---|
| py_compile | PASS |
| targeted `tests.unit.test_v7_users_autoswitch_policy` | PASS, 70 tests |
| full `unittest discover tests` | PASS, 370 tests |

Added test coverage:

- legacy two-LARGE POOL rule still promotes;
- equivalence promotes only with operator approval;
- equivalence review does not promote without operator approval;
- rollback history blocks equivalence;
- nonzero planner demand blocks equivalence.

Verdict:

`tests_pass=true`

## Phase 7 - Safe Deploy

Push:

`Updatesystem` pushed to GitHub through commit `6e8eb4ede049d176f9225f8ec11458b8e9028569`.

Safe deploy:

`deploy-z8-14-Updatesystem-6e8eb4e-20260607T181029`

Evidence:

- `pool_equivalence_rule_evidence/safe_deploy_after_success_split.json`
- `pool_equivalence_rule_evidence/final_truth_check.json`
- `pool_equivalence_rule_evidence/final_convergence_status.json`

Final gates:

| Gate | Result |
|---|---|
| safe deploy | PASS |
| truth check | PASS / FULLY_ALIGNED |
| convergence status | PASS / ALIGNED |
| runtime_action_safe | true |

Verdict:

`deploy_pass=true`

## Phase 8 - POOL Promotion Review

Production review command:

`/usr/local/bin/v7-users-autoswitch --promote-authority-to POOL --authority-promotion-operation-id runtime_autoswitch_0425741b308df19ccc0c1e03 --pretty`

No confirmation token was provided. This was intentional because the program forbids automatic POOL promotion.

Evidence:

- `pool_equivalence_rule_evidence/pool_promotion_review_no_confirm.json`
- `pool_equivalence_rule_evidence/pool_equivalence_snapshot_refresh.json`
- `pool_equivalence_rule_evidence/pool_promotion_review_after_refresh_no_confirm.json`
- `pool_equivalence_rule_evidence/final_snapshot_refresh.json`
- `pool_equivalence_rule_evidence/final_pool_promotion_review_no_confirm.json`

Final production review result:

| Field | Value |
|---|---|
| status | DENIED |
| users_moved | 0 |
| autoswitch_apply_run | false |
| routing_mutation_performed | false |
| evidence_valid | false |
| equivalence_accepted | false |
| equivalence_blocker | pool_equivalence_requires_3600s_large_stability_window |

The final review also includes `missing_explicit_authority_promotion_confirmation`, as expected for a no-confirm review. That is not the material blocker in this program because POOL promotion was not allowed to execute automatically.

Verdict:

`pool_promotion_review_complete=true`

## Phase 9 - Decision

POOL promotion is denied.

Single material blocker:

`pool_equivalence_requires_3600s_large_stability_window`

Meaning:

The equivalence rule is now available and correctly deployed, but the previous LARGE feedback records still carry `stability_window_seconds=0`. The system needs canonical stability materialization through the existing feedback/governance owner before POOL promotion can be approved.

Do not manually edit JSONL state.

Do not bypass the promotion owner.

Do not promote POOL with a report-only stability claim.

## Final Verdicts

| Verdict | Value |
|---|---|
| rule_intent_understood | true |
| equivalence_review_complete | true |
| equivalence_safe | true |
| equivalence_rule_defined | true |
| equivalence_rule_implemented | true |
| tests_pass | true |
| deploy_pass | true |
| pool_promotion_review_complete | true |
| pool_promotion_approved | false |
| single_blocker | pool_equivalence_requires_3600s_large_stability_window |
| SAFE_NEXT_STEP | PROGRAM_LARGE_STABILITY_WINDOW_CANONICAL_FEEDBACK_MATERIALIZATION_AND_POOL_PROMOTION_APPROVAL |

## Safe Next Step

Run:

`PROGRAM_LARGE_STABILITY_WINDOW_CANONICAL_FEEDBACK_MATERIALIZATION_AND_POOL_PROMOTION_APPROVAL`

That program must:

1. Locate the existing feedback/governance owner for stability materialization.
2. Prove the 3600 second LARGE stability window from runtime truth.
3. Materialize stability into canonical feedback/promotion evidence through the owner.
4. Re-run POOL promotion review.
5. If equivalence is accepted, request explicit operator approval before actual POOL promotion.

No users should be moved.

No autoswitch apply should run.

No manual JSONL editing should occur.
