# E25.7 Dedicated Target Long Window

## Result

- `long_window_collected=false`
- `sustained_go=false`
- `no_sample_below_floor=false`
- `quality_spikes_detected=unknown`
- `target_users_zero=true`
- `selected_moves_zero=true`
- `hidden_movers_absent=true`

## Reason

The long-window validation was intentionally not run. The normalized interface failed target-local connectivity before the long window:

- `ping_exit=1`
- `3 packets transmitted, 0 received`
- WireGuard receive bytes remained `0 B`

Running a 20-30 minute stability window after basic connectivity failure would not add meaningful safety evidence.

