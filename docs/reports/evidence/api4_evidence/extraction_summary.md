# API.4 Extraction Summary

## New Modules

- `admin_core/overview_views.py`
- `admin_core/performance_summaries.py`

## Extracted Overview Layer

`admin_core.overview_views` now owns:

- `OverviewSnapshot`
- request-scoped overview snapshot creation
- active user derivation
- egress health summary
- overview summary payload builder
- registry payload builder
- checks payload builder
- overview/API.4 schema contracts

## Extracted Performance Summary Layer

`admin_core.performance_summaries` now owns:

- runtime path map
- admin path map
- overview dependency map
- cache candidates
- background aggregation candidates
- async candidates
- request-path forbidden items
- small pure measurement helper

## What Remained In The Monolith

- `overview()` orchestration
- runtime command reads
- route probes
- service status reads
- HTTP handlers
- auth/session/RBAC/CSRF
- mutation handlers
- audit and closure writers
