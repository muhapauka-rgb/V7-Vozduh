# E35.B Implementation Readiness

## What E35.C Must Implement

E35.C should define the implementation contract for:

- boundary evaluator;
- conflict resolver;
- effective authority chain output;
- boundary event schema;
- admin read APIs;
- autoswitch boundary read integration;
- governance boundary recheck integration.

## What P2 Must Implement

P2 should implement:

- read-only boundary surfaces first;
- boundary preview APIs;
- authority/boundary event storage;
- autoswitch denial-by-boundary explanation;
- admin drawer integration;
- later controlled write actions.

## What Remains Architecture Only

- future scheduler authority;
- user-facing self-service routing requests;
- autonomous production pool execution;
- broad policy automation.

## Classification

| Area | Classification |
|---|---|
| Safety gates | Reuse |
| Governance packets | Extend |
| Autoswitch gates | Extend |
| Group policy | Extend |
| Operator manual switch | Extend |
| Containment model | Extend |
| Sticky score | Do Not Touch |
| Speed/score | Do Not Touch |
| Execution-only target isolation | Do Not Touch |
| Admin UI | Extend |
| Evidence/Proposal/Trust | Extend links only |
| `users.registry` | Reuse |
| `egress.registry` | Reuse |

## Readiness Verdict

```text
implementation_ready=true
e35_c_ready=true
```
