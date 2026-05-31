# P1.B Product Capability

proposal_product_capability_defined=true

## Product Capability

Proposal System is the product layer that turns evidence-backed diagnosis into a safe operator-readable recommendation.

It sits between Evidence Bundle and Governance:

```text
Problem
-> Evidence Bundle
-> Proposal
-> Governance
-> Execution
```

## Purpose

A proposal explains what V7 recommends and why.

It can recommend:

- moving a user or batch to a better channel;
- avoiding a target because of service, capacity or policy blockers;
- running a check or preview before action;
- opening recovery, rollback or containment workflow;
- waiting because evidence is stale or incomplete.

## Operator Value

The operator sees:

- the recommendation;
- the affected users or objects;
- confidence and severity;
- required services and blockers;
- expected benefit;
- linked evidence;
- rollback hint;
- governance path required before execution.

The operator should not need to infer an action from raw logs.

## Relationship To Evidence

Proposal must not exist without evidence.

Each proposal must reference at least one Evidence Bundle:

```text
proposal.evidence_bundle_id = required
```

Evidence explains the problem. Proposal explains the recommended response.

## Relationship To Governance

Proposal is not an authority and cannot execute runtime mutation.

Governance still owns:

- approval packet;
- policy admission;
- capacity gates;
- concurrency locks;
- scheduling;
- execution-time recheck;
- audit and replay protection.

## Relationship To Routing Intelligence

Routing Intelligence can generate or refresh proposals using:

- required services;
- service health;
- channel readiness;
- target quality;
- route reality;
- user/company policy;
- stickiness and flapping protection.

Proposal System stores the recommendation, confidence and rationale in a form the admin can show.

## Capability Verdict

Proposal System is a P0 implementation package because it turns V7 intelligence into bounded, explainable operator choices while preserving fail-closed governance.
