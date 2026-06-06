# RULE_ORIGIN_REPORT

Project: V7 Vozduh

Program: `PROGRAM_MEDIUM_BATCH_CERTIFICATION_RULE_REVIEW_AND_EVIDENCE_EQUIVALENCE_DECISION`

Scope: certification rule review only. No runtime mutation, no user movement, no apply, no authority promotion.

## Rule Location

The current MEDIUM_BATCH certification rule is implemented in `tools/v7-users-autoswitch` in `_authority_certification_rules`.

Relevant rule:

```text
MEDIUM_BATCH:
  required_successful_small_batch_runs: 2
  requires_no_recent_rollback_or_verification_failure: true
  requires_trust_prediction_recommendation_feedback: true
```

Source references:

- `tools/v7-users-autoswitch`, `_authority_certification_rules`, lines around `1997-2000`.
- `PROGRAM_MEDIUM_BATCH_AUTHORITY_PROMOTION_DECISION_AND_PACKET_PREPARATION_REPORT.md`, rule audit section.
- `medium_batch_authority_evidence/phase2_4_rule_audit_and_promotion_decision.json`.

## Origin Rationale

The rule exists as an authority promotion guard between:

- current certified runtime scope: `SMALL_BATCH`, budget 2
- next runtime scope: `MEDIUM_BATCH`, budget 5

The safety objective is to prevent a direct promotion from one successful 2-user governed run into a 5-user authority class without proving repeatability of the governed execution envelope.

The rule is not only a throughput rule. It is primarily a governance repeatability rule.

## Risk Model

The second SMALL_BATCH run was designed to mitigate these risks:

| Risk | Why it matters before MEDIUM_BATCH |
| --- | --- |
| Repeatability risk | One successful governed run may prove the path once, but not prove repeat behavior under a fresh packet, fresh restore barrier, and fresh selected move hash. |
| Packet lineage risk | MEDIUM_BATCH needs confidence that approval packet generation and replay protection behave consistently across more than one governed execution. |
| Rollback envelope risk | MEDIUM_BATCH expands rollback scope. A second SMALL_BATCH run gives another rollback-ready envelope before increasing blast radius. |
| Planner variance risk | A second run proves the planner can select and verify a bounded cohort again, not only preserve stability of the previous cohort. |
| Feedback closure risk | A second run proves outcome, trust, prediction, recommendation, and closure feedback can be materialized repeatedly. |
| Blast-radius escalation risk | Moving from 2 to 5 users increases impact by 2.5x. The rule requires repeated evidence before the jump. |

## Safety Objective

The rule aims to certify:

1. at least one successful SMALL_BATCH movement,
2. no recent rollback or verification failure,
3. feedback materialized,
4. one additional independent SMALL_BATCH governed execution cycle before budget 5 is authorized.

## Rule Origin Verdict

`rule_origin_identified=true`

The rule came from the authority certification model, not from an ad hoc report. Its rationale is a conservative blast-radius escalation guard: prove repeatability at budget 2 before allowing budget 5.

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO
