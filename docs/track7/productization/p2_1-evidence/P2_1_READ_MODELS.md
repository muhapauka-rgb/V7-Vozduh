# P2.1 Execution Read Models

## Models Implemented

Execution Summary:
aggregates contracts, active contracts, rollback readiness, failed contracts, event counts, recent contracts, recent events, and consistency status.

Execution Contract Detail:
returns one contract with related timeline, events, verification summary, and rollback summary.

Execution Timeline:
combines contract records and event records into a chronological read model.

Execution Verification:
summarizes verification state and verification-related events.

Execution Rollback:
summarizes rollback state, rollback manifest, and rollback events.

Execution Explain:
operator explanation of what P2.1 can and cannot do.

## Non-Authority Rule

Every read model states or implies:

- read-only
- non-authoritative
- execution not allowed now
- no runtime mutation path

## Verdict

read_models_implemented=true
runtime_mutation_performed=false
