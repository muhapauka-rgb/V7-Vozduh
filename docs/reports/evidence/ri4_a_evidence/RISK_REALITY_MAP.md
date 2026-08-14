# Risk Reality Map

## Existing Risk Model

| Component | Owner | Inputs | Outputs | Active Runtime Consumption |
|---|---|---|---|---|
| service risk in `RoutingBrain` | `admin_core/routing_brain.py` | service/advisory scores | `degradation_risk_score`, service risk input | fallback/advisory path |
| `DynamicBlastRadiusModel` risk inputs | `admin_core/routing_intelligence.py` | execution trust, service risk, platform health | recommended budget | advisory/foundation |
| risk snapshot worker | `admin_core/intelligence_workers.py` | `service-scores`, `channel-service-scores`, quality summary | `risk-summaries.json` | PERF.4 fast path |
| runtime snapshot risk guard | `tools/v7-users-autoswitch` | `risk-summaries.json` via snapshot gate | stop/warn/ignore behavior | ACTIVE when snapshot root exists |
| route leak/trusted RU risk | `admin_core/route_reality_views.py`, admin diagnostics | route outputs/trusted RU states | read-only admin risk surfaces | admin only |

## Active vs Foundation

Active:

- `risk-summaries.json` is runtime-required for intelligence apply.
- Missing/corrupt/expired/unknown/low-confidence risk snapshot can stop selected moves through PERF.4 gate.

Foundation/advisory:

- predictive risk examples are disabled.
- risk does not approve governance.
- risk does not move users.

## Truth Source

Risk is derived from:

- service/channel snapshots;
- quality summary;
- route reality;
- trust history;
- runtime counts.

Canonical risk snapshot:

- `/opt/v7/egress/state/intelligence/risk-summaries.json`

## RI.4 Verdict

Risk model exists and is active through snapshots.

RI.4 should EXTEND existing risk worker/snapshot semantics only.

Do not create a separate risk authority.

