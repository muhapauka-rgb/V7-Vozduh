# CTR.P1 Production Readiness Program Report

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Program: `CTR.P1 CTR PRODUCTION READINESS PROGRAM`

Date: 2026-06-11

Safety envelope:

- runtime mutation: not performed
- user movement: not performed
- autoswitch apply: not performed
- routing changes: not performed
- governance bypass: not performed
- restore barrier changes: not performed
- deploy: not performed

## 1. Executive Summary

CTR уже имеет реальную основу: lifecycle states, trust/recovery snapshot, owner mapping, admin surface, no-bypass governance chain and integration design.

CTR.P1 перевёл состояние из `DESIGN_READY` в первый безопасный production-readiness шаг:

- operator visibility улучшена в существующей админке;
- тексты CTR теперь короткие, русские и понятные оператору;
- для каждого состояния добавлены причина, действие, recovery path и blocked action summary;
- добавлены no-bypass тесты для read-only CTR surface;
- runtime/planner/governance authority не изменены.

Final verdict: `READY_FOR_ADVISORY_IMPLEMENTATION`

Важно: CTR ещё не должен быть hard runtime gate. Безопасно начинать с advisory/operator surface и тестов. Governance/pool integration готовы к реализации следующим этапом, но runtime enforcement пока рано включать.

## 2. Visibility & Explainability Spec

Current UI behavior:

- existing admin column: `Состояние доверия`
- existing click drawer: `openChannelStateDrawer`
- source: `trust-evolution-summaries.channel_trust_recovery`
- fallback: `legacy_operator_decision_surface_fallback`

Implemented in CTR.P1:

- `admin_core/operator_decision_surface.py`
  - `CHANNEL_STATE_COPY` converted to short Russian operator-facing text.
  - Added `channel_state_recovery_path`.
  - Added `channel_state_blocked_action_summary`.
- `admin/v7-admin-api`
  - Existing channel drawer now shows:
    - `Путь восстановления`
    - `Заблокировано`

Final operator-facing state contract:

| State | Reason | Recommended Action | Recovery Path | Blocked Action Summary |
|---|---|---|---|---|
| NEW | Мало успешной истории | Наблюдать и ждать свежих успешных исходов | После успехов перейти в WATCH/TRUSTED | Не расширять нагрузку без review |
| TRUSTED | Проверки и исходы хорошие | Обычный мониторинг | Recovery не требуется | Прямой обход planner/governance запрещён |
| WATCH | Работает, но истории мало | Наблюдать 24-72 часа или до success feedback | После успехов перейти в TRUSTED | Массовое расширение требует review |
| DEGRADED | Качество или сервисы просели | Обновить проверки сервисов и качества | После стабильных проверок перейти в RECOVERING/WATCH | Не выбирать как обычную цель без operator review |
| RECOVERING | Канал восстанавливается | Дождаться стабильности или двух успешных наблюдений | После подтверждения перейти в WATCH/TRUSTED | Не расширять нагрузку автоматически |
| QUARANTINED | Жёсткий негатив или провал сервисов | Починить причину и обновить проверки | Сначала RECOVERING, потом WATCH/TRUSTED | Не выбирать как обычную цель; только emergency/rollback review |

No new top-level admin section was created.

## 3. No-Bypass Certification

CTR.P1 adds targeted no-bypass coverage in `tests/unit/test_operator_decision_surface.py`.

Certification matrix:

| Capability | CTR status | Evidence |
|---|---:|---|
| create selected moves | cannot | no selected move write path in operator surface |
| approve packets | cannot | no packet approval API in operator surface |
| write restore barrier | cannot | no restore barrier write function/import |
| bypass planner | cannot | `planner_authority_changed=false` |
| bypass governance | cannot | `governance_changed=false` |
| bypass runtime owner | cannot | `execution_allowed_now=false` |
| bypass capacity owner | cannot | no capacity decision write path |
| bypass batch owner | cannot | no batch authority or promotion path |
| create truth source | cannot | `new_truth_sources_created=false` |
| create duplicate system | cannot | `duplicate_systems_created=false` |

Targeted tests run:

- `python3 -m unittest tests.unit.test_operator_decision_surface` -> PASS

## 4. Governance Integration Map

State-to-governance contract:

