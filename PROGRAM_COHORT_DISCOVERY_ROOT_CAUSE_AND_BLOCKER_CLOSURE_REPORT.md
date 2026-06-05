# PROGRAM COHORT DISCOVERY ROOT CAUSE AND BLOCKER CLOSURE REPORT

Project: V7 Vozduh
Workspace: /Users/ponch/Documents/New project
Branch: Updatesystem
Generated: 2026-06-05
Evidence folder: cohort_discovery_evidence/

## Mission

The previous real small batch certification stopped with:

- healthy_egress_total=0
- candidate_moves=0
- selected_moves=0

This program traces the planner chain to determine why candidate generation was zero and whether the blocker is now closed.

No autonomy was enabled. No users were moved. No `--apply` was run. No routing, governance, planner ownership, execution ownership, truth source, or snapshot root was changed.

## Executive Verdict

Outcome A is achieved for candidate generation.

The original `candidate_moves=0` condition no longer reproduces on production after a fresh pre-planner refresh. The current production planner produces:

- healthy_egress_total=1
- candidate_moves=14
- candidate_moves_total=14
- selected_moves=0

The root cause of the old zero-candidate condition was channel eligibility state, specifically that no failover target was eligible at that moment. In the old evidence, `vless` was blocked by `min_mbps_below_floor` and `stability_below_floor`; the remaining channels were blocked by health, quality, reservation, or service gates. In the fresh production run, `vless` became eligible and entered the best available pool, so candidate generation recovered without a code change.

The remaining blocker is no longer candidate generation. The current blocker is selected move finalization: restore barrier clearance is expired, and authority is still capped to CANARY.

## PLANNER_PIPELINE_TRACE

| Stage | Current result | Evidence |
| --- | --- | --- |
| Users | 18 active users | current_planner_any_target.json |
| Channels | 7 egress channels | current_planner_any_target.json |
| Health | 1 healthy channel | pipeline_summary.json |
| Eligibility | only `vless` is eligible for planned/failover candidate use | per_channel_eligibility_summary.json |
| Required services | `vless` passes VIDEO_OPTIMIZED required service policy | per_channel_eligibility_summary.json |
| Capacity | capacity is not the elimination root cause | per_channel_eligibility_summary.json |
| Trust | trust/routing intelligence does not create or remove hard candidates | current_planner_any_target.json |
| Prediction | prediction is advisory and does not eliminate candidate generation | current_planner_any_target.json |
| Best Available Pool | `vless` is best_available_pool_rank_1 | per_channel_eligibility_summary.json |
| Candidate Generation | 14 failover candidate moves generated toward `vless` | per_user_decision_summary.json |
| Authority Gate | 14 candidates capped to 1 by CANARY runtime authority | pipeline_summary.json |
| Restore Barrier | final selected moves dropped to 0 because clearance expired | pipeline_summary.json |

## HEALTH_ROOT_CAUSE_REPORT

Current production health summary:

- dynamic_load.mode: dynamic
- active_users: 18
- total_channels: 7
- healthy_channels: 1
- degraded_or_dead_channels: 6
- working_channels: 1
- status: warm

Per-channel current health/eligibility:

| Channel | Planner eligible | Main blockers |
| --- | --- | --- |
| `1` | false | health_code_000, severity_FAIL, avg_mbps_below_floor, min_mbps_below_floor, service failures |
| `amneziawg-exec-20260528-10-8-1-14` | false | manual_only, reserve_only, canary_reserved_production_assignment_blocked, quality floors |
| `awg0` | false | avg_mbps_below_floor, min_mbps_below_floor |
| `awg3` | false | avg_mbps_below_floor, min_mbps_below_floor, stability_below_floor |
| `openvpn-1779388847-d2ad7c` | false | health_code_000, severity_FAIL, interface/service failures |
| `vless` | true | none |
| `wireguard-1779454504-c43409` | false | canary_reserved_production_assignment_blocked |

Health root cause:

The old `healthy_egress_total=0` occurred because the only generally usable candidate target, `vless`, did not pass the quality/stability eligibility gates at that time. In the current production run, `vless` passes these gates and becomes the single healthy/eligible channel.

## ELIGIBILITY_ROOT_CAUSE_REPORT

Current eligibility root cause:

- `vless` is eligible across 18 observations.
- All other channels are ineligible for at least one hard gate.
- Candidate generation therefore depends on `vless` being eligible.

Old evidence showed `vless` as ineligible:

- avg_mbps: 33.0
- min_mbps: 6.7
- stability: 0.203
- hist_1h_min_mbps: 9.242
- hist_1h_stability: 0.3177
- blockers:
  - min_mbps_below_floor
  - stability_below_floor
- best_available_pool: false

Current evidence shows `vless` as eligible:

- avg_mbps: 45.81
- min_mbps: 42.09
- stability: 0.919
- hist_1h_min_mbps: 14.472
- hist_1h_stability: 0.3929
- blockers: []
- quality_floor_overridden_by_service_evidence: present
- best_available_pool: true
- pool_rank: 1

Therefore candidate generation recovered when `vless` moved from ineligible to eligible.

## CAPACITY_ROOT_CAUSE_REPORT

Capacity is not the root cause.

Examples:

- `vless` projected load: 4 users, soft_limit 21, hard_limit 27, capacity_available.
- `awg0` projected load: 3 users, soft_limit 21, hard_limit 27, capacity_available.
- `awg3` projected load: 2 users, soft_limit 21, hard_limit 27, capacity_available.
- `wireguard-1779454504-c43409` projected load: 0 users, empty_capacity_available.

Capacity breaks ties after service suitability; it is not eliminating the current candidate pool.

