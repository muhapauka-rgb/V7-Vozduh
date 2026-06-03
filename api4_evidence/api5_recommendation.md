# API.5 Recommendation

## Recommended Scope

API.5 should extract read-only runtime command read adapters and route reality snapshots.

Suggested modules:

- `admin_core.runtime_read_views`
- `admin_core.route_reality_views`

## First Safe Candidates

- `service_status`
- route reality serialization around existing `route_status` result shape
- stale/killswitch/capacity result serializers
- direct/trusted diagnostic result serializers
- overview command-read timing hooks

## Required Guards

- no `run_action`
- no POST apply handlers
- no auth/RBAC/CSRF movement
- no rollback execution
- no governance mutation
- no audit writes
- no closure writes

## Required Tests

- `/api/overview` fixture parity
- route reality response parity
- endpoint inventory unchanged
- command adapter safety scan
- full unit suite
