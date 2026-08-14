# PERF.1 Fast Runtime Architecture

## Principle

Runtime is a consumer, not a thinker.

The runtime path may read compact summaries, validate hashes, enforce governance, and execute bounded selected moves. It must not run heavy service intelligence, broad history scans, network probe matrices, or expensive prediction.

## Allowed Runtime Inputs

- `users.registry`
- `egress.registry`
- `v7-state.json`
- autoswitch safety state
- restore barrier state
- compact service summary snapshot
- compact route-class/channel score snapshot
- compact execution trust summary
- compact dynamic blast radius summary
- selected move packet
- governance packet

## Runtime Must Never Do

- full service matrix refresh
- curl/socket probe matrix
- full audit/event JSONL scan
- SQLite traffic aggregation
- per-user predictive modeling across 2000 users
- per-user x per-channel x per-service heavy scoring
- background history compaction
- service intelligence recalculation
- hidden admin overview recomputation

## Runtime Decision Shape

1. Load bounded runtime snapshot.
2. Load compact intelligence summaries.
3. Compute eligible candidates using local hard gates.
4. Apply bounded advisory score parts from summaries.
5. Select moves under policy and blast radius caps.
6. Validate restore barrier and generation hashes.
7. If apply requested, execute only selected moves through governed path.
8. Emit audit/closure metadata.

## Target Runtime Complexity

- Planner: O(users + channels) over compact summaries
- Candidate ranking: O(eligible candidates), not O(users x channels x services x history)
- Snapshot reads: bounded file count
- History reads: zero full scans
- Network probes: zero
