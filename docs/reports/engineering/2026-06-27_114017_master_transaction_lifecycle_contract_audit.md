# Master Transaction Lifecycle Contract Audit

Status: COMPLETE
Date: 2026-06-27
Language: Russian

## Summary

Аудит определил, когда production transaction официально считается COMPLETE в V7.

Короткий вывод:

- Runtime-level завершение наступает при terminalized lease: `EXECUTION_FINISHED`, `ROLLBACK_FINISHED` или `STOP_SAFE`.
- Product/OMP-level завершение наступает позже: outcome должен быть закрыт, feedback материализован, learning/evidence должны его потребить, promotion readiness должен быть пересчитан, Current Program State должен отразить результат.
- Эти определения не были идентичны для последней реальной A4 transaction.
- Первый разрыв старого жизненного цикла: после `finish_execution_lease(... EXECUTION_FINISHED ...)` и до feedback/learning materialization.
- Дефект классифицируется как `Lifecycle Contract Defect`: transaction owner завершил execution lifecycle, но контракт обязательной downstream-пропагации не был enforced как часть полного production completion.

## Action Performed

Выполнен forensic-аудит без изменения Runtime, OMP, кода, authority, backlog или architecture.

Прочитаны и сопоставлены:

- Product Specification / Business Objectives;
- Runtime Model;
- Decision Model;
- OMP;
- Current Program State;
- Canonical Reference;
- SYSTEM_MAP;
- Decision Commit / Governed Transaction / A4 reports;
- Feedback / Learning / Evidence Inventory owners;
- production transaction reports and current implementation owner path.

## Latest Real Governed Transaction

Последняя реальная successful governed transaction:

| Field | Value |
| --- | --- |
| packet | `pkt_preview_a69fe12e51c528c2a0402c0c` |
| decision | `decision_commit_1ecf28e69a44b11699ebef0d` |
| operation | `govdry_2fb035b74bb3a5af0ecf7c13` |
| lease | `execlease_5f4d34d80de62bf6445d73b4` |
| user | `10.7.0.5` |
| movement | `awg0 -> awg3` |
| apply | `YES` |
| verification | `PASS` |
| rollback | `NOT_REQUIRED` |
| lease terminal state | `EXECUTION_FINISHED` |

## Complete Production Transaction Lifecycle

Official lifecycle:

```text
Reality
-> Decision
-> Governed Transaction
-> Apply
-> Verification
-> Rollback / No-Rollback
-> Outcome
-> Feedback
-> Learning
-> Trust
-> Evidence
-> Promotion
-> Current Program State
-> OMP
```

## Completion Definition By Owner

| Owner | Transaction complete means | Latest historical transaction status |
| --- | --- | --- |
| Runtime / execution lease | Lease terminalized as `EXECUTION_FINISHED`, `ROLLBACK_FINISHED`, or safe stop. | COMPLETE |
| Autoswitch apply | Apply attempted once, result emitted, verification/rollback verdict available. | COMPLETE |
| Verification | User/service check passed or failed with terminal verdict. | COMPLETE |
| Rollback | Rollback not required or rollback completed/failed with terminal record. | COMPLETE (`NOT_REQUIRED`) |
| Feedback owner | Closed feedback/closure records exist for the observed outcome. | INCOMPLETE historically |
| Learning owner | Closed real outcome is consumed and produces learning/trust/evidence rows. | INCOMPLETE historically |
| Evidence Inventory | Outcome appears in representative evidence and learning/evidence readiness. | PARTIAL historically |
| Promotion Engine / OMP | A4 readiness recalculated from consumed evidence. | PARTIAL / BLOCKED |
| Current Program State | Terminal state, learning status, next action, and OMP stop/continue state recorded. | PARTIAL |

Therefore the definitions were not identical.

## Stage Contracts

