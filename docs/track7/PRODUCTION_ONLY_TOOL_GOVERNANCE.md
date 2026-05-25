# V7 Track 7.2 — Production-Only Tool Governance & Lineage Resolution

Track 7.2 governs production-only tools. It does not import them, delete them, sync runtime to repo, or rewrite deployment.

## 1. Expanded Governance Inventory

Known production-only state from Block 3.3 and the first release object:

| Metric | Count |
|---|---:|
| Unknown active-like runtime tools | 117 |
| Repo-known unknown tools | 14 |
| Production-only unknown tools | 103 |
| Referenced unknown tools | 90 |
| Unreferenced unknown tools | 27 |
| Known deeper-inspection tools named locally | 20 |
| Not locally enumerated production-only tools | 83 |

The 83 unlisted tools are intentionally not invented. They require live manifest import or read-only VPS enumeration.

## 2. Finalized Governance Taxonomy

| Class | Meaning | Operational Rule |
|---|---|---|
| `authoritative_runtime` | Proven active runtime executable owned by a release manifest | Must be in release object; cleanup forbidden without replacement release |
| `runtime_local_pending_lineage` | Runtime-local tool accepted temporarily but not reproducible from repo | Add owner/role/hash, then import or explicitly keep runtime-local |
| `runtime_generated` | Generated artifact/tool with known generator | Record generator and inputs; do not hand-edit |
| `legacy_runtime_drift` | Historical runtime artifact still present without current workflow proof | Freeze; archive only in dedicated cleanup block after verification |
| `operator_local_helper` | Manual operator utility not required by automated runtime | Document allowed use; keep out of automated dependency chains |
| `repo_missing_critical` | Runtime tool needed for critical behavior but absent from repo | Highest import/rewrite priority |
| `repo_missing_noncritical` | Useful runtime tool absent from repo but not critical | Import later or mark runtime-local |
| `safe_archive_candidate` | No references and no critical/mutation semantics after review | Archive only, never delete, preserve manifest |

## 3. Runtime Criticality Map

| Criticality | Tool Classes | Action |
|---|---|---|
| Datapath-critical | kill switch, route check, user switch, direct/RU policy render/apply | No cleanup; release-owned; mandatory live verification |
| Autoswitch-critical | `v7-users-autoswitch`, safety state writers, rebalance tools | No broad changes; import/govern before commercial release |
| Provisioning-critical | egress lifecycle, config render, set-state, reconcile | Import/govern; rollback required |
| Identity-critical | profile delivery, user reissue/rotate, identity consistency | Import/govern; sensitive-state review required |
| Observability-only | summaries, performance, service matrix diagnostics | Import later or mark operator-local |
| Operator convenience | dry-runs, review helpers, setup helpers | Keep with owner; exclude from automated release if truly manual |
| Rollback-only | archive helpers, backup verify, rollback preview/apply | Release-relevant; keep governed |
| Dormant/legacy | no refs, no owner, no workflow | Freeze; future archive candidate only after verification |

## 4. Known Production-Only Entries

The first release object lists 20 known deeper-inspection tools with owners and roles in:

```text
releases/v7-runtime-20260523T174503Z/production-only-tools.json
```

Current priority groups:

### Must Resolve Before Commercial Release

- mutation tools;
- identity/profile tools;
- policy/direct/RU tools;
- provisioning/egress tools;
- unknown-risk support tools such as audit/state helpers.

### Can Remain Runtime-Local Temporarily

- read-only diagnostics;
- operator-local dry-runs;
- review/setup helpers.

### Cannot Be Classified Locally Yet

- 83 production-only tools not locally enumerated.

Required next evidence:

- live manifest import, or
- read-only VPS enumeration, no mutation.

## 5. Repo Convergence Strategy

Safest-first sequence:

1. Import or document audit/state support tools:
   - `v7-audit-log`;
   - `v7-state-json`;
   - `v7-user-desired-state`;
   - `v7-switch-log`.
2. Import/govern identity/profile tools:
   - `v7-user-reissue-config`;
   - `v7-user-rotate-key`.
3. Import/govern routing mutation tools:
   - `v7-user-reconcile-apply`;
   - `v7-users-rebalance`;
   - keep dry-run variant for planning.
