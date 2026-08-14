# API.4 Performance-First Plan

## Runtime Path Map

- runtime platform: server-owned
- runtime state: admin reads only
- execution: not owned by overview layer
- rollback: not owned by overview layer
- governance mutation: not owned by overview layer

## Admin Path Map

- request entry: `admin/v7-admin-api Handler`
- overview orchestration: `admin/v7-admin-api overview`
- overview builders: `admin_core.overview_views`
- registry views: `admin_core.admin_registry_views`
- service views: `admin_core.service_views`
- route views: `admin_core.route_views`
- operator views: `admin_core.operator_views`
- shared summaries: `admin_core.summary_builders`
- performance architecture: `admin_core.performance_summaries`

## Cache Candidates

- overview
- service matrix
- route reality
- Trusted RU
- traffic summary
- audit tail

## Background Aggregation Candidates

- route reality snapshot
- traffic summary snapshot
- Trusted RU diagnostic snapshot
- service matrix refresh
- client speed rollup
- overview boot payload

## Async Candidates

- direct routing probe
- Trusted RU live diagnostic
- route status per-user probe
- traffic live probe
- capacity command reads

## Must Never Execute Inside Implicit Request Path

- runtime execution
- rollback execution
- governance mutation
- audit append
- closure append
- service restart
- autoswitch apply
- user movement
