# E32.1.4 Final Methodology Decision

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

capacity_validation_methodology_defined=true

## Final Methodology

V7 capacity validation uses a staged evidence method:

```text
STAGE_0_DISCOVERY
STAGE_1_TARGET_LOCAL
STAGE_2_LONG_WINDOW
STAGE_3_EXECUTION_PROOF
STAGE_4_CERTIFICATION
STAGE_5_RECERTIFICATION
```

## Certification Rule

A class is certified only when:

- target-local pressure validation passes;
- long-window validation passes;
- readiness is GO;
- restore-settle is GO;
- runtime checkers are OK;
- class-sized governed movement succeeds;
- rollback succeeds;
- delayed monitoring is clean;
- replay is denied;
- audit chain validates.

## Confidence Rule

```text
LOW=static_or_partial
MEDIUM=target_local_plus_long_window
HIGH=governed_execution_plus_rollback_replay_audit
VERY_HIGH=repeated_success_plus_production_pool_controls
```

Current target remains:

```text
target=amneziawg-exec-20260528-10-8-1-14
current_class=CLASS_10
capacity_confidence=HIGH
```

## Floor Rule

For CLASS_10 and below:

```text
target_local_aggregate_min >= class_size * 10 Mbps
target_local_aggregate_avg >= class_size * 12 Mbps
long_window_min >= 10 Mbps
long_window_avg >= 15 Mbps
readiness_all_go=true
runtime_checkers_ok=true
restore_settle_gate_status=GO
```

## Architecture Decisions Required

- production-pool quality floors for CLASS_50 and CLASS_100;
- exact versus staged large-scale proof;
- production-pool reservation ledger storage.

recommended_next_block=E32_1_5_CAPACITY_RUNTIME_IMPACT

