# Service Failure Episode — production deploy and consumer verification

Дата: 2026-07-25  
Commit: `a2b448860437ab1adcd67e2070ea09defba01472`  
Deploy: `deploy-z8-14-Updatesystem-a2b4488-20260725T181727`

## Результат

`PASS — DEPLOYED_AND_CONSUMER_VERIFIED`

Исправление устойчивого service-failure episode развернуто штатным `tools/v7-safe-deploy`. После изменения admin entrypoint применён требуемый инструментом штатный restart admin API. Запрещённых effects, routing mutation, user movement, Packet/rollback apply, Authority change и Production Maturity change не было.

## Production caller → consumer

На production были загружены установленные `/usr/local/bin/v7-service-matrix-test` и `/usr/local/bin/v7-users-autoswitch`. Проверка работала только с одноразовыми каталогами `/tmp`; production state, сеть, users и routing не использовались.

Подтверждён путь:

```text
3 continuous probe observations
→ one EXTERNAL_UNATTRIBUTED service-failure event
→ one NATURAL_PRODUCTION_CANDIDATE
→ NO_ACTION_NATURAL_EVENT_PENDING_PROVENANCE_AND_LEGAL_OUTCOME
```

Полученные инварианты:

- `failure_samples=3`, `consecutive_failures=3`, `bad_for_seconds=120`;
- event provenance: `EXTERNAL_UNATTRIBUTED`;
- passive consumer active: `true`;
- `execution_performed=false`;
- natural production credit: `false`;
- временное состояние удалено после проверки.

Следовательно, исправление активно готовит и потребляет наблюдаемый эпизод, но не фабрикует Natural L8 evidence.

## Final verification

```text
tools/v7-safe-deploy --json: PASS, deployment_required=false, mismatches=[]
tools/v7-truth-check --all --json: PASS, FULLY_ALIGNED
tools/v7-convergence-status --json: PASS
local = GitHub = production linkage: a2b448860437ab1adcd67e2070ea09defba01472
```

## Legal terminal

`SERVICE_FAILURE_EPISODE_CAPTURE_AND_PASSIVE_CONSUMPTION_DEPLOYED`.

`natural_production_present` остаётся открытым: для его закрытия требуется настоящий owner-backed natural production outcome с доказанной provenance, а не данная изолированная verification.
