# V7 Vozduh - документация для передачи проекта

Дата: 2026-06-13

Ветка разработки: `Updatesystem`

Репозиторий: `muhapauka-rgb/V7-Vozduh`

Назначение документа: передать стороннему инженеру или команде целостное понимание проекта без доступа к истории чата.

Важно: документ не содержит паролей, секретов, токенов, приватных ключей и команд, которые сами по себе дают доступ к production.

---

## 1. Краткое резюме

V7 Vozduh - это control plane для управления VPN/egress-каналами, пользователями, маршрутизацией, качеством сервисов и безопасным переносом пользователей между каналами.

Система выросла от ручного управления каналами до управляемого и частично автономного контура:

```text
Наблюдение
-> Анализ
-> Планирование
-> Governance / approval
-> Restore barrier
-> Apply
-> Verification
-> Feedback
-> Trust / prediction update
-> Следующие решения
```

Текущий доказанный статус:

- one-user autonomy: certified
- two-user autonomy: certified
- five-user autonomy: certified
- ten-user autonomy: certified
- 25-user autonomy: not certified, потому что сейчас нет 25 реальных planner-selected кандидатов
- pool state: stable equilibrium
- current production pool: `awg3`, `wireguard-1779454504-c43409`, `vless`
- current distribution: `awg3=8`, `wireguard=8`, `vless=10`
- runtime truth/convergence по последним отчетам: PASS / FULLY_ALIGNED

Главный вывод: ядро маршрутизации и безопасного исполнения работает. Текущие пробелы относятся в основном к эксплуатации, резерву каналов, UX админки, lineage высокорисковых инструментов и будущей модели динамического batch sizing.

---

## 2. Что делает система

V7 управляет:

- пользователями и их текущим egress-каналом;
- списком egress/VPN-каналов;
- health/service quality каналов;
- route-class логикой;
- рекомендациями планировщика;
- safe apply перемещений;
- rollback readiness;
- feedback после исполнения;
- trust/prediction/recommendation evidence;
- operator/admin UI.

Система не должна просто "перетаскивать всех". Правильная логика:

1. Сначала измерить состояние каналов.
2. Проверить, есть ли реальные кандидаты на перенос.
3. Сформировать план.
4. Зафиксировать approved plan lock.
5. Проверить restore barrier.
6. Перед apply повторно проверить snapshot/source bundle.
7. Двигать только approved users.
8. Проверить маршруты.
9. Материализовать feedback.
10. Обновить trust/prediction/recommendation.

---

## 3. Основные директории и файлы

### Runtime / planner

- `tools/v7-users-autoswitch`
  - главный runtime planner и executor;
  - умеет dry-run, selected moves, restore barrier, apply, verify;
  - владелец planner decision chain.

- `tools/v7-truth-check`
  - проверяет локальную, GitHub и production truth;
  - блокирует runtime action, если truth неизвестна или опасна.

- `tools/v7-convergence-status`
  - показывает convergence и `runtime_action_safe`.

- `tools/v7-safe-deploy`
  - approved deploy path;
  - копирует только разрешенные runtime binaries;
  - пишет deployment provenance;
  - не двигает пользователей.

- `tools/v7-intelligence-snapshot-refresh`
  - materializes intelligence snapshots;
  - используется pre-planner refresh / feedback loop.

### Admin

- `admin/v7-admin-api`
  - основной admin API и embedded UI;
  - все еще большой монолит;
  - содержит auth/RBAC/CSRF, handlers, UI, action endpoints, read endpoints.

### Admin core modules

- `admin_core/operator_execution.py`
  - execution packet/governance/restore-barrier model.

- `admin_core/operator_execution_feedback.py`
  - feedback materialization.

- `admin_core/operator_observability.py`
  - read-only operator timeline/evidence.

- `admin_core/operator_decision_surface.py`
  - operator decision/readiness surface.

- `admin_core/routing_brain.py`
  - advisory routing brain integration.

- `admin_core/routing_intelligence.py`
  - routing intelligence models.

- `admin_core/intelligence_platform.py`
  - intelligence platform models.

- `admin_core/intelligence_workers.py`
  - snapshot workers.

- `admin_core/intelligence_snapshots.py`
  - snapshot readers/writers/contracts.

- `admin_core/admin_registry_views.py`
  - read-only registry views.

