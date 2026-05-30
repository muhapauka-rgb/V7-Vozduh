# E33.B Human Review Model

human_review_model_defined=true

## Purpose

Human review is required when Routing Intelligence can explain a possible movement but cannot safely hand it to automated governance admission without operator judgment.

## Review Outcomes

| Outcome | Meaning |
| --- | --- |
| APPROVE_FOR_GOVERNANCE | Proposal may become a governed batch. |
| REQUEST_MORE_EVIDENCE | Proposal remains observation-only. |
| DENY | Proposal is closed and cannot execute. |
| QUARANTINE_TARGET | Target should be excluded pending remediation. |
| MARK_FALSE_POSITIVE | Feedback lowers confidence for similar future signals. |

## Mandatory Review Triggers

Human review is mandatory for:

- LOW or MEDIUM movement confidence;
- conflicting service health signals;
- unknown required_services;
- SERVICE_UNKNOWN for any REQUIRED service;
- large blast radius above current policy cap;
- evacuation with incomplete candidate evidence;
- rebalance proposal affecting many users;
- sensitive route class or policy ambiguity;
- flapping risk;
- recent operator incident or rollback anomaly.

## Denial Triggers

Proposal must be denied or observation-only when:

- it would bypass Governance Control Plane;
- it would mutate runtime directly;
- required_services stop affecting target selection;
- rollback recommendation is missing;
- proposed target is policy/capacity ineligible;
- service evidence is stale and no fresh validation exists.

## Operator Visibility

Review UI/report must show:

- affected users;
- required services;
- current target and proposed target;
- failed/degraded services;
- confidence and confidence penalties;
- reason for review;
- next safe action;
- governance path if approved.

human_review_model_defined=true
