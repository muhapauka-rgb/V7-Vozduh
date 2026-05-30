# E34.A Release Object Model

release_object_model_defined=true

## Definition

A release_object is the immutable commercial deployment unit that links repository truth to expected runtime truth.

## Required Fields

```text
release_id
release_version
created_at
source_branch
source_commit
release_fingerprint
release_manifest
artifact_manifest
config_schema_version
expected_runtime_fingerprint
expected_config_fingerprint
release_lineage
certification_status
certification_refs
rollback_release_id
```

## Certification Status

| Status | Meaning | Deployment Eligibility |
| --- | --- | --- |
| DRAFT | Release object exists but not certified. | No production deployment. |
| CERTIFIED | Release passed required tests and provenance checks. | Eligible for production deployment. |
| SUPERSEDED | Newer release replaces it. | Deployment denied unless rollback-approved. |
| REVOKED | Release is unsafe or provenance broken. | Deployment denied. |
| ROLLBACK_ONLY | Release may be used only for rollback containment. | Forward deployment denied. |

## Release Manifest

The release manifest should include:

- source commit;
- file manifest;
- build commands;
- test results;
- expected runtime services;
- expected config schema;
- certification reports;
- known limitations;
- rollback target.

## Authority

The release object is authoritative for what should be deployed. Runtime truth remains authoritative for what is actually running.

release_object_model_defined=true
