# V7 Vozduh Track 7.17 Report

## Direct/RU Mutation Governance Preview Batch

Track 7.17 resolved repo-side lineage and governance visibility for Direct/RU mutation tooling and Trusted RU diagnostic state tooling. No VPS runtime mutation, Direct/RU apply, policy resolve execution, Trusted RU diagnostic execution, routing sync, autoswitch execution, nftables update, route change, dnsmasq restart, chmod/chown, delete/archive, deploy, or service restart was performed.

## 1. Tools Resolved

```text
v7-direct-add-domain
v7-direct-remove-domain
v7-direct-auto-sync
v7-policy-resolve
v7-trusted-ru-diagnostic
```

All five tools were copied read-only from `/usr/local/bin` into `tools/runtime-support/`, with hashes matching `runtime-enumeration.json`.

## 2. Tools Skipped

```text
v7-direct-preview
v7-policy-preview-apply
v7-trusted-ru-decision
v7-trusted-ru-refresh-missing
```

Reasons:

- `v7-direct-preview` and `v7-policy-preview-apply` were not present in runtime enumeration.
- `v7-trusted-ru-decision` and `v7-trusted-ru-refresh-missing` are adjacent Trusted RU/Gosuslugi-sensitive layers and should be reviewed separately.

Excluded by rule:

```text
v7-routing-sync
v7-user-switch
v7-users-autoswitch
v7-policy-apply
v7-proxy-runtime-guard-apply
v7-proxy-public-enable
v7-proxy-public-disable
v7-user-enable
v7-user-disable
v7-user-create
```

## 3. Repo Paths Created / Updated

Created:

```text
docs/track7/lineage/direct-ru-mutation-governance-tools.json
TRACK7_17_DIRECT_RU_MUTATION_GOVERNANCE_REPORT.md
tools/runtime-support/v7-direct-add-domain
tools/runtime-support/v7-direct-remove-domain
tools/runtime-support/v7-direct-auto-sync
tools/runtime-support/v7-policy-resolve
tools/runtime-support/v7-trusted-ru-diagnostic
```

Updated:

```text
docs/track7/PRODUCTION_ONLY_TOOL_GOVERNANCE.md
```

## 4. Lineage Metadata File

```text
docs/track7/lineage/direct-ru-mutation-governance-tools.json
```

The metadata records:

- runtime path, sha256, size, mode, mtime;
- reference evidence and systemd references;
- governance class, criticality, release relevance, provenance confidence;
- repo path;
- owner/purpose/mutation level;
- route-class reads/writes;
- Direct/RU reads/writes;
- nftables/iprule behavior;
- Trusted RU behavior;
- audit behavior;
- temp/backup behavior;
- verification requirements and safety notes.

## 5. Direct/RU Mutation Safety Review

`v7-direct-add-domain`:

- Writes `/etc/v7/direct/domains.conf`.
- Creates timestamped backup.
- Calls `v7-direct-render-dnsmasq`.
- Restarts `dnsmasq`.
- Writes audit event when `v7-audit-log` exists.

`v7-direct-remove-domain`:

- Writes filtered `/etc/v7/direct/domains.conf`.
- Creates backup and temp file.
- Calls `v7-direct-render-dnsmasq`.
- Restarts `dnsmasq`.
- Writes audit event when available.

`v7-direct-auto-sync`:

- Ensures base `.ru` and `.xn--p1ai` entries.
- Reads `/etc/v7/policy/direct_ru_domains.conf`.
- Can append to `/etc/v7/direct/domains.conf`.
- Creates autosync backup on first change.
- Calls `v7-direct-render-dnsmasq`.
- Restarts `dnsmasq` when changed.
- Writes `/opt/v7/egress/state/direct-ru-autosync.state`.
- Runs Direct/RU sample checks.

`v7-policy-resolve`:

- Resolves policy class domains, including `TRUSTED_RU_SENSITIVE`.
- Writes `/opt/v7/egress/state/route-classes.state`.
- Does not apply routes directly, but its state can feed later policy apply decisions.

Safety verdict:

```text
lineage-only safe: yes
live execution safe in this track: no
runtime mutation if executed normally: yes
Direct/RU safety proven: no
```

