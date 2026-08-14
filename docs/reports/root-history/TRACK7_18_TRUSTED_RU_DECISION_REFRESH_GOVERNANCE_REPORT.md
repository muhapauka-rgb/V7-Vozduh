# V7 Vozduh Track 7.18 Report

## Trusted RU Decision / Refresh Governance Lineage Batch

Track 7.18 resolved repo-side lineage and governance visibility for Trusted RU decision/refresh tooling. No VPS runtime mutation, Trusted RU decision execution, Trusted RU refresh execution, Gosuslugi live probe, Direct/RU mutation, policy apply, routing sync, autoswitch execution, nftables update, route change, service restart, chmod/chown, delete/archive, deploy, or live profile/onboarding action was performed.

## 1. Tools Resolved

```text
v7-trusted-ru-decision
v7-trusted-ru-refresh-missing
```

Both tools were copied read-only from `/usr/local/bin` into `tools/runtime-support/`, with hashes matching `runtime-enumeration.json`.

## 2. Tools Skipped

```text
v7-trusted-ru-preview
v7-trusted-ru-status
v7-trusted-ru-report
```

These optional candidates were not present in `runtime-enumeration.json`.

Excluded by rule:

```text
v7-routing-sync
v7-user-switch
v7-users-autoswitch
v7-policy-apply
v7-policy-resolve
v7-direct-add-domain
v7-direct-remove-domain
v7-direct-auto-sync
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
docs/track7/lineage/trusted-ru-decision-refresh-tools.json
TRACK7_18_TRUSTED_RU_DECISION_REFRESH_GOVERNANCE_REPORT.md
tools/runtime-support/v7-trusted-ru-decision
tools/runtime-support/v7-trusted-ru-refresh-missing
```

Updated:

```text
docs/track7/PRODUCTION_ONLY_TOOL_GOVERNANCE.md
```

## 4. Lineage Metadata File

```text
docs/track7/lineage/trusted-ru-decision-refresh-tools.json
```

The metadata records:

- runtime path, sha256, size, mode, mtime;
- reference evidence and systemd references;
- governance class, criticality, release relevance, provenance confidence;
- repo path;
- owner/purpose/mutation level;
- diagnostic and decision state reads/writes;
- route-class, Direct/RU, policy/routing influence;
- Gosuslugi-sensitive and network probe behavior;
- audit/temp behavior;
- verification requirements and safety notes.

## 5. Trusted RU Decision / Refresh Safety Review

`v7-trusted-ru-decision`:

- Reads `/opt/v7/egress/state/trusted-ru-diagnostic.state`.
- Reads `/etc/v7/policy/trusted_ru_sensitive_domains.conf` when present.
- Falls back to a built-in Gosuslugi-sensitive domain set when that file is absent.
- Produces decision output for `TRUSTED_RU_SENSITIVE`.
- Does not directly call policy apply, routing sync, autoswitch, nftables, `ip route`, or `ip rule`.
- Does not directly perform network probes.
- With `--write-state`, writes `/opt/v7/egress/state/trusted-ru-decision.state` through a temporary state file and `mv`.

`v7-trusted-ru-refresh-missing`:

- Reads `/opt/v7/egress/state/trusted-ru-decision.state`.
- If the decision state is missing, calls `v7-trusted-ru-decision --write-state`.
- Selects domains marked `MISSING_DIAGNOSTIC`.
- Calls `v7-trusted-ru-diagnostic` for selected domains.
- Calls `v7-trusted-ru-decision --write-state` after refresh.
- Calls `v7-state-json-save` when available.
- Can therefore trigger live Trusted RU/Gosuslugi probes and state writes if executed.

Safety verdict:

```text
lineage-only safe: yes
live execution safe in this track: no
runtime mutation if executed normally: yes
Trusted RU safety proven: no
```

## 6. Gosuslugi-Sensitive Boundary Review

