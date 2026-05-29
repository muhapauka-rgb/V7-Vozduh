# E32.1.3 Promotion Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

promotion_model_defined=true

## General Promotion Rule

A target is promoted only when the requested class has complete evidence:

- target-local pressure validation for the requested class;
- long-window readiness above floors;
- runtime checkers OK;
- restore-settle GO;
- exact approval packet for requested class size;
- execution-time recheck;
- exact forward proof;
- exact rollback proof;
- delayed monitoring;
- replay denial;
- audit chain valid;
- capacity metadata updated after evidence, not before evidence.

Promotion never occurs from metadata alone.

## CLASS_1 To CLASS_2

Required evidence:

- two eligible users with deterministic rollback;
- target hard limit at least 2;
- readiness GO;
- restore-settle GO;
- two-user approval packet;
- exact two-user forward and rollback;
- no third-user movement;
- replay denial.

Required confidence: HIGH after successful two-user execution proof.

## CLASS_2 To CLASS_4

Required evidence:

- four eligible users;
- four-stream or equivalent target-local validation;
- long-window readiness;
- hard limit requalified to at least 4;
- four-user approval packet;
- exact four-user forward and rollback;
- no fifth-user movement;
- replay denial.

Required confidence: HIGH after successful four-user execution proof.

## CLASS_4 To CLASS_10

Required evidence:

- ten-user candidate pool;
- ten-stream target-local validation;
- post-requalification long-window validation;
- hard limit requalified to at least 10;
- ten-user approval packet;
- exact ten-user forward and rollback;
- no eleventh-user movement;
- replay denial.

Required confidence: HIGH after successful ten-user execution proof.

## CLASS_10 To CLASS_20

Required evidence:

- 20-user candidate pool;
- target-local 20-stream validation;
- long-window validation under class-appropriate pressure;
- audit volume review;
- rollback set review;
- hard limit requalified to at least 20;
- 20-user approval packet;
- exact 20-user forward and rollback;
- delayed monitoring;
- replay denial.

Required confidence before execution: MEDIUM.

Required confidence after execution: HIGH.

## CLASS_20 To CLASS_50

Required evidence:

- prior CLASS_20 certification;
- 50-user candidate pool;
- 50-stream or production-equivalent load validation;
- audit volume and storage review;
- rollback orchestration review;
- operator workflow review;
- concurrency risk review;
- exact 50-user governed proof or approved production-pool staged proof.

Required confidence before execution: MEDIUM.

Required confidence after execution: HIGH.

## CLASS_50 To CLASS_100

Required evidence:

- prior CLASS_50 certification;
- 100-user candidate pool or production-pool eligibility model;
- production-pool policy controls;
- scheduling controls;
- reservation ledger controls;
- rollback orchestration;
- audit/replay volume controls;
- exact 100-user governed proof or approved staged production-pool certification.

Required confidence before execution: MEDIUM.

Required confidence after execution: HIGH.

## Product Decision Boundary

For CLASS_50 and CLASS_100, exact all-at-once movement may be less safe than staged production-pool certification. This requires an explicit architecture decision in the authority model rather than an implicit assumption.

