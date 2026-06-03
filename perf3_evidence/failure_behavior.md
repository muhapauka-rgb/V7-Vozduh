# PERF.3 Failure Behavior

## Missing Inputs

Workers produce valid snapshot envelopes with warnings and lower confidence.

Examples:

- missing service matrix -> `service_matrix_missing_or_empty`
- missing quality summary -> `quality_summary_missing_or_empty`
- missing history -> `history_missing`
- missing runtime state -> `runtime_state_missing`

## Stale Inputs

PERF.3 producers do not yet ingest source mtimes as freshness decisions. Freshness is expressed in produced snapshot envelope timestamps and is enforced by PERF.2 readers.

## Corrupt Inputs

CLI JSON reads treat corrupt JSON as default empty structures.

JSONL tail reader skips corrupt lines and keeps valid bounded records.

## Partial Inputs

Partial service/channel data still produces valid snapshots. Confidence decreases through confidence factors:

- source_completeness
- history_completeness
- probe_completeness
- service_completeness

## Runtime Impact

Runtime is unaffected because PERF.3 does not integrate snapshots into runtime decisions.
