# V7 Phase 2 - Safe State Persistence

## Purpose

Provisioning writes must be atomic, recoverable, and auditable.

## Required Write Rules

For dangerous writes:

- backup before write;
- atomic replace;
- preserve file mode;
- fsync where practical in future implementation;
- validate after write;
- audit result;
- keep rollback pointer.

## Critical Files

- `egress.registry`;
- `egress-flags.state`;
- draft `metadata.json`;
- draft `config.input`;
- runtime profile files;
- policy files;
- service/quarantine result files.

## Corruption Handling

If state cannot be parsed:

- block enable;
- block autoswitch eligibility;
- surface explicit operator warning;
- do not silently regenerate from partial runtime state;
- preserve corrupt file for manual recovery.

## Runtime Consistency Checks

After writes:

- contract validation;
- provisioning reconcile check;
- kill switch check when egress interface eligibility changed;
- lifecycle validation.

## Phase 2 Boundary

This file defines persistence rules. It does not change existing write helpers.
