# PROGRAM POOL PROMOTION RULE INTENT REVIEW AND SECOND LARGE EVIDENCE DECISION REPORT

Project: V7 Vozduh
Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`
Report time: 2026-06-07

## Mission Result

The second `LARGE_BATCH` requirement still serves a unique safety purpose.

POOL promotion readiness is not justified yet.

No users were moved. No apply was run. POOL was not promoted. Authority was not changed. Planner policy was not changed. No synthetic failures or artificial movement were created.

## Phase 1 - Rule Origin Audit

Evidence:

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`
- `docs/reports/evidence/pool_promotion_rule_intent_review_evidence/phase4_5_6_7_intent_coverage_equivalence_decision.json`

The rule is defined in `AUTHORITY_PROMOTION_RULES["POOL"]`:

- Source authority: `LARGE_BATCH`
- Target authority: `POOL`
- Required successful runs: `2`
- Minimum users per run: `10`
- Run label: `large_batch`
- Evidence floor: `two_successful_large_batch_runs_with_feedback_closure_and_pool_no_regression_window`
- Count blocker: `two_successful_large_batch_operation_ids_required`
- Failure blocker: `pool_evidence_validation_failed`
- Required feedback: `outcome`, `trust`, `prediction`, `recommendation`, `closure`
- Required stability window: `3600` seconds

The unit test `test_authority_promotion_to_pool_requires_two_large_runs_and_no_regression_window` encodes the same intent: two large operation IDs, each with 10 users and `stability_window_seconds=3600`, are required before POOL promotion succeeds.

Rule origin identified: true

## Phase 2 - Rule Intent Analysis

The second successful `LARGE_BATCH` is not just a bureaucratic duplicate. It is designed to prove:

- Repeatability: the system can execute a 10-user governed cohort more than once.
- Rollback confidence: rollback remains unnecessary across independent large operations.
- Feedback confidence: all feedback streams materialize across more than one large operation.
- Planner confidence: planner, packet, restore barrier, approved plan lock, apply, verify and feedback are repeatable at large blast radius.
- Stability confidence: POOL promotion has a 3600 second no-regression/stability evidence floor.
- Operator confidence: one successful large run cannot automatically unlock a 25-user runtime budget.

Rule intent understood: true

## Phase 3 - Current Evidence Inventory

Evidence file:

- `docs/reports/evidence/pool_promotion_rule_intent_review_evidence/phase3_current_evidence_inventory.json`

Current certified evidence:

- CANARY certified.
- SMALL_BATCH certified.
- MEDIUM_BATCH certified.
- LARGE_BATCH certified.
- One real LARGE operation completed:
  - Operation ID: `runtime_autoswitch_0425741b308df19ccc0c1e03`
  - Users moved: `10`
  - Terminal state: `APPLIED`
  - Verification: all `verify_rc=0`
  - Rollback required: false
  - Feedback materialized: true
- LARGE stability review completed:
  - all 10 moved users remained on expected routes.
- POOL preparation completed:
  - active users: `25`
  - routing users: `25`
  - planner-visible users: `25`
  - synthetic users created through existing owner: `7`
- Planner health:
  - snapshot gate clean.
  - current planner candidates: `0`
  - no current planner-approved second LARGE movement.
- Truth:
  - truth check: `PASS`
  - blockers: `[]`
- Convergence:
  - retry convergence: `ALIGNED`
  - runtime action safe: `true`

Current evidence inventory complete: true

## Phase 4 - Intent Coverage Review

Covered:

- Single LARGE execution correctness: proven.
- LARGE feedback materialization: proven.
- Post-LARGE user and route stability: proven.
- 25-user planner/routing visibility: proven.
- Truth and convergence health: proven.
- Synthetic user capacity for POOL-scale testing: proven.

Not covered:

- Second independent LARGE execution repeatability.
- Second LARGE rollback and feedback repeatability.
- Operation-linked 3600 second POOL no-regression/stability evidence.

