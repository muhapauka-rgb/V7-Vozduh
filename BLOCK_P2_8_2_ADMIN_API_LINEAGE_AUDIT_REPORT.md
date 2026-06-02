# BLOCK P2.8.2 ADMIN API LINEAGE AUDIT REPORT

Project: V7 Vozduh
Block: P2.8.2
Mode: Audit / Discovery / Lineage Verification
Date: 2026-05-31

## 1. Runtime Provenance

Runtime Admin API is `/usr/local/bin/v7-admin-api`, active under `v7-admin-api.service`, running as `root` through `python3 /usr/local/bin/v7-admin-api`.

Runtime hash: `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04`.

The runtime file was copied read-only to `/private/tmp` for diffing. No runtime mutation was performed.

See `P2_8_2_RUNTIME_ADMIN_API_PROVENANCE.md`.

## 2. Local Provenance

Local Admin API is dirty:

- path: `admin/v7-admin-api`
- hash: `8da1e5479723891f8619bbf5296239afb7e41d27f456b9601bd9799d289b705e`
- diff against HEAD: 3432 insertions, 20 deletions
- branch: `Updatesystem`
- HEAD/upstream: `b848fbf82f76f916b2fc6e5d04b24a1068e6048f`

See `P2_8_2_LOCAL_ADMIN_API_PROVENANCE.md`.

## 3. GitHub Provenance

No inspected GitHub branch equals runtime.

| Branch | Hash | Relation |
| --- | --- | --- |
| `main` | `7f33f9721777e726c81617e984fd581cc9b5c1c3e2ecc7f74726b18b2a580977` | far behind runtime |
| `Updatesystem` | `145f86a410ceaac87f80d97f7d8b8c72bf033b8a78e7106b10aa1500ea7c7ca4` | closest committed baseline |
| `codex/dynamic-load-autoswitch` | `7a1d133a9a4be1a5b4863248ae809c91788333432e69d1770b9f772843da3e26` | behind runtime |
| `codex/integratsiya-tunelya` | `34b64c9bd67ac2919df405f49413894ad95b9c9fa6b76a6bb673106b58fdca09` | behind runtime |
| `codex/dynamic-load-autoswitch-pr` | `61b32bc43940b5ca9fd1249f921adab7dfd1897ffcec8f9c1dcf117c40e63da6` | behind runtime |

See `P2_8_2_GITHUB_ADMIN_API_PROVENANCE.md`.

## 4. Runtime Vs Local

Local is a superset candidate of runtime:

- runtime-only detected routes vs local: none
- local-only detected routes vs runtime: 31
- local adds execution drafts, validation/verification/rollback previews, readiness, simulation, candidate approval/governance/rehearsal/workflow

See `P2_8_2_RUNTIME_LOCAL_DIFF.md`.

## 5. Runtime Vs GitHub

Runtime contains a production-only patch relative to `origin/Updatesystem`:

- 8 execution read-only routes are runtime-only vs `origin/Updatesystem`
- runtime hash has no match in local Git history
- no inspected GitHub branch equals runtime

See `P2_8_2_RUNTIME_GITHUB_DIFF.md`.

## 6. Local Vs GitHub

Local dirty work contains runtime execution APIs plus P2.2-P2.7 preview/candidate workflow work absent from `origin/Updatesystem`.

See `P2_8_2_LOCAL_GITHUB_DIFF.md`.

## 7. Feature Lineage

Runtime has execution summary/contracts/events/timeline/verification/rollback/explain. Local adds candidate, validation, simulation, readiness, approval, governance, rehearsal, and workflow layers. GitHub `Updatesystem` is behind runtime for execution store read APIs.

See `P2_8_2_FEATURE_LINEAGE_AUDIT.md`.

## 8. Production Patch Audit

Runtime Admin API is a production-only patch with UNKNOWN source lineage. It is not safe to overwrite automatically from any branch.

See `P2_8_2_PRODUCTION_PATCH_AUDIT.md`.

## 9. Canonical Source Decision

| Canonical target | Decision |
| --- | --- |
| Runtime source | runtime hash `8d7adc...` only for current live behavior |
| Development source | `origin/Updatesystem` as committed baseline; local dirty file as candidate patch |
| GitHub branch | `Updatesystem` for current control-plane development |
| Release branch | `main` until branch governance changes |
| Full Admin API source of truth | not certified |

See `P2_8_2_CANONICAL_SOURCE_DECISION.md`.

## 10. Safe Convergence Strategy

