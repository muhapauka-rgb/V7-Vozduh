# E35.F Event Model

## Event Families

Execution events are append-only, audit-linked, and evidence-linked.

## Core Events

| Event | Meaning |
|---|---|
| `EXECUTION_CANDIDATE_CREATED` | Candidate shaped from proposal |
| `EXECUTION_CONTRACT_CREATED` | Contract generated |
| `EXECUTION_VALIDATION_STARTED` | Pre-execution validation began |
| `EXECUTION_VALIDATED` | Validation passed |
| `EXECUTION_DENIED` | Validation denied |
| `EXECUTION_REVIEW_REQUIRED` | Review required |
| `EXECUTION_RECHECK_STARTED` | Final runtime recheck began |
| `EXECUTION_RECHECK_PASSED` | Final recheck passed |
| `EXECUTION_RECHECK_FAILED` | Final recheck failed |
| `EXECUTION_STARTED` | Runtime action started |
| `EXECUTION_COMPLETED` | Runtime action completed |
| `EXECUTION_FAILED` | Runtime action failed |
| `VERIFICATION_STARTED` | Verification began |
| `VERIFICATION_COMPLETED` | Verification passed |
| `VERIFICATION_FAILED` | Verification failed |
| `OBSERVATION_STARTED` | Observation window began |
| `OBSERVATION_SAMPLE_RECORDED` | Observation sample recorded |
| `OBSERVATION_COMPLETED` | Observation window passed |
| `ROLLBACK_READY` | Rollback is available |
| `ROLLBACK_CREATED` | Rollback action created |
| `ROLLBACK_STARTED` | Rollback started |
| `ROLLBACK_COMPLETED` | Rollback completed |
| `ROLLBACK_FAILED` | Rollback failed |
| `REPLAY_DENIED` | Consumed/expired contract replay denied |
| `EXECUTION_CLOSED` | Closure completed |

## Event Fields

Required fields:

- event_id;
- event_type;
- timestamp;
- actor_type;
- actor_id;
- contract_id;
- batch_id;
- evidence_bundle_ids;
- proposal_id;
- authority_verdict_id;
- affected_users;
- affected_targets;
- result;
- reason;
- source_hashes;
- audit_hash.

## Retention

- active execution events: retain until closure plus 365 days;
- failed/rollback/emergency events: retain 730 days;
- summaries: retain indefinitely unless archived with hash-preserving manifest.

event_model_defined=true
