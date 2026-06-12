# PROGRAM EXEC.5_6 - Batch Execution Certification and Batch Governance Activation

## 1. Executive Summary

EXEC.5_6 выполнен как production batch execution certification.

Финальный verdict: `PARTIALLY_CERTIFIED`.

Сертифицировано:

- `TWO_USER_CERTIFIED=true`
- `FIVE_USER_CERTIFIED=true`
- `CURRENT_FULL_PLANNER_BATCH_CERTIFIED=true`

Не сертифицировано:

- `TEN_USER_CERTIFIED=false`

Причина: после Stage A и Stage B в текущем production planner pool осталось только 8 реальных кандидатов. Выполнять Stage C на 10 пользователей было бы искусственным расширением blast radius и нарушением planner/governance-first правила.

Фактически выполнено в EXEC.5_6:

- Stage A: 2 пользователя
- Stage B: 5 пользователей
- Stage D: текущий full planner batch, 8 пользователей

Всего EXEC.5_6 переместил 15 пользователей.

Все реальные движения прошли через:

fresh planner -> fresh packet -> fresh restore barrier -> dry-run -> governed apply --verify -> rollback packet -> rollback dry-run.

## 2. Runtime Truth Gate

Перед execution:

- truth-check: `PASS`
- convergence-status: `PASS`
- runtime action guard: `READY_FOR_RUNTIME_ACTION`

После execution:

- truth-check: `PASS`
- blockers: `[]`
- convergence-status: `PASS`
- convergence status: `ALIGNED`
- runtime action guard: `READY_FOR_RUNTIME_ACTION`

Evidence:

- `EXEC5_6_EVIDENCE/phase1_truth_gate.json`
- `EXEC5_6_EVIDENCE/phase1_convergence_gate.json`
- `EXEC5_6_EVIDENCE/phase9_final_truth_check.json`
- `EXEC5_6_EVIDENCE/phase9_final_convergence_status.json`

## 3. Planner Reality

Initial fresh planner reality:

- candidate moves total: `15`
- selected moves after old barrier: `0`
- approved candidate moves before guard: `15`
- target: `vless`
- blocker before fresh clearance: `restore_barrier_clearance_selected_moves_exceed_budget`

This confirmed that batch execution required a fresh packet and fresh restore barrier clearance.

After all certified stages:

- candidate moves total: `0`
- selected moves: `0`
- approved candidates before guard: `0`

The current planner pool was fully consumed by governed execution.

## 4. Batch Ladder Results

### Stage A - 2 Users

Moved:

- `10.0.0.2: awg0 -> vless`
- `10.0.0.3: awg3 -> vless`

Result:

- apply terminal state: `APPLIED`
- verification: `PASS`
- rollback packet items: `2`
- rollback dry-run: `ROLLBACK_DRY_RUN`

Verdict: `TWO_USER_CERTIFIED=true`

### Stage B - 5 Users

Moved:

- `10.0.0.6: awg0 -> vless`
- `10.7.0.3: awg3 -> vless`
- `10.7.0.2: awg3 -> vless`
- `10.7.0.4: awg0 -> vless`
- `10.7.0.6: awg3 -> vless`

Result:

- apply terminal state: `APPLIED`
- verification: `PASS`
- rollback packet items: `5`
- rollback dry-run: `ROLLBACK_DRY_RUN`

Verdict: `FIVE_USER_CERTIFIED=true`

### Stage C - 10 Users

Stage C was not executed.

Reason:

- requested budget: `10`
- available candidates after Stage A+B: `8`
- decision: `DO_NOT_EXECUTE_STAGE_C`

Verdict: `TEN_USER_CERTIFIED=false`

Single blocker:

`insufficient_current_planner_candidates_without_synthetic_user_movement`

### Stage D - Current Full Planner Batch

Current full planner batch after Stage A+B was 8 users.

Moved:

- `10.7.0.8: awg0 -> vless`
- `10.7.0.9: awg3 -> vless`
- `10.7.0.10: awg0 -> vless`
- `10.7.0.11: awg3 -> vless`
- `10.7.0.12: awg0 -> vless`
- `10.7.0.13: awg0 -> vless`
- `10.7.0.14: awg3 -> vless`
- `10.7.0.15: awg0 -> vless`

Result:

