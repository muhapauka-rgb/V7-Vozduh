# PERF.3 Updated Load Model

## PERF.1 Targets Rechecked

| Area | PERF.1 target | PERF.3 result |
|---|---:|---:|
| Heavy Brain service/trust/risk/blast/overview production | background, under seconds | 37.043 ms for 50 channels synthetic |
| Snapshot size | under 1 MB per snapshot | max 10009 bytes |
| Runtime path | unchanged | unchanged |
| Governance path | unchanged | unchanged |
| Network probe budget | no hidden probes | no probes added |

## CPU Budget

Current producer batch for 50 channels / 2000 users / 10 services is comfortably under 100 ms locally.

Recommended PERF.3 cadence remains safe:

- service score worker: 60s
- trust worker: 300s
- risk worker: 60s
- blast radius worker: 60s
- overview worker: 30s

## Disk Budget

Current six snapshots total about 18 KB for 50 channels.

Even with service expansion, the PERF.2 1 MB snapshot read ceiling remains realistic if producers keep raw history out of snapshots.

## Probe Budget

PERF.3 adds no probes.

Probe scheduling remains deferred to future adaptive testing work.
