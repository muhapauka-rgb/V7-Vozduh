# PROGRAM EXEC.2_4 - Fresh Packet, Fresh Restore Barrier, One User Execution Certification

## 1. Executive Summary

EXEC.2_4 выполнен как реальный governed runtime execution для одного пользователя.

Итог: `ONE_USER_CERTIFIED`.

Реальное движение:

- пользователь: `10.7.0.5`
- было: `awg3`
- стало: `vless`
- scope: ровно 1 пользователь
- apply: выполнен через существующий `tools/v7-users-autoswitch --apply --verify`
- verification: PASS
- rollback: не потребовался
- rollback readiness: PASS через rollback packet dry-run

Новые planner/governance/execution пути не создавались.

## 2. Evidence Folder

Evidence folder:

`EXEC2_4_EVIDENCE/`

Ключевые файлы:

- `phase2_one_user_plan.json`
- `phase4_packet_generate.json`
- `phase5_restore_barrier_clearance.json`
- `phase6_post_clearance_dry_run.json`
- `phase7_one_user_apply_result.json`
- `phase8_user_route_check.txt`
- `phase9_rollback_packet_generate.json`
- `phase9_rollback_packet_dry_run.json`
- `phase10_truth_check_after_snapshot_refresh.json`
- `phase10_convergence_after_snapshot_refresh.json`

## 3. Phase 1 - Truth Gate

Перед выполнением runtime-действия был закрыт локальный truth/convergence blocker по классификации evidence/test путей.

Коммиты:

- `6fcc1dc` - `Add SNAP1 close and EXEC1 certification evidence`
- `568c7df` - `Treat uppercase evidence folders as documentation`
- `6933631` - `Classify tests as non-runtime change paths`

Production был обновлен approved safe deploy до:

`6933631b317485e3ca472d7e9adcea96f4129c93`

Truth/convergence перед runtime-действием:

- truth-check: `PASS`
- convergence-status: `PASS`
- runtime action guard: `READY_FOR_RUNTIME_ACTION`

## 4. Phase 2 - Fresh Planner

Fresh production planner был запущен без apply.

Planner выбрал одного кандидата до старого restore-barrier gate:

- `user_ip`: `10.7.0.5`
- `current_egress`: `awg3`
- `recommended_egress`: `vless`
- `move_type`: `failover`

Старый restore barrier ожидаемо блокировал selected moves:

- `terminal_reason`: `dry_run_restore_barrier_clearance_generation_expired`
- `selected_moves`: `0`
- `clearance_selected_moves_before_guard`: `1`
- `approved_candidate_moves_before_guard`: `1`

Это подтвердило исходный blocker: нужен fresh packet и fresh restore barrier clearance для текущего planner generation.

## 5. Phase 3 - One User Candidate

Выбран текущий planner-selected кандидат:

`10.7.0.5 awg3 -> vless`

Старый target не форсировался. Пользователь не заменялся вручную после packet.

## 6. Phase 4 - Fresh Packet

Fresh operator packet создан через canonical owner:

`v7-operator-execution-packet`

Packet constraints:

- `allowed_users`: `["10.7.0.5"]`
- `allowed_targets`: `["vless"]`
- `selected_move_budget`: `1`
- rollback manifest items: `1`

Packet сам по себе не разрешал apply. Он зафиксировал один план, одного пользователя, одну цель и rollback manifest.

## 7. Phase 5 - Fresh Restore Barrier

Fresh restore barrier clearance записан через canonical owner:

`admin_core/operator_execution.py`

Результат:

- `recheck_verdict`: `ALLOW_RESTORE_BARRIER_CLEARANCE`
- `clearance_verdict`: `RESTORE_BARRIER_CLEARANCE_WRITTEN`
- `execution_allowed_now`: `true`
- `real_runtime_action_performed`: `true`

Это runtime action было ограничено restore-barrier clearance. Пользователи на этом шаге не двигались.

