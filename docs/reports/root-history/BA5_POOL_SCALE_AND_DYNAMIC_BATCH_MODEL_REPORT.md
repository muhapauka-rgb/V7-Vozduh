# BA5 POOL SCALE AND DYNAMIC BATCH MODEL REPORT

Дата: 2026-06-13

Проект: V7 Vozduh

Ветка: Updatesystem

Режим: read-only audit. Runtime не менялся. Пользователи не двигались. Policy не менялась.

## 0. Phase 0: Existing Model Discovery

Главный результат Phase 0: модель batch уже существует и реально используется runtime.

Authoritative runtime owner:

- `tools/v7-users-autoswitch`

Authoritative admin policy owner:

- `admin/v7-admin-api`
- endpoint: `/api/actions/policy-update`

Runtime chain:

1. planner генерирует candidate moves;
2. `_select_moves()` разделяет движения по типам: failover, reconnect, rebalance, planned;
3. каждый тип режется своим лимитом:
   - `autoswitch_max_failover_per_run`;
   - `autoswitch_max_reconnect_per_run`;
   - `rebalance_max_moves_per_run`;
   - `autoswitch_max_planned_per_run`;
4. `--max-selected-moves` может дополнительно сузить выбор;
5. `authority_budget_gate` режет итог по certified/runtime authority;
6. restore barrier фиксирует approved plan lock;
7. snapshot gate проверяет свежесть источников;
8. atomic execution envelope защищает от опасного drift между approval и apply;
9. apply исполняет только утверждённый набор;
10. feedback/trust/prediction/recommendation замыкают learning loop.

Что уже есть:

| Область | Статус | Runtime authority |
|---|---:|---:|
| Execution batches | есть | да |
| Blast radius | есть как effective runtime scope | да |
| Planned limits | есть | да |
| Authority budgets | есть | да |
| Candidate scaling | есть через planner/selection | да |
| Pool-aware execution | есть через projected target load / healthy pool | да |
| Dynamic batch sizing | есть частично | advisory only |

Важно: `DynamicBlastRadiusModel` уже есть, но сейчас это не runtime-владелец. В коде он помечен как `runtime_decision_authority: none_shadow_only`. Значит его нельзя просто объявить главным лимитом без отдельного этапа.

## 1. Execution Reality

Сертифицированная лестница уже доказана реальными исполнениями:

| Этап | Размер | Результат |
|---|---:|---|
| BA1 | 1 user | APPLIED, feedback/learning loop закрыт |
| BA2 | 2 users | APPLIED, feedback/learning loop закрыт |
| BA3 | 5 users | APPLIED, feedback/learning loop закрыт |
| BA4 | 10 users | APPLIED, feedback/learning loop закрыт |

BA4 доказал:

- selected_moves=10;
- users_moved=10;
- snapshot gate clean;
- source mismatch empty;
- feedback materialized=10;
- trust/prediction/recommendation updated=true;
- final truth PASS;
- convergence ALIGNED.

## 2. Blast Radius Analysis

Текущий blast radius не является “свободным числом”.

Он фактически равен минимуму из:

- сколько кандидатов реально есть;
- сколько planner выбрал по типам move;
- сколько запросил оператор/CLI через `--max-selected-moves`;
- сколько разрешает `authority_budget_gate`;
- сколько разрешает restore barrier;
- сколько разрешает atomic envelope после recheck.

Это правильная безопасная модель.

Наблюдение по BA4: 10 пользователей были распределены по двум целям примерно как 5 + 5. Поэтому текущая доказанная реальность: 10 total и около 5 на один target в одном автономном batch.

## 3. Capacity Analysis

Последние доказанные capacity snapshots:

| Момент | Users | Egress | Healthy egress | Candidate moves |
|---|---:|---:|---:|---:|
| перед BA2 | 26 | 7 | 2 | 26 |
| перед BA3 | 26 | 7 | 3 | 25 |
| после BA3 feedback | 26 | 7 | 2 | 23 |
| перед BA4 | 26 | 7 | 3 | 20 |
| после BA4 feedback | unknown | unknown | 4 | 13 |

Вывод: batch size не должен быть фиксированным навсегда. После каждого исполнения pool меняется, candidate count меняется, healthy channels меняются.

## 4. Scaling Models

### Option A: Fixed Batch

Пример: всегда 10.

Плюсы:

- просто;
- уже доказано BA4;
- хорошо как текущий production ceiling.

Минусы:

- плохо масштабируется на 500/2000 users;
- не учитывает healthy pool;
- может быть слишком мало при большом здоровом pool;
- может быть слишком много при деградации каналов.

Verdict: не рекомендовать как финальную модель. Можно оставить как текущий safe ceiling.

### Option B: Ladder

Пример:

10 → 25 → 50

Плюсы:

- хорошо ложится на уже существующую authority ladder;
- безопасно;
- понятно оператору;
- не требует нового planner.

Минусы:

- слишком ручная модель, если оставить её единственной;
- не учитывает текущую плотность candidate pool.

