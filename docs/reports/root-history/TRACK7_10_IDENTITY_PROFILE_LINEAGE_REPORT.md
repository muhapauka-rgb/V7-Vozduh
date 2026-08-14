# V7 Vozduh — Track 7.10 Identity & Profile Support Lineage Batch

Generated: 2026-05-24

Scope: repo-side lineage resolution only. No live deploy, no VPS runtime mutation, no key rotation, no config reissue, no identity bind/sync execution, no live profile generation, no routing/datapath/autoswitch changes.

## 1. Tools Resolved

Resolved into repo-side lineage:

```text
v7-user-reissue-config
v7-user-rotate-key
v7-smart-client-profile-generate
v7-proxy-identity-bind
v7-proxy-identity-sync-users
v7-proxy-multi-user-identity-dry-run
v7-proxy-two-identity-live-probe
```

Repo path for all resolved tools:

```text
tools/runtime-support/
```

All copied hashes match `runtime-enumeration.json`.

## 2. Tools Skipped

Skipped intentionally:

```text
v7-admin-auth-init
v7-admin-auth-status
v7-admin-password-rotate
```

Reason: present in runtime enumeration, but admin auth/password tooling belongs in a separate admin/security lineage batch. It is adjacent to identity, but not core customer profile/support lineage.

Explicitly excluded from this batch:

```text
v7-user-switch
v7-routing-sync
v7-users-autoswitch
v7-policy-*
v7-direct-*
v7-proxy-public-enable
v7-proxy-public-disable
v7-proxy-runtime-guard-apply
v7-maintenance-cleanup-apply
v7-secrets-cleanup-apply
```

## 3. Repo Paths Created / Updated

Created repo-side lineage copies:

```text
tools/runtime-support/v7-user-reissue-config
tools/runtime-support/v7-user-rotate-key
tools/runtime-support/v7-smart-client-profile-generate
tools/runtime-support/v7-proxy-identity-bind
tools/runtime-support/v7-proxy-identity-sync-users
tools/runtime-support/v7-proxy-multi-user-identity-dry-run
tools/runtime-support/v7-proxy-two-identity-live-probe
```

Created metadata:

```text
docs/track7/lineage/identity-profile-support-tools.json
```

Updated governance:

```text
docs/track7/PRODUCTION_ONLY_TOOL_GOVERNANCE.md
```

## 4. Identity / Profile Safety Review

| Tool | Classification | Safety Notes |
|---|---|---|
| `v7-user-reissue-config` | `customer-config-write` | Rebuilds client `.conf` and QR from existing keys; writes backups and chmods artifacts. Supports dry-run but normal mode writes customer profile material. |
| `v7-user-rotate-key` | `key-rotation` | High risk. Rotates WireGuard keypair, rewrites `/etc/wireguard/wg0.conf`, updates live `wg` peer state, and calls `v7-routing-sync` for enabled users. Lineage only. |
| `v7-smart-client-profile-generate` | `profile-write` | Writes Karing/Hiddify/Happ profiles containing WireGuard or VLESS credential material. Redacted print exists, but normal mode writes secrets to output files. |
| `v7-proxy-identity-bind` | `identity-binding-write` | Preview is temp-only; apply mode writes disabled proxy identity binding JSON with proxy UUID after confirm. Does not start service or change routing by itself. |
| `v7-proxy-identity-sync-users` | `identity-binding-write` | Preview prints plan with redacted UUIDs; apply mode writes disabled binding files and backups after confirm. |
| `v7-proxy-multi-user-identity-dry-run` | `dry-run` | Reads proxy/runtime/registry state and writes temporary summary files only. Not a passive pure function, but declares no persistent writes/routing/firewall changes. |
| `v7-proxy-two-identity-live-probe` | `live-probe` | Starts temporary loopback sing-box processes and performs curl probes after confirm. No persistent runtime writes, but not safe for casual test execution. |

No tool was executed against live identity/profile state.

## 5. Owner / Purpose / Mutation Classification

Owners:

```text
identity/profile: v7-user-reissue-config, v7-user-rotate-key, v7-smart-client-profile-generate
proxy-identity: v7-proxy-identity-bind, v7-proxy-identity-sync-users, v7-proxy-multi-user-identity-dry-run, v7-proxy-two-identity-live-probe
```

Mutation classes:

```text
customer-config-write: 1
key-rotation: 1
profile-write: 1
identity-binding-write: 2
dry-run: 1
live-probe: 1
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
  tools/runtime-support/v7-smart-client-profile-generate \
  tools/runtime-support/v7-proxy-identity-sync-users
```

Passed:

```text
bash -n \
  tools/runtime-support/v7-user-reissue-config \
  tools/runtime-support/v7-user-rotate-key \
  tools/runtime-support/v7-proxy-identity-bind \
  tools/runtime-support/v7-proxy-multi-user-identity-dry-run \
  tools/runtime-support/v7-proxy-two-identity-live-probe
```

Passed:

```text
python3 -m json.tool docs/track7/lineage/identity-profile-support-tools.json
```

## 7. Updated Governance Counts

Before Track 7.10:

```text
Runtime-only unresolved tools: 99
Critical unresolved lineage: 67
Total lineage resolved in metadata: 24
```

After Track 7.10:

```text
Runtime-only unresolved tools by basename: 92
Critical unresolved lineage by basename: 60
Total lineage resolved in metadata: 31
Remaining known unresolved by lineage metadata: 87
```

## 8. Runtime / Repo Diff Result

Read-only diff result:

```text
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 92
Named lineage gaps: 92
Critical lineage gaps (known): 60
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
lineage_resolved_tools=31
remaining_known_unresolved=87
runtime_lineage=partial
release_provenance=incomplete
release_object=releases/v7-runtime-20260523T174503Z ready=True missing=0
```

Warnings remain:

```text
runtime_manifest_missing_locally_or_not_supplied
source_worktree_dirty
known_87_production_only_tools_require_lineage
archive_manifest_missing_locally_or_not_supplied
```

Identity/profile lineage visibility improved, but commercial reproducibility is still incomplete.

## 10. Remaining Identity / Profile Blockers

- Admin auth/password tools are still unresolved and should be handled in a separate admin/security batch.
- Identity/profile tools are now lineage-resolved in repo, but their live behavior remains high-risk and customer-affecting.
- No endpoint/admin contract was changed, and no live identity/profile workflow was exercised.
- Apply/write paths for proxy identity and key rotation still need future guarded operational runbooks before commercial use.

## 11. Next Bounded Batch Safety

Next batch is safe only if it remains narrow and repo-side:

- admin auth/status/password lineage, or
- provisioning support lineage, or
- profile delivery/token tooling lineage.

Do not move next into routing/policy/proxy-public/autoswitch mutation tools until those are isolated as their own high-risk governance batch.
