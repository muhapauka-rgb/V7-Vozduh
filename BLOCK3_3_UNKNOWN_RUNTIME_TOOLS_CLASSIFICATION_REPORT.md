# V7 Vozduh - Block 3.3 Unknown Runtime Tools & Suspicious Executable Classification

Generated: 2026-05-23

Scope: classify the remaining `/usr/local/bin/v7*` executables after Block 3.2.

Rules followed:

- No files were deleted.
- No files were moved.
- No file modes were changed.
- No systemd units were changed.
- No routing, datapath, kill switch, route class, Trusted RU, or Gosuslugi behavior was changed.
- Inspection only, plus a temporary analysis artifact at `/tmp/block33_unknown_classification.json`.

Authoritative baseline used:

- `/opt/v7/ops/deploy-baseline/20260523T122251Z/manifest.json`
- `/opt/v7/ops/deploy-baseline/20260523T122251Z/checksums.sha256`
- Block 3.2 archive manifest:
  `/root/v7-backups/usr-local-bin-archive/20260523T122936Z/archive-manifest.json`

## 1. Unknown Executable Classification

After Block 3.2, stale executable backups were already archived out of PATH. Remaining live PATH state:

- `/usr/local/bin/v7*` total: 142
- Active runtime executables from manifest/systemd binding: 24
- Unknown active-like executables: 117
- Suspicious executable: 1 (`v7-admin-api.tmp`)
- Backup-like executables remaining in PATH: 0

The 117 unknown active-like executables are not all unsafe. Most are operator utilities, dry-run tools, policy helpers, diagnostics, or production-only support tools. However, they are not currently governed by a release manifest, package boundary, or clean repository lineage.

Classification counts:

| Category | Count | Verdict |
|---|---:|---|
| `diagnostic_or_readonly_utility` | 26 | Mostly safe to keep; useful for operator/runtime inspection |
| `policy_or_direct_ru_utility` | 26 | Must not be cleaned casually; many touch direct/RU policy workflows |
| `operator_mutation_tool` | 22 | Medium risk; can change runtime state and must remain governed |
| `unknown_risk` | 20 | Requires deeper inspection before any cleanup |
| `provisioning_or_egress_utility` | 13 | Potential runtime/provisioning dependency; keep until workflow verified |
| `identity_or_profile_utility` | 4 | Identity/profile sensitive; keep until dependency map is complete |
| `observability_or_measurement_tool` | 4 | Low-to-medium risk; keep unless owner workflow proves obsolete |
| `review_setup_or_governance_tool` | 2 | Low risk; can remain for now |

Risk counts:

| Risk | Count |
|---|---:|
| Low | 38 |
| Medium | 79 |
| High | 0 among the 117 unknown tools |

High risk is limited to the separate suspicious executable `v7-admin-api.tmp`.

Future cleanup readiness:

| Readiness | Count | Meaning |
|---|---:|---|
| `keep_until_owner_workflow_verified` | 88 | Do not archive until exact admin/operator workflows are checked |
| `deeper_inspection_required` | 20 | Needs file-level review before cleanup |
| `keep_as_operator_utility` | 9 | Should stay as intentional operator tooling |

## 2. Suspicious Executable Analysis

Suspicious executable:

- Path: `/usr/local/bin/v7-admin-api.tmp`
- Executable: yes
- Mode: `0755`
- Size: `1,219,483` bytes
- SHA256: `0b8ba074a7392816a8705721a2a0746f1154bfc02967c77d75a8fc80b1e23c10`
- Active admin API hash match: no
- Size delta vs active `/usr/local/bin/v7-admin-api`: `-527,981` bytes
- Runtime references found: 0 real references in compact scan
- Broad scan note: only generated/cache-style reference noise was observed; no operational binding was found.

Verdict:

`v7-admin-api.tmp` is almost certainly a temporary deploy artifact, not an active runtime executable. It is dangerous only because it is executable and still lives in PATH with an admin-like name.

Cleanup status:

- Do not delete now.
- Do not archive in Block 3.3.
- Safe candidate for future archive after one more confirmation pass:
  - hash compare recorded;
  - no systemd references;
  - no admin subprocess references;
  - no shell-loop references;
  - include it in a future archive manifest.

Risk:

- High operational hygiene risk.
- Low immediate runtime risk based on references.
- High confusion risk during incident response or manual operator use.

## 3. Hidden Dependency Map

Unknown does not mean unused.

Reference scan result:

- Unknown tools with references: 90
- Unknown tools with no references found: 27

Important referenced tools:

