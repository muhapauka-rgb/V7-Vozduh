# Z7.4 Discovery Scope

Project: V7 Vozduh  
Branch target: v7-next  
Mode: READ ONLY implementation conflict audit  
Date: 2026-06-02

## Scope

Z7.4 audited the conflict surface for adding operation lineage wiring to:

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

No code implementation, runtime mutation, autoswitch apply, service restart, systemd mutation, timer mutation, deletion, merge, deploy, cleanup, or force push was performed.

The local working tree contains unrelated dirty/untracked files. Z7.4 treated tracked source and current Z6/Z7 audit outputs as audit context and did not stage or modify unrelated work.

## Main Evidence Commands

- `git status --short --branch`
- `git diff --name-only origin/v7-next..HEAD`
- `rg --files | rg '(^tools/v7-users-autoswitch$|autoswitch|v7-users)'`
- `git grep -n "v7-users-autoswitch" -- .`
- `git grep -n "selected_moves|autoswitch-selected-moves|autoswitch-restore-barrier" -- admin/v7-admin-api admin_core/operator_execution.py admin_core/operator_observability.py tests tools systemd`
- `git grep -n "operation_id|request_id|correlation_id|event_id|record_hash|runtime_snapshot_hash|planner_generation_id" -- admin/v7-admin-api admin_core tools tests`
- `git grep -n "json.loads|get(\"plan\"|plan\\.|selected_moves|apply_result" -- admin/v7-admin-api admin_core tools tests`

## Primary Files Inspected

| File | Role |
|---|---|
| `tools/v7-users-autoswitch` | Runtime autoswitch planner/apply JSON producer and partial orchestrator owner |
| `systemd/v7-users-autoswitch.service` | Scheduler/service bridge invoking `/usr/local/bin/v7-users-autoswitch --apply` |
| `systemd/v7-users-autoswitch.timer` | Periodic runtime cycle scheduler |
| `admin/v7-admin-api` | Admin autoswitch endpoints, JSON parser, UI consumer, selected move adapters |
| `admin_core/operator_execution.py` | Runtime recheck and selected-move hash reader |
| `admin_core/operator_observability.py` | Operator observability selected-move/barrier readers |
| `tools/runtime-support/v7-audit-log` | Existing audit sink and `request_id` owner |
| `tools/v7-control-plane-governance-check` | Report generator / governance evidence parser |
| `tests/unit/test_v7_users_autoswitch_policy.py` | Main autoswitch policy/schema behavior test target |

## Discovery Note

Some tracked historical evidence files contain very large embedded autoswitch JSON and journal logs. They prove legacy consumers and output shape but are not active code consumers. Active code consumer classification is therefore separated from historical report/evidence classification.
