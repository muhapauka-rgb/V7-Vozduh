# V7 Production Ordinary Failover Authority Activation — reconciliation report

Дата: 2026-08-29 (MSK)  
Mission: `V7_PRODUCTION_ORDINARY_FAILOVER_AUTHORITY_ACTIVATION`  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Выполнено: свежая сверка CPS/OMP/Program/Runtime, владельцев Matrix/Planner/Authority, VLESS и фактического контура автоматического failover.

## Итог

Миссия остановлена на точной границе Authority/production contract. Код, политика, маршруты и назначения пользователей не менялись.

Текущая система умеет автоматически обнаружить проблему VLESS и сформировать governed решение, но не имеет действующего разрешения на перемещение обычных пользователей. Текущий delegated policy разрешает только certification/controlled операции; `ordinary_assignment_mutation_allowed=false`. Автоматически включить обычный failover только настройкой или ручным запуском нельзя.

## Что подтверждено свежими данными

### Matrix и VLESS

- Последняя Matrix: `2026-08-28T21:16:29.875876Z`.
- Канал `vless`: `WARN`, `1/14` успешных сервисов.
- Telegram проходит (`10/10`), остальные профильные сервисы для обычного маршрута (YouTube, Instagram, Google, Google Auth и др.) имеют ошибки TLS/тайм-ауты.
- Статус `WARN` является особенностью агрегатора: один успешный сервис не означает готовность канала для всего профиля. Подробные строки Matrix показывают реальные отказы.
- Каналы с полным `14/14`: `wireguard-1779454504-c43409` и `amneziawg-exec-20260528-10-8-1-14`.

### Пользователи и цели

Текущие назначения из `users.registry`:

- `10.7.0.126` → `vless`, обычный, включён;
- `10.7.0.127` → `vless`, обычный, включён;
- `10.7.0.7` → `vless`, выключен.

Planner для обоих включённых пользователей вернул `action=keep`, причина `no_eligible_failover_target`.

Причины по существующим целям:

- `amneziawg-exec-20260528-10-8-1-14`: сервисы готовы, но `manual_only`, `reserve_only`, `canary_reserved_production_assignment_blocked`;
- `wireguard-1779454504-c43409`: сервисы готовы, но `planned_hard_full` по действующему лимиту;
- `awg0`: persistent failure по Instagram/Google/Google Auth;
- `awg3`: persistent failure по Google;
- `openvpn-1779388847-d2ad7c`: SUSPECT/Telegram down и профильные сервисные отказы;
- `1`: FAIL/Telegram down и устаревшие сервисные данные.

Это корректный fail-closed результат: цель не подменялась вручную, обычные пользователи не переносились.

### Реальный автоматический потребитель

`v7-health.service` активен и является текущим Matrix owner. Контур `v7-users-autoswitch.service` — существующий oneshot-потребитель через `v7-governed-canary-dry-run-cycle`; он завершён с `--max-users 0`, без движения пользователей.

Свежий `observe`:

- `emergency_failover_enabled=false`;
- `emergency_failover_authorized=false`;
- `l3_wake_decision=REJECT_WAKE`;
- `l3_incident_state=NO_INCIDENT_DISABLED`;
- `selected_moves=0`, `candidate_moves=0`;
- `terminal_outcome=NOT_EXECUTED_PHASE1`, `next_action=STOP_SAFE`;
- `active_capability=false` при наличии исторического certified/production-proven счётчика — capability не означает разрешение на текущую ordinary mutation.

### Действующий Authority-контракт

Через `admin_core/operator_execution.py` прочитан текущий контракт:

- contract: `sdpc_a6ede21bc2965aac1dc7597d`;
- состояние: `ACTIVE`, срок до `2026-09-25T11:18:37Z`;
- policy: `dap_default_tier1_readonly`;
- `max_users_per_action=1`, `max_concurrent_transactions=1`;
- action classes: governed single-user, controlled certification topology, bounded availability-first controlled failover;
- разрешённые production effects для availability-first явно ограничены certification-only assignment, reservation, bounded apply/rollback;
- обычное назначение запрещено: `certification_identities_only=true`, `ordinary_assignment_mutation_allowed=false`, `ordinary_user_delta=0`;
- stop conditions включают `ACTION_CLASS_NOT_AUTONOMOUS_RUNTIME`, `STALE_EVIDENCE`, `UNKNOWN_FAILURE_MODE`, `AUTHORITY_BOUNDARY`.

