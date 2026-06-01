# PROGRAM Z4 Scaling Forecast

## Forecast Basis

Current live runtime:

- active_users: `18`
- total_channels: `7`
- working_channels: `1`
- healthy_egress_total: `0`
- capacity status: `warm`
- selected_moves: `0`

This forecast assumes the current architecture and observed target-pool condition.

## 50 Users

First break:

- capacity and health pool readiness

Why:

- current runtime already has `healthy_egress_total=0`.
- one working channel is not enough for robust bounded autonomy.
- rollback remains command-available, but repeated autonomous movement cannot be certified.

## 100 Users

First break:

- capacity headroom and observation signal quality

Why:

- dynamic soft/hard limits need more eligible targets.
- planner can refuse unsafe moves, but production autonomy value is lost if no eligible failover exists.

## 500 Users

First break:

- approval/recheck throughput and observation freshness

Why:

- one-user budget can remain safe, but certification requires faster evidence collection, compacted history, and target-pool health guarantees.
- rollback audit volume grows quickly.

## 2000 Users

First break:

- governance, observation retention, and rollback orchestration

Why:

- one-user bounded moves are safe but operationally too slow without larger certified cohorts.
- current architecture needs stronger capacity classes, event compaction, replay indexing, and staged rollback automation before this scale.

## Component Forecast

- Planner: safe fail-closed now; throughput and target scoring must be load-tested at higher user counts.
- Approval: safe for one-user packets; needs runtime-integrated approval-to-apply path before broad production autonomy.
- Runtime: currently not autonomy-ready because no eligible failover target exists.
- Capacity: breaks first at current state.
- Observation: adequate for 18 users; must be compacted and indexed for 500+ users.
- Rollback: command path exists; stressed rollback is not certified.
- Governance: generation and replay controls work; production workflow needs recovery certification.

## Verdict

- scaling_forecast_complete=true
- first_breaks_first=capacity_and_health_pool