- `admin_core/runtime_read_views.py`
  - read-only runtime payload builders.

- `admin_core/route_reality_views.py`
  - route reality read views.

- `admin_core/diagnostic_views.py`
  - diagnostic read views.

- `admin_core/performance_summaries.py`
  - API performance/read-only summary foundation.

### Documentation / evidence

В корне много `*_REPORT.md` и evidence-папок. Это не мусор, а аудитная история проекта. Для текущего состояния важнее всего:

- `POOL1_POST_AUTONOMY_STABILITY_AND_EQUILIBRIUM_REPORT.md`
- `BA6_25_USER_AUTONOMY_CERTIFICATION_REPORT.md`
- `BA5_POOL_SCALE_AND_DYNAMIC_BATCH_MODEL_REPORT.md`
- `BA4_TEN_USER_AUTONOMY_CERTIFICATION_REPORT.md`
- `BA3_RETRY_FIVE_USER_AUTONOMY_CERTIFICATION_REPORT.md`
- `ATOMIC1_CLOSE_AND_BA2_RECERTIFICATION_REPORT.md`
- `BA1_FINAL_AUTONOMY_CERTIFICATION_REPORT.md`
- `WG_PROMOTE_APPLY_AND_POOL_VALIDATION_REPORT.md`
- `TRANSPORT1_AWG0_AWG3_RAW_STABILITY_FORENSICS_REPORT.md`
- `PROGRAM_API5_RUNTIME_READ_VIEWS_AND_PERFORMANCE_FOUNDATION_REPORT.md`
- `LOOP1_GOVERNED_EXECUTION_LOOP_ASSEMBLY_REPORT.md`
- `OA2_CLOSE_AND_OA34_RECERTIFICATION_REPORT.md`

---

## 4. Текущий production/runtime статус

По последним отчетам:

- source branch: `Updatesystem`
- last committed report: `ae7f35a PROGRAM POOL1 post autonomy stability certification`
- previous BA6 commit: `811d122 PROGRAM BA6 twenty five user autonomy certification`
- runtime truth: known
- convergence: aligned / fully aligned
- runtime action safe: true, когда truth gate PASS

Модель deployment:

- production использует copied-binary deployment model;
- runtime root не обязательно является git checkout;
- provenance пишется через deploy manifest / runtime linkage;
- truth-check знает docs-only mismatch и не блокирует runtime action из-за отчетов/evidence.

Важно для стороннего:

Не делать `scp` файлов вручную в production.
Использовать только approved safe deploy process.

---

## 5. Главный runtime loop

Сертифицированный loop:

```text
Observe
-> Analyze
-> Plan
-> Governance
-> Execute
-> Verify
-> Feedback
-> Trust Update
-> Future Decisions
-> Observe Again
```

Сертифицированные владельцы:

| Stage | Owner |
|---|---|
| Observe | runtime registry/snapshot readers |
| Analyze | `admin_core/intelligence_workers.py`, `admin_core/intelligence_platform.py`, CTR/RI |
| Plan | `tools/v7-users-autoswitch` |
| Governance | `admin_core/operator_execution.py`, execution packet tools |
| Restore barrier | existing operator execution/governance path |
| Apply/Verify | `tools/v7-users-autoswitch --apply --verify` |
| Feedback | `admin_core/operator_execution_feedback.py`, `/api/actions/execution-feedback-materialize` |
| Trust refresh | `tools/v7-intelligence-snapshot-refresh` |
| Future decision reuse | planner snapshots and trust/prediction/recommendation summaries |

Система fail-closed. Если любой gate UNKNOWN/FAIL, action должен остановиться.

---

## 6. Planner и выбор канала

Планировщик не выбирает канал только по скорости. Он учитывает:

- health/severity;
- service suitability;
- Telegram/Google/YouTube/Instagram/Google Auth;
- route class;
- speed average;
- speed floor/min/p10;
- stability;
- load/capacity/headroom;
- trust;
- prediction;
- suitability;
- CTR advisory;
- canary/reserve/manual flags;
- governance limits;
- sticky/current route behavior.

Ключевое:

- service score отвечает: "сервисы доступны?"
- stability отвечает: "скорость достаточно ровная?"
- capacity отвечает: "канал не перегружен?"
- trust/prediction отвечают: "есть ли историческая уверенность?"

