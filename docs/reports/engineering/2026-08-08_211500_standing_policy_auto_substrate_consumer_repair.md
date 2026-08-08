# Автоматическое потребление exact substrate-request без повторного подтверждения

## Причина петли

Активный Tier-48 contract `SERVICE_FAILURE_WITH_CONTROLLED_CERTIFICATION_AVAILABILITY_FIRST_V2` покрывал уже материализованные certification-only failover stages, но явно исключал incremental identity provisioning. Поэтому request `cpsauth_r1_ef268a075d65194d0fae03a1` с `max_new_certification_identities=8` корректно останавливался на `ENGINEERING_AUTHORITY`, а не мог быть повторно подтверждён автоматически.

## Исправление

Расширен существующий Authority/policy owner, не создан новый owner, registry, queue или watcher.

- Добавлен узкий V3 profile `SERVICE_FAILURE_WITH_CONTROLLED_CERTIFICATION_AVAILABILITY_FIRST_V3`.
- V3 может потребить только pending request точной схемы Tier-48: active program, contract ID/hash, TTL, source, certification-only scope, пустой target, ladder `5/10/25/48`, concurrency `1`, все четыре named subscopes и ceiling `max_new <= 48` обязаны совпасть.
- Потребление append-only и cross-process exact-once через существующий policy/audit lock; provenance actor — `existing-standing-delegated-policy-consumer`.
- Обычные пользователи, Packet/lease, routing apply, rollback, self-expansion и Production Maturity не затрагиваются решением Authority. Existing provisioning owner получает право выполнить только fresh incremental delta после отдельной текущей проверки.
- Исправлен existing substrate consumer: он вычисляет delta от текущего certification pool, а не ошибочно требует создать 48 identity при уже имеющихся 40.
- Existing Matrix timer стал consumer: сначала exact audit decision, затем existing provisioning consumer. Повторный Matrix cycle не создаёт вторую decision record.

## Проверка до deploy

Пройдены focused suites:

`tests.unit.test_operator_execution_packet`, `tests.unit.test_service_failure_automation_evolution`, `tests.unit.test_service_failure_episode`, `tests.unit.test_governed_canary_cli`.

Новый regression test подтверждает: V3 policy потребляет только exact unexpired request; второй consumer возвращает `ALREADY_CONSUMED_EXACT`; в audit остаётся ровно одна decision record. Второй test подтверждает delta `40 -> 48` = 8, без вызова provisioner в preflight.

## Следующий безопасный шаг

После production deploy existing Authority owner атомарно заменит V2 на exact V3 contract, опираясь на постоянное operator-delegation разрешение. Затем обычный Matrix cycle должен автоматически потребить текущий request и передать его existing provisioning owner. Любой mismatch, expiry или live preflight failure остаётся `STOP_SAFE` с automatic Matrix re-entry; повторное ручное подтверждение не требуется.
