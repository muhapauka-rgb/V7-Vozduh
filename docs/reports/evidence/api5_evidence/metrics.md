# API.5 Metrics

## Line Counts

- `admin/v7-admin-api`: 35747 lines after API.5
- `admin_core/runtime_read_views.py`: 120 lines
- `admin_core/route_reality_views.py`: 163 lines
- `admin_core/diagnostic_views.py`: 241 lines
- `admin_core/performance_summaries.py`: 180 lines
- `tests/unit/test_api5_runtime_route_diagnostic_views.py`: 196 lines

## Monolith Reduction

- `admin/v7-admin-api` diff: 56 insertions, 343 deletions
- Net reduction in monolith diff: 287 lines
- Inventory source_line_count before: 36034
- Inventory source_line_count after: 35747
- Inventory line-count reduction: 287 lines

## New Read-Only Module Surface

- Runtime read module: 120 lines
- Route reality module: 163 lines
- Diagnostic module: 241 lines
- API.5 unit test module: 196 lines

## Extracted Functions

- `runtime_fingerprint_payload`
- `service_status_payload`
- `proxy_runtime_payload`
- `route_status_row`
- `parse_direct_domain_test`
- `direct_routing_freshness_summary`
- `direct_routing_quick_summary`
- `traffic_zero_summary`
- `traffic_entity_payload`
- `client_speed_summary`
- `killswitch_summary`
- `capacity_pool_row`
- `capacity_state`
- `api5_performance_foundation`
