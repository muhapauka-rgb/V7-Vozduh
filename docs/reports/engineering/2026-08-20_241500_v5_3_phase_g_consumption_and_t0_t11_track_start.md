# V5.3: потребление Phase G и старт T0–T11 latency track

**Дата:** 2026-08-20 (MSK)
**Логический блок:** закрытие текущего Phase G через существующий OMP/CPS и переход в уже интегрированный track `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`.

## Итог

Phase G корректно закрыт. Решение: `NO_CROSS_EGRESS_PARALLELISM_ADMITTED`.
Параллельно проверять несколько серверов не стали: на полигоне возможный выигрыш
не повторился, а нагрузка выросла. Полная Matrix остаётся основным безопасным
режимом, subset — сравнительной проверкой, automatic FAST — на удержании.

Существующий атомарный OMP/CPS consumer записал это решение и перевёл текущий
фронтир в существующий V5.3 T0–T11 track. Это не новая Program, Mission,
owner, Runtime или архитектура.

## Phase G: доказанный результат

Источник: [2026-08-20_233000_v5_3_phase_g_cross_egress_polygon_measurement.md](2026-08-20_233000_v5_3_phase_g_cross_egress_polygon_measurement.md).

| Cap | Результат полигона | Вывод |
| --- | --- | --- |
| 1 | стабильный serial baseline | сохранить |
| 2 | два быстрых запуска, затем медленнее serial | выгода не воспроизводится |
| 4 | выше давление и нет устойчивого выигрыша | не допускать |

Во всех контролируемых прогонах сохранены один Matrix writer, отсутствие
производственного события, маршрутов и движения клиентов. Поэтому решение не
«отложить параллельность», а именно **не допустить её как оптимизацию** до
нового доказанного invalidator.

## CPS transition

Существующий `tools/v7-truth-check` получил узкую команду
`--reconcile-v5-3-phase-g-to-t0-t11`. Она расширяет только существующий
OMP/CPS atomic reconciliation owner и принимает переход лишь когда:

1. текущий CPS действительно находится на активном Phase G frontier;
2. отчёт Phase G подтверждает `PASS; NO_CROSS_EGRESS_PARALLELISM_ADMITTED`;
3. Program уже содержит интегрированный T0–T11 track;
4. начальный T0–T11 evidence report существует.

Фактический результат вызова:

```text
ATOMIC_CPS_UPDATE_APPLIED
post_write_reread = PASS
OMP_POINTER_ATOMIC_UPDATE_APPLIED
```

Новая projection CPS:

| Поле | Значение |
| --- | --- |
| текущий scope | `V5_3_T0_T11_LATENCY_OPTIMIZATION` |
| текущий frontier | `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION` |
| решение Phase G | `NO_CROSS_EGRESS_PARALLELISM_ADMITTED` |
| реализация Phase G | `REJECTED_NO_RUNTIME_ADMISSION` |
| FAST | `HOLD_PENDING_EXPLICIT_PHASE_H_ADMISSION` |

Повторная проверка Continue OMP вернула `PASS` и выбрала
`V5_3_T0_T11_LATENCY_TRACK_PREEMPTS_GENERIC_OMP`; настоящий caller —
`continue_omp_engineering_control_loop`, consumer — существующие
Health/Test/Stability owners.

## Старт T0–T11 track

Track не начинает исследование заново. Его стартовым доказательством является
[2026-08-20_235500_v5_3_t0_t11_latency_trace_and_safe_optimization_register.md](2026-08-20_235500_v5_3_t0_t11_latency_trace_and_safe_optimization_register.md).
В нём уже построены:

- статическая/Polygon карта T0–T11;
- семь классов сбоев;
- разделение signal → confirmation → decision → action;
- роли Matrix/Telegram/quality/verification;
- начальные root contributors и safe optimization register.

### Известно

- Telegram даёт раннее подозрение примерно по 4-секундному timer, но не
  переключает пользователя сам.
- Full Matrix запускается по 15-минутному циклу с jitter до минуты и остаётся
  fallback/diagnostic contour.
- Persistence, freshness, readiness резерва и post-switch verification имеют
  защитный смысл и не считаются «лишней задержкой» без измерения.
- Short→full comparison уже проверен на полигоне без движения клиентов.

### Пока неизвестно

- реальные production распределения времени T0–T11;
- вклад очереди/ожидания Matrix writer в живом инциденте;
- доля задержки между decision-ready, action и подтверждённым восстановлением
  конкретного клиента.

Причина честной неопределённости: read-only Runtime проверка ранее обнаружила
несовпадение локального и установленного commit. Это не повод менять Runtime
в данном блоке и не позволяет выдавать Polygon или конфигурационные интервалы
за live-метрики.

## Проверки

```text
tests.unit.test_v5_3_matrix_decision_lifecycle_binding: 8/8 PASS
```

Проверка покрывает отказ при неверном CPS/frontier, обязательные отчёты,
атомарную запись, сохранение FAST hold, запрет Runtime-mutation и распознавание
нового track существующим Continue OMP.

## Эффекты и ограничения

| Область | Эффект |
| --- | --- |
| CPS/OMP lifecycle | изменён: Phase G consumed → T0–T11 track active |
| Matrix / autoswitch / cadence | не изменены |
| Runtime / production | без эффекта |
| Маршруты / пользователи | без эффекта |
| Архитектурный выбор | не выполнялся |
| FAST | не включался |

## Текущая позиция и точный следующий шаг

**Позиция в общем плане:**

```text
Phase G controlled validation — завершён и consumed
→ L1–L6 T0–T11 evidence — начаты и частично уже доказаны static/Polygon
→ Runtime evidence reconciliation — следующий подшаг
→ problem-to-pattern comparison
→ architecture decision only if a proved gap remains
```

**Точный следующий подшаг внутри текущего CPS frontier:** получить через
существующего Runtime owner только read-only timing snapshot уже имеющихся
T0–T11/performance spans. Не создавать сбой, не менять таймеры, не трогать
маршруты и не переключать клиентов. Если согласованной Runtime-версии нет,
сохранить это как `UNKNOWN` и продолжить только независимые static/Polygon
доказательства; это не разрешает переходить к FAST или архитектуре.
