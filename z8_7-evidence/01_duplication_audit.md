# Z8.7 Evidence 01 - Duplication Audit

## Duplicate Source Candidates

| Candidate | Evidence | Risk | Decision |
| --- | --- | --- | --- |
| Local `Updatesystem` | Latest Z7/Z8 operation-aware work, commit `d61480d` | Dirty worktree, not pushed | Keep as `AUTHORITATIVE_WORKSPACE` / `CURRENT_WORK` |
| Remote `Updatesystem` | Exists, commit `7c84354` | Behind local by one commit | Keep but sync only after approval |
| Local `v7-next` worktree | `/private/tmp/v7-convergence-c`, commit `c40cae1` | Stale for operation wiring | Retire from active work |
| Remote `v7-next` | commit `c40cae1` | Stale for operation wiring despite historic name | Retire or redefine only after explicit branch decision |
| Remote `main` | default branch, commit `593619d` | Stale for operation wiring | Keep as public/default until governance decision, not runtime authority |
| `/private/tmp/v7-vozduh-main` | prunable/missing detached worktree | Confusing stale worktree record | Do not use; archive/prune later with approval |
| Production runtime `/opt/v7` | known from docs | Runtime truth unknown | Authoritative for state only after read-only proof |

## Dangerous Duplicates

- multiple active-looking branch names: `Updatesystem`, `v7-next`, `main`
- multiple local worktree records
- root-level report/evidence sprawl
- production runtime state unverified
- install script can copy source to `/usr/local/bin`, but no current deploy manifest is proven

## Retirement Requirement

`v7-next` cannot remain an active-authority branch while latest work lives on `Updatesystem`.

Only one branch may carry runtime authority after convergence.
