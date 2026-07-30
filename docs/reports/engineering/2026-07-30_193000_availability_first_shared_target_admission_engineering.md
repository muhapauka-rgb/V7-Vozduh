# Engineering Report: availability-first shared-target admission

Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission: `BOUNDED_AVAILABILITY_FIRST_CONTROLLED_FAILOVER_AND_PROGRESSIVE_LADDER_V1`  
Scope in this change: read-only availability classification and bounded
technical-capacity projection only.

## Итог

Исправлен конкретный semantic gap существующего shared-target owner: попадание
ниже normal stability floor больше не отождествляется с hard failure и нулевой
технической capacity. Normal production floor не менялся.

Во время production read-only caller обнаружен и устранён второй owner-link
defect: к shared destination ошибочно применялся strict baseline controlled
source. Этот baseline нужен только для канала, который V7 может намеренно
деградировать и затем восстанавливать. Для non-destructive destination теперь
используется existing Planner profile-aware service suitability; genuine hard
Planner blockers, reserve, verification, containment, freshness и
source=target collision по-прежнему fail closed.

Во втором production-read-only проходе обнаружен и закрыт третий
producer-consumer defect: allocation строилась по historical campaign source,
а фактический controlled source исключался только после выбора target. Поэтому
`vless` мог ложно участвовать в denominator capacity, хотя позже та же
topology-проекция фиксировала collision. Теперь existing allocation owner
получает actual controlled source как explicit exclusion до ranking и stage
allocation; историческая проекция сохранена только для диагностики.

Новая compact projection различает:

- `HEALTHY` — normal admission, существующая reserve capacity;
- `DEGRADED_USABLE` — свежие sustained positive measurements при soft quality
  deviation; максимум одна certification identity до реального Outcome;
- `LAST_RESORT_USABLE` — только current positive measurement, также максимум
  одна identity и отдельный exact policy boundary;
- `DEGRADED_OBSERVATION_INSUFFICIENT` — hard failure не доказан, но данных для
  emergency allocation недостаточно;
- `HARD_INELIGIBLE` — source=target, reachability, reserve/capacity,
  verification, containment, freshness либо иной hard owner-backed gate failed.

`DEGRADED_USABLE` и `LAST_RESORT_USABLE` не являются execution admission. Они
не создают Candidate, Packet, lease, restore barrier, policy write, routing,
user movement или Production Maturity effect. Единственный возможный дальнейший
шаг — exact existing standing-policy Authority contract, затем полностью fresh
planner generation.

## Reuse and extension

Использованы существующие Matrix, quality, service reachability,
capacity/reserve, Planner ranking, controlled-topology, policy, verification,
rollback/containment и Polygon contract owners. Не создано новых owners,
registries, queues, schedulers или Runtime paths.

Projection теперь публикует availability-first stages `1`, `2` и все stages
уже существующей campaign. Multi-target allocation использует только
`target_safe_additional_capacity`, а не raw hard limit. Обычные assignments и
routes остаются неизменяемыми, target fault injection запрещён.

Если после такого re-projection доступен ровно один
`DEGRADED_USABLE`/`LAST_RESORT_USABLE` target, CPS получает точный
`ENGINEERING_AUTHORITY_EXACT_DEGRADED_SHARED_TARGET_ACTION_CLASS_CONTRACT_REQUIRED`.
Это не заменяет и не расширяет campaign `5→10→25→48`: контракт может разрешить
только последующую fresh planner revalidation для одной availability-first
identity. Candidate, Packet, lease, restore barrier и production effect до
отдельной реальной admission не создаются.

Production caller также выявил и этот terminal через фактическую fresh
generation: `awg3` оказался `DEGRADED_USABLE`, тогда как `vless` был исключён
как actual source. В той же ветке старый fallback ошибочно публиковал
`EXTERNAL_RESOURCE_REQUIRED:NONE`. Он заменён на один непротиворечивый durable
successor
`ENGINEERING_AUTHORITY_REQUIRED:EXACT_DEGRADED_SHARED_TARGET_ACTION_CLASS_CONTRACT`.
Это закрывает потерю causal consumer: Authority boundary теперь имеет точный
producer и не маскируется под отсутствие внешнего ресурса.

При первом атомарном CPS reconciliation тот же production result корректно
остановился: legacy bridge не считал этот новый Engineering Authority frontier
внешним input и отказался создавать противоречивый CPS. Bridge расширен через
существующие CPS/OMP поля — stop, external-input type, next consumer, terminal
и re-entry. Никакая новая очередь, registry или Authority system не создана.

## Verification before deploy

- focused unit tests: `test_service_failure_automation_evolution`,
  `test_operator_execution_packet`, `test_omp_live_state_pointer_consistency`;
- syntax compilation: `tools/v7-users-autoswitch`;
- `git diff --check`.

All focused checks passed. Existing legacy `DeprecationWarning` in
`tools/v7_sync_lib.py` remains unrelated.

## Exact next step

Deploy this narrow runtime-owner change through `tools/v7-safe-deploy`, invoke
the production read-only topology diagnostic, and classify the actual target
set. If at least one distinct target is `DEGRADED_USABLE` or
`LAST_RESORT_USABLE`, produce the exact existing Authority frontier only. If
none is usable, retain an owner-backed capacity-substrate boundary instead of
repeating diagnosis or manufacturing production evidence.
