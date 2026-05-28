# E9.4.6 Post-Restore Settle Analysis

Mode: read-only observation.

## Scope

E9.4.6 did not start or stop timers. The apply timer was already active from E9.4.2 before this block began.

This analysis uses the fresh E9.4.6 live observation window:

- current authority snapshot: `docs/track7/control-plane/e9_4_6-evidence/current-authority-snapshot.txt`
- raw settle samples: `docs/track7/control-plane/e9_4_6-evidence/fresh-settle-samples-combined.txt`
- hash-stability window: `docs/track7/control-plane/e9_4_6-evidence/fresh-settle-hash-window.txt`
- normalized checker samples: `docs/track7/control-plane/e9_4_6-evidence/settle-samples/`
- machine verdicts: `docs/track7/control-plane/e9_4_6-evidence/fresh-restore-settle.json` and `docs/track7/control-plane/e9_4_6-evidence/fresh-post-restore-settle.json`

## Fresh Window

```text
sample_A=2026-05-26T10:24:28Z
sample_B=2026-05-26T10:25:01Z
sample_C=2026-05-26T10:25:36Z
samples_count=3
samples_span_seconds=68
apply_timer_intervals_covered=3.4
```

## Stability

```text
users.registry_hash=d73974c8547fac49fe02f70a64b64ed422157dc94ccf75a030737e2163de1b6d
egress.registry_hash=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
users.registry_stable=true
egress.registry_stable=true
switch_history_latest=32513:1779789200
```

The switch-history marker stayed stable across the three hash samples. No new movement was observed during the fresh E9.4.6 settle window.

## Autoswitch State

```text
selected_moves_by_sample=[0,0,0]
movement_count_by_sample=[0,0,0]
telegram_hard_blocked_by_sample=[false,false,false]
egress_1_eligible_by_sample=[true,true,true]
hidden_movers_observed=false
```

Telegram remained degraded/advisory for egress `1` in the planner output, but not hard-blocked. Egress `1` remained globally eligible.

## Runtime Checks

All samples reported:

```text
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

## Classification

```text
current_restore_settle_status=GO
new_delayed_movements_observed=false
restore_governance_live_proven=true_for_fresh_settle_window
```

Historical delayed movement from E9.4.3/E9.4.4 remains classified separately. E9.4.6 proves only that the current fresh settle window is clean and that restore governance can now return to approval-packet planning. It does not authorize canary execution.
