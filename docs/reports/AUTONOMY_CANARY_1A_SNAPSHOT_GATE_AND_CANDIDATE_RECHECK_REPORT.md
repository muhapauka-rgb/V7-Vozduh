# AUTONOMY.CANARY.1A Snapshot Gate And Candidate Recheck Report

Date: 2026-06-23
Workspace: `/Users/ponch/Documents/New project`
Branch: `Updatesystem`
Local commit at start: `c7c54604`

## 1. Mission

Determine why current production canary evidence has `selected_move_count=0`:

- stable no-candidate state,
- candidate visibility blocked by snapshot gate,
- or inconclusive evidence.

No user movement, runtime apply, daemon enablement, new planner, new governance, new execution path, new truth source, synthetic candidate, synthetic event, synthetic evidence, prediction actual, or operator comparison was created.

## 2. Truth Gate

Initial sandboxed truth/convergence failed only because GitHub remote access was blocked by the sandbox. Escalated gate passed and is stored as evidence:

| Check | Evidence | Result |
| --- | --- | --- |
| Truth gate | `docs/reports/AUTONOMY_CANARY_1A_EVIDENCE/pre_truth_check_escalated.json` | PASS |
| Convergence gate | `docs/reports/AUTONOMY_CANARY_1A_EVIDENCE/pre_convergence_status_escalated.json` | PASS |

Sandboxed non-go files are retained as diagnostic evidence: `pre_truth_check.json`, `pre_convergence_status.json`.

## 3. Commands Run

Read-only / observe:

- `./tools/v7-truth-check --all --json`
- `./tools/v7-convergence-status --json`
- `ssh v7-vps '/usr/local/bin/v7-users-autoswitch --mode observe --pretty'`
- `ssh v7-vps '/usr/local/bin/v7-users-autoswitch --mode observe --max-selected-moves 1 --pretty'`
- `ssh v7-vps '/usr/local/bin/v7-users-autoswitch --mode observe --max-selected-moves 1 --pre-planner-refresh=dry-run --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh --pretty'`
- `ssh v7-vps '/usr/local/bin/v7-intelligence-snapshot-refresh --dry-run --pretty'`
- `ssh v7-vps '/usr/local/bin/v7-autonomy-trust-evidence-inventory --pretty'`
- `ssh v7-vps 'systemctl status ... --no-pager'`
- read-only JSON freshness/hash probes under `/opt/v7/egress/state`.

Snapshot-only existing-owner correction:

- `ssh v7-vps '/usr/local/bin/v7-intelligence-snapshot-refresh --pretty'`
- `ssh v7-vps '/usr/local/bin/v7-users-autoswitch --mode observe --max-selected-moves 1 --pre-planner-refresh=write --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh --pretty'`

These commands did not use `--apply` and did not move users.

## 4. Evidence Files

| Evidence | Path |
| --- | --- |
| Before planner observe | `docs/reports/AUTONOMY_CANARY_1A_EVIDENCE/production_planner_observe_before.json` |
| Before canary observe | `docs/reports/AUTONOMY_CANARY_1A_EVIDENCE/production_planner_observe_canary_before.json` |
| Snapshot refresh dry-run | `docs/reports/AUTONOMY_CANARY_1A_EVIDENCE/production_snapshot_refresh_dry_run_before.json` |
| Snapshot-only refresh write | `docs/reports/AUTONOMY_CANARY_1A_EVIDENCE/production_snapshot_refresh_write.json` |
| Planner-owned refresh observe | `docs/reports/AUTONOMY_CANARY_1A_EVIDENCE/production_planner_pre_refresh_write_observe.json` |
| Final normal observe | `docs/reports/AUTONOMY_CANARY_1A_EVIDENCE/production_planner_observe_final.json` |
| Trust inventory before/after | `production_trust_inventory_before.json`, `production_trust_inventory_after.json` |
| Systemd status | `production_systemd_status_full.txt` |
| Summaries | `canary_1a_before_summary.json`, `canary_1a_after_summary.json`, `canary_1a_pre_refresh_write_summary.json`, `canary_1a_final_summary.json` |

## 5. Branch Decision

`SCENARIO_B_CANDIDATE_VISIBILITY_BLOCKED`

Reason: production has real candidate pressure, but normal planner observe still suppresses selected moves because intelligence snapshot gate fails on service-derived snapshot families.

## 6. Current Production Snapshot

| Field | Value |
| --- | --- |
| `candidate_moves_total` | `18` |
| `selected_move_count` normal observe | `0` |
| Normal observe terminal reason | `dry_run_intelligence_snapshot_stop_required` |
| Current distribution | `awg3=8`, `wireguard-1779454504-c43409=8`, `vless=10` |
| Snapshot stop families | `service-scores`, `channel-service-scores` |
| Snapshot mismatch | `source_hash_mismatch:*:service_matrix` |
| Existing approved plan lock selected moves | `10` |
| Autoswitch service/timer | inactive |
| Intelligence snapshot refresh service/timer | missing |

## 7. Before / After Gate Behavior

