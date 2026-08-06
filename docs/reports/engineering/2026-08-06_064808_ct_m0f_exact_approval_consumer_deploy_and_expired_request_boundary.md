# CT-M0F: exact approval consumer deploy и expired-request boundary

Дата: `2026-08-06T06:48:08Z`

## Итог

Решение пользователя для request
`ctm0fauth_r1_cda5955e978cc52c22477670` было записано существующим Authority
owner до expiry: decision `ctm0fdec_7aca2104a4e87cb25fc90e8f`. Production
audit подтверждает `decision_count=1`, `consumption_count=0`.

Обнаруженный producer-consumer gap закрыт в существующих owners. Governed L3
path до effects проверяет exact request/generation и после создания только
fresh Packet/lease атомарно потребляет admission. Autoswitch Time consumer
независимо подтверждает тот же request/Packet/operation/lease/user/source/
target lineage. Duplicate, expiry, mismatch и generic-path bypass дают
`STOP_SAFE` до apply. TTL новых запросов увеличен с 15 минут до 24 часов без
расширения scope: request остаётся short-lived, exact и one-use.

## Проверки и deploy

- focused tests: `5 PASS`;
- полный affected contour: `372 PASS`;
- commit/push: `2b79ce558844a264731f78fd131304be2385b943`;
- safe-deploy preflight: `PASS`, blockers `0`, changed runtime files `3`;
- runtime delta после deploy: `0`;
- local/GitHub/production commit: `2b79ce558844a264731f78fd131304be2385b943`;
- изменены только существующие owners: `operator_execution`, governed L3 cycle,
  autoswitch consumer; новый owner/store/queue/watcher/Runtime не создан.

## Production effects

- prior request consumption: `0`;
- Candidate/Packet/lease: `0`;
- runtime apply/routing mutation/users moved: `false/false/0`;
- rollback apply: `false`;
- Authority expansion: `false`;
- Production Maturity change: `false`;
- CT-M0F samples: `0`.

## Legal terminal

Первый request истёк в `2026-08-06T06:45:09.824288+00:00` и не может быть
переиспользован. Следующий безопасный action — production non-test вызов уже
развёрнутого producer для одного свежего 24-часового request. Он делает только
append-only Authority audit write. После этого требуется независимое решение
по новому exact ID/hash; затем deployed consumer может выполнить одну bounded
certification-only validation через fresh Matrix/Packet/lease.

Terminal: `EXTERNAL_OWNER_INPUT_FRESH_CT_M0F_REQUEST_WRITE_REQUIRED`.
