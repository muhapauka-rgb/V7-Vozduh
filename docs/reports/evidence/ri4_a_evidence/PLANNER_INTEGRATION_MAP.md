# Planner Integration Map

Planner owner:

```text
tools/v7-users-autoswitch
```

## Planner Inputs

| Input | Source | Use |
|---|---|---|
| users registry | `users.registry` | active users and current routes |
| egress registry | `egress.registry` | candidate channels |
| policy/org policy | `/etc/v7/policy.json`, org policy | hard limits, service preferences, capacity and autoswitch policy |
| service matrix | `service-matrix.json` | service suitability |
| quality summary | `egress-quality-summary.json` | historical quality and load quality checks |
| restore barrier | restore barrier state | generation/clearance enforcement |
| autoswitch safety | `autoswitch-safety.json` | anti-flap and quarantine |
| reconnect state | `client-reconnect-state.json` | reconnect rotation logic |
| intelligence snapshots | `/opt/v7/egress/state/intelligence/*.json` | fast-path advisory/gates |

## Existing Ranking Inputs

- native service suitability;
- capacity decision;
- best available pool;
- route class;
- quality/load checks;
- RI `routing_intelligence` score part;
- snapshot-backed `channel-service-scores` score part.

## Existing RI Extension Points

- `--intelligence-snapshot-root` CLI argument;
- `_load_intelligence_snapshots()`;
- `_intelligence_snapshot_gate()`;
- `_snapshot_candidate_advisory_scores()`;
- `_routing_intelligence_scores_for_user()`;
- `_routing_intelligence_candidate_advice()`;
- `_snapshot_routing_brain_advisory()`;
- `_routing_brain_advisory()`;
- `_score_parts(..., routing_intelligence=...)`;
- selected move suppression when snapshot stop gate is active.

## What Planner Already Supports Without Architecture Change

- reading compact RI snapshots;
- using channel service scores as bounded score part;
- using risk/trust/blast snapshot context in advisory output;
- fail-closed selected move suppression when required snapshot truth is unsafe;
- fallback to in-process RoutingBrain when snapshots are absent.

## What Planner Ignores / Does Not Yet Consume

- `capacity-forecast-summaries.json`, intentionally not integrated in PERF.4;
- `prediction-summaries.json`, advisory contract exists but not production-generated;
- `user-service-scores.json`, advisory-only and can be stale/missing without suppressing moves.

## RI.4 Verdict

Planner integration exists.

RI.4 should use current extension points.

Do not add a second planner or selected move writer.

