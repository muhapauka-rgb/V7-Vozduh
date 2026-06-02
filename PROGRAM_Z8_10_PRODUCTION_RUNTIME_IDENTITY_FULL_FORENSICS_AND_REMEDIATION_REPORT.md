# PROGRAM Z8.10 - Production Runtime Identity Full Forensics And Remediation Report

Project: V7 Vozduh

Branch: `Updatesystem`

Mode: read-only production forensics, local truth-check update, no production mutation.

## Executive verdict

Z8.10 found the root cause of the Z9 runtime truth failure.

Production is not a git checkout of the authoritative workspace. `/opt/v7` is a state/runtime tree. Production execution uses copied binaries in `/usr/local/bin`, with partial provenance in `/opt/v7/ops/deploy-*`. The latest deploy metadata identifies `v7-next` commit `12e51a5ad4a6c34b09e37c9343d7ee78cb7678d6`, while the authoritative local/GitHub branch is `Updatesystem` at `c85e5cb82892b07853a19ed6e97629f5e85112dd`.

The production autoswitch and admin API binaries do not match authoritative local hashes. Production autoswitch also lacks the Z7/Z8 operation markers required by the current runtime execution model.

## Safety record

No deploy was performed.
No git pull, push or merge was performed during production discovery.
No autoswitch apply was run.
No user movement was performed.
No route mutation was performed.
No restore barrier mutation was performed.
No service restart or systemd mutation was performed.
No cleanup or deletion was performed.

## Evidence folder

Evidence is stored in `z8_10-evidence`.

- `runtime_identity_snapshot.json`
- `00_local_and_github_truth.md`
- `01_production_inventory.md`
- `02_binary_and_operation_wiring_forensics.md`
- `03_scheduler_and_service_forensics.md`
- `04_runtime_root_and_provenance.md`
- `05_state_store_forensics.md`
- `06_root_cause_and_remediation_plan.md`

## Root cause

Primary root cause:

Production runtime identity diverged from repository truth because production is a copied-binary deployment from an older `v7-next` commit, not a live checkout of the current authoritative `Updatesystem` branch.

Secondary causes:

- Missing canonical deploy manifest at `/opt/v7/deploy-manifest.json`.
- Missing release root/symlink at `/opt/v7/releases/current`.
- Autoswitch timer is inactive and no alternate autoswitch scheduler was found.
- Closure and execution stores are absent.
- Production autoswitch lacks current operation wiring.

## Binary truth

| Component | Production hash | Authoritative hash | Verdict |
| --- | --- | --- | --- |
| `v7-users-autoswitch` | `8eedfae073f756d0c70a893b477cf1c19996e467a9e9e3d4bacb116cc20d4c4c` | `a5480fdfe33c3618aeea345899b98cfad259001576069e9f3721ce01add5d0d3` | MISMATCH |
| `v7-audit-log` | `c2a524d4b5b2023dfd3a2923c1f3148ad647853fd00e50454d3cd7095d3f0a86` | `c2a524d4b5b2023dfd3a2923c1f3148ad647853fd00e50454d3cd7095d3f0a86` | MATCH |
| `v7-admin-api` | `acbdce035c6f33ad28bd40abb8b76ac1887db9e57f87d696eae98633d760345a` | `8da1e5479723891f8619bbf5296239afb7e41d27f456b9601bd9799d289b705e` | MISMATCH |

## Runtime provenance

Closest production provenance source:

- `/opt/v7/ops/deploy-a-v7-next-12e51a5-20260601T093725Z/deploy-metadata.env`

Discovered values:

- `deploy_id=deploy-a-v7-next-12e51a5-20260601T093725Z`
- `commit=12e51a5ad4a6c34b09e37c9343d7ee78cb7678d6`
- `package_sha=40e92c43631a0e589cbdd790b938325252f105e6fe98b196b33b013b5274bfc5`

This proves runtime provenance is known enough to classify divergence, but not aligned enough to continue.

## Scheduler truth

Autoswitch service and timer exist but are inactive. Root crontab and cron directories did not reveal an alternate autoswitch scheduler. Running V7 loops maintain benchmark/state files but do not launch autoswitch.

Therefore the runtime cycle starter is not active. This blocks Z9.

## Store truth

Available:

- Runtime state root
- Audit root
- Event root
- Admin state root
- Restore barrier file

Missing:

- Closure store
- Execution contract store
- Execution event store
- Selected move stores

This blocks Z9 because operation completion and closure cannot be validated on production.

## Truth-check update

`v7-truth-check` was updated to recognize copied-binary deployment metadata as a runtime identity source. The change does not weaken fail-closed behavior. It converts the former unknown runtime branch/commit into explicit blockers when the deploy branch, deploy commit or binary hashes do not match the authoritative branch.

Expected Z8.10 all-mode blockers now include:

- `runtime_branch_mismatch`
- `runtime_local_commit_mismatch`
- `binary_hash_mismatch`
- `autoswitch_scheduler_inactive`
- `closure_path_available_false_or_unknown`
- `operation_wiring_present_false_or_unknown`

## Remediation plan

1. Approve a bounded production convergence remediation window.
2. Back up current `/usr/local/bin/v7-users-autoswitch`, `/usr/local/bin/v7-admin-api` and `/usr/local/bin/v7-audit-log`.
3. Deploy authoritative `Updatesystem` binaries to production using a reversible copied-binary deployment.
4. Create a runtime deploy manifest or linkage manifest that records branch, commit, package hash, binary hashes, deploy id, backup path and timestamp.
5. Decide whether autoswitch is timer-driven or approved manual mode.
6. If timer-driven, restore timer activity only after binary convergence and governance review.
7. Create missing empty closure/execution stores only after schema, ownership and permissions are confirmed.
8. Run `v7-truth-check --local`, `--github` and `--all`.
9. Retry Z9 only after full PASS.

## Final verdicts

root_cause_found=true

runtime_root_identified=true

production_binary_hash_known=true

production_binary_matches_authoritative_commit=false

runtime_provenance_known=true

scheduler_truth_known=true

service_inactive_explained=true

closure_store_status_known=true

execution_store_status_known=true

operation_wiring_confirmed_on_runtime=false

safe_remediation_performed=false

truth_check_updated=true

truth_check_all_pass=false

safe_to_retry_Z9=false

