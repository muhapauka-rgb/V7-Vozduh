# End-to-End Operation Timeline and Gap Impact

## Final Lifecycle Timelines

### Successful Movement

`CREATED`
-> `PLANNED`
-> `REVIEW_REQUIRED`
-> `APPROVED`
-> `READY`
-> `EXECUTING`
-> `VERIFYING`
-> `COMPLETED`
-> `AUDITED`
-> `CLOSED`

### Autonomous No-Op

`CREATED`
-> `PLANNED`
-> `COMPLETED`
-> `AUDITED`
-> `CLOSED`

### Denied / Blocked No-Op

`CREATED`
-> `PLANNED`
-> `DENIED`
-> `AUDITED`
-> `CLOSED`

### Failure With Rollback

`CREATED`
-> `PLANNED`
-> `APPROVED`
-> `READY`
-> `EXECUTING`
-> `VERIFYING`
-> `ROLLBACK_READY`
-> `ROLLING_BACK`
-> `ROLLED_BACK`
-> `AUDITED`
-> `CLOSED`

### Failure Without Successful Rollback

`CREATED`
-> `PLANNED`
-> `APPROVED`
-> `READY`
-> `EXECUTING`
-> `VERIFYING`
-> `FAILED_CLOSED`
-> `AUDITED`
-> `CLOSED`

### Cancelled / Expired

`CREATED`
-> `PLANNED`
-> `CANCELLED`
-> `AUDITED`
-> `CLOSED`

`CREATED`
-> `PLANNED`
-> `EXPIRED`
-> `AUDITED`
-> `CLOSED`

## Orchestrator Gap Impact

| Lifecycle Piece | Already Exists? | Needs Ownership Wiring Only? | Requires Future Implementation? | No Work? |
|---|---:|---:|---:|---:|
| Planner | yes | no | no | mostly |
| Selected moves | yes, in autoswitch | yes, for audit/closure references | maybe for canonical operation linkage | no |
| Restore-barrier validation | yes | yes, for lifecycle creation/closure | maybe | no |
| Runtime recheck | partial | yes | likely for global/manual paths | no |
| Execution | yes | yes, to reduce bypasses | maybe | no |
| Verification | yes | yes | maybe | no |
| Movement rollback | yes, local | yes | maybe for non-autoswitch/generic paths | no |
| Generic rollback | yes | yes | no new engine | no |
| Audit sink | yes | yes | maybe event coverage expansion | no |
| Closure model | yes | yes | maybe linkage to runtime outcomes | no |
| Runtime terminal state semantics | partial | yes | likely as mapping/wiring | no |
| No-op lifecycle | partial | yes | likely event/closure coverage | no |
| Operation identity | partial/historical | yes | likely if later implementation proceeds | no |

## Missing Pieces

- single semantic operation identity across plan/apply/audit/closure;
- canonical terminal state mapping from autoswitch apply result;
- guaranteed audit event for every terminal runtime operation;
- closure blocker logic for insufficient audit/rollback evidence;
- no-op audit/closure coverage;
- restore-barrier lifecycle audit linkage;
- manual/direct path lifecycle mapping.

## Existing Pieces Needing No New Owner

- runtime owner remains autoswitch;
- scheduler remains systemd;
- audit sink remains `v7-audit-log`;
- closure owner remains Admin/operator observability;
- proposal/evidence/gate states remain supporting states, not operation terminal states.

## Truth Source Audit

No duplicate lifecycle truth:

- lifecycle semantic truth is derived from runtime owner terminal state, audit evidence, and closure record.

No duplicate operation truth:

- Runtime Operation is semantic composition of existing artifacts; Z6.5 does not create storage/API truth.

No duplicate closure truth:

- closure truth remains Admin closure records/operator observability.

No duplicate rollback truth:

- movement rollback truth remains runtime owner; generic rollback primitive supplies command result only.

No duplicate audit truth:

- audit truth remains `v7-audit-log`.

