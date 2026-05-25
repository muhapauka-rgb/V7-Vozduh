# V7 Vozduh - Track 4 Platform Evolution & Commercial Maturity Foundation

Generated: 2026-05-23

Scope: move V7 from stabilized operational prototype toward predictable commercial-grade routing platform foundation.

No runtime behavior changes were applied in Track 4.

## 1. Runtime Governance Registry

Created:

- `docs/track4/RUNTIME_GOVERNANCE_REGISTRY.md`

The registry formalizes:

- owner;
- category;
- mutation level;
- safety level;
- rollback sensitivity;
- repo lineage;
- operational criticality;
- cleanup status;
- required verification.

Current governed baseline:

| Runtime Class | Count | Status |
|---|---:|---|
| Active runtime executables | 24 | Preserve |
| Unknown active-like tools | 117 | Govern before cleanup |
| Known suspicious executables | 0 | Cleared in Block 3.4 |
| Backup-like stale executables in PATH | 0 | Cleared in Block 3.2 |
| Total `/usr/local/bin/v7*` | 141 | Cleaner but not release-governed |

Main risk:

`103` production-only tools still lack clean repo lineage.

## 2. Release Lineage Foundation

Created:

- `docs/track4/RELEASE_LINEAGE_FOUNDATION.md`

Defined:

- release ID model;
- release manifest structure;
- provenance rules;
- production-only tool handling;
- runtime reproducibility classes.

Current reality:

- deploy baseline exists:
  `/opt/v7/ops/deploy-baseline/20260523T122251Z`
- archive manifests exist:
  - `/root/v7-backups/usr-local-bin-archive/20260523T122936Z`
  - `/root/v7-backups/usr-local-bin-archive/20260523T124646Z`
- no release ID/provenance chain exists yet.

Verdict:

Release truth foundation is now defined, but not implemented as a release process.

## 3. Sensitive-State Inventory

Created:

- `docs/track4/SENSITIVE_STATE_HARDENING_PLAN.md`

Read-only live inventory found:

| Path | Mode | Risk |
|---|---|---|
| `/opt/v7/egress/state/profile-delivery-tokens.json` | `0644` | High |
| `/opt/v7/admin/v7-identity.db` | `0600` | Controlled |
| `/opt/v7/identity/v7-identity.db` | missing | Historical contract mismatch |
| `/etc/v7/policy.json` | `0644` | Medium |
| `/etc/v7/org-egress-policy.json` | `0644` | Medium |
| `/opt/v7/egress/state/users.registry` | `0644` | Medium |
| `/opt/v7/egress/state/egress.registry` | `0644` | Medium |
| `/opt/v7/egress/state/autoswitch-safety.json` | `0644` | Medium |
| `/opt/v7/egress/state/client-reconnect-state.json` | `0644` | Medium |

Identity DB:

- canonical live path: `/opt/v7/admin/v7-identity.db`
- read-only open: OK
- tables present: 12
- organizations: 3
- identity users: 12
- devices: 21
- onboarding attempts: 42

No chmod/chown changes were applied.

## 4. Monolith Containment Plan

Created:

- `docs/track4/MONOLITH_CONTAINMENT_AND_COMMERCIAL_MATURITY.md`

Current state:

- `admin/v7-admin-api`: `30067` lines
- runtime-critical;
- contains auth, identity, provisioning, policy, diagnostics, observability, autoswitch wrappers, and embedded UI.

Containment strategy:

1. Extract read-only helpers first.
2. Freeze endpoint schemas before moving code.
3. Avoid early extraction of switching, policy apply, direct/RU, profile delivery, provisioning apply, and autoswitch apply.
4. Preserve endpoint paths, JSON shapes, auth behavior, redaction, audit, and shell command semantics.

Verdict:

Do not rewrite. Contain, freeze contracts, extract low-risk read-only code first.

## 5. Operator UX Evolution Priorities

Track 4 keeps Calm Operator UX as a hard constraint.

Priorities:

- compact platform status;
- incident-first navigation;
- runtime governance summary;
- provisioning readiness summary;
- grouped diagnostics with drill-down;
- no metric wall;
- no Grafana-style screen.

Recommended operator summary fields:

```text
System state
Affected users
Degraded channels
Autoswitch guard state
Trusted/direct RU status
Runtime baseline status
Sensitive-state warnings
```

