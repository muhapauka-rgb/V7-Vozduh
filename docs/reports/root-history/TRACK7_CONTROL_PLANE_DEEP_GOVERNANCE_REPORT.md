# V7 Vozduh Track 7 Control Plane Deep Governance Report

## Scope

This block audited the V7 control-plane nervous system by static/read-only inspection only. No Trusted RU refresh, Trusted RU diagnostic, routing-sync, user-switch, autoswitch apply, policy apply, proxy runtime apply, kill-switch mutation, service restart, chmod/chown, delete/archive, deploy, or live runtime mutation was performed.

## 1. What Was Analyzed

Control-plane layers:

```text
Trusted RU decision / refresh
routing-sync
user-switch
autoswitch
policy resolve / policy apply influence chain
proxy runtime guard apply
kill switch rebuild / disable
rollback tools
admin API action bindings
systemd autoswitch binding
```

Created governance docs:

```text
docs/track7/control-plane/TRUSTED_RU_DECISION_GOVERNANCE.md
docs/track7/control-plane/ROUTING_SYNC_GOVERNANCE.md
docs/track7/control-plane/USER_SWITCH_GOVERNANCE.md
docs/track7/control-plane/AUTOSWITCH_GOVERNANCE.md
docs/track7/control-plane/MUTATION_AUTHORITY_MAP.md
docs/track7/control-plane/SAFE_EXECUTION_MODEL.md
docs/track7/control-plane/CONTROL_PLANE_TEST_PLAN.md
```

Created checker:

```text
tools/v7-control-plane-governance-check
```

## 2. High-Risk Tools Remaining

High-risk tools are not necessarily unresolved, but they remain execution-sensitive:

```text
v7-killswitch-enable
v7-killswitch-disable-temporary
v7-routing-sync
v7-user-switch
v7-users-autoswitch --apply
v7-policy-resolve
v7-policy-apply --apply
v7-policy-apply-systemd --apply
v7-proxy-runtime-guard-apply
v7-trusted-ru-diagnostic
v7-trusted-ru-decision --write-state
v7-trusted-ru-refresh-missing
v7-rollback-last-change --apply
v7-proxy-runtime-guard-rollback
```

## 3. Tools That Can Mutate Runtime

| Tool | Mutation |
|---|---|
| `v7-trusted-ru-diagnostic` | Probes Trusted RU/Gosuslugi domains and writes diagnostic state |
| `v7-trusted-ru-decision --write-state` | Writes Trusted RU decision state |
| `v7-trusted-ru-refresh-missing` | Calls diagnostic, writes diagnostic/decision state |
| `v7-policy-resolve` | Writes `route-classes.state` |
| `v7-policy-apply --apply` | Writes policy preview state, JSON state, audit; live marks blocked |
| `v7-policy-apply-systemd --apply` | Rewrites service files, daemon-reload, restarts health/benchmark |
| `v7-routing-sync` | Replaces per-user route tables and `ip rule`s for all enabled users |
| `v7-user-switch` | Changes one user's route table and registry assignment |
| `v7-users-autoswitch --apply` | Calls `v7-user-switch` for selected users and writes safety state |
| `v7-proxy-runtime-guard-apply` | Adds nft output guard rules and may create runtime user |
| `v7-killswitch-enable` | Rebuilds nft kill-switch table, NAT, direct mark rule/table |
| `v7-killswitch-disable-temporary` | Removes kill-switch table and direct table/rule |
| `v7-rollback-last-change --apply` | Restores latest backup across broad target classes |

Important nuance: `v7-users-autoswitch` can write load/reconnect state even without `--apply`. That means "dry-run" is not automatically no-write.

## 4. Largest Blast Radius

| Rank | Tool | Blast Radius |
|---:|---|---|
| 1 | `v7-killswitch-enable` / disable | Entire datapath leak guard, NAT, Direct/RU marking |
| 2 | `v7-routing-sync` | Every enabled user in `users.registry` |
| 3 | `v7-users-autoswitch --apply` | Bounded selected users, but can become broad if policy limits are loose |
| 4 | `v7-policy-apply-systemd --apply` | Health/benchmark service behavior and restarts |
| 5 | `v7-proxy-runtime-guard-apply` | Proxy runtime nft output guard and runtime user |
| 6 | `v7-trusted-ru-refresh-missing` | Trusted RU/Gosuslugi probes and state that can influence downstream decisions |

