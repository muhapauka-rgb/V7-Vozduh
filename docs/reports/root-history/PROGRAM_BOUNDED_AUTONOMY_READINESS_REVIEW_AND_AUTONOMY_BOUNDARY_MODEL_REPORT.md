# PROGRAM BOUNDED AUTONOMY READINESS REVIEW AND AUTONOMY BOUNDARY MODEL REPORT

Дата: 2026-06-08

Проект: V7 Vozduh  
Ветка: `Updatesystem`  
Режим: review only, без apply, без движения пользователей, без включения автономии.

## Короткий Итог

Система готова к shadow autonomy и operator approval mode.

Это значит: V7 может сама анализировать, предлагать, объяснять и готовить решение для оператора.

Но V7 пока не должна сама выполнять live apply. Главный стопор: автоматический live execution и автоматический rollback ещё не сертифицированы как безопасный замкнутый контур.

## Truth Baseline

Проверено:

- local/GitHub/production commit: `54b971f947db38e733601d96f948b86d1865e619`
- branch: `Updatesystem`
- `tools/v7-truth-check --all --json`: PASS
- `tools/v7-convergence-status --json`: ALIGNED
- runtime action guard: `READY_FOR_RUNTIME_ACTION`

Вывод: база синхронна. Можно честно оценивать границы автономии.

## 1. Autonomy Surface Inventory

| Поверхность | Текущий владелец | Статус |
|---|---|---|
| Planner dry-run | `tools/v7-users-autoswitch` | можно автоматизировать read-only |
| Candidate/recommendation view | `admin_core/operator_decision_surface.py` | можно автоматизировать read-only |
| Packet draft | `tools/v7-operator-execution-packet` | можно с guard, без apply |
| Restore barrier clearance | `admin_core/operator_execution.py` | только после operator approval |
| Apply approval | оператор + governed apply | operator approval required |
| Governed apply | `tools/v7-users-autoswitch --apply --verify` | не автономно сейчас |
| Rollback | rollback packet + governed rollback executor | operator approval required сейчас |
| Authority promotion | `tools/v7-users-autoswitch` + explicit confirmation | operator only |
| Trust review | `admin_core/operator_decision_surface.py` / snapshots | можно автоматизировать read-only |
| Channel review | snapshots / service matrix | можно автоматизировать read-only |

## 2. Autonomy Classification

| Действие | Класс |
|---|---|
| Truth/convergence summary | AUTONOMOUS_ALLOWED |
| Snapshot status review | AUTONOMOUS_ALLOWED |
| Planner dry-run | AUTONOMOUS_ALLOWED |
| Recommendation explanation | AUTONOMOUS_ALLOWED |
| Trust/prediction/recommendation scoring review | AUTONOMOUS_ALLOWED |
| Packet draft generation | AUTONOMOUS_ALLOWED_WITH_GUARDS |
| 5/10/25 user packet preview | AUTONOMOUS_ALLOWED_WITH_GUARDS |
| Feedback materialization after verified governed execution | AUTONOMOUS_ALLOWED_WITH_GUARDS |
| Restore barrier clearance | OPERATOR_APPROVAL_REQUIRED |
| Governed apply invocation | OPERATOR_APPROVAL_REQUIRED |
| Rollback invocation | OPERATOR_APPROVAL_REQUIRED |
| Authority promotion | OPERATOR_ONLY |
| Pool expansion | OPERATOR_ONLY |
| Autonomy promotion | OPERATOR_ONLY |
| Planner floors / policy changes | OPERATOR_ONLY |
| Disable gates / force eligibility | OPERATOR_ONLY |

## 3. Blast Radius Model

| Level | Users | Safe autonomy now |
|---|---:|---|
| CANARY | 1 | shadow only |
| SMALL_BATCH | 2 | shadow + operator approval |
| MEDIUM_BATCH | 5 | shadow + operator approval |
| LARGE_BATCH | 10 | shadow + operator approval |
| POOL | 25 | shadow + operator approval |

Maximum safe live autonomy scope now: `0 users`.

Reason: automatic live apply and automatic rollback execution are not certified.

## 4. Trust Requirements

Before any future bounded live autonomy, each selected move must have:

