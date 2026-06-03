# API.4 Metrics

## Line Counts

- `admin/v7-admin-api` before API.4: `36046`
- `admin/v7-admin-api` after API.4: `36034`
- lines removed from monolith in API.4: `12`
- `admin_core/overview_views.py`: `213`
- `admin_core/performance_summaries.py`: `141`
- API.4 admin_core lines added: `354`
- `tests/unit/test_api4_overview_performance.py`: `108`

## New Modules

- `admin_core.overview_views`
- `admin_core.performance_summaries`

## Remaining Monolith Size

`admin/v7-admin-api` remains `36034` lines.

## Remaining Hotspots

- `html_page_v2`
- `Handler`
- `overview()` orchestration
- per-user route probes
- direct/trusted live checks
- traffic SQLite summaries
- mutation/action response wrappers
