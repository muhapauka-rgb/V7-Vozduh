# Feedback / Learning Materialization Forensics

Status: COMPLETE
Date: 2026-06-27
Language: Russian

## Summary

Forensic-аудит подтвердил точную причину A4-блокировки после успешной governed transaction.

Реальная transaction:

- packet: `pkt_preview_a69fe12e51c528c2a0402c0c`
- decision: `decision_commit_1ecf28e69a44b11699ebef0d`
- operation: `govdry_2fb035b74bb3a5af0ecf7c13`
- lease: `execlease_5f4d34d80de62bf6445d73b4`
- user: `10.7.0.5`
- movement: `awg0 -> awg3`
- apply: `YES`
- verification: `PASS`
- rollback: `NOT_REQUIRED`
- lease terminal state: `EXECUTION_FINISHED`

Candidate coverage advanced correctly:

- `missing_candidate_outcomes`: `70 -> 69`

But verified feedback / learning did not advance:

- `decision_learning.rows = []`
- `knowledge_gained = 0`
- `no_verified_learning_growth_from_closed_real_outcomes` remains active

Primary root cause:

`tools/v7-governed-canary-dry-run-cycle.execute_governed_transaction` completes apply, verification and lease terminalization, but does not call the existing feedback materialization owner after successful apply.

## Full Forward Materialization Graph

| Node | Owner | File / Function | Expected | Actual | Status |
| --- | --- | --- | --- | --- | --- |
| Apply | Autoswitch owner | `tools/v7-users-autoswitch`, `Autoswitch.apply` | One selected move applied | User moved `awg0 -> awg3` | PRESENT |
| Verification | Autoswitch owner | `tools/v7-users-autoswitch`, `--verify` | Route verification PASS | `verify_rc=0`, PASS | PRESENT |
| Terminal verdict | Autoswitch owner | `Autoswitch.finalize_operation`, `_terminal_verdict` | terminal state APPLIED | Apply payload terminalized | PRESENT |
| Terminal audit | Autoswitch owner | `_terminal_audit_reference`, `_emit_terminal_audit` | runtime terminal audit emitted | user switch/audit records exist | PRESENT |
| Lease finish | Packet/lease owner | `admin_core.operator_execution.finish_execution_lease` | lease `EXECUTION_FINISHED` | lease terminalized | PRESENT |
| Feedback contract | Feedback owner | `operator_execution_feedback.execution_feedback_contract` | SUCCESS feedback contract | not called by transaction workflow | MISSING |
| Materialized records | Feedback owner | `materialized_feedback_records` | outcome/trust/prediction/recommendation/closure records | absent for `pkt_preview_a69...` | MISSING |
| Closed feedback row | Feedback owner | `closure-records.jsonl` | `execution_feedback` CLOSED row | absent for `pkt_preview_a69...` | MISSING |
| Decision learning model | Learning owner | `decision_outcome_learning_model` | row with SUCCESS and knowledge gained | rows empty for latest transaction | MISSING |
| Evidence inventory | Trust inventory owner | `v7-autonomy-trust-evidence-inventory` | learning growth consumed | `knowledge_gained=0` | BLOCKED |
| A4 readiness | OMP / A4 owner | `build_action_class_runtime_enablement_model` | learning blocker removed | blocker remains | BLOCKED |
| Current Program State | OMP state owner | `V7_CURRENT_PROGRAM_STATE.md` | A4 advances if learning proof exists | A4 remains `REAL_WORLD_LIMIT` | BLOCKED |

## Full Backward Dependency Graph

Current Program State blocker
-> A4 runtime enablement
-> `no_verified_learning_growth_from_closed_real_outcomes`
-> `decision_outcome_learning.knowledge_growth.knowledge_gained == 0`
-> `decision_outcome_learning_model` consumed no closed feedback rows
-> no matching feedback/closure records in feedback stores
-> `materialized_feedback_records` not called for the transaction
-> `execution_feedback_contract` not created for the transaction
-> governed transaction stopped after apply/lease terminalization
-> successful apply and verification exist in switch/audit stores only

## Exact Propagation Stop

Propagation stops immediately after governed transaction terminalization:

`execute_governed_transaction`
-> `run_autoswitch_apply`
-> `finish_execution_lease`
-> returns transaction payload
-> no feedback contract creation
-> no feedback record writes

The terminal outcome exists operationally, but not as a closed feedback/learning object.

