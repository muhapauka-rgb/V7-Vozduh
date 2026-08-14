# V7 Vozduh Track 7.16 Report

## Read-Only Policy / Direct / Proxy Diagnostics Lineage Batch

Track 7.16 resolved repo-side lineage for policy, Direct/RU, route visibility, and proxy runtime diagnostics/readiness tooling. No VPS runtime mutation, policy apply, routing sync, autoswitch execution, nftables change, route change, proxy runtime apply, service restart, Direct/RU behavior change, chmod/chown, delete/archive, or live diagnostic execution was performed.

## 1. Tools Resolved

```text
v7-direct-diagnose-domain
v7-direct-list
v7-direct-status
v7-direct-test-domain
v7-policy-live-preview
v7-policy-matrix
v7-policy-route-check
v7-policy-show
v7-policy-test-domain
v7-proxy-inbound-loopback-test
v7-proxy-inbound-preflight
v7-proxy-policy-runtime-adapter-dry-run
v7-proxy-public-candidate-preview
v7-proxy-public-enable-guard-dry-run
v7-proxy-route-policy-dry-run
v7-proxy-runtime-guard-apply-preview
v7-proxy-service-aware-routing-dry-run
```

All resolved tools were copied read-only from `/usr/local/bin` into `tools/runtime-support/`, with hashes matching `runtime-enumeration.json`.

## 2. Tools Skipped

```text
v7-policy-resolve
v7-direct-add-domain
v7-direct-remove-domain
v7-direct-auto-sync
v7-proxy-runtime-guard-apply
v7-proxy-public-enable
v7-proxy-public-disable
v7-trusted-ru-diagnostic
```

Reasons:

- `v7-policy-resolve` writes `/opt/v7/egress/state/route-classes.state`.
- Direct add/remove/auto-sync tools mutate Direct/RU runtime state.
- Proxy enable/disable/apply tools mutate public/proxy runtime state.
- `v7-trusted-ru-diagnostic` is deferred to a separate Trusted RU/Gosuslugi-sensitive review.

## 3. Repo Paths Created / Updated

Created:

```text
docs/track7/lineage/policy-direct-proxy-diagnostics-tools.json
TRACK7_16_POLICY_DIRECT_PROXY_DIAGNOSTICS_LINEAGE_REPORT.md
tools/runtime-support/v7-direct-diagnose-domain
tools/runtime-support/v7-direct-list
tools/runtime-support/v7-direct-status
tools/runtime-support/v7-direct-test-domain
tools/runtime-support/v7-policy-live-preview
tools/runtime-support/v7-policy-matrix
tools/runtime-support/v7-policy-route-check
tools/runtime-support/v7-policy-show
tools/runtime-support/v7-policy-test-domain
tools/runtime-support/v7-proxy-inbound-loopback-test
tools/runtime-support/v7-proxy-inbound-preflight
tools/runtime-support/v7-proxy-policy-runtime-adapter-dry-run
tools/runtime-support/v7-proxy-public-candidate-preview
tools/runtime-support/v7-proxy-public-enable-guard-dry-run
tools/runtime-support/v7-proxy-route-policy-dry-run
tools/runtime-support/v7-proxy-runtime-guard-apply-preview
tools/runtime-support/v7-proxy-service-aware-routing-dry-run
```

Updated:

```text
docs/track7/PRODUCTION_ONLY_TOOL_GOVERNANCE.md
```

## 4. Lineage Metadata File

```text
docs/track7/lineage/policy-direct-proxy-diagnostics-tools.json
```

The metadata records runtime path, sha256, size, mode, mtime, reference evidence, repo path, owner, purpose, mutation level, policy/routing/proxy reads and writes, Direct/RU behavior, audit behavior, logging/redaction behavior, verification requirements, and safety notes.

## 5. Policy / Direct / Proxy Diagnostics Safety Review

Direct/RU tools:

- `v7-direct-list` and `v7-direct-status` are read-only visibility tools.
- `v7-direct-test-domain` reads DNS, nft direct sets, and route decisions.
- `v7-direct-diagnose-domain` also performs external HTTPS probing and writes/removes a temporary `/tmp` output file.

Policy tools:

- `v7-policy-live-preview` prints would-add route/rule actions only.
- `v7-policy-show` reads policy and Trusted RU diagnostic state only.
- `v7-policy-test-domain` and `v7-policy-route-check` perform route/policy diagnostics.
- `v7-policy-matrix` is read-only by default, but `--write-state` writes a summary state file and remains out of scope for execution.

