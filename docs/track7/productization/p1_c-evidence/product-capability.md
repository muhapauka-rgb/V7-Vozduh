# P1.C Product Capability

runtime_convergence_product_capability_defined=true

## Product Capability

Runtime Convergence Surface is the product layer that tells the operator whether the running V7 node matches the expected release and can be trusted.

It answers:

- what is running;
- whether runtime matches release expectations;
- whether drift exists;
- whether drift is informational, warning-level or blocking;
- what the operator should do next.

## Purpose

Operators should not need to inspect runtime fingerprint internals, raw hashes or lineage details to understand trust.

The surface should translate technical checks into clear states:

```text
System matches release
```

or

```text
System drift detected
```

plus the next safe action.

## Operator Value

The operator sees:

- runtime trust status;
- release match status;
- drift summary;
- verification age;
- whether governance actions are blocked;
- recommended next safe action;
- link to advanced details when needed.

## Relationship To Release

Runtime convergence compares current runtime fingerprint and metadata against release expectations.

Release Surface provides:

- expected release id;
- expected build/provenance identity;
- expected runtime fingerprint;
- release validation state.

Runtime Convergence Surface displays whether runtime matches that release.

## Relationship To Backup/Restore

Backup/Restore uses convergence to verify:

- restore returned runtime to expected state;
- backup manifest matches current runtime scope;
- post-restore drift is absent or understood.

## Relationship To Governance

Governance must treat runtime convergence as a gate.

If runtime is unknown, blocking or materially drifted, forward movement should fail closed. Rollback and containment remain allowed when needed.

## Capability Verdict

Runtime Convergence Surface is a P0 implementation package because operators must know whether V7 runtime is trustworthy before acting on proposals, checks, releases or recovery workflows.
