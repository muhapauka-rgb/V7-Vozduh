# P6.A Fail-Closed Certification

Project: V7 Vozduh

Block: P6.A

## Fail-Closed Matrix

| State | Required behavior |
| --- | --- |
| unknown packet | abort |
| missing packet | abort |
| stale packet | abort |
| expired approval | abort |
| invalid approval | abort |
| mismatched users registry hash | abort |
| mismatched egress registry hash | abort |
| mismatched selected moves hash/count | abort |
| candidate current not `1` | abort |
| candidate duplicate/missing/disabled | abort |
| destination missing/disabled/not GO | abort |
| movement budget not `1` | abort |
| allowed users not exactly `10.7.0.11` | abort |
| allowed targets not exactly `amneziawg-exec-20260528-10-8-1-14` | abort |
| autoswitch apply requested | abort |
| policy apply requested | abort |
| broad routing sync requested | abort |
| rollback requested before forward verification | abort |
| replayed approval | abort |

## Certification Boundary

P6.A certifies the design fail-closed model only. It does not certify execution.

## Verdict

- fail_closed_certified=true
- unknown_aborts=true
- missing_aborts=true
- stale_aborts=true
- expired_aborts=true
- invalid_aborts=true
- mismatched_aborts=true
- blocked_aborts=true
