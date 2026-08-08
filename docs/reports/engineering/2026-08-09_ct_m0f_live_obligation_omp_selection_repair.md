# CT-M0F: repair выбора живого obligation и доставки OMP receipt

Дата: 2026-08-09  
Статус: `DEPLOY_REQUIRED_THEN_NEXT_ORDINARY_MATRIX_REVALIDATION`

## Что подтвердил штатный Matrix-цикл

Штатный `v7-service-matrix-refresh.timer` завершил вызов без systemd-ошибки,
но CT-M0F вернул `STOP_SAFE_NO_SAMPLE_ADMITTED` с
`ct_m0f_service_failure_causal_binding_invalid`. Действие, Packet, lease и
маршрутизация не выполнялись.

Read-only production reconciliation после цикла подтвердила живой
accounted VLESS incident: один source, `affected_scope=35`,
`unresolved_scope=35`, fresh passive event, obligation и selector
`CT_M0F_STANDING_CONTROLLED_FAILURE_READY`. Поэтому это не Authority,
не отсутствие target и не terminal канала.

## Корневая причина

В existing `closure-records` owner были одновременно:

1. живой VLESS obligation с accounted unresolved source scope;
2. более новые исторические zero-scope STOP_SAFE obligations.

`service_failure_automation_frontier()` выбирал pending запись только по
timestamp. Такой zero-scope terminal мог быть передан OMP вместо живого
incident. Дополнительно Matrix запускал OMP consumer только после успешного
advisory refresh. Если этот read-only refresh упирался в прежний 45-second
timeout, уже durable живой obligation оставался без `OMP_CONSUMED` receipt.
Governed executor в таком состоянии корректно fail-closed: не разрешает
создать Packet для causal binding без exact OMP receipt.

## Исправление существующих owners

- `tools/v7_sync_lib.py`: existing closure owner теперь сначала выбирает
  `ACCOUNTED` obligation с `unresolved_scope_count > 0`; timestamp остаётся
  только детерминированным tie-breaker. Новый registry не создан.
- `tools/v7-service-matrix-refresh-all`: advisory reconciliation получает
  bounded 90-second budget; OMP exact-once consumer вызывается после
  успешного passive consumer и при timeout advisory тоже. При отсутствии
  pending obligation он возвращает свой прежний безопасный
  `NO_PENDING_OBLIGATION`.
- Новый unit test доказывает, что более новый historical zero-scope terminal
  не может вытеснить accounted live VLESS scope.

## Проверка

`119` targeted tests passed:

- frontier prioritisation;
- CT-M0F reset/re-entry contract;
- governed canary CLI guards.

## Второй выявленный residual и его закрытие

Первый post-deploy ordinary Matrix caller подтвердил исправленный
`passive -> advisory -> OMP receipt` путь. Затем CT-M0F честно остановился на
`AMBIGUOUS_ACTIVE_SERVICE_FAILURE_BINDING`: несколько re-observation одного
и того же VLESS failure generation оставались отдельными открытыми compact L3
records.

Это не несколько action opportunities. Добавлена read-only semantic
coalescing rule existing L3 selector:

- допустимо выбрать только самый свежий record, когда все contenders имеют
  один `incident_generation` и один current scope fingerprint;
- выбранный record обязан иметь exact `OMP_CONSUMED` receipt для своего
  `obligation_id + source_incident_id`;
- разные generation или scope остаются `AMBIGUOUS...` и fail-closed.

Новые focused tests доказывают оба случая. Это не объединяет исторические
records и не переписывает L3 history; правило существует только на границе
текущего selector consumer.

## Границы безопасности

Изменение не выдаёт Authority, не меняет policy, не создаёт Candidate/Packet/
lease само по себе и не выполняет routing mutation, user movement, rollback,
Stage-48 credit или изменение Production Maturity.

## Точный successor

После minimal safe deploy следующий **обычный** Matrix generation обязан:

`accounted live VLESS obligation -> exact-once OMP receipt -> CT-M0F causal
revalidation -> fresh Candidate/Packet/lease only if all existing live gates
still pass -> one bounded certification-only cutover -> Time lineage`.

Если любой live gate изменился, ожидаемый терминал — exact `STOP_SAFE` с
durable ordinary-timer re-entry, а не повторное использование старого Packet
или sample.