| Run | Candidate Moves | Selected Moves | Snapshot Gate | Terminal Reason |
| --- | ---: | ---: | --- | --- |
| Normal observe before refresh | 18 | 0 | STOP: service/channel service scores | `dry_run_intelligence_snapshot_stop_required` |
| Standalone snapshot refresh write | n/a | n/a | `source_stable=true`, `snapshot_count=11` | snapshot-only write |
| Normal observe after standalone refresh | 18 | 0 | STOP: service/channel service scores | `dry_run_intelligence_snapshot_stop_required` |
| Planner-owned pre-refresh write observe | 18 | 0 | PASS: `stop_required=false` | `dry_run_restore_barrier_clearance_generation_expired` |
| Final normal observe | 18 | 0 | STOP: service/channel service scores | `dry_run_intelligence_snapshot_stop_required` |

Interpretation: candidate visibility is partially proven but not durable. The existing planner-owned refresh path clears snapshot gate inside the same observe run. The default/normal observe path still re-enters fail-closed snapshot mismatch.

## 8. Why `selected_move_count=0`

There are two sequential blockers:

1. Normal observe stops before selected moves because `service-scores` and `channel-service-scores` source hashes do not match the planner's current `service_matrix`.
2. When the existing planner-owned refresh write is used, the snapshot gate clears, but selected moves still stop because restore-barrier clearance generation is expired.

Therefore the zero selected moves are not evidence of a stable no-candidate state.

## 9. Candidate Reality

| Question | Answer |
| --- | --- |
| Are candidates present? | YES, `candidate_moves_total=18` |
| Are the old `awg3=8` users still present? | YES |
| Is WireGuard still in the distribution? | YES, `wireguard-1779454504-c43409=8` |
| Is `vless` still in the distribution? | YES, `vless=10` |
| Is normal observe allowed to select? | NO, snapshot gate stops first |
| Does planner-owned refresh prove a safe path? | PARTIAL: snapshot gate clears inside observe, but restore barrier generation then blocks |

## 10. Snapshot Gate Recheck

Standalone `v7-intelligence-snapshot-refresh --pretty`:

- `source_stable=true`
- `snapshot_count=11`
- `runtime_behavior_changed=false`
- `governance_behavior_changed=false`
- `users_moved=false`

Planner-owned `--pre-planner-refresh=write` observe:

- `routing_brain.snapshot_gate.stop_required=false`
- `routing_brain.snapshot_gate.stop_families=[]`
- service snapshot validation errors: `[]`
- channel-service snapshot validation errors: `[]`
- terminal reason moved forward to `dry_run_restore_barrier_clearance_generation_expired`

This proves the existing owner can clear the snapshot gate in a safe observe-only context, but not yet durably for normal observe.

## 11. Confidence / Trust Recheck

Trust inventory remains below canary floor:

| Metric | Value |
| --- | ---: |
| Prediction confidence before | `36.799` |
| Prediction confidence after | `36.765` |
| Users moved | `0` |
| Apply executed | `false` |

No trust/confidence floor was changed.

## 12. Safety Assessment

| Risk | Status |
| --- | --- |
| Runtime apply | Did not occur |
| User movement | Did not occur |
| Autoswitch daemon/timer enablement | Did not occur |
| Snapshot-only write | Occurred through existing `v7-intelligence-snapshot-refresh` owner |
| New planner/governance/execution/truth source | Not created |
| Synthetic candidates/events/evidence | Not created |
| Formula/floor/threshold changes | Not changed |

## 13. Tests / Verification

No program code changed in this phase. Verification was runtime evidence based:

- Truth gate PASS after escalation.
- Convergence PASS after escalation.
- Snapshot-only refresh reported `users_moved=false`.
- Planner-owned observe with `--pre-planner-refresh=write` reported snapshot gate PASS.
- Normal observe still reported snapshot gate STOP, so the fix is not complete.

## 14. Documentation Updated

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/reference/V7_PROJECT_MAP.md`
- `docs/reference/V7_AUTONOMY_BLUEPRINT.md`

No ADR was created because no new architectural rule was established. Existing event-driven autonomy and reference-first rules still apply.

## 15. Required Next Phase

`AUTONOMY.CANARY.1B_PLANNER_SNAPSHOT_GATE_DURABILITY_FIX`

Scope:

1. Reuse existing `tools/v7-users-autoswitch` and `tools/v7-intelligence-snapshot-refresh`.
2. Make the existing planner/snapshot lifecycle durable enough that normal observe no longer reverts to `dry_run_intelligence_snapshot_stop_required` immediately after a planner-owned refresh.
3. Preserve fail-closed behavior if source volatility is real.
4. Preserve no-apply/no-user-movement semantics in observe mode.
5. Recheck restore-barrier generation only after snapshot gate is durably clean.

## 16. Final Verdict

`CANDIDATE_VISIBILITY_BLOCKED`

Candidate visibility is not solved yet. The system has candidates, and the existing planner-owned refresh path can clear the snapshot gate in-run, but normal production observe still fails closed on service snapshot source mismatch. Do not start canary apply. Do not move users. The next safe step is an existing-owner lifecycle durability fix.