4. Govern proxy/public profile tools:
   - render/enable/disable/canary service tools.
5. Import or mark read-only utilities as operator-local.
6. Only after live manifest import, classify the remaining 83.

Do not mass-import all 103 tools. Each imported tool needs owner, purpose, mutation class, state reads/writes, verification expectation, and release relevance.

## 6. Runtime Ownership Model

| Owner | Responsibility |
|---|---|
| `safety` | kill switch, no-leak checks, route safety verification |
| `routing` | user assignment, route tables, rebalance, reconcile |
| `autoswitch` | guarded switching, anti-flap, capacity/safety memory |
| `provisioning` | egress lifecycle, drafts, enable/disable, rollback |
| `identity/profile` | identity DB, devices, profile delivery, key rotation |
| `policy` | global/org policy and direct/RU-adjacent policy |
| `observability` | summaries, matrix, diagnostics, operator truth |
| `audit/runtime` | audit events, switch logs, actor/reason traceability |
| `admin` | admin API, safe-run, operator workflows |
| `security` | secret cleanup and sensitive-state warnings |

Each tool must eventually state:

- owner;
- maintainer;
- mutation level;
- state files read/written;
- release relevance;
- verification required.

## 7. Release Relevance Classification

| Release Relevance | Meaning |
|---|---|
| `must_be_release_owned` | Required for runtime safety/provisioning/identity/policy/autoswitch. |
| `runtime_local_allowed` | Host-specific or operator-local utility with documented owner/purpose. |
| `generated_runtime` | Rebuilt from repo generator or runtime state. |
| `operator_only_optional` | Useful but not part of automated runtime. |
| `archive_candidate_future` | Potentially obsolete but only after dedicated cleanup verification. |

Boundary:

- commercial release cannot rely on unknown tools with mutation or critical support roles;
- operator-local tools can remain outside release package only if explicitly governed.

## 8. Governance UX Summary

Recommended operator summary:

```text
Runtime governance: partial
Authoritative runtime tools: 24
Production-only tools: 103
Critical lineage gaps (known): 16
Unlisted lineage gaps: 83
Safe convergence candidates (known): 4
Next action: import/govern audit/state/identity/routing support tools first
```

Do not show raw filesystem walls by default.

## 9. Track 7.5 Lineage Resolution Batch

Track 7.5 resolved the first audit/state support batch into repo-side lineage without mutating the VPS runtime.

Resolved tools:

```text
v7-audit-log
v7-state-json
v7-state-json-save
v7-user-desired-state
v7-user-desired-state-save
v7-switch-log
```

Repo representation:

```text
tools/runtime-support/
```

Lineage metadata:

```text
docs/track7/lineage/audit-state-support-tools.json
```

Updated counts after repo-side lineage resolution:

```text
Runtime-only unresolved tools: 112
Critical unresolved lineage: 70
Lineage resolved in repo: 6
```

This does not make the platform commercially reproducible yet. It only closes the first bounded lineage batch.

## 10. Track 7.6 Observability / Capacity Support Batch

Track 7.6 resolved the recommended observability and capacity lineage batch without mutating the VPS runtime.

Resolved tools:

```text
v7-observability-summary
v7-capacity-check
v7-capacity-readiness
v7-service-matrix-test
v7-egress-quality-compact
v7-path-benchmark
v7-path-optimizer-advice
```

Repo representation:

```text
tools/
tools/runtime-support/
```

Lineage metadata:

```text
docs/track7/lineage/observability-capacity-support-tools.json
```

Mutation classification:

```text
state-read: v7-observability-summary
runtime-check: v7-capacity-check, v7-capacity-readiness, v7-path-benchmark
summary-write: v7-service-matrix-test, v7-path-optimizer-advice
metric-write: v7-egress-quality-compact
```

Updated counts after this batch:

```text
Runtime-only unresolved tools by basename: 110
Critical unresolved lineage by basename: 70
Total lineage resolved in metadata: 13
Remaining known unresolved by lineage metadata: 105
```

Five tools were already exact-hash present in the repo. Two capacity tools were copied into `tools/runtime-support/`.

