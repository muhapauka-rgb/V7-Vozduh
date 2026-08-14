# API.3 Metrics

## Line Counts

- `admin/v7-admin-api` before API.3: `36459`
- `admin/v7-admin-api` after API.3: `36046`
- lines removed from monolith: `413`
- `admin_core/operator_views.py`: `70`
- `admin_core/service_views.py`: `321`
- `admin_core/route_views.py`: `224`
- `admin_core/summary_builders.py`: `95`
- API.3 admin_core lines added: `710`
- `tests/unit/test_api3_read_only_views.py`: `127`

## New Modules

- `admin_core.operator_views`
- `admin_core.service_views`
- `admin_core.route_views`
- `admin_core.summary_builders`

## Remaining Monolith Size

`admin/v7-admin-api` remains `36046` lines.

## Top Remaining Hotspots

- HTTP `Handler`
- `html_page_v2`
- `overview`
- traffic summaries
- direct/trusted live route checks
- egress draft/runtime helpers
- mutation/action response wrappers
