# E32.1.4 Failure Handling

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

failure_handling_defined=true

## Default

Any validation failure fails closed for forward movement.

Rollback remains allowed as containment when exact rollback scope is known.

## Failure Matrix

| Failure | Result | Required Response |
| --- | --- | --- |
| Throughput below pressure floor | CANDIDATE or DEGRADED | Investigate quality, rerun after safe remediation, no promotion. |
| Long-window floor breach | DEGRADED | Quality recovery or replacement target. |
| Readiness not GO | DEGRADED | Diagnose readiness, no packet generation. |
| Restore-settle not GO | DEGRADED | Stop movement, investigate selected moves/hidden movers/checkers. |
| Runtime checker failure | DEGRADED | Remediate platform issue before validation continues. |
| Hidden movers detected | DEGRADED or REVOKED | Stop, classify cause, audit investigation. |
| Selected moves nonzero | DEGRADED | Stop until restore-settle returns GO. |
| Rollback failure | REVOKED unless fully contained | Incident review and full recertification. |
| Replay failure | REVOKED | Governance defect, no forward movement. |
| Audit inconsistency | REVOKED or EXPIRED | Audit repair/review before any certification. |
| Missing evidence | EXPIRED or UNKNOWN | Reconstruct or rerun validation. |

## Repeated Failure

Repeated quality failures at the same class imply:

- class remains uncertified;
- prior lower class may remain only if not implicated;
- replacement target strategy should be prepared.

## Evidence Preservation

Failed validation is still evidence. It must be recorded with:

- timestamp;
- failure class;
- root-cause classification if known;
- whether runtime was mutated;
- whether rollback was needed;
- next safe action.