## 8. Phase 6 - Post-Clearance Dry-Run

Post-clearance dry-run подтвердил:

- `selected_moves`: `1`
- selected user: `10.7.0.5`
- selected target: `vless`
- `approved_plan_lock_valid`: `true`
- `clearance_generation_ok`: `true`
- `terminal_reason`: `dry_run_selected_moves_available`

Apply еще не выполнялся.

## 9. Phase 7 - Real Governed Apply

Выполнен bounded governed apply:

`v7-users-autoswitch --mode guarded --apply --verify --user 10.7.0.5 --target-egress vless --max-selected-moves 1`

Результат:

- `terminal_state`: `APPLIED`
- `terminal_reason`: `selected_moves_applied`
- `selected_moves`: `1`
- `apply_result.applied`: `true`
- `results_count`: `1`
- moved user: `10.7.0.5`
- from: `awg3`
- to: `vless`
- switch rc: `0`
- verify rc: `0`
- rollback attempted: `false`

Ни один дополнительный пользователь не был перемещен.

## 10. Phase 8 - Verification

Production registry после apply:

`ip=10.7.0.5 current=vless table=1003 enabled=1`

Route verification:

- `V7_USER_ROUTE_CHECK=OK`

Post-apply planner refresh был выполнен без apply, чтобы закрыть snapshot mismatch после изменения `users.registry`.

После refresh:

- snapshot gate не остановил planner
- selected moves для того же пользователя: `0`
- оставшийся dry-run terminal reason: `dry_run_restore_barrier_clearance_generation_mismatch`

Это ожидаемо: fresh approved plan уже был использован, а следующий runtime action снова должен начинаться с fresh packet/fresh restore barrier.

## 11. Phase 9 - Rollback Readiness

Rollback packet был сгенерирован из реального apply-result.

Результат генерации:

- validation errors: `[]`
- rollback packet items: `1`

Rollback dry-run:

- `terminal_state`: `ROLLBACK_DRY_RUN`
- `terminal_reason`: `rollback_packet_valid`
- rollback applied: `false`

Rollback не выполнялся, потому что verification прошла и rollback не требовался.

## 12. Phase 10 - Final Truth / Convergence

После apply и post-apply snapshot refresh:

- truth-check: `PASS`
- blockers: `[]`
- convergence-status: `PASS`
- convergence status: `ALIGNED`
- runtime action guard: `READY_FOR_RUNTIME_ACTION`

## 13. Safety Review

Подтверждено:

- batch execution: не выполнялся
- moved users: `1`
- only approved user moved: `true`
- apply scope: one-user only
- user replacement during apply: `false`
- target replacement during apply: `false`
- planner bypass: `false`
- packet bypass: `false`
- restore barrier bypass: `false`
- governance bypass: `false`
- new planner: `false`
- new governance path: `false`
- new execution path: `false`
- authority model changed: `false`
- autonomy enabled: `false`

## 14. Final Verdicts

- truth_gate_passed: `true`
- fresh_planner_generated: `true`
- one_user_candidate_selected: `true`
- fresh_packet_created: `true`
- fresh_restore_barrier_written: `true`
- post_clearance_dry_run_passed: `true`
- approved_plan_lock_valid: `true`
- real_governed_apply_executed: `true`
- users_moved: `1`
- only_approved_user_moved: `true`
- verification_passed: `true`
- rollback_required: `false`
- rollback_packet_created: `true`
- rollback_dry_run_passed: `true`
- final_truth_passed: `true`
- final_convergence_passed: `true`
- ONE_USER_CERTIFIED: `true`

## 15. Safe Next Step

`SAFE_NEXT_STEP=EXECUTION_OUTCOME_FEEDBACK_AND_SMALL_SCOPE_STABILITY_REVIEW`

Следующий этап должен закрыть outcome/trust/prediction/recommendation feedback для реального one-user execution и затем решить, можно ли готовить следующий bounded execution scope.

