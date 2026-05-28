# E25.1 Restore-Settle Revalidation

Fresh sample directory:

- `docs/track7/productization/e25_1-evidence/restore-settle-samples/`

Samples:

- `sample-01.json`
  - timestamp: `2026-05-28T10:34:05.349211+00:00`
- `sample-02.json`
  - timestamp: `2026-05-28T10:35:12.098821+00:00`
- `sample-03.json`
  - timestamp: `2026-05-28T10:35:48.041558+00:00`

Command:

```bash
tools/v7-restore-settle-gate --pre-restore --state-dir docs/track7/productization/e25_1-evidence/restore-settle-samples --pretty
```

Output:

```text
V7 restore settle gate (read-only)
runtime_commands_executed=False
mode=pre-restore
gate_status=GO
sample_count=3
required_samples=3
samples_span_seconds=102
apply_timer_intervals_covered=5.1
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
```

## Gate Verdict

- `restore_settle_gate_status=GO`
- `selected_moves_zero=true`
- `hidden_movers_absent=true`
- `runtime_checkers_ok=true`
- `candidate_still_on_1=true`

Note:

- planner/apply timers remained inactive in all samples.
- interval coverage is nominal helper coverage over wall-clock sample span, not active apply timer firing evidence.