- apply terminal state: `APPLIED`
- verification: `PASS`
- rollback packet items: `8`
- rollback dry-run: `ROLLBACK_DRY_RUN`

Verdict: `CURRENT_FULL_PLANNER_BATCH_CERTIFIED=true`

## 5. Verification Results

For every executed stage:

- selected move count matched approved packet budget
- approved plan lock was valid
- restore barrier generation was valid
- apply moved exactly approved users
- all switch return codes were `0`
- all verification return codes were `0`
- standalone route-check returned `V7_USER_ROUTE_CHECK=OK`
- rollback was not attempted during forward apply

No extra users were moved.

## 6. Rollback Certification

Rollback packet generation passed for all executed stages:

- Stage A rollback items: `2`
- Stage B rollback items: `5`
- Stage D rollback items: `8`

Rollback dry-run passed for all executed stages:

- Stage A: `ROLLBACK_DRY_RUN`
- Stage B: `ROLLBACK_DRY_RUN`
- Stage D: `ROLLBACK_DRY_RUN`

Important operational finding:

Rollback readiness checks must run with explicit state path:

`--state-dir /opt/v7/egress/state`

Without explicit state-dir, rollback dry-run intermittently returned:

`rollback_user_not_on_forward_target`

Production registry and route-check showed users were correctly on `vless`; explicit state-dir resolved the validation path. Batch governance must require explicit state-dir for rollback readiness.

## 7. Blast Radius Review

Certified blast radius:

- 1 user: certified by EXEC.2_4
- 2 users: certified by EXEC.5_6 Stage A
- 5 users: certified by EXEC.5_6 Stage B
- current full planner batch: certified at 8 users by EXEC.5_6 Stage D

Not certified:

- 10 users

Reason:

There were not 10 real remaining planner candidates at Stage C. The system correctly did not fabricate movements.

Maximum certified batch in this run:

`8`

Maximum total governed batch movement in EXEC.5_6:

`15`

## 8. Batch Formula Audit

Existing batch logic is already present and should be reused.

Classifications:

- planner batch selection: `REUSE`
- `--max-selected-moves`: `REUSE`
- authority budget logic: `REUSE`
- approved plan lock: `REUSE`
- restore barrier generation clearance: `REUSE`
- rollback packet generation: `REUSE`
- rollback dry-run validation: `EXTEND`, because explicit `--state-dir /opt/v7/egress/state` must be mandatory in operational runbooks
- synthetic candidate generation: `DO_NOT_TOUCH`
- planner bypass path: `DO_NOT_TOUCH`
- governance bypass path: `DO_NOT_TOUCH`

No new planner was created.

No new governance owner was created.

No new execution path was created.

## 9. Governance Activation

Batch governance can be activated as a normal governed operation model for certified scopes only.

Activation scope:

- governed 2-user batch: allowed
- governed 5-user batch: allowed
- governed current planner batch up to 8 users: allowed when current planner provides real candidates

Not activated:

- 10-user guarantee
- autonomy
- automatic execution
- planner bypass
- restore barrier bypass

Required operational constraints:

- fresh planner required
- fresh packet required
- fresh restore barrier required
- post-clearance dry-run required
- apply must use governed path
- verification required
- rollback packet required
- rollback dry-run must use explicit `--state-dir /opt/v7/egress/state`
- no synthetic users
- no replacement of approved users during apply
- no replacement of targets during apply

## 10. Final Certification

Final certification values:

- TWO_USER_CERTIFIED: `true`
- FIVE_USER_CERTIFIED: `true`
- TEN_USER_CERTIFIED: `false`
- FULL_BATCH_CERTIFIED: `true`
- FULL_BATCH_CERTIFIED_SIZE: `8`
- total_users_moved_exec56: `15`
- verification_passed_all_executed_stages: `true`
- rollback_readiness_passed_all_executed_stages: `true`
- final_truth_passed: `true`
- final_convergence_passed: `true`

## 11. Final Verdict

`PARTIALLY_CERTIFIED`

Single blocker:

`insufficient_current_planner_candidates_for_10_user_stage`

Safe next step:

`EXECUTION_OUTCOME_FEEDBACK_MATERIALIZATION_AND_BATCH_GOVERNANCE_RUNBOOK`

The next step should materialize outcome/trust/prediction/recommendation feedback for EXEC.2_4 and EXEC.5_6, then record the batch governance runbook with the explicit rollback state-dir requirement.

