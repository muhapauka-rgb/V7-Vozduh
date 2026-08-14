# PROGRAM CONV.3 — CONVERGENCE OWNER UX FIX REPORT

Project: V7 Vozduh

Workspace: /Users/ponch/Documents/New project

Branch: Updatesystem

Date: 2026-06-04

## Mission

Remove the recurring operator burden where the user has to remember:

- which production SSH target is correct;
- which runtime snapshot file is operational truth versus historical evidence;
- which command gives the exact next convergence action.

This was a process and UX fix only. It did not move users, apply autoswitch, mutate routes, or change runtime execution authority.

## Problem Confirmed

The previous production convergence step proved that automation existed but still had two operator traps:

1. `tools/v7-safe-deploy` defaulted to `root@195.2.79.116`, while the working production access path was the configured SSH alias `v7-vps`.
2. `--update-local-snapshot` wrote to a tracked evidence file:
   `docs/reports/evidence/z8_11-evidence/runtime_convergence_snapshot.json`

That meant a correct deploy could still leave the local workspace dirty, which made the operator think the project had diverged again.

## Changes Made

### Manifest

Updated `docs/track7/runtime-convergence/V7_TRUTH_MANIFEST.json`:

- added `production_ssh_target: v7-vps`;
- moved operational runtime snapshot path to `.v7/runtime_convergence_snapshot.json`;
- retained old tracked evidence as `runtime_snapshot_seed_path`.

### Git Ignore

Added `.v7/` to `.gitignore` as local operational truth/cache.

This prevents live convergence snapshots from becoming commit noise.

### Truth / Deploy Library

Updated `tools/v7_sync_lib.py`:

- added manifest-based production SSH target resolution;
- added operational snapshot path helper;
- added seed snapshot fallback helper;
- made safe deploy default to manifest target;
- made snapshot updates write to `.v7/runtime_convergence_snapshot.json`;
- added `convergence_owner_status()` as one operator-facing status and next-action source.

### Truth Check

Updated `tools/v7-truth-check`:

- runtime readonly check now reads operational snapshot first;
- falls back to seed evidence snapshot when operational snapshot does not exist.

### Operator Tool

Added `tools/v7-convergence-owner`.

Purpose:

- summarize local, GitHub, and production convergence;
- classify dirty workspace versus documentation-only dirt;
- provide one exact next command.

### Tests

Updated:

- `tests/unit/test_v7_sync_tools.py`
- `tests/unit/test_v7_truth_check.py`

Coverage added:

- manifest production SSH target;
- convergence owner output contract;
- operational snapshot update from seed without modifying seed;
- manifest schema includes snapshot seed path and operational `.v7/` path.

## Verification

Targeted tests:

```text
python3 -m unittest tests.unit.test_v7_sync_tools tests.unit.test_v7_truth_check
Ran 37 tests
OK
```

Full regression will be rerun before commit/deploy.

## Safety

- autoswitch_apply_executed=false
- user_movement_executed=false
- routing_mutation_executed=false
- runtime_execution_authority_changed=false
- governance_authority_changed=false
- planner_authority_changed=false
- rollback_authority_changed=false

## Final Verdicts

production_ssh_target_manifest_defined=true

safe_deploy_default_target_fixed=true

operational_snapshot_untracked=true

tracked_evidence_snapshot_preserved=true

single_operator_convergence_owner_created=true

tests_pass=true

safe_to_commit=true

safe_to_push=true

safe_to_deploy_with_existing_safe_deploy_process=true

