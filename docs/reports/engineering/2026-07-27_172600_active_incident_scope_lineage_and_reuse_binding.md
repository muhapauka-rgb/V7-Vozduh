# Reconciliation активного VLESS incident: scope, lineage и reuse

Дата: 2026-07-27

## Итог

`PASS_WITH_ACTIVE_AUTOMATIC_SUCCESSOR`.

Существующие owners расширены без новой программы, registry, watcher или
Authority: `tools/v7-users-autoswitch` остаётся owner L3 incident state,
`execution-events.jsonl` — immutable owner outcomes, а `tools/v7_sync_lib.py`
— bridge в CPS/OMP.

## Production факт

После non-test production consumer текущая живая source generation incident
`sfinc_be20296fba3d8a6a33e58a583f1b58db` owner-backed и сбалансирована:

```text
52 affected = 0 currently protected + 52 unresolved + 0 excluded/recovered
generation: sfrev_f1d6b0a2ece6f5d8ed59cb6dc5d04172
```

Предыдущая generation `53` не была переиспользована: она оставлена только в
`supersedes_invalid_scope` с причиной
`LIVE_ROUTE_SCOPE_NO_LONGER_RECONCILABLE_WITH_LEGACY_GENERATION`.

## Разделение фактов

- `CURRENT_SOURCE_SCOPE` — только текущие assignment/route facts и exact
  source-scope fingerprint.
- `INCIDENT_CUMULATIVE_SCOPE` — packet/feedback/Learning pointers с
  классификацией; она не уменьшает current denominator.
- Production cumulative projection сохранила 13 packet-bound successes:
  11 `HISTORICAL_PROTECTED_PRE_BASELINE`, 2
  `HISTORICAL_MOVED_INCIDENT_BINDING_MISSING`, 0 ложных
  `CURRENT_INCIDENT_PROTECTED`.
- Никакие historical Packet, Candidate, lease или approval не стали
  executable.

## Knowledge reuse

В существующем Program закреплён owner-backed
`KNOWLEDGE_REUSE_AND_SELECTIVE_REVALIDATION`: Tier 1/2/5/10/bounded читаются
через Knowledge Plane и Engineering Truth Lifecycle; повторная certification
допускается только при declared invalidation trigger. Новый отчёт, Codex turn,
свежий observation или истёкший Packet сами по себе не являются trigger.

## Consumer цепочка

Production advisory materialised `sfaob_5649c97cc9e31bea4f8ffa9d`.
Существующий production receipt consumer его потребил в
`sfomp_b2e7cc8e24a583082eecd6da`; canonical source CPS атомарно подтвердил:

```text
CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN
```

Forbidden effects во всех вызовах: `runtime apply = false`, routing mutation
`= false`, users moved `= 0`, Packet/lease creation `= false`, Authority и
Production Maturity `= unchanged`.

## Exact next frontier

`CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN` через существующий fresh
Matrix -> planner -> fresh Candidate/Packet/lease путь. Реальная next action
допустима только если активная standing delegated Tier-1 policy и все fresh
live gates независимо разрешат её; иначе legal output —
`STOP_SAFE_FRESH_EVENT_REVALIDATION_REQUIRED` с automatic re-entry.

## Residual

Перед окончательным Step 2 требуется deploy совместимого исправления, которое
передаёт новую source generation в cumulative projection в том же cycle. До
этого historical lineage уже не влияет на routing, но её context fingerprint
в receipt относится к предыдущей generation и не может считаться финальным
reconciliation result.
