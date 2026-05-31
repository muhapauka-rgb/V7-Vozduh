# E35.0.1 Current Priority Chain

## Scope

Audit question: what is the actual current priority chain.

priority_chain_defined=true

## Autoswitch Candidate Priority Chain

The actual candidate chain is:

Runtime availability / basic health
↓
Reservation / canary protection
↓
Organization/group constraints
↓
Quality floors: avg Mbps, min Mbps, stability
↓
Required services and route-class fitness
↓
Capacity hard gates
↓
Safety / anti-flap / quarantine gates
↓
Score
↓
Current-channel sticky threshold
↓
Move type selection: failover, reconnect, rebalance, planned
↓
Global move limits and projected capacity

## Score Priority Components

Once hard gates pass, score is the sum of:

- health baseline
- service score
- Telegram required score/penalty
- speed
- stability
- latency
- load
- quality history
- priority
- weight
- sticky current-channel bonus
- org preference
- reserve penalty

## Movement Priority Order

Selected moves are picked by type in this order:

1. failover
2. reconnect rotation
3. rebalance
4. planned

Each has its own configured maximum.

## Service-Aware Route Priority Chain

For route-class selection in admin:

Enabled egress
↓
route-class exclusion/manual-only/trusted-RU gates
↓
health and service matrix fitness
↓
Telegram hard/degraded semantics
↓
role/service tag match
↓
priority/weight/speed score

## Proposal Priority Chain

For proposals:

User required services
↓
current channel service status
↓
best fully matching channel by service availability/latency
↓
proposal or observation

This is non-authoritative and does not execute.

## Audit Verdict

current_selection_chain=HARD_GATES_THEN_SCORE_THEN_STICKY_THRESHOLD_THEN_PROJECTED_CAPACITY
selection_is_not_pure_speed=true
required_services_before_score=true
capacity_before_final_selection=true
