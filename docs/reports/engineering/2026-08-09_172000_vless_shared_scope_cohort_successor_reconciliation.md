# Инженерный отчёт: reconciliation общего VLESS source-scope и successor

Дата: 2026-08-09  
Статус: `COMPLETE_CONSUMED`; активная программа продолжается через существующий Matrix consumer.

## Причина

У пяти service-specific VLESS incident-проекций был одинаковый неизменяемый source-scope (один fingerprint и размер 34), но feedback ранее успешного packet-bound перехода учитывался только в одном incident ID. Остальные проекции оставались с `protected=0`, `unresolved=33`, что давало `INCIDENT_SCOPE_ACCOUNTING_BROKEN` и удерживало repair frontier вместо нормального successor.

## Исправление

`tools/v7-users-autoswitch` теперь объединяет scope только при полном совпадении source, размера и fingerprint, а текущая route truth подтверждает target. После успешного accounting-repair старый repair consumer заменяется на существующий normal successor; при несовпадении scope repair по-прежнему fail-closed.

Коммиты:

- `16972203` — shared source-scope cohort reconciliation;
- `8eb41341` — successor advance после подтверждённого repair.

## Проверка

- focused unit tests: PASS;
- deploy manifest: PASS, фактический runtime diff только `tools/v7-users-autoswitch`;
- штатный `tools/v7-safe-deploy`: PASS, deploy `deploy-z8-14-Updatesystem-8eb4134-20260809T171523`;
- production passive consumer: PASS, `changed_records=1`;
- запрещённые эффекты: все `false` (нет Candidate/Packet/lease, apply, routing mutation, user movement, rollback, Authority или Production Maturity change);
- current production scope: `affected=34`, `protected=1`, `unresolved=33`;
- active records имеют существующий successor (`reconcile_service_failure_shadow_outcomes` либо OMP residual recomputation), без старого accounting repair consumer;
- `tools/v7-truth-check --all --json`: PASS, `FULLY_ALIGNED`;
- local, GitHub и production: `8eb413418e7b9ba41c78f1e2516b4c4c7a0714c2`.

## Текущий legal frontier

`CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`.

Следующий владелец — существующий `tools/v7-service-matrix-refresh-all` по активному timer. Он должен создавать только свежую Matrix-admitted revalidation; ручной запуск, reuse старого Packet/lease и создание искусственной транзакции не допускаются.