## 11. Track 7.7 Runtime Health / Stability Support Batch

Track 7.7 resolved the recommended runtime-health and stability batch without mutating the VPS runtime.

Resolved tools:

```text
v7-egress-history
v7-egress-load
v7-egress-stability
v7-recent-performance
v7-state-stale-check
v7-system-check
```

Repo representation:

```text
tools/runtime-support/
```

Lineage metadata:

```text
docs/track7/lineage/runtime-health-stability-tools.json
```

Mutation classification:

```text
summary-write: v7-egress-history, v7-egress-load, v7-egress-stability
state-read: v7-recent-performance, v7-state-stale-check
runtime-check: v7-system-check
```

`v7-system-check` is not pure read-only: it can call runtime refresh helpers such as `v7-egress-stability` and `v7-state-merge`. It is lineage-resolved, but must not be used as a unit-test command or run casually during repo-only verification.

Updated counts after this batch:

```text
Runtime-only unresolved tools by basename: 104
Critical unresolved lineage by basename: 67
Total lineage resolved in metadata: 19
Remaining known unresolved by lineage metadata: 99
```

Optional maintenance/node tools were intentionally skipped for a later bounded batch.

## 12. Track 7.8 Maintenance / Node Runtime Support Batch

Track 7.8 resolved the maintenance and node-runtime support batch without mutating the VPS runtime.

Resolved tools:

```text
v7-log-maintenance-status
v7-maintenance-cleanup-preview
v7-node-config-check
v7-node-env
```

Repo representation:

```text
tools/runtime-support/
```

Lineage metadata:

```text
docs/track7/lineage/maintenance-node-runtime-tools.json
```

Mutation classification:

```text
runtime-check: v7-log-maintenance-status, v7-node-config-check
maintenance-preview: v7-maintenance-cleanup-preview
read-only: v7-node-env
```

Special safety finding:

`v7-maintenance-cleanup-preview` does not invoke cleanup apply, journal vacuum, logrotate, or deletion. It does create and remove a temporary file while calculating backup retention preview, so it is not pure read-only and should not be used as a unit-test command.

Updated counts after this batch:

```text
Runtime-only unresolved tools by basename: 100
Critical unresolved lineage by basename: 67
Total lineage resolved in metadata: 23
Remaining known unresolved by lineage metadata: 95
```

Optional cleanup/security tools were intentionally skipped for separate safety review.

## 13. Track 7.9 Security / Sensitive-State Preview-Only Batch

Track 7.9 resolved the preview-only security lineage item and added metadata for the repo-side sensitive-state validator without mutating VPS runtime.

Resolved runtime tool:

```text
v7-secrets-cleanup-preview
```

Repo-present metadata-only tool:

```text
v7-sensitive-state-check
```

Repo representation:

```text
tools/runtime-support/v7-secrets-cleanup-preview
tools/v7-sensitive-state-check
```

Lineage metadata:

```text
docs/track7/lineage/security-sensitive-preview-tools.json
```

Safety classification:

```text
security-preview: v7-secrets-cleanup-preview
sensitive-state-read: v7-sensitive-state-check
```

Special safety finding:

`v7-secrets-cleanup-preview` does not call apply tools, chmod/chown, delete files, or mutate `/opt/v7` or `/etc/v7`. It can print full paths to private-material files under the selected client artifact root, so its output is sensitive and operator-only.

`v7-sensitive-state-check` is repo-present but absent from live runtime enumeration. It is a read-only metadata/dry-run validator and does not close a VPS runtime lineage gap.

Updated counts after this batch:

```text
Runtime-only unresolved tools by basename: 99
Critical unresolved lineage by basename: 67
Total lineage resolved in metadata: 24
Remaining known unresolved by lineage metadata: 94
```

Apply tools remain out of scope.

## 14. Track 7.10 Identity / Profile Support Batch

Track 7.10 resolved the recommended identity/profile lineage batch without mutating VPS runtime or live customer/profile state.

Resolved runtime tools:

```text
v7-user-reissue-config
v7-user-rotate-key
v7-smart-client-profile-generate
v7-proxy-identity-bind
v7-proxy-identity-sync-users
v7-proxy-multi-user-identity-dry-run
v7-proxy-two-identity-live-probe
```

