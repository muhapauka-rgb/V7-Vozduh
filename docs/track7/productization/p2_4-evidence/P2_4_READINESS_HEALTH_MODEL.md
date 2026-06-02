# P2.4 Readiness Health Model

## Result

readiness_health_model_implemented=true

## Categories

| Health | Criteria | Operator Meaning |
| --- | --- | --- |
| READY | All preview gates pass. | No blocker is visible in preview. |
| READY_WITH_REVIEW | No failed gate exists, but review remains. | Operator review is still required. |
| BLOCKED | At least one validation gate fails closed. | Execution must not proceed. |
| DEGRADED | Trust, policy, or runtime evidence is incomplete but inspectable. | Continue review before readiness can be trusted. |
| UNKNOWN | No draft or no readable gate state exists. | Collect evidence or create proposal-derived draft. |

## Implementation

`execution_health_from_readiness` derives the health model from P2.3 readiness without changing the underlying readiness contract.
