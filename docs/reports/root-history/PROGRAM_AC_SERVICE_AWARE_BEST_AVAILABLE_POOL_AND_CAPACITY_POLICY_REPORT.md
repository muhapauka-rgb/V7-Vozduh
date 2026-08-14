# PROGRAM A.C - SERVICE-AWARE BEST AVAILABLE POOL AND CAPACITY-AWARE POLICY REPORT

Date: 2026-06-02

Project: V7 Vozduh

Branch: `Updatesystem`

Canonical workspace: `/Users/ponch/Documents/New project`

## Safety

No production mutation was performed.

- deploy: no
- git push: no
- merge: no
- autoswitch apply: no
- user movement: no
- routing mutation: no
- service restart: no
- systemd/timer modification: no
- cleanup/deletion: no

## Discovery / Duplication Gate

A.C reused the existing autoswitch planner ownership chain. No parallel planner, duplicate orchestrator, duplicate scheduler, duplicate execution path, or duplicate state writer was created.

Primary reused owners:

- `AutoswitchPlanner._decision_for_user`
- `AutoswitchPlanner._candidate`
- `AutoswitchPlanner._pick_projected_moves`
- `AutoswitchPlanner._projected_target_for_move`
- existing safety/reservation/quality/load/service/sticky/anti-flap gates

Evidence: `docs/reports/evidence/program_ac_evidence/discovery_duplication_audit.md`

## Implementation Summary

Implemented in `tools/v7-users-autoswitch`:

- `DEFAULT_BEST_AVAILABLE_POOL_POLICY`
- candidate metadata for `capacity_decision`, `best_available_pool`, `pool_rank`, `pool_reason`, `pool_cutoff_reason`
- planner loading for `best_available_pool` policy
- `_capacity_decision(...)`
- `_mark_best_available_pool(...)`
- capacity score in score parts
- pool-aware projected target selection
- projected load/capacity metadata in selected moves

The pool is applied after existing gates, so unsafe or reserved candidates cannot enter the final pool. Capacity affects distribution among already safe service-suitable candidates; it does not override service suitability, hard safety, reservation, restore barrier, route class, quality, sticky, or relative improvement constraints.

## Policy Semantics

Best Available Pool:

- enabled by default
- default `top_n=3`
- default `max_score_gap_pct=0.15`
- default `min_service_suitability=50.0`
- ranks eligible candidates by non-sticky score, projected load, and egress id
- annotates selected candidates as pool members

Capacity-aware selection:

- computes projected load against soft/hard limits
- exposes `capacity_score`, `load_penalty`, `projected_load`, and `capacity_decision`
- uses capacity as a distribution/tie-break signal after service suitability and gates
- selected moves are assigned using projected load to avoid piling every move onto one pool member when multiple suitable targets exist

## Safety Gates Preserved

Preserved gates:

- hard safety blocks
- reserved/canary/manual-only blocks
- restore barrier suppression
- health code and severity hard blocks
- route-class FAIL block
- required service evidence block
- service failure persistence logic
- quality floors and contextual service-evidence exception
- relative improvement threshold
- sticky/anti-flap cooldown
- hard/soft load protection

## Shadow Replay

Evidence file: `docs/reports/evidence/program_ac_evidence/shadow_replay_ac_policy.json`

Source: `docs/reports/evidence/program_a2_evidence/a2_final_forensics_summary.json`

Runtime mutation: false

Autoswitch apply: false

Observed old policy from A.2:

- users_total=18
- egress_total=7
- healthy_egress_total=0
- candidate_moves_total=0
- selected_moves=0

A.B policy shadow:

- pool_enabled=false
- healthy_egress_total=1
- candidate_moves_total=15
- selected_moves=15
- selected_move_distribution=`{"vless": 15}`

A.C policy shadow:

- pool_enabled=true
- healthy_egress_total=1
- candidate_moves_total=15
- selected_moves=15
- selected_move_distribution=`{"vless": 15}`

A.C with A.2 restore barrier:

- pool_enabled=true
- first_decision_reason=`restore_barrier_failover_suppressed`
- healthy_egress_total=1
- candidate_moves_total=0
- selected_moves=0

Interpretation: A.C restores candidate/selected-move generation under local shadow conditions, while restore barrier still suppresses movement. The current production-like fixture has only one eligible safe target (`vless`), so real multi-target distribution cannot appear there without admitting weak AWG or reserved WireGuard. Multi-target capacity distribution is covered by unit tests with two close safe/suitable pool members.

## Tests

Evidence: `docs/reports/evidence/program_ac_evidence/test_results.md`

Final combined command:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m unittest tests/unit/test_service_aware_policy.py tests/unit/test_best_available_pool_policy.py tests/unit/test_v7_users_autoswitch_policy.py tests/unit/test_v7_truth_check.py tests/unit/test_v7_sync_tools.py
```

Result: PASS, 66 tests OK.

## Truth / Release Gate

Evidence: `docs/reports/evidence/program_ac_evidence/release_sync_gate.md`

Final read-only truth check:

- GitHub remote commit known and aligned with local HEAD: `ddc7d1cf048277e8ffa7e7ef3d6a0c85f256e7ca`
- runtime access: READY
- runtime truth: KNOWN
- state truth: KNOWN
- final verdict: NO-GO
- blockers: `dirty_workspace,runtime_critical_dirty`

Safe release sync dry-run:

- no apply
- no production mutation
- deployment would be required for `/usr/local/bin/v7-users-autoswitch`
- local A.C autoswitch hash differs from production autoswitch hash
- sync blocked until runtime-critical dirty work is explicitly committed/pushed/released

## Production Dry-Run

Not completed.

Reason: the A.C binary was not deployed to production, and running a production dry-run against old production code would not validate the new A.C policy. This report therefore treats local shadow replay and unit tests as implementation evidence, while live production retry remains blocked until safe release sync is approved and completed.

## Final Verdicts

- service_aware_policy_active=true
- best_available_pool_implemented=true
- capacity_aware_selection_implemented=true
- hard_safety_gates_preserved=true
- reservation_gates_preserved=true
- relative_improvement_preserved=true
- sticky_antiflap_preserved=true
- tests_pass=true
- truth_check_all_pass=false
- production_dry_run_completed=false
- candidate_restored=true
- selected_moves_present=true
- safe_to_retry_PROGRAM_A=false

## Required Next Step Before Program A Retry

Do not retry Program A live execution yet.

Required sequence:

1. Explicitly approve commit/stage of runtime-critical A.C changes.
2. Push the committed branch to GitHub.
3. Run safe release sync apply with explicit runtime-critical allowance.
4. Re-run `tools/v7-truth-check --all`.
5. Run production autoswitch dry-run only after production binary hash matches the released A.C binary.
6. Retry Program A only if truth check passes and production dry-run shows expected selected moves without restore-barrier suppression.
