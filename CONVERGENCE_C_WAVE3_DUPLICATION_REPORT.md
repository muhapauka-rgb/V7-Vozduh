# Convergence C Wave 3 Duplication Report

Project: V7 Vozduh
Block: Convergence C
Wave: 3
Title: Candidate Workflow Layer Preservation And Integration
Date: 2026-05-31

## Reality Audit

Direct `/usr/local/bin/v7-admin-api` remained unavailable in this local environment. Runtime comparison used cached runtime artifact `/private/tmp/p2_8_2-runtime-v7-admin-api`.

Remote refs were revalidated read-only:

- `origin/Updatesystem`: `b848fbf82f76f916b2fc6e5d04b24a1068e6048f`
- `origin/main`: `593619d494e215d11fd826086593527a4a555690`

## Hash And Route Inventory

| Source | Admin API sha256 | Routes | Execution routes |
| --- | --- | ---: | ---: |
| Runtime cached artifact | `8d7adc4d81f625c143ac4f227185c2b7e8708b511c01205c61b8905cbf3c1c04` | 221 | 8 |
| Convergence branch after Wave 3 | `bc34b6afbb440b12fbc121e9c42c1a5195f1adb1f4e0dc82afe13588950164f6` | 249 | 36 |
| Local dirty worktree | `8da1e5479723891f8619bbf5296239afb7e41d27f456b9601bd9799d289b705e` | 252 | 39 |
| `origin/Updatesystem` | `145f86a410ceaac87f80d97f7d8b8c72bf033b8a78e7106b10aa1500ea7c7ca4` | 213 | 0 |
| `origin/main` | `7f33f9721777e726c81617e984fd581cc9b5c1c3e2ecc7f74726b18b2a580977` | 165 | 0 |

## Overlaps

| Overlap | Location | Owner | Truth Source | Risk | Migration Decision |
| --- | --- | --- | --- | --- | --- |
| Approval Center | Runtime, branch, local | Operator admin | `operator_approval_preview` | High if duplicated | Reuse |
| Governance Preview | Runtime, branch, local | Operator execution governance | `operator_execution_governance_preview` | High if duplicated | Reuse |
| Rehearsal Preview | Runtime, branch, local | Operator execution rehearsal | `operator_execution_rehearsal_preview` | High if duplicated | Reuse |
| Candidate model | Local only | Candidate workflow layer | Derived from proposal plus draft preview | Medium | Merge as derived read model |
| Candidate approval | Local only | Candidate workflow layer | Approval Center preview | High | Merge as mapping only |
| Candidate governance | Local only | Candidate workflow layer | Governance Preview | High | Merge as mapping only |
| Candidate rehearsal | Local only | Candidate workflow layer | Rehearsal Preview | High | Merge as mapping only |
| Candidate admin UI | Local only | Admin UI | Execution drawer JS | Medium | Defer to Wave 4 |

## Excluded Public Routes

The following local-only routes remain excluded:

- `/api/execution/outcome-preview`
- `/api/execution/blast-radius`
- `/api/execution/service-impact`

## Verdict

duplication_audit_complete=true

Safety:

- runtime_mutation_performed=false
- routing_changed=false
- users_moved=false
- autoswitch_apply_run=false
- deploy_performed=false
- git_push_performed=false
- systemd_changed=false