| State | Packet Generation | Packet Validation | Operator Approval | Pool Participation | Expansion Approval |
|---|---|---|---|---|---|
| TRUSTED | ALLOWED | ALLOWED | normal | ALLOWED | ALLOWED under existing budget |
| WATCH | ALLOWED | ALLOWED | REVIEW_REQUIRED for expansion | ALLOWED | REVIEW_REQUIRED |
| NEW | ALLOWED | ALLOWED | REVIEW_REQUIRED | ALLOWED with observation | REVIEW_REQUIRED |
| RECOVERING | REVIEW_REQUIRED | REVIEW_REQUIRED | required | limited | REVIEW_REQUIRED |
| DEGRADED | REVIEW_REQUIRED | DENIED unless emergency/recovery | required | suppress as normal target | EMERGENCY_ONLY |
| QUARANTINED | DENIED for normal target | DENIED for normal target | emergency/rollback only | removed as normal target | EMERGENCY_ONLY |

Already exists:

- approval packet lifecycle: `admin_core/operator_execution_pipeline.py`
- restore barrier lifecycle: `admin_core/operator_execution_pipeline.py`
- governed runtime executor: `tools/v7-users-autoswitch`
- blocked direct switch path: `direct_user_switch_blocker`
- admin operator surface: `admin_core/operator_decision_surface.py`

Needs implementation later:

- packet evidence fields for CTR state;
- packet validation warnings/denials based on CTR state;
- review-required semantics for WATCH/NEW/RECOVERING/DEGRADED;
- normal-target hard deny for QUARANTINED only after emergency tests.

## 5. Pool Integration Plan

CTR must reuse existing best available pool logic. It must not create a new pool, ranking engine, planner or truth source.

| State | Pool Entry | Ranking | Removal | Re-entry | Classification |
|---|---|---|---|---|---|
| TRUSTED | yes | soft positive | no | normal | READY_TO_IMPLEMENT |
| WATCH | yes | neutral | no | normal | READY_TO_IMPLEMENT |
| NEW | yes | small soft penalty | no | after evidence | READY_TO_IMPLEMENT |
| RECOVERING | conditional | soft penalty | no hard removal | after recovery evidence | READY_TO_IMPLEMENT |
| DEGRADED | conditional/emergency | strong penalty | normal target suppression later | after stable checks | HIGH_RISK |
| QUARANTINED | emergency/rollback only | no normal ranking | remove as normal target later | after recovery path | DEFER |

Safe now:

- expose CTR state and reasons;
- add dry-run explanations;
- add pool/ranking tests.

Unsafe now:

- hard runtime suppression before emergency matrix tests;
- lowering service floors;
- forcing eligibility;
- changing selected move generation without governance tests.

## 6. Emergency Matrix

| Scenario | Planner Behavior | Governance Behavior | Runtime Behavior | Operator Behavior | Recovery Behavior | Verdict |
|---|---|---|---|---|---|---|
| All channels DEGRADED | fail closed or review only | REVIEW_REQUIRED | no automatic apply | show all degraded reasons | refresh checks/recovery | REVIEW_REQUIRED |
| All channels RECOVERING | limited candidates only | REVIEW_REQUIRED | no automatic expansion | show recovery path | wait for success evidence | REVIEW_REQUIRED |
| All channels QUARANTINED | no normal target | DENIED except emergency/rollback | no normal apply | show hard block | fix cause first | FAIL_CLOSED |
| Single remaining channel | preserve availability, no blind block | REVIEW_REQUIRED | no unsafe movement | show capacity/risk | monitor and recover alternatives | REVIEW_REQUIRED |
| Required services unavailable | service-aware suppression | DENIED for affected service class | no normal movement to failing channel | show missing service | repair service checks | FAIL_CLOSED |
| Capacity exhausted | no expansion | DENIED | no apply over budget | show capacity blocker | free capacity or add channel | FAIL_CLOSED |

Emergency implementation must be tested before hard runtime enforcement.

## 7. Gap Closure Matrix

CTR.2.5 gaps revisited:

| Gap | Current Status | CTR.P1 Action | Next Classification |
|---|---|---|---|
| Russian operator copy incomplete | open | implemented | closed |
| Recovery path visibility incomplete | open | implemented | closed |
| Blocked action visibility incomplete | open | implemented | closed |
| No-bypass tests for surface | partial | implemented targeted tests | closed for advisory surface |
| Governance packet CTR evidence | missing | mapped | READY NOW |
| Pool soft CTR influence | missing | mapped | READY NOW |
| DEGRADED hard gate | missing | mapped | HIGH RISK |
| QUARANTINED hard gate | missing | mapped | NEEDS TESTS |
| Emergency scenarios | missing | matrix defined | NEEDS TESTS |
| Runtime enforcement | missing | explicitly deferred | DEFER |