## 6. Trusted RU Governance Review

`v7-trusted-ru-diagnostic`:

- Probes Gosuslugi/Trusted RU domains.
- Uses DNS, direct curl, browser-like curl when available, VLESS/SOCKS curl, AWG curl when interface exists, and OpenSSL TLS checks.
- Calls `v7-direct-test-domain` for policy decision evidence.
- Writes `/opt/v7/egress/state/trusted-ru-diagnostic.state`.
- Preserves previous untested keys from existing state.
- Does not directly rewrite route classes.
- Does not directly apply routing.

Trusted RU verdict:

```text
truly read-only: no
diagnostic-state-write: yes
Gosuslugi-sensitive: yes
changes route classes directly: no
can influence downstream operator/decision workflows: yes
live execution allowed in this track: no
```

## 7. Owner / Purpose / Mutation Classification

```text
v7-direct-add-domain
owner: Direct/RU
mutation: Direct/RU-state-write service-restart

v7-direct-remove-domain
owner: Direct/RU
mutation: Direct/RU-state-write service-restart

v7-direct-auto-sync
owner: Direct/RU
mutation: auto-sync Direct/RU-state-write summary-write service-restart

v7-policy-resolve
owner: policy
mutation: policy-resolution-write route-class-state-write

v7-trusted-ru-diagnostic
owner: Trusted-RU
mutation: Trusted-RU-read diagnostic-state-write network-probe
```

## 8. Static Verification Results

```text
bash -n tools/runtime-support/v7-direct-add-domain
bash -n tools/runtime-support/v7-direct-remove-domain
bash -n tools/runtime-support/v7-direct-auto-sync
bash -n tools/runtime-support/v7-policy-resolve
bash -n tools/runtime-support/v7-trusted-ru-diagnostic
OK

python3 -m json.tool docs/track7/lineage/direct-ru-mutation-governance-tools.json
OK

tools/v7-run-tests
Ran 28 tests
OK

PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/*.py tools/v7-release-lineage-check tools/v7-runtime-repo-diff
OK
```

No imported tool was executed against live Direct/RU, policy, routing, or Trusted RU state.

## 9. Updated Governance Counts

Before Track 7.17:

```text
Runtime-only unresolved tools: 63
Critical unresolved lineage: 40
Total lineage resolved in metadata: 68
```

After Track 7.17:

```text
Runtime-only unresolved tools by basename: 58
Critical unresolved lineage by basename: 35
Total lineage resolved in metadata: 73
Remaining known unresolved by lineage metadata: 45
```

## 10. Runtime / Repo Diff Result

```text
V7 runtime/repo governance diff (read-only)
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 58
Named lineage gaps: 58
Critical lineage gaps (known): 35
Unlisted lineage gaps: 0
Safe convergence candidates (known): 4
warnings:
  - runtime_manifest_not_supplied
```

## 11. Release Object Warning Status

```text
V7 release lineage check (read-only)
lineage_resolved_tools=73
remaining_known_unresolved=45
runtime_lineage=partial
release_provenance=incomplete
```

Warnings remain:

- runtime manifest is not locally available at the default live path;
- source worktree is dirty;
- 45 known production-only tools still require lineage;
- archive manifests are not locally available at default live paths.

## 12. Remaining Routing / Policy / Trusted RU Blockers

- `v7-routing-sync` remains unresolved and high-risk.
- `v7-policy-apply` remains unresolved and high-risk.
- `v7-users-autoswitch`, `v7-user-switch`, and user movement layers remain out of scope.
- Trusted RU decision/refresh tooling remains unresolved.
- Direct/RU safety is not proven; only source provenance and mutation semantics are now visible.
- Live rollout would require explicit approval, preflight, backups, rollback mapping, and datapath verification.

## 13. Next Bounded Batch Safety

Next bounded batch is safe only if it remains lineage-only.

Recommended next batch:

```text
Trusted RU decision / refresh governance, still no execution
```

Do not execute Trusted RU refresh, policy apply, routing sync, autoswitch, user movement, or proxy apply behavior without a separate high-risk review.