Do not converge automatically. Preserve runtime-only execution APIs, review local dirty P2 implementation, and only then decide whether to backport runtime patch, commit local candidate work, or replace runtime in a separate approved deploy block.

See `P2_8_2_SAFE_CONVERGENCE_STRATEGY.md`.

## 11. Risk Analysis

Overall lineage risk: CRITICAL.

Overall convergence risk: HIGH.

See `P2_8_2_RISK_ANALYSIS.md`.

## 12. Recommended Next Block

Recommended next block: Admin API convergence design package.

It should produce a reviewed patch plan that preserves runtime-only execution read APIs and splits local dirty P2 work into reviewable commits. It must still avoid deploy/runtime mutation unless separately authorized.

## Required Tables

### Table 1: Admin API Component

| Admin API Component | Runtime | Local | GitHub | Status |
| --- | --- | --- | --- | --- |
| File hash | `8d7adc...` | `8da1e...` | `Updatesystem` `145f86...`, `main` `7f33f...` | Diverged |
| Service binding | active systemd unit | not running | source only | Runtime canonical for behavior |
| Execution contracts/events | present | present | absent from `Updatesystem` | Runtime-only patch |
| Draft/validation/candidate previews | absent | present | absent | Local-only candidate |
| Operator governance/rehearsal | present | present | present in `Updatesystem` | Mostly aligned |

### Table 2: Runtime Only Features

| Runtime Only Features | Purpose | Risk | Migration Needed |
| --- | --- | --- | --- |
| `/api/execution/summary` and read APIs vs `Updatesystem` | read-only execution visibility | High | preserve/backport or supersede by reviewed local implementation |
| execution store normalization helpers | contract/event read models | High | preserve semantics |
| execution UI summary/contract drawers | operator visibility | Medium | migrate or replace through reviewed UI |

### Table 3: Local Only Features

| Local Only Features | Purpose | Risk | Migration Needed |
| --- | --- | --- | --- |
| execution draft APIs | dry-run contract preparation | High | review before commit/deploy |
| validation/verification/rollback previews | non-executable readiness workflow | High | review and test |
| candidate approval/governance/rehearsal/workflow | P2.7 workflow | High | review and commit |
| simulation/outcome/blast-radius previews | P2.5 previews | Medium | review retention and fail-closed behavior |

### Table 4: GitHub Only Features

| GitHub Only Features | Purpose | Risk | Migration Needed |
| --- | --- | --- | --- |
| `main` as default branch | release/default history | High if mistaken for runtime source | branch policy |
| remote `codex/dynamic-load-autoswitch-pr` | old candidate branch | Medium | archive/close/triage |

### Table 5: Feature

| Feature | Runtime | Local | GitHub | Canonical Source | Status |
| --- | --- | --- | --- | --- | --- |
| Authority | present | present | partial | runtime for behavior, `Updatesystem` for source | Partial |
| Candidate | partial/absent P2.7 | present | absent | local candidate | Local-only |
| Execution | read-only APIs present | expanded | absent from `Updatesystem` | runtime for behavior | Runtime-only |
| Simulation | limited | present | absent | local candidate | Local-only |
| Readiness | general | execution readiness present | partial | local candidate | Local-only extension |
| Approval Center | preview | candidate approval present | partial | local candidate | Partial |
| Governance Preview | present | present | present | aligned baseline | Present |
| Rehearsal Preview | present | present | present | aligned baseline | Present |
| Execution Contracts | present | present plus drafts | absent from `Updatesystem` | runtime/local split | Diverged |
| Execution Events | present | present | absent from `Updatesystem` | runtime | Runtime-only |
| Operator Workflow | present | expanded | present baseline | runtime/local split | Partial |
| Validation Preview | absent | present | absent | local candidate | Local-only |
| Rollback Preview | partial | expanded | partial | local candidate | Partial |

## Required Verdicts

runtime_admin_api_provenance_complete=true
local_admin_api_provenance_complete=true
github_admin_api_provenance_complete=true
runtime_local_diff_understood=true
runtime_github_diff_understood=true
local_github_diff_understood=true
feature_lineage_complete=true
canonical_source_defined=true
safe_convergence_strategy_defined=true
safe_to_continue=false

## Safety Verdict

runtime_mutation_performed=false
routing_changed=false
users_moved=false
autoswitch_apply_run=false
git_push_performed=false
git_merge_performed=false
deploy_performed=false
systemd_changed=false

Read-only lineage audit only. P2.9 was not started.
