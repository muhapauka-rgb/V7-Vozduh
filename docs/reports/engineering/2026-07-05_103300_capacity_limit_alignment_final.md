# V7 Capacity Limit Alignment Final

Date: 2026-07-05

## Summary

The `vless` channel still showed `Лимит назначений достигнут` because production `egress-load.state` was still generated from a static global load policy:

- `V7_LOAD_SOFT_LIMIT=1`
- `V7_LOAD_HARD_LIMIT=2`

This was not a `vless`-only limit and not a per-channel registry cap. The same artificial cap affected `awg0`, `awg3`, and `openvpn-1779388847-d2ad7c`.

## Source Of Limit

Source chain:

`/etc/v7/policy.json`
-> `/usr/local/bin/v7-policy-env`
-> `/usr/local/lib/v7-egress-lib::v7_load_policy_env`
-> `/usr/local/bin/v7-egress-load`
-> `/opt/v7/egress/state/egress-load.state`
-> Admin UI load card.

Root source:

`/etc/v7/policy.json` had:

```json
"load": {
  "mode": "dynamic",
  "soft_limit": 1,
  "hard_limit": 2
}
```

## Classification

The `1/2` values were stale static defaults inside an otherwise dynamic load policy. They acted as an artificial per-channel assignment cap.

They were not canonical per-channel capacity limits.

## Changes Made

Repository:

- `tools/v7_sync_lib.py`: added existing runtime-support owner `tools/runtime-support/v7-egress-load` to the safe deploy allowlist so production receives the corrected load-state producer.

Production config:

- `/etc/v7/policy.json`: changed `load.soft_limit` from `1` to `0`.
- `/etc/v7/policy.json`: changed `load.hard_limit` from `2` to `0`.

Backup created:

- `/etc/v7/policy.json.backup.capacity-limit-align-20260705T033143Z`

No users were moved.

Runtime automation was not enabled.

Authority was not expanded.

## Validation

Unit tests:

- `python3 -m unittest tests.unit.test_admin_egress_capacity_policy tests.unit.test_v7_egress_load_policy tests.unit.test_admin_registry_views tests.unit.test_operator_observability`
- Result: PASS, 25 tests.

Safe deploy:

- `tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --restart-admin-if-changed --json`
- Result: PASS.

Truth:

- `tools/v7-truth-check --all --json`
- Result: PASS.

Convergence:

- `tools/v7-convergence-status --json`
- Result: PASS / ALIGNED.

Production load-state after refresh:

```text
vless_users=59
vless_soft_limit=0
vless_hard_limit=0
vless_load_status=OK

awg0_users=10
awg0_soft_limit=0
awg0_hard_limit=0
awg0_load_status=OK

awg3_users=6
awg3_soft_limit=0
awg3_hard_limit=0
awg3_load_status=OK

openvpn-1779388847-d2ad7c_users=0
openvpn-1779388847-d2ad7c_soft_limit=0
openvpn-1779388847-d2ad7c_hard_limit=0
openvpn-1779388847-d2ad7c_load_status=OK
```

## Impact

The UI should no longer show `vless` as overloaded only because it has more than two assigned users.

Load protection is not removed globally as a concept:

- dynamic policy fields remain in `/etc/v7/policy.json`;
- explicit future policy limits can still be applied;
- service, readiness, stability, movement protection, authority, restore barrier, verification, rollback, and automation gates are unchanged.

## Canonical Knowledge Changes

NONE.

## Verdict

OPENVPN_CHANNEL_CAPACITY_LIMIT_ALIGNED

