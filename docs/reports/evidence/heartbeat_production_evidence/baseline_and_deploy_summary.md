# Heartbeat Production Baseline And Deploy Summary

Program: PROGRAM_HEARTBEAT_PRODUCTION_MATERIALIZATION_AND_OPERATOR_VISIBLE_CERTIFICATION
Date: 2026-06-04
Workspace: /Users/ponch/Documents/New project
Branch: Updatesystem

## Baseline

- Initial local branch state: Updatesystem was ahead of origin/Updatesystem by 2 commits.
- Baseline heartbeat certification commits already present locally:
  - ccb4e3c PROGRAM runtime heartbeat refresh cadence certification
  - 9c408ae PROGRAM V7 runtime nervous system policy certification
- Pre-deploy truth check before materialization:
  - local commit: ccb4e3cd76c376923de76f1e12f2a0d54fa2c7c4
  - production commit: 4905000...
  - verdict: NO-GO / runtime_local_commit_mismatch

## Push And First Safe Deploy

- Pushed Updatesystem to origin.
- Safe deploy applied ccb4e3cd76c376923de76f1e12f2a0d54fa2c7c4.
- Deploy id: deploy-z8-14-Updatesystem-ccb4e3c-20260604T180018
- Safety flags from deploy:
  - autoswitch_apply_executed=false
  - user_movement_executed=false
  - routing_mutation_executed=false

## Closure Discovered During Verification

The first deploy materialized binaries but did not update the production planner service ExecStart.

Production still had:

```text
/usr/local/bin/v7-users-autoswitch
```

Expected heartbeat ExecStart:

```text
/usr/local/bin/v7-users-autoswitch --pre-planner-refresh=write --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh
```

Existing broad installer was rejected because it can install/enable movement-capable autoswitch units. The closure reused the existing safe deploy path instead.

## Closure Commit

- Commit: 6bf4fdf PROGRAM heartbeat planner service safe deploy closure
- Changes:
  - Added systemd/drafts/v7-autoswitch-planner.service to safe deploy allowlist.
  - Added planner service/timer to runtime fingerprint.
  - Added safe deploy daemon-reload when /etc/systemd/system files change.
  - Added tests for allowlist and runtime fingerprint coverage.

## Second Safe Deploy

- Safe deploy applied 6bf4fdfb76d47985e0cf683aa4e5b04c10fd60a8.
- Deploy id: deploy-z8-14-Updatesystem-6bf4fdf-20260604T180350
- Safety flags from deploy:
  - autoswitch_apply_executed=false
  - user_movement_executed=false
  - routing_mutation_executed=false

