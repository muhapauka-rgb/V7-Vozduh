# Autoswitch Authority Map

This is governance-only analysis. No autoswitch process, timer, service, user switch, routing sync, or admin action was executed.

## Authority Surfaces

| Surface | Can move users? | Writes state? | Requires apply? | Canary interference | Blast radius |
|---|---:|---:|---:|---|---|
| `v7-users-autoswitch --apply` | yes, through `v7-user-switch` | yes | yes | direct | bounded by policy per run, repeated by timer |
| `v7-users-autoswitch` without `--apply` | no direct move | yes, load/reconnect summaries can update | no | yes, changes observation state | state layer only, but global signal |
| `v7-users-autoswitch.timer` | yes indirectly | yes indirectly | service has `--apply` | direct | repeated every timer cadence |
| `v7-users-autoswitch.service` | yes | yes | unit ExecStart includes `--apply` | direct | selected users per run |
| Admin `/api/actions/autoswitch-apply-guarded` | yes | yes | requires confirm `AUTOSWITCH` | direct | selected users, target-scoped optional |
| Admin `/api/actions/autoswitch-dry-run` | no direct move | yes, because planner can write summaries | no | yes, can alter observation state | signal layer |
| Admin `/api/actions/user-switch` | yes | yes | direct action | direct | one user plus proxy runtime side effects |
| Channel autoswitch UI action | yes, via apply endpoint | yes | confirm path | direct | target-scoped selected users |
| Telegram sentinel | no in repo-side unit with `--no-autoswitch` | yes, sentinel/matrix/event state | no | advisory/direct signal | egress scoring and downstream decisions |
| Client reconnect observation | no direct move | yes, reconnect state | no | advisory/direct signal | can create reconnect rotation candidates |
| Load/rebalance logic | yes when applied | yes | yes for movement | direct | bounded by rebalance limits |
| Failover logic | yes when applied | yes | yes for movement | direct | bounded by failover limits |
| Policy settings UI | not immediately, but changes limits/mode | yes | later apply/timer uses it | indirect | can change future blast radius |

## Decision Chain

```text
quality/load/sentinel/reconnect state
  -> v7-users-autoswitch planner
  -> selected_moves
  -> --apply
  -> v7-user-switch
  -> user registry/assignment/route table/proxy runtime side effects
```

## Current Authority Risk

The systemd service declares:

```text
ExecStart=/usr/local/bin/v7-users-autoswitch --apply
```

The timer cadence is short. That makes the control plane non-quiet for canary attribution unless timer authority is explicitly held under a separately approved operation.

## Quiet-Window Implication

A future quiet window must block user movement and state-writing planners that can change canary observations. Read-only checks are allowed; autoswitch planning via the production tool is not quiet because it can write load/reconnect state even without `--apply`.
