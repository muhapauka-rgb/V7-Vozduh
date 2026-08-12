# Восстановление цепочки fast failure -> существующий planner consumer

**Дата:** 2026-08-12  
**Commit / deploy:** `5e62b622fcc0bfcb928da9db938a8938191d7b10` / `deploy-z8-14-Updatesystem-5e62b62-20260812T215013`

## Итог

Исправлен общий producer-consumer разрыв: новый канонический
`SERVICE_FAILURE_OBSERVED` с ненулевым *текущим* scope теперь будит только
существующий `v7-autoswitch-planner.service`, а его штатный 30-секундный timer
сначала потребляет поток уже существующих service-failure events. Новых timer,
scheduler, queue, owner, Runtime или хранилищ не создано.

`v7-users-autoswitch.timer` **не запускался**. Его состояние
`enabled + inactive (dead)` является намеренно удерживаемым legacy apply-path,
а не отсутствующим consumer; запуск нарушил бы действующий safety contract.

## Причина

1. Fast Telegram sentinel уже создавал каноническое failure evidence, но
   обычный planner не имел отдельного event-only входа и не был его consumer.
2. При продолжающемся отказе sentinel мог заменить временной Matrix-записью
   поля канонического episode. Это превращало одно продолжающееся событие в
   повторные «новые» события и могло будить consumer чаще, чем требуется.
3. Historical `source_scope` нельзя использовать как основание для action:
   на момент потребления source может восстановиться либо уже не иметь
   пользователей.

## Реализация

- `tools/v7-telegram-sentinel` сохраняет canonical episode lineage при
  обновлении fast-status и просит запуск существующего planner только для
  нового observed event с ненулевым текущим scope. Revalidation и zero-scope
  этого не делают.
- `tools/v7-service-matrix-refresh-all --consume-existing-service-failure-events-only`
  потребляет только канонический event stream; он пересчитывает фактический
  source scope по текущим Matrix и user owners. При zero-scope публикуется
  безопасный `NO_ACTION_CURRENT_FAILED_SOURCE_SCOPE_EMPTY`, без Candidate,
  Packet, lease, apply или движения пользователей.
- В существующий `v7-autoswitch-planner.service` добавлен этот event-only
  consumer перед уже существующим planner invocation. Его существующий timer
  остаётся единственным normal scheduler.

## Проверка

- Focused unit suite для sentinel, passive capture, sync/deploy contract и
  runtime snapshot выполнена; `git diff --check` — PASS.
- До deploy: GitHub truth — `GITHUB_ALIGNED` на `5e62b622`.
- Deploy manifest: только `tools/v7-telegram-sentinel`,
  `tools/v7-service-matrix-refresh-all`,
  `systemd/drafts/v7-autoswitch-planner.service`; forbidden effects — отсутствуют.
- После deploy: штатный `v7-autoswitch-planner.timer` сработал в
  `2026-08-12 21:51:16 MSK`; ручной Matrix/autoswitch run не выполнялся.
- `tools/v7-truth-check --all --json` — PASS, `FULLY_ALIGNED`;
  `tools/v7-convergence-status --json` — PASS, runtime commit = GitHub/local
  commit `5e62b622`.

## Границы и следующий frontier

Изменение само не создаёт production cutover и не выдаёт CT-M0F latency sample:
это было бы фальсификацией evidence. Следующий owner-backed путь остаётся
`ordinary Matrix -> fresh lawful incident binding -> existing planner -> fresh
Candidate/Packet/lease -> standing-policy admission -> bounded cutover -> Time
receipt`. Если текущий failed source не имеет пользователей, terminal строго
`NO_ACTION_CURRENT_FAILED_SOURCE_SCOPE_EMPTY`; если scope есть и target lawful,
путь продолжается автоматически без восстановления failed source как
предварительного условия.
