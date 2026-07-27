# CAUSAL M3: fresh revalidation активных passive incidents

Дата: 2026-07-27 03:44 UTC  
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Миссия: `CAUSAL_M3_ACTIVE_INCIDENT_REVALIDATION`  
Статус: `CURRENT_ACTIVE_INCIDENT_REVALIDATED_TO_EXACT_STOP_SAFE`

## Причина и исправление

Fresh production probe показал, что `https://api.anthropic.com/` на трёх
каналах возвращает HTTP `404` при успешной сетевой достижимости. До исправления
Matrix owner умел распознавать `401`, `403`, `429` как ограничение метода
проверки, но `404` и `405` ошибочно становились `FAIL` и могли продолжать
ложный service-failure episode.

Commit `f2307e91` расширил существующую классификацию Matrix только на
`404`/`405`. Они теперь имеют `ok=true`, `http_reachable=true`,
`status=HTTP_LIMITED`, `severity=WARN`; ограничение остаётся видимым, но не
создаёт failure episode, passive incident или failover opportunity. HTTP `5xx`
и транспортные ошибки остаются реальными failures. Добавлены прямые тесты обеих
границ.

## Production caller и consumer

Safe deploy manifest: единственный изменённый runtime файл
`tools/v7-service-matrix-test`; allowlist и GitHub truth — `PASS`.

Три fresh Matrix caller наблюдения (`awg0`, `awg3`,
`amneziawg-exec-20260528-10-8-1-14`) дали HTTP `404` с
`http_reachable=true`, `HTTP_LIMITED`.

Existing passive consumer затем потребил две точные recovery records через
существующие `Situation → Decision Trace → Outcome → Learning → closure`
owners. Existing OMP consumer вернул `NO_PENDING_OBLIGATION`. Compact
reconciliation после этого показал `open=0`, а повторный caller дал
`changed_records=0`, `invalid_open_incidents=0`: active incident не потерян и
не оставлен без successor, но новых Candidate/Packet/lease не возникло.

## Effects и итоговая граница

На всех production вызовах: Candidate `false`, Packet `false`, lease `false`,
Runtime apply `false`, routing mutation `false`, users moved `0`, rollback
apply `false`, Authority change `false`, Production Maturity `false`.

`tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`.  
`tools/v7-convergence-status --json`: `ALIGNED`. Local, GitHub и production
runtime указывают на `f2307e91`.

M3 закрыта. M4 не получает церемониальную работу: current passive incidents
отсутствуют. Точный current OMP frontier остаётся owner-backed
`V7_SERVICE_FAILURE_STANDING_DELEGATED_POLICY_AUTHORITY_DECISION` с границей
`ENGINEERING_AUTHORITY`; этот report не выдаёт contract и не расширяет
Authority.
