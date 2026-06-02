# Convergence B Wave 0 Baseline

Project: V7 Vozduh
Program: Project Convergence
Block: Convergence B
Mode: Implementation Preparation
Date: 2026-05-31

## Scope

Wave 0 baseline capture only. No branch was created. No source file was modified. No deploy, runtime mutation, systemd change, routing change, user movement, autoswitch apply, policy apply, killswitch mutation, trusted/direct RU mutation, execution engine, or runtime hook was performed.

## Runtime Hashes

| Artifact | Hash / Count | Notes |
| --- | --- | --- |
| `/usr/local/bin/v7-admin-api` | `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04` | active runtime Admin API |
| `/usr/local/bin` | 181 files at maxdepth 3 | read-only count |
| `/etc/systemd/system` | 45 files at maxdepth 3 | read-only count |
| `/etc/v7` | 90 files at maxdepth 3 | read-only count |
| `/opt/v7` | 509 files at maxdepth 3 | live state count; expected to drift over time |

## Local Hashes

| Artifact | Hash / Status |
| --- | --- |
| `admin/v7-admin-api` | `8da1e5479723891f8619bbf5296239afb7e41d27f456b9601bd9799d289b705e` |
| Local branch | `Updatesystem` |
| Local Admin API diff | 3432 insertions, 20 deletions |
| Worktree status | dirty |

## GitHub Hashes

| Ref | Branch SHA | Admin API hash |
| --- | --- | --- |
| `origin/Updatesystem` | `b848fbf82f76f916b2fc6e5d04b24a1068e6048f` | `145f86a410ceaac87f80d97f7d8b8c72bf033b8a78e7106b10aa1500ea7c7ca4` |
| `origin/main` | `593619d494e215d11fd826086593527a4a555690` | `7f33f9721777e726c81617e984fd581cc9b5c1c3e2ecc7f74726b18b2a580977` |
| `origin/codex/dynamic-load-autoswitch` | `0ea6d4ef82abaad26b0609d254bb6cf297db6432` | `7a1d133a9a4be1a5b4863248ae809c91788333432e69d1770b9f772843da3e26` |
| `origin/codex/integratsiya-tunelya` | `a0e689c67ef7d47e7f04e5c30e5430acd05752cb` | `34b64c9bd67ac2919df405f49413894ad95b9c9fa6b76a6bb673106b58fdca09` |
| `codex/dynamic-load-autoswitch-pr` | `3b0fab9b639a10d55e232a8d6320a12d97f0c34e` | remote-only in current local refs |

## Route And API Inventory

| Source | Lines | Functions | Routes | API routes | GET role entries | UI API fetches |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Runtime Admin API | 33800 | 585 | 221 | 212 | 204 | 16 |
| Local Admin API | 36469 | 681 | 252 | 243 | 232 | 30 |
| `origin/Updatesystem` Admin API | 33057 | 560 | 213 | 204 | 197 | 14 |
| `origin/main` Admin API | 21624 | 352 | 165 | 157 | 157 | 4 |

## Runtime Execution Read Routes

Runtime has exactly these execution read routes:

- `/api/execution/summary`
- `/api/execution/contracts`
- `/api/execution/contracts/`
- `/api/execution/events`
- `/api/execution/timeline`
- `/api/execution/verification`
- `/api/execution/rollback`
- `/api/execution/explain`

`origin/Updatesystem` and `origin/main` are missing all eight runtime execution read routes. Local contains all eight plus 31 local-only execution/candidate/preview routes.

## Package Inventory

Package inventory remains aligned with Convergence A:

1. Runtime Read APIs
2. Execution Draft
3. Validation Preview
4. Simulation
5. Rollback Preview
6. Candidate Workflow
7. Approval/Governance/Rehearsal
8. UI Integration
9. Tests
10. Documentation
11. Runtime Support
12. Systemd
13. Tools
14. Branch/Release Governance

## Truth Source Map

Runtime remains live behavior truth. `origin/Updatesystem` remains development baseline. `main` remains release history. Local dirty Admin API remains candidate package source.

## Convergence Matrix Pointer

Use `CONVERGENCE_A_CONVERGENCE_MATRIX.md` as the current matrix foundation. No package-level drift was discovered in Convergence B reality audit.

baseline_captured=true
