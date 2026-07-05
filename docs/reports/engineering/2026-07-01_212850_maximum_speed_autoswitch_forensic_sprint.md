# V7 Maximum Speed Autoswitch Forensic Sprint

Timestamp: 2026-07-01_212850 Asia/Bangkok

Mode: read-only forensic sprint. No patch, no deploy, no apply, no user movement.

## Verdict

ROOT_FOUND

Root classification: AUTHORITY_RESTORE_LOCK_DEFECT

First actionable blocker: `restore_barrier_failover_suppressed`

Owner: `tools/v7-users-autoswitch` for Planner suppression; `admin_core/operator_execution.py` owns restore-barrier clearance materialization.

Exact file/function:
- Historical persisted behavior: `tools/v7-users-autoswitch::_decision_for_user()`
- Current local code equivalent enforcement points:
  - `tools/v7-users-autoswitch::plan()` restore clearance budget guard, lines 5201-5212
  - `tools/v7-users-autoswitch::plan()` restore barrier execution gate, lines 5269-5290
  - `tools/v7-users-autoswitch::_approved_l3_production_validation_envelope()`, lines 1085-1166

Next action: F. rerun one-user L3 production validation with a fresh approved plan lock / restore-barrier clearance for exactly one failed-source user and an eligible target.

## Scope

Target production issue:
- source channel: `openvpn-1779388847-d2ad7c`
- affected users: 14 in persisted planner artifact
- apply/movement: forbidden for this sprint

Live server snapshot attempt:
- SSH to `77.110.103.131` succeeded read-only.
- Expected V7 state paths were not present under `/opt`, `/root`, `/home`, `/var`, or `/srv`.
- No live production state was used for conclusions.

Primary historical source object:
- `docs/reports/engineering/live_openvpn_trace_2026-06-30/fixture_all_no_target.json`
- producer: `tools/v7-users-autoswitch`
- operation owner: `tools/v7-users-autoswitch`
- operation id: `runtime_autoswitch_7d1a84de540d525fa249ac22`
- planner generation id: `5ac20d4906a172d0bdb9f8ecd5de019cdc9e054a967439c72730910538b8dc2e`
- updated: `2026-06-29T17:15:32.007703+00:00`
- freshness: historical persisted plan, not recomputed current state

Secondary replay:
- State copied to `/tmp/v7_forensic_openvpn_state`.
- Current local `tools/v7-users-autoswitch` run with `--source-egress openvpn-1779388847-d2ad7c --max-selected-moves 25 --pretty`, no `--apply`.
- Replay is non-authoritative for historical eligibility because service truth ages are recomputed relative to 2026-07-01 and now expire target evidence.

## Historical Candidate Proof

For 14 users currently on `openvpn-1779388847-d2ad7c`, the persisted plan shows:
- `action: keep`
- `move_type: none`
- `recommended_egress: openvpn-1779388847-d2ad7c`
- `reason: ["restore_barrier_failover_suppressed"]`

Sample user: `10.0.0.2`

Current/source candidate:
- egress: `openvpn-1779388847-d2ad7c`
- eligible: `false`
- blockers: `telegram_required_telegram_down_14s`, `planned_hard_full`
- Telegram status: `TELEGRAM_DOWN_14S`
- Telegram hard blocked: `true`
- load: `users=14`, `hard_limit=14`, `status=HARD_FULL`

Eligible target candidates in the same historical decision:
- `vless`: eligible `true`, score `2170.34`, Telegram OK, load `0/14`
- `awg3`: eligible `true`, score `2112.44`, Telegram OK, load `1/14`
- `awg0`: eligible `true`, score `2093.79`, Telegram OK, load `1/14`
- `wireguard-1779454504-c43409`: eligible `true`, score `2060.8`, Telegram OK, load `11/14`

Therefore a legal failed-source candidate existed at Planner decision time:
- same subject: user on `openvpn-1779388847-d2ad7c`
- source failure: required Telegram hard failure plus hard-full source
- safe targets: at least `vless`, `awg3`, `awg0`
- selected result for failed source: none

## Selected Move Mismatch

The persisted plan selected one unrelated move:
- user: `10.7.0.16`
- source: `wireguard-1779454504-c43409`
- target: `vless`
- move_type: `rebalance`
- reason: `load_rebalance_even_distribution`

Summary:
- users total: 27
- source users on failed OpenVPN: 14
- candidate moves total: 11
- selected moves: 1
- selected failed-source L3 moves: 0

This is the operational mismatch: the failed source had legal target candidates, but the selected move path contained an unrelated rebalance.

## Gate Matrix

`tools/v7-users-autoswitch::_decision_for_user()`
- input: active user, important services, route class, all egress candidates
- output for failed-source users: `keep`, `none`, current source retained
- eligible before: current candidate created as false after gates
- eligible after: no selected failover decision emitted
- blocker added: none at decision layer; decision reason added `restore_barrier_failover_suppressed`
- source object: `fixture_all_no_target.json`
- producer: `tools/v7-users-autoswitch`
- owner: `tools/v7-users-autoswitch`

