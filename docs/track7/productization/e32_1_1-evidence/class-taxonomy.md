# E32.1.1 Class Taxonomy

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

class_taxonomy_defined=true

## Class List

| Class | Meaning | Allowed Batch Size | Current Status For `amneziawg-exec-20260528-10-8-1-14` |
| --- | --- | ---: | --- |
| UNCERTIFIED | No safe governed movement proof. | 0 | Superseded |
| CLASS_1 | One-user governed movement certified. | 1 | Certified historically |
| CLASS_2 | Two-user governed movement certified. | 2 | Certified historically |
| CLASS_4 | Four-user small cohort certified. | 4 | Certified historically |
| CLASS_10 | Ten-user governed cohort certified. | 10 | Current certified class |
| CLASS_20_CANDIDATE | Candidate class for 20-user scale. | 20 max only after certification | Not certified |
| CLASS_50_CANDIDATE | Candidate class for 50-user scale. | 50 max only after certification | Not certified |
| CLASS_100_CANDIDATE | Candidate class for 100-user scale. | 100 max only after certification | Not certified |
| PRODUCTION_POOL | Policy-controlled production pool class. | Policy-controlled | Architecture target |

## CLASS_1

Meaning: target has proven one approved user can move forward and roll back under governance.

Required evidence:

- one-user approval packet;
- fresh execution-time recheck;
- exact one-user forward proof;
- exact rollback proof;
- delayed monitoring;
- replay denial;
- restore-settle GO;
- runtime checkers OK.

Required validation window:

- target readiness GO before execution;
- post-rollback restore-settle GO;
- delayed monitoring after rollback.

Expiration/staleness:

- stale if target readiness is no longer GO;
- stale if registry/egress hash drift invalidates packet-bound assumptions;
- stale if target metadata changes without revalidation.

Downgrade triggers:

- rollback failure;
- replay acceptance;
- hidden mover detected;
- selected moves nonzero before execution.

## CLASS_2

Meaning: target has proven two approved users can move forward and roll back as a bounded batch.

Required evidence:

- all CLASS_1 requirements;
- two-user capacity metadata;
- two-user approval packet;
- exact two-user forward and rollback proof;
- no third-user movement.

Allowed batch size: 2.

Downgrade triggers:

- target hard limit below 2;
- runtime checkers fail under two-user state;
- delayed monitoring detects unapproved movement.

## CLASS_4

Meaning: target has proven a four-user small cohort can move forward and roll back.

Required evidence:

- all CLASS_2 requirements;
- four-user target-local capacity validation;
- long-window readiness above floor;
- four-user approval packet;
- exact four-user forward and rollback proof;
- no fifth-user movement.

Allowed batch size: 4.

Downgrade triggers:

- target hard limit below 4;
- no-sample-below-floor proof expires;
- readiness oscillates under class validation.

## CLASS_10

Meaning: target has proven a ten-user cohort can move forward and roll back.

Required evidence:

- all CLASS_4 requirements;
- ten-user candidate pool;
- ten-stream target-local validation;
- post-requalification long window;
- ten-user approval packet;
- exact ten-user forward and rollback proof;
- no eleventh-user movement;
- replay denial after execution.

Allowed batch size: 10.

Current evidence:

- E30.2 capacity requalification passed.
- E30.3 ten-user governed movement passed.
- E31 certified production-grade governance up to 10 users.

Downgrade triggers:

- hard_limit below 10;
- target readiness NO-GO;
- runtime checker failure;
- audit or replay proof invalid;
- evidence staleness policy exceeded.

## CLASS_20_CANDIDATE

Meaning: architecture candidate for the next scale proof.

Required evidence before certification:

- 20-user candidate pool;
- target-local 20-stream validation;
- long-window validation;
- hard_limit and soft_limit requalification to 20;
- 20-user approval packet;
- 20-user forward, observation, rollback, delayed monitoring, replay denial.

Allowed batch size before certification: 0 for execution; 20 only for model/prep.

## CLASS_50_CANDIDATE

Meaning: architecture candidate for larger production-like cohorts.

Required evidence before certification:

- prior CLASS_20 certification or explicit architecture waiver;
- 50-user candidate pool;
- target-local 50-stream validation;
- audit-volume validation;
- rollback-volume validation;
- concurrency risk review.

Allowed batch size before certification: 0 for execution; 50 only for model/prep.

## CLASS_100_CANDIDATE

Meaning: high-scale candidate requiring production-pool controls.

Required evidence before certification:

- prior CLASS_50 certification or production-pool policy certification;
- batching controls;
- audit-volume controls;
- rollback orchestration;
- operator error guardrails;
- concurrency controls.

Allowed batch size before certification: 0 for execution; 100 only for model/prep.

## PRODUCTION_POOL

Meaning: target is governed by production-pool policy instead of a single hard-coded proof class.

Required evidence:

- capacity class engine;
- policy-defined batch size;
- scheduling and concurrency controls;
- class staleness enforcement;
- operator workflow controls;
- audit/replay volume controls;
- rollback orchestration.

Allowed batch size:

- not fixed by taxonomy;
- must be less than or equal to the active policy cap and the target certified class.

Status:

- not certified yet;
- E31 recommends architecture work before additional scale proofs.

