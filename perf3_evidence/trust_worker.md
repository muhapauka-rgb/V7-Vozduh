# PERF.3 Trust Worker

## Inputs

- audit history
- switch history
- rollback history

## Output

- `trust-summaries.json`

## Reused Logic

- `ExecutionTrustModel.from_records`

## Bounded Reads

JSONL tail reader limits:

- `MAX_HISTORY_RECORDS=1000`
- `MAX_HISTORY_BYTES=512000`

Corrupt JSONL lines are skipped.

If more records are available than the bound, the worker uses the latest bounded records and writes warning:

- `history_records_truncated_to_bound`

## Output Shape

- trust score
- counters
- median blast radius
- records_seen
- records_available
- bounded=true
- runtime_decision_authority=`none_snapshot_only`

## Failure Behavior

Missing history yields a valid snapshot with warning:

- `history_missing`
