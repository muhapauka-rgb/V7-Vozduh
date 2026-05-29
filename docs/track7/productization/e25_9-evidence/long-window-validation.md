# E25.9 Long Window Validation

## Result

`sustained_go=false`

Long-window validation was not started.

## Reason

No new profile was provided and no target-local connectivity was established. A long-window stability sample without a working target would be meaningless.

## Required Future Gate

After a new profile passes target-local connectivity, collect a 20-30 minute window with:

- target readiness GO;
- no sample below floor;
- selected moves zero;
- hidden movers absent;
- runtime checkers OK;
- target users zero.
