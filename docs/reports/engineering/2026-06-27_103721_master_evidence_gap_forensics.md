# Master Evidence Gap Forensics

Status: COMPLETE
Date: 2026-06-27
Language: Russian

## Summary

Проверка показала, что `missing_candidate_outcomes = 69` является ожидаемым текущим значением, а не первичным дефектом счетчика.

До завершенной governed transaction в A4 было `70` недостающих representative candidate outcomes. После production transaction инвентарь показывает:

- `candidate_count = 156`
- `candidate_outcomes_consumed = 87`
- `missing_candidate_outcomes = 69`
- `coverage_ratio = 0.5577`

Это означает, что один новый реальный outcome был засчитан в candidate coverage.

Root cause A4-блокировки находится дальше по цепочке: outcome появился в switch/audit evidence, но не был материализован как closed verified feedback/learning record через `admin_core.operator_execution_feedback`. Поэтому A4 все еще видит `no_verified_learning_growth_from_closed_real_outcomes`.

## Action Performed

Выполнен forensic-аудит без изменения кода, формул, threshold, Runtime behavior, authority, backlog или architecture.

## Production Object Traced

Latest real governed production transaction:

- packet: `pkt_preview_a69fe12e51c528c2a0402c0c`
- decision: `decision_commit_1ecf28e69a44b11699ebef0d`
- operation: `govdry_2fb035b74bb3a5af0ecf7c13`
- lease: `execlease_5f4d34d80de62bf6445d73b4`
- user: `10.7.0.5`
- movement: `awg0 -> awg3`
- verification: `PASS`
- rollback: `NOT_REQUIRED`
- terminal state: `EXECUTION_FINISHED`

## Dependency Graph

Current Program State
-> Action-Class Runtime Enablement
-> Suitability Quality Model
-> Candidate Outcome Reality Collection
-> Evidence Inventory
-> Intelligence Workers
-> Decision / Switch / Feedback Records
-> Outcome / Verification
-> Apply
-> Governed Transaction
-> Decision Commit
-> Reality

Learning side:

Current Program State
-> Action-Class Runtime Enablement
-> Decision Outcome Learning
-> `admin_core.operator_execution_feedback.decision_outcome_learning_model`
-> closed feedback / closure records
-> materialized execution feedback
-> verified outcome
-> apply / verification

## Propagation Result

### Candidate outcome path

Owner:

- `admin_core.intelligence_workers`

Decision point:

- `build_candidate_outcome_rows`
- `_candidate_keys`
- `_switch_history_arrival_evidence`

Behavior:

- candidate key is a `(user, channel)` pair.
- production `switch-history.jsonl` contains the latest movement.
- the movement was consumed as a real candidate outcome.

Expected value:

- `missing_candidate_outcomes`: `70 -> 69`

Actual value:

- `missing_candidate_outcomes = 69`

Verdict:

- `EXPECTED_BEHAVIOR`

### Feedback / learning path

Owner:

- `admin_core.operator_execution_feedback`

Decision point:

- `execution_feedback_contract`
- `materialized_feedback_records`
- `decision_outcome_learning_model`

Expected:

- successful transaction should create closed feedback / closure records.
- `decision_outcome_learning_model` should consume them.
- A4 should see verified learning growth from closed real outcomes.

Actual:

- production inventory reports `decision_learning.rows = []`
- `knowledge_gained = 0`
- `no_verified_learning_growth_from_closed_real_outcomes` remains active.
- latest transaction appears in switch/audit/lease/restore-barrier evidence, but not in the closed feedback/learning stores consumed by the learning model.

Verdict:

- propagation stops between terminalized governed transaction and materialized feedback/closure records.

## Exact Propagation Stop

Stop:

Apply / verification terminalized the transaction, but terminal outcome was not materialized into the feedback/closure records consumed by `operator_execution_feedback`.

Observed present:

- switch history record
- audit record
- operator execution audit record
- governance lifecycle restore-barrier/lease records

Observed missing for latest transaction:

- closed execution feedback row
- decision outcome learning row
- verified learning growth row

## Root Cause

The completed governed transaction updates candidate evidence through switch history, but the transaction workflow does not complete the feedback/learning materialization path required by A4.

The blocker is not that `69` failed to decrease. It decreased correctly.

The blocker is that A4 requires both:

- representative candidate outcome coverage
- verified learning growth from closed real outcomes

Only the first path advanced.

## Classification

Primary classification:

- `WORKFLOW_DEFECT`

Secondary affected area:

- `LEARNING_EVIDENCE_MATERIALIZATION`

Why:

- Runtime apply and verification succeeded.
- Evidence inventory correctly counted one more representative candidate outcome.
- The workflow did not persist the terminal outcome into the existing learning/closure owner.

