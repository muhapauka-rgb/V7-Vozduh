# A4 Bounded Collection Stop On Verification Failure

## Summary

A4 продолжен по уже согласованному bounded authority envelope, без packet-by-packet approval.

## Action Performed

Executed existing owner:

`tools/v7-governed-canary-dry-run-cycle --execute-a4-bounded-evidence-collection`

Limit at start: `66` remaining A4 evidence outcomes.

## Objective Observations

| Metric | Value |
| --- | --- |
| Final verdict | `A4_BOUNDED_EVIDENCE_COLLECTION_STOPPED` |
| Stop reason | `transaction_verification_failed` |
| Transactions attempted | `3` |
| Successful verified outcomes | `2` |
| Runtime automation | `NO` |
| Authority expansion | `NO` |
| New owner/backlog/runtime path | `NO` |

## Outcomes

| User | Move | Verification | Rollback |
| --- | --- | --- | --- |
| `10.7.0.22` | `vless -> awg3` | `PASS` | `NOT_REQUIRED` |
| `10.7.0.23` | `vless -> awg3` | `PASS` | `NOT_REQUIRED` |
| `10.7.0.24` | `vless -> awg3` | `FAIL` | `ROLLBACK_COMPLETED` to `vless` |

## Progress

| Section | Before | After |
| --- | --- | --- |
| A4 evidence | `90 / 156 = 57.7%` | `93 / 156 = 59.6%` |
| Missing A4 evidence | `66 / 156 = 42.3%` | `63 / 156 = 40.4%` |
| Production Maturity | `24.0%` | `24.0%` |

## Engineering Conclusions

The bounded authority model worked as intended: it did not ask for packet approval, executed one-user transactions, stopped on the first failed verification gate, and rollback succeeded.

The current stop is not authority. It is `VERIFY_FAILED_ROLLBACK_COMPLETED`.

## Canonical Knowledge

No new owner, backlog item, runtime path, governance layer, or authority model was created.

## Evidence

Local result artifact: `/private/tmp/v7_a4_bounded_collection_result.json`.

## Next Step

Analyze the failed verification for `10.7.0.24 vless -> awg3` through existing apply/verify/A4 owners before resuming bounded collection.

## Re-audit Rule

Do not re-audit packet approval for A4 unless bounded collection again requests packet-by-packet approval inside the already approved A4 envelope.
