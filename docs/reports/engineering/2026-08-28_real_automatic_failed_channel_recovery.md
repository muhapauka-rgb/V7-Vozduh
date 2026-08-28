# V7 — реальное автоматическое восстановление клиента после отказа канала

Дата: 2026-08-28  
Объект: текущая `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM`  
Клиент: Лиза (`10.7.0.125`)

## Цель

Проверить и восстановить реальный путь `обнаружение отказа канала → выбор
здорового канала → governed apply → проверка`, чтобы клиент переключался самой
системой, без ручного переноса через Codex.

## Состояние до исправления

- Лиза находилась на `vless`.
- Matrix зафиксировал продолжающийся отказ исходного канала:
  `sfinc_cf3f65f71454a5ad2dbfa5f8e77b4b34`.
- Автоматический потребитель доходил до `STOP_SAFE` и не создавал допустимое
  изменение маршрута.

## Найденные причины

1. Проверки готовности целевых сервисов и фоновые проверки могли не успеть
   обновить доказательства для выбора цели.
2. Контекст отказа сервиса терялся между Matrix и governed apply; downstream
   путь видел операцию как неподходящую для обычного service-failure recovery.
3. Устаревший execution lease/preview блокировал повторное принятие операции.
   Он был закрыт штатным владельцем lease, без редактирования state-файлов.
4. После восстановления свежих доказательств оставался конфликт между
   аварийным eligibility-контрактом и обычным отказом сервиса. Исправлен только
   scoped-путь для `ordinary_service_failure_context`; широкое исключение,
   ослабляющее safety-gates, было отклонено safe-deploy и не попало в Runtime.

## Изменения

В текущем дереве и Runtime опубликованы:

- `7ccf2654` — сохранение контекста service failure в governed apply;
- `52ec86c1` — передача контекста во второй фактический apply-путь;
- `cf76c7ea` — scoped eligibility только для ordinary service-failure;
- `2c5c449d` — прямое использование свежих Matrix-доказательств отказа
  источника, готовности цели и обязательных сервисов.

Safe-deploy прошёл для финального commit `2c5c449d045b8bb6c3339b37b57649e9507c88c7`.
Никаких новых owner, timer, registry или источника истины не добавлено.

## Проверки

- focused autoswitch/governed pipeline: `423 PASS`;
- дополнительный health fast-deadline набор: `19 PASS`;
- governed canary + operator pipeline: `204 PASS`;
- `v7-health.service`: `active`;
- локальный и Runtime SHA-256 для `v7-users-autoswitch`:
  `4462ebd98f93491e3fdc517321230b2a40239f0325fc4e4ee7091bfd5950e51a`;
- локальный и Runtime SHA-256 для
  `v7-governed-canary-dry-run-cycle`:
  `9d4c2acf9ebe65423d50554a3a5fbd4b5ee9bb09081a72ddd946a9e1ffa7684c`.

## Реальный автоматический результат

Операция: `runtime_autoswitch_a478c4092e5a26b6a43e00be`  
Источник: `vless`  
Цель, выбранная системой: `awg0`  
Наблюдение: `2026-08-28T10:53:49.987802+00:00`

Durable execution receipt:

- `terminal_state=APPLIED`;
- `terminal_reason=selected_moves_applied`;
- `outcome_status=success`;
- `verification_result.success=true`;
- exact route check: `V7_SCOPED_USER_ROUTE_CHECK=OK`;
- required-service verification: `status=ok`;
- rollback: `NOT_REQUIRED`;
- `users_moved=1` — только Лиза;
- обычные пользователи не затронуты;
- активный execution lease после завершения отсутствует (`EXECUTION_FINISHED`).

Текущее состояние registry:

```text
ip=10.7.0.125 current=awg0 table=1123 enabled=1
```

Цепочка фактически прошла через существующие владельцы:

```text
Matrix incident
→ existing service-failure consumer
→ Planner/target eligibility
→ Candidate/Packet/Lease/Barrier
→ existing v7-user-switch
→ exact route/kernel verification
→ required-service verification
→ durable success receipt
```

Codex не выполнял ручной `v7-user-switch` и не выбирал цель вручную.

## Ограничения и вывод

Автоматический путь отказа канала для реального клиента доказан end-to-end на
Лизе. Это закрывает текущий дефект lifecycle/eligibility, а не утверждает, что
каждый канал и каждый сервис всегда здоров: отдельные Matrix-пробы могут
показывать частичную деградацию и должны оставаться основанием для fail-closed.

## Положение в плане и следующий шаг

Логический блок восстановления автоматического переключения завершён.
Следующий шаг программы — Polygon-регрессия того же existing-owner пути на
другом отказавшем канале (без ручной подстановки цели), затем проверка
группового/N10-контракта. До этого не менять маршруты вручную и не ослаблять
Matrix/Authority safety-gates.
