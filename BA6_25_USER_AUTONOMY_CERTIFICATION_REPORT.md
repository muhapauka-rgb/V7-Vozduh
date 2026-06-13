# BA6 25 USER AUTONOMY CERTIFICATION REPORT

Дата: 2026-06-13

Проект: V7 Vozduh

Ветка: Updatesystem

Режим: controlled certification attempt.

Итог: `TWENTY_FIVE_USER_AUTONOMY_BLOCKED`

Пользователи не двигались. `apply` не запускался. Packet/restore barrier для 25 пользователей не создавались, потому что fresh planner не дал 25 реальных кандидатов.

## 1. Truth Gate

Truth gate пройден.

- truth-check: `PASS`
- convergence: `FULLY_ALIGNED`
- runtime_action_safe: `true`
- runtime_access_status: `READY`

Важная деталь: local/GitHub содержат docs-only BA4/BA5 отчёты, production runtime code не требует deploy. Truth gate классифицировал это как docs-only mismatch и не заблокировал runtime action.

Evidence:

- `BA6_EVIDENCE/phase1/truth_gate_summary.json`
- `BA6_EVIDENCE/final/final_truth_convergence_summary.json`

## 2. Policy Escalation

Через canonical owner `/api/actions/policy-update` был поднят:

`autoswitch_max_planned_per_run: 10 -> 25`

Authority budget при этом уже был:

- authority_class: `POOL`
- current_allowed_user_budget: `25`

Пользователи не двигались. Routing не менялся.

Evidence:

- `BA6_EVIDENCE/phase2/policy_before.json`
- `BA6_EVIDENCE/phase2/policy_update_patch.json`
- `BA6_EVIDENCE/phase2/policy_after.json`
- `BA6_EVIDENCE/phase2/policy_update_summary.json`

## 3. Canonical Refresh

Был выполнен production snapshot refresh.

Затем был выполнен fresh planner dry-run с:

- pre-planner refresh: `write`
- `--max-selected-moves 25`
- no `--apply`

Старый BA4 restore barrier был expired и мешал обычному dry-run показать свежую реальность. Поэтому для чистого discovery был использован отдельный пустой `--restore-barrier-file /tmp/ba6-empty-restore-barrier.json`.

Это не bypass execution, потому что:

- `apply=false`;
- restore barrier не создавался;
- packet не создавался;
- runtime mutation не было;
- цель была только увидеть fresh planner reality.

Evidence:

- `BA6_EVIDENCE/phase3/snapshot_refresh.json`
- `BA6_EVIDENCE/phase4/fresh_planner_no_stale_barrier.json`
- `BA6_EVIDENCE/phase4/fresh_planner_no_stale_barrier_summary.json`

## 4. Fresh Planner

Fresh planner result:

- users_total: `26`
- egress_total: `7`
- healthy_egress_total: `3`
- planned_limit: `25`
- requested_max_selected_moves: `25`
- authority_class: `POOL`
- current_allowed_user_budget: `25`
- candidate_moves_total: `0`
- selected_moves: `0`
- apply_requested: `false`

Direct root cause:

`candidate_moves_total=0`

All 26 planner-visible users were classified as:

- action: `keep`
- move_type: `none`

Current/recommended distribution:

- `awg3`: 8 users
- `wireguard-1779454504-c43409`: 8 users
- `vless`: 10 users

Planner reasons:

- `sticky_keep_current`: 18
- `current_is_best`: 8

Meaning: after BA3/BA4 execution and feedback, the planner no longer sees 25 users that should be moved. The system is already in a stable enough distribution for current evidence.

Evidence:

- `BA6_EVIDENCE/phase4/no_candidate_root_cause_summary.json`

## 5. Stop Decision

BA6 rule says:

If candidate count `<25`, stop and explain.

This condition was hit:

- required candidates: `25`
- actual candidates: `0`

Therefore BA6 stopped before:

- packet generation;
- restore barrier generation;
- post-clearance dry-run;
- autonomous execution;
- feedback materialization.

This is the correct safety outcome.

## 6. Policy Cleanup

Because 25-user execution was not certified, the temporary planned limit was reverted:

`autoswitch_max_planned_per_run: 25 -> 10`

Reason:

Keep runtime aligned with the last proven execution ceiling: 10 users.

Authority budget remains:

- authority_class: `POOL`
- current_allowed_user_budget: `25`

Meaning:

The authority model still allows 25, but execution policy remains at the last certified runtime ceiling until a real 25-candidate situation exists.

Evidence:

- `BA6_EVIDENCE/phase4/policy_revert_to_10_patch.json`
- `BA6_EVIDENCE/phase4/policy_after_revert.json`
- `BA6_EVIDENCE/phase4/policy_revert_summary.json`

## 7. Blast Radius Review

Blast radius remained zero.

- unexpected users moved: `false`
- target replacement: `false`
- planner bypass: `false`
- governance bypass: `false`
- restore barrier bypass: `false`
- atomic envelope bypass: `false`
- rollback failure: `false`

Why:

No packet was created and no apply was executed.

## 8. Authority Budget Validation

Question: Was authority_budget=25 validated in real execution?

Answer: `false`

Reason:

The authority budget exists and was accepted by the planner policy chain, but there were not 25 real planner-selected candidates. A budget can only be validated by executing a real eligible batch.

Did any hidden ceiling appear?

Answer: `no`

Reason:

The system accepted planned_limit=25 and authority_budget=25. The blocker was not a hidden ceiling. The blocker was zero candidate demand.

Did runtime remain stable?

Answer: `yes`

Reason:

Final truth/convergence remained PASS/FULLY_ALIGNED after policy cleanup.

## 9. Final Certification

Final verdict:

`TWENTY_FIVE_USER_AUTONOMY_BLOCKED`

Single blocker:

`candidate_moves_total=0`

Final flags:

- truth_gate_pass=true
- convergence_pass=true
- runtime_action_safe=true
- policy_escalated_to_25=true
- authority_budget_valid_in_policy=true
- candidate_moves_total=0
- selected_moves=0
- packet_created=false
- restore_barrier_created=false
- apply_executed=false
- users_moved=0
- feedback_materialized=false
- policy_reverted_to_last_certified_ceiling=true
- final_planned_limit=10
- twenty_five_user_autonomy_certified=false

SAFE_NEXT_STEP:

`WAIT_FOR_REAL_25_CANDIDATE_POOL_OR_RUN_POOL_STABILITY_OBSERVATION`

Plain meaning:

V7 did not fail technically. It refused to manufacture work. Right now there are no 25 users that the planner honestly wants to move.

