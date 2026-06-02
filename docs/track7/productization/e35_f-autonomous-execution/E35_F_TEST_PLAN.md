# E35.F Test Plan

## Architecture Tests

- lifecycle state transition consistency;
- execution contract schema completeness;
- validation gate completeness;
- verification requirement completeness;
- rollback scope completeness;
- observability placement consistency;
- event taxonomy consistency;
- safety invariant scan.

## Future P2 Functional Tests

| Test | Expected |
|---|---|
| AUTO execution with all gates GO | ALLOW in dry-run, later bounded execute |
| OPERATOR_PINNED forward attempt | DENY or REVIEW_REQUIRED |
| MANUAL forward attempt | DENY unless explicit operator contract |
| Conflict present | REVIEW_REQUIRED or DENY |
| Review required | No execution |
| Rollback manifest missing | DENY |
| Runtime trust stale | DENY |
| Release trust unknown | REVIEW_REQUIRED/DENY by policy |
| Capacity stale | DENY |
| Selected moves nonzero | DENY |
| Hidden movers present | DENY |
| Store unreadable | DENY |
| Evaluator mismatch | DENY/REVIEW_REQUIRED |
| Conflict resolver mismatch | REVIEW_REQUIRED |
| Replay contract | DENY |
| Verification success | COMPLETED or ROLLBACK_READY |
| Verification failure | ROLLBACK_READY/FAILED_CLOSED |
| Rollback success | ROLLED_BACK |
| Rollback failure | CONTAINMENT_REQUIRED |

## Static Checks For This Block

- marker scan for required verdicts;
- no runtime mutation wording scan;
- `git diff --check`;
- no command execution helpers added;
- no user movement commands run.

test_plan_defined=true
runtime_mutation_performed=false
