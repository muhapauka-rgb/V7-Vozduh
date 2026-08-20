# V5.3: fresh exact target revalidation

Дата: 2026-08-21 02:08 MSK  
Track: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Блок: fresh Matrix → target/certification context, read-only

## Результат

Существующий `v7-users-autoswitch --controlled-target-selection-diagnostic
--pretty` повторно прочитал свежие Matrix, quality, capacity и policy owners.
Диагностика завершилась без мутаций (`read_only=true`), но production T10–T11
не допущен.

| Проверка | Факт |
|---|---|
| Diagnostic status | `AUTO_ADMITTED_BY_EXISTING_STANDING_POLICY` |
| Matrix/quality observed | `2026-08-20T23:03:24Z` / `23:06:06Z` |
| Ranked controlled targets | `amneziawg-exec-20260528-10-8-1-14` |
| Selected exact target | пусто |
| Full-live admission | `false` |
| Controlled rebind | `true` для ranked target |
| Target health | `14/14`, `PASS_HEALTHY_BASELINE` |
| Target current-stage safe scope | `4` |
| Требуемый текущий этап | `5` |
| Current-stage feasible на ranked target | `false` |
| Multi-target authority | `false` |
| Runtime activation | `NOT_READY` |
| Candidate/Packet/Lease | не созданы |
| Users/routes | `0` / `0` |

## Почему это STOP_SAFE

Наличие здорового сервера само по себе не означает готовность переключения.
Existing selection law требует сначала full-live admission и exact current
action-class context. Сейчас diagnostic не выбрал exact target, а joint
allocation не проходит: доступен один controlled target с безопасным объёмом 4,
тогда как текущий campaign stage требует 5. Дополнительно отсутствует
current-campaign multi-target authority и runtime activation.

Глобальное поле `current_stage_feasible=true` в projection не отменяет этот
STOP_SAFE: оно относится к допустимому общему плану, а не к выбранному exact
target/action context.

## Неизменённые эффекты

- production users moved: `0`;
- route/routing mutation: `0`;
- candidate, packet, lease, restore barrier: `0`;
- policy/authority write: `0`;
- Matrix cadence, timeout, FAST и full fallback: unchanged;
- новый owner, Runtime, queue, watcher, registry или truth source: не создавались.

## Допустимое продолжение

Production branch остаётся `STOP_SAFE`, но это не останавливает инженерную
ветку. Тот же T10–T11 будет выполнен на изолированном Polygon synthetic
context с одним synthetic user и существующими owners; результат не получает
production credit и не меняет Authority. Повторная production revalidation
нужна после появления exact target/action-class context.

## Источники

- read-only diagnostic на `v7-vps`, выполнен 2026-08-21;
- свежий Matrix lifecycle из
  `2026-08-21_020500_v5_3_t0_t11_timing_breakdown_and_bottleneck.md`;
- existing selection law и standing policy projection из
  `tools/v7-users-autoswitch`.
