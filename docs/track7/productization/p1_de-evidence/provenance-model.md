# P1.D/E Provenance Model

release_provenance_model_defined=true

## Release Provenance

Release provenance explains where the current release came from and why it can be trusted.

Operator-facing provenance should include:

- release label;
- release source;
- certification state;
- validation evidence;
- release lineage;
- rollback lineage;
- runtime match state.

## Release Source

Release source records:

- repository or build source reference;
- build/release identifier;
- deployment source;
- operator-visible label.

Raw commit hashes can be shown in advanced details, not as primary operator copy.

## Release Certification

Certification includes:

- checks passed;
- validation timestamp;
- evidence bundle;
- certifying authority/source;
- freshness state.

## Release Lineage

Release lineage shows:

- previous release;
- current release;
- transition event;
- verification evidence;
- audit reference.

## Rollback Lineage

Rollback lineage shows:

- rollback target;
- rollback artifact or restore point;
- rollback verification status;
- backup/restore relationship;
- known limitations.

## Release Verification

Release verification must answer:

- is this release known;
- is this release certified;
- does runtime match;
- does rollback exist;
- is verification fresh.

## Provenance Verdict

Provenance model provides enough operator trust without forcing normal users to parse commit, manifest or signature internals.
