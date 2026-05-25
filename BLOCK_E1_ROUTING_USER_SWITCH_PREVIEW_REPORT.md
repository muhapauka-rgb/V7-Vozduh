# V7 Vozduh Block E1 Report

## Routing/User-Switch Static Tests & Non-Mutating Preview Model

Block E1 created a repo-only, non-mutating foundation for future one-user canary work. No live routing sync, user-switch, autoswitch apply, route change, ip rule change, nft change, kill switch change, service restart, deploy, chmod/chown, or runtime file mutation was performed.

## 1. What Changed

Added a separate read-only planner instead of modifying dangerous runtime tools:

```text
tools/v7-route-movement-preview
```

Added fixture-based tests:

```text
tests/unit/test_v7_route_movement_preview.py
tests/unit/fixtures/route_movement/
```

Added governance docs:

```text
docs/track7/control-plane/ROUTE_MOVEMENT_PREVIEW_SCHEMA.md
docs/track7/control-plane/ONE_USER_CANARY_READINESS.md
```

Updated governance docs:

```text
docs/track7/control-plane/SAFE_EXECUTION_MODEL.md
docs/track7/control-plane/CONTROL_PLANE_TEST_PLAN.md
docs/track7/control-plane/USER_SWITCH_GOVERNANCE.md
docs/track7/control-plane/ROUTING_SYNC_GOVERNANCE.md
```

Updated checker:

```text
tools/v7-control-plane-governance-check
```

## 2. Tests Added

`tests.unit.test_v7_route_movement_preview` covers:

- user switch one-user preview;
- user not found;
- target egress missing;
- target egress disabled;
- same-egress no-op;
- duplicate user forbidden;
- routing-sync enabled/disabled user handling;
- routing-sync duplicate users;
- missing egress;
- invalid table IDs;
- invalid user IPs;
- routing-sync no-op when no enabled users exist;
- CLI JSON output with `mutation=false`.

## 3. Fixtures Added

```text
tests/unit/fixtures/route_movement/users.registry
tests/unit/fixtures/route_movement/egress.registry
tests/unit/fixtures/route_movement/users_duplicate.registry
tests/unit/fixtures/route_movement/users_invalid.registry
tests/unit/fixtures/route_movement/users_disabled_only.registry
```

All fixtures are local repo files. Tests do not read `/opt/v7`, `/etc/v7`, `/etc/wireguard`, live route tables, or nftables.

## 4. Was v7-routing-sync Changed?

No.

`v7-routing-sync` remains untouched. It is still classified as datapath mutation and cannot be the first live mutation.

## 5. Was v7-user-switch Changed?

No.

`v7-user-switch` remains untouched. Future live use still requires explicit approval.

## 6. Separate Planner

Planner:

```text
tools/v7-route-movement-preview
```

Modes:

```text
tools/v7-route-movement-preview user-switch --users-registry <file> --egress-registry <file> --user-ip <ip> --to-egress <egress>
tools/v7-route-movement-preview routing-sync --users-registry <file> --egress-registry <file>
```

Planner guarantees by construction:

```text
mutation=false
runtime_commands_executed=false
no calls to v7-user-switch
no calls to v7-routing-sync
no calls to ip/nft/systemctl
```

## 7. Preview JSON Example

User switch preview:

```json
{
  "action": "user_switch_preview",
  "mutation": false,
  "runtime_commands_executed": false,
  "user": "10.7.0.10",
  "from_egress": "vless",
  "to_egress": "awg3",
  "table": "110",
  "target_interface": "awg3",
  "routes_would_change": [
    {
      "command": "ip route replace default dev awg3 table 110"
    }
  ],
  "rollback": {
    "type": "switch_back",
    "previous_egress": "vless",
    "command": "v7-user-switch 10.7.0.10 vless"
  },
  "blast_radius": "one_user",
  "requires_approval": true
}
```

Routing-sync preview reports `blast_radius=all_enabled_users_in_registry` and lists each `ip route replace`, `ip rule del`, and `ip rule add` command that would be needed, without running any of them.

## 8. Canary Readiness Criteria

Documented in:

```text
docs/track7/control-plane/ONE_USER_CANARY_READINESS.md
```

Minimum gate:

- preview JSON exists;
- preview has `mutation=false`;
- preview has no `errors`;
- previous egress captured;
- target egress healthy and enabled;
- kill switch OK before;
- route check OK before;
- rollback command prepared;
- blast radius exactly one user;
- post-checks and rollback checks defined.

## 9. Verification

Expected verification commands:

```text
python3 -m unittest tests.unit.test_v7_route_movement_preview
tools/v7-run-tests
tools/v7-control-plane-governance-check --pretty
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty
PYTHONPYCACHEPREFIX=/private/tmp python3 -m py_compile admin/v7-admin-api admin_core/*.py tools/v7-release-lineage-check tools/v7-runtime-repo-diff tools/v7-control-plane-governance-check tools/v7-route-movement-preview
```

`tools/v7-route-movement-preview` is a Python executable, so shell `bash -n` is not applicable to it. No existing shell runtime tool was changed.

## 10. Runtime Mutation Verdict

```text
Runtime mutation: NO
Live deploy: NO
v7-routing-sync executed: NO
v7-user-switch executed: NO
v7-users-autoswitch --apply executed: NO
ip route/ip rule/nft mutation: NO
```

## 11. Can V7 Move To One-User Canary Now?

Not automatically.

The repo now has the static tests, preview schema, planner, and readiness checklist needed before canary. A future canary still needs separate live approval, a named user, live pre-checks, rollback readiness, and confirmation that autoswitch is not concurrently moving users.

## 12. Remaining Blockers

- `v7-routing-sync` still has no native no-write mode and remains registry-wide mutation.
- `v7-user-switch` still mutates live route table before registry rewrite.
- Autoswitch apply path can call user-switch repeatedly.
- Live kill-switch and route checks were not run in this block.
- No one-user canary has been executed.
