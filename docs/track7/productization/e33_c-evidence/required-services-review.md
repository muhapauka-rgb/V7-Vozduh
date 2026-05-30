# E33.C Required Services Review

required_services_integrated=true

## Reviewed Requirement

`required_services` must remain first-class inputs in Routing Intelligence.

## Integration Points

| Point | Required Services Effect | Result |
| --- | --- | --- |
| service influence | Required services determine which service health must be evaluated. | VALID |
| target selection influence | A target must satisfy the user's required services before it can be user-specific OK. | VALID |
| proposal influence | Proposals must include required services by user and related service evidence. | VALID |
| confidence influence | Missing, stale, unknown, or failed required service evidence lowers confidence or forces review/observation. | VALID |

## Certified Rules

- required_services are not decorative UI metadata.
- required_services affect user-specific target health.
- SERVICE_UNKNOWN is not OK.
- REQUIRED service failure blocks high-confidence movement proposal.
- Missing required_services produces USER_TARGET_UNKNOWN or REVIEW_REQUIRED/OBSERVE.

## Decision

required_services are correctly integrated into the architecture and preserved through foundation, operations, proposal, and governance compatibility.

required_services_integrated=true
