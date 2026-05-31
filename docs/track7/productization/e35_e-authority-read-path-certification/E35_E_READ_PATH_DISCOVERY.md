# E35.E Read Path Discovery

## Scope

E35.E certifies that every authority read path sees the same truth before any autonomous execution design begins.

No runtime mutation is performed.

## Canonical Path

```text
Authority Store
-> Adapter
-> Read Model
-> API
-> Admin
-> Evaluator
-> Conflict Resolver
```

## Path Steps

| Step | Input | Output | Transformation | Potential Drift |
|---|---|---|---|---|
| Authority Store | `routing-authority.json` | current authority records | schema validation | stale/unreadable state |
| Event Store | `routing-authority-events.jsonl` | event stream | parse/sort/filter | corrupt line, missing event |
| Adapter | state/events/registries/trust links | normalized context | merge by user/channel ids | duplicate interpretation |
| Read Model | normalized context | operator-safe models | derive summaries/timelines | stale cache |
| API | read model | JSON response | redact/paginate/filter | field mismatch |
| Admin | API response | UI cards/drawers | label/status mapping | presentation drift |
| Evaluator | read model/context | verdict inputs | copy fields into envelope | missing/stale input |
| Conflict Resolver | evaluator context | deterministic conflict result | classify conflict | mismatch with evaluator |

## Drift Risk Areas

- store says `OPERATOR_PINNED`, API displays `AUTO`;
- event timeline misses latest state change;
- admin renders stale cached response;
- evaluator receives group default while API shows explicit user authority;
- conflict resolver receives a different target/channel than evaluator.

## Discovery Verdict

```text
read_path_discovery_complete=true
drift_points_identified=true
```
