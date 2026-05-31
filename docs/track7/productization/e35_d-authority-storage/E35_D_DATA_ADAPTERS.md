# E35.D Data Adapters

## Purpose

Adapters transform raw stores into operator-safe read models.

## Adapter Flow

```text
Authority State -> Effective Authority
Events -> Timeline
Conflicts -> Conflict Queue
Reviews -> Review Queue
Emergency Events -> Emergency Queue
Registries -> Current Runtime Context
Evidence/Proposal/Trust -> Links and explanations
```

## Required Adapters

| Adapter | Input | Output |
|---|---|---|
| Authority State Adapter | `routing-authority.json` | effective authority per user |
| Event Timeline Adapter | `routing-authority-events.jsonl` | ordered timeline |
| Conflict Adapter | events + policy | unresolved conflict queue |
| Review Adapter | review events | pending/closed review queue |
| Emergency Adapter | emergency events + state | active emergency queue |
| Registry Context Adapter | users/egress registries | current route/channel context |
| Link Adapter | evidence/proposal/trust stores | operator links |

## Fail-Closed Rules

- unreadable authority state: `authority_health=DEGRADED`;
- unreadable event log: timeline unavailable, summary still derives from state;
- missing registry: authority cannot produce movement ALLOW;
- broken links: show missing link, do not drop authority event.

## Tests

- adapters handle empty stores;
- adapters handle corrupt event line;
- adapters preserve source IDs;
- adapters do not mutate input stores.

## Verdict

```text
data_adapters_defined=true
```