Поэтому канал может иметь service score около 100, но быть непригодным как target из-за плохой stability.

---

## 7. Каналы и текущий pool

Текущий стабильный pool после autonomy этапов:

| Канал | Пользователи | Eligible | Роль |
|---|---:|---|---|
| `awg3` | 8 | yes | production pool |
| `wireguard-1779454504-c43409` | 8 | yes | production pool |
| `vless` | 10 | yes | production pool |

Нерабочие/нецелевые сейчас:

| Канал | Причина |
|---|---|
| `awg0` | transport instability / low speed floor |
| `openvpn-1779388847-d2ad7c` | hard fail / service failure |
| `1` | hard fail / Telegram down / speed floors |
| `amneziawg-exec-20260528-10-8-1-14` | manual/reserve/canary/execution-only + stability issue |

WireGuard был ранее canary-reserved, затем прошел governance/capacity review и был promoted в production pool.

---

## 8. Autonomy ladder

Доказанная лестница:

| Stage | Status | Evidence |
|---|---|---|
| 1 user | certified | `BA1_FINAL_AUTONOMY_CERTIFICATION_REPORT.md` |
| 2 users | certified | `ATOMIC1_CLOSE_AND_BA2_RECERTIFICATION_REPORT.md` |
| 5 users | certified | `BA3_RETRY_FIVE_USER_AUTONOMY_CERTIFICATION_REPORT.md` |
| 10 users | certified | `BA4_TEN_USER_AUTONOMY_CERTIFICATION_REPORT.md` |
| 25 users | blocked, not failed | `BA6_25_USER_AUTONOMY_CERTIFICATION_REPORT.md` |

25-user статус:

- authority budget 25 существует;
- policy временно принимала planned limit 25;
- скрытого ceiling не найдено;
- execution не был выполнен, потому что `candidate_moves_total=0`;
- лимит был возвращен к последнему доказанному ceiling 10.

Смысл: система не должна двигать людей ради сертификации. Нужны реальные planner-selected candidates.

---

## 9. Batch sizing model

BA5 рекомендовал `HYBRID_RECOMMENDED`.

Существующая модель уже имеет:

- candidate count;
- move type limits;
- `autoswitch_max_planned_per_run`;
- `--max-selected-moves`;
- authority budget gate;
- restore barrier;
- snapshot gate;
- atomic envelope;
- rollback cap.

Рекомендуемая будущая формула:

```text
batch_size =
  min(
    candidate_moves_total,
    certified_authority_budget,
    current_policy_cap,
    target_capacity_headroom,
    rollback_cap,
    snapshot_gate_cap,
    atomic_envelope_cap,
    dynamic_pool_advice
  )
```

Но сейчас dynamic batch sizing не является runtime-authoritative owner. Он advisory/partial.

Текущий честный runtime ceiling: 10.

Authority budget: 25.

---

## 10. Feedback и learning loop

Feedback loop сертифицирован.

После execution материализуются:

- outcome;
- trust;
- prediction;
- recommendation;
- closure.

Эти записи попадают в:

- execution events;
- runtime trust;
- proposal records;
- closure records;
- intelligence snapshots.

После refresh planner видит новые evidence.

Ограничение: часть feedback scoring исторически консервативна. Ранние отчеты показывали `outcome_status=unknown` / zero deltas в отдельных случаях. Это не блокирует loop, но требует будущей calibration, чтобы feedback давал более сильный обучающий сигнал.

---

## 11. CTR / Channel Trust Recovery

CTR-трек прошел архитектуру, advisory implementation и verification.

Фактическая роль CTR:

- полезен для explainability;
- полезен как governance evidence;
- полезен как advisory signal;
- не является hard gate;
- не должен напрямую approve/deny packets;
- не должен создавать selected moves;
- не должен быть отдельным planner.

Финальное понимание: CTR остается advisory/explainability слоем, а фактический winner selection контролирует planner chain через service/capacity/safety/trust/suitability.

---

## 12. Admin UI / Admin API

Admin UI доступен через `/admin-v2`.

Что уже есть:

- users table;
- channels table;
- route/status views;
- operator surfaces;
- approval/preview surfaces;
- channel drawers;
- inline speed/service checks;
- evidence/proposal surfaces;
- execution controller preview.

Крупная проблема:

`admin/v7-admin-api` все еще монолит примерно `35k+` строк.

Уже вынесено:

- read-only registry views;
- operator/service/runtime/route/diagnostic views;
- performance summaries;
- helper modules.

Осталось внутри монолита:

- auth/session/RBAC/CSRF;
- HTTP routing;
- action handlers;
- governance entrypoints;
- rollback entrypoints;
- execution entrypoints;
- audit writers;
- closure writers;
- embedded UI.

Следующий безопасный путь: не трогать auth первым. Продолжать read-only/preview extraction, затем отдельно handler decomposition.

---

## 13. Operator UX

Принцип UX, который нужно сохранить:

```text
Оператор не должен думать, где какая версия и что запускать руками.
Админка должна показывать коротко:
что не так,
почему,
что можно сделать,
какая кнопка исправляет именно это.
```

Текущее состояние:

- часть UX уже улучшена;
- channel warnings открывают конкретные drawers;
- speed/service rows получили inline behavior;
- operator approved controller умеет approve/reject preview.

Пробел:

в UI все еще встречаются английские/технические элементы вроде:

- `Apply Best Recommendations`
- `Recommendation`
- `Warning`
- raw technical statuses

Для стороннего UI-инженера: следующая задача - `ADMIN_RU_OPERATOR_SIMPLIFICATION`.

Цель:

- все visible labels на русском;
- короткие фразы;
- no generic technical dumps by default;
- каждая проблема открывает одно окно решения;
- не показывать оператору лишние ветки, если действие не относится к текущей проблеме.

---

## 14. Truth / convergence / release model

В проекте уже есть постоянная модель truth:

- local workspace;
- GitHub branch;
- production runtime binary/linkage;
- runtime state;
- convergence snapshot.

Ключевые tools:

- `tools/v7-truth-check --all --json`
- `tools/v7-convergence-status --json`
- `tools/v7-convergence-owner`
- `tools/v7-safe-deploy`
- `tools/v7-safe-push`
- `tools/v7-safe-commit`
- `tools/v7-release-sync`

Важное правило:

Документационные commits не должны блокировать runtime action, если runtime code не менялся. Это уже закрыто через docs-only mismatch classification.

Запрещено:

- manual copy random files;
- force push;
- deploy без safe deploy;
- runtime mutation без truth gate.

---

## 15. Restore barrier / atomic envelope / drift protection

Были исторические проблемы:

- stale restore barrier;
- expired generation;
- approved plan lock mismatch;
- snapshot source mismatch;
- quality_summary/service_matrix drift.

Они закрыты через:

- fresh packet;
- fresh restore barrier;
- source bundle stability;
- decision signature;
- atomic envelope;
- fail-closed recheck.

Правило:

Если between approval and apply изменился decision-significant source bundle и selected users/targets/hash уже не совпадают, apply должен быть заблокирован.

Если drift безопасен и decision signature не изменилась, ATOMIC.1/STABILITY.1 позволяют не блокировать бессмысленно.

---

## 16. Security / safety boundaries

Нельзя делать без отдельного approved program:

- autoswitch apply;
- user movement;
- routing mutation;
- policy apply;
- restore barrier write;
- authority promotion;
- autonomy expansion;
- systemd mutation;
- service restart;
- cleanup/delete;
- manual production file copy.

Любое runtime action должно проходить:

1. truth-check;
2. convergence-status;
3. planner;
4. packet;
5. restore barrier;
6. post-clearance dry-run;
7. atomic envelope;
8. apply;
9. verify;
10. feedback/trust refresh.

---

## 17. Что сейчас работает

Работает:

- production truth/convergence model;
- safe deploy model;
- planner dry-run;
- restore barrier;
- atomic source bundle guard;
- 1/2/5/10 user autonomy;
- WireGuard production pool;
- feedback materialization;
- trust/prediction/recommendation refresh;
- operator approved preview controller;
- pool equilibrium after autonomy execution;
- read-only admin decomposition foundation;
- channel service/speed UI improvements.

---

## 18. Что не реализовано до конца

### 18.1 25-user autonomy

Не сертифицирована.

Причина: сейчас нет 25 реальных кандидатов.

Это не дефект. Не форсировать.

Следующий шаг: pool observation + ждать real candidate demand.

### 18.2 Runtime-owned hybrid batch sizing

