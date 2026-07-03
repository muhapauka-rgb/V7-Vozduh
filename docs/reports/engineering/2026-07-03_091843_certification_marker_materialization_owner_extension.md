# Certification Marker Materialization Owner Extension

Timestamp: 2026-07-03T09:18:43+0700

## Summary

After the controlled-certification egress guard was deployed, the next Certification Program blocker was marker materialization.

Search proved that no existing production writer owned:

- `controlled_certification_source=1`
- `certification_user=1`
- `certification_group=<value>`

Manual registry editing would violate the Controlled Production Certification Program.

The required resolution was converted into the next Engineering Mission and implemented by extending the existing egress lifecycle owner `tools/v7-egress-set-state`.

## Prior Deploy Evidence

Commit deployed:

```text
20b888aeecba6ac4326a97cd9ff6c2437c2553a5
```

Safe deploy result:

```text
PASS
```

Post-deploy convergence:

```text
local=20b888aeecba6ac4326a97cd9ff6c2437c2553a5
github=20b888aeecba6ac4326a97cd9ff6c2437c2553a5
production=20b888aeecba6ac4326a97cd9ff6c2437c2553a5
runtime_action_status=READY_FOR_RUNTIME_ACTION
final_verdict=PASS
```

Deployed hashes:

```text
/usr/local/bin/v7-egress-guard      a27f786bca990a86f7473e700f46843a30e8ef14d7ea7f4f10c063b0fc47cc31
/usr/local/bin/v7-egress-set-state  20febee99b63187fd60c392076f1e60b34fea374f26894793968b1d73d59bf99
```

## Implemented Owner Extension

Existing owner:

```text
tools/v7-egress-set-state
```

New action:

```text
v7-egress-set-state <egress_id> certification-scope --certification-users ip1,ip2 --certification-group <group> [--apply]
```

Behavior:

- validates that every requested certification user is enabled and currently assigned to the requested source;
- dry-run mode reports intended marker writes and mutates nothing;
- apply mode backs up `egress.registry` and `users.registry`;
- marks the source with `controlled_certification_source=1`;
- marks selected users with `certification_user=1`;
- attaches `certification_group=<group>`;
- writes existing audit event `egress_certification_scope` when `v7-audit-log` is available;
- performs no routing mutation, no interface down/up, no Runtime Apply, and no user movement.

## Safety Preserved

Ordinary lifecycle behavior is unchanged.

`maintenance|disabled` still blocks assigned enabled users unless:

1. the source is explicitly marked as a controlled certification source;
2. every enabled assigned user on that source is marked as a certification user or group member;
3. the operator explicitly invokes `--controlled-certification`.

## Tests

Command:

```text
python3 -m unittest tests.unit.test_v7_egress_lifecycle_guard tests.unit.test_v7_sync_tools
```

Result:

```text
Ran 34 tests in 7.104s
OK
```

Command:

```text
bash -n tools/runtime-support/v7-egress-guard tools/v7-egress-set-state tools/v7-safe-deploy
```

Result:

```text
PASS
```

Command:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile tools/v7_sync_lib.py tests/unit/test_v7_egress_lifecycle_guard.py tests/unit/test_v7_sync_tools.py
```

Result:

```text
PASS
```

## Production Impact

Production marker materialization performed: `NO`

Deploy performed for this marker extension: `NO`

Users moved: `0`

Routing changed: `NO`

## Next Required Action

Commit, push, and safe-deploy the marker materialization extension.

Then resume Phase 4 by using the existing deployed owner to materialize certification markers for:

```text
source=wireguard-1779454504-c43409
users=10.7.0.16..10.7.0.26
group=medium-batch
```

After marker materialization, run:

```text
v7-egress-set-state wireguard-1779454504-c43409 maintenance --controlled-certification --apply
```

only through the existing approved production procedure, then resume the governed MEDIUM_BATCH certification mission.

