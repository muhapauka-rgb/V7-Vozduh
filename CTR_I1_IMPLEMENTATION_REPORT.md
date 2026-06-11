# CTR.I1 Implementation Report

Project: V7 Vozduh

Program: `CTR.I1 CTR ADVISORY + GOVERNANCE EVIDENCE + POOL SOFT INFLUENCE IMPLEMENTATION`

Date: 2026-06-11

Safety envelope:

- runtime mutation: not performed
- user movement: not performed
- autoswitch apply: not performed
- routing changes: not performed
- packet bypass: not performed
- restore barrier changes: not performed
- execution authority changes: not performed
- deploy: not performed

## 1. Executive Summary

CTR.I1 moves Channel Trust & Recovery from architecture/design into safe advisory influence.

Implemented:

- planner-facing CTR advisory evidence on every candidate;
- existing dry-run output now exposes CTR state, reason, recovery state/path, confidence, evidence summary, blocked actions and recommended action;
- existing operator surface now carries CTR governance evidence into recommendation rows and batch preview;
- recommendation execution contract now preserves CTR evidence for approval packet review;
- pool soft influence is computed as `soft_adjustment` and `advisory_score`;
- no hard gates, no target suppression, no score mutation and no routing changes were introduced;
- dedicated no-bypass tests were added.

Final verdict: `PASS`

## 2. Files Changed

Code:

- `tools/v7-users-autoswitch`
- `admin_core/operator_decision_surface.py`
- `admin_core/operator_execution_pipeline.py`
- `admin/v7-admin-api`

Tests:

- `tests/unit/test_ctr_i1_no_bypass.py`
- `tests/unit/test_operator_decision_surface.py`
- `tests/unit/test_operator_execution_pipeline.py`
- `tests/unit/test_v7_users_autoswitch_policy.py`

Reports/evidence:

- `CTR_I1_IMPLEMENTATION_REPORT.md`
- `CTR_I1_EVIDENCE/validation.md`
- `CTR_I1_EVIDENCE/no_bypass_certification.md`
- `CTR_I1_EVIDENCE/truth_source_and_duplication_audit.md`

## 3. Advisory Explainability Implementation

Implemented in `tools/v7-users-autoswitch`:

- `_snapshot_channel_trust_recovery_map()`
- `_ctr_advisory_for_egress()`
- `_ctr_soft_adjustment_for_state()`
- `_ctr_recommended_action_for_state()`
- `_ctr_blocked_actions_for_state()`

Every candidate can now expose:

- `ctr_advisory.state`
- `ctr_advisory.reason`
- `ctr_advisory.recovery_state`
- `ctr_advisory.recovery_path`
- `ctr_advisory.confidence`
- `ctr_advisory.evidence_summary`
- `ctr_advisory.blocked_actions`
- `ctr_advisory.recommended_action`
- `ctr_advisory.soft_adjustment`
- `ctr_advisory.advisory_score`

The existing explanation path also adds a short CTR advisory line for the chosen candidate.

Important guard:

- `planner_score_applied=false`
- `hard_gate_applied=false`
- `target_suppression_applied=false`

## 4. Governance Evidence Integration

Implemented in `admin_core/operator_decision_surface.py`:

- `_ctr_governance_evidence()`
- user recommendation rows now include `ctr_governance_evidence`;
- batch preview rows now include `ctr_governance_evidence`;
- `review_required` and `review_required_reasons` are surfaced for operator review.

Implemented in `admin_core/operator_execution_pipeline.py`:

- `recommendation_execution_contract()` now preserves CTR evidence;
- contract includes `ctr_authority` with all authority set to `none`.

CTR does not approve packets.

CTR does not deny packets directly.

CTR only contributes evidence.

## 5. Pool Soft Influence Implementation

Implemented soft influence values:

| State | Soft Adjustment | Runtime Effect |
|---|---:|---|
| TRUSTED | +20 | computed only |
| WATCH | 0 | computed only |
| NEW | -8 | computed only |
| RECOVERING | -12 | computed only |
| DEGRADED | -18 | computed only |
| QUARANTINED | -24 | computed only |

