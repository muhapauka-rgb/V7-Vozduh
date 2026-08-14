# Z8.10 Root Cause And Remediation Plan

## Root cause

Production is not running the current authoritative `Updatesystem` code. It is using copied binaries in `/usr/local/bin` from a previous deployment model. The latest discovered deployment metadata points to `v7-next` commit `12e51a5ad4a6c34b09e37c9343d7ee78cb7678d6`, while the authoritative local/GitHub branch is `Updatesystem` at `c85e5cb82892b07853a19ed6e97629f5e85112dd`.

## Contributing causes

- `/opt/v7` is a state root, not a git checkout.
- Canonical deploy manifest and release symlink are missing.
- Production autoswitch binary lacks Z7/Z8 operation wiring markers.
- Production admin API hash does not match the authoritative local admin API.
- Autoswitch systemd timer is inactive, and no alternate autoswitch scheduler was found.
- Closure/execution stores required by the current operation model are absent on production.

## Safe remediation plan

No production remediation was performed during Z8.10.

Required before Z9 retry:

1. Approve a bounded convergence remediation window.
2. Back up current production binaries and state paths without deletion.
3. Deploy authoritative `Updatesystem` binaries to `/usr/local/bin` using a reversible copied-binary deploy procedure.
4. Create a deploy manifest or runtime linkage manifest recording branch, commit, package hash, binary hashes, deploy id, backup dir and timestamp.
5. Decide explicitly whether autoswitch is timer-driven or approved manual mode.
6. If timer-driven, restore scheduler activity only after binary convergence and governance review.
7. Initialize missing empty closure/execution stores only after ownership, permissions and expected schema are confirmed.
8. Run `v7-truth-check --local`, `--github` and `--all`.
9. Retry Z9 only if all truth-check blockers are cleared.

## Do not touch

- Do not run autoswitch `--apply` during remediation preparation.
- Do not move users.
- Do not mutate routes.
- Do not mutate restore barrier state.
- Do not delete backups or old deploy artifacts.
- Do not treat `/opt/v7` as a git checkout unless a future approved architecture change establishes that model.

