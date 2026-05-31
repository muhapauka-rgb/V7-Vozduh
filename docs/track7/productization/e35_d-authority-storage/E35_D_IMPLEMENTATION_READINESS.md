# E35.D Implementation Readiness

## Recommended Order

1. Authority Store.
2. Event Store.
3. Read Models.
4. Data Adapters.
5. Read APIs.
6. Admin Visibility.
7. Runtime Readers.
8. Future Write Paths.

## Classification

| Area | Decision |
|---|---|
| Evidence Store | Reuse link only |
| Proposal Store | Reuse link only |
| Runtime Trust Store | Reuse as input |
| Release Trust Store | Reuse as input |
| Audit Logs | Reuse/extend events |
| Switch Logs | Reuse as movement history |
| Identity DB | Reuse |
| Users Registry | Reuse, Do Not Duplicate |
| Egress Registry | Reuse, Do Not Duplicate |
| Operator Execution Records | Reuse |
| Approval Packet Records | Reuse |
| Admin Data Adapters | Extend |
| Authority Store | Add |
| Authority Event Store | Add |

## Build Readiness

Implementation can begin with read-only storage and read APIs.

Do not implement write/mutation APIs until:

- read models are visible;
- event schema validated;
- admin can explain authority state;
- tests prove single source of truth.

## Verdict

```text
implementation_ready=true
e35_e_ready=true
```
