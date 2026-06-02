# Z8.7 Evidence 02 - V7 Truth Manifest Design

## Manifest Name

```text
V7_TRUTH_MANIFEST
```

## Manifest Format

```json
{
  "schema": "v7-truth-manifest/v1",
  "project": "V7 Vozduh",
  "canonical_workspace": "/Users/ponch/Documents/New project",
  "canonical_branch": "Updatesystem",
  "canonical_remote": "https://github.com/muhapauka-rgb/V7-Vozduh.git",
  "canonical_commit_policy": "must_match_github_canonical_branch_before_deploy",
  "runtime_root": "/opt/v7",
  "runtime_release_root": "/opt/v7/releases",
  "runtime_current_release": "/opt/v7/releases/current",
  "runtime_deploy_manifest": "/opt/v7/deploy-manifest.json",
  "state_root": "/opt/v7/egress/state",
  "event_root": "/opt/v7/events",
  "audit_root": "/opt/v7/audit",
  "admin_root": "/opt/v7/admin",
  "expected_services": [
    "v7-users-autoswitch.service",
    "v7-users-autoswitch.timer"
  ],
  "expected_binaries": [
    "/usr/local/bin/v7-users-autoswitch",
    "/usr/local/bin/v7-audit-log"
  ],
  "expected_truth_checks": [
    "workspace_path",
    "workspace_branch",
    "workspace_commit",
    "workspace_clean_or_scoped",
    "github_branch_commit",
    "runtime_branch",
    "runtime_commit",
    "runtime_binary_hashes",
    "service_status",
    "state_freshness",
    "restore_barrier_state",
    "audit_availability",
    "closure_availability"
  ],
  "expected_runtime_checks": [
    "hostname",
    "date",
    "runtime_root_exists",
    "autoswitch_binary_executable",
    "audit_binary_executable",
    "autoswitch_service_status",
    "autoswitch_timer_status",
    "autoswitch_dry_run_output_schema"
  ],
  "unknown_means": "NO_GO",
  "generated_by": "PROGRAM_Z8_7"
}
```

## Manifest Placement Decision

Design target:

```text
docs/track7/runtime-convergence/V7_TRUTH_MANIFEST.json
```

No file was implemented in this block.
