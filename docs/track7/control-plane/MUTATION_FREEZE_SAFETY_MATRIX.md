# Mutation Freeze Safety Matrix

| Action | Allowed During Rehearsal? | Allowed During Canary? | Reason |
|---|---|---|---|
| stop `v7-users-autoswitch.timer` | conditional | conditional | rehearsal/canary hold only after approval |
| start `v7-users-autoswitch.timer` restore | conditional | conditional | restore exact prior authority |
| disable/mask autoswitch timer | no | no | broader persistence change than rehearsal needs |
| restart autoswitch service | no | no | could execute apply path |
| `v7-users-autoswitch --apply` | no | no | moves users |
| production autoswitch dry-run | no | no | may write load/reconnect state |
| fixture autoswitch analysis | yes | yes | no production state |
| `v7-user-switch` | no | conditional | canary only for approved user |
| `v7-routing-sync` | no | no | registry-wide route/rule mutation |
| policy apply | no | no | route/policy mutation |
| Trusted RU refresh/decision | no | no | sensitive probe/state write |
| proxy apply | no | no | proxy runtime mutation |
| kill switch rebuild | no | no | whole datapath mutation |
| rollback apply | no | conditional | only approved canary rollback |
| `ip -4 rule show` | yes | yes | read-only inspection |
| `ip -4 route show table all` | yes | yes | read-only inspection |
| `v7-reconcile-check` | yes | yes | read-only check in this governance context |
| `v7-user-route-check` | yes | yes | read-only check |
| `v7-killswitch-check` | yes | yes | read-only check |
| `v7-provisioning-reconcile-check` | yes | yes | read-only check |
| `tools/v7-route-movement-preview` | yes | yes | non-mutating preview |

## Rule

Rehearsal allows only the autoswitch hold/restore mutation. Canary allows only the approved one-user switch and its rollback. Everything else remains frozen.