The decision layer distinguishes diagnostic observation from decision state, but it does not prove route safety. `v7-trusted-ru-decision` consumes existing diagnostic evidence and converts it into decision categories such as `DIRECT_OK`, `USE_TEMP_VLESS`, `USE_AWG`, `MISSING_DIAGNOSTIC`, and `NO_SAFE_PATH`.

The refresh layer crosses from decision governance into live diagnostic refresh: it can invoke `v7-trusted-ru-diagnostic`, which is already known to probe Gosuslugi/Trusted RU domains and write `trusted-ru-diagnostic.state`. Failed, missing, stale, or timeout-influenced probe state can affect future decision output and operator interpretation.

Boundary verdict:

```text
diagnostic observation: represented by trusted-ru-diagnostic.state
routing decision preview: represented by v7-trusted-ru-decision output
decision state mutation: possible with --write-state and refresh-missing
policy mutation: not directly observed
route apply: not directly observed
Gosuslugi behavior changed in this track: no
```

Operator UI output is decision-oriented and does not print tokens or private keys, but it can expose sensitive route/domain status and should not be treated as public-safe telemetry.

## 7. Owner / Purpose / Mutation Classification

```text
v7-trusted-ru-decision
owner: Trusted-RU
mutation: Trusted-RU-decision diagnostic-state-read optional-decision-state-write route-class-influence

v7-trusted-ru-refresh-missing
owner: Trusted-RU
mutation: Trusted-RU-refresh diagnostic-state-read diagnostic-state-write decision-state-write network-probe route-class-influence
```

## 8. Static Verification Results

```text
bash -n tools/runtime-support/v7-trusted-ru-decision
bash -n tools/runtime-support/v7-trusted-ru-refresh-missing
OK

python3 -m json.tool docs/track7/lineage/trusted-ru-decision-refresh-tools.json
OK

tools/v7-run-tests
Ran 28 tests
OK

PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/*.py tools/v7-release-lineage-check tools/v7-runtime-repo-diff
OK
```

No imported Trusted RU decision/refresh tool was executed against live Trusted RU, policy, Direct/RU, routing, or Gosuslugi state.

## 9. Updated Governance Counts

Before Track 7.18:

```text
Runtime-only unresolved tools: 58
Critical unresolved lineage: 35
Total lineage resolved in metadata: 73
```

After Track 7.18:

```text
Runtime-only unresolved tools by basename: 56
Critical unresolved lineage by basename: 33
Total lineage resolved in metadata: 75
Remaining known unresolved by lineage metadata: 43
```

## 10. Runtime / Repo Diff Result

```text
V7 runtime/repo governance diff (read-only)
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 56
Named lineage gaps: 56
Critical lineage gaps (known): 33
Unlisted lineage gaps: 0
Safe convergence candidates (known): 4
warnings:
  - runtime_manifest_not_supplied
```

## 11. Release Object Warning Status

```text
V7 release lineage check (read-only)
lineage_resolved_tools=75
remaining_known_unresolved=43
runtime_lineage=partial
release_provenance=incomplete
```

Warnings remain:

- runtime manifest is not locally available at the default live path;
- source worktree is dirty;
- 43 known production-only tools still require lineage;
- archive manifests are not locally available at default live paths.

## 12. Remaining Trusted RU / Routing / Policy Blockers

- Trusted RU diagnostic/decision/refresh safety is not proven for live execution.
- `v7-routing-sync` remains unresolved and high-risk.
- `v7-policy-apply` remains unresolved and high-risk.
- `v7-users-autoswitch`, `v7-user-switch`, and user movement layers remain out of scope.
- Trusted RU state freshness/timeout semantics still need a dedicated non-mutating review before any operator automation depends on them.
- Live rollout would require explicit approval, stale-state handling, probe privacy review, backups, rollback mapping, and datapath verification.

## 13. Next Bounded Batch Safety

Next bounded batch is safe only if it remains lineage-only.

Recommended next batch:

```text
routing/policy apply governance preview, or another narrow non-executed runtime-affecting layer
```

Do not execute Trusted RU refresh, policy apply, routing sync, autoswitch, user movement, or proxy apply behavior without a separate high-risk review.