- planner confidence known,
- trust score known,
- prediction confidence known,
- recommendation confidence known,
- source hashes stable,
- snapshot gate PASS,
- no hard service blocker,
- rollback target known,
- audit and closure paths available.

If any value is UNKNOWN: stop.

## 5. Rollback Requirements

Required for future bounded live autonomy:

- rollback packet per selected user,
- rollback target still known at execution time,
- rollback executor available,
- rollback verification path defined,
- automatic stop on partial success,
- no ad hoc rollback path,
- audit and closure for rollback result.

Current blocker: rollback policy exists, but autonomous rollback execution is not certified as an operator-free loop.

## 6. Operator Boundary

These remain operator-controlled:

- authority promotion,
- pool expansion,
- autonomy promotion,
- governance/policy changes,
- service eligibility overrides,
- planner floor changes,
- disabling safety gates,
- manual incident handling,
- rollback after ambiguous or partial execution.

This boundary should remain permanent unless a later explicit certification changes it.

## 7. Shadow Autonomy Model

Allowed now:

1. System runs truth/snapshot/planner review.
2. System forms recommendation.
3. System explains reason, risk, trust, prediction and rollback readiness.
4. Operator compares system decision with expected action.
5. No apply. No user movement.

Verdict: SHADOW_READY=true.

## 8. Approval Autonomy Model

Allowed now:

1. System proposes.
2. System prepares packet draft.
3. Operator approves.
4. Restore barrier is cleared through canonical owner.
5. Governed apply remains explicit and approved.
6. Verification and feedback close the result.

Verdict: APPROVAL_READY=true.

## 9. Bounded Autonomy Model

Not enabled now.

Future model must be:

- same planner,
- same packet schema,
- same restore barrier,
- same governed apply,
- same rollback packet,
- same audit/closure,
- no second execution path,
- blast radius capped by authority and packet,
- automatic rollback only after separate certification.

Verdict: BOUNDED_READY=false.

## 10. Readiness Review

| Capability | Verdict | Reason |
|---|---|---|
| Shadow | READY | all required surfaces are read-only and aligned |
| Operator approval | READY | packet, barrier, recheck, governed apply and feedback chain exist |
| Bounded live autonomy | NOT READY | automatic apply/rollback loop not certified |
| Production autonomy | NOT READY | would violate current safety boundary |

## 11. Gap Analysis

| Area | Status |
|---|---|
| Trust | usable for decision support |
| Telemetry | usable for operator review |
| Performance | usable for slow-path visibility |
| Governance | strong, operator-owned |
| Rollback | policy and executor exist, autonomous loop not certified |
| Operator visibility | ready enough for approval mode |

Single blocker: `AUTONOMOUS_APPLY_AND_ROLLBACK_LOOP_NOT_CERTIFIED`.

## 12. Certification

The current system can safely move from “operator sees reports” to “operator sees system decisions and approves them”.

It cannot yet move to “system executes without operator”.

## Final Verdicts

autonomy_surface_inventory_complete=true  
autonomy_classification_complete=true  
blast_radius_model_defined=true  
trust_requirements_defined=true  
rollback_requirements_defined=true  
operator_boundary_model_defined=true  
shadow_model_defined=true  
approval_model_defined=true  
bounded_model_defined=true  
autonomy_readiness_review_complete=true  
shadow_ready=true  
approval_ready=true  
bounded_ready=false  
single_blocker=AUTONOMOUS_APPLY_AND_ROLLBACK_LOOP_NOT_CERTIFIED  
users_moved=0  
apply_executed=false  
autonomy_enabled=false  
SAFE_NEXT_STEP=SHADOW_AUTONOMY_DECISION_LOG_AND_OPERATOR_COMPARISON_NO_APPLY

## Plain Russian Summary

Сейчас V7 уже можно учить “думать самой”: выбирать лучший вариант, объяснять почему, показывать риск, доверие, прогноз и готовить пакет.

Но кнопку “сделай сама” включать рано.

Следующий правильный этап: сделать журнал shadow autonomy. Система будет сама предлагать действие, оператор будет видеть “что бы она сделала”, сравнивать с реальным решением и накапливать доказательства. Без движения пользователей.

