# V7 Vozduh — Track 7.11 Admin Auth & Security Runtime Lineage Batch

Generated: 2026-05-24

Scope: repo-side lineage resolution only. No live deploy, no VPS runtime mutation, no auth initialization, no password rotation, no admin command execution, no routing/datapath/autoswitch changes.

## 1. Tools Resolved

Resolved into repo-side lineage:

```text
v7-admin-auth-init
v7-admin-auth-status
v7-admin-password-rotate
v7-safe-run
```

`v7-safe-run` was included as the optional same-scope tool because runtime enumeration shows it is referenced by `v7-admin-api` and it is the admin safe-mode/security gate for delegated commands.

Repo path for all resolved tools:

```text
tools/runtime-support/
```

All copied hashes match `runtime-enumeration.json`.

## 2. Tools Skipped

No recommended admin-auth tools were missing or skipped.

Explicitly excluded from this batch:

```text
v7-user-switch
v7-routing-sync
v7-users-autoswitch
v7-policy-*
v7-direct-*
v7-proxy-*
v7-user-rotate-key
v7-maintenance-cleanup-apply
v7-secrets-cleanup-apply
```

## 3. Repo Paths Created / Updated

Created repo-side lineage copies:

```text
tools/runtime-support/v7-admin-auth-init
tools/runtime-support/v7-admin-auth-status
tools/runtime-support/v7-admin-password-rotate
tools/runtime-support/v7-safe-run
```

Created metadata:

```text
docs/track7/lineage/admin-auth-security-tools.json
```

Updated governance:

```text
docs/track7/PRODUCTION_ONLY_TOOL_GOVERNANCE.md
```

## 4. Admin / Security Safety Review

| Tool | Classification | Safety Notes |
|---|---|---|
| `v7-admin-auth-init` | `bootstrap-init` | Writes `/etc/v7/admin/auth.json`, creates `session_secret`, writes plaintext initial password to `/root/v7-admin-initial-password.txt` with mode `0600`, and writes audit event. |
| `v7-admin-auth-status` | `admin-auth-read` | Reads `/etc/v7/admin/auth.json` and checks initial password file existence. Does not print hash/session secret/password contents. |
| `v7-admin-password-rotate` | `password-rotation` | Rewrites auth config, writes backup, writes plaintext rotated password to `/etc/v7/admin/rotated-password.txt`, can invalidate sessions, unlinks initial password file, writes audit event. |
| `v7-safe-run` | `security-gate` | Blocks unknown commands and selected unsafe apply/lifecycle paths, then delegates to allowlisted commands and writes a `safe_run` audit event. Not pure read-only. |

No selected tool was executed against live admin/auth state.

## 5. Owner / Purpose / Mutation Classification

Owner:

```text
admin/security: v7-admin-auth-init, v7-admin-auth-status, v7-admin-password-rotate, v7-safe-run
```

Mutation classes:

```text
bootstrap-init: 1
admin-auth-read: 1
password-rotation: 1
security-gate: 1
```

## 6. Static Verification Results

Passed:

```text
tools/v7-run-tests
Ran 28 tests OK
```

Passed:

```text
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile \
  admin/v7-admin-api admin_core/*.py \
  tools/v7-release-lineage-check tools/v7-runtime-repo-diff \
  tools/runtime-support/v7-admin-auth-init \
  tools/runtime-support/v7-admin-auth-status \
  tools/runtime-support/v7-admin-password-rotate
```

Passed:

```text
bash -n tools/runtime-support/v7-safe-run
```

Passed:

```text
python3 -m json.tool docs/track7/lineage/admin-auth-security-tools.json
```

## 7. Updated Governance Counts

Before Track 7.11:

```text
Runtime-only unresolved tools: 92
Critical unresolved lineage: 60
Total lineage resolved in metadata: 31
```

After Track 7.11:

```text
Runtime-only unresolved tools by basename: 88
Critical unresolved lineage by basename: 59
Total lineage resolved in metadata: 35
Remaining known unresolved by lineage metadata: 83
```

## 8. Runtime / Repo Diff Result

Read-only diff result:

```text
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 88
Named lineage gaps: 88
Critical lineage gaps (known): 59
Unlisted lineage gaps: 0
Safe convergence candidates (known): 4
```

Warning remains:

```text
runtime_manifest_not_supplied
```

## 9. Release Object Warning Status

Release lineage checker result:

```text
lineage_resolved_tools=35
remaining_known_unresolved=83
runtime_lineage=partial
release_provenance=incomplete
release_object=releases/v7-runtime-20260523T174503Z ready=True missing=0
```

Warnings remain:

```text
runtime_manifest_missing_locally_or_not_supplied
source_worktree_dirty
known_83_production_only_tools_require_lineage
archive_manifest_missing_locally_or_not_supplied
```

Admin/security lineage visibility improved, but admin hardening is not complete.

## 10. Remaining Admin / Security Blockers

- `v7-admin-auth-init` and `v7-admin-password-rotate` are now lineage-resolved but remain live credential mutation tools.
- `v7-safe-run` is governed, but the safety of delegated commands still depends on each allowlisted tool's semantics.
- No live auth status, auth init, password rotation, session invalidation, or safe-run delegated flow was executed.
- Commercial reproducibility remains incomplete while 83 known production-only lineage gaps remain.

## 11. Next Bounded Batch Safety

Next batch is safe only if kept narrow and repo-side. Candidate next scopes:

- provisioning support lineage;
- profile delivery/token tooling lineage;
- backup/rollback support lineage;
- selected read-only policy diagnostics.

Do not mix routing mutation, policy apply, Direct/RU, proxy-public apply, or autoswitch tools into the next batch.
