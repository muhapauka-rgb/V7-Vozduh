# BLOCK P2.8 REPOSITORY RUNTIME GITHUB CONVERGENCE AUDIT REPORT

Project: V7 Vozduh
Block: P2.8
Mode: Audit / Discovery / Truth Verification

## 1. Runtime Discovery

Public runtime is alive:

- Admin health: OK
- Admin `/admin-v2`: redirects to `/login`
- Public gateway: responds as `V7PublicGateway/0.1 Python/3.14.4`

Local workstation is not the production runtime:

- macOS/launchd, not Linux/systemd
- no local `/opt/v7` or `/etc/v7`
- no local `127.0.0.1:7080`
- Docker has unrelated `rent_*` containers

## 2. Runtime Source Discovery

Local runtime source candidates are `admin/v7-admin-api`, `admin_core/*`, `tools/v7-*`, `tools/runtime-support/v7-*`, and `systemd/*`.

Production source hash is not proven. Public checks do not expose `/usr/local/bin/v7-admin-api` content.

## 3. Local Repository Audit

- Branch: `Updatesystem`
- HEAD: `b848fbf82f76f916b2fc6e5d04b24a1068e6048f`
- Upstream: `origin/Updatesystem`
- Ahead/behind: `0/0`
- Dirty: yes
- Modified: `admin/v7-admin-api`
- Untracked: P2.1-P2.7 reports/evidence and P2.7 tests

## 4. GitHub Audit

Remote HEAD is `main` at `593619d494e215d11fd826086593527a4a555690`.

Live remote branches:

- `Updatesystem`: `b848fbf82f76f916b2fc6e5d04b24a1068e6048f`
- `main`: `593619d494e215d11fd826086593527a4a555690`
- `codex/dynamic-load-autoswitch`: `0ea6d4ef82abaad26b0609d254bb6cf297db6432`
- `codex/dynamic-load-autoswitch-pr`: `3b0fab9b639a10d55e232a8d6320a12d97f0c34e`
- `codex/integratsiya-tunelya`: `a0e689c67ef7d47e7f04e5c30e5430acd05752cb`

## 5. Runtime vs Local

runtime_local_aligned=false

Runtime is alive, but local machine is not production and local source has uncommitted changes that are not proven deployed.

## 6. Runtime vs GitHub

runtime_github_aligned=false

Runtime source hash was not collected. Runtime cannot be proven equal to GitHub `main` or `Updatesystem`.

## 7. Local vs GitHub

local_github_aligned=false

Committed `Updatesystem` tip matches upstream, but worktree is dirty and GitHub has a branch not present in local remote refs.

## 8. Production-Only Audit

Production-only risk remains around `/usr/local/bin/v7-*`, `/opt/v7`, `/etc/v7`, systemd units, Caddy, proxy/sing-box, and live state stores. Historical docs already identify production-only lineage gaps.

## 9. Documentation Drift

documentation_drift_found=true

Endpoint inventory docs are stale. Current local static inventory reports `264` endpoints; `docs/track5/endpoint-inventory.json` reports `211`.

## 10. Admin Drift

admin_drift_found=true

Runtime admin is alive; local admin is dirty; GitHub default branch is not the local branch; runtime source hash is unverified.

## 11. API Drift

api_drift_found=true

Local current source inventory:

- endpoint_count `264`
- GET `118`
- HEAD `8`
- POST `138`

Documented inventory:

- endpoint_count `211`
- GET `66`
- HEAD `8`
- POST `137`

## 12. Truth Source Map

See `P2_8_TRUTH_SOURCE_MAP.md`. Live production state remains canonical for runtime/user/channel/routing state. Local repo is only implementation intent until committed/deployed. GitHub is committed source, not current dirty work.

## 13. Convergence Plan

Do not fix in P2.8. Required future convergence:

- collect production source hashes
- decide `main` vs `Updatesystem` release/default branch policy
- triage local dirty work
- triage GitHub-only branch
- regenerate or mark stale endpoint inventory
- map production-only tools to repo source

## 14. Risk Analysis

Overall risk: High.

Main reason: runtime, local repository, GitHub, API inventory, and docs are not proven converged.

## 15. Recommended Next Step

Run a dedicated read-only runtime provenance block with SSH or a signed runtime manifest: hash `/usr/local/bin/v7-*`, systemd units, `/etc/v7` configs, and selected non-secret state metadata; compare those hashes to local and GitHub without applying changes.

## Required Tables

### Table 1: Component Matrix

| Component | Runtime | Local | GitHub | Status |
| --- | --- | --- | --- | --- |
| Admin API | Public health OK | dirty `admin/v7-admin-api` | branch source exists | Drift |
| Public Gateway | Active on port 80 | `tools/v7-public-gateway` exists | source exists | Source hash unverified |
| Client Speed API | port 7090 refused from public path | `tools/v7-client-speed-api` exists | source exists | Runtime path unclear |
| Systemd units | historical production active | `systemd/*` exists | source exists | Current runtime unverified |
| Candidate APIs | runtime unknown due auth | local P2.7 added | not pushed | Drift |
| Endpoint inventory | runtime unknown | 264 generated to temp | docs show 211 | Drift |

### Table 2: Runtime Only

| Runtime Only | Purpose | Risk | Migration Needed |
| --- | --- | --- | --- |
| `/opt/v7/egress/state/*` | live users/channels/state | High | manifest/hash metadata |
| `/etc/v7/*` | policy/config/auth | High | source-of-truth map |
| `/usr/local/bin/v7-*` | deployed tools | High | repo lineage check |
| Caddy runtime config | public TLS/ingress | Medium | config provenance |

### Table 3: Local Only

| Local Only | Purpose | Risk | Migration Needed |
| --- | --- | --- | --- |
| dirty `admin/v7-admin-api` | P2.1-P2.7 implementation | High | commit/review/deploy decision |
| `P2_7_*.md` | local docs | Medium | commit or archive |
| P2 evidence dirs | implementation evidence | Medium | commit or archive |
| `tests/unit/test_p2_7_candidate_workflow.py` | P2.7 tests | Medium | commit/review |

### Table 4: GitHub Only

| GitHub Only | Purpose | Risk | Migration Needed |
| --- | --- | --- | --- |
| `codex/dynamic-load-autoswitch-pr` | unknown branch from remote | Medium | fetch/triage later |
| `main` as default | repository default branch | Medium | branch policy decision |

### Table 5: Domain Truth Source

| Domain | Canonical Truth Source | Derived Sources | Dangerous Duplicates |
| --- | --- | --- | --- |
| Users | production `users.registry` | admin/state JSON | fixtures/backups |
| Channels | production `egress.registry` | admin views | stale backups |
| Candidate | derived P2.6 model | P2.7 bridge | second candidate queue |
| Execution | execution contract/event stores | previews | executable dry-run store |
| Audit | production audit files | audit APIs | report excerpts |
| Release | Git plus deploy manifest | release trust API | docs without hashes |

## Required Verdicts

runtime_discovered=true
local_repository_audited=true
github_audited=true
runtime_local_aligned=false
runtime_github_aligned=false
local_github_aligned=false
truth_source_map_complete=true
documentation_drift_found=true
admin_drift_found=true
api_drift_found=true
safe_to_continue=false

## Safety Verdict

runtime_mutation_performed=false
routing_changed=false
users_moved=false
autoswitch_apply_run=false
git_push_performed=false
deploy_performed=false
systemd_changed=false

Read-only audit only. P2.9 was not started.
