# CT-M0F: repair active-incident causal binding

## Факт

Обычный `v7-service-matrix-refresh.timer` запустил Matrix и выполнил одну
certification-only транзакцию. Route и service verification завершились
успешно, однако CT-M0F отказался засчитать latency sample:
`CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_INVALID`, blocker
`incident_id_missing`.

Это не отказ сети и не отсутствие Authority. Matrix selector не передал
current passive service-failure obligation/incident/scope binding в
CT-M0F governed execution. Поэтому Packet и Outcome feedback не имели
incident lineage; текущий scope остался `39 != 0 + 38 + 0`.

## Минимальный ремонт существующих owners

- `v7-users-autoswitch` читает единственный active accounted passive incident
  как компактную selection projection. Для реального source без точного
  binding дальнейшее выполнение теперь STOP_SAFE; controlled-condition путь
  не изменён.
- Matrix передаёт exact obligation, incident, source-scope fingerprint и
  incident generation в существующий governed CT-M0F executor.
- Governed executor повторно валидирует тот же durable binding до Packet,
  переносит его в Packet, child autoswitch и Outcome feedback.
- Historical CT-M0F certification outcomes без current event binding не могут
  уменьшать новый live denominator. Они остаются immutable history; только
  следующий Packet с exact current event/scope binding может быть потреблён
  как protection. Это исключает смешение нескольких Matrix generations.

## Проверка

Focused tests: 357 PASS (`test_service_failure_episode`,
`test_v7_users_autoswitch_policy`, `test_governed_canary_cli`).

Production postflight: safe deploy manifest изменил только три нужных tools,
последняя точечная коррекция — только `v7-users-autoswitch`; passive causal
reconciliation прошёл без forbidden effects. Current selector вернул
`CT_M0F_STANDING_CONTROLLED_FAILURE_READY`: active binding корректен,
есть fresh certification identity и healthy shared target с zero
ordinary-user delta. Production truth и convergence: PASS; local/GitHub/
production runtime fingerprints совпадают.

## Следующий consumer

После safe deploy штатный read-only passive causal reconciliation должен
восстановить accounted active scope. Следующий обычный Matrix timer обязан
создать свежий generation и провести новую CT-M0F sample по связанной
Matrix → binding → Packet → feedback линии. Manual Matrix запуск не является
доказательством и не выполняется. CT-M0F остаётся незавершённой до valid
user-path latency sample и выполнения её SLO.
