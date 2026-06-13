# PROGRAM BA.4 - Ten User Autonomy Certification Report

Date: 2026-06-13
Project: V7 Vozduh
Branch: Updatesystem
Evidence: `BA4_EVIDENCE/`

## 1. Executive Summary

BA.4 certified autonomous execution for 10 real planner-selected users.

Final verdict:

`TEN_USER_AUTONOMY_CERTIFIED`

The run reused the existing certified path:

Observe -> fresh planner -> fresh packet -> restore barrier -> post-clearance dry-run -> autonomous apply -> verify -> rollback readiness -> feedback -> trust/prediction/recommendation update -> planner reuse.

No new planner, governance owner, execution path, or truth source was created.

## 2. Truth Gate

Initial gate evidence:

- `BA4_EVIDENCE/phase1/truth_check.json`
- `BA4_EVIDENCE/phase1/convergence_status.json`
- `BA4_EVIDENCE/phase1/github_ls_remote_updatesystem.txt`

Final gate evidence:

- `BA4_EVIDENCE/final/truth_check_after_ba4.json`
- `BA4_EVIDENCE/final/convergence_status_after_ba4.json`
- `BA4_EVIDENCE/final/github_ls_remote_updatesystem_after_ba4.txt`

Final truth:

- truth-check: `PASS`
- convergence: `FULLY_ALIGNED`
- convergence-status: `ALIGNED`
- runtime access: `READY`
- blockers: `[]`

## 3. Policy Escalation

Canonical owner:

- Admin API: `/api/actions/policy-update`
- Policy file: `/etc/v7/policy.json`
- Runtime consumer: `v7-users-autoswitch`

Policy update:

- `autoswitch_max_planned_per_run`: `5 -> 10`
- users moved during policy update: `0`
- routing changed during policy update: `false`

Evidence:

- `BA4_EVIDENCE/phase2/policy_before.json`
- `BA4_EVIDENCE/phase2/policy_update_patch.json`
- `BA4_EVIDENCE/phase2/policy_update_response.json`
- `BA4_EVIDENCE/phase2/policy_after.json`
- `BA4_EVIDENCE/phase2/policy_update_summary.json`

## 4. Fresh Planner

Command path:

`v7-users-autoswitch --pre-planner-refresh write --pre-planner-refresh-command v7-intelligence-snapshot-refresh --max-selected-moves 10 --pretty`

Planner result:

- users total: `26`
- egress total: `7`
- healthy egress total: `3`
- candidate moves total: `20`
- selected moves before gate: `10`
- selected moves after authority gate: `10`
- authority class: `POOL`
- authority budget: `25`
- snapshot stop required: `false`
- source mismatch families: `[]`
- pre-planner refresh: `REFRESH_SUCCESS`

Evidence:

- `BA4_EVIDENCE/phase3/fresh_planner.json`
- `BA4_EVIDENCE/phase3/fresh_planner_remote.json`
- `BA4_EVIDENCE/phase3/fresh_planner_summary.json`

## 5. Fresh Packet

Packet owner:

- `v7-operator-execution-packet`

Packet:

- packet id: `pkt_bfb877957fd610d73bf451e3`
- runtime action: `CREATE_RESTORE_BARRIER_CLEARANCE`
- rollback manifest: present
- allowed user count: `10`
- allowed targets: `awg3`, `wireguard-1779454504-c43409`

Approved users:

| User | Approved Target |
|---|---|
| `10.7.0.6` | `wireguard-1779454504-c43409` |
| `10.7.0.8` | `awg3` |
| `10.7.0.9` | `wireguard-1779454504-c43409` |
| `10.7.0.10` | `awg3` |
| `10.7.0.11` | `wireguard-1779454504-c43409` |
| `10.7.0.12` | `awg3` |
| `10.7.0.13` | `wireguard-1779454504-c43409` |
| `10.7.0.14` | `awg3` |
| `10.7.0.15` | `wireguard-1779454504-c43409` |
| `10.7.0.16` | `awg3` |

