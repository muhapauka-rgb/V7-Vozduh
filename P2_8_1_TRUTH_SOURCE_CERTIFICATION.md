# P2.8.1 Truth Source Certification

Project: V7 Vozduh
Block: P2.8.1

## Certification Decision

truth_source_certified=false

## Reason

Evidence does not support a single certified source of truth for all layers:

| Layer | Candidate truth source | Certification |
| --- | --- | --- |
| Live users/channels/routing/state | production runtime files under `/opt/v7`, `/etc/v7`, and live route/process state | canonical for runtime behavior only |
| Deployed executables | production `/usr/local/bin/v7-*` hashes | canonical for what is running, but source lineage incomplete |
| Committed implementation | GitHub `origin/Updatesystem` and `origin/main` | canonical for committed history only |
| Local implementation intent | local dirty worktree on `Updatesystem` | not certified until reviewed/committed |
| Documentation | P2/E reports and docs | descriptive, not canonical without hashes |

## Blocking Findings

- Runtime `v7-admin-api` hash is not equal to local working tree, `origin/Updatesystem`, or `origin/main`.
- Local worktree is dirty and contains untracked implementation reports/evidence.
- GitHub default branch is `main`, while active local implementation work is on `Updatesystem`.
- Runtime has production-only files and systemd units with incomplete repository lineage.

## Certified Interim Rule

Until convergence is completed:

- runtime state wins for live behavior
- runtime hashes win for deployed binaries
- GitHub hashes win for committed source history
- local dirty files are implementation intent only
- docs are advisory unless backed by current hashes
