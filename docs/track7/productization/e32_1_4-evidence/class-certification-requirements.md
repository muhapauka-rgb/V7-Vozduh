# E32.1.4 Class Certification Requirements

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

class_certification_requirements_defined=true

## Requirements By Class

| Class | Required Validation | Required Execution Proof | Required Confidence |
| --- | --- | --- | --- |
| CLASS_1 | readiness, restore-settle, runtime checkers, long-window | one-user forward, observation, rollback, replay denial | HIGH |
| CLASS_2 | two-user target-local or inherited pressure, long-window | two-user forward, observation, rollback, replay denial | HIGH |
| CLASS_4 | four-user target-local pressure, long-window | four-user forward, observation, rollback, replay denial | HIGH |
| CLASS_10 | ten-user target-local pressure, long-window | ten-user forward, observation, rollback, replay denial | HIGH |
| CLASS_20 | 20-user target-local pressure, long-window, audit/rollback volume review | 20-user forward, observation, rollback, replay denial | HIGH after proof |
| CLASS_50 | CLASS_50 pressure validation and production-pool architecture controls | exact or approved staged proof | HIGH after proof |
| CLASS_100 | CLASS_100 pressure validation and production-pool architecture controls | exact or approved staged proof | HIGH after proof |

## Mandatory Cross-Class Requirements

Every class certification requires:

- exact class size;
- exact allowed user set;
- exact target;
- rollback manifest;
- fresh execution-time recheck;
- target readiness GO;
- restore-settle GO;
- runtime checkers OK;
- no hidden movers;
- selected moves zero before execution;
- delayed monitoring after rollback;
- replay denial;
- audit chain validation.

## Candidate Versus Certified

Target-local and long-window validation can make a class a candidate with MEDIUM confidence. It cannot make it certified without governed movement, rollback, replay, and audit proof.

