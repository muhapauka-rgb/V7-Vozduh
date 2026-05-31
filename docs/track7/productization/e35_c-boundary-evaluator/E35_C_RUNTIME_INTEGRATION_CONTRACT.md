# E35.C Runtime Integration Contract

## Call Sites

Evaluator should be called:

1. Before autoswitch apply.
2. Before manual switch.
3. Before governed execution.
4. Before scheduler execution.
5. Before containment action.

## Required Inputs By Call Site

### Autoswitch Apply

- selected move;
- routing authority;
- group boundary;
- suitability/capacity/service status;
- runtime trust;
- restore-settle;
- selected moves/hidden movers.

Failure behavior:

- fail closed;
- omit move from apply;
- include denied reason in plan.

### Manual Switch

- operator actor;
- user/current/target;
- authority state;
- group boundary;
- safety/runtime trust;
- suitability summary.

Failure behavior:

- deny or review;
- no command execution.

### Governed Execution

- packet scope;
- authority hash;
- protected-user overrides;
- runtime recheck;
- rollback manifest.

Failure behavior:

- deny packet/recheck;
- append denial audit.

### Scheduler Execution

- scheduled batch;
- current authority state;
- packet expiry;
- reservation/concurrency state.

Failure behavior:

- skip/expire scheduled work.

### Containment Action

- emergency trigger;
- current unsafe state;
- target safe state;
- return plan;
- lease.

Failure behavior:

- deny containment if trigger/scope missing.

## Output Contract

Every call site receives:

- verdict;
- reason;
- authority chain;
- conflicts;
- review/emergency IDs;
- audit requirement;
- admin message.

## Fail-Closed Requirements

If evaluator is unavailable:

- forward movement denied;
- rollback/containment requires explicit fallback policy;
- admin shows evaluator unavailable.

## Verdict

```text
runtime_integration_defined=true
```
