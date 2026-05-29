# E32.1.4 Validation Stages

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

validation_stages_defined=true

## STAGE_0_DISCOVERY

Purpose: identify target and candidate class.

Required evidence:

- target metadata;
- current class/status;
- current readiness;
- current runtime checker state;
- prior evidence inventory.

Pass criteria:

- target exists;
- target role and isolation are understood;
- no contradiction with existing certification.

Fail criteria:

- missing target identity;
- metadata contradiction;
- governance isolation unknown.

## STAGE_1_TARGET_LOCAL

Purpose: validate class-sized pressure without user movement.

Required evidence:

- class-sized parallel probe;
- aggregate avg/min Mbps;
- per-stream minimum when available;
- readiness after probe;
- runtime checkers after probe;
- selected moves zero;
- hidden movers absent.

Pass criteria:

- pressure floors pass;
- readiness remains GO;
- runtime checkers remain OK.

Fail criteria:

- aggregate min below class floor;
- readiness NO-GO;
- runtime checker failure.

## STAGE_2_LONG_WINDOW

Purpose: validate sustained quality and stability.

Required evidence:

- 20-30 minute window or documented equivalent;
- at least 20 samples for current V7 block pattern;
- avg/min Mbps;
- readiness per sample;
- no sample below floor;
- target users expected;
- selected moves zero;
- hidden movers absent;
- runtime checkers OK.

Pass criteria:

- readiness all GO;
- min Mbps above floor;
- no sample below floor;
- runtime remains clean.

Fail criteria:

- readiness oscillation;
- quality floor breach;
- hidden mover or selected move appears.

## STAGE_3_EXECUTION_PROOF

Purpose: prove class-sized governed movement and rollback.

Required evidence:

- approval packet;
- execution-time recheck;
- exact forward proof;
- observation window;
- exact rollback proof;
- post-rollback restore-settle;
- delayed monitoring;
- replay denial.

Pass criteria:

- only approved users moved;
- route mutation limited to approved users;
- rollback succeeds;
- replay denied;
- runtime checkers OK.

Fail criteria:

- blast radius breach;
- rollback failure;
- replay accepted;
- delayed movement observed.

## STAGE_4_CERTIFICATION

Purpose: accept evidence and update certification status.

Required evidence:

- stage 1, 2, and 3 pass;
- audit chain valid;
- report created;
- capacity metadata decision recorded.

Pass criteria:

- `capacity_status=CERTIFIED`;
- confidence assigned;
- next class or program decision recorded.

Fail criteria:

- missing evidence;
- contradictory evidence;
- authority rejects certification.

## STAGE_5_RECERTIFICATION

Purpose: refresh stale/degraded/expired targets.

Required evidence:

- depends on prior state;
- at minimum readiness, restore-settle, runtime checkers, and class-appropriate validation.

Pass criteria:

- cause resolved;
- evidence freshness restored.

Fail criteria:

- cause unknown;
- validation repeats failure;
- rollback/replay/audit chain compromised.

