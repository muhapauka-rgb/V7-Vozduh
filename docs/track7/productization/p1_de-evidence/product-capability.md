# P1.D/E Product Capability

release_trust_product_capability_defined=true

## Product Capability

Release Trust Surface is the operator-facing layer that explains what release is running, where it came from, whether it is certified, whether rollback exists and whether runtime matches it.

It turns release/provenance/rollback facts into simple operator language:

```text
Current Release
Certified
Rollback Available
Release Matches Runtime
```

or:

```text
Attention Required
```

## Purpose

Operators should not need to understand commit hashes, signature internals, manifest internals or lineage internals during normal operation.

They need to know:

- current release identity;
- certification status;
- provenance confidence;
- rollback availability;
- runtime match;
- next safe action.

## Operator Value

The operator sees:

- release status;
- current release label;
- certification state;
- rollback availability;
- runtime match state;
- verification age;
- recommended action;
- advanced details only when needed.

## Relationship To Runtime Trust

Runtime Trust answers:

```text
Does running runtime match expected release?
```

Release Trust answers:

```text
Is the expected release itself known, certified and rollback-safe?
```

Together they determine whether the operator can trust the system state before governance actions.

## Relationship To Backup/Restore

Backup and Restore rely on release lineage:

- backup should indicate which release/runtime state it protects;
- restore should verify returned release/runtime state;
- rollback lineage should be visible before risky action.

## Relationship To Rollback

Release Trust must show whether rollback exists and whether rollback lineage is known.

Rollback availability is not only "there is a file"; it means:

- rollback target exists;
- lineage is known;
- verification evidence exists;
- operator can inspect recovery path.

## Capability Verdict

Release Trust Surface is a P0 implementation package because runtime trust is incomplete unless the operator can also trust the release identity and rollback path.
