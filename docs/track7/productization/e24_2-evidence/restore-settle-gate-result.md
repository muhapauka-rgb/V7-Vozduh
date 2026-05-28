# E24.2 Restore-Settle Gate Result

Command:

```bash
tools/v7-restore-settle-gate --pre-restore --state-dir docs/track7/productization/e24_2-evidence/restore-settle-samples --pretty
```

Output:

```text
V7 restore settle gate (read-only)
runtime_commands_executed=False
mode=pre-restore
gate_status=GO
sample_count=3
required_samples=3
samples_span_seconds=115
apply_timer_intervals_covered=5.75
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
  - docs/track7/productization/e24_2-evidence/restore-settle-samples/sample-01.json
  - docs/track7/productization/e24_2-evidence/restore-settle-samples/sample-02.json
  - docs/track7/productization/e24_2-evidence/restore-settle-samples/sample-03.json
```

## Timing Note

- Sample span: `115` seconds.
- Helper `apply_timer_seconds`: `20`.
- Covered nominal apply-timer intervals: `5.75`.
- Actual planner/apply timers were inactive throughout the sample window.
- This is a restore-settle observation window over nominal interval length, not evidence of actual timer firing.

## Gate Verdict

`restore_settle_gate_status=GO`
