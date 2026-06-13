# BA3.CANDIDATE_FORENSICS - Full User-By-User Planner Candidate Root Cause Audit

Дата: 2026-06-13  
Workspace: `/Users/ponch/Documents/New project`  
Branch: `Updatesystem`  
Mode: READ ONLY, no apply, no user movement, no routing/policy/restore-barrier/deploy changes.

## 1. Executive Summary

Финальный вывод: `CANDIDATE_COUNT_CORRECT`.

BA.3 увидел только 3 кандидата не из-за бага лимита, не из-за policy suppression и не из-за authority budget. Planner увидел 3 кандидата потому, что на момент STABILITY1.CLOSE только 3 пользователя реально находились на каналах, которые planner считал неeligible: `10.0.0.2` на `awg3`, `10.0.0.3` на `awg0`, `10.0.0.6` на `awg0`.

Остальные 23 пользователя уже были на `vless`, а `vless` был единственным eligible + best available pool каналом для всех 26 пользователей.

Главная причина падения пула кандидатов:

- в прежнем BA.3: `healthy_egress_total=3`, `candidate_moves_total=23`, тип кандидатов `rebalance`;
- в STABILITY1.CLOSE: `healthy_egress_total=1`, `candidate_moves_total=3`, тип кандидатов `failover`;
- `awg0` и `awg3` перестали быть eligible из-за `stability_below_floor`;
- `vless` остался единственным целевым каналом.

BA.3 сейчас не надо форсировать. Нужно ждать/восстановить healthy pool так, чтобы снова появилось минимум 5 реальных planner-selected candidates, затем rerun BA.3.

## 2. Planner State Comparison

Evidence:

- `BA3_CANDIDATE_FORENSICS_EVIDENCE/planner_state_comparison.json`
- `BA3_CANDIDATE_FORENSICS_EVIDENCE/planner_state_comparison.csv`

| Stage | Healthy egress | Candidate moves | Type | Planned limit | Authority budget | Meaning |
|---|---:|---:|---|---:|---:|---|
| `ATOMIC1_CLOSE` / BA2 prep | 3 | 25 | rebalance | 2 | 25 | healthy pool был широким, planner хотел распределять пользователей |
| Original `BA3` | 3 | 23 | rebalance | 5 | 25 | BA3 имел достаточно кандидатов, но apply был заблокирован source drift |
| `STABILITY1_CLOSE` / BA3 rerun | 1 | 3 | failover | 5 | 25 | healthy pool сузился до `vless`, кандидаты только те, кто сидит на неeligible `awg0/awg3` |

`STABILITY1_CLOSE_EVIDENCE/phase6_fresh_planner.json`:

- `users_total=26`
- `egress_total=7`
- `healthy_egress_total=1`
- `candidate_moves_total=3`
- `rebalance_candidates=0`
- `policy_planned_limit=5`
- `authority_allowed_user_budget=25`
- `effective_blast_radius=3`
- `scope=bounded_by_affected_candidates`

## 3. Full User Candidate Table

Evidence:

- `BA3_CANDIDATE_FORENSICS_EVIDENCE/full_user_candidate_table.json`
- `BA3_CANDIDATE_FORENSICS_EVIDENCE/full_user_candidate_table.csv`

Candidate users:

| User | Current | Recommended | Type | Exact reason |
|---|---|---|---|---|
| `10.0.0.2` | `awg3` | `vless` | failover | `current_egress_not_eligible`, current blocked by `stability_below_floor` |
| `10.0.0.3` | `awg0` | `vless` | failover | `current_egress_not_eligible`, current blocked by `stability_below_floor` |
| `10.0.0.6` | `awg0` | `vless` | failover | `current_egress_not_eligible`, current blocked by `stability_below_floor` |

All other 23 users:

- current egress: `vless`
- recommended egress: `vless`
- action: `keep`
- exact reason: `current_is_best; only eligible best_available_pool is current route`

## 4. Per-Target Eligibility Table

Evidence:

- `BA3_CANDIDATE_FORENSICS_EVIDENCE/per_target_eligibility_table.json`
- `BA3_CANDIDATE_FORENSICS_EVIDENCE/per_target_eligibility_table.csv`

Result: 182 rows (`26 users * 7 egress targets`).

Summary:

