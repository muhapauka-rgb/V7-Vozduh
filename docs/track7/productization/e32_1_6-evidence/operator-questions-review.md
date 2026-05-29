# E32.1.6 Operator Questions Review

mode=ARCHITECTURE_MODELING
runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

operator_questions_defined=true

## Core Operator Questions

Operators need fast answers to these questions:

1. What class is this target certified for?
2. Is the target eligible for forward movement right now?
3. How many users can be approved safely right now?
4. Why is capacity blocked, if blocked?
5. How fresh is the certification evidence?
6. What confidence level does the certification have?
7. What evidence supports the certification?
8. Is rollback still available?
9. Is the target isolated from autoswitch/rebalance?
10. What action is safe next?

## Required Visible Fields

- target id;
- target role;
- capacity class;
- capacity status;
- capacity confidence;
- certified capacity;
- hard limit;
- active policy cap;
- effective batch cap;
- available capacity;
- target users count;
- capacity reserved;
- validation age;
- stale/expiration times;
- readiness status;
- restore-settle status;
- runtime checker status;
- autoswitch/rebalance/prod-assignment eligibility;
- allowed operator actions;
- blocked action reasons.

## Fields Operators Should Not Treat As Authority

The view may display derived fields, but must label them as derived:

- effective batch cap;
- current capacity;
- available capacity;
- execution eligibility.

The UI or CLI must not imply derived values are editable source-of-truth.

## Current Target Operator View

```text
target=amneziawg-exec-20260528-10-8-1-14
capacity_class=CLASS_10
capacity_status=CERTIFIED
capacity_confidence=HIGH
effective_batch_cap=10
max_concurrent_batches=1
forward_execution=allowed_only_if_all_governance_gates_pass
production_pool_authority=false
```

