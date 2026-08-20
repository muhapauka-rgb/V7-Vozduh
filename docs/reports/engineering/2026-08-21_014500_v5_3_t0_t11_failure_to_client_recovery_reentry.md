# V5.3 T0–T11: возврат от свежего Matrix к цепочке переключения клиента

Дата: 2026-08-21 01:45 MSK  
Track: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Логический блок: failure cause → Matrix → target selection → safe re-entry  

## Зачем ожидался Matrix

Matrix нужен не сам по себе. Его задача в T0–T11 — дать свежую доказательную
картину причины отказа и пригодности каналов, чтобы не переключать клиента по
старым или противоречивым данным:

```text
T0 failure observed
  → Matrix подтверждает источник и сервисный scope
  → Planner выбирает допустимый target
  → создаются Candidate → Packet → Lease → Barrier
  → выполняется Apply
  → проверяются маршрут и клиентский трафик
  → T11 traffic recovered
```

Timer и Matrix не принимают решение о перемещении сами. Они поставляют свежий
state существующему Planner/OMP/CPS владельцу.

## CURRENT FRESH MATRIX

Новый production Matrix cycle завершён:

- start `01:31:39 MSK`;
- finish `01:32:44 MSK`;
- exit code `0`;
- duration около `65 s`;
- 7 egress rows, 14 service probes на row;
- общий lifecycle `OK`, 6 rows OK;
- `vless`: `WARN`, 13/14 сервисов не прошли;
- egress `1`: `FAIL`, 14/14 сервисов не прошли;
- Matrix state и summary обновлены;
- consumer read-only diagnostic прочитал свежий state.

## FAILURE CAUSE AND SCOPE

Fresh target-selection diagnostic показал:

| Канал | Matrix health | Service result | Ordinary scope | Решение |
|---|---|---:|---:|---|
| `vless` | `STOP_SAFE_BASELINE_UNHEALTHY` | 1 reachable / 13 failed | обычный scope отсутствует; certification-only | не переключать |
| `1` | `STOP_SAFE_BASELINE_UNHEALTHY` | 0 reachable / 14 failed | ordinary target admission отсутствует | не переключать |
| `awg0` | `PASS_HEALTHY_BASELINE` | 14/14 | ordinary eligible, но нет exact transaction context | не выбран |
| `awg3` | `PASS_HEALTHY_BASELINE` | 14/14 | ordinary eligible, но нет exact transaction context | не выбран |
| `amneziawg-exec-20260528-10-8-1-14` | `PASS_HEALTHY_BASELINE` | 14/14 | controlled-only, authority отсутствует | не выбран |

Это подтверждает причину отсутствия переключения: Matrix видит service-level
failures, но текущий state не связывает их с обычным затронутым клиентом и не
содержит действующего exact authority/request для controlled synthetic action.

## EXACT TARGET CONTEXT

Read-only consumer result:

- `read_only=true`;
- `selected_target_id=""`;
- `full_live_admission=false` для всех текущих target rows;
- `candidate_packet_lease_created=false`;
- `routing_mutation=false`;
- `user_movement=0`;
- `authority_status=NONE`;
- request id/hash/status пустые;
- ordinary autoswitch service `inactive (dead)`.

Existing target-selection owner не выбрал запасной канал, потому что отсутствует
законный client-scoped transaction context. Это корректный `STOP_SAFE`, а не
ошибка Matrix.

## T0–T11 CURRENT MAP

| Шаг | Состояние сейчас | Почему |
|---|---|---|
| T0 failure | не сформирован для ordinary client | нет owner-backed ordinary affected scope |
| T1 Matrix observation | PASS | fresh generation и service evidence есть |
| T2 source/scope confirmation | certification-only / empty ordinary scope | текущий failure не привязан к ordinary client |
| T3 decision | STOP_SAFE | нет exact legal input для решения |
| T4 Candidate | не создан | target/context gate не пройден |
| T5 Packet | не создан | Candidate отсутствует |
| T6 Lease | не создан | Packet отсутствует |
| T7 Barrier | не создан | Lease отсутствует |
| T8 Apply | не выполнялся | production mutation запрещена текущими gates |
| T9 route effect | не наблюдался | Apply не выполнялся |
| T10 client verification | не выполнялась | нет client movement |
| T11 traffic recovered | не заявляется | реального переключения не было |

## GOVERNED SYNTHETIC DRY-RUN

В этом блоке dry-run не запускался. Причина доказана read-only diagnostic:

`NO_CURRENT_EXACT_CERTIFICATION_CONTEXT`

Создание нового authority/request, synthetic identity, Candidate или Packet для
обхода этого gate запрещено scope текущего track. Polygon evidence не повышается
до production evidence.

## RUNTIME AND PRODUCTION EFFECT

- Timer и Matrix service не изменялись.
- Cadence и timeout не изменялись.
- FAST не включался.
- Autoswitch не запускался.
- Клиенты не перемещались.
- Маршруты не менялись.
- Candidate/Packet/Lease/Barrier не создавались.
- Runtime mutation: `NONE`.

## NEXT STEP IN T0–T11

Свежий Matrix блокер снят. Следующий законный шаг — получить от существующего
failure/CT-M0F owner новый owner-backed input одного из двух видов:

1. реальный ordinary failure с непустым affected client scope; или
2. действующий exact certification request и online-capable synthetic context.

После этого повторяется T2 target revalidation и, только при прохождении gates,
один governed synthetic-client dry-run. До появления такого input нельзя
создавать искусственный T0 или двигать обычного клиента.

## CHECKS

- Fresh Matrix live service/journal/state checks: PASS.
- Existing target-selection diagnostic: `read_only=true`, `candidate_packet_lease_created=false`.
- Ordinary autoswitch service: inactive.
- Local truth check: PASS.
- Production mutation: `NONE`.