| Target | Eligible users | Best pool users | Candidate attraction | Main blocker |
|---|---:|---:|---:|---|
| `vless` | 26 | 26 | 3 | none |
| `awg0` | 0 | 0 | 0 | `stability_below_floor` |
| `awg3` | 0 | 0 | 0 | `stability_below_floor` |
| `wireguard-1779454504-c43409` | 0 | 0 | 0 | `canary_reserved_production_assignment_blocked` |
| `amneziawg-exec-20260528-10-8-1-14` | 0 | 0 | 0 | `manual_only`, `reserve_only`, `canary_reserved_production_assignment_blocked`, `stability_below_floor` |
| `1` | 0 | 0 | 0 | `health_code_000`, `severity_FAIL`, speed floors, Telegram down |
| `openvpn-1779388847-d2ad7c` | 0 | 0 | 0 | `health_code_000`, `severity_FAIL`, speed floors, Telegram down |

## 5. Why Only 3 Moves

Прямой ответ: потому что ровно 3 пользователя находятся не на `vless`, а все остальные уже находятся на единственном eligible/best channel.

Planner не делает движение ради “добрать до 5”. Он создает кандидата только если есть смысловая причина:

- current channel неeligible;
- другой target лучше текущего;
- нужен rebalance;
- reconnect rotation;
- failover.

В STABILITY1.CLOSE:

- rebalance исчез, потому что `awg0` и `awg3` неeligible;
- planned move отсутствует, потому что `vless` уже лучший доступный канал;
- failover есть только у трех пользователей, которые остались на `awg0/awg3`.

Итог: `candidate_moves_total=3` корректен.

## 6. Planned Limit Audit

Evidence:

- `BA3_CANDIDATE_FORENSICS_EVIDENCE/planned_limit_counterfactual.json`
- code owner: `tools/v7-users-autoswitch`

Relevant code:

- candidate creation: `tools/v7-users-autoswitch:5031`
- selected move selection: `tools/v7-users-autoswitch:5850`
- dynamic blast radius calculation: `tools/v7-users-autoswitch:3904`
- summary candidate count: `tools/v7-users-autoswitch:4073`

`autoswitch_max_planned_per_run` is consumed in `_select_moves()` for the `planned` bucket. It does not create or suppress candidate decisions. `candidate_moves_total` is computed from decisions where `recommended_egress != current_egress`.

For STABILITY1.CLOSE:

- `planned_limit=5`
- `failover_limit=25`
- `requested_max_selected_moves=5`
- `authority_allowed_user_budget=25`
- `affected_candidate_moves=3`
- `effective_blast_radius=3`
- `scope=bounded_by_affected_candidates`

The planned limit did not reduce 5 to 3. There were only 3 affected candidates.

## 7. Authority And Policy Audit

Authority was not the blocker:

- authority class: `POOL`
- current allowed budget: `25`
- requested max selected moves: `5`
- effective blast radius: `3`
- scope: `bounded_by_affected_candidates`

Policy was not the blocker:

- `autoswitch_max_planned_per_run=5`
- `autoswitch_max_failover_per_run=25`
- the three current candidates are `failover`, not `planned`;
- no evidence of silent suppression by planned limit.

Restore barrier was not the candidate-count cause:

- 3 moves existed before restore barrier guard in `safety.restore_barrier.approved_candidate_moves_before_guard`;
- final `selected_moves=[]` happened because there was no fresh packet/barrier for those 3 moves;
- this explains why execution did not proceed, not why candidate count was only 3.

## 8. Post-BA1/BA2 Effect Audit

Evidence:

- `BA3_CANDIDATE_FORENSICS_EVIDENCE/post_ba1_ba2_effect_audit.json`
- `BA1_FINAL_AUTONOMY_CERTIFICATION_REPORT.md`
- `ATOMIC1_CLOSE_AND_BA2_RECERTIFICATION_REPORT.md`

Previous real movements:

| Program | User | Before | After |
|---|---|---|---|
| BA1 | `10.0.0.2` | `vless` | `awg3` |
| BA2 | `10.0.0.3` | `vless` | `awg0` |
| BA2 | `10.0.0.6` | `vless` | `awg0` |

Current STABILITY1.CLOSE planner status:

| User | Current | Candidate? | Reason |
|---|---|---|---|
| `10.0.0.2` | `awg3` | true | current channel blocked by `stability_below_floor`, failover to `vless` |
| `10.0.0.3` | `awg0` | true | current channel blocked by `stability_below_floor`, failover to `vless` |
| `10.0.0.6` | `awg0` | true | current channel blocked by `stability_below_floor`, failover to `vless` |

Conclusion: BA1/BA2 correctly changed the real pool. They did not “break” candidate counting. They made three users visible as failover candidates once `awg0/awg3` dropped below stability floor.

## 9. Egress Quality Audit

Evidence:

- `BA3_CANDIDATE_FORENSICS_EVIDENCE/egress_quality_audit.json`
- `BA3_CANDIDATE_FORENSICS_EVIDENCE/egress_quality_audit.csv`

Key values from STABILITY1.CLOSE:

