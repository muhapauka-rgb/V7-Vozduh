# PERF.2 Performance Certification

Mode: local synthetic benchmark of read-only snapshot readers.

No runtime commands, network probes, planner integration, or writes were performed.

## Results

- single snapshot reads: 1000
  - total: 54.322 ms
  - average: 0.0543 ms

- bundle reads: 200 bundles x 9 families
  - total: 102.438 ms
  - average bundle: 0.5122 ms

- validation + freshness + behavior checks: 10000
  - total: 48.658 ms
  - average: 0.0049 ms

## Verdict

Snapshot contract reads are cheap enough for runtime consumption if snapshots remain compact and bounded.

The implemented reader enforces `MAX_SNAPSHOT_BYTES=1000000`.

Performance certified for PERF.2 interface scope.
