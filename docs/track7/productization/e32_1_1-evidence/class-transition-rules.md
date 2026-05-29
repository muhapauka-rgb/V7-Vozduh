# E32.1.1 Class Transition Rules

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

class_transition_rules_defined=true

## Promotion Chain

```text
UNCERTIFIED
  -> CLASS_1
  -> CLASS_2
  -> CLASS_4
  -> CLASS_10
  -> CLASS_20_CANDIDATE
  -> CLASS_50_CANDIDATE
  -> CLASS_100_CANDIDATE
  -> PRODUCTION_POOL
```

Candidate classes above CLASS_10 are not execution-certified by naming alone. They require their own preparation, capacity requalification, approval packet, governed execution proof, rollback proof, delayed monitoring, and replay denial.

## Promotion Rules

A target may be promoted from class N to class M only if:

- target-local pressure validation for M passes;
- long-window validation for M passes;
- soft_limit and hard_limit are safely requalified to M;
- a fresh approval packet is generated with `movement_budget=M` and `blast_radius=M`;
- execution-time recheck passes immediately before movement;
- exactly the approved M users move;
- rollback returns exactly those users to the rollback target;
- delayed monitoring shows no unapproved movement;
- replay validation denies reuse;
- runtime checkers remain OK;
- restore-settle returns GO.

## Downgrade Rules

A target must be downgraded or marked conditional if:

- target readiness becomes NO-GO;
- runtime checkers fail;
- hidden movers appear;
- selected_moves becomes nonzero outside approved movement;
- audit chain is broken;
- replay denial fails;
- rollback proof fails;
- hard_limit is lowered below class size;
- target quality drops below floor during validation;
- stale validation window exceeds policy age;
- governance isolation or autoswitch exclusion is violated.

## Stale Validation Rules

Capacity evidence becomes stale when:

- target metadata changes;
- target interface/profile changes;
- NAT/MSS/diagnose/load integration changes;
- runtime registry drift invalidates assumptions;
- long-window evidence exceeds the configured freshness window;
- target readiness becomes NO-GO after certification;
- quality floor drops are observed.

Stale evidence does not erase historical certification, but it blocks new movement until refreshed.

## Fail-Closed Behavior

All promotion and execution paths fail closed:

- no class promotion on partial evidence;
- no packet generation if readiness is NO-GO;
- no execution if packet is expired or stale;
- no execution if selected_moves is nonzero;
- no execution if hidden movers are present;
- no execution if runtime checkers fail;
- no execution if target class is lower than requested batch size.

## Manual Override Rules

Manual override may not weaken the class model.

Allowed manual actions:

- request a fresh validation window;
- request candidate-pool preparation;
- request target-local capacity validation;
- lower a target class;
- mark a class conditional or stale.

Forbidden manual actions:

- raise a class without evidence;
- ignore execution-time recheck;
- bypass rollback manifest;
- permit autoswitch/rebalance consumption of execution-only targets;
- lower quality floors to force promotion.

