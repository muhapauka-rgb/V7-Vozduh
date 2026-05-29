# E32.1.1 Final Model Decision

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

capacity_class_model_defined=true

## Final Decision

V7 capacity classes are formal governance certifications that combine:

- maximum bounded batch size;
- target quality evidence;
- runtime checker health;
- restore-settle health;
- rollback proof;
- delayed movement protection;
- replay denial;
- evidence freshness.

## Certified Classes

```text
CLASS_1=CERTIFIED
CLASS_2=CERTIFIED
CLASS_4=CERTIFIED
CLASS_10=CERTIFIED
```

Current certified class for `amneziawg-exec-20260528-10-8-1-14`:

```text
CLASS_10
```

## Candidate Classes

```text
CLASS_20_CANDIDATE=NOT_CERTIFIED
CLASS_50_CANDIDATE=NOT_CERTIFIED
CLASS_100_CANDIDATE=NOT_CERTIFIED
```

Candidate classes may be modeled and prepared, but they do not allow live execution until promoted by the full evidence chain.

## Production Pool Class

```text
PRODUCTION_POOL=ARCHITECTURE_TARGET_NOT_CERTIFIED
```

Production pool must be policy controlled and may not inherit CLASS_10 as blanket production-pool authority. CLASS_10 only certifies bounded operator-driven execution through ten users.

## Promotion And Demotion

Promotion requires:

- capacity validation;
- long-window validation;
- metadata requalification;
- approval packet;
- execution-time recheck;
- governed forward movement;
- rollback;
- delayed monitoring;
- replay denial;
- clean restore-settle;
- runtime checker OK state.

Demotion or conditional status is required when readiness, quality, runtime checkers, rollback, replay, audit, or evidence freshness fail.

## Batch Constraints

Current rule:

```text
max_batch_size = min(certified_class_limit, hard_limit, active_policy_cap)
```

For current target:

```text
certified_class_limit=10
hard_limit=10
active_policy_cap=10
max_batch_size=10
```

## Open Questions

- exact freshness TTL for capacity evidence;
- whether CLASS_20 should require 20-user proof or may use a production-pool staged rollout;
- how production-pool policy should represent concurrent packets;
- how to encode confidence levels in registry metadata;
- whether target class and route class should be separate fields or one composite policy object.

recommended_next_block=E32_1_2_CAPACITY_METADATA_MODEL

