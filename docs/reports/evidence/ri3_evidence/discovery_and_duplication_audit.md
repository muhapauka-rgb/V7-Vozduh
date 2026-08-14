# RI.3 Discovery And Duplication Audit

## Discovery

Existing implementation found and reused:

| Area | Location | Decision |
| --- | --- | --- |
| Runtime planner | `tools/v7-users-autoswitch` | Reuse and extend ranking only |
| Candidate scoring | `tools/v7-users-autoswitch::_score_parts` | Extend with bounded `routing_intelligence` score part |
| Candidate ranking | `tools/v7-users-autoswitch::_decision_for_user` | Reuse existing sort path |
| Best available pool | `tools/v7-users-autoswitch::_mark_best_available_pool` | Preserve; RI affects score only before pool marking |
| Capacity-aware routing | `tools/v7-users-autoswitch::_capacity_decision` and load gates | Preserve hard/soft capacity gates |
| Service-aware routing | `tools/v7-users-autoswitch::_service_suitability` | Preserve existing gate and service score |
| Service History | `admin_core/routing_intelligence.py::ServiceHistoryStore` | Reuse |
| User Service Weights | `admin_core/routing_intelligence.py::UserServiceWeights` | Reuse |
| Execution Trust | `admin_core/routing_intelligence.py::ExecutionTrustModel` | Reuse |
| Dynamic Blast Radius | `admin_core/routing_intelligence.py::DynamicBlastRadiusModel` | Reuse as recommendation only |
| Routing Brain | `admin_core/routing_brain.py::RoutingBrain` | Extend with RI.3 candidate advisory score contract |
| Shadow replay | `tools/v7-routing-intelligence-shadow` | Reuse for evidence |

## Current Decision Chain

```text
registry/runtime state
-> planner loads users and egress
-> hard gates
-> service suitability
-> quality/capacity/safety/reservation gates
-> score_parts
-> ranking
-> best available pool
-> movement selection limits
-> restore barrier
-> runtime recheck/governance outside RI
```

## Current Scoring Chain

```text
health
service
telegram_required
speed
stability
latency
load
capacity
quality_history
priority
weight
sticky
org_preference
reserve_penalty
```

RI.3 adds:

```text
routing_intelligence
```

Only eligible candidates receive the score part.

## Duplication Audit

No second planner was created.

No second governance system was created.

No second routing authority was created.

No duplicate service history store was created.

No duplicate user weights store was created.

No duplicate execution trust model was created.

No duplicate dynamic blast radius model was created.

The existing planner remains the ranking and decision owner. Routing Brain only supplies bounded candidate advice.

## Safety Finding

Routing Brain cannot:

- create candidates;
- bypass hard gates;
- bypass canary reservation;
- bypass best available pool;
- bypass governance;
- write selected moves;
- apply runtime changes;
- move users.

