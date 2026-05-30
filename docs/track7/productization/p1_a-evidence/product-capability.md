# P1.A Product Capability

evidence_product_capability_defined=true

## Product Capability

Evidence Bundle System is the product layer that turns scattered checks, logs, probe output, registry snapshots, packet decisions and audit records into one operator-readable proof package.

It exists to support the V7 operational workflow:

```text
Problem
-> Evidence
-> Diagnosis
-> Action
-> Verification
-> Closure
```

## Scope

An evidence bundle can describe:

- a user issue;
- a channel/target issue;
- a route or service-health issue;
- a proposal or batch decision;
- a release, backup, restore or recovery event;
- a failed gate, denied action or completed verification.

It is not an execution authority. It does not move users, mutate routes, apply autoswitch or change runtime state.

## Operator Value

Evidence bundles answer:

- what happened;
- which object is affected;
- what proof exists;
- what the system thinks the diagnosis is;
- what action is recommended;
- what verification is required;
- whether the case is closed.

The operator should not have to read raw logs first. Raw detail remains available behind the summary and timeline.

## Relationship To Proposals

Proposal System uses evidence bundles as its proof source.

A proposal must link to evidence that explains:

- why the proposal exists;
- what gates were checked;
- what blockers exist;
- what rollback path is available;
- what verification must pass after execution.

## Relationship To Recovery

Recovery and rollback flows use evidence bundles to prove:

- pre-failure state;
- containment scope;
- rollback commands or actions;
- post-rollback verification;
- residual risks.

## Relationship To Runbooks

Runbooks use evidence bundles as both input and output:

- input: bundle explains the problem and required checks;
- output: bundle records what was done, what passed, and what remains.

## Capability Verdict

Evidence Bundle System is a P0 implementation package because it is the common proof surface for proposals, checks, logs, release verification, recovery verification and operator runbooks.

