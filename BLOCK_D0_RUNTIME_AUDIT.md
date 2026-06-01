# Block D0 Runtime Audit

Project: V7 Vozduh

Block: D0 - Execution Cohort Decision Program

Date: 2026-06-01

## Execution Target

- Target: `amneziawg-exec-20260528-10-8-1-14`
- Interface: `v7execwg0`
- Current count: `10`
- Soft limit: `10`
- Hard limit: `10`
- Headroom: `0`

## Route Stability

All execution cohort users have route tables pointing to `v7execwg0`:

- `10.7.0.2 table=1000`
- `10.7.0.3 table=1001`
- `10.7.0.4 table=1002`
- `10.7.0.5 table=1003`
- `10.7.0.6 table=1004`
- `10.7.0.8 table=1006`
- `10.7.0.11 table=1009`
- `10.7.0.12 table=1010`
- `10.7.0.14 table=1012`
- `10.7.0.15 table=1013`

Each table has:

```text
default dev v7execwg0 scope link
```

## Checker Outputs

- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

## Runtime Risk

The execution target is full. It is not suitable for future expansion or autoswitch testing with additional users.

## Verdict

Runtime audit complete.

