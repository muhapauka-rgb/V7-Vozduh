# E25.9 Quarantine And Offline Safety

## Result

`safe_for_normalization=false`

No new external profile was provided, so no quarantine copy was created.

## Not Performed

- no profile copied;
- no secrets handled;
- no endpoint parsed;
- no hook scan performed on a new profile;
- no normalization candidate selected.

## Reason

The only available profiles are known invalid/dead profiles from E25.7/E25.8 or active/runtime artifacts. Reusing them is forbidden unless the remote peer is repaired and proven by handshake/RX.

## Required Next Input

Operator must provide a new external outbound WireGuard profile in one of the accepted import locations, or explicitly provide a path in the next block.
