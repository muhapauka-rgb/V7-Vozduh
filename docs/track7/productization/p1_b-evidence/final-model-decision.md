# P1.B Final Model Decision

proposal_system_defined=true

## Decision

Proposal System is the second implementation package after Evidence Bundle System.

It converts evidence-backed diagnosis into safe, explainable recommendations that can later enter governance.

## Model Summary

A proposal includes:

- stable proposal id;
- type;
- status;
- confidence;
- severity;
- reason;
- affected users;
- current target;
- proposed target;
- required services;
- mandatory evidence bundle link;
- expected benefit;
- rollback hint;
- creation timestamp.

## Admin Decision

Proposal appears in existing V7 Admin surfaces:

- `Главная`;
- `Маршруты`;
- `Пользователи`;
- `Каналы`.

No new top-level navigation is created.

## Governance Decision

Proposal is not authority.

It can feed:

```text
Batch
-> Policy
-> Capacity
-> Concurrency
-> Scheduling
-> Execution-Time Recheck
-> Execution
```

but it cannot execute or bypass those gates.

## Storage/API Decision

P0 requires:

- Proposal Store;
- Proposal API;
- Proposal Drawer;
- evidence linkage requirement;
- lifecycle and expiration handling.

## Recommended Next Block

recommended_next_block=P1.C_RUNTIME_CONVERGENCE_SURFACE
