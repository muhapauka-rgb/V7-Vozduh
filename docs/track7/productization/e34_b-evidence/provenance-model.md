# E34.B Provenance Model

provenance_model_defined=true

## Definition

Provenance is the evidence chain that explains where a release came from, how it was certified, how it was deployed, and how it can be rolled back.

## Provenance Chain

```text
repo source
-> commit identity
-> release creator
-> release manifest
-> release fingerprint
-> certification source
-> deployment lineage
-> runtime convergence
-> rollback lineage
```

## Required Provenance Fields

```text
source_repository
source_branch
source_commit
source_tree_hash
release_creator
release_created_at
release_fingerprint
certification_report_refs
certification_status
deployment_lineage_ref
runtime_fingerprint_ref
rollback_release_id
rollback_lineage_ref
```

## Provenance Failure Modes

| Failure | Impact | Safe Behavior |
| --- | --- | --- |
| missing source commit | Release identity cannot be verified. | Deny certification. |
| dirty source without explicit dev status | Release cannot be commercial. | DRAFT only. |
| missing certification source | Release cannot be trusted. | REVIEW or DRAFT. |
| missing deployment lineage | Runtime cannot be linked to release. | Deployment UNKNOWN/BLOCKING. |
| missing rollback lineage | Rollback safety cannot be certified. | Require operator review. |

provenance_model_defined=true