## Whether Feedback Path Was Called

Verdict:

`NO`

Evidence:

- `rg` finds no call to `execution_feedback_contract` or `materialized_feedback_records` inside `tools/v7-governed-canary-dry-run-cycle` or `tools/v7-users-autoswitch`.
- Existing calls are in `admin/v7-admin-api` endpoint `/api/actions/execution-feedback-materialize` and unit tests.
- Production stores contain no latest transaction row in:
  - `execution-events.jsonl`
  - `runtime-trust.jsonl`
  - `proposal-records.jsonl`
  - `proposals.jsonl`
  - `closure-records.jsonl`

## Whether Feedback Contract Accepted / Rejected

Verdict:

`NOT_CALLED`

Counterfactual:

The existing contract accepts this transaction shape.

Using the real transaction fields with:

- execution result: applied
- verification result: verified / pass
- rollback result: empty
- user: `10.7.0.5`
- source: `awg0`
- target: `awg3`
- packet: `pkt_preview_a69fe12e51c528c2a0402c0c`

the existing owner produces:

- `outcome_status = success`
- `outcome_quality = SUCCESS`
- `closure_state = CLOSED`
- `knowledge_gained = 1`
- learning row count = `1`

So this is not contract rejection.

## Whether Feedback Record Was Written

Verdict:

`NO`

Expected stores:

- `/opt/v7/egress/state/execution-events.jsonl`
- `/opt/v7/egress/state/runtime-trust.jsonl`
- `/opt/v7/egress/state/proposal-records.jsonl`
- `/opt/v7/egress/state/proposals.jsonl`
- `/opt/v7/egress/state/closure-records.jsonl`

Actual:

No records match:

- `pkt_preview_a69fe12e51c528c2a0402c0c`
- `decision_commit_1ecf28e69a44b11699ebef0d`
- `govdry_2fb035b74bb3a5af0ecf7c13`
- `execlease_5f4d34d80de62bf6445d73b4`

## Whether Closure Record Was Written

Verdict:

`NO`

The latest matching closure rows are older records for different packets, such as `pkt_preview_5c4bcfaa59d769ced6d6e5dc`.

The latest successful transaction has no `execution_feedback` closure row.

## Whether Learning Read It

Verdict:

`NO`, because there was no feedback/closure record to read.

Learning owner:

- `admin_core.operator_execution_feedback.decision_outcome_learning_model`

Read input:

- bounded decision records assembled from audit + feedback stores by inventory/trust evolution.

Actual model output:

- `rows = []`
- `knowledge_gained = 0`

## Exact Missing Function / Rule

Missing function call:

- `operator_execution_feedback.execution_feedback_contract`
- `operator_execution_feedback.materialized_feedback_records`

Missing write behavior:

After `execute_governed_transaction` receives successful `apply_payload`, it must materialize existing feedback records through the existing feedback owner.

Current function:

- `tools/v7-governed-canary-dry-run-cycle.execute_governed_transaction`

Current condition:

- `apply_result.get("applied") == True`
- verification result PASS
- lease terminalized as `EXECUTION_FINISHED`

Missing condition handling:

- no call to feedback owner after this condition.

## Contract Analysis

| Field | Available from transaction? | Contract required? | Status |
| --- | --- | --- | --- |
| `packet_id` | YES | YES | OK |
| `decision_id` | YES | useful lineage | OK |
| `operation_id` | YES | audit/closure reference | OK |
| `lease_id` | YES | useful lineage | OK |
| `selected_move_hash` | YES | recommendation id | OK |
| `user` | YES | YES | OK |
| `source` | YES | YES | OK |
| `target` | YES | YES | OK |
| `action_class` | inferable from governed canary | useful | OK |
| `authority_tier` | inferable from transaction | useful | OK |
| `authority_generation` | YES | useful | OK |
| `apply_result` | YES | YES | OK |
| `verification_result` | YES | YES | OK |
| `rollback_result` | empty / NOT_REQUIRED | YES | OK |
| `terminal_state` | YES | useful | OK |
| `restore_barrier` | YES | useful | OK |
| `approved_plan_lock` | YES through apply payload | useful | OK |
| `timestamp` | YES | YES | OK |
| `real_outcome_flag` | implied by apply | required by policy | OK |
| `synthetic_flag` | false | required by policy | OK |
| `learning_eligible_flag` | not materialized | derived by feedback | MISSING WRITE |
| `representative_flag` | candidate coverage consumed | evidence dimension | OK for coverage |
| `failure_family` | not required for contract | optional | NOT_APPLICABLE |
| `recovery_family` | not required for contract | optional | NOT_APPLICABLE |
| `evidence_class` | real governed outcome | useful | OK |

