# Инженерный отчёт: CT-M0F binding к текущему VLESS scope

Дата: 2026-08-09  
Статус: `COMPLETE_CONSUMED`; CT-M0F продолжает работу через существующий ordinary Matrix consumer.

## Причина

Production сохранял несколько OMP-consumed пассивных наблюдений одного VLESS hard-failure generation. Старые наблюдения относились к историческому scope из 34 пользователей, а два новых — к текущему route scope из 33 пользователей. Предыдущий selector считал любое такое множество неоднозначным и законно возвращал `STOP_SAFE_CONTROLLED_SOURCE_PREDECESSOR_REQUIRED`, хотя текущая production route truth уже давала точную связку.

## Исправление

`tools/v7-users-autoswitch` получает краткую текущую source-scope projection из существующего `users.registry`: только source, count и fingerprint; raw user list не сохраняется. В CT-M0F selector:

- выбирается только OMP-consumed incident с точным current scope;
- повторные наблюдения допускается coalesce только при одинаковых incident generation и scope fingerprint;
- при таком повторении детерминированно выбирается самый свежий observation;
- разные generation, scope либо stale single binding по-прежнему fail-closed.

Коммиты:

- `76552372` — привязка CT-M0F к current route scope;
- `b5e52067` — coalesce повторных current-scope observations.

## Проверка

- 7 focused unit tests и syntax/diff checks: PASS;
- safe-deploy manifest: PASS; runtime package содержит только `tools/v7-users-autoswitch`;
- штатный deploy: PASS, `deploy-z8-14-Updatesystem-b5e5206-20260809T173740`;
- production non-test selector: `CT_M0F_STANDING_CONTROLLED_FAILURE_READY`;
- owner-backed binding: `sfinc_c20bcdd3ebcf42524fe8361fdd308c1e`, generation `egid_be6367407f70e591005185a2`, current VLESS scope `33`, fingerprint `9b541371...8ceb`;
- target: `awg0`, admitted existing availability-first policy; ordinary-user delta `0`;
- forbidden effects: все `false` — нет policy/audit write, Candidate, Packet, lease, apply, routing mutation, movement, Authority expansion или Production Maturity change;
- `tools/v7-truth-check --all --json`: PASS, `FULLY_ALIGNED`;
- `tools/v7-convergence-status --json`: `ALIGNED`; local, GitHub и production runtime — `b5e5206746c168f30e6ce30d4f9e29caee7eb04d`.

## Текущий legal frontier

`NEXT_ORDINARY_MATRIX_GENERATION_PREPARES_FRESH_SAMPLE` внутри `CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`.

Следующий producer — активный `tools/v7-service-matrix-refresh-all` timer. Он сам выполнит новую Matrix observation и, только если все fresh live gates пройдут, создаст свежие Candidate/Packet/lease и выполнит один certification-only action внутри уже действующей standing policy. Ручной запуск Matrix, reuse старых артефактов и искусственное движение пользователей запрещены.
