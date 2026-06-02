# P2.5 Verification Preview Expansion

## Result

verification_preview_expanded=true

## Change

P2.5 includes the existing verification preview inside outcome preview, so the operator can see what success would mean for the simulated contract.

## Covered

- approved users moved;
- no extra users moved;
- route tables match expected target;
- required services available;
- runtime checkers OK;
- blast radius intact.

## Failure Meaning

Any future failure in these checks would keep execution blocked or require rollback in later certified stages. P2.5 does not execute those checks live.
