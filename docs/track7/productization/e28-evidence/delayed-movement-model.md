# E28 Delayed Movement Model

date_utc=2026-05-29T06:18:00Z

restore_settle_gate_status=GO
sample_count=3
apply_timer_intervals_covered=6.0
selected_moves_by_sample=[0,0,0]
movement_count_by_sample=[0,0,0]
hidden_movers_observed=false
registry_stable=true
egress_registry_stable=true
runtime_checkers_ok=true

Delayed monitoring for a small cohort must preserve the E25/E27 pattern:

- forward observation samples
- rollback verification
- post-rollback restore-settle
- delayed monitoring samples
- selected_moves must remain zero
- hidden movers must remain absent
- runtime checkers must remain OK

delayed_movement_protection_scales=true

