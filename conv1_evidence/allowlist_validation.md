# CONV.1 Allowlist Validation Evidence

Owner: `tools/v7_sync_lib.APPROVED_DEPLOY_FILES`

## Runtime Entrypoints

- `tools/v7-users-autoswitch`
- `tools/v7-intelligence-snapshot-refresh`
- `admin/v7-admin-api`
- `tools/v7-operator-execution-packet`

## Validation Model

CONV.1 adds `deploy_allowlist_validation()` with schema:

`v7-deploy-allowlist-validation/v1`

The validation performs:

- local file existence checks for every approved deploy file;
- duplicate remote target detection;
- AST import discovery from runtime entrypoints into `admin_core`;
- required runtime dependency comparison against the deploy allowlist.

## Observed Result

The validation returned:

```text
final_verdict=PASS
missing_required_paths=[]
missing_local_files=[]
duplicate_remote_paths=[]
```

## PERF.4 Closure

The prior SYNC.1 blocker was that PERF.4 introduced deploy-required files that were not present in the
safe deploy allowlist:

- `admin_core/intelligence_snapshots.py`
- `admin_core/intelligence_workers.py`
- `tools/v7-intelligence-snapshot-refresh`

CONV.1 includes those files in the canonical allowlist and makes future omissions fail closed before deploy.

