# E9.4.4 Clean Gate Failure Analysis

## What Failed

The final E9.4.2 gate was clean, but it was too short:

```text
final_gate_selected_moves=0
immediate_post_restore_movements=0
delayed_post_restore_movements=3
```

The gate validated the state at one instant and the immediate aftermath of restore. It did not validate that the service-signal state would remain clean through multiple apply timer periods.

## Why It Failed

The signal changed from soft/degraded to hard-block after restore:

```text
DOWN_GRACE -> TELEGRAM_DOWN_14S -> selected_moves=3
```

The autoswitch apply timer was active, so the next hard-block cycle was allowed to mutate runtime. The restored apply authority was therefore bounded by `max_failover_per_run`, but not by the canary restore blast-radius model.

## Minimum Future Clean Window

Future restore proof should require all of the following before canary planning resumes:

1. At least `N=3` consecutive planner-only samples with `selected_moves=0`.
2. The samples must span at least two full apply timer intervals.
3. Telegram must remain below hard-block threshold for the whole window.
4. `users.registry` hash must remain stable through the window.
5. No new switch-history/safety incoming entries.
6. Post-apply restore observation must also span at least two full apply timer intervals.
7. Any delayed movement must be classified as autoswitch recovery, outside the canary blast radius.

## Restore Model Implication

The restore model cannot treat immediate `selected_moves=0` as sufficient. It needs a delayed-settle stage:

```text
planner-only clean window
-> apply restore
-> immediate check
-> delayed settle across multiple timer cycles
-> only then mark restore governance live-proven
```

## Verdict

`CLEAN_GATE_WINDOW_TOO_SHORT` is a root governance failure. The autoswitch policy did what it was configured to do once Telegram became hard-blocked; the restore procedure failed to prove stability across enough timer cycles.

