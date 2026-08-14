# Program A Duplication Audit

Scope: discover possible alternate execution, rollback, audit, closure, and governance paths before any live runtime action.

## Canonical runtime owner

- `tools/v7-users-autoswitch`
- Runtime owner role: planner, selected move creation, apply owner, internal verification, terminal audit reference, closure target creation.
- Runtime mutation path inside the tool: `_run_switch()` invokes `v7-user-switch` with `V7_SWITCH_REASON=autoswitch_<reason>`.
- Program A rule: forward execution must use `tools/v7-users-autoswitch` only.

## Canonical audit owner

- `tools/v7-users-autoswitch` prepares terminal audit action `runtime_operation_terminal`.
- Audit emission uses `v7-audit-log` only when `--apply` is used.
- Dry-run audit status remains `ready_not_emitted_dry_run`.

## Canonical closure owner

- `admin/v7-admin-api`
- Closure store: `/opt/v7/egress/state/closure-records.jsonl`.
- Closure action: `closure_set_response()` appends closure records and emits `admin_action_closure_set`.
- Autoswitch closure target uses object type `runtime` and object id `operation_id`.

## Alternate or bypass-capable paths found

| Path | Capability | Classification | Program A handling |
| --- | --- | --- | --- |
| `v7-user-switch` | Direct user movement | Bypass-capable low-level primitive | Do not call directly for forward execution. Only allowed when invoked by canonical owner. |
| `admin/v7-admin-api` `/api/actions/user-switch` | Admin user switch action | Alternate execution path | Do not use for Program A movement. |
| `admin/v7-admin-api` `/api/actions/autoswitch-apply-guarded` | Admin-triggered autoswitch apply | Alternate entrypoint into autoswitch | Do not use unless explicitly scoped by a later program. |
| `admin/v7-admin-api` `/api/actions/rollback-apply` | Admin rollback action | Alternate rollback path | Do not use in Program A without a fresh canonical rollback packet. |
| Historical reports with `v7-user-switch <ip> <target>` | Prior manual movement/rollback precedent | Legacy evidence, not authority | Treat as historical only. |
| `tools/runtime-support/v7-rollback-last-change` and related support tools | Runtime support rollback helpers | Support/legacy rollback material | Do not execute in Program A. |
| `tools/runtime-support/v7-policy-live-rollback` | Policy live rollback | Different authority domain | Out of scope; do not execute. |
| `tools/runtime-support/v7-direct-auto-sync` | Direct sync support | Potential mutation path | Out of scope; do not execute. |
| `tools/runtime-support/v7-proxy-runtime-guard-rollback` | Proxy runtime guard rollback | Different authority domain | Out of scope; do not execute. |

## Duplication risk verdict

- Duplicate authority risk: MEDIUM.
- Duplicate execution path risk: HIGH if operators use direct/admin/manual entrypoints instead of the canonical Program A owner.
- Duplicate state writer risk: MEDIUM because closure, audit, routing, and support tools each write different state families.
- Program A mitigation: fail closed and refuse all bypass-capable paths.

## Conclusion

Program A must not use direct `v7-user-switch`, admin movement endpoints, policy rollback tools, or support rollback helpers. The only acceptable movement owner for this program is `tools/v7-users-autoswitch`; the only acceptable closure owner is `admin/v7-admin-api`; the only acceptable terminal runtime audit path is `v7-audit-log` invoked by the canonical runtime owner during apply.
