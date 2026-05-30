# E34.B Release Manifest Model

release_manifest_model_defined=true

## Definition

release_manifest describes exactly what belongs to a release.

## Required Manifest Sections

| Section | Required Contents |
| --- | --- |
| code_artifacts | tracked files, executable scripts, service entrypoints, package manifests, migrations. |
| configuration_artifacts | config schemas, default config, service units, environment schema, registry schema references. |
| governance_artifacts | capacity, batch, policy, concurrency, scheduling, execution-boundary docs/schemas/tests. |
| routing_intelligence_artifacts | required_services, service health, target quality, proposal, confidence, observability docs/schemas/tests. |
| release_metadata | release id, version, creator, source commit, build host, created_at, certification refs. |
| test_artifacts | static checks, unit/integration checks, provenance checks, drift checks. |
| rollback_artifacts | rollback release id, rollback manifest, compatibility notes. |

## Completeness Rules

- Every deployed executable must appear in code_artifacts.
- Every config that affects governance, routing, policy, capacity, locks, scheduling, execution, service health, or user movement must appear in configuration_artifacts.
- Every release must include certification_refs.
- Every production release must define a rollback_release_id or explicitly state ROLLBACK_UNAVAILABLE with human approval.
- Missing safety-critical manifest sections block certification.

release_manifest_model_defined=true
