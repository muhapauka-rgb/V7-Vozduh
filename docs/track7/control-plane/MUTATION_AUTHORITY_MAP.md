# Mutation Authority Map

| Layer | Tool | Can mutate runtime? | Blast radius | Needs approval? | Needs rollback? |
|---|---|---:|---|---:|---:|
| Trusted RU diagnostic | `v7-trusted-ru-diagnostic` | Yes | Trusted RU diagnostic state; live probes | Yes | State cleanup/staleness plan |
| Trusted RU decision | `v7-trusted-ru-decision --write-state` | Yes | Trusted RU decision state | Yes | State restore/remove plan |
| Trusted RU refresh | `v7-trusted-ru-refresh-missing` | Yes | Diagnostic + decision state, live probes | Yes | State restore/staleness plan |
| Direct/RU add/remove | `v7-direct-add-domain`, `v7-direct-remove-domain` | Yes | Direct/RU domain policy, dnsmasq | Yes | Config backup restore |
| Direct/RU auto-sync | `v7-direct-auto-sync` | Yes | Direct/RU config, dnsmasq, autosync state | Yes | Config backup restore |
| Policy resolve | `v7-policy-resolve` | Yes | `route-classes.state` | Yes | State backup/restore |
| Policy apply preview | `v7-policy-apply --apply` | Yes | Preview state + audit only; live marks blocked | Yes | Preview state cleanup |
| Policy apply systemd | `v7-policy-apply-systemd --apply` | Yes | systemd service loops, restarts health/benchmark | Yes | Service file backups |
| Routing sync | `v7-routing-sync` | Yes | All enabled users in `users.registry` | Yes | Registry backup and per-user canary |
| User switch | `v7-user-switch` | Yes | One user per invocation | Yes | Switch back to previous egress |
| Autoswitch | `v7-users-autoswitch --apply` | Yes | Bounded selected users; can be broad if policy allows | Yes | Auto rollback per failed verification plus manual rollback |
| Proxy runtime apply | `v7-proxy-runtime-guard-apply` | Yes | nft output guard and runtime user | Yes | `v7-proxy-runtime-guard-rollback` |
| Kill switch rebuild | `v7-killswitch-enable` | Yes | Entire datapath leak guard table, NAT, direct mark rule | Yes | Known-good ruleset backup required |
| Kill switch disable | `v7-killswitch-disable-temporary` | Yes | Entire leak guard disabled | Owner-only emergency | Immediate re-enable |
| Generic rollback | `v7-rollback-last-change --apply` | Yes | Latest matching backup target; uncertain target class | Owner-only | Pre-rollback backup |
| Policy rollback | `v7-policy-live-rollback` | Placeholder | None currently; blocked placeholder | Yes before future use | Fixed backup argument |
| Proxy rollback | `v7-proxy-runtime-guard-rollback` | Yes | Restores nft ruleset; may delete runtime user | Yes | Backup dir validation |

## Highest-Risk Authority

1. `v7-killswitch-enable` / `v7-killswitch-disable-temporary`
2. `v7-routing-sync`
3. `v7-users-autoswitch --apply`
4. `v7-user-switch`
5. `v7-policy-apply-systemd --apply`
6. `v7-proxy-runtime-guard-apply`

