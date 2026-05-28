# BLOCK E24.2 Fresh Restore-Settle Sample Window For E25 Execution Gate Report

Date: 2026-05-28

## Executive Verdict

`fresh_restore_settle_window_collected=true`

E24.2 collected a fresh VPS read-only restore-settle sample window for the E25 movement execution gate. The sample window passed the restored helper gate:

- `gate_status=GO`
- `sample_count=3`
- `apply_timer_intervals_covered=5.75`
- `selected_moves_by_sample=[0,0,0]`
- `registry_stable=true`
- `egress_registry_stable=true`
- `checkers_ok=true`
- `hidden_movers_observed=false`

No runtime mutation was performed.

## Sample Window

Sample directory:

- `docs/track7/productization/e24_2-evidence/restore-settle-samples/`

Sample files:

- `sample-01.json`
  - timestamp: `2026-05-28T09:40:54.302276+00:00`
- `sample-02.json`
  - timestamp: `2026-05-28T09:42:07.682717+00:00`
- `sample-03.json`
  - timestamp: `2026-05-28T09:42:49.750771+00:00`

Window:

- span: `115` seconds
- helper apply timer seconds: `20`
- nominal intervals covered: `5.75`

Important caveat:

- planner timer was inactive in all samples.
- apply timer was inactive in all samples.
- This proves a clean observation window across nominal interval duration; it does not prove an active apply timer fired cleanly.

## Restore-Settle Gate Output

Command:

```bash
tools/v7-restore-settle-gate --pre-restore --state-dir docs/track7/productization/e24_2-evidence/restore-settle-samples --pretty
tools/v7-restore-settle-gate --pre-restore --state-dir docs/track7/productization/e24_2-evidence/restore-settle-samples --json
```

Result:

- `restore_settle_gate_status=GO`
- `sample_count=3`
- `required_samples=3`
- `samples_span_seconds=115`
- `apply_timer_intervals_covered=5.75`
- `required_apply_timer_intervals=2`
- `selected_moves_by_sample=[0,0,0]`
- `movement_count_by_sample=[0,0,0]`
- `registry_stable=true`
- `egress_registry_stable=true`
- `checkers_ok=true`
- `hidden_movers_observed=false`
- `moved_users=[]`
- `execution_allowed_now=false`

## Manual Cross-Check

Runtime hashes stayed stable:

- `users.registry=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

Candidate:

- `10.7.0.11` remained on `1`
- table remained `1009`

Target:

- `wireguard-1779454504-c43409`
- readiness remained `GO`
- users count remained `0`
- reservation remained present from E24/E24.1 evidence

Selected moves:

- no selected-move files observed
- sample value stayed `0`

Hidden movers:

- none observed in samples or final safety check

Runtime checkers:

- `v7-reconcile-check=OK`
- `v7-user-route-check=OK`
- `v7-killswitch-check=OK`
- `v7-provisioning-reconcile-check=OK`

Switch history:

- `/opt/v7/egress/state/switch-history.log` remains missing.
- No movement evidence observed; absence is treated as "no switch-history source", not as a substitute for movement proof.

## E24 Packet Revalidation

E24 packet remains valid:

- candidate user: `10.7.0.11`
- selected target: `wireguard-1779454504-c43409`
- rollback target: `1`
- movement budget: `1`
- registry hashes unchanged
- selected_moves still zero
- target readiness GO
- fresh restore-settle gate GO

Packet refresh decision:

- `packet_needs_refresh=false`

Reason:

- Runtime registry hashes did not drift.
- Candidate/target/rollback semantics did not drift.
- E25 must reference the E24.2 fresh restore-settle evidence and still perform execution-time rechecks.

## Risk Matrix Verdict

- selected_moves appears during sample window: NO
- hidden mover starts: NO
- candidate moves before E25: NO
- WireGuard target becomes occupied: NO
- target readiness regresses: NO
- restore-settle helper reads stale data: NO for the explicit fresh sample dir
- sample dir format incompatible: NO
- apply timer interval calculation wrong: NO, helper computed 5.75 nominal intervals
- runtime checker fails intermittently: NO
- registry hash drifts: NO
- restore barrier/generation state inconsistent: NO blocker observed
- missing switch-history causes false assumptions: mitigated by explicit caveat
- helper GO false-positive: no evidence after manual cross-check
- helper NO-GO false-negative: not observed
- VPS time/timestamps inconsistent: NO

## Tests

- helper `py_compile`: PASS
- targeted helper unit tests: PASS, `19` tests
- full unittest discovery: PASS, `116` tests
- sample JSON validation: PASS
- restore-settle gate pretty/json: PASS
- target readiness pretty/json: PASS
- runtime checkers: PASS
- hidden mover scan: PASS
- credential scan: PASS
- `git diff --check`: PASS

Unavailable/not applicable:

- endpoint inventory: not applicable, no API route changes.
- `/admin-v2` render: not applicable, no UI changes.

## Mandatory Answers

- `fresh_restore_settle_window_collected=true`
- `sample_count=3`
- `apply_timer_intervals_covered=5.75`
- `restore_settle_gate_status=GO`
- `selected_moves_zero=true`
- `hidden_movers_absent=true`
- `runtime_checkers_ok=true`
- `candidate_still_valid=true`
- `target_readiness_go=true`
- `e24_packet_still_valid=true`
- `e25_execution_gate_ready=true`
- `recommended_next_block=E25_FIRST_OPERATOR_DRIVEN_BOUNDED_USER_MOVEMENT_EXECUTION`
- `execution_allowed_now=false`

## Final Mutation Statement

- Runtime mutation performed: NO
- User movement performed: NO
- Routing mutation performed: NO
- Kill switch mutation performed: NO
- Autoswitch apply performed manually: NO
- Canary performed: NO