| Stage | Entry contract | Exit contract | Persistence | Consumers |
| --- | --- | --- | --- | --- |
| Reality | Real production state exists. | Real event/candidate can be observed. | Event/snapshot stores. | Decision/Planner. |
| Decision | Candidate and policy evidence available. | Decision identity and selected move are fixed. | Decision/packet preview. | Governed transaction. |
| Governed Transaction | One bounded authority envelope exists. | Either STOP_SAFE or one execution attempt completed. | Transaction output, audit. | Apply/lease/feedback. |
| Apply | Restore barrier and live gates pass. | Mutation applied or explicit fail-closed. | switch/audit/apply result. | Verification, lease. |
| Verification | Apply result exists. | PASS/FAIL/INCONCLUSIVE. | apply payload/audit. | Rollback/outcome. |
| Rollback | Verification failed after mutation or rollback not required. | rollback completed, failed, or `NOT_REQUIRED`. | operation verdict. | Outcome closure. |
| Outcome | Execution + verification + rollback facts exist. | Exact observed outcome closed. | feedback/closure records. | Learning. |
| Feedback | Outcome closure contract exists. | outcome/trust/prediction/recommendation/closure records materialized. | existing JSONL stores. | Learning/evidence inventory. |
| Learning | Closed real feedback exists. | knowledge/trust/evidence read models update. | learning/evidence read models. | Promotion/OMP. |
| Trust | Learning deltas exist. | trust/readiness signal updated. | runtime trust store/read model. | Evidence/promotion. |
| Evidence | Real outcome and learning signals exist. | A4 evidence inventory recalculated. | evidence inventory output. | Promotion engine. |
| Promotion | Evidence inventory available. | action-class state stays/goes forward with reasons. | OMP/CPS. | Current Program State. |
| Current Program State | Lifecycle/promotion result known. | next safe action and stop/continue state recorded. | `V7_CURRENT_PROGRAM_STATE.md`. | OMP/operator. |

## Responsibility Graph

| Node | Owner | Caller | Verifier | Consumer | Auditor |
| --- | --- | --- | --- | --- | --- |
| Reality | Event/knowledge owners | OMP/dry-run | truth/convergence where relevant | Decision surface | reports |
| Decision | Decision Model / operator decision surface | governed dry-run | packet identity checks | transaction owner | decision reports |
| Transaction | `tools/v7-governed-canary-dry-run-cycle` | operator/OMP | transaction constraints | apply/lease/feedback | engineering reports |
| Apply | `tools/v7-users-autoswitch` / autoswitch owner | transaction owner | apply result + verification | lease/outcome | audit stores |
| Verification | autoswitch/runtime readiness | apply owner | verify return code/result | rollback/outcome | audit stores |
| Rollback | restore barrier / rollback owner | apply/transaction owner | rollback verdict | outcome | audit stores |
| Outcome | feedback owner | transaction owner | closure record completeness | learning | closure records |
| Feedback | `admin_core/operator_execution_feedback.py` | transaction owner | materialized record set | learning/trust/evidence | JSONL stores |
| Learning | feedback/learning owners | evidence inventory | real-only learning checks | promotion | inventory reports |
| Trust | feedback/trust owner | feedback materialization | trust record presence | evidence inventory | trust store |
| Evidence | `autonomy_trust_acceleration` / inventory tool | OMP | inventory consistency | promotion | A4 reports |
| Promotion | OMP / action-class promotion | OMP continuation | policy/authority gates | CPS | OMP reports |
| Current Program State | CPS owner | OMP | truth/convergence | OMP/operator | engineering reports |

## Contract Graph

```text
Apply PASS
  requires Verification PASS/FAIL
  requires Rollback verdict
  produces operation terminal facts

Operation terminal facts
  require lease terminalization
  require outcome closure

Outcome closure
  requires feedback materialization
  requires closure record

Feedback materialization
  requires learning/trust/evidence consumption

Learning/trust/evidence consumption
  requires promotion recalculation

Promotion recalculation
  requires Current Program State update

Current Program State update
  lets OMP decide next action
```

## First Lifecycle Break

First owner where lifecycle broke historically:

```text
tools/v7-governed-canary-dry-run-cycle
```

Break point:

```text
finish_execution_lease(EXECUTION_FINISHED)
-> transaction returned completed execution facts
-> feedback/closure/learning records were not materialized
```

Why propagation stopped:

- lease terminalization was treated as sufficient transaction completion for the governed transaction output;
- feedback materialization was not mandatory in the transaction completion barrier;
- evidence inventory later saw candidate coverage but not verified learning growth.

Why this was not automatically detected:

- observability existed per subsystem: switch history, audit, lease, restore barrier, inventory;
- no single lifecycle completeness sentinel compared all required terminal artifacts:
  - lease terminalized;
  - feedback materialized;
  - closure record written;
  - learning row consumed;
  - evidence inventory updated;
  - promotion/CPS recalculated.

This should have been impossible once the governed transaction was considered product-complete.

## Counterfactual

If the latest transaction had propagated correctly at the time:

- closure record would exist for `pkt_preview_a69fe12e51c528c2a0402c0c`;
- decision learning rows would include the real successful outcome;
- trust/recommendation/prediction records would exist;
- evidence inventory would no longer report missing verified learning growth for that transaction;
- Current Program State would show the transaction as learning-materialized;
- A4 would still not necessarily complete because `missing_candidate_outcomes = 69` remains a real evidence limit.

## Failure Tree

