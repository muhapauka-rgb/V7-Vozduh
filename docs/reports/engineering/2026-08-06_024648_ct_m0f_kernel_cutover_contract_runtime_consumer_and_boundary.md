# CT-M0F: kernel cutover contract, Runtime consumer и текущая граница

Дата: `2026-08-06T02:46:48Z`

## Итог

Текущий CT-M0F больше не заблокирован отсутствием online remote client agent.
Remote-device/application recovery сохранён как отдельный будущий evidence gate
и остаётся `NOT_MEASURED`; он не подменён server-side доказательством.

Текущий инженерный объект:

`CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_LATENCY`.

Он соединяет существующие owners:

`Matrix failure clock -> Planner decision -> Candidate/Packet/lease -> assignment writer -> exact policy rule/table/route verification -> target-egress fresh TLS/HTTP payload -> Time consumer -> deferred Outcome/Replay/Learning`.

## Реализация

- Program `V4.6` и OMP `V4.69` закрепили dual gate и точную claim boundary.
- Time owner получил composed cutover contract, монотонные интервалы и bounded
  five-sample nearest-rank gate.
- `v7-client-speed-api` переиспользует существующий fresh DNS/socket,
  `SO_BINDTODEVICE`, TLS/HTTP payload и expected-egress-IP verifier в новом
  target-only режиме. Режим никогда не заявляет exact-user payload или remote
  recovery.
- Matrix сохраняет reboot-scoped monotonic failure confirmation для новых и
  continuing incidents; исторический UTC не преобразуется в elapsed time.
- Scoped route verifier теперь доказывает policy rule, table и effective route.
- Governed canary передаёт существующие Packet/operation/lease identities в
  autoswitch; consumer запускается автоматически только с явным CT-M0F
  validation flag и certification identity.
- Missing lineage, ordinary identity, route failure, Matrix failure, missing
  target address или payload mismatch останавливают consumer до claim.

## Проверка и deploy

- Focused affected tests: `403 PASS`.
- Первый commit: `a441dbe0bc7d6bbe1f1022a962bc486659439dd6`.
- Runtime-consumer commit: `4e21b65856f4b62fcbd7bc0b4f9008845e4e1b6a`.
- Оба commit отправлены в GitHub и применены только через
  `tools/v7-safe-deploy`.
- После второго deploy: `deployment_required=false`, allowlist `PASS`, Runtime
  linkage указывает `4e21b65856f4b62fcbd7bc0b4f9008845e4e1b6a`.
- Production non-test consumers: deployed Time owner вернул
  `KERNEL_CUTOVER_GATE_INSUFFICIENT_OR_FAILED` для пустого набора без effects;
  governed production CLI экспонирует три CT-M0F validation bindings.
- Truth после первого deploy: `PASS`, `FULLY_ALIGNED`; финальная проверка
  выполняется после атомарной CPS-проекции этого отчёта.

Полный монолитный unit-suite был остановлен как непропорционально долгий после
обнаружения несвязанных ранних failures; целевой affected suite завершён
полностью и зелёный. Failures не маскировались и assertions не ослаблялись.

## Evidence и effects

- valid controlled cutover samples: `0`;
- ordinary-user delta: `0`;
- routing/user movement этой Mission: `0`;
- restore-barrier write: `0`;
- Authority expansion: `0`;
- Production Maturity change: `0`;
- Natural L8 credit: `0`;
- remote client/application recovery: `NOT_MEASURED_NO_CLIENT_AGENT`.

## Текущий legal terminal

Production audit owner сообщает:

`CONTROLLED_CERTIFICATION_SUBSTRATE_AUTHORITY_STATUS=NONE`.

В production существуют `41` enabled certification identities на текущем VLESS
source, но ни одна CT-M0F sample generation ещё не получила отдельный текущий
owner-backed admission и не была выполнена. Попытка запустить даже read-only
governed canary без явного dry-run contract была остановлена внешним safety
reviewer; обход не выполнялся.

Точный terminal:

`ENGINEERING_AUTHORITY_CT_M0F_CONTROLLED_VALIDATION_ADMISSION_REQUIRED`.

Точный successor после независимого допуска:

`ordinary Matrix generation -> existing controlled-production owner -> one certification identity -> fresh Candidate/Packet/lease -> CT-M0F flag -> bounded forward cutover -> target payload -> composed Time receipt -> reset -> deferred Outcome/Replay/Learning -> next independently required sample or gate verdict`.

CT-M0F не завершён. CT-M1 остаётся `FORMED_DEPENDENCY_BLOCKED`. Remote client
agent не является текущим blocker, но остаётся будущим production/end-user
validation residual.
