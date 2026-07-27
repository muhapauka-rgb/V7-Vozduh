# Отчёт: замыкание active-incident heartbeat → Matrix consumer

Дата: 2026-07-27

## Результат

Active VLESS incident `sfinc_be20296fba3d8a6a33e58a583f1b58db` остаётся
открытым и теперь проходит без ручного сообщения через существующую цепочку:

```text
production execution feedback + L3 compact scope
→ source CPS reconciliation
→ CODEX_AUTOMATION_PLATFORM heartbeat
→ existing Service Matrix consumer
→ fresh Matrix revalidation
```

Последний owner-backed production Outcome: `execfb_b85c0bc5e39adbc63c5511d5`,
Packet `pkt_preview_09ac9ac50f8c09852c95ba0d`, source event
`sfrev_e7fdcc39fc02eecf448488f2f577c2c9`. Он успешно переместил ровно одного
пользователя `10.7.0.42` с VLESS на существующий здоровый WireGuard target и
был потреблён CPS. После актуальной scope reconciliation:

```text
affected=34; protected=1; unresolved=33; excluded_or_recovered=0
next=CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN
```

Это не закрытие incident: VLESS остаётся деградированным, а 33 пользователя в
текущей source scope ещё не разрешены. Следующая попытка принадлежит только
существующему `tools/v7-service-matrix-refresh-all`, который каждый раз создаёт
свежие Candidate/Packet/lease и повторно проходит все live gates.

## Устранённые разрывы

1. Heartbeat ожидал старый task identity и безопасно отказывался от platform
   wake. Контракт синхронизирован с текущей platform-owned задачей, при этом
   произвольный target по-прежнему fail-closed.
2. Повторное чтение уже consumed Outcome сравнивало его исторический Packet
   scope с новой L3 scope и ошибочно возвращало STOP_SAFE. Idempotent replay
   теперь признаётся только после базовой identity/CPS проверки; новый
   feedback по-прежнему обязан совпадать со своим source generation.
3. После активного incident generic Continue OMP мог выбрать исторический
   Polygon frontier. Active incident drain теперь имеет явный приоритет и
   возвращается к существующему Matrix consumer, без запуска Polygon,
   Packet/lease, routing mutation или user movement из heartbeat.

## Production verification

- Focused unit suites для heartbeat, external/event-driven re-entry,
  service-failure evolution и truth owner: PASS.
- `tools/v7-safe-deploy` для `36673b77`, `14351d93` и `e3c059a1`: allowlist
  PASS, blockers отсутствуют.
- Production heartbeat после финального deploy: `PASS`,
  `REENTRY_COMPLETED`, consumer `tools/v7-service-matrix-refresh-all`,
  `ACTIVE_INCIDENT_DRAIN_PREEMPTS_GENERIC_POLYGON`.
- Production `v7-service-matrix-refresh.timer`: `enabled` и `active`; его
  последний owner-backed trigger был `2026-07-27 19:09:05 MSK`.
- `tools/v7-truth-check --all --json`: PASS.
- `tools/v7-convergence-status --json`: `ALIGNED`; local, GitHub и production
  runtime находятся на `e3c059a1f7eaa2168d96651a6df3b4aaf97112bc` на момент
  проверки.

## Safety

Новая связка не выдала Authority, не изменила Production Maturity и не
выполнила restore-barrier, rollback или routing action сама. Реальный action
`execfb_b85…` был ранее допущен действующей Tier-1 standing policy и прошёл
существующие packet-bound verification/Outcome/Learning owners.

## Точный следующий frontier

`CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN` через свежую наблюдаемую
Matrix generation. Термин наступит только при `CURRENT_SOURCE_SCOPE_EMPTY`,
подтверждённом recovery VLESS или точном owner-backed live blocker.
