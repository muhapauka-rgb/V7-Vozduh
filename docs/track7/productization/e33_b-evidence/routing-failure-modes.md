# E33.B Routing Failure Modes

routing_failure_modes_defined=true

## Failure Inventory

| Failure Mode | Detection | Impact | Operator Action | Fail-Closed Behavior |
| --- | --- | --- | --- | --- |
| FALSE_DEGRADATION | Later probes contradict degradation or operator marks false positive. | Proposal confidence drops; duplicate proposals suppressed. | Inspect evidence and mark false positive if confirmed. | No automatic movement. |
| FALSE_RECOVERY | Service appears recovered briefly but degradation returns. | NO_ACTION may be unsafe if accepted too early. | Extend observation window. | Recovery requires stable evidence before suppressing evacuation. |
| INSUFFICIENT_EVIDENCE | Missing samples, stale service health, unknown target quality. | Cannot justify movement. | Collect evidence. | OBSERVE or REVIEW_REQUIRED only. |
| CONFLICTING_SIGNALS | Service matrix, sentinel, quality, or operator feedback disagree. | Confidence cannot be HIGH. | Human review. | No high-confidence proposal. |
| LOW_CONFIDENCE | Confidence model yields LOW. | Proposal cannot proceed as executable. | Observe, collect evidence, or manually deny. | Deny execution path. |
| FLAPPING_RISK | Recent A/B reversal or repeated duplicate proposals. | Movement may create oscillation. | Wait, review, or pin suppression. | Suppress proposal or require review. |
| SERVICE_HEALTH_UNKNOWN | Required service lacks fresh target evidence. | User-target OK cannot be proven. | Run service validation or require review. | SERVICE_UNKNOWN is not OK. |
| REQUIRED_SERVICES_UNKNOWN | User service requirements are absent or malformed. | User-specific target health cannot be computed. | Fix metadata. | USER_TARGET_UNKNOWN, no movement proposal. |
| GOVERNANCE_PATH_MISSING | Proposal cannot attach batch/policy/capacity/concurrency/scheduling path. | Unsafe to execute. | Repair architecture/config. | Proposal remains non-executable. |

## Containment Rules

- Failure modes may produce observations, alerts, or review items.
- Failure modes cannot produce direct runtime mutation.
- Rollback recommendations remain advisory until governed execution exists.
- If routing failure mode affects evidence integrity, proposal confidence must be LOW.

routing_failure_modes_defined=true
