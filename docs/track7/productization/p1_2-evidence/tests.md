# P1.2 Tests

## Reality-First Compliance Scan

reality_first_rule_satisfied=true

Every implementation plan answers:

```text
Product Capability
-> Operator Meaning
-> Admin Surface
-> Runtime Service
-> Storage
-> API
-> UI Component
```

## Admin Integration Scan

admin_integration_defined=true

Uses existing sections:

- `Главная`;
- `Проверки`;
- `Безопасность`.

No new top-level navigation is required.

## Runtime Trust Scan

runtime_trust_scan_passed=true

Defined:

- Runtime Convergence Store;
- runtime status;
- fingerprint storage;
- drift storage;
- verification history;
- runtime APIs;
- runtime UI.

## Release Trust Scan

release_trust_scan_passed=true

Defined:

- Release Trust Store;
- release summary;
- release lineage;
- rollback lineage;
- certification state;
- release APIs;
- release UI.

## Trust Chain Scan

trust_chain_defined=true

Validated:

```text
Problem
-> Evidence
-> Proposal
-> Runtime Trust
-> Release Trust
```

## Marker Scan

Required markers present:

- runtime_store_implementation_defined=true
- runtime_api_implementation_defined=true
- runtime_ui_implementation_defined=true
- release_store_implementation_defined=true
- release_api_implementation_defined=true
- release_ui_implementation_defined=true
- trust_chain_defined=true
- implementation_order_defined=true
- build_ready=true
- reality_first_rule_satisfied=true

## No Runtime Mutation Scan

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false
autoswitch_apply_performed_manually=false
canary_performed=false
cohort_performed=false

## Git Diff Check

`git diff --check` must pass before final handoff.
