# E33.B Proposal Engine

proposal_engine_defined=true

## Purpose

The proposal engine converts Routing Intelligence decisions into structured proposals for Governance Control Plane. It produces data only. It never mutates runtime.

## Proposal Types

| Type | When Generated | Governance Requirement |
| --- | --- | --- |
| MOVEMENT | A user or bounded group has a better target for required_services and quality. | Must become a governed execution batch. |
| EVACUATION | Current target is failing or unsafe for affected users. | Must pass policy, capacity, concurrency, scheduling, and execution-time recheck. |
| REBALANCE | Load/capacity/service distribution would improve without service regression. | Must pass governance and anti-flap gates. |
| OBSERVATION | Evidence is insufficient for movement. | No execution path; may request more measurement. |

## Required Proposal Fields

```text
proposal_id
proposal_type
created_at
expires_at
affected_users
required_services_by_user
current_target_by_user
proposed_target
candidate_targets
evidence
reason
confidence
expected_benefit
risk_summary
rollback_recommendation
flapping_state
human_review_requirement
governance_path
fail_closed_conditions
```

## Evidence Requirements

Each movement, evacuation, or rebalance proposal must include:

- user-specific required_services;
- current target service health for required services;
- proposed target service health for required services;
- global target quality;
- capacity eligibility signal;
- policy eligibility signal or policy unknown marker;
- concurrency/scheduling assumptions marked as pending;
- rollback recommendation.

## Proposal Generation Rules

- A proposal is generated only when it can name exact affected users and exact candidate targets.
- Any missing required service evidence lowers confidence or forces OBSERVATION/REVIEW_REQUIRED.
- A proposal cannot claim execution eligibility until Governance Control Plane evaluates it.
- Proposal expiration is mandatory; stale proposals must fail closed.
- Duplicate proposals are coalesced by user set, current target, proposed target, service reason, and evidence generation.

## Governance Path

Every executable proposal must declare:

```text
Batch -> Policy -> Capacity -> Concurrency -> Scheduling -> Execution-Time Recheck -> Execution
```

proposal_engine_defined=true
