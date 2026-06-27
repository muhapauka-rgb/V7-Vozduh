# Master Rollback Learning Audit

## Summary

A4 bounded collection stopped correctly on a real verification failure:

`10.7.0.24 vless -> awg3`

Apply happened, route verification failed, rollback completed to `vless`.

## Action Performed

Audit only. No code change. No runtime mutation. No new owner. No new backlog item.

## Objective Observations

| Field | Value |
| --- | --- |
| Packet | `pkt_preview_0e0612a563a0c4b946d5a319` |
| Decision | `decision_commit_8b272728c53a95a1b54d1e1e` |
| Operation | `runtime_autoswitch_a4bfd69157ec127d8fbba808` |
| User | `10.7.0.24` |
| Move | `vless -> awg3` |
| Apply | `YES` |
| Verification | `FAIL` |
| Rollback | `ROLLBACK_COMPLETED` |
| Final user state | `vless` |

## Exact Verification Failure

The switch command reported the user moved to `awg3`, but immediate route verification found:

- registry/assignment expected `awg3`;
- table route still defaulted to `tun0`;
- route_get still used `tun0`;
- verifier returned `V7_USER_ROUTE_CHECK=FAIL`.

This is a valid verification failure, not proof that the verifier is broken.

## Stage Trace

| Stage | Owner | Expected | Actual | Verdict |
| --- | --- | --- | --- | --- |
| Decision | `admin_core/operator_execution_pipeline.py` | one committed governed decision | committed | OK |
| Packet | `admin_core/operator_execution.py` | preserve packet identity | preserved | OK |
| Lease | `admin_core/operator_execution.py` | bind exact packet | bound | OK |
| Apply | `tools/v7-users-autoswitch` | one user move | applied | OK |
| Verify | `tools/v7-users-autoswitch` | prove route matches target | failed | OK |
| Rollback | `tools/v7-users-autoswitch` | restore to source | completed | OK |
| Feedback | `tools/v7-governed-canary-dry-run-cycle` + `admin_core/operator_execution_feedback.py` | classify rollback/failure as rollback/failure learning | recorded `SUCCESS` | DEFECT |
| A4 collection | `tools/v7-governed-canary-dry-run-cycle` | stop on failed verification | stopped | OK |

## Root Cause

Rollback was expected and correct.

The defect is in feedback materialization: the governed transaction feedback builds:

`execution_result = {"success": true, "result": "applied"}`

even when verification failed and rollback completed.

`classify_outcome()` sees `success=true` / `applied` before rollback context dominates, so the materialized feedback becomes:

`outcome_status=success`, `outcome_quality=SUCCESS`, `trust_delta=+1.0`, `recommendation_delta=+1.0`

This is wrong for `verification FAIL + rollback COMPLETED`.

## Classification

`IMPLEMENTATION_DEFECT`

More specific:

`FEEDBACK_LEARNING_CLASSIFICATION_DEFECT`

Not planner defect. Not rollback defect. Not architecture defect. Not new owner.

## Planner Analysis

No evidence proves planner selected an invalid candidate before apply:

- candidate was inside A4 scope;
- one-user blast radius held;
- packet/lease/restore barriers held;
- target was live enough to reach apply.

The observed failure occurred at post-apply route verification.

## Rollback Analysis

Rollback was correct:

- rollback attempted automatically after verification failure;
- rollback returned `rc=0`;
- user returned to `vless`;
- lease terminalized as `ROLLBACK_FINISHED`;
- bounded collection stopped.

## Learning Analysis

Learning should increase, but as rollback/failure learning, not success learning.

Expected learning:

- reduce recommendation confidence for this exact condition;
- mark suitability/prediction as degraded or watch;
- increase rollback confidence because rollback succeeded;
- keep A4 evidence as real observed outcome;
- do not count this as successful move evidence;
- do not promote authority or runtime automation.

## Evidence Impact

The transaction is real evidence, but it must be consumed as rollback/failure evidence.

It must not increase success-rate, trust, recommendation, or promotion readiness as if the move succeeded.

## Existing Owner Mapping

| Finding | Existing owner |
| --- | --- |
| Route verification failure | `tools/v7-users-autoswitch` |
| Rollback execution | `tools/v7-users-autoswitch` |
| Transaction feedback payload | `tools/v7-governed-canary-dry-run-cycle::materialize_governed_transaction_feedback` |
| Outcome classification | `admin_core/operator_execution_feedback.py::classify_outcome` |
| A4 evidence consumption | `admin_core/autonomy_trust_acceleration.py`; `tools/v7-autonomy-trust-evidence-inventory` |
| Backlog owner | `A4` primary; `B16` secondary for rollback authority after verification reliability |

## Minimal Correction

Do not continue bounded A4 collection until existing feedback materialization handles:

`apply YES + verification FAIL + rollback COMPLETED`

as rollback/failure learning, not success learning.

Exact existing files:

- `tools/v7-governed-canary-dry-run-cycle`
- `admin_core/operator_execution_feedback.py`
- tests around governed transaction feedback and rollback outcome classification.

## Capability Progress

A4 remains `93 / 156 = 59.6%`.

The third transaction produced real evidence but exposed a learning-classification defect.

## Backlog Progress

No new backlog item required. Existing owner: `A4`.

## Production Maturity

No maturity increase. Runtime automation remains disabled. Authority not expanded.

## Re-audit Rule

Re-audit only after the feedback classification fix is implemented and a rollback-completed governed transaction is classified as rollback/failure learning.

## Final Verdict

`ROLLBACK_REQUIRES_IMPLEMENTATION`
