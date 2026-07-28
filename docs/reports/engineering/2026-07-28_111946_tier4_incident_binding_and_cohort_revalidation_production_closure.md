# Tier‑4 incident binding и cohort revalidation — production closure

Дата: `2026-07-28`

## Итог

Mission закрыла два дефекта существующей цепочки Tier‑4:

1. Matrix могла передать standing‑policy лимит в общий planner без точной
   привязки к текущему Service Failure obligation.
2. Downstream restore‑barrier revalidation для cohort использовала только
   первого участника вместо атомарного all‑member binding.

Новых Program, owner, registry, queue, watcher, Planner, Runtime или Authority
не создано.

## Исходное production‑наблюдение

Первый естественный Tier‑4 вызов дошёл до существующего L3 cohort executor:

- Packet: `pkt_a39c6102794b5c9a920149c1`;
- lease: `execlease_7f47f564636afa8df07c5e5c`;
- operation: `govexec_bb1f0f6c57d1c71fb75fd513`;
- выбранные пользователи:
  `10.0.0.6`, `10.7.0.3`, `10.7.0.2`, `10.7.0.8`;
- источники: `awg0`, `awg3`;
- target: `wireguard-1779454504-c43409`;
- terminal: `atomic_execution_envelope_source_changed`;
- apply: `false`;
- users moved: `0`.

Это не был incident‑bound VLESS cohort. Попытка безопасно остановилась до
apply и не дала Tier‑4 evidence.

## Исправление

Расширены только существующие owners:

- Matrix передаёт exact obligation ID, incident ID, source и scope fingerprint;
- executor независимо перечитывает durable obligation, OMP receipt и fresh
  capture‑only event;
- пустой scope останавливается до planner;
- Packet сохраняет exact causal binding;
- cohort source/snapshot binding строится из одной стабильной read generation;
- restore‑barrier revalidation повторно проверяет весь cohort, а не первого
  участника.

## Проверка

- целевые и затронутые тесты: `529 PASS`;
- commit:
  `038568d4c78b91f108da1f91d154e89f6bdc273e`;
- GitHub branch `Updatesystem`: тот же commit;
- safe deploy:
  `deploy-z8-14-Updatesystem-038568d-20260728T110359`;
- production hashes совпали для всех четырёх изменённых Runtime файлов.

Matrix вручную не запускалась. Первый полностью post‑deploy timer cycle:

- start: `2026-07-28T04:18:28+00:00`;
- end: `2026-07-28T04:19:46+00:00`;
- systemd result: `success`;
- obligation: `sfaob_bbb80ec875743dbf720c8395`;
- incident: `sfinc_79c7265b16283934089d5119f65455dd`;
- source: `1`;
- affected: `0`;
- unresolved: `0`;
- terminal: `STOP_SAFE_CURRENT_SOURCE_SCOPE_EMPTY`;
- action attempted: `false`;
- Runtime mutation: `false`;
- users moved: `0`.

Lease и restore barrier после цикла не менялись. Последний production Packet
остался исторической безопасно остановленной попыткой от `03:48 UTC`; новых
Packet/lease не создано.

В `users.registry` существует одна строка `current=vless` для `10.7.0.7`, но
она `enabled=0`. Поэтому active VLESS source scope по действующему контракту
равен нулю; это не потерянный активный пользователь.

## Authority и evidence

- Authority‑approved tier: `4`;
- Runtime‑enabled tier: `4`, serial cohort;
- production‑proven tier: `1`;
- первый реальный Tier‑4 positive‑scope Outcome всё ещё отсутствует;
- Authority expansion: `NONE`;
- Production Maturity change: `NONE`;
- Natural L8 credit: `NONE`.

## Legal terminal и successor

Текущий legal terminal:

`STOP_SAFE_CURRENT_SOURCE_SCOPE_EMPTY`.

Durable successor:

`V7_SERVICE_FAILURE_AUTOMATION_FRESH_EVENT_REVALIDATION`.

Следующий genuine positive‑scope matching incident автоматически войдёт в
существующую Matrix → obligation → planner → fresh Candidate/Packet/lease
цепочку. Tier‑5 в этой Mission не начинается.