```text
Observed symptom
-> A4 still reports missing verified learning growth after successful governed transaction

Immediate cause
-> transaction terminalized lease but did not materialize feedback/closure records

Owner
-> governed transaction owner calling existing feedback owner

Missing contract
-> production transaction completion barrier did not require feedback -> learning -> evidence -> promotion propagation

Root cause
-> lifecycle completion definitions were split across owners and not enforced as one official production completion contract
```

## Classification

Exact classification:

```text
Lifecycle Contract Defect
```

Reason:

- Runtime apply, verification, and lease terminalization succeeded.
- Feedback/Learning owners already existed.
- Backlog owner A4 already covered the work.
- The missing part was the enforced lifecycle contract between terminal execution and downstream product completion.

The later code fix materialized the implementation side of this contract for future transactions, but this audit classifies the historical root cause at the lifecycle-contract level.

## Minimal Correction

No new owner, backlog, runtime path, lifecycle owner, or architecture is required.

Minimal correction through existing owners:

1. Governed transaction owner must treat a production transaction as product-complete only after feedback materialization has run or an explicit `STOP_SAFE`/`PENDING_BACKGROUND_PROPAGATION` state is recorded.
2. Feedback owner must persist the existing outcome/trust/prediction/recommendation/closure records only from real apply + verification facts.
3. Evidence inventory must consume those records and expose whether learning/evidence propagation succeeded.
4. Current Program State must record the final lifecycle status:
   - Runtime complete;
   - Feedback materialized;
   - Learning consumed;
   - Promotion recalculated;
   - A4 complete or still blocked.

The currently deployed fix already implements the key forward path: successful future governed transactions call `materialize_governed_transaction_feedback`.

Remaining validation:

- wait for the next real eligible A4 transaction;
- execute only with bounded authority;
- verify that feedback records are written;
- verify that A4 inventory consumes them;
- update CPS/OMP from the real result.

## Existing Owner Mapping

| Contract area | Existing owner |
| --- | --- |
| Transaction lifecycle invocation | `tools/v7-governed-canary-dry-run-cycle` |
| Apply and terminal operation facts | `tools/v7-users-autoswitch` / autoswitch owner |
| Lease terminalization | `admin_core/operator_execution.py` |
| Feedback/closure materialization | `admin_core/operator_execution_feedback.py` |
| Learning/evidence inventory | `admin_core/autonomy_trust_acceleration.py`, evidence inventory tool |
| Promotion decision | OMP / action-class promotion |
| State publication | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` |
| Canonical lifecycle model | `docs/reference/V7_RUNTIME_MODEL.md` |

## Existing Backlog

Existing backlog owner:

```text
A4_MATERIALIZE_REPRESENTATIVE_OUTCOME_EVIDENCE_FOR_FIRST_ACTION_CLASS
```

Secondary consumers later:

- `B13` metric/evidence reliability;
- `A6` runtime eligibility arbitration;
- authority promotion items after evidence is certified.

## Need New Checks

| Question | Verdict |
| --- | --- |
| Need New Owner | FALSE |
| Need New Backlog | FALSE |
| Need New Runtime | FALSE |
| Need New Architecture | FALSE |
| Need New Lifecycle | FALSE |
| Only lifecycle materialization | TRUE |

## Progress

| Area | Current |
| --- | --- |
| A4 candidate coverage | `87 / 156 = 55.77%` |
| Missing candidate outcomes | `69` |
| Learning capability | `40.0%` |
| Authority Evolution | `40.0%` |
| Production Readiness | `24.0%` |
| Production Autonomy | `0.0%` |
| Production Maturity | `24.0%` |

## Canonical Knowledge

No canonical owner update was required during this audit.

Reason:

- Runtime Model already defines the intended lifecycle:
  `Outcome -> Learning -> Update Current Program State -> Notify OMP -> Sleep`.
- Current Program State already records that the old transaction missed feedback materialization and that the deployed fix is waiting for a new real candidate.
- The durable knowledge is preserved here as historical execution evidence.

## Evidence

- `docs/reference/V7_RUNTIME_MODEL.md`
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
- `docs/reports/engineering/2026-06-27_103721_master_evidence_gap_forensics.md`
- `docs/reports/engineering/2026-06-27_113109_a4_feedback_materialization_fix.md`
- `docs/reports/engineering/2026-06-27_113534_a4_feedback_fix_deploy_and_omp_continuation.md`
- `tools/v7-governed-canary-dry-run-cycle`
- `admin_core/operator_execution.py`
- `admin_core/operator_execution_feedback.py`

## Next Step

Continue OMP from A4.

Do not repeat the old transaction.
Wait for a real eligible A4 governed candidate.
If a READY governed transaction appears, stop for bounded operational authority or execute only if the prompt explicitly grants one governed transaction.

FINAL VERDICT:

```text
TRANSACTION_LIFECYCLE_ROOT_CAUSE_IDENTIFIED
```