BA5 рекомендовал hybrid, но runtime-authoritative model еще не внедрен.

Следующий шаг: design/implementation stage, где dynamic advice может только уменьшать batch внутри certified ceiling.

### 18.3 Channel reserve / recovery

`awg0` нестабилен.

`openvpn` и `1` не production-ready.

Следующий шаг: `AWG0_RECOVERY_OR_REPLACEMENT`, затем channel reserve hardening.

### 18.4 Admin API monolith

Read-only extraction сделан, но action/governance/execution/UI все еще в монолите.

Следующий шаг: decomposition без изменения runtime behavior.

### 18.5 Admin UX localization/simplification

Нужно убрать английские/технические labels и сделать operator-first русский интерфейс.

Следующий шаг: `ADMIN_RU_OPERATOR_SIMPLIFICATION`.

### 18.6 Track7 high-risk lineage

Direct/RU, Trusted RU, policy apply, proxy apply, 일부 production-only tools не полностью закрыты по live safety/rollback.

Следующий шаг: lineage/governance closure без live apply.

### 18.7 Feedback calibration

Learning loop есть, но feedback scoring можно усилить, чтобы успешные executions сильнее и понятнее влияли на future decisions.

Следующий шаг: `FEEDBACK_CALIBRATION_AND_OUTCOME_SCORE_TUNING`.

---

## 19. Рекомендуемый порядок следующих работ

### Шаг 1. Admin RU Operator Simplification

Зачем: сделать систему понятной не инженеру.

Scope:

- русский язык;
- короткие статусы;
- кликабельные problems;
- одно окно на одну проблему;
- убрать английские labels;
- не трогать runtime.

### Шаг 2. Pool Observation Window

Зачем: доказать, что `POOL_STABLE` сохраняется во времени.

Scope:

- read-only;
- planner dry-run;
- channel health;
- distribution;
- feedback drift;
- no movement.

### Шаг 3. AWG0 Recovery / Replacement

Зачем: расширить резерв.

Scope:

- raw transport audit;
- endpoint/path diagnosis;
- no floor lowering without proof;
- if unrecoverable, replacement channel plan.

### Шаг 4. Hybrid Batch Runtime Owner Design

Зачем: перейти от fixed ladder к production batch model.

Scope:

- dynamic desired size;
- hard certified ceiling;
- fail-closed gates;
- no autonomy expansion.

### Шаг 5. Track7 High-Risk Lineage Closure

Зачем: закрыть коммерческие runtime риски вне autoswitch.

Scope:

- Direct/RU;
- Trusted RU;
- policy apply;
- proxy apply;
- rollback runbooks;
- no live mutation first.

---

## 20. Как стороннему инженеру безопасно начать

1. Прочитать этот документ.
2. Прочитать последние отчеты:
   - `POOL1_POST_AUTONOMY_STABILITY_AND_EQUILIBRIUM_REPORT.md`
   - `BA6_25_USER_AUTONOMY_CERTIFICATION_REPORT.md`
   - `BA5_POOL_SCALE_AND_DYNAMIC_BATCH_MODEL_REPORT.md`
   - `PROGRAM_API5_RUNTIME_READ_VIEWS_AND_PERFORMANCE_FOUNDATION_REPORT.md`
   - `TRANSPORT1_AWG0_AWG3_RAW_STABILITY_FORENSICS_REPORT.md`
3. Не запускать apply.
4. Не менять production.
5. Для любых runtime действий сначала:

```bash
tools/v7-truth-check --all --json
tools/v7-convergence-status --json
```

6. Для разработки начинать с read-only/UI/report/test blocks.
7. Все изменения коммитить маленькими отдельными commits.
8. Production deploy только через approved safe deploy path.

---

## 21. Самое важное для передачи

V7 сейчас не находится в хаосе.

Проект прошел длинную цепочку сертификаций. Исторические NO-GO отчеты не должны восприниматься как текущие блокеры, если они закрыты более поздними PASS/certified отчетами.

Текущий живой смысл:

- execution ядро работает;
- pool стабилен;
- система не двигает пользователей без реальной причины;
- 25-user batch не доказан не потому что сломан, а потому что сейчас нечего двигать;
- следующий коммерчески полезный слой - не новые apply, а UX, резерв каналов, lineage и batch model.
