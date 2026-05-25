# Mutation Freeze Boundaries

This table defines what is allowed during a future quiet window. It does not execute the window.

| Tool / Action | Allowed During Quiet Window? | Reason |
|---|---|---|
| `v7-users-autoswitch --apply` | forbidden | can move users and invalidate attribution |
| `v7-users-autoswitch` dry-run against production paths | forbidden | can write load/reconnect observation state |
| `v7-users-autoswitch` fixture/local dry-run | allowed | no production state writes |
| `v7-user-switch <approved-user> <target>` | conditional | only as the named canary mutation |
| `v7-user-switch` for any other user | forbidden | expands blast radius |
| `v7-routing-sync` | forbidden | registry-wide route/rule mutation |
| admin `/api/actions/autoswitch-apply-guarded` | forbidden | can move selected users |
| admin `/api/actions/autoswitch-dry-run` | forbidden | production planner may write summaries |
| admin `/api/actions/user-switch` | conditional | only if it is the approved canary path |
| policy apply | forbidden | can change route class/policy state |
| Direct/RU mutation | forbidden | can affect route classes and policy decisions |
| Trusted RU refresh/decision execution | forbidden | can probe/write sensitive decision state |
| proxy runtime apply/guard apply | forbidden | can change public/proxy runtime behavior |
| kill switch rebuild/enable/disable | forbidden | whole datapath risk |
| rollback apply for approved canary | conditional | only if rollback criteria trigger |
| generic rollback tools | forbidden | broad restore blast radius |
| `v7-killswitch-check` | allowed | read-only safety check |
| `v7-user-route-check` | allowed | read-only route check |
| `v7-provisioning-reconcile-check` | allowed | read-only reconcile check |
| `ip -4 rule show` / `ip -4 route show` | allowed | read-only inspection |
| `tools/v7-route-movement-preview` | allowed | non-mutating local/fixture preview |

## Boundary Rule

If a command writes production state, starts/stops services, changes route/rule/nft/WG/proxy state, or can move a user other than the approved candidate, it is outside the quiet window.
