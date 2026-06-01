# Program Z1.5 Runtime Audit

Date: 2026-06-01

## Runtime State

Fresh read-only runtime summary:

- enabled users: `18`
- enabled egress: `7`
- safety status: `ok`
- autoswitch safety freezes: `0`
- autoswitch target blocks: `0`
- egress quarantines: `0`

## Health / Capacity / Trust

Observability groups:

- autoswitch: healthy
- capacity: warm
- channels: unstable
- direct routing: unknown
- routing: degraded
- services: blocked
- trusted RU: unknown

## Recent Drift Evidence

F2 drift:

- candidate held stable: `10.7.0.16`
- target drifted from `awg3` to `awg0`
- both targets were eligible then

Z1 drift:

- target drifted again
- candidate changed from `10.7.0.16` to `10.7.0.10`
- healthy egress total dropped from `2` to `1`
- `awg0` became ineligible due `stability_below_floor`

## Runtime Conclusion

Recent drift includes both target drift and candidate drift. Policy approval can reduce target drift pain, but candidate drift must remain critical unless the policy explicitly approves a candidate class, not a specific user.

