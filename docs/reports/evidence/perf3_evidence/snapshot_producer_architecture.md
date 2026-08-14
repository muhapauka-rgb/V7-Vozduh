# PERF.3 Snapshot Producer Architecture

## Module

`admin_core/intelligence_workers.py`

Responsibilities:

- build service/channel score snapshots
- build trust snapshot
- build risk snapshot
- build blast radius snapshot
- build overview snapshot
- write snapshot files atomically when explicitly called

## CLI

`tools/v7-intelligence-snapshot-refresh`

The CLI reads explicit input files/directories and writes snapshots to an output directory unless `--dry-run` is used.

Default output:

`/opt/v7/egress/state/intelligence/`

PERF.3 did not run it against production paths.

## Snapshot Families Produced

- `service-scores.json`
- `channel-service-scores.json`
- `trust-summaries.json`
- `risk-summaries.json`
- `blast-radius-summaries.json`
- `overview-summary.json`

## Envelope

Every produced snapshot uses the PERF.2 envelope:

- schema
- generated_at
- expires_at
- ttl_seconds
- freshness_state
- confidence
- source_hashes
- generator
- item_count
- warnings
- confidence_factors

## Atomic Writes

`write_snapshots()` writes only snapshot files. It does not write runtime state, registries, selected moves, governance state, audit logs, or service files.