Intentionally skipped adjacent admin/security tools:

```text
v7-admin-auth-init
v7-admin-auth-status
v7-admin-password-rotate
```

Repo representation:

```text
tools/runtime-support/
```

Lineage metadata:

```text
docs/track7/lineage/identity-profile-support-tools.json
```

Safety classification:

```text
customer-config-write: v7-user-reissue-config
key-rotation: v7-user-rotate-key
profile-write: v7-smart-client-profile-generate
identity-binding-write: v7-proxy-identity-bind, v7-proxy-identity-sync-users
dry-run: v7-proxy-multi-user-identity-dry-run
live-probe: v7-proxy-two-identity-live-probe
```

Special safety findings:

`v7-user-rotate-key` is highly customer-affecting: it rotates WireGuard key material, rewrites `/etc/wireguard/wg0.conf`, updates live `wg` peer state, and calls `v7-routing-sync` for enabled users. It is lineage-resolved only and must not be executed casually.

`v7-smart-client-profile-generate` writes profile files containing WireGuard or VLESS credential material. It has redacted print support, but normal operation writes secrets to output files.

`v7-proxy-identity-bind` and `v7-proxy-identity-sync-users` can write disabled proxy identity binding JSON when their apply/confirm gates are used. They do not start services or change routing by themselves, but they create customer identity material and remain customer-facing mutation tools.

`v7-proxy-multi-user-identity-dry-run` is non-persistent but reads proxy identity/runtime state and writes temporary summary files. `v7-proxy-two-identity-live-probe` starts temporary loopback sing-box processes and performs network probes, so it is not a passive read-only validator.

Updated counts after this batch:

```text
Runtime-only unresolved tools by basename: 92
Critical unresolved lineage by basename: 60
Total lineage resolved in metadata: 31
Remaining known unresolved by lineage metadata: 87
```

Identity/profile lineage visibility improved, but identity/profile hardening is not complete and no live identity migration, key rotation, profile generation, or binding sync was performed.

## 15. Track 7.11 Admin Auth / Security Runtime Batch

Track 7.11 resolved the admin auth/security runtime lineage batch without mutating VPS runtime or live admin/auth state.

Resolved runtime tools:

```text
v7-admin-auth-init
v7-admin-auth-status
v7-admin-password-rotate
v7-safe-run
```

Repo representation:

```text
tools/runtime-support/
```

Lineage metadata:

```text
docs/track7/lineage/admin-auth-security-tools.json
```

Safety classification:

```text
bootstrap-init: v7-admin-auth-init
admin-auth-read: v7-admin-auth-status
password-rotation: v7-admin-password-rotate
security-gate: v7-safe-run
```

Special safety findings:

`v7-admin-auth-init` writes `/etc/v7/admin/auth.json`, creates a session secret, and writes the initial plaintext password to `/root/v7-admin-initial-password.txt` with mode `0600`. It does not print the generated password, but it is a live bootstrap mutation tool.

`v7-admin-password-rotate` rewrites `/etc/v7/admin/auth.json`, writes `/etc/v7/admin/rotated-password.txt`, may invalidate sessions by replacing `session_secret`, and removes the initial password file if present. It does not print the generated password, but it changes operator access material.

`v7-admin-auth-status` is read-only, but its output is still operator-only because it reveals auth state and sensitive file path existence.

`v7-safe-run` is an admin-facing safety gate. It blocks unknown commands and lifecycle mutations without `--dry-run`, but it delegates to allowlisted tools and writes an audit event, so it should not be treated as a pure read-only helper.

Updated counts after this batch:

```text
Runtime-only unresolved tools by basename: 88
Critical unresolved lineage by basename: 59
Total lineage resolved in metadata: 35
Remaining known unresolved by lineage metadata: 83
```

Admin/security lineage visibility improved, but admin hardening is not complete and no live password rotation, auth initialization, or safe-run workflow was executed.

## 16. Track 7.12 Provisioning Support Batch

Track 7.12 resolved the provisioning support lineage batch without mutating VPS runtime or live provisioning state.

