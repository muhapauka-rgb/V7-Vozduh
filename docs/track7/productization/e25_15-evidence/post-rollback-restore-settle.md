# E25.15 Post-Rollback Restore-Settle

V7 restore settle gate (read-only)
runtime_commands_executed=False
mode=pre-restore
gate_status=GO
sample_count=3
required_samples=3
samples_span_seconds=49
apply_timer_intervals_covered=2.45
required_apply_timer_intervals=2
selected_moves_by_sample=[0, 0, 0]
telegram_hard_blocked_by_sample=[False, False, False]
egress_1_eligible_by_sample=[True, True, True]
movement_count_by_sample=[0, 0, 0]
registry_stable=True
egress_registry_stable=True
checkers_ok=True
hidden_movers_observed=False
moved_users=[]
recommended_action=pre_restore_gate_clean_request_separate_apply_restore_approval
execution_allowed_now=False
sample_sources:
  - /tmp/e25_15_post_rollback_samples/sample-01.json
  - /tmp/e25_15_post_rollback_samples/sample-02.json
  - /tmp/e25_15_post_rollback_samples/sample-03.json

candidate_row=ip=10.7.0.11 current=1 table=1009 enabled=1
drift_row=ip=10.7.0.16 current=vless table=1014 enabled=1
target_users=0
selected_moves_count=0
hidden_movers_count=0
runtime_checkers_ok=true
