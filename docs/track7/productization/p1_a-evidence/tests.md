# P1.A Tests

## Reality-First Compliance Scan

reality_first_rule_satisfied=true

Evidence Bundle System maps:

```text
Product Capability
-> Operator Meaning
-> Admin Surface
-> Runtime Service
-> Storage/API
```

## Admin Integration Scan

evidence_admin_surface_defined=true

Evidence integrates into existing admin sections:

- `Главная`;
- `Проверки`;
- `Логи`;
- `Пользователи`;
- `Каналы`;
- `Маршруты`.

No new top-level navigation is required.

## Evidence Linkage Scan

evidence_linkage_defined=true

Supported linkage includes:

- User;
- Channel;
- Proposal;
- Alert;
- Route;
- Release;
- Backup;
- Restore.

## Storage Consistency Scan

evidence_storage_defined=true

Storage model separates bundle metadata from raw payload references and preserves append-only payload lineage.

## Marker Scan

Required markers present:

- evidence_bundle_system_defined=true
- evidence_product_capability_defined=true
- evidence_admin_surface_defined=true
- evidence_model_defined=true
- evidence_linkage_defined=true
- evidence_storage_defined=true
- evidence_api_defined=true
- evidence_drawer_defined=true
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

