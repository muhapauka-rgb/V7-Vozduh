# P1.3 Tests

## Reality-First Compliance Scan

reality_first_rule_satisfied=true

Each wave answers:

- what capability appears;
- what operator value appears;
- what admin surface appears.

## Dependency Consistency Scan

dependency_graph_defined=true

Evidence is the root dependency.

Proposal depends on Evidence.

Runtime/Release Trust depend on Evidence links and can later block proposal/batch flow.

## Wave Consistency Scan

implementation_waves_defined=true

Waves:

- Wave 1 Evidence Foundation Visible In Admin;
- Wave 2 Proposal Visibility;
- Wave 3 Runtime And Release Trust Status;
- Wave 4 Production Hardening.

## Operator Value Scan

operator_value_defined=true

Every wave produces visible admin value. No invisible backend-only wave exists.

## Marker Scan

Required markers present:

- implementation_roadmap_defined=true
- implementation_inventory_loaded=true
- dependency_graph_defined=true
- implementation_waves_defined=true
- operator_value_defined=true
- admin_evolution_defined=true
- build_sequence_defined=true
- implementation_ready=true
- phase1_completion_defined=true
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
