# CT-M0F: штатный Matrix re-entry и текущая граница controlled validation

Дата проверки: 2026-08-09.

## Результат

Промпт продолжения выполнен через существующих owners. Новый ручной запуск
Matrix, создание Candidate/Packet/lease, policy write, routing mutation и
перемещение пользователей не выполнялись.

Штатный `v7-service-matrix-refresh.timer` завершил очередной цикл в
`2026-08-09T07:05:20Z` (MSK `10:05:20`) с `Result=success`:

- Matrix: `OK`, 6 из 7 каналов в нормальном состоянии; VLESS остаётся
  `WARN` (10 из 14 проверяемых сервисов доступны).
- passive event consumer: `PASS`;
- service-failure advisory: `PASS`;
- существующий OMP consumer: `PASS`;
- durable next output: `CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`.

Значит цепочка наблюдения и автоматического потребления не потеряна: новый
ordinary Matrix tick сам публикует и сам доставляет безопасный successor. Следующий
tick остаётся владельцем re-entry; на момент проверки он запланирован на
`2026-08-09T10:17:09 MSK`.

## Разделение текущих состояний

Для продолжающегося VLESS incident существующий prepared-decision owner создал
свежий class projection к существующему Planner target. Это engineering
preparation, а не permission на действие: `execution_allowed=false`, а
bounded delegated action завершился
`STOP_SAFE_CURRENT_INCIDENT_NOT_ACTIONABLE` с точной причиной
`current_incident_has_no_owner_backed_actionable_recommendation`.

Это означает, что наличие healthy альтернативного канала само по себе не
равно допустимому production failover. Нужны одновременно свежая Matrix
classification, matching action recommendation, capacity/anti-flap/live policy
gates и fresh Candidate/Packet/lease.

CT-M0F — независимая certification-only ветка. Её read-only selector и
topology diagnostic согласованно вернули:

- `STOP_SAFE_CT_M0F_STANDING_CONTROLLED_SOURCE_REQUIRED`;
- `CONTROLLED_TOPOLOGY_FULL_PATH_EXTERNAL_RESOURCE_REQUIRED`;
- нет admissible isolated controlled source;
- нет exact certification identity на таком source;
- нет admissible distinct controlled target;
- CT-M0F standing validation consumer:
  `INACTIVE_NO_VALID_STANDING_CT_M0F_POLICY` /
  `ct_m0f_standing_authority_audit_missing_or_duplicate`.

Исторические availability-first receipts для tiers 1/2/5/10/25 сохранены и
не переиспользованы как CT-M0F permission. Они подтверждают прошлые
bounded outcomes, но не создают текущие source/topology/CT-contract.

## Точный terminal и re-entry

`CONTROLLED_TOPOLOGY_FULL_PATH_EXTERNAL_RESOURCE_REQUIRED` — это корректная
внешняя граница, а не повод ослабить isolation или назначить обычного
пользователя certification subject. Нужен owner-verified isolated controlled
source и correlation-distinct target (или target set) с usable capacity;
только после этого существующий owner может сформировать свежий matching
CT-M0F Authority package. Истёкший или отсутствующий CT contract не может
быть автоматически продлён, поскольку это был бы Authority bypass.

До появления этой resource truth safe continuation остаётся автоматическим:

`existing draft/resource owner -> Matrix/quality/capacity -> topology diagnostic
-> fresh matching Authority package -> existing CT-M0F consumer`.

Ни Natural L8 credit, ни Production Maturity, ни user effect в этом цикле не
зафиксированы.

## Проверки

- `tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`;
- `tools/v7-convergence-status --json`: `PASS`, `ALIGNED`.