Verdict: использовать как сертификационный потолок.

### Option C: Percentage

Пример:

5%, 10%, 20%.

Плюсы:

- естественно масштабируется.

Минусы:

- опасно без учёта channel health, rollback, trust, snapshot, atomic envelope;
- при 2000 users 20% может означать 400 движений, а это не сертифицировано.

Verdict: не использовать самостоятельно.

### Option D: Dynamic Pool-Aware

Размер зависит от:

- candidate_moves_total;
- healthy_egress_total;
- target capacity/headroom;
- trust/confidence;
- rollback readiness;
- snapshot gate;
- feedback freshness;
- authority budget.

Плюсы:

- правильная долгосрочная цель;
- хорошо подходит для 100/500/2000 users.

Минусы:

- сейчас runtime dynamic blast radius advisory-only;
- нельзя дать ему право превышать certified ceiling без нового этапа.

Verdict: правильная логика, но только внутри сертифицированного потолка.

### Option E: Hybrid

Рекомендуемая модель:

```
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

Где:

- ladder задаёт максимум, который вообще можно;
- dynamic модель выбирает разумный размер внутри этого максимума;
- runtime gates могут только уменьшить или остановить;
- ни один advisory-сигнал не может сам поднять лимит.

Verdict: HYBRID_RECOMMENDED.

## 5. Simulations

Симуляции сделаны только по существующим evidence-derived assumptions:

- current authority budget=25;
- current policy cap=10;
- доказанный per-target observed cap=5;
- текущий post-BA4 candidate pool=13;
- observed candidate ratios: 13/26, 20/26, 25/26.

Итог:

| Сценарий | Fixed 10 | Hybrid сейчас | Hybrid после 25-cert |
|---|---:|---:|---:|
| current 26 users / 13 candidates | 10 | 10 | 13 |
| 100 users | 10 | 10 | 25 |
| 500 users | 10 | 10 | 25 |
| 2000 users | 10 | 10 | 25 |

Это не значит, что V7 навсегда ограничена 25. Это значит: при текущем certified authority=POOL budget 25 и текущем policy cap=10 нельзя честно рекомендовать больше без следующей сертификации.

## 6. Failure Analysis

Fail-closed условия должны остаться обязательными:

- truth unknown;
- convergence unknown;
- snapshot mismatch;
- atomic envelope mismatch;
- restore barrier invalid;
- approved plan lock mismatch;
- rollback packet missing;
- feedback path unavailable;
- healthy channel pool below floor.

Если любой пункт UNKNOWN или FAIL, batch должен стать 0.

## 7. Production Readiness

Текущая доказанная production readiness:

- 10-user autonomy certified;
- 25-user authority budget exists;
- dynamic advisory model exists;
- runtime gates already protect execution;
- full dynamic runtime authority not yet certified.

Поэтому готовность такая:

- ready_for_fixed_10_operation=true;
- ready_for_25_user_certification_review=true;
- ready_for_unbounded_dynamic_autonomy=false;
- ready_for_hybrid_model_design=true;
- ready_for_hybrid_model_implementation=false, пока не будет отдельного implementation/certification этапа.

## 8. Recommended Batch Strategy

Рекомендация:

1. Сейчас оставить текущий безопасный runtime ceiling=10.
2. Следующий execution stage: 25-user autonomy certification, потому что authority budget уже 25.
3. После 25-user certification внедрять hybrid model:
   - ladder/authority задаёт hard ceiling;
   - dynamic pool-aware расчёт предлагает desired size;
   - restore barrier/atomic/snapshot/rollback могут только уменьшить или остановить.
4. Для больших объёмов использовать порционное исполнение.

Практически:

- 23 пользователя сейчас: `10 + 10 + 3`, с verification/feedback/trust refresh между порциями.
- 40 пользователей сейчас: `10 + 10 + 10 + 10`, с проверкой между порциями.
- После 25-user certification:
  - 23 пользователя: до `23` одним batch, если все gates PASS;
  - 40 пользователей: `25 + 15`;
  - 100+ пользователей: по 25, пока не сертифицирован следующий потолок.

## 9. Final Verdict

Final verdict:

`HYBRID_RECOMMENDED`

Финальные флаги:

- existing_execution_batch_model=true
- authoritative_runtime_owner=`tools/v7-users-autoswitch`
- authoritative_policy_owner=`admin/v7-admin-api /api/actions/policy-update`
- dynamic_batch_sizing_exists=true
- dynamic_batch_sizing_runtime_authoritative=false
- fixed_batch_recommended=false
- ladder_recommended_as_certification_ceiling=true
- pure_percentage_recommended=false
- pure_dynamic_recommended=false
- hybrid_recommended=true
- current_safe_batch_ceiling=10
- current_authority_budget=25
- next_certification_target=25
- ready_for_25_user_autonomy_certification=true
- ready_for_unbounded_pool_autonomy=false

SAFE_NEXT_STEP:

`PROGRAM BA6 25 USER AUTONOMY CERTIFICATION AND HYBRID BATCH MODEL FOUNDATION`

