# E34.B Fingerprint & Signing Model

release_fingerprint_model_defined=true

## Release Fingerprint

release_fingerprint identifies the immutable release object and its manifest.

## Generation

The release fingerprint should hash a canonical release bundle:

```text
release_object_core
release_manifest
artifact_manifest
config_schema_refs
certification_refs
rollback_refs
```

Generation rules:

- sort manifest entries deterministically;
- include full source commit;
- include artifact content hashes;
- include expected runtime/config fingerprints;
- include schema version;
- exclude volatile timestamps except release_created_at in canonical position.

## Verification

A release verifies when:

```text
recomputed_release_fingerprint == stored_release_fingerprint
```

Runtime verifies against release when:

```text
observed_runtime_fingerprint == expected_runtime_fingerprint
observed_config_fingerprint == expected_config_fingerprint
```

## Ownership

- Release builder generates fingerprint.
- Certification process verifies fingerprint.
- Deployment verifier compares runtime/config fingerprints.
- Operator visibility displays mismatch status.

## Signed Release Model

E34.B evaluates signatures but does not implement them.

```text
ARCHITECTURE_DECISION_REQUIRED:
decision_needed=release_signing_policy
options=unsigned_internal, operator_signed, ci_signed, cosign_or_gpg_signed
pros=unsigned is simple; operator signed is accountable; ci signed is reproducible; cosign/gpg has ecosystem support
cons=unsigned weak provenance; operator signed may be manual; ci signed requires infra; cosign/gpg requires key management
recommended_option=ci_signed_with_operator_approval_record
```

release_fingerprint_model_defined=true
