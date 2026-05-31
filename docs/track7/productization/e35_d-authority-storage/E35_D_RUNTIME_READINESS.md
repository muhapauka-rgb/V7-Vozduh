# E35.D Runtime Readiness

## Scope

Read-only integration readiness only.

No execution.

## Future Integration Points

| Runtime Consumer | Read Need | Behavior |
|---|---|---|
| Autoswitch | effective authority per selected move | deny/explain in future hook |
| Manual Switch | authority and conflict state | precheck before command |
| Governed Execution | authority hash and protected-user status | packet/recheck input |
| Containment | emergency state and return target | bounded emergency decision |
| Scheduler | authority and expiry | skip expired/denied work |
| Evaluator | full state/read model inputs | verdict generation |
| Conflict Resolver | authority/domain inputs | deterministic outcome |

## Readiness Requirements

- stable authority state schema;
- event log schema;
- read adapters;
- read APIs;
- admin visibility;
- tests for no mutation.

## Failure Behavior

If authority store unreadable:

- forward movement cannot be allowed by future hooks;
- admin shows DEGRADED;
- current runtime routing remains unchanged.

## Verdict

```text
runtime_readiness_defined=true
```