Resolved runtime tools:

```text
v7-egress-guard
v7-egress-set-state
v7-egress-import-regression
v7-egress-draft-runtime-helper
v7-ipam-allocate
v7-ipam-preview
v7-reconcile-check
v7-reconcile-repair-preview
v7-provisioning-reconcile-check
```

Repo representation:

```text
tools/runtime-support/
tools/v7-egress-set-state
tools/v7-egress-import-regression
hardening/v7-provisioning-reconcile-check
```

Lineage metadata:

```text
docs/track7/lineage/provisioning-support-tools.json
```

Safety classification:

```text
read-only: v7-egress-guard, v7-provisioning-reconcile-check
egress-state-write: v7-egress-set-state
local-regression-write: v7-egress-import-regression
provisioning-write: v7-egress-draft-runtime-helper
IP-allocation: v7-ipam-allocate
provisioning-preview: v7-ipam-preview
reconcile-preview: v7-reconcile-check, v7-reconcile-repair-preview
```

Special safety findings:

`v7-egress-set-state` is a high-risk provisioning mutation tool. Dry-run is safe by intent, but `--apply` can start/stop interface runtimes, modify `egress.registry`, update `egress-flags.state`, rebuild kill switch, and write audit events.

`v7-egress-draft-runtime-helper` is a high-risk provisioning helper. It writes draft test results and draft metadata, can create temporary WireGuard/AmneziaWG or sing-box runtimes, runs curl/service probes, and cleans up temporary runtime config. It is not a passive validator.

`v7-ipam-allocate` defaults to dry-run, but confirmed apply mode writes `/opt/v7/ipam/leases.registry` and audit events after `--confirm ALLOCATE_IPAM`.

`v7-reconcile-repair-preview` is preview-only, but it emits suggested `v7-user-reconcile-apply` commands. That apply tool remains intentionally excluded from this batch.

`v7-egress-import-regression` and `v7-provisioning-reconcile-check` were already exact-hash present in the repo and were metadata-resolved without duplicating source.

Updated counts after this batch:

```text
Runtime-only unresolved tools by basename: 82
Critical unresolved lineage by basename: 55
Total lineage resolved in metadata: 44
Remaining known unresolved by lineage metadata: 74
```

Provisioning lineage visibility improved, but provisioning convergence is not complete and no live egress enable/disable, IP allocation, draft runtime, or reconcile repair was executed.

## 17. Track 7.13 Backup / Rollback Support Batch

Track 7.13 resolved the rollback/backup support lineage batch without mutating VPS runtime or executing rollback flows.

Resolved runtime tools:

```text
v7-rollback-last-change
v7-policy-live-rollback
v7-proxy-runtime-guard-rollback
v7-subnet-test-rollback
```

Repo representation:

```text
tools/runtime-support/
```

Lineage metadata:

```text
docs/track7/lineage/rollback-backup-support-tools.json
```

Safety classification:

```text
rollback-write: v7-rollback-last-change
rollback-preview: v7-policy-live-rollback
proxy-runtime-restore: v7-proxy-runtime-guard-rollback
routing-restore: v7-subnet-test-rollback
```

Special safety findings:

`v7-rollback-last-change` is broad rollback tooling. Dry-run identifies the newest backup candidate, but `--apply` can restore executables, WireGuard configs, V7 config files, admin auth config, identity DB, or egress state depending on the newest backup. It can also chmod restored targets and trigger systemd daemon-reload or restart `systemd-journald` for specific target classes.

`v7-policy-live-rollback` is currently a guarded placeholder. It validates backup readability and exits `BLOCKED_PLACEHOLDER`; it does not restore nftables or policy state yet.

`v7-proxy-runtime-guard-rollback` is high-risk rollback tooling. It restores nftables from `/root/v7-install-backups/proxy-runtime-guard-*` and can remove a created runtime user if no process is running under that user.

`v7-subnet-test-rollback` is optional rollback tooling. Dry-run is inert, but apply rewrites `/etc/v7/node.env`, removes iptables NAT rules for the test subnet, runs `v7-killswitch-enable`, then `v7-killswitch-check`.