## 5. Where Rollback Is Understandable

| Area | Rollback Model |
|---|---|
| User switch | Switch same user back to previous egress |
| Autoswitch | Auto rollback on failed route verify plus manual per-user switch-back |
| Proxy runtime guard | `v7-proxy-runtime-guard-rollback --backup-dir ... --confirm ...` |
| Direct/RU add/remove | Restore config backup and rerender/restart with approval |
| Generic backup | `v7-rollback-last-change --apply`, but only after target review |

## 6. Where Rollback Is Not Yet Clear Enough

| Area | Gap |
|---|---|
| `v7-routing-sync` | No built-in dry-run or registry snapshot/route diff rollback contract |
| Kill switch rebuild | Needs explicit known-good ruleset backup/restore plan before mutation |
| Trusted RU refresh | Needs stale-state and diagnostic-state rollback model |
| Policy resolve/apply chain | Needs route-class state snapshot and downstream consumer map |
| Autoswitch timer apply | Needs policy-bound blast-radius guarantee and current timer authority review |

## 7. Where Canary Is Required

Canary is required for:

- any user movement beyond one manual switch;
- autoswitch apply;
- any routing-sync after registry changes;
- any policy/routing change that may alter user traffic path;
- Trusted RU decision state used to influence routing policy.

Minimum canary:

```text
one user
known previous egress
verified target egress
kill switch OK before
route check after
kill switch OK after
rollback to previous egress ready
```

## 8. Manual Approval Required

Manual approval is required for all runtime mutations listed in this report. Owner-level approval is required for:

- kill switch disable/rebuild;
- proxy runtime guard apply/rollback;
- generic rollback apply;
- routing-sync;
- autoswitch apply;
- policy apply systemd;
- Trusted RU refresh/diagnostic execution.

## 9. Strictly Forbidden Until Separate Approval

```text
v7-trusted-ru-diagnostic
v7-trusted-ru-refresh-missing
v7-trusted-ru-decision --write-state
v7-routing-sync
v7-user-switch
v7-users-autoswitch --apply
v7-policy-resolve
v7-policy-apply --apply
v7-policy-apply-systemd --apply
v7-proxy-runtime-guard-apply
v7-killswitch-enable
v7-killswitch-disable-temporary
v7-rollback-last-change --apply
```

## 10. Key Answers

Who decides where user traffic should go?

- Policy/registry state, service matrix, egress health, quality/load summaries, org policy, Trusted RU state, and autoswitch scoring decide recommendations.

Who applies that decision?

- `v7-user-switch` applies one-user movement.
- `v7-routing-sync` applies registry-wide routing.
- `v7-policy-apply` currently writes preview state only for live marks, with live marks blocked.
- Kill switch tools apply datapath guard rules.

Who can move users?

- `v7-user-switch` directly.
- `v7-users-autoswitch --apply` indirectly through `v7-user-switch`.
- Admin API actions can call both under role/confirmation gates.

Who can change routes?

- `v7-routing-sync`.
- `v7-user-switch`.
- `v7-killswitch-enable`.
- Future policy live marks if enabled in a later build.

Who can affect Gosuslugi / Trusted RU?

- `v7-trusted-ru-diagnostic`, `v7-trusted-ru-decision`, `v7-trusted-ru-refresh-missing`.
- `v7-policy-resolve` via `TRUSTED_RU_SENSITIVE` route class state.
- Downstream policy/routing consumers if they use Trusted RU state.

Where can too many users move?

- Autoswitch failover/reconnect/rebalance/planned limits.
- `v7-routing-sync` if registry contains broad changed assignments.

Where can kill switch break?

- `v7-killswitch-enable` rebuilds the full nft table.
- `v7-killswitch-disable-temporary` removes it.
- Routing sync/user switch can create routes that rely on kill switch to prevent direct leaks.
- Proxy runtime guard apply modifies nft output rules.

## 11. Recommended Next 3 Steps

1. Create fixture/static tests for `v7-routing-sync` and `v7-user-switch` parsing/planning without touching live `ip route`.
2. Add a non-mutating route-change preview format for `routing-sync` and `user-switch`, then require it before any canary.
3. Formalize a one-user canary runbook with pre/post `v7-killswitch-check`, previous-egress capture, and explicit rollback command.

## Verification Summary

The block was verified with static/repo checks only. Live runtime actions remain unexecuted.

