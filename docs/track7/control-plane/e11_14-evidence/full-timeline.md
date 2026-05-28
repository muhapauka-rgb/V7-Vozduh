# BLOCK E11.14 Full Post-E11.13 Timeline

timeline_reconstructed=true
timezone_note=local timestamps are Europe/Moscow (+03:00); switch-history timestamps are UTC.

## Timeline

| Time | Event | Evidence |
| --- | --- | --- |
| 2026-05-27T13:12:48+03:00 | E11.13 rollback user 10.7.0.11 from WireGuard to target 1. | `switch-history`: 2026-05-27T10:12:48.953810Z |
| 2026-05-27T13:12:49+03:00 | E11.13 rollback user 10.7.0.12 from WireGuard to target 1. | `switch-history`: 2026-05-27T10:12:49.408242Z |
| 2026-05-27T13:13:33+03:00 | Planner timer restored; apply timer still held. | `e11_13-evidence/planner-restore.txt` |
| 2026-05-27T13:13:55+03:00 | Restore-settle sampling started. | `e11_13-evidence/restore-settle-raw.txt` |
| 2026-05-27T13:13:55-13:15:04+03:00 | Restore-settle gate passed: 3 samples, 3.45 apply intervals, selected_moves=[0,0,0], users hash stable. | `e11_13-evidence/restore-settle.txt`, `restore-settle.json` |
| 2026-05-27T13:16:37+03:00 | Apply timer restored after gate GO. | `e11_13-evidence/apply-restore.txt` |
| 2026-05-27T13:16:38+03:00 | First apply timer run after restore: selected_moves=0, no apply. | `e11_14-evidence/journals/users-autoswitch-apply-window-reconstructed.json` |
| 2026-05-27T13:17:00+03:00 | Apply timer run: selected_moves=0, no apply. | same |
| 2026-05-27T13:17:23+03:00 | Apply timer run: selected_moves=0, no apply. | same |
| 2026-05-27T13:17:43+03:00 | Apply timer run: selected_moves=0, no apply. | same |
| 2026-05-27T13:18:04+03:00 | Apply timer run: selected_moves=0, no apply. | same |
| 2026-05-27T13:18:24+03:00 | Fresh apply timer recompute found target 1 ineligible for Telegram hard signal (`telegram_required_telegram_down_14s`), candidate_moves=5, selected_moves=3. | same, `apply-window-selected-moves-detail.txt` |
| 2026-05-27T13:18:25+03:00 | Autoswitch moved 10.7.0.9 from 1 to awg0. | `switch-history` |
| 2026-05-27T13:18:27+03:00 | Autoswitch moved 10.7.0.10 from 1 to awg0. | `switch-history` |
| 2026-05-27T13:18:29+03:00 | Autoswitch moved 10.7.0.13 from 1 to awg0. | `switch-history` |
| 2026-05-27T13:18:46-13:21:13+03:00 | Subsequent apply timer runs selected_moves=0. | `users-autoswitch-apply-window-reconstructed.json` |
| 2026-05-27T13:21:31+03:00 | Emergency containment: apply timer stopped; planner left active. | `e11_13-evidence/emergency-containment-apply-held.txt` |
| 2026-05-27T13:43:29+03:00 | E11.14 fresh runtime snapshot: apply timer inactive, planner active, selected_moves=0. | `e11_14-evidence/full-runtime-snapshot.txt` |
| 2026-05-27T13:51:51+03:00 | E11.14 bounded deploy: autoswitch restore barrier support installed, backup created. | `e11_14-evidence/runtime-fix-deploy.txt` |
| 2026-05-27T13:52:27+03:00 | Restore barrier TTL refreshed for 24h containment; apply timer still inactive. | `e11_14-evidence/runtime-fix-barrier-refresh.txt` |
| 2026-05-27T13:53:07-13:54:25+03:00 | Post-fix samples A/B/C stable: users hash unchanged, selected_moves=0, checkers OK, no hidden movers. | `e11_14-evidence/post-fix-stability-samples.txt` |

## Verdict

timeline_verdict=COMPLETE
stale_selected_moves_supported=false
fresh_apply_recompute_supported=true
delayed_movement_source=v7-users-autoswitch.timer
manual_autoswitch_apply_observed=false
