# RI4-B Performance Certification

## Rule

```text
Brain may be heavy.
Runtime may not be heavy.
```

## Placement

Heavy work:

- user service score calculation;
- per-user per-channel candidate suitability;
- best available pool ranking.

Placement:

- `admin_core/intelligence_workers.py`
- `tools/v7-intelligence-snapshot-refresh`

Runtime:

- reads compact snapshots only;
- does not scan JSONL;
- does not run service probes;
- does not compute prediction;
- does not recompute candidate suitability from raw history.

## Benchmark Evidence

Generated locally with fixture samples:

```json
{
  "runs": 25,
  "snapshot_generation_mean_ms": 6.3788,
  "snapshot_generation_p95_ms": 7.0901,
  "max_snapshot_bytes": 7204,
  "total_snapshot_bytes": 22150,
  "runtime_mutation_performed": false
}
```

PERF.4 prior runtime hot-path certification:

```json
{
  "legacy_mean_ms": 2.7198,
  "snapshot_mean_ms": 1.1775,
  "snapshot_mode": "snapshot_backed_planner_advisory_context"
}
```

## Verdict

performance_certified=true

runtime_hot_path_heavy_work_added=false

snapshot_generation_bounded=true

