# E33.C User-Specific Health Review

user_specific_health_preserved=true

## Reviewed Principle

A target can be globally healthy while unhealthy for a specific user.

Example:

```text
target_global_quality=OK
user.required_services=["youtube","telegram","instagram"]
target.youtube=SERVICE_OK
target.telegram=SERVICE_FAIL
target.instagram=SERVICE_OK
user_specific_health=USER_TARGET_FAIL
```

## Certified Health States

| State | Meaning | Proposal Effect |
| --- | --- | --- |
| USER_TARGET_OK | Global target quality and user required services are healthy. | Candidate may be considered. |
| USER_TARGET_DEGRADED | Target works but some important/non-required signals are weak. | Observe, review, or lower confidence. |
| USER_TARGET_FAIL | Required service, target, policy, or capacity makes target unsuitable. | Do not propose as positive target. |
| USER_TARGET_UNKNOWN | Required service metadata or service evidence is missing/stale/contradictory. | OBSERVE or REVIEW_REQUIRED. |

## Preservation Across Program

- E33.A defines user-specific health.
- E33.B uses user-specific health in decisions, confidence, proposals, and observability.
- E33.C certifies that global target OK does not imply user-specific OK.

user_specific_health_preserved=true
