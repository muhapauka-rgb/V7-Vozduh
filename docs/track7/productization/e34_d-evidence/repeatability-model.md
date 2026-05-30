# E34.D Repeatability Model

repeatable_deployment_defined=true

## Definition

Repeatable deployment means:

```text
same release + same manifest + same profile + same approved config -> same certified outcome
```

within supported host constraints.

## Reproducibility Inputs

- release_id;
- release_fingerprint;
- release_manifest;
- deployment_profile;
- config manifest;
- preflight result;
- installation stage log;
- health check result;
- certification result;
- deployment lineage event.

## Repeatability Rules

- Installer must be idempotent by stage where safe.
- Each CHECK can be rerun without hidden side effects.
- Partial installation must produce a known recovery state.
- Same release cannot silently install different artifacts.
- Config drift blocks repeatability certification.

## Repeatability Output

```text
repeatability_status=REPRODUCIBLE|PROFILE_DEPENDENT|NOT_REPRODUCIBLE
release_id
manifest_hash
config_fingerprint
stage_history_hash
certification_hash
```

repeatable_deployment_defined=true
