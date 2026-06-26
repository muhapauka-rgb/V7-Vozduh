# Engineering Report: A4 representative vs enumerative evidence audit

Status: COMPLETE
Language: Russian
Task: A4 representative evidence audit
Runtime mutation: NO
Apply executed: NO
Users moved: NO
Thresholds changed: NO
Formulas changed: NO
New owner created: NO
New backlog item created: NO
Architecture changed: NO

## Summary

Аудит проверил, что именно измеряет A4: репрезентативную готовность action class или перечисление конкретных user->candidate-channel вариантов.

Вывод:

A4 сегодня измеряет смешанную модель.

На уровне product/OMP intent A4 должен сертифицировать action class: `single-user governed candidate failover`.

На уровне текущего evidence calculation основная числовая метрика `candidate_count` является перечислением конкретных пар:

```text
candidate_key = (user, candidate_channel)
candidate_count = count(unique user -> candidate_channel keys)
missing_candidate_outcomes = candidate_count - consumed_outcome_keys
```

Поэтому текущая метрика ближе к enumeration coverage, чем к чистой representative action-class evidence.

## Action Performed

Выполнен read-only аудит существующих владельцев:

- `admin_core/intelligence_workers.py`
- `admin_core/autonomy_trust_acceleration.py`
- `admin_core/operator_execution_pipeline.py`
- `tools/v7-autonomy-trust-evidence-inventory`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/programs/V7_IMPLEMENTATION_BACKLOG.md`
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/product/V7_PRODUCT_SPECIFICATION.md`
- `docs/policies/POLICY_005_ACTION_CLASS_PROMOTION.md`

Запущен read-only inventory:

```text
tools/v7-autonomy-trust-evidence-inventory --action-class-runtime-only --pretty
```

Команда не выполняла apply, не двигала пользователей, не писала restore barrier и не включала runtime automation.

## Objective Observations

### 1. Что такое candidate_key

Точный владелец:

```text
admin_core/intelligence_workers.py::_candidate_keys
```

Текущая структура:

```text
candidate_key = (candidate_user, channel)
```

Это не пользователь сам по себе.

Это не канал сам по себе.

Это не action class.

Это конкретная пара:

```text
user -> candidate_channel
```

### 2. Почему candidate_count равен 156

`candidate_count` строится из `candidate-suitability-summary`.

Точный владелец:

```text
admin_core/intelligence_workers.py::build_candidate_suitability_snapshot
```

Модель:

```text
active_users = enabled users with user_ip
channels = available egress channels
for each active user:
    build candidate targets across available channels
candidate_count = unique user -> candidate_channel keys
```

Текущий A4-аудит ранее зафиксировал:

```text
candidate_count = 156
candidate_outcomes_consumed = 86
missing_candidate_outcomes = 70
coverage_ratio = 0.5513
```

`70` является текущим динамическим разрывом, а не постоянным числом.

### 3. Растет ли candidate_count при росте пользователей

Да.

Если увеличивается количество активных пользователей, а количество доступных candidate channels остается больше нуля, число user->channel ключей растет вместе с числом пользователей.

При 5,000 пользователях `candidate_count` может вырасти пропорционально:

```text
candidate_count ~= active_users * candidate_channels_per_user
```

С учетом фильтров availability/risk число может быть меньше полного произведения, но природа метрики остается перечислительной.

### 4. Что A4 фактически измеряет сегодня

A4 сегодня измеряет:

1. class-level readiness в Product/OMP смысле;
2. suitability evidence coverage через user->candidate-channel enumeration;
3. отсутствие synthetic evidence;
4. наличие/отсутствие real observed outcomes;
5. readiness blockers для runtime promotion.

Но главный числовой blocker `missing_candidate_outcomes=70` измеряет не репрезентативность класса как абстрактного поведения, а непокрытые конкретные пары user->candidate-channel.

## Engineering Conclusions

### Representative or enumerative

Текущая реализация:

```text
ENUMERATIVE_WITH_REPRESENTATIVE_INTENT
```

То есть:

- intention: сертифицировать action class;
- implementation: считает покрытие конкретных user->channel candidate variants.

### Does it scale

Как прямой обязательный критерий полного покрытия всех candidate keys модель не масштабируется до 5,000+ пользователей.

Причина:

```text
candidate_count grows with active users and available candidate channels
```

Если трактовать A4 как "закрыть все missing_candidate_outcomes", то A4 может стать практически невыполнимым на большом масштабе.

Если трактовать эту метрику как suitability knowledge signal, а не как единственный action-class promotion requirement, она полезна.

### Does it match OMP intent

Частично.

Соответствует:

- A4 требует real outcomes;
- A4 запрещает synthetic evidence;
- A4 не включает runtime automation;
- A4 не должен продвигать класс по одному успешному кейсу;
- A4 должен учитывать representativeness.

Не полностью соответствует:

- OMP/Product говорят про action-class promotion;
- текущий numeric blocker в основном считает user->candidate-channel enumeration;
- action class может быть коммерчески репрезентативно доказан без полного покрытия всех текущих user->channel пар.

### Commercial best-practice comparison

Зрелые production control planes обычно сертифицируют не все конкретные entity->target комбинации, а класс поведения внутри ограниченного blast radius:

