# Engineering Report: A4 bounded collection outcome

## Summary

A4 bounded evidence collection continued through existing governed transaction owners. One real governed no-rollback outcome was recorded.

## Action Performed

Ran production A4 bounded evidence collection with the existing `tools/v7-governed-canary-dry-run-cycle` owner.

## Objective Observations

- Successful outcome: `10.7.0.25 vless -> awg3`.
- Apply: `YES`.
- Verification: `PASS`.
- Rollback: `NOT_REQUIRED`.
- Users moved: `1`.
- Runtime automation: `NO`.
- Authority expansion: `NO`.
- Second in-run candidate stopped safely as `duplicate_transaction_candidate` before lease, restore barrier, apply, or user movement.

## Engineering Conclusions

The bounded collection path worked as intended for the first transaction. The duplicate guard protected the second transaction before mutation.

## Impact

A4 representative evidence increased from `93 / 156` to `94 / 156`.

## Capability Progress

- A4: `60.3%` representative candidate outcome coverage.
- Missing candidate outcomes: `62`.
- Runtime enablement state: `GOVERNED_ONLY`.

## Backlog Progress

A4 remains `IN_PROGRESS`.

## Production Maturity

Production Maturity remains `24.0%` until A4 certification criteria are satisfied.

## Canonical Knowledge

No new durable canonical knowledge discovered. Existing duplicate guard and terminal outcome classification rules remain valid.

## Evidence

- Production inventory: `candidate_outcomes_consumed=94`, `candidate_count=156`, `missing_candidate_outcomes=62`.
- Truth: `PASS`.
- Convergence: `ALIGNED`.

## Next Step

Continue A4 bounded evidence collection under the existing approved envelope. Do not request packet-by-packet approval.

## Re-audit Rule

Re-audit only if duplicate selection repeatedly prevents new evidence, terminal classification regresses, or production evidence contradicts current A4 behavior.