The transaction has enough data to materialize feedback.

## Policy / Rule Analysis

No policy rule was found that intentionally excludes this transaction from learning.

Falsified exclusions:

- duplicate rule: no matching feedback id/packet row exists.
- observation window: previous feedback rows are materialized immediately.
- cooldown: no evidence of learning exclusion.
- freshness: transaction passed live gates before apply.
- rollback/no-rollback: no-rollback is valid outcome.
- verification quality: verification passed.
- representative rule: candidate coverage consumed one outcome.
- action-class rule: current A4 governed learning class.
- user/cohort/target/source rule: candidate coverage accepted user/target pair.
- trust threshold: not required for recording real feedback.
- synthetic/real distinction: apply was real; no synthetic evidence.
- closed outcome rule: closure record missing, not rejected.

## Multi-Hypothesis Falsification

| Hypothesis | Verdict | Reason |
| --- | --- | --- |
| H1 feedback path never invoked | TRUE | No call path and no records. |
| H2 terminal audit lacks required fields | FALSE | Transaction has packet/user/source/target/apply/verify/hash. |
| H3 feedback contract rejects transaction | FALSE | Counterfactual contract returns SUCCESS/CLOSED/knowledge_gained=1. |
| H4 feedback record written but not closed | FALSE | No feedback record exists. |
| H5 feedback record closed but learning ignores it | FALSE | No matching closure exists. Older closures are read normally. |
| H6 learning works but inventory ignores it | FALSE | Inventory reads feedback stores; absent row is the issue. |
| H7 inventory works but Current Program State is stale | FALSE | Inventory itself reports no learning rows. |
| H8 transaction is not learning-eligible by policy | FALSE | No such exclusion found; real verified no-rollback outcome is eligible. |
| H9 successful no-rollback outcome is not learning | FALSE | Existing tests/older production rows treat success/no-rollback as HIGH learning. |
| H10 coverage and verified learning are separate by design | TRUE | Coverage advanced; learning requires separate feedback materialization. |
| H11 implementation defect in autoswitch / transaction terminal path | TRUE | Terminal path omits feedback materialization. |
| H12 implementation defect in operator_execution_feedback | FALSE | Owner works when called. |
| H13 expected behavior | FALSE | Expected to remain safe, but not expected to omit feedback for a completed real transaction. |

## Root Cause

Exactly one primary root cause:

`tools/v7-governed-canary-dry-run-cycle.execute_governed_transaction` does not materialize a successful governed transaction into the existing `operator_execution_feedback` records after apply/verification/lease terminalization.

Exact owner:

- Governed transaction owner: `tools/v7-governed-canary-dry-run-cycle`

Exact missing downstream owner call:

- `admin_core.operator_execution_feedback.execution_feedback_contract`
- `admin_core.operator_execution_feedback.materialized_feedback_records`

Exact condition:

- `apply_result.get("applied") == True`
- verification PASS
- terminal lease `EXECUTION_FINISHED`
- but no feedback materialization call.

## Root Cause Classification

`WORKFLOW_DEFECT`

Why not `LEARNING_DEFECT`:

- learning works when records exist.

Why not `FEEDBACK_DEFECT`:

- feedback contract and materialized records work when called.

Why not `READ_MODEL_DEFECT`:

- read model reads existing feedback rows.

Why not `POLICY_DEFECT`:

- no policy excludes this real verified outcome.

## Minimal Correction

Do not change formulas.

Do not lower thresholds.

Do not create synthetic evidence.

Do not create new owner/backlog/runtime path.

Minimal implementation:

Extend existing `tools/v7-governed-canary-dry-run-cycle.execute_governed_transaction`.

After successful apply and verification, call existing feedback owner:

1. Build `execution_feedback_contract` from:
   - packet id
   - decision id / operation id as references
   - selected move hash as recommendation id
   - user
   - source
   - target
   - apply result
   - verification result
   - rollback/no-rollback result
2. Materialize records with `materialized_feedback_records`.
3. Append records to existing stores:
   - `execution-events.jsonl`
   - `runtime-trust.jsonl`
   - `proposal-records.jsonl` or `proposals.jsonl` according to existing store convention
   - `closure-records.jsonl`