- Kubernetes: readiness/liveness, rollout/canary, progressive rollout и rollback проверяют workload/class behavior, а не все pod-node комбинации как предварительное условие для каждой политики.
- AWS/control planes: используют policy boundaries, health gates, canary/ring/cell isolation, rollback и blast-radius controls; не требуют исчерпывающего перебора всех entity-placement вариантов.
- Cloudflare/traffic systems: используют POP/colo/cell/ring/canary evidence, health signals и guarded failover; конкретные flows помогают learning, но promotion строится вокруг класса действия и blast-radius.
- Google SRE: требует representative signals, gradual rollout, rollback, error budgets и post-action learning; не требует full enumeration как универсальный критерий готовности.

Коммерческий паттерн:

```text
action-class evidence
+ representative sample
+ risk segmentation
+ blast radius
+ rollback
+ verification
+ freshness
+ learning
```

а не:

```text
all current user -> candidate-channel pairs must be observed
```

## Impact

Engineering Maturity: unchanged at `100.0%`.

Production Maturity: unchanged at `24.0%`.

Runtime behavior: unchanged.

Runtime automation: still disabled.

Authority: unchanged.

Users moved: `0`.

No formulas, thresholds, code, backlog items, runtime paths, owners, or architecture were changed.

## Capability Progress

Current relevant capability progress remains:

| Capability | Progress |
| --- | ---: |
| Learning | `40.0%` |
| Authority Evolution | `40.0%` |
| Production Readiness | `24.0%` |
| Production Autonomy | `0.0%` |
| Movement Protection | `35.7%` |

A4 remains incomplete because production-grade action-class evidence is still insufficient.

## Backlog Progress

| Scope | Progress |
| --- | ---: |
| Tier A | `3 / 6` = `50.0%` |
| Tier B | `0 / 21` = `0.0%` |
| Tier C | `0 / 7` = `0.0%` |
| Overall actionable | `3 / 34` = `8.8%` |

Current backlog item:

```text
A4: Materialize representative outcome evidence for the first action class.
```

## Production Maturity

| Dimension | Current |
| --- | ---: |
| Engineering Maturity | `100.0%` |
| Production Maturity | `24.0%` |
| Production remaining | `76.0%` |
| Autonomy tier | `TIER_1_GOVERNED` |

## Canonical Knowledge

Durable knowledge discovered:

A4 must not be interpreted as requiring full enumeration of every user->candidate-channel pair as the permanent certification model for action-class promotion.

The current candidate coverage model remains useful as a suitability knowledge signal, but production-grade autonomy should certify action classes through representative evidence, risk segmentation, rollback/no-rollback proof, blast-radius history, freshness, anti-flap, verification, and learning.

Canonical owner updated:

```text
docs/reference/V7_CANONICAL_REFERENCE.md
```

No new owner was created.

Need New Owner:

```text
FALSE
```

Need New Backlog Item:

```text
FALSE
```

Architecture Extension:

```text
NO
```

## Evidence

Code evidence:

```text
admin_core/intelligence_workers.py::_candidate_keys
admin_core/intelligence_workers.py::build_candidate_suitability_snapshot
admin_core/intelligence_workers.py::build_candidate_outcome_rows
admin_core/autonomy_trust_acceleration.py::build_candidate_outcome_reality_collection
admin_core/autonomy_trust_acceleration.py::_promotion_missing_evidence
```

Current key formula:

```text
candidate_keys = set((candidate_user, channel))
consumed_keys = observed outcomes keyed by (user, channel)
missing_keys = candidate_keys - consumed_keys
missing_candidate_outcomes = len(missing_keys)
coverage_ratio = len(consumed_keys) / len(candidate_keys)
```

Existing owner mapping:

| Finding | Existing owner |
| --- | --- |
| Action-class promotion evidence | `POLICY_005_ACTION_CLASS_PROMOTION`, OMP, A4 |
| Candidate outcome coverage | `admin_core/autonomy_trust_acceleration.py`, `admin_core/intelligence_workers.py` |
| Runtime enablement recommendation | `tools/v7-autonomy-trust-evidence-inventory` |
| Runtime eligibility arbitration | Existing backlog item `A6` |
| Metric reliability / promotion confidence | Existing backlog item `B13` |

## Minimal Recommendation

Do not implement now.

Do not lower thresholds.

Do not change formulas.

Do not create a new owner.

Do not create a new backlog item.

Map the finding to existing owners:

```text
A4 -> clarify representative action-class evidence semantics
A6 -> runtime eligibility arbitration should consume class-level evidence, not raw enumeration alone
B13 -> metric reliability should prevent over-weighting enumeration coverage as promotion proof
POLICY_005 -> action-class promotion remains the canonical policy owner
```

Minimal future correction, if implementation is later selected through OMP:

```text
Extend existing A4/A6/B13 owners so candidate_count remains a suitability signal,
while action-class certification uses representative class evidence and risk segmentation.
```

## Re-audit Rule

Do not re-audit this finding unless one of these changes:

- candidate suitability snapshot owner changes materially;
- candidate outcome matcher changes materially;
- action-class promotion owner changes materially;
- runtime eligibility arbitration begins consuming candidate_count as a hard promotion gate;
- production evidence disproves the current interpretation;
- explicit operator request.

