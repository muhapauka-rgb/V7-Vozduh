# P1.D/E Tests

## Reality-First Compliance Scan

reality_first_rule_satisfied=true

Release Trust Surface maps:

```text
Product Capability
-> Operator Meaning
-> Admin Surface
-> Runtime Service
-> Storage/API
```

## Release Trust Scan

release_trust_surface_defined=true

Operator language defined:

- Current Release;
- Certified;
- Rollback Available;
- Release Matches Runtime;
- Attention Required.

## Runtime/Release Integration Scan

runtime_release_integration_defined=true

Runtime Trust answers whether runtime matches expected release.

Release Trust answers whether expected release is known, certified and rollback-safe.

## Phase 1 Chain Validation Scan

phase_1_chain_valid=true

Validated chain:

```text
Problem
-> Evidence
-> Proposal
-> Runtime Trust
-> Release Trust
```

## Marker Scan

Required markers present:

- release_trust_surface_defined=true
- release_trust_product_capability_defined=true
- release_trust_admin_surface_defined=true
- release_status_model_defined=true
- release_provenance_model_defined=true
- release_trust_storage_defined=true
- release_trust_api_defined=true
- release_drawer_defined=true
- phase_1_chain_valid=true
- implementation_phase_1_certified=true
- implementation_backlog_defined=true
- implementation_gaps_defined=true

## No Runtime Mutation Scan

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false
autoswitch_apply_performed_manually=false
canary_performed=false
cohort_performed=false

## Git Diff Check

`git diff --check` must pass before final handoff.
