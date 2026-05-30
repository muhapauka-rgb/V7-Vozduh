# E32.5.B Admission Model

scheduler_admission_defined=true

## Queue Admission Purpose

Scheduler admission decides whether a prepared batch may enter the scheduling queue. It does not authorize execution and does not mutate runtime.

## Admission Requirements

A batch may enter queue only when:

- batch exists;
- batch metadata is valid;
- batch scope is explicit;
- rollback manifest is complete;
- policy admission is not DENY;
- capacity is not impossible for requested batch size;
- target is not revoked;
- no hard conflict is known;
- audit lineage exists;
- schedule metadata is complete;
- schedule type is allowed for the batch;
- dependencies are representable and acyclic;
- packet strategy is defined.

## Admission Outcomes

| Outcome | Meaning | Effect |
| --- | --- | --- |
| ADMIT | Batch may enter queue. | Schedule becomes QUEUED. |
| DENY | Batch cannot enter queue. | Schedule becomes FAILED_CLOSED or remains DRAFT. |
| WAIT | Batch is structurally valid but waiting for window/dependency/lock/reservation state. | Schedule becomes appropriate waiting state. |
| REVIEW_REQUIRED | Human review is required before queue admission. | Schedule is blocked. |

## Admission Denials

Queue admission is denied when:

- policy returns DENY;
- rollback manifest is missing;
- batch scope is unknown;
- target capacity is impossible;
- schedule window has already expired;
- dependency graph is cyclic;
- audit lineage is missing;
- emergency schedule lacks emergency authority;
- queue admission would require runtime mutation.

## Decision

scheduler_admission_defined=true
