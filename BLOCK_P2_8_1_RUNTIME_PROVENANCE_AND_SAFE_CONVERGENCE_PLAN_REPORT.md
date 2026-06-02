# BLOCK P2.8.1 RUNTIME PROVENANCE AND SAFE CONVERGENCE PLAN REPORT

Project: V7 Vozduh
Block: P2.8.1
Mode: Audit / Discovery / Version Governance
Date: 2026-05-31

## 1. Runtime Provenance

Runtime host was inspected through read-only SSH:

- hostname: `v3119922.hosted-by-vdsina.ru`
- kernel: `Linux v3119922.hosted-by-vdsina.ru 7.0.0-14-generic #14-Ubuntu SMP PREEMPT_DYNAMIC Mon Apr 13 11:09:53 UTC 2026 x86_64 GNU/Linux`
- admin runtime: `127.0.0.1:7080`, `python3 /usr/local/bin/v7-admin-api`
- public gateway: `0.0.0.0:80`, `python3 /usr/local/bin/v7-public-gateway`
- key runtime directories: `/usr/local/bin`, `/etc/systemd/system`, `/etc/v7`, `/opt/v7`

See `P2_8_1_RUNTIME_PROVENANCE.md`.

## 2. Runtime Manifest

Runtime manifest was collected by path, size, mtime, and SHA256. Directory counts:

- `/usr/local/bin`: 181 files
- `/etc/systemd/system`: 45 files
- `/etc/v7`: 90 files
- `/opt/v7`: 512 files

Important runtime hash:

- `/usr/local/bin/v7-admin-api`: `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04`

See `P2_8_1_RUNTIME_MANIFEST.md`.

## 3. Local Provenance

Local repository:

- branch: `Updatesystem`
- HEAD: `b848fbf82f76f916b2fc6e5d04b24a1068e6048f`
- upstream: `origin/Updatesystem`
- dirty: yes
- modified tracked file: `admin/v7-admin-api`
- untracked entries: 41

See `P2_8_1_LOCAL_PROVENANCE.md`.

## 4. GitHub Provenance

GitHub remote was checked with read-only `git ls-remote`:

- default branch: `main`
- `main`: `593619d494e215d11fd826086593527a4a555690`
- `Updatesystem`: `b848fbf82f76f916b2fc6e5d04b24a1068e6048f`
- `codex/dynamic-load-autoswitch-pr`: `3b0fab9b639a10d55e232a8d6320a12d97f0c34e`

See `P2_8_1_GITHUB_PROVENANCE.md`.

## 5. Hash Audits

Runtime/local:

- many operational tools match exactly
- Admin API differs: runtime `8d7adc...`, local dirty `8da1e...`
- runtime `v7-api` has no local exact basename match

Runtime/GitHub:

- runtime is closer to `origin/Updatesystem` than `origin/main`
- Admin API differs from both `origin/Updatesystem` and `origin/main`

Local/GitHub:

- local HEAD equals `origin/Updatesystem`
- worktree does not equal GitHub because `admin/v7-admin-api` is dirty and reports/evidence are untracked

See:

- `P2_8_1_RUNTIME_LOCAL_HASH_AUDIT.md`
- `P2_8_1_RUNTIME_GITHUB_HASH_AUDIT.md`
- `P2_8_1_LOCAL_GITHUB_HASH_AUDIT.md`

## 6. Production-Only Gaps

Production-only or uncertified gaps include:

- runtime Admin API source lineage
- `/usr/local/bin/v7-api`
- `/usr/local/bin/v7-traffic-snapshot`
- several runtime systemd units without exact local source paths
- `/etc/v7` config/state classification
- `/opt/v7` live state/event stores
- remote-only `codex/dynamic-load-autoswitch-pr`

See `P2_8_1_PRODUCTION_ONLY_GAPS.md`.

## 7. Truth Source Certification

Single Source Of Truth cannot be certified.

Interim rule:

- runtime state wins for live behavior
- runtime hashes win for deployed binaries
- GitHub hashes win for committed source history
- local dirty files are implementation intent only
- docs are advisory unless backed by current hashes

See `P2_8_1_TRUTH_SOURCE_CERTIFICATION.md`.

## 8. Branch Strategy

`main` remains the GitHub default branch. `Updatesystem` is the active candidate convergence branch because it contains most runtime tool paths and matches many runtime hashes.

No merge/rebase/push was performed.

See `P2_8_1_BRANCH_STRATEGY.md`.

## 9. Safe Convergence Plan

Convergence should be done only after:

1. Admin API lineage is resolved.
2. Production-only artifacts are mapped.
3. Branch policy is approved.
4. Dirty local work is reviewed and committed or split.
5. A signed runtime deploy manifest exists.

See `P2_8_1_SAFE_CONVERGENCE_PLAN.md`.

## 10. Risk Analysis

Overall risk: High.

Primary blocker: runtime/local/GitHub Admin API hashes do not converge.

See `P2_8_1_RISK_ANALYSIS.md`.

## 11. Next Block Recommendation

Run a dedicated Admin API lineage block:

- compare runtime Admin API behavior and source lineage
- decide whether runtime Admin API must be captured as a production-only patch or replaced by reviewed repository source
- keep runtime mutation forbidden until the decision is explicit

## Required Verdicts

runtime_provenance_complete=false
runtime_manifest_complete=true
local_provenance_complete=true
github_provenance_complete=true
runtime_local_hashes_verified=false
runtime_github_hashes_verified=false
local_github_hashes_verified=false
truth_source_certified=false
branch_strategy_defined=true
safe_convergence_plan_defined=true
safe_to_continue=false

## Safety Verdict

runtime_mutation_performed=false
routing_changed=false
users_moved=false
autoswitch_apply_run=false
policy_apply_run=false
killswitch_mutation_performed=false
trusted_direct_ru_mutation_performed=false
execution_engine_implemented=false
runtime_hooks_implemented=false
git_push_performed=false
git_merge_performed=false
git_rebase_performed=false
deploy_performed=false
systemd_changed=false
