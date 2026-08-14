# BLOCK P2.8.3 ADMIN API CONVERGENCE DESIGN PACKAGE REPORT

Project: V7 Vozduh
Block: P2.8.3
Mode: Audit / Design / Convergence Planning
Date: 2026-05-31

## 1. Reality Revalidation

P2.8.2 findings were revalidated.

| Source | Admin API hash | Status |
| --- | --- | --- |
| Runtime | `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04` | active production behavior |
| Local | `8da1e5479723891f8619bbf5296239afb7e41d27f456b9601bd9799d289b705e` | dirty candidate |
| `origin/Updatesystem` | `145f86a410ceaac87f80d97f7d8b8c72bf033b8a78e7106b10aa1500ea7c7ca4` | committed development baseline |
| `origin/main` | `7f33f9721777e726c81617e984fd581cc9b5c1c3e2ecc7f74726b18b2a580977` | default/release history, behind |

See `P2_8_3_REALITY_REVALIDATION.md`.

## 2. Feature Map

Runtime-only features are the execution read APIs. Local-only features are P2.2-P2.7 draft, validation, simulation, candidate, approval, governance, rehearsal, workflow, and dry-run preview work. Shared features include operator observability, evidence/proposals, runtime/release trust, governance preview, and rehearsal preview.

See `P2_8_3_ADMIN_API_FEATURE_MAP.md`.

## 3. Feature Lineage Matrix

No single Admin API file is canonical for all subsystems. Runtime is canonical for live behavior, `Updatesystem` is canonical for committed development baseline, and local dirty work is a candidate for future convergence.

See `P2_8_3_FEATURE_LINEAGE_MATRIX.md`.

## 4. Convergence Options

Four options were designed:

- Option A: runtime becomes source.
- Option B: local becomes source.
- Option C: hybrid convergence.
- Option D: feature-by-feature convergence.

Recommended design direction is Option C executed through Option D.

See `P2_8_3_CONVERGENCE_OPTIONS.md`.

## 5. Canonical Source Model

Canonical model:

- Runtime source: runtime hash only for current deployed behavior.
- Development source: `origin/Updatesystem`.
- GitHub source: `origin/Updatesystem` for development; `main` for default/release history.
- Future source: reviewed convergence branch with deploy manifest.

See `P2_8_3_CANONICAL_SOURCE_MODEL.md`.

## 6. Migration Package Design

Migration should be split into packages:

1. Runtime read API preservation.
2. Execution draft and validation preview.
3. Simulation and rollback preview.
4. Candidate approval/workflow.
5. UI integration.
6. Tests and documentation.

See `P2_8_3_MIGRATION_PACKAGE_DESIGN.md`.

## 7. Production Patch Strategy

Runtime-only execution read APIs must be kept and reviewed. They should be backported or explicitly replaced by reviewed local equivalents. They must not be overwritten automatically.

See `P2_8_3_PRODUCTION_PATCH_STRATEGY.md`.

## 8. Branch Governance

`main` remains default/release history. `Updatesystem` is the convergence development baseline. `codex/*` branches remain experimental until audited. No branch operation was performed.

See `P2_8_3_BRANCH_GOVERNANCE.md`.

## 9. Convergence Risks

Highest risks:

- replacing runtime with `origin/Updatesystem` would remove runtime-only execution read APIs
- deploying local dirty file would ship unreviewed P2 preview/candidate code
- switching default/release branch without governance would obscure release truth

See `P2_8_3_CONVERGENCE_RISK_MODEL.md`.

## 10. Safe Convergence Roadmap

Roadmap:

1. Freeze runtime mutation.
2. Review runtime-only features.
3. Review local-only features.
4. Review GitHub/branch-only features.
5. Build convergence branch in a future block.
6. Run verification.
7. Prepare release package.
8. Execute deployment only in a separate approved block.

See `P2_8_3_SAFE_CONVERGENCE_ROADMAP.md`.

## 11. Recommended Canonical Direction

Recommended canonical direction: Hybrid, feature-by-feature convergence.

Runtime behavior must be preserved; local P2.2-P2.7 work should be reviewed and split; `Updatesystem` should be the development baseline; `main` should remain release/default history until branch governance explicitly changes it.

## 12. Recommended Next Block

Recommended next block: Admin API convergence branch preparation, still non-runtime and non-deploy.

It should produce reviewable patch packages from the runtime-only read APIs and local-only P2 work, without pushing or deploying unless separately authorized.

## Required Verdicts

feature_map_complete=true
feature_lineage_complete=true
convergence_options_defined=true
canonical_source_model_defined=true
migration_package_defined=true
production_patch_strategy_defined=true
branch_governance_defined=true
safe_convergence_roadmap_defined=true
recommended_canonical_direction_defined=true
safe_to_continue=false

## Safety Verdict

runtime_mutation_performed=false
routing_changed=false
users_moved=false
autoswitch_apply_run=false
git_push_performed=false
git_merge_performed=false
git_rebase_performed=false
deploy_performed=false
systemd_changed=false

Design package only. P2.9 was not started.
