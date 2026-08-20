# V5.3: production STOP_SAFE и Polygon T10–T11 продолжение

Дата: 2026-08-21 02:10 MSK  
Track: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`

## Что выполнено

После свежего production Matrix cycle выполнены два независимых действия:

1. existing read-only target diagnostic повторно проверил exact
   source/target/certification context;
2. изолированный Polygon fixture выполнил один governed synthetic T10–T11.

Эти ветки не смешивались: production branch осталась `STOP_SAFE`, synthetic
branch дала engineering evidence без production credit.

## Production branch

Fresh diagnostic увидел здоровый controlled target
`amneziawg-exec-20260528-10-8-1-14` (`14/14` сервисов), но не создал exact
selection:

- `selected_target_id` пуст;
- `full_live_admission=false`;
- `current_stage_feasible=false` на ranked target;
- safe scope target: `4`, требуемый текущий stage: `5`;
- `current_campaign_multi_target_authority=false`;
- `runtime_activation=NOT_READY`;
- candidate/packet/lease/route mutation/users moved: `0`.

Причина: действующий selection law не позволяет считать просто здоровый сервер
готовым к действию без exact action-class context и достаточного scope.
Production T10–T11 поэтому не запускался.

## Polygon T10–T11

В существующем временном fixture использованы текущие owners
Planner → Packet → Lease → restore barrier → apply/verification →
Feedback/Closure. Synthetic user: `10.7.0.5`, source `vless`, target `awg3`.

| Проверка | Результат |
|---|---|
| Final verdict | `GOVERNED_TRANSACTION_COMPLETED` |
| Fresh packet | `pkt_preview_test` |
| Lease | `EXECUTION_FINISHED` |
| Restore barrier | записан внутри fixture |
| Apply/verification | PASS, только stub в temp fixture |
| Closure records | `1` |
| Safe Mode | `OPEN` |
| Authority expanded | `false` |
| Runtime automation enabled | `false` |
| Synthetic users moved | `1` внутри fixture |
| Production users/routes | `0` / `0` |

Timing из существующего governed transaction receipt:

| Этап | Время |
|---|---:|
| planner | `11.188 ms` |
| packet and lease | `5.964 ms` |
| restore barrier | `3.877 ms` |
| apply and verification | `0.079 ms` |
| feedback and learning | `3.105 ms` |
| **итого** | **`24.212 ms`** |

Clock: `time.monotonic_ns`; новая timing-база не создавалась. Прогон не
подтверждает реальное перемещение production-клиента и не заменяет live
route/traffic verification.

## Safety conclusion

- production Matrix/timer/timeout/cadence/FAST unchanged;
- ordinary clients и маршруты не затронуты;
- Authority не расширялась;
- full Matrix fallback сохранён;
- неизвестный или неполный exact context продолжает блокировать production
  action.

## Позиция и следующий шаг

Polygon T10–T11 для одного synthetic user выполнен. В исходном V5.3 T0–T11
track ещё не доказаны natural production T0 и real traffic recovery.

Следующий шаг: существующий OMP/CPS owner должен потребить свежий diagnostic
результат и получить exact action-class context либо явно оставить
production `STOP_SAFE`; после появления такого контекста повторить bounded
one-user governed exercise с текущими guards. До этого новые production
действия не выполняются.

## Источники

- read-only `v7-users-autoswitch --controlled-target-selection-diagnostic`
  на `v7-vps`;
- существующий `tools/v7-governed-canary-dry-run-cycle` в temp Polygon fixture;
- timing receipt из текущего governed transaction;
- отчёты `2026-08-21_020500_v5_3_t0_t11_timing_breakdown_and_bottleneck.md` и
  `2026-08-21_020800_v5_3_exact_target_revalidation_stop_safe.md`.
