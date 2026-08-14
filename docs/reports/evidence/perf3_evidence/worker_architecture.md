# PERF.3 Worker Architecture

## Ownership

Heavy Brain workers own snapshot production.

Runtime owns runtime decisions.

Governance owns execution authorization.

Workers do not own execution, approval, selected moves, or route state.

## Producers

| Worker | Inputs | Outputs | Cadence |
|---|---|---|---:|
| service score worker | service matrix, quality summary, service preferences | `service-scores.json`, `channel-service-scores.json` | 60s |
| trust worker | audit history, switch history, rollback history | `trust-summaries.json` | 300s |
| risk worker | service/channel snapshots, quality summary | `risk-summaries.json` | 60s |
| blast radius worker | trust snapshot, risk snapshot, counts | `blast-radius-summaries.json` | 60s |
| overview worker | runtime state, registries, snapshot statuses | `overview-summary.json` | 30s |

## Failure Behavior

- missing inputs produce valid snapshots with warnings and lower confidence
- corrupt JSON inputs are treated as missing by CLI readers
- JSONL history is bounded and corrupt lines are skipped
- workers do not affect runtime when inputs are missing
- runtime behavior remains unchanged because snapshots are not integrated

## Forbidden Actions

Workers must never:

- move users
- write selected moves
- approve governance
- execute runtime actions
- restart services
- integrate into planner decisions
