# E34.B Final Provenance Decision

release_provenance_defined=true

## Decision Summary

E34.B defines Release & Provenance Architecture.

A release is an immutable, certified, fingerprinted unit that links repository truth to expected runtime truth and rollback lineage.

## Certified Model Markers

```text
release_context_loaded=true
release_object_model_defined=true
release_manifest_model_defined=true
provenance_model_defined=true
release_certification_model_defined=true
release_rollback_model_defined=true
release_fingerprint_model_defined=true
release_visibility_defined=true
governance_compatible=true
routing_intelligence_compatible=true
runtime_convergence_compatible=true
release_provenance_defined=true
```

## Core Rules

- Release identity requires source commit, manifest, fingerprint, certification status, and lineage reference.
- Release manifest must include code, configuration, governance, routing intelligence, metadata, tests, and rollback artifacts.
- Release provenance must link source -> commit -> manifest -> fingerprint -> certification -> deployment -> runtime -> rollback.
- Missing safety-critical provenance denies certification.
- Rollback target must be represented as a release object or explicitly marked as emergency containment.
- Release object is intended truth; runtime convergence proves actual deployment.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- release_object_storage_backend
- release_manifest_schema_version
- release_signing_policy
- release_versioning_scheme
- provenance_ledger_backend
- rollback_release_policy
- release_certification_authority
```

## Remaining Open Questions

- Which backend stores immutable release objects?
- Should release versions be calendar, semantic, or block-based?
- Which signature mechanism is required?
- Who is allowed to certify and revoke releases?
- What is the emergency rollback policy when rollback provenance is incomplete?

recommended_next_block=E34.C_BACKUP_RESTORE_ARCHITECTURE
