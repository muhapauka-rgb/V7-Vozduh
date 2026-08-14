# BLOCK E35.C Boundary Evaluator And Conflict Resolution Report

## 1. Discovery Summary

E35.C completed as architecture/governance/admin-integration/implementation-planning only.

Discovery found existing decision points that become evaluator inputs:

- autoswitch gates;
- approval packets;
- operator execution/manual switch;
- group constraints;
- required services;
- service matrix status;
- capacity limits;
- quality floors;
- restore-settle;
- runtime trust;
- release trust;
- selected moves;
- hidden movers;
- quarantine;
- anti-flap;
- rollback paths.

Evaluator must not reimplement those systems. It consumes their outputs.

## 2. Evaluator Model

Boundary Evaluator:

```text
Проверка допустимости действия
```

It receives a proposed action and returns:

```text
ALLOW
DENY
REVIEW_REQUIRED
EMERGENCY_ONLY
```

It never executes movement.

## 3. Input Model

Inputs include:

- proposed action;
- user;
- current channel;
- target channel;
- routing authority;
- group boundary;
- required services;
- suitability;
- capacity;
- governance;
- runtime trust;
- release trust;
- restore-settle;
- selected moves;
- hidden movers;
- proposal context;
- containment context;
- emergency context;
- audit context.

## 4. Verdict Engine

Verdict priority:

```text
DENY > EMERGENCY_ONLY > REVIEW_REQUIRED > ALLOW
```

Exception:

If safety says no mutation at all, final verdict is `DENY`, not `EMERGENCY_ONLY`.

## 5. Conflict Resolver

Conflict resolver produces deterministic outcomes.

Unknown conflict:

```text
REVIEW_REQUIRED
```

Never `ALLOW`.

## 6. Emergency Model

`EMERGENCY_ONLY` means normal forward action is denied, but bounded containment/rollback may proceed.

Emergency cannot:

- become permanent automatically;
- bypass safety;
- bypass containment scope;
- be used for speed/score/rebalance.

## 7. Review Model

`REVIEW_REQUIRED` means machine cannot safely allow movement without human/governance decision.

Triggers:

- group conflict;
- authority conflict;
- stale trust;
- unknown suitability;
- expired authority;
- policy ambiguity;
- operator override request.

## 8. Event Model

Defined events:

- `VERDICT_CREATED`
- `VERDICT_DENIED`
- `VERDICT_ALLOWED`
- `VERDICT_REVIEW_REQUIRED`
- `VERDICT_EMERGENCY`
- `CONFLICT_DETECTED`
- `CONFLICT_RESOLVED`
- `REVIEW_CREATED`
- `REVIEW_CLOSED`
- `EMERGENCY_CREATED`
- `EMERGENCY_EXPIRED`

## 9. API Contract

Read APIs only:

- `GET /api/authority/verdicts`
- `GET /api/authority/conflicts`
- `GET /api/authority/reviews`
- `GET /api/authority/emergency`
- `GET /api/authority/explain`

No runtime mutation APIs.

## 10. Runtime Integration Contract

Evaluator call sites:

- before autoswitch apply;
- before manual switch;
- before governed execution;
- before scheduler execution;
- before containment action.

Failure behavior:

```text
fail closed
```

## 11. Implementation Readiness

Recommended P2 order:

1. Evaluator model.
2. Conflict resolver.
3. Read APIs.
4. Admin visibility.
5. Event model.
6. Runtime hooks.
7. Controlled write paths.

## 12. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Evaluator starts mutating runtime | High | Read-only contract and tests. |
| Evaluator duplicates autoswitch logic | Medium | Consume existing gate outputs only. |
| Unknown conflict allows movement | High | Unknown conflict -> REVIEW_REQUIRED. |
| Emergency used as bypass | High | Emergency categories and TTL. |
| Admin hides verdict reason | Medium | Mandatory explanation surfaces. |
| Runtime hook blocks unexpectedly | Medium | Start read-only, compare decisions before enforcing. |

## 13. Recommendations For E35.D

Recommended next block:

```text
E35.D_AUTHORITY_STORAGE_AND_READ_API_IMPLEMENTATION_CONTRACT
```

Focus:

- concrete storage schema;
- event retention;
- read API response contracts;
- admin data adapters;
- non-mutating evaluator preview implementation plan.

## Required Verdicts

```text
boundary_evaluator_defined=true
conflict_resolver_defined=true
verdict_engine_defined=true
review_model_defined=true
emergency_model_defined=true
event_model_defined=true
api_contract_defined=true
runtime_integration_defined=true
implementation_ready=true
e35_d_ready=true
```

## Safety Verdict

```text
runtime_mutation_performed=false
routing_changed=false
users_moved=false
autoswitch_apply_run=false
policy_apply_run=false
killswitch_changed=false
```
