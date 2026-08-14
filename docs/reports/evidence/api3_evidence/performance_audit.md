# API.3 Performance Foundation Audit

## Before/After

- monolith line count before API.3: `36459`
- monolith line count after API.3: `36046`
- lines removed from monolith: `413`

## Foundation Added

- Request/query extraction helpers moved to `admin_core.summary_builders`.
- Bounded JSONL reader foundation added as `bounded_jsonl_records`.
- Service matrix and service recommendation builders moved out of the hot monolith path.
- Trusted RU diagnostic/readiness builders moved to reusable pure route builders.
- Schema contracts were added for future parity protection.

## Remaining Hotspots

- `overview()` still performs broad aggregation and runtime read calls.
- `route_status()` still performs per-user `run_readonly` route probes.
- Trusted/direct route live checks still call command-line diagnostics.
- Traffic summaries still involve SQLite reads.
- `Handler` remains large and owns dispatch, auth, JSON responses, actions, and redirects.
- `html_page_v2` remains a large UI string.

## Future Cache Opportunities

- overview short-TTL snapshot keyed by registry/state/policy mtimes
- service matrix file-backed latest summary
- Trusted RU background diagnostic status
- route reality background snapshot
- traffic SQLite summary snapshot

No cache was added in API.3 because the goal was behavior-preserving read-only decomposition.
