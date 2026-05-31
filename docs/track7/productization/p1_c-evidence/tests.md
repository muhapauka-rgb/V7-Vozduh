# P1.C Tests

## Reality-First Compliance Scan

reality_first_rule_satisfied=true

Runtime Convergence Surface maps:

```text
Product Capability
-> Operator Meaning
-> Admin Surface
-> Runtime Service
-> Storage/API
```

## Admin Integration Scan

runtime_convergence_admin_surface_defined=true

Runtime Convergence integrates into existing admin sections:

- `Главная`;
- `Проверки`;
- `Безопасность`.

No new top-level navigation is required.

## Runtime Trust Scan

runtime_status_model_defined=true

Defined states:

- `RUNTIME_OK`;
- `RUNTIME_WARNING`;
- `RUNTIME_DRIFT`;
- `RUNTIME_UNKNOWN`;
- `RUNTIME_BLOCKING`.

## Drift Coverage Scan

runtime_drift_model_defined=true

Defined drift types:

- `runtime_drift`;
- `config_drift`;
- `release_drift`;
- `lineage_drift`.

## Marker Scan

Required markers present:

- runtime_convergence_surface_defined=true
- runtime_convergence_product_capability_defined=true
- runtime_convergence_admin_surface_defined=true
- runtime_status_model_defined=true
- runtime_drift_model_defined=true
- runtime_convergence_storage_defined=true
- runtime_convergence_api_defined=true
- runtime_convergence_drawer_defined=true
- runtime_convergence_relationships_defined=true
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
