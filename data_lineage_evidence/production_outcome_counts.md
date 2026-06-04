# Production Outcome Counts

Read-only production inspection via SSH.

## Direct Outcome And Audit Files

| File | Exists | Lines | Bytes |
| --- | --- | ---: | ---: |
| `/opt/v7/events/switch-history.jsonl` | true | 2792 | 517129 |
| `/opt/v7/audit/audit.jsonl` | true | 4140 | 1840159 |
| `/opt/v7/audit/operator-execution-audit.jsonl` | true | 16 | 12871 |
| `/opt/v7/audit/operator-runtime-governance-actions.jsonl` | true | 1 | 1392 |
| `/opt/v7/egress/state/closure-records.jsonl` | true | 0 | 0 |
| `/opt/v7/egress/state/execution-events.jsonl` | true | 0 | 0 |
| `/opt/v7/egress/state/egress-history.jsonl` | true | 120 | 54478 |

Direct outcome/audit count used for final verdict:

`2792 + 4140 + 16 + 1 + 0 + 0 = 6949`

## Term Counts

| File | rollback | apply | applied | selected_move | terminal_state | failed | error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| switch-history | 40 | 0 | 0 | 0 | 0 | 0 | 0 |
| audit.jsonl | 127 | 3057 | 15 | 38 | 17 | 31 | 50 |
| operator-execution-audit | 3 | 12 | 0 | 5 | 0 | 0 | 8 |
| governance actions | 1 | 1 | 0 | 3 | 0 | 0 | 0 |

## Service And Channel History

Observed service matrix refresh event files:

- 20260520: 15
- 20260521: 95
- 20260522: 92
- 20260523: 93
- 20260524: 93
- 20260525: 92
- 20260526: 93
- 20260527: 93
- 20260528: 93
- 20260529: 93
- 20260530: 92
- 20260531: 93
- 20260601: 93
- 20260602: 95
- 20260603: 93
- 20260604: 48

Total service refresh history lines: 1363.

Observed Telegram sentinel event files total: 121468 lines.

## Conclusion

Outcome data exists. The blocker is not a blank production history. The blocker is incomplete consumption and normalization into RI6 actual outcome inputs.