| Tool | Observed Role | Reference Impact |
|---|---|---|
| `v7-audit-log` | Audit/event support | Referenced heavily by admin and operator mutation tools; must remain |
| `v7-user-switch` | Manual/user movement support | Referenced by admin, autoswitch, and rebalance tooling; runtime-critical support |
| `v7-user-route-check` | Safety verification | Referenced by policy/direct checks and admin paths |
| `v7-killswitch-check` | Safety verification | Referenced by admin, observability, safe-run |
| `v7-state-json` | State helper | Referenced by health, policy, and Trusted RU refresh helpers |
| `v7-user-desired-state` | Desired-state helper | Referenced by health service, admin, capacity readiness |
| `v7-service-matrix-test` | Service quality check | Referenced by admin/diagnostic workflows |
| `v7-direct-render-dnsmasq` | Direct/RU support | Referenced by direct/RU workflows; do not touch casually |
| `v7-policy-apply` | Policy mutation | Medium risk; must be governed, not archived blindly |
| `v7-users-rebalance` / `v7-users-rebalance-dry-run` | Rebalance support | Needs deeper inspection before any cleanup |

The highest hidden dependency risk is not systemd. It is admin/API subprocess usage, shell helper chains, and operator workflows that call `v7-*` tools by PATH.

## 4. Runtime Reference Map

Reference channels checked:

- systemd unit ExecStart/ExecStop style bindings;
- active service/timer dependency map from Block 3.1;
- `/usr/local/bin/v7*` scripts and executable text references;
- admin/API subprocess references;
- shell-loop and helper references;
- manifest classification from Block 3.1.

Reference findings:

- 24 tools are clearly active runtime executables from systemd/baseline binding.
- 117 are not directly bound by systemd but many are indirectly referenced.
- 90 of the 117 unknown tools have at least one internal reference.
- 27 of the 117 have no references found in this pass.
- The no-reference group is not automatically safe to archive because operator/manual workflows may not appear in static scans.

Most dangerous implicit dependency pattern:

```text
admin/API or operator tool -> subprocess("v7-*") -> PATH lookup -> production behavior
```

This means future cleanup must be manifest-driven and workflow-aware, not name-pattern-driven.

## 5. Repository / Runtime Alignment Analysis

Alignment of 117 unknown runtime tools against the local repository:

- Runtime unknown tools also present in repo by basename: 14
- Production-only unknown tools not present in local repo by basename: 103

Repo-known unknown tools:

- `v7-autoswitch-install-systemd`
- `v7-direct-diagnose-domain`
- `v7-direct-render-dnsmasq`
- `v7-direct-test-domain`
- `v7-egress-import-regression`
- `v7-egress-mtu-probe`
- `v7-egress-set-state`
- `v7-killswitch-check`
- `v7-observability-summary`
- `v7-path-benchmark`
- `v7-path-optimizer-advice`
- `v7-path-sample-ingest`
- `v7-provisioning-reconcile-check`
- `v7-service-matrix-test`

Production-only does not mean obsolete. Many production-only tools are referenced by other runtime tools and represent live operational history not captured cleanly in the repo.

Production-only categories:

- Diagnostics and read-only utilities: 23
- Policy/direct/RU utilities: 23
- Operator mutation tools: 21
- Unknown-risk tools: 20
- Provisioning/egress utilities: 10
- Identity/profile utilities: 4
- Observability/measurement utilities: 1
- Review/setup/governance utilities: 1

Governance issue:

The live VPS contains a large amount of operational code that is either production-only or diverged from the local repository. This weakens reproducibility, rollback trust, code review, and operator confidence.

## 6. Sensitive Runtime Warnings

Sensitive/runtime files with notable permissions:

| Path | Current Concern | Severity |
|---|---|---|
| `/opt/v7/egress/state/profile-delivery-tokens.json` | Mode `0644`; token-related state is readable beyond owner | High |
| `/etc/v7/policy.json` | Mode `0644`; policy is readable system-wide | Medium |
| `/etc/v7/org-egress-policy.json` | Mode `0644`; org policy is readable system-wide | Medium |
| `/usr/local/bin/v7-admin-api.tmp` | Executable temporary admin artifact in PATH | High hygiene risk |

No permission change was applied in Block 3.3.

Production recommendation:

- Do not change permissions blindly in this block.
- Add a dedicated sensitive-state permission hardening pass.
- Confirm runtime users/groups before chmod/chown.
- Especially verify whether admin/API services require non-root read access before changing token or identity paths.

## 7. Deeper Inspection Required

The following 20 tools require deeper file-level and workflow-level inspection before any future cleanup:

- `v7-audit-log`
- `v7-decide-egress`
- `v7-proxy-public-candidate-render`
- `v7-proxy-public-disable`
- `v7-proxy-public-enable`
- `v7-proxy-public-port-canary`
- `v7-proxy-public-service-render`
- `v7-proxy-service-aware-routing-dry-run`
- `v7-recent-performance`
- `v7-safe-run`
- `v7-secrets-cleanup-apply`
- `v7-sing-box-tun-mtu-set`
- `v7-state-json`
- `v7-switch-log`
- `v7-user-desired-state`
- `v7-user-reconcile-apply`
- `v7-user-reissue-config`
- `v7-user-rotate-key`
- `v7-users-rebalance`
- `v7-users-rebalance-dry-run`

