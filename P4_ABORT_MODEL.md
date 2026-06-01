# P4 Abort Model

Project: V7 Vozduh
Block: P4 Controlled Runtime Action Planning

## Abort Principle

Any uncertainty aborts. The operator can prepare a new packet from fresh evidence instead of pushing through stale or conflicting facts.

## Abort Reasons

- `STALE_EVIDENCE`
- `MISSING_EVIDENCE`
- `HEALTH_DEGRADED`
- `TRUST_CHANGED`
- `CAPACITY_CHANGED`
- `REQUIRED_SERVICES_CHANGED`
- `CANDIDATE_INVALID`
- `CANDIDATE_EXPIRED`
- `CANDIDATE_BLOCKED`
- `APPROVAL_EXPIRED`
- `DUAL_APPROVAL_INVALID`
- `SCOPE_CHANGED`
- `TARGET_CHANGED`
- `ROLLBACK_UNAVAILABLE`
- `VERIFICATION_MISMATCH`
- `DRYRUN_STALE`
- `OBSERVATION_UNAVAILABLE`
- `REPLAY_RISK`

## Abort Output

Abort output must include:

- abort reason
- changed source refs
- changed hashes
- operator-readable explanation
- safe next step
- whether packet may be refreshed

## Verdict

`abort_model_defined=true`

