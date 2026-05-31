# E35.E Read Path Matrix

| Component | Consumes | Produces | Truth Level | Derived Level | Mutation Rights | Cache Rights | Failure Impact |
|---|---|---|---|---|---|---|---|
| Authority Store | write path later | current authority state | Authoritative | none | none in E35.E | no | fail closed |
| Event Store | authority/evaluator events | timeline/history | Authoritative history | none | append later only | no | timeline degraded |
| Adapters | state/events/registries/trust | normalized context | none | high | none | bounded in-memory | REVIEW_REQUIRED/DEGRADED |
| Read Models | normalized context | summaries/details | none | high | none | yes, with source hash | stale warning |
| APIs | read models | redacted JSON | none | transport | none | HTTP cache only if hash-stable | endpoint degraded |
| Admin | APIs | UI state | none | presentation | none | UI cache only | operator warning |
| Evaluator | normalized context | verdict inputs | none | decision input | none | no hidden cache | fail closed |
| Conflict Resolver | evaluator context | conflict outcome | none | decision input | none | no hidden cache | REVIEW_REQUIRED |

## Verdict

```text
read_path_matrix_defined=true
```
