# SYNC.1 Phase 3 - Safe Deploy Gate

Tool discovered:

```text
tools/v7-safe-deploy
```

Approved deploy files from `tools/v7_sync_lib.py`:

```text
tools/v7-users-autoswitch -> /usr/local/bin/v7-users-autoswitch
tools/runtime-support/v7-audit-log -> /usr/local/bin/v7-audit-log
admin/v7-admin-api -> /usr/local/bin/v7-admin-api
tools/v7-operator-execution-packet -> /usr/local/bin/v7-operator-execution-packet
admin_core/operator_execution.py -> /usr/local/bin/admin_core/operator_execution.py
```

PERF.4 requires production availability of additional files:

```text
admin_core/intelligence_snapshots.py
admin_core/intelligence_workers.py
tools/v7-intelligence-snapshot-refresh
```

These files are not in the approved safe-deploy allowlist.

Dry-run result after network/GitHub read was allowed:

```text
tool=v7-safe-deploy
mode=dry-run
final_verdict=PASS
deployment_required=true
commit=9facbc19be40a71490d97fea797086132bd89dba
```

Important deploy delta:

```text
v7-users-autoswitch matches=false
v7-audit-log matches=true
v7-admin-api matches=false
v7-operator-execution-packet matches=false
admin_core/operator_execution.py matches=false
```

Decision:

```text
safe_deploy_apply_run=false
reason=approved_safe_deploy_scope_does_not_cover_complete_PERF4_runtime_package
```

No deploy, service restart, route mutation, autoswitch apply, or user movement was performed.

