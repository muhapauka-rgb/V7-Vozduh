# PERF.4 Discovery And Duplication Audit

Date: 2026-06-03
Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`

## Baseline

`git status --short` was clean before PERF.4 implementation.

Baseline full test suite:

```text
Ran 241 tests in 11.023s
OK
```

## Runtime Planner Ownership

Runtime planner owner remains:

- `tools/v7-users-autoswitch`

Existing runtime intelligence path before PERF.4:

- `AutoswitchPlanner._routing_intelligence_scores_for_user`
- `AutoswitchPlanner._routing_brain_advisory`
- direct `RoutingBrain(...)` construction in runtime planner
- direct `_recent_audit_records()` history read from `switch-history.jsonl`

PERF.4 replacement scope:

- runtime candidate advisory scores may now be read from `channel-service-scores.json`
- runtime advisory context may now be read from `risk-summaries.json`, `trust-summaries.json`, and `blast-radius-summaries.json`
- runtime snapshot gate validates `service-scores.json`, `channel-service-scores.json`, `risk-summaries.json`, `trust-summaries.json`, and `blast-radius-summaries.json`
- `user-service-scores.json` is advisory-only and may be ignored when stale/missing

Out of PERF.4 scope:

- execution
- rollback
- governance mutation
- selected move writers
- audit writers
- auth/RBAC/CSRF
- user movement
- deployment/runtime mutation
- capacity forecast snapshot consumption

## Duplication Audit

No duplicate runtime orchestrator was created.

No duplicate selected move writer was created.

No duplicate execution path was created.

No duplicate governance path was created.

Legacy `RoutingBrain` runtime construction remains as fallback only when no snapshot store is active. When a snapshot store is active, runtime consumes compact snapshot data and does not read runtime history in the fast path.