Updated counts after this batch:

```text
Runtime-only unresolved tools by basename: 78
Critical unresolved lineage by basename: 52
Total lineage resolved in metadata: 48
Remaining known unresolved by lineage metadata: 70
```

Rollback lineage visibility improved, but rollback safety is not proven and no restore operation was executed.

## 18. Track 7.14 Profile Delivery / Token Tooling Batch

Track 7.14 resolved the profile delivery/token public gateway lineage without mutating VPS runtime or executing onboarding/profile delivery flows.

Resolved runtime tools:

```text
v7-public-gateway
```

Repo representation:

```text
tools/v7-public-gateway
```

Lineage metadata:

```text
docs/track7/lineage/profile-delivery-token-tools.json
```

Safety classification:

```text
public-delivery-proxy: v7-public-gateway
```

Special safety findings:

`v7-public-gateway` is the runtime-critical public ingress surface for `/connect`, `/api/connect/*`, `/api/profile-delivery-qr`, `/api/profile-import-qr`, `/profile-delivery/<token>`, `/profile-import/<token>`, and token-scoped speed paths. It does not create, rotate, persist, or print profile delivery tokens. It validates token-shaped path components, strips `Cookie` and `Authorization` headers before proxying, suppresses default request logging, and forwards allowlisted requests to the local admin upstream.

No standalone production-only delivery token writer was found in `runtime-enumeration.json`. Profile delivery token creation, revocation, QR rendering, delivery, import, and public connect onboarding are currently implemented inside `admin/v7-admin-api`; related profile-generation lineage for `v7-smart-client-profile-generate` and `v7-user-reissue-config` was already resolved in Track 7.10.

Skipped from this batch:

```text
v7-client-speed-api
v7-path-sample-ingest
```

These are token-scoped client speed/telemetry support tools, not profile delivery, token issuance, or onboarding ownership. They should be handled in a separate client telemetry/public API lineage batch.

Updated counts after this batch:

```text
Runtime-only unresolved tools by basename: 78
Critical unresolved lineage by basename: 52
Total lineage resolved in metadata: 49
Remaining known unresolved by lineage metadata: 69
```

`v7-public-gateway` already had an exact repo-side representation at `tools/v7-public-gateway`, so this batch improves lineage metadata and release ownership rather than reducing the runtime-only unresolved diff count. Profile delivery public ingress lineage is now visible, but onboarding safety and token governance are not proven complete because the core delivery-token lifecycle remains monolith-owned.

## 19. Track 7.15 Client Telemetry / Public Speed API Batch

Track 7.15 resolved the client telemetry and public speed-token API lineage batch without mutating VPS runtime, starting public services, ingesting live telemetry, or touching public gateway behavior.

Resolved runtime tools:

```text
v7-client-speed-api
v7-path-sample-ingest
```

Repo representation:

```text
tools/v7-client-speed-api
tools/v7-path-sample-ingest
```

Lineage metadata:

```text
docs/track7/lineage/client-telemetry-public-api-tools.json
```

Safety classification:

```text
public-api-service telemetry-write client-data-write: v7-client-speed-api
telemetry-ingest telemetry-write: v7-path-sample-ingest
```

Special safety findings:

`v7-client-speed-api` is a runtime-critical service bound by systemd. It serves a client speed-test page, `/health`, `/api/my-speed`, `/api/agent/poll`, and POST `/api/sample`. It reads users and egress registries, writes `client-speed.json`, `client-agents.json`, and `client-commands.json`, and delegates path sample persistence to `v7-path-sample-ingest`.

`v7-path-sample-ingest` validates sample JSON and writes bounded path sample history to `path-samples.json` unless `--dry-run` is used. Normal execution is telemetry-state mutation, so it was not executed against live runtime.

No profile delivery token file reads/writes were observed in either tool. Token-scoped public exposure is mediated by `v7-public-gateway`; this batch resolves the client telemetry/public speed support behind that path, not token lifecycle ownership.

Updated counts after this batch:

```text
Runtime-only unresolved tools by basename: 78
Critical unresolved lineage by basename: 52
Total lineage resolved in metadata: 51
Remaining known unresolved by lineage metadata: 67
```

