# E34.B Release Object Model

release_object_model_defined=true

## Definition

A release_object is the immutable commercial unit that binds repository truth, build artifacts, configuration schema, certification evidence, rollback target, and expected runtime identity.

## Required Fields

```text
release_id
release_version
release_created_at
release_created_by
source_repository
source_branch
source_commit
source_tree_hash
release_manifest
release_fingerprint
release_certification_status
release_certification_refs
release_lineage_reference
rollback_release_id
expected_runtime_fingerprint
expected_config_fingerprint
```

## Identity Rules

- release_id must be globally unique.
- release_version must be human-readable and monotonic within the product line.
- source_commit must be a full commit SHA.
- release_fingerprint must be derived from release_manifest and artifact manifest.
- release object is immutable after certification. Corrections require a new release object or explicit revocation/supersession event.

## Authority

The release object is authoritative for intended deployment contents. It is not proof of live runtime until deployment lineage and runtime fingerprint confirm convergence.

release_object_model_defined=true
