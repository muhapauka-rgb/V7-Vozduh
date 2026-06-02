# P2.6 Candidate Lifecycle

## Result

candidate_lifecycle_implemented=true

## States

- DISCOVERED
- CANDIDATE
- VALIDATING
- READY_FOR_REVIEW
- BLOCKED
- READY_FOR_CONTRACT
- ARCHIVED
- EXPIRED

## Current Derivation

P2.6 derives lifecycle from validation and readiness forecast:

- failed gates -> BLOCKED;
- review or unknown gates -> READY_FOR_REVIEW;
- no blockers or reviews -> READY_FOR_CONTRACT;
- expired or archived draft status -> EXPIRED or ARCHIVED.

## Boundary

Lifecycle is a preview state only. It does not schedule, approve, or execute.
