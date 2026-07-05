# OpenVPN d2ad7c Capacity Limit Alignment

## Summary

Target channel:

```text
openvpn-1779388847-d2ad7c
```

Problem:

```text
soft_limit=1
hard_limit=2
```

was repeatedly present for this channel in saved production `egress.registry` snapshots and could also be reintroduced by legacy load fallback.

Finding: this was not a canonical per-channel capacity policy for `openvpn-1779388847-d2ad7c`. It came from admin/default/legacy behavior:

- admin draft usage policy materialized blank limits as `soft_limit=1 hard_limit=2`;
- UI placeholders suggested `1/2`;
- admin preview helpers treated missing registry limits as `1/2`;
- legacy `tools/runtime-support/v7-egress-load` defaulted to `V7_LOAD_SOFT_LIMIT=1`, `V7_LOAD_HARD_LIMIT=2` when no explicit environment policy existed.

## Source Of Limit

### Registry snapshots

Saved production snapshots show:

```text
id=openvpn-1779388847-d2ad7c enabled=1 role=GLOBAL_FAST soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0
```

Examples:

- `full_egress_pool_large_capacity_evidence/production_state/egress.registry`
- `awg3_forced_closure_large_escalation_evidence/production_state_before/egress.registry`
- `docs/track7/control-plane/e10_3-evidence/current-state/egress.registry`
- `docs/reports/engineering/live_openvpn_trace_2026-06-30/fixture/state/egress.registry`

### Admin source

Owner: `admin/v7-admin-api`

Previous behavior:

```python
"soft_limit": bounded_int_value(..., 1, ...)
"hard_limit": bounded_int_value(..., 2, ...)
```

Blank operator input became an explicit per-channel cap.

### Legacy load source

Owner: `tools/runtime-support/v7-egress-load`

Previous behavior:

```bash
SOFT_LIMIT="${V7_LOAD_SOFT_LIMIT:-1}"
HARD_LIMIT="${V7_LOAD_HARD_LIMIT:-2}"
```

So even without real policy, any channel with 2+ users could become `HARD_FULL`.

## Canonical Status

Canonical per-channel cap for this channel: not found.

Canonical capacity protection still exists through:

- dynamic autoswitch load policy;
- explicit registry `capacity` / `capacity_users`;
- explicit registry `soft_limit` / `hard_limit` when intentionally set;
- explicit `V7_LOAD_SOFT_LIMIT` / `V7_LOAD_HARD_LIMIT`;
- existing planner/load gates;
- existing authority/restore/verification gates.

Classification:

```text
STALE_DEFAULT / ACCIDENTAL_ADMIN_DEFAULT
```

## Files Changed

### `admin/v7-admin-api`

Changed:

- blank `soft_limit` / `hard_limit` no longer materialize as `1/2`;
- `0` clears an explicit per-channel limit;
- registry serialization omits empty limits;
- admin preview helper treats missing registry limit as no per-channel cap, not legacy `1/2`;
- UI placeholders changed from `1/2` to `pool default` / `not capped`;
- UI capacity labels show `pool default` / `not capped` when no explicit cap exists.

### `tools/runtime-support/v7-egress-load`

Changed:

- default legacy load fallback is now uncapped:

```bash
SOFT_LIMIT=0
HARD_LIMIT=0
```

- `HARD_FULL` / `SOFT_FULL` are emitted only when explicit env limits are greater than zero.
- `V7_STATE_DIR` is now honored for testability and consistency with other runtime-support tools.

### Tests

Added:

- `tests/unit/test_admin_egress_capacity_policy.py`
- `tests/unit/test_v7_egress_load_policy.py`

## Validation

Commands run:

```bash
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile admin/v7-admin-api tests/unit/test_admin_egress_capacity_policy.py tests/unit/test_v7_egress_load_policy.py
bash -n tools/runtime-support/v7-egress-load
python3 -m unittest tests.unit.test_admin_egress_capacity_policy tests.unit.test_v7_egress_load_policy tests.unit.test_admin_registry_views tests.unit.test_operator_observability
```

Result:

```text
25 tests PASS
```

Local behavioral proof:

- blank admin policy serializes no `soft_limit` / `hard_limit`;
- explicit `8/12` is preserved;
- explicit `0/0` clears the cap;
- missing registry limit returns `0`, not fallback `2`;
- legacy load with no env cap reports `OK` for 3 users;
- legacy load with explicit env `1/2` still reports `HARD_FULL`.

## Production State Note

No production users were moved.

Runtime automation was not enabled.

Authority was not expanded.

This workspace does not contain live `/opt/v7/egress/state`, and authenticated production API access was not used. Therefore this patch prevents reintroduction of the artificial cap and changes effective behavior after deploy/restart, but it does not directly mutate the current live `egress.registry` in this local run.

If the production registry still contains:

```text
soft_limit=1 hard_limit=2
```

for `openvpn-1779388847-d2ad7c`, the existing admin/registry owner must remove those two fields or set them to `0` through the approved production update process. After this patch, `0` and blank mean no explicit per-channel cap.

## New Effective Capacity

For `openvpn-1779388847-d2ad7c`:

```text
explicit per-channel soft_limit: none
explicit per-channel hard_limit: none
effective capacity: dynamic pool policy or explicit canonical capacity policy only
```

## Impact On V7

Artificial per-channel `1/2` limits are no longer created by default.

Capacity protection remains active when a real policy exists:

- explicit registry limits;
- explicit env limits;
- dynamic autoswitch capacity;
- planner/load gates;
- restore/verification/authority gates.

## Canonical Knowledge Changes

NONE.

This is implementation alignment with existing capacity semantics, not a new capacity model.

## Verdict

OPENVPN_CHANNEL_CAPACITY_LIMIT_ALIGNED