`v7-client-speed-api` and `v7-path-sample-ingest` already had exact repo-side representations, so this batch improves lineage metadata and release ownership without reducing the runtime-only unresolved diff count. Telemetry privacy/safety is not proven complete.

## 20. Track 7.16 Read-Only Policy / Direct / Proxy Diagnostics Batch

Track 7.16 resolved a diagnostics/readiness-only lineage batch for policy, Direct/RU, and proxy runtime visibility. No VPS runtime mutation, policy apply, routing sync, autoswitch run, nftables change, route change, proxy runtime apply, service restart, or Direct/RU behavior change was performed.

Resolved runtime tools:

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

Repo representation:

```text
tools/runtime-support/
```

Lineage metadata:

```text
docs/track7/lineage/policy-direct-proxy-diagnostics-tools.json
```

Safety classification:

```text
read-only direct-state-read: v7-direct-list
read-only direct-status: v7-direct-status
direct-diagnostic network-probe temp-file: v7-direct-diagnose-domain
route-check direct-state-read: v7-direct-test-domain
policy-preview read-only: v7-policy-live-preview
policy-read by default; optional summary-write: v7-policy-matrix
route-check read-only wrapper: v7-policy-route-check
policy-read trusted-ru-state-read: v7-policy-show
policy-read route-check: v7-policy-test-domain
readiness-check state-read network-probe: v7-proxy-inbound-preflight
loopback-live-probe temp-process: v7-proxy-inbound-loopback-test
proxy-runtime-check temp-config: v7-proxy-policy-runtime-adapter-dry-run, v7-proxy-public-candidate-preview
readiness-check chained-dry-run: v7-proxy-public-enable-guard-dry-run
route-check proxy-runtime-check: v7-proxy-route-policy-dry-run
proxy-runtime-check apply-preview: v7-proxy-runtime-guard-apply-preview
policy-preview proxy-runtime-check temp-config: v7-proxy-service-aware-routing-dry-run
```

Skipped from this batch:

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

Skip rationale:

`v7-policy-resolve` writes `route-classes.state` during normal execution. Direct add/remove/auto-sync and proxy enable/disable/apply tools are mutation layers. `v7-trusted-ru-diagnostic` is intentionally deferred to a separate Trusted RU/Gosuslugi-sensitive review.

Special safety findings:

Most tools are read-only or dry-run by intent, but diagnostics are not automatically harmless. Some perform DNS, curl, systemctl, nft/ip reads, public IP probes, or `sing-box check` against temporary configs. `v7-proxy-inbound-loopback-test` starts temporary loopback-only `sing-box` processes if executed, so it is lineage-resolved but not treated as passive read-only execution. None of these tools was executed against live runtime in this track.

Updated counts after this batch:

```text
Runtime-only unresolved tools by basename: 63
Critical unresolved lineage by basename: 40
Total lineage resolved in metadata: 68
Remaining known unresolved by lineage metadata: 50
```

Policy/Direct/proxy diagnostics visibility improved, but policy/routing/proxy safety is not proven. Apply and synchronization layers remain out of scope.

## 21. Track 7.17 Direct/RU Mutation Governance Preview Batch

Track 7.17 resolved lineage and governance metadata for the first Direct/RU mutation-governance preview layer. No Direct/RU mutation, policy resolve execution, Trusted RU diagnostic execution, routing sync, autoswitch, nftables update, route change, dnsmasq restart, or Trusted RU/Gosuslugi behavior change was performed.

Resolved runtime tools:

```text
v7-direct-add-domain
v7-direct-remove-domain
v7-direct-auto-sync
v7-policy-resolve
v7-trusted-ru-diagnostic
```

Repo representation:

```text
tools/runtime-support/
```

Lineage metadata:

```text
docs/track7/lineage/direct-ru-mutation-governance-tools.json
```

Safety classification:

```text
Direct/RU-state-write service-restart: v7-direct-add-domain, v7-direct-remove-domain
auto-sync Direct/RU-state-write summary-write service-restart: v7-direct-auto-sync
policy-resolution-write route-class-state-write: v7-policy-resolve
Trusted-RU-read diagnostic-state-write network-probe: v7-trusted-ru-diagnostic
```

