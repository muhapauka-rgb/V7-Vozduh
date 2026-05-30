# E33.A Proposal Boundary Model

proposal_boundary_defined=true

## Allowed Outputs

Routing Intelligence may output:

- movement proposal;
- evacuation proposal;
- rebalance proposal;
- no-action recommendation;
- observation recommendation.

## Forbidden Outputs

Routing Intelligence may not output or perform:

- runtime mutation;
- user movement;
- route table changes;
- direct autoswitch apply;
- governance bypass;
- packet consumption;
- execution scheduling bypass;
- execution-time recheck bypass.

## Proposal Required Fields

Each proposal must include:

```text
proposal_id
proposal_type
affected_users
reason
evidence
current_target
proposed_target
required_services_impact
confidence
expected_benefit
rollback_suggestion
governance_path
created_at
expires_at
```

## Governance Path

Proposal must enter:

```text
Batch -> Policy -> Capacity -> Concurrency -> Scheduling -> Execution-Time Recheck -> Execution
```

## Fail-Closed Boundary

If evidence is missing, stale, contradictory, or required_services are unknown, Routing Intelligence should produce observation or review recommendation, not high-confidence movement proposal.

## Decision

proposal_boundary_defined=true
