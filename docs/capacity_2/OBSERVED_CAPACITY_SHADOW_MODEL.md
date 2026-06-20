# OBSERVED CAPACITY SHADOW MODEL

Project: V7 VOZDUH
Program: CAPACITY.2_OBSERVED_CAPACITY_MODEL_AUDIT
Mode: audit only
Last verified commit: `67fbd8506321802222c6f8ed3d34cfe406a45d8a`

## Boundary

Observed Capacity Shadow must not influence:

- runtime execution;
- planner candidate eligibility;
- assignment decisions;
- autoswitch;
- governance;
- current `soft_limit`, `hard_limit`, `capacity_users`, or score formulas.

## Purpose

Observe whether real channel quality remains stable as assigned users change.

## Proposed Shadow Fields

| Field | Meaning |
| --- | --- |
| `channel` | egress id |
| `observed_users` | assigned user count at sample time |
| `quality_state` | `STABLE`, `WATCH`, `DEGRADING`, `BROKEN`, `UNKNOWN` |
| `quality_signals` | service, fail_rate, p95_latency, avg/min Mbps, stability, runtime |
| `baseline_users` | highest user count with stable evidence |
| `degradation_users` | lowest user count where degradation was observed |
| `practical_capacity_estimate` | advisory midpoint or stable max when confidence permits |
| `confidence` | `LOW`, `MEDIUM`, `HIGH`, `CERTIFIED` |
| `reason` | human-readable explanation |
| `recommendation` | `observe`, `review`, `consider_limit_review`, never execute |
| `updated` | sample/update timestamp |

## Safe Progression

```text
Observe
  |
  v
Learn
  |
  v
Recommend
  |
  v
Future planner integration only after separate approval
```

## Reuse

Use existing patterns:

- `tools/v7-egress-quality-compact` for quality windows.
- `admin_core/intelligence_workers.py` for snapshot-only derived evidence.
- `admin_core/shadow_autonomy.py` for shadow comparison/evidence confidence.
- Existing `service_matrix`, runtime readiness, history, and assigned-user counts.

## Anti-Patterns

Do not create:

- new planner;
- new truth source;
- new database;
- new execution path;
- hidden autoswitch influence;
- direct writeback to capacity limits.

## Audit Verdict

Recommended future design: `Observed Capacity Shadow`, snapshot-only and advisory-only.
