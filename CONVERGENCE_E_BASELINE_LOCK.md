# Convergence E Baseline Lock

Project: V7 Vozduh
Program: Project Convergence
Block: Convergence E
Date: 2026-06-01

## Reality Audit

- Worktree: `/private/tmp/v7-convergence-c`
- Required branch: `convergence/admin-api-2026-05`
- Current branch: `convergence/admin-api-2026-05`
- Current HEAD: `b848fbf82f76f916b2fc6e5d04b24a1068e6048f`
- Local `origin/Updatesystem`: `b848fbf82f76f916b2fc6e5d04b24a1068e6048f`
- Remote `origin/Updatesystem`: `b848fbf82f76f916b2fc6e5d04b24a1068e6048f`
- Local `origin/main`: `593619d494e215d11fd826086593527a4a555690`
- Remote `origin/main`: `593619d494e215d11fd826086593527a4a555690`

No remote drift was found during the read-only ref check.

## Baseline Artifacts

| Artifact | SHA256 | Lines | API string inventory | Execution string inventory | Functions | Store constants |
|---|---:|---:|---:|---:|---:|---:|
| cached runtime `/private/tmp/p2_8_2-runtime-v7-admin-api` | `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04` | 33800 | 232 | 8 | 559 | 31 |
| convergence branch `admin/v7-admin-api` | `8bffa6a072ff411883c2522e7f760ac2df6713484d5cb2d8be834f438d707991` | 36097 | 261 | 37 | 647 | 31 |
| local dirty source `admin/v7-admin-api` | `8da1e5479723891f8619bbf5296239afb7e41d27f456b9601bd9799d289b705e` | 36469 | 264 | 40 | 655 | 31 |

The execution string inventory includes handler routes, role entries, and UI fetch references.
The contract tests use the handler route inventory for exact route verification.

## Baseline Decision

The baseline is locked on the local convergence branch. Convergence E proceeds without whole-file
replacement, without runtime overwrite, and without synchronizing to GitHub or runtime.

baseline_locked=true
