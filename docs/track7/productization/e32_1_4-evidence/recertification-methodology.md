# E32.1.4 Recertification Methodology

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

recertification_methodology_defined=true

## STALE Recertification

Minimum evidence:

- readiness GO;
- restore-settle GO;
- runtime checkers OK;
- selected moves zero;
- hidden movers absent;
- class-appropriate long-window refresh.

Confidence effect:

- preserves confidence if no degradation occurred;
- evidence timestamps refresh.

## DEGRADED Recertification

Minimum evidence:

- root-cause classification;
- safe remediation evidence;
- target-local validation if quality/capacity was implicated;
- long-window validation;
- readiness GO;
- restore-settle GO;
- runtime checkers OK.

Confidence effect:

- confidence may be reduced until a new governed movement proof succeeds;
- repeated degradation blocks promotion.

## EXPIRED Recertification

Minimum evidence:

- full validation sequence for the target class;
- evidence schema/version compatibility;
- long-window validation;
- execution proof if historical proof cannot be trusted for current runtime.

Confidence effect:

- restored only after full evidence acceptance.

## REVOKED Recovery

Minimum evidence:

- incident review;
- root-cause fix;
- full certification path from CANDIDATE;
- operator plus evidence authority approval.

Confidence effect:

- starts LOW or MEDIUM;
- cannot return directly to HIGH without execution proof.