Trusted RU governance notes:

`v7-trusted-ru-diagnostic` is not passive read-only. It probes Gosuslugi/Trusted RU domains over direct, browser-like direct, VLESS/SOCKS, and AWG paths, then writes `/opt/v7/egress/state/trusted-ru-diagnostic.state`. It does not directly apply routing or rewrite route classes, but the state can influence operator/decision workflows downstream. It is Gosuslugi-sensitive and remains execution-blocked in governance work.

Skipped / deferred:

```text
v7-direct-preview
v7-policy-preview-apply
v7-trusted-ru-decision
v7-trusted-ru-refresh-missing
```

The two preview names were not present in runtime enumeration. Trusted RU decision/refresh tooling is adjacent and should be reviewed in a dedicated Trusted RU/Gosuslugi governance batch.

Updated counts after this batch:

```text
Runtime-only unresolved tools by basename: 58
Critical unresolved lineage by basename: 35
Total lineage resolved in metadata: 73
Remaining known unresolved by lineage metadata: 45
```

Direct/RU mutation semantics are now visible in repo-side lineage, but Direct/RU safety is not proven. These tools remain forbidden for live execution without an explicit high-risk rollout and rollback plan.

## 22. Track 7.18 Trusted RU Decision / Refresh Governance Batch

Track 7.18 resolved repo-side lineage and governance visibility for the Trusted RU decision/refresh layer. No Trusted RU decision execution, Trusted RU refresh execution, Gosuslugi live probing, Direct/RU mutation, policy apply, routing sync, autoswitch, nftables update, route change, service restart, chmod/chown, delete/archive, deploy, or VPS runtime mutation was performed.

Resolved runtime tools:

```text
v7-trusted-ru-decision
v7-trusted-ru-refresh-missing
```

Repo representation:

```text
tools/runtime-support/
```

Lineage metadata:

```text
docs/track7/lineage/trusted-ru-decision-refresh-tools.json
```

Safety classification:

```text
Trusted-RU-decision diagnostic-state-read optional-decision-state-write route-class-influence: v7-trusted-ru-decision
Trusted-RU-refresh diagnostic-state-read diagnostic-state-write decision-state-write network-probe route-class-influence: v7-trusted-ru-refresh-missing
```

Gosuslugi-sensitive boundary notes:

`v7-trusted-ru-decision` reads `/opt/v7/egress/state/trusted-ru-diagnostic.state` and converts probe results into `TRUSTED_RU_SENSITIVE` decision output. Its default fallback domain set includes Gosuslugi-sensitive domains. By default it prints preview output, but `--write-state` writes `/opt/v7/egress/state/trusted-ru-decision.state` through a temporary state file and `mv`.

`v7-trusted-ru-refresh-missing` is not read-only. It reads missing domains from decision state, can initialize decision state by calling `v7-trusted-ru-decision --write-state`, invokes `v7-trusted-ru-diagnostic` for selected missing domains, recalculates decision state with `--write-state`, and optionally calls `v7-state-json-save`. Because `v7-trusted-ru-diagnostic` performs live Trusted RU/Gosuslugi probes and writes diagnostic state, this wrapper is classified as refresh/state-write/network-probe governance.

Neither tool directly calls `v7-policy-apply`, `v7-routing-sync`, autoswitch, nftables, `ip route`, or `ip rule`, and neither directly rewrites Direct/RU domain lists. Their persisted state can still influence downstream operator and policy/routing decisions, so Trusted RU safety is not proven.

Skipped optional candidates:

```text
v7-trusted-ru-preview
v7-trusted-ru-status
v7-trusted-ru-report
```

These optional names were not present in runtime enumeration.

Updated counts after this batch:

```text
Runtime-only unresolved tools by basename: 56
Critical unresolved lineage by basename: 33
Total lineage resolved in metadata: 75
Remaining known unresolved by lineage metadata: 43
```

Trusted RU decision/refresh lineage is now visible, but Gosuslugi routing safety is not proven. Refresh/decision execution remains forbidden without a separate high-risk rollout, stale-state review, probe safety review, and rollback plan.
