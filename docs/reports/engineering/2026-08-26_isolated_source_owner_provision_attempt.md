# V7 isolated source owner provision attempt

Дата: 2026-08-26 01:30 MSK  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission: `V7_RUNTIME_CONTENTION_AND_MULTI_COHORT_FAILOVER_EXPERIMENT`

## Результат

`EXTERNAL_SOURCE_ENDPOINT_UNAVAILABLE_CLEANED_UP`

Попытка выполнена через существующий `admin/v7-admin-api` draft lifecycle, без
ручной записи registry, без нового owner и без включения источника в pool.

## Что использовано

Найден уже существующий, но не зарегистрированный config:

- AmneziaWG config с отдельным endpoint `94.241.139.241:44286`;
- существующий путь `/etc/amnezia/amneziawg/v7e19caebd878.conf`;
- новый временный draft был создан только штатным `egress_draft_create`;
- роль draft: `EXECUTION_ONLY`, `manual_only=1`, `reserve_only=1`.

Секреты и private key в отчёт не попали.

## Owner evidence

1. `egress_draft_preflight_run` — **PASS**:
   - обязательные поля распознаны;
   - config не был в active registry;
   - hooks отсутствуют;
   - `Table=off` подтверждён;
   - endpoint присутствует.
2. `egress_draft_runtime_run(..., requested_mode=quarantine)`:
   - временный interface создан (`runtime_up=OK`);
   - interface видим в Linux;
   - внешний IP не получен: `curl timeout 8002 ms`;
   - service Matrix не запускался, потому что внешний IP gate не пройден;
   - cleanup `PASS`: process остановлен, interface и runtime config удалены.
3. `egress_draft_delete` — **DELETED**:
   - draft не был добавлен в pool;
   - draft перемещён существующим owner-ом в предусмотренный архив
     `/etc/v7/egress-drafts/.deleted/...`;
   - users moved: `false`; routes changed: `false`.

## Production invariants

- `users.registry`: не изменён;
- `egress.registry`: не изменён;
- Matrix/Planner/Authority semantics: не изменены;
- ordinary clients: `0` затронуто;
- active pool additions: `0`;
- persistent interfaces после cleanup: `0`;
- existing `v7-health.service`: продолжает работать;
- old standalone Matrix/Telegram timers: не включались.

## Причина блокировки

Config физически создаёт интерфейс, но его upstream не отвечает. Это внешний
ресурсный дефект (peer/UDP endpoint), а не дефект V7 lifecycle. Продолжать через
этот config нельзя: без внешнего IP и Matrix baseline он не является здоровым
controlled source, а добавление его в pool создало бы невалидную основу для
failover evidence.

## Следующий шаг

Через тот же `admin/v7-admin-api` принять минимум два реально отвечающих
certification-only source config с capacity, достаточной для заявленной
campaign. После успешного quarantine Matrix baseline автоматически продолжить
Phase A (quiet/moderate/back-to-back), затем Phase B (cohort 1/10/100/300).
До появления отвечающего external peer source-failure production experiment
остаётся `STOP_SAFE`; Polygon baseline уже сохранён отдельно.
