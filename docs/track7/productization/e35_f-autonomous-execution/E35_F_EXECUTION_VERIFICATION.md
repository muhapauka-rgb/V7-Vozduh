# E35.F Execution Verification

## Purpose

Execution Verification proves that an action completed exactly as contracted and caused no unauthorized side effects.

Verification starts after execution completes or after rollback completes.

## Forward Verification

Forward verification must prove:

- every approved user moved to the approved target;
- no unapproved user moved;
- no route table outside scope changed;
- target users count changed by exactly the approved movement count;
- route-get for each user matches the approved target path;
- required services are available on the target for affected users;
- target readiness remains GO or accepted observation state;
- selected moves remains zero;
- hidden movers remain absent;
- runtime checkers remain OK;
- audit record exists and references the contract.

## Rollback Verification

Rollback verification must prove:

- every affected user returned to the rollback target specified in the contract;
- no unapproved user changed;
- route tables restored to expected rollback state;
- target users count decreased by exact rollback count;
- route-get restored;
- restore-settle returns GO;
- selected moves remains zero;
- hidden movers remain absent;
- rollback audit record exists.

## Verification Failure Handling

| Failure | Required action |
|---|---|
| Approved user did not move | Enter rollback/containment review |
| Unapproved user moved | Immediate containment, operator review |
| Route table mismatch | Rollback if safe, otherwise containment |
| Required service unavailable | Rollback or REVIEW_REQUIRED depending scope |
| Hidden mover observed | Fail closed, containment review |
| Audit missing | Fail closed, block closure |
| Rollback verification failed | Escalate to containment and human review |

## Verification Verdict

verification_model_defined=true
runtime_mutation_performed=false
