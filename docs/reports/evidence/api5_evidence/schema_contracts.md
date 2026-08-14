# API.5 Schema Contracts

## Runtime Read Views

- `runtime_summary`
  - schema: `v7.admin.runtime-summary.v1`
  - read_only: true
  - required: status, summary, components, read_only

- `runtime_snapshot`
  - schema: `v7.admin.runtime-snapshot.v1`
  - read_only: true
  - required: state, components

## Route Reality Views

- `route_reality`
  - schema: `v7.admin.route-reality.v1`
  - read_only: true
  - required: ip, current, expected_dev, route_get, ok, leak_risk

- `trusted_ru`
  - schema: `v7.admin.trusted-ru-summary.v1`
  - read_only: true
  - required: validation, checks, blockers, warnings

## Diagnostic Views

- `diagnostic`
  - schema: `v7.admin.diagnostic.v1`
  - read_only: true
  - required: status

- `traffic_summary`
  - schema: `v7.admin.traffic-summary.v1`
  - read_only: true
  - required: entity_type, entity_id, today, last_24h, week, month, all_time

## Performance Foundation

- `api5_performance_foundation`
  - schema: `v7.admin.api5-performance-foundation.v1`
  - read_only: true
  - no_cache_enabled: true
  - modules: runtime_read_views, route_reality_views, diagnostic_views