The adjustment is exposed as advisory evidence:

- `soft_adjustment`
- `advisory_score`

It is not added to `score_parts`.

It is not added to `candidate.score`.

It cannot change selected moves.

## 6. No-Bypass Tests

Added dedicated test suite:

- `tests/unit/test_ctr_i1_no_bypass.py`

Certified:

- CTR cannot create selected moves.
- CTR cannot approve packets.
- CTR cannot write restore barrier.
- CTR cannot mutate runtime.
- CTR cannot bypass planner.
- CTR cannot bypass governance.
- CTR cannot bypass capacity.
- CTR cannot bypass batch controls.

Key behavior test:

- CTR advisory visible on candidate.
- Candidate score unchanged.
- Candidate score parts unchanged.
- Selected move hash unchanged.
- Selected moves unchanged.

## 7. Validation Results

Validation evidence:

- `CTR_I1_EVIDENCE/validation.md`

Results:

- py_compile: PASS
- targeted CTR/operator/autoswitch tests: PASS, 109 tests
- full unit suite: PASS, 427 tests
- git diff whitespace check: PASS

Commands included:

- `python3 -m py_compile ...`
- `python3 -m unittest tests.unit.test_ctr_i1_no_bypass tests.unit.test_operator_decision_surface tests.unit.test_operator_execution_pipeline tests.unit.test_v7_users_autoswitch_policy`
- `python3 -m unittest discover tests`
- `git diff --check`

## 8. Duplication Audit

No duplicate planner was created.

No duplicate governance path was created.

No duplicate runtime authority was created.

No duplicate routing system was created.

No duplicate snapshot family was created.

CTR reuses:

- planner owner: `tools/v7-users-autoswitch`
- governance evidence path: `admin_core/operator_execution_pipeline.py`
- operator view path: `admin_core/operator_decision_surface.py`
- admin drawer: `admin/v7-admin-api`
- canonical CTR truth: `trust-evolution-summaries.channel_trust_recovery`

## 9. Truth Source Audit

Canonical CTR truth remains:

- `trust-evolution-summaries.channel_trust_recovery`

CTR.I1 did not add:

- `ctr-summaries`
- `channel-trust-recovery.json`
- any new CTR-specific snapshot family
- any new runtime state file

Runtime reads existing snapshot store only.

Admin reads existing snapshot store only.

Governance receives evidence derived from existing operator rows only.

## 10. Risk Review

Low risk:

- adding advisory fields to candidate JSON;
- adding governance evidence to recommendation rows;
- exposing review-required reasons;
- adding no-bypass tests.

Medium future risk:

- using CTR soft adjustment in real score;
- adding packet validation semantics for DEGRADED/QUARANTINED.

High future risk:

- hard suppressing targets before emergency matrix tests;
- making QUARANTINED a runtime hard gate without single-channel and degraded-pool scenarios;
- allowing CTR to deny packets directly.

CTR.I1 avoids all high-risk actions.

## 11. Runtime Safety Review

Runtime safety flags:

- users_moved=0
- autoswitch_apply_run=false
- runtime_mutation_performed=false
- routing_changed=false
- deploy_performed=false
- restore_barrier_changed=false
- packet_bypass_created=false
- execution_authority_changed=false

Authority flags:

- planner_decision_owner=`tools/v7-users-autoswitch`
- governance_authority=`none`
- runtime_execution_authority=`none`
- selected_moves_write_authority=`none`

## 12. Final Verdict

Final verdict: `PASS`

Final flags:

- ctr_advisory_explainability_implemented=true
- ctr_governance_evidence_integrated=true
- ctr_pool_soft_influence_computed=true
- ctr_pool_soft_influence_applied_to_score=false
- hard_gates_added=false
- target_suppression_added=false
- routing_behavior_changed=false
- users_moved=0
- autoswitch_apply_run=false
- runtime_mutation_performed=false
- no_bypass_tests_created=true
- validation_pass=true
- duplication_audit_pass=true
- truth_source_audit_pass=true
- safe_next_step=CTR.I2_governance_review_required_semantics_and_packet_evidence_preview