Important detail:

The successful LARGE feedback rows have `stability_window_seconds=0`. The later LARGE stability review is useful operational evidence, but it is not equivalent to two independent `LARGE_BATCH` operation IDs with operation-linked 3600 second stability evidence, which is what the promotion owner currently validates.

Intent coverage complete: true

## Phase 5 - Equivalence Review

Question:

Does one certified LARGE_BATCH plus stable platform plus POOL preparation plus 25-user readiness equal two successful LARGE_BATCH runs?

Answer:

No.

Reason:

The current evidence proves that the platform can execute one 10-user governed cohort and remain stable afterward. It also proves that the platform now has 25 planner-visible users and is prepared for POOL-scale review. But it does not prove independent repeatability of the full 10-user execution lifecycle.

The missing evidence is not theoretical. It is exactly what the rule checks:

- second operation ID,
- at least 10 users,
- feedback closure,
- rollback not required,
- 3600 second stability/no-regression evidence.

Equivalence review complete: true

## Phase 6 - Staging User Option Review

Controlled staging/synthetic users are valid for user-base capacity. They are not valid as fake movement evidence.

Current state:

- 25 active routing/planner-visible users exist.
- Planner currently reports `candidate_moves_total=0`.
- Snapshot gate is clean.
- Production is healthy and balanced.

If the planner later selects legitimate moves involving staging users, a second LARGE run could be valid. But creating users, failures, bad-channel placement, target drift, or policy changes just to manufacture movement would weaken certification quality and violate the safety model.

Staging user model valid: false for manufacturing second LARGE evidence.

Staging user model valid: true only if future planner-selected movement appears naturally under existing rules.

## Phase 7 - Decision

Decision:

`SECOND_LARGE_STILL_REQUIRED`

Single missing criterion:

`second independent planner-approved LARGE_BATCH execution with >=10 users, feedback closure, rollback_required=false, and 3600s no-regression/stability evidence`

POOL promotion readiness is not justified yet.

## Phase 8 - Next Step Review

Safe next step:

`PROGRAM_SECOND_LARGE_BATCH_EVIDENCE_ACQUISITION_WITH_NO_MANUFACTURED_MOVEMENT`

That program should:

- remain under `LARGE_BATCH` authority,
- monitor for legitimate planner-approved LARGE movement,
- not create synthetic failures,
- not force targets,
- not change planner policy,
- not place users on bad channels,
- not bypass packet/restore barrier/approved plan lock,
- execute a second LARGE only if planner selects at least 10 legitimate moves,
- materialize feedback,
- observe or materialize the required 3600 second no-regression/stability evidence,
- then retry POOL promotion with two real LARGE operation IDs.

Alternative:

If the project wants to change the rule, that must be a separate implementation/governance program. This review does not approve changing the rule, because the original rule still protects unique evidence: independent repeatability at 10-user blast radius.

## Final Verdicts

rule_origin_identified=true

rule_intent_understood=true

current_evidence_inventory_complete=true

intent_coverage_complete=true

equivalence_review_complete=true

second_large_still_required=true

pool_promotion_readiness_justified=false

staging_user_model_valid=false

single_missing_criterion=second_independent_planner_approved_large_batch_execution_with_10_users_feedback_closure_rollback_false_and_3600s_no_regression_evidence

SAFE_NEXT_STEP=PROGRAM_SECOND_LARGE_BATCH_EVIDENCE_ACQUISITION_WITH_NO_MANUFACTURED_MOVEMENT

## Operator Conclusion

The current safety rule is still doing useful work.

It prevents a single successful 10-user operation from unlocking a 25-user runtime budget. The system is healthy and prepared, but health plus preparation is not the same as repeatable large execution evidence.

The next move should be patient and governed: wait for a legitimate second LARGE opportunity, or run a dedicated implementation program only if the team deliberately chooses to redesign the POOL promotion rule.
