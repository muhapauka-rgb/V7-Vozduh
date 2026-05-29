# E32.1.6 Status Visibility Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

status_visibility_defined=true

## Status Semantics

| Status | Display State | Meaning | Forward Action | Operator Action |
| --- | --- | --- | --- | --- |
| CERTIFIED | Green / Eligible | Capacity can be used if all runtime gates pass. | Allowed only after recheck. | Prepare packet, view evidence, run refresh. |
| STALE | Amber / Refresh Required | Historical proof exists but freshness expired. | Denied. | Refresh validation. |
| DEGRADED | Red / Degraded | Quality, readiness, checker, or isolation problem. | Denied. | Diagnose/remediate, recertify. |
| EXPIRED | Red / Expired | Evidence beyond hard expiry or incompatible. | Denied. | Full recertification. |
| REVOKED | Red / Incident | Certification invalidated by governance/safety defect. | Denied. | Incident review, containment. |
| CANDIDATE | Blue / Prep Only | Candidate capacity, not executable. | Denied. | Validate. |
| VALIDATING | Blue / In Progress | Evidence collection or review in progress. | Denied for new class. | Continue validation. |
| UNKNOWN | Gray / Unknown | Capacity cannot be trusted. | Denied. | Discover/inspect. |

## Escalation Rules

- STALE escalates to operator refresh.
- DEGRADED escalates to remediation owner.
- EXPIRED escalates to recertification.
- REVOKED escalates to incident review.

## Safety Copy

Operator-facing status text should be explicit:

- CERTIFIED: "Eligible only if execution-time recheck passes."
- STALE: "Historical certification exists; new forward movement blocked until refresh."
- DEGRADED: "Forward movement blocked; rollback/containment may remain available."
- EXPIRED: "Full recertification required."
- REVOKED: "Incident review required; no forward movement."

