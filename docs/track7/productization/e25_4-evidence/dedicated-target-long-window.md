# E25.4 Dedicated Target Long Window

## Result

`dedicated_target_long_window_collected=false`

No dedicated execution-only target exists yet, so a dedicated-target stability window could not be collected.

## Existing WireGuard Reference

The existing `wireguard-1779454504-c43409` target was already observed in E25.3:

- 16 samples over about 15 minutes
- 16/16 GO
- `min_mbps` range `16.81` to `19.54`
- `stability` range `0.655310` to `0.771378`

But E25.2 also proved the same target can fall to:

- `min_mbps=4.61`
- `stability≈0.30`

Therefore the existing WireGuard target cannot substitute for a dedicated execution-only target.

## Required Future Window

After provisioning a new dedicated execution-only target, collect:

- 20-30 minutes minimum;
- sequential samples every 60s or faster;
- target readiness verdict;
- avg/min Mbps;
- stability;
- load users;
- registry users;
- diagnose state;
- selected target result;
- hidden movers;
- selected_moves.

Success criteria:

- sustained GO;
- no readiness oscillation;
- no quality floor drops;
- zero users throughout;
- governance reservation intact.
