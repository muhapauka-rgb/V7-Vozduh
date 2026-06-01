# DEPLOY A Truth Source Audit

## Truth Sources

| Domain | Truth Source | Handling |
| --- | --- | --- |
| Code | GitHub `v7-next` at `12e51a5ad4a6c34b09e37c9343d7ee78cb7678d6` | deployed selected code files only |
| Runtime state | server `/opt/v7/egress/state` | preserved, not copied from local |
| Users | server `/opt/v7/egress/state/users.registry` | preserved, hash checked before/after |
| Channels | server `/opt/v7/egress/state/egress.registry` | preserved, hash checked before/after |
| Logs | server-owned logs and events | not overwritten |
| Secrets/private config | server-owned files under `/etc`, `/root`, `/opt/v7` | not copied into Git, not replaced |
| Client profiles | server-owned profile roots | not touched |
| Systemd | server-owned unit files | backed up, not changed |

## Package Boundary

The deployed package contained code-only paths:

- `admin/v7-admin-api`
- `admin_core/*`
- `tools/runtime-support/*`
- selected `tools/v7-*`

It did not contain runtime registries, runtime state files, logs, secrets, client profiles, or private configs.

## Verdicts

- truth_source_audit_complete=true
- code_truth_source=GitHub_v7_next
- runtime_truth_source=server_opt_v7_egress_state
- runtime_truth_replaced=false
- secrets_replaced=false
- logs_replaced=false