Important nuance:

Some of these are probably legitimate runtime support tools, not obsolete files. For example `v7-audit-log`, `v7-state-json`, `v7-user-desired-state`, and `v7-user-switch`-related workflows look like real dependencies. They are on this list because cleanup safety requires deeper understanding, not because they should be removed.

## 8. Future Cleanup Readiness

Safe to consider for future archive:

- `v7-admin-api.tmp`, after one final reference scan and inclusion in an archive manifest.
- Unreferenced unknown tools only after manual owner/workflow verification.

Must remain for now:

- All active runtime executables from Block 3.1.
- All direct/RU and Trusted RU adjacent tools.
- All policy mutation tools.
- All user-switch, rebalance, audit, and desired-state tools.
- All identity/profile delivery tools.
- All safety verification tools.

Future cleanup model:

1. Generate a new manifest after Block 3.3.
2. Create a reviewed allowlist:
   - active runtime;
   - referenced support;
   - operator utility;
   - policy/direct/RU utility;
   - identity/profile utility.
3. Create a candidate list only from:
   - no references found;
   - not repo-known active;
   - no mutation semantics;
   - no direct/RU/identity/policy scope;
   - no systemd/admin references.
4. Archive out of PATH, never delete.
5. Preserve hashes, modes, mtimes, and filenames.
6. Verify runtime safety after every small batch.

## 9. Runtime Verification Results

Post-inspection runtime verification:

| Check | Result |
|---|---|
| `v7-killswitch-check` | PASS |
| `v7-user-route-check` | PASS |
| `v7-provisioning-reconcile-check` | PASS |
| `systemctl --failed` | PASS, 0 failed units |

No datapath regression was observed.

No routing change was applied.

No kill switch change was applied.

No autoswitch policy change was applied.

No systemd change was applied.

## 10. Remaining Operational Risks

### Risk 1 - Runtime still has weak release lineage

The platform is cleaner than before Block 3.2, but deploy truth still depends heavily on the live filesystem plus baseline manifests.

Impact:

- hard to reproduce exact release;
- hard to review production-only tools;
- rollback trust is better but not complete.

### Risk 2 - 103 production-only unknown tools

Most unknown tools are not in the local repo by basename.

Impact:

- production behavior may not be reviewable from the repository;
- future rebuild from repo alone would likely miss operator/runtime tooling;
- code drift risk remains high.

### Risk 3 - Hidden PATH dependencies

Many unknown tools are called indirectly through admin/API scripts or other shell tools.

Impact:

- aggressive cleanup could break operator workflows;
- static systemd binding map is insufficient.

### Risk 4 - `v7-admin-api.tmp` remains executable in PATH

Impact:

- confusing during incidents;
- possible accidental manual execution;
- clear future cleanup candidate.

### Risk 5 - Sensitive state permissions need a dedicated hardening pass

Impact:

- token-related files may be more broadly readable than desired;
- policy files may expose routing/business assumptions.

Do not fix blindly. First verify service user/group access requirements.

## 11. Operator Runtime Clarity Summary

Calm operator view after Block 3.3:

```text
Runtime executable baseline: improved
Stale backups in PATH: removed in Block 3.2
Unknown active-like tools: 117
Referenced unknown tools: 90
Unreferenced unknown tools: 27
Suspicious executable: 1
Production-only unknown tools: 103
Immediate datapath risk: not observed
Immediate cleanup action: not recommended
Next safe cleanup target: v7-admin-api.tmp, archive-only, after final confirmation
```

## 12. Final Verdict

Block 3.3 confirms that V7 is no longer suffering from backup-executable clutter in PATH, but it still has substantial operational ambiguity from production-only tools and hidden PATH dependencies.

The remaining unknown executables are not random junk. Most look like real operator, policy, diagnostic, provisioning, identity, or support utilities. Cleanup must therefore be conservative and evidence-based.

Production blockers from this block:

- missing repository lineage for 103 production-only tools;
- executable `v7-admin-api.tmp` still in PATH;
- token-related state permission warning;
- no formal release manifest ownership for operator utilities.

Recommended next stabilization priorities:

1. Archive `v7-admin-api.tmp` in a dedicated tiny cleanup block after one final reference check.
2. Build a permanent runtime tool registry:
   - owner;
   - category;
   - mutates runtime or read-only;
   - allowed operator use;
   - repo source;
   - cleanup status.
3. Pull production-only tools into repository or explicitly mark them as runtime-local artifacts.
4. Create a sensitive-state permission hardening plan.
5. Keep all direct/RU, policy, identity, audit, user-switch, and rebalance tools untouched until workflow ownership is formalized.

