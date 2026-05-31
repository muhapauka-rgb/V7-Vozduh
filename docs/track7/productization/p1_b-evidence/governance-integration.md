# P1.B Governance Integration

proposal_governance_integration_defined=true

## Integration Principle

Proposal can enter governance, but it is not governance.

Proposal provides recommendation context. Governance decides whether execution can be prepared and later executed.

## Governance Path

```text
Proposal
-> Batch
-> Policy
-> Capacity
-> Concurrency
-> Scheduling
-> Execution-Time Recheck
-> Execution
```

## Batch Integration

A proposal can be converted into an execution batch only if:

- proposal is `ACTIVE`;
- evidence is fresh;
- affected user set is exact;
- target set is exact;
- rollback hint exists;
- proposal has not expired or been superseded.

## Policy Integration

Policy evaluates:

- whether proposal type is allowed;
- whether user/company/route/service rules permit it;
- whether review is required;
- whether proposal conflicts with policy.

Policy can deny or require additional gates.

## Capacity Integration

Capacity checks:

- target certified capacity;
- effective batch cap;
- available capacity;
- freshness and confidence;
- target eligibility.

Proposal cannot override capacity.

## Concurrency Integration

Concurrency controls:

- user locks;
- target locks;
- batch lock;
- packet lock;
- audit lock;
- capacity/target reservations.

Proposal cannot reserve capacity without governance.

## Scheduling Integration

Scheduler can decide whether a proposal-derived batch is executable now or later.

Scheduling must preserve:

- exact user set;
- exact target;
- packet freshness;
- no autoswitch side effects.

## Execution-Time Recheck

Execution-time recheck remains mandatory.

It must verify:

- proposal-derived batch still matches runtime truth;
- evidence is still acceptable;
- packet is non-expired;
- target still eligible;
- selected moves and hidden movers are absent;
- runtime checkers OK.

## Execution Boundary

Proposal may:

- recommend;
- explain;
- prioritize;
- preview.

Proposal may not:

- move users;
- mutate runtime;
- change routing;
- execute autoswitch;
- bypass governance.

## Governance Verdict

Proposal System is governance-compatible because it feeds exact, evidence-linked recommendations into governance without becoming authority.
