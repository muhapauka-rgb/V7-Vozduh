# Program A.D Release And Readiness Summary

Date: 2026-06-03 local / 2026-06-02 UTC

## Source / GitHub

- authoritative workspace: `/Users/ponch/Documents/New project`
- authoritative branch: `Updatesystem`
- A.C release commit: `9d2ab0bf7c17ce0eec767bd3f182dea3d3192d2e`
- safe deploy payload streaming fix commit: `25fc8d251fd1b9eb4302edaac1ec93e1ba75f597`
- GitHub `Updatesystem`: `25fc8d251fd1b9eb4302edaac1ec93e1ba75f597`

## Safe Deploy

Applied through `v7-safe-deploy` using `V7_PROD_SSH_TARGET=v7-vps`.

- deploy id: `deploy-z8-14-Updatesystem-25fc8d2-20260603T000215`
- autoswitch apply: false
- user movement: false
- routing mutation: false
- service restart: false
- restore barrier modified: false

Production hashes after deploy:

- `/usr/local/bin/v7-users-autoswitch`: `20d916a4a98051bf0c2f3cf7ba7e97882cab7ff64688d4f2c9d286cb6db43ad6`
- `/usr/local/bin/v7-audit-log`: `c2a524d4b5b2023dfd3a2923c1f3148ad647853fd00e50454d3cd7095d3f0a86`
- `/usr/local/bin/v7-admin-api`: `8da1e5479723891f8619bbf5296239afb7e41d27f456b9601bd9799d289b705e`

Post-deploy manifests:

- `/opt/v7/deploy-manifest.json`: commit `25fc8d251fd1b9eb4302edaac1ec93e1ba75f597`
- `/opt/v7/runtime-linkage.json`: commit `25fc8d251fd1b9eb4302edaac1ec93e1ba75f597`
- `/opt/v7/releases/current/release-manifest.json`: commit `25fc8d251fd1b9eb4302edaac1ec93e1ba75f597`

## Truth Check

Post-deploy `tools/v7-truth-check --all`:

- runtime_access_status=`READY`
- runtime_truth_status=`KNOWN`
- state_truth_status=`KNOWN`
- convergence_status=`FULLY_ALIGNED`
- final_verdict=`PASS`
- warning=`documentation_dirty_ignored`

## Production Dry-Run

Evidence:

- `program_ad_evidence/production_planner_dry_run.json`
- `program_ad_evidence/production_one_user_dry_run.json`

Full production planner dry-run:

- users_total=18
- egress_total=7
- healthy_egress_total=1
- candidate_moves_total=15
- selected_moves=0
- terminal_reason=`dry_run_restore_barrier_clearance_selected_moves_exceed_budget`

One-user production dry-run for `10.0.0.2`:

- current_egress=`awg3`
- recommended_egress=`vless`
- candidate_moves_total=1
- selected_moves=0
- terminal_reason=`dry_run_restore_barrier_clearance_generation_expired`
- planner_generation_id=`90fe14fa976a3c10e202ceae9b2b19241639eae22e9896ba2998bbfeed28ff90`

Candidate validation:

- service-aware policy active: `vless` service score `100.0`
- best available pool active: `vless` is `best_available_pool_member`, pool rank `1`
- capacity-aware selection active: `vless` capacity decision `capacity_available`, projected load users `3`, soft limit `21`, hard limit `27`
- unsafe channels remain blocked: `1` and `openvpn` blocked by health/severity/service/route-class failures
- reserved channels remain blocked: execution AWG blocked by `manual_only`, `reserve_only`, `canary_reserved_production_assignment_blocked`; WireGuard blocked by `canary_reserved_production_assignment_blocked`

## Exact External Blocker

`restore_barrier_clearance_generation_expired`

Details:

- restore barrier clearance expected selected moves: `1`
- one-user dry-run selected moves before guard: `1`
- budget exceeded: `false`
- approved generation id: `c4a2bfa3637a1cd69ecab5ec10b0cf4da4be16aece95630c7a2161eeaffff2d8`
- current planner generation id: `90fe14fa976a3c10e202ceae9b2b19241639eae22e9896ba2998bbfeed28ff90`
- clearance expires at: `2026-06-01T18:02:59.305408+00:00`
- guard reason: `restore_barrier_clearance_generation_expired`

This is an external governance/restore-barrier freshness blocker. A.D safety rules forbid restore barrier bypass/modification, so it was not changed.
