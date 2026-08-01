# Stage-25: устранение historical completed-stage recovery override

Дата: 2026-08-01  
Статус: DEPLOYED_ORDINARY_MATRIX_STAGE25_TRANSACTION_ACTIVE

## Точное owner-backed наблюдение

Первый ordinary Matrix tick после `bcef5849` произошёл в
`2026-08-01T15:55:52Z`, но передал executor Stage-10 и получил безопасный
`availability_first_stage_not_current`, без mutation. Это был не live capacity
или Authority boundary.

Причина: existing Matrix partial-recovery scan выбирал historical
`AVAILABILITY_FIRST_STANDING_STAGE_STOPPED` Stage-10 с baseline-reset marker,
хотя Stage-10 уже имеет immutable consumed campaign receipt
`afstage_74d124e8951bfaccf499067a`. Такой historical row не может владеть
current Stage-25 successor.

## Безопасное исправление

`tools/v7-service-matrix-refresh-all` теперь исключает из partial-recovery
только записи, чья campaign stage уже находится в canonical
`completed_stages`. Незавершённая Stage-25 запись остаётся в recovery path;
completed effects не повторяются.

Проверка: focused affected suite `148` passed.

## Deploy и текущая работа owner

- Runtime deploy: `deploy-z8-14-Updatesystem-7862993-20260801T231051`.
- Commit: `7862993f7a41752bf78db1c08dfab8ac7516f782`.
- Safe-deploy manifest: только
  `tools/v7-service-matrix-refresh-all`; allowlist/truth PASS.
- Следующий ordinary Matrix caller начался в `2026-08-01T16:11:17Z`.
- Он передал governed executor `--availability-first-stage 25`.
- В момент checkpoint executor работает по existing standing policy с fresh
  production child для certification identity `10.7.0.107`,
  `source=vless`, `target=awg3`.

Это активная owner-authorized transaction. Отчёт не утверждает Outcome,
receipt, reset, Stage-48 successor или campaign completion до завершения
verification, recovery, Outcome/Replay/Learning и exact-once accounting.
Matrix не запускался вручную; новых Authority, policy writes, manual
Candidate/Packet/lease или operator actions не было.
