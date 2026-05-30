# E33.A User-Specific Health Model

user_specific_health_model_defined=true

## Function

```text
user_specific_health(user, target)
```

## Inputs

- required_services;
- service_health per target;
- global target quality;
- user current route;
- target capacity;
- target policy eligibility;
- incident state;
- signal freshness and confidence.

## Outputs

| Output | Meaning | Proposal Impact |
| --- | --- | --- |
| USER_TARGET_OK | Target is globally healthy and all REQUIRED services are OK for user. | Candidate for positive proposal if governance path is clean. |
| USER_TARGET_DEGRADED | Target works but one or more IMPORTANT/OPTIONAL services are degraded, or global quality is degraded. | May propose observation, review, or alternate target. |
| USER_TARGET_FAIL | Required service fails, target is down, or capacity/policy makes target unsuitable. | Do not propose target for user. |
| USER_TARGET_UNKNOWN | Required service list or service evidence is missing/stale/unknown. | Do not assume OK; observation or operator review required. |

## Evaluation Rules

- REQUIRED service SERVICE_FAIL => USER_TARGET_FAIL.
- REQUIRED service SERVICE_UNKNOWN => USER_TARGET_UNKNOWN.
- Missing required_services => USER_TARGET_UNKNOWN.
- Global target fail => USER_TARGET_FAIL.
- Capacity not eligible => USER_TARGET_FAIL for proposal purposes.
- Policy not eligible => USER_TARGET_FAIL for proposal purposes.
- Current route health and candidate target health must both be evaluated.

## Decision

user_specific_health_model_defined=true