`_candidate()`
- input: user, egress, services, route class
- output: candidate rows
- source candidate output: ineligible
- target candidate output: `vless`, `awg3`, `awg0`, `wireguard-*` eligible
- owner: `tools/v7-users-autoswitch`

`_gate_basic()`
- historical source candidate blocker: none shown for source sample
- historical target blockers: none for eligible targets
- owner: `tools/v7-users-autoswitch`

`_gate_quality()`
- historical source candidate: no source hard quality blocker in sample; quality was not the first failed-source blocker
- historical targets: passed
- owner: `tools/v7-users-autoswitch`

`_gate_service()`
- historical source candidate blocker: `telegram_required_telegram_down_14s`
- service evidence object: candidate `telegram` subobject from service matrix/sentinel projection
- producer: service matrix / Telegram sentinel inputs consumed by Planner
- owner: `tools/v7-users-autoswitch` for consumption

`_gate_load()`
- historical source candidate blocker: `planned_hard_full`
- source object: candidate `load`
- producer: egress registry / dynamic load summary consumed by Planner
- owner: `tools/v7-users-autoswitch`

`_gate_safety()`
- historical source and target sample: no safety blocker shown
- owner: `tools/v7-users-autoswitch`

Restore barrier gate:
- input: `plan.safety.restore_barrier`
- historical values: `active=true`, `failover_quarantine=true`, `clearance_max_selected_moves=0`, `cleared=true`
- output: failover suppressed in historical decisions
- blocker/reason: `restore_barrier_failover_suppressed`
- owner of clearance: `admin_core/operator_execution.py`

## Current Local Replay

Command class:

`tools/v7-users-autoswitch --state-dir /tmp/v7_forensic_openvpn_state --source-egress openvpn-1779388847-d2ad7c --max-selected-moves 25 --pretty`

Result:
- return code: 0
- selected moves: 0
- source decisions: 14
- replay reason: `no_eligible_failover_target`
- replay target blockers: `service_*_truth_stale`

Interpretation:
- This replay is not stronger than the historical persisted plan because target service freshness aged after capture.
- It proves the current CLI can be run read-only only on a copied state; direct production no-apply is not mutation-free because finalize/closure paths may materialize runtime state.
- It does not disprove the historical legal candidate.

## Function Ownership Matrix

`tools/v7-users-autoswitch`
- owns candidate creation, service/load/safety gates, move classification, selection, authority budget gate, restore-barrier execution gate, and L3 emergency gate evidence consumption.
- current relevant functions: `_decision_for_user`, `_candidate`, `_gate_basic`, `_gate_quality`, `_gate_service`, `_gate_load`, `_gate_safety`, `_select_moves`, `plan`.

`tools/v7-governed-canary-dry-run-cycle`
- owns governed dry-run/canary packet constraints for L3 production validation.
- relevant function: `l3_packet_constraints_ok`.

`admin_core/operator_execution_pipeline.py`
- owns operator packet/candidate review surfaces and L3 production validation transition logic.
- relevant functions: `_candidate_selection_review_row`, `l3_production_validation_runtime_action_transition`.

`admin_core/operator_execution.py`
- owns restore-barrier / approval path used by runtime execution.
- exact current source was not modified.

## Classification

Selected root classification: AUTHORITY_RESTORE_LOCK_DEFECT

Why not `NO_LEGAL_L3_CANDIDATE_EXISTS`:
- Historical persisted plan shows `vless`, `awg3`, and `awg0` eligible for a failed-source user.

Why not `SERVICE_EVIDENCE_DEFECT`:
- Historical source failure evidence was sufficient: `telegram_required_telegram_down_14s`.
- Historical target evidence was sufficient: target Telegram and VIDEO_OPTIMIZED service rows OK.
- The current replay has stale target evidence, but that is a replay-time freshness artifact, not the historical blocker.

Why not only `OBSERVABILITY_ONLY_BLOCKER`:
- The historical plan preserves enough evidence to identify the decision reason.

Why not only `OMP_AUTHORITY_BOUNDARY`:
- Authority/OMP constraints explain why movement must remain bounded, but the first failed-source loss occurred earlier: Planner suppressed L3 failover decisions under restore barrier instead of surfacing a one-user L3 candidate for the validation ladder.

## Final Answer To Sprint Questions

1. Legal L3 candidate existed historically for at least user `10.0.0.2` on `openvpn-1779388847-d2ad7c` to `vless`.
2. The first actionable blocker was `restore_barrier_failover_suppressed`.
3. It was an authority/restore-lock suppression, not target selection, load, or service evidence.
4. The selected move path then chose unrelated `wireguard-1779454504-c43409 -> vless` rebalance.
5. Planner did not legally move users from the failed channel because failed-source failover was suppressed before selected moves.
6. The existing owner is available: Planner owner `tools/v7-users-autoswitch`; restore-barrier clearance owner `admin_core/operator_execution.py`.
7. Next action is one-user L3 production validation with a fresh approved plan lock / restore-barrier clearance.
