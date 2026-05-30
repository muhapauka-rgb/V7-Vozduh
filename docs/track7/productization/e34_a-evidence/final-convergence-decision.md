# E34.A Final Convergence Decision

runtime_repo_convergence_defined=true

## Decision Summary

E34.A defines Runtime / Repo Convergence Architecture for commercial deployability.

The model separates:

- runtime_truth: what is actually running;
- repo_truth: what source control intends;
- release_object: what is officially packaged/certified;
- deployment_lineage: how release became runtime;
- fingerprints: how convergence and drift are verified.

## Certified Model Markers

```text
current_state_loaded=true
runtime_truth_model_defined=true
repo_truth_model_defined=true
fingerprint_model_defined=true
drift_detection_defined=true
release_object_model_defined=true
deployment_lineage_defined=true
operator_visibility_defined=true
governance_compatible=true
routing_intelligence_compatible=true
runtime_repo_convergence_defined=true
```

## Core Rules

- Runtime truth and repo truth are distinct.
- Runtime is not production-certified unless linked to a release object.
- Dirty working tree is not release truth.
- Unknown runtime fingerprint is blocking for commercial deployment.
- Unknown governance/routing config fingerprint is blocking.
- Broken deployment lineage makes production deployability UNKNOWN/BLOCKING.
- Rollback remains allowed for containment.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- fingerprint_hash_algorithm
- release_object_storage_backend
- deployment_lineage_backend
- runtime_inventory_collector
- config_manifest_scope
- secret_hashing_policy
- release_signing_policy
- drift_severity_policy
```

## Remaining Open Questions

- Where should release objects be stored?
- Which runtime services must expose version endpoints?
- Which config artifacts belong in commercial config_fingerprint?
- What signing policy is required for release objects?
- Who can manually certify lineage reconstruction?

recommended_next_block=E34.B_RELEASE_AND_PROVENANCE_ARCHITECTURE