## 6. Provisioning Maturity Review

Current maturity:

- lifecycle docs exist;
- quarantine model exists;
- driver/capability model exists in docs;
- rollback model exists;
- egress validation helpers exist.

Commercial gaps:

- lifecycle is not fully enforced as a runtime contract everywhere;
- driver capabilities are not consistently persisted/enforced;
- rollback verification is not yet one operator-visible truth;
- actor/reason/before-after audit is not fully uniform;
- production-only provisioning tools lack clean repo lineage.

Next safe priorities:

1. Make lifecycle validator operator-visible.
2. Add capability metadata to egress registry without changing routing.
3. Add dry-run enable report.
4. Keep production enable explicit/manual.

## 7. Commercial Readiness Gap Analysis

| Area | Status | Commercial Risk |
|---|---|---|
| Datapath safety | Verified OK in this pass | Needs continuous validation |
| Autoswitch | Stabilized | Frozen-user/health nuance remains |
| Runtime governance | Started | 117 unknown active-like tools need ownership |
| Release lineage | Defined, not implemented | Rebuild from repo not guaranteed |
| Sensitive state | Mixed | Token state mode `0644` |
| Identity | Operational | Historical path mismatch remains documented |
| Provisioning | Partially mature | Lifecycle enforcement incomplete |
| Admin monolith | Operational | 30k-line coupling risk |
| Operator UX | Calmer foundation | Still dense/monolithic |
| Commercial org model | Partially present | Needs stronger policy/workflow enforcement |

Overall classification:

```text
stabilized operational prototype with credible commercial-grade foundation
```

Not yet:

```text
commercial-grade platform
```

## 8. Runtime Reproducibility Analysis

Good:

- baseline manifest exists;
- archive manifests exist;
- stale/suspicious PATH clutter removed;
- active runtime checks pass.

Weak:

- no release ID;
- no source commit to runtime manifest chain;
- production-only tools remain;
- deployment still file-based and partly manual;
- rollback material exists but is not tied to a release object.

Bounded next step:

Create a current release manifest that links:

- source state;
- deploy baseline;
- archive lineage;
- current executable inventory;
- verification results;
- unresolved production-only tools.

## 9. Exact Changes Applied

Local documentation/foundation files added:

- `docs/track4/RUNTIME_GOVERNANCE_REGISTRY.md`
- `docs/track4/RELEASE_LINEAGE_FOUNDATION.md`
- `docs/track4/SENSITIVE_STATE_HARDENING_PLAN.md`
- `docs/track4/MONOLITH_CONTAINMENT_AND_COMMERCIAL_MATURITY.md`
- `TRACK4_PLATFORM_EVOLUTION_REPORT.md`

Live runtime changes:

- None.

## 10. Verification Results

Read-only live verification after Track 4 inspection:

| Check | Result |
|---|---|
| `systemctl --failed` | PASS, `0 loaded units listed` |
| `v7-killswitch-check` | PASS |
| `v7-user-route-check` | PASS |
| `v7-provisioning-reconcile-check` | PASS |
| `v7-observability-summary --pretty` | PASS |

Runtime notes:

- `/usr/local/bin/v7*.tmp`: none.
- `/usr/local/bin/v7*`: `141`.
- deploy baseline present.
- archive manifests present.
- identity DB readable at canonical path.

## 11. Remaining Maturity Blockers

Critical:

- release lineage is defined but not implemented;
- production-only runtime tools need ownership;
- sensitive token state hardening is pending;
- admin monolith is still a major coupling risk;
- provisioning lifecycle needs runtime enforcement maturity.

Important:

- operator UX needs runtime governance and sensitive-state warnings in calm summary form;
- direct/RU diagnostics remain intentionally untouched and should be handled separately;
- commercial org/user/device model needs stronger policy enforcement review.

## 12. Recommended Next Platform-Evolution Priorities

1. Create current release manifest with release ID.
2. Build runtime tool registry v1 from Block 3.3 data.
3. Do a sensitive-state access mapping pass before chmod.
4. Add a read-only sensitive-state permission validator.
5. Freeze admin API endpoint schemas before extraction.
6. Extract read-only helper modules from admin monolith.
7. Add operator-visible provisioning readiness summary.
8. Keep all routing/direct/RU/autoswitch behavior stable unless a dedicated safety block requires change.

