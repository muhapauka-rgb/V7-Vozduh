# Reconciliation активного VLESS-инцидента: scope accounting

Дата: 2026-07-27

## Результат

Production Matrix сформировал свежую `SERVICE_FAILURE_REVALIDATED` для
`sfinc_be20296fba3d8a6a33e58a583f1b58db`. Existing Matrix -> governed
executor -> L3 consumer выполнили один разрешённый bounded failover и затем
потребили его в compact incident projection.

Текущая owner-backed проекция:

- affected scope: 55;
- protected scope: 1;
- unresolved scope: 54;
- explicitly excluded/recovered: 0;
- balance: `55 = 1 + 54 + 0` (`ACCOUNTED`);
- raw список пользователей в новой durable projection не хранится.

Новый feedback: `execfb_7108319ce372188b72a31e0b`; Packet:
`pkt_preview_c7764a4d410da230bdc3f8f3`; пользователь `10.7.0.18` переведён
из `vless` в `wireguard-1779454504-c43409`, immediate verification: PASS,
rollback: NOT_REQUIRED.

## Изменение

Commit `0ccd2efb` добавил compact source-scope snapshot в существующий Matrix
event producer, перенос этого snapshot в causal binding и cumulative L3
reconciliation с exact-once consumption. Commit `2fff6447` добавил CPS consumer
для owner-backed accounted scope. Оба коммита прошли `tools/v7-safe-deploy`;
local, GitHub и production runtime выровнены на `2fff6447`.

Проверки: 101 focused tests PASS, production non-test Matrix caller PASS,
`tools/v7-truth-check --all --json`: PASS/FULLY_ALIGNED,
`tools/v7-convergence-status --json`: PASS/ALIGNED.

## Незакрытый residual

Runtime/L3 и CPS incident fields доказывают active continuing-incident drain,
но верхняя legacy CPS/OMP projection всё ещё содержит
`CURRENT_STOP_CONDITION=REAL_WORLD_LIMIT`, `PROGRAM_TERMINAL_*` и empty
program frontier. Это противоречит active scope, но atomic CPS consistency gate
правильно отклонил прямую замену: связанные registry/WIP/deterministic-sequence
owners ещё не дают единую допустимую projection.

Следующий exact engineering frontier:

`V7_SERVICE_FAILURE_ACTIVE_INCIDENT_CPS_OMP_PROJECTION_RECONCILIATION_V1`

Он обязан связать только существующих CPS, protected-WIP, capability registry
и deterministic-sequence owners так, чтобы `CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`
стал единой canonical projection. До этого terminal программы не заявляется;
existing production drain продолжает работать только в пределах standing
single-user policy и свежих live gates.

## Forbidden effects

Нет нового owner/registry/runtime/policy. Нет Authority expansion, Production
Maturity change, synthetic L8, restore-barrier write, rollback apply или
ручного bypass существующих gates.