Proxy tools:

- `v7-proxy-inbound-preflight` reads host/network/service readiness and can perform public IP probing.
- `v7-proxy-route-policy-dry-run`, `v7-proxy-policy-runtime-adapter-dry-run`, `v7-proxy-public-candidate-preview`, `v7-proxy-public-enable-guard-dry-run`, `v7-proxy-runtime-guard-apply-preview`, and `v7-proxy-service-aware-routing-dry-run` use temporary files/configs and read live state, but static review found no runtime file writes, route writes, nft writes, service starts, or user moves.
- `v7-proxy-inbound-loopback-test` starts temporary loopback-only `sing-box` processes if executed; it is lineage-resolved but not passive read-only execution.

## 6. Owner / Purpose / Mutation Classification

```text
Direct/RU:
  v7-direct-diagnose-domain -> direct-diagnostic network-probe temp-file
  v7-direct-list -> read-only direct-state-read
  v7-direct-status -> read-only direct-status
  v7-direct-test-domain -> route-check direct-state-read

Policy:
  v7-policy-live-preview -> policy-preview read-only
  v7-policy-matrix -> policy-read by default; optional summary-write
  v7-policy-route-check -> route-check read-only wrapper
  v7-policy-show -> policy-read trusted-ru-state-read
  v7-policy-test-domain -> policy-read route-check

Proxy runtime:
  v7-proxy-inbound-loopback-test -> loopback-live-probe temp-process
  v7-proxy-inbound-preflight -> readiness-check state-read network-probe
  v7-proxy-policy-runtime-adapter-dry-run -> proxy-runtime-check temp-config
  v7-proxy-public-candidate-preview -> proxy-runtime-check temp-config
  v7-proxy-public-enable-guard-dry-run -> readiness-check chained-dry-run
  v7-proxy-route-policy-dry-run -> route-check proxy-runtime-check
  v7-proxy-runtime-guard-apply-preview -> proxy-runtime-check apply-preview
  v7-proxy-service-aware-routing-dry-run -> policy-preview proxy-runtime-check temp-config
```

## 7. Static Verification Results

```text
bash -n <17 resolved tools>
OK

python3 -m json.tool docs/track7/lineage/policy-direct-proxy-diagnostics-tools.json
OK

tools/v7-run-tests
Ran 28 tests
OK

PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/*.py tools/v7-release-lineage-check tools/v7-runtime-repo-diff
OK
```

No diagnostic tool was executed against live routing/policy/proxy state.

## 8. Updated Governance Counts

Before Track 7.16:

```text
Runtime-only unresolved tools: 78
Critical unresolved lineage: 52
Total lineage resolved in metadata: 51
```

After Track 7.16:

```text
Runtime-only unresolved tools by basename: 63
Critical unresolved lineage by basename: 40
Total lineage resolved in metadata: 68
Remaining known unresolved by lineage metadata: 50
```

## 9. Runtime / Repo Diff Result

```text
V7 runtime/repo governance diff (read-only)
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 63
Named lineage gaps: 63
Critical lineage gaps (known): 40
Unlisted lineage gaps: 0
Safe convergence candidates (known): 4
warnings:
  - runtime_manifest_not_supplied
```

## 10. Release Object Warning Status

```text
V7 release lineage check (read-only)
lineage_resolved_tools=68
remaining_known_unresolved=50
runtime_lineage=partial
release_provenance=incomplete
```

Warnings remain:

- runtime manifest is not locally available at the default live path;
- source worktree is dirty;
- 50 known production-only tools still require lineage;
- archive manifests are not locally available at default live paths.

## 11. Remaining Routing / Policy / Proxy Blockers

- Apply tools remain unresolved and intentionally excluded.
- `v7-routing-sync`, `v7-user-switch`, and `v7-users-autoswitch` remain high-risk runtime nervous-system layers.
- Direct/RU mutation tools remain unresolved.
- Proxy public enable/disable/apply tools remain unresolved.
- Trusted RU/Gosuslugi-specific diagnostics remain deferred to a dedicated sensitive review.
- Policy/routing/proxy safety is not proven by lineage; only source provenance and static safety classification improved.

## 12. Next Bounded Batch Safety

Next bounded batch is safe only if it remains lineage-only.

Recommended next batch:

```text
Direct/RU mutation governance preview, excluding apply execution
```

Do not execute routing sync, autoswitch, policy apply, Direct/RU refresh/apply, proxy enable/disable/apply, or any live mutation without a separate high-risk review.