4. Preserve fail-closed behavior:
   - if feedback write fails after apply, report explicit workflow defect and do not count certification until materialization is present.

## Tests Required

Focused tests:

1. Governed transaction success calls feedback materialization exactly once.
2. Successful apply + PASS verification writes outcome, trust, prediction, recommendation, and closure rows.
3. Closure row has `closure_state=CLOSED`.
4. `decision_outcome_learning_model` consumes the materialized row and returns `knowledge_gained=1`.
5. No-rollback success becomes `SUCCESS` / `HIGH` learning.
6. STOP_SAFE / no apply does not create successful production outcome evidence.
7. Failed verification records failure or rollback outcome correctly.
8. Duplicate transaction does not duplicate feedback for same operation/packet if idempotency is required by existing store rules.
9. A4 inventory no longer reports `no_verified_learning_growth_from_closed_real_outcomes` after a real materialized closed outcome.

Regression tests:

1. Existing feedback unit tests still pass.
2. Existing governed transaction tests still preserve one-user, no automation, no authority expansion.
3. Candidate coverage behavior remains unchanged.

## Existing Owner

Primary:

- `tools/v7-governed-canary-dry-run-cycle`

Secondary:

- `admin_core.operator_execution_feedback.py`
- `tools/v7-users-autoswitch`
- `tools/v7-autonomy-trust-evidence-inventory`
- `admin_core.autonomy_trust_acceleration.py`
- `admin_core.intelligence_workers.py`

## Existing Backlog

`A4_MATERIALIZE_REPRESENTATIVE_OUTCOME_EVIDENCE_FOR_FIRST_ACTION_CLASS`

No new backlog item is required.

## Need New Items

| Question | Verdict |
| --- | --- |
| Need New Owner | FALSE |
| Need New Backlog | FALSE |
| Need New Runtime | FALSE |
| Need New Architecture | FALSE |
| Need Formula Change | FALSE |
| Need Threshold Change | FALSE |

## Counterfactual

If the transaction had been materialized correctly:

- `execution-events.jsonl` would contain outcome and prediction feedback rows for `pkt_preview_a69...`.
- `runtime-trust.jsonl` would contain trust feedback for `awg3`.
- `proposal(s).jsonl` would contain recommendation feedback with selected move hash.
- `closure-records.jsonl` would contain `execution_feedback` row with `closure_state=CLOSED`.
- `decision_outcome_learning_model` would contain at least one SUCCESS row.
- `knowledge_gained` would become at least `1`.
- A4 would still not necessarily be complete because candidate coverage remains `87/156` and `missing_candidate_outcomes=69`.
- The specific blocker `no_verified_learning_growth_from_closed_real_outcomes` would be removed for this real outcome.
- `missing_candidate_outcomes` would not decrease again from feedback materialization alone, because it already decreased through switch-history candidate evidence.

## Whether Another Production Transaction Is Required

After the fix:

- Another production transaction is required to produce a new clean real materialized outcome through the corrected path.
- Existing historical transaction should not be retroactively synthesized as certification evidence unless an explicit, governed backfill policy already exists and is approved. No such backfill was performed in this audit.

## Current Progress

| Area | Current |
| --- | --- |
| Engineering Maturity | `100%` |
| Production Maturity | `24%` |
| Tier A backlog progress | `3 / 6 = 50%` |
| Overall backlog progress | `3 / 34 = 8.8%` |
| A4 candidate evidence | `87 / 156 = 55.77%` |
| A4 missing candidate outcomes | `69` |
| A4 verified learning growth | `0` for latest transaction |

## Canonical Knowledge

No canonical owner update is required.

The finding is an implementation workflow gap inside existing A4 ownership. It does not introduce new architecture, policy, owner, backlog item, or formula.

## Next Step

Continue OMP with:

`A4_FIX_GOVERNED_TRANSACTION_FEEDBACK_MATERIALIZATION_IN_EXISTING_TRANSACTION_OWNER`

Expected completion evidence:

- successful governed transaction writes feedback/closure rows;
- `decision_outcome_learning_model` sees the row;
- A4 inventory shows verified learning growth from closed real outcomes;
- runtime automation remains disabled until all A4/A5/B13/A6 gates are satisfied.

Final verdict:

`FEEDBACK_LEARNING_ROOT_CAUSE_IDENTIFIED`
