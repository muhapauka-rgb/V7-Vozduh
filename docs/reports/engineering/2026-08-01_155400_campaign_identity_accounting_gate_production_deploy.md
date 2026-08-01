# Campaign identity accounting gate — production deploy

## Итог

В существующие owners добавлен и production-подтверждён компактный mandatory gate
`v7.controlled-campaign-identity-accounting.v1`. Это не новый registry: truth
остается в `users.registry`, а projection содержит только counts, locations и
fingerprints без raw list identity.

## Исправленный причинный разрыв

До исправления historical `campaign.source_id` мог оставаться `1` после
owner-backed topology rebind, хотя реальный controlled baseline уже был
`vless`. Counts совпадали, но causal classification была неверной:
`baseline=0; targets=48`.

Теперь baseline выбирается только при однозначном совпадении current
`controlled_certification_source`, certification group и non-zero live
occupancy. При другой ситуации owner не делает предположений и сохраняет
historical fallback как явный selection mode.

## Production caller / consumer evidence

Deploy:

- `ee3c5e04` — gate до/после availability stage;
- `77c4139b` — live controlled-source binding;
- `24724edd` — causal classification non-baseline identity.

Каждый deploy выполнен только через `tools/v7-safe-deploy`; manifest содержал
только ожидаемые executable paths, service restart = `false`, policy/Authority
write = `false`, routing/user movement = `false`.

Production non-test read-only caller
`v7-users-autoswitch --controlled-source-topology-diagnostic` подтвердил:

- `status=ACCOUNTED`;
- `baseline_source_id=vless`;
- `baseline_source_selection=CURRENT_CONTROLLED_SOURCE_GROUP_OCCUPANCY`;
- `expected=48 = baseline_source=43 + active_forward=5`;
- `targets=0`, `active_reset=0`, `contained=0`;
- `raw_user_list_stored=false`.

Тем самым пять текущих identity вне baseline не потеряны и не ошибочно
засчитаны как permanent target allocation: они являются active forward work
текущего Stage 10.

## Runtime состояние и безопасность

На момент проверки один существующий Matrix-owned Stage 10 был активен.
Новый Matrix/service не запускался вручную, текущая transaction не изменялась,
Packet/lease не создавались вручную. Последняя наблюдаемая operation оставалась
packet-bound существующего owner для certification identity; ordinary users = 0.

`tools/v7-truth-check --all --json`: `PASS`.

`tools/v7-convergence-status --json`: `PASS`, `ALIGNED`.

## Следующий exact frontier

`EXISTING_MATRIX_FRESH_REVALIDATION_AFTER_EXACT_STOP_SAFE` внутри уже активного
`V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`: завершить/восстановить
текущий Stage 10 по fresh Packet/lease и затем записать stage receipt только
при полном Outcome/Replay/Learning и baseline reset.

`Stage 25/48` и настоящая batch-window ladder не объявлены закрытыми: current
runtime всё ещё использует serial one-user Packet/lease path. Следующая
engineering задача — reuse existing multi-move checkpoint/containment primitive
для bounded batch window после отдельной Polygon proof и без расширения
standing semantic envelope.
