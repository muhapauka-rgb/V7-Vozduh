# PROGRAM POOL PREPARATION GOVERNANCE CAPACITY SYNTHETIC USERS AND EXECUTION STRATEGY REPORT

Project: V7 Vozduh
Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`
Report time: 2026-06-07

## Mission Result

POOL preparation can begin.

The platform did not have enough planner-visible users for a POOL-sized cohort at the start of this program. The current POOL target budget is `25`, but production had only `18` active routing/planner-visible users.

The gap was closed by creating exactly `7` controlled synthetic users through the existing production owner:

`/usr/local/bin/v7-user-create-from-ipam --apply --confirm CREATE_IPAM_USER`

No POOL execution was performed. No autoswitch apply was run. No users were moved. No authority was promoted. No autonomy was enabled. No new planner, governance path, execution path, or truth source was created.

## Phase 1 - Production Truth

Evidence:

- `pool_preparation_governance_capacity_evidence/phase1_truth_check.json`
- `pool_preparation_governance_capacity_evidence/phase1_convergence_status.json`

Result:

- Truth check: `PASS`
- Truth blockers: `[]`
- Convergence: `ALIGNED`
- Runtime action safe: `true`

Final post-synthetic checks:

- `pool_preparation_governance_capacity_evidence/phase12_truth_check_after_synthetic.json`
- `pool_preparation_governance_capacity_evidence/phase12_convergence_status_after_synthetic.json`

Final result:

- Truth check: `PASS`
- Convergence: `ALIGNED`
- Runtime action safe: `true`

## Phase 2 - POOL User Base Audit

Evidence:

- `pool_preparation_governance_capacity_evidence/phase2_users.registry`
- `pool_preparation_governance_capacity_evidence/phase2_best_available_pool.json`
- `pool_preparation_governance_capacity_evidence/phase2_candidate_suitability_summary.json`
- `pool_preparation_governance_capacity_evidence/phase2_pool_user_base_audit.json`

Initial state:

- Total users: `19`
- Active users: `18`
- Routing users: `18`
- Planner-visible users: `18`
- Eligible users: `18`

## Phase 3 - POOL Capacity Gap

Evidence:

- `pool_preparation_governance_capacity_evidence/phase3_pool_capacity_gap_report.json`

Result:

- POOL target budget: `25`
- Required user count: `25`
- Current planner/routing user count: `18`
- Capacity gap: `7`
- Synthetic users required: `true`

## Phase 4 - Synthetic User Discovery

Discovered existing owners:

- Admin API: `/api/actions/user-create-from-ipam`
- Production CLI owner: `/usr/local/bin/v7-user-create-from-ipam`
- IPAM allocation owner: `/usr/local/bin/v7-ipam-allocate`
- Registry owner: `/opt/v7/egress/state/users.registry`
- Lease owner: `/opt/v7/ipam/leases.registry`
- Runtime visibility owner: `v7-intelligence-snapshot-refresh`
- Planner visibility owner: `v7-users-autoswitch`

The canonical creation owner is `v7-user-create-from-ipam`.

This owner:

- reserves the next IPAM lease,
- creates the WireGuard client through `v7-user-create`,
- writes the user row into `users.registry`,
- creates config/QR artifacts,
- verifies route visibility,
- leaves future routing under V7.

No direct registry editing was used.

## Phase 5 - Synthetic User Policy

Policy decision:

- Current users were below POOL budget.
- Required synthetic users: `7`
- Create only the minimum required.
- Use existing owners only.
- Place synthetic users on `vless`, because this makes them routing/planner visible without moving existing users.
- Do not fake planner, routing, governance, feedback, or rollback paths.

Dry-run evidence:

- `pool_preparation_governance_capacity_evidence/phase6_synthetic_user_dry_runs.txt`

Dry-run result:

- `V7_USER_CREATE_FROM_IPAM=DRY_RUN_OK`
- Next IP before creation: `10.7.0.18`
- Next table before creation: `1016`
- Live changes: `NO`

## Phase 6 - Controlled Synthetic User Creation

Creation evidence:

- `pool_preparation_governance_capacity_evidence/phase6_synthetic_user_creation.txt`
- `pool_preparation_governance_capacity_evidence/phase6_users_before_synthetic.registry`
- `pool_preparation_governance_capacity_evidence/phase6_users_after_synthetic.registry`
- `pool_preparation_governance_capacity_evidence/phase6_synthetic_user_creation_summary.json`

Created users:

| User | Egress | Table | Route |
|---|---|---:|---|
| `10.7.0.18` | `vless` | `1016` | `tun0` |
| `10.7.0.19` | `vless` | `1017` | `tun0` |
| `10.7.0.20` | `vless` | `1018` | `tun0` |
| `10.7.0.21` | `vless` | `1019` | `tun0` |
| `10.7.0.22` | `vless` | `1020` | `tun0` |
| `10.7.0.23` | `vless` | `1021` | `tun0` |
| `10.7.0.24` | `vless` | `1022` | `tun0` |

Visibility evidence:

- `pool_preparation_governance_capacity_evidence/phase6_synthetic_route_visibility.txt`
- `pool_preparation_governance_capacity_evidence/phase6_synthetic_route_visibility_summary.json`
- `pool_preparation_governance_capacity_evidence/phase6_snapshot_refresh_after_synthetic.json`
- `pool_preparation_governance_capacity_evidence/phase6_planner_dry_run_after_synthetic.json`
- `pool_preparation_governance_capacity_evidence/phase6_synthetic_user_visibility_summary.json`

Post-creation state:

- Total users: `26`
- Active users: `25`
- Routing users: `25`
- Planner-visible users: `25`
- Candidate snapshot item count: `25`
- Capacity gap after creation: `0`
- Snapshot stop required: `false`
- Source mismatch families: `[]`

Note:

`v7-user-create-from-ipam` uses `--apply --confirm CREATE_IPAM_USER` for creation. This was user provisioning, not POOL execution and not autoswitch apply. `v7-users-autoswitch --apply` was not run.

## Phase 7 - POOL Governance Model

POOL execution requires:

- Certified `LARGE_BATCH` evidence.
- POOL preparation evidence with 25 planner-visible/routing-visible users.
- Fresh truth check: `PASS`.
- Fresh convergence: `ALIGNED`.
- Clean snapshot gate.
- Explicit operator approval for POOL authority promotion.
- Fresh POOL approval packet.
- Rollback manifest covering the exact selected users.
- Restore barrier written through the canonical owner.
- Dry-run recheck after restore barrier clearance.
- No embedded multi-user pre-planner-refresh write during apply.

POOL must remain non-autonomous. Operator approval remains mandatory.

## Phase 8 - POOL Execution Strategy

Recommended strategy: batched execution, not 25 users at once.

Safest model:

`10 + 10 + 5`

Why:

- The system has already certified 10-user `LARGE_BATCH`.
- `10 + 10 + 5` reuses the proven blast-radius step.
- Each batch can have its own packet, rollback manifest, restore barrier, apply, verify, and feedback closure.
- It avoids turning the first POOL execution into a single 25-user blast-radius jump.

Rejected for first POOL:

- `25 at once`: too large for first POOL execution.
- `5 + 5 + 5 + 5 + 5`: safe but too operationally slow and does not test POOL efficiently.
- Fully dynamic batches: useful later, but should not be introduced during first POOL certification.

## Phase 9 - POOL Rollback Model

Rollback scope:

- Per batch, not full 25 at once.
- Each batch must have an exact rollback manifest.
- Rollback target is the pre-batch source egress for each user.

Rollback speed:

- Must be measured during POOL preparation dry-runs.
- Verification must run after each rollback-capable apply.

Rollback blast radius:

- First POOL execution should cap rollback blast radius to the active batch.
- If batch 1 fails, stop before batch 2.
- If batch 2 fails, do not execute batch 3.

Rollback verification:

- registry current egress,
- route table default dev,
- `ip route get` for each user,
- feedback records with rollback status if needed.

## Phase 10 - POOL Capacity Model

Evidence:

- `pool_preparation_governance_capacity_evidence/phase10_pool_capacity_model.json`
- `pool_preparation_governance_capacity_evidence/phase10_egress_load_after_synthetic.json`
- `pool_preparation_governance_capacity_evidence/phase10_channel_service_scores_after_synthetic.json`

Post-synthetic load:

- Active users: `25`
- Healthy channels: `3`
- Working channels: `2`
- Average load: `12.5`
- Soft limit: `15`
- Hard limit: `19`
- Failover hard limit: `25`
- Load status: `ok`

Production eligible channels:

- `vless`: 9 users, service `OK`, load `OK`
- `awg0`: 8 users, service `OK`, load `OK`
- `awg3`: 8 users, service `OK`, load `OK`

Healthy reserved channels:

- `wireguard-1779454504-c43409`
- `amneziawg-exec-20260528-10-8-1-14`

Low-service-score channels:

- `1`
- `openvpn-1779388847-d2ad7c`

Capacity interpretation:

The platform has enough users to exercise POOL-sized cohorts. The current production-eligible channel pool is healthy but narrow. Reserved healthy channels must not be counted for POOL execution unless a future governance program explicitly releases them.

## Phase 11 - POOL Packet Model

Recommended packet model:

- One POOL parent preparation review.
- Three child execution packets: `10`, `10`, `5`.
- Each child packet has:
  - selected users,
  - exact source/target egress,
  - selected move hash,
  - rollback manifest,
  - approved plan lock,
  - restore barrier,
  - final dry-run recheck,
  - verification checklist,
  - feedback closure requirement.

Restore barrier:

- Must be fresh per child packet.
- Must expire quickly enough to prevent stale execution.
- Must bind to the exact selected move hash and snapshot bundle.

Approved plan lock:

- Must match selected users and targets.
- Must fail closed on target drift, user replacement, snapshot mismatch, or expired generation.

## Phase 12 - POOL Execution Loop Review

Current loop:

planner -> packet -> restore barrier -> approved plan lock -> apply -> verify -> feedback

Verdict:

The loop can support POOL preparation.

Required missing piece before execution:

- POOL authority is not promoted yet, by design.
- A future program must promote authority only after reviewing this preparation evidence.
- A future program must generate a real POOL packet model from a fresh planner result.

Important rule:

Do not run multi-user apply with embedded `--pre-planner-refresh write`. Refresh snapshots separately, then dry-run recheck, then execute only under a fresh approved packet and restore barrier.

## Phase 13 - Readiness Decision

Decision:

`POOL_READY_FOR_EXECUTION_PREPARATION`

Reason:

- The user base gap was proven and closed.
- 25 active routing/planner-visible users now exist.
- POOL governance requirements are defined.
- POOL execution strategy is defined.
- POOL rollback model is defined.
- POOL capacity model is defined.
- POOL packet model is defined.
- Truth and convergence are clean after synthetic user creation.

## Final Verdicts

current_user_count=25

pool_budget=25

synthetic_users_required=true

synthetic_users_created=7

pool_governance_defined=true

pool_execution_strategy_defined=true

pool_rollback_model_defined=true

pool_capacity_model_defined=true

pool_packet_model_defined=true

pool_execution_loop_ready=true

pool_ready_for_execution_preparation=true

single_blocker=NONE

users_moved=0

apply_executed=false

authority_promoted=false

SAFE_NEXT_STEP=PROGRAM_POOL_AUTHORITY_PROMOTION_AND_BATCHED_PACKET_PREPARATION_REVIEW

## Operator Conclusion

The platform is now ready to prepare POOL execution.

It is not ready to execute POOL in this program. The correct next step is a POOL authority promotion and batched packet preparation review. The recommended first POOL strategy is `10 + 10 + 5`, with separate packet, restore barrier, verification, rollback scope, and feedback closure for each batch.
