# P1.D/E Storage Model

release_trust_storage_defined=true

## Store Ownership

Release Trust Store owns release summary, certification summary, release lineage, rollback lineage and verification history.

It references artifacts, backups, runtime convergence snapshots and evidence bundles.

## Storage Objects

Minimum entities:

- `release_summaries`;
- `release_certifications`;
- `release_lineage_events`;
- `rollback_lineage_records`;
- `release_verification_events`;
- `release_evidence_links`.

## Release Summary Store

Release summary should include:

- release id;
- display label;
- status;
- certification state;
- runtime match state;
- rollback availability;
- verification freshness;
- evidence bundle id.

## Release Lineage Store

Lineage store should preserve:

- previous release id;
- current release id;
- transition timestamp;
- actor/source;
- verification evidence;
- audit reference.

## Rollback Lineage Store

Rollback lineage should preserve:

- rollback target release;
- restore point or backup reference;
- rollback readiness status;
- verification state;
- known blockers.

## Verification History

Verification history should include:

- release verification event;
- runtime convergence reference;
- backup/restore reference;
- evidence bundle;
- result;
- timestamp.

## Storage Verdict

Release Trust Store is an operator-facing trust index over release, runtime, backup and rollback evidence.