| Egress | 1h stability | Service score | Eligibility |
|---|---:|---:|---|
| `vless` | `0.4814` | `100.0` | eligible for all 26 |
| `awg0` | `0.2162` | `100.0` | blocked for all 26 by `stability_below_floor` |
| `awg3` | `0.1836` | `99.767` | blocked for all 26 by `stability_below_floor` |
| `wireguard-1779454504-c43409` | `0.8216` | `100.0` | canary reserved |

This means the service scores alone are not enough. `awg0/awg3` have good service suitability but fail the stability floor.

## 10. Bug Hunt

Evidence:

- `BA3_CANDIDATE_FORENSICS_EVIDENCE/bug_hunt_summary.json`

Inspected code path:

- `_decision_for_user()` creates per-user decision and candidate list;
- `_mark_best_available_pool()` marks eligible channels inside top/gap/service constraints;
- `_select_moves()` selects from existing decisions using failover/reconnect/rebalance/planned limits;
- plan summary recomputes `candidate_moves_total` from decisions, not from selected moves.

No candidate-count bug proven.

Reasons:

- STABILITY1.CLOSE `candidate_moves_total=3`;
- recomputation from decisions also equals 3;
- the only three `recommended_egress != current_egress` rows are the three BA1/BA2 moved users;
- per-target table proves `awg0/awg3` are not eligible due stability floor;
- 23 non-candidate users all have `current_is_best`.

## 11. Counterfactual Check

Direct live policy simulation was not performed because this program is READ ONLY and must not update runtime policy. Non-interactive SSH planner collection also failed with `Permission denied (publickey,password)`.

Evidence:

- `BA3_CANDIDATE_FORENSICS_EVIDENCE/production_readonly_planner.json`
- `BA3_CANDIDATE_FORENSICS_EVIDENCE/planned_limit_counterfactual.json`

Static counterfactual from saved STABILITY1.CLOSE decisions:

| Planned limit | Candidate moves total |
|---:|---:|
| 5 | 3 |
| 10 | 3 |
| 25 | 3 |

Reason: all 3 candidates are `failover`, and candidate count is decided before selected-move caps. `planned_limit` cannot manufacture extra candidates.

## 12. Final Root Cause

Final classification: `CANDIDATE_COUNT_CORRECT`.

Detailed root cause:

1. Original BA.3 had enough candidates because healthy pool had 3 channels and planner generated rebalance candidates from overloaded/centralized `vless` toward `awg0/awg3`.
2. After later production state changed, `awg0` and `awg3` fell below stability floor.
3. With `awg0/awg3` below floor, planner no longer treats them as valid rebalance targets.
4. `vless` became the only eligible best available pool member.
5. 23 users already on `vless` became `current_is_best`.
6. The only remaining candidate moves were the three users already moved by BA1/BA2 onto `awg0/awg3`, because their current egress became not eligible.

Not a bug:

- candidate count matches decision recomputation;
- no planned-limit suppression;
- no authority-budget suppression;
- no hidden governance suppression;
- no selected-move count bug found.

## 13. Recommended Next Step

`SAFE_NEXT_STEP=CHANNEL_POOL_RECOVERY_OR_WAIT_FOR_HEALTHY_POOL_THEN_RERUN_BA3`

Do not force BA.3 while only 3 real candidates exist.

Correct next action:

1. Observe/recover channel health for `awg0` and/or `awg3`, specifically stability above floor.
2. Rerun read-only planner with fresh snapshots.
3. Proceed with BA.3 only when `candidate_moves_total >= 5` and at least 5 candidates are real planner decisions.

Optional focused next program:

`PROGRAM_CHANNEL_STABILITY_RECOVERY_AND_BA3_CANDIDATE_POOL_REOPEN`

Goal: prove whether `awg0/awg3` stability can recover safely, without lowering floors blindly and without forcing eligibility.

## Final Verdicts

| Verdict | Value |
|---|---|
| candidate_count_root_cause_known | true |
| full_user_table_created | true |
| per_target_eligibility_created | true |
| planned_limit_bug_found | false |
| authority_budget_blocking | false |
| policy_suppression_found | false |
| candidate_count_correct | true |
| candidate_count_bug | false |
| candidate_count_policy_suppressed | false |
| ba1_ba2_reduced_pool_correctly | true |
| ba3_safe_to_rerun_now | false |
| users_moved | 0 |
| apply_executed | false |
| routing_changed | false |
| policy_changed | false |
| deploy_executed | false |
| final_classification | CANDIDATE_COUNT_CORRECT |
| SAFE_NEXT_STEP | CHANNEL_POOL_RECOVERY_OR_WAIT_FOR_HEALTHY_POOL_THEN_RERUN_BA3 |
