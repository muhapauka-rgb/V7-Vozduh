# Trust Reality Map

## Existing Trust Systems

| Component | Owner | Inputs | Outputs | Consumer |
|---|---|---|---|---|
| `ExecutionTrustModel` | `admin_core/routing_intelligence.py` | audit/switch/rollback records | trust score, counters, median blast radius | Routing Brain, trust worker |
| trust snapshot worker | `admin_core/intelligence_workers.py` | bounded audit/switch/rollback history | `trust-summaries.json` | runtime fast path |
| runtime trust snapshot guard | `tools/v7-users-autoswitch` | `trust-summaries.json` | STOP/WARN/IGNORE gate result | runtime planner |
| admin runtime trust read view | `admin_core/runtime_read_views.py` / API.5 | runtime trust store payload | read-only admin view | admin only |

## Trust Calculations

ExecutionTrustModel starts from 70 and:

- rewards successful executions;
- rewards successful rollbacks;
- penalizes failed executions;
- penalizes failed rollbacks;
- penalizes governance violations;
- penalizes blast radius expansions;
- slightly penalizes high median blast radius.

## Active Runtime Consumption

`trust-summaries.json` is a runtime-required intelligence snapshot:

- stale behavior: STOP;
- confidence floor: 0.70;
- missing/corrupt/expired/unknown/low-confidence trust can stop selected moves when snapshot gate is active.

## Governance Consumption

No evidence found that governance consumes trust as an authority.

Trust is advisory/runtime guard input only. Governance authority remains unchanged.

## RI.4 Verdict

Trust model exists and is active as snapshot guard input.

RI.4 should EXTEND `ExecutionTrustModel` and `trust-summaries` worker if needed.

Do not create a second trust model or governance trust authority.