## SERVICE_ROUTING_ROOT_CAUSE_REPORT

Service-aware routing is not the current blocker for `vless`.

Current `vless` service state:

- service aggregate score: 100.0
- route_class_fitness: OK
- VIDEO_OPTIMIZED service checks: OK
- best_available_pool_rank_1: true

Service policy does eliminate clearly failed channels:

- `1` and `openvpn-1779388847-d2ad7c` fail VIDEO_OPTIMIZED/service checks and are hard blocked.

This is expected behavior, not a planner bug.

## TRUST_ROOT_CAUSE_REPORT

Trust is not the root cause of zero candidates.

The planner evidence preserves routing intelligence as advice only:

- can_create_candidates: false
- can_bypass_hard_gates: false
- can_bypass_reservation: false
- can_bypass_governance: false
- can_execute_runtime: false

No trust gate was found that eliminated `vless`. The previous zero-candidate state was explained by quality/stability eligibility, not trust policy.

## PREDICTION_ROOT_CAUSE_REPORT

Prediction is not the root cause of zero candidates.

Prediction and routing intelligence can influence ranking among eligible candidates, but cannot create candidates or bypass hard gates. In the current run, candidate generation recovered because `vless` became eligible, not because prediction policy changed.

## BEST_AVAILABLE_POOL_ROOT_CAUSE_REPORT

Old state:

- `vless` was not eligible.
- Therefore no usable best available pool member existed for failover candidate generation.

Current state:

- `vless` is eligible.
- `vless` is marked best_available_pool_rank_1.
- 14 users receive failover recommendations to `vless`.

Pool logic is not removing all candidates. Pool logic now correctly marks the only eligible usable target.

## CANDIDATE_ROOT_CAUSE_REPORT

Candidate generation now works.

Current candidate moves:

- 14 users have recommended_egress different from current_egress.
- All 14 are failover moves caused by `current_egress_not_eligible`.
- Target: `vless`.

Users with current failover recommendation to `vless` include:

- 10.0.0.3: awg3 -> vless
- 10.0.0.6: awg3 -> vless
- 10.7.0.3: amneziawg-exec-20260528-10-8-1-14 -> vless
- 10.7.0.9: awg0 -> vless
- 10.7.0.13: awg0 -> vless

Candidate generation stage is no longer the blocker.

The current selected move blocker is later:

- authority gate: selected_moves_before_gate=14, selected_moves_after_gate=1
- authority decision: cap_prepared_authority_to_certified_evidence
- runtime authority: CANARY
- restore barrier clearance: restore_barrier_clearance_generation_expired
- final selected_moves=0

## BLOCKER_CLOSURE

Discovered blocker:

- Previous `candidate_moves=0`.

Proven cause:

- No eligible failover target existed in the old evidence.
- `vless`, the only currently viable broad failover target, was blocked by quality/stability floors at that time.

Closure:

- Fresh production pre-planner refresh now shows `vless` eligible.
- Candidate generation now produces 14 candidates.
- No code or policy fix was required.

In-scope fix performed:

- None. No safe planner bug was proven.

Out-of-scope mutation intentionally not performed:

- No restore barrier refresh.
- No approval packet mutation.
- No apply.
- No user movement.

## POST_FIX_VALIDATION

Fresh production general planner run:

- Evidence: cohort_discovery_evidence/current_planner_any_target.json
- candidate_moves: 14
- candidate_moves_total: 14
- healthy_egress_total: 1
- selected_moves: 0

Fresh production targeted `vless` run:

- Evidence: cohort_discovery_evidence/current_planner_target_vless.json
- candidate_moves: 14
- candidate_moves_total: 14
- healthy_egress_total: 1
- selected_moves: 0

Planner summaries:

- cohort_discovery_evidence/pipeline_summary.json
- cohort_discovery_evidence/per_channel_eligibility_summary.json
- cohort_discovery_evidence/per_user_decision_summary.json

Local validation:

- py_compile tools/v7-users-autoswitch: PASS
- planner policy tests: PASS, 47 tests

Truth check note:

- cohort_discovery_evidence/truth_check_after_candidate_recovery.json reports runtime_local_commit_mismatch because production is still at deploy commit `8ce0647109741fbc49957be05ce29836d14ec2d5`, while local contains later report/evidence commits.
- This is not a candidate generation blocker because the production planner dry-run evidence was collected directly from production.
- It is a convergence follow-up before any later live action.

## Final Verdict

Why candidate_moves=0?

The old zero-candidate state was caused by eligibility, not by missing users or a planner selection bug. At the time of the previous certification, no failover target was eligible. `vless` was blocked by `min_mbps_below_floor` and `stability_below_floor`; other channels were blocked by health, quality, reservation, or service gates.

Was it fixed?

Yes for candidate generation. A fresh production pre-planner refresh shows `vless` eligible and candidate generation now works.

Current healthy_egress_total:

- 1

Current candidate_moves:

- 14

Current selected_moves:

- 0

Current blocker:

- restore_barrier_clearance_generation_expired prevents final selected moves.
- authority remains capped to CANARY, so even with 14 candidates the runtime budget is 1 until SMALL_BATCH is certified.

Current next action:

- Do not retry SMALL_BATCH execution immediately.
- First re-align local/GitHub/production truth after this report if required by the convergence gate.
- Then generate a fresh governed approval packet and restore barrier clearance for the current real planner snapshot.
- Because runtime authority is still CANARY, the next live action must be a bounded CANARY apply/verify unless an explicit governance program certifies SMALL_BATCH from valid evidence.

## Success Condition

Outcome A:

- candidate generation works: true
- planner produces candidates: true

Outcome B is not needed for candidate generation because a candidate generation blocker no longer remains.