Это не устаревшая запись: контракт выдан 2026-08-26 для Telegram certification и действует сейчас. Его нельзя расширить самим исполнителем.

### Reservation/operation

Последний найденный lease/restore barrier относится к завершённой governed операции над `10.0.0.3` (`awg0→awg3`), имеет `operation_terminal_state=APPLIED`, завершён и просрочен. Действующего lease, который можно было бы использовать для ordinary VLESS failover, нет. Просроченный barrier не переиспользовался.

### Runtime provenance

Локальная ветка и GitHub:

- branch `Updatesystem`;
- commit `dea95b685eeaf35ca25e60b91fa1d5534bf97d0b`;
- рабочее дерево чистое;
- `git ls-remote` подтвердил тот же commit на GitHub.

Фактический `/opt/v7/runtime-linkage.json` всё ещё указывает на deploy `df9d428579793a586c314a2ec0114d642ce91f02`.

Независимая проверка фактических файлов обнаружила drift, который штатный snapshot не видит:

- локальный/ожидаемый `tools/v7-users-autoswitch`: `4462ebd98f...`;
- фактический `/usr/local/bin/v7-users-autoswitch`: `2bea7c845a...`;
- diff показывает, что Runtime содержит старый удалённый `--new-user-admission` adapter, которого нет в текущем canonical коде;
- snapshot safe-deploy при этом заявляет совпадение, потому что использует сохранённые hash-данные, а не live checksum.

Это отдельный provenance/deploy-integrity дефект. Автоматически перезаписывать Runtime более старым или неразрешённым содержимым нельзя до отдельной безопасной reconciliation-процедуры.

## Проверки

- `tests.unit.test_v7_users_autoswitch_policy`: **219 PASS**;
- `tests.unit.test_admin_realtime_truth`: **8 PASS**;
- `tests.unit.test_service_failure_episode`: **2 FAIL из 122**.

Два отказа относятся к уже существующему расхождению старых тестовых ожиданий с текущим подготовленным cohort projection/idempotent feedback поведением (тест ожидает отсутствие `ordinary_member_slice` и другое потребление feedback). В рамках этой миссии они не исправлялись, чтобы не подменять Authority/Program задачу и не менять Runtime семантику без отдельного решения.

Safe-deploy gate в read-only режиме: allowlist PASS, GitHub PASS при сетевом доступе. Его production delta опирается на устаревший snapshot, поэтому live hash drift оставлен явно зафиксированным, а deploy не выполнялся.

## Изменения и эффект

- Изменений кода, конфигурации, Matrix, Planner, Authority, маршрутов и `users.registry` нет.
- Обычные пользователи не перемещались (`0`).
- Новых owner/timer/queue/registry/state source не создано.
- VLESS не объявлен здоровым: `1/14` не даёт права на обычную выдачу/перевод.
- Система сохранила безопасное поведение: при отсутствии одновременно разрешённой и пригодной цели — `STOP_SAFE`.

## Точная граница продолжения

Требуется решение/контракт существующего Authority owner (`admin_core/operator_execution.py`), который явно разрешит bounded ordinary failed-source recovery (начальный лимит, классы профилей, target/capacity, rollback, S11 и условия остановки). Одного общего согласия оператора или флага `emergency_failover_enabled` недостаточно: текущий действующий контракт запрещает ordinary assignment mutation.

После появления такого owner-backed контракта следующий порядок:

`Authority contract admission` → `live Runtime provenance reconciliation` → `реальный неблокирующий consumer от Matrix` → `один ordinary-like controlled proof` → `small cohort` → `bounded production proof` → `N11 closure`.

До этого состояния ручное перемещение клиентов и самовольное расширение политики нарушили бы действующий контракт.

