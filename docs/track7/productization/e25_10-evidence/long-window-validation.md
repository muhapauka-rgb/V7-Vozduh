# E25.10 Long-Window Validation

## Result

`long_window_validation_performed=false`

`sustained_go=false`

`no_sample_below_floor=false`

## Reason

The normalized profile passed target-local connectivity validation, including handshake, RX packets, and successful ping through `v7execwg0`.

Long-window validation was not performed because active dedicated target metadata caused runtime checker failures before the target could become a governed movement destination:

- `v7-killswitch-check=FAIL`
- `v7-provisioning-reconcile-check=FAIL`
- missing `v7execwg0` NAT/MSS integration
- readiness helper rejected the target due missing diagnose/load/quality state and execution-only metadata semantics

The metadata row and active interface were rolled back immediately to restore clean runtime state.

## Decision

Do not fake sustained GO. The profile is usable, but first movement is still blocked by execution-target integration, not by peer connectivity.
