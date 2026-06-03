# PERF.1 Performance Risk Analysis

## Largest Future Risks

1. Running Heavy Brain per user in runtime.
2. Hidden service probes in admin overview or planner.
3. Full audit/event JSONL scans during live apply.
4. SQLite traffic aggregation inside broad overview requests.
5. Network probe storms across 50 channels.
6. Duplicate service suitability calculations in planner and RI.
7. Snapshot freshness UNKNOWN being treated as OK.

## CPU Risks

- users x channels x services x windows scoring
- prediction models over long histories
- repeated JSON parsing of large summaries
- unbounded log aggregation

## Memory Risks

- materializing all user histories
- loading full audit/event logs
- admin endpoints returning too much detail
- per-request full service matrix expansion

## Disk Risks

- append-only probe history without compaction
- large JSON snapshots with per-user/per-service raw detail
- raw evidence duplication inside runtime state

## Network-Test Risks

- 50 channels x many services x short interval
- Telegram multi-endpoint checks multiplied per channel
- direct/trusted RU checks triggered by UI refresh

## Main Mitigation

PERF.2 must define the snapshot store and freshness gate before RI.4 expands intelligence.
