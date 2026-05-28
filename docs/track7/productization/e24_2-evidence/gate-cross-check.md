# E24.2 Gate Cross-Check

## Sample Files

- `sample-01.json`
  - timestamp: `2026-05-28T09:40:54.302276+00:00`
- `sample-02.json`
  - timestamp: `2026-05-28T09:42:07.682717+00:00`
- `sample-03.json`
  - timestamp: `2026-05-28T09:42:49.750771+00:00`

Window:

- first to last span: approximately `115` seconds.
- helper reported `samples_span_seconds=115`.
- helper reported `apply_timer_intervals_covered=5.75`.

Timer truth:

- `planner_timer_state=inactive` in all samples.
- `apply_timer_state=inactive` in all samples.
- Interval coverage is nominal helper coverage against `apply_timer_seconds=20`, not actual timer firing evidence.

## Registry Stability

All samples:

- `users_registry_hash=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress_registry_hash=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

Helper result:

- `registry_stable=true`
- `egress_registry_stable=true`

Manual cross-check:

- registry hash drift observed: NO

## Selected Moves

All samples:

- `selected_moves=0`
- `selected_moves_hash=NONE`

Helper result:

- `selected_moves_by_sample=[0,0,0]`

Manual cross-check:

- selected_moves appeared during window: NO

## Hidden Movers

All samples:

- `hidden_movers_observed=false`
- `hidden_movers=[]`

Helper result:

- `hidden_movers_observed=false`

Manual cross-check:

- hidden mover observed: NO

## Runtime Checkers

All samples:

- `checkers_ok=true`

Final VPS safety check:

- `v7-reconcile-check=OK`
- `v7-user-route-check=OK`
- `v7-killswitch-check=OK`
- `v7-provisioning-reconcile-check=OK`

Helper result:

- `checkers_ok=true`

## Candidate Validity

All samples:

- `candidate_user=10.7.0.11`
- `candidate_current_egress=1`
- `candidate_table=1009`

Final VPS safety check:

- `ip=10.7.0.11 current=1 table=1009 enabled=1`

Candidate moved before E25: NO

## Target Readiness

All samples:

- `target_readiness_status=GO`
- `target_readiness_selected_target=wireguard-1779454504-c43409`
- `wireguard_users_count=0`
- `wireguard_users=[]`

Final VPS target readiness helper:

- `approval_status=GO`
- `selected_target=wireguard-1779454504-c43409`
- WireGuard target status: `GO`, `zero_user=True`

Target readiness regression: NO

## Gate False-Positive / False-Negative Review

False-positive risk:

- Low for the sampled properties because the helper result matches manual sample inspection.
- Caveat: apply timer was inactive, so this window proves stability across nominal interval time, not actual apply timer firing.

False-negative risk:

- Not observed. Helper returned GO and manual cross-check supports the clean window.

## Cross-Check Verdict

`restore_settle_gate_cross_checked=true`

The fresh sample window satisfies the helper's pre-restore gate semantics and supports E25 gate readiness, with the explicit caveat that apply timer remained held/inactive.
