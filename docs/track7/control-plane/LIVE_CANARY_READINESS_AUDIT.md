# Live Canary Readiness Audit

Evidence captured read-only on 2026-05-24 around 23:23 MSK. No `v7-user-switch`, `v7-routing-sync`, `v7-users-autoswitch --apply`, policy apply, route mutation, nft mutation, restart, chmod/chown, cleanup, or deploy was executed.

## Read-Only Evidence Sources

- copied runtime state snapshot under `/private/tmp/v7-e2-state`;
- read-only systemd status/timer inspection;
- `v7-killswitch-check`;
- `v7-user-route-check`;
- `v7-provisioning-reconcile-check`;
- `v7-reconcile-check`;
- local planner output from `tools/v7-route-movement-preview`.

## Autoswitch Authority

`v7-users-autoswitch.timer` is active and enabled. The service unit is static/inactive at the sampled instant, but the timer fires every 20 seconds and the service command is:

```text
/usr/local/bin/v7-users-autoswitch --apply
```

This means autoswitch currently has live apply authority. A one-user canary must not proceed while that timer can concurrently move users.

## Current Safety Signals

| Check | Result | Canary meaning |
|---|---:|---|
| Kill switch | OK | Required precondition satisfied at sample time |
| User route check | OK | Current user routing matched registry at sample time |
| Provisioning reconcile check | OK | Provisioning contract matched at sample time |
| Reconcile check | FAIL, 11 missing `ip rule lookup table` errors | NO-GO until explained or resolved |
| Autoswitch safety state | most enabled users have `switches_1h=2`, `switches_24h=10`, penalty until 2026-05-25T02:02-02:05Z | NO-GO for live canary |
| Egress load | operator status `warm`; active users 16; healthy channels 1 | high caution |
| Trusted RU state | diagnostic from 2026-05-22, decision from 2026-05-07 | stale/Gosuslugi-sensitive |

## Egress Snapshot

- `awg0`: enabled, 15 users, current majority path, route checks OK, quality near lower threshold.
- `awg3`: enabled, 0 users, load OK, but 1h avg/min quality below policy floor.
- `vless`: enabled, good speed, but stability below policy threshold and state reports soft-full.
- `1`: enabled, high quality, already has 1 user and route-class exclusions for `TRUSTED_RU_SENSITIVE,DIRECT_RU`.
- `openvpn-1779388847-d2ad7c` and `wireguard-1779454504-c43409`: enabled but diagnostic severity `SUSPECT`.

## Verdict

Current one-user canary status is **NO-GO**.

Primary blockers are active autoswitch apply authority, anti-flap penalties across enabled users, `v7-reconcile-check` failure, target egress quality ambiguity, and stale Trusted RU decision evidence.
