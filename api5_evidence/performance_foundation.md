# API.5 Performance Foundation

## Extension

API.5 extends the existing `admin_core.performance_summaries` ownership instead of creating a duplicate performance map.

Added read-only foundation:

- `api5_performance_foundation`
- API.5 payload builder modules
- API.5 request snapshot extension names
- Runtime and route read cache candidates
- Runtime and proxy async candidates

## No Runtime Cache Enabled

API.5 does not add caching, background workers, timers, scheduling, or persistence.

`no_cache_enabled=true` means the foundation is a contract and map only.

## Future Safe Candidates

- runtime_fingerprint: short TTL keyed by component mtimes
- proxy_runtime: short TTL keyed by runtime file mtimes and service state
- direct_routing: TTL keyed by direct-domain state and user IP
- route_reality: async probe candidate
- traffic_summary: SQLite summary cache candidate

## Forbidden Request Path Items Preserved

- runtime_execution
- rollback_execution
- governance_mutation
- audit_append
- closure_append
- service_restart
- autoswitch_apply
- user_movement
