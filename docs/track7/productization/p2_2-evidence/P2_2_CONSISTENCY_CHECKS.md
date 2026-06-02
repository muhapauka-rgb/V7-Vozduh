# P2.2 Consistency Checks

## Checks Implemented

Implemented consistency checks for:

- Proposal to Contract Draft
- Authority to Contract Draft
- Evaluator to Validation Preview
- Conflict Resolver to Validation Preview
- Contract to Verification Preview
- Contract to Rollback Preview

## Fail-Closed Conditions

Preview fails closed when:

- proposal reference is missing
- evidence reference is missing
- movement target is missing
- movement budget does not match affected user count
- validation preview contains FAIL
- verification preview contains FAIL
- rollback preview contains FAIL

## Safety

Consistency checks do not repair state.
Consistency checks do not create events.
Consistency checks do not mutate runtime.

## Verdict

consistency_checks_implemented=true
fail_closed_behavior_implemented=true
runtime_mutation_performed=false