Evidence:

- `BA4_EVIDENCE/phase4/packet_generate.json`
- `BA4_EVIDENCE/phase4/ba4_packet.json`
- `BA4_EVIDENCE/phase4/packet_and_plan_summary.json`

## 6. Fresh Restore Barrier

The first restore-barrier attempt correctly failed closed with:

`DENY_RUNTIME_PLAN_MISSING`

The same packet could not be replayed and was correctly blocked with:

`DENY_REPLAY`

A new fresh planner and packet were generated, then restore barrier was written with explicit planner snapshot binding.

Final restore-barrier result:

- recheck verdict: `ALLOW_RESTORE_BARRIER_CLEARANCE`
- clearance verdict: `RESTORE_BARRIER_CLEARANCE_WRITTEN`
- restore barrier file: `/opt/v7/egress/state/autoswitch-restore-barrier.json`
- users moved during restore-barrier phase: `0`

Evidence:

- `BA4_EVIDENCE/phase5/restore_barrier.json`
- `BA4_EVIDENCE/phase5/restore_barrier_with_snapshot.json`
- `BA4_EVIDENCE/phase5/restore_barrier_retry.json`
- `BA4_EVIDENCE/phase5/restore_barrier_retry_summary.json`

## 7. Post-Clearance Dry Run

Dry-run result:

- terminal state: `DRY_RUN`
- terminal reason: `dry_run_selected_moves_available`
- selected moves: `10`
- selected users matched approved lock: `true`
- snapshot stop required: `false`
- source mismatch families: `[]`
- approved plan lock valid: `true`
- atomic condition: `ENVELOPE_VALID`
- atomic mismatches: `[]`
- apply present: `false`

Evidence:

- `BA4_EVIDENCE/phase6/post_clearance_dry_run.json`
- `BA4_EVIDENCE/phase6/post_clearance_dry_run_summary.json`

## 8. Autonomous Execution

Execution command:

`v7-users-autoswitch --pre-planner-refresh write --pre-planner-refresh-command v7-intelligence-snapshot-refresh --allow-pre-planner-refresh-with-apply --max-selected-moves 10 --apply --verify --pretty`

Execution result:

- operation id: `runtime_autoswitch_031937d65d1a2048d3c7f276`
- selected move hash: `d1b28e651e46bd59fcf3cec8ce210a6edde7ce814ee3930e6069ca924ee7c5d1`
- selected moves: `10`
- users moved: `10`
- apply applied: `true`
- all switch return codes: `0`
- all verify return codes: `0`
- rollback attempted: `false`
- snapshot stop required: `false`
- source mismatch families: `[]`
- atomic condition: `ENVELOPE_VALID`

Moved users:

| User | From | To | Verify |
|---|---|---|---|
| `10.7.0.6` | `vless` | `wireguard-1779454504-c43409` | PASS |
| `10.7.0.8` | `vless` | `awg3` | PASS |
| `10.7.0.9` | `vless` | `wireguard-1779454504-c43409` | PASS |
| `10.7.0.10` | `vless` | `awg3` | PASS |
| `10.7.0.11` | `vless` | `wireguard-1779454504-c43409` | PASS |
| `10.7.0.12` | `vless` | `awg3` | PASS |
| `10.7.0.13` | `vless` | `wireguard-1779454504-c43409` | PASS |
| `10.7.0.14` | `vless` | `awg3` | PASS |
| `10.7.0.15` | `vless` | `wireguard-1779454504-c43409` | PASS |
| `10.7.0.16` | `vless` | `awg3` | PASS |

Evidence:

- `BA4_EVIDENCE/phase7/ten_user_apply.json`
- `BA4_EVIDENCE/phase7/ten_user_apply_summary.json`

## 9. Post Execution Review

Canonical runtime registry confirmed the moved users:

- `10.7.0.6`: `wireguard-1779454504-c43409`
- `10.7.0.8`: `awg3`
- `10.7.0.9`: `wireguard-1779454504-c43409`
- `10.7.0.10`: `awg3`
- `10.7.0.11`: `wireguard-1779454504-c43409`
- `10.7.0.12`: `awg3`
- `10.7.0.13`: `wireguard-1779454504-c43409`
- `10.7.0.14`: `awg3`
- `10.7.0.15`: `wireguard-1779454504-c43409`
- `10.7.0.16`: `awg3`

Admin API note:

The first non-forced `/api/overview` read returned stale cached values. A forced refresh via `/api/overview?force=1` matched canonical runtime registry.

Evidence:

- `BA4_EVIDENCE/phase8/users_registry_post_apply.txt`
- `BA4_EVIDENCE/phase8/admin_api_post_apply_users.json`
- `BA4_EVIDENCE/phase8/admin_api_force_overview_post_apply_users.json`

## 10. Rollback Readiness

Rollback result:

- rollback packet id: `rbpkt_b5c40611f0fe46737137fc88`
- rollback items: `10`
- max rollback users: `10`
- rollback target: `vless`
- rollback apply requested: `false`
- rollback applied: `false`
- rollback dry-run reason: `dry_run`
- rollback packet valid: `true`

Evidence:

- `BA4_EVIDENCE/phase8/rollback_packet.json`
- `BA4_EVIDENCE/phase8/rollback_packet_remote_objects.json`
- `BA4_EVIDENCE/phase8/rollback_packet_dry_run_summary.json`

## 11. Feedback And Learning Loop

Feedback materialization:

- requested: `10`
- materialized: `10`
- trust feedback updated: `true`
- prediction feedback updated: `true`
- recommendation feedback updated: `true`
- errors: `[]`

Snapshot refresh after feedback:

- snapshot count: `11`
- source stable: `true`
- warnings: `[]`
- runtime behavior changed: `false`

Planner reuse:

- planner consumed execution feedback inputs:
  - `/opt/v7/egress/state/execution-events.jsonl`
  - `/opt/v7/egress/state/runtime-trust.jsonl`
  - `/opt/v7/egress/state/proposal-records.jsonl`
  - `/opt/v7/egress/state/proposals.jsonl`
  - `/opt/v7/egress/state/closure-records.jsonl`
- trust evolution snapshot present: `true`
- prediction snapshot present: `true`
- recommendation inputs present: `true`
- source mismatch families: `[]`

Evidence:

- `BA4_EVIDENCE/phase8/feedback_materialization_summary.json`
- `BA4_EVIDENCE/phase8/snapshot_refresh_after_feedback.json`
- `BA4_EVIDENCE/phase8/planner_reuse_after_feedback.json`
- `BA4_EVIDENCE/phase8/planner_reuse_after_feedback_summary.json`

## 12. Blast Radius Review

| Check | Result |
|---|---|
| Maximum scope | 10 users |
| Actual users moved | 10 |
| Only approved users moved | true |
| Only approved targets used | true |
| User substitution | false |
| Target substitution | false |
| Planner bypass | false |
| Governance bypass | false |
| Restore barrier bypass | false |
| Atomic envelope bypass | false |
| Verification failures | 0 |
| Rollback required | false |
| Rollback readiness | true |

## 13. Final Verdict

`TEN_USER_AUTONOMY_CERTIFIED`

Final verdicts:

- ten_user_autonomy_certified: `true`
- users_moved: `10`
- only_approved_users_moved: `true`
- only_approved_targets_used: `true`
- verification_passed: `true`
- rollback_required: `false`
- rollback_readiness_passed: `true`
- feedback_materialized: `true`
- trust_updated: `true`
- prediction_updated: `true`
- recommendation_updated: `true`
- planner_reuse_passed: `true`
- truth_check_pass: `true`
- convergence_aligned: `true`
- safe_next_step: `BA5_POOL_SCALE_AUTONOMY_REVIEW_OR_AUTONOMY_STABILITY_WINDOW`

