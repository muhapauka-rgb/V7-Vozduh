# API.4 Performance Measurement

## Mode

Static and pure-builder measurement.

Live `overview()` benchmarking was not performed because the function executes read-only runtime/probe commands. API.4 did not add runtime probing or production measurement commands.

## Before

- monolith line count before API.4: `36046`
- `overview()` users registry reads: up to `2`
- overview summary builder: inline in `admin/v7-admin-api`
- registry/check payload builders: inline in `admin/v7-admin-api`

## After

- monolith line count after API.4: `36034`
- `overview()` users registry reads: `1`
- overview summary builder: `admin_core.overview_views.build_summary`
- registry/check payload builders: `admin_core.overview_views`

## Pure Builder Timing Sample

Measured with synthetic in-memory data:

- `overview_summary_builder`: `0.035 ms`
- `egress_health_summary`: `0.011 ms`

These timings are not production latency. They show that the extracted pure builders are negligible compared with command probes, route checks, JSONL reads, and SQLite summaries.
