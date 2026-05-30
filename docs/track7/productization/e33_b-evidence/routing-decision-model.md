# E33.B Routing Decision Model

routing_decision_model_defined=true

## Purpose

Routing Intelligence produces recommendations and proposals. It never executes movement, mutates runtime, changes routing, applies autoswitch, consumes packets, or bypasses Governance Control Plane.

## Decision Types

| Decision | Purpose | Trigger | Required Evidence | Confidence Requirement | Governance Path |
| --- | --- | --- | --- | --- | --- |
| NO_ACTION | Keep current user-target assignment. | Current user-specific health is OK, no better safe target, or movement benefit is too small. | Current target quality, required_services health, load, incident state. | MEDIUM or higher for explicit keep; LOW may become OBSERVE. | No execution path. Stored as observation only. |
| OBSERVE | Collect more evidence before proposing movement. | Missing, stale, weak, or contradictory signals. | Signal inventory and missing-evidence reason. | LOW or UNKNOWN. | No execution path. May create monitoring task for future RI pass. |
| MOVEMENT_PROPOSAL | Suggest moving affected user set to a better target. | Current target is degraded for required_services and candidate target is user-specific OK. | Required services, current health, candidate health, target quality, expected benefit, rollback recommendation. | HIGH for direct approval path; MEDIUM requires review. | Batch -> Policy -> Capacity -> Concurrency -> Scheduling -> Execution-Time Recheck -> Execution. |
| EVACUATION_PROPOSAL | Suggest moving users away from failing target. | Target down, required service fail, severe target degradation, or capacity conflict. | Failure proof, affected users, target state, alternate candidates, rollback/containment recommendation. | MEDIUM may be acceptable with human review; HIGH for normal path. | Same governance path; never direct mutation. |
| REBALANCE_PROPOSAL | Suggest redistributing users for load or service affinity. | Target load imbalance, capacity pressure, or better service-affinity distribution. | Load, capacity, current/candidate service health, anti-flap state, expected benefit. | HIGH or VERY_HIGH unless operator manually requests review. | Same governance path; policy and capacity may deny. |
| REVIEW_REQUIRED | Require operator inspection before proposal can proceed. | Large blast radius, low confidence, conflicting evidence, sensitive route class, unknown services, policy ambiguity. | Reason list and exact missing/contradictory signals. | Any confidence. | No execution until operator approval creates/permits a governed batch. |

## Decision Order

1. Evaluate required_services for each user and each candidate target.
2. Evaluate current route health and target degradation.
3. Evaluate candidate target health, capacity, policy eligibility, and incident state.
4. Apply flapping protection and safety suppression.
5. Select the safest decision:
   - hard failure with safe alternate -> EVACUATION_PROPOSAL or REVIEW_REQUIRED;
   - clear service improvement -> MOVEMENT_PROPOSAL;
   - load-only improvement -> REBALANCE_PROPOSAL;
   - missing evidence -> OBSERVE;
   - no useful change -> NO_ACTION.

## Fail-Closed Rules

- Missing required_services does not imply all services are OK.
- SERVICE_UNKNOWN is not OK for a high-confidence proposal.
- Global target OK cannot override user-specific required service failure.
- If governance path cannot be attached, output REVIEW_REQUIRED or OBSERVE.

routing_decision_model_defined=true
