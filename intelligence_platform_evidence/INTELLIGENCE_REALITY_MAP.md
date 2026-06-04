# INTELLIGENCE_REALITY_MAP

Program: Intelligence Platform Certification And Hardening

Date: 2026-06-04

## Architecture Chain

```text
RI.1 ServiceHistoryStore / ServiceIntelligenceEngine
-> RI.2 RoutingBrain
-> RI.3 candidate advisory score parts
-> RI.4.B candidate suitability + best available pool
-> RI.4.CD service quality / calibration / user service scores
-> RI.5 PredictiveFoundation forecasts
-> intelligence_workers
-> intelligence snapshots
-> tools/v7-users-autoswitch optional advisory reads
```

## Owners

| Layer | Owner | Truth Sources | Runtime Consumer |
| --- | --- | --- | --- |
| RI.1 | `admin_core.routing_intelligence` | service matrix, quality summary, service preferences | RoutingBrain / workers |
| RI.2 | `admin_core.routing_brain` | RI.1 read models, audit history | planner advisory context |
| RI.3 | RoutingBrain candidate advisory contract | eligible planner candidates, service history, trust | planner ranking score parts |
| RI.4.B | `intelligence_workers` | users/egress registry, risk/trust/blast snapshots | optional advisory snapshot reader |
| RI.4.CD | `ServiceIntelligenceEngine` | service matrix, quality summary, preferences | service/user score snapshots |
| RI.5 | `PredictiveFoundation` | service history, risk/trust snapshots | optional prediction advice |

## Implemented Map

Code:

- `admin_core/intelligence_platform.py::intelligence_reality_map`

## Verdict

```text
owners_known=true
truth_sources_known=true
runtime_consumers_known=true
extension_points_known=true
```