## 8. Implementation Roadmap

Step 1: CTR advisory visibility closure

- Files:
  - `admin_core/operator_decision_surface.py`
  - `admin/v7-admin-api`
  - `tests/unit/test_operator_decision_surface.py`
- Status: implemented in CTR.P1
- Risk: LOW
- Rollback: revert these three files

Step 2: CTR.4 advisory dry-run explanations

- Files:
  - `tools/v7-users-autoswitch`
  - `admin_core/operator_decision_surface.py`
  - tests for dry-run explanation output
- Expected impact:
  - dry-run explains CTR state per candidate/channel;
  - no selected move behavior change.
- Risk: LOW
- Rollback: remove explanation fields only

Step 3: CTR.5 governance packet evidence

- Files:
  - `admin_core/operator_execution_pipeline.py`
  - packet validation tests
- Expected impact:
  - packets include CTR evidence;
  - operator sees review reason;
  - still no automatic denial except explicit policy cases.
- Risk: MEDIUM
- Rollback: stop requiring CTR evidence in packet validation

Step 4: CTR.6 pool soft influence

- Files:
  - `tools/v7-users-autoswitch`
  - planner unit tests
- Expected impact:
  - TRUSTED/WATCH/NEW/RECOVERING influence ranking softly;
  - no hard suppression yet.
- Risk: MEDIUM
- Rollback: remove CTR score adjustment

Step 5: CTR.7 emergency dry-run matrix

- Files:
  - `tools/v7-users-autoswitch`
  - emergency scenario tests
- Expected impact:
  - fail-closed behavior proven before enforcement.
- Risk: MEDIUM
- Rollback: tests only unless dry-run explanation changes

Step 6: CTR.8 QUARANTINED normal-target hard deny

- Files:
  - `tools/v7-users-autoswitch`
  - governance tests
- Expected impact:
  - QUARANTINED cannot be normal target.
- Risk: HIGH
- Rollback: disable hard deny and keep review-only

Step 7: CTR.9 DEGRADED conditional enforcement

- Files:
  - `tools/v7-users-autoswitch`
  - service-aware routing tests
- Expected impact:
  - DEGRADED suppressed for normal target when safe alternatives exist.
- Risk: HIGH
- Rollback: return to advisory penalty

## 9. Risk Review

Low risk:

- Russian operator copy.
- Additional read-only fields.
- Drawer visibility inside existing admin.
- No-bypass tests.

Medium risk:

- Packet validation requirements.
- Pool score influence.
- Review-required semantics.

High risk:

- Hard runtime suppression.
- DEGRADED/QUARANTINED enforcement without emergency tests.
- Any change to selected move generation before dry-run parity.

Main future risk:

If CTR becomes a hard gate too early, the system can over-block healthy channels during degraded-pool or single-channel scenarios. That would turn trust recovery into availability risk.

## 10. Readiness Certification

Readiness flags:

- ready_for_advisory_implementation=true
- ready_for_governance_integration=true
- ready_for_pool_integration=true
- ready_for_runtime_enforcement=false

Reason:

Advisory surface is safe and already partially implemented. Governance and pool integration have clear owners and bounded next steps. Runtime enforcement must wait until emergency matrix tests pass.

## 11. Recommended First Implementation Block

Recommended first block:

`CTR.4_advisory_surface_dry_run_explanations_and_no_bypass_tests`

Scope:

- Add CTR state to planner dry-run explanations.
- Keep selected moves unchanged.
- Show review-required reason for WATCH/NEW/RECOVERING/DEGRADED.
- Keep QUARANTINED as explanation-only until emergency tests.
- Add no-bypass tests proving CTR does not approve, apply, write restore barrier, or mutate runtime.

Do not start with hard runtime enforcement.

## 12. Final Verdict

Final verdict: `READY_FOR_ADVISORY_IMPLEMENTATION`

Final flags:

- ctr_visibility_spec_complete=true
- russian_operator_copy_implemented=true
- recovery_path_visible=true
- blocked_action_summary_visible=true
- no_bypass_tests_added=true
- governance_integration_mapped=true
- pool_integration_mapped=true
- emergency_matrix_defined=true
- implementation_roadmap_ready=true
- runtime_mutation_performed=false
- users_moved=0
- autoswitch_apply_run=false
- deploy_performed=false
- ready_for_advisory_implementation=true
- ready_for_governance_integration=true
- ready_for_pool_integration=true
- ready_for_runtime_enforcement=false
- safe_next_step=CTR.4_advisory_surface_dry_run_explanations_and_no_bypass_tests
