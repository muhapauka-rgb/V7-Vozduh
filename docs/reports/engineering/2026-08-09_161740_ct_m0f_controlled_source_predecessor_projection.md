# CT-M0F: честный controlled-source predecessor

Дата: 2026-08-09

## Результат

Исправлена семантическая связь между существующим `controlled-source topology`
owner и CT-M0F sample selector. Наличие healthy shared target больше не
публикуется как `AUTO_ADMITTED`, когда отсутствует изолированный,
group-aligned controlled source.

## Причина

Production topology diagnostic допускал availability-first target, хотя
current campaign не имел controlled source. Следующий selector корректно
останавливался, но прежняя проекция создавала ложное впечатление готовности
campaign и скрывала истинный predecessor.

## Исправление и проверка

- Commit: `e82a00181b740569e550ce9cad4f148165f5f0a2`.
- Изменён только existing owner `tools/v7-users-autoswitch` и его unit test.
- Новая production-проекция:
  `CONTROLLED_SOURCE_TOPOLOGY_PROVISIONING_REQUIRED`.
- Durable successor:
  `SAFE_PREDECESSOR_REQUIRED:EXISTING_CONTROLLED_SOURCE_RESERVATION_AND_CERTIFICATION_GROUP_OWNER`.
- Production non-test read-only caller подтвердил terminal.
- `tools/v7-safe-deploy` применил только `tools/v7-users-autoswitch`.
- `tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`.
- `tools/v7-convergence-status --json`: `ALIGNED`; local/GitHub/production
  runtime commit совпадают на `e82a0018`.

## Границы

Не выполнялись: policy/registry write, identity provisioning, Candidate,
Packet, lease, restore barrier, apply, routing mutation, user movement,
rollback, Authority expansion и изменение Production Maturity.

VLESS в последнем штатном Matrix цикле восстановился до `14/14`; поэтому
реальный service-failure incident не был искусственно продлён.

## Точный следующий frontier

`EXISTING_CONTROLLED_SOURCE_RESERVATION_AND_CERTIFICATION_GROUP_OWNER`:
создать только owner-backed isolated controlled source и group-aligned
certification binding, затем existing Matrix consumer сможет подготовить
свежий CT-M0F sample. Это отдельная Authority/production-assignment граница;
она не вытекает из target-only standing policy.
