# P1.B Tests

## Reality-First Compliance Scan

reality_first_rule_satisfied=true

Proposal System maps:

```text
Product Capability
-> Operator Meaning
-> Admin Surface
-> Runtime Service
-> Storage/API
```

## Proposal/Evidence Linkage Scan

proposal_evidence_linkage_required=true

Proposal must reference Evidence Bundle:

```text
proposal.evidence_bundle_id = required
```

## Admin Integration Scan

proposal_admin_surface_defined=true

Proposal integrates into existing admin sections:

- `Главная`;
- `Маршруты`;
- `Пользователи`;
- `Каналы`.

No new top-level navigation is required.

## Governance Integration Scan

proposal_governance_integration_defined=true

Governance path defined:

```text
Proposal
-> Batch
-> Policy
-> Capacity
-> Concurrency
-> Scheduling
-> Execution-Time Recheck
-> Execution
```

Proposal remains non-authoritative.

## Marker Scan

Required markers present:

- proposal_system_defined=true
- proposal_product_capability_defined=true
- proposal_admin_surface_defined=true
- proposal_model_defined=true
- proposal_lifecycle_defined=true
- proposal_storage_defined=true
- proposal_api_defined=true
- proposal_drawer_defined=true
- proposal_governance_integration_defined=true
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
