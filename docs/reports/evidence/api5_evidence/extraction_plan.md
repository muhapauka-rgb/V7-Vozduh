# API.5 Extraction Plan

Program: API.5 - Runtime Read Views, Route Reality Views and Read-Only Performance Foundation

## Baseline

- Workspace branch: Updatesystem
- Baseline endpoint inventory: docs/reports/evidence/api5_evidence/before_endpoint_inventory.json
- Baseline admin monolith size: 36034 lines
- Safety mode: no deploy, no runtime mutation, no governance mutation

## Classification

### EXTRACT_NOW

- Runtime fingerprint payload construction
- Proxy runtime payload status classification
- systemctl service status payload normalization
- Per-user route reality row construction
- Direct-routing domain test parser
- Direct-routing freshness summary
- Direct-routing quick summary
- Traffic zero and traffic entity payload construction
- Client speed egress summary
- Killswitch summary payload construction
- Capacity pool and capacity state payload construction
- API.5 read-only schema contracts
- API.5 performance foundation map

### EXTRACT_LATER

- Live runtime command scheduling
- Larger operator timeline builders that still mix file reads and endpoint orchestration
- Full diagnostic endpoint orchestration
- UI route-specific decomposition
- Request-scoped read aggregation beyond lightweight snapshot dataclasses

### DO_NOT_TOUCH

- Auth, RBAC, CSRF
- do_POST and action routing
- run_action and execution handlers
- rollback handlers
- governance mutation handlers
- audit writers
- closure writers
- user movement
- autoswitch apply
- service restarts

## Ownership Decision

The admin monolith continues to own request entry, authentication, authorization, command invocation, file reads, and endpoint routing.

API.5 modules own pure read-only payload construction only.
