# E9.4.4 Delayed Movement Timeline

Mode: read-only root-cause reconstruction. No runtime mutation was performed by this block.

## Timeline

| Time (UTC) | Event | Evidence |
|---|---|---|
| 2026-05-26 07:17:56 | E9.4.2 final planner-only gate captured. Apply timer still inactive/held. | `docs/track7/control-plane/e9_4_2-evidence/final-planner-only-gate.txt` |
| 2026-05-26 07:17:56 | Latest final gate decision was clean: `selected_moves=[]`, `apply_result.applied=false`, `reason=no_selected_moves`. Older journal lines in the same evidence still showed a previous `telegram_required_telegram_down_14s` decision, but the latest decision was eligible/keep. | `BLOCK_E9_4_2_FRESH_BOUNDED_APPLY_RESTORE_RETRY_REPORT.md` |
| 2026-05-26 07:20:02 | Planner/apply output showed no selected moves: `candidate_moves_total=0`, `selected_moves=0`, `apply_result.reason=no_selected_moves`. Egress `1` was eligible but in `DOWN_GRACE`, not hard-blocked. | `runtime-apply-window-extract.txt` |
| 2026-05-26 07:29:03 | A later timer cycle changed state: `candidate_moves_total=16`, `selected_moves=3`. Egress `1` was rejected with `telegram_required_telegram_down_14s`; Telegram status was `TELEGRAM_DOWN_14S` and `hard_blocked=true`. | `runtime-apply-window-extract.txt` |
| 2026-05-26 07:29:08 | Autoswitch apply recorded three failover movements into `vless`: `10.7.0.5`, `10.0.0.2`, `10.0.0.3`. | `autoswitch-safety.json` excerpts in `post-restore-baseline.txt` and `runtime-journal-restore-window.txt` |
| 2026-05-26 07:29:23 | The next apply/planner output returned to `selected_moves=[]`, `apply_result.reason=no_selected_moves`; moved users were on cooldown/frozen. | `runtime-apply-window-extract.txt` |
| 2026-05-26 07:30-07:35 | Later monitoring remained stable: checks OK, no hidden `v7-routing-sync`, no hidden manual `v7-user-switch`, no further selected moves. | `docs/track7/control-plane/e9_4_3-evidence/monitor-*.txt` |

## Key Finding

The E9.4.2 clean final gate was a valid instant-in-time sample, but it was not a sufficient restore proof. A later timer cycle saw a Telegram hard-block recurrence and applied the normal autoswitch failover path.

## Evidence Summary

```text
clean_gate:
  selected_moves=0
  egress_1_eligible=true
  telegram_status=DOWN_GRACE
  telegram_hard_blocked=false

delayed_apply_cycle:
  candidate_moves_total=16
  selected_moves=3
  egress_1_blocker=telegram_required_telegram_down_14s
  telegram_status=TELEGRAM_DOWN_14S
  telegram_hard_blocked=true

movement_ts:
  2026-05-26T07:29:08.088818+00:00 user_ip=10.7.0.5
  2026-05-26T07:29:08.088941+00:00 user_ip=10.0.0.2
  2026-05-26T07:29:08.088994+00:00 user_ip=10.0.0.3
```

## Verdict

The delayed movement was timer-driven autoswitch apply behavior after restore, not an E9.4.4 mutation and not a hidden manual action.

