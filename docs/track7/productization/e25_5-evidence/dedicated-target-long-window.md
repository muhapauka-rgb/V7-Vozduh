# E25.5 Dedicated Target Long Window

## Result

`dedicated_target_sustained_go=false`

No long-window observation was collected because no dedicated execution target exists.

## Required Future Window

After provisioning:

- collect 20-30 minutes minimum;
- at least 20 samples or documented cadence;
- every sample must include readiness, selected target, avg/min Mbps, stability, latency/loss if available, users count, diagnose, load, interface state;
- no sample below floor;
- no hidden movers;
- selected_moves stays zero.

## Flags

- `samples_count=0`
- `sustained_go=false`
- `no_sample_below_floor=false`
- `quality_spikes_detected=unknown`
