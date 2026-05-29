# E32.1.4 Quality Floors

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

quality_floors_defined=true

## Floor Types

V7 capacity validation uses two throughput floor types:

1. Target-local pressure floors: prove class-sized pressure before movement.
2. Long-window sustained floors: prove target stability over time.

This avoids retroactively invalidating E30.2, where target-local ten-stream pressure was high while long-window sustained throughput was lower but still above the movement floor.

## Baseline Long-Window Floors

For all classes through CLASS_10:

```text
long_window_avg_mbps >= 15.0
long_window_min_mbps >= 10.0
stability >= 1.000 or no readiness oscillation
readiness_all_go=true
runtime_checkers_ok=true
restore_settle_gate_status=GO
no_sample_below_floor=true
```

For CLASS_20 and above, these remain minimums but should be supplemented by production-pool policy floors.

## Target-Local Pressure Floors

Recommended initial floor:

```text
aggregate_min_mbps >= class_size * 10.0
aggregate_avg_mbps >= class_size * 12.0
per_stream_min_mbps >= 1.0 when measured
readiness_after=GO
runtime_checkers_ok=true
```

Rationale:

- E28.1 CLASS_4 evidence: aggregate_min_mbps=48.699, which is above 4 * 10.
- E30.2 CLASS_10 evidence: aggregate_min_mbps=119.541, which is above 10 * 10.
- E30.2 aggregate_avg_mbps=131.537, which is above 10 * 12.

## Class-Specific Floors

| Class | Target-Local Aggregate Min | Target-Local Aggregate Avg | Long-Window Min | Long-Window Avg | Required Readiness |
| --- | ---: | ---: | ---: | ---: | --- |
| CLASS_1 | >= 10 Mbps | >= 15 Mbps | >= 10 Mbps | >= 15 Mbps | GO |
| CLASS_2 | >= 20 Mbps | >= 24 Mbps | >= 10 Mbps | >= 15 Mbps | GO |
| CLASS_4 | >= 40 Mbps | >= 48 Mbps | >= 10 Mbps | >= 15 Mbps | GO |
| CLASS_10 | >= 100 Mbps | >= 120 Mbps | >= 10 Mbps | >= 15 Mbps | GO |
| CLASS_20 | >= 200 Mbps | >= 240 Mbps | >= 10 Mbps | >= 15 Mbps | GO |
| CLASS_50 | Architecture decision required | Architecture decision required | >= 10 Mbps minimum | >= 15 Mbps minimum | GO |
| CLASS_100 | Architecture decision required | Architecture decision required | >= 10 Mbps minimum | >= 15 Mbps minimum | GO |

## ARCHITECTURE_DECISION_REQUIRED

decision_needed=production_pool_quality_floors_for_CLASS_50_AND_CLASS_100

Options:

1. Linear pressure floors continue through CLASS_100.
2. Production-pool floors become policy-based using measured per-user service-level objectives.
3. Hybrid model: linear minimum plus policy-based SLO.

Recommended option:

```text
Option 3: hybrid model for CLASS_50 and CLASS_100.
```

Reason:

Linear floors are simple but may not represent actual production traffic. Pure policy SLOs are flexible but could weaken certification. Hybrid floors preserve a hard technical minimum and allow production-pool-specific SLOs.

