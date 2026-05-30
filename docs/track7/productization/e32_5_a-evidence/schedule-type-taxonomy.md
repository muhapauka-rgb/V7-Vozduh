# E32.5.A Schedule Type Taxonomy

schedule_type_taxonomy_defined=true

## Schedule Types

| Type | Purpose | Allowed Use | Forbidden Use | Required Gates | Expiration Rules |
| --- | --- | --- | --- | --- | --- |
| IMMEDIATE | Run as soon as all gates are satisfied. | Operator-approved batch that should dispatch after final readiness. | Bypassing approval, policy, locks, or execution-time recheck. | Batch approved, policy not DENY, capacity sufficient, concurrency clear, packet valid. | Expires with packet or configured immediate TTL. |
| DEFERRED | Run after a specific not_before time. | Known batch held for later execution. | Running before not_before or after not_after. | Same as IMMEDIATE plus time gate. | Expires at not_after or packet expiry, whichever is earlier. |
| WINDOWED | Run inside an execution_window. | Operator or policy-constrained execution windows. | Running outside window. | Same as DEFERRED plus window open. | Expires when window closes. |
| DEPENDENT | Run after one or more parent batches complete. | Sequential batch flows. | Running if dependency fails, expires, cancels, or has unknown result. | Parent terminal success, current gates valid. | Expires when dependency timeout or own not_after is reached. |
| MAINTENANCE | Run only in maintenance window. | Controlled operational work during maintenance. | Production movement outside maintenance window. | Maintenance window valid, batch approved, all gates valid. | Expires at maintenance window end. |
| EMERGENCY | Dispatch urgent containment or exact rollback-oriented action. | Emergency exact-scope containment after human approval. | Broad movement, bypassing audit, expanding scope, or selecting new users/targets. | Emergency approval, exact scope, rollback manifest, audit, locks. | Very short TTL; expires on first failed recheck or window close. |

## Type Selection Rules

- Schedule type must not change allowed users or target.
- Schedule type must not weaken gates.
- Emergency does not bypass governance; it only changes queue priority for exact approved scope.
- Dependent schedules fail closed if parent result is not provably successful.

## Decision

schedule_type_taxonomy_defined=true
