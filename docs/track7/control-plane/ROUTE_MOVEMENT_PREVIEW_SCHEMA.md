# Route Movement Preview Schema

All route/user movement must produce a non-mutating preview before any canary or apply. The preview is an evidence object, not permission to mutate runtime.

## Common Fields

```json
{
  "schema_version": 1,
  "action": "user_switch_preview",
  "mutation": false,
  "runtime_commands_executed": false,
  "requires_approval": true,
  "errors": [],
  "warnings": [],
  "blast_radius": "one_user"
}
```

Required invariant:

```text
mutation=false
runtime_commands_executed=false
```

Any preview tool that calls `ip`, `nft`, `systemctl`, `v7-user-switch`, `v7-routing-sync`, or `v7-users-autoswitch` is not a preview tool.

## User Switch Preview

Example:

```json
{
  "schema_version": 1,
  "action": "user_switch_preview",
  "mutation": false,
  "runtime_commands_executed": false,
  "requires_approval": true,
  "user": "10.7.0.10",
  "from_egress": "vless",
  "to_egress": "awg3",
  "table": "110",
  "target_interface": "awg3",
  "blast_radius": "one_user",
  "files_would_change": [
    {"path": "users.registry", "operation": "rewrite_user_current_via_temp_and_mv"},
    {"path": "user-10.7.0.10.assign", "operation": "write_assignment_file"}
  ],
  "routes_would_change": [
    {
      "type": "route_replace_default",
      "user": "10.7.0.10",
      "table": "110",
      "dev": "awg3",
      "command": "ip route replace default dev awg3 table 110"
    }
  ],
  "ip_rules_would_change": [],
  "rollback": {
    "type": "switch_back",
    "previous_egress": "vless",
    "command": "v7-user-switch 10.7.0.10 vless"
  }
}
```

## Routing Sync Preview

Routing sync preview is registry-wide. It must show every enabled user it would touch.

Required fields:

- `users_registry`;
- `egress_registry`;
- `users`;
- `routes_would_change`;
- `ip_rules_would_change`;
- `rollback.status`.

Rollback is not ready unless there is a registry backup and route snapshot. Therefore the default routing-sync preview rollback is:

```json
{
  "type": "registry_restore_then_resync",
  "status": "not_ready_without_registry_backup_and_route_snapshot"
}
```

## Error Semantics

If `errors` is non-empty:

- no canary;
- no apply;
- no routing sync;
- no autoswitch.

Expected error codes include:

```text
user_not_found
duplicate_user
target_egress_missing
target_egress_disabled
target_interface_missing
invalid_user_ip
invalid_table
egress_missing
egress_interface_missing
```