## Existing Owner Mapping

Primary owner:

- `tools/v7-users-autoswitch`

Relevant existing owner path:

- `Autoswitch.apply`
- `Autoswitch.finalize_operation`
- `_terminal_verdict`
- `_terminal_audit_reference`
- `_emit_terminal_audit`

Learning owner:

- `admin_core/operator_execution_feedback.py`

Relevant functions:

- `execution_feedback_contract`
- `materialized_feedback_records`
- `decision_outcome_learning_model`

Inventory / promotion owner:

- `admin_core/autonomy_trust_acceleration.py`
- `tools/v7-autonomy-trust-evidence-inventory`

Candidate evidence owner:

- `admin_core/intelligence_workers.py`

## Existing Backlog Mapping

Existing backlog owner:

- `A4_MATERIALIZE_REPRESENTATIVE_OUTCOME_EVIDENCE_FOR_FIRST_ACTION_CLASS`

A4 remains the correct owner because it explicitly covers:

- representative real outcome evidence
- outcome leverage
- feedback / learning recognition
- promotion readiness for the first action class

## Expected vs Actual

| Field | Expected after one successful transaction | Actual | Verdict |
| --- | --- | --- | --- |
| `missing_candidate_outcomes` | `70 -> 69` | `69` | PASS |
| `candidate_outcomes_consumed` | increase by 1 | `87 / 156` | PASS |
| `decision_learning.rows` | at least one closed latest outcome | `[]` | FAIL |
| `knowledge_gained` | `> 0` | `0` | FAIL |
| A4 promotion | still blocked if learning missing | blocked | EXPECTED |
| Runtime automation | disabled | disabled | PASS |
| Authority expansion | none | none | PASS |

## Minimal Correction

Do not change evidence formulas.

Do not lower thresholds.

Do not create synthetic evidence.

Minimal implementation recommendation:

Extend the existing governed transaction / autoswitch terminal path so a successful real governed transaction materializes an `operator_execution_feedback` contract and writes the existing feedback/closure records consumed by `decision_outcome_learning_model`.

Required behavior:

- only after real apply + verification
- preserve packet, decision, operation, selected move hash, user, source, target
- record rollback/no-rollback result
- write closed feedback/closure records through existing owner
- A4 inventory then consumes verified learning growth naturally

## Need New Owner / Backlog / Architecture

| Question | Verdict |
| --- | --- |
| Need New Owner | FALSE |
| Need New Backlog Item | FALSE |
| Need New Architecture | FALSE |
| Need New Runtime Path | FALSE |
| Need Formula Change | FALSE |
| Need Threshold Change | FALSE |

## Capability Progress

| Area | Current |
| --- | --- |
| Engineering Maturity | `100%` |
| Production Maturity | `24%` |
| Tier A backlog progress | `3 / 6 = 50%` |
| Overall backlog progress | `3 / 34 = 8.8%` |
| A4 candidate evidence | `87 / 156 = 55.77%` |
| A4 missing candidate outcomes | `69` |
| A4 learning growth | `0` |

## Production Impact

The latest transaction helped representative candidate coverage, but did not yet advance verified learning maturity. A4 is correctly blocked until closed outcome learning is materialized from real observed results.

## Runtime Impact

No runtime behavior changed during this audit.

Runtime automation remains disabled.

No users were moved by this audit.

## Canonical Knowledge

No canonical owner update was required.

The finding is an implementation/workflow materialization gap inside existing A4 ownership, not a new product, policy, runtime, or architecture truth.

## Evidence

Production inventory:

- `candidate_count = 156`
- `candidate_outcomes_consumed = 87`
- `missing_candidate_outcomes = 69`
- `real_missing_experience = 69`
- `decision_learning.rows = []`
- `knowledge_gained = 0`

Production stores checked:

- switch history: transaction present
- audit: transaction present
- operator execution audit: transaction present
- governance lifecycle: lease / restore-barrier records present
- feedback / closure learning rows for latest transaction: absent

## Next Step

Continue A4 through existing owners:

`A4_FIX_GOVERNED_TRANSACTION_FEEDBACK_MATERIALIZATION_IN_EXISTING_AUTOSWITCH_OWNER`

Expected completion evidence:

- latest governed transaction appears in closed execution feedback records
- `decision_outcome_learning_model` reports non-zero closed outcome learning
- A4 readiness no longer reports `no_verified_learning_growth_from_closed_real_outcomes` for real completed transactions

## Re-audit Rule

Do not repeat this forensic audit unless:

- A4 feedback materialization is implemented;
- production evidence again fails to propagate;
- Current Program State contradicts the evidence inventory;
- operator explicitly requests re-audit.

Final verdict:

`EVIDENCE_GAP_ROOT_CAUSE_FOUND`
